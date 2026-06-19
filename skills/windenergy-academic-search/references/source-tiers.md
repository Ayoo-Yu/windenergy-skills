# Source Tiers

## API-backed Sources

| Source | Strength | Limitation |
|---|---|---|
| CrossRef | DOI metadata, venue data, formatted DOI citations | Search relevance can be broad |
| OpenAlex | Broad coverage, citation counts, open-access metadata | Metadata quality varies by venue |
| Semantic Scholar | AI/ML relevance, abstracts, citation counts | Rate limits without API key |
| arXiv | Recent AI/control/optimization preprints | Preprints are not peer reviewed |

## Manual Verification Sources

Use these when available through browsing, institutional access, or user-provided
exports:

- Scopus and Web of Science for curated citation indexes.
- IEEE Xplore for power systems and engineering conference papers.
- ScienceDirect for Elsevier final article pages.
- NREL, IRENA, Copernicus, ECMWF, EIA, and grid-operator sites for technical
  reports and datasets.

## Source Use Policy

- Never imply that a manual source was searched by the MCP server.
- Report per-source warnings when an API fails.
- Cross-check important citations by DOI or publisher page before manuscript use.
- Label preprints and technical reports distinctly from peer-reviewed journal
  articles.
