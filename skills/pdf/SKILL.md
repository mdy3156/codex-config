---
name: "pdf"
description: "Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; first check for same-directory PDF-to-Markdown conversion directories `filename.mineru/` and `filename.marker/`, prefer MinerU output for searchable text when available, verify important details against the original PDF by rendering pages with Poppler, and use the local PDF tools virtual environment at `~/.venvs/pdf-tools` for Python-based generation and extraction."
---

# PDF Skill

## When to use

- Read or review PDF content where layout and visuals matter.
- Create PDFs programmatically with reliable formatting.
- Validate final rendering before delivery.
- Compare PDF-to-Markdown conversions against the original PDF.

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
