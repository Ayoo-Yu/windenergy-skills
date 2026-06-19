# Section: Conclusion (writing)

## Core Rule

Conclusion is the final judgment AFTER the reader has seen all evidence.
It must be more mature than the Abstract, not a compression of Results.
Its interpretation ceiling is **synthesize** -- no new depth beyond what
Discussion already established.

## Default structure

Four-paragraph template:

### Paragraph 1: Contribution synthesis

Restate the solved problem and core technical contribution in one
sentence. Do not summarize each experiment. State the contribution
hierarchy:
- Primary: the main method or framework contribution.
- Secondary: the empirical finding or mechanism insight.
- Tertiary: the practical guideline or operational boundary (when applicable).

### Paragraph 2: Decisive evidence

State the strongest 1-2 pieces of evidence that support the primary
contribution. Use precise numbers but fewer than in Results.
Do not introduce evidence not presented in Results or Discussion.

### Paragraph 3: Implication and boundary

State what the evidence means for the field. Frame implications as
narrower than or equal to the evidence scope. State the operating
boundary where the conclusion stops holding.

### Paragraph 4: Future direction

One concrete next step that follows from the evidence and its
limitations. Not generic "more work is needed." Must be specific
enough that another researcher could design the study.

## Drafting rules

- No new data. No unsupported promises.
- Restate the central contribution in one sentence. Do not summarize each
  Result figure.
- The implication must be narrower than or equal to the scope of the
  evidence.
- A bounded future-work pointer is acceptable, but generic "more work is
  needed" is not.

### Abstract vs Conclusion differentiation

| Aspect | Abstract | Conclusion |
|--------|----------|------------|
| Purpose | First contact, attract reading | Final judgment after evidence |
| Evidence | Preview, 0-2 anchor numbers | Confirmed evidence from Results |
| Contribution | Preview what will be shown | Synthesize what was established |
| Future work | None | One bounded direction |
| Length | Journal-specified (150-250 words) | Flexible, proportional to paper |
| Tone | Compressed, forward-looking | Reflective, bounded |

Common failure: Conclusion paragraphs that are the Abstract with
synonyms swapped. If the Conclusion could be swapped with the Abstract
and neither reader would notice, the Conclusion needs rewriting to
reference specific evidence and state bounded implications.

### Evidence-scoped recommendation framing

When the paper includes practical recommendations from experimental
evidence:
- Frame recommendations from the evidence: "Under [tested conditions],
  method X achieves [result], suggesting it as a candidate when
  [operating constraint]."
- Always qualify with the evidence scope: "within the tested conditions",
  "based on this study's evidence", or "as a starting point". Do not
  make absolute recommendations unless the evidence exhaustively covers
  the claim scope.
- State the conditions tested and the gap to full validation.

For benchmark papers, load the `benchmark-paper` paper-type fragment for
additional benchmark-derived recommendation qualifiers.

## Overclaim check

Before finalizing, run the check:

- Does each claim trace back to evidence in this paper?
- Are mechanism words (`demonstrates`, `proves`, `establishes`) backed by
  the right study design?
- Is the scope of the implication narrower than or equal to the scope of
  the evidence?
- Is any "first" claim genuinely first within a stated scope?
- Is the Conclusion substantively different from the Abstract, not just
  reworded?

## Deeper reference

For full conclusion structure (contribution-evidence-impact-limitation-future),
open `references/conclusion.md`.

## Cross-References

- Interpretation ceiling: `section-role-matrix.md` (Conclusion = synthesize)
- Claim strength ladder: `quality-principles.md`
- Full conclusion template: `references/conclusion.md`
- Abstract vs Conclusion differentiation: this file, table above
