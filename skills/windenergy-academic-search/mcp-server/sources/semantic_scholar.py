"""Semantic Scholar data source for renewable academic search."""

from __future__ import annotations

import requests

from utils.config import get_config
from utils.errors import DataSourceError

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"


class SemanticScholarSource:
    """Semantic Scholar Graph API wrapper."""

    SOURCE_NAME = "semantic_scholar"

    def __init__(self):
        config = get_config()
        self._api_key = config.semantic_scholar_api_key
        self._timeout = config.semantic_scholar_timeout

    def search(self, query: str, rows: int = 5) -> dict:
        params = {
            "query": query,
            "limit": min(rows, 50),
            "fields": "title,authors,year,venue,abstract,externalIds,citationCount,url,openAccessPdf,publicationTypes",
        }
        data = self._request("/paper/search", params=params)
        items = data.get("data", [])
        return {
            "total": data.get("total", len(items)),
            "results": [self._normalize_item(item) for item in items],
        }

    def _request(self, path: str, params: dict | None = None) -> dict:
        url = f"{SEMANTIC_SCHOLAR_API}{path}"
        headers = {"User-Agent": "windenergy-academic-search/1.0"}
        if self._api_key:
            headers["x-api-key"] = self._api_key
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=self._timeout)
            resp.raise_for_status()
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else "?"
            if status == 429:
                message = "Rate limited by Semantic Scholar; set SEMANTIC_SCHOLAR_API_KEY or retry later"
            else:
                message = f"HTTP {status} from {url}"
            raise DataSourceError(self.SOURCE_NAME, message, exc) from exc
        except requests.RequestException as exc:
            raise DataSourceError(self.SOURCE_NAME, f"Network error calling {url}: {exc}", exc) from exc
        return resp.json()

    def _normalize_item(self, item: dict) -> dict:
        external_ids = item.get("externalIds") or {}
        open_pdf = item.get("openAccessPdf") or {}
        return {
            "title": item.get("title", ""),
            "authors": [author.get("name", "") for author in item.get("authors", []) if author.get("name")],
            "year": item.get("year"),
            "doi": external_ids.get("DOI", ""),
            "journal": item.get("venue", ""),
            "source": self.SOURCE_NAME,
            "citation_count": item.get("citationCount", 0),
            "url": item.get("url", ""),
            "pdf_url": open_pdf.get("url", ""),
            "abstract": item.get("abstract", ""),
            "publication_types": item.get("publicationTypes") or [],
        }
