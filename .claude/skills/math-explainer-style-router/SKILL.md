---
name: math-explainer-style-router
description: >-
  Decide which explanatory voice to use for a math/science/technical piece and
  then write in it — automatically choosing between an intuition-first,
  geometric "3Blue1Brown" style (the intuition-first-explainer skill) and a
  rigorous, discovery-driven "Abbott" style (the abbott-style-analysis skill).
  The deciding question: does the topic hinge on a place where naive intuition
  actively FAILS or misleads — paradoxes, counterexamples, subtle ε-δ / limit /
  completeness definitions, theorems whose obvious version is false? If so, route
  to the Abbott style; if intuition is merely absent and can be built into a
  vivid picture (linear maps, determinants, gradients, Fourier), route to the
  geometric style; blend when both apply. Use this whenever the user asks to
  draft, rewrite, or explain a math or technical concept WITHOUT specifying a
  style, or explicitly asks you to pick the right approach, choose between
  intuition and rigor, or "write it in the best style for this topic."
---

# Math Explainer Style Router

This skill picks the right teaching voice for a piece and then writes in it. You
have two finished styles available, and they are complementary, not
interchangeable:

- **`intuition-first-explainer`** — the geometric, 3Blue1Brown-in-prose voice.
  Turns abstract symbols into vivid pictures; answers "what it means" and "why we
  do it" before "how to compute." Its job is to *build* a mental image the reader
  never had.
- **`abbott-style-analysis`** — the rigorous, discovery-driven Abbott voice. Opens
  with a paradox, pushes naive intuition until it breaks, then introduces the
  precise definition as the rescue, with proof-construction commentary. Its job is
  to *repair* an intuition that misleads, using rigor.

Choosing well matters because the two styles answer different reader needs. Force
a visual picture onto a topic whose whole point is a subtle trap, and you'll
paper over the very difficulty the reader needs to feel. Wrap a clean, picturable
idea in crisis-and-rescue scaffolding, and you'll manufacture drama where none
exists and bury a simple insight.

## The one question that decides it

Before writing anything, answer this out loud (a sentence or two), because it
determines everything that follows:

> **What does a smart but untrained reader naively believe about this topic — and
> is that belief correct?**

This splits cleanly into two cases.

**Case A — intuition FAILS (→ Abbott style).** The naive belief is *wrong*, or
has a hidden hole, or quietly assumes something false. There's a trap. The reader
"knows" something that isn't so, and the payoff of the piece is a rigorous tool
that resolves the contradiction. Tell-tale signs:

- The obvious version of a statement is actually false, and a counterexample or
  pathological object exists (a limit of continuous functions that isn't
  continuous; a conditionally convergent series you can rearrange to any sum).
- The topic is a carefully engineered definition built precisely to exclude
  pathologies (ε-δ continuity, uniform continuity, uniform convergence,
  completeness, measurability, compactness).
- There's a gap or paradox at the heart (√2 has no home in ℚ; a bounded
  increasing set of rationals with no rational least upper bound).
- The reward is *why the proof works* and *why the definition is written exactly
  this way*, more than any picture.

**Case B — intuition is merely ABSENT (→ geometric style).** The naive belief
isn't wrong, the reader just has no mental image yet. Once you hand them the right
picture, everything clicks and stays correct. Tell-tale signs:

- The concept is abstract or symbol-heavy but, once visualized, is perfectly
  well-behaved (linear transformations as stretching/rotating space; the
  determinant as area/volume scaling; the dot product as alignment; the gradient
  as the direction of steepest ascent; Fourier as sums of rotating arrows).
- The goal is to translate formulas into geometry or physical imagery.
- There is no trap, no paradox, no counterexample lurking — just a missing
  picture.
- The reward is an "aha, I can *see* it now," not a resolved contradiction.

If you can describe a concrete way the reader gets *fooled*, you're in Case A.
If the reader is simply *blank* rather than *misled*, you're in Case B.

## When both apply — the blend

Many real-analysis and advanced topics are genuinely both: the reader needs a
picture *and* there's a subtlety that will bite. Don't force a single label.
Blend, with this default ordering:

1. **Open in the geometric voice** to build a stage the reader can see — give them
   the intuitive picture first so they have something concrete to hold.
2. **Switch to the Abbott voice exactly when the picture starts to lie** — the
   moment naive intuition would lead them astray, name the crisis and bring in
   rigor as the rescue.

This sequencing is powerful because the geometric picture makes the later crisis
land harder: the reader has to watch an image they trusted develop a crack.
Signal the handoff explicitly in the prose ("The picture has served us well — but
here's where it quietly breaks down…").

Use the blend when, for example: explaining why pointwise limits of continuous
functions can fail to be continuous (picture of graphs converging, then the
spike that survives), or motivating uniform continuity (picture of a function
getting ever-steeper, then the δ that can't keep up).

## How to use the chosen style

Once you've decided, **state your choice and the one-line reason before writing**,
so the user can redirect you cheaply if they disagree. For example: "This topic
hinges on a counterexample where the obvious claim is false, so I'll write it in
the rigorous Abbott style." Then:

- Load and follow the corresponding skill for the full method:
  - Case A → apply **`abbott-style-analysis`** (its five-movement workflow:
    motivational hook → crisis of intuition → rigorous definition with the "why" →
    logical cascade with proof commentary → guided "what if?" exploration).
  - Case B → apply **`intuition-first-explainer`** (its arc: empathetic hook →
    plant the picture → simple concrete case → build up → payoff → intentional
    pauses).
  - Blend → run the geometric arc until the subtlety appears, then switch into the
    Abbott workflow for the rigorous core.

If those skills are installed, invoke the relevant one so you get its full
guidance and phrasebook rather than working from memory. If they aren't available
in the current environment, the summaries above are enough to carry the voice.

## What to avoid

- **Don't skip the diagnosis.** Writing first and labeling later defeats the
  purpose; the opening move of each style is different, so you must decide before
  the first sentence.
- **Don't default to the geometric style just because it's friendlier.** A topic
  built around a trap *needs* the crisis; smoothing it over with a pretty picture
  shortchanges the reader.
- **Don't force the Abbott crisis onto a trap-free concept.** Inventing a fake
  paradox to dramatize something simple is worse than just showing the picture.
- **Don't hide your choice.** A one-line statement of which style and why lets the
  user steer; silent routing makes disagreement expensive.
