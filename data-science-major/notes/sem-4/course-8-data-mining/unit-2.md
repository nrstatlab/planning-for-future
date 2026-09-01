# Unit 2 — Data Mining and Preprocessing

**Syllabus topics:** What is Data Mining? Definitions, KDD vs Data Mining,
Data Mining Tasks, Data Preprocessing — Data Cleaning, Missing Data,
Dimensionality Reduction, Feature Subset Selection, Discretization and
Binarization, Data Transformation; Measures of Similarity and Dissimilarity —
Basics. Issues and Challenges in DM, DM Applications — Case Studies.

---

## 2.1 What data mining is

### 🎯 The big idea

Data mining is the **extraction of implicit, previously unknown and
potentially useful patterns from large volumes of data**.

Every word in that definition is doing work:

| Word | Why it is there |
|---|---|
| **implicit** | Nobody stored the pattern; it emerges from the data |
| **previously unknown** | A query you already knew to write is *reporting*, not mining |
| **potentially useful** | The pattern must be actionable, not merely true |
| **large volumes** | The techniques exist because the data is too big to eyeball |

### ⚠️ What is *not* data mining

This distinction is examined and students lose marks on it constantly.

| Not data mining | Why |
|---|---|
| `SELECT * FROM customers WHERE city = 'Guntur'` | A query: you knew the question |
| Computing a monthly sales total | Reporting: aggregation of known facts |
| Looking up a phone number | Retrieval |
| Sorting a table | Data processing |
| **Discovering** that Guntur customers buy differently | **This is mining** |

The line is whether the *question* or only the *answer* was unknown. Retrieval
answers a question you posed; mining discovers the question is worth asking.

### 💡 Why the name is a misnomer

You mine *gold* from rock, not *rock* from gold — so the process should be
called "knowledge mining from data". Fayyad and colleagues proposed **KDD**
for exactly that reason. "Data mining" won because it was catchier, and it now
means both the whole process (in industry) and one step of it (in textbooks).
Knowing that both usages exist prevents confusion in the exam.

## 2.2 KDD versus data mining

### 🔢 The KDD process

**KDD** — Knowledge Discovery in Databases — is the whole pipeline. Data
mining is **one step** within it.

```
   Databases          Target       Preprocessed    Transformed     Patterns      Knowledge
  ┌─────────┐          data           data            data
  │ ▓▓▓▓▓▓▓ │  1.Selection  2.Preprocessing  3.Transformation  4.Mining  5.Evaluation
  │ ▓▓▓▓▓▓▓ │ ──────────►  ──────────────►  ──────────────►  ───────►  ─────────►
  └─────────┘
                            └──────────── iterate ────────────┘
```

| Step | What happens | Share of the effort |
|---|---|---|
| 1. **Selection** | Choose the relevant data | 5% |
| 2. **Preprocessing** | Clean, handle missing values and noise | **60%** |
| 3. **Transformation** | Reduce, normalise, derive features | **20%** |
| 4. **Data mining** | Apply the algorithm | **10%** |
| 5. **Interpretation/evaluation** | Judge and present the patterns | 5% |

**Note the proportions.** Preprocessing and transformation are 80% of the
work; the algorithm is 10%. That is not a comment on this course's emphasis —
it is why Unit 2 exists at all, and it is true in every real project.

Some texts split it into seven steps by adding *data cleaning* and
*integration* separately. Either enumeration earns full marks; what matters is
that mining is **one step**, near the end, and that the process **iterates**.

| | KDD | Data mining |
|---|---|---|
| Scope | The **whole** process | **One step** of it |
| Input | Raw databases | Preprocessed, transformed data |
| Output | Actionable knowledge | Patterns |
| Includes | Selection, cleaning, transformation, mining, evaluation | Algorithm application only |

## 2.3 Data mining tasks

Two families, and the split is the most important vocabulary in the course.

### 🔢 Predictive versus descriptive

| | **Predictive** | **Descriptive** |
|---|---|---|
| Goal | Predict an unknown value | Describe the data's structure |
| Has a target variable? | **Yes** | **No** |
| Learning | **Supervised** | **Unsupervised** |
| Tasks | Classification, regression, deviation detection | Clustering, association, summarisation, sequence discovery |
| Evaluated by | Accuracy on unseen data | Interpretability, internal measures |

### The tasks

