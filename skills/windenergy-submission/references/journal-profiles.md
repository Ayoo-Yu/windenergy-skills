# 18 Journal Submission Profiles

These profiles support wind power, renewable energy, smart grid, and AI-for-energy manuscript preparation. Use them with `windenergy-submission`, `windenergy-writing`, and `windenergy-polishing`.

## Source Policy

- Source archive: `期刊整理/output/*.md` and the downloaded ScienceDirect guide PDFs in `期刊整理/`.
- Official verification date: 2026-05-31.
- Current official English guides override this file when they conflict.
- Verified web examples include ScienceDirect guide pages for Renewable Energy, Applied Energy, Applied Soft Computing, Pattern Recognition, and International Journal of Electrical Power and Energy Systems.
- Treat all limits as submission-stage checks. If a journal system shows a newer rule, follow the system.

## How To Use

1. Detect a journal slug from the user request. If none is named, use `common-18`.
2. Load the matching profile and apply hard limits first.
3. Mark profile-dependent requirements as `PASS`, `FAIL`, `UNCHECKED`, or `AUTHOR_INPUT_NEEDED`.
4. Never auto-fill author details, grants, conflicts, CRediT roles, data access rights, or AI usage.
5. For a named target journal, count cited references from that journal. Mark
   fewer than 10 as `FAIL`, missing reference data as `UNCHECKED`, and missing
   relevant additions as `AUTHOR_INPUT_NEEDED`.

## Common 18 Journal Baseline

Slug: `common-18`

- Abstract: prepare a 200-word compact version and a 250-word standard version. Energy and AI may allow 100 to 300 words.
- Keywords: prepare 6 keywords by default. Add a seventh only when the target journal allows 1 to 7.
- Highlights: prepare 3 to 5 bullets, each 85 characters or fewer including spaces.
- Citation style: default to numbered references in square brackets for portability. Switch style for Energy Reports, Energy and AI, Engineering Applications of Artificial Intelligence, Expert Systems with Applications, and target-specific requests.
- Target-journal citation coverage: when a specific journal is selected, the
  manuscript should cite at least 10 papers published in that journal.
- Declarations: check CRediT, data availability, competing interests, funding, and generative AI use for every submission.
- Figures: use editable tables, high-resolution artwork, color-accessible palettes, and separate figure files when required.
- Scope: connect wind and AI work to energy generation, conversion, forecasting, operation, control, grids, or decision support.

## Journal Slugs

### `renewable-energy`

- Journal: Renewable Energy. ISSN 0960-1481. Elsevier. Single anonymized review.
- Article types and length: research paper 4000 to 6000 words excluding captions and references; review up to 10000 words and normally invited.
- Abstract: max 250 words.
- Keywords: 1 to 6.
- References: max 50.
- Highlights: required, 3 to 5 bullets, 85 characters max each.
- Cover letter: required, max 1 page.
- Required checks: CRediT, data availability, competing interests, funding, AI use assessment, word count statement.
- Scope risk: manuscript must concern renewable energy research, measurement, development, application, or generation-related systems. Pure storage or grid management with no renewable link may be weak.

### `applied-energy`

- Journal: Applied Energy. ISSN 0306-2619. Elsevier. Single anonymized review.
- Article types and length: full article, review article, short communication. No fixed word limit in the local guide.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: required.
- Graphical abstract: encouraged.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: work should emphasize applied energy systems, transition, optimization, forecasting, decision-making, or energy-system implementation value.

### `applied-soft-computing`

- Journal: Applied Soft Computing. ISSN 1568-4946. Elsevier. Single anonymized review.
- Length: local guide lists 20 to 30 pages, with an upper bound of 50 pages.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: encouraged.
- Graphical abstract: required.
- Author biography: required, about 100 words plus photo.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: method should fit soft computing and real-life application, not only generic deep learning.

### `computers-electrical-engineering`

- Journal: Computers and Electrical Engineering. ISSN 0045-7906. Elsevier. Single anonymized review.
- Article types and length: full article and technical communication. Technical communication up to 6 pages.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: required.
- Graphical abstract: encouraged.
- Author biography: required, about 100 words plus photo.
- Required checks: data statement, declaration of interest, funding, AI use assessment. CRediT is encouraged in the local matrix.
- Scope risk: connect algorithms to electrical engineering, power systems, or energy computing.

### `electric-power-systems-research`

- Journal: Electric Power Systems Research. ISSN 0378-7796. Elsevier. Single anonymized review.
- Article types and length: full article up to 7000 words; review up to 9000 words; short communication up to 1000 words.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: required.
- Graphical abstract: encouraged.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: emphasize power-system operation, planning, reliability, forecasting, control, or integration.

### `energy`

- Journal: Energy. ISSN 0360-5442. Elsevier. Single anonymized review.
- Article types and length: full article 5000 to 7000 words; review 7000 to 9000 words.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: required.
- Graphical abstract: not required in the local matrix.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: keep claims connected to energy conversion, resources, systems, efficiency, or policy-relevant technical evidence.

### `energy-conversion-management`

- Journal: Energy Conversion and Management. ISSN 0196-8904. Elsevier. Single anonymized review.
- Article types and length: full article up to 9000 words; review up to 12000 words.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: required.
- Graphical abstract: encouraged.
- Cover letter: required, max 1 page.
- Figure and table limit: 15 total for full articles.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: emphasize conversion, management, storage, transmission, conservation, or system performance.

### `energy-reports`

