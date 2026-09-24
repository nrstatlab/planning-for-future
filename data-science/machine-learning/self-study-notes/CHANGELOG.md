# Changelog

## 2026-08-30 — Split into unit and topic pages

The notes were a single 277 KB page holding all 23 algorithms. They are now a
three-level site — hub, four unit pages, nine topic pages — following the same
structure and visual system as `nrstatlab/Statistics-Major`, so the two read as
one family.

### New structure

| Level | Pages | Holds |
|---|---|---|
| Hub | `index.html` | The four units, how the material is organised, the full topic table |
| Unit | `unit1..4.html` | The idea behind the unit, learning outcomes, topic tiles, every algorithm in it |
| Topic | `unit1-classification.html` and 8 more | The algorithms themselves |
| Reference | `syllabus.html` | Full inventory, prerequisites, and an honest list of what is not covered |

Largest page is now 58 KB rather than 277 KB, and no page carries more than five
algorithms.

### Adopted from the Statistics-Major system

- Shared `css/styles.css` — same palette, typography and box vocabulary
  (`.concept`, `.formula`, `.example`, `.tip`, `.banner`, `.unit-grid`,
  `.page-nav`). ML-specific additions are appended in one clearly marked block.
- Banner with breadcrumbs on every inner page; previous/next navigation
  chaining all nine topic pages in reading order.
- **Math delimiters changed from `$…$` to `\( … \)` and `\[ … \]`**, per that
  repository's convention. A literal `$` is now always currency, which also
  removes the whole class of MathJax/currency collisions the audit flagged
  (T-7) — the `tex2jax_ignore` shields are gone with it.
- `CLAUDE.md` authoring guide, adapted for this subject.

### Kept, and carried across intact

All 23 algorithms, 69 worked examples and 46 code panes, with every correction
from the earlier audit. Each algorithm keeps its six parts, now as numbered
`<h2>`/`<h3>` sections. Verified after the split: 23 of 23 Python panes still
run end to end.

### Also changed

- Each topic page now ends with an **At a Glance** table putting its algorithms
  side by side on assumptions and failure modes — derived from the chip rows,
  and the comparison that decides which method to use.
- Prism.js is gone. `pre` is styled directly, so the code panes no longer depend
  on a CDN stylesheet loading — the root cause of finding T-1.
- `js/notes.js` replaces the inline script: tab switching by delegation, arrow-key
  movement between tabs, and a copy button that lives outside `<pre>`.
- `scripts/check_notes.py` rewritten for the multi-page structure: it now checks
  delimiter balance and stray `$` per page, cross-page links and anchors, code-tab
  targets, shared-asset links, and that the algorithm inventory still totals 23.
- CI validates every page rather than one file.

### Removed

- The single long page. Keeping a one-page copy alongside the split would
  reintroduce exactly the duplication that finding P-1 was about.
  `ml_self_study_notes.html` remains a redirect, so old links still work.

## 2026-08-30 — Conceptual audit and remediation

A full concept-first audit of the notes (see `AUDIT_REPORT.md`), followed by the
corrections it called for. 41 findings were raised; the corrective ones are fixed
here. The coverage gaps — new algorithms and a foundations unit — are not, and are
listed at the bottom as outstanding.

### Mathematics corrected

- **Label Propagation (3.3)** — the maths box printed the row-stochastic
  normalisation $T = D^{-1}W$ and the symmetric normalisation $D^{-1/2}WD^{-1/2}$
  as a single equation, and gave Label *Spreading's* α-recursion and closed form
  under Label Propagation's name. Now split into two labelled derivations, each
  attributed and each naming the scikit-learn class that implements it.
- **Ridge (1.8)** — the SVD shrinkage factor $d_j^2/(d_j^2+\lambda)$ was captioned
  "for feature $j$". It holds in the rotated basis $\gamma = V^\top\beta$, not per
  original feature. Restated correctly, with the insight it carries: Ridge shrinks
  low-variance *directions* hardest.
- **Lasso (1.9)** — the coordinate-descent step soft-thresholded the RSS gradient.
  It thresholds the partial residual correlation $\rho_j$, then divides by $z_j$.
  Corrected, with a note on why the gradient is the wrong quantity. The Elastic Net
  penalty gained its conventional ½ on the L2 term so that α = 0 recovers Ridge.
- **Isolation Forest (2.6)** — the three score bands conflated "no anomaly in the
  sample" ($s ≈ 0.5$) with "this point is normal" ($s ≪ 0.5$). Rewritten, and the
  score threshold is now connected to scikit-learn's quantile-based
  `contamination` parameter.
- **Co-Training (3.2)** — an error bound was attributed to Blum & Mitchell (1998)
  that does not appear in that paper. Replaced with the PAC-learnability result
  the paper actually proves.
- **Self-Training (3.1)** — the method's premise was named as the low-density
  assumption. It is confidence calibration; low-density separation is a different,
  geometric assumption. Corrected, and linked to why confirmation bias follows.
- **Six smaller imprecisions** — C4.5 uses gain ratio, not information gain; the
  normal equation costs $O(Np^2 + p^3)$; Apriori makes $k_{\max}+1$ passes, not a
  fixed $k+1$; the FP-Tree is not $O(N)$ in general; weighted KNN needs a $d = 0$
  guard; the policy-gradient theorem carries $\gamma^t$ for the discounted
  objective, and $G_t$ is now defined.