| Task | Question it answers | Example | Unit |
|---|---|---|---|
| **Classification** | Which *class*? (discrete) | Will this loan default? | 4 |
| **Regression** | What *value*? (continuous) | What will sales be? | — |
| **Clustering** | Which natural groups? | Customer segments | 5 |
| **Association** | What occurs together? | Nappies and beer | 3 |
| **Sequence discovery** | What follows what? | Bought a phone, then a case |  |
| **Deviation/anomaly detection** | What is unusual? | Fraudulent transaction |  |
| **Summarisation** | A compact description | Demographic profile |  |

### ⚠️ Classification versus clustering

The exam asks this every year.

| | Classification | Clustering |
|---|---|---|
| Learning | **Supervised** | **Unsupervised** |
| Classes | **Known** in advance | **Discovered** |
| Training data | Labelled | Unlabelled |
| Output | A model mapping features → a known label | A grouping |
| Evaluation | Accuracy against true labels | Cohesion, separation, silhouette |
| Example | Spam / not spam | Segment customers into k groups |

**One-sentence version:** classification puts records into boxes you already
have; clustering works out what the boxes should be.

### ⚠️ Classification versus regression

Both are supervised. The difference is **the type of the target**:
classification predicts a **discrete label** (pass/fail, three species);
regression predicts a **continuous number** (marks, price, temperature).
Predicting "the exam mark" is regression; predicting "pass or fail" is
classification, even though it is the same underlying quantity.

## 2.4 Data preprocessing

### 🎯 Why it is 60% of the work

Real data is **dirty**, and every algorithm in Units 3–5 assumes it is not.

| Problem | Example |
|---|---|
| **Incomplete** | `income = NULL` for 30% of customers |
| **Noisy** | `age = 215`, `salary = -5000` |
| **Inconsistent** | `M/F` in one source, `1/0` in another; two spellings of one city |
| **Duplicated** | The same customer entered twice with different spellings |
| **Outdated** | An address from six years ago |

**Garbage in, garbage out.** A decision tree built on data where "missing"
was silently replaced by 0 will confidently split on that 0, and the model
will be wrong in a way that no accuracy metric reveals.

### The four preprocessing tasks

| Task | Purpose |
|---|---|
| **Data cleaning** | Fill missing values, smooth noise, resolve inconsistency |
| **Data integration** | Merge multiple sources coherently |
| **Data reduction** | Fewer rows, columns or distinct values — same conclusions |
| **Data transformation** | Normalise, aggregate, discretise, derive |

## 2.5 Data cleaning: missing data

### 🔢 Why values are missing — and why it matters

| Mechanism | Meaning | Safe to drop? |
|---|---|---|
| **MCAR** — missing completely at random | Missingness unrelated to anything | Yes, just loses power |
| **MAR** — missing at random | Related to *observed* variables | With care, using those variables |
| **MNAR** — missing not at random | Related to the **missing value itself** | **No — dropping biases the result** |

MNAR is the dangerous one, and the standard example is income: high earners
decline to state it more often. Drop those rows and your average income is
biased *downwards*, and nothing in the data will tell you.

**The fact of missingness is itself information.** Add a `income_missing`
boolean column before imputing; a decision tree will often find it predictive.

### The seven methods

| Method | How | When to use | Danger |
|---|---|---|---|
| 1. **Ignore the tuple** | Delete the row | Few rows affected, MCAR | Loses data; biased if MNAR |
| 2. **Fill manually** | A human supplies it | Small, high-value data | Infeasible at scale |
| 3. **Global constant** | `"Unknown"`, `-1` | Categorical, when "missing" is meaningful | The algorithm may treat it as a real category |
| 4. **Attribute mean** | Column mean | Numeric, roughly symmetric | **Shrinks variance**; distorts correlations |
| 5. **Attribute median** | Column median | Numeric, **skewed or with outliers** | Same variance problem, but robust |
| 6. **Class-conditional mean** | Mean *within the same class* | Supervised setting | Leaks the label if done before splitting |
| 7. **Predict it** | Regression, k-NN, EM | Most accurate | Costly; can invent structure |

### ⚠️ Two traps in imputation

**Mean imputation shrinks the variance.** Replace 30% of a column with its
mean and the standard deviation falls, the correlations with other variables
weaken, and every subsequent statistical test is over-confident. The values are
plausible and the *distribution* is wrong.

**Impute after splitting, never before.** Computing the mean over the whole
dataset and then splitting into train and test leaks test information into
training — the mean encodes values the model should not have seen. Fit the
imputer on training data, apply it to both.

