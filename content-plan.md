# Content plan from the MATHSnotes library

An analysis of the five textbooks in `MATHSnotes`, sorted by discipline, with each
strand split into **CS / algorithm-combinable** material and **pure-theory** material,
plus concrete post ideas matched to this blog's intuition-first voice. (This is a private
planning note; it is not published as a page.)

## The library at a glance

| Book | Discipline | Character | CS overlap |
|---|---|---|---|
| Niven, Zuckerman & Montgomery, *An Introduction to the Theory of Numbers* | Number theory | Classical, very clean | **Very high** (crypto, primality, algorithms) |
| Stanley, *Enumerative Combinatorics I* | Combinatorics | Deep, structural | **High** (DP, counting, generating functions) |
| Demaine, Gasarch & Hajiaghayi, *Algorithmic Lower Bounds* | Complexity theory | CS-native, reduction-driven | **It is the CS** (NP-hardness, puzzles, games) |
| Hulek notes (Thompson) | Algebraic geometry (intro) | Short, gentle on-ramp | Low–medium (bridges to Gröbner, codes) |
| Hartshorne, *Algebraic Geometry* | Algebraic geometry (advanced) | Abstract, foundational | Low (mostly pure; elliptic curves bridge) |

Two of these (Niven, Stanley) are content goldmines for the blog. One (Demaine) is the
natural CS anchor to pair them with. The two algebraic-geometry texts are mostly pure, but
they host a few high-impact bridges (elliptic curves, the algebra↔geometry dictionary).

---

## 1. Number theory — Niven *(richest vein; you've already mined CRT)*

### CS / algorithm-combinable
- **Primitive roots & the discrete logarithm → Diffie–Hellman.** Niven's congruence
  chapter gives primitive roots; the CS payoff is key exchange and the baby-step
  giant-step algorithm. *Post: "The discrete log: easy to make, hard to undo" — group
  intuition + runnable BSGS + why DH is safe.* Code: yes. Pairs with Demaine (hardness
  assumptions).
- **Quadratic residues & quadratic reciprocity → primality testing.** Legendre/Jacobi
  symbols power Solovay–Strassen and inform Miller–Rabin. *Post: "How to convince yourself
  a 300-digit number is prime" — QR intuition + runnable Miller–Rabin.* Code: yes.
- **Continued fractions → best rational approximation and Wiener's attack on RSA.**
  Niven's continued-fractions chapter; CS payoff is the Stern–Brocot tree and breaking RSA
  with a small private exponent. *Post: "Continued fractions, or how to break RSA when the
  key is lazy."* Code: yes. Visual + dramatic.
