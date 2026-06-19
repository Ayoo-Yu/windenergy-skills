---
name: windenergy-submission
description: >-
  Pre-submission packaging, compliance audit, resubmission, and transfer checks
  for 18 Elsevier energy, power, AI, and pattern-recognition journals used by
  wind-power and AI-for-energy manuscripts. Generates or audits Highlights,
  Cover Letter, CRediT author contributions, generative AI declarations,
  Declaration of Competing Interests, file packaging, word count, reference
  count, journal scope, double-anonymized review readiness, and target-journal
  switch requirements. Use when the user asks to prepare a submission, check
  readiness, adapt a manuscript to another journal, write submission documents,
  run a pre-submission checklist, or check scope fit.
---

# Renewable Multi-Journal Submission Packaging

Use this skill for the final stage between a finished manuscript and journal
submission. It covers 18 target journals listed in
`references/journal-profiles.md`.

Before writing any generated file, load
`../_shared/core/output-run-folders.md` and create a run folder for this
invocation. Put the audit report, tracked `.docx` files, changes JSON, scan
reports, and manifests in that run folder.

For final manuscript readiness, also load
`../_shared/core/quality-principles.md`,
`../_shared/core/narrative-principles.md`, and the active profile when
available. Run a content maturity audit. This audit checks manuscript
completeness, narrative maturity, and claim-evidence alignment in addition to
journal files, declarations, length, and citation integrity.

## Journal Routing

1. Load `references/journal-profiles.md`.
2. Detect the target journal slug. If no journal is named, use `common-18`.
3. If the user names several journals, audit against `common-18` first and then
   list target-specific differences.
4. Use current official English journal instructions when available. Treat
   local `期刊整理` files as a read-only source archive.

## Task Modes

| Mode | Trigger | Reference |
|---|---|---|
| `full-check` | pre-submission, readiness, checklist | `references/submission-checklist.md` plus `references/journal-profiles.md` |
| `highlights` | highlights | `references/highlights-guide.md` |
| `cover-letter` | cover letter | `references/cover-letter-guide.md` and target profile |
| `credit` | CRediT, author contributions | `references/credit-guide.md` |
| `ai-declaration` | AI declaration | `references/ai-declaration-guide.md` |
| `competing` | competing interests | `references/competing-interests-guide.md` |
| `scope-test` | scope check | `references/scope-test.md` and target profile |
| `word-audit` | word count, reference count | `references/word-count-audit.md` and target profile |
| `file-package` | files, packaging | `references/file-packaging.md` and target profile |
| `final-manuscript-audit` | abbreviations, citations, final manuscript consistency | `references/final-manuscript-audit.md` |

Default to `full-check` if the user does not specify a mode.

After any mode that audits editable `.docx` files, load
`references/revision-protocol.md`, then load `../windenergy-polishing/SKILL.md`
as the tracked-edit engine. Apply every safe text-level fix with tracked
changes.

For final manuscript checks, load `references/final-manuscript-audit.md`.
Route abbreviation issues through `windenergy-polishing` and citation issues
through `windenergy-citation`. The citation route must produce `audit.json`
from `../windenergy-citation/scripts/windenergy_citation.py --audit`; if the
audit file is missing or contains any `FAIL` or `UNCHECKED` reference item, do
not report the manuscript ready for submission.
For orchestrator workspaces, require `audits/manuscript_quality_audit.json`,
`audits/figure_consistency_audit.json`,
`diagnostics/profile_evidence_strength_audit.json` when available, or the
legacy `diagnostics/mechanism_evidence_strength_audit.json` during migration,
and `audits/scientific_maturity_audit.json`. If any required file is missing or
has a status other than `PASS`, do not report the manuscript ready.
If the final manuscript audit reports empty sections, placeholders, undefined
core terms, missing experimental setup facts, missing method settings, figure
and table inconsistency, or claim-evidence mismatch, report the manuscript as
`FAIL` or `UNCHECKED` until the issue is resolved.

If the main manuscript exceeds the target word or page limit, also load
`references/manuscript-compression-protocol.md`, route the manuscript through
`windenergy-polishing`, and attempt a tracked manuscript compression pass.

## Compliance Levels

- `PASS`: verified against manuscript or supplied submission files.
- `FAIL`: checked and currently violates the target profile.
- `UNCHECKED`: relevant files or facts were not supplied.
- `AUTHOR_INPUT_NEEDED`: the agent cannot safely infer the fact.

