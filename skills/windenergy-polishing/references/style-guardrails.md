# Style Guardrails

Load `../_shared/core/quality-principles.md` and
`../_shared/core/narrative-principles.md` when polishing interpretive
scientific claims.

- Use one English variant consistently.
- Prefer concrete verbs: estimate, forecast, compare, reduce, evaluate.
- Avoid empty intensifiers: very, extremely, remarkable, revolutionary.
- Avoid unsupported absolutes: prove, guarantee, fully, universally.
- Run a claim risk pass for titles, abstracts, contribution paragraphs, results,
  discussion, conclusions, and response letters.
- Prefer evidence-calibrated language that is rhetorically clear when the
  original sentence makes a claim stronger or weaker than the supplied evidence.
- Run a narrative preservation pass for foreground sections. Mark
  `NARRATIVE_WARNING` when title, abstract, introduction, highlights,
  contribution, or conclusion lacks problem tension, synthesis, or a take-home
  message.
- Preserve numbers, method names, metric names, citation keys, equations,
  dataset names, and statistical qualifiers while reducing claim strength.
- Mark content risks when a full manuscript has empty or table-only sections,
  missing profile-required setup or methodology details, future work that lists
  current evidence gaps, or a claim that lacks diagnostics required by the
  active profile.
- Mark content risks when a title is stronger than the evidence boundary, a
  required control is mentioned only in a diagnostic file, advice-level claims
  exceed result granularity, a low-support condition lacks uncertainty or
  sensitivity evidence, or a profile-required display target lacks a documented
  exception.
- Run a visual-language pass for captions, figure references, table references,
  axis terms, abbreviations, and legend terminology.
- Remove internal workflow artifact language from the main text. Put raw file
  names, code paths, diagnostic file names, and figure-map names in a
  reproducibility statement or appendix when they are needed.
- Rewrite avoidable parenthetical sentence structures into natural prose while
  preserving the information inside the parentheses.
- Integrate parenthetical information with commas, `including`, `such as`,
  appositive phrases, or a short follow-up sentence when meaning is preserved.
- Keep parentheses when they are needed for equations, variable definitions,
  units, statistics, citations, abbreviations, model names, or legal names.
- Check abbreviations at first use in the abstract and again at first use in
  the main text when the abstract is separate.
- Do not invent missing abbreviation expansions. Mark them as
  `AUTHOR_INPUT_NEEDED`.
- Keep titles concise and specific to the method, asset, and task.
- Keep figure legends concise but complete enough to identify data, metrics, and
  conditions.
- In `.docx` outputs, color main-text mentions of figures, tables, appendices,
  and numbered citations such as `[1]`, `[1,2]`, or `[1-3]` in blue `#0000FF`,
  which is RGB `(0, 0, 255)`.
- Do not color captions, reference-list entries, headers, footers, text boxes,
  fields, citation-manager generated content, or unsafe runs containing complex
  OOXML unless the user explicitly requests manual handling. When a paragraph
  contains formulas or tracked changes, color only safe plain-text runs.
