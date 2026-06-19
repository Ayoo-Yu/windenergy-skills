# Paper Type Fragment: Benchmark Paper

## Activation Condition

Load when the contribution is a dataset, testbed, benchmark protocol, or
systematic evaluation.

## Scope

Use for task definition, fairness, repeatability, baselines, metric rationale,
and evidence coverage.

## Allowed Content

Benchmark cells, data splits, comparison fairness, metric definitions, coverage
of conditions, reporting granularity, and reproducibility package details.

## Forbidden Content

One benchmark's counts, named models, or result conclusions unless supplied by a
manuscript fragment.

## Output Influence

The manuscript should explain why the benchmark design answers a field question,
not only list many runs.

## Audit Influence

Audits check whether the benchmark protocol and evidence coverage match the
claims.

## Benchmark-Derived Recommendation Rules

When a benchmark paper includes practical recommendations or method selection
guidance, apply these rules:

### In Discussion
- Frame operational recommendations as conditional rules derived from the
  tested conditions: "When [condition], consider [action] because
  [evidence-linked reason]."
- Always qualify as "benchmark-derived", "starting point", or "within the
  tested conditions".
- State the boundary where the recommendation stops being reliable.
- Do not present benchmark findings as validated deployment strategy.
- Recommendations are heuristic selection principles, not universal rules.

### In Conclusion
- Frame recommendations from the benchmark evidence: "Under [tested
  conditions], method X achieves [result], suggesting it as a candidate
  when [operating constraint]."
- Always qualify with "within this benchmark" or "benchmark-derived
  selection principles".
- Do not make absolute recommendations unless the benchmark exhaustively
  covers the claim scope.
- State the conditions tested and the gap to full deployment.

## Examples

"The benchmark varies data regimes, methods, and operating conditions to test a
general claim."

"When the benchmark covers multiple residual structures, the resulting
benchmark-derived selection rules may guide initial method choice, though
deployment validation remains necessary."

## Anti Examples

"This fragment hard-codes a particular number of runs or tasks."

"Dynamic calibration is the recommended approach for high-coverage scenarios"
(without "within this benchmark" qualifier).
