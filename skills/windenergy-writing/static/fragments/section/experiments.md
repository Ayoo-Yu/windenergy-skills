# Section: Experiments / Results (writing)

## Default evidence ladder

`system / workflow validation -> main result -> baseline comparison -> ablation / mechanism analysis -> application or generalization -> stress tests / failure modes`

Each subsection has a claim-first opening, then data support.

## Drafting rules

- Stay mainly in past tense.
- Report what was observed, under what conditions, with what quantitative support.
- Use statistics correctly and sparingly. Every test needs a stated hypothesis.
- Use supplementary data sparingly. If a result belongs in the main text, do not hide it in supplements.
- **Each major claim needs comparison, ablation, or stress-test evidence.** If a claim has none, mark it for follow-up rather than drafting around it.

## Results syntax (vs Discussion)

Results sentences usually report:

- `was detected` / `increased` / `showed` / `enabled` / `achieved`

Do not drift into Discussion syntax (`may reflect`, `suggests`, `is likely due to`) unless the transition is intentional and limited to one bridge sentence per finding.

### Bridge sentence pattern

Each major finding may be followed by ONE sentence of immediate
interpretation that connects it to the next analysis step:

- "This pattern motivates the diagnostic analysis in the following
  subsection."
- "Table X shows [observation], which raises the question of whether
  [mechanism]."
- "This reduction is accompanied by [secondary observation], suggesting
  a trade-off explored below."

Do not go beyond this bridge into full mechanism conclusion, operational
recommendation, or literature reconnection. Those belong in Discussion.

## Common failure modes when drafting

- Mixing observation and interpretation in the same paragraph.
- Citing supplementary data when the result should be in the main text.
- Vague comparisons (`higher than control`) without effect size, sample size, or test.
- Per-paragraph claims without per-paragraph evidence.
- Explaining mechanisms or causal chains in Results prose.
- Making practical recommendations (e.g., "suitable for reserve planning")
  in Results. These belong in Discussion.
- Using "this is why the paper avoids..." or similar self-referential
  explanation. Let the evidence speak.

## Review-Defensive Tone Anti-Pattern

In experiment and results sections, review-defensive tone commonly appears as:

- Explaining why a baseline was chosen before presenting the comparison
  result. Present the comparison; justify the baseline choice in one
  sentence.
- Preemptively acknowledging limitations inside result paragraphs.
  Limitations belong in Discussion.
- Over-justifying preprocessing steps with defensive language
  ("To avoid potential data leakage, which is a common concern...").
  State what was done; justify briefly if non-obvious.
- Adding "we note that" or "it is important to emphasize" before
  results that the author fears might be questioned. Let the numbers
  speak; discuss caveats in Discussion.
- Naming reviewer concerns explicitly: "To prevent concerns about
  hidden temporal leakage..." instead write "The benchmark uses
  chronological splits without shuffling to prevent temporal leakage."

For full detection rules, see `narrative-principles.md`.

## Inter-Chapter Boundary Management

The experiment and results sections have specific boundaries with
neighboring chapters:

### Results vs Discussion boundary

- Results: "Method A achieves RMSE of 2.3 on Dataset X."
- Discussion: "The lower RMSE of Method A may reflect its explicit
  modeling of temporal structure."
- If the sentence contains an interpretive verb (suggests, reflects,
  indicates, implies, challenges) beyond one bridge sentence, it likely
  belongs in Discussion.
- Results may observe a pattern; Discussion names the mechanism.

### Experiments/Setup vs Methodology boundary

- Methodology defines the algorithm and its parameters.
- Experiments defines the data, splits, baselines, and evaluation
  protocol.
- If you are describing HOW a module works, it belongs in Methodology.
  If you are describing WHAT conditions it was tested under, it belongs
  in Experiments.
- Do not repeat method protocol, metric definitions, or update timing rules
  already defined in Methodology.

### Task selection logic

- Every experiment task must connect to a claim or research question
  stated in Introduction.
- If a task exists only to show the method works on another dataset
  without a stated purpose, remove it or add the purpose.
- State why each task was chosen: what dimension of the claim it tests.
- Example: "[Condition A] was included to test behavior under a different
  operating regime."

## Cross-References

- Interpretation ceiling: `section-role-matrix.md` (Results = observe)
- Review-defensive tone detection: `narrative-principles.md`
- Internal language replacement: `quality-principles.md`
- Full experiment reference: `references/experiments.md`
