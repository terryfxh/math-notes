# Draft workspace

Everything under `drafts/` is private writing material. Quarto renders only
`posts/`, so files here cannot appear on the published site.

## Sections

- `mathematics/` — pure, applied, computational, and series-based math drafts.
- `reflections/` — learning, teaching, philosophy, and other reflective essays.
- `research-notes/` — source gathering, paper notes, and pieces that still need
  substantial verification before becoming article drafts.

Use the front-matter `categories` field for finer classification. Keep one
article per folder:

```text
drafts/<section>/<slug>/index.qmd
```

## Workflow

```bash
python tools/blog.py new "Title" --section mathematics --categories "pure, algebra"
python tools/blog.py status
python tools/blog.py draft-preview <slug>
python tools/blog.py fast-check
python tools/blog.py promote <slug>
```

`promote` moves a finished draft into `posts/` and changes `draft` to `false`.
It does not commit, push, or deploy. Run the normal pre-publish checks after
promotion.
