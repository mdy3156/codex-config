---
name: scientific-visualization
description: Create or revise scientific figures, or audit their data encoding, accessibility, and publication exports.
license: MIT
metadata:
  version: "1.2"
  skill-author: K-Dense Inc.
  compatibility: Python 3.11+ for bundled helpers; optional plotting/image libraries depend on the selected task.
---

# Scientific Visualization

Produce the requested figure or audit with accurate data encoding and a usable final artifact. Preserve the project's plotting stack and export conventions unless the task requires a change.

## Scientific constraints

- Preserve raw data/images and the transformations needed to reproduce the figure. Do not invent, hide, or selectively enhance evidence.
- Distinguish missing, zero, censored, and excluded values; do not silently interpolate across gaps. Identify uncertainty, sample size, and the unit of replication when relevant.
- Use scales, baselines, normalization, and area/volume encodings that represent the quantity honestly. Disclose filtering, smoothing, binning, and image adjustments.
- Use color with another cue and inspect readability at the delivered size. A palette audit or grayscale check alone does not certify accessibility.
- Follow the exact journal, article type, figure type, and submission phase when publication compliance is requested. Verify current official instructions; bundled publisher profiles are dated snapshots. If the destination is unknown, a provisional general figure can proceed.
- Keep interactive and static artifacts distinct. For web delivery, supply appropriate labels and accessible text/data alternatives; hover alone is insufficient.

## Choose the relevant resource

| Task | Resource |
| --- | --- |
| Selecting encodings, uncertainty, or integrity review | [Publication guidelines](references/publication_guidelines.md) |
| Palette choice, contrast, grayscale, color management | [Color palettes](references/color_palettes.md) |
| Matplotlib, Seaborn, or Plotly implementation examples | [Plotting examples](references/matplotlib_examples.md) |
| Target-journal export requirements | [Journal requirements](references/journal_requirements.md), then live official guidance |
| Metadata, palette, style, export, or publisher helper commands | [Bundled tools](references/tools.md) |
| Source provenance and version snapshots | [Sources](references/sources.md) |

Load only what the task needs. A label edit does not require a publisher audit or a fresh dependency environment.

## Implementation and completion

Use scoped plotting styles. When physical dimensions matter, preserve the intended page size: `bbox_inches="tight"` can change it. For example code importing bundled helpers, follow the import-path setup in the plotting examples rather than assuming those modules are installed globally.

Export to the user's destination, inspect the affected render at its final size, and fix clipping, illegible labels, misleading encodings, or export errors caused by the change. For a compliance audit, also inspect the relevant metadata and current venue rules. Stop after the requested artifacts and checks are complete; report unverified properties explicitly. Automatic screening does not certify scientific validity, accessibility, or publisher acceptance.

Keep upstream attribution in the skill's metadata and source files. Add acknowledgments or bibliography entries to a user's manuscript only when requested or required by the applicable publication policy.
