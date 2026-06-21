# Style Learning Report: Applied Energy

Profile name: Applied Energy wind forecasting full-text research v13
Profile strength: `normal`
Article count: 69
PDF count: 69
Excluded count: 11

## Section Coverage

| Section | Count | Share |
| --- | --- | --- |
| abstract | 69 | 1.0 |
| acknowledgements | 44 | 0.638 |
| appendix | 4 | 0.058 |
| case_study | 33 | 0.478 |
| conclusion | 67 | 0.971 |
| data_availability | 1 | 0.014 |
| declaration | 59 | 0.855 |
| discussion | 14 | 0.203 |
| funding | 4 | 0.058 |
| introduction | 69 | 1.0 |
| keywords | 69 | 1.0 |
| methods | 59 | 0.855 |
| nomenclature | 19 | 0.275 |
| references | 69 | 1.0 |
| related_work | 14 | 0.203 |
| results | 16 | 0.232 |
| results_discussion | 6 | 0.087 |

## Downstream Constraints

### Writing

- Use the learned section order when it is compatible with the target journal instructions.
- Make the energy-system value explicit before presenting algorithmic novelty.
- Tie each major claim to a metric, unit, comparison baseline, or figure reference.
- Target abstract length near 196 to 244 words for this profile.
- For full Applied Energy wind-forecasting manuscripts, draft the Conclusion around 500 to 700 words unless the evidence scope is narrow.

### Polishing

- Preserve all supplied numbers, method names, datasets, and citations.
- Replace audit-style wording with claim-first scientific prose when the evidence supports it.
- Keep uncertainty and limitations visible when claims depend on subgroup or regime support.

### Figures

- Make captions self-contained with metric, unit, sample definition, and main interpretation.
- Keep panel order aligned with the claim sequence in the Results section.
- Use consistent colors for method families across the manuscript.
- Target figure caption length near 49 to 68 words when figure complexity is comparable.

### Guardrails

- In Results and Discussion, reserve wind-forecasting importance statements for context. Start result claims with evidence-first templates such as <result_evidence> shows <finding_or_pattern>.
- When unit templates are sparse, use fallback unit framing: kW, MW, and GW for power; kWh, MWh, and GWh for energy; h for forecast horizon or temporal resolution.
- Treat the learned Conclusion word-count distribution as extraction-sensitive when drafting full papers; do not compress a complete Conclusion only to match this corpus median.
- Treat Methods median sentence P75 above 45 words as sentence-splitter noise; keep drafted long Methods sentences below about 35 words.


## Excluded PDFs

- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\002_wind-power-forecasting-with-deep-representation-a-survey.txt`: document_type_excluded:survey; pages=36; words=26375
- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\003_a-review-of-wind-speed-and-wind-power-forecasting-with-deep-neural-networks.txt`: document_type_excluded:review; pages=44; words=32892
- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\008_conditional-aggregated-probabilistic-wind-power-forecasting-based-on-spatio-temp.txt`: introduction_words_below_250; pages=12; words=8920
- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\015_wind-power-forecasting-considering-data-privacy-protection-a-federated-deep-rein.txt`: introduction_words_below_250; pages=11; words=8127
- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\017_a-review-of-predictive-uncertainty-modeling-techniques-and-evaluation-metrics-in.txt`: document_type_excluded:review; pages=46; words=34435
- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\019_a-hybrid-convolutional-llm-paradigm-for-robust-wind-power-forecasting-in-data-sc.txt`: introduction_words_below_250; pages=15; words=10940
- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\042_a-fuzzy-time-series-forecasting-model-with-both-accuracy-and-interpretability-is.txt`: introduction_words_below_250; pages=21; words=15209
- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\048_a-combined-forecasting-model-for-time-series-application-to-short-term-wind-spee.txt`: abstract_words_below_80; pages=27; words=20146
- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\054_turbine-specific-short-term-wind-speed-forecasting-considering-within-farm-wind.txt`: missing_sections:introduction; pages=16; words=11522
- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\075_a-review-and-discussion-of-decomposition-based-hybrid-models-for-wind-energy-for.txt`: document_type_excluded:review; pages=19; words=13950
- `D:\skill\test\style-learning\applied-energy-wind-forecasting-sciencedirect-fulltext-xml-v11\fulltext\079_probabilistic-wind-speed-forecasting-via-bayesian-dlms-and-its-application-in-gr.txt`: topic_mismatch:excluded_electrolyzer; pages=20; words=14391
