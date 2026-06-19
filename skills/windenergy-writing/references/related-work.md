# Related Work Writing Guide

Load `../_shared/core/section-role-matrix.md` with this guide.

## Goal

Write Related Work as a literature map and gap validation section. The section
should synthesize what prior work has established, compare assumptions and
mechanisms across research lines, identify what remains unresolved, and delimit
the manuscript's novelty.

## Literature Role Types

Use these roles to build the coverage matrix before drafting:

1. Foundational work: defines the problem, theory, method family, or evaluation
   concept.
2. Recent direct competitors: papers closest to the manuscript's task, method,
   or claim.
3. Application-domain studies: papers that establish the energy asset, decision
   context, data setting, physical constraint, or operational need.
4. Method-family studies: papers that develop or compare the relevant algorithm
   family.
5. Evaluation or benchmark studies: papers that define metrics, protocols,
   baselines, robustness checks, or evidence standards.
6. Deployment or operational studies: papers that connect technical outputs to
   planning, control, market, reliability, risk, or field use.

## Gap Type Taxonomy

Name the main gap before writing:

- Method gap: existing methods lack a capability or design property.
- Mechanism gap: prior work reports performance but leaves the explanation
  unclear.
- Evaluation gap: evidence is missing, incomparable, weakly controlled, or
  measured at the wrong granularity.
- Application gap: methods are under-tested in the target asset, domain, or
  physical setting.
- Deployment gap: technical results are not connected to operational decisions.
- Evidence gap: claims rely on narrow data, missing baselines, or incomplete
  diagnostics.

## Coverage Matrix

Prepare this table before drafting or use it as an internal checklist:

| Topic bucket | Representative papers | Why relevant | What they cover | What remains unresolved |
|---|---|---|---|---|
| [research line] | [citations] | [role] | [established knowledge] | [gap] |

Every major topic bucket needs representative papers and a clear unresolved
point. If a bucket has too few direct papers, mark coverage as thin or
unchecked rather than filling the section with loosely related sources.

## Synthesis Density Rule

Avoid one-paper-one-sentence listing. A strong paragraph uses this order:

1. Synthesize the common paradigm or assumption across a research line.
2. Cite representative papers compactly.
3. Compare mechanisms, data settings, evaluation criteria, or operational
   context.
4. State the shared limitation or unresolved gap.

## Related Work Boundary Control

Related Work can explain what prior studies do not answer. It should not:

- report the current manuscript's detailed empirical outcomes or numerical
  results
- announce final method rankings or operational recommendations
- reproduce the current experimental protocol or implementation settings
- mention reviewer patches, internal audit files, or submission strategy
- repeat the Introduction's motivation without adding literature synthesis

End each topic by stating the unresolved gap that motivates the next step of
the manuscript. Mention the current paper only when the distinction cannot be
inferred from the gap.

## Topic Design

Use two to four focused topic buckets for most research articles:

1. Application-domain or decision-context literature.
2. Method family or theory closest to the manuscript.
3. Evaluation, benchmark, or evidence-standard literature.
4. Deployment, operational, or boundary literature when relevant.

## Quality Checklist

1. Does the section map research lines rather than teach generic background?
2. Are foundational papers, recent direct competitors, and evaluation papers
   covered when relevant?
3. Does each topic bucket synthesize a shared paradigm before listing papers?
4. Is the gap type clear and connected to the manuscript's contribution type?
5. Are current-paper transitions restrained?
6. Are detailed protocol choices, result numbers, rankings, and recommendations
   left for later sections?
