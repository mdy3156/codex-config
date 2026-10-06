# LaTeX Templates for ML/AI Conferences

This directory contains historical LaTeX snapshots for ML/AI conferences, including community or modified templates. They are not guaranteed current or complete. Use the official venue/year/track source below for submission requirements; preserve an existing project's working template.

Systems conference templates are not bundled here; obtain the selected venue's current official template.

## Compiling LaTeX to PDF

Use the project's declared engine and build recipe. For the user's LaTeX Workshop conventions, see [latex-documents](../../latex-documents/SKILL.md). Install missing packages only when the selected project requires them; do not replace editor settings or install a full TeX distribution as a routine step.

For an ordinary pdfLaTeX template with no project-specific recipe:

```bash
latexmk -pdf main.tex
```

Build the actual root file and resolve the first meaningful error. If an example references an absent figure, supply the requested figure or replace/remove the example in the copied project before compiling.

## Available Templates

### ML/AI Conferences

| Conference | Directory | Year | Source |
|------------|-----------|------|--------|
| ICML | `icml2026/` | 2026 | [Official ICML](https://icml.cc/Conferences/2026/AuthorInstructions) |
| ICLR | `iclr2026/` | 2026 | [Official GitHub](https://github.com/ICLR/Master-Template) |
| NeurIPS | `neurips2025/` | 2025 | Community snapshot; verify against [official NeurIPS](https://neurips.cc/) |
| ACL | `acl/` | 2025+ | [Official ACL](https://github.com/acl-org/acl-style-files) |
| AAAI | `aaai2026/` | 2026 | Modified unified snapshot; compare with [AAAI Author Kit](https://aaai.org/authorkit26/) |
| COLM | `colm2025/` | 2025 | [Official COLM](https://github.com/COLM-org/Template) |

## Usage

### ICML 2026

```latex
\documentclass{article}
\usepackage{icml2026}  % For submission
% \usepackage[accepted]{icml2026}  % For camera-ready

\begin{document}
% Your paper content
\end{document}
```

Key files:
- `icml2026.sty` - Style file
- `icml2026.bst` - Bibliography style
- `example_paper.tex` - Example document

### ICLR 2026

```latex
\documentclass{article}
\usepackage[submission]{iclr2026_conference}  % For submission
% \usepackage[final]{iclr2026_conference}  % For camera-ready

\begin{document}
% Your paper content
\end{document}
```

Key files:
- `iclr2026_conference.sty` - Style file
- `iclr2026_conference.bst` - Bibliography style
- `iclr2026_conference.tex` - Example document

### ACL Venues (ACL, EMNLP, NAACL)

```latex
\documentclass[11pt]{article}
\usepackage[review]{acl}  % For review
% \usepackage{acl}  % For camera-ready

\begin{document}
% Your paper content
\end{document}
```

Key files:
- `acl.sty` - Style file
- `acl_natbib.bst` - Bibliography style
- `acl_latex.tex` - Example document

### AAAI 2026

```latex
\documentclass[letterpaper]{article}
\usepackage[submission]{aaai2026}  % For submission
% \usepackage{aaai2026}  % For camera-ready

\begin{document}
% Your paper content
\end{document}
```

Key files:
- `aaai2026.sty` - Style file
- `aaai2026.bst` - Bibliography style

### COLM 2025

```latex
\documentclass{article}
\usepackage[submission]{colm2025_conference}  % For submission
% \usepackage[final]{colm2025_conference}  % For camera-ready

\begin{document}
% Your paper content
\end{document}
```

Key files:
- `colm2025_conference.sty` - Style file
- `colm2025_conference.bst` - Bibliography style

## Historical Page-Limit Notes

The values below are stored planning notes, not verified current rules. Check the official venue/year/track and submission stage before using them.

| Conference | Submission | Camera-Ready | Notes |
|------------|-----------|--------------|-------|
| ICML 2026 | 8 pages | 9 pages | +unlimited refs/appendix |
| ICLR 2026 | 9 pages | 10 pages | +unlimited refs/appendix |
| NeurIPS 2025 | 9 pages | 9 pages | +checklist outside limit |
| ACL 2025 | 8 pages (long) | varies | +unlimited refs/appendix |
| AAAI 2026 | 7 pages | 8 pages | +unlimited refs/appendix |
| COLM 2025 | 9 pages | 10 pages | +unlimited refs/appendix |


## Common Issues

### Compilation Errors

1. **Missing packages**: Install only the package required by the existing template
2. **Bibliography errors**: Follow the template's existing `.bst` setup; AAAI sets its bibliography style in the style file, so do not add it twice
3. **Font warnings**: Diagnose the missing font and preserve venue-mandated font settings

### Anonymization

For an anonymous review submission, follow the venue rules; typical checks are:
- No author names in `\author{}`
- No acknowledgments section
- No grant numbers
- Use anonymous repositories
- Cite own work in third person

### Common LaTeX Packages

```latex
% Recommended packages (check compatibility with venue style)
\usepackage{amsmath,amsthm,amssymb}  % Math
\usepackage{graphicx}                 % Figures
\usepackage{booktabs}                 % Tables
\usepackage{hyperref}                 % Links
\usepackage{algorithm,algorithmic}    % Algorithms
\usepackage{natbib}                   % Citations
```

## Updating Templates

Templates are updated annually. Check official sources before each submission:
**ML/AI:**
- ICML: https://icml.cc/
- ICLR: https://iclr.cc/
- NeurIPS: https://neurips.cc/
- ACL: https://github.com/acl-org/acl-style-files
- AAAI: https://aaai.org/
- COLM: https://colmweb.org/

