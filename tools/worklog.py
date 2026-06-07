#!/usr/bin/env python3
"""Keep WORKLOG.md in sync with the published posts.

Run after publishing (``python tools/blog.py worklog``). The script is idempotent:

* It regenerates the "Status snapshot" table between the
  ``<!-- AUTO:STATUS:START -->`` / ``<!-- AUTO:STATUS:END -->`` markers from the
  YAML front matter of every ``posts/*/index.qmd`` with ``draft: false``.
* It appends one Changelog entry between the ``<!-- AUTO:LOG:START -->`` /
  ``<!-- AUTO:LOG:END -->`` markers for every newly published post it has not logged
  before (newest on top). Already-logged slugs are left untouched, so re-running is safe.

Exit status is 0 on success, 1 if WORKLOG.md or its markers are missing.
"""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WORKLOG = ROOT / "WORKLOG.md"

STATUS_START = "<!-- AUTO:STATUS:START -->"
STATUS_END = "<!-- AUTO:STATUS:END -->"
LOG_START = "<!-- AUTO:LOG:START -->"
LOG_END = "<!-- AUTO:LOG:END -->"

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - yaml is optional
    yaml = None


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


def fmt_categories(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return "" if value is None else str(value)


def fmt_date(value: Any) -> str:
    if isinstance(value, (_dt.date, _dt.datetime)):
        return value.isoformat()[:10]
    return str(value or "")


def is_published(meta: dict[str, Any]) -> bool:
    draft = meta.get("draft", False)
    if isinstance(draft, str):
        return draft.strip().lower() not in {"true", "yes", "1"}
    return not bool(draft)


def collect_posts() -> list[dict[str, str]]:
    posts: list[dict[str, str]] = []
    for path in sorted((ROOT / "posts").glob("*/index.qmd")):
        meta = load_meta(path)
        if not meta or not is_published(meta):
            continue
        posts.append(
            {
                "slug": path.parent.name,
                "title": str(meta.get("title") or path.parent.name),
                "date": fmt_date(meta.get("date")),
                "categories": fmt_categories(meta.get("categories")),
            }
        )
    posts.sort(key=lambda p: (p["date"], p["slug"]))
    return posts


def build_status(posts: list[dict[str, str]]) -> str:
    today = _dt.date.today().isoformat()
    lines = [
        f"_Last updated {today} — {len(posts)} published posts._",
        "",
        "| Date | Slug | Title | Categories |",
        "|---|---|---|---|",
    ]
    for p in posts:
        title = p["title"].replace("|", "\\|")
        lines.append(f"| {p['date']} | `{p['slug']}` | {title} | {p['categories']} |")
    return "\n".join(lines)


def replace_block(text: str, start: str, end: str, body: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    return pattern.sub(f"{start}\n{body}\n{end}", text, count=1)


def logged_slugs(text: str) -> set[str]:
    match = re.search(re.escape(LOG_START) + r"(.*?)" + re.escape(LOG_END), text, re.S)
    if not match:
        return set()
    return set(re.findall(r"`([^`]+)`", match.group(1)))


def existing_log_body(text: str) -> str:
    match = re.search(re.escape(LOG_START) + r"(.*?)" + re.escape(LOG_END), text, re.S)
    return match.group(1).strip("\n") if match else ""


def main() -> int:
    if not WORKLOG.exists():
        print(f"error: {WORKLOG} not found", flush=True)
        return 1
    text = WORKLOG.read_text(encoding="utf-8")
    for marker in (STATUS_START, STATUS_END, LOG_START, LOG_END):
        if marker not in text:
            print(f"error: marker {marker} missing from WORKLOG.md", flush=True)
            return 1

    posts = collect_posts()

    # Status table: always regenerated.
    text = replace_block(text, STATUS_START, STATUS_END, build_status(posts))

    # Changelog: append entries only for slugs not seen before.
    known = logged_slugs(text)
    new_posts = [p for p in posts if p["slug"] not in known]
    if new_posts:
        new_lines = [
            f"- **{p['date']}** — published `{p['slug']}`: {p['title']}"
            f"{' (' + p['categories'] + ')' if p['categories'] else ''}"
            for p in sorted(new_posts, key=lambda p: (p["date"], p["slug"]), reverse=True)
        ]
        body = "\n".join(new_lines)
        prior = existing_log_body(text)
        if prior:
            body = body + "\n" + prior
        text = replace_block(text, LOG_START, LOG_END, body)

    WORKLOG.write_text(text, encoding="utf-8")
    if new_posts:
        print(f"worklog: added {len(new_posts)} changelog entr"
              f"{'y' if len(new_posts) == 1 else 'ies'}; status table refreshed "
              f"({len(posts)} posts).")
    else:
        print(f"worklog: status table refreshed ({len(posts)} posts); no new entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