**Worked example.** Ages `[25, 30, NULL, 35, 40, NULL, 28]`.

```
Known values: 25, 30, 35, 40, 28   →  sum 158, n = 5
Mean   = 158 / 5 = 31.6
Median = sorted [25, 28, 30, 35, 40] → 30
```

Mean imputation gives `[25, 30, 31.6, 35, 40, 31.6, 28]`; median gives
`[25, 30, 30, 35, 40, 30, 28]`. With a symmetric spread like this either is
defensible. Add one value of 200 and the mean jumps to 59.7 while the median
moves to 32.5 — which is why **median is the safer default**.

## 2.6 Data cleaning: noisy data

**Noise** is random error or variance in a measured value — distinct from an
**outlier**, which is a genuine but extreme observation. A sensor glitch is
noise; a genuinely enormous transaction is an outlier. Removing outliers
because they are inconvenient discards exactly the fraud you were looking for.

### 🔢 Binning

Sort the values, divide into bins, then replace within each bin.

**Worked example.** Prices: `4, 8, 9, 15, 21, 21, 24, 25, 26, 28, 29, 34`
(already sorted, n = 12). Use **equal-frequency** bins of depth 4:

```
Bin 1: 4, 8, 9, 15
Bin 2: 21, 21, 24, 25
Bin 3: 26, 28, 29, 34
```

| Method | Rule | Result |
|---|---|---|
| **Smoothing by means** | Replace each with the bin mean | Bin1 mean = 36/4 = **9** → `9, 9, 9, 9` |
| | | Bin2 mean = 91/4 = **22.75** → `22.75 ×4` |
| | | Bin3 mean = 117/4 = **29.25** → `29.25 ×4` |
| **Smoothing by medians** | Replace each with the bin median | Bin1 → (8+9)/2 = **8.5** |
| **Smoothing by boundaries** | Replace with the *nearer* of min and max | Bin1: `4, 4, 4, 15` |

For bin-boundary smoothing on Bin 1, min = 4 and max = 15: 8 and 9 are both
closer to 4 than to 15, so both become 4.

| Binning type | How bins are chosen | Effect |
|---|---|---|
| **Equal-width** | Range split into k intervals of equal size | Simple; skewed data leaves bins empty |
| **Equal-frequency (equal-depth)** | Each bin holds the same *count* | Handles skew; bin widths vary |

### The other noise-handling methods

| Method | How |
|---|---|
| **Regression** | Fit a function; use the fitted values |
| **Clustering** | Points outside every cluster are candidate outliers |
| **Combined human/computer** | The computer flags suspects; a person judges |

## 2.7 Dimensionality reduction

### 🎯 The curse of dimensionality

As dimensions grow, three things happen, and all of them are bad:

1. **Data becomes sparse.** 100 points cover a line well, a square poorly, and
   a 10-dimensional cube not at all.
2. **All distances converge.** The ratio of nearest to farthest distance tends
   to 1, so "nearest neighbour" stops meaning anything — which breaks k-NN,
   K-Means and DBSCAN alike.
3. **Compute and overfitting both grow.** More features, more parameters, more
   ways to fit noise.

**Concretely:** to keep the same density, adding one dimension multiplies the
data you need. Ten samples per dimension means 10 points in 1-D and 10¹⁰ in
10-D.

### 🔢 Principal Component Analysis

PCA finds new axes — **principal components** — that are linear combinations
of the originals, mutually orthogonal, ordered by the variance they capture.
Keep the first few and you keep most of the information in fewer dimensions.

**The algorithm:**

1. **Standardise** each attribute to mean 0, variance 1.
2. Compute the **covariance matrix** (p × p).
3. Find its **eigenvalues and eigenvectors**.
4. Sort eigenvectors by eigenvalue, descending.
5. Keep the top *k* — these are the principal components.
6. Project the data onto them.

Each eigenvalue is the variance along its component, so

```
proportion of variance explained by component i = λᵢ / Σλ
```

**Worked example.** Eigenvalues `[4.2, 2.1, 0.9, 0.5, 0.3]`, total = 8.0.

| Component | λ | Proportion | Cumulative |
|:---:|---:|---:|---:|
| PC1 | 4.2 | 52.5% | 52.5% |
| PC2 | 2.1 | 26.25% | **78.75%** |
| PC3 | 0.9 | 11.25% | **90.0%** |
| PC4 | 0.5 | 6.25% | 96.25% |
| PC5 | 0.3 | 3.75% | 100% |

