---
name: windenergy-reader
description: >-
  Build full-paper Chinese-English side-by-side, figure/table-aware, and
  source-grounded Markdown readers for journal or conference papers in renewable
  energy, wind power, smart grids, energy forecasting, and AI-for-energy. Use
  when the user asks to translate or read a paper, make 中英文对照, 原文对照,
  全文翻译解读, extract figures/tables into the right positions, preserve
  figure/table placement near relevant prose, or keep exact source anchors. Do
  not degrade into a summary-only output unless the user explicitly asks for a
  summary.
---

# Renewable Paper Reader

Turn a research paper into a complete Markdown reading artifact. The default
output is a bilingual companion, not a summary.

## Router Protocol

Read `manifest.yaml`, load all `always_load` files, detect `source_format`, and
then load only the matching `static/fragments/source/*.md` files. Use
`references/output-spec.md` or `references/grounding-rules.md` only when the
task needs exact schemas or follow-up grounding rules.

Before writing generated files, load `../_shared/core/output-run-folders.md`
and create a run folder for this invocation. Put `paper.md`, source maps,
notes, and extracted assets in that run folder.

## Default Deliverables

- `paper.md`: full bilingual reader.
- `source_map.json`: page/block/figure/table traceability.
- `translation_notes.md`: extraction, OCR, and terminology notes.
- `assets/`: cropped figures and tables.

## Workflow

1. Identify the source type: selectable PDF, scanned PDF, publisher HTML, DOI or
   arXiv link, pasted text, or notes.
2. Build a full-document source map before translating.
3. Create stable IDs: `S001` for text, `C001` for captions, `F001` for figures,
   and `T001` for tables.
4. Translate every substantive block conservatively, preserving equations,
   units, citations, model names, metrics, and hedging.
5. Crop figures/tables tightly and place them near the first substantive
   discussion, with original and Chinese captions.
6. Write `paper.md` with section/page navigation, bilingual blocks, figure/table
   blocks, terminology notes, and uncertainty notes when needed.
7. Answer follow-up questions from source block IDs rather than memory.

## Bilingual Block Format

```markdown
<a id="S001"></a>
**Source:** p.1 S001

**Original:** [source paragraph]

**中文:** [faithful Chinese translation]
```

## Figure/Table Block Format

```markdown
<a id="F001"></a>
### Fig. 1. [short translated title]

**Placed near:** p.3 S012
**Source:** p.4 C001

![Fig. 1](assets/fig1.png)

**Original caption:** [caption text]

**中文图注:** [caption translation]

**Reading note:** [what to inspect in the figure]
```

## Red Lines

- Do not replace a requested full reader with only a summary.
- Do not skip methods, limitations, data availability, or extended captions.
- Do not guess unreadable OCR text.
- Do not reproduce long copyrighted text directly in chat; write local artifacts
  for user-provided files and summarize in chat.
