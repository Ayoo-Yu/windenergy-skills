# Learned Style Digest: Applied Energy

Profile strength: `normal`
Article count: 69
PDF count: 69
Corpus years: Unchecked

## Architecture

Common detected order:

abstract, keywords, introduction, methods, case_study, conclusion, acknowledgements, declaration, references

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

## Front Matter

Highlights appear in most sampled papers and are concise claim bullets. Keywords appear in every sampled paper.

| Section | Metric | Median | P25 | P75 |
| --- | --- | --- | --- | --- |
| keywords | word_count | 14.0 | 11.0 | 16.0 |
| keywords | sentence_count | 1.0 | 1.0 | 1.0 |
| keywords | median_sentence_words | 14.0 | 11.0 | 16.0 |

## Abstract

The abstract is compact and usually follows context, gap, method, quantified result, and operational implication.

| Metric | Median | P25 | P75 |
| --- | --- | --- | --- |
| word_count | 219.0 | 196.0 | 244.0 |
| sentence_count | 9.0 | 8.0 | 11.0 |
| median_sentence_words | 23.0 | 20.5 | 26.0 |
| numeric_tokens_per_1000_words | 5.03 | 0.0 | 15.71 |

| Move | Count | Share |
| --- | --- | --- |
| context | 69 | 1.0 |
| gap | 41 | 0.594 |
| method | 67 | 0.971 |
| result | 43 | 0.623 |
| implication | 39 | 0.565 |

### Abstract Expression Templates

- Sentence starters: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=55, n=124); wind <target_variable> forecasting is important for <power_system_operation> (docs=51, n=67); however, <gap_statement> (docs=31, n=31); <finding_or_method> can <enable_or_support> <operational_decision> (docs=15, n=20); <method_or_result> is compared with <baseline> (docs=14, n=16); <method> outperforms <baseline> in terms of <metric> (docs=13, n=14)
- Verb preferences: show (27); provide (27); demonstrate (26); propose (26); improve (26); develop (19); outperform (17); address (15)
- Hedging and degree terms: effectively (20); potential (10); significantly (8); consistently (7); indicate (6); may (5); notably (4); could (2)
- Frequent bigrams: wind power (185); wind speed (101); power forecasting (79); wind farms (43); wind farm (36); neural network (31); speed forecasting (26); wind energy (25)
- Frequent trigrams: wind power forecasting (69); wind speed forecasting (26); wind power generation (15); numerical weather prediction (14); accurate wind power (11); power forecasting wpf (8); weather prediction nwp (8); wind speed data (8)
- Move-level normalized templates:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=51, n=67); <renewable_energy_context> creates <operational_need_or_challenge> (docs=11, n=12)
  - gap: however, <gap_statement> (docs=31, n=31); <existing_work_or_system> is limited by <gap_or_uncertainty> (docs=7, n=8)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=55, n=124); this study <method_verb> <method_or_framework> for <forecasting_task> (docs=13, n=13); in this study, <method_or_experiment> is <described_or_evaluated> (docs=9, n=9)
  - result: <method_or_result> is compared with <baseline> (docs=14, n=16); <method> outperforms <baseline> in terms of <metric> (docs=13, n=14); <result_evidence> shows <finding_or_pattern> (docs=11, n=13)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=15, n=20)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=5, n=5)
- Move-level starters:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=51, n=67); <renewable_energy_context> creates <operational_need_or_challenge> (docs=11, n=12)
  - gap: however, <gap_statement> (docs=31, n=31); <existing_work_or_system> is limited by <gap_or_uncertainty> (docs=7, n=8)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=55, n=124); this study <method_verb> <method_or_framework> for <forecasting_task> (docs=13, n=13); in this study, <method_or_experiment> is <described_or_evaluated> (docs=9, n=9)
  - result: <method_or_result> is compared with <baseline> (docs=14, n=16); <method> outperforms <baseline> in terms of <metric> (docs=13, n=14); <result_evidence> shows <finding_or_pattern> (docs=11, n=13)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=15, n=20)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=5, n=5)

## Introduction

The introduction establishes the energy-system setting before narrowing to the method gap and contribution.

