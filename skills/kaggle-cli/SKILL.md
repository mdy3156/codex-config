---
name: kaggle-cli
description: "Use Kaggle CLI safely for Kaggle competition workflows: inspect installed command help, browse and read Discussions, download competition data, manage notebooks/kernels and datasets, submit entries, check leaderboard/submission state, and document research artifacts. Use when working with Kaggle or this Orbit Wars repository, especially when credentials must remain private and raw research evidence must be kept separate from summaries."
---

# Kaggle CLI

## Core Rules

Treat the installed CLI as the source of truth. Before using any command, inspect
the relevant help:

```bash
kaggle --help
kaggle competitions --help
kaggle kernels --help
kaggle datasets --help
kaggle forums --help
```

Never read or print credential files or secret values. Do not inspect
`~/.kaggle/kaggle.json`, `.env`, API keys, tokens, private keys, or shell
history. If authentication fails, report the command error without exposing
credential contents.

Prefer read-only discovery commands before write commands. Avoid delete,
overwrite, public publishing, expensive downloads, and submissions unless the
user explicitly requested that action.

## Workflow

1. Identify the competition slug, output path, and intended artifact.
2. Run `--help` for the relevant command group in the installed CLI.
3. Use a small read-only command to confirm the command works.
4. Save downloaded or generated artifacts under this repository's documented
   ignored paths, usually `data/`, `outputs/`, or the relevant `docs/*/raw/`.
5. Write summaries under the matching `docs/*/summaries/` path when doing
   research.

For detailed command patterns, read [references/commands.md](references/commands.md).

## Discussions and Forums

Use the current Kaggle CLI Discussion commands. For competition-specific
research, prefer `kaggle competitions topics list/show`. Use `kaggle forums`
and `kaggle forums topics list/show` to browse across general forums. Inspect
the exact subcommand help first because older installed versions may not include
these commands.

Save command output as raw evidence before synthesizing it:

- raw captures: `docs/discussions/raw/`
- synthesized notes: `docs/discussions/summaries/`

For every summary, record the source URL or reconstructable topic reference,
topic title and ID, collection date, key claims, implementation ideas,
verification status, and next actions. Label claims as `verified`,
`speculative`, or `needs local validation`; Discussion statements are not
ground truth.

If Discussion commands are missing, report that the installed CLI must be
updated. Do not substitute Gemini CLI as a Discussion retrieval path. Kaggle
notebooks remain under `kaggle kernels`.

## Repository Hygiene

Follow this repository's `AGENTS.md`.

- keep reusable commands centered in `src/orbit_wars/cli.py`, not a repo
  `scripts/` directory
- keep raw evidence and summaries separate
- keep generated outputs out of git
- do not commit credentials, competition data, checkpoints, submissions, or raw
  downloaded artifacts unless the repository explicitly allows it
