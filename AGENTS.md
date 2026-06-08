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

## Skill & plugin automation

Goal: reach for the right skill or plugin automatically, ask before pulling in
more, and stay light so the session never stalls. This is a Quarto math blog, so
default to a small, focused set — most finance/support/ops plugins are
irrelevant here.

### Invoke automatically (no need to ask)

- `intuition-first-explainer` — drafting, rewriting, or polishing any post or
  explainer. This is the house style; use it for content work by default.
- Output skills only when an export is actually requested: `docx`, `pdf`,
  `pptx`, `xlsx`.
- `theme-factory` when styling a standalone HTML/artifact deliverable.
- `schedule` / scheduled tasks for anything recurring (daily checks, publish
  reminders) — this supports the "continuously run" project goal.
- Built-in tools (Read/Edit/Write/Bash/Grep/Glob) and the `tools/blog.py` +
  `tools/check.py` commands are always preferred over heavier machinery.

### Ask first before

- Connecting or authenticating any MCP plugin (marketing, brightdata, data,
  productivity, etc.). Name which plugin and why before connecting.
- Pulling in anything outside the relevant set for a math blog. In-scope when
  needed: web search/scrape for sourcing references, an SEO audit of the live
  site, data-viz helpers. Treat finance / intercom / engineering-ops MCPs as
  out of scope unless asked.
- Any action that authenticates, sends, publishes, or spends.

### Performance guardrails (balanced budget)

- Default to the single most relevant skill per task; don't stack skills
  speculatively.
- Lazy-load deferred MCP/plugin tools via `ToolSearch` only when the task needs
  them — never pre-connect "just in case."
- Cap parallel tool-schema loads at ~3–5 per turn, and batch them in one
  `ToolSearch` call (a keyword query loads a whole toolkit) instead of
  one-tool-at-a-time round-trips.
- Don't trigger MCP servers you won't actually call; each connected server adds
  latency and context weight.
- If a task would need more than this focused set, pause and ask rather than
  fanning out across many plugins.

When unsure whether a heavier skill/plugin is worth it, prefer the lighter
built-in path and ask.