| Metric | Median | P25 | P75 |
| --- | --- | --- | --- |
| word_count | 2485.0 | 1373.0 | 5487.0 |
| paragraph_count | 23.0 | 12.0 | 50.0 |
| median_sentence_words | 23.0 | 22.0 | 25.0 |
| citation_markers_per_1000_words | 11.74 | 7.49 | 18.05 |
| numeric_tokens_per_1000_words | 44.12 | 33.1 | 58.28 |
| contrast_terms_per_1000_words | 3.22 | 2.24 | 4.31 |

Recommended moves:

- energy-system context
- field practice or methodological gap
- why the gap matters operationally
- proposed contribution
- evidence design preview

### Introduction Narrative Arc

- Arc sequences: context > context > quantitative > statement > method > method > method (1); context > gap > context > context > result > method > gap (1); context > context > method > method > context > gap > context (1); context > context > literature > gap > statement > gap > context (1); context > gap > result > method > context > implication > method (1)
- Transition starters: the remainder of this paper is organized as follows (2); wpf confronts a multitude of challenges that stem from the (1); in recent decades a plethora of methods have been developed (1); nevertheless existing methods still have some limitations and drawbacks (1); in this paper we aim to answer the following research (1); to address these objectives we propose temporal collaborative attention tcoat (1)
- paragraph_1: moves context (56); statement (4); result (4); starters wind power is a renewable and clean energy source that (1); electricity generation through wind power has remained a well-researched topic (1); wind power is a highly effective renewable energy source for (1)
- paragraph_2: moves context (34); statement (10); method (9); starters wpf confronts a multitude of challenges that stem from the (1); despite these merits wind energy is highly intermittent and uncertain (1); extensive studies have been conducted on wind power forecasting and (1)
- paragraph_3: moves context (27); statement (11); method (8); starters in recent decades a plethora of methods have been developed (1); there are a number of ways to cater large-scale penetration (1); as far as the physical model is concerned numerical weather (1)
- paragraph_4: moves context (15); statement (12); gap (11); starters nevertheless existing methods still have some limitations and drawbacks (1); among these technologies the battery energy storage system bess is (1); regarding statistical models the widely used methods in wind power (1)
- paragraph_5: moves method (15); context (12); statement (10); starters in this paper we aim to answer the following research (1); recent trends in literature suggest that improvement in economic viability (1); recently there has been a surge of interest in the (1)
- paragraph_6: moves method (20); context (10); statement (9); starters to address these objectives we propose temporal collaborative attention tcoat (1); devising an optimal economic dispatch method for wind power plants (1); the lack of interpretability in most ai models undermines user (1)

### Introduction Expression Templates

- Sentence starters: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=68, n=1581); wind <target_variable> forecasting is important for <power_system_operation> (docs=63, n=395); however, <gap_statement> (docs=63, n=256); <renewable_energy_context> creates <operational_need_or_challenge> (docs=58, n=143); <finding_or_method> can <enable_or_support> <operational_decision> (docs=55, n=169); <result_evidence> shows <finding_or_pattern> (docs=49, n=294)
- Verb preferences: improve (274); show (248); provide (205); present (194); develop (161); achieve (118); reduce (117); indicate (95)
- Hedging and degree terms: effectively (134); may (126); could (91); significantly (79); potential (71); indicate (21); approximately (20); slightly (15)
- Frequent bigrams: wind power (1318); wind speed (949); power forecasting (431); time series (249); wind farms (226); neural network (214); wind energy (191); forecasting model (191)
- Frequent trigrams: wind power forecasting (376); wind speed forecasting (145); wind power generation (77); wind speed series (68); wind power data (64); wind speed data (59); wind power prediction (58); wind power output (55)
- Move-level normalized templates:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=63, n=395); <renewable_energy_context> creates <operational_need_or_challenge> (docs=58, n=143)
  - gap: however, <gap_statement> (docs=63, n=256); <existing_work_or_system> is limited by <gap_or_uncertainty> (docs=48, n=115); although <prior_work_or_condition>, <gap_statement> (docs=32, n=56)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=68, n=1581); in this study, <method_or_experiment> is <described_or_evaluated> (docs=23, n=43); this study <method_verb> <method_or_framework> for <forecasting_task> (docs=15, n=16)
  - result: <result_evidence> shows <finding_or_pattern> (docs=49, n=294); <method_or_result> is compared with <baseline> (docs=41, n=126); <method> achieves <metric> of <num> (docs=28, n=49)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=55, n=169); the results <indicate_or_suggest> <operational_implication> (docs=6, n=8)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=35, n=83); <limitation_or_uncertainty> should be considered when <applying_the_method> (docs=26, n=64)
