# Conceptual Audit — *Machine Learning: Complete Self-Study Notes*

**Artefact audited:** `index.html` / `ml_self_study_notes.html` (4,774 lines, 252 KB, byte-identical copies)
**Repository:** `nrstatlab/Machine-Learning` · **Published at:** https://nrstatlab.github.io/Machine-Learning/
**Commit audited:** `2519245`
**Date:** 30 August 2026
**Perspective:** *concept-first* — the artefact is judged as a body of knowledge, not as a codebase. The
question throughout is whether each **concept** is correctly stated, correctly located in the taxonomy,
internally coherent across its five representations, and reliably transmitted to the reader.

> ### ⚠ Status: remediated
>
> This report records the audit **as performed on commit `2519245`**. The corrective
> findings below — every item in families **C**, **R**, **E**, **T** and **P**, plus
> **G-6**, **G-8** and **G-9** — have since been fixed. See `CHANGELOG.md` for what
> changed and `scripts/check_notes.py` for the checks that now guard against
> regression. One further defect was found while verifying the fixes and is also
> resolved: `SelfTrainingClassifier(base_estimator=…)` was removed in
> scikit-learn 1.6, so card 3.1's Python pane no longer ran.
>
> **Still open** — the coverage gaps, which need new material rather than edits:
> **G-1** (no dimensionality reduction or GMM/EM), **G-2** (no boosting),
> **G-3** (no evaluation and model-selection unit), **G-4** (no preprocessing card),
> **G-5** (no SARSA), **G-7** (no neural-network card), and the choice of a licence.
>
> Read the sections below as the reasoning behind each change, not as a to-do list.
>
> **Structure has since changed too.** The single page this audit examined has been
> split into a hub, four unit pages and nine topic pages, mirroring
> `nrstatlab/Statistics-Major`. Findings that named the single file still describe
> the defect and the fix; only the file they live in has moved. Two are now moot
> by construction: **T-1** (Prism is gone — `pre` is styled directly) and **T-7**
> (`$` is no longer a math delimiter anywhere).

---

## 1. Method

The document is built from one repeating unit — the **algorithm card** — and every card presents the same
concept five times, in five registers:

```
  Definition  →  Mathematics  →  Brief Explanation  →  3 Domain Examples  →  Python + R Code
   (verbal)      (formal)          (intuitive)          (situated)            (executable)
```

A concept is only *sound* when all five registers agree. The audit therefore ran four passes:

| Pass | Question asked | Method |
|---|---|---|
| **Taxonomy** | Is the concept map complete and correctly partitioned? | Extracted the full unit → subsection → card tree |
| **Coherence** | Do the five registers of each card agree with each other? | Extracted and cross-read all 23 def/math/explanation blocks, 69 examples, 46 code panes |
| **Correctness** | Is each formal statement true? | Checked every equation against the canonical source for that method |
| **Transmission** | Does the concept actually reach the reader? | Checked rendering, escaping, anchors, a11y, responsiveness |

**Inventory verified:** 4 units · 7 subsections · **23** algorithm cards · **69** worked examples ·
**46** code panes (23 Python + 23 R, all intact, none truncated) · 23 anchors and 46 tab targets, **0 broken**.

---

## 2. Verdict

> **The conceptual skeleton is sound and unusually disciplined. The defects are concentrated in
> (a) three formal statements that are wrong as written, (b) five places where the code tab teaches a
> different concept than the maths tab, (c) two structural absences that leave whole branches of the
> subject unrepresented, and (d) one rendering fault that may be suppressing the code layer entirely.**

| Dimension | Grade | One-line justification |
|---|---|---|
| Taxonomic frame | **Strong** | Partition by supervision signal is the right top-level cut, held consistently |
| Template discipline | **Strong** | All 5 registers present in 23/23 cards — zero drift |
| Mathematical correctness | **Good** | ~17 of 23 cards fully sound; 3 formal errors, 3 imprecisions |
| Register coherence | **Mixed** | 5 cards where maths and code teach different things |
| Coverage completeness | **Weak** | Entire branches absent; contradicts the "Complete / All Algorithms" claim |
| Evidence integrity | **Weak** | ~30 quantified claims, 0 citations, 0 reproducible |
| Transmission | **At risk** | Likely-invisible code panes; no mobile layout; no keyboard access |

