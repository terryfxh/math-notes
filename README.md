# Math Notes Blog

A Quarto static-site blog for pure & applied mathematics notes. English-first,
LaTeX-native, with runnable code cells.

See [`WORKFLOW.md`](WORKFLOW.md) for the full positioning to publishing to
growth process, and [`WRITING.md`](WRITING.md) for the daily command loop.

## Project layout

```
.
├── _quarto.yml          # site config: title, navbar, theme, citation defaults
├── index.qmd            # homepage (auto-listing of posts)
├── about.qmd            # bio / research interests
├── styles.css           # custom styling
├── references.bib       # shared bibliography
├── posts/
│   ├── _metadata.yml    # defaults applied to all posts
│   ├── welcome/index.qmd
│   └── spectral-theorem/index.qmd   # formatting template (theorems, code, citations)
├── drafts/
│   ├── mathematics/     # private math drafts
│   ├── reflections/     # private reflective essays
│   └── research-notes/  # source gathering and early-stage notes
├── tools/
│   ├── blog.py          # command hub: new/status/check/render/preview
│   ├── check.py         # pre-publish safety check
│   └── posts_status.py  # post inventory table
├── AGENTS.md            # Codex / AI collaboration safety rules
├── CLAUDE.md            # Claude entrypoint: goal, language rules, persona, safety (see AGENTS.md)
├── WORKFLOW.md          # the complete plan
└── ideas.md             # running list of post ideas
```

## One-time setup

1. **Install Quarto** — download from <https://quarto.org/docs/get-started/>
   (or `brew install quarto` / `winget install Posit.Quarto`). Verify with `quarto --version`.
2. **Install Python** (3.9+) for code cells, plus the libraries posts use:
   ```bash
   pip install -r requirements.txt
   ```
3. **Personalize** `_quarto.yml` and `about.qmd`: replace every `yourusername`,
   `Your Name`, and placeholder URL/email.

## Local development

```bash
python tools/blog.py status       # quick table of all posts
python tools/blog.py preview      # live site with hot reload
python tools/blog.py render       # fast local render into _site/
python tools/blog.py fast-check   # YAML, metadata, links, citations
python tools/blog.py full-check   # also executes Python code cells
```

Only finished articles live in `posts/`. Private writing lives under `drafts/`,
which is outside Quarto's render allowlist.

## Writing a new post

```bash
python tools/blog.py new "My Post Title" --categories "pure, number-theory"
python tools/blog.py draft-preview my-post-title
python tools/blog.py promote my-post-title
python tools/blog.py preview
python tools/blog.py fast-check
```

Commit, push, open a PR (or merge), then publish.

## Deploy

### Option A — GitHub Pages (simplest)

Push to `main`. The GitHub Action runs `python tools/check.py --fast`, renders
the site, and publishes the result to `gh-pages`. The site is served from the
`site-url` configured in `_quarto.yml`.

### Option B — Netlify (auto-deploy on every push)

1. Push this repo to GitHub.
2. In Netlify: **New site from Git** → pick the repo.
3. Build command: `quarto render` · Publish directory: `_site`.
4. (Add a Netlify build plugin for Quarto, or commit `_site/` — the Quarto docs
   cover both.) Netlify rebuilds on every push to `main`.

### Custom domain (optional)

Point a `CNAME` record at GitHub Pages / Netlify and set the domain in their
dashboard. Update `site-url` accordingly.

## Comments & analytics (optional)

- **Comments:** add [giscus](https://giscus.app) (GitHub Discussions-backed) to
  `_quarto.yml` under `website: comments:`.
- **Analytics:** privacy-friendly options like Plausible or GoatCounter — add the
  script via `include-in-header` in `_quarto.yml`.