Keeping three components retains **90%** of the variance in 60% of the
dimensions. Three common stopping rules: a variance threshold (90% or 95%),
**Kaiser's criterion** (keep λ > 1 on standardised data — here, two
components), and the **scree plot elbow**.

### ⚠️ Standardise first, always

PCA maximises variance, and variance depends on units. Leave income in rupees
(variance ~10⁸) alongside age in years (variance ~100) and PC1 will be income,
almost exactly, regardless of the structure in the data. Standardising is not
optional; it is part of the method.

### ⚠️ Feature *extraction* versus feature *selection*

| | Dimensionality reduction (PCA) | Feature subset selection |
|---|---|---|
| Output features | **New**, combinations of originals | A **subset** of the originals |
| Interpretable? | **No** — "0.3×age + 0.6×income − 0.2×tenure" | **Yes** — still "age" |
| Information | Compressed from all features | Discarded features are gone |
| Also called | Feature **extraction** | Feature **selection** |

This is a two-mark question, and PCA's loss of interpretability is a real cost:
a bank cannot tell a customer their loan was refused because of principal
component 2.

## 2.8 Feature subset selection

Choose a subset of the original attributes, discarding those that are
**irrelevant** (no information about the target) or **redundant** (duplicating
another attribute — `date_of_birth` and `age`).

### 🔢 The three approaches

| Approach | How it chooses | Cost | Model-specific? |
|---|---|---|---|
| **Filter** | A statistical score, computed **before** any model | Cheap | No |
| **Wrapper** | Trains the model on each candidate subset and scores it | **Expensive** | Yes |
| **Embedded** | Selection happens *during* training | Moderate | Yes |

**Filter methods** — correlation with the target, chi-square, information
gain, variance threshold. Fast and general; blind to feature *interactions*,
so two features useless alone but powerful together are dropped.

**Wrapper methods** — forward selection (start empty, add the best feature
each round), backward elimination (start full, drop the worst), stepwise,
recursive feature elimination. They catch interactions because they test real
model performance. The cost is brutal: an exhaustive search over *p* features
is **2ᵖ** subsets — over a billion at p = 30.

**Embedded methods** — LASSO (L1 regularisation drives coefficients to exactly
zero), decision-tree feature importance, regularised trees. The usual practical
compromise.

**Worked example.** Predicting exam pass/fail from 8 attributes:

| Attribute | Verdict |
|---|---|
| `attendance_pct` | Keep — relevant |
| `internal_marks` | Keep — relevant |
| `hours_studied` | Keep — relevant |
| `student_id` | **Drop** — irrelevant; unique per row, pure noise a tree will overfit |
| `date_of_birth` | **Drop** — redundant with `age` |
| `age` | Keep |
| `name` | **Drop** — irrelevant |
| `final_marks` | **Drop — LEAKAGE.** Pass/fail is computed *from* it |

That last row is the one that matters. **Data leakage** is including a feature
that would not be available at prediction time, or that encodes the answer.
The model scores 100% in testing and is useless in production. It is the most
expensive mistake in applied machine learning and it is invisible to every
accuracy metric.

## 2.9 Discretization and binarization

### Discretization — continuous → categorical

| Method | How | Supervised? |
|---|---|---|
| **Equal-width** | Range ÷ k | No |
| **Equal-frequency** | Equal counts per bin | No |
| **Clustering** | 1-D K-Means on the values | No |
| **Entropy-based (MDL)** | Split where information gain is greatest | **Yes** |
| **ChiMerge** | Merge adjacent intervals with similar class distributions | **Yes** |

**Worked example.** Ages `[8, 15, 22, 25, 31, 38, 44, 51, 67]`, k = 3.

**Equal-width:** range = 67 − 8 = 59, so width = 59/3 ≈ 19.67.

```
[8, 27.67)   → 8, 15, 22, 25       (4 values)
[27.67, 47.33)→ 31, 38, 44          (3 values)
[47.33, 67]  → 51, 67              (2 values)
```

**Equal-frequency:** 9 values ÷ 3 = 3 per bin.

```
Bin 1: 8, 15, 22
Bin 2: 25, 31, 38
Bin 3: 44, 51, 67
```

Equal-width gives interpretable boundaries but uneven counts; equal-frequency
gives even counts but boundaries that are hard to explain. Neither uses the
class label, which is why entropy-based discretization usually wins in a
supervised task.