- Move-level starters:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=63, n=395); <renewable_energy_context> creates <operational_need_or_challenge> (docs=58, n=143); in recent years, <field_context> has <trend_or_change> (docs=7, n=8)
  - gap: however, <gap_statement> (docs=63, n=256); <existing_work_or_system> is limited by <gap_or_uncertainty> (docs=48, n=115); although <prior_work_or_condition>, <gap_statement> (docs=32, n=56)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=68, n=1581); in this study, <method_or_experiment> is <described_or_evaluated> (docs=23, n=43); this study <method_verb> <method_or_framework> for <forecasting_task> (docs=15, n=16)
  - result: <result_evidence> shows <finding_or_pattern> (docs=49, n=294); <method_or_result> is compared with <baseline> (docs=41, n=126); <method> achieves <metric> of <num> (docs=28, n=49)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=55, n=169); the results <indicate_or_suggest> <operational_implication> (docs=6, n=8)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=35, n=83); <limitation_or_uncertainty> should be considered when <applying_the_method> (docs=26, n=64)
- Paragraph flow templates: quantitative > quantitative (40); method > method (31); quantitative > statement (26); result > statement (20); method > result (17)

## Methods And Case Study

Methods sections are present in most sampled papers. Case-study sections appear when the paper needs a concrete system, geography, dataset, or operational setup.

| Section | Metric | Median | P25 | P75 |
| --- | --- | --- | --- | --- |
| methods | word_count | 2649.0 | 713.0 | 4021.5 |
| methods | paragraph_count | 7.0 | 3.0 | 17.5 |
| methods | median_sentence_words | 28.0 | 23.0 | 62.75 |
| methods | citation_markers_per_1000_words | 1.94 | 0.0 | 4.87 |
| case_study | word_count | 1913.0 | 788.0 | 2945.0 |
| case_study | paragraph_count | 15.0 | 4.0 | 25.0 |
| case_study | median_sentence_words | 26.5 | 22.0 | 32.0 |
| case_study | citation_markers_per_1000_words | 0.93 | 0.0 | 2.7 |
| nomenclature | word_count | 231.0 | 164.5 | 350.5 |
| nomenclature | paragraph_count | 1.0 | 1.0 | 1.0 |
| nomenclature | median_sentence_words | 219.0 | 151.0 | 265.25 |
| nomenclature | citation_markers_per_1000_words | 0.0 | 0.0 | 0.0 |

### Methods Expression Templates

- Sentence starters: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=41, n=1044); <result_evidence> shows <finding_or_pattern> (docs=33, n=230); however, <gap_statement> (docs=24, n=101); wind <target_variable> forecasting is important for <power_system_operation> (docs=24, n=95); <method_or_result> is compared with <baseline> (docs=22, n=78); <method_performance> is evaluated using <metric> (docs=22, n=40)
- Verb preferences: show (124); present (116); improve (92); achieve (90); indicate (89); provide (79); develop (62); reduce (52)
- Hedging and degree terms: effectively (94); may (70); significantly (70); indicate (37); potential (29); could (21); approximately (16); slightly (15)
- Frequent bigrams: wind speed (484); wind power (467); time series (173); proposed model (123); shown fig (122); wind farm (100); forecasting model (99); forecasting performance (93)
- Frequent trigrams: wind power forecasting (73); wind speed forecasting (69); wind speed data (54); wind power curve (29); wind power data (27); wind speed time (27); wind speed prediction (27); wind speed wind (24)
- Move-level normalized templates:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=24, n=95); <renewable_energy_context> creates <operational_need_or_challenge> (docs=14, n=39)
  - gap: however, <gap_statement> (docs=24, n=101); <existing_work_or_system> is limited by <gap_or_uncertainty> (docs=11, n=27); although <prior_work_or_condition>, <gap_statement> (docs=11, n=22)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=41, n=1044); in this study, <method_or_experiment> is <described_or_evaluated> (docs=18, n=37); we propose <method_or_framework> for <forecasting_task> (docs=5, n=9)
  - result: <result_evidence> shows <finding_or_pattern> (docs=33, n=230); <method_or_result> is compared with <baseline> (docs=22, n=78); <method_performance> is evaluated using <metric> (docs=22, n=40)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=18, n=51)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=17, n=33); <limitation_or_uncertainty> should be considered when <applying_the_method> (docs=14, n=27)
