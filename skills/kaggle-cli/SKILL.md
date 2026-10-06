---
name: kaggle-cli
description: Use or troubleshoot the Kaggle CLI, including commands, authentication, metadata, downloads, uploads, and submissions.
---

# Kaggle CLI

Use the installed `kaggle` command and the task-specific reference below. Inspect `kaggle --help` or the relevant subcommand's help when syntax or availability is uncertain. Live help takes precedence over this reference snapshot; report meaningful version differences.

## Reference Map

Read only the reference needed for the user's task:

- [Competitions](references/competitions.md) - competition discovery, files, downloads, submissions, leaderboards, simulations, pages, topics.
- [Datasets](references/datasets.md) - dataset search, files, downloads, metadata, create/version/status/delete, topics.
- [Kernels](references/kernels.md) - notebook/script discovery, metadata, push/pull, outputs, status, logs, delete.
- [Models](references/models.md) - model records, metadata, create/get/update/delete, model topics.
- [Model Variations](references/model_variations.md) - create and manage framework-specific model variations.
- [Model Variation Versions](references/model_variations_versions.md) - create, list, download, inspect, and delete variation versions.
- [Files](references/files.md) - inbox uploads, resumable uploads, directory compression behavior.
- [Forums](references/forums.md) - global discussion forums, topics, and comments.
- [Benchmarks](references/benchmarks.md) - benchmark auth/init, task push/run/status/download/log/model flows, benchmark topics.
- [Configuration](references/configuration.md) - config file, default path, proxy, default competition.
- [Authentication](references/auth.md) - OAuth login, access token printing, revocation, token/key sources.
- [Quota](references/quota.md) - weekly GPU/TPU accelerator quota.
- [Search](references/search.md) - unified cross-content search over competitions, datasets, notebooks, models, users, and discussions.

## Operating guidance

- Use the existing installation; install the CLI only when execution is requested and it is missing.
- Use the relevant `init` command for new metadata when available. Variation-version metadata starts with `models variations init`; there is no `models variations versions init` in this snapshot.
- Authentication choices and token locations are in the authentication reference. Keep tokens out of chat and logs.
- Carry out requested local preparation and validation without repeated approval. Downloads, uploads, execution, publication, submissions, and deletions have different effects: perform only the operations covered by the request and inspect their results. A metadata edit alone does not authorize publication or submission.
- On authentication, quota, or version failures, resolve the specific blocker or report it. Do not retry external mutations indefinitely.
