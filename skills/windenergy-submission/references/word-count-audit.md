# Word Count And Reference Count Audit

Use `journal-profiles.md` first. The target journal controls the limit.

## Default Compatibility Targets

- `common-18`: 5000 to 7000 words for full articles and 7000 to 9000 words for
  reviews.
- `applied-energy`: use the renewable suite readiness floor of 5000 to 7000
  main-body words from Introduction through Conclusion when the journal profile
  has no fixed local word limit.
- `renewable-energy`: 4000 to 6000 words for research papers, max 10000 words
  for invited reviews, max 50 references.
- `energy`: 5000 to 7000 words for full articles, 7000 to 9000 words for
  reviews.
- `energy-conversion-management`: max 9000 words for full articles, max 12000
  words for reviews, max 15 figures and tables for full articles.
- `information-sciences`: experimental papers up to 40 pages and 8 figures;
  theoretical papers up to 45 pages and 10 figures.
- `ijepes`, `knowledge-based-systems`, and `neurocomputing`: page limits
  dominate in the local profiles.
- `pattern-recognition`: local profile requests 35 to 55 references.

## Counting Rules

- Report the counting basis used by the target journal.
- For renewable suite full-paper readiness, report the main-body count from
  Introduction through Conclusion separately from the abstract and declarations.
- Exclude references and appendices only when the target profile says to do so.
- Count the abstract separately.
- Count references by entries in the reference list.
- Count cited target-journal references when a target journal is named.
- Require at least 10 cited references from the target journal.
- Do not delete references or renumber citations automatically.
- If the main manuscript exceeds the target and a `.docx` is available, run
  `manuscript-compression-protocol.md` and hand the file to
  `windenergy-polishing` before final reporting.

## Audit Output

```text
## Word And Reference Audit

Target journal: [slug]
Article type: [type]
Counting basis: [words/pages/exclusions]

Body length: [N]
Target limit: [limit]
Status: PASS / FAIL / UNCHECKED

Abstract length: [N]
Abstract limit: [limit]
Status: PASS / FAIL / UNCHECKED

References: [N]
Reference limit: [limit or no explicit limit]
Status: PASS / FAIL / UNCHECKED

Target-journal cited references: [N]
Target-journal coverage target: at least 10
Status: PASS / FAIL / UNCHECKED

Manual items:
- [AUTHOR_INPUT_NEEDED item]
```

## Reduction Guidance

- Shorten literature review synthesis before removing method details.
- Preserve reproducibility details, datasets, baselines, metrics, uncertainty,
  and physical constraints.
- Move extended ablations, sensitivity analyses, and large tables to
  supplementary material only when the target journal allows it.
- For Renewable Energy reference overages, ask the author to approve pruning
  priorities before changing the reference list.

## Required Revision Output

When the manuscript is over the limit:

- Apply safe tracked compression edits to the main manuscript when possible.
- Use the existing `windenergy-polishing` Word Output Protocol for manuscript
  edits.
- Report approximate words removed.
- Keep reference pruning and new citations as manual author decisions.
- If no compression is applied, explain why with `Applied tracked manuscript
  compression: 0`.
