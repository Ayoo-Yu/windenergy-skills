# Manuscript Gap Audit

Use this reference when comparing a draft manuscript with a learned target
journal profile.

## Audit Priorities

1. Abstract structure and length.
2. Introduction logic, contribution placement, and citation density.
3. Results and discussion balance.
4. Quantitative claim support.
5. Figure-reference density, caption specificity, and panel layout signals.
6. Table and nomenclature load.
7. Conclusion specificity and limitation handling.

## Severity Rules

Use `BLOCKER` when a mismatch can harm review readiness:

- Missing abstract, introduction, results, discussion, or conclusion.
- Central claim lacks a quantitative result or display item.
- Figures or tables are cited inconsistently.
- The manuscript materially exceeds or undershoots a strong target-journal
  norm.

Use `MAJOR` for structural or style mismatches that need revision:

- Abstract has the wrong move order.
- Introduction reports too many detailed results before the contribution
  paragraph.
- Results paragraphs read like methods or audit logs.
- Captions omit metric, unit, sample, or interpretation.

Use `MINOR` for local density and consistency issues:

- Sentence length is outside the profile range.
- Repeated hedging or repeated connector pattern.
- Inconsistent figure naming.

Use `INFO` for measurement caveats and profile-strength notes.

## Output Shape

Write a Markdown audit with:

- summary table.
- profile strength and corpus coverage.
- manuscript metrics.
- ranked issues.
- section-specific revision targets.
- downstream handoff notes for writing, polishing, and figure skills.

Write a JSON audit with the same issue ids, severities, evidence fields, and
recommended downstream skill.
