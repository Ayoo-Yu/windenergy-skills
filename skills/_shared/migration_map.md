# Layered Refactor Migration Map

This map records where rules moved during the layered refactor. Use it to keep
core rules generic and to prevent specialized rules from drifting back into
global skill instructions.

| Source rule | Moved to | Reason |
|---|---|---|
| Claim strength control | `_shared/core/quality-principles.md` | Cross-topic scientific writing rule. |
| Evidence chain and no fabrication | `_shared/core/quality-principles.md` | Cross-topic integrity rule. |
| Abstract take-home message and high-impact framing | `_shared/core/narrative-principles.md` | Cross-topic narrative rule for foreground sections. |
| Fixed word count targets | `_shared/fragments/journal/*.md` | Journal and article-type dependent. |
| Fixed reference scale targets | `_shared/fragments/journal/*.md` | Journal and article-type dependent. |
| Fixed display-item and figure-count targets | `_shared/fragments/journal/*.md` and `_shared/fragments/paper_type/*.md` | Depends on article type and venue. |
| Kupiec, Christoffersen, interval score, matched-width, matched-reliability controls | `_shared/fragments/topic/conformal-calibration.md` | Topic-specific diagnostics. |
| Coverage axis and reliability plotting rules | `_shared/fragments/topic/probabilistic-forecasting.md` | Topic-specific visualization and evaluation issue. |
| Data source, sampling, splits, inputs, preprocessing checklist | `_shared/core/quality-principles.md` as generic provenance, with topic details in topic fragments | Generic need, topic-specific fields vary. |
| NWP, curtailment, capacity scaling, lead-time wording | `_shared/fragments/topic/wind-power-forecasting.md` | Wind forecasting specific. |
| Four wind farms, four predictors, 24 horizons, 3528 tests, named predictor conclusions | `_shared/fragments/manuscript/wind-conformal-benchmark.md` | Single benchmark evidence. |
| Applied Energy main-body word target and reference scale | `_shared/fragments/journal/applied-energy.md` | Journal-specific readiness target. |