- Move-level starters:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=24, n=95); <renewable_energy_context> creates <operational_need_or_challenge> (docs=14, n=39)
  - gap: however, <gap_statement> (docs=24, n=101); <existing_work_or_system> is limited by <gap_or_uncertainty> (docs=11, n=27); although <prior_work_or_condition>, <gap_statement> (docs=11, n=22)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=41, n=1044); in this study, <method_or_experiment> is <described_or_evaluated> (docs=18, n=37); we propose <method_or_framework> for <forecasting_task> (docs=5, n=9)
  - result: <result_evidence> shows <finding_or_pattern> (docs=33, n=230); <method_or_result> is compared with <baseline> (docs=22, n=78); <method_performance> is evaluated using <metric> (docs=22, n=40)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=18, n=51)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=17, n=33); <limitation_or_uncertainty> should be considered when <applying_the_method> (docs=14, n=27)
- Paragraph flow templates: result > quantitative (12); method > method (11); statement > quantitative (11); quantitative > statement (9); quantitative > quantitative (9)

### Case Study Expression Templates

- Sentence starters: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=25, n=366); <result_evidence> shows <finding_or_pattern> (docs=25, n=156); <method_or_result> is compared with <baseline> (docs=18, n=48); <method_performance> is evaluated using <metric> (docs=16, n=28); <method> outperforms <baseline> in terms of <metric> (docs=15, n=39); wind <target_variable> forecasting is important for <power_system_operation> (docs=14, n=54)
- Verb preferences: show (106); indicate (68); demonstrate (61); achieve (58); present (47); improve (46); outperform (40); provide (37)
- Hedging and degree terms: significantly (56); effectively (51); may (36); indicate (32); potential (14); notably (13); slightly (12); approximately (11)
- Frequent bigrams: wind power (281); wind speed (231); wind farms (134); wind farm (105); proposed method (81); proposed model (75); forecasting accuracy (67); shown fig (66)
- Frequent trigrams: wind power forecasting (60); nwp wind speed (30); wind power data (23); wind speed forecasting (23); wind speed wind (17); wind power output (17); regional wind power (16); actual wind power (14)
- Move-level normalized templates:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=14, n=54); <renewable_energy_context> creates <operational_need_or_challenge> (docs=7, n=12)
  - gap: however, <gap_statement> (docs=13, n=30); although <prior_work_or_condition>, <gap_statement> (docs=7, n=8); <existing_work_or_system> is limited by <gap_or_uncertainty> (docs=6, n=13)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=25, n=366); in this study, <method_or_experiment> is <described_or_evaluated> (docs=6, n=16)
  - result: <result_evidence> shows <finding_or_pattern> (docs=25, n=156); <method_or_result> is compared with <baseline> (docs=18, n=48); <method_performance> is evaluated using <metric> (docs=16, n=28)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=10, n=15)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=10, n=16)
- Move-level starters:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=14, n=54); <renewable_energy_context> creates <operational_need_or_challenge> (docs=7, n=12)
  - gap: however, <gap_statement> (docs=13, n=30); although <prior_work_or_condition>, <gap_statement> (docs=7, n=8); <existing_work_or_system> is limited by <gap_or_uncertainty> (docs=6, n=13)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=25, n=366); in this study, <method_or_experiment> is <described_or_evaluated> (docs=6, n=16)
  - result: <result_evidence> shows <finding_or_pattern> (docs=25, n=156); <method_or_result> is compared with <baseline> (docs=18, n=48); <method_performance> is evaluated using <metric> (docs=16, n=28)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=10, n=15)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=10, n=16)

