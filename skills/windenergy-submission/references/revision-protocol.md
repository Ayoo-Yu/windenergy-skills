# Submission Revision Protocol

Use this protocol after every `full-check`, `word-audit`, `cover-letter`, or
`file-package` task that receives editable manuscript files.

Load `../../_shared/core/output-run-folders.md` before writing files. All
tracked documents, reports, plans, and scan outputs from this invocation belong
inside the run folder.

## Mandatory Two-Stage Output

1. Audit the submission package.
2. Apply every safe text-level fix with tracked changes.

Do not stop at a Markdown audit when a `.docx` file is available and at least
one safe fix exists.

Use `../windenergy-polishing/SKILL.md` as the required tracked-edit engine for
all `.docx` revisions. The submission skill decides compliance requirements and
manual author decisions. The polishing skill applies safe manuscript and
submission-file wording changes with OOXML tracked changes.

For main-manuscript word-count failures, also load
`manuscript-compression-protocol.md`.

## Safe Fixes

Apply these without asking for more author input when the exact old and new text
are known:

- Fresh-submission wording, such as changing `reconsideration` to
  `consideration` in a cover letter.
- Target-journal name, article type, or heading wording when the correction is
  explicitly stated by the audit.
- Highlights character-limit edits when the source claim and numbers already
  exist in the supplied files.
- Declaration heading normalization when the declaration facts are already
  supplied.
- Keyword trimming or reordering when the exact target list is supplied.
- Typographical, grammar, capitalization, and consistency fixes.
- Main-manuscript prose compression where exact replacement text preserves the
  same scientific meaning.

Skip safe exact text fixes when the target paragraph contains MathType,
equations, OLE objects, field codes, citation-manager fields, hyperlinks,
comments, footnotes, endnotes, drawings, or other complex OOXML. Report these
as manual Word edits. Do not rebuild such paragraphs programmatically.

## Manual Fixes

Use `AUTHOR_INPUT_NEEDED` for these:

- New scientific claims, new results, new citations, or reference pruning.
- Major section deletion or scientific reprioritization for word-count
  reduction.
- Adding AI declarations before the author states tool use.
- Adding author details, affiliations, grants, conflicts, CRediT roles, data
  rights, reviewer names, or figure files.
- Double-anonymized review decisions that change author identity disclosure.

## Revision Workflow

1. Build a change plan grouped by source document.
2. Load `../windenergy-polishing/SKILL.md` and follow its Word Output Protocol.
3. Create or reuse the invocation run folder.
4. For each `.docx`, create a changes JSON file with exact `old`, `new`, and
   `note` fields.
5. Run `scripts/apply_submission_revisions.py` or
   `../windenergy-polishing/scripts/polish_docx.py`.
6. Name outputs with `_submission_tracked.docx` inside the run folder.
7. Update the final response and audit report with:
   - run folder path
   - revised file paths
   - applied change count
   - not-applied changes
   - remaining manual items

## Tool Failure Recovery

If a file-writing tool fails with missing required fields such as `file_path` or
`content`, do not keep retrying that tool call. Use the existing run folder,
write or reuse a changes JSON plan, and run the existing bundled script:

```bash
python ../windenergy-polishing/scripts/polish_docx.py INPUT.docx changes.json OUTPUT.docx --color-crossrefs
```

Do not create ad hoc scripts for routine submission polishing, second
compression passes, cross-reference coloring, or citation-marker coloring.

## Required Report Language

Separate results into:

- `Applied tracked revisions`: fixes already written to revised `.docx` files.
- `Applied tracked manuscript compression`: main-manuscript compression already
  written to revised `.docx` files.
- `Manual author decisions`: items requiring facts, approval, citations, or
  scientific judgment.
- `Still unchecked`: items lacking files or metadata.

Do not label safe exact text replacements as `AUTHOR_INPUT_NEEDED`.
