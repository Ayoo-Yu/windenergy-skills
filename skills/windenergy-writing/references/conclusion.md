# Conclusion Writing Guide

## Goal

Close the paper with clear takeaways and credible limitations.

## Structure

1. Restate solved problem and core technical idea.
2. Summarize strongest evidence from experiments.
3. State practical impact or new insight.
4. Add limitation paragraph.
5. End with concrete future direction.

## Contribution Hierarchy Synthesis

Organize the conclusion around a contribution hierarchy, not around a
chronological summary of experiments:

1. **Primary contribution**: The method, framework, or protocol the paper
   introduces. One sentence restating the core technical idea.
2. **Secondary contribution**: The empirical finding or mechanism insight
   the paper establishes. Reference the strongest 1-2 pieces of evidence.
3. **Tertiary contribution** (when applicable): Practical guidelines,
   operating boundaries, or selection rules derived from the evidence.

Each level must be distinguishable. If the reader cannot tell which
contribution is primary, the hierarchy is unclear.

## Abstract Differentiation in Detail

The Conclusion must differ from the Abstract in substance, not just in
wording:

| Attribute | Abstract | Conclusion |
|-----------|----------|------------|
| Timing in paper | Before evidence | After evidence |
| Evidence status | Previewed | Established |
| Contribution | Forward-looking claim | Backward-looking synthesis |
| Numbers | 0-2 anchor numbers | Selected confirmed numbers |
| Limitations | Brief boundary or none | Specific, evidence-linked |
| Future work | None | One concrete direction |
| Purpose | Attract reading | Deliver final judgment |

If swapping Abstract and Conclusion produces no informational loss,
the Conclusion needs evidence-linked specificity.

## Limitation Guidance

Prefer limitations tied to task goal/setting boundaries, for example:

1. Data regime limitation (e.g., only short sequences).
2. Assumption limitation (e.g., controlled viewpoints only).
3. Deployment scope limitation (e.g., specific sensor setup).

Avoid framing conclusion around fixable implementation flaws unless they critically define your method's scope.

## Distinguish Limitation Types

1. Technical defect: underperforms strong baselines on key metrics or causes unacceptable tradeoff.
2. Scope limitation: bounded by current task setting and still competitive vs. current SOTA.

## Evidence-Scoped Recommendation Framing

When the paper includes practical recommendations derived from
experimental evidence, frame them with explicit qualifiers:

- "Within the tested conditions, ..."
- "These evidence-derived principles suggest ..."
- "Under the conditions studied, ..."

Do not present study findings as validated deployment strategy without
external validation.

For benchmark papers, load the `benchmark-paper` paper-type fragment
for additional recommendation qualifiers.

## Future Work Depth

A conclusion's future-work paragraph must pass the specificity test:

- Vague: "Future work could extend this approach to other domains."
- Specific: "Testing whether the calibration transfer holds across
  wind regimes beyond the temperate-coastal conditions studied here
  would clarify the deployment boundary for operational forecasting."

The specific version names: (1) the open question, (2) the condition
to test, and (3) what the answer would clarify.

Organize future work into 2-3 bounded categories:

- Finer diagnostic granularity (e.g., per-time hit-sequence analysis)
- Controlled ablations (e.g., fixed-width or fixed-coverage experiments)
- Cross-domain transfer (e.g., different wind regimes, solar, load)

## Template

1. This paper addresses [problem] by proposing [method].
2. The key idea is [core insight], which enables [main benefit].
3. Experiments show [main gains] across [datasets/settings].
4. A current limitation is [scope boundary], and extending to [future setting] is an important next step.

## Quality Checklist

1. Does the conclusion state a final judgment, not just compress results?
2. Is the conclusion substantively different from the abstract?
3. Are operational recommendations qualified with evidence scope?
4. Is future work specific enough for another researcher to design the study?
5. Does each claim trace back to evidence already presented?
6. Is the contribution hierarchy clear (primary, secondary, tertiary)?
