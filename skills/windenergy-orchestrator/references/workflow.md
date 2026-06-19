# Renewable Orchestrator Workflow

This workflow borrows the workspace, stage, gate, and refinement mechanisms from
paper-orchestra, but it does not depend on paper-orchestra at runtime and does
not accept paper-orchestra as a substitute final quality gate.

Load `../_shared/core/quality-principles.md`,
`../_shared/core/narrative-principles.md`, and
`../_shared/core/fragment-contract.md` for every full-paper or benchmark run.
Use reviewer comments as quality diagnostics and abstract them into transferable
checks rather than copying paper-specific requests into every future workflow.

## Stage 0: Intake

Run `scripts/init_workspace.py` if the workspace does not exist. Then run
`scripts/validate_workspace.py`.

Required inputs:

- `inputs/idea.md`
- `inputs/experimental_log.md`
- `inputs/template.tex`
- `inputs/conference_guidelines.md`
- `inputs/figures/`

If any required input is missing, stop and mark the stage `UNCHECKED`.

Create or read `workflow_profile.json` before drafting. The profile records
paper type, topics, journal, routing confidence, profile source, loaded
fragments, disabled fragments, routing notes, and quality thresholds. Topic
confidence below `0.70` loads only core and paper-type rules. Topic confidence
from `0.70` to below `0.85` loads lightweight topic guidance. Topic confidence
at `0.85` or above loads full topic guidance.

## Stage 0.5: Workbench Resume

Before any stage work in an existing workspace, read `project_state.json`,
`decision_log.md`, and `task_queue.md`. Use `project_state.json.next_action` as
the resume target unless the user gives a newer instruction.

Run:

```bash
python scripts/update_workspace_state.py WORKSPACE
```

This refreshes `project_state.json` and `artifact_index.json` from the
workspace validator, stage validator, and output collector. For legacy
workspaces without control files, first run:

```bash
python scripts/init_workspace.py --init-missing --workspace WORKSPACE
```

Merge new user steering into `decision_log.md` when it changes durable paper
constraints, reviewer judgments, scope, journal targeting, or evidence limits.
Add queued follow-up work to `task_queue.md` with trigger and completion
criteria. Do not use automation recipes to send external messages; create
drafts or next actions for author review.

## Stage 1: Outline and Claim Map

Use `windenergy-writing` for:

- Profile-selected article architecture.
- Contribution framing.
- Profile-selected storyline and evidence logic.
- `outline/outline.json`.
- `diagnostics/claim_evidence_map.md`.
- `diagnostics/source_code_evidence_register.md` when source-code evidence is
  active.

The outline must connect every major claim to experiment-log evidence or a
diagnostic artifact.
When method definitions, metric definitions, statistical tests, ramping rules,
predictor diagnostics, figure meaning, or judgment rules are uncertain, inspect
the source code, configs, CSV, JSON, and existing revision scripts before
drafting.
The outline stage must also classify major claims by strength using the shared
claim strength control ladder and apply high-impact narrative control to
foreground sections.

## Stage 2: Diagnostics

Use deterministic scripts or existing project result files to produce
`diagnostics/mechanism_diagnostics.md`.

For benchmark-specific work, load the manuscript fragment that defines the
required diagnostics. Generic full-paper workflows must not inherit benchmark
diagnostic requirements.

## Stage 3: Literature

Use `windenergy-academic-search` for discovery and candidate metadata. Use only
English scholarly sources, DOI records, CrossRef, OpenAlex, arXiv, Semantic
Scholar, or publisher pages.

Expected outputs:

- `literature/candidate_references.md`
- `literature/refs.bib`
- `literature/search_log.md`

Do not treat discovery as final citation verification.

## Stage 4: Figures

Use `windenergy-figure` for figure selection, captions, and figure-text checks.

Expected outputs:

- `figures/selected_figures.md`
- `figures/captions.json`
- `figures/figure_text_audit.md`
- `figures/figure_data_map.json` for quantitative figures

The figure stage must apply the shared figure professionalism rules: journal
serif font, minimum 8 pt text, stable category colors, consistent line widths,
unambiguous axes, conclusion-first captions, and figure-table-text consistency.
The figure stage must also record figure portfolio roles, style metadata,
axis-interpretation choices, visual-contract metadata, and low-support
condition evidence when relevant. Visual-contract metadata covers dual-axis
justification, colorblind-safe palette status, uncertainty visibility,
unexplained labels, reference-line sources, subset-selection rationale, and
low-support visual warnings.
For workflow figures, include the research object, comparison unit, method
families or alternatives, diagnostic layer, and boundary analysis. Keep code
filenames out of the main figure.