### Binarization — anything → 0/1

**Nominal, unordered → one-hot encoding.** One binary column per value:

| colour | → | is_red | is_green | is_blue |
|---|---|:---:|:---:|:---:|
| red | | 1 | 0 | 0 |
| green | | 0 | 1 | 0 |
| blue | | 0 | 0 | 1 |

**Ordinal, ordered → integer or thermometer encoding.** For
`low < medium < high`, integers 1/2/3 preserve the order that one-hot
destroys.

### ⚠️ Never integer-encode an unordered nominal attribute

Mapping `red=1, green=2, blue=3` tells every distance-based algorithm that
green is *between* red and blue and that blue is *three times* red. K-Means,
k-NN and every regression will act on that fiction. Use one-hot for unordered
values, integers only where the order is real.

The **dummy variable trap**: with *k* categories, *k* one-hot columns are
perfectly collinear (they sum to 1). Drop one — use *k − 1* columns — for
linear and logistic regression. Tree methods do not care.

## 2.10 Data transformation

### 🔢 Normalisation

| Method | Formula | Range | Outlier-sensitive? |
|---|---|---|---|
| **Min–max** | (x − min) / (max − min) | [0, 1] | **Very** |
| **Z-score** | (x − μ) / σ | ≈ [−3, 3] | Moderately |
| **Decimal scaling** | x / 10ʲ, smallest j with `max(|x'|) < 1` | (−1, 1) | Low |
| **Robust** | (x − median) / IQR | Varies | **Low** |

**Worked example.** Income = ₹73,600, with min ₹12,000, max ₹98,000,
μ = ₹54,000, σ = ₹16,000.

```
Min–max        = (73600 − 12000) / (98000 − 12000) = 61600 / 86000 = 0.7163
Z-score        = (73600 − 54000) / 16000           = 19600 / 16000 = 1.225
Decimal scaling: max is 98000, so j = 5 → 73600 / 100000            = 0.736
```

**Why normalise at all?** Because distance-based algorithms compare
magnitudes. With income in rupees and age in years, `(73600−54000)² = 3.8×10⁸`
dwarfs `(45−38)² = 49`, so **age contributes nothing** to the distance. K-Means,
k-NN, DBSCAN, SVM and neural networks all need scaled inputs.

**Which algorithms do NOT need it:** decision trees, random forests and Naïve
Bayes. Trees split one attribute at a time and only care about the *order* of
values, which scaling does not change. Saying so shows you understand *why*
scaling matters rather than applying it by rote.

### ⚠️ Min–max and one outlier

Values `[10, 12, 11, 13, 1000]`. Min–max scaling gives
`[0, 0.002, 0.001, 0.003, 1]` — the four sensible values are crushed into the
bottom 0.3% of the range. **One outlier destroys min–max scaling**, which is
why z-score or robust scaling is the safer default on real data.

### Other transformations

| Transformation | Purpose |
|---|---|
| **Aggregation** | Daily → monthly; reduces size and noise |
| **Log transform** | Compresses right-skewed data (income, population) |
| **Square root / Box–Cox** | Stabilises variance |
| **Attribute construction** | Derive `BMI` from height and weight |
| **Concept hierarchy generation** | Street → city → state → country |

## 2.11 Measures of similarity and dissimilarity

### 🔢 Distance measures for numeric data

**Minkowski distance** of order *p* generalises the family:

```
d(x, y) = ( Σᵢ |xᵢ − yᵢ|^p )^(1/p)
```

| p | Name | Formula | Geometry |
|:---:|---|---|---|
| 1 | **Manhattan / city-block** | Σ\|xᵢ − yᵢ\| | Grid movement |
| 2 | **Euclidean** | √(Σ(xᵢ − yᵢ)²) | Straight line |
| ∞ | **Chebyshev / supremum** | maxᵢ\|xᵢ − yᵢ\| | Largest single difference |

**Worked example.** x = (2, 3, 5), y = (5, 7, 1).

```
Differences:  |2−5| = 3,  |3−7| = 4,  |5−1| = 4

Manhattan  = 3 + 4 + 4                        = 11
Euclidean  = √(3² + 4² + 4²) = √(9+16+16) = √41 ≈ 6.403
Chebyshev  = max(3, 4, 4)                     = 4
```

Note `Chebyshev ≤ Euclidean ≤ Manhattan` always — a useful check on your
arithmetic.

### Properties of a metric

