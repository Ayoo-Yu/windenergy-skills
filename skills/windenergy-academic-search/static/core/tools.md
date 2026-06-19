# Tool Inventory

Bundled MCP server:

- `search_papers`: CrossRef, OpenAlex, Semantic Scholar, and arXiv.
- `get_paper_by_id`: DOI or arXiv lookup.
- `get_citation`: Elsevier, IEEE, APA, or Harvard style citation formatting.

Default sources remain free metadata providers. Scopus and ScienceDirect are
optional providers only when a separate authenticated tool or local configuration
is available. Their Python dependencies live in
`mcp-server/requirements-elsevier.txt`, not the default requirements file.
