#!/usr/bin/env python3
"""Run the user's LaTeX Workshop latexmk recipe for a root .tex file."""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from pathlib import Path


RECIPES = {
    "uplatex": [
        "latexmk",
        "-pdfdvi",
        "-e",
        "$latex='uplatex %O %S'; $bibtex='upbibtex %O %B'; $dvipdf='dvipdfmx %O -o %D %S'",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
    ],
    "lualatex": [
        "latexmk",
        "-lualatex",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
    ],
    "pdflatex": [
        "latexmk",
        "-pdf",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
    ],
}

RECIPE_RE = re.compile(r"^\s*%\s*!LW\s+recipe\s*=\s*([A-Za-z0-9_-]+)\s*$")


def read_magic_recipe(tex_file: Path) -> str | None:
    with tex_file.open("r", encoding="utf-8") as file:
        for index, line in enumerate(file):
            if index >= 40:
                break
            match = RECIPE_RE.match(line)
            if match:
                return match.group(1)
    return None


def build_command(tex_file: Path, recipe: str) -> list[str]:
    if recipe not in RECIPES:
        known = ", ".join(sorted(RECIPES))
        raise SystemExit(f"Unknown recipe '{recipe}'. Expected one of: {known}")

    return [*RECIPES[recipe], "-outdir=build", tex_file.name]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a LaTeX Workshop-equivalent latexmk recipe."
    )
    parser.add_argument("tex_file", type=Path, help="Root .tex file to compile")
    parser.add_argument(
        "--recipe",
        choices=sorted(RECIPES),
        help="Override the file's % !LW recipe=... selector",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved command without running latexmk",
    )
    args = parser.parse_args()

    tex_file = args.tex_file.expanduser().resolve()
    if not tex_file.exists():
        raise SystemExit(f"File not found: {tex_file}")
    if tex_file.suffix.lower() != ".tex":
        raise SystemExit(f"Expected a .tex file: {tex_file}")

    recipe = args.recipe or read_magic_recipe(tex_file)
    if recipe is None:
        raise SystemExit(
            "No % !LW recipe=... selector found. Add one or pass --recipe."
        )

    command = build_command(tex_file, recipe)
    print("Recipe:", recipe)
    print("Command:", shlex.join(command))
    if args.dry_run:
        return 0

    (tex_file.parent / "build").mkdir(exist_ok=True)
    return subprocess.run(command, cwd=tex_file.parent).returncode


if __name__ == "__main__":
    sys.exit(main())
