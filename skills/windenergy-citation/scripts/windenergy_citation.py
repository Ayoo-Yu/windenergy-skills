#!/usr/bin/env python3
"""CrossRef citation helper and strict manuscript citation auditor."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote

import requests
from docx import Document

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CROSSREF_API = "https://api.crossref.org/works"
OPENALEX_API = "https://api.openalex.org/works"
ARXIV_API = "https://export.arxiv.org/api/query"
USER_AGENT = "windenergy-citation/1.0 (mailto:unknown@example.com)"
DOI_RE = re.compile(r"(?:doi:\s*|https?://(?:dx\.)?doi\.org/)?(10\.\d{4,9}/[^\s,;]+)", re.I)
ARXIV_DOI_RE = re.compile(r"10\.48550/arxiv\.([^/\s]+)", re.I)
CITATION_RE = re.compile(r"\[([0-9,\s\-\u2013\u2014]+)\]")
REFERENCE_HEADING_RE = re.compile(r"^\s*(references|reference)\s*$", re.I)
REFERENCE_MARKER_RE = re.compile(r"^\s*(?:\[(\d+)\]|(\d+)[.)])\s*(.*)$")


@dataclass
class ReferenceRecord:
    number: int
    raw: str = ""
    key: str = ""
    title: str = ""
    authors: str = ""
    year: str = ""
    journal: str = ""
    volume: str = ""
    pages: str = ""
    article_number: str = ""
    doi: str = ""
    source: str = "docx"
    status: str = "UNCHECKED"
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    verified: dict[str, Any] = field(default_factory=dict)


def clean_doi(value: str) -> str:
    value = value.strip().rstrip(".,;)")
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.I)
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    return value


def search_crossref(query: str, rows: int) -> list[dict]:
    resp = requests.get(
        CROSSREF_API,
        params={"query": query, "rows": rows, "filter": "type:journal-article"},
        headers={"User-Agent": USER_AGENT},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("message", {}).get("items", [])


def search_openalex(query: str, rows: int) -> list[dict]:
    resp = requests.get(
        OPENALEX_API,
        params={"search": query, "per-page": max(1, min(rows, 50)), "filter": "type:article"},
        headers={"User-Agent": USER_AGENT},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])


def get_by_doi(doi: str) -> dict:
    resp = requests.get(
        f"{CROSSREF_API}/{quote(clean_doi(doi), safe='/')}",
        headers={"User-Agent": USER_AGENT},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("message", {})


def get_arxiv_by_doi(doi: str) -> dict | None:
    match = ARXIV_DOI_RE.match(clean_doi(doi))
    if not match:
        return None
    arxiv_id = match.group(1)
    try:
        return get_arxiv_by_id_api(arxiv_id)
    except Exception:
        return get_arxiv_by_id_html(arxiv_id)


def get_arxiv_by_id_api(arxiv_id: str) -> dict | None:
    resp = requests.get(
        ARXIV_API,
        params={"id_list": arxiv_id},
        headers={"User-Agent": USER_AGENT},
        timeout=20,
    )
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    entry = root.find("atom:entry", ns)
    if entry is None:
        return None
    title_node = entry.find("atom:title", ns)
    published_node = entry.find("atom:published", ns)
    id_node = entry.find("atom:id", ns)
    authors_found = []
    for author in entry.findall("atom:author", ns):
        name_node = author.find("atom:name", ns)
        if name_node is not None and name_node.text:
            authors_found.append(" ".join(name_node.text.split()))
    arxiv_id = (id_node.text.rsplit("/", 1)[-1] if id_node is not None and id_node.text else arxiv_id)
    published = published_node.text if published_node is not None and published_node.text else ""
    return arxiv_record(arxiv_id, " ".join((title_node.text or "").split()) if title_node is not None else "", authors_found, published[:4])


def get_arxiv_by_id_html(arxiv_id: str) -> dict | None:
    resp = requests.get(
        f"https://arxiv.org/abs/{arxiv_id}",
        headers={"User-Agent": USER_AGENT},
        timeout=20,
    )
    resp.raise_for_status()
    text = resp.text
    metas: dict[str, list[str]] = {}
    for tag in re.findall(r"<meta\b[^>]*>", text, flags=re.I):
        name = re.search(r'\bname=["\']([^"\']+)["\']', tag, flags=re.I)
        content = re.search(r'\bcontent=["\']([^"\']*)["\']', tag, flags=re.I)
        if name and content:
            metas.setdefault(name.group(1).lower(), []).append(html.unescape(content.group(1)))
    title_value = (metas.get("citation_title") or [""])[0]
    authors_found = metas.get("citation_author", [])
    date_value = (metas.get("citation_date") or [""])[0]
    if not title_value:
        title_match = re.search(r"<title>\s*\[.*?\]\s*(.*?)\s*</title>", text, flags=re.I | re.S)
        title_value = html.unescape(re.sub(r"\s+", " ", title_match.group(1)).strip()) if title_match else ""
    if not title_value:
        return None
    return arxiv_record(arxiv_id, title_value, authors_found, date_value[:4])


def arxiv_record(arxiv_id: str, title_value: str, authors_found: list[str], year_value: str) -> dict:
    return {
        "title": " ".join(title_value.split()),
        "authors": authors_found,
        "year": year_value,
        "journal": "arXiv",
        "volume": "",
        "pages": "",
        "article_number": "",
        "doi": f"10.48550/arXiv.{arxiv_id}",
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "source": "arxiv",
    }


def authors(item: dict) -> list[str]:
    result = []
    for author in item.get("author", []):
        given = author.get("given", "")
        family = author.get("family", "")
        name = " ".join(part for part in [given, family] if part).strip()
        if name:
            result.append(name)
    return result


def year(item: dict) -> str:
    for key in ("published-print", "published-online", "published", "issued", "created"):
        parts = item.get(key, {}).get("date-parts")
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def title(item: dict) -> str:
    return (item.get("title") or [""])[0]


def journal(item: dict) -> str:
    return (item.get("container-title") or [""])[0]


def normalize(item: dict) -> dict:
    return {
        "title": title(item),
        "authors": authors(item),
        "year": year(item),
        "journal": journal(item),
        "volume": item.get("volume", ""),
        "pages": item.get("page", ""),
        "article_number": item.get("article-number", ""),
        "doi": item.get("DOI", ""),
        "url": item.get("URL", ""),
        "source": "crossref",
    }


def normalize_openalex(item: dict) -> dict:
    doi = (item.get("doi") or "").removeprefix("https://doi.org/")
    source = ((item.get("primary_location") or {}).get("source") or {}).get("display_name", "")
    return {
        "title": item.get("display_name", ""),
        "authors": [
            ((entry.get("author") or {}).get("display_name") or "").strip()
            for entry in item.get("authorships", [])[:8]
            if ((entry.get("author") or {}).get("display_name") or "").strip()
        ],
        "year": str(item.get("publication_year") or ""),
        "journal": source,
        "volume": "",
        "pages": "",
        "article_number": "",
        "doi": doi,
        "url": item.get("id") or "",
        "source": "openalex",
    }


def to_ris(records: list[dict]) -> str:
    blocks = []
    for rec in records:
        lines = ["TY  - JOUR"]
        for author in rec["authors"]:
            lines.append(f"AU  - {author}")
        lines.extend([
            f"TI  - {rec['title']}",
            f"PY  - {rec['year']}",
            f"JO  - {rec['journal']}",
            f"DO  - {rec['doi']}",
            f"UR  - {rec['url']}",
            "ER  -",
        ])
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + "\n"


def to_bib(records: list[dict]) -> str:
    entries = []
    for idx, rec in enumerate(records, 1):
        seed = (rec["authors"][0] if rec["authors"] else "ref") + rec["year"]
        key = re.sub(r"[^A-Za-z0-9]+", "", seed) or f"ref{idx}"
        entries.append(
            "@article{" + key + ",\n"
            f"  title = {{{rec['title']}}},\n"
            f"  author = {{{' and '.join(rec['authors'])}}},\n"
            f"  journal = {{{rec['journal']}}},\n"
            f"  year = {{{rec['year']}}},\n"
            f"  doi = {{{rec['doi']}}},\n"
            f"  url = {{{rec['url']}}}\n"
            "}"
        )
    return "\n\n".join(entries) + "\n"


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


def similarity(left: str, right: str) -> float:
    left_norm = normalize_text(left)
    right_norm = normalize_text(right)
    if not left_norm or not right_norm:
        return 0.0
    return SequenceMatcher(None, left_norm, right_norm).ratio()


def extract_doi(text: str) -> str:
    match = DOI_RE.search(text)
    return clean_doi(match.group(1)) if match else ""


def expand_citation_text(text: str) -> tuple[set[int], list[str]]:
    numbers: set[int] = set()
    malformed: list[str] = []
    for match in CITATION_RE.finditer(text):
        value = match.group(1)
        for token in [part.strip() for part in value.split(",") if part.strip()]:
            range_parts = re.split(r"\s*(?:-|\u2013|\u2014)\s*", token)
            if len(range_parts) == 1 and range_parts[0].isdigit():
                numbers.add(int(range_parts[0]))
            elif len(range_parts) == 2 and all(part.isdigit() for part in range_parts):
                start, end = int(range_parts[0]), int(range_parts[1])
                if start <= end:
                    numbers.update(range(start, end + 1))
                else:
                    malformed.append(match.group(0))
            else:
                malformed.append(match.group(0))
    return numbers, sorted(set(malformed))


def split_body_and_references(docx_path: Path) -> tuple[list[str], list[str]]:
    doc = Document(str(docx_path))
    paragraphs = [paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip()]
    ref_start = None
    for idx, text in enumerate(paragraphs):
        if REFERENCE_HEADING_RE.match(text):
            ref_start = idx
            break
    if ref_start is None:
        return paragraphs, []
    return paragraphs[:ref_start], paragraphs[ref_start + 1 :]


def extract_in_text_citations(docx_path: Path) -> dict[str, Any]:
    body, _references = split_body_and_references(docx_path)
    numbers, malformed = expand_citation_text("\n".join(body))
    return {"numbers": sorted(numbers), "malformed": malformed}


def parse_docx_references(docx_path: Path) -> list[ReferenceRecord]:
    _body, paragraphs = split_body_and_references(docx_path)
    records: list[ReferenceRecord] = []
    current_number = 0
    current_text = ""
    for text in paragraphs:
        marker = REFERENCE_MARKER_RE.match(text)
        if marker:
            if current_text:
                records.append(reference_from_text(current_number, current_text, "docx"))
            current_number = int(marker.group(1) or marker.group(2))
            current_text = marker.group(3).strip()
            continue
        if current_text:
            current_text += " " + text
        else:
            current_number += 1
            current_text = text
    if current_text:
        records.append(reference_from_text(current_number or len(records) + 1, current_text, "docx"))
    return records


def reference_from_text(number: int, text: str, source: str) -> ReferenceRecord:
    doi = extract_doi(text)
    years = re.findall(r"\b(?:19|20)\d{2}\b", text)
    year_value = years[-1] if years else ""
    title_value = ""
    quoted = re.findall(r'"([^"]{8,})"', text)
    if quoted:
        title_value = quoted[0]
    return ReferenceRecord(number=number, raw=text, year=year_value, title=title_value, doi=doi, source=source)


def split_bib_entries(text: str) -> list[str]:
    entries: list[str] = []
    idx = 0
    while True:
        start = text.find("@", idx)
        if start == -1:
            break
        brace = text.find("{", start)
        if brace == -1:
            break
        depth = 0
        end = brace
        while end < len(text):
            char = text[end]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    entries.append(text[start : end + 1])
                    idx = end + 1
                    break
            end += 1
        else:
            break
    return entries


def parse_bib_fields(entry: str) -> tuple[str, dict[str, str]]:
    header = re.match(r"@\w+\s*\{\s*([^,]+),", entry, re.S)
    key = header.group(1).strip() if header else ""
    body_start = header.end() if header else 0
    body = entry[body_start:].strip().rstrip("}")
    fields: dict[str, str] = {}
    idx = 0
    while idx < len(body):
        match = re.search(r"([A-Za-z][A-Za-z0-9_-]*)\s*=", body[idx:])
        if not match:
            break
        name = match.group(1).lower()
        value_start = idx + match.end()
        while value_start < len(body) and body[value_start].isspace():
            value_start += 1
        if value_start >= len(body):
            break
        opener = body[value_start]
        if opener == "{":
            depth = 0
            pos = value_start
            while pos < len(body):
                if body[pos] == "{":
                    depth += 1
                elif body[pos] == "}":
                    depth -= 1
                    if depth == 0:
                        fields[name] = body[value_start + 1 : pos].strip()
                        idx = pos + 1
                        break
                pos += 1
            else:
                break
        elif opener == '"':
            pos = value_start + 1
            while pos < len(body):
                if body[pos] == '"' and body[pos - 1] != "\\":
                    fields[name] = body[value_start + 1 : pos].strip()
                    idx = pos + 1
                    break
                pos += 1
            else:
                break
        else:
            pos = value_start
            while pos < len(body) and body[pos] != ",":
                pos += 1
            fields[name] = body[value_start:pos].strip()
            idx = pos + 1
    return key, {key: re.sub(r"\s+", " ", value) for key, value in fields.items()}


def parse_bib(path: Path) -> list[ReferenceRecord]:
    records: list[ReferenceRecord] = []
    for number, entry in enumerate(split_bib_entries(path.read_text(encoding="utf-8")), 1):
        key, fields = parse_bib_fields(entry)
        records.append(
            ReferenceRecord(
                number=number,
                key=key,
                title=fields.get("title", ""),
                authors=fields.get("author", ""),
                year=fields.get("year", ""),
                journal=fields.get("journal") or fields.get("journaltitle") or fields.get("booktitle", ""),
                volume=fields.get("volume", ""),
                pages=fields.get("pages", ""),
                article_number=fields.get("article-number") or fields.get("eid", ""),
                doi=clean_doi(fields.get("doi", "")) if fields.get("doi") else "",
                raw=entry,
                source="bib",
            )
        )
    return records


def compare_metadata(record: ReferenceRecord, metadata: dict[str, Any]) -> None:
    record.verified = metadata
    if record.title and metadata.get("title"):
        score = similarity(record.title, str(metadata["title"]))
        if score < 0.82:
            record.issues.append(f"title mismatch score {score:.2f}")
    if record.year and metadata.get("year") and str(record.year) != str(metadata["year"]):
        record.issues.append(f"year mismatch local={record.year} verified={metadata['year']}")
    if record.journal and metadata.get("journal"):
        local_journal = str(record.journal)
        verified_journal = str(metadata["journal"])
        if local_journal.lower().startswith("arxiv") and verified_journal.lower().startswith("arxiv"):
            score = 1.0
        else:
            score = similarity(local_journal, verified_journal)
        if score < 0.70:
            record.issues.append(f"journal mismatch score {score:.2f}")
    if record.volume and metadata.get("volume") and str(record.volume) != str(metadata["volume"]):
        record.issues.append(f"volume mismatch local={record.volume} verified={metadata['volume']}")
    verified_pages = metadata.get("pages") or metadata.get("article_number")
    local_pages = record.pages or record.article_number
    if local_pages and verified_pages and normalize_text(str(local_pages)) != normalize_text(str(verified_pages)):
        record.warnings.append(f"page or article number differs local={local_pages} verified={verified_pages}")


def best_title_match(
    record: ReferenceRecord,
    crossref_search: Callable[[str, int], list[dict]],
    openalex_search: Callable[[str, int], list[dict]],
) -> dict[str, Any] | None:
    if not record.title:
        return None
    candidates: list[dict[str, Any]] = []
    try:
        candidates.extend(normalize(item) for item in crossref_search(record.title, 5))
    except Exception as exc:
        record.warnings.append(f"CrossRef title search failed: {exc}")
    try:
        candidates.extend(normalize_openalex(item) for item in openalex_search(record.title, 5))
    except Exception as exc:
        record.warnings.append(f"OpenAlex title search failed: {exc}")
    if not candidates:
        return None
    scored = [(similarity(record.title, str(item.get("title", ""))), item) for item in candidates]
    scored.sort(key=lambda item: item[0], reverse=True)
    score, metadata = scored[0]
    metadata["title_match_score"] = round(score, 3)
    return metadata if score >= 0.90 else None


def audit_references(
    manuscript: Path,
    bib: Path | None = None,
    doi_lookup: Callable[[str], dict] = get_by_doi,
    crossref_search: Callable[[str, int], list[dict]] = search_crossref,
    openalex_search: Callable[[str, int], list[dict]] = search_openalex,
) -> dict[str, Any]:
    citation_info = extract_in_text_citations(manuscript)
    references = parse_bib(bib) if bib else parse_docx_references(manuscript)
    cited_numbers = set(citation_info["numbers"])
    reference_numbers = {record.number for record in references}
    missing_references = sorted(cited_numbers - reference_numbers)
    duplicate_dois = sorted(
        doi
        for doi, count in {
            clean_doi(record.doi).lower(): sum(
                1 for item in references if clean_doi(item.doi).lower() == clean_doi(record.doi).lower()
            )
            for record in references
            if record.doi
        }.items()
        if count > 1
    )

    for record in references:
        if record.number not in cited_numbers:
            record.issues.append("reference is not cited in manuscript text")
        if record.doi:
            try:
                metadata = normalize(doi_lookup(record.doi))
                compare_metadata(record, metadata)
            except Exception as exc:
                record.warnings.append(f"DOI metadata lookup failed: {exc}")
                try:
                    metadata = get_arxiv_by_doi(record.doi)
                except Exception as arxiv_exc:
                    record.warnings.append(f"arXiv metadata lookup failed: {arxiv_exc}")
                    metadata = None
                if metadata:
                    compare_metadata(record, metadata)
                    record.warnings.append("verified by arXiv metadata after DOI lookup failure")
                else:
                    metadata = best_title_match(record, crossref_search, openalex_search)
                    if metadata:
                        compare_metadata(record, metadata)
                        record.warnings.append("verified by title search after DOI lookup failure")
                if metadata:
                    pass
                else:
                    record.issues.append("DOI metadata lookup failed and title metadata could not be verified")
                    record.status = "UNCHECKED"
                    continue
        else:
            record.warnings.append("missing DOI")
            metadata = best_title_match(record, crossref_search, openalex_search)
            if metadata:
                compare_metadata(record, metadata)
            else:
                record.issues.append("no DOI and title metadata could not be verified")
                record.status = "UNCHECKED"
                continue
        record.status = "FAIL" if record.issues else "PASS"

    for record in references:
        if record.doi and clean_doi(record.doi).lower() in duplicate_dois:
            record.status = "FAIL"
            record.issues.append("duplicate DOI in reference list")

    fail_count = sum(1 for record in references if record.status == "FAIL")
    unchecked_count = sum(1 for record in references if record.status == "UNCHECKED")
    manual_count = sum(1 for record in references if record.status == "MANUAL")
    if missing_references or citation_info["malformed"]:
        fail_count += len(missing_references) + len(citation_info["malformed"])
    strict_ready = fail_count == 0 and unchecked_count == 0
    return {
        "strict_ready": strict_ready,
        "overall_status": "PASS" if strict_ready else "FAIL",
        "manuscript": str(manuscript),
        "bib": str(bib) if bib else "",
        "in_text_citations": sorted(cited_numbers),
        "malformed_citations": citation_info["malformed"],
        "missing_references": missing_references,
        "uncited_references": [record.number for record in references if record.number not in cited_numbers],
        "duplicate_dois": duplicate_dois,
        "counts": {
            "references": len(references),
            "cited_numbers": len(cited_numbers),
            "pass": sum(1 for record in references if record.status == "PASS"),
            "fail": fail_count,
            "unchecked": unchecked_count,
            "manual": manual_count,
        },
        "references": [record_to_dict(record) for record in references],
    }


def record_to_dict(record: ReferenceRecord) -> dict[str, Any]:
    return {
        "number": record.number,
        "key": record.key,
        "source": record.source,
        "status": record.status,
        "title": record.title,
        "authors": record.authors,
        "year": record.year,
        "journal": record.journal,
        "volume": record.volume,
        "pages": record.pages,
        "article_number": record.article_number,
        "doi": record.doi,
        "issues": record.issues,
        "warnings": record.warnings,
        "verified": record.verified,
    }


def markdown_audit(report: dict[str, Any]) -> str:
    lines = [
        "# Citation Audit",
        "",
        f"Overall status: {report['overall_status']}",
        f"Strict ready: {report['strict_ready']}",
        f"References checked: {report['counts']['references']}",
        f"Failures: {report['counts']['fail']}",
        f"Unchecked: {report['counts']['unchecked']}",
        "",
        "| No. | Status | DOI | Title | Issues |",
        "|---|---|---|---|---|",
    ]
    for record in report["references"]:
        title_value = (record["title"] or record["verified"].get("title", ""))[:80]
        issues = "; ".join(record["issues"] or record["warnings"])
        lines.append(
            f"| {record['number']} | {record['status']} | {record['doi']} | "
            f"{title_value} | {issues} |"
        )
    if report["missing_references"]:
        lines.extend(["", f"Missing reference entries for citations: {report['missing_references']}"])
    if report["malformed_citations"]:
        lines.extend(["", f"Malformed citations: {report['malformed_citations']}"])
    if report["duplicate_dois"]:
        lines.extend(["", f"Duplicate DOIs: {report['duplicate_dois']}"])
    return "\n".join(lines) + "\n"


def write_audit_outputs(report: dict[str, Any], output: Path | None, markdown: Path | None) -> None:
    json_content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json_content, encoding="utf-8")
    else:
        print(json_content, end="")
    if markdown:
        markdown.parent.mkdir(parents=True, exist_ok=True)
        markdown.write_text(markdown_audit(report), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Search, export, or audit DOI-backed energy citations.")
    parser.add_argument("--query", help="CrossRef query")
    parser.add_argument("--doi", action="append", default=[], help="DOI to fetch; repeatable")
    parser.add_argument("--audit", type=Path, help="Manuscript .docx to audit")
    parser.add_argument("--bib", type=Path, help="Optional BibTeX reference list for audit")
    parser.add_argument("--markdown", type=Path, help="Optional Markdown audit output")
    parser.add_argument("--rows", type=int, default=5)
    parser.add_argument("--format", choices=["json", "ris", "bib"], default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.audit:
        report = audit_references(args.audit, args.bib)
        write_audit_outputs(report, args.output, args.markdown)
        return 0 if report["strict_ready"] else 1

    items = []
    for doi in args.doi:
        items.append(get_by_doi(doi))
    if args.query:
        items.extend(search_crossref(args.query, max(1, min(args.rows, 50))))

    records = [normalize(item) for item in items]
    if args.format == "ris":
        content = to_ris(records)
    elif args.format == "bib":
        content = to_bib(records)
    else:
        content = json.dumps(records, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