A true **distance metric** satisfies four conditions:

1. **Non-negativity** — d(x, y) ≥ 0
2. **Identity** — d(x, y) = 0 if and only if x = y
3. **Symmetry** — d(x, y) = d(y, x)
4. **Triangle inequality** — d(x, z) ≤ d(x, y) + d(y, z)

Squared Euclidean distance violates the triangle inequality, so it is **not a
metric** — though K-Means uses it anyway, because minimising it is what makes
the mean the optimal centroid.

### Measures for binary data

For two binary vectors, build the contingency counts:

|  | y = 1 | y = 0 |
|---|:---:|:---:|
| **x = 1** | a | b |
| **x = 0** | c | d |

| Coefficient | Formula | Counts 0-0 matches? |
|---|---|---|
| **Simple matching (SMC)** | (a + d) / (a + b + c + d) | **Yes** |
| **Jaccard** | a / (a + b + c) | **No** |

**Worked example.** Two shopping baskets over 100 products; both bought 3 of
the same items, x bought 2 others, y bought 5 others.

```
a = 3, b = 2, c = 5, d = 100 − 3 − 2 − 5 = 90

SMC     = (3 + 90) / 100     = 0.93
Jaccard = 3 / (3 + 2 + 5)    = 3 / 10 = 0.30
```

**SMC says the baskets are 93% similar; Jaccard says 30%.** Jaccard is right
here, and the reason is the whole point of the distinction: SMC counts the 90
products that *neither* customer bought as evidence of similarity. For sparse,
**asymmetric** data — market baskets, document term vectors, disease symptoms
— joint absence is meaningless and Jaccard is correct. Use SMC only when 0 and
1 are equally informative, as with gender coded 0/1.

### Cosine similarity

For high-dimensional sparse vectors, especially documents:

```
cos(x, y) = (x · y) / (‖x‖ ‖y‖)
```

**Worked example.** x = (3, 2, 0, 5), y = (1, 0, 0, 4).

```
x · y  = 3(1) + 2(0) + 0(0) + 5(4) = 3 + 20 = 23
‖x‖    = √(9 + 4 + 0 + 25) = √38 ≈ 6.164
‖y‖    = √(1 + 0 + 0 + 16) = √17 ≈ 4.123
cos    = 23 / (√38 × √17) = 23 / √646 = 23 / 25.417 ≈ 0.9049
```

**Cosine measures direction, not magnitude.** A 200-word document and a
2,000-word document on the same topic have very different Euclidean distance
but nearly identical cosine similarity — which is exactly what you want when
comparing texts. It also ignores 0-0 matches, like Jaccard, which is why it
suits sparse term vectors.

### Other measures

| Data | Measure |
|---|---|
| Categorical (nominal) | Simple matching; Hamming distance |
| Ordinal | Map to ranks, then treat as numeric |
| Mixed types | **Gower distance** — per-attribute measure, weighted average |
| Correlation | Pearson r — linear relationship, ignores scale and offset |
| Sets | Jaccard |
| Strings | Edit (Levenshtein) distance |

## 2.12 Issues and challenges

| Issue | The problem |
|---|---|
| **Scalability** | Algorithms must work when data exceeds memory |
| **High dimensionality** | The curse of dimensionality (§2.7) |
| **Data quality** | Noise, missing values, inconsistency |
| **Heterogeneity** | Relational, text, image, stream, graph in one problem |
| **Distributed data** | Data spread across sites that cannot be pooled |
| **Non-traditional analysis** | Data collected for another purpose entirely |
| **Overfitting** | Patterns that fit the sample, not the population |
| **Spurious patterns** | Enough tests and something is always "significant" |
| **Interpretability** | An accurate model nobody can explain will not be deployed |
| **Privacy and ethics** | See below |
| **Changing data (drift)** | The pattern was true last year |
| **Presentation** | A pattern nobody understands changes nothing |

### ⚠️ Spurious patterns

Test 1,000 random hypotheses at the 5% level and about **50 will appear
significant by chance alone**. Data mining tests enormously more than 1,000,
so *some* discovered patterns are guaranteed to be noise. The defences:
hold-out validation, cross-validation, multiple-testing correction, and the
oldest one — asking whether the pattern makes sense.

### Ethics and privacy

Not a footnote, and increasingly examinable:

- **Privacy** — mining combined datasets re-identifies people who were
  anonymous in each one separately.
- **Bias** — a model trained on historical decisions reproduces historical
  discrimination, and does so with the authority of arithmetic.
