#!/usr/bin/env python3
"""
Pre-publish health check for the blog.

Run this before every commit. It does three jobs, in order:

  1. Strips stray NUL bytes from .qmd / .yml / .bib / .md files. OneDrive
     occasionally appends these during sync and they break Quarto's YAML parser.
  2. Validates the YAML front matter of every post and the site config.
  3. Executes every Python code cell so a broken snippet is caught here, not
     after a five-minute CI deploy.

Usage:
    python tools/check.py            # clean + validate + run code
    python tools/check.py --no-run   # skip executing code cells (faster)

Exit code 0 means "safe to commit and push"; non-zero means something failed.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUN_CODE = "--no-run" not in sys.argv

try:
    import yaml
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

errors: list[str] = []
notes: list[str] = []


def strip_nuls() -> None:
    for ext in ("*.qmd", "*.yml", "*.yaml", "*.bib", "*.md"):
        for f in ROOT.rglob(ext):
            if "_site" in f.parts or ".quarto" in f.parts or ".git" in f.parts:
                continue
            raw = f.read_bytes()
            if b"\x00" in raw:
                cleaned = raw.replace(b"\x00", b"")
                if not cleaned.endswith(b"\n"):
                    cleaned += b"\n"
                f.write_bytes(cleaned)
                notes.append(f"stripped NUL bytes from {f.relative_to(ROOT)}")


def validate_yaml() -> None:
    if not HAVE_YAML:
        notes.append("PyYAML not installed; skipped deep YAML validation "
                     "(run: pip install pyyaml). NUL cleaning still ran.")
        return
    for cfg in ("_quarto.yml", "posts/_metadata.yml"):
        p = ROOT / cfg
        if p.exists():
            try:
                yaml.safe_load(p.read_text(encoding="utf-8"))
            except Exception as e:
                errors.append(f"{cfg}: {e}")
    for qmd in ROOT.rglob("*.qmd"):
        if "_site" in qmd.parts:
            continue
        text = qmd.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not m:
            errors.append(f"{qmd.relative_to(ROOT)}: missing front matter")
            continue
        try:
            yaml.safe_load(m.group(1))
        except Exception as e:
            errors.append(f"{qmd.relative_to(ROOT)} front matter: {e}")


def run_code() -> None:
    if not RUN_CODE:
        return
    for qmd in sorted(ROOT.rglob("posts/**/*.qmd")):
        text = qmd.read_text(encoding="utf-8")
        cells = re.findall(r"```\{python\}\n(.*?)\n```", text, re.S)
        ns: dict = {}
        for i, code in enumerate(cells, 1):
            try:
                exec(compile(code, f"{qmd.name}#cell{i}", "exec"), ns)
            except Exception as e:
                errors.append(f"{qmd.relative_to(ROOT)} code cell {i}: "
                              f"{type(e).__name__}: {e}")


def main() -> int:
    strip_nuls()
    validate_yaml()
    run_code()

    for n in notes:
        print(f"  note: {n}")
    if errors:
        print("\nFAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nAll checks passed. Safe to commit and push.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
