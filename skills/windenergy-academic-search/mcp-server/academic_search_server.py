"""Academic search MCP server for renewable energy research.

Tools:
  - search_papers: concurrent search across CrossRef, OpenAlex, Semantic Scholar, arXiv
  - get_paper_by_id: fetch details by DOI or arXiv ID
  - get_citation: format a DOI or arXiv citation for common journal styles
"""

from __future__ import annotations

import asyncio
import json
import re
from typing import Any

from mcp.server import FastMCP

from sources import ArxivSource, CrossRefSource, OpenAlexSource, SemanticScholarSource
from utils import DataSourceError, setup_logging

mcp = FastMCP("windenergy-academic-search")
logger = setup_logging()

_crossref = CrossRefSource()
_openalex = OpenAlexSource()
_semantic_scholar = SemanticScholarSource()
_arxiv = ArxivSource()


def _clean_id(identifier: str) -> str:
    value = identifier.strip()
    value = re.sub(r"^https - ://(dx\.) - doi\.org/", "", value, flags=re.I)
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    value = re.sub(r"^https - ://arxiv\.org/(abs|pdf)/", "", value, flags=re.I)
    value = value.removesuffix(".pdf")
    return value.strip()


def _detect_id_type(identifier: str) -> str:
    value = _clean_id(identifier)
    if value.startswith("10.") and "/" in value:
        return "doi"
    if re.match(r"^(arxiv:)?\d{4}\.\d{4,5}(v\d+)?$", value, flags=re.I):
        return "arxiv"
    raise ValueError(f"Cannot detect DOI or arXiv ID for: {identifier}")


def _resolve_id_type(identifier: str, id_type: str) -> str:
    if id_type == "auto":
        return _detect_id_type(identifier)
    normalised = id_type.lower().strip().replace("-", "_")
    if normalised in {"doi", "arxiv"}:
        return normalised
    raise ValueError(f"Unsupported id_type: {id_type}. Use doi, arxiv, or auto.")


