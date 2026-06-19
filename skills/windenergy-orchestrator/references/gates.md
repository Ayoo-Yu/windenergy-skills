# Renewable Orchestrator Gates

Each gate returns one of three states.

- `PASS`: required artifact exists and deterministic checks passed.
- `FAIL`: required artifact exists but violates a rule.
- `UNCHECKED`: required artifact or evidence is missing.
- `NARRATIVE_WARNING`: a checked foreground writing section lacks synthesis or
  take-home message.
- `SECTION_WARNING`: a checked section is structurally weak but factual.

## Required Gates

| Gate | Required artifact | Owner |
|---|---|---|
| workbench state | `project_state.json`, `decision_log.md`, `task_queue.md`, `artifact_index.json`, `automation_recipes.md` | windenergy-orchestrator |
| input | `inputs/idea.md`, `inputs/experimental_log.md`, template, guidelines | windenergy-orchestrator |
| profile | `workflow_profile.json` or explicit no-profile audit note | windenergy-orchestrator |
| outline | `outline/outline.json` | windenergy-writing |
| source evidence | `diagnostics/source_code_evidence_register.md` | windenergy-writing plus source inspection |
| claim evidence | `diagnostics/claim_evidence_map.md` | windenergy-writing |
| mechanism diagnostics | `diagnostics/mechanism_diagnostics.md` | windenergy-writing plus deterministic scripts |
| literature | `literature/refs.bib` and search log | windenergy-academic-search |
| figures | captions and figure-text audit | windenergy-figure |
| draft | `drafts/paper.tex` | windenergy-writing |
| polishing | `drafts/paper_polished.tex` and polishing audit | windenergy-polishing |
| writing quality | `audits/writing_quality_audit.json`, `audits/writing_quality_audit.md`, `audits/writing_revision_plan.md` | windenergy-orchestrator plus windenergy-writing |
| manuscript quality | `audits/manuscript_quality_audit.json` | windenergy-orchestrator |
| figure consistency | `audits/figure_consistency_audit.json` | windenergy-orchestrator plus windenergy-figure |
| mechanism evidence strength | `diagnostics/mechanism_evidence_strength_audit.json` | windenergy-orchestrator plus windenergy-writing |
| scientific maturity | `audits/scientific_maturity_audit.md` | windenergy-orchestrator plus windenergy-writing |
| citation audit | `audits/citation_audit.json` | windenergy-citation |
| submission audit | `audits/submission_audit.md` | windenergy-submission |
| final package | `final/paper.tex`, `final/paper.pdf`, manifest | windenergy-orchestrator |

## Hard Gate Rules

- Citation audit is mandatory before ready status.
- Submission audit is mandatory before ready status.
- Workbench state gate is mandatory before ready status.
- Source evidence register is mandatory before manuscript drafting.
- Polishing audit is mandatory before citation and submission audits.
- Writing quality audit is mandatory before citation and submission audits.
- General scientific maturity gate is mandatory before ready status.
- Manuscript quality, figure consistency, and mechanism evidence strength audits
  are mandatory before ready status.
- Any citation `FAIL` or `UNCHECKED` blocks ready status.
- Any required submission `FAIL` or `UNCHECKED` blocks ready status.
- Any manuscript quality, figure consistency, or mechanism evidence strength
  `FAIL`, `UNCHECKED`, `NARRATIVE_WARNING`, or blocking `SECTION_WARNING`
  blocks ready status.
- Any target-profile declaration `AUTHOR_INPUT_NEEDED`, `FAIL`, or `UNCHECKED`
  blocks ready status.
- Any figure visual-contract `FAIL` or `UNCHECKED` blocks ready status.
- Any unresolved `Claim risk` or `AUTHOR_INPUT_NEEDED` in polishing audit
  blocks ready status.
- Any `FAIL`, `UNCHECKED`, `NARRATIVE_WARNING`, `SECTION_WARNING`,
  `LANGUAGE_WARNING`, or `TONE_WARNING` in writing quality audit blocks ready
  status.
- Any unresolved blocking issue in `audits/scientific_maturity_audit.md` blocks
  ready status.
- Missing or invalid workbench control files block ready status.
- A `project_state.json` ready claim fails when any required stage is missing,
  `FAIL`, or `UNCHECKED`.
- A compiled PDF alone is not enough for ready status.
- paper-orchestra outputs may be used as comparison evidence, but never as a
  substitute for renewable citation audit or submission audit.
- A local paper-workflow fallback is not a valid windenergy-orchestrator run. If
  the requested renewable skill files are not exposed, stop and report
  `AUTHOR_INPUT_NEEDED`; do not create a ready manifest.
- A manifest that claims ready while any required renewable stage is missing,
  `FAIL`, or `UNCHECKED` is itself a blocking failure.

## General Scientific Maturity Gate

This gate uses `../_shared/core/quality-principles.md`,
`../_shared/core/narrative-principles.md`, `workflow_profile.json`, and the
loaded fragments. It is generic until the profile activates a paper-type, topic,
journal, or manuscript rule.

It checks:

- Claim strength control for title, abstract, contribution, results,
  discussion, and conclusion.
- Evidence chain completeness for each core claim.
- Method reproducibility, including parameters, assumptions, and implementation
  details when relevant.
- Experimental setup completeness, including data provenance, sampling,
  splits, inputs, targets, preprocessing, and exclusions when relevant.
- Figure professionalism, including font, minimum 8 pt text, line widths,
  color stability, colorblind-safe palette metadata, axis terminology, caption
  quality, dual-axis justification, uncertainty visibility, and
  figure-table-text consistency.
- Journal fit when a journal profile is active.
- Empty sections, placeholders, undefined abbreviations, unsupported future-work
  substitutions, and conclusion claims that introduce new evidence.
- The executable audit script must produce the scientific maturity status. Do
  not hand-write a PASS audit.
- Subsections with only a table or figure fail manuscript quality.
- Experimental Setup and Methodology must include the fields required by the
  active profile.
- Quantitative figures without `figure_data_map.json` are `UNCHECKED`.
- Plotted values that conflict with table or text values fail figure
  consistency.
- Strong mechanism or causal claims require profile-selected controls.
- Display-item and reference scale checks come from paper-type and journal
  fragments.
- When a journal profile is active, missing profile thresholds do not disable
  journal hard checks. The audit must apply the journal fragment defaults.
- Mechanism controls needed for a central claim must be visible in the main
  manuscript as a table, figure, or explicit results paragraph.
- Result granularity must match the advice level.
- Workflow figures must show the research object, comparison unit, alternatives,
  diagnostic layer, and boundary analysis when the profile calls for them.
- Low-support conditions need sample count, sample share, uncertainty, or
  sensitivity evidence, plus visual-warning metadata when shown as a subgroup,
  before supporting a strong boundary claim.
- Named external methods need a citation near first substantive mention or a
  clear statement that the manuscript defines the method.
- Numbered process labels such as stages, phases, and steps need reader-facing
  definitions before use.
- Target-journal manuscripts need required declaration sections according to
  the active profile.
- Internal workflow artifact names belong in a reproducibility statement or
  appendix, not repeated in the main article.

## Benchmark Gate Content

Benchmark-only requirements live in manuscript fragments. The wind conformal
benchmark is defined by `_shared/fragments/manuscript/wind-conformal-benchmark.md`
and must not be applied to generic full-paper workflows.
