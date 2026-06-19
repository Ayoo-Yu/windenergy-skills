# Default stance

- Language serves argument. Do not polish sentences while leaving the reasoning broken.
- Write with empathy for the reader: relevance first, then novelty, then trust, then reuse, then meaning.
- There should be no mystery for the writer, but there may be one for the reader.
- Do not invent data, references, mechanisms, or novelty claims.
- Do not let AI draft the paper's core scientific argument from scratch.
- If the draft is Chinese or structurally rough, reconstruct the logic first and the prose second.
- Avoid em dashes in polished output by default. Prefer commas, parentheses, or full stops. Use colons sparingly unless the user explicitly asks to preserve dash-based punctuation or wants a colon-led style.

## Reader workflow

See `../../../_shared/core/reader-workflow.md` (loaded via manifest `always_load`) for the 5-step reader question sequence. Polishing should help the paper answer those questions in order.

## Protect the core argument

The paper's core argument includes:

- the scientific question the paper actually answers
- why that question matters
- how the work differs from existing research
- what the results imply
- how the main line of reasoning unfolds

AI may help polish, structure, or compare phrasings. AI should not invent or author the core argument. If the argument is weak or unclear, expose that weakness rather than hiding it under polished language.

## Target-Journal Polishing Stance

When polishing for a named journal, load
`../../../windenergy-submission/references/journal-profiles.md` and apply the
matching slug:

1. **English variant**: Pick American or British. Do not mix. Flag inconsistencies.
2. **Length awareness**: Flag text that may push the manuscript beyond the target profile.
3. **Reference awareness**: Apply reference-count or citation-style limits only after checking the target profile.
4. **Scope signal**: Tie wind and AI claims to energy-system value and journal scope.
5. **Review mode**: For double-anonymized targets, flag author-identifying text.
6. **Math formatting**: Prefer editable equations, solidus for fractions, exp() for powers of e, and clear variable definitions.
