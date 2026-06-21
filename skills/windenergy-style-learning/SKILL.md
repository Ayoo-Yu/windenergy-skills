---
name: windenergy-style-learning
description: >-
  Build reusable target-journal style profiles for wind power, renewable
  energy, smart-grid, energy forecasting, and AI-for-energy SCI manuscripts
  from ScienceDirect or local PDF corpora, then audit draft manuscripts against
  the learned prose, section, citation, caption, and figure-style constraints.
  Use when the user asks to learn a target journal's writing style, download
  representative Elsevier papers for style learning, create style_profile.yaml
  figure_style.yaml, or visual_figure_style.yaml, compare a manuscript with
  published SCI article patterns, or improve windenergy-writing,
  windenergy-polishing, and windenergy-figure with journal-specific evidence.
---

# Target Journal Style Learning

Use this skill before high-stakes drafting, polishing, figure redesign, or
submission preparation when a target SCI journal's article style matters.

The skill creates reusable style profiles from entitled ScienceDirect articles
or local PDFs. Profiles are statistical and procedural summaries. They must not
store long copied passages from copyrighted papers.

Before writing generated files, load `../_shared/core/output-run-folders.md`
and create a run folder unless the user has supplied an explicit output
directory. Put corpora, manifests, style profiles, audits, and revision targets
in that run folder.

## Workflow

1. Define the target journal, paper type, topic scope, years, and corpus size.
   Use at least 30 complete research articles for a normal profile. Use 10 to
   29 articles only for a caution profile. Use fewer than 10 articles only for
   a pilot.
   For broad journals such as Applied Energy, define a topic gate before
   learning language templates. Use `wind_forecasting` for wind-power
   forecasting manuscripts.
2. Build or update a corpus:
   - For ScienceDirect, run `scripts/fetch_sciencedirect_corpus.py`.
   - If entitled PDF retrieval returns one-page preview PDFs, rerun with
     `--download-full-text --full-text-format xml-text` and build the profile
     from the generated `fulltext/` directory.
   - If PDF access is unavailable, run
     `scripts/discover_crossref_candidates.py` to create a DOI target list,
     then pass that file to `scripts/fetch_sciencedirect_corpus.py` with
     `--candidate-json` when ScienceDirect access is available.
   - For author-supplied PDFs, place files in one folder and skip the fetch
     step.
3. Build the style profile:
   `python <skill_base>/scripts/build_style_profile.py --pdf-dir CORPUS --journal JOURNAL --topic-profile wind_forecasting --require-topic-match --min-template-doc-support 5 --output PROFILE_DIR`
   Use `--text-dir CORPUS/fulltext` instead of `--pdf-dir` when the corpus was
   built from ScienceDirect XML full text.
4. Optionally learn image-level figure style when visual design or figure
   redesign is part of the task:
   `python <skill_base>/scripts/learn_visual_figure_style.py --sciencedirect-manifest CORPUS/corpus_manifest.json --topic-screening-report PROFILE_DIR/topic_screening_report.json --api-key-file PRIVATE_KEY_FILE --max-records 30 --max-figures-per-record 14 --journal JOURNAL --source sciencedirect_xml_figure_objects --output VISUAL_PROFILE_DIR`
   Use this for layout, aspect ratio, palette, ink density, figure topic mix,
   and image-level consistency. For complete caption length and syntax, use
   the full-text profile produced in step 3.
5. Audit the active manuscript:
   `python <skill_base>/scripts/audit_manuscript_style.py --manuscript PAPER.pdf --profile PROFILE_DIR/style_profile.yaml --output AUDIT_DIR`
6. Load the generated profile files before using downstream windenergy skills:
   - `style_profile.yaml` for writing and polishing.
   - `learned_style_digest.md` for a human-readable summary of all learned
     section, prose, citation, caption, figure, language-template, numeric
     reporting, and table-header patterns.
   - `section_moves.md` for abstract, introduction, results, discussion, and
     conclusion structure.
   - `figure_style.yaml` for figure construction, figure audit, caption polish,
     and visual consistency.
   - `visual_figure_style.yaml` for image-level figure layout, aspect ratio,
     palette, ink density, and topic-mix constraints learned from figure
     objects or rendered figure crops.
   - `visual_figure_style_digest.md` for a human-readable summary of the
     visual figure style profile.
   - `manuscript_style_audit.md` when revising a specific draft.

## ScienceDirect Ingest

Read `references/sciencedirect-ingest.md` before fetching. Use environment
variables for credentials. Never write API keys into a skill file, profile,
manifest, corpus log, or command transcript that will be shared.

Default credential lookup:

```bash
SCIENCEDIRECT_API_KEY
ELSEVIER_API_KEY
X_ELS_APIKEY
```

If a newly added Windows environment variable is not visible to Codex, use
`--api-key-file PATH` with a private local text file outside the run folder.

Example:

