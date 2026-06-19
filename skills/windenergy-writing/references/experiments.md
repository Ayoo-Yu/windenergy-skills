# Experiments Writing Guide for Renewable Energy Papers

Use this guide for generic experiment structure. Load topic fragments for
domain-specific datasets, metrics, baselines, and physical variables.

## Goal

Convince reviewers that the evidence is fair, reproducible, and aligned with
the claim.

## Three Core Questions

1. Is the method, design, or analysis better than strong alternatives under a
   fair protocol?
2. Which component, condition, or assumption explains the gain or limitation?
3. How far does the result generalize across settings that matter for the
   active paper type?

## Experiment Section Structure

```text
\section{Experiments}
\subsection{Data and Experimental Setup}
\subsection{Baselines or Comparators}
\subsection{Main Results}
\subsection{Ablation, Sensitivity, or Robustness}
\subsection{Case Study or Visualization}
\subsection{Computational or Operational Cost}
```

## Data and Setup

| Item | What to include |
|---|---|
| Study object | Asset, system, site, market, simulator, or dataset |
| Time or spatial scope | Period, region, split, or scenario definition |
| Resolution | Sampling or spatial resolution when relevant |
| Inputs | Features, controls, covariates, or scenario variables |
| Target | Output, decision, state, cost, risk, or physical quantity |
| Preprocessing | Missing data, filtering, normalization, exclusions |
| Metrics | Definitions and direction of improvement |

## Baselines and Comparators

Choose comparators that match the claim:

- operational baseline for deployment value
- recent method baseline for algorithmic value
- physical or analytical model for scientific explanation
- ablation for module contribution
- sensitivity analysis for boundary claims

Do not add loosely related baselines only to increase table size.

## Main Results Table Format

```text
Table X: Performance on [study object].

| Method or scenario | Condition | Metric A | Metric B | Notes |
|---|---|---:|---:|---|
| Baseline | [condition] | X.XX | X.XX | [short note] |
| Proposed | [condition] | X.XX | X.XX | [short note] |
```

Rules: caption above table, booktabs style for LaTeX, metric direction in
headers, consistent decimals, and no unsupported bolding.

## Robustness and Sensitivity

Use robustness checks when the central claim depends on a setting, subgroup,
parameter, scenario, or operating condition. Report uncertainty when the claim
depends on statistical stability.

## Benchmark Matrix Table

For comparison and benchmark papers, use a benchmark matrix to present
results across multiple methods, datasets, and conditions in a single
table.

### Structure

```text
Table X: Benchmark results across [datasets/conditions].
Best results in bold. Second best underlined.

| Method | Dataset A |  | Dataset B |  | Dataset C |  |
|        | Metric 1 | Metric 2 | Metric 1 | Metric 2 | Metric 1 | Metric 2 |
|--------|----------|----------|----------|----------|----------|----------|
| Baseline 1 | X.XX | X.XX | X.XX | X.XX | X.XX | X.XX |
| Baseline 2 | X.XX | X.XX | X.XX | X.XX | X.XX | X.XX |
| Proposed    | **X.XX** | **X.XX** | X.XX | **X.XX** | **X.XX** | X.XX |
```

### Rules

- State metric direction in caption or header (lower is better / higher
  is better).
- Bold only the best result per column. Underline the second best when
  the paper emphasizes comparison competitiveness.
- Use consistent decimal places within each metric column.
- Include a rank column or relative improvement column when the paper
  claims ranking improvements.
- When the matrix is large, split by metric family rather than by
  dataset to maintain readability.

## Task Selection Justification

Every dataset or condition in the benchmark must be justified:

| Category | Justification type |
|----------|-------------------|
| Primary dataset | Directly tests the central claim |
| Secondary dataset | Tests generalization across data regimes |
| Stress condition | Tests operating boundary or failure mode |
| Ablation condition | Isolates a specific mechanism or component |

If a dataset appears without a justification type, flag it for removal
or add the justification. State why each task was chosen, not just what
was done.

### Experiment Scale Presentation

When the experiment grid is large (many tasks, predictors, horizons,
alphas, seeds), use a benchmark dimension table instead of burying the
numbers in running text:

| Dimension | Values | Purpose |
|-----------|--------|---------|
| Task | [list] | [what it tests] |
| Predictor | [list] | [what it tests] |
| Horizon | [list] | [what it tests] |
| Alpha | [list] | [what it tests] |
| Seed | [count] | [what it tests] |
| Method | [list] | [what it tests] |

This replaces long sentences listing every dimension and run count inline.

## Preprocessing Boundary Framing

State preprocessing decisions as bounded choices, not universal
recommendations:

- State what was done and why for this specific study context.
- Do not present preprocessing as "the correct approach" unless
  the paper includes a preprocessing ablation.
- Separate normalization, missing data handling, and feature
  construction into distinct paragraphs.
- State whether preprocessing was applied identically to all methods
  or whether method-specific preprocessing was used (and why).
- Frame boundaries positively:
  - "This study evaluates the method on processed pipeline outputs.
    Anomalous-operation screening is outside the benchmark scope."
  - NOT: "We don't have a filter for this so it is a limitation."

## Feature Description Best Practice

When listing features, use a table rather than inline prose:

| Feature group | Variables | Source |
|---------------|-----------|--------|
| Forecast covariates | primary predictors, derived features | Forecast model |
| Lagged target | target at t-1, t-2, ... | Measurement |
| Temporal features | hour of day, day of week | Calendar |
| Auxiliary | additional domain-relevant variables | Varies |

This replaces dense paragraphs listing feature names and sources.

## Horizon and Sampling Interval Boundary

When experiments span datasets with different sampling intervals, state
the interpretation boundary explicitly:

- "Horizon index 1-24 corresponds to different physical lead times
  depending on the dataset's sampling interval. Cross-dataset
  comparisons use the common horizon-index grid; physical lead-time
  interpretation must account for sampling interval."

Load topic fragments for domain-specific horizon and interval details.
