---
name: windenergy-data
description: >-
  Prepare, audit, or revise Data Availability statements, data repository plans,
  dataset citations, software/code availability notes, and FAIR metadata checks
  for the 18 target Elsevier energy, power, AI, and pattern-recognition
  journals used by wind-power, renewable-energy integration, and AI-for-energy
  submissions. Use when the user asks about SCADA data sharing, NWP/reanalysis
  datasets, repository choice, restricted operator data, dataset DOI citation,
  code release, or data availability wording.
---

# Renewable Multi-Journal Data Availability

Use this skill when manuscript claims depend on datasets, code, simulation
outputs, SCADA records, NWP inputs, reanalysis products, or third-party energy
data.

## Router Protocol

Read `manifest.yaml`, load all `always_load` files, and then load on-demand
references only for policy, repository, FAIR, statement, source-basis, or
Chinese-author wording needs.

Before writing generated files, load `../_shared/core/output-run-folders.md`
and create a run folder for this invocation. Put data availability drafts,
FAIR checklists, repository plans, and audit reports in that run folder.

## Data Types

| Data type | Typical source | Sharing stance |
|---|---|---|
| Wind farm SCADA | Operator or field campaign | Often restricted; disclose reason |
| NWP forecasts | ECMWF, GFS, ERA5-derived products | Public or licensed |
| Reanalysis | ERA5, MERRA-2, NOAA products | Public with citation |
| Wind resource | NREL WIND Toolkit, Global Wind Atlas | Public with terms |
| Power system | ENTSO-E, EIA, grid operators | Varies by region |
| Simulation outputs | Author generated | Deposit when practical |
| Code | Author repository | Archive release with DOI if possible |

## Workflow

1. Identify every dataset and code artifact supporting the manuscript.
2. Mark each item as public, restricted, third-party, generated, or unavailable.
3. Choose a repository or access route; prefer a DOI-bearing repository for
   author-generated data and code.
4. Draft a Data Availability statement that matches actual rights and access.
5. Add dataset/software citations when the target journal or repository supports
   them.
6. Flag missing DOIs, unclear licenses, vague "available on request" wording, or
   promises that conflict with operator NDAs.

## Common Repositories

Zenodo, Figshare, Dryad, Mendeley Data, IEEE DataPort, OSF, institutional
repositories, NREL Data Catalog, Copernicus Climate Data Store, NOAA/NCEI,
ECMWF data portals, ENTSO-E Transparency Platform, EIA Open Data.

## Red Lines

- Do not fabricate DOIs, repository URLs, licenses, or access permissions.
- Do not promise public access to proprietary SCADA or grid-operator data.
- Do not omit reused public datasets that materially support figures or tables.
- Do not claim code is available unless the repository or archive exists.

## References

- `references/repository-and-identifiers.md`
- `references/statement-patterns.md`
- `references/fair-metadata-checklist.md`
- `references/policy-principles.md`
- `references/chinese-author-alignment.md`
