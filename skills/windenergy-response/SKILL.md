---
name: windenergy-response
description: >-
  Draft, audit, or revise point-by-point reviewer response letters for the 18
  target energy, power-system, AI, and pattern-recognition journals used by
  wind-power and AI-for-energy manuscripts, including Renewable Energy, Applied
  Energy, Energy, Energy Conversion and Management, Energy Reports, Energy and
  AI, IJEPES, EPSR, SETA, SEGAN, Applied Soft Computing, Information Sciences,
  Neurocomputing, Knowledge-Based Systems, Pattern Recognition, Engineering
  Applications of Artificial Intelligence, Expert Systems with Applications,
  and Computers and Electrical Engineering. Use when the user provides reviewer
  comments, editor decision letters, revision notes, response drafts, rebuttal
  letters, response to reviewers, peer-review reports, council-review requests,
  multi-expert reviewer analysis, revision direction summaries, major revision,
  minor revision, rejection resubmission, 审稿意见回复, 逐点回复, 审稿意见评价,
  多专家分析, 修改方向总结, 大修, 小修, 拒稿转投, 修回信, or 如何回复 reviewer.
---

# Renewable Multi-Journal Reviewer Response

Use this skill to convert editor letters, reviewer comments, author notes, or
draft rebuttals into a traceable response package for target-journal revisions.

## Router Protocol

Read `manifest.yaml`, load all `always_load` files, and then load on-demand
references only for the active task. Use `references/revision-council.md` for
`council-review`; use `references/qa-checklist.md` before final delivery.

Before writing generated files, load `../_shared/core/output-run-folders.md`
and create a run folder for this invocation. Put response drafts, action maps,
revision plans, and tracked outputs in that run folder.

## Default Stance

- Preserve each reviewer comment faithfully before responding.
- Answer every concern with a manuscript change, evidence-based explanation,
  justified disagreement, or `AUTHOR_INPUT_NEEDED`.
- Map replies to manuscript locations when line, page, or section information
  is available.
- Stay respectful, concise, and factual.
- Do not invent new experiments, citations, figures, line numbers, editor
  instructions, or reviewer identities.

## Workflow

1. Read `references/intake-and-routing.md`.
2. Build a comment inventory by reviewer and topic.
3. Classify each concern using `references/comment-taxonomy.md`.
4. For council-review, load `references/revision-council.md` and run the
   energy, AI, and math or physics perspectives before drafting responses.
5. Map each response action using `references/action-mapping.md`.
6. Use `references/response-structure.md` and `references/tone-and-stance.md`
   for final wording.
7. Use `references/difficult-cases.md` when a request is impossible, out of
   scope, conflicting, or unsupported by available data.

## Council-Review Mode

Use `council-review` when the user asks for reviewer-comment evaluation,
multi-agent or multi-expert analysis, revision direction, major-revision
strategy, minor-revision triage, or rejection-resubmission planning.

Required outputs:

- `revision_council_plan.md`: Chinese unified revision plan with comment
  inventory, three expert summaries, consensus table, priority tiers, and
  author-decision items.
- `response_draft.md`: English point-by-point response draft grounded in the
  approved revision direction.
- `reviewer_pattern_update.md`: reusable reviewer-pattern notes for the
  cumulative memory file.

When a `.docx` manuscript is supplied, use it only for extraction and planning
inside this skill. Any tracked manuscript edits must be routed through
`../windenergy-polishing/scripts/polish_docx.py` and its protected-content rules.
Do not run legacy `paper_revision_helpers.py` or `apply_minimal_revisions.py`
for automatic Word rewriting.

## Target-Journal Awareness

- For resubmission, preserve the editor's requested format exactly.
- For transfer after rejection, separate old-reviewer response material from new
  submission documents.
- For double-anonymized targets, ensure response packages and revised files do
  not expose author identity if the journal requires anonymized review.

## Output

Return reviewer comments and author responses in a point-by-point format.
Include an action list for unresolved facts, missing line numbers, or manuscript
changes that the author still needs to make. If files are written, report the
run folder path.
