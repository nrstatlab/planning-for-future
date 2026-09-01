# Unit 4 — Supervised Learning: Classification

**Syllabus topics:** Introduction of supervised learning; classification
model and learning steps; classification algorithms — Naïve Bayes classifier,
k-Nearest Neighbour (kNN), decision tree, support vector machines, random
forest.

---

## 4.1 A note on the overlap with Course 8

**Three of the five algorithms here were taught in Course 8**, and that unit
traced them by hand.

| Algorithm | Course 8 | What is new here |
|---|---|---|
| **Decision tree** | §4.3–4.5 — ID3, C4.5, CART, with entropy and information gain computed by hand | **Pruning, overfitting, and how to know**. The arithmetic is revision |
| **Naive Bayes** | §4.7 — the posterior computed by hand | **Variants (Gaussian, Multinomial), and Laplace smoothing** |
| **k-NN** | §4.6 | **Scaling, and choosing k** |
| **SVM** | — | **New** — §4.6 |
| **Random forest** | — | **New**, and the introduction to ensembles — §4.7 |

**The difference in framing is the point.** Course 8 asked *how does ID3 choose
a split?* — arithmetic. This course asks *is this tree overfitting, and how
would you know?* Both are examined, in different words.

If you took Course 8, spend your time on **SVM and random forest**, and on the
evaluation habits from Unit 2.

---

## 4.2 Introduction of supervised learning

### 🎯 What makes learning "supervised"

**Supervised learning is learning a mapping from features to a known target,
from examples where the target is given.**

The word *supervised* is the teaching analogy of Unit 1 §1.1: a teacher
supplies both the questions and the right answers, and the learner's job is to
generalise from them to questions the teacher never asked.

```
   training                                    prediction
   ────────                                    ──────────
   x₁, y₁                                        x_new
   x₂, y₂   ──►  learning algorithm  ──►  f  ──►   │
   ...                                             ▼
   xₙ, yₙ                                        ŷ = f(x_new)
```

**The whole point is the arrow on the right.** Reproducing y for the rows you
already have is trivial — store them in a dictionary. Supervised learning is
judged only on rows it has never seen, which is why Unit 2's held-out test set
is not a formality.

### 🔢 The two supervised tasks

| | **Classification** | **Regression** |
|---|---|---|
| Target | **Discrete** — a category | **Continuous** — a number |
| Output | setosa / versicolor / virginica | 75.3 marks |
| Metric | Accuracy, precision, recall, F1, AUC | RMSE, MAE, R² |
| Unit | **This one** | Unit 3 |

### 🔢 The vocabulary, restated for this unit

| Term | Means |
|---|---|
| **Hypothesis space** | The set of functions the algorithm is allowed to choose from — all straight lines, all trees of depth ≤ 3 |
| **Inductive bias** | The assumptions that make generalisation possible at all |
| **Training error** | Error on the data used to fit |
| **Generalisation error** | Error on unseen data — **the only one that matters** |

### 💡 Inductive bias — why learning is impossible without an assumption

Given any finite set of examples, **infinitely many functions fit them all**
and disagree everywhere else. Nothing in the data alone can choose between
them.

**So every algorithm must assume something**, and that assumption is its
*inductive bias*:

| Algorithm | Its inductive bias |
|---|---|
| Linear regression | The relationship is **linear** |
| Decision tree | The target is captured by **axis-parallel splits** |
| k-NN | **Nearby points share a label** |
| Naive Bayes | Features are **conditionally independent** given the class |
| SVM (RBF) | The boundary is **smooth** |

**This is the "no free lunch" theorem in practical terms: no algorithm is best
on every problem**, because being better on one class of problems means holding
an assumption that is wrong on another. That is why Unit 2 insists on
measuring rather than believing, and it is a legitimate five-mark answer.

## 4.3 The classification model and its learning steps

### 🔢 The steps

