# SKILL: pdfdelta
**Source:** https://github.com/mli55/pdfdelta
**Domain:** code
**Trigger:** When comparing two versions of a PDF document (academic papers, technical reports) to visually highlight changes directly on the original pages

## Summary
pdfdelta is a lightweight visual diff tool for born-digital PDFs. It produces two annotated PDFs: one with deletions highlighted on the old version, one with additions highlighted on the new version. Handles multi-column layouts and filters reflow noise.

## Key Patterns
- Global diff: flatten all pages → SequenceMatcher → word-level precision
- Reflow filter: suppresses cross-page/cross-column noise from text reflow
- Layout-aware: handles multi-column papers, figures, tables, math formulas
- Output: `old_marked.pdf` (deletions) + `new_marked.pdf` (additions)
- Built on PyMuPDF for word-level bounding boxes

## Usage
```bash
pip install pdfdelta
pdfdelta old.pdf new.pdf
# Options:
pdfdelta old.pdf new.pdf --old-out deletions.pdf --new-out additions.pdf --opacity 0.5
```

## Code/Template
```python
# Programmatic use
from pdfdelta import diff_pdfs
diff_pdfs("old.pdf", "new.pdf", old_out="old_marked.pdf", new_out="new_marked.pdf")
```