## Results And Discussion

Result prose should start from a claim, then give metric, unit, comparison, uncertainty or support, and operational interpretation.

| Metric | Median | P25 | P75 |
| --- | --- | --- | --- |
| word_count | 1557.5 | 838.5 | 2346.0 |
| paragraph_count | 13.0 | 8.75 | 20.5 |
| median_sentence_words | 23.0 | 21.0 | 29.38 |
| figure_refs_per_1000_words | 1.54 | 0.0 | 4.67 |
| citation_markers_per_1000_words | 1.57 | 0.55 | 5.32 |
| limitation_terms_per_1000_words | 0.29 | 0.0 | 1.23 |

Recommended moves:

- claim-first result sentence
- quantified comparison with metric and unit
- uncertainty or support statement
- operational interpretation
- boundary or limitation when needed

### Results Expression Templates

- Sentence starters: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=13, n=133); <result_evidence> shows <finding_or_pattern> (docs=11, n=46); <method> achieves <metric> of <num> (docs=10, n=19); <method> improves <metric> compared with <baseline> (docs=9, n=11); <method> outperforms <baseline> in terms of <metric> (docs=8, n=26); <method_or_result> is compared with <baseline> (docs=8, n=18)
- Verb preferences: show (74); achieve (35); improve (29); indicate (28); outperform (26); present (21); demonstrate (17); evaluate (16)
- Hedging and degree terms: slightly (17); significantly (14); could (13); consistently (13); may (11); effectively (9); indicate (8); might (6)
- Frequent bigrams: wind power (95); wind speed (83); time series (38); power data (35); wind farm (30); power forecasting (27); forecasting performance (21); wind farms (21)
- Frequent trigrams: wind power data (34); wind power forecasting (21); wind speed forecasting (13); proposed forecasting system (11); ahead days ahead (9); wind speed data (9); wind speed wind (8); localized spatial module (8)
- Move-level normalized templates:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=7, n=26)
  - gap: however, <gap_statement> (docs=6, n=14)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=13, n=133)
  - result: <result_evidence> shows <finding_or_pattern> (docs=11, n=46); <method> achieves <metric> of <num> (docs=10, n=19); <method> improves <metric> compared with <baseline> (docs=9, n=11)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=5, n=7)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=6, n=8)
- Move-level starters:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=7, n=26)
  - gap: however, <gap_statement> (docs=6, n=14)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=13, n=133)
  - result: <result_evidence> shows <finding_or_pattern> (docs=11, n=46); <method> achieves <metric> of <num> (docs=10, n=19); <method> improves <metric> compared with <baseline> (docs=9, n=11)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=5, n=7)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=6, n=8)
- Paragraph flow templates: result > result > result > statement (6); result > quantitative (5); result > statement (5); quantitative > quantitative > method > statement (3); statement > result > statement (3)

### Discussion Expression Templates

- Sentence starters: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=13, n=119); <result_evidence> shows <finding_or_pattern> (docs=12, n=29); wind <target_variable> forecasting is important for <power_system_operation> (docs=7, n=21); <method_or_result> is compared with <baseline> (docs=7, n=13); <finding_or_method> can <enable_or_support> <operational_decision> (docs=7, n=12); <method_performance> is evaluated using <metric> (docs=7, n=8)
- Verb preferences: show (28); indicate (21); improve (20); demonstrate (17); provide (14); reduce (14); present (13); achieve (13)
- Hedging and degree terms: may (15); significantly (15); effectively (10); indicate (10); could (9); potential (7); slightly (4); might (3)
- Frequent bigrams: wind speed (66); wind power (54); proposed model (37); forecasting performance (30); adversarial training (25); forecasting results (24); forecasting accuracy (24); time series (24)
- Frequent trigrams: wind speed forecasting (21); wind power forecasting (14); nonlinear ensemble method (8); wind speed data (8); wind energy forecasting (8); mae rmse mape (7); data processing methods (7); ensemble method based (6)
- Move-level normalized templates:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=7, n=21)
  - gap: however, <gap_statement> (docs=6, n=19)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=13, n=119); in this study, <method_or_experiment> is <described_or_evaluated> (docs=5, n=10)
  - result: <result_evidence> shows <finding_or_pattern> (docs=12, n=29); <method_or_result> is compared with <baseline> (docs=7, n=13); <method_performance> is evaluated using <metric> (docs=7, n=8)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=7, n=12)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=5, n=5)