```
 1. Define the problem      what classes? what does a mistake cost?
 2. Collect and label       the labels ARE the expense
 3. Split                   train / validation / test  ← BEFORE anything else
 4. Preprocess              impute, encode, scale (fit on train only)
 5. Train                   fit on the training set
 6. Tune                    hyperparameters, on VALIDATION folds
 7. Evaluate                on the test set, ONCE
 8. Deploy and monitor      watch for drift
```

Steps 3 to 7 are Unit 2, and they matter more than the choice made at step 5.

### 💡 Binary, multi-class, multi-label — three different things

| | Classes | Each instance gets |
|---|---|---|
| **Binary** | 2 | One of two labels |
| **Multi-class** | k > 2, mutually exclusive | **Exactly one** of k |
| **Multi-label** | k, **not** exclusive | **Any number** of k |

Iris is multi-class — a flower is one species. Tagging an article
"politics, economics" is multi-label, and needs a different model setup (`k`
independent binary classifiers), not just a different metric.

---

## 4.4 Naive Bayes

### 🔢 Bayes' theorem, applied

> **P(class | features) = P(features | class) × P(class) / P(features)**

| Term | Name |
|---|---|
| P(class \| features) | **Posterior** — what we want |
| P(features \| class) | **Likelihood** |
| P(class) | **Prior** |
| P(features) | Evidence — the same for every class, so it can be **dropped** for comparison |

### 🎯 What "naive" means

**It assumes every feature is conditionally independent of every other, given
the class.** That lets the likelihood factorise:

> **P(x₁, x₂, …, xₚ | C) = P(x₁|C) × P(x₂|C) × … × P(xₚ|C)**

**The assumption is almost always false** — in text, "New" and "York" are
plainly not independent. Naive Bayes works well anyway, because for
*classification* you only need the correct class to have the highest score, not
the probabilities to be right. It is a famously biased and famously useful
estimator.

### ⚠️ The zero-frequency problem, and Laplace smoothing

If a feature value never occurs with a class in training, its conditional
probability is 0 — and since the likelihood is a **product**, one zero makes
the entire posterior zero, whatever the other features say.

**Laplace (add-one) smoothing** fixes it:

> **P(xᵢ | C) = (count + α) / (total + α × number of distinct values)**

with α = 1 the usual choice. In scikit-learn this is the `alpha` parameter.

**This is a guaranteed exam question**, and the reason it matters — *a product
is destroyed by a single zero* — is the half of the answer people omit.

### 🔢 The variants

| Variant | Features | Use for |
|---|---|---|
| **GaussianNB** | Continuous; assumes each is normal within a class | Numeric data — iris |
| **MultinomialNB** | Counts | **Text** — word counts, TF-IDF |
| **BernoulliNB** | Binary | Text as presence/absence |
| CategoricalNB | Discrete categories | Categorical tables |

### 💡 Why Naive Bayes owns spam filtering

Text has tens of thousands of features (one per word) and few examples relative
to that. Naive Bayes is **linear in the number of features**, needs little
data, trains in one pass, and updates incrementally as new mail is labelled.
The independence assumption is wrong and does not stop it working.

---

## 4.5 k-Nearest Neighbours

### 🎯 The idea

**Store the training set. To classify a new point, find its k nearest
neighbours and take a majority vote.**

There is no model. Fitting stores the data; all the work happens at prediction
time — which is why it is called a **lazy** learner, and an
**instance-based** or **non-parametric** method.

| | **Lazy (k-NN)** | **Eager (tree, NB, SVM)** |
|---|---|---|
| Training | **Instant** — just stores | Slower — builds a model |
| Prediction | **Slow** — O(n) distances per query | Fast |
| Memory | Holds **all** training data | Holds the model only |
| New data | Just append it | Retrain |

### 🔢 Distance metrics