- **Multiplicative functions & sieves.** Euler's totient, Möbius; the linear sieve.
  *Post: "Sieves: counting primes without checking them."* Code: yes. (Also bridges to
  Stanley's Möbius inversion — see synthesis below.)

### Pure theory
- **Quadratic reciprocity itself.** A genuine jewel. *Post: a visual proof (Eisenstein's
  lattice-point counting) — "Why do two primes secretly agree?"* The lattice-point picture
  is perfect for the blog's style. Code: optional (illustrate the lattice).
- **Sums of two squares / Gaussian integers.** *Post: "Which numbers are sums of two
  squares?" — Gaussian-integer factorization, with Cornacchia's algorithm as the
  constructive payoff.* Code: yes, light.
- **Pell's equation & continued fractions.** *Post: the geometry of $x^2 - D y^2 = 1$ and
  why continued fractions solve it.* Pure with an algorithmic tail.

---

## 2. Combinatorics — Stanley *(deepest CS/algorithm bridges after number theory)*

### CS / algorithm-combinable
- **The transfer-matrix method → dynamic programming.** Stanley Ch. 4. Counting tilings,
  walks, and constrained strings becomes matrix powers; this *is* DP in disguise.
  *Post: "Counting domino tilings, or: dynamic programming is a matrix."* Code: yes,
  great visuals.
- **Generating functions → solving recurrences in code.** *Post: "Generating functions:
  a bookkeeping trick that solves recurrences" — Fibonacci closed form, then automated
  recurrence-solving.* Code: yes.
- **Permutation statistics → sorting.** Inversions equal bubble-sort distance; the Lehmer
  code ranks/unranks permutations. *Post: "Inversions, descents, and what sorting really
  measures."* Code: yes.
- **Catalan numbers → parsing & stacks.** Stack-sortable permutations, balanced
  parentheses, binary trees. *Post: "Catalan numbers: the same answer to ten different
  questions" (echoes your Poincaré epigraph!).* Code: yes.

### Pure theory
- **Möbius functions on posets / inclusion–exclusion.** Stanley Ch. 3. *Post: "Inclusion–
  exclusion is just one example of a much bigger idea" — the Möbius function on a poset.*
  Bridges to number theory's Möbius (synthesis below). Conceptual, elegant.
- **Posets, lattices, Dilworth's theorem.** *Post: Dilworth's theorem and why it secretly
  computes a minimum path cover* (this one straddles pure ↔ algorithm via matching).

---

## 3. Complexity theory — Demaine *(your CS anchor; pairs with everything above)*

This whole book is the "algorithms / CS" side. Its specialty — proving puzzles and games
hard — is unusually fun and visual, which suits the blog.

- **"Why your favorite puzzle is NP-hard."** Reductions from 3SAT/Planar SAT to games
  (the book is full of them). *Post series: pick one puzzle, build the gadgets, show the
  reduction.* Highly visual, accessible, shareable.
- **NP-hardness via Hamiltonian cycle / 3-Partition.** Gadget-based reduction explainers.
- **ETH — "why we believe some problems truly need exponential time."** Conceptual.
- **#P and counting hardness.** Sets up the synthesis gem below (permanent vs determinant).

---

## 4. Algebraic geometry — Hulek notes + Hartshorne *(mostly pure; a few sharp bridges)*

### CS / algorithm-combinable (the bridges)
- **Elliptic curves → elliptic-curve cryptography.** The single highest-value bridge here.
  The chord-and-tangent group law is intensely visual, and it powers modern ECC. *Post:
  "The group law on an elliptic curve, drawn by hand" → follow-up on ECC.* Bridges to
  Niven (number theory) and crypto. Code: yes.
- **(Adjacent) Gröbner bases & Buchberger.** Not in these texts, but the computational
  shadow of the Nullstellensatz: solving polynomial systems by computer. Worth a post that
  starts from Hulek's affine-variety material. Code: yes.
- **Algebraic curves over finite fields → error-correcting codes.** Goppa / AG codes.
  Advanced; a later-stage post.

### Pure theory
- **The Nullstellensatz & the algebra↔geometry dictionary.** From the Hulek notes (Zariski
  topology, $V(I)$ and $I(X)$, irreducible ↔ prime). *Post: "Geometry you can do with
  algebra: the Nullstellensatz dictionary."* Conceptual, beautiful, accessible entry point.
- **What is a scheme, and why?** From Hartshorne. *Post: an expository "why schemes" —
  motivation over machinery.* Pure, hard, for a mature blog.
- **Riemann–Roch for curves.** Hartshorne Ch. IV. Long-term, advanced expository goal.

---

## 5. Cross-book synthesis posts (the standouts)

These connect two or three of the books and would be the most distinctive pieces on the blog:

- **Permanent vs. determinant.** Same formula up to signs, yet the determinant is easy
  (Gaussian elimination) and the permanent is #P-hard (Valiant). Bridges Stanley
  (matchings/counting), linear algebra, and Demaine (counting hardness). *A genuinely
  striking post.*
- **One Möbius, two worlds.** The Möbius function of number theory (Niven) and the Möbius
  function of a poset (Stanley) are the same idea; inclusion–exclusion is the simplest
  case. Bridges two of your books under one picture.
- **Discrete log: the number theory of a hardness assumption.** Primitive roots (Niven) +
  the believed hardness (Demaine) + Diffie–Hellman. Shows pure math becoming a security
  guarantee.
- **Elliptic curves, three ways.** Geometry (Hartshorne/Hulek), number theory (Niven),
  cryptography. A flagship long-form or mini-series.

---

## Suggested roadmap (building on what's live)

You've published the Spectral Theorem, Gram–Schmidt, and the Chinese Remainder Theorem, so
the number-theory/CS vein is already your spine. A natural ordering:

1. **Miller–Rabin primality** (Niven QR → CS). Direct sequel to CRT; same audience.
2. **Discrete log + Diffie–Hellman** (Niven → Demaine). Completes a small "crypto from
   number theory" arc.
3. **Counting domino tilings = DP is a matrix** (Stanley → algorithms). Opens the
   combinatorics vein with strong visuals.
4. **The Nullstellensatz dictionary** (Hulek). Your first algebraic-geometry post, gentle.
5. **Permanent vs. determinant** (synthesis flagship).
6. **The group law on an elliptic curve** (Hulek/Hartshorne → crypto).

Items 1–3 are high-overlap, runnable, and on-brand right now; 4–6 broaden the blog's range
once the spine is established.

## 6. Real analysis series — "What Calculus Becomes When We Ask Why" (running)

An off-library series (Abbott / Rudin / Tao rather than the `MATHSnotes` five), opened
June 2026. Proof-heavy posts in the Abbott voice: paradox first, crisis of intuition,
definition as rescue, logical cascade.

1. **Lesson One — Why the Real Line Has No Holes** (`reconstructing-calculus`,
   2026-06-07, published): completeness → nested intervals → Bolzano–Weierstrass →
   Cauchy criterion, then limits, compactness, FTC.
2. **Lesson Two — Pointwise vs. Uniform Convergence** (`uniform-convergence`,
   2026-06-10): the sliding-spike debt repaid; quantifier diagnosis, ε/3 theorem,
   integrable/differentiable limit theorems, M-test, Weierstrass monster.
3. **Lesson Three — candidates** (pick when the series resumes):
   - *Series and rearrangements*: conditional vs. absolute convergence, the Riemann
     rearrangement theorem with a runnable rearrange-to-any-target algorithm
     (Abbott Ch. 2). Pays off Lesson One's alternating-series hook.
   - *Continuity and the IVT, deep dive*: uniform continuity, Dirichlet/Thomae
     pathologies, the Darboux property of derivatives, MVT (Abbott Ch. 4–5). Pays off
     Lesson One's compactness sketch.
   - Loose threads planted in Lesson Two for later lessons: dominated convergence
     (the door to measure theory), Dini's theorem.

Interleave these with the MATHSnotes roadmap above (whose next item remains
"Permanent vs. determinant") rather than running the series back-to-back.

## Style fit

Everything above is chosen to support the blog's "see it first, then prove it" approach:
each has a strong visual or computational hook (a lattice-point picture, a gadget, a matrix,
a chord-and-tangent construction) before any formal machinery. Number theory and
combinatorics give you the most runnable, immediately shareable posts; algebraic geometry
gives you the long, beautiful, conceptual pieces for when you want depth over reach.

## 7. Reflections series — see `reflections-plan.md`

The Learning & Philosophical Reflections section has its own plan tree (12 candidate
essays in four branches, each anchored to a thread the published essays planted, with
explicit non-overlap rules and sequencing). Interleave roughly one reflection per 3–4
math posts.
