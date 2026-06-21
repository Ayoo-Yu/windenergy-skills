"""从Crossref发现目标期刊候选文献DOI。"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from style_learning_lib import TOPIC_PROFILES


CROSSREF_WORKS_URL = "https://api.crossref.org/works"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Discover candidate article DOIs through Crossref metadata.")
    parser.add_argument("--journal", required=True, help="Target journal title.")
    parser.add_argument(
        "--query",
        action="append",
        required=True,
        help="Topic query. Repeat this option to combine several query seeds.",
    )
    parser.add_argument("--year-from", type=int, default=None, help="Inclusive start publication year.")
    parser.add_argument("--year-to", type=int, default=None, help="Inclusive end publication year.")
    parser.add_argument("--rows", type=int, default=100, help="Maximum candidates to write after filtering.")
    parser.add_argument("--per-query-rows", type=int, default=50, help="Rows requested from Crossref per query.")
    parser.add_argument("--max-pages", type=int, default=4, help="Maximum Crossref pages to inspect per query.")
    parser.add_argument("--issn", action="append", default=[], help="Target journal ISSN. Repeat if needed.")
    parser.add_argument(
        "--topic-profile",
        default="none",
        choices=["none", *sorted(TOPIC_PROFILES)],
        help="Optional metadata topic gate.",
    )
    parser.add_argument("--min-topic-score", type=int, default=None, help="Override topic score threshold.")
    parser.add_argument("--include-keyword", action="append", default=[], help="Extra include keyword.")
    parser.add_argument("--exclude-keyword", action="append", default=[], help="Extra exclude keyword.")
    parser.add_argument("--allow-related-journals", action="store_true", help="Keep non-exact container titles.")
    parser.add_argument("--mailto", default=os.getenv("CROSSREF_MAILTO"), help="Email for Crossref polite pool.")
    parser.add_argument("--sleep", type=float, default=0.2, help="Delay between Crossref calls.")
    parser.add_argument("--output", required=True, help="Output JSON file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    seen: set[str] = set()
    journal_issns = args.issn or resolve_journal_issns(args.journal, args.mailto)

    for query in args.query:
        for issn in journal_issns or [None]:
            try:
                for item in search_crossref(args, query, issn):
                    record = normalize_record(item, query)
                    if not args.allow_related_journals and not journal_matches(args.journal, record["journal"]):
                        continue
                    screen = topic_screen_metadata(
                        record,
                        item,
                        args.topic_profile,
                        args.min_topic_score,
                        args.include_keyword,
                        args.exclude_keyword,
                    )
                    if not screen["accepted"]:
                        continue
                    key = dedupe_key(record)
                    if key in seen:
                        continue
                    seen.add(key)
                    record["topic_screen"] = screen
                    records.append(record)
                    if len(records) >= args.rows:
                        break
            except requests.RequestException as exc:
                errors.append({"query": query, "issn": issn, "error": str(exc)})
            if len(records) >= args.rows:
                break
        if len(records) >= args.rows:
            break
        time.sleep(args.sleep)

    payload = {
        "source": "Crossref Works API",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "journal": args.journal,
        "queries": args.query,
        "filters": {
            "year_from": args.year_from,
            "year_to": args.year_to,
            "journal_issns": journal_issns,
            "topic_profile": args.topic_profile,
            "min_topic_score": args.min_topic_score,
            "include_keywords": args.include_keyword,
            "exclude_keywords": args.exclude_keyword,
            "allow_related_journals": args.allow_related_journals,
        },
        "count": len(records),
        "items": records,
        "errors": errors,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Candidates: {len(records)}")
    print(f"Output: {output}")
    if errors:
        print(f"Errors: {len(errors)}")
    return 0


def search_crossref(args: argparse.Namespace, query: str, issn: str | None) -> list[dict[str, Any]]:
    filters = ["type:journal-article"]
    if issn:
        filters.append(f"issn:{issn}")
    if args.year_from:
        filters.append(f"from-pub-date:{args.year_from}-01-01")
    if args.year_to:
        filters.append(f"until-pub-date:{args.year_to}-12-31")
    headers = {"User-Agent": user_agent(args.mailto)}
    rows = min(max(args.per_query_rows, 1), 100)
    records: list[dict[str, Any]] = []
    search_query = strip_journal_from_query(query, args.journal)
    for page in range(max(args.max_pages, 1)):
        params = {
            "query.title": search_query,
            "rows": rows,
            "offset": page * rows,
            "filter": ",".join(filters),
        }
        response = requests.get(CROSSREF_WORKS_URL, params=params, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        page_items = list(data.get("message", {}).get("items", []))
        records.extend(page_items)
        if len(page_items) < rows:
            break
        time.sleep(args.sleep)
    return records


def strip_journal_from_query(query: str, journal: str) -> str:
    cleaned = re.sub(re.escape(journal), " ", query, flags=re.I)
    return re.sub(r"\s+", " ", cleaned).strip() or query


def resolve_journal_issns(journal: str, mailto: str | None) -> list[str]:
    params = {"query": journal, "rows": 10}
    headers = {"User-Agent": user_agent(mailto)}
    response = requests.get("https://api.crossref.org/journals", params=params, headers=headers, timeout=60)
    response.raise_for_status()
    data = response.json()
    items = data.get("message", {}).get("items", [])
    exact: list[str] = []
    related: list[str] = []
    target = normalize_label(journal)
    for item in items:
        title = clean_text(item.get("title"))
        issns = [clean_text(value) for value in item.get("ISSN", []) if clean_text(value)]
        if normalize_label(title) == target:
            exact.extend(issns)
        elif target in normalize_label(title):
            related.extend(issns)
    return sorted(set(exact or related))


def normalize_record(item: dict[str, Any], source_query: str) -> dict[str, Any]:
    title = first_text(item.get("title"))
    journal = first_text(item.get("container-title"))
    doi = clean_text(item.get("DOI"))
    return {
        "title": title,
        "doi": doi,
        "year": publication_year(item),
        "journal": journal,
        "url": clean_text(item.get("URL")),
        "publisher": clean_text(item.get("publisher")),
        "type": clean_text(item.get("type")),
        "source_query": source_query,
    }


def topic_screen_metadata(
    record: dict[str, Any],
    raw_item: dict[str, Any],
    profile_name: str,
    min_score: int | None,
    include_keywords: list[str],
    exclude_keywords: list[str],
) -> dict[str, Any]:
    if profile_name == "none":
        return {"accepted": True, "profile": "none", "score": None, "reason": "topic_screen_disabled"}
    profile = TOPIC_PROFILES[profile_name]
    include = {name: list(values) for name, values in profile.get("include", {}).items()}
    if include_keywords:
        include.setdefault("custom", []).extend(include_keywords)
    exclude = list(profile.get("exclude", []))
    if exclude_keywords:
        exclude.extend(exclude_keywords)

    screened_text = " ".join(
        [
            record.get("title", ""),
            record.get("journal", ""),
            " ".join(clean_text(s) for s in raw_item.get("subject", []) if s),
            clean_abstract(raw_item.get("abstract")),
        ]
    ).lower()
    group_hits: dict[str, list[str]] = {}
    score = 0
    for group, terms in include.items():
        hits = sorted({term for term in terms if term.lower() in screened_text})
        group_hits[group] = hits
        score += len(hits) * (3 if group in profile.get("required_groups", []) else 1)
    exclude_hits = sorted({term for term in exclude if term.lower() in screened_text})
    score -= len(exclude_hits) * 4
    required_missing = [
        group for group in profile.get("required_groups", []) if not group_hits.get(group)
    ]
    threshold = min_score if min_score is not None else int(profile.get("min_score", 0))
    accepted = not required_missing and not exclude_hits and score >= threshold
    reason = "accepted" if accepted else "topic_mismatch"
    if required_missing:
        reason += ":missing_" + ",".join(required_missing)
    if exclude_hits:
        reason += ":excluded_" + ",".join(exclude_hits[:5])
    if score < threshold:
        reason += f":score_below_{threshold}"
    return {
        "accepted": accepted,
        "profile": profile_name,
        "score": score,
        "threshold": threshold,
        "required_missing": required_missing,
        "include_hits": group_hits,
        "exclude_hits": exclude_hits,
        "reason": reason,
    }


def journal_matches(target: str, actual: str) -> bool:
    return normalize_label(target) == normalize_label(actual)


def publication_year(item: dict[str, Any]) -> int | None:
    for key in ("published-print", "published-online", "published", "issued"):
        value = item.get(key, {})
        parts = value.get("date-parts") if isinstance(value, dict) else None
        if parts and parts[0]:
            year = parts[0][0]
            if isinstance(year, int):
                return year
    return None


def first_text(value: Any) -> str:
    if isinstance(value, list) and value:
        return clean_text(value[0])
    return clean_text(value)


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def clean_abstract(value: Any) -> str:
    text = clean_text(value)
    text = re.sub(r"<[^>]+>", " ", text)
    return clean_text(text)


def normalize_label(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def dedupe_key(record: dict[str, Any]) -> str:
    doi = record.get("doi")
    if doi:
        return f"doi:{doi.lower()}"
    return f"title:{normalize_label(record.get('title', ''))}"


def user_agent(mailto: str | None) -> str:
    base = "windenergy-style-learning/1.0"
    if mailto:
        return f"{base} (mailto:{mailto})"
    return base


if __name__ == "__main__":
    raise SystemExit(main())
