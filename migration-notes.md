# windenergy-skills migration notes

Baseline:

- `windenergy-skills`: `20ca94313e18463e1eabf4616f958de94372c434`
- `nature-skills`: `5d2ba1dee1c087be6de8f4a8aad4b27f04974be9`

This update keeps the wind and renewable-energy scope while adopting the newer
`nature-skills` maintenance pattern: short routers, declarative manifests,
static core fragments, on-demand references, eval fixtures, and reproducible
figure assets.

## Common skill mapping

| windenergy skill | nature baseline | update stance |
|---|---|---|
| `windenergy-academic-search` | `nature-academic-search` | Keep free-source default; add workflow routing and optional Scopus/ScienceDirect boundary. |
| `windenergy-citation` | `nature-citation` | Keep final manuscript audit script; add core workflow split and eval framing. |
| `windenergy-data` | `nature-data` | Keep energy data policy details; add core policy split. |
| `windenergy-figure` | `nature-figure` | Adopt backend gate, figure contract, evals, and atlas assets with wind-specific patterns. |
| `windenergy-paper2ppt` | `nature-paper2ppt` | Keep Chinese energy journal-club deck stance; add task fragments and QA contract. |
| `windenergy-reader` | `nature-reader` | Adopt source-format routing while keeping renewable paper and figure-placement rules. |
| `windenergy-response` | `nature-response` | Keep council-review mode and energy response patterns; add core routing split. |
| `windenergy-writing` | `nature-writing` | Already router-style; keep wind-specific paper type, topic, and journal axes. |
| `windenergy-polishing` | `nature-polishing` | Already router-style; keep Word safety and wind journal profiles. |

## Wind-specific additions

- `windenergy-orchestrator` and `windenergy-submission` remain the suite's
  primary differentiators and are not replaced by Nature-generic modules.
- `windenergy-reviewer` adds pre-submission simulated review for energy,
  power-system, wind, and AI-for-energy manuscripts.
- `windenergy-figure/assets` now includes a reproducible wind-energy chart
  atlas generated from synthetic demonstration data.