## Safe Auto-Fix Policy

When a `.docx` manuscript is supplied, produce a tracked-changes `.docx` for
safe text-level fixes and a Markdown audit. Use
`../windenergy-polishing/SKILL.md` and its tracked-change script
`../windenergy-polishing/scripts/polish_docx.py`.

Safe auto-fixes:

- Wording, grammar, consistency, hedging, heading labels, and declaration text
  after the user provides the underlying facts.
- Keyword trimming or reordering when the exact replacement is obvious.
- Highlights shortening when the source claim and quantitative result are
  already supplied.
- Cover-letter wording that is clearly stale for the target submission, such as
  replacing `reconsideration` with `consideration` for a fresh submission.
- Main-manuscript prose compression that preserves claims, evidence,
  reproducibility, and physical meaning.

Manual items:

- Removing references, renumbering citations, changing citation style across the
  manuscript, or deciding which citations to keep.
- Adding author details, affiliations, grants, conflicts, CRediT roles, AI-tool
  usage, data access rights, or reviewer suggestions.
- Creating missing figures, graphical abstracts, separate artwork files, author
  photos, bios, checklists, or cover-letter facts.
- Anonymization decisions for double-anonymized journals.
- Adding target-journal citations to satisfy a profile coverage check.
- Major section deletion, reference pruning, or scientific reprioritization for
  word-count reduction.

Mark manual items as `AUTHOR_INPUT_NEEDED` and explain exactly what the author
must provide.

If no safe fixes are applied, state `Applied tracked revisions: 0` and explain
why each remaining issue requires author input or scientific judgment.

For word-count failures, treat the main manuscript as a required polishing
handoff. Either produce `Manuscript_submission_tracked.docx` with safe
compression edits or state `Applied tracked manuscript compression: 0` with the
exact blocker.

## Word Output Protocol

When the input is a `.docx` file, generate:

1. A run folder under `<SOURCE_DIR>/skill_runs/`.
2. `*_submission_tracked.docx` with OOXML tracked changes for safe auto-fixes.
3. A Markdown audit with pass, fail, unchecked, and author-input-needed items.
4. A list of changes that could not be found or could not be safely applied.

Do not use `python-docx` direct replacement for manuscript edits. Direct
replacement removes reviewable revision history.

### Changes JSON

The tracked-changes script accepts the existing interface:

```json
[
  {
    "paragraph_index": 25,
    "old": "exact text",
    "new": "replacement text",
    "note": "short reason"
  }
]
```

It also accepts optional `block_id` values emitted by the script inventory mode.
Use `delete_paragraph` only for safe deletion of author-approved text, not for
reference pruning.

For multiple files, write a plan JSON and run:

```bash
python <skill_base>/scripts/apply_submission_revisions.py PLAN.json
```

Prefer this plan shape so all generated files land in the run folder:

```json
{
  "source_dir": "D:/papers/RE0530",
  "output_dir": "D:/papers/RE0530/skill_runs/20260531-153012_windenergy-submission_renewable-energy",
  "jobs": []
}
```

This wrapper delegates tracked document edits to the existing
`windenergy-polishing` implementation. Use it for submission packets with
several editable files, including the main manuscript.

For manuscript compression triage, list long blocks first:

```bash
python <skill_base>/scripts/scan_docx_blocks.py Manuscript.docx --min-words 80
```

## Report Format

Return:

1. Target journal and profile used.
2. Run folder path.
3. Output `.docx` path when applicable.
4. Applied tracked revisions, with file paths and change counts.
5. Applied tracked manuscript compression, with file path, change count, and
   approximate words removed.
6. Summary counts for pass, fail, unchecked, and author-input-needed items.
7. Full compliance audit grouped by abstract, keywords, highlights, length,
   references, profile citation coverage, abbreviations, citation
   integrity, figures, declarations, review mode, scope, and files.
8. Manual author decisions.
9. Source note stating whether official English guidance was checked.

## Red Lines

- Do not fabricate author details, grants, affiliations, DOIs, reviewer
  suggestions, data-access rights, AI-tool usage, or funding statements.
- Do not write a final AI declaration until the user discloses actual AI-tool
  usage.
- Do not claim a checklist item passes without seeing the relevant manuscript or
  submission document.
- If current journal instructions conflict with this skill, follow the current
  journal instructions and report the conflict.
