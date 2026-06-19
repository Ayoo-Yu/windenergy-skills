# Renewable Orchestrator Workspace Contract

The workspace is self-contained and repeatable.

## Layout

```text
workspace/
  project_state.json
  decision_log.md
  task_queue.md
  artifact_index.json
  automation_recipes.md
  workflow_profile.json
  inputs/
    idea.md
    experimental_log.md
    template.tex
    conference_guidelines.md
    figures/
  diagnostics/
    source_code_evidence_register.md
    claim_evidence_map.md
    mechanism_diagnostics.md
    profile_evidence_strength_audit.json
    profile_evidence_strength_audit.md
    mechanism_evidence_strength_audit.json
    mechanism_evidence_strength_audit.md
  outline/
    outline.json
  literature/
    candidate_references.md
    refs.bib
    search_log.md
  figures/
    captions.json
    selected_figures.md
    figure_text_audit.md
    figure_data_map.json
  drafts/
    paper.tex
    paper_polished.tex
  refinement/
    worklog.json
  audits/
    polishing_audit.md
    writing_quality_audit.json
    writing_quality_audit.md
    writing_revision_plan.md
    manuscript_quality_audit.json
    manuscript_quality_audit.md
    figure_consistency_audit.json
    figure_consistency_audit.md
    scientific_maturity_audit.md
    scientific_maturity_audit.json
    citation_audit.json
    citation_audit.md
    submission_audit.md
  final/
    paper.tex
    paper.pdf
    refs.bib
    final_manifest.json
```

## Status File

Scripts may write `orchestrator_status.json` at the workspace root. It records
the current status, checked paths, missing artifacts, and warnings. Status values
are:

- `PASS`
- `FAIL`
- `UNCHECKED`

## Workbench Control Files

The orchestrator workspace is also a durable workbench. These root-level files
must exist before ready status:

- `project_state.json`: current stage, stage status, next action, blocking
  items, queued tasks, author decision summary, validator status, and timestamp.
- `decision_log.md`: durable user steering, reviewer judgments, scope choices,
  and constraints that future runs must preserve.
- `task_queue.md`: queued work with status, trigger, task, and completion
  criteria.
- `artifact_index.json`: reviewable artifact index with path, type, stage,
  size, sha256, generated timestamp, and review status.
- `automation_recipes.md`: reusable thread automation recipes that only draft
  next actions or replies for author review.

`project_state.json` must use schema version `1` and contain:

- `schema_version`: `1`
- `project_status`: `active`, `blocked`, or `ready`
- `current_stage`: one of the windenergy-orchestrator stage names
- `stage_status`: `PASS`, `FAIL`, `UNCHECKED`, `AUTHOR_INPUT_NEEDED`,
  `NARRATIVE_WARNING`, `SECTION_WARNING`, `LANGUAGE_WARNING`, or
  `TONE_WARNING`
- `next_action`: one sentence describing the next resume step
- `blocking_items`: list of author input needs, external blockers, or failed
  stage sources
- `queued_tasks`: list derived from `task_queue.md`
- `author_decisions_summary`: durable decision excerpts from `decision_log.md`
- `updated_at`: ISO timestamp

Legacy workspaces may be upgraded with:

```bash
python scripts/init_workspace.py --init-missing --workspace WORKSPACE
```

This command creates only missing workbench control files. It must not edit
manuscript text, figures, citations, `.docx` files, or source materials.

## Workflow Profile

`workflow_profile.json` records the rules that are active for the current
manuscript. It must contain:

- `paper_type`
- `topics`
- `journal`
- `paper_type_confidence`
- `topic_confidence`
- `journal_confidence`
- `profile_source`
- `routing_notes`
- `loaded_fragments`
- `disabled_fragments`
- `quality_thresholds`

Topic routing uses these thresholds:

- below `0.70`: core and paper-type rules only
- `0.70` to below `0.85`: lightweight topic guidance
- `0.85` or higher: full topic guidance

Missing profile information makes topic-specific and journal-specific checks
`UNCHECKED`; it must not silently activate benchmark rules.