def _json_ok(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def _json_error(message: str, source: str | None = None) -> str:
    payload: dict[str, Any] = {"error": message}
    if source:
        payload["source"] = source
    return json.dumps(payload, ensure_ascii=False, indent=2)


async def _search_source(
    source_name: str,
    query: str,
    rows: int,
    filter_type: str | None,
) -> dict:
    if source_name == "crossref":
        return await asyncio.to_thread(_crossref.search, query, rows, filter_type)
    if source_name == "openalex":
        return await asyncio.to_thread(_openalex.search, query, rows, filter_type)
    if source_name == "semantic_scholar":
        return await asyncio.to_thread(_semantic_scholar.search, query, rows)
    if source_name == "arxiv":
        return await asyncio.to_thread(_arxiv.search, query, rows)
    raise ValueError(f"Unknown source: {source_name}")


async def _search_all(
    query: str,
    sources: list[str],
    rows: int,
    filter_type: str | None,
) -> dict:
    tasks = [
        asyncio.create_task(_search_source(source, query, rows, filter_type))
        for source in sources
    ]
    outcomes = await asyncio.gather(*tasks, return_exceptions=True)

    merged_results: list[dict] = []
    errors: list[dict] = []
    total = 0
    seen: set[str] = set()

    for source, outcome in zip(sources, outcomes):
        if isinstance(outcome, BaseException):
            logger.error("Source %s failed: %s", source, outcome)
            errors.append({"source": source, "error": str(outcome)})
            continue
        total += outcome.get("total", 0)
        for item in outcome.get("results", []):
            key = (item.get("doi") or item.get("arxiv_id") or item.get("title") or "").lower()
            if key and key in seen:
                continue
            if key:
                seen.add(key)
            merged_results.append(item)

    return {
        "query": query,
        "sources_queried": sources,
        "total_reported_by_sources": total,
        "result_count": len(merged_results),
        "results": merged_results,
        "warnings": errors,
    }


@mcp.tool()
def search_papers(
    query: str,
    sources: list[str] | None = None,
    rows: int = 5,
    type: str | None = None,
) -> str:
    """Search renewable-energy papers across free academic metadata sources.

    Args:
        query: Search keywords, title phrase, author, or DOI-like text.
        sources: Any subset of crossref, openalex, semantic_scholar, arxiv.
        rows: Number of results per source, capped at 50.
        type: Optional source-specific work type filter for CrossRef/OpenAlex.

    Returns:
        JSON with merged results and per-source warnings.
    """
    if not query or not query.strip():
        return _json_error("Empty search query")

    if sources is None:
        sources = ["crossref", "openalex", "semantic_scholar", "arxiv"]
    sources = [source.lower().strip().replace("-", "_") for source in sources]

    valid_sources = {"crossref", "openalex", "semantic_scholar", "arxiv"}
    invalid = [source for source in sources if source not in valid_sources]
    if invalid:
        return _json_error(f"Invalid sources: {invalid}. Valid: {sorted(valid_sources)}")

    rows = max(1, min(rows, 50))

    try:
        result = asyncio.run(_search_all(query.strip(), sources, rows, type))
    except Exception as exc:
        logger.exception("search_papers failed")
        return _json_error(f"Search failed: {exc}")
    return _json_ok(result)


@mcp.tool()
def get_paper_by_id(id: str, id_type: str = "auto") -> str:
    """Get paper details by DOI or arXiv ID."""
    if not id or not id.strip():
        return _json_error("Empty identifier")

    clean_id = _clean_id(id)
    try:
        resolved_type = _resolve_id_type(clean_id, id_type)
    except ValueError as exc:
        return _json_error(str(exc))

    try:
        if resolved_type == "doi":
            result = _crossref.get_by_doi(clean_id)
        elif resolved_type == "arxiv":
            result = _arxiv.get_by_id(clean_id)
        else:
            return _json_error(f"Unsupported ID type: {resolved_type}")
    except DataSourceError as exc:
        return _json_error(str(exc), source=exc.source)
    except Exception as exc:
        logger.exception("get_paper_by_id failed")
        return _json_error(f"Unexpected error: {exc}")
    return _json_ok(result)


@mcp.tool()
def get_citation(id: str, id_type: str = "auto", style: str = "elsevier") -> str:
    """Get a formatted citation for a DOI or arXiv paper.

    Supported style aliases: elsevier, renewable-energy, apa, ieee, harvard.
    """
    if not id or not id.strip():
        return _json_error("Empty identifier")

    clean_id = _clean_id(id)
    style = _normalize_style(style)
    try:
        resolved_type = _resolve_id_type(clean_id, id_type)
    except ValueError as exc:
        return _json_error(str(exc))

    try:
        if resolved_type == "doi":
            citation = _crossref.get_citation(clean_id, style=style)
            return _json_ok({"id": clean_id, "id_type": "doi", "style": style, "citation": citation})
        if resolved_type == "arxiv":
            paper = _arxiv.get_by_id(clean_id)
            citation = _format_basic_citation(paper, style)
            return _json_ok({"id": clean_id, "id_type": "arxiv", "style": style, "citation": citation})
    except DataSourceError as exc:
        return _json_error(str(exc), source=exc.source)
    except Exception as exc:
        logger.exception("get_citation failed")
        return _json_error(f"Unexpected error: {exc}")
    return _json_error(f"Unsupported ID type: {resolved_type}")


def _normalize_style(style: str) -> str:
    alias = style.lower().strip().replace("_", "-")
    if alias in {"elsevier", "renewable-energy", "re"}:
        return "elsevier-harvard"
    if alias in {"ieee", "apa", "harvard"}:
        return alias
    return alias or "elsevier-harvard"


def _format_basic_citation(paper: dict, style: str) -> str:
    authors = paper.get("authors", [])
    title = paper.get("title", "Untitled")
    year = paper.get("year", "n.d.")
    venue = paper.get("journal") or "arXiv preprint"
    arxiv_id = paper.get("arxiv_id", "")

    if len(authors) > 3:
        author_str = f"{authors[0]} et al."
    elif authors:
        author_str = ", ".join(authors)
    else:
        author_str = "Unknown"

    if style == "ieee":
        return f'{author_str}, "{title}," {venue}, {year}. arXiv:{arxiv_id}.'
    if style == "apa":
        return f"{author_str} ({year}). {title}. {venue}. arXiv:{arxiv_id}."
    return f"{author_str}, {title}, {venue}, {year}. arXiv:{arxiv_id}."


if __name__ == "__main__":
    mcp.run(transport="stdio")
