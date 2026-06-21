# ScienceDirect Ingest Notes

Use this reference when building a target-journal corpus from Elsevier
ScienceDirect.

## Credential Handling

- Read API keys only from environment variables.
- Prefer `SCIENCEDIRECT_API_KEY`.
- Accept `ELSEVIER_API_KEY` or `X_ELS_APIKEY` as fallbacks.
- If the Codex process cannot see a newly added Windows environment variable,
  place the key in a private local text file outside the run folder and pass
  `--api-key-file PATH`.
- Do not write keys to logs, manifests, profiles, notebooks, or Markdown
  reports.

## Query Strategy

Use a query that combines journal, topic, years, and article type. The fetch
script prefers ScienceDirect's PUT search interface with `qs`, `pub`, and
`display`. It keeps a GET fallback for older API configurations. It applies
year, journal, correction-type, and title-regex filtering locally after
retrieval because some ScienceDirect configurations reject date comparison
operators.

ScienceDirect search fields documented by Elsevier include:

- `Srctitle` or `src` for journal title.
- `Title-Abstr-Key` or `tak` for topic terms.
- `Pub-Date` or `pdt` for publication date filtering.
- `DOI` for exact DOI lookup.

Keep the topic broad enough to retrieve candidates, then apply a strict profile
builder topic gate before learning style. For wind-power forecasting, include
terms such as `wind power`, `wind energy`, `wind farm`, `forecasting`,
`prediction interval`, `probabilistic forecasting`, `scenario generation`,
`conformal prediction`, or `grid operation`.

Do not treat horizon terms such as `day-ahead`, `ahead`, `short-term`, or
`ultra-short-term` as sufficient evidence by themselves. They are useful only
when paired with true forecasting terms such as `forecast`, `prediction`, or
`scenario generation`.

When ScienceDirect PDF access is missing, create a DOI target list first:

```bash
python scripts/discover_crossref_candidates.py \
  --journal "Applied Energy" \
  --query "wind power forecasting Applied Energy" \
  --query "probabilistic wind power forecasting Applied Energy" \
  --query "wind speed forecasting Applied Energy" \
  --year-from 2018 \
  --year-to 2026 \
  --topic-profile wind_forecasting \
  --rows 80 \
  --max-pages 8 \
  --output runs/applied-energy-wind-forecasting-candidates.json
```

Use the candidate JSON to retrieve complete PDFs through ScienceDirect,
institutional access, Zotero, or author-supplied folders. Candidate metadata is
not sufficient for a style profile.

After a candidate JSON exists, prefer DOI-exact PDF retrieval over another
broad ScienceDirect topic search:

```bash
python scripts/fetch_sciencedirect_corpus.py \
  --journal "Applied Energy" \
  --candidate-json runs/applied-energy-wind-forecasting-candidates.json \
  --max-results 80 \
  --download-pdf \
  --output runs/applied-energy-wind-forecasting-corpus
```

This route keeps the retrieval queue tied to the screened wind-forecasting DOI
list and avoids broad Applied Energy query drift.

Recommended Applied Energy wind-forecasting build command after candidate
downloads:

```bash
python scripts/build_style_profile.py \
  --pdf-dir runs/applied-energy-corpus/pdfs \
  --journal "Applied Energy" \
  --topic-profile wind_forecasting \
  --require-topic-match \
  --min-template-doc-support 5 \
  --output runs/applied-energy-wind-forecasting-profile
```

Do not build a normal Applied Energy wind-forecasting profile from a broad
Applied Energy query without `--require-topic-match`. Broad queries can pull in
UBEM, building energy, hot-water systems, pure PV forecasting, hydrogen storage,
and generic microgrid scheduling papers.

## Access Outcomes

ScienceDirect article retrieval can return different access levels:

- PDF downloaded successfully.
- PDF endpoint returns a one-page preview while XML or plain full text is
  available.
- JSON or XML full text available while PDF is unavailable.
- Metadata only.
- Authorization failure due to API configuration, IP, institutional
  entitlement, article coverage, or unsupported response format.

Record these outcomes in `corpus_manifest.json`. A partial corpus can still be
useful when enough local PDFs are available.

When many PDFs are one-page previews, retrieve section-aware XML full text:

```bash
python scripts/fetch_sciencedirect_corpus.py \
  --journal "Applied Energy" \
  --candidate-json runs/applied-energy-wind-forecasting-candidates.json \
  --max-results 80 \
  --download-full-text \
  --full-text-format xml-text \
  --output runs/applied-energy-wind-forecasting-fulltext
```

Then build the profile with `--text-dir runs/applied-energy-wind-forecasting-fulltext/fulltext`.

## Corpus Quality

Use these minimums after incomplete PDFs are excluded:

- 30 or more complete articles: normal profile.
- 10 to 29 complete articles: usable profile with caution.
- 1 to 9 complete articles: pilot profile only.

Prefer recent research articles from the target journal. Avoid editorials,
corrigenda, conference announcements, and review articles unless the manuscript
is a review.

Before building the profile, filter incomplete PDFs. A normal profile should use
PDFs with at least 4 pages, at least 1500 extracted words, and detected
`abstract` plus `introduction` sections unless the target article type justifies
different thresholds.

## Copyright Guardrail

Store only file paths, metadata, aggregate metrics, short section labels, and
synthetic templates. Do not store copied paragraphs from source papers in style
profiles.