| Metric | Formula | Use |
|---|---|---|
| **Euclidean** | √Σ(xᵢ − yᵢ)² | The default; continuous features |
| **Manhattan** | Σ\|xᵢ − yᵢ\| | High dimensions; grid-like data |
| Minkowski | (Σ\|xᵢ − yᵢ\|^p)^(1/p) | General — p=2 Euclidean, p=1 Manhattan |
| **Cosine** | 1 − (a·b)/(\|a\|\|b\|) | **Text**, where direction matters and length does not |
| Hamming | Count of differing positions | Categorical |

### ⚠️ Scaling is not optional for k-NN — measured

A dataset of **age in years** and **income in rupees**, where the true rule
depends on **age only**:

| | Test accuracy |
|---|---:|
| **Unscaled** | **0.5500** |
| **Scaled** | **0.9750** |

Income's standard deviation is **42,669×** age's, so Euclidean distance is
determined almost entirely by income — which is irrelevant. The classifier is
barely better than a coin flip.

### 💡 But iris is a bad example of this, and it is worth knowing why

On iris, unscaled k-NN (k=5) scores **0.9778** and scaled scores **0.9111** —
scaling *hurt*. Iris's four features are all in centimetres with standard
deviations spanning only **4.05×**, so there was no imbalance to correct and
the small change is noise on a 45-row test set.

**The rule is about units, not ritual.** Scale when features are on genuinely
different scales; iris is the case where it barely matters.

### 🔢 Choosing k

| k | Effect |
|---|---|
| **k = 1** | Zero training error, **very high variance** — every noisy point gets its own region |
| **Small k** | Flexible, low bias, high variance |
| **Large k** | Smooth, high bias, low variance |
| **k = n** | Always predicts the majority class |

**k is a hyperparameter**, chosen on validation folds. Use an **odd** k for
binary problems to avoid ties. A common heuristic is k ≈ √n, but validate it.

⚠️ **k-NN degrades badly in high dimensions** — the curse of dimensionality
(Unit 1 §1.7) makes all points roughly equidistant, and "nearest" stops meaning
anything.

---

## 4.6 Support Vector Machines

### 🎯 The idea

**Find the hyperplane that separates the classes with the widest possible
margin.**

```
        ●  ●                    │ ← the maximum-margin hyperplane
     ●     ●    ○          │    │    │
  ●    ● ○     ○      ─────┼────┼────┼─────
       ●    ○   ○          │    │    │
          ○  ○             ↑    ↑    ↑
                        margin  │  margin
                          support vectors
```

Of the infinitely many separating lines, SVM chooses the one **furthest from
both classes**. The intuition: the widest margin is the most robust to a new
point landing slightly off.

### 🔢 Support vectors

**Only the points on the margin matter.** They are the *support vectors*, and
they alone define the hyperplane — remove any other training point and the
solution is unchanged.

**That is SVM's defining property**, and the answer to "why is it called a
support vector machine?"

### 🔢 Hard margin, soft margin, and C

Real data is not perfectly separable, so SVM allows violations, penalised by
**C**:

| C | Margin | Behaviour |
|---|---|---|
| **Small C** | **Wide**, more violations tolerated | More regularised, **higher bias**, may underfit |
| **Large C** | **Narrow**, few violations | **Higher variance**, may overfit |

**C is inversely a regularisation strength**, which is the opposite direction
from `alpha` in Ridge — a common source of confusion.

### 🔢 The kernel trick

For data not linearly separable, map it into a higher-dimensional space where
it is. **The trick is that the mapping is never computed** — the algorithm only
needs inner products, and a kernel function computes those directly.

| Kernel | Form | Use |
|---|---|---|
| **Linear** | x·y | Many features, text. **Try this first** |
| **RBF (Gaussian)** | exp(−γ‖x−y‖²) | **The general-purpose default** |
| Polynomial | (x·y + c)^d | Occasionally |
| Sigmoid | tanh(...) | Rare |

