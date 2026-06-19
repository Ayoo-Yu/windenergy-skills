"""Data source modules for renewable academic search."""

from .arxiv import ArxivSource
from .crossref import CrossRefSource
from .openalex import OpenAlexSource
from .semantic_scholar import SemanticScholarSource

__all__ = ["ArxivSource", "CrossRefSource", "OpenAlexSource", "SemanticScholarSource"]
