#!/usr/bin/env python3
"""Print compact Markdown tables for published posts and private drafts."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _frontmatter import load_meta

ROOT = Path(__file__).resolve().parent.parent


def fmt(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return "" if value is None else str(value)


def print_table(paths: list[Path], heading: str, include_section: bool = False) -> None:
    print(f"## {heading}")
    section_header = " | Section" if include_section else ""
    section_rule = "|---" if include_section else ""
    print(f"| Post | Date | Draft | Categories | Description{section_header} |")
    print(f"|---|---:|---:|---|---{section_rule}|")
    for path in paths:
        meta = load_meta(path)
        title = fmt(meta.get("title")) or path.parent.name
        desc = fmt(meta.get("description"))
        desc_state = "ok" if desc and not desc.startswith("One sentence") else "missing"
        section = f" | {path.parents[1].name}" if include_section else ""
        print(
            f"| {title} | {fmt(meta.get('date'))} | {fmt(meta.get('draft'))} | "
            f"{fmt(meta.get('categories'))} | {desc_state}{section} |"
        )


def main() -> int:
    posts = sorted((ROOT / "posts").glob("*/index.qmd"))
    drafts = sorted((ROOT / "drafts").glob("*/*/index.qmd"))
    print_table(posts, "Published posts")
    print()
    print_table(drafts, "Private drafts", include_section=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
