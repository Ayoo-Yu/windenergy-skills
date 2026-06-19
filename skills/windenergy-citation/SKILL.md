---
name: windenergy-citation
description: >-
  Add, verify, screen, and export citations for renewable energy, wind power,
  energy forecasting, smart-grid, and AI-for-energy manuscripts. Use when the
  user asks for supporting literature, DOI checks, reference-list cleanup,
  EndNote/RIS/BibTeX export, or claim-by-claim citation suggestions for
  the 18 target Elsevier energy, power, AI, and pattern-recognition journals,
  IEEE energy journals, final manuscript citation audits, or similar venues.
---

# Renewable Citation

Use this skill after the claim or paragraph is known and the user needs
references that actually support it. For broad discovery, coordinate with
`windenergy-academic-search`; for final submission limits, coordinate with
`windenergy-submission`.

## Router Protocol

Read `manifest.yaml`, load all `always_load` files, and then open on-demand
references only for claim search, journal scope, export, or script execution.

Boundary: this skill owns final reference-list audits, in-text citation to
reference-list consistency, DOI metadata mismatch checks, reference cleanup,
and claim-by-claim support decisions. `windenergy-academic-search` owns broad
discovery and candidate metadata retrieval before a source is selected.

Before writing generated files, load `../_shared/core/output-run-folders.md`
and create a run folder for this invocation. Put reference exports, citation
screening tables, claim maps, and logs in that run folder.

When a citation task involves claim support or final readiness, load
`../_shared/core/quality-principles.md` and check the evidence chain for each
claim that depends on prior work. Keep broad literature coverage issues routed
to `windenergy-academic-search`. If the final manuscript has far fewer references
than the active profile's planning rule, report the count gap but do not pad
the reference list. Route discovery of additional sources back to
`windenergy-academic-search`. Without an active profile, do not apply a fixed
reference-count target.

## Citation Workflow

1. Extract each claim that needs support.
2. Classify the claim: background, method, baseline, dataset, physical
   mechanism, forecasting result, uncertainty, grid relevance, or limitation.
3. Search with energy-specific terms and screen for direct relevance.
4. Prefer DOI-backed journal articles; label arXiv papers as preprints.
5. Export only verified references and check the active profile before applying
   a reference-count limit.
6. For a named target journal, count cited references from that journal only
   when the active profile defines that coverage check. Present directly
   relevant candidates for author approval.

## Final Citation Audit

Use this mode when `windenergy-submission` requests final manuscript citation
review.

- Run the strict audit script for `.docx` manuscripts before writing a final
  readiness conclusion:

```bash
python scripts/windenergy_citation.py --audit MANUSCRIPT.docx --bib REFERENCES.bib --output audit.json --markdown audit.md
```

- The `--bib` input is optional. When it is absent, the script parses the Word
  References section.
- Treat the script exit code as authoritative for readiness. A nonzero exit
  means the manuscript has `FAIL` or `UNCHECKED` citation items and cannot be
  reported ready.
- Include `audit.json` in the run folder. If no `audit.json` exists, mark the
  citation audit as `UNCHECKED`.
- Verify every in-text citation resolves to one reference-list entry.
- Verify every reference-list entry is cited or flagged as uncited.
- Check citation ranges, grouped citations, and renumbering maps.
- Check DOI-backed metadata for title, year, journal, volume, pages, and article
  number when metadata is available.
- Confirm each added target-journal citation supports a specific manuscript
  claim.
- Flag unsupported claims, weak sources, missing DOI metadata, duplicate
  references, and citation-manager field risks.
- Do not modify references without explicit author approval unless the edit is
  an exact formatting correction backed by verified metadata.

## Preferred Journal Scope

- Renewable Energy, Applied Energy, Energy, Energy Conversion and Management.
- Energy Reports, Energy and AI, Sustainable Energy, Grids and Networks.
- Renewable and Sustainable Energy Reviews, Solar Energy, Wind Energy.
- IEEE Transactions on Sustainable Energy, IEEE Transactions on Power Systems,
  IEEE Transactions on Smart Grid, IET Renewable Power Generation.
- Applied Soft Computing, Information Sciences, Neurocomputing,
  Knowledge-Based Systems, Pattern Recognition, Engineering Applications of
  Artificial Intelligence, and Expert Systems with Applications when the cited
  claim is about the method itself.

## Script

Use `scripts/windenergy_citation.py` for strict citation audits, quick
CrossRef-backed DOI screening, and RIS/BibTeX export:

```bash
python scripts/windenergy_citation.py --audit MANUSCRIPT.docx --bib REFERENCES.bib --output audit.json --markdown audit.md
python scripts/windenergy_citation.py --query "wind power forecasting transformer" --format ris --output <RUN_DIR>/refs.ris
python scripts/windenergy_citation.py --doi 10.xxxx/example --format bib
```

## Red Lines

- Do not invent references, DOIs, journal names, page ranges, or citation counts.
- Do not cite a paper for a stronger claim than its title/abstract supports.
- Do not use generic AI citations as substitutes for wind-energy evidence.
- Do not add target-journal citations only to satisfy the count. Each suggested
  paper must support a specific manuscript claim.
- If the user asks for a reference to support a questionable claim, offer a
  narrowed wording or say that a stronger source is needed.

## References

- `references/search-strategy.md` for claim-to-query patterns.
- `references/journal-scope.md` for preferred energy venues.
- `references/ris-endnote.md` for export conventions.
