#!/usr/bin/env python3
"""Build the paste-ready Substack body from the canonical article."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "article.md"
OUTPUT = ROOT / "substack.md"
RAW_IMAGES = (
    "https://raw.githubusercontent.com/wilfgrainger/blog/main/"
    "articles/whose-xg-is-it-anyway/images/"
)


def build() -> str:
    article = ARTICLE.read_text(encoding="utf-8")
    header = (
        "# Whose xG Is It Anyway?\n\n"
        "*The striker passed the screen. Then Mark asked about the penalties.*\n\n"
    )
    if not article.startswith(header):
        raise ValueError("Article title or subtitle changed; review the export.")
    text = article[len(header):]
    for name in (
        "01-hero",
        "02-five-green-ticks",
        "03-mcbaggio-repair",
    ):
        source = f"(images/{name}.svg)"
        if text.count(source) != 1:
            raise ValueError(f"Expected one image reference: {source}")
        text = text.replace(source, f"({RAW_IMAGES}{name}.png)")
    return text


if __name__ == "__main__":
    expected = build()
    if sys.argv[1:] == ["--check"]:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("substack.md is out of date; run build-substack.py")
        print("substack.md matches article.md")
    elif not sys.argv[1:]:
        OUTPUT.write_text(expected, encoding="utf-8")
        print(f"Wrote {OUTPUT}")
    else:
        raise SystemExit("Usage: build-substack.py [--check]")
