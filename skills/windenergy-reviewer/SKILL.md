---
name: windenergy-reviewer
description: >-
  Simulate conservative pre-submission reviewer assessment for wind-power,
  renewable-energy integration, smart-grid, power-system, and AI-for-energy
  manuscripts targeting Applied Energy, Renewable Energy, Energy, IEEE TSTE,
  Energy and AI, IJEPES, EPSR, and related journals. Use when the user asks for
  pre-submission review, reviewer reports, rejection-risk assessment, broad
  energy-journal fit, technical soundness review, novelty critique, 审稿人视角,
  投稿前评审, 预审, 模拟审稿, or manuscript risk audit before submission.
---

# Renewable Reviewer Assessment

Use this skill to pressure-test a manuscript before submission. Load
`../_shared/core/output-run-folders.md` and create a run folder before writing
files. For manuscript-level quality, also load `../_shared/core/quality-principles.md`,
`../_shared/core/narrative-principles.md`, and `../windenergy-submission/references/journal-profiles.md`.

## Router Protocol

1. Read `manifest.yaml`.
2. Load every file under `always_load`.
3. Detect the target journal family and paper type if the user supplies them.
4. Load only the matching fragments from `static/fragments` and any on-demand
   references needed for the case.
5. If the target journal is Applied Energy and the topic is wind-power
   forecasting, probabilistic wind forecasting, prediction intervals,
   calibration, or grid-risk forecasting, load the bundled style-learning
   profile:
   `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/learned_style_digest.md`,
   `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/style_profile.yaml`,
   and `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/figure_style.yaml`.
   Use it to assess target-journal fit, section architecture, results language,
   caption adequacy, figure count, and Applied Energy wind-forecasting style
   gaps.
6. Produce the default package: `review_setup.md`, `reviewer_reports.md`,
   `cross_review_synthesis.md`, and `author_action_list.md` when files are
   requested.

## Default Output

- `Review setup`: source material, target journal, paper type, missing inputs.
- `Reviewer 1`: energy-system significance and journal fit.
- `Reviewer 2`: method, data, baseline, and reproducibility.
- `Reviewer 3`: AI/statistical validity, uncertainty, and deployment claims.
- `Cross-review synthesis`: consensus, disagreement, likely decision risk.
- `Author action list`: concrete revisions and `AUTHOR_INPUT_NEEDED` items.

## Red Lines

- Do not invent reviewer identities, editor policy, experiments, line numbers,
  data, p-values, citations, or journal requirements.
- Do not present the simulated review as a real journal decision.
- Mark unsupported claims as `AUTHOR_INPUT_NEEDED` or `Not assessable from
  provided material`.
- Keep all criticism evidence-forward and useful for revision.
