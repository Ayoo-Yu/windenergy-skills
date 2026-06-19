---
name: windenergy-academic-search
description: >-
  Search, discover, screen, deduplicate, and export candidate references for
  renewable energy, wind power, energy forecasting, and AI-for-energy papers.
  Uses free academic metadata sources including CrossRef, OpenAlex, Semantic
  Scholar, and arXiv, plus DOI/arXiv lookup and citation formatting for
  candidate sources. Use when the user asks to find papers, build literature
  searches, retrieve candidate metadata, export RIS/BibTeX-style records, or
  locate sources that may support a claim. For final reference-list audits,
  in-text citation checks, DOI metadata mismatch checks, or reference cleanup,
  use `windenergy-citation`.
---

# Renewable Academic Search

Use this skill for literature-search and reference-verification tasks in wind
energy, renewable power generation, smart grids, energy forecasting, and
AI-for-energy manuscripts.

Boundary: this skill finds and screens candidate sources. `windenergy-citation`
owns final citation audits, reference-list cleanup, in-text citation to
reference-list consistency, DOI metadata mismatch checks, and claim-by-claim
support decisions in finished manuscripts.

Before writing generated files, load `../_shared/core/output-run-folders.md`
and create a run folder for this invocation. Put search logs, screened
candidates, RIS, BibTeX, CSV, and Markdown reports in that run folder.

For manuscript-level literature planning, also load
`../_shared/core/quality-principles.md` and run a literature coverage audit for
journal fit. This audit checks whether the source pool covers the target
application domain, method family, evaluation criteria, and closest alternatives.
Reference scale and topic-bucket requirements must come from the active profile,
including journal, topic, or paper-type fragments. Without a profile, report
reference-pool scale as `UNCHECKED` and avoid padding claims with loosely
related papers.

For Related Work planning, use `related_work_literature_map` mode. This mode
structures search results for synthesis rather than dumping citations into the
manuscript.

## Source Routing

- Use CrossRef first for DOI metadata, journal provenance, and citation export.
- Use OpenAlex for broad discovery, citation counts, open-access metadata, and
  interdisciplinary renewable-energy coverage.
- Use Semantic Scholar for AI/ML papers, citation counts, and abstract-level
  relevance; `SEMANTIC_SCHOLAR_API_KEY` is optional but helps with rate limits.
- Use arXiv for AI, optimization, control, and forecasting preprints.
- Treat Scopus, Web of Science, IEEE Xplore, ScienceDirect, NREL, and IRENA as
  manual/browser-verification sources unless a separate authenticated tool is
  available.

## MCP Tools

The bundled server is under `mcp-server/academic_search_server.py`.
Before registering it as an MCP server, install its runtime dependencies from
`mcp-server/requirements.txt` in the Python environment that will launch the
server.
If those dependencies are unavailable, report that the MCP server is not available
and continue with ordinary literature-search planning or with any available
metadata tools. Do not imply that MCP-backed sources were queried when the server
did not run.

| Tool | Purpose |
|---|---|
| `search_papers` | Search CrossRef, OpenAlex, Semantic Scholar, and arXiv |
| `get_paper_by_id` | Fetch details by DOI or arXiv ID |
| `get_citation` | Format DOI/arXiv citations for Elsevier, IEEE, APA, or Harvard |

When several sources return the same DOI or arXiv ID, deduplicate before
recommending papers. If a source fails or is rate-limited, report it as a warning
and continue with the other sources.

## Search Workflow

1. Translate the user's claim or Chinese notes into 2-4 concise English queries.
2. Search with `search_papers`; default to all free sources unless the user asks
   for a specific source.
3. Prefer peer-reviewed journal papers for manuscript claims; use arXiv to track
   recent AI methods and label them as preprints.
4. Screen candidates by title, venue, year, DOI, abstract, and citation context.
5. Verify candidate DOI/arXiv metadata before recommending a source.
6. For target-journal submissions, check `windenergy-submission` profiles and
   journal fragments before applying a reference-count limit.
7. For named target journals, support the 10 target-journal citation coverage
   check by searching that journal for papers that directly match existing
   manuscript claims.
8. For profile-driven full papers, record whether the candidate pool reaches
   the profile's reference-scale target and which topic buckets are still thin.
9. Report literature coverage gaps separately from final citation errors.
   Discovery gaps belong here; reference-list and DOI mismatch failures belong
   to `windenergy-citation`.
10. When the user asks for Related Work support, produce a
    `related_work_literature_map` before prose drafting.

## Related Work Literature Map

`related_work_literature_map` must include:

- `topic bucket`: the research line or evidence role
- `search queries used`: English queries and sources attempted
- `representative papers`: directly relevant papers with DOI, venue, or source
  status when available
- `seminal papers`: foundational sources for the bucket
- `recent direct competitors`: closest recent studies
- `method or assumption shared by the bucket`: common paradigm to synthesize
- `known limitation`: what the bucket still leaves unresolved
- `connection to manuscript gap`: why this bucket matters for the manuscript
- `coverage status`: `sufficient`, `thin`, or `unchecked`

This skill owns candidate discovery and coverage-gap reporting. It should not
write manuscript sentences about submission strategy, journal reference scale,
or publication expectations. Those limits belong to the active profile,
journal fragment, or submission audit.

## Energy Query Patterns

Use field terms that match the evidence need:

- Application domain: combine the asset, decision, data source, and physical or
  market setting from the active profile.
- Physical or operational constraints: combine profile constraint terms with
  method or evaluation terms.
- AI methods: combine the method family with the energy task and evidence need.
- Grid or deployment relevance: combine profile decision terms with risk, cost,
  reliability, or operational value.
- Target-journal coverage: combine the claim terms with the exact journal title,
  then verify venue metadata by DOI, CrossRef, OpenAlex, or publisher page.

## Output Rules

- Do not fabricate DOIs, authors, venues, citation counts, or arXiv IDs.
- Mark preprints clearly.
- Flag metadata conflicts instead of silently choosing one source.
- Include enough bibliographic detail for the user to verify the paper.
- Include a topic-bucket coverage summary for manuscript-level searches:
  application domain, method family, evaluation criteria, closest alternatives,
  and target-journal context.
- For Related Work requests, include `related_work_literature_map` with topic
  bucket, representative papers, known limitation, connection to manuscript gap,
  and coverage status.
- If files are written, report the run folder path.
- If a claim is weakly supported, say so and suggest a narrower claim or better
  evidence search.

## Useful References

- `references/search-strategy.md` for renewable-energy search patterns.
- `references/source-tiers.md` for source strengths and limitations.
- `references/dedup-engine.md` for DOI/title deduplication rules.
- `references/ris-bibtex-format.md` for export field mapping.