- Move-level starters:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=7, n=21)
  - gap: however, <gap_statement> (docs=6, n=19)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=13, n=119); in this study, <method_or_experiment> is <described_or_evaluated> (docs=5, n=10)
  - result: <result_evidence> shows <finding_or_pattern> (docs=12, n=29); <method_or_result> is compared with <baseline> (docs=7, n=13); <method_performance> is evaluated using <metric> (docs=7, n=8)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=7, n=12)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=5, n=5)
- Paragraph flow templates: result > result > result > result (3); method > result (3); result > result (3); statement > method (2); method > method (2)

### Results And Discussion Combined Templates

- Sentence starters: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=6, n=110); <result_evidence> shows <finding_or_pattern> (docs=6, n=47); <method_performance> is evaluated using <metric> (docs=5, n=13)
- Verb preferences: show (53); present (22); indicate (20); improve (13); outperform (12); evaluate (11); demonstrate (8); provide (8)
- Hedging and degree terms: slightly (14); might (12); could (11); significantly (11); may (10); consistently (8); potential (8); likely (8)
- Frequent bigrams: wind farms (126); wind farm (101); lasso model (48); reference wind (45); target wind (36); time step (27); power generation (24); wind power (23)
- Frequent trigrams: reference wind farms (37); target wind farm (36); candidate wind farms (18); prediction error rate (13); number candidate wind (11); pinball loss function (10); selected lasso model (9); wind farms within (7)
- Move-level normalized templates:
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=6, n=110)
  - result: <result_evidence> shows <finding_or_pattern> (docs=6, n=47); <method_performance> is evaluated using <metric> (docs=5, n=13)
- Move-level starters:
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=6, n=110)
  - result: <result_evidence> shows <finding_or_pattern> (docs=6, n=47); <method_performance> is evaluated using <metric> (docs=5, n=13)
- Paragraph flow templates: result > method (4); method > method > result (3); quantitative > statement > statement (2); result > method > context (2); method > method (2)

### Numeric Reporting Templates

- Format types: numeric_context (625); display_reference_with_number (270); metric_value (165); percent_change_or_comparison (122); from_to_change (28); energy_unit_value (12)
- Short normalized templates: <quantity_or_metric> changes from <num> to <num> (docs=8, n=12); <interval_type> is reported for <forecast_or_metric> (docs=7, n=12)
- Unit co-occurrence: % (485); h (67); MW (23); s (12); min (12); MWh (4); kW (3); H (1); kWh (1)
- Uncertainty expressions: standard_deviation (10); prediction_interval (9); p_value (5); error_bar (1)
- Numeric pattern by section:
  - abstract: numeric_context (45); percent_change_or_comparison (25); metric_value (4)
  - results: numeric_context (279); display_reference_with_number (115); metric_value (66); percent_change_or_comparison (54)
  - discussion: numeric_context (158); display_reference_with_number (63); metric_value (45); percent_change_or_comparison (24)
  - results_discussion: numeric_context (143); display_reference_with_number (92); metric_value (50); percent_change_or_comparison (19)
- Unit context templates:
  - %: <percentage_value> is reported for <metric_or_case> (docs=46, n=424); <quantity_or_metric> changes by <percent> (docs=11, n=50)
  - H: Unchecked
  - MW: <power_value> is reported in <power_unit> (docs=6, n=23)
  - MWh: Unchecked
  - h: <time_context> is reported as <num> h (docs=10, n=42); <forecast_horizon> is reported as <num> h (docs=5, n=20)
  - kW: Unchecked
  - kWh: Unchecked

### Comparison Language Templates

