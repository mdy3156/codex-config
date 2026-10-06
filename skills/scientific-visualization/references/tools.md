# Figure tools and example environment

Use the relevant helper from the figure project. Honor the requested output location; the examples use `outputs/`:

```bash
SCIVIZ_SKILL="${CODEX_HOME:-$HOME/.codex}/skills/scientific-visualization"
mkdir -p outputs
```

Use the project's Python environment. Raster inspection needs Pillow; PDF inspection needs pypdf; rendering needs Matplotlib. Palette audits and profile planning use the standard library. Install only dependencies needed for the selected operation.

## Pinned snapshot

Optional historical environment snapshot (2026-07-23). Prefer the project environment; use these direct pins only when reproducing that snapshot:

```bash
uv run --isolated --no-project --python 3.13 \
  --with "matplotlib==3.11.1" \
  --with "seaborn==0.13.2" \
  --with "plotly==6.9.0" \
  --with "kaleido==1.3.0" \
  --with "pillow==12.3.0" \
  --with "pypdf==6.14.2" \
  python your_figure.py
```

This is a dated direct-dependency snapshot, not a transitive lock. Use the project's uv lock for exact replay; this skill intentionally ships no dependency lock.

## Bundled CLIs

The Python helpers perform local operations. Commands using `uv run --with` may download dependencies. Helpers reject symlink inputs/destinations where relevant and require explicit overwrite flags; consult the relevant `--help`.

### Inspect raster/vector metadata

```bash
python3 "$SCIVIZ_SKILL/scripts/image_metadata.py" figure.tiff \
  --format tiff --mode RGB --min-dpi 300 --target-width-mm 85 \
  --alpha-policy forbid
```

Supports raster images (Pillow), SVG, PDF (pypdf), and EPS/PS. Reports dimensions, DPI/effective DPI, mode, alpha, ICC presence, compression, page size, and conservative first-page PDF font resources. It does not inspect every embedded raster in a vector container.

### Audit palette contrast and grayscale

```bash
python3 "$SCIVIZ_SKILL/scripts/palette_audit.py" \
  --palette okabe_ito_on_white \
  --background FFFFFF \
  --role graphical
```

Reports exact WCAG sRGB contrast plus pairwise CIE L* grayscale screening. The grayscale threshold is a heuristic, not a standard.

### Plan/screen publisher export

```bash
python3 "$SCIVIZ_SKILL/scripts/export_plan.py" \
  --publisher nature \
  --figure-type combination \
  --width single \
  --phase final
```

Add `--input figure.pdf` to screen machine-readable properties. Profiles are official-source snapshots accessed 2026-07-23, not automatic compliance rules.

### Preview styles

```bash
python3 "$SCIVIZ_SKILL/scripts/style_preview.py" \
  --output outputs/style-preview \
  --style default \
  --palette okabe_ito_on_white \
  --formats png,svg
```

### Inspect/write styles and smoke-test export

```bash
python3 "$SCIVIZ_SKILL/scripts/style_presets.py" --list
python3 "$SCIVIZ_SKILL/scripts/style_presets.py" --show nature
python3 "$SCIVIZ_SKILL/scripts/figure_export.py" --demo outputs/export-smoke --manifest
```

## Assets

- `assets/publication.mplstyle`: general print starting point.
- `assets/nature.mplstyle`: dated flagship Nature visual starting point, not a compliance preset.
- `assets/presentation.mplstyle`: larger projected-display style.
- `assets/color_palettes.py`: importable Okabe-Ito and Paul Tol values with metadata.
- `assets/publisher_profiles.json`: dated, machine-readable planning snapshots.

Matplotlib style files omit `#` in hex colors because `#` begins comments in `.mplstyle` parsing.

