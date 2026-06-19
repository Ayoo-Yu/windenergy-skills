# Example: council-review

## Minimal Input

Reviewer 1 asks for clearer novelty over recent hybrid PV forecasting studies.
Reviewer 2 asks for stronger ablation experiments and better uncertainty
analysis. Reviewer 3 asks for a clearer physical interpretation of the governing
equations and the boundary conditions.

## Expected Output Structure

### comment inventory

| ID | Reviewer | Comment focus | Required action |
| --- | --- | --- | --- |
| R1.C1 | Reviewer 1 | Novelty and positioning | Add targeted comparison and sharpen contribution claims |
| R2.C1 | Reviewer 2 | Ablation and uncertainty | Add ablation table and uncertainty discussion |
| R3.C1 | Reviewer 3 | Mathematical physics | Explain assumptions, governing equations, and boundary conditions |

### three expert summaries

Energy Domain Expert: prioritize system relevance, renewable-energy context,
benchmark choice, and practical implications.

AI and Computer Science Expert: prioritize model ablation, baseline fairness,
uncertainty calibration, reproducibility, and implementation clarity.

Math and Physics Expert: prioritize equation consistency, physical assumptions,
boundary conditions, dimensional reasoning, and interpretation of parameters.

### consensus table

| Issue | Energy view | AI view | Math and physics view | Consensus action |
| --- | --- | --- | --- | --- |
| Novelty | Link claims to renewable use case | Compare against recent ML baselines | State where physics constraints matter | Rewrite novelty paragraph and add comparison |
| Validation | Add practical metrics | Add ablation and uncertainty | Check assumptions and units | Add one validation subsection |

### priority plan

P0: Fix claims that could be judged as overstated or unsupported.

P1: Add ablation, uncertainty analysis, and targeted literature comparison.

P2: Improve wording, response tone, and figure or table explanations.

### author decision items

1. Confirm whether new experiments can be run within the revision window.
2. Confirm which recent hybrid PV forecasting papers should be treated as key comparators.
3. Confirm whether physical boundary-condition details belong in the main text or supplement.

### English response draft

Response to Reviewer 1, Comment 1:
Thank you for pointing out the need to clarify the novelty of the work. We have
revised the Introduction and Related Work sections to position the proposed
approach against recent hybrid PV forecasting studies, and we now state the
specific contribution more explicitly.

Response to Reviewer 2, Comment 1:
We agree that additional validation improves the credibility of the method. We
have added an ablation study and expanded the uncertainty analysis to show the
effect of each major component.

Response to Reviewer 3, Comment 1:
Thank you for requesting a clearer physical interpretation. We have revised the
method section to define the assumptions, boundary conditions, and parameter
meaning more explicitly.
