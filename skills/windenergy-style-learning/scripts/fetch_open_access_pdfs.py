"""从开放获取元数据源下载候选DOI的合法PDF。"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests


OPENALEX_WORK_URL = "https://api.openalex.org/works/doi:{doi}"
UNPAYWALL_WORK_URL = "https://api.unpaywall.org/v2/{doi}"


DEFAULT_LANDING_HOSTS = {
    "arxiv.org",
    "biorxiv.org",
    "medrxiv.org",
    "osti.gov",
    "www.osti.gov",
    "pmc.ncbi.nlm.nih.gov",
    "europepmc.org",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download open-access PDFs for DOI candidates.")
    parser.add_argument("--candidate-json", required=True, help="Candidate JSON from discover_crossref_candidates.py.")
    parser.add_argument("--output", required=True, help="Output corpus directory.")
    parser.add_argument("--max-results", type=int, default=80, help="Maximum DOI candidates to inspect.")
    parser.add_argument("--sleep", type=float, default=0.25, help="Delay between metadata requests.")
    parser.add_argument("--timeout", type=float, default=45, help="HTTP timeout in seconds.")
    parser.add_argument("--min-pdf-bytes", type=int, default=50_000, help="Minimum bytes for a saved PDF.")
    parser.add_argument("--openalex-mailto", default=os.getenv("OPENALEX_MAILTO"), help="Optional email for OpenAlex.")
    parser.add_argument("--unpaywall-email", default=os.getenv("UNPAYWALL_EMAIL"), help="Optional email for Unpaywall.")
    parser.add_argument("--allow-landing-probe", action="store_true", help="Probe trusted OA landing pages for PDF links.")
    parser.add_argument(
        "--allowed-landing-host",
        action="append",
        default=[],
        help="Extra landing host allowed for PDF-link probing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    pdf_dir = output / "pdfs"
    output.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(exist_ok=True)

    candidates = load_candidates(Path(args.candidate_json))[: args.max_results]
    manifest: dict[str, Any] = {
        "source": "open_access_pdf_discovery",
        "candidate_json": args.candidate_json,
        "max_results": args.max_results,
        "records": [],
    }
    session = requests.Session()
    headers = {"User-Agent": user_agent(args.openalex_mailto or args.unpaywall_email)}

    for index, candidate in enumerate(candidates, start=1):
        record = {
            "title": candidate.get("title"),
            "doi": candidate.get("doi"),
            "journal": candidate.get("journal"),
            "year": candidate.get("year"),
            "open_access": {},
            "pdf_candidates": [],
            "download": {"status": "not_attempted"},
        }
        doi = str(candidate.get("doi") or "").strip()
        if not doi:
            record["download"] = {"status": "missing_doi"}
            manifest["records"].append(record)
            continue
        metadata = collect_oa_metadata(session, doi, args, headers)
        record["open_access"] = metadata["summary"]
        pdf_candidates = pdf_urls_from_metadata(metadata, args)
        record["pdf_candidates"] = [public_url_item(item) for item in pdf_candidates]
        record["download"] = download_first_pdf(session, pdf_candidates, pdf_dir, index, record, args, headers)
        manifest["records"].append(record)
        time.sleep(args.sleep)

    manifest["summary"] = {
        "records": len(manifest["records"]),
        "pdf_saved": sum(1 for r in manifest["records"] if r["download"].get("status") == "pdf_saved"),
        "oa_detected": sum(1 for r in manifest["records"] if r["open_access"].get("is_oa")),
    }
    (output / "open_access_pdf_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Records: {manifest['summary']['records']}")
    print(f"OA detected: {manifest['summary']['oa_detected']}")
    print(f"PDFs: {manifest['summary']['pdf_saved']}")
    print(f"Manifest: {output / 'open_access_pdf_manifest.json'}")
    return 0


def load_candidates(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("items") or data.get("records") or []
    if not isinstance(items, list):
        raise SystemExit("Candidate JSON must contain an items or records list.")
    return [item for item in items if isinstance(item, dict)]


def collect_oa_metadata(
    session: requests.Session,
    doi: str,
    args: argparse.Namespace,
    headers: dict[str, str],
) -> dict[str, Any]:
    metadata: dict[str, Any] = {"openalex": None, "unpaywall": None, "summary": {"is_oa": False}}
    openalex = get_openalex(session, doi, args, headers)
    if openalex:
        metadata["openalex"] = openalex
        oa = openalex.get("open_access") or {}
        metadata["summary"] = {
            "is_oa": bool(oa.get("is_oa")),
            "oa_status": oa.get("oa_status"),
            "source": "openalex",
        }
    if args.unpaywall_email:
        unpaywall = get_unpaywall(session, doi, args, headers)
        if unpaywall:
            metadata["unpaywall"] = unpaywall
            if unpaywall.get("is_oa"):
                metadata["summary"] = {
                    "is_oa": True,
                    "oa_status": unpaywall.get("oa_status"),
                    "source": "unpaywall",
                }
    return metadata


def get_openalex(
    session: requests.Session,
    doi: str,
    args: argparse.Namespace,
    headers: dict[str, str],
) -> dict[str, Any] | None:
    params = {}
    if args.openalex_mailto:
        params["mailto"] = args.openalex_mailto
    response = session.get(OPENALEX_WORK_URL.format(doi=doi), params=params, headers=headers, timeout=args.timeout)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def get_unpaywall(
    session: requests.Session,
    doi: str,
    args: argparse.Namespace,
    headers: dict[str, str],
) -> dict[str, Any] | None:
    response = session.get(
        UNPAYWALL_WORK_URL.format(doi=doi),
        params={"email": args.unpaywall_email},
        headers=headers,
        timeout=args.timeout,
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def pdf_urls_from_metadata(metadata: dict[str, Any], args: argparse.Namespace) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    openalex = metadata.get("openalex") or {}
    for location in openalex_locations(openalex):
        if not location.get("is_oa"):
            continue
        add_url(candidates, location.get("pdf_url"), "openalex_pdf_url", location)
        if args.allow_landing_probe:
            for pdf_url in landing_pdf_urls(location.get("landing_page_url"), args):
                add_url(candidates, pdf_url, "openalex_landing_probe", location)

    unpaywall = metadata.get("unpaywall") or {}
    if unpaywall:
        for location in unpaywall_locations(unpaywall):
            if not is_unpaywall_oa_location(location):
                continue
            add_url(candidates, location.get("url_for_pdf"), "unpaywall_pdf_url", location)
            if args.allow_landing_probe:
                for pdf_url in landing_pdf_urls(location.get("url") or location.get("url_for_landing_page"), args):
                    add_url(candidates, pdf_url, "unpaywall_landing_probe", location)
    return dedupe_url_items(candidates)


def openalex_locations(openalex: dict[str, Any]) -> list[dict[str, Any]]:
    locations = []
    for key in ("best_oa_location", "primary_location"):
        location = openalex.get(key)
        if isinstance(location, dict):
            locations.append(location)
    locations.extend([item for item in openalex.get("locations", []) if isinstance(item, dict)])
    return locations


def unpaywall_locations(unpaywall: dict[str, Any]) -> list[dict[str, Any]]:
    locations = []
    location = unpaywall.get("best_oa_location")
    if isinstance(location, dict):
        locations.append(location)
    locations.extend([item for item in unpaywall.get("oa_locations", []) if isinstance(item, dict)])
    return locations


def is_unpaywall_oa_location(location: dict[str, Any]) -> bool:
    return bool(location.get("url_for_pdf") or location.get("url") or location.get("url_for_landing_page"))


def add_url(candidates: list[dict[str, Any]], url: Any, source: str, location: dict[str, Any]) -> None:
    if not url:
        return
    candidates.append(
        {
            "url": str(url),
            "source": source,
            "host": urlparse(str(url)).netloc.lower(),
            "license": location.get("license"),
            "location_is_oa": location.get("is_oa"),
        }
    )


def landing_pdf_urls(url: Any, args: argparse.Namespace) -> list[str]:
    if not url:
        return []
    landing = str(url)
    parsed = urlparse(landing)
    host = parsed.netloc.lower()
    allowed_hosts = DEFAULT_LANDING_HOSTS | {item.lower() for item in args.allowed_landing_host}
    if host not in allowed_hosts:
        return []
    if host == "arxiv.org" and parsed.path.startswith("/abs/"):
        arxiv_id = parsed.path.removeprefix("/abs/")
        return [f"https://arxiv.org/pdf/{arxiv_id}.pdf"]
    try:
        response = requests.get(
            landing,
            headers={"User-Agent": user_agent(args.openalex_mailto or args.unpaywall_email)},
            timeout=args.timeout,
        )
        if not response.ok:
            return []
    except requests.RequestException:
        return []
    html = response.text
    urls = []
    for href in re.findall(r"""href=["']([^"']+)["']""", html, flags=re.I):
        href = unescape(href)
        absolute = urljoin(landing, href)
        if looks_like_pdf_url(absolute):
            urls.append(absolute)
    return urls[:5]


def looks_like_pdf_url(url: str) -> bool:
    lower = url.lower()
    return lower.endswith(".pdf") or "/pdf/" in lower or "/servlets/purl/" in lower


def dedupe_url_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped = []
    seen = set()
    for item in items:
        key = item["url"]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def public_url_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "url": item.get("url"),
        "source": item.get("source"),
        "host": item.get("host"),
        "license": item.get("license"),
        "location_is_oa": item.get("location_is_oa"),
    }


def download_first_pdf(
    session: requests.Session,
    pdf_candidates: list[dict[str, Any]],
    pdf_dir: Path,
    index: int,
    record: dict[str, Any],
    args: argparse.Namespace,
    headers: dict[str, str],
) -> dict[str, Any]:
    attempts = []
    for item in pdf_candidates:
        url = item["url"]
        try:
            response = session.get(url, headers=headers, timeout=args.timeout, allow_redirects=True)
        except requests.RequestException as exc:
            attempts.append({"url": url, "status": "request_error", "error": str(exc)})
            continue
        content_type = response.headers.get("content-type", "")
        attempt = {
            "url": url,
            "http_status": response.status_code,
            "content_type": content_type,
            "bytes": len(response.content),
        }
        if is_pdf_response(response, args):
            filename = f"{index:03d}_{slug(record.get('title') or record.get('doi') or 'article')}.pdf"
            path = pdf_dir / filename
            path.write_bytes(response.content)
            attempt["status"] = "pdf_saved"
            attempt["path"] = str(path)
            return attempt
        attempt["status"] = "not_pdf"
        attempts.append(attempt)
    return {"status": "pdf_unavailable", "attempts": attempts}


def is_pdf_response(response: requests.Response, args: argparse.Namespace) -> bool:
    content_type = response.headers.get("content-type", "").lower()
    return (
        response.ok
        and len(response.content) >= args.min_pdf_bytes
        and (response.content.startswith(b"%PDF") or "pdf" in content_type)
    )


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return (value[:90] or "article").strip("-")


def user_agent(mailto: str | None) -> str:
    base = "windenergy-style-learning/1.0"
    if mailto:
        return f"{base} (mailto:{mailto})"
    return base


if __name__ == "__main__":
    raise SystemExit(main())
