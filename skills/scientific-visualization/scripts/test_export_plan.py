"""Offline regression check: recommendations must not become hard limits or passes.

Run with a Python environment containing Pillow (also used for raster inspection).
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from export_plan import build_plan, validate_against_plan


def main() -> None:
    failures = []
    with TemporaryDirectory() as directory:
        root = Path(directory)
        svg = root / "tall.svg"
        svg.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="85mm" '
            'height="210mm"><rect width="10" height="10"/></svg>',
            encoding="utf-8",
        )
        cell = build_plan("cell", figure_type="combination", width="single")
        report = validate_against_plan(cell, svg)
        if any(
            item["name"] == "final_height_mm" and item["status"] == "fail"
            for item in report["findings"]
        ):
            failures.append("Cell's recommended 200 mm height became a hard failure")

        raster = root / "image.tiff"
        bmc = build_plan("bmc", figure_type="photo")
        for rule, dpi, expected in (
            (bmc["raster_dpi"], 72, "review"),
            (bmc["raster_dpi"], 300, "review"),
            ({"min": 300, "max": 600}, 299, "fail"),
            ({"min": 300, "max": 600}, 300, "pass"),
            ({"min": 300, "max": 600}, 600, "pass"),
            ({"min": 300, "max": 600}, 601, "fail"),
            ({"min_exclusive": 300}, 300, "fail"),
            ({"min_exclusive": 300}, 301, "pass"),
        ):
            Image.new("RGB", (16, 16), "white").save(raster, dpi=(dpi, dpi))
            report = validate_against_plan({**bmc, "raster_dpi": rule}, raster)
            actual = next(
                item["status"] for item in report["findings"]
                if item["name"] == "effective_raster_dpi"
            )
            if actual != expected:
                failures.append(f"DPI {dpi}, rule {rule}: {actual}, expected {expected}")
    assert not failures, "\n".join(failures)
    print("Export-plan recommendation and DPI boundary checks passed.")


if __name__ == "__main__":
    main()
