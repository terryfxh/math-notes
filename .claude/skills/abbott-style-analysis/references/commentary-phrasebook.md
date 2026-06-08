# Commentary Phrasebook & Worked Example

Read this when you want more options for the explanatory voice that runs
alongside a proof, sharper counterfactual prompts, or a concrete model of the
Abbott rhythm. SKILL.md gives the structure; this gives the texture.

## Proof-commentary phrases (the aside voice)

**Announcing the goal of a step**
- "Our target is clear: we need to produce a single number that sits above the
  whole set but as low as possible. Where could such a thing come from?"
- "Before we write anything down, let's ask what shape the answer must have."

**Naming what's doing the work**
- "Notice that completeness is quietly carrying the entire argument here."
- "This is the exact moment the hypothesis pays off — watch what it buys us."

**Orienting the reader mid-proof**
- "Let's take stock. We've secured X; what remains is to connect it to Y."
- "We're halfway home. The hard part is behind us; the rest is bookkeeping."

**Motivating a construction that looks unmotivated**
- "Pulling this particular sequence out of thin air looks like a magic trick.
  It isn't — here's the question it answers."
- "Why ε/2 and not ε? Hold that thought; the reason will surface in two lines."

## Counterfactual-definition prompts (step 3 & step 5 engine)

Use these to probe *why the definition is written exactly as it is*:

- "What goes wrong if we drop the word 'every' here and only ask for 'some'?"
- "Suppose we weakened the strict inequality to ≤. Construct an example that now
  sneaks through but shouldn't."
- "The definition demands this hold for *all* ε > 0. What pathological object
  becomes 'continuous' if we only require it for ε = 1?"
- "Swap the order of these two quantifiers. Is the new statement the same idea,
  a strictly stronger one, or nonsense?"
- "We insisted the bound not depend on x. Where, precisely, in the proof would
  an x-dependent bound betray us?"

## Crisis-of-intuition openers (step 1 & 2)

- "Here's something that should bother you more than it probably does…"
- "Everyone agrees this is obvious. Let's try to actually prove it — and watch it
  fall apart."
- "Naively, you'd reorder the sum and expect the same answer. Let's do exactly
  that, carefully, and arrive somewhere absurd."

## Worked example (~280 words): why we need the Axiom of Completeness

> Here's a question that sounds almost too easy to bother with: does the equation
> x² = 2 have a solution? Of course it does — it's √2, about 1.414. But pause and
> ask *where that number lives.* If our entire universe were the rational numbers,
> would √2 be in it?
>
> Let's try to corner it. Consider the set A of all positive rationals whose
> square is less than 2: numbers like 1, 1.4, 1.41, 1.414, marching upward. This
> set is clearly bounded above — 2 is a ceiling, and so is 1.5. Intuition says a
> set that climbs but never exceeds a ceiling should pile up against a *highest*
> point, a least upper bound. So where is it?
>
> Here's the crisis. Whatever rational candidate r you propose as that boundary,
> we can show r² can't equal 2 (that's the classic irrationality argument), so
> either r² < 2 — and then we can nudge r slightly larger and stay inside A, so r
> wasn't an upper bound at all — or r² > 2, and we can shrink r a little and still
> have an upper bound, so r wasn't the *least* one. The boundary the set so
> obviously wants simply isn't there. The rationals have a hole exactly where √2
> should be.
>
> So intuition hasn't lied to us; our number system has failed us. That gap is
> precisely what the Axiom of Completeness is built to forbid: it *declares* that
> every nonempty set bounded above has a least upper bound. Notice what we did —
> we didn't define completeness and then look for a use. We felt the absence
> first, and the axiom is the smallest thing that fills it. What if we'd demanded
> less? That's worth chewing on before the next section.

Notice the moves: an "obvious" question (hook), an honest attempt that collapses
at the boundary (crisis), the definition introduced as the minimal rescue with
its "why" intact (rebuild), and a counterfactual handed to the reader (guided
exploration).
