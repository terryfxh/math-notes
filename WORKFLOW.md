# Math & Technical Notes Blog — Complete Workflow

A start-to-finish process for launching, publishing, and sustaining an English-language blog showcasing your pure & applied mathematics work. Built on **Quarto** (static site generator) + **Git** + **GitHub Pages**.

---

## 0. Why this stack

| Need | Quarto delivers |
|---|---|
| LaTeX math | Native `$...$` / `$$...$$` via MathJax/KaTeX, no setup |
| Theorems, proofs, lemmas | `.theorem`/`.proof` callout environments with auto-numbering |
| Citations / bibliography | BibTeX (`references.bib`) + auto-formatted reference list |
| Executable code | Embed & run Python/R/Julia, show output and figures inline |
| Cross-references | `@eq-...`, `@thm-...`, `@fig-...` auto-numbered links |
| Cost | Free hosting on GitHub Pages or Netlify |
| Portability | Plain `.qmd` (Markdown) files in Git — you own everything |

Output is a fast static site. No database, no server to maintain.

---

## Phase 1 — Positioning & identity (Day 1, ~2 hrs)

Decide these before writing a line of code. They shape every later choice.

1. **Audience.** Who reads this? (Graduate peers, recruiters/grad-admissions, your future self, the general math-curious.) You picked English-first → optimize for an international/academic audience and citability.
2. **Scope & pillars.** Pick 3–4 recurring categories so the blog reads as coherent, not random. Suggested for pure + applied math:
   - *Pure*: analysis, algebra, topology, number theory
   - *Applied*: numerical methods, optimization, probability/statistics, PDEs
   - *Meta*: paper reviews, study notes, problem sets / solutions
3. **The promise.** One sentence describing what a reader reliably gets. E.g. *"Self-contained notes that derive results from first principles, with runnable code where it helps intuition."*
4. **Cadence.** Be honest. One solid post every 2 weeks beats five then silence. Set a sustainable rhythm now.
5. **Name & domain.** Short, memorable, ideally your name or a math handle. Reserve the matching GitHub repo and (optionally) a `.com`/`.dev`/`.xyz` domain.

Deliverable: a half-page note (audience, pillars, promise, cadence, name).

---

## Phase 2 — Build the site skeleton (Day 1–2)

This repo already contains the scaffold. Steps:

1. Install Quarto (see `README.md`) and a recent Python (for code cells).
2. `quarto preview` to see it live with hot reload.
3. Edit `_quarto.yml`: set title, your name, social links, repo URL.
4. Personalize `about.qmd` (bio, research interests, CV link, contact).
5. Replace the sample posts in `posts/` once you understand the pattern.
6. Tune look in `styles.css` (or swap the Bootstrap theme in `_quarto.yml`).

Definition of done: site builds clean, homepage lists posts, About reads as you.

---

## Phase 3 — Establish the writing pipeline (repeatable per post)

A consistent pipeline is what makes a blog survive past post #3.

1. **Capture.** Keep a running `ideas.md` of post seeds (a theorem you re-derived, a paper you read, a problem you solved). Never start from a blank page.
2. **Draft in a branch.** `git checkout -b post/spectral-theorem`. New folder `posts/<slug>/index.qmd`.
3. **Front matter.** Title, `date`, `categories`, `description`, `draft: true` until ready.
4. **Write math-first.** State the result, then build to it. Use theorem/proof callouts. Define notation once. Add a figure or runnable snippet only where it earns its place.
5. **Cite.** Add sources to `references.bib`, reference with `[@key]`.
6. **Self-review checklist** (see Phase 6).
7. **Render & proof locally.** Check every equation renders, every cross-ref resolves, code runs top-to-bottom in a clean kernel.
8. **Flip `draft: false`, merge, push.** CI (or `quarto publish`) deploys.

Target: idea → published in 2–4 focused sessions per post.

---

## Phase 4 — Publish & distribute (per launch + ongoing)

1. **Deploy.** GitHub Pages via `quarto publish gh-pages`, or connect the repo to Netlify for auto-deploy on push. (Full commands in `README.md`.)
2. **Custom domain** (optional but worth it for credibility): point a CNAME at GitHub Pages / Netlify.
3. **SEO baseline.** Each post needs a `description`, descriptive title, and `image` for social cards. Quarto generates sitemap + Open Graph tags when `site-url` is set.
4. **Make it citable.** Add a "How to cite" block to substantial posts; consider archiving milestone notes to Zenodo for a DOI.
5. **Share intentionally.** Post to the venues your audience actually reads: relevant subreddits (r/math, r/mathematics), Mathstodon, Hacker News for applied/CS-adjacent pieces, your university/department channels, LinkedIn for the recruiter audience. Don't spam — share the ones genuinely worth others' time.
6. **RSS.** Quarto emits a feed automatically; mention it so regular readers can subscribe.

---

## Phase 5 — Grow & sustain (ongoing)

- **Content calendar.** Keep `ideas.md` ranked; schedule the next 2–3 posts.
- **Series.** Group related notes (e.g. a "Functional Analysis notes" series) — series convert one-time readers into followers.
- **Engagement.** Enable comments (giscus = GitHub Discussions, spam-free and fits the audience).
- **Analytics.** Add privacy-friendly analytics (Plausible, or GoatCounter free) to learn what resonates. Avoid vanity-metric chasing.
- **Refactor old posts.** Fix errors readers flag; mathematics blogs gain authority from being correct and maintained.
- **Review cadence quarterly.** What got traction? What drained time for no return? Adjust pillars.

---

## Phase 6 — Quality bar (the self-review checklist)

Run this before every publish. Correctness is the whole reputation of a math blog.

- [ ] Every claim is either proved, cited, or explicitly flagged as conjecture/intuition.
- [ ] Notation is defined before use; consistent throughout.
- [ ] All equations render; numbered ones are referenced.
- [ ] Proofs have no silent gaps ("clearly", "obviously" earn scrutiny).
- [ ] Code runs end-to-end in a fresh kernel and outputs match the prose.
- [ ] `description` + title are accurate and search-friendly.
- [ ] Links and citations resolve.
- [ ] A non-expert can follow the motivation, even if not every step.

---

## Suggested timeline

| When | Milestone |
|---|---|
| Day 1 | Phase 1 positioning + repo/domain reserved |
| Day 2 | Site builds locally, About done, deployed to a live URL |
| Week 1 | First real post published (start with something you already know cold) |
| Weeks 2–8 | Establish cadence: 1 post / 1–2 weeks; refine template |
| Quarter 1 | 5–8 posts, comments + analytics live, 1 series started |

Start small and real. Your first post should be something you can already explain without notes — that gets you to "published" fastest and builds momentum.