---

## 3. What the artefact gets right

These are load-bearing and should be preserved through any remediation.

1. **The organising concept is correct.** Partitioning by *supervision signal* — labelled / unlabelled /
   partially labelled / reward — is the partition that actually explains why the algorithms differ.
   It is held without exception across all four units.
2. **The five-register card is applied with perfect regularity.** 23/23 cards carry definition, mathematics,
   explanation, exactly 3 examples, and both language tabs. This regularity is itself pedagogy: the reader
   learns where to look, and the format makes cross-algorithm comparison possible.
3. **The three-domain rule (finance · agriculture · medicine) forces transfer.** Presenting each concept in
   three unrelated domains is the single most effective structural choice in the document — it is what
   separates a concept from a recipe.
4. **Notation is stable across cards.** $\mathbf{w}, b, \boldsymbol{\beta}, \lambda, \alpha, \gamma, C, K$
   carry consistent meanings throughout; cross-references between cards (Ridge ↔ Lasso ↔ Elastic Net,
   Decision Tree ↔ Random Forest, Q-Learning ↔ Dyna-Q ↔ Value Iteration) are accurate.
5. **The mathematics is right in the large majority of cards.** Naive Bayes, Logistic Regression, KNN, SVM,
   Decision Tree, Linear Regression, Polynomial Regression, K-Means, DBSCAN, Hierarchical Clustering,
   Apriori, Q-Learning and Value Iteration are all correctly and completely stated.
6. **Navigation integrity is perfect.** Every one of the 23 TOC anchors and all 46 code-tab targets resolves.

---

## 4. Findings — Conceptual accuracy

> Errors in the *formal* register. These are the highest-cost defects: a reader who trusts the maths and
> derives from it will derive something false.

### C-1 · **HIGH** · Label Propagation (3.2) — two different normalisations presented as one equation

The maths box states:

$$T_{ij} = \frac{W_{ij}}{\sum_k W_{ik}}, \qquad \mathbf{T} = D^{-1/2} W D^{-1/2}$$

These are **not** the same matrix. The left expression is the row-stochastic normalisation $T = D^{-1}W$
(Zhu & Ghahramani, 2002 — Label **Propagation**). The right is the symmetric normalisation
(Zhou et al., 2004 — Label **Spreading**). Joining them with a comma asserts an equality that is false
except in the degenerate case of a regular graph.

Compounding this, the update rule and closed form given underneath —
$F^{(t+1)} = \alpha T F^{(t)} + (1-\alpha)Y_0$ and $F^* = (1-\alpha)(I-\alpha T)^{-1}Y_0$ — are **Label
Spreading's**, not Label Propagation's. Label Propagation uses hard clamping and has no $\alpha$.

**The card contradicts its own code tab**, which correctly instantiates `LabelPropagation` (no `alpha`)
and `LabelSpreading` (`alpha=0.2`) as two distinct estimators. The explanation box even names the
distinction correctly. Only the maths box is wrong.

**Fix:** present two labelled equations — hard clamping for Label Propagation, the $\alpha$ recursion with
$\mathcal{S}=D^{-1/2}WD^{-1/2}$ for Label Spreading — and say which sklearn class implements which.

---

### C-2 · **HIGH** · Ridge Regression (1.8) — shrinkage factor attributed to the wrong basis

$$\hat{\beta}_j^{\text{ridge}} = \frac{d_j^2}{d_j^2 + \lambda}\,\hat{\beta}_j^{\text{OLS}} \qquad \text{“(for feature } j\text{)”}$$

The $d_j^2/(d_j^2+\lambda)$ shrinkage factor applies to coordinates in the **SVD / principal-component
basis** of $\mathbf{X}$, where $d_j$ is the $j$-th singular value. It does *not* apply per original feature
— that would require $\mathbf{X}$ to have orthonormal columns, which is precisely the case Ridge exists to
handle the absence of. The parenthetical "(for feature $j$)" turns a correct theorem into a false one.

This matters conceptually: the whole *point* of the SVD view is that Ridge shrinks **low-variance
directions** hardest — a statement about directions in feature space, not about individual columns. As
written, the reader loses the insight and gains a wrong formula.

**Fix:** write $\mathbf{X} = UDV^\top$, state the result in the rotated basis, then say in words:
*"directions of low variance in the data are shrunk most."*

