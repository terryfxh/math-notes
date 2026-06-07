# AI collaboration rules

This repository is shared by humans, Codex, and Claude Code. Treat article text
as user-owned source material and keep changes narrow.

## Safety rules

- Run `git status --short` before editing.
- Do not delete, move, rename, or overwrite posts unless the user explicitly asks.
- Do not run destructive Git commands such as `git reset --hard` or checkout a
  file over local changes.
- Prefer adding small workflow files over rewriting existing prose.
- Keep `_site/` and `.quarto/` as disposable build output; keep `_freeze/`
  because it stores reproducible Quarto execution results.
- Before publishing or asking the user to publish, run `python tools/check.py`
  or at least `python tools/check.py --fast`.

## Daily commands

```bash
python tools/blog.py status
python tools/blog.py new "My Post Title" --categories "pure, number-theory"
python tools/blog.py fast-check
python tools/blog.py render
```

Use `python tools/blog.py full-check` before a real publish when code cells were
changed.
