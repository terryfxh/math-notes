# Writing & publishing workflow (optimized)

This replaces the old "edit, then run `quarto publish gh-pages` by hand" loop.
The big change: **publishing is now just `git push`.** A GitHub Action renders the
site on a clean machine and deploys it for you.

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
python tools/new_post.py "Your Post Title"     # 1. scaffold
quarto preview                                  # 2. write, see it live (drafts hidden)
#    ...set draft: false when ready...
python tools/check.py                           # 3. clean + validate + run code
git add . && git commit -m "add post: ..." && git push   # 4. publish
```

That is the whole flow. Step 4 triggers the Action; the live site updates in a
minute or two. You no longer touch `quarto publish`, the `gh-pages` branch, or the
directory-and-remote dance that used to cause errors.

### What each step does

- **`new_post.py`** writes `posts/<slug>/index.qmd` with the front matter, an
  epigraph block, starter sections, and a filled-in "How to cite". It starts as a
  draft, so it stays off the live listing until you flip `draft: false`.
- **`quarto preview`** is the only step that still needs Quarto + Python installed
  locally. It is optional but recommended for seeing math and code render.
- **`check.py`** is the safety net (details below). Run it before every commit.
- **`git push`** is the publish button.

## The pre-publish check: `python tools/check.py`

One command that does three things, in order:

1. **Strips NUL bytes** from `.qmd` / `.yml` / `.bib` / `.md`. OneDrive sometimes
   appends these during sync, and they are what kept breaking Quarto's YAML parser.
   This makes that whole class of failure self-healing.
2. **Validates YAML** front matter for every post and the site config.
3. **Runs every Python code cell** so a broken snippet is caught in seconds, not
   after a slow CI deploy.

Exit code `0` means safe to push. Add `--no-run` to skip executing code for a
faster check. (Optional one-time `pip install pyyaml` enables the deep YAML check;
without it, NUL-cleaning and code-running still work.)

## The publishing checklist

- [ ] New post created with `tools/new_post.py` (correct slug, today's date).
- [ ] Opens with an epigraph from `quotes.md` (verified, attributed).
- [ ] Intuition/picture comes before the formal statement.
- [ ] Every claim is proved, cited, or flagged as intuition.
- [ ] Math renders and any code cell runs top to bottom in a clean kernel.
- [ ] Prose minimizes dashes; voice matches the existing posts.
- [ ] `description` is one accurate, search-friendly sentence.
- [ ] `draft: false` set.
- [ ] `python tools/check.py` passes.
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
  README, WORKFLOW, TODO, quotes, ideas, content-plan, and this file are never
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
| Ad-hoc validation | One `check.py` gate |
