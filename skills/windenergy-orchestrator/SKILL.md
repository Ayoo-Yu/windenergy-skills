---
name: windenergy-orchestrator
description: >-
  End-to-end renewable-energy manuscript orchestration for Applied Energy and
  related journals. Use when the user wants to write a full paper from an
  experiment folder, run a repeatable benchmark writing workflow, coordinate
  windenergy-writing, windenergy-academic-search, windenergy-figure,
  windenergy-citation, windenergy-submission, and windenergy-polishing, or produce
  a complete LaTeX manuscript package with evidence, citation, and submission
  audits.
---

# Renewable Orchestrator

Use this skill as the main entry point for full-paper generation and repeatable
benchmark runs in the renewable skill suite.

When a workspace already exists, first read `project_state.json`,
`decision_log.md`, and `task_queue.md`. Treat them as the durable workbench
state for the thread. Resume from `project_state.json.next_action`, preserve
decisions recorded in `decision_log.md`, and merge queued follow-up work from
`task_queue.md` before choosing the next stage.

Before writing generated files, load `../_shared/core/output-run-folders.md`
unless the user has supplied an explicit workspace path. Put all artifacts in a
dedicated workspace.

Load `../_shared/core/quality-principles.md`,
`../_shared/core/narrative-principles.md`, and
`../_shared/core/fragment-contract.md` before any full-paper workflow,
benchmark run, reviewer-comment diagnosis, or final readiness decision.

## Modes

- `full-paper`: build a complete manuscript package from an experiment folder.
- `benchmark-run`: run the fixed mechanism-diagnosis paper benchmark for
  repeatable suite testing.

## Required References

Load these files as needed:

- `references/workflow.md` for the stage sequence and skill handoffs.
- `references/workspace-contract.md` for workspace layout and artifact names.
- `references/gates.md` for PASS, FAIL, and UNCHECKED rules.
- `references/benchmark-mechanism-paper.md` for the wind-power mechanism paper
  benchmark.

## Workflow

1. Initialize or validate the workspace with `scripts/init_workspace.py` and
   `scripts/validate_workspace.py`.
2. For existing workspaces, refresh workbench state with
   `scripts/update_workspace_state.py` before resuming stage work. For legacy
   workspaces, run `scripts/init_workspace.py --init-missing --workspace
   WORKSPACE` to create only missing workbench control files.
3. Create or read `workflow_profile.json`. Record paper type, topics, journal,
   routing confidence, profile source, loaded fragments, disabled fragments,
   routing notes, and quality thresholds.
4. If the target journal is Applied Energy and the topic is wind-power
   forecasting, probabilistic wind forecasting, prediction intervals,
   calibration, or grid-risk forecasting, register the bundled style-learning
   profile in `workflow_profile.json` and load it before downstream handoffs:
   `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/learned_style_digest.md`,
   `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/style_profile.yaml`,
   `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/figure_style.yaml`,
   `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/visual-profile/visual_figure_style_digest.md`,
   and `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/visual-profile/visual_figure_style.yaml`.
   Pass these paths to writing, polishing, figure, and reviewer stages as the
   Applied Energy wind-forecasting constraint layer.
5. Route outline, claim evidence mapping, manuscript drafting, and refinement
   through `windenergy-writing`.
6. Route literature discovery and candidate reference pools through
   `windenergy-academic-search`.
7. Route figure selection, captioning, and figure-text checks through
   `windenergy-figure`.
8. Run `scripts/audit_writing_quality.py` after polishing and before final
   manuscript maturity audits. This blocks draft residue, abstract number
   overload, weak section roles, method-definition gaps, confusing alpha and
   target-coverage wording, method citation gaps, undefined process labels,
   repeated disclaimer phrasing, Results and Discussion overlap, weak Related
   Work to Discussion dialogue, and workflow-derived table language.
9. Run `scripts/audit_manuscript_quality.py` before final audits. Pass the
   profile when available. This creates manuscript quality, figure consistency,
   profile evidence strength, and scientific maturity audits. Do not hand-write
   a PASS maturity audit.
10. Route final citation integrity through `windenergy-citation`.
11. Route final readiness and journal compliance through `windenergy-submission`.
12. Use `windenergy-polishing` only for safe `.docx` tracked edits after a LaTeX
   manuscript exists.
13. Refresh `project_state.json` and `artifact_index.json` with
    `scripts/update_workspace_state.py`, then collect the final manifest with
    `scripts/collect_outputs.py`.

## Red Lines

- Do not use paper-orchestra as a runtime dependency or as a substitute final
  quality gate. Its workspace and gate ideas are a design source only.
- Do not continue through a local paper-workflow fallback when this renewable
  skill is requested. If the renewable skill files are not exposed in the
  current session, stop the run and report `AUTHOR_INPUT_NEEDED` with the exact
  missing skill path.
- Do not report a manuscript as ready unless citation audit and submission audit
  both pass and the general scientific maturity gate has no unresolved blocking
  issues.
- Do not report a manuscript as ready when workbench control files are missing,
  invalid, or inconsistent with the stage validator.
- Do not proceed from polishing to citation or submission readiness when
   `audits/writing_quality_audit.json` has unresolved draft residue,
  narrative, section-role, terminology, method-citation, undefined-process, or
  table-language issues.
- Do not lose user steering or queued work. Record durable author decisions in
  `decision_log.md` and next tasks in `task_queue.md`.
- Do not apply a topic, journal, or manuscript-specific rule unless the active
  profile loads that fragment with sufficient confidence.
- Do not report a full manuscript as ready when it has empty or table-only
  sections, lacks profile-required setup or method details, lacks figure data
  maps for quantitative figures, leaves internal workflow artifact language in
  the main text, has unresolved `NARRATIVE_WARNING` in foreground sections, or
  uses claims stronger than the available diagnostics.
- Do not report a target-journal manuscript as ready when required declaration
  sections are missing, or when figure visual-contract metadata reports
  unresolved dual-axis, palette, uncertainty, label, reference-line, subset
  selection, or low-support warnings.
- Do not fabricate citations, DOI metadata, experimental results, author
  details, funding, conflicts, data rights, or journal requirements.
- Do not edit `.docx` files outside `windenergy-polishing`.
