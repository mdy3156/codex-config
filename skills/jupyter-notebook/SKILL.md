---
name: jupyter-notebook
description: Create or edit Jupyter notebooks (.ipynb) for experiments, analysis, or tutorials.
---

# Jupyter Notebooks

Produce a notebook that supports the requested experiment or teaching objective and can be read and run in order. For existing notebooks, preserve the user's content and structure outside the requested change.

## New notebooks

Use the bundled standard-library helper to avoid malformed notebook JSON:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/jupyter-notebook/scripts/new_notebook.py" \
  --kind experiment --title "Compare prompt variants" \
  --out output/jupyter-notebook/compare-prompt-variants.ipynb
```

Choose `experiment` for analysis and `tutorial` for teaching. Honor the user's output path and project conventions. Without `--out`, the helper writes under `output/jupyter-notebook/` in the working repository, or the working directory when outside a repository. Existing files require an intentional `--force` overwrite.

## Relevant guidance

- Experiments: [experiment patterns](references/experiment-patterns.md).
- Teaching material: [tutorial patterns](references/tutorial-patterns.md).
- Direct JSON edits or structural problems: [notebook structure](references/notebook-structure.md).
- Delivery review of a new or substantially revised notebook: [quality checklist](references/quality-checklist.md).

Read the resource that fits the change. A small edit does not require every checklist or a structural rewrite.

## Execution and delivery

Keep code cells focused and explain non-obvious assumptions or expected results in Markdown. Use the project's environment; the scaffold helper needs no extra packages. Execution may require the notebook's own dependencies.

Run changed code and its prerequisites, or a fresh top-to-bottom run for a new notebook, when inputs and resources are available and execution is within the authorized scope. Inspect cells before running notebooks with external writes, paid calls, or lengthy computations. Report what ran and any missing data or execution blockers; do not present saved outputs as proof of a fresh run.
