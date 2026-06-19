# Deduplication Rules

Deduplicate search results in this order:

1. DOI, case-insensitive and without `https://doi.org/`.
2. arXiv ID, without version suffix unless the version matters.
3. Normalized title: lowercase, whitespace collapsed, punctuation removed.
4. Title plus first author plus year when DOI is missing.

When two records conflict:

- Prefer DOI metadata from CrossRef for final citation details.
- Prefer OpenAlex or Semantic Scholar citation counts only as approximate
  screening signals.
- Preserve arXiv metadata for preprints even if a later DOI exists; tell the user
  when both versions appear.
