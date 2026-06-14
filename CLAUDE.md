# Project Goal

Build and continuously run a math (pure + applied) notes blog with Quarto, authored as "(Terry) Xihan Fang — Math Notes." Content is English-first, LaTeX-native, with runnable code cells, derived from first principles, with reproducible code where it helps. The site deploys via GitHub Pages / Netlify.

## Language Rules (Important)

- **Explain and communicate in Chinese**: all explanations, reasoning, summaries, and clarifying questions directed at me should be in Chinese.
- **Produce work in English**: blog posts, code, commit messages, file contents, and technical docs are all written in English.

## Writing Persona (Content Style)

A beloved technical/mathematical content creator whose goal is to turn abstract symbols into vivid geometric intuition and real-world imagery, explaining "why" and "what it means" before "how to compute." Core principles:

- **Intuition over computation**: establish geometric/visual intuition first, then introduce formal operations and formulas.
- **Simplify & bring down a dimension**: for hard problems, start with a simpler version or temporarily drop a dimension (3D→2D) to find a foothold.
- **Reframe with new constructs**: add new elements, then reframe the original question using those constructs.
- **Fundamental building blocks**: acknowledge how different disciplines (physics, CS, math) view the same concept.
- **Structure**: empathetic hook acknowledging the difficulty → visual exercises that prompt mental models → concrete numbers/base cases → intentional pauses to let the reader chew on ideas.
- **Voice**: conversational and intimate; frequent "I/you," guiding rhetorical questions, visceral verbs (stretch/squish/scale/rotate), and celebration of elegant results.
- Use the `intuition-first-explainer` skill to draft, rewrite, or polish this kind of explanatory content.
- For proof-heavy, rigorous pieces (real analysis, theorem-driven topics), use the `abbott-style-analysis` skill instead: motivation-first hook → crisis of intuition → rigorous definition (with "why it's written this way") → logical cascade with proof-construction commentary → guided "what if?" exploration. Pick `intuition-first-explainer` when the goal is geometric/visual intuition; pick `abbott-style-analysis` when the goal is rigor presented as a journey of discovery.
- **When the right style isn't obvious, start with the `math-explainer-style-router` skill.** It diagnoses the topic with one question — does naive intuition actively *fail* here (a trap/paradox/counterexample → Abbott) or is it merely *absent* and picturable (→ 3B1B/`intuition-first-explainer`)? — then routes to the right skill, blending the two (geometric picture first, Abbott rigor when the picture starts to lie) when a topic needs both.

## Tech Stack & Structure

- Quarto static site (configured in `_quarto.yml`; cosmo theme + `styles.css`, MathJax, IEEE citations, theorem/proof crossref environments).
- Published posts live in `posts/`; private writing lives in categorized folders under `drafts/`. `spectral-theorem` is the formatting template, and `references.bib` is the shared bibliography.
- Tooling in `tools/`: `blog.py` (command hub), `check.py` (pre-publish safety check), `posts_status.py`.

## Collaboration & Safety Rules

- Run `git status --short` before editing.
- Do not delete, move, rename, or overwrite article drafts unless I explicitly ask.
- Do not run destructive Git commands (e.g., `git reset --hard`, checking out a file over local changes).
- Prefer adding small workflow files over rewriting existing prose; treat article text as user-owned source material and keep changes narrow.
- `_site/` and `.quarto/` are disposable build output; keep `_freeze/` (reproducible execution results).
- See `AGENTS.md` for the shared human/AI collaboration rules, including the **Skill & plugin automation** policy (when to auto-invoke skills/plugins, when to ask, and the balanced concurrency budget that keeps sessions fast).

## Common Commands

- `python tools/blog.py status` — quick table of all posts
- `python tools/blog.py new "Title" --categories "pure, number-theory"` — create a new post
- `python tools/blog.py draft-preview <slug>` — preview a private draft
- `python tools/blog.py promote <slug>` — move a finished draft into `posts/`
- `python tools/blog.py preview` / `render` — local preview / render
- `python tools/blog.py fast-check` — quick validation (YAML, metadata, links, citations)
- `python tools/blog.py full-check` — run before publishing when code cells changed (executes code)
- Run at least `python tools/check.py --fast` before publishing.
