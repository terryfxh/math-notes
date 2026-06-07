#!/usr/bin/env python3
"""Print a compact Markdown table describing all Quarto posts."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def front_matter(text: str) -> str | None:
    match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    return match.group(1) if match else None


def fallback_parse(block: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def load_meta(path: Path) -> dict[str, Any]:
    block = front_matter(path.read_text(encoding="utf-8"))
    if not block:
        return {}
    if yaml is None:
        return fallback_parse(block)
    data = yaml.safe_load(block)
    return data if isinstance(data, dict) else {}


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
