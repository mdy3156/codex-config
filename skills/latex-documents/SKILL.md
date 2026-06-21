---
name: latex-documents
description: Work with LaTeX documents and papers, especially Japanese documents that use the user's LaTeX Workshop recipes. Use when editing .tex files, choosing uplatex/lualatex/pdflatex from `% !LW recipe=...`, compiling with latexmk, diagnosing LaTeX build errors, or formatting numbered display equations with the user's equation-numbering conventions.
---

# LaTeX Documents

## Overview

Follow the user's VS Code LaTeX Workshop build behavior and math formatting conventions. Keep document edits surgical: preserve the existing class, engine, packages, and style unless the user explicitly asks for a broader rewrite.

## Build Workflow

1. Treat the root `.tex` file as the build target. If the user points at a chapter/subfile, find the intended root before compiling.
2. Read the first lines of the root file for the user's engine selector:

   ```tex
   % !LW recipe=uplatex
   % !LW recipe=lualatex
   % !LW recipe=pdflatex
   ```

3. Prefer the declared recipe. If no `% !LW recipe=...` exists, infer only when obvious from the existing document; otherwise ask before adding or changing an engine selector.
4. Compile with LaTeX Workshop-equivalent `latexmk` commands and `build` as the output directory.

Use the bundled helper when possible:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/latex-documents/scripts/latex_workshop_build.py" path/to/main.tex
```

For inspection without compiling:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/latex-documents/scripts/latex_workshop_build.py" path/to/main.tex --dry-run
```

Recipe mapping:

- `uplatex`: `latexmk -pdfdvi -e "$latex='uplatex %O %S'; $bibtex='upbibtex %O %B'; $dvipdf='dvipdfmx %O -o %D %S'" -synctex=1 -interaction=nonstopmode -file-line-error`
- `lualatex`: `latexmk -lualatex -synctex=1 -interaction=nonstopmode -file-line-error`
- `pdflatex`: `latexmk -pdf -synctex=1 -interaction=nonstopmode -file-line-error`

## Equation Numbering

Default to numbered display math. Do not use starred environments such as `equation*`, `align*`, or `gather*` unless the user asks for no equation numbers or the expression is clearly incidental.

Use these patterns:

- One single-line equation: use `equation`.
- Multiple independent equations: use `align` and allow each equation line to receive its own number.
- One logical equation or derivation split across visual lines: use `align` and put `\notag` or `\nonumber` on all earlier continuation lines so only the final line is numbered.

Example of one logical equation split over several lines:

```tex
\begin{align}
  F(x)
  &= a_1 + a_2 + a_3 + a_4 \notag \\
  &\quad + a_5 + a_6.
\end{align}
```

Example of separate equations, each numbered:

```tex
\begin{align}
  f'(x) &= 2x + 1, \\
  f''(x) &= 2.
\end{align}
```

Avoid `eqnarray`. Prefer `amsmath`/`mathtools` conventions already present in the document.

## Editing Guidance

- Preserve Japanese punctuation, macros, labels, bibliography commands, and package order unless changing them is required.
- Keep labels stable. When adding labels, match the local naming style.
- After edits, compile the root file when practical and report the exact recipe used.
- If compilation fails, fix the first meaningful LaTeX error before chasing later cascade errors.