- **Transparency** — GDPR and India's DPDP Act give people rights over
  automated decisions about them.
- **Consent** — data collected for billing was not consented to for profiling.
- **Correlation is not causation** — the single most abused finding in the
  field.

## 2.13 Applications

| Domain | Application |
|---|---|
| **Retail** | Market basket analysis, loyalty, layout, demand forecasting |
| **Banking** | Credit scoring, fraud detection, churn, anti-money-laundering |
| **Healthcare** | Diagnosis support, readmission risk, drug discovery |
| **Telecom** | Churn prediction, network fault prediction, fraud |
| **Manufacturing** | Predictive maintenance, quality control, yield |
| **Web** | Recommenders, search ranking, ad targeting, clickstream |
| **Education** | At-risk student identification, curriculum analytics |
| **Science** | Genomics, astronomy, climate |
| **Government** | Tax fraud, census analysis, resource planning |

### Case study — market basket analysis

A supermarket's Apriori run finds `{bread, butter} → {jam}` with support 3%,
confidence 68%, lift 2.4. **Every one of those numbers is needed to act:**
support says it happens often enough to matter, confidence says the rule is
reliable when it fires, and lift says jam buyers are 2.4× more likely among
bread-and-butter buyers than in general. Unit 3 defines them precisely.

Acting on it: place jam near bread, bundle them, or — counter-intuitively —
place them *far apart* so customers walk past everything else. Retailers do
all three, and A/B test which works.

### Case study — the beer and nappies story

The famous claim is that a US retailer found young fathers sent out for nappies
on Friday evening also bought beer, and moved the two together.

**Say in the exam that the story is probably apocryphal.** It has been traced
to a 1992 consultancy anecdote and no retailer has ever confirmed it. It
survives because it perfectly illustrates the point — an unexpected,
actionable, unqueryable pattern — and knowing it is illustrative rather than
documented is exactly the critical judgement the subject requires.

---

## Practice problems

### Problem 1

Data: `12, 15, 18, 20, 22, 25, 28, 30, 35, 40, 45, 100`

(a) Smooth by bin means with equal-frequency bins of depth 4.
(b) Smooth by bin boundaries.
(c) Min–max normalise 25 to [0, 1].
(d) Comment on the effect of the value 100.

**Solution.**

**(a)** Equal-frequency, depth 4 — the data is already sorted:

```
Bin 1: 12, 15, 18, 20   mean = 65/4  = 16.25
Bin 2: 22, 25, 28, 30   mean = 105/4 = 26.25
Bin 3: 35, 40, 45, 100  mean = 220/4 = 55
```

Smoothed: `16.25 ×4, 26.25 ×4, 55 ×4`.

**(b)** Bin boundaries — replace with the nearer of the bin's min and max:

```
Bin 1 (min 12, max 20): 12→12, 15→12, 18→20, 20→20   →  12, 12, 20, 20
Bin 2 (min 22, max 30): 22→22, 25→22, 28→30, 30→30   →  22, 22, 30, 30
Bin 3 (min 35, max 100):35→35, 40→35, 45→35, 100→100 →  35, 35, 35, 100
```

For 15: |15−12| = 3 versus |15−20| = 5, so it goes to 12. For 18: |18−12| = 6
versus |18−20| = 2, so 20. For 45 in Bin 3: |45−35| = 10 versus |45−100| = 55,
so 35.

**(c)** min = 12, max = 100:

```
(25 − 12) / (100 − 12) = 13 / 88 = 0.1477
```

**(d)** The 100 is an outlier and it damages both operations. In (a) it drags
Bin 3's mean to 55, above every other value in that bin — the "smoothed" value
is higher than 45, the largest genuine member. In (c) it stretches the range so
that eleven of the twelve values compress into [0, 0.375], wasting nearly
two-thirds of the scale. **Z-score or robust scaling would be the correct choice here**, and
the outlier should be investigated before anything else is done.

### Problem 2

x = (1, 0, 1, 1, 0, 0, 1, 0, 0, 1) and y = (1, 1, 1, 0, 0, 0, 1, 0, 1, 0).

Compute the simple matching coefficient, Jaccard coefficient, Hamming
distance and cosine similarity, and say which is appropriate if these are
market baskets.

**Solution.**

Position by position:

| Pos | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| x | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| y | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| | a | c | a | b | d | d | a | d | c | b |

