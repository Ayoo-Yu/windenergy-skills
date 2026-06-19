"""OpenAlex data source for renewable academic search."""

from __future__ import annotations

from urllib.parse import quote

import requests

from utils.config import get_config
from utils.errors import DataSourceError

OPENALEX_API = "https://api.openalex.org"


class OpenAlexSource:
    """OpenAlex Works API wrapper."""

    SOURCE_NAME = "openalex"

    def __init__(self):
        config = get_config()
        self._mailto = config.openalex_mailto
        self._timeout = config.openalex_timeout
        self._headers = {"User-Agent": "windenergy-academic-search/1.0"}

    def search(self, query: str, rows: int = 5, filter_type: str | None = None) -> dict:
        params: dict[str, str | int] = {
            "search": query,
            "per-page": min(rows, 50),
            "sort": "relevance_score:desc",
        }
        filters = ["type:article"]
        if filter_type:
            filters = [f"type:{filter_type}"]
        if filters:
            params["filter"] = ",".join(filters)
        if self._mailto:
            params["mailto"] = self._mailto

        data = self._request("/works", params=params)
        items = data.get("results", [])
        return {
            "total": data.get("meta", {}).get("count", len(items)),
            "results": [self._normalize_item(item) for item in items],
        }

    def _request(self, path: str, params: dict | None = None) -> dict:
        url = f"{OPENALEX_API}{path}"
        try:
            resp = requests.get(url, params=params, headers=self._headers, timeout=self._timeout)
            resp.raise_for_status()
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else "?"
            raise DataSourceError(self.SOURCE_NAME, f"HTTP {status} from {url}", exc) from exc
        except requests.RequestException as exc:
            raise DataSourceError(self.SOURCE_NAME, f"Network error calling {url}: {exc}", exc) from exc
        return resp.json()

    def _normalize_item(self, item: dict) -> dict:
        doi = (item.get("doi") or "").removeprefix("https://doi.org/")
        source = ((item.get("primary_location") or {}).get("source") or {}).get("display_name", "")
        if not source:
            source = (item.get("host_venue") or {}).get("display_name", "")
        return {
            "title": item.get("display_name", ""),
            "authors": self._extract_authors(item.get("authorships", []), limit=5),
            "year": item.get("publication_year"),
            "doi": doi,
            "journal": source,
            "source": self.SOURCE_NAME,
            "citation_count": item.get("cited_by_count", 0),
            "url": item.get("id") or item.get("landing_page_url") or "",
            "abstract": _abstract_from_inverted_index(item.get("abstract_inverted_index")),
            "open_access": item.get("open_access", {}),
            "type": item.get("type"),
        }

    @staticmethod
    def _extract_authors(authorships: list[dict], limit: int = 5) -> list[str]:
        names = [
            ((entry.get("author") or {}).get("display_name") or "").strip()
            for entry in authorships[:limit]
        ]
        names = [name for name in names if name]
        if len(authorships) > limit:
            names.append("et al.")
        return names


def _abstract_from_inverted_index(index: dict | None) -> str:
    if not index:
        return ""
    words: list[tuple[int, str]] = []
    for word, positions in index.items():
        for position in positions:
            words.append((position, word))
    return " ".join(word for _, word in sorted(words))
