# Reader Workflow

Use this shared reader workflow for drafting, polishing, and submission checks.

## Core Questions

Every manuscript section should help a reviewer answer five questions in order:

1. What energy or AI-for-energy problem is being solved?
2. Why is the current solution insufficient for that problem?
3. What evidence does the manuscript provide?
4. Why is the evidence trustworthy under the stated data, physics, and protocol limits?
5. What conclusion can be drawn without exceeding the evidence?

## Wind and AI Grounding

- Tie AI claims to a concrete energy task: wind forecasting, resource assessment, turbine operation, grid integration, dispatch, ramp-event management, wake/layout analysis, or decision support.
- Preserve physical context that is relevant to the active profile: measurement
  source, sampling, operating constraints, environmental drivers, system state,
  seasonality, regimes, and uncertainty.
- Check machine-learning validity: chronological splitting, leakage control, baseline strength, ablation, robustness, cross-site testing, metric choice, and statistical stability.
- Separate method novelty from energy-system value. A model change needs a clear operational reason.

## Reviewer-Visible Output

- Prefer traceable claims over broad significance statements.
- Mark missing evidence as `AUTHOR_INPUT_NEEDED`.
- Mark unsupported wording as `Claim risk:` followed by the exact phrase.
- Do not invent results, citations, datasets, grants, author roles, or deployment claims.
