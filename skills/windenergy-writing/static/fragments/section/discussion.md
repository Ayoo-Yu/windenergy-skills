# Section: Discussion (writing)

## Core Rule

Discussion answers "what do the results mean?" It does NOT re-report what was
observed. Its interpretation ceiling is **interpret** -- the highest active
reasoning level in the paper.

## Default structure

`central advance -> what the evidence means -> relation to prior work -> constraints / limitations -> future use or open questions`

### Structural expansion

1. **Central advance paragraph**: Open with the strongest interpretation
   the evidence supports. State the mechanism or boundary the paper
   establishes. Do not start by repeating Result numbers.

2. **What the evidence means** (2-4 paragraphs): For each major finding,
   move beyond restatement. Apply the three-layer meaning framework:
   - Layer 1 (Statistical mechanism): What the diagnostics reveal about
     method behavior -- e.g., score decomposition, test pass rates,
     distribution shifts.
   - Layer 2 (Evaluation implication): What this means for how the field
     should measure and compare methods -- e.g., why single-metric rankings
     are misleading, which metrics must be jointly reported.
   - Layer 3 (Operational/domain implication): What this means for practical
     deployment -- only when evidence supports it, and always qualified.

3. **Relation to prior work** (1-2 paragraphs): Reconnect to literature
   from Related Work. State where findings agree, contradict, or extend
   prior studies. Do not introduce new citations not in Related Work.

4. **Constraints and limitations** (1 paragraph, structured): Name the
   specific condition, dataset regime, or assumption where the
   interpretation stops holding. Do not use generic disclaimers. Organize
   by category:
   - Data and task boundary
   - Diagnostic granularity boundary
   - Causal explanation boundary
   - External transfer boundary

5. **Future direction** (1 paragraph): State concrete open questions
   that follow from the evidence, not generic "more research is needed."

## Drafting rules

- Discussion **interprets**, it does not repeat Results figure by figure.
- Address rival explanations before generalizing. Reviewers look for this.
- Hedging strength must match evidence strength. Do not promote a "consistent
  with" finding to "demonstrates" wording.
- Limitations come from inside the paper, not from generic disclaimers. Name
  the specific condition or dataset where the result stops holding.

### Anti-repetition rules

- Do not re-list Result table numbers. Reference them by table/figure
  number and state the interpretation: "Table 3 shows X, which suggests Y."
- If a paragraph could be moved to Results without losing meaning, it
  belongs in Results, not Discussion.
- The ratio of new reasoning to repeated facts should be at least 3:1.
  If Discussion is mostly restating Results, it has failed.
- Each Discussion paragraph must contain at least one interpretive
  verb (suggests, indicates, reflects, implies, challenges, supports)
  that was not present in the Results description of the same finding.
- When referencing Results, use one sentence to anchor the evidence
  ("As shown in Section 5.2, ..."), then immediately interpret.

### Evidence boundary structure

- Every interpretive claim must state its evidence anchor: which table,
  figure, or experiment supports it.
- When the evidence is ambiguous between two interpretations, state both
  and name the experiment that would distinguish them.
- Do not promote an interpretation beyond its evidence strength.
  Reference the claim strength ladder in `quality-principles.md`.
- Use scholarly language for limitations:
  - "per-time sequence diagnostics are not available for every method cell"
  - "sensitivity under alternative thresholds requires further investigation"
  - NOT: "saved key slices", "diagnostic control file", "revision workspace"

### Operational guidance framing

When the paper's contribution includes practical recommendations:
- Frame recommendations as conditional rules: "When [condition], consider
  [action] because [evidence-linked reason]."
- Always qualify with the evidence scope: "starting point", "within the
  tested conditions", or "based on the available evidence". Do not present
  as universal best practices.
- State the boundary where the recommendation stops being reliable.

For benchmark papers, load the `benchmark-paper` paper-type fragment for
additional benchmark-derived recommendation qualifiers.

## Sentence syntax

Discussion sentences interpret:

- `may reflect`
- `suggests that`
- `could indicate`
- `is likely due to`
- `may facilitate`
- `is more consistent with ... than with ...`
- `challenges the assumption that ...`
- `extends the finding in [citation] by ...`

## Common failure modes when drafting

- Re-summarizing Results instead of interpreting them.
- Skipping rival explanations.
- Omitting boundaries: when does the interpretation stop holding?
- Future-work statements that read as marketing, not as honest open questions.
- Writing to preempt reviewer objections rather than to explain the
  finding (see review-defensive tone in `narrative-principles.md`).
- Giving unconditional deployment advice without evidence scope qualifier.

## Short rule to memorize

- Results = what we observed (observe)
- Discussion = why we think it happened, when it may fail, and what it
  means compared to what others found (interpret)
- If Discussion reads like Results with hedging words inserted, rewrite it.

## Cross-References

- Interpretation strength ceiling: `section-role-matrix.md` (Discussion = interpret)
- Claim strength ladder: `quality-principles.md`
- Review-defensive tone: `narrative-principles.md`
- Internal language replacement: `quality-principles.md`
