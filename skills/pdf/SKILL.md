---
name: "pdf"
description: "Read, create, or review PDFs when text extraction, page rendering, or layout fidelity matters."
---

# PDF Skill

## Local tools

Use `~/.venvs/pdf-tools/bin/python` for Python-based PDF generation and extraction when available; use the project environment if it already provides the required tools. Poppler's `pdftoppm` can render selected pages for visual inspection:

```bash
pdftoppm -f 3 -l 3 -scale-to 1600 -png input.pdf /tmp/pdf-page
```

Choose the pages needed for the request. After layout changes, inspect the affected renders and correct clipping, pagination, or font issues before delivery. Report unavailable render checks rather than claiming visual verification.

## PDF-to-Markdown conversions

For `filename.pdf`, first check whether same-directory conversion outputs exist:

1. `filename.mineru/filename.md`
2. `filename.marker/filename.md`

Prefer `filename.mineru/filename.md` for searchable text when available. Use `filename.marker/filename.md` as a fallback or comparison source.

Treat all PDF-to-Markdown outputs as convenience layers, not as the source of truth. They may contain:

- incorrect reading order,
- malformed equations,
- missing or misplaced figures,
- table reconstruction errors,
- repeated hallucinated fragments,
- simplified mathematical symbols.

Always verify important claims, formulas, page references, figures, tables, captions, and exact notation against the original PDF.

When images are needed, keep the whole conversion directory together. Do not copy only the Markdown file, because image links usually depend on relative paths such as `images/...`.

Expected local conversion layouts:

```text
filename.mineru/
  filename.md
  images/

filename.marker/
  filename.md
  images/ or extracted image files
```
