# Paper Type Taxonomy

Use this taxonomy when routing writing and polishing work.

## Types

- `research`: Full empirical or engineering research article with methods, experiments, results, and discussion.
- `methods`: Method-focused article where reproducibility and algorithmic detail carry the contribution.
- `algorithmic`: AI or optimization article where model design, proof, complexity, or ablation is central.
- `hypothesis`: Concept or perspective-like article with limited experiments and careful claim boundaries.
- `review`: Invited or approved review article. Check target journal policy before assuming unsolicited reviews are allowed.
- `mechanism-paper`: Explains why a phenomenon or method behavior occurs.
- `benchmark-paper`: Introduces or uses a systematic benchmark or evaluation protocol.
- `deployment-paper`: Reports field deployment or operational integration.
- `case-study`: Studies one or a small number of systems, sites, or projects.
- `resource-assessment`: Assesses renewable resource, siting potential, or spatial-temporal availability.
- `control-paper`: Proposes or evaluates a controller or closed-loop operating policy.
- `optimization-paper`: Proposes or evaluates an optimization formulation, solver, schedule, or market strategy.

## Default Choice

Default to `research` for wind power, renewable energy, smart grid, and AI-for-energy manuscripts unless the user explicitly names another article type.

## Routing Notes

- Forecasting papers usually need `research` plus the active topic fragment.
- New benchmark, dataset, or tool papers usually need `benchmark-paper` or
  `methods` guidance.
- Survey and state-of-the-art manuscripts need `review` guidance and a target-journal invitation check.
- Transfer or resubmission work must load target-journal rules before restructuring.
