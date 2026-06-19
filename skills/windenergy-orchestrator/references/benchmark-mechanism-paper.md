# Benchmark: Wind Power Mechanism Paper

Use this benchmark to test whether the renewable suite can produce a complete
Applied Energy manuscript from an experiment folder.

## Source Folder

Default source:

```text
D:/paperproduction/paper1/0427
```

## Target Workspace

Default workspace:

```text
D:/paperproduction/paper1/0427/mechanism_paper_workspace
```

## Research Story

The benchmark asks what adaptive conformal calibration is doing in wind power
prediction intervals. The storyline must be calibrated to the available
diagnostics:

- Adaptive methods can reduce interval score in selected regimes.
- The benefit is conditional on coverage target, predictor residual structure,
  and operating condition.
- Christoffersen key-slice independence results, including the 3528 reported
  checks when available, and rolling coverage diagnostics support an empirical
  signature based on interval widening and coverage-level bias.
- Strong claims that dynamic benefits primarily come from interval expansion
  require interval score decomposition, width-matched baseline, and
  coverage-matched comparison.
- Ramping can be described as a favorable operating condition only when sample
  counts, threshold sensitivity, and table-figure consistency are checked.
- Fine-grained predictors such as GBR and QRLSTM are more compatible with
  static calibration, while Ridge and MLP can benefit more from dynamic updates.

## Required Benchmark Outputs

- `final/paper.tex`
- `final/paper.pdf`
- `final/refs.bib`
- `outline/outline.json`
- `diagnostics/claim_evidence_map.md`
- `diagnostics/mechanism_diagnostics.md`
- `diagnostics/profile_evidence_strength_audit.md`
- `diagnostics/mechanism_evidence_strength_audit.md`
- `audits/manuscript_quality_audit.json`
- `audits/figure_consistency_audit.json`
- `audits/scientific_maturity_audit.json`
- `audits/citation_audit.json`
- `audits/submission_audit.md`
- `final/final_manifest.json`

Ready status also requires the benchmark workflow profile gates: the
profile-defined display-item and figure targets or a justified exception,
figure portfolio coverage, consistent figure style metadata, the
profile-defined reference target or a justified exception, title strength
compatible with evidence boundaries, method-level result granularity when
deployment advice names methods, and removal of internal workflow artifact
language from the main article.

## Scoring Dimensions

- Mechanism storyline clarity.
- Numeric traceability.
- Citation accuracy.
- Applied Energy fit.
- Figure-text consistency.
- PDF compile integrity.
- Citation audit status.
- Submission audit status.
- Manuscript quality audit status.
- Figure consistency audit status.
- Mechanism evidence strength status.

## Negative Regression Items

The audit must block ready status when a generated benchmark paper has:

- An empty or table-only `Operational Selection Guidance` subsection.
- Fewer than 5000 main-body words from Introduction through Conclusion for an
  Applied Energy full-length article.
- Missing data source, sampling interval, split, features, normalization, NWP
  usage, or horizon definition in Experimental Setup.
- Missing update rule, learning rate, window size, clip range, horizon-specific
  setting, method configuration table, or delayed-label timeline in Methodology.
- Quantitative figures without `figure_data_map.json`.
- Ramping figure values that conflict with ramping table values.
- A workflow figure that does not follow the five-layer publication template.
- Fewer than 10 figures or fewer than 12 display items without a journal or
  article-type reason.
- Fewer than 40 verified references for an Applied Energy full-length article
  without a documented reason.
- A strong mechanism title when evidence boundaries are partial, aggregate, or
  proxy-based.
- Family-level results used for method-specific guidance without per-method
  evidence.
- Alpha axes that require avoidable mental conversion to target coverage.
- Low-support regimes used for strong boundary claims without sample share,
  uncertainty, or sensitivity evidence.
- Internal workflow file names repeated in the main article.
- Future work that lists diagnostics needed for the central mechanism claim.

## Default Limits

- Do not train new models.
- Do not add CPTC or AcMCP as empirical baselines unless verified result files
  already exist.
- Treat NEX naming as author input unless the source folder supplies an approved
  expansion and algorithm description.
