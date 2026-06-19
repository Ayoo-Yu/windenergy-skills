---
name: windenergy-figure
description: >-
  Create, audit, or polish publication-grade figures for renewable energy, wind
  power, energy forecasting, and AI-for-energy manuscripts in Python or R. Use
  when the user asks for wind roses, power curves, forecast-vs-actual plots,
  residual/error distributions, ablation heatmaps, wake/layout diagrams, model
  comparison charts, graphical abstracts, artwork resolution checks, or
  Elsevier target-journal figure checks. If the user has not chosen Python or R,
  ask "Python or R?" before writing plotting code.
---

# Renewable Figure Workflow

Use this skill to produce figures that support manuscript claims without
overloading the reader.

Before writing generated files, load `../_shared/core/output-run-folders.md`
and create a run folder for this invocation. Put figures, source data snapshots,
plot scripts, QA reports, and derived assets in that run folder.

Also load `../_shared/core/quality-principles.md` and
`../_shared/core/fragment-contract.md` before creating, auditing, or polishing
figures for a manuscript package. When `workflow_profile.json` exists, load
only the profile-selected paper-type, topic, journal, and manuscript fragments.

## Figure Contract

Before plotting, identify:

1. The claim the figure supports.
2. The data source and units.
3. The comparison baseline or physical reference.
4. The target output format: SVG or PDF for vectors, PNG/TIFF at journal-grade
   resolution for raster exports.
5. The backend: Python or R.

For every quantitative manuscript figure, write `figure_data_map.json` in the
figure run folder or orchestrator workspace. Record source file, filters,
groups, metric names, transformations, plotted values, and expected table or
text values when applicable. Also record visual-contract metadata when relevant:
dual-axis justification, colorblind-safe palette status, uncertainty or
confidence-interval visibility, unexplained labels, reference-line sources,
displayed-subset selection basis, and low-support subgroup warnings.

For full-paper workflows, maintain a figure portfolio plan. Display-item count,
required figure roles, and any figure-count target must come from the active
paper-type or journal profile. Without an active profile, report figure
portfolio adequacy as `UNCHECKED` rather than importing a benchmark rule.

## Common Figure Types

- Power curve with operating-region annotations.
- Wind rose or direction-speed distribution.
- Forecast versus actual power over time.
- Error distribution by horizon, season, wind-speed bin, or operating region.
- Model comparison with confidence intervals.
- Ablation or robustness heatmap.
- Wake/layout schematic or farm-level spatial graph.
- Reliability diagram or prediction interval plot when the active topic needs
  uncertainty evaluation.

## Style Defaults

- Use Times New Roman or a journal-compatible serif font by default for
  journal figures.
- Keep figure text at least 8 pt at final printed size.
- Use 9 to 11 pt for main figure text when space allows.
- Use consistent line widths, marker sizes, panel labels, axis styles, and
  legend placement across a figure set.
- Use colorblind-safe palettes; avoid decorative gradients.
- Keep semantic category colors stable across figures. For example, static and
  dynamic method families must keep the same colors throughout one manuscript.
- Prefer no more than two dominant semantic colors unless the data structure
  requires more.
- Put panels in claim order: overview, comparison, mechanism, robustness.
- Show uncertainty when the claim depends on statistical stability.
- Keep captions conclusion-first and labels specific: site, horizon, metric,
  unit, target quantity, and sample period.
- Avoid crowded labels, ambiguous axes, color-meaning drift, and captions that
  only restate the visual pattern.
- Use topic fragments for metric-specific axis conventions.
- For low-support regimes or subgroups, show sample count, sample share,
  uncertainty, or sensitivity before using the figure to support a strong
  boundary claim.
- Avoid dual axes unless both quantities share a justified interpretation and
  the map records the justification.
- If a figure displays only a subset of possible method pairs, regimes, or
  conditions, state the selection basis in the caption and figure map.
- For workflow figures, use a clear but informative publication template. Show
  the research object, fair comparison unit, alternatives, diagnostic layer, and
  boundary analysis when the profile calls for a workflow figure. Keep code
  filenames out of the main figure.

## Figure Text Audit

For each manuscript figure, write or update `figure_text_audit.md` with:

1. The claim supported by the figure.
2. The data source, metric, units, and sample definition.
3. The visual encoding and category color mapping.
4. The manuscript sentences, tables, or captions that cite the figure.
5. Any inconsistency between figure, table, caption, and main text.
6. Figure portfolio role and whether the overall manuscript satisfies the
   profile's display-item expectation.
7. Style metadata: font family, minimum font size, line width, palette, and
   legend policy.
8. Visual-contract metadata: dual-axis use, palette accessibility,
   uncertainty visibility, label definitions, reference-line source,
   subset-selection basis, and low-support warning status.
9. Status: `PASS`, `FAIL`, `UNCHECKED`, or `AUTHOR_INPUT_NEEDED`.

Run the orchestrator figure consistency audit when working inside a full-paper
workspace. Missing `figure_data_map.json` makes quantitative figures
`UNCHECKED`; plotted values that conflict with tables make the figure `FAIL`.
Missing style metadata, missing profile-required figure portfolio roles, or
unsupported low-sample conditions block ready status until explained or fixed.

## References

- `references/chart-types.md` for chart selection.
- `references/python-workflow.md` for Matplotlib/Seaborn defaults.
- `references/r-workflow.md` for ggplot2 defaults.
- `references/qa-checklist.md` for pre-submission checks.
- `references/template-index.md` for lightweight wind/AI figure templates.
