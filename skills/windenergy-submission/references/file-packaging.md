# File Packaging Guide

Use this guide with `journal-profiles.md`. It uses Elsevier-style editable
source and artwork rules as the default, then applies target-journal
differences.

## Default File Format Requirements

### Manuscript file

| Format | Accepted | Notes |
|--------|----------|-------|
| .doc / .docx | Yes (preferred) | Single-column layout |
| .tex | Yes | Double-column permitted |
| .pdf | No | Usually not accepted as the editable source file |

**Key rules:**
- Provide **editable source files** for the entire submission
- Format Word files in **single-column layout**
- Remove any **strikethrough** and **underlined text** (unless scientifically significant)
- Run **spell-check and grammar-check** before submission

### Figure files

| Format | Use case | Resolution |
|--------|----------|------------|
| TIFF / JPG / PNG | Color or grayscale photos (halftone) | min 300 dpi |
| TIFF / JPG / PNG | Bitmapped line drawings | min 1000 dpi |
| TIFF / JPG / PNG | Line/halftone combinations | min 500 dpi |
| EPS / PDF | Vector drawings | Embed fonts or save text as graphics |

**Key rules:**
- Submit each figure as a **separate file**
- Use **logical naming**: Figure_1, Figure_2, etc.
- Text graphics may be embedded in the manuscript text at the appropriate position
- LaTeX: text graphics may be embedded in the .tex file

**Pixel requirements:**

| Type | Single column width | Full page width |
|------|--------------------|-----------------|
| Halftone | min 1063 pixels | min 2244 pixels |
| Bitmapped | min 3543 pixels | min 7480 pixels |
| Combination | min 1772 pixels | min 3740 pixels |

### Graphical abstract file

| Property | Requirement |
|----------|-------------|
| Dimensions | 531 x 1328 pixels (h x w) or proportionally larger |
| Readable at | 5 x 13 cm |
| Format | TIFF, EPS, PDF, or MS Office files |
| Generative AI | Check target guide and AI policy before use |

### Highlights file

- Separate editable file (.docx or .txt)
- Filename must include "highlights"
- 3-5 bullet points, each max 85 characters

### Competing interests declaration

- .doc or .docx format
- No signatures required

### Supplementary material

- Any standard format
- Cite all files in manuscript text
- Include concise descriptive caption for each
- Will appear online exactly as received (not formatted or checked)

### Video files

| Property | Requirement |
|----------|-------------|
| Max per file | 150 MB |
| Max total | 1 GB |
| Format | Recommended formats (check Elsevier guidelines) |
| Stills | Provide for each video file |

## File packaging checklist

### Required files

- [ ] Main manuscript (.docx or .tex, NOT .pdf)
- [ ] All figure files (separate, logically named)
- [ ] Highlights file (separate, "highlights" in filename)
- [ ] Competing interests declaration (.docx)
- [ ] Cover letter when required by the target profile or submission system

### Conditional files

- [ ] Graphical abstract when required or encouraged by the target profile
- [ ] Supplementary material files (if any)
- [ ] Video files (if any, with stills)
- [ ] Data availability statement (if not in manuscript)

### File naming convention

Recommended naming for clarity:

```text
Manuscript.docx
Figure_1.tif
Figure_2.tif
Figure_3.png
Highlights.docx
Cover_Letter.docx
Competing_Interests.docx
Graphical_Abstract.pdf
Supplementary_Material.pdf
Supplementary_Video_1.mp4
Supplementary_Video_1_Still.png
```

## LaTeX-specific guidance

- Double-column formatting is permitted
- Use standard Elsevier LaTeX class (elsarticle)
- Embed figures using standard LaTeX commands
- Text graphics may be embedded in the .tex file
- Submit .tex source, .bib file, and all figure files

## Common packaging issues

### Issue 1: PDF submitted instead of editable source

Many Elsevier submissions require editable source files and do not accept a PDF
as the source manuscript.

**Fix:** Convert to .docx or provide .tex source files.

### Issue 2: Figures embedded in manuscript instead of separate files

Many target journals require figures as **separate files**. Text graphics may
be embedded, but photographic and complex figures should usually be separate.

**Fix:** Extract each figure to its own file with proper naming.

### Issue 3: Low-resolution figures

Figures below the minimum resolution will be flagged.

**Fix:** Regenerate at proper resolution:
- Photos: 300+ dpi
- Line art: 1000+ dpi
- Combinations: 500+ dpi

### Issue 4: Strikethrough or tracked changes in manuscript

Final submission files should not contain unresolved tracked changes,
strikethrough, or underlined revision markup unless it has scientific
significance.

**Fix:** Accept all tracked changes and remove strikethrough formatting before submission.

## QA checklist

- [ ] Main manuscript is .docx or .tex (not PDF)
- [ ] Word files are single-column layout
- [ ] No strikethrough or underlined text
- [ ] Each figure is a separate file
- [ ] Figure files properly named (Figure_1, etc.)
- [ ] Figure resolution meets minimum requirements
- [ ] Highlights file has "highlights" in filename
- [ ] Competing interests saved as .docx
- [ ] All supplementary files cited in text
- [ ] Video files within size limits (150 MB each, 1 GB total)
- [ ] Spell-check and grammar-check completed
