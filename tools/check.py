#!/usr/bin/env python3
"""
Pre-publish health check for the Quarto blog.

Default mode is the full local check:
    python tools/check.py

Fast mode is intended for quick local use and CI before deploy:
    python tools/check.py --fast

The check intentionally avoids deleting, moving, or rewriting posts. The only
write it may perform is removing stray NUL bytes from text files, which protects
Quarto's YAML parser from OneDrive sync corruption.

Performance: every post is read from disk exactly once and the text is reused by
all validators (front matter, citations, links, code, freeze).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, NamedTuple

ROOT = Path(__file__).resolve().parent.parent
TEXT_GLOBS = ("*.qmd", "*.yml", "*.yaml", "*.bib", "*.md")
SKIP_PARTS = {".git", ".quarto", "_site", "_freeze", "__pycache__", ".venv"}
REQUIRED_POST_FIELDS = ("title", "description", "date", "categories", "draft")

try:
    import yaml  # type: ignore

    HAVE_YAML = True
except ImportError:
    yaml = None
    HAVE_YAML = False


class Post(NamedTuple):
    path: Path
    text: str


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []
        self._seen_notes: set[str] = set()

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        if msg in self._seen_notes:
            return
        self._seen_notes.add(msg)
        self.notes.append(msg)

    def finish(self) -> int:
        for note in self.notes:
            print(f"note: {note}")
        for warning in self.warnings:
            print(f"warning: {warning}")
        if self.errors:
            print("\nFAILED:")
            for error in self.errors:
                print(f"  - {error}")
            return 1
        print("\nAll checks passed. Safe to commit and push.")
        return 0


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    return bool(SKIP_PARTS.intersection(path.parts))


def text_files() -> list[Path]:
    found: list[Path] = []
    for pattern in TEXT_GLOBS:
        found.extend(p for p in ROOT.rglob(pattern) if not should_skip(p))
    return sorted(set(found))


def strip_nuls(reporter: Reporter) -> None:
    for path in text_files():
        raw = path.read_bytes()
        if b"\x00" not in raw:
            continue
        cleaned = raw.replace(b"\x00", b"")
        if not cleaned.endswith(b"\n"):
            cleaned += b"\n"
        path.write_bytes(cleaned)
        reporter.note(f"stripped NUL bytes from {rel(path)}")


def load_posts() -> list[Post]:
    """Read every published post and private draft exactly once."""
    posts: list[Post] = []
    paths = [
        *(ROOT / "posts").glob("*/index.qmd"),
        *(ROOT / "drafts").glob("*/*/index.qmd"),
    ]
    for path in sorted(p for p in paths if p.is_file()):
        posts.append(Post(path, path.read_text(encoding="utf-8")))
    return posts


def front_matter(text: str) -> str | None:
    match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    return match.group(1) if match else None


def fallback_yaml(block: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            continue
        if value.lower() == "true":
            data[key] = True
        elif value.lower() == "false":
            data[key] = False
        elif value.startswith("[") and value.endswith("]"):
            items = value[1:-1].strip()
            data[key] = [item.strip().strip("\"'") for item in items.split(",") if item.strip()]
        else:
            data[key] = value.strip("\"'")
    return data


def load_yaml_block(block: str, source: str, reporter: Reporter) -> dict[str, Any] | None:
    if not HAVE_YAML:
        reporter.note(
            "PyYAML is not installed; using lightweight front matter checks "
            "(pip install pyyaml for deep YAML validation)."
        )
        return fallback_yaml(block)
    try:
        data = yaml.safe_load(block)  # type: ignore[union-attr]
    except Exception as exc:
        reporter.error(f"{source}: YAML parse error: {exc}")
        return None
    if data is None:
        return {}
    if not isinstance(data, dict):
        reporter.error(f"{source}: YAML front matter must be a mapping")
        return None
    return data


def validate_project_yaml(reporter: Reporter) -> None:
    for name in ("_quarto.yml", "posts/_metadata.yml"):
        path = ROOT / name
        if not path.exists():
            reporter.error(f"{name}: missing")
            continue
        if HAVE_YAML:
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))  # type: ignore[union-attr]
            except Exception as exc:
                reporter.error(f"{name}: YAML parse error: {exc}")


def validate_posts(posts: list[Post], reporter: Reporter) -> None:
    for path, text in posts:
        block = front_matter(text)
        if block is None:
            reporter.error(f"{rel(path)}: missing front matter")
            continue
        data = load_yaml_block(block, f"{rel(path)} front matter", reporter)
        if data is None:
            continue
        for field in REQUIRED_POST_FIELDS:
            if field not in data:
                reporter.error(f"{rel(path)}: missing required field '{field}'")
        description = str(data.get("description", "")).strip()
        if not description or description.startswith("One sentence"):
            reporter.error(f"{rel(path)}: description is empty or still the template placeholder")
        categories = data.get("categories")
        if not isinstance(categories, list) or not categories:
            reporter.error(f"{rel(path)}: categories should be a non-empty YAML list")
        if not isinstance(data.get("draft"), bool):
            reporter.error(f"{rel(path)}: draft should be true or false")
        if "drafts" in path.parts and data.get("draft") is not True:
            reporter.error(f"{rel(path)}: files under drafts/ must use draft: true")
        if "posts" in path.parts and data.get("draft") is not False:
            reporter.error(f"{rel(path)}: files under posts/ must use draft: false")
        if "::: {.epigraph}" not in text and "::: {.epigraph " not in text:
            reporter.warn(f"{rel(path)}: no epigraph block found")
        if "## How to cite" not in text and "## 如何引用" not in text:
            reporter.warn(f"{rel(path)}: no 'How to cite' section found")


def bibliography_keys() -> set[str]:
    bib = ROOT / "references.bib"
    if not bib.exists():
        return set()
    text = bib.read_text(encoding="utf-8")
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", text))


def validate_citations(posts: list[Post], reporter: Reporter) -> None:
    keys = bibliography_keys()
    if not keys:
        return
    citation_re = re.compile(r"\[@([A-Za-z0-9_:\-]+)")
    for path, text in posts:
        for key in citation_re.findall(text):
            if key not in keys:
                reporter.error(f"{rel(path)}: citation [@{key}] is missing from references.bib")


def validate_local_links(posts: list[Post], reporter: Reporter) -> None:
    link_re = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
    extra = [
        Post(p, p.read_text(encoding="utf-8"))
        for p in (ROOT / "README.md", ROOT / "WRITING.md")
        if p.exists()
    ]
    for path, text in [*extra, *posts]:
        for raw_target in link_re.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            target = target.strip("<>")
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                reporter.warn(f"{rel(path)}: local link points outside repo: {raw_target}")
                continue
            if not candidate.exists():
                reporter.error(f"{rel(path)}: broken local link: {raw_target}")


def python_cells(text: str) -> list[str]:
    return re.findall(r"```\{python\}\r?\n(.*?)\r?\n```", text, re.S)


def validate_freeze(posts: list[Post], reporter: Reporter) -> None:
    """Guard against publishing stale or uncached code output.

    With `freeze: auto`, only posts whose source changed are re-executed, and the
    committed _freeze/ output is reused. A code-bearing post with no committed
    freeze is re-executed on every CI build; one whose source is newer than its
    freeze would publish output that no longer matches the prose. The mtime
    comparison is meaningful only locally (a fresh CI checkout rewrites mtimes),
    so it is skipped under CI.
    """
    freeze_root = ROOT / "_freeze" / "posts"
    in_ci = bool(os.environ.get("CI"))
    for path, text in posts:
        if "drafts" in path.parts:
            continue
        if not python_cells(text):
            continue
        slug = path.parent.name
        fdir = freeze_root / slug
        if not fdir.exists():
            reporter.warn(
                f"{rel(path)}: has runnable code but no committed _freeze/posts/{slug}; "
                f"CI re-executes it every build. Run `python tools/blog.py render --execute` "
                f"locally and commit _freeze/ to cache it."
            )
            continue
        if in_ci:
            continue
        src_mtime = path.stat().st_mtime
        freeze_mtimes = [f.stat().st_mtime for f in fdir.rglob("*") if f.is_file()]
        if freeze_mtimes and src_mtime > max(freeze_mtimes) + 1:
            reporter.warn(
                f"{rel(path)}: source is newer than its _freeze cache; re-render with "
                f"`python tools/blog.py render --execute` so the published output matches the post."
            )


def run_code_cells(posts: list[Post], reporter: Reporter) -> None:
    for path, text in posts:
        namespace: dict[str, Any] = {}
        for index, code in enumerate(python_cells(text), 1):
            try:
                exec(compile(code, f"{rel(path)}#cell{index}", "exec"), namespace)
            except Exception as exc:
                reporter.error(f"{rel(path)} code cell {index}: {type(exc).__name__}: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check the blog before publishing.")
    parser.add_argument("--fast", action="store_true", help="Skip Python code execution.")
    parser.add_argument("--no-run", action="store_true", help="Alias for --fast.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    reporter = Reporter()
    strip_nuls(reporter)
    validate_project_yaml(reporter)
    posts = load_posts()
    validate_posts(posts, reporter)
    validate_citations(posts, reporter)
    validate_local_links(posts, reporter)
    validate_freeze(posts, reporter)
    if args.fast or args.no_run:
        reporter.note("fast mode: skipped Python code cell execution")
    else:
        run_code_cells(posts, reporter)
    return reporter.finish()


if __name__ == "__main__":
    raise SystemExit(main())
