# 3Blue1Brown video reference map

Generated 2026-06-18 from the 3Blue1Brown YouTube channel feed plus official
3Blue1Brown lesson pages. This is a private research note for choosing videos as
reference objects for future posts; it is not a source transcript and should not
be treated as prose to adapt.

## Selection rule

Use a video when it supports the blog's core promise:

- intuition before calculation;
- one vivid picture that forces the formalism to appear;
- pure math with an applied, computational, or conceptual payoff;
- enough room for an independent prose reconstruction, not a transcript rewrite.

## High-priority matches

| Priority | Video / lesson | Fit | Blog action |
|---|---|---|---|
| 1 | 3Blue1Brown, "But what is a convolution?" | Exact fit for the current transform arc: probability, polynomial multiplication, image processing, FFTs, and the convolution theorem. | Draft created: "Convolution: The Mathematics of Overlap and Echo" at `drafts/mathematics/convolution-the-arithmetic-of-overlap/index.qmd`. |
| 2 | 3Blue1Brown, "But what is the Fourier Transform? A visual introduction" | Natural continuation after the Laplace post; winding graph picture can be rebuilt into prose around frequency as coordinates. | Future post: "Fourier Transform: Listening for Coordinates". |
| 3 | 3Blue1Brown, "The more general uncertainty principle, beyond quantum" | Excellent bridge from Fourier transform to analysis and physics: localization in one domain forces spread in the other. | Future post after Fourier/convolution. |
| 4 | 3Blue1Brown, "Visualizing the Riemann zeta function and analytic continuation" | Strong match for number theory + complex analysis; pairs with prime spirals and the blog's interest in analytic continuation. | Future post: "Analytic Continuation: Extending a Function Without Lying". |
| 5 | 3Blue1Brown, "Reinventing Entropy | Compression is Intelligence Part 1" | Very current and on-brand for CS/probability/information theory; connects compression, surprise, and learning. | Future post candidate: "Entropy: The Price of Not Knowing". |
| 6 | 3Blue1Brown, "How (and why) to take a logarithm of an image" | Complex logarithm, branch cuts, and domain coloring; visual but more specialized. | Future complex-analysis post. |
| 7 | 3Blue1Brown, "The Hairy Ball Theorem" | Topology with an immediately memorable visual statement; complements the inscribed-rectangle post. | Future topology post. |

## Already mined or partly mined

| Video / lesson | Current blog connection |
|---|---|
| "Why do prime numbers make these spirals?" | Already cited in `posts/prime-spirals/index.qmd`. |
| "Visualizing quaternions (4d numbers) with stereographic projection" | Already cited in `posts/quaternions/index.qmd`. |
| "Who cares about topology? (Inscribed rectangle problem)" | Already cited in `posts/the-inscribed-rectangle-problem/index.qmd`. |
| "Eigenvectors and eigenvalues" / Essence of Linear Algebra | Conceptually overlaps with `spectral-theorem` and `gram-schmidt`; useful for visual language, less urgent as a new post. |

## Latest channel signals from YouTube feed

Recent main-channel items from the feed include:

- 2026-06-07: "Reinventing Entropy | Compression is Intelligence Part 1"
- 2026-03-22: "How (and why) to take a logarithm of an image"
- 2026-02-27: "The most beautiful formula not enough people understand"
- 2026-01-31: "The Hairy Ball Theorem"

Shorts can provide puzzle hooks, but for full posts prefer long-form videos or
official lesson pages because they expose a complete mathematical arc.

## Sources

- 3Blue1Brown YouTube feed: `https://www.youtube.com/feeds/videos.xml?channel_id=UCYO_jab_esuFRV4b17AJtAw`
- Convolution lesson: `https://www.3blue1brown.com/lessons/convolutions/`
- Fourier transform lesson: `https://www.3blue1brown.com/lessons/fourier-transforms/`
- Uncertainty principle lesson: `https://www.3blue1brown.com/lessons/uncertainty-principle/`
- Zeta / analytic continuation lesson: `https://www.3blue1brown.com/lessons/zeta/`
- Eigenvalues lesson: `https://www.3blue1brown.com/lessons/eigenvalues/`
