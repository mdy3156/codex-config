# Kaggle CLI Command Patterns

These examples are patterns, not a substitute for the installed CLI help. Always
confirm the exact flags with `--help` before running a command.

Use `orbit-wars` as the competition slug for Kaggle Orbit Wars.

## Help and Version Discovery

```bash
kaggle --help
kaggle --version
kaggle competitions --help
kaggle kernels --help
kaggle datasets --help
kaggle forums --help
```

For a subcommand, inspect that exact subcommand:

```bash
kaggle competitions download --help
kaggle kernels pull --help
kaggle datasets create --help
```

## Competition Data

List available files:

```bash
kaggle competitions files orbit-wars
```

Download competition data to an ignored local data directory:

```bash
kaggle competitions download orbit-wars -p data/raw/orbit-wars
```

After download, inspect archive names and extract intentionally. Do not
overwrite existing raw data without user approval.

Useful competition commands to inspect:

```bash
kaggle competitions list --help
kaggle competitions files --help
kaggle competitions download --help
kaggle competitions submit --help
kaggle competitions submissions --help
kaggle competitions leaderboard --help
```

## Submissions and Leaderboards

Submit only when the user explicitly asks. For Orbit Wars, submissions are bot
files, not prediction CSVs. The submitted file should be a `main.py` with an
`agent` function at the root, or a `.tar.gz` archive with `main.py` at the archive
root.

```bash
kaggle competitions submit orbit-wars \
  -f outputs/submission-export/20260515_001_baseline/main.py \
  -m "baseline single-file agent"
```

For multi-file agents:

```bash
kaggle competitions submit orbit-wars \
  -f outputs/submission-export/20260515_001_baseline/submission.tar.gz \
  -m "baseline packaged agent"
```

List prior submissions:

```bash
kaggle competitions submissions orbit-wars
```

Fetch leaderboard data only after checking the command help:

```bash
kaggle competitions leaderboard orbit-wars
```

For simulation competitions, inspect these commands before downloading replays
or logs:

```bash
kaggle competitions episodes --help
kaggle competitions replay --help
kaggle competitions logs --help
```

Typical replay/log flow:

```bash
kaggle competitions episodes SUBMISSION_ID
kaggle competitions replay EPISODE_ID -p outputs/replay-analysis/20260515_001_episode_123456/artifacts
kaggle competitions logs EPISODE_ID 0 -p outputs/replay-analysis/20260515_001_episode_123456/logs
```

## Notebooks and Kernels

Kaggle CLI uses the `kernels` command group for notebooks.

Find notebooks related to a competition:

```bash
kaggle kernels list --competition orbit-wars --kernel-type notebook
```

Before relying on filters such as language, sort, page, or page size, inspect:

```bash
kaggle kernels list --help
```

Pull notebook source into this repository's notebook raw/download area:

```bash
kaggle kernels pull OWNER/KERNEL-SLUG \
  -p docs/notebooks/downloaded/OWNER-KERNEL-SLUG
```

If metadata or output files are needed, inspect and use:

```bash
kaggle kernels files OWNER/KERNEL-SLUG
kaggle kernels output OWNER/KERNEL-SLUG -p outputs/kernels/OWNER-KERNEL-SLUG
```

After pulling notebooks, summarize relevant methods and findings in
`docs/notebooks/summaries/`.

## Datasets

Search and inspect datasets:

```bash
kaggle datasets list -s "orbit wars"
kaggle datasets files OWNER/DATASET-SLUG
kaggle datasets download OWNER/DATASET-SLUG -p data/external/OWNER-DATASET-SLUG
```

Create a private dataset from a prepared local directory. Keep the staging
directory under an ignored path such as `outputs/kaggle-datasets/NAME`.

```bash
kaggle datasets init -p outputs/kaggle-datasets/NAME
```

Edit the generated metadata without adding secrets. Then create the dataset:

```bash
kaggle datasets create -p outputs/kaggle-datasets/NAME
```

Create a new version:

```bash
kaggle datasets version \
  -p outputs/kaggle-datasets/NAME \
  -m "short reproducible version message"
```

Do not make a dataset public unless the user explicitly requests it and the
contents have been checked for credentials, private data, competition-rule
issues, and unnecessary large artifacts.

## Discussions, Forums, and Topics

Browse competition-specific topics:

```bash
kaggle competitions topics list --help
kaggle competitions topics show --help
kaggle competitions topics list orbit-wars --sort-by recent
kaggle competitions topics list orbit-wars --search "strategy"
kaggle competitions topics show orbit-wars/TOPIC_ID
```

Browse general Kaggle forums and topics:

```bash
kaggle forums
kaggle forums topics list --category competitions --sort-by recent
kaggle forums topics list FORUM_SLUG --search "query"
kaggle forums topics show FORUM_SLUG/TOPIC_ID
```

Both `show` commands accept a bare numeric topic ID. They also accept the scope
and ID as two arguments; prefer `scope/TOPIC_ID` because it is easy to preserve
as one reconstructable reference. Use `--page-size` and `--page-token` when the
topic or topic list is paginated. Use `-v` for CSV when structured capture is
useful.

Do not use the deprecated `kaggle competitions topic-messages`; use
`kaggle competitions topics show` so the topic and its comments are displayed
in tree form.

Save raw command output and synthesized summaries separately:

```text
docs/discussions/raw/
docs/discussions/summaries/
```

Raw captures should include the collection command, topic reference, source URL
when known, topic title and ID, collection date, and pagination or access
limitations. Summaries should include key claims, implementation ideas,
verification status, and next actions. Classify each claim as `verified`,
`speculative`, or `needs local validation`.

If these subcommands are absent, update the installed Kaggle CLI and recheck
`--help`. Do not use Gemini CLI as a substitute for retrieving Discussions.

## Credential Safety

Allowed:

- run Kaggle commands that rely on already configured credentials
- report authentication errors without revealing secret values
- tell the user to configure credentials outside the repository

Forbidden:

- read `~/.kaggle/kaggle.json`
- print tokens or API keys
- copy credentials into `.env`, docs, configs, notebooks, or dataset metadata
- commit credential files or downloaded private data