---

### C-3 · **MEDIUM-HIGH** · Lasso Regression (1.9) — soft-threshold argument is not the RSS gradient

$$\hat{\beta}_j = S\!\left(\frac{\partial\,\text{RSS}}{\partial \beta_j},\; \lambda\right)$$

The coordinate-descent update soft-thresholds the **partial residual correlation**
$\rho_j = \mathbf{x}_j^\top(\mathbf{y} - \mathbf{X}_{-j}\boldsymbol{\beta}_{-j})$, then divides by
$z_j = \mathbf{x}_j^\top\mathbf{x}_j$:

$$\hat{\beta}_j = \frac{1}{z_j}\,S(\rho_j,\ \lambda)$$

The RSS gradient is $-2\rho_j + 2z_j\beta_j$ — wrong sign, wrong scale, and it still contains $\beta_j$,
so the stated update is not even a fixed-point iteration. A reader implementing from this formula gets a
diverging loop.

Secondary: the Elastic Net objective omits the conventional $\tfrac12$ on the L2 term, so it does not
reduce to the Ridge objective stated one card earlier at $\alpha=0$.

---

### C-4 · **MEDIUM** · Isolation Forest (2.6) — score ladder is muddled, and disagrees with the code

The card gives three bands: $s\to1$ "very likely anomaly", $s\approx0.5$ "normal observation",
$s\to0$ "definitely not anomaly". In Liu, Ting & Zhou (2008), $s\approx0.5$ means *the sample contains no
distinct anomaly* — a statement about the **dataset**, not about the point — while $s \ll 0.5$ means the
point is safely normal. As printed, two of the three bands claim the same thing and the diagnostic value
of $s\approx0.5$ is lost.

The card then states the decision rule as *"flag as anomaly if $s>$ threshold (commonly 0.6)"*, but the
code tab thresholds by `contamination=0.02` — a quantile rule, not a score rule. The two are never
connected, so the reader cannot map the equation onto the API.

---

### C-5 · **MEDIUM** · Co-Training (3.3) — an attributed bound that is not in the cited paper

> Error bound: $\epsilon_\infty \le \epsilon_1^{(t)} + \epsilon_2^{(t)} + \delta$ (Blum & Mitchell, 1998)

No such inequality appears in Blum & Mitchell (1998). That paper's contribution is a **PAC-learnability
result**: given two views that are conditionally independent given the label, and a weak initial learner
on one view, unlabelled data can boost to arbitrarily low error. The displayed inequality has undefined
terms ($\epsilon_\infty$, $\delta$) and is not derivable from the paper. A named citation attached to a
statement the source does not make is worse than no citation.

---

### C-6 · **MEDIUM** · Self-Training (3.1) — the wrong assumption is named

> "Self-training assumes the classifier's high-confidence predictions are likely correct (the low-density assumption)."

The **low-density separation** assumption says the decision boundary passes through low-density regions
of the input space. That is a geometric claim, and it is what justifies *transductive SVMs* and, indirectly,
entropy minimisation. What self-training actually requires is **confidence calibration** — that high
predicted probability tracks high accuracy — plus smoothness. Naming the wrong assumption breaks the
chain the reader needs in order to understand *why* confirmation bias (correctly flagged two lines above)
is the characteristic failure mode.

---

### C-7 · **LOW-MEDIUM** · Six smaller formal imprecisions

