# Figure QA Checklist

Use `../_shared/core/quality-principles.md` for the shared figure
professionalism rules.

- Times New Roman or a journal-compatible serif font is used by default.
- Figure text is at least 8 pt at final printed size.
- Line widths, marker sizes, panel labels, axis styles, and legend placement are
  consistent across the figure set.
- Semantic categories such as baseline, proposed method, method family, or
  operating regime keep stable colors across all figures.
- The palette is colorblind-safe and uses no more than two dominant semantic
  colors unless the data structure requires more.
- Claim is visible without reading the full manuscript.
- Axes include units and time scale where relevant.
- Axes use precise target quantities. Metric-specific axis rules come from the
  active topic fragment.
- Metrics match the manuscript text and tables.
- Sample period, farm/turbine scope, and data split are stated.
- Colors are distinguishable in grayscale and colorblind-safe palettes.
- Uncertainty or variability is shown for model comparisons.
- Raster outputs are at least 300 dpi; vector text remains editable.
- No generated or decorative imagery is used as scientific evidence.
- Every panel is cited in the manuscript and every cited panel exists.
- Captions state the conclusion first, then define data, metrics, samples, and
  panels.
- `figure_text_audit.md` records the supported claim, data source, visual
  encoding, manuscript references, table consistency, status, and unresolved
  risks for every figure.
- Quantitative figures have `figure_data_map.json` entries with source file,
  filters, groups, metric names, transformations, plotted values, and expected
  table or text values.
- Full-paper figure maps record portfolio role, style metadata, axis metadata,
  and low-support condition metadata when relevant.
- Full-length empirical manuscripts use the display-item targets supplied by the
  active paper-type or journal profile.
- The figure portfolio covers workflow, data or task overview, method
  comparison, condition boundary, mechanism evidence, robustness, and deployment
  guidance when these claim types appear.
- Low-support regime or subgroup figures state sample count, sample share,
  uncertainty, or sensitivity.
- Regime or subgroup figures compare plotted values against corresponding
  manuscript tables when those values support a central claim.
- Workflow figures show the research object, comparison unit, alternatives,
  diagnostic layer, and boundary analysis. For the orchestrator
  benchmark, use the active manuscript fragment.
- Main workflow figures do not include code filenames or dense implementation
  labels that belong in a reproducibility appendix.
