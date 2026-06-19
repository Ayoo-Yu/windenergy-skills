# Manuscript Compression Protocol

Use this protocol when the main manuscript exceeds the target word or page
limit and an editable `.docx` file is available.

## Required Behavior

Do not stop at advice. Produce a tracked-changes manuscript revision whenever
there are safe prose-compression opportunities.

## Polishing Skill Handoff

Load `../windenergy-polishing/SKILL.md` and use its Word Output Protocol for the
main manuscript. This protocol supplies the submission-specific trigger,
protected-content rules, and required reporting. The actual `.docx` tracked
edits should use the existing polishing workflow and
`../windenergy-polishing/scripts/polish_docx.py`.

Load `../../_shared/core/output-run-folders.md` before writing files. Put the
manuscript scan, changes JSON, tracked manuscript, and compression note in the
same run folder as the submission audit.

## Compression Triage

- Small overage: up to 10 percent or up to 800 words over the target. Apply a
  safe compression pass immediately.
- Medium overage: 10 to 25 percent over the target. Apply a safe compression
  pass and list remaining section-level decisions.
- Large overage: more than 25 percent over the target. Apply only low-risk
  compression and ask the author to choose section-level cuts.

## Safe Compression Targets

Apply tracked changes to:

- Repeated motivation sentences.
- Long transitions that restate the same result.
- Redundant phrases such as `It is worth noting that`, `In order to`, and
  `the results clearly demonstrate that`.
- Over-detailed training, implementation, or interpretability prose when the
  same details already appear in equations, tables, figures, appendices, or
  supplementary material.
- Repeated figure or table narration where the caption already carries the
  detail.

## Protected Content

Do not remove or weaken:

- Main contributions, claims, or quantitative results.
- Dataset descriptions needed for reproducibility.
- Baselines, metrics, ablations, uncertainty, and statistical protocol.
- Physical assumptions, site or system conditions, data-source details, and
  operating constraints.
- Limitations and validity boundaries.

## Workflow

1. Load `../windenergy-polishing/SKILL.md`.
2. Use `../windenergy-polishing/scripts/polish_docx.py --list-blocks
   Manuscript.docx` to identify paragraph block ids.
3. Choose paragraphs from overlong sections named by the audit report.
4. Rewrite only exact paragraphs or exact substrings whose meaning is preserved.
5. Write a changes JSON with exact `old`, `new`, and `note` fields.
6. Run `../windenergy-polishing/scripts/polish_docx.py` or
   `scripts/apply_submission_revisions.py`.
7. Name the output `Manuscript_submission_tracked.docx` inside the run folder
   unless the user requests another name.

## Minimum Output

For any manuscript overage with editable `.docx` input, the final response must
include one of these:

- `Applied tracked manuscript compression`, with output path and approximate
  words removed.
- `Applied tracked manuscript compression: 0`, with a concrete reason such as
  no manuscript file supplied, no exact source text available, or every possible
  change would require author scientific judgment.

## Report Format

```text
Applied tracked manuscript compression:
- Output: [path]
- Changes applied: [N]
- Approximate words removed: [N]
- Remaining overage: [N]

Manual author decisions:
- [reference pruning, citation additions, AI statement, figure files, etc.]
```
