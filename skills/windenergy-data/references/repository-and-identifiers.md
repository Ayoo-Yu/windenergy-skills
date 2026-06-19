# Repository and Identifiers

Use this file when choosing repositories or checking dataset/software citations.

## Decision Tree

1. Use the data provider's official archive when the dataset is reused.
2. Use a domain repository for public energy or meteorological data.
3. Use a DOI-bearing general repository for author-generated data or code.
4. Use a controlled-access or metadata-only record when data are proprietary or
   sensitive.
5. Do not use personal cloud folders as the only availability route.

## Energy Repository Patterns

| Data or artifact | Good routes |
|---|---|
| Author-generated processed data | Zenodo, Figshare, Dryad, Mendeley Data |
| Code release | GitHub plus Zenodo archive DOI |
| ERA5/reanalysis | Copernicus Climate Data Store citation and access URL |
| NREL wind data | NREL Data Catalog or WIND Toolkit citation |
| Grid data | ENTSO-E, EIA, official grid/operator portal |
| Large simulation outputs | Institutional repository, Zenodo communities, data portal |
| Restricted SCADA | Metadata-only statement plus access conditions |

## Repository Record Checklist

- Persistent identifier or stable landing page.
- Title, creators, version, date, license, and related manuscript.
- File manifest, README, units, variable definitions, and time zone.
- Provenance: raw source, cleaning, aggregation, and exclusions.
- Clear access terms for restricted data.
- Code/data version that matches the manuscript revision.

## Dataset Citation Pattern

```text
[dataset] Author(s), Dataset title, Repository, version, Year.
https://doi.org/[DOI]
```

## Software Citation Pattern

```text
Author(s), Software Name (Version X.Y) [software], Repository, Date.
https://doi.org/[DOI]
```
