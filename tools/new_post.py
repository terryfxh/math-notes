#!/usr/bin/env python3
"""
Scaffold a new post so you never copy-paste boilerplate again.

Usage:
    python tools/new_post.py "The Title of My Post"
    python tools/new_post.py "My Post" --categories "pure, number-theory"

It creates posts/<slug>/index.qmd with the front matter, an epigraph block
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
    if "--categories" in args:
        i = args.index("--categories")
        categories = args[i + 1]
        del args[i:i + 2]
    if not args:
        print('Usage: python tools/new_post.py "The Title" [--categories "a, b"]')
        return 1

    title = " ".join(args)
    slug = slugify(title)
    today = datetime.date.today().isoformat()
    folder = ROOT / "posts" / slug
    target = folder / "index.qmd"
    if target.exists():
        print(f"Refusing to overwrite existing {target.relative_to(ROOT)}")
        return 1
    folder.mkdir(parents=True, exist_ok=True)

    cats = ", ".join(c.strip() for c in categories.split(","))
    template = f'''---
title: "{title}"
description: "One sentence that says what a reader gets from this post."
date: {today}
categories: [{cats}]
bibliography: ../../references.bib
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
    print(f"Created posts/{slug}/index.qmd  (draft)")
    print("Next:")
    print("  1. Write it; pick an epigraph from quotes.md.")
    print("  2. quarto preview            # see it locally (draft is hidden on the live site)")
    print("  3. set draft: false when ready")
    print("  4. python tools/check.py     # clean + validate + run code")
    print("  5. git add . && git commit -m \"add post: {0}\" && git push".format(slug))
    print("     ...the GitHub Action renders and deploys automatically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
