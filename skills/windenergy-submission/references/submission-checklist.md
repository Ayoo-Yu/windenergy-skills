# Multi-Journal Submission Checklist

Use this checklist with `journal-profiles.md`. Default to `common-18` and then
apply the named journal profile.

## Required Inputs

- Target journal slug or `common-18`.
- Manuscript file, preferably `.docx` or `.tex`.
- Title page or author metadata.
- Abstract, keywords, highlights, figures, tables, captions, and references.
- Declarations: CRediT, data availability, competing interests, funding, and AI
  tool usage.
- Submission files: cover letter, graphical abstract, checklist, author bios, or
  separate artwork when the target profile requires them.

## Audit Items

After the audit, apply `revision-protocol.md` to every editable `.docx` file.
Safe exact text fixes must be written as tracked changes before final reporting.
Use `windenergy-polishing` as the tracked-edit engine for main manuscript
changes and submission-document wording changes.
For main-manuscript word-count failures, also apply
`manuscript-compression-protocol.md`.
For final manuscript checks, also apply `final-manuscript-audit.md`.
For content maturity, also apply `../_shared/core/quality-principles.md` and
`../_shared/core/narrative-principles.md`.
For orchestrator workspaces, require manuscript quality, figure consistency,
profile evidence strength, and scientific maturity audit JSON files to report
`PASS`.

### Article Type And Length

- Confirm article type is accepted by the target journal.
- Count words or pages according to the target profile.
- Mark review articles that require invitation or editor approval.
- Record transfer risk when the manuscript is far outside the target length.

### Abstract And Keywords

- Check target abstract limit.
- Check keyword count.
- Flag undefined abbreviations in abstract and title when the target profile
  requires it.
- Confirm the abstract states purpose, method, main result, and conclusion.

### Highlights

- Check whether highlights are required or encouraged.
- Use 3 to 5 bullets.
- Keep each bullet at or below 85 characters including spaces.
- Avoid generic statements and unsupported quantitative claims.

### References And Citations

- Check target citation style: numbered, author-year, superscript numbered, APA
  7th, or flexible.
- Check reference count only when the active profile gives a limit or target.
- When a specific target journal is named, count references published in that
  journal and cited in the manuscript text.
- Require at least 10 cited references from the target journal.
- Count only verified journal-title matches or DOI metadata matches. Do not
  count uncited bibliography entries.
- Do not prune references or renumber citations automatically.
- Flag missing DOI, missing cited references, uncited references, and active
  profile citation-coverage gaps.
- Run final citation integrity checks with `final-manuscript-audit.md` before
  reporting the manuscript ready for submission.
- The final citation check must produce `audit.json` from
  `../windenergy-citation/scripts/windenergy_citation.py --audit`. Without that
  file, mark citation readiness `UNCHECKED`.
- Any `FAIL` or `UNCHECKED` item in `audit.json` blocks a ready-for-submission
  conclusion.

### Abbreviations

- Build an abbreviation inventory for abstract and main text.
- Check first-use definitions, consistency, and undefined abbreviations.
- Keep necessary technical parentheses and rewrite avoidable parenthetical
  sentence structures into natural prose while preserving their information.
- Mark missing or ambiguous expansions as `AUTHOR_INPUT_NEEDED`.

### Review Mode

- For double-anonymized journals, check author names, affiliations,
  acknowledgements, funding, self-citations, file metadata, repository links,
  and supplementary files.
- For single-anonymized journals, keep author information when required by the
  submission system.

### Figures And Tables

- Check figure and table count limits when the target profile has them.
- For full-length empirical manuscripts, use the display-item target supplied by
  the active article-type or journal profile.
- Verify editable tables.
- Verify separate artwork files and resolution when required.
- Flag graphical abstract requirements.
- Flag color accessibility and excessive text inside figures.
- Confirm figure font, minimum 8 pt text, line width consistency, stable
  category colors, axis terminology, conclusion-first captions, and
  figure-table-text consistency when manuscript figures are supplied.
- Confirm figure portfolio completeness for the claim types activated by the
  profile.
- Confirm metric-specific axis conventions only when the active topic fragment
  defines them.
- Confirm main-text mentions of figures, tables, appendices, and numbered
  citation markers are colored blue `#0000FF` in `.docx` outputs when the user
  requests that house style.

### Content Maturity

- Check for empty sections, placeholders, undefined core terms, unresolved TODO
  markers, and template residue.
- Check whether title, abstract, contributions, results, discussion, and
  conclusion use evidence-calibrated claim strength.
- Check whether title, abstract, highlights, contribution, and conclusion retain
  high-impact narrative structure when the section calls for it.
- Check whether the title strength is compatible with evidence boundaries,
  especially when central evidence is partial, aggregate, proxy-based, or
  missing direct controls.
- Check whether each core claim has a traceable evidence chain.
- Check whether experimental setup and methodology include the profile-relevant
  detail needed for an expert reviewer to assess reproducibility.
- Check whether Related Work covers the target journal's application domain,
  method family, evaluation criteria, and closest alternatives.
- Check whether advice-level claims are downgraded or supported by matching
  result granularity.
- Check whether low-support conditions include sample count, sample share,
  uncertainty, or sensitivity before supporting strong boundary claims.
- Check whether internal workflow artifact names are removed from the main
  article or moved to a reproducibility statement or appendix.
- A claim-evidence mismatch, missing method configuration, missing data
  provenance, or unresolved content maturity issue blocks a ready conclusion.
- A draft that fails the active journal or article-type length profile blocks a
  ready conclusion.
- Empty or table-only subsections block a ready conclusion.
- Future work that lists diagnostics required for the current central claim
  blocks a ready conclusion.

### Declarations

- CRediT: ensure all authors are covered by standard roles.
- Data availability: match actual data rights and repository status.
- Competing interests: include a declaration or no-conflict statement.
- Funding: include grant names, numbers, and sponsor role only when supplied.
- AI declaration: assess AI use for every journal; draft final wording only
  after the user provides tool name and purpose.

### Journal-Specific Files

- Cover letter: required for Renewable Energy, Energy Conversion and Management,
  and Pattern Recognition in the local profiles.
- Pattern Recognition: cover letter must answer journal-specific editor
  questions.
- Applied Soft Computing: graphical abstract and author biography are required
  in the local profile.
- SETA: checklist and institutional corresponding-author email are required in
  the local profile.

## Output Status

Use `PASS`, `FAIL`, `UNCHECKED`, and `AUTHOR_INPUT_NEEDED`.

## Manual Action Policy

Use `AUTHOR_INPUT_NEEDED` for missing author facts, grants, affiliations,
conflicts, AI usage, data rights, cover-letter facts, graphical abstract,
author photos, figure resolution, citation pruning, target-journal citation
additions, and anonymization decisions.

Do not put safe exact wording fixes in this manual category. Apply them with
tracked changes and list them under `Applied tracked revisions`.
