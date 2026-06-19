# Reviewer Comment To Skill Gap Example

This example shows how to convert reviewer feedback into transferable renewable
skill improvements. Use it as a pattern when a reviewed draft exposes pipeline
weaknesses.

## Input Comment Types

| Reviewer comment pattern | Abstract skill gap | Skill owner | General repair direction |
|---|---|---|---|
| The title and abstract overstate the mechanism. | Claim strength control is weak. | `windenergy-writing`, `windenergy-polishing` | Calibrate wording to the evidence ladder and flag unsupported absolutes as `Claim risk`. |
| Figures are too few for a data-dense paper. | Display-item coverage is weak. | `windenergy-writing`, `windenergy-figure`, `windenergy-orchestrator` | Use the active paper-type or journal profile to plan enough display items, and record the exception when fewer figures are appropriate. |
| Figures are crowded, inconsistent, too sparse, or use ambiguous axes. | Figure professionalism is weak. | `windenergy-figure` | Enforce profile-compatible font, minimum readable text size, stable colors, clear axes, and conclusion-first captions. |
| A workflow figure is visually clean but scientifically thin. | Figure portfolio design is underchecked. | `windenergy-figure` | Show research object, comparison unit, method families or alternatives, diagnostic layer, and boundary analysis. |
| The method section lacks parameter and timing details. | Method reproducibility is underchecked. | `windenergy-writing`, `windenergy-submission` | Require method settings, assumptions, timing, score functions, and implementation notes when relevant. |
| Results imply a mechanism, but the diagnostic chain is incomplete or only stored in an internal file. | Evidence chain validation is weak. | `windenergy-orchestrator`, `windenergy-writing` | Link every core claim to source artifacts, metrics, figures, tables, code paths, or verified citations, and show central controls in the manuscript. |
| Family-level results are used to recommend concrete methods. | Result granularity is underchecked. | `windenergy-writing`, `windenergy-submission` | Require per-method or method-level evidence before giving method-specific deployment advice. |
| A rare condition supports a strong boundary claim. | Low-support condition evidence is underchecked. | `windenergy-writing`, `windenergy-figure`, `windenergy-submission` | Report sample count, sample share, uncertainty, or sensitivity before using the condition as strong evidence. |
| Related Work is too thin for the journal. | Journal fit is underchecked. | `windenergy-academic-search`, `windenergy-writing` | Audit coverage of the application domain, method family, evaluation criteria, closest alternatives, and reference-pool scale. |
| A section is empty or reads like a placeholder. | Manuscript completeness is weak. | `windenergy-submission` | Block ready status until empty sections, placeholders, and missing core facts are resolved. |
| Main text contains internal file names or pipeline labels. | Reproducibility wording is leaking into the article body. | `windenergy-polishing`, `windenergy-submission` | Translate internal artifacts into scholarly wording and move file names to a reproducibility statement or appendix. |
| References are plausible but not verified. | Citation verification is separate from discovery. | `windenergy-citation` | Run strict citation audit after broad literature discovery. |

## Output Pattern

When asked to analyze reviewer comments for skill improvement, produce:

1. A comment inventory grouped by writing, figures, methods, evidence, literature,
   citation, submission, and orchestration.
2. A skill gap table with owner, current weakness, reusable repair, and whether
   the repair is a general rule or only an example.
3. A prioritized repair plan.
4. A validation plan that tests general behavior on a different manuscript topic.

## Rule Of Abstraction

Do not turn a paper-specific requested experiment into a universal hard gate.
Ask what capability failed. Examples include claim calibration, figure style,
display-item coverage, method reproducibility, evidence traceability, result
granularity, low-support condition handling, literature coverage, citation
accuracy, reproducibility wording, or final manuscript maturity.