```bash
python scripts/fetch_sciencedirect_corpus.py \
  --journal "Applied Energy" \
  --query "wind power forecasting OR prediction interval OR conformal prediction" \
  --year-from 2022 \
  --year-to 2026 \
  --max-results 80 \
  --max-search-pages 12 \
  --download-pdf \
  --output runs/applied-energy-corpus
```

ScienceDirect PDF access depends on API permissions and institutional
entitlements. If PDF retrieval fails, keep the metadata manifest and report the
authorization status. Use local PDFs or open-access items to continue profile
building.

## Profile Contract

Read `references/style-profile-schema.md` before editing profile files by hand.
The profile must include:

- corpus source, journal, years, article count, and extraction status.
- section order and section-level metric distributions.
- abstract and introduction move patterns.
- result and discussion reporting patterns.
- citation density and citation placement signals.
- caption length, panel-label, table, and figure-reference patterns.
- language-template patterns: section-level sentence starters, move-level
  normalized sentence templates, paragraph flow, introduction arc, conclusion
  closing, bigrams, trigrams, verb preferences, hedging terms, numeric
  reporting formats, number-unit co-occurrence, caption syntax, and table
  header naming patterns.
- optional visual figure style: figure image dimensions, aspect ratio,
  ink-density, color fraction, neutral or accent palette signals, visual topic
  mix, and measurement notes that identify extraction-sensitive fields.
- corpus topic screening: accepted and excluded PDFs with topic scores,
  required keyword-group hits, exclusion hits, and reasons.
- downstream writing, polishing, and figure constraints.

Profiles are reusable context. Keep them compact and evidence-bound. Use
quantiles, counts, and synthetic templates. Do not store long verbatim source
text.

The build script must also write `learned_style_digest.md`. Use this file when
the user asks what was learned from a target journal. The manuscript audit is a
gap report and may only mention sections where the active manuscript deviates
from the profile.

## Bundled Profiles

For Applied Energy wind forecasting manuscripts, a reusable normal-strength
profile is bundled here:

```text
references/profiles/applied-energy-wind-forecasting/main-profile/
references/profiles/applied-energy-wind-forecasting/visual-profile/
```

Use `main-profile/learned_style_digest.md`, `main-profile/style_profile.yaml`,
and `main-profile/figure_style.yaml` for section structure, prose templates,
numeric reporting, caption patterns, and figure-reference language.

Use `visual-profile/visual_figure_style_digest.md` and
`visual-profile/visual_figure_style.yaml` for image-level figure proportions,
palette, ink density, and topic mix.

This bundled profile is topic-gated for wind forecasting and should be reused
for wind-power forecasting, prediction interval, calibration, and grid-risk
manuscripts targeting Applied Energy. Build a new profile for other Applied
Energy domains.

## Manuscript Gap Audit

Read `references/manuscript-gap-audit.md` when applying a profile to a draft.
The audit should classify each issue as:

- `BLOCKER`: likely to harm review readiness.
- `MAJOR`: material style, structure, evidence, or figure mismatch.
- `MINOR`: local wording, density, or consistency issue.
- `INFO`: measurement or context note.

The audit should produce:

- `manuscript_style_audit.md`
- `manuscript_style_audit.json`
- optional `revision_targets.md`

Do not rewrite the whole manuscript inside this skill. Use the audit to drive
`windenergy-polishing`, `windenergy-writing`, or `windenergy-figure`.

## Downstream Use

When another windenergy skill receives a style-learning profile:

- Treat the profile as a target-journal constraint layer above generic
  `common-18` guidance.
- Use `language_patterns` to shape expression at the section, paragraph,
  sentence, caption, figure-reference, and table-header levels. Prefer
  normalized templates and high-frequency starters over generic rhetorical
  labels.
- Trust language templates only when `doc_support` meets the profile's
  `min_template_doc_support`; otherwise treat the pattern as exploratory.
- For broad target journals, reject profiles whose topic screening shows
  off-topic clusters such as UBEM, building energy, hot-water systems,
  unrelated hydrogen storage, pure PV forecasting, or generic microgrid
  scheduling when the manuscript target is wind forecasting.
- Keep the author's claims, data, citations, and numerical results unchanged
  unless the user supplies corrected evidence.
- Use target-journal ranges to identify mismatches, then revise only the
  affected section, paragraph, caption, or figure.
- When `visual_figure_style.yaml` is available, use it with `figure_style.yaml`:
  visual style controls plot proportions, palette, ink density, and topic mix;
  full-text figure style controls caption length, caption syntax, and in-text
  figure-reference language.
- When the profile is based on fewer than 10 papers, label conclusions as
  `PILOT_PROFILE` and avoid hard style rules.
- Build normal target-journal profiles from at least 30 complete PDFs after
  filtering short or incomplete downloads.

## Validation

After editing this skill, run:

```bash
python C:/Users/Administrator/.codex/skills/.system/skill-creator/scripts/quick_validate.py D:/skill/windenergy-style-learning
```

For a functional smoke test, run profile building and manuscript audit on a
small local PDF folder. Verify that the output contains no API key and no long
copied paper passages.
