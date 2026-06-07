#!/usr/bin/env python3
"""Print a compact Markdown table describing all Quarto posts."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _frontmatter import load_meta

ROOT = Path(__file__).resolve().parent.parent


def fmt(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return "" if value is None else str(value)


def main() -> int:
    posts = sorted((ROOT / "posts").glob("*/index.qmd"))
    print("| Post | Date | Draft | Categories | Description |")
    print("|---|---:|---:|---|---|")
    for path in posts:
        meta = load_meta(path)
        title = fmt(meta.get("title")) or path.parent.name
        desc = fmt(meta.get("description"))
        desc_state = "ok" if desc and not desc.startswith("One sentence") else "missing"
        print(
            f"| {title} | {fmt(meta.get('date'))} | {fmt(meta.get('draft'))} | "
            f"{fmt(meta.get('categories'))} | {desc_state} |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
