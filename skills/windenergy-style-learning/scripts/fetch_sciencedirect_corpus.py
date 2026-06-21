"""通过ScienceDirect API获取目标期刊语料。"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests


SEARCH_ENDPOINTS = [
    "https://api.elsevier.com/content/search/sciencedirect",
    "https://api.elsevier.com/content/search/scidir",
]

ARTICLE_ENDPOINTS = [
    ("pii", "https://api.elsevier.com/content/article/pii/{id}"),
    ("doi", "https://api.elsevier.com/content/article/doi/{id}"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch ScienceDirect metadata and entitled PDFs.")
    parser.add_argument("--journal", required=True, help="ScienceDirect source title.")
    parser.add_argument("--query", default="", help="Topic query for title, abstract, and keywords.")
    parser.add_argument("--candidate-json", default=None, help="Candidate JSON from discover_crossref_candidates.py.")
    parser.add_argument("--doi", action="append", default=[], help="Exact DOI to retrieve. May be repeated.")
    parser.add_argument("--year-from", type=int, default=None, help="Inclusive start year.")
    parser.add_argument("--year-to", type=int, default=None, help="Inclusive end year.")
    parser.add_argument("--max-results", type=int, default=20, help="Maximum records to collect.")
    parser.add_argument("--output", required=True, help="Output corpus directory.")
    parser.add_argument("--api-key-env", default=None, help="Environment variable containing the API key.")
    parser.add_argument("--api-key-file", default=None, help="Private text file containing the API key.")
    parser.add_argument("--download-pdf", action="store_true", help="Attempt entitled PDF downloads.")
    parser.add_argument("--download-full-text", action="store_true", help="Attempt ScienceDirect full-text downloads.")
    parser.add_argument(
        "--full-text-format",
        default="xml-text",
        choices=["xml-text", "plain"],
        help="Full-text retrieval mode. xml-text converts ScienceDirect XML to section-aware text.",
    )
    parser.add_argument("--min-full-text-bytes", type=int, default=5000, help="Minimum bytes for saved full text.")
    parser.add_argument("--sleep", type=float, default=0.2, help="Delay between article retrieval calls.")
    parser.add_argument("--allow-related-journals", action="store_true", help="Keep records from similarly named journals.")
    parser.add_argument("--include-corrections", action="store_true", help="Keep corrigenda, errata, and editorials.")
    parser.add_argument("--title-regex", default=None, help="Optional regex that titles must match after retrieval.")
    parser.add_argument("--max-search-pages", type=int, default=4, help="Maximum ScienceDirect result pages to inspect.")
    args = parser.parse_args()
    if not args.query and not args.candidate_json and not args.doi:
        parser.error("Provide --query, --candidate-json, or --doi.")
    return args


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    pdf_dir = output / "pdfs"
    pdf_dir.mkdir(exist_ok=True)
    text_dir = output / "fulltext"
    if args.download_full_text:
        text_dir.mkdir(exist_ok=True)
    needs_api_key = bool(args.download_pdf or args.download_full_text or args.query)
    api_key = read_api_key(args.api_key_env, args.api_key_file) if needs_api_key else ""
    query = build_query(args) if args.query else ""
    records, search_status = collect_records(api_key, args, query)
    records = filter_records(records, args)[: args.max_results]
    manifest = {
        "journal": args.journal,
        "query": args.query,
        "compiled_query": query,
        "candidate_json": args.candidate_json,
        "doi_count": len(args.doi),
        "max_results": args.max_results,
        "search_status": search_status,
        "records": [],
    }
    for index, record in enumerate(records, start=1):
        normalized = normalize_record(record)
        normalized["download"] = {"status": "not_requested"}
        normalized["full_text"] = {"status": "not_requested"}
        if args.download_pdf:
            normalized["download"] = download_pdf(api_key, normalized, pdf_dir, index)
            time.sleep(args.sleep)
        if args.download_full_text:
            normalized["full_text"] = download_full_text(
                api_key,
                normalized,
                text_dir,
                index,
                args.min_full_text_bytes,
                args.full_text_format,
            )
            time.sleep(args.sleep)
        manifest["records"].append(normalized)

    (output / "corpus_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Records: {len(manifest['records'])}")
    print(f"PDFs: {sum(1 for r in manifest['records'] if r['download'].get('status') == 'pdf_saved')}")
    print(f"Full text: {sum(1 for r in manifest['records'] if r.get('full_text', {}).get('status') == 'text_saved')}")
    print(f"Manifest: {output / 'corpus_manifest.json'}")
    return 0


def collect_records(
    api_key: str,
    args: argparse.Namespace,
    query: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if args.candidate_json or args.doi:
        records = candidate_records(args)
        status = {
            "method": "candidate_doi_queue",
            "candidate_json": args.candidate_json,
            "doi_count": len(args.doi),
            "records_found": len(records),
        }
        return records, status
    return search_records(api_key, args, query, args.max_results)


def read_api_key(env_name: str | None, key_file: str | None = None) -> str:
    if key_file:
        value = Path(key_file).read_text(encoding="utf-8").strip()
        if value:
            return value
    names = [env_name] if env_name else []
    names.extend(["SCIENCEDIRECT_API_KEY", "ELSEVIER_API_KEY", "X_ELS_APIKEY"])
    for name in names:
        if name and os.getenv(name):
            return os.environ[name]
    registry_value = read_windows_environment_key(names)
    if registry_value:
        return registry_value
    raise SystemExit("ScienceDirect API key not found in environment.")


def read_windows_environment_key(names: list[str | None]) -> str | None:
    # Codex进程可能看不到新添加的Windows环境变量，注册表回退只读变量值，不写入日志。
    if os.name != "nt":
        return None
    try:
        import winreg
    except ImportError:
        return None
    registry_paths = [
        (winreg.HKEY_CURRENT_USER, "Environment"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
    ]
    for raw_name in names:
        if not raw_name:
            continue
        for hive, path in registry_paths:
            try:
                with winreg.OpenKey(hive, path) as key:
                    value, _ = winreg.QueryValueEx(key, raw_name)
            except OSError:
                continue
            if value:
                return str(value)
    return None


def candidate_records(args: argparse.Namespace) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if args.candidate_json:
        path = Path(args.candidate_json)
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data.get("items") or data.get("records") or []
        if not isinstance(items, list):
            raise SystemExit("Candidate JSON must contain an items or records list.")
        for item in items:
            if isinstance(item, dict):
                records.append(candidate_record(item, args.journal))
    for doi in args.doi:
        records.append(candidate_record({"doi": doi}, args.journal))
    return dedupe_records(records)


def candidate_record(item: dict[str, Any], default_journal: str) -> dict[str, Any]:
    year = item.get("year") or item.get("publication_year")
    cover_date = str(year) if year else item.get("cover_date")
    return {
        "title": item.get("title") or item.get("dc:title"),
        "doi": item.get("doi") or item.get("DOI"),
        "pii": item.get("pii"),
        "journal": item.get("journal") or item.get("container-title") or default_journal,
        "cover_date": cover_date,
        "volume": item.get("volume"),
        "pages": item.get("pages"),
        "openaccess": item.get("openaccess") or item.get("openAccess"),
        "sciencedirect_link": item.get("sciencedirect_link") or item.get("url") or item.get("URL"),
        "api_link": item.get("api_link"),
        "candidate_source_query": item.get("source_query"),
    }


def dedupe_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped = []
    seen = set()
    for record in records:
        doi = str(record.get("doi") or "").strip().lower()
        title = str(record.get("title") or "").strip().lower()
        key = f"doi:{doi}" if doi else f"title:{title}"
        if key in seen:
            continue
        seen.add(key)
        deduped.append(record)
    return deduped


def build_query(args: argparse.Namespace) -> str:
    # 日期比较在部分ScienceDirect配置中会被拒绝，年份改为后处理过滤。
    parts = [f'srctitle("{args.journal}")', f"tak({topic_expression(args.query)})"]
    return " AND ".join(parts)


def search_records(
    api_key: str,
    args: argparse.Namespace,
    query: str,
    max_results: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    put_records, put_status = search_records_put(api_key, args, max_results)
    if put_records:
        return put_records, put_status
    get_records, get_status = search_records_get(api_key, query, max_results)
    if get_records:
        get_status["put_attempt"] = put_status
        return get_records, get_status
    return [], {"put_attempt": put_status, "get_attempt": get_status}


def search_records_put(
    api_key: str,
    args: argparse.Namespace,
    max_results: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    endpoint = SEARCH_ENDPOINTS[0]
    headers = {
        "X-ELS-APIKey": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    records: list[dict[str, Any]] = []
    errors = []
    results_found = None
    show = 25
    for page in range(max(args.max_search_pages, 1)):
        offset = page * show
        body = {
            "qs": args.query,
            "pub": args.journal,
            "display": {"offset": offset, "show": show, "sortBy": "date"},
        }
        response = requests.put(endpoint, headers=headers, json=body, timeout=60)
        if not response.ok:
            errors.append({"offset": offset, "http_status": response.status_code, "body_preview": response.text[:500]})
            break
        data = response.json()
        results_found = data.get("resultsFound")
        page_records = data.get("results", [])
        records.extend(page_records)
        if len(page_records) < show:
            break
        if len(records) >= max(max_results * 10, show):
            break
    status = {
        "method": "PUT",
        "endpoint": endpoint,
        "http_status": 200 if records else (errors[0]["http_status"] if errors else None),
        "content_type": "application/json;charset=UTF-8" if records else None,
        "payload": {"qs": args.query, "pub": args.journal, "show": show},
        "pages_inspected": math_ceil_div(len(records), show) if records else 0,
        "results_found": results_found,
    }
    if errors:
        status["errors"] = errors
    return records, status


def search_records_get(api_key: str, query: str, max_results: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    headers = {"X-ELS-APIKey": api_key, "Accept": "application/json"}
    params = {"query": query, "count": min(max_results, 25), "start": 0}
    errors = []
    for endpoint in SEARCH_ENDPOINTS:
        response = requests.get(endpoint, headers=headers, params=params, timeout=60)
        status = {
            "endpoint": endpoint,
            "http_status": response.status_code,
            "content_type": response.headers.get("content-type"),
        }
        if response.ok:
            data = response.json()
            entries = data.get("search-results", {}).get("entry", [])
            if isinstance(entries, dict):
                entries = [entries]
            return entries[:max_results], status
        status["body_preview"] = response.text[:500]
        errors.append(status)
    return [], {"errors": errors}


def topic_expression(query: str) -> str:
    # 保留用户已经写好的字段查询，只处理普通关键词串。
    raw = query.strip()
    if re.search(r"\b[A-Za-z-]+\s*\(", raw) or re.search(r"[()\"]", raw):
        return raw
    parts = re.split(r"\s+OR\s+", raw, flags=re.I)
    quoted = []
    for part in parts:
        item = part.strip()
        if not item:
            continue
        if item.startswith('"') and item.endswith('"'):
            quoted.append(item)
        elif re.search(r"\s", item):
            quoted.append(f'"{item}"')
        else:
            quoted.append(item)
    return " OR ".join(quoted) or raw


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    links = {}
    for link in as_list(record.get("link")):
        if isinstance(link, dict):
            key = link.get("@ref") or link.get("rel")
            href = link.get("@href") or link.get("href")
            if key and href:
                links[key] = href
    pages = record.get("pages")
    if isinstance(pages, dict):
        page_text = join_pages(pages.get("first"), pages.get("last"))
    else:
        page_text = join_pages(record.get("prism:startingPage"), record.get("prism:endingPage"))
    pii = record.get("pii")
    api_link = links.get("self") or record.get("prism:url")
    if not api_link and pii:
        api_link = f"https://api.elsevier.com/content/article/pii/{pii}"
    title = clean_label(record.get("dc:title") or record.get("title"))
    return {
        "title": title,
        "doi": record.get("prism:doi") or record.get("doi") or clean_doi(record.get("dc:identifier")),
        "pii": pii,
        "journal": record.get("prism:publicationName") or record.get("sourceTitle") or record.get("journal"),
        "cover_date": record.get("prism:coverDate") or record.get("publicationDate") or record.get("loadDate") or record.get("cover_date"),
        "volume": record.get("prism:volume") or record.get("volumeIssue") or record.get("volume"),
        "pages": page_text or record.get("pages") or "",
        "openaccess": record.get("openaccess") if "openaccess" in record else record.get("openAccess"),
        "sciencedirect_link": links.get("scidir") or record.get("uri") or record.get("sciencedirect_link"),
        "api_link": api_link,
        "candidate_source_query": record.get("candidate_source_query"),
    }


def filter_records(records: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    filtered = []
    for record in records:
        journal = str(record.get("prism:publicationName") or record.get("sourceTitle") or record.get("journal") or "")
        if not args.allow_related_journals and journal.casefold() != args.journal.casefold():
            continue
        title = str(record.get("dc:title") or record.get("title") or "")
        if not args.include_corrections and re.search(r"\b(corrigendum|erratum|editorial|commentary|preface)\b", title, re.I):
            continue
        if args.title_regex and not re.search(args.title_regex, title, re.I):
            continue
        date = str(record.get("prism:coverDate") or record.get("publicationDate") or record.get("loadDate") or record.get("cover_date") or record.get("year") or "")
        match = re.match(r"(\d{4})", str(date))
        if (args.year_from or args.year_to) and not match:
            continue
        if match:
            year = int(match.group(1))
            if args.year_from and year < args.year_from:
                continue
            if args.year_to and year > args.year_to:
                continue
        filtered.append(record)
    return filtered


def math_ceil_div(value: int, divisor: int) -> int:
    return (value + divisor - 1) // divisor


def download_pdf(api_key: str, record: dict[str, Any], pdf_dir: Path, index: int) -> dict[str, Any]:
    identifiers = []
    if record.get("pii"):
        identifiers.append(("pii", str(record["pii"])))
    if record.get("doi"):
        identifiers.append(("doi", str(record["doi"])))
    if not identifiers:
        return {"status": "no_identifier"}
    headers = {"X-ELS-APIKey": api_key, "Accept": "application/pdf"}
    attempts = []
    for kind, value in identifiers:
        for endpoint_kind, template in ARTICLE_ENDPOINTS:
            if endpoint_kind != kind:
                continue
            encoded = quote(value, safe="") if kind == "doi" else quote(value, safe="")
            url = template.format(id=encoded)
            response = requests.get(
                url,
                headers=headers,
                params={"httpAccept": "application/pdf"},
                timeout=90,
            )
            content_type = response.headers.get("content-type", "")
            attempt = {
                "kind": kind,
                "http_status": response.status_code,
                "content_type": content_type,
            }
            if response.ok and (response.content.startswith(b"%PDF") or "pdf" in content_type.lower()):
                filename = f"{index:03d}_{slug(record.get('title') or value)}.pdf"
                path = pdf_dir / filename
                path.write_bytes(response.content)
                attempt["path"] = str(path)
                attempt["bytes"] = len(response.content)
                attempt["status"] = "pdf_saved"
                return attempt
            attempt["body_preview"] = response.text[:300] if response.text else ""
            attempts.append(attempt)
    return {"status": "pdf_unavailable", "attempts": attempts}


def download_full_text(
    api_key: str,
    record: dict[str, Any],
    text_dir: Path,
    index: int,
    min_bytes: int,
    full_text_format: str,
) -> dict[str, Any]:
    identifiers = []
    if record.get("pii"):
        identifiers.append(("pii", str(record["pii"])))
    if record.get("doi"):
        identifiers.append(("doi", str(record["doi"])))
    if not identifiers:
        return {"status": "no_identifier"}
    accept = "text/xml" if full_text_format == "xml-text" else "text/plain"
    headers = {"X-ELS-APIKey": api_key, "Accept": accept}
    attempts = []
    for kind, value in identifiers:
        for endpoint_kind, template in ARTICLE_ENDPOINTS:
            if endpoint_kind != kind:
                continue
            encoded = quote(value, safe="")
            url = template.format(id=encoded)
            response = requests.get(
                url,
                headers=headers,
                params={"httpAccept": accept},
                timeout=90,
            )
            content_type = response.headers.get("content-type", "")
            text = full_text_response_text(response, full_text_format)
            attempt = {
                "kind": kind,
                "http_status": response.status_code,
                "content_type": content_type,
                "bytes": len(response.content),
                "format": full_text_format,
            }
            if response.ok and text and len(text.encode("utf-8")) >= min_bytes:
                filename = f"{index:03d}_{slug(record.get('title') or value)}.txt"
                path = text_dir / filename
                path.write_text(text, encoding="utf-8", errors="replace")
                attempt["path"] = str(path)
                attempt["status"] = "text_saved"
                return attempt
            attempt["body_preview"] = response.text[:300] if response.text else ""
            attempts.append(attempt)
    return {"status": "text_unavailable", "attempts": attempts}


def full_text_response_text(response: requests.Response, full_text_format: str) -> str:
    if not response.ok:
        return ""
    if full_text_format == "plain":
        content_type = response.headers.get("content-type", "").lower()
        if "text/plain" not in content_type:
            return ""
        return response.text
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError:
        return ""
    return sciencedirect_xml_to_text(root)


def sciencedirect_xml_to_text(root: ET.Element) -> str:
    pieces: list[str] = []

    def walk(element: ET.Element) -> None:
        tag = local_name(element.tag)
        if tag in {"cross-ref", "xref"}:
            rendered_ref = cross_reference_text(element)
            if rendered_ref:
                pieces.append(rendered_ref)
                return
        if tag in {"figure", "table-wrap"}:
            rendered_object = display_object_text(element, tag)
            if rendered_object:
                pieces.append(f"\n\n{rendered_object}\n\n")
                return
        if tag == "section-title":
            title = clean_whitespace(" ".join(element.itertext()))
            if title:
                pieces.append(f"\n\n{title}\n\n")
            return
        if tag == "abstract":
            pieces.append("\n\nAbstract\n\n")
        if tag in {"caption", "figure", "table-wrap"}:
            pieces.append("\n\n")
        if tag == "label":
            label = clean_whitespace(" ".join(element.itertext()))
            if re.fullmatch(r"(Fig\.?\s*\d+|Figure\s*\d+|Table\s*\d+)", label, re.I):
                pieces.append(f"\n\n{label} ")
                return
        if element.text:
            pieces.append(element.text)
        for child in element:
            walk(child)
            if child.tail:
                pieces.append(child.tail)
        if tag in {"para", "simple-para", "section", "caption", "title", "abstract"}:
            pieces.append("\n\n")

    article = original_text_article(root)
    if article is not None:
        head = first_child(article, "head")
        body = first_child(article, "body")
        floats = first_child(article, "floats")
        tail = first_child(article, "tail")
        if head is not None:
            for abstract in descendants(head, "abstract"):
                walk(abstract)
                break
            keyword_text = keyword_section_text(head)
            if keyword_text:
                pieces.append(f"\n\nKeywords\n\n{keyword_text}\n\n")
        if body is not None:
            walk(body)
        if floats is not None:
            pieces.append("\n\nFigure And Table Captions\n\n")
            walk(floats)
        if tail is not None:
            walk(tail)
    else:
        walk(root)
    text = "".join(pieces)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return clean_whitespace_lines(text)


def display_object_text(element: ET.Element, tag: str) -> str:
    label = display_object_label(element, tag)
    caption = display_object_caption(element)
    if label and caption:
        caption = re.sub(r"^" + re.escape(label) + r"\s*[\.:]?\s*", "", caption, flags=re.I)
        return clean_whitespace(f"{label}. {caption}")
    return clean_whitespace(caption or label or "")


def display_object_label(element: ET.Element, tag: str) -> str:
    kind = "figure" if tag == "figure" else "table"
    for label_element in descendants(element, "label"):
        label = clean_whitespace(" ".join(label_element.itertext()))
        normalized = normalize_display_label(label, kind)
        if normalized:
            return normalized
    element_id = " ".join(str(value) for value in element.attrib.values())
    match = re.search(r"(?:fig|f|table|tbl)[-_]?(\d+[A-Za-z]?)", element_id, re.I)
    if match:
        return f"Fig. {match.group(1)}" if kind == "figure" else f"Table {match.group(1)}"
    return ""


def display_object_caption(element: ET.Element) -> str:
    for caption in descendants(element, "caption"):
        text = element_text_without_tags(caption, {"label"})
        if text:
            return text
    return ""


def element_text_without_tags(element: ET.Element, skip_tags: set[str]) -> str:
    chunks: list[str] = []

    def collect(node: ET.Element) -> None:
        tag = local_name(node.tag)
        if tag not in skip_tags and node.text:
            chunks.append(node.text)
        for child in node:
            if local_name(child.tag) not in skip_tags:
                collect(child)
            if child.tail:
                chunks.append(child.tail)

    collect(element)
    return clean_whitespace(" ".join(chunks))


def normalize_display_label(label: str, kind: str) -> str:
    label = clean_whitespace(label).rstrip(".")
    if kind == "figure":
        if re.fullmatch(r"(?:Fig\.?|Figure)\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", label, re.I):
            number = re.search(r"\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", label).group(0)
            return f"Fig. {number}"
        if re.fullmatch(r"\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", label):
            return f"Fig. {label}"
    if kind == "table":
        if re.fullmatch(r"Table\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", label, re.I):
            number = re.search(r"\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", label).group(0)
            return f"Table {number}"
        if re.fullmatch(r"\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", label):
            return f"Table {label}"
    return ""


def cross_reference_text(element: ET.Element) -> str:
    raw = clean_whitespace(" ".join(element.itertext()))
    attrs = " ".join(str(value) for value in element.attrib.values()).lower()
    if is_figure_reference(raw, attrs):
        return normalize_cross_reference_label(raw, "Fig.")
    if is_table_reference(raw, attrs):
        return normalize_cross_reference_label(raw, "Table")
    return ""


def is_figure_reference(raw: str, attrs: str) -> bool:
    return bool(
        re.search(r"\b(?:Fig\.?|Figure)\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", raw, re.I)
        or re.search(r"\b(fig|figure)\b", attrs, re.I)
        or re.search(r"\b(?:fig|f)[-_]?\d+", attrs, re.I)
    )


def is_table_reference(raw: str, attrs: str) -> bool:
    return bool(
        re.search(r"\bTable\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", raw, re.I)
        or re.search(r"\b(table|tbl)\b", attrs, re.I)
        or re.search(r"\b(?:table|tbl)[-_]?\d+", attrs, re.I)
    )


def normalize_cross_reference_label(raw: str, prefix: str) -> str:
    raw = clean_whitespace(raw)
    if prefix == "Fig." and re.search(r"\b(?:Fig\.?|Figure)\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", raw, re.I):
        return raw
    if prefix == "Table" and re.search(r"\bTable\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", raw, re.I):
        return raw
    match = re.search(r"\d+[A-Za-z]?(?:\([A-Za-z0-9]+\))?", raw)
    if match:
        return f"{prefix} {match.group(0)}"
    return raw


def original_text_article(root: ET.Element) -> ET.Element | None:
    for element in root.iter():
        if local_name(element.tag) == "originaltext":
            for candidate in element.iter():
                if local_name(candidate.tag) == "article":
                    return candidate
    for candidate in root.iter():
        if local_name(candidate.tag) == "article":
            return candidate
    return None


def first_child(element: ET.Element, name: str) -> ET.Element | None:
    for child in element:
        if local_name(child.tag) == name:
            return child
    return None


def descendants(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in element.iter() if local_name(child.tag) == name]


def keyword_section_text(head: ET.Element) -> str:
    chunks = []
    for keywords in descendants(head, "keywords"):
        text = clean_whitespace(" ".join(keywords.itertext()))
        text = re.sub(r"^Keywords\s*", "", text, flags=re.I).strip()
        if text:
            chunks.append(text)
    return "; ".join(dict.fromkeys(chunks))


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].rsplit(":", 1)[-1].lower()


def clean_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def clean_whitespace_lines(value: str) -> str:
    lines = [clean_whitespace(line) for line in value.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def clean_doi(identifier: Any) -> str | None:
    if isinstance(identifier, str) and identifier.lower().startswith("doi:"):
        return identifier[4:]
    return identifier if isinstance(identifier, str) else None


def join_pages(start: str | None, end: str | None) -> str:
    if start and end:
        return f"{start}-{end}"
    return start or end or ""


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return (value[:80] or "article").strip("-")


def clean_label(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).replace("\u2014", "-").replace("\u2013", "-")


if __name__ == "__main__":
    raise SystemExit(main())