- Comparison templates: <method_or_result> is compared with <baseline> (docs=32, n=58); <method> outperforms <baseline> in terms of <metric> (docs=31, n=62); <method> achieves <metric> of <num> (docs=26, n=43); <method> improves <metric> compared with <baseline> (docs=24, n=37); <method> reduces <metric> compared with <baseline> (docs=10, n=11); <method> reduces <metric> by <percent> compared with <baseline> (docs=9, n=11)
- Comparison verbs: compare (122); outperform (66); achieve (45); improve (42); reduce (14); increase (14); decrease (6)

## Conclusion

Conclusions are common and should restate the evidence-bound contribution, operational implication, and boundary conditions.

| Section | Metric | Median | P25 | P75 |
| --- | --- | --- | --- | --- |
| conclusion | word_count | 351.0 | 244.5 | 442.0 |
| conclusion | paragraph_count | 3.0 | 2.0 | 4.0 |
| conclusion | median_sentence_words | 25.0 | 21.0 | 27.0 |
| conclusion | limitation_terms_per_1000_words | 0.0 | 0.0 | 4.56 |

### Conclusion Expression Templates

- Sentence starters: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=62, n=222); wind <target_variable> forecasting is important for <power_system_operation> (docs=30, n=48); <result_evidence> shows <finding_or_pattern> (docs=22, n=22); in this study, <method_or_experiment> is <described_or_evaluated> (docs=20, n=24); <method> outperforms <baseline> in terms of <metric> (docs=19, n=20); <method_or_result> is compared with <baseline> (docs=18, n=19)
- Verb preferences: improve (51); show (41); provide (35); address (33); achieve (30); demonstrate (27); propose (26); present (25)
- Hedging and degree terms: effectively (36); significantly (21); potential (19); may (18); could (16); consistently (11); notably (4); might (3)
- Frequent bigrams: wind power (192); wind speed (142); power forecasting (87); wind farms (44); forecasting accuracy (38); wind farm (36); proposed method (31); proposed model (29)
- Frequent trigrams: wind power forecasting (73); wind speed forecasting (26); wind power generation (18); wind speed data (16); wind speed prediction (13); nwp wind speed (11); wind speed series (8); future work will (7)
- Move-level normalized templates:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=30, n=48); <renewable_energy_context> creates <operational_need_or_challenge> (docs=9, n=11)
  - gap: however, <gap_statement> (docs=13, n=14); <existing_work_or_system> is limited by <gap_or_uncertainty> (docs=8, n=9); although <prior_work_or_condition>, <gap_statement> (docs=7, n=7)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=62, n=222); in this study, <method_or_experiment> is <described_or_evaluated> (docs=20, n=24); this study <method_verb> <method_or_framework> for <forecasting_task> (docs=14, n=15)
  - result: <result_evidence> shows <finding_or_pattern> (docs=22, n=22); <method> outperforms <baseline> in terms of <metric> (docs=19, n=20); <method_or_result> is compared with <baseline> (docs=18, n=19)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=12, n=16)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=16, n=19)
- Move-level starters:
  - context: wind <target_variable> forecasting is important for <power_system_operation> (docs=30, n=48); <renewable_energy_context> creates <operational_need_or_challenge> (docs=9, n=11)
  - gap: however, <gap_statement> (docs=13, n=14); <existing_work_or_system> is limited by <gap_or_uncertainty> (docs=8, n=9); although <prior_work_or_condition>, <gap_statement> (docs=7, n=7)
  - method: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=62, n=222); in this study, <method_or_experiment> is <described_or_evaluated> (docs=20, n=24); this study <method_verb> <method_or_framework> for <forecasting_task> (docs=14, n=15)
  - result: <result_evidence> shows <finding_or_pattern> (docs=22, n=22); <method> outperforms <baseline> in terms of <metric> (docs=19, n=20); <method_or_result> is compared with <baseline> (docs=18, n=19)
  - implication: <finding_or_method> can <enable_or_support> <operational_decision> (docs=12, n=16)
  - limitation: future work should <extend_or_validate> <method_or_application> (docs=16, n=19)
- Paragraph flow templates: result > result (8); method > method > method > method (5); context > context (4); context > result (4); context > method > method > method (3)

### Conclusion Closing Patterns

