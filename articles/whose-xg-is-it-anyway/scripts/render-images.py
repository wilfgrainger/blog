#!/usr/bin/env python3
"""Render the four editable SVGs and verify their committed PNG exports."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

IMAGES = Path(__file__).resolve().parents[1] / "images"
MANIFEST = IMAGES / "render-manifest.json"
NAMES = (
    "01-hero",
    "02-five-green-ticks",
    "03-mcbaggio-repair",
    "04-authority-ambiguity",
)
WIDTH = 1600


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_manifest() -> dict:
    return {
        name: {
            "svg_sha256": digest(IMAGES / f"{name}.svg"),
            "png_sha256": digest(IMAGES / f"{name}.png"),
        }
        for name in NAMES
    }


if __name__ == "__main__":
    if sys.argv[1:] == ["--check"]:
        expected = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if expected != current_manifest():
            raise SystemExit("Image source or export changed; rerun render-images.py and inspect the PNGs.")
        print("Four PNG exports match their recorded SVG sources")
    elif not sys.argv[1:]:
        for name in NAMES:
            subprocess.run(
                [
                    "inkscape",
                    str(IMAGES / f"{name}.svg"),
                    f"--export-filename={IMAGES / f'{name}.png'}",
                    f"--export-width={WIDTH}",
                ],
                check=True,
            )
        MANIFEST.write_text(
            json.dumps(current_manifest(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print("Rendered four PNG exports; inspect them at article and phone widths")
    else:
        raise SystemExit("Usage: render-images.py [--check]")
