# Final Manuscript Audit

Use this audit for the final `.docx` or `.tex` manuscript before submission.
It is required in `full-check` after word count, reference count, and safe
tracked revisions.

Load `../_shared/core/quality-principles.md`,
`../_shared/core/narrative-principles.md`, and the active
`workflow_profile.json` before final readiness decisions. The final audit
includes content maturity, not only file packaging, declaration, abbreviation,
and citation checks.

## Skill Routing

- Use `windenergy-polishing` for abbreviation consistency, avoidable
  parentheses, and main-text figure, table, and appendix color formatting.
- Use `windenergy-citation` for citation integrity, claim support, DOI metadata,
  and reference-list consistency.
- Use `windenergy-submission` to combine both results into the final submission
  decision.

## Content Maturity Audit

Check whether the manuscript is a complete target-journal article.

- No empty sections, placeholder headings, placeholder citations, unresolved
  template text, or hidden TODO markers remain.
- Title, abstract, highlights, contribution paragraph, discussion, and
  conclusion follow claim strength control.
- Every core claim has an evidence chain to a result, figure, table, code path,
  dataset note, or verified citation.
- Experimental setup includes profile-relevant data provenance, sampling,
  period, splits, inputs, targets, preprocessing, and exclusions.
- Methodology includes algorithms, scores, assumptions, parameters, update
  timing, and implementation settings needed for reproducibility.
- Figures, tables, captions, and main text are mutually consistent.
- Related Work covers the profile-selected application, method family,
  evaluation criteria, and closest alternatives.
- Reference scale and source-bucket expectations come from the active journal,
  topic, or paper-type fragment. Without a profile, mark reference-pool scale
  `UNCHECKED`.
- Limitations and future work do not replace evidence needed for a central
  claim.
- Main-body depth and article length come from the active journal or paper-type
  profile.
- Operational guidance and selection tables have explanatory prose outside the
  table.
- Display-item expectations come from the active journal or paper-type profile.
- Figure sets have a consistent visual style: journal serif font, at least
  8 pt text, stable colors, consistent line widths, clear legends, and clear
  axis wording.
- The figure portfolio covers workflow, data or task overview, method
  comparison, condition boundary, mechanism evidence, robustness, and deployment
  guidance when those claim types appear in the manuscript.
- Strong titles align with evidence boundaries. If key diagnostics are partial,
  aggregate, proxy-based, or unavailable, mark the title as `Claim risk` unless
  it uses calibrated wording.
- Advice level is backed by matching result granularity.
- Mechanism or causal claims use the controls required by the active paper-type,
  topic, or manuscript fragment, or the claim is downgraded.
- Low-support conditions include sample count, sample share, uncertainty, or
  sensitivity evidence before they support strong boundary claims.
- Internal workflow artifact names are absent from the main article unless they
  appear in a reproducibility statement or appendix.
- Title, abstract, highlights, contribution, and conclusion pass the active
  narrative check. Missing problem tension or take-home message is reported as
  `NARRATIVE_WARNING`.

If any required item is missing, report `FAIL`, `UNCHECKED`, or
`AUTHOR_INPUT_NEEDED` and do not mark the manuscript ready.

For orchestrator workspaces, treat these files as required final gates:

- `audits/manuscript_quality_audit.json`
- `audits/figure_consistency_audit.json`
- `diagnostics/profile_evidence_strength_audit.json` or the legacy
  `diagnostics/mechanism_evidence_strength_audit.json` during migration
- `audits/scientific_maturity_audit.json`

Each must report `PASS`.

## Abbreviation Audit

Build an abbreviation inventory from title, abstract, keywords, main text,
tables, captions, declarations, and appendices when available.

Check:

- First use in the abstract is defined unless the abbreviation is a standard
  unit, chemical formula, dataset name, model name, or journal-accepted term.
- First use in the main text is defined again when the abstract is separate.
- The same abbreviation always maps to the same expansion.
- The same expansion does not appear under multiple abbreviations.
- Plural and possessive forms are consistent.
- Abbreviations in figures, tables, captions, and appendices are defined in the
  caption, footnote, or nearby text when needed.
- Nonstandard abbreviations in the title, highlights, and keywords are avoided.
- User-defined model names are introduced before first use.

Safe fixes:

- Expand an abbreviation at first use when the expansion already appears in the
  manuscript or supplied notes.
- Rewrite avoidable parenthetical wording into natural prose while preserving
  the information inside the parentheses.
- Standardize capitalization and hyphenation of an abbreviation that is already
  defined.

Manual items:

- Missing expansion that the manuscript never defines.
- Ambiguous abbreviation with several possible expansions.
- Abbreviations embedded in images, equations, fields, or citation-manager
  content.

## Citation Audit

Check every in-text citation and every reference-list entry.

Required script gate:

```bash
python ../windenergy-citation/scripts/windenergy_citation.py --audit MANUSCRIPT.docx --bib REFERENCES.bib --output audit.json --markdown audit.md
```

- Store `audit.json` in the run folder.
- If `audit.json` is missing, mark citation integrity `UNCHECKED`.
- If any reference has `FAIL` or `UNCHECKED`, the manuscript cannot be reported
  ready for submission.
- If the script returns a nonzero exit code, report citation integrity as
  `FAIL` or `UNCHECKED` using the per-reference table.

Required checks:

- Every in-text citation resolves to exactly one reference-list entry.
- Every reference-list entry is cited in the manuscript or flagged as uncited.
- Numbered citations increase consistently after renumbering.
- Citation ranges and grouped citations are valid.
- Claims with quantitative results, datasets, baselines, physical mechanisms,
  and method comparisons have direct citation support when they rely on prior
  work.
- Added target-journal citations support a specific manuscript claim.
- DOI, title, year, journal, volume, pages, and article number match verified
  metadata when metadata is available.
- Preprints, conference papers, datasets, and standards are labeled correctly.
- The target-journal citation coverage check is updated after any reference
  edit.

Safe fixes:

- Correct a citation number when the renumbering map is explicit and complete.
- Remove duplicated citation markers when both point to the same reference and
  no support is lost.
- Correct obvious reference formatting based on verified DOI metadata.

Manual items:

- Adding new citations.
- Removing references.
- Replacing a weak source with a stronger source.
- Changing claim wording because a cited source does not support it.
- Any citation-manager field that cannot be edited safely.

## Required Output

Report:

- Abbreviation inventory with status: defined, undefined, inconsistent, or
  manual.
- Citation integrity table with status: pass, fail, unchecked, or manual.
- Profile-driven citation and literature-coverage notes.
- Safe tracked fixes already applied.
- Manual author decisions.
