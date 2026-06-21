---
name: zoom-out
description: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code, need to understand how it fits into the bigger picture, or want a CodeGraph-backed map of relevant modules, callers, callees, and data flow in a larger repository.
---

# Zoom Out

Go up a layer of abstraction. Give the user a map of the relevant modules, callers, callees, data flow, and domain concepts.

## Workflow

1. Read project orientation files first when they exist: `AGENTS.md`, `README.md`, `CONTEXT.md`, and relevant ADRs.
2. For large repositories or unfamiliar areas, use CodeGraph before manual grep/read exploration.
   - Use `codegraph_explore` for natural-language architecture questions and symbol-to-symbol flows.
   - Use `codegraph_search` only when the task is just locating a named symbol.
   - Use `codegraph_callers`, `codegraph_callees`, or `codegraph_impact` for call relationships or refactor blast radius.
3. Summarize at the domain level before implementation details.
4. Include concrete file and symbol references for claims that matter.
5. Call out uncertainty, stale CodeGraph results, or missing index state. If CodeGraph is unavailable, fall back to focused `rg` and file reads.

## Output Shape

- What this area is for.
- The important modules and how they relate.
- The main entry points and downstream effects.
- The vocabulary the project uses for these concepts.
- Where to look next for a change or bug.
