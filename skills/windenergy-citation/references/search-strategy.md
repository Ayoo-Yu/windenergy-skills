# Citation Search Strategy

## Claim Types

| Claim type | Search pattern |
|---|---|
| Background | `[application domain] review [core problem]` |
| Method | `[method family] [energy task]` |
| Physical or system mechanism | `[profile physical or operational terms] [mechanism]` |
| Dataset | `[data source type] [energy asset or system] dataset` |
| Baseline | `[task] benchmark baseline` |
| Limitation | `[task] generalization robustness limitation` |
| Grid or decision value | `[task] [decision value] renewable integration` |
| Target-journal coverage | `[claim terms] "[target journal title]"` |

## Evidence Fit

- Direct support: same energy asset, task, and evidence type.
- Partial support: same task but different renewable source, or same method in a
  neighboring power-system task.
- Weak support: generic AI/time-series paper with no energy context.

## Target-Journal Coverage

- For a named target journal, count cited references published in that journal
  only when the active profile defines this coverage check.
- If the active profile has a target-journal coverage target and the count is
  low, search the target journal for papers that directly support existing
  manuscript claims.
- Do not add loosely related papers for numerical coverage.

## Output Pattern

For each recommended citation, report:

```text
Claim: [claim being supported]
Recommended source: [authors, year, title, journal, DOI]
Fit: direct / partial / weak
Use for: [exact manuscript sentence or narrowed claim]
Risk: [preprint, metadata conflict, broad claim, old baseline, etc.]
```
