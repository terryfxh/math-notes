#!/usr/bin/env python3
"""Shared YAML front-matter parsing for the blog tools.

Single source of truth used by posts_status.py and worklog.py so the parsing
logic lives in one place. check.py keeps its own variant because it threads
errors through a Reporter.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - yaml is optional
    yaml = None


def front_matter(text: str) -> str | None:
    """Return the YAML block between the leading --- fences, or None."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    return match.group(1) if match else None


def fallback_parse(block: str) -> dict[str, Any]:
    """Minimal key: value parser used when PyYAML is unavailable."""
    data: dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def load_meta(path: Path) -> dict[str, Any]:
    """Parse a post's front matter into a dict (PyYAML if present, else fallback)."""
    block = front_matter(path.read_text(encoding="utf-8"))
    if not block:
        return {}
    if yaml is None:
        return fallback_parse(block)
    data = yaml.safe_load(block)
    return data if isinstance(data, dict) else {}