- Journal: Energy Reports. ISSN 2352-4847. Elsevier. Single anonymized review. Open access.
- Article types and length: full article 5000 to 7000 words; review 7000 to 9000 words; replication 2000 to 4000 words; short communication 1500 to 3000 words.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: author-year.
- Highlights: required.
- Graphical abstract: encouraged.
- SI units: required.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment, APC awareness.
- Scope risk: make novelty and reproducibility clear for open access broad energy readership.

### `energy-and-ai`

- Journal: Energy and AI. ISSN 2666-5468. Elsevier. Single anonymized review. Open access.
- Length: no clear fixed limit in the local guide.
- Abstract: 100 to 300 words.
- Keywords: up to 6.
- Citation style: superscript numbered references.
- Highlights: required.
- Graphical abstract: encouraged.
- Required checks: CRediT, AI use assessment, declaration of interest, funding. Data statement is encouraged in the local matrix.
- Template: LaTeX recommended.
- Scope risk: explicitly connect AI method to energy-domain value and constraints.

### `engineering-applications-ai`

- Journal: Engineering Applications of Artificial Intelligence. ISSN 0952-1976. Elsevier. Double anonymized review.
- Length: up to 50 pages.
- Abstract: max 250 words.
- Keywords: 1 to 6.
- Citation style: author-year.
- Highlights: encouraged.
- SI units: required.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Anonymization: remove author identities, acknowledgements, funding identifiers, and self-identifying file metadata before review when required.
- Scope risk: distinguish AI contribution from the engineering application and avoid undefined abbreviations in title or abstract.

### `expert-systems-applications`

- Journal: Expert Systems with Applications. ISSN 0957-4174. Elsevier. Double anonymized review.
- Length: no clear fixed limit in the local guide.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: APA 7th.
- Highlights: encouraged.
- Required checks: data statement, declaration of interest, funding, AI use assessment. CRediT is encouraged in the local matrix.
- Anonymization: remove author identities and self-identifying metadata before review.
- Scope risk: local guide flags military and defense topics as out of scope.

### `information-sciences`

- Journal: Information Sciences. ISSN 0020-0255. Elsevier. Single anonymized review.
- Length: experimental papers up to 40 pages; theoretical papers up to 45 pages.
- Abstract: max 200 words.
- Keywords: 1 to 7.
- Citation style: flexible in the local matrix.
- Highlights: encouraged.
- Figure limit: experimental papers up to 8 figures; theoretical papers up to 10 figures.
- Author biography: required, about 100 words plus photo.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: justify information science contribution, not only application performance.

### `ijepes`

- Journal: International Journal of Electrical Power and Energy Systems. ISSN 0142-0615. Elsevier. Single anonymized review.
- Article types and length: full article up to 20 pages; short communication up to 10 pages.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: required.
- Graphical abstract: encouraged.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: emphasize electrical power and energy systems relevance.

### `knowledge-based-systems`

- Journal: Knowledge-Based Systems. ISSN 0950-7051. Elsevier. Single anonymized review.
- Article types and length: full article up to 20 pages; short communication up to 10 pages.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: encouraged.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: show knowledge-based, intelligent-systems, or decision-support contribution beyond routine forecasting.

### `neurocomputing`

- Journal: Neurocomputing. ISSN 0925-2312. Elsevier. Single anonymized review.
- Article types and length: full article up to 20 pages; short communication up to 10 pages.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: encouraged.
- Author biography: required, about 100 words plus photo.
- SI units: required.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: connect neural or computational method novelty to rigorous experiments.

### `pattern-recognition`

- Journal: Pattern Recognition. ISSN 0031-3203. Elsevier. Single anonymized review in the local matrix.
- Length: original articles 20 to 35 pages; reviews up to 40 pages.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- References: requested range 35 to 55.
- Highlights: required.
- Graphical abstract: encouraged.
- Cover letter: required and must answer journal-specific editor questions.
- SI units: required.
- Formatting: local guide flags Times New Roman 10 pt.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: ground the paper in pattern-recognition literature. Routine applications of known methods should be redirected.

### `seta`

- Journal: Sustainable Energy Technologies and Assessments. ISSN 2213-1388. Elsevier. Single anonymized review.
- Length: no clear fixed limit in the local guide.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: required.
- Graphical abstract: encouraged.
- SI units: required.
- Checklist: required.
- Corresponding author: institutional email required in local guide.
- Required checks: CRediT, data statement, declaration of interest, funding, AI use assessment.
- Scope risk: emphasize technology assessment, sustainable energy application, and evaluation evidence.

### `segan`

- Journal: Sustainable Energy, Grids and Networks. ISSN 2352-4677. Elsevier. Single anonymized review.
- Length: no clear fixed limit in the local guide.
- Abstract: max 250 words.
- Keywords: 1 to 7.
- Citation style: numbered references in square brackets.
- Highlights: encouraged.
- Graphical abstract: encouraged.
- Required checks: CRediT, declaration of interest, funding, AI use assessment. Data statement is encouraged in the local matrix.
- Scope risk: emphasize sustainable grids, power networks, smart grids, integrated energy systems, or grid-facing AI.

## Safety Rules For Auto-Fix

- Safe auto-fixes: text-level wording, heading labels, declaration wording after user-provided facts, keyword trimming when the exact replacement is clear, and minor style normalization.
- Manual items: missing author details, missing grants, missing affiliations, missing conflicts, missing AI usage facts, missing data rights, missing cover letter facts, missing graphical abstract, figure resolution, reference pruning, citation renumbering, target-journal citation additions, anonymization decisions, and any journal-rule conflict.
- Use `AUTHOR_INPUT_NEEDED` for manual items. Do not silently generate facts.
