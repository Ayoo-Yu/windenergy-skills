# Renewable Section Role Matrix

Use this matrix before drafting, revising, polishing, or auditing a manuscript
section. It is core guidance and must stay topic neutral.

## Core Rule

Each section has a distinct job. Do not let one section borrow the job of
another section unless the target journal explicitly requires a combined
structure.

## Section Roles

| Section | Role | Allowed content | Boundary | Interpretation ceiling |
|---|---|---|---|---|
| Abstract | Whole-paper compression | question, approach, central finding, implication, boundary | no long setup, no full protocol | **compress** (synthesis level): restate and compress; do not interpret or explain mechanism |
| Introduction | Reading necessity | field tension, unresolved question, difficulty, evidence design, contribution preview | no detailed results, rankings, recommendations | **motivate** (below specify): frame tension and gap; do not conclude or rank |
| Related Work | Literature map and gap validation | research lines, assumptions, mechanisms, representative papers, unresolved gaps, novelty boundary | no protocol detail, no result reporting, no journal-readiness logic | **compare**: synthesize literature; do not evaluate this paper's results |
| Methodology | Reproducible method definition | algorithms, assumptions, variables, parameters, implementation choices | no broad literature survey | **define** (below specify): describe protocol; do not justify with results or defend design |
| Experimental Setup | Evaluation reproducibility | data, splits, features, preprocessing, baselines, metrics, protocol | no final interpretation | **specify**: state conditions; do not interpret outcomes or preview results |
| Results | Direct evidence | observations, tables, figures, effect sizes, robustness checks | no unsupported mechanism expansion | **observe**: report measurements; one sentence immediate interpretation per finding allowed; no mechanism explanation |
| Discussion | Meaning and boundary | interpretation, practical implication, limitations, comparison across findings | no new evidence | **interpret**: explain meaning, boundaries, alternatives, literature reconnection |
| Conclusion | Final judgment | synthesis, boundary, take-home message, future path | no new results | **synthesize**: combine established points; no new depth beyond Discussion |

Interpretation ceiling defines the maximum depth of reasoning each section may use. The ladder runs from lowest to highest: specify, observe, compare, interpret, synthesize. If a section's prose moves above its ceiling, it is doing another section's job. The full ladder definition is in `narrative-principles.md`.

## Related Work Role

Related Work = literature map and gap validation. It validates the knowledge gap
through literature synthesis. It should:

- group studies by research line rather than by citation order
- compare assumptions, mechanisms, data settings, evaluation criteria, and
  operational context when relevant
- identify what each line has established
- state what remains unresolved
- delimit the manuscript's novelty without repeatedly explaining the current
  implementation

Related Work should not report the manuscript's detailed results, reproduce
Methodology, justify implementation settings, discuss submission strategy, or
use internal audit language.

## Common Role Collisions

- Introduction becomes an abstract when it announces detailed results.
- Related Work becomes a background tutorial when it teaches definitions without
  comparing studies.
- Related Work becomes Methodology when it explains the current protocol or
  implementation choices.
- Results becomes Discussion when it over-interprets before evidence is shown.
- Conclusion becomes Results when it introduces new numbers.
- Discussion becomes Results when it re-narrates findings without adding
  interpretation.
- Conclusion becomes Abstract when it only compresses results without
  synthesizing a final judgment.

## Section Anti-Patterns

### Abstract
- Do not justify the method choice (Introduction's job).
- Do not report per-baseline comparisons (Results' job).
- Do not explain why results occurred (Discussion's job).

### Introduction
- Do not report numerical outcomes or rankings.
- Do not compare this paper's method to specific baselines with metrics.
- Do not state operating boundaries or selection rules.

### Related Work
- Do not reproduce the manuscript's protocol or implementation choices.
- Do not evaluate the manuscript's own results against cited work.
- Do not use internal audit or submission-strategy language.

### Methodology
- Do not justify design choices by citing this paper's own results.
- Do not include literature survey paragraphs (Related Work's job).
- Do not describe experimental conditions (Setup's job).
- Do not explain mechanisms or causal chains (Discussion's job).
- Do not open with a checklist of what will be covered.

### Experimental Setup
- Do not interpret why a preprocessing step improves results.
- Do not preview which baseline will win.
- Do not include method algorithm descriptions (Methodology's job).
- Do not repeat evaluation protocol already defined in Methodology.

### Results
- Do not explain mechanisms or causal chains.
- Do not connect findings to prior work.
- Do not make practical recommendations.
- Do not use hedging/interpretation syntax (may reflect, suggests that, is
  likely due to) for more than one bridge sentence per finding.
- Do not explain what the paper does NOT do instead of what it DOES.

### Discussion
- Do not repeat Results numbers without adding interpretation.
- Do not introduce new tables or figures.
- Do not re-describe the method.
- Do not present unconditional deployment advice.

### Conclusion
- Do not introduce new numbers, figures, or analyses.
- Do not re-write the abstract with minor wording changes.
- Do not expand interpretation beyond what Discussion already established.
- Do not add new literature citations not discussed earlier.

## Cross-References

- Interpretation strength ladder definition: see `narrative-principles.md`.
- Internal language replacement table: see `quality-principles.md`.
- Review-defensive tone detection: see `narrative-principles.md`.
