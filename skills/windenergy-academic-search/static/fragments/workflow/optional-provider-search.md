# Optional Provider Search

Scopus, ScienceDirect, IEEE Xplore, Web of Science, NREL, and IRENA are optional
or manual verification sources. Use them only when a configured authenticated
tool is available or the user explicitly supplies source data.

For the bundled MCP server, Scopus and ScienceDirect require
`mcp-server/requirements-elsevier.txt` and a valid `pybliometrics`
configuration. If either is missing, report the provider warning and continue
with free sources where useful.