## Stage 5: Full Draft

Use `windenergy-writing` to generate a complete LaTeX manuscript in
`drafts/paper.tex`. The draft must follow the target journal profile and the
workspace outline.

Required sections:

- Introduction
- Related Work
- Methodology
- Experimental Setup
- Results
- Discussion
- Conclusion

## Stage 6: Polishing

Use `windenergy-polishing` after the full draft and before citation or submission
audit. The polishing stage produces:

- `drafts/paper_polished.tex`
- `audits/polishing_audit.md`

The audit must check profile style, academic English, narrative force in
foreground sections, unsupported absolute claims, parenthetical structures,
abbreviation first use, method names, metric names, numeric fidelity, and
citation-key preservation. Any unresolved `Claim risk`, `NARRATIVE_WARNING`, or
`AUTHOR_INPUT_NEEDED` blocks ready status when it affects final readiness.

## Stage 6.5: Writing Quality Review

Run `scripts/audit_writing_quality.py` after polishing and before manuscript
quality audits. This stage is separate from technical readiness. It asks
whether the polished manuscript reads like a mature paper rather than a
complete workflow report.

Expected outputs:

- `audits/writing_quality_audit.json`
- `audits/writing_quality_audit.md`
- `audits/writing_revision_plan.md`

The audit must block unresolved draft residue, author placeholders, temporary
journal or workspace language, abstract number overload, confusing alpha versus
target-coverage wording, repeated cautious disclaimers, missing benchmark
method update rules, named methods without citation or self-defined status,
undefined numbered process labels, weak Related Work to Discussion dialogue,
Results and Discussion overlap, unclear figure or table claim language, and
section-role collisions.

## Stage 7: Refinement

Use `windenergy-writing` for content-level refinement. Each refinement iteration
must record:

- Review findings.
- Changes requested.
- Evidence used.
- Accepted or rejected decision.

Store this under `refinement/`.

## Stage 8: Scientific Maturity Audit

Run `scripts/audit_manuscript_quality.py` before final citation and submission
audits. Pass `--profile workflow_profile.json` when the profile exists. The
script writes:

- `audits/manuscript_quality_audit.json`
- `audits/manuscript_quality_audit.md`
- `audits/figure_consistency_audit.json`
- `audits/figure_consistency_audit.md`
- `diagnostics/mechanism_evidence_strength_audit.json`
- `diagnostics/mechanism_evidence_strength_audit.md`
- `audits/scientific_maturity_audit.json`
- `audits/scientific_maturity_audit.md`

The audit must contain status, evidence, open issues, and downstream impact for:

- Claim strength and evidence chain.
- Method reproducibility and parameter disclosure.
- Experimental setup completeness.
- Figure professionalism and figure text audit.
- Profile-required display-item coverage and figure portfolio completeness.
- Target-profile declaration integrity.
- Title strength, profile-control visibility, result granularity, internal
  artifact cleanup, and low-support condition evidence.
- Literature coverage and journal fit when a profile activates those checks.
- Empty sections, placeholders, undefined abbreviations, and unsupported
  conclusion claims.
- Empty or table-only subsections, profile-required setup fields, methodology
  fields, future-work evidence gaps, figure data maps, figure style metadata,
  figure visual-contract metadata, reference pool size when a journal profile
  activates it, and profile evidence strength.

Use `PASS`, `FAIL`, `UNCHECKED`, `AUTHOR_INPUT_NEEDED`,
`NARRATIVE_WARNING`, and `SECTION_WARNING`. A blocking issue in this audit
prevents ready status.

## Stage 9: Final Audits

Use `windenergy-citation` for final citation audit. Use `windenergy-submission`
for final manuscript and journal readiness audit.

Expected outputs:

- `audits/citation_audit.json`
- `audits/citation_audit.md`
- `audits/submission_audit.md`

If any citation item is `FAIL` or `UNCHECKED`, final status is not ready.
If submission audit is missing, failed, or unchecked, final status is not ready.

## Stage 10: Final Package

Compile or place the accepted files under `final/`, then run
`scripts/collect_outputs.py`.

Expected outputs:

- `final/paper.tex`
- `final/paper.pdf`
- `final/refs.bib`
- `final/final_manifest.json`