- Opening starters: wind <target_variable> forecasting is important for <power_system_operation> (docs=11, n=11); this study <method_verb> <method_or_framework> for <forecasting_task> (docs=11, n=11); in this study, <method_or_experiment> is <described_or_evaluated> (docs=9, n=9); <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=8, n=8)
- Closing starters: <method_or_framework> is used to <forecast_or_evaluate> <target_variable> (docs=20, n=20); future work should <extend_or_validate> <method_or_application> (docs=7, n=7); wind <target_variable> forecasting is important for <power_system_operation> (docs=5, n=5)
- Closing moves: method (23); context (10); statement (10); result (10); limitation (7); implication (7)

## Figures And Tables

Figures and tables are expected to support the evidence chain. Captions should name the metric, unit, sample, and main interpretation.

| Metric | Median | P25 | P75 |
| --- | --- | --- | --- |
| figures_per_article | 10.0 | 8.0 | 13.0 |
| tables_per_article | 0.0 | 0.0 | 1.0 |
| figure_caption_words | 57.0 | 49.0 | 68.25 |
| table_caption_words | 160.0 | 68.25 | 238.25 |

### Figure And Caption Expression

- Figure caption opening types: descriptive_caption (660); performance_or_prediction_caption (52); time_or_space_caption (31); comparison_caption (26); framework_caption (23); distribution_or_uncertainty_caption (10); effect_or_impact_caption (3)
- Figure caption starters: <method_framework_or_architecture> (docs=46, n=89); wind <target_variable> forecasting <result_or_setup> (docs=36, n=104); <data_or_case_study> description (docs=34, n=50); <forecast_or_performance> of <method_or_target> (docs=23, n=45); <distribution_or_uncertainty> of <target_variable> (docs=19, n=35); <proposed_method> <figure_content> (docs=15, n=27); comparison of <methods_or_results> (docs=13, n=22); <performance_metric_or_error> under <case_or_method> (docs=12, n=18)
- Figure caption syntax: single_sentence:descriptive_caption (247); descriptive_caption > interpretation (201); descriptive_caption > quantified_detail (108); single_sentence:performance_or_prediction_caption (32); descriptive_caption > interpretation > quantified_detail (20); descriptive_caption > interpretation > interpretation (16); descriptive_caption > quantified_detail > interpretation (14); descriptive_caption > quantified_detail > quantified_detail (12)
- Table caption opening types: descriptive_caption (36); time_or_space_caption (2)
- Table caption starters: <performance_metric_or_error> under <case_or_method> (docs=5, n=5)
- Table header shapes: descriptive_columns (364); scenario_or_model_columns (152); unit_columns (59); scenario_metric_matrix (30); metric_with_unit (12)
- Table header terms: model (101); wind (91); forecasting (78); results (64); different (54); time (53); models (51); proposed (46); power (42); comparison (36); speed (36); method (35)
- Figure reference templates: <fig> referenced inside explanatory sentence (docs=68, n=430); shown in <fig> (docs=55, n=159); as shown in <fig> (docs=47, n=174); illustrated in <fig> (docs=25, n=36); <fig> shows <result_or_setup> (docs=24, n=35); as illustrated in <fig> (docs=17, n=32); presented in <fig> (docs=15, n=20); depicted in <fig> (docs=15, n=19)
- Figure topic to caption starter:
  - comparison_caption: comparison of <methods_or_results> (docs=13, n=22)
  - descriptive_caption: <method_framework_or_architecture> (docs=41, n=70); <data_or_case_study> description (docs=34, n=50); wind <target_variable> forecasting <result_or_setup> (docs=32, n=86)
  - distribution_or_uncertainty_caption: <distribution_or_uncertainty> of <target_variable> (docs=6, n=10)
  - effect_or_impact_caption: Unchecked
  - framework_caption: <method_framework_or_architecture> (docs=15, n=18)
  - performance_or_prediction_caption: <forecast_or_performance> of <method_or_target> (docs=23, n=45)
  - time_or_space_caption: <temporal_or_spatial_pattern> of <target_variable> (docs=9, n=15); wind <target_variable> forecasting <result_or_setup> (docs=7, n=9)

## Downstream Use

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