**γ (gamma) controls the reach of one training point.** Large γ = each point
influences only its immediate neighbourhood = a wiggly boundary that overfits.
Small γ = smoother.

⚠️ **SVM requires scaling** — the kernel is a distance function.

| Property | SVM |
|---|---|
| Strong when | p is large relative to n; a clear margin exists; text |
| Weak when | n is very large (training is roughly O(n²)–O(n³)) |
| Probabilities | Not natively — needs Platt scaling (`probability=True`, and it is slow) |
| Interpretability | Low, except with a linear kernel |

---

## 4.7 Random forest

### 🎯 The idea

**Many decision trees, each on a different bootstrap sample and each choosing
splits from a random subset of features. Predict by majority vote.**

Random forest is **bagging** (Unit 2 §2.6) plus one extra idea.

### 🔢 The two sources of randomness — and why the second matters

1. **Bootstrap sampling.** Each tree trains on n rows drawn *with replacement*,
   so each sees about **63.2%** of the distinct rows.
2. **Random feature subsets.** At **every split**, only √p features (for
   classification) are considered.

**The second is what makes it a *random forest* rather than plain bagging.**
Without it, if one feature is strongly predictive, every tree splits on it
first and all the trees look alike — and averaging near-identical trees reduces
nothing. Forcing each split to ignore most features **decorrelates** the trees,
and it is the decorrelation that makes the average work.

**That is the question examiners ask, and the half most answers miss.**

### 🔢 Out-of-bag error — cross-validation for free

Each tree omits about 36.8% of the rows. Predicting each row using only the
trees that did *not* see it gives an unbiased estimate at no extra cost
(`oob_score=True`).

> *Where 63.2% comes from:* the chance a given row is never drawn in n draws
> with replacement is (1 − 1/n)ⁿ → **1/e ≈ 0.368**. So about 63.2% are in the
> sample, and 36.8% are out of bag.

### 💡 Feature importance, with a warning

Random forests report feature importance from impurity decrease — but it is
**biased toward high-cardinality and continuous features**, which simply offer
more places to split. **Permutation importance is more trustworthy**, and Unit
2 §2.4 says so too.

### ⚠️ A measured caution: the fancy model does not always win

On iris, with a 45-row test set:

| Model | Test accuracy | 5-fold CV |
|---|---:|---:|
| Decision tree (depth 3) | **0.9778** | 0.9600 ± 0.0249 |
| **Random forest (100 trees)** | **0.8889** | 0.9467 ± 0.0267 |
| k-NN (k=5, scaled) | 0.9111 | **0.9733 ± 0.0249** |
| Gaussian NB | 0.9111 | 0.9467 ± 0.0400 |
| SVM (RBF) | 0.9333 | 0.9600 ± 0.0389 |

**Random forest came last on the test split.** Two lessons, both examinable:

1. **On a small, clean, nearly-separable dataset an ensemble has nothing to
   fix.** Iris is not a problem that needs 100 trees.
2. **A 45-row test split is noise.** The CV column tells a different story
   (0.9467 for the forest, not 0.8889), and the standard deviations overlap
   almost entirely — **these models are not meaningfully different on this
   data**, and claiming a winner from one split would be wrong.

**Saying that is a better answer than naming a winner.**

---

## 4.8 Choosing a classifier

| Algorithm | Fast to train | Fast to predict | Needs scaling | Interpretable | Handles non-linear |
|---|---|---|---|---|---|
| **Naive Bayes** | **Very** | **Very** | No | Moderate | Limited |
| **k-NN** | **Instant** | **Slow** | **Yes** | Moderate | **Yes** |
| **Decision tree** | Fast | **Very fast** | **No** | **High** | **Yes** |
| **SVM** | Slow on large n | Fast | **Yes** | Low | **Yes** (kernel) |
| **Random forest** | Moderate | Fast | **No** | Low | **Yes** |
| Logistic regression | Fast | **Very fast** | For regularisation | **High** | No |