```
a (1,1) = 3   positions 1, 3, 7
b (1,0) = 2   positions 4, 10
c (0,1) = 2   positions 2, 9
d (0,0) = 3   positions 5, 6, 8
                                  total = 10 ✓
```

```
SMC      = (a + d) / 10        = (3 + 3) / 10 = 0.60
Jaccard  = a / (a + b + c)     = 3 / 7        = 0.4286
Hamming  = b + c               = 4            (positions differing)
Cosine   = 3 / (√5 × √5)       = 3 / 5        = 0.60
```

For cosine: x·y = 3 (the three shared 1s); ‖x‖ = √5 since x has five 1s;
‖y‖ = √5 likewise.

**Which is appropriate?** **Jaccard.** For market baskets the data is sparse
and asymmetric: the three products *neither* customer bought carry no
information about their similarity, but SMC counts them as agreement. SMC's
0.60 is inflated by exactly that. Note also that here cosine happens to equal
SMC numerically — a coincidence of these particular counts, not a general
relationship.

### Problem 3

A dataset has 12 attributes. PCA gives eigenvalues
`5.4, 2.8, 1.6, 1.1, 0.8, 0.4, 0.3, 0.2, 0.2, 0.1, 0.1, 0.0`.

(a) How many components retain 90% of the variance?
(b) How many by Kaiser's criterion?
(c) What is lost, besides variance?

**Solution.**

Total = 5.4 + 2.8 + 1.6 + 1.1 + 0.8 + 0.4 + 0.3 + 0.2 + 0.2 + 0.1 + 0.1 + 0.0
= **13.0**

| PC | λ | % | Cumulative % |
|:--:|---:|---:|---:|
| 1 | 5.4 | 41.54 | 41.54 |
| 2 | 2.8 | 21.54 | 63.08 |
| 3 | 1.6 | 12.31 | 75.38 |
| 4 | 1.1 | 8.46 | 83.85 |
| 5 | 0.8 | 6.15 | **90.00** |
| 6 | 0.4 | 3.08 | 93.08 |

**(a) Five components** reach exactly 90.00%, reducing 12 dimensions to 5.

**(b)** Kaiser's criterion keeps λ > 1, which is PCs 1–4 — **four
components**, retaining 83.85%. The two rules disagree, which is normal;
Kaiser is the more conservative here.

**(c) Interpretability.** The five components are linear combinations of all
twelve original attributes, so no component is "age" or "income" any more.
A model built on them cannot explain its decisions in terms a customer, a
regulator or a domain expert would accept. If explanation matters, **feature
selection** — keeping five of the original twelve — is the right tool even
though it retains less variance.

---

## Exam questions from this unit

**Two marks**

1. Define data mining.
2. Distinguish KDD from data mining.
3. Distinguish classification from clustering.
4. Distinguish classification from regression.
5. Distinguish predictive from descriptive mining.
6. What is the curse of dimensionality?
7. Distinguish feature selection from feature extraction.
8. Distinguish SMC from the Jaccard coefficient.
9. Why does mean imputation shrink the variance?
10. What is data leakage?
11. Which algorithms do not need normalisation, and why?

**Five marks**

1. Explain the KDD process with a diagram.
2. Explain the data mining tasks with examples.
3. Explain the methods of handling missing data.
4. Explain binning with a worked example.
5. Explain PCA and how many components to retain.
6. Explain filter, wrapper and embedded feature selection.
7. Explain normalisation methods with a worked example.
8. Explain the similarity and dissimilarity measures.
9. Explain the issues and challenges in data mining.

**Ten marks**

1. Explain data preprocessing exhaustively — cleaning, integration, reduction
   and transformation — with worked examples.
2. Explain similarity and dissimilarity measures for numeric, binary and
   mixed data, with computations.
3. Explain dimensionality reduction and feature subset selection, comparing
   them, with PCA worked through.

## Mistakes that cost marks

- Calling an SQL query "data mining"
- Saying KDD and data mining are the same thing
- Confusing classification (labels known) with clustering (labels discovered)
- Forgetting to standardise before PCA
- Claiming PCA selects a subset of the original attributes
- Integer-encoding an unordered nominal attribute
- Min–max normalising data containing an outlier
- Using SMC on sparse asymmetric data such as market baskets
- Imputing before splitting into train and test
- Treating outliers as noise and deleting them unexamined
- Leaving an identifier column in the feature set
- Including a feature that encodes the target — leakage
- Saying correlation implies causation
