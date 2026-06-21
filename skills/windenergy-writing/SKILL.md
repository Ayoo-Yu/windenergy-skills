---
name: windenergy-writing
description: >-
  Draft, restructure, or plan manuscript sections from author-provided claims,
  results, figures, notes, or Chinese drafts for wind power, renewable energy,
  smart grids, energy forecasting, and AI-for-energy papers targeting 18
  Elsevier energy, power systems, AI, and pattern-recognition journals. Use when
  the user wants to write or rebuild an abstract, introduction, related work,
  method, experiments, discussion, conclusion, title, highlights, keywords,
  cover-letter draft, or full manuscript argument with journal-aware constraints.
---

# Renewable Multi-Journal Scientific Writing Router

Use this skill for drafting and argument design. For sentence-level polishing,
use `windenergy-polishing`. For final submission documents, use
`windenergy-submission`.

Before writing generated files, load `../_shared/core/output-run-folders.md`
and create a run folder for this invocation. Put drafted sections, outlines,
claim maps, and export files in that run folder.

For any manuscript-level or foreground writing task, load
`../_shared/core/quality-principles.md`,
`../_shared/core/narrative-principles.md`, and
`../_shared/core/section-role-matrix.md`, and
`../_shared/core/fragment-contract.md`. Then load only the paper-type, topic,
journal, and manuscript fragments selected by the active profile.

## Routing Protocol

1. Read `manifest.yaml`.
2. Load every file listed under `always_load`.
3. Detect `paper_type`, `topic`, `section`, `language`, `journal`, and
   `evidence_strength`.
4. Build or read `workflow_profile.json` when the task is part of a full-paper
   workflow. Record confidence, profile source, loaded fragments, disabled
   fragments, routing notes, and quality thresholds.
5. Load only the fragments selected by the profile. If topic confidence is
   below `0.70`, load core and paper-type guidance only. From `0.70` to below
   `0.85`, load lightweight topic guidance. At `0.85` or above, load the full
   topic fragment.
6. If a journal is named, load the matching journal fragment and the shared
   profile file.
7. If the target journal is Applied Energy and the topic is wind-power
   forecasting, probabilistic wind forecasting, prediction intervals,
   calibration, or grid-risk forecasting, load the bundled style-learning
   profile before drafting:
   `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/learned_style_digest.md`,
   `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/style_profile.yaml`,
   and `../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/figure_style.yaml`.
   Use these files as the target-journal constraint layer for section
   architecture, move-level templates, numeric reporting, comparison language,
   caption syntax, and figure-reference language.
8. Create the run folder before writing artifacts.
9. Load on-demand references only when the task needs them.

## Writing Stance

- Start from the user's evidence and the profile. Do not import rules from an
  unrelated benchmark, topic, or journal.
- Make the energy-system problem explicit: generation, forecasting, operation,
  integration, resource assessment, control, or decision support.
- Connect AI methods to energy-system value, physical constraints, and
  operational risk.
- Preserve uncertainty, assumptions, data limitations, and scope boundaries.
- Do not invent results, equations, baselines, citations, datasets, author
  details, funding, or deployment claims.

## Quality Controls

- Apply claim strength control from `quality-principles.md`.
- Apply section-specific high-impact narrative control. Title, abstract,
  highlights, and conclusion should reveal the central finding when evidence is
  available and should end with a clear take-home message when the section form
  allows it. Introduction should identify the field tension, state the
  unresolved question, explain why the gap is difficult, preview the evidence
  design, and state contribution types without reporting detailed results,
  final rankings, operating boundaries, or recommendations.
- Apply standard narrative control to methods, experiments, limitations,
  response letters, and supplementary material.
- Apply related-work synthesis control to Related Work sections. Related Work
  should map literature lines, compare assumptions and mechanisms, identify
  unresolved gaps, and delimit novelty. It should avoid detailed experimental
  protocols, final results, internal audit language, journal-readiness logic, or
  repeated explanations of the current paper's design.
- Use a manuscript completeness checklist for full papers: abstract structure,
  research question, related work coverage, method details, experimental setup,
  results, interpretation, limitations, and future work.
- Use a per-claim presentation check. Core contributions, boundary conclusions,
  mechanism interpretations, robustness claims, and deployment advice need a
  figure, table, or explicit quantitative paragraph when the profile makes the
  claim central.
- Do not leave a heading with only a table or figure. Add explanatory prose for
  guidance, selection rules, and evidence-boundary sections.
- Avoid internal workflow artifact language in the main manuscript. Use
  scholarly wording and place raw file names in a reproducibility statement or
  appendix when they are needed.
- Apply interpretation overflow control. Each section has an
  interpretation ceiling defined in `section-role-matrix.md`. When a
  section's prose moves above its ceiling on the interpretation
  strength ladder defined in `narrative-principles.md`, flag it as
  `SECTION_WARNING` and move the overflowing content to the correct
  section.
- Apply review-defensive tone control. Detect and flag review-defensive
  phrasing as `TONE_WARNING` using the detection rules in
  `narrative-principles.md`. Replace defensive framing with confident,
  bounded statements.
- Apply internal language cleanup. Before finalizing any section, scan
  for internal workflow language using the replacement table in
  `quality-principles.md`. Flag as `LANGUAGE_WARNING` and apply the
  scholarly replacement.
- Use `NARRATIVE_WARNING` for checked foreground sections that lack problem
  tension, synthesis, or a take-home message. Use `UNCHECKED` only when a
  profile, artifact, or evidence source is missing.

## Journal-Aware Defaults

- If no target journal is named, use `common-18`.
- Prepare abstracts in a 200-word compact version and a 250-word standard
  version when the user has not chosen a journal.
- Prepare 6 keywords by default.
- Prepare 3 to 5 highlights with each bullet up to 85 characters when the user
  asks for submission-ready material.
- Apply target-specific profile limits when the user names a journal.
- For double-anonymized journals, avoid author-identifying language in review
  files.

## Output Rules

- If key facts are missing, mark `AUTHOR_INPUT_NEEDED`.
- Report the run folder path when files are written.
- Include a compact claim-evidence map for major claims.
- For Chinese drafts, translate intent and technical meaning while preserving
  model names, units, metrics, datasets, equations, and citations.
- For transfer writing, list the target-journal changes before drafting.
