---
name: windenergy-polishing
description: >-
  Polish, shorten, restructure, translate, or produce tracked changes for
  academic prose in wind power, renewable energy, smart grids, energy
  forecasting, and AI-for-energy manuscripts targeting 18 Elsevier energy, power
  systems, AI, and pattern-recognition journals. Use when the user asks to
  improve manuscript paragraphs, abstracts, introductions, results, discussion,
  conclusions, titles, methods, response text, Chinese drafts, journal-specific
  style, transfer polishing, or Word .docx tracked edits.
---

# Renewable Multi-Journal Academic Polishing Router

Use this skill for prose already drafted by the author. For building a section
from notes, use `windenergy-writing`. For final submission compliance, use
`windenergy-submission`.

Before writing generated files, load `../_shared/core/output-run-folders.md`
and create a run folder for this invocation. Put tracked `.docx`, change logs,
changes JSON, and scan reports in that run folder.

Also load `../_shared/core/quality-principles.md`,
`../_shared/core/narrative-principles.md`, and
`../_shared/core/fragment-contract.md` when polishing titles, abstracts,
contribution paragraphs, results, discussion, conclusions, response letters, or
any manuscript section with interpretive claims. Load only the profile-selected
paper-type, topic, journal, and manuscript fragments.

## Routing Protocol

1. Read `manifest.yaml`.
2. Load every file listed under `always_load`.
3. Detect `paper_type`, `topic`, `section`, `language`, `journal`, and
   `evidence_strength`.
4. Read `workflow_profile.json` when available. Respect routing confidence:
   below `0.70` for a topic, do not load heavy topic guidance; from `0.70` to
   below `0.85`, use lightweight topic guidance; at `0.85` or above, use full
   topic guidance.
5. Load only matching fragments and needed references.
6. If a journal is named, load the matching journal profile and fragment.
7. Create the run folder before writing artifacts.
8. Generate output following the Word Output Protocol when the input is `.docx`.

## Polishing Stance

- Improve clarity, logic, concision, reviewer readability, and evidence
  alignment.
- Rewrite avoidable parenthetical sentence structures into natural prose while
  preserving the information inside the parentheses.
- Integrate parenthetical information with commas, `including`, `such as`,
  appositive phrases, or a short follow-up sentence when meaning is preserved.
- Preserve necessary parentheses in equations, variable definitions, units,
  statistics, citations, and standard model names.
- Keep technical terms stable unless the supplied term is incorrect or
  ambiguous.
- Soften claims that exceed the supplied results.
- Preserve narrative force when the evidence supports it. Do not convert
  abstracts, introductions, contribution paragraphs, titles, or conclusions into
  audit-style records.
- Preserve reproducibility details, uncertainty, and physical constraints.
- Connect AI wording to the wind or energy-system task when the supplied text
  supports that connection.
- Do not add citations, numbers, datasets, baselines, equations, author facts,
  or results that the user did not provide.

## Journal-Aware Checks

- Use `common-18` when no target journal is named.
- Use target-specific limits for abstract length, keyword count, highlights,
  reference style, review mode, cover letter, figure limits, and special files.
- For double-anonymized journals, flag self-identifying text and metadata as a
  compliance risk.
- For transfer polishing, state what can remain stable and what needs
  target-journal adjustment.

## Word Output Protocol

When the input is a `.docx` file, produce a revised `.docx` with OOXML tracked
changes. Also provide a Markdown change log. Do not stop at a clean revised
version.

### Step 1. Identify Changes

Read the manuscript with `python-docx` or extracted text. Compile changes:

- `paragraph_index`: existing 0-based paragraph index for body paragraphs.
- `block_id`: optional stable block id from the script inventory mode.
- `old`: exact text to find in that block.
- `new`: replacement text.
- `note`: short reason for the change log.

### Step 2. Run The Script

Use the bundled script for normal polishing, second compression passes, color
formatting, and submission handoffs. Do not create a new Python script for these
standard operations.

```bash
python <skill_base>/scripts/polish_docx.py INPUT.docx changes.json OUTPUT.docx
```

Name the output `*_polished_tracked.docx` inside the run folder.

The script applies paragraph and table-cell text replacements as tracked
deletions and insertions. It reports unmatched changes and validates that the
output contains OOXML tracked-change elements.

The script must use package-preserving save behavior for `.docx` files: replace
only `word/document.xml` and keep all other package parts unchanged, including
`word/embeddings/*`, MathType OLE payloads, relationship files, media, and
custom XML.

