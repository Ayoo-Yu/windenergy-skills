# Output format

## Default: Word document with tracked changes

When polishing a `.docx` manuscript, the primary output is a revised Word
document with OOXML tracked changes. Follow the Word Output Protocol in
`SKILL.md` to produce this automatically.

The output `.docx` must be placed next to the source file, named
`<source>_polished_tracked.docx`.

## Secondary: Markdown change log

Alongside the Word file, produce a Markdown report with the following structure
for each change:

```
### P<index>: <note>

**Original**:
> <old text>

**Polished**:
> <new text>

*Why*: <reason for the change>
```

Group changes by section (Abstract, Introduction, Methodology, etc.).

## Revision notes

After the change log, include a `Revision notes` section with 3-5 bullets on
the major structural and stylistic changes made across the whole manuscript.

If any paragraph's structural problem could not be fixed without inventing
content, say so explicitly instead of papering over it.

## Side-by-side format

If the user asks for side-by-side revision, provide:

- `Original`
- `Polished`
- `Why changed`

## Claim risk annotations

For any change that affects the strength of a scientific claim, add:

```
Claim risk: "<exact phrase to verify>"
```

This alerts the author to double-check that the softened claim still matches
their evidence.