A profile-driven full-paper run must use this top-level contract. A nested
`profile` object may be read for backward diagnosis, but missing top-level
contract fields or workflow mappings to local fallback modules are blocking
profile contract failures.

## Input Rules

- Text inputs must decode as UTF-8.
- `template.tex` must contain a LaTeX document skeleton.
- `conference_guidelines.md` must name the target journal or journal class.
- `inputs/figures/` may contain PNG, PDF, JPG, JPEG, or SVG.
- Raw experiment files copied from the source folder must be preserved under
  `inputs/source_materials/` when available.

## Final Readiness

The final package is ready only when:

- `project_state.json`, `decision_log.md`, `task_queue.md`,
  `artifact_index.json`, and `automation_recipes.md` exist and pass the
  workbench state gate.
- `final/paper.tex` exists.
- `final/paper.pdf` exists.
- `final/refs.bib` or `literature/refs.bib` exists.
- `workflow_profile.json` exists for profile-driven workflows, or the final
  audit explicitly records why no profile was available.
- `diagnostics/source_code_evidence_register.md` exists when source-code
  evidence is part of the active profile.
- `drafts/paper_polished.tex` exists.
- `audits/polishing_audit.md` exists and contains no unresolved `Claim risk`
  or `AUTHOR_INPUT_NEEDED`.
- `audits/writing_quality_audit.json` exists and reports `PASS`, and
  `audits/writing_revision_plan.md` has no unresolved blocking writing rewrite
  items.
- `audits/manuscript_quality_audit.json` exists and reports `PASS`.
- `audits/figure_consistency_audit.json` exists and reports `PASS`.
- `diagnostics/mechanism_evidence_strength_audit.json` exists and reports
  `PASS`.
- `audits/scientific_maturity_audit.md` exists and reports no blocking `FAIL`,
  `UNCHECKED`, or unresolved `AUTHOR_INPUT_NEEDED`.
- `audits/citation_audit.json` exists and contains no `FAIL` or `UNCHECKED`
  reference items.
- `audits/submission_audit.md` exists and does not report unresolved `FAIL` or
  `UNCHECKED` status for required checks.
- `final/final_manifest.json` is generated by `scripts/collect_outputs.py` and
  does not contradict the stage validator.
- `project_state.json` does not claim `ready` while any required stage is
  missing, `FAIL`, or `UNCHECKED`.

Root-level manifests created by fallback workflows are diagnostic artifacts
only. They cannot establish ready status for a windenergy-orchestrator run.

## Manuscript Quality Audits

Run the writing-quality audit before deterministic manuscript maturity gates:

```bash
python scripts/audit_writing_quality.py WORKSPACE
```

This audit checks draft residue, abstract number density, central argument
alignment, section-role integrity, paragraph function flow, benchmark method
definition depth, alpha versus target-coverage terminology, repeated cautious
phrasing, method citation binding, undefined process labels, Related Work gap
strength, Results storyline, Discussion depth, and table claim language. Any
`FAIL`, `UNCHECKED`, `NARRATIVE_WARNING`, `SECTION_WARNING`,
`LANGUAGE_WARNING`, or `TONE_WARNING` blocks ready status.

Run:

```bash
python scripts/audit_manuscript_quality.py WORKSPACE
```

The script parses the manuscript, strips figure and table environments for
prose checks, reads `workflow_profile.json` when available, writes the new audit
outputs, and blocks ready status for empty subsections, missing profile-required
details, figure data-map gaps, missing figure style metadata, internal workflow
artifact language, missing target-profile declarations, unresolved figure
visual-contract warnings, unresolved foreground narrative warnings, and claims
stronger than the available diagnostics.

For profile-driven workflows, `figure_data_map.json` should include figure
portfolio role, style metadata, axis metadata, source data, plotted values,
expected values, and low-support condition metadata when relevant. When a
figure uses a secondary axis, displayed subset, reference line, heatmap palette,
or low-support subgroup, also record visual-contract metadata such as
dual-axis justification, subset-selection rationale, reference-line source,
colorblind-safe palette status, uncertainty visibility, unexplained labels, and
visual-warning status.
