# RIS and BibTeX Export Notes

Use these minimum fields when exporting verified references.

## RIS

```text
TY  - JOUR
TI  - [Title]
AU  - [Author]
PY  - [Year]
JO  - [Journal]
DO  - [DOI]
UR  - [URL]
ER  -
```

Use `TY  - ELEC` or `TY  - RPRT` for datasets, software records, and technical
reports when journal fields are not appropriate.

## BibTeX

```bibtex
@article{key,
  title = {[Title]},
  author = {[Authors]},
  journal = {[Journal]},
  year = {[Year]},
  doi = {[DOI]},
  url = {[URL]}
}
```

For arXiv preprints, use `@misc` with `archivePrefix = {arXiv}` and `eprint`.
