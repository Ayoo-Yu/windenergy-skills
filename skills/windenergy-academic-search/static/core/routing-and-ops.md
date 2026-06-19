# Routing And Operations

Use free providers first:

1. CrossRef for DOI metadata and journal provenance.
2. OpenAlex for broad discovery and open metadata.
3. Semantic Scholar for AI/ML relevance.
4. arXiv for preprints.

If MCP dependencies are missing, report that the MCP server is not available
and continue with planning or available metadata tools. Do not imply that
MCP-backed sources were queried when the server did not run.

Use optional Scopus or ScienceDirect only when the user requests them and the
environment is configured. Report provider failures as warnings.

