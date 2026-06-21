# Style Profile Schema

`style_profile.yaml` is the machine-readable contract shared with downstream
windenergy skills.

`learned_style_digest.md` is the human-readable companion. It should summarize
all learned section, prose, citation, caption, and figure patterns, including
sections that do not appear as manuscript audit issues.

`visual_figure_style.yaml` is an optional image-level companion for figure
redesign and visual audit tasks. It should summarize figure object or rendered
crop measurements, not copied figure artwork.

## Required Top-Level Keys

- `schema_version`: profile schema version.
- `profile_name`: human-readable profile name.
- `journal`: target journal.
- `created_utc`: ISO timestamp.
- `profile_strength`: `normal`, `caution`, or `pilot`.
- `corpus`: source type, article count, PDF count, years, and manifest path.
  For topic-screened corpora, include `selection_criteria.topic_profile`,
  `selection_criteria.require_topic_match`, and
  `language_pattern_settings.min_template_doc_support`.
- `sections`: section order, detected section coverage, and section metrics.
- `abstract`: abstract length, sentence count, numeric density, and move
  signals.
- `introduction`: paragraph count, citation density, problem-gap-contribution
  signals.
- `results_discussion`: result reporting, figure reference, uncertainty, and
  limitation signals.
- `figures`: figure count, caption length, panel-label, table, and caption
  density patterns.
- `language_patterns`: normalized sentence templates, move starters,
  section-level bigrams and trigrams, verb preferences, numeric reporting
  formats, figure-caption syntax, figure-reference templates, introduction
  arc patterns, conclusion closing patterns, comparison-language templates,
  and table-header naming signals.
- `constraints`: concise instructions for writing, polishing, figures, and
  guardrails for extraction-sensitive metrics.

## Visual Figure Style Profile

Use `visual_figure_style.yaml` when the task requires target-journal visual
plotting style. Required top-level keys:

- `schema_version`: visual profile schema version.
- `profile_name`: human-readable visual profile name.
- `journal`: target journal.
- `source`: local PDF crop extraction or ScienceDirect XML figure-object
  extraction.
- `profile_strength`: `normal`, `caution`, or `pilot`.
- `corpus`: document count, figure count, failure count, and source document
  records.
- `visual_metrics`: distributions for figures per article, image dimensions,
  aspect ratio, ink density, dark fraction, light-gray fraction, color
  fraction, and edge density.
- `figure_topics`: compact topic mix inferred from figure captions or labels.
- `dominant_palette`: neutral and accent color signals learned from measured
  figures.
- `measurement_notes`: extraction limitations, including whether caption text
  is a short XML fragment rather than complete caption prose.
- `style_rules`: downstream rules for layout, color, axes, gridlines, and
  caption handoff.

If the visual source is ScienceDirect XML figure objects, treat
`caption_fragment_words` as a diagnostic field. Use full-text
`figure_caption_patterns` and `figure_caption_metrics.word_count` for complete
caption length and syntax.

## Metric Objects

Use this shape for distribution metrics:

```yaml
word_count:
  median: 245
  p25: 220
  p75: 280
  min: 180
  max: 330
```

Use `null` when a metric cannot be computed reliably.

## Constraint Style

Constraints should be actionable:

- Good: "Keep abstract between 190 and 260 words for this profile."
- Good: "Make figure captions conclusion-first and include metric, unit, and
  sample definition when available."
- Good: "Treat Methods sentence-length P75 as extraction-sensitive when it
  exceeds readable drafting targets."
- Weak: "Write like Applied Energy."

## Safe Examples

Use synthetic or normalized templates when examples are needed:

```text
Context sentence. Gap sentence. Method sentence. Quantified finding sentence.
Operational implication sentence.
```

Do not copy source article sentences into the profile.

## Language Pattern Layer

`language_patterns` should support downstream writing and figure work, not only
metadata reporting. Include these compact subkeys when extraction supports
them:

- `by_section`: for each major section, include sentence starters,
  move-level normalized templates, move starters, frequent bigrams, frequent
  trigrams, verb preferences, and hedging or degree terms.
- `numeric_reporting`: include format classes, short normalized templates,
  number-unit co-occurrence, uncertainty expressions, and section-specific
  numeric pattern frequencies.
- `comparison_language`: include result-comparison templates such as
  `<method> outperforms <baseline> by <percent> in terms of <metric>` and
  comparison verb frequencies.
- `figure_caption_patterns` and `table_caption_patterns`: include caption
  opening types, opening starters, syntax patterns, and topic-to-starter
  mappings where available.
- `figure_reference_patterns`: include normalized in-text figure-reference
  templates.
- `paragraph_flow_templates`: include common move sequences inside paragraphs.
- `introduction_arc_patterns`: include paragraph-position moves, transition
  starters, and arc sequences.
- `conclusion_closing_patterns`: include opening starters, closing starters,
  and closing moves.
- `table_header_patterns`: include header terms and shapes such as
  metric-with-unit or scenario-metric matrices.

Use `doc_support` for reusable templates. A normal profile should suppress
move-level, numeric, comparison, and figure-reference templates supported by
fewer than 5 source documents.

## Topic Screening

For broad journals, profile construction should write
`topic_screening_report.json` when a topic gate is used. The report should show
accepted status, score, threshold, include hits, exclude hits, and reason for
each screened PDF. For wind forecasting, require wind-related terms plus a
forecasting core term, and exclude off-topic clusters such as UBEM, building
energy, hot-water systems, unrelated hydrogen storage, pure PV-only work, and
generic microgrid scheduling.
