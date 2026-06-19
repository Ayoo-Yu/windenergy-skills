# Renewable Energy Search Strategy

Use this reference when building queries for renewable generation, energy
systems, energy markets, planning, control, forecasting, or AI-for-energy
literature searches.

## Query Construction

Build each search from four optional blocks:

```text
[energy asset] + [task] + [method] + [evidence qualifier]
```

Profile-based examples:

- `[asset] [task] [method family] [evaluation need]`
- `[energy system] [operational constraint] [decision value]`
- `[data source type] [application domain] [benchmark or validation]`
- `[physical mechanism] [model family] [energy asset]`
- `[market or planning problem] [optimization method] [risk metric]`

## Routing

| Need | Primary source | Secondary source |
|---|---|---|
| DOI verification | CrossRef | OpenAlex |
| Broad review search | OpenAlex | CrossRef |
| AI/ML method discovery | Semantic Scholar | arXiv |
| Recent preprints | arXiv | Semantic Scholar |
| Citation count screening | OpenAlex | Semantic Scholar |
| Journal formatting | CrossRef | Manual check |

## Screening Rules

- Prefer papers whose title or abstract directly matches the energy system, not
  only the AI method.
- Use the active journal profile to prioritize application domain, method
  family, and evaluation criteria.
- Treat venue, year, DOI, abstract, and citation count as screening signals, not
  proof that the paper supports a specific claim.
- Use manual verification for paywalled publisher pages or institution-only
  indexes.

## Reference Budget

Some target journals limit references. When a search returns many candidates:

1. Keep foundational or directly comparable energy-domain studies.
2. Keep recent method papers only when the method is actually used or contrasted.
3. Remove generic AI citations that do not affect the manuscript argument.
4. Prefer one strong review over several weak background citations.

## Related Work Literature Map

When search results will support a Related Work section, organize candidates as
a literature map:

| Field | Purpose |
|---|---|
| topic bucket | research line or evidence role |
| search queries used | exact English queries and source routing |
| representative papers | direct papers that define the bucket |
| seminal papers | older or foundational sources |
| recent direct competitors | closest current alternatives |
| shared assumption or method | common paradigm to synthesize |
| known limitation | unresolved point left by the bucket |
| connection to manuscript gap | why the bucket matters |
| coverage status | sufficient, thin, or unchecked |

Do not convert the map into manuscript prose by listing one paper per sentence.
Pass the map to `windenergy-writing` for synthesis.