### 💡 A practical order to try things

1. **A dummy classifier** — the baseline (Unit 2 §2.5). Not optional.
2. **Logistic regression** or **Naive Bayes** — fast, interpretable, often
   enough.
3. **Random forest** — strong default on tabular data, few knobs.
4. **Gradient boosting** — usually the best on tabular data, more tuning.
5. **SVM** — when p is large relative to n.

**Never start at step 4.** You will not know whether the complexity bought
anything, and the answer is often that it did not.

---

## Practice problems

### Problem 1

Explain the Naive Bayes classifier. What does "naive" mean, and what is the
zero-frequency problem? *(10 marks)*

**Solution.**

**Start from Bayes' theorem** — P(C|X) = P(X|C)P(C)/P(X) — naming posterior,
likelihood, prior and evidence, and noting the evidence is identical across
classes so it can be dropped when comparing.

**"Naive" means the conditional independence assumption:** every feature is
assumed independent of every other given the class, so
P(x₁,…,xₚ|C) = ∏P(xᵢ|C). Say plainly that **the assumption is almost always
false** — "New" and "York" are not independent — and that it works anyway,
because classification needs only the *correct class to score highest*, not the
probabilities to be accurate.

**The zero-frequency problem:** if a feature value never occurs with a class in
training, P(xᵢ|C) = 0, and since the likelihood is a **product**, that single
zero drives the whole posterior to zero regardless of every other feature.

**Laplace (add-one) smoothing** is the fix:

> P(xᵢ|C) = (count + α) / (total + α × number of distinct values)

with α = 1 typical. Add the variants — **Gaussian** for continuous features,
**Multinomial** for counts (text), **Bernoulli** for binary — and why Naive
Bayes suits spam filtering: linear in the number of features, trains in one
pass, needs little data, updates incrementally.

### Problem 2

Explain k-NN. How is k chosen, and why does scaling matter? *(10 marks)*

**Solution.**

**The algorithm:** store the training set; to classify a new point compute its
distance to every training point, take the k nearest, and vote. Emphasise that
**there is no model** — this is a **lazy, instance-based, non-parametric**
learner, and give the lazy-versus-eager table.

**Distance metrics:** Euclidean (default), Manhattan (high dimensions), Cosine
(text, where direction matters and length does not), Hamming (categorical).

**Choosing k:** k = 1 gives zero training error and very high variance; large k
smooths and biases; k = n always predicts the majority. **k is a
hyperparameter, tuned on validation folds**, and odd for binary problems to
avoid ties.

**Why scaling matters — with the number.** On a dataset of age in years and
income in rupees where the true rule depends on **age only**, k-NN scores
**0.5500 unscaled and 0.9750 scaled**. Income's standard deviation is
**42,669×** age's, so Euclidean distance is essentially income alone, and
income is irrelevant.

**Then the nuance that earns the last mark:** on iris, scaling barely matters —
all four features are in centimetres with standard deviations spanning only
4.05×. **The rule is about differing units, not ritual.**

Close with the curse of dimensionality: in high dimensions all points become
roughly equidistant and "nearest" stops meaning anything.

### Problem 3

Explain support vector machines, including the margin, support vectors and the
kernel trick. *(10 marks)*

**Solution.**

**The objective:** of the infinitely many hyperplanes separating two classes,
SVM finds the one with the **maximum margin** — the greatest distance to the
nearest point of either class. The intuition is robustness: the widest margin
best tolerates a new point landing slightly off. Draw it.

**Support vectors** are the points lying on the margin. **They alone define the
hyperplane** — delete any other training point and the solution is identical.
That property is what the algorithm is named after.

**Soft margin and C:** real data is not separable, so violations are allowed
and penalised by C. **Small C = wide margin, more violations tolerated, more
regularised, higher bias. Large C = narrow margin, higher variance.** Note that
C works in the opposite direction to a regularisation `alpha`.

