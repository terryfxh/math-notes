#!/usr/bin/env python3
"""
Scaffold a new post so you never copy-paste boilerplate again.

Usage:
    python tools/new_post.py "The Title of My Post"
    python tools/new_post.py "My Post" --section mathematics --categories "pure, number-theory"

It creates drafts/<section>/<slug>/index.qmd with the front matter, an epigraph block
(ready for a quote from quotes.md), starter sections, and a filled-in
"How to cite" line, then prints the next steps.
"""
from __future__ import annotations
import re
import sys
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_BASE = "https://terryfxh.github.io/math-notes"


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "untitled"


def main() -> int:
    args = [a for a in sys.argv[1:]]
    categories = "pure"
    section = "mathematics"
    if "--categories" in args:
        i = args.index("--categories")
        categories = args[i + 1]
        del args[i:i + 2]
    if "--section" in args:
        i = args.index("--section")
        section = args[i + 1].strip().lower()
        del args[i:i + 2]
    if not args:
        print(
            'Usage: python tools/new_post.py "The Title" '
            '[--section mathematics|reflections|research-notes] [--categories "a, b"]'
        )
        return 1
    allowed_sections = {"mathematics", "reflections", "research-notes"}
    if section not in allowed_sections:
        print(f"Unknown draft section '{section}'. Choose: {', '.join(sorted(allowed_sections))}")
        return 1

    title = " ".join(args)
    slug = slugify(title)
    today = datetime.date.today().isoformat()
    folder = ROOT / "drafts" / section / slug
    target = folder / "index.qmd"
    existing = [
        ROOT / "posts" / slug / "index.qmd",
        *(ROOT / "drafts").glob(f"*/{slug}/index.qmd"),
    ]
    if any(path.exists() for path in existing):
        print(f"Refusing to create duplicate article slug '{slug}'")
        return 1
    folder.mkdir(parents=True, exist_ok=True)

    cats = ", ".join(c.strip() for c in categories.split(","))
    template = f'''---
title: "{title}"
description: "One sentence that says what a reader gets from this post."
date: {today}
categories: [{cats}]
bibliography: ../../../references.bib
draft: true
---

::: {{.epigraph}}
"Pick a fitting quote from quotes.md."

[— Author, *Work*]{{.attribution}}
:::

Open with the intuition. State the result in plain words and promise the picture
before the proof.

## First, the picture

The geometric or visual heart of the idea, before any formalism.

## The result

State it precisely once the intuition is in place.

## A check

```{{python}}
# A small runnable demonstration, if it sharpens the idea.
print("hello")
```

## What to remember

The one or two sentences you want the reader to keep.

## How to cite

> Terry (2026). *{title}*. Retrieved from `{SITE_BASE}/posts/{slug}/`.
'''
    target.write_text(template, encoding="utf-8")
    print(f"Created drafts/{section}/{slug}/index.qmd")
    print("Next:")
    print("  1. Write it; pick an epigraph from quotes.md.")
    print(f"  2. python tools/blog.py draft-preview {slug}")
    print(f"  3. python tools/blog.py promote {slug}")
    print("  4. python tools/blog.py fast-check")
    print("     python tools/blog.py full-check   # before publishing code-heavy posts")
    print("  5. git add . && git commit -m \"add post: {0}\" && git push".format(slug))
    print("     ...the GitHub Action renders and deploys automatically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
