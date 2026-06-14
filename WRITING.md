# Writing & publishing workflow (optimized)

This replaces the old "edit, then run `quarto publish gh-pages` by hand" loop.
The big change: **publishing is now just `git push`.** A GitHub Action renders the
site on a clean machine and deploys it for you.

## Fast daily commands

```
python tools/blog.py status
python tools/blog.py new "Your Post Title" --categories "pure, number-theory"
python tools/blog.py preview
python tools/blog.py fast-check
python tools/blog.py full-check
python tools/blog.py render
```

Use `fast-check` while drafting. Use `full-check` before publishing a post that
contains or changes Python code cells.

## One-time setup (do this once)

1. Commit the new tooling (the Action, the scripts, this guide):

   ```
   python tools/check.py
   git add .
   git commit -m "add CI deploy, check + new-post scripts"
   git push
   ```

2. On GitHub, open **Settings → Actions → General → Workflow permissions** and make
   sure **Read and write permissions** is enabled (so the Action can push to
   `gh-pages`). Settings → Pages should still point at the `gh-pages` branch.

3. Watch the **Actions** tab after the push: the first run renders and deploys.
   From now on you can stop running `quarto publish` locally.

## Writing a new post (the everyday loop)

```
python tools/blog.py new "Your Post Title"      # 1. scaffold
python tools/blog.py draft-preview <slug>        # 2. write and preview privately
python tools/blog.py promote <slug>              # 3. move the finished article to posts/
python tools/blog.py fast-check                  # 4. quick clean + validate
python tools/blog.py full-check                  # 4b. before publishing code-heavy posts
git add . && git commit -m "add post: ..." && git push   # 5. publish
```

That is the whole flow. Step 4 triggers the Action; the live site updates in a
minute or two. You no longer touch `quarto publish`, the `gh-pages` branch, or the
directory-and-remote dance that used to cause errors.

### What each step does

- **`new_post.py`** writes `drafts/<section>/<slug>/index.qmd` with the front
  matter, an epigraph block, starter sections, and a filled-in "How to cite".
- **`blog.py promote`** moves a finished draft into `posts/` and changes
  `draft: true` to `draft: false`. It does not commit, push, or deploy.
- **`quarto preview`** is the only step that still needs Quarto + Python installed
  locally. It is optional but recommended for seeing math and code render.
- **`blog.py`** is the command hub. It wraps post creation, status, checks,
  preview, and render so Codex, Claude Code, and you can use the same entrypoint.
- **`check.py`** is the safety net (details below). Run a fast check before every
  commit and a full check before publishing code-heavy posts.
- **`git push`** is the publish button.

## The pre-publish check

Fast mode:

```
python tools/blog.py fast-check
```

Full mode:

```
python tools/blog.py full-check
```

The check does these things:

1. **Strips NUL bytes** from `.qmd` / `.yml` / `.bib` / `.md`. OneDrive sometimes
   appends these during sync, and they are what kept breaking Quarto's YAML parser.
   This makes that whole class of failure self-healing.
2. **Validates YAML** front matter for every post and the site config.
3. **Checks post metadata**, local links, and bibliography citations.
4. **Runs every Python code cell** in full mode so a broken snippet is caught
   locally, not after a slow CI deploy.

Exit code `0` means safe to push. `python tools/check.py --fast` and
`python tools/check.py --no-run` skip executing code cells for speed. If full
mode reports missing Python packages, run `pip install -r requirements.txt`.

## The publishing checklist

- [ ] New post created with `tools/new_post.py` (correct slug, today's date).
- [ ] Opens with an epigraph from `quotes.md` (verified, attributed).
- [ ] Intuition/picture comes before the formal statement.
- [ ] Every claim is proved, cited, or flagged as intuition.
- [ ] Math renders and any code cell runs top to bottom in a clean kernel.
- [ ] Prose minimizes dashes; voice matches the existing posts.
- [ ] `description` is one accurate, search-friendly sentence.
- [ ] `draft: false` set.
- [ ] `python tools/blog.py fast-check` passes.
- [ ] `python tools/blog.py full-check` passes if the post has code cells.
- [ ] `git push` done; the Actions tab shows a green deploy.

## Known gotchas (so they never recur)

- **OneDrive + NUL bytes.** Root cause of most past failures. `check.py` cleans them
  automatically. For maximum safety you could keep the working copy outside the
  OneDrive-synced tree, but the check script makes that optional.
- **YAML colons in values.** A value like `mailto: x@y.com` needs quoting:
  `href: "mailto:x@y.com"`. Front-matter validation in `check.py` catches this.
- **`styles.css` under `theme:`** must begin with the line `/*-- scss:rules --*/`,
  or Quarto rejects it as a theme layer.
- **Helper docs stay private.** `_quarto.yml` only renders `*.qmd` and `posts/`, so
  README, WORKFLOW, quotes, ideas, content-plan, and this file are never
  published as pages. Keep that allowlist intact when editing config.
- **Windows shell.** Run commands one per line. Do not wrap URLs in `< >`, and avoid
  chaining with `&&` if a step might fail; `<` and `>` are redirection operators.

## Why this is faster and simpler than before

| Old | New |
|---|---|
| Manual `quarto publish gh-pages` each time | `git push`; CI renders and deploys |
| Local Quarto+Python required to publish | Only needed for optional preview |
| Directory / remote / identity errors | Removed; CI builds from a clean checkout |
| YAML breakage from OneDrive NULs | Auto-healed by `check.py` |
| Copy-paste boilerplate per post | `new_post.py` scaffolds it |
| Ad-hoc validation | `blog.py fast-check` and `blog.py full-check` |
| Codex / Claude context hunting | `AGENTS.md`, `CLAUDE.md`, and `blog.py status` |