**The kernel trick:** map the data into a higher-dimensional space where it is
separable — but **never compute the mapping**. The algorithm needs only inner
products, and a kernel function computes those directly, which is what makes
the whole thing tractable. Give linear (text, large p), **RBF** (the
general-purpose default), and polynomial, and note that **γ controls the reach
of a single training point**: large γ gives a wiggly, overfitting boundary.

**Finish with the practical points:** SVM **requires scaling** because the
kernel is a distance; training is roughly O(n²)–O(n³) so it is poor for very
large n; and it does not produce probabilities natively.

### Problem 4

Explain random forest. How does it differ from bagging, and what is out-of-bag
error? *(10 marks)*

**Solution.**

**The algorithm:** build many decision trees, each on a bootstrap sample of the
rows, and each choosing its splits from a **random subset of features**;
classify by majority vote.

**Bagging versus random forest — the distinction that is the question.**
Bagging alone gives each tree a different bootstrap sample. Random forest adds
**random feature subsetting at every split** (√p features for classification).

**Why that second source of randomness matters:** with one strongly predictive
feature, every bagged tree splits on it first and all the trees end up alike —
and averaging near-identical trees reduces nothing. Forcing each split to
consider only a subset **decorrelates** the trees, and it is the decorrelation
that makes averaging effective. **This is the half most answers omit.**

**Out-of-bag error:** each bootstrap sample omits about **36.8%** of the rows —
because the chance of never drawing a given row in n draws is (1 − 1/n)ⁿ →
1/e ≈ 0.368. Predicting each row using only the trees that did not see it gives
an unbiased validation estimate **for free**, with no separate split.

**Add the caution, which shows judgement.** On iris a 100-tree forest scored
**0.8889** on the test split against **0.9778** for a single depth-3 tree —
because a small, clean, nearly-separable dataset gives an ensemble nothing to
fix, and because a 45-row test split is noise. The cross-validated figures
(0.9467 ± 0.0267 against 0.9600 ± 0.0249) overlap almost entirely, so **the
honest conclusion is that these models are not meaningfully different on this
data** — not that one won.

---

## Exam questions from this unit

**Two marks**

1. What assumption makes Naive Bayes "naive"?
2. What is Laplace smoothing for?
3. Why is k-NN called a lazy learner?
4. What is a support vector?
5. What does the C parameter control in an SVM?
6. What fraction of rows is out of bag, and why?
7. Which of the five algorithms need feature scaling?

**Five marks**

1. Explain the steps of building a classification model.
2. Distinguish binary, multi-class and multi-label classification.
3. Explain the kernel trick.
4. How would you choose k in k-NN?
5. Distinguish bagging from random forest.
6. Compare any three classifiers on speed, scaling and interpretability.

**Ten marks**

1. Explain Naive Bayes, the naive assumption and the zero-frequency problem.
2. Explain k-NN, choosing k, and why scaling matters.
3. Explain SVMs — margin, support vectors, soft margin and kernels.
4. Explain random forest, its two sources of randomness, and out-of-bag error.

---

## Mistakes that cost marks

- **Saying the naive assumption is usually true.** It is usually false, and
  Naive Bayes works anyway — that is the interesting part.
- **Explaining Laplace smoothing without saying why a zero is fatal.** The
  likelihood is a **product**.
- **Forgetting to scale for k-NN or SVM.** 0.5500 against 0.9750.
- **Saying random forest is "just bagging with trees".** The random **feature
  subsetting at each split** is what decorrelates them.
- **Claiming out-of-bag error needs a validation set.** It replaces one.
- **Calling k = 1 the best k.** Zero training error, maximum variance.
- **Confusing C with a regularisation strength.** Larger C means **less**
  regularisation.
- **Naming a winner from one test split.** Quote cross-validated mean ± sd, and
  say when the difference is not meaningful.
