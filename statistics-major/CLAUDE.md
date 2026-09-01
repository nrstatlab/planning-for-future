# Statistics-Major — Authoring Guide

This repository is **study material for undergraduate statistics students**.
The audience is learners, not experts, so content must teach — not merely state
the answer.

## Pedagogy — write for undergraduates (most important)

**Never take "direct steps" when solving a problem or proving a theorem.**
Show the full reasoning at a pace a first-time learner can follow:

- **Proofs:** give the *Statement*, then a *Proof* that moves one small,
  justified step at a time. Name the tool each step uses (definition, a named
  theorem, an inequality, an algebraic identity) rather than jumping to the
  result. Do not compress several manipulations into a single line, and do not
  write "clearly", "obviously", or "it follows that" in place of a step.
- **Problems:** restate what is given and what is asked, then work through
  *every* intermediate step — set up the formula, substitute the numbers, show
  the arithmetic, and end with a one-line interpretation of what the answer
  means. Never present only the final value.
- Prefer an extra explanatory line over a skipped one. When a step relies on a
  result from earlier in the unit, say so explicitly.

A worked example is good when a student who is seeing the topic for the first
time could reproduce it without external help.

## Correctness

- **Verify every numeric claim and each step of algebra in Python before
  writing it** (pure `math`/`statistics`/`fractions`; no numpy/scipy — implement
  special functions by hand when needed). This applies to proofs, worked
  examples, tables, and figure coordinates.
- When a source (textbook/PDF) has a slip, use the correct value and note the
  correction; never propagate an error.

## HTML / math conventions

- Math uses **MathJax v3**: `\( … \)` for inline, `\[ … \]` for display.
  **Never** use `$` as a math delimiter (a literal `$` is allowed only inside
  `<code>` for R syntax). Unicode symbols (μ, σ, χ², ≤, ×) are fine.
- In display math, break lines with `\\`, not `\\[6pt]` (the row-spacing form
  trips the delimiter-balance check).
- Section content sits inside `.concept`, `.formula`, and `.example` blocks with
  a `<span class="label">` heading, matching the existing units.

## Figures

- Inline **SVG** wrapped in `<figure class="figure"> … <figcaption>`, reusing the
  site palette (#1e7fbf blue, #dc2626 red, #f59e0b amber, #059669 green,
  #8b5cf6 purple, #0f4c81 title-blue, grays #374151/#64748b/#94a3b8).
- Compute all plotted coordinates in Python; keep figure text as plain SVG
  `<text>` (no LaTeX inside SVG). Every `<svg>` must be well-formed XML.

## Structure

- Topics live as numbered `<h2>`/`<h3>` sections. There is **no** "Some more
  related topics" catch-all — put each topic beside the core section it extends.

## Workflow

- Develop on the designated feature branch; **one squash-merged PR per course**.
- Before committing, validate each edited file: `\(`/`\)` and `\[`/`\]` balance,
  `<div>`/`<h2>` balance, no stray `$`, and every `<svg>` parses.

## Course status notes

- The **`computational statistics and r programming 2023`** directory is a
  deliberate, *temporary* duplicate of the current `computational statistics and
  r programming` course. It is to be **kept until about January 2027**, after
  which the entire `…2023` course (its unit/index/syllabus/practical files and
  its link from the root `index.html`) should be **removed**. Until then, keep
  both in sync when adding shared R content. Do the removal as its own PR and
  confirm before merging — do not delete it earlier without the user's say-so.