| # | Card | Statement | Correction |
|---|---|---|---|
| a | 1.5 Decision Tree | "ID3/C4.5 use entropy with information gain" | C4.5 uses **gain ratio** — that is the whole point of C4.5 over ID3, correcting IG's bias toward high-cardinality splits. The IG formula is also written only over $\{L,R\}$, while ID3/C4.5 split multiway. |
| b | 1.6 Linear Regression | "normal equation … in $O(p^3)$ time" | $O(Np^2 + p^3)$; forming $\mathbf{X}^\top\mathbf{X}$ dominates whenever $N \gg p$, which is the usual case. |
| c | 2.4 Apriori | "makes $k+1$ database passes" | One pass per candidate level: $k_{\max}+1$ passes, where $k_{\max}$ is the longest frequent itemset. As written it reads as a fixed constant. |
| d | 2.5 FP-Growth | "$O(N)$ space vs $O(2^N)$ candidates in Apriori" | Compares a space bound to a candidate count. FP-tree size is not $O(N)$ in general (worst case: no shared prefixes). |
| e | 1.3 KNN | Weighted vote $\propto 1/d^2$ | Undefined when a query coincides with a training point ($d=0$); the standard guard (return that point's label, or $1/(d+\varepsilon)$) is not mentioned. |
| f | 4.2 REINFORCE | $\nabla_\theta J = \mathbb{E}[\sum_t \nabla_\theta\log\pi_\theta(a_t\vert s_t)\,G_t]$ | For the **discounted** objective stated just above, the unbiased estimator carries $\gamma^t$. Also $G_t$ is used but never defined in the box. |

---

## 5. Findings — Register coherence (maths tab vs. code tab)

> These are the most damaging defects pedagogically, because the code tab is where the reader goes to
> *check their understanding*. When it teaches something else, the check silently fails.

### R-1 · **MEDIUM** · FP-Growth (2.5): the R tab implements a different algorithm

The card teaches FP-Growth. The R pane runs **`eclat()`** — Eclat is a vertical-tidset-intersection miner,
a genuinely different concept from FP-tree prefix-sharing — and the inline comment even says so
("*efficient alternative to Apriori*") without ever flagging that this is **not** the card's subject.
A reader working the R track never meets an FP-tree.

*(Note: `arules` has no FP-Growth; `rCBA::fpgrowth()` does. If no R implementation is used, the tab should
say explicitly that R has no native FP-Growth and that Eclat is being shown as the closest available
vertical miner.)*

### R-2 · **MEDIUM** · Dyna-Q (4.3): the model is not the model the maths describes

Maths box: $M(s,a) = (r_{\text{avg}},\ s'_{\text{most common}})$.
Code: `model[(state, action)] = (reward, next_state)` — the **last observed** transition, overwritten each visit.

The environment is stochastic (`yield_val` carries Gaussian noise; soil drifts by `randint(-1,2)`), so the
learned model is a single noisy draw, not an expectation. The card's own equation says how to fix it; the
code ignores it. Since the entire concept of Dyna-Q is *"planning is only as good as your model,"* this is
the one card where the gap actively teaches the wrong lesson.

Two further deviations in the same pane: the planning gate is `if len(model) >= n_plan and n_plan > 0`,
which suppresses planning until 20 *distinct* $(s,a)$ pairs have been seen (the algorithm requires only
$\ge 1$); and the R tab gates on `length(M) >= 2` instead — the two language tracks do not implement the
same procedure.

### R-3 · **MEDIUM** · Q-Learning (4.1): the action semantics in the code are not the ones described

```python
water_added = [0, 5, 10, 20][action]     # computed…
water_cost  = [0, 0.8, 1.5, 2.8][action]
new_moisture = min(4, max(0, moisture + action - int(0.3*temp+0.5)))
                                #  ^^^^^^ …and never used
```

The dynamics advance moisture by the **action index** (0–3), while `water_added` (0/5/10/20 mm) is dead.
So the environment the agent solves is not the irrigation environment described in the header comment or
in the example card ("*Actions: irrigate 0/5/10/20 mm*"). The cost vector *does* use the real amounts, so
the reward function and the transition function disagree about what an action means.

### R-4 · **LOW-MEDIUM** · Label Propagation (3.2) — see C-1; the code is right and the maths is wrong.

### R-5 · **LOW** · Value Iteration (4.4): rewards and transitions drift from the stated MDP

The maths uses $R(s,a,s')$; the code uses `R[s,a]`. (Harmless — the expectation collapses — but the reader
comparing the two will look for the missing index.) More substantively, `P[s,a] /= P[s,a].sum()` force-
renormalises every row, which conceals that the hand-constructed probabilities do not sum to 1 and makes
"improve response" a silent no-op for good-response states. A worked MDP should have rows that sum to 1
*by construction*; renormalisation hides modelling errors from the learner.

### R-6 · **LOW** · REINFORCE (4.2): `log_prob()` is defined and never called.

The one method that would show the reader the link between $\log \pi_\theta$ and the analytic gradient is
dead code. The gradient is instead hand-derived inline, so the connection to the policy-gradient theorem
above it is left implicit.

---

## 6. Findings — Conceptual coverage

> The header claims *"Every Data Scientist Must Know"*, *"Complete Self-Study Notes"*, *"All Algorithms"*.
> Judged against that claim, these are gaps, not choices.

### G-1 · **HIGH** · Unit 2 contains no dimensionality reduction or latent-variable modelling

Unit 2 is defined as *"Discover hidden structure and patterns in unlabelled data."* It then covers
clustering, association rules and anomaly detection — and **nothing else**. Absent:

- **PCA / SVD** — the single most-used unsupervised method in practice, and the one the Ridge card
  (C-2) already implicitly depends on;
- **Gaussian Mixture Models / EM** — the probabilistic generalisation of K-Means, which is what makes
  K-Means' "spherical, equally-sized clusters" limitation (correctly noted in card 2.1) *understandable*
  rather than merely stated;
- **t-SNE / UMAP** — manifold learning, which is the assumption Label Propagation (3.2) is built on;
- **Autoencoders** — the bridge to representation learning.

This is the largest single gap. Three cards elsewhere in the document lean on concepts that live here.

### G-2 · **HIGH** · No boosting anywhere — the ensemble concept is presented half-formed

Random Forest (1.10) teaches **bagging** (variance reduction through decorrelation). Its counterpart —
**boosting** (bias reduction through sequential residual fitting) — has no card: no AdaBoost, no Gradient
Boosting, no XGBoost/LightGBM. The Decision Tree card (1.5) even ends by naming "Gradient Boosted Trees"
as a downstream use, pointing at a card that does not exist. Without both halves, "ensemble" is not
actually taught — only one instance of it is.

### G-3 · **HIGH** · No unit on evaluation, validation and model selection

Every card *assumes* this material and none teaches it. The document uses, without ever defining:
AUC-ROC, precision/recall/F1, cross-validation, OOB error, $R^2$ and adjusted $R^2$, silhouette score,
stratification, `class_weight='balanced'`, train/test splitting. It states "found via cross-validation"
in six separate cards as if cross-validation were a primitive.

Missing as first-class concepts: the **bias–variance decomposition** (invoked by name in five cards),
**data leakage**, **class imbalance**, **metric selection under asymmetric cost**, **probability
calibration**, **nested CV for honest hyperparameter selection**.

For a self-study reader, this is the difference between being able to run the code and being able to
*trust* a result.

### G-4 · **MEDIUM** · No preprocessing / feature-engineering concept

"Feature scaling is critical" is asserted in KNN (1.3), K-Means (2.1) and Ridge (1.8) — three times, never
explained, never given a home. Also absent: categorical encoding, missing-data strategy, outlier handling,
and the fit-on-train/transform-on-test discipline that the code panes correctly demonstrate but never name.

### G-5 · **MEDIUM** · Unit 4 omits SARSA, leaving "off-policy" undefined by contrast

Q-Learning's headline tag is **Off-Policy**. Nothing in the unit is on-policy TD, so the reader has no
contrast class and the tag carries no information. SARSA is the missing card. Policy Iteration is likewise
mentioned only in prose (4.4's explanation box) despite being the natural partner to Value Iteration.

### G-6 · **MEDIUM** · Unit 1 shows each tree concept in only one modality

Decision Tree appears **only** as a classifier (1.5); Random Forest **only** as a regressor (1.10). Both
span both tasks, and the document never says so. The reader is left to infer that trees classify and
forests regress. A single sentence in each card would close this.

### G-7 · **MEDIUM** · No neural-network concept, yet the examples depend on one

The notes reference DQN (4.1), "CNN embeddings" (3.3 medical example) and function approximation (4.4)
as if neural networks had been introduced. They have not. Either the references should be removed or a
foundational card (perceptron → MLP → backpropagation) added.

### G-8 · **LOW** · Unit 3 alone has no subsection layer

Units 1, 2 and 4 group their cards (Classification/Regression; Clustering/Association/Anomaly;
Model-Free/Model-Based). Unit 3's three cards sit flat. The natural — and conceptually useful — split is
**inductive** (Self-Training, Co-Training: produce a reusable classifier) vs **transductive**
(Label Propagation: label *this* unlabelled set only). That distinction is currently invisible, and it is
the distinction that determines which method a reader should pick.

### G-9 · **LOW** · Taxonomic placements are never justified

Association-rule mining and anomaly detection are placed under "Unsupervised Learning". Both placements
are defensible, but neither is argued — and anomaly detection in particular is routinely supervised or
semi-supervised. In a document whose top-level organising principle *is* the taxonomy, the boundary cases
are exactly where a sentence of justification pays off.

---

## 7. Findings — Evidence integrity

### E-1 · **HIGH** · ~30 quantified performance claims, zero citations, zero reproducible

Across the 69 example cards, roughly thirty carry hard numbers stated as established fact:

> "Naive Bayes yields **94.2% accuracy**" (569 biopsy samples) · "**79% accuracy**" (768 patient records) ·
> "SVM … **97.3%** overall accuracy" · "**reducing trial-and-error prescribing by 40%**" ·
> "**reduces water use by 25%** while maintaining **98%** of maximum yield" ·
> "**reduces false positives** vs rule-based systems **by 60%**" ·
> "outperforming fixed-dose guidelines **by 18%**" · "reducing viral load **22% better** than standard care"

None carries a source. The accompanying code panes generate **synthetic data via `np.random`**, so not one
of these figures can be reproduced from the document itself. Several evoke well-known public datasets
without naming them — "569 biopsy samples … cell-nucleus features (radius, texture, perimeter)" is
Wisconsin Diagnostic Breast Cancer; "768 patient records … glucose, BMI, age, blood pressure" is Pima
Indians Diabetes — but the code does not load them.

The clinical claims are the most serious: *"reducing trial-and-error prescribing by 40%"* and
*"outperforming fixed-dose guidelines by 18%"* are assertions about medical outcomes presented to a
learner as settled fact.

**Fix (choose one per claim):** cite the source; or load the named public dataset in the code so the
figure is reproducible; or reword as illustrative — *"a model of this kind typically reaches…"*.

### E-2 · **MEDIUM** · Footer statistics contradict the document

The footer reads **"4 Units · 20 Algorithms · 60 Real-World Examples"**. The document contains
**23 algorithms** (unit headers correctly say 10 + 6 + 3 + 4) and **69 examples** (23 × 3). The footer
appears to be left over from an earlier draft.

### E-3 · **MEDIUM** · Isolation Forest demo is handed the answer it should estimate

`contamination=0.02` exactly equals the injected fraud rate (200 / 10,000), and the pane then reports
precision, recall and F1 as if they were earned. The `contamination` parameter is the *unknown* in any
real deployment; setting it to ground truth makes the reported metrics uninformative. Worth either a
sensitivity sweep or an explicit note.

### E-4 · **LOW** · Internal inconsistency in a repeated dataset

"**569** biopsy samples" (card 1.1) and "**568** samples" (card 1.4) describe what reads as the same
tumour dataset.

### E-5 · **LOW** · Currency and register inconsistencies

The house-price example (1.6) is denominated in **€** under a heading labelled *Financial*, while every
other financial example uses **$**. Spelling is consistently British (`-ise`) except a single
`maximizes` in card 1.1.

---

## 8. Findings — Concept transmission (delivery layer)

> A correct concept that does not render is not transmitted. These are ranked by how much of the content
> they put at risk.

### T-1 · **HIGH** · The code panes are probably rendering as light-grey text on white

The markup is:

```html
<div class="code-pane" id="nb-py"><pre><code class="language-python"> … </code></pre></div>
```

The `language-*` class is on `<code>`, but every Prism theme paints the block background, padding and
horizontal scrolling through **`pre[class*="language-"]`** — a selector this `<pre>` does not match. The
theme's `code[class*="language-"] { color: #ccc }` *does* match. The page's own rule
(`.code-pane pre { margin:0; border-radius:0; max-height:480px; overflow-y:auto }`) sets no background.

Net effect: `#ccc` text on the white card background — a contrast ratio near 1.6:1 — with no horizontal
scroll, so long lines are clipped rather than scrollable. **This puts all 46 code panes at risk**, i.e. one
of the five registers for every concept in the document.

*Confidence: high, from the selector structure common to all Prism themes. The CDN was unreachable from
the audit environment, so this should be confirmed with one look in a browser before fixing.*

**Fix:** move the class to the `<pre>` (`<pre class="language-python"><code class="language-python">`),
or add `.code-pane pre { background:#2d2d2d; padding:1em; overflow:auto; }`.

### T-2 · **MEDIUM** · Every copied snippet ends with the word "Copy"

The copy button is appended **inside** the `<pre>`, and the handler reads `pre.textContent.trim()` — which
includes the button's own label. Readers pasting a snippet into an editor get a trailing `Copy` (or
`✓ Copied` if they click twice), producing a syntax error on the last line.

**Fix:** append the button to a positioned wrapper around the `<pre>`, or copy from the `<code>` element.

### T-3 · **MEDIUM** · A global helper shadows a built-in browser API

```js
function scrollTo(id) { … }
```

Declared at global scope, this replaces **`window.scrollTo`**. Any subsequent call to
`window.scrollTo(x, y)` — from the page, a library, or the browser's own scroll restoration — hits this
function instead. Rename to `scrollToUnit`.

### T-4 · **MEDIUM** · One media query in the entire stylesheet; no mobile layout

The only breakpoint is `@media(max-width:900px){ .examples-grid{ grid-template-columns:1fr } }`. The
sidebar remains `width:270px; position:sticky; height:100vh` at every viewport, so on a phone the notes
render in a narrow column beside a full-height navigation rail. For a self-study resource — read on
phones as much as on desktops — this is a substantial accessibility-of-content problem.

### T-5 · **MEDIUM** · No keyboard or assistive-technology access to navigation

The TOC unit headers and the four header pills are `<div onclick="scrollTo(…)">` with no `role`,
`tabindex`, or key handler. The file contains **zero** `aria-*` or `role` attributes. Keyboard and screen-
reader users cannot reach the primary navigation.

### T-6 · **LOW** · Invalid HTML that browsers currently forgive

458 raw `<-` (R assignment), unescaped `&&` and `&` in R code, and `$<1$` in the Apriori lift note are
emitted without escaping. Browsers recover — `<` before `-` or a digit is not a tag open — but the file is
not valid HTML, and any strict parser, sanitiser, feed generator, or documentation pipeline will mangle
these blocks. `&lt;` is used in only 3 places in the whole file.

### T-7 · **LOW** · Latent MathJax hazard from currency symbols

12 unpaired `$` appear in prose and tables (`Amount ($)`, `+$1,850`, `$3,200`). Each currently sits alone
in its own table cell, so MathJax finds no closing delimiter and leaves them alone. Adding a second
currency value to any one of those cells would silently render the text between them as italic maths.
Escape as `\$` or `&#36;`. Relatedly, the MathJax config overrides `skipHtmlTags` and **drops `code`** from
the default list; this is safe only because every `<code>` happens to sit inside a `<pre>`.

### T-8 · **LOW** · A planned component was dropped, and the cards need it

`.note-callout`, `.key-points` and `.kp` are fully styled in the CSS and used **nowhere** in the document.
The "key points" chip row is precisely what several cards need to carry assumptions and failure modes
(see the Recommendations). The styling already exists.

### T-9 · **LOW** · Missing metadata for a public resource

No `<meta name="description">`, no Open Graph/Twitter tags, no `prefers-color-scheme` support, no print
stylesheet. All four matter for a document published on GitHub Pages and intended for extended reading.

---

## 9. Findings — Repository

| # | Sev | Finding |
|---|---|---|
| P-1 | **MEDIUM** | `index.html` and `ml_self_study_notes.html` are **byte-identical** (`a99eeb90…`) — two 252 KB copies of one document. They will diverge on the first edit that touches only one. Keep `index.html` as canonical; make the other a redirect stub, or delete it. |
| P-2 | **LOW** | `README.md` is a single bare URL (46 bytes). No title, abstract, unit list, audience statement, licence, or contribution note. |
| P-3 | **LOW** | No `LICENSE` — for an educational resource intended to be shared and reused, the reuse terms are undefined. |
| P-4 | **LOW** | No CI. An HTML validator + link checker on push would have caught T-6, and a headless-browser screenshot diff would catch T-1. |
| P-5 | **LOW** | No `.gitignore`, no `CHANGELOG.md`. |

---

## 10. Prioritised remediation plan

**Tier 1 — correctness and transmission (do first; small, bounded, high value)**

1. **T-1** Confirm and fix the code-pane rendering. One CSS rule or one class move. Unblocks 46 panes.
2. **C-1 / C-2 / C-3** Correct the three wrong equations (Label Propagation normalisation, Ridge SVD
   basis, Lasso soft-threshold argument). Three edits.
3. **E-2** Fix the footer to `4 Units · 23 Algorithms · 69 Real-World Examples`.
4. **T-2 / T-3** Move the copy button outside `<pre>`; rename `scrollTo` → `scrollToUnit`.
5. **C-5** Remove or correct the Blum & Mitchell attribution.

**Tier 2 — register coherence (medium effort, restores the code tab's teaching role)**

6. **R-3** Use `water_added` in the Q-Learning transition, or renumber the actions to match.
7. **R-2** Store running averages / modal successors in the Dyna-Q model, per the card's own equation;
   align the Python and R planning gates.
8. **R-1** Either implement FP-Growth in R (`rCBA::fpgrowth`) or add an explicit note that Eclat is being
   substituted and why.
9. **C-4 / C-6 / C-7** Correct the Isolation Forest score bands, the self-training assumption name, and
   the six smaller imprecisions.
10. **E-1** Resolve the ~30 unsourced metrics: cite, make reproducible by loading the named public
    dataset, or reword as illustrative. Prioritise the clinical claims.

**Tier 3 — coverage (this is the work that changes the document's standing)**

11. **G-3** Add a cross-cutting **Unit 0: Foundations & Evaluation** — bias–variance, cross-validation,
    metrics, leakage, imbalance, calibration. Every existing card already depends on it.
12. **G-1** Add a *Dimensionality Reduction* subsection to Unit 2: PCA/SVD, GMM + EM, t-SNE/UMAP.
13. **G-2** Add a *Boosting* subsection to Unit 1: AdaBoost, Gradient Boosting, XGBoost.
14. **G-5 / G-6** Add SARSA to Unit 4; add one sentence each to 1.5 and 1.10 noting that trees and forests
    both span classification and regression.
15. **G-8** Split Unit 3 into **Inductive** (Self-Training, Co-Training) and **Transductive**
    (Label Propagation) — matching the other three units and surfacing the distinction that governs
    method choice.
16. **G-4 / G-7** Add a preprocessing card; and either add a neural-network foundation card or remove the
    forward references to DQN and CNN embeddings.

**Tier 4 — presentation and repository**

17. **T-4 / T-5** Add a mobile breakpoint that collapses the sidebar; give the nav elements `role="button"`,
    `tabindex="0"` and key handlers.
18. **T-8** Revive `.key-points` — add an assumptions / failure-modes chip row to each card. The CSS exists.
19. **T-6 / T-7 / T-9** Escape `<`, `&` and currency `$`; add description and Open Graph meta.
20. **P-1 / P-2 / P-3 / P-4** De-duplicate the HTML; write a real README; add a licence; add a validator +
    link-checker CI job.

---

## 11. One structural recommendation

Beyond the defect list, the highest-leverage change to the document *as a concept map* is to make each
card state **what it assumes and where it fails**. The five current registers say what a method *is* and
what it *does*; none says when it *breaks*.

That knowledge is already scattered through the explanation boxes — K-Means "assumes spherical,
equally-sized clusters", Naive Bayes' independence assumption, self-training's confirmation bias, Dyna-Q's
model error under non-stationarity — but it is buried in prose, inconsistent between cards, and absent
from several. Promoting it to a sixth register (a chip row, using the `.key-points` CSS that already
exists and is already unused) would:

- make the cards **comparable** on the axis that actually governs method selection;
- give the missing Unit 0 (G-3) something concrete to connect to in every card;
- convert the notes from a reference — *what is Ridge?* — into a decision aid — *should I use Ridge here?*

That is the difference between notes a reader can recall and notes a reader can apply.

---

*Audit performed by static analysis of the committed HTML: full structural extraction of the unit →
subsection → card tree; cross-reading of all 23 definition, mathematics and explanation blocks against
canonical sources; extraction and review of all 69 examples and all 46 code panes; and checks of anchors,
tab targets, escaping, MathJax delimiter pairing, stylesheet selectors, and repository hygiene. No code
was executed. Finding T-1 rests on the selector structure common to all Prism themes; the CDN was
unreachable from the audit environment, so it is flagged for one browser confirmation before the fix.*
