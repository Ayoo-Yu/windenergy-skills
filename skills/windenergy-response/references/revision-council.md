# Revision Council Mode

Use this reference for `council-review`, when reviewer comments need a
multi-expert judgment before drafting the response letter or editing the
manuscript.

## Inputs

- Manuscript file or extracted paper text.
- Reviewer comments, decision letter, or response draft.
- Revision type: `major`, `minor`, `resubmission`, or `transfer`.
- Target journal when known.

If the full paper is too long, give each expert the title, abstract, section
map, methods, experiments, discussion, tables, figure captions, and any section
named by reviewers. Every expert must receive all reviewer comments.

## Expert Passes

Run three independent perspectives. Use sub-agents in parallel when available;
otherwise write the three analyses sequentially and keep labels clear.

### Energy Domain Expert

Focus on wind power, renewable-energy integration, power-system operation,
forecasting value, physical constraints, datasets, and journal scope.

For each comment, provide:

- Classification: `ACCEPT`, `PARTIAL`, `REJECT`, or `AUTHOR_INPUT_NEEDED`.
- Manuscript target: section, paragraph, table, figure, equation, or claim.
- Proposed fix and reason.
- Energy-specific risk or opportunity.

### AI and Computer Science Expert

Focus on model design, baselines, ablation, metrics, uncertainty,
generalization, reproducibility, training protocol, and statistical comparison.

For each comment, provide:

- Classification and proposed fix.
- Missing experiment or analysis when needed.
- Claim or response text that must be softened.
- AI-method risk that reviewers may recheck.

### Math and Physics Expert

Focus on equations, notation, assumptions, objective functions, dimensional
consistency, statistics, wind physics, and uncertainty statements.

For each comment, provide:

- Classification and proposed fix.
- Mathematical or physical correction if needed.
- Assumption that should be stated more clearly.
- Concern that requires author data or manual confirmation.

## Council Synthesis

Build a consensus table:

| Reviewer comment | Energy | AI and CS | Math or physics | Consensus |
|---|---|---|---|---|
| R1.1 summary | ACCEPT | PARTIAL | N/A | ACCEPT with AI refinement |

Resolve disagreements this way:

- Three experts agree: put in Priority 1.
- Two experts agree: put in Priority 2 and keep the dissenting caveat.
- No clear majority: put in Author Decision Items.
- A reviewer asks for work outside current evidence: propose a scoped response,
  a limitation, or author input.

## Output Shape

Write `revision_council_plan.md` in Chinese:

```markdown
# 统一修订方案

## Comment Inventory
[Reviewer, comment id, short summary, topic, evidence needed]

## 三专家意见摘要
[Energy, AI and CS, Math or physics summaries]

## 共识表
[One row per reviewer comment]

## Priority 1: 必须修改
### R1.1: [审稿意见摘要]
- 操作: [具体修改]
- 位置: [section or paragraph]
- 理由: [why it answers the concern]
- 回复草稿: [English response seed]

## Priority 2: 建议修改
[2 of 3 experts support or medium-risk issue]

## Author Decision Items
[Conflicts, new experiments, data access, added citations, or scope choices]
```

Write `response_draft.md` in English:

```markdown
# Response to Reviewers

Dear Editor,

We thank the editor and reviewers for their constructive comments. We have
revised the manuscript and provide point-by-point responses below.

## Reviewer 1

**Comment R1.1:** [verbatim comment]

**Response:** [specific answer grounded in supplied evidence]

**Changes in manuscript:** [section, paragraph, table, or author input needed]
```

Write `reviewer_pattern_update.md` with:

- High-frequency reviewer themes.
- Methodology expectations.
- Journal-specific preferences.
- Preventive checklist for future submissions.

Append durable lessons to `reviewer_patterns/_cumulative.md` when the revision
cycle is complete.

## Safe Routing

- Use this skill for analysis, planning, response drafting, and reviewer-pattern
  memory.
- Use `windenergy-citation` for DOI, metadata, reference-list, or claim-support
  checks.
- Use `windenergy-submission` for final package readiness.
- Use `windenergy-polishing` for tracked `.docx` manuscript edits.
- Do not run `paper_revision_helpers.py` or `apply_minimal_revisions.py` for
  automatic Word rewriting.