Before applying text replacements, the script must refuse paragraphs containing
MathType, Word equations, OLE objects, drawings, images, field codes,
hyperlinks, footnotes, endnotes, comments, citation-manager fields, or other
complex OOXML. Report those paragraphs as manual items instead of rebuilding
them. Preserving formulas and variables has priority over applying an automatic
wording change.

For `.docx` manuscripts, color every main-text `Fig.`, `Figure`, `Table`,
`Appendix`, and numbered citation marker such as `[1]`, `[1,2]`, or `[1-3]`
in blue `#0000FF`, which is RGB `(0, 0, 255)`, unless the user requests another
color. Do not color captions, references, headers, footers, text boxes, fields,
or unsafe runs containing complex OOXML. For paragraphs that contain formulas or
tracked changes, color only safe plain-text runs and preserve the complex
objects.

Run the formatter during polishing:

```bash
python <skill_base>/scripts/polish_docx.py INPUT.docx changes.json OUTPUT.docx --color-crossrefs
```

For color-only formatting:

```bash
python <skill_base>/scripts/polish_docx.py --color-crossrefs INPUT.docx OUTPUT.docx
```

### Tool Failure Recovery

If a file-writing tool fails because required fields such as `file_path` or
`content` are missing, stop using that file-writing tool for the current
operation. Continue with this fallback:

1. Reuse the latest input `.docx` and the existing run folder.
2. Create only a `changes.json` plan if text edits are needed.
3. Run `scripts/polish_docx.py` with the existing command shape.
4. Add `--color-crossrefs` when figure, table, appendix, or citation coloring
   is needed.
5. Report the recovery in the audit.

Do not retry a broken write-tool call repeatedly. Do not create ad hoc scripts
for routine compression, parenthetical rewriting, or cross-reference coloring.

### Step 3. Report

Tell the user:

1. Run folder path.
2. Output file path.
3. Number of changes applied.
4. Number of figure, table, appendix, and citation mentions colored blue.
5. Changes that could not be found or safely applied.
6. Manual items for equations, images, fields, text boxes, headers, footers, or
   citation-manager fields.

## Output Rules

- Primary output for `.docx`: tracked-changes document.
- Secondary output: Markdown change log with original text, polished text, and
  reason.
- Sentence-level polishing should rewrite avoidable parenthetical wording into
  non-parenthetical prose while preserving all scientific information,
  technical notation, and citation integrity.
- Audit abbreviations in final manuscript polishing. Check first-use
  definitions, consistency, and ambiguous expansions without inventing missing
  definitions.
- In Word outputs, format main-text figure, table, appendix, and numbered
  citation mentions in blue `#0000FF`.
- For risky claims, add `Claim risk:` with the exact phrase to verify.
- For missing facts, mark `AUTHOR_INPUT_NEEDED`.
- Maintain a consistent English variant within the supplied text.
- Run a claim risk pass before finalizing polished prose. Prefer language that
  is both evidence-calibrated and worth reading when the original wording
  overstates or understates the supplied evidence.
- Run a narrative preservation pass for foreground sections. Mark
  `NARRATIVE_WARNING` when the polished text lacks field tension, synthesis, or
  a take-home message.
- Preserve numbers, method names, metric names, citation keys, equations,
  dataset names, and statistical qualifiers while softening claims.
- Run a content-risk pass for full manuscripts. Mark `Claim risk` or
  `AUTHOR_INPUT_NEEDED` when polishing reveals empty sections, table-only
  sections, missing profile-required setup or method details, future work that
  lists evidence needed for the central claim, or a claim stronger than the
  available diagnostics.
- Run a visual-language pass for full manuscripts. Check figure captions,
  figure titles, table titles, axis terms, abbreviations, and main-text figure
  references for consistent terminology.
- Mark `Claim risk` when the title is stronger than the evidence boundary,
  when result granularity is weaker than the advice level, when a low-support
  condition supports a strong boundary claim without sensitivity or
  uncertainty, or when a profile-required display or reference target is missing
  without a documented reason.
- Clean internal workflow artifact language from the main text. Use scholarly
  wording and move raw file names, source-code paths, diagnostic file names, and
  figure-map names to a reproducibility statement or appendix.

## Limitations

- The script handles normal body paragraphs and table-cell paragraphs.
- Equation objects, images, charts, text boxes, headers, footers, comments,
  footnotes, endnotes, fields, and citation-manager fields require manual
  review unless future tooling explicitly supports them.
- Paragraphs containing MathType, formulas, OLE objects, drawings, field codes,
  hyperlinks, comments, footnotes, endnotes, or citation-manager content must
  be skipped for automatic text replacement and reported as manual items.
- Insertions use the formatting of the first affected run. Complex mixed-run
  formatting may need manual cleanup in Word.