### Code brought back into line with the mathematics

- **Q-Learning (4.1)** — the environment advanced soil moisture by the action
  *index*; `water_added` (0/5/10/20 mm) was computed and never used, so the reward
  and the transition disagreed about what an action meant. The transition now uses
  the millimetres.
- **Dyna-Q (4.3)** — the model stored the last observed transition in a stochastic
  environment. It now accumulates a running mean reward and a successor histogram,
  matching the $M(s,a) = (r_{avg}, s'_{most\ common})$ in the maths box. The
  planning gate no longer suppresses planning until 20 distinct pairs are seen,
  and the Python and R panes now implement the same procedure.
- **Value Iteration (4.4)** — transition rows were force-renormalised, hiding the
  fact that they were constructed ad hoc and that "response improves" was a no-op
  for good-response states. Rows now sum to 1 by construction, with an assertion
  instead of a renormalisation, and response can move in both directions.
- **REINFORCE (4.2)** — `log_prob()` was defined and never called, leaving the
  link to the policy-gradient theorem implicit. It is now used and reported.
- **FP-Growth (2.5)** — the R pane runs `eclat()`, a different algorithm. That
  substitution is now stated explicitly in a callout and in the code comments,
  with a pointer to `rCBA::fpgrowth()`.
- **Self-Training (3.1)** — `SelfTrainingClassifier(base_estimator=…)` was removed
  in scikit-learn 1.6 and the pane no longer ran. Passed positionally so it works
  on both sides of the rename.
- **Isolation Forest (2.6)** — `contamination` was set to the true injected fraud
  rate, handing the model the answer it was meant to estimate. Now `'auto'`, with
  the existing parameter sweep annotated to show what actually moves.

All 23 Python panes are verified to run end-to-end.

### Evidence integrity

- 28 quantified performance claims were stated as fact with no source, while the
  code panes generate synthetic data. Each is now either reproducible from a named
  public dataset (Wisconsin Diagnostic Breast Cancer, Pima Indians Diabetes),
  deferred to what the pane actually prints, or rewritten to teach the underlying
  caveat instead of asserting a number. Several now carry a genuine warning —
  look-ahead bias in the stock example, clustered standard errors in the panel
  example, stability selection in the Lasso example.
- Footer corrected from "20 Algorithms · 60 Real-World Examples" to 23 and 69.
- Mini-tables left orphaned by those rewrites were replaced with structural ones.
- Currency unified to `$`; one stray `maximizes` brought into line with the
  document's British spelling.

### Structure

- **Unit 3 now has subsections**, as the other three units do: *Inductive*
  (Self-Training, Co-Training) and *Transductive* (Label Propagation). Cards
  reordered and renumbered; sidebar updated. This is the distinction that decides
  which of the three to use.
- **Every card gained an "Assumptions & failure modes" row** — what the method
  takes for granted, and the conditions under which it breaks. This uses the
  `.key-points` styling that was defined but never used.
- Decision Tree and Random Forest each note that the same method spans both
  classification and regression, and what changes.
- Association-rule mining and anomaly detection now justify their placement in
  the unsupervised unit rather than merely occupying it.

### Rendering and access

- **Code panes were rendering as `#ccc` text on white.** The Prism `language-*`
  class sat only on `<code>`, but Prism themes paint the block through
  `pre[class*="language-"]`. The class is now on both, plus standalone
  background/padding/overflow rules so the panes stay legible if the CDN fails.
- The copy button lived inside `<pre>` and the handler read `pre.textContent`, so
  every copied snippet ended with the word "Copy". It now sits in a wrapper and
  copies from the `<code>` element.
- `function scrollTo()` shadowed `window.scrollTo`. Renamed `scrollToUnit`.
- Added responsive breakpoints — the 270px sidebar no longer stays fixed on
  phones — and a print stylesheet.
- Navigation divs gained `role="button"`, `tabindex` and keyboard handlers.
- `<` and `&` inside code panes are escaped, so the file parses strictly.
- Currency cells shielded with `tex2jax_ignore`, and `code` restored to MathJax's
  skip list.
- Added description, Open Graph and Twitter metadata.

### Repository

- `ml_self_study_notes.html` was a byte-identical 252 KB copy of `index.html`.
  It is now a redirect stub, so the two cannot drift.
- Real README, `.gitignore`, and this changelog.
- CI on every push: structural checks (`scripts/check_notes.py`), HTML validation,
  execution of all 23 Python panes, and external link checking.

### Outstanding — not addressed here

These are coverage gaps rather than defects; each needs new material written:

- No dimensionality reduction or latent-variable modelling in Unit 2 (PCA/SVD,
  GMM + EM, t-SNE/UMAP).
- No boosting anywhere (AdaBoost, Gradient Boosting, XGBoost) — the ensemble
  concept is present only in its bagging half.
- No unit on evaluation and model selection, though every card assumes one.
- No SARSA, leaving Q-Learning's "off-policy" tag without a contrast.
- No preprocessing card, and no neural-network card despite forward references
  to DQN and CNN embeddings.
- No licence chosen.
