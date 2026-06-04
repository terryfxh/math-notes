# Math Notes Blog

A Quarto static-site blog for pure & applied mathematics notes. English-first,
LaTeX-native, with runnable code cells.

See [`WORKFLOW.md`](WORKFLOW.md) for the full positioning → publishing → growth process.

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
├── WORKFLOW.md          # the complete plan
└── ideas.md             # running list of post ideas
```

## One-time setup

1. **Install Quarto** — download from <https://quarto.org/docs/get-started/>
   (or `brew install quarto` / `winget install Posit.Quarto`). Verify with `quarto --version`.
2. **Install Python** (3.9+) for code cells, plus the libraries posts use:
   ```bash
   pip install jupyter numpy matplotlib
   ```
3. **Personalize** `_quarto.yml` and `about.qmd`: replace every `yourusername`,
   `Your Name`, and placeholder URL/email.

## Local development

```bash
quarto preview      # live site with hot reload at http://localhost:port
quarto render       # build the static site into _site/
```

Posts with `draft: true` are excluded from the published listing. Flip to
`draft: false` when ready.

## Writing a new post

```bash
git checkout -b post/my-slug
cp -r posts/spectral-theorem posts/my-slug   # start from the template
# edit posts/my-slug/index.qmd, set title/date/categories
quarto preview
```

Commit, push, open a PR (or merge), then publish.

## Deploy

### Option A — GitHub Pages (simplest)

```bash
# one-time: create an empty GitHub repo and add it as origin
quarto publish gh-pages
```

This builds and pushes to a `gh-pages` branch and serves at
`https://yourusername.github.io/your-repo/`. Set `site-url` in `_quarto.yml`
to that address so sitemap and social cards generate correctly.

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
