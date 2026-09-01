# Machine Learning — Authoring Guide

This repository is **self-study material for people learning machine learning**.
The audience is learners, not experts, so the material must *teach* — not merely
state the result. It is the sibling of `nrstatlab/Statistics-Major` and follows
the same conventions; where this file is silent, follow that repository.

## Site structure

Three levels, no build step. Every page is hand-authored HTML.

```
index.html            Course hub — the four units, plus the scope page
unitN.html            Unit page — the idea, learning outcomes, topic tiles
unitN-<topic>.html    Topic page — the algorithms themselves
syllabus.html         Full inventory, prerequisites, and what is NOT covered
css/styles.css        Shared stylesheet (base is the Statistics-Major system)
js/notes.js           Python/R tab switching and the copy button
scripts/check_notes.py  Structural validator — run before every commit
```

Units divide by the **kind of supervision signal**: labelled, unlabelled, a
mixture, or a reward. Topics divide a unit by task. Do not add a page that
breaks that division.

## Every algorithm carries the same six parts, in this order

1. **Definition** — `.concept` with `<span class="label">DEFINITION</span>`.
2. **Mathematical Foundation** — `.formula` with `<span class="label">FORMULAE</span>`.
3. **How It Works** — plain prose: intuition, the hyperparameters that matter, named variants.
4. **Assumptions and Failure Modes** — the `.assume` block. What it takes for
   granted, and the conditions under which it breaks. This is the part that makes
   two algorithms comparable, so it is not optional.
5. **Worked Examples** — exactly three, always in finance, agriculture and
   medicine. Seeing one idea in three unrelated domains is what separates a
   concept from a recipe.
6. **Code** — Python and R, in switchable tabs. Both simulate their own data.

Headings are numbered `<h2>` for the algorithm and `<h3>` for its parts
(`2.6`, then `2.6.1` … `2.6.5`). A topic page ends with an **At a Glance** table
drawn from the assumption blocks.

## Correctness

- **Verify every formula against its canonical source** before writing it — the
  original paper or a standard text, not memory. Say which convention you are
  using when more than one exists.
- **Run every Python pane before committing it.** A pane that does not execute is
  a bug, not a snippet. `scripts/check_notes.py` parses them; CI runs them.
- Never state a performance figure as fact unless it is reproducible from a named
  public dataset that the code actually loads. The code simulates its data, so
  printed accuracies are properties of the simulation — say so, or cite a source,
  or teach the caveat instead of asserting a number.
- Prefer teaching the failure mode over quoting a flattering metric.

## HTML and math conventions

- Math uses **MathJax v3**: `\( … \)` inline, `\[ … \]` display. **Never** use `$`
  as a delimiter — a literal `$` in the text is always currency. Unicode symbols
  (μ, σ, ×, ≤) are fine in prose.
- Inside math, write comparisons as `&lt;` and `&gt;`. A raw `<` in prose is
  invalid HTML and breaks strict parsers.
- Inside `<pre><code>`, `<` and `&` must be escaped as `&lt;` and `&amp;` —
  otherwise R's `<-` breaks any strict parser. The validator enforces this.
- Code panes are `<div class="code-pane"><pre class="language-python"><code>…`.
  The copy button is added by `js/notes.js` and must never live inside `<pre>`:
  reading `pre.textContent` with the button inside appends its label to the code.
- Wide content (tables, formulae) goes in its own scroll container so the page
  body never scrolls sideways.

## Adding a new algorithm

1. Put it on the topic page whose task it belongs to; create a new topic page
   only if it belongs to no existing one.
2. Give it the next number in its topic, and update: the topic page's chip list
   and At a Glance table, the unit page's tile count and algorithm table, the
   hub's topic table, and `syllabus.html`.
3. Bump `EXPECTED_ALGORITHMS` in `scripts/check_notes.py`.

## Before committing

```bash
python scripts/check_notes.py      # delimiters, escaping, links, inventory
```

CI additionally validates the HTML, executes every Python pane, and checks
external links.

## Known gaps

`syllabus.html` lists what these notes do not yet cover — dimensionality
reduction, GMM/EM, boosting, an evaluation unit, preprocessing, SARSA, and
neural networks. Keep that list honest: when you add one of them, remove it
from the list in the same commit.
