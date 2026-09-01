# Unit 4 — Classification

**Syllabus topics:** Definition, What is a Decision Tree?, Tree Construction
Principle, Best Split, Splitting Indices, Splitting Criteria, Decision Tree
Construction Algorithms: CART, ID3, C4.5, Method for Comparing Classifiers,
Rule Based Classifiers, Nearest Neighbor Classifiers, Bayesian Classifiers.

---

## 4.1 What classification is

### 🎯 The big idea

Classification learns a function from **labelled examples** that assigns new,
unseen records to one of a **fixed set of known classes**.

```
TRAINING                                  PREDICTION
┌──────────────────────┐                 ┌──────────────────┐
│ features  →  LABEL   │                 │ features → ?     │
│ (25, 40k) →  approve │  ──► MODEL ──►  │ (31, 55k) → ???  │
│ (52, 90k) →  approve │                 └──────────────────┘
│ (19, 12k) →  reject  │
└──────────────────────┘
```

It is **supervised** learning: every training record carries its correct
answer. That is the whole difference from clustering, where no answer exists.

| Term | Meaning |
|---|---|
| **Attribute / feature** | An input variable |
| **Class label / target** | What is being predicted — **discrete** |
| **Training set** | Labelled records used to build the model |
| **Test set** | Labelled records **held out**, used to measure accuracy |
| **Validation set** | Held out again, used to tune the model |
| **Model / classifier** | The learned function |

### The two phases

| Phase | What happens |
|---|---|
| **1. Learning (induction)** | Build the model from the training set |
| **2. Classification (deduction)** | Apply it to unseen records |

### ⚠️ Never measure accuracy on the training set

A model that memorises its training data scores 100% on it and may be useless.
Accuracy quoted on data the model has seen is meaningless — this is the single
most common mistake in applied classification, and §4.9 explains how to
measure honestly.

## 4.2 Decision trees

### 🎯 The big idea

A decision tree is a flowchart: each **internal node** tests one attribute,
each **branch** is an outcome of that test, and each **leaf** is a class label.
Classifying a record means walking from the root to a leaf.

```
                    [ Outlook ]
              ┌──────────┼──────────┐
          sunny       overcast     rain
            │            │           │
      [Humidity]      « Yes »     [ Wind ]
        ┌───┴───┐                 ┌───┴───┐
      high    normal            strong   weak
        │        │                │        │
     « No »   « Yes »          « No »   « Yes »
```

To classify *(sunny, high humidity, weak wind)*: Outlook = sunny → Humidity =
high → **No**.

**Why decision trees dominate teaching and much of practice:**

| Strength | Weakness |
|---|---|
| **Interpretable** — you can read the rules aloud | Unstable: small data changes give a different tree |
| No normalisation needed | Greedy — no guarantee of the optimal tree |
| Handles numeric and categorical | Biased toward attributes with many values |
| Handles irrelevant attributes | Overfits without pruning |
| Fast to train and to apply | Axis-parallel splits only — poor on diagonal boundaries |
| Missing values manageable | Poor at modelling smooth numeric relationships |

## 4.3 Tree construction and the best split

### The generic algorithm — Hunt's algorithm

```
buildTree(D, attributes):
    if all records in D have the same class C:  return leaf(C)
    if attributes is empty or D is too small:   return leaf(majority class of D)
    A = SELECT_BEST_ATTRIBUTE(D, attributes)          ← the whole question
    create a node testing A
    for each outcome v of A:
        Dv = records in D with A = v
        if Dv is empty: attach leaf(majority class of D)
        else:           attach buildTree(Dv, attributes − {A})
    return the node
```

Every decision-tree algorithm is this skeleton with a different
`SELECT_BEST_ATTRIBUTE`. It is **greedy** and **recursive**: it takes the
locally best split at each node and never reconsiders. Finding the globally
optimal tree is NP-complete, which is why greedy is used.

### 🎯 What "best" means

**The split that produces the purest children.** A node is *pure* if all its
records share one class; a split is good in proportion to how much purity it
buys. The three ways to quantify impurity are the three splitting indices.

## 4.4 Splitting indices

### 🔢 Entropy

```
Entropy(D) = − Σᵢ pᵢ log₂ pᵢ
```

where pᵢ is the proportion of class i in D. Measured in **bits**.

| Distribution | Entropy | Meaning |
|---|---|---|
| All one class (1.0, 0.0) | **0** | Pure — no uncertainty |
| (0.5, 0.5) | **1** | Maximum for 2 classes |
| (0.9, 0.1) | 0.469 | Nearly pure |
| (0.25, 0.25, 0.25, 0.25) | **2** | Maximum for 4 classes |

Maximum entropy for c equally likely classes is **log₂ c**.

Note the convention `0 log₂ 0 = 0`, taken as the limit — otherwise a pure node
would be undefined.

### 🔢 Information gain — ID3's criterion

```
Gain(D, A) = Entropy(D) − Σᵥ (|Dᵥ| / |D|) × Entropy(Dᵥ)
```

The entropy before the split, minus the **weighted average** entropy after.
Choose the attribute with the **highest gain**.

The weighting matters: a split producing one pure child of 1 record and one
messy child of 99 has barely improved anything, and the weights say so.

### 🔢 Gini index — CART's criterion

```
Gini(D) = 1 − Σᵢ pᵢ²
```

| Distribution | Gini |
|---|---|
| (1.0, 0.0) | **0** |
| (0.5, 0.5) | **0.5** |
| (0.9, 0.1) | 0.18 |

Maximum for c classes is **1 − 1/c**, so 0.5 for two classes.

```
Gini_split(D, A) = Σᵥ (|Dᵥ| / |D|) × Gini(Dᵥ)
```

Choose the attribute **minimising** Gini_split (equivalently, maximising the
Gini *reduction*).

### 🔢 Classification error

```
Error(D) = 1 − max(pᵢ)
```

Rarely used for splitting — it is insensitive, often scoring two very
different splits identically — but it is used for **pruning**.

### 💡 Comparing the three

For a two-class problem with proportion p of the positive class:

| p | Entropy | Gini | Error |
|---|---|---|---|
| 0.0 | 0.000 | 0.000 | 0.00 |
| 0.1 | 0.469 | 0.180 | 0.10 |
| 0.3 | 0.881 | 0.420 | 0.30 |
| 0.5 | **1.000** | **0.500** | **0.50** |
| 0.7 | 0.881 | 0.420 | 0.30 |
| 0.9 | 0.469 | 0.180 | 0.10 |

All three peak at p = 0.5 and are zero at the extremes. **Entropy and Gini
usually choose the same attribute** — disagreements are reported in only a few
percent of splits. Gini is marginally faster (no logarithm) and is CART's
default; entropy is ID3's and C4.5's.

Note that entropy is scaled to [0, 1] for two classes and Gini to [0, 0.5], so
the two are not directly comparable in magnitude — only in which attribute
they rank first.

## 4.5 ID3

**Iterative Dichotomiser 3**, Ross Quinlan, 1986.

| Property | ID3 |
|---|---|
| Splitting criterion | **Information gain** |
| Attribute types | **Categorical only** |
| Split type | **Multi-way** — one branch per value |
| Missing values | Not handled |
| Pruning | **None** |
| Attribute reuse | An attribute is used at most once per path |

### 🔢 The complete worked example

The classic 14-record weather dataset. **Play** is the class.

| Day | Outlook | Temperature | Humidity | Wind | Play |
|:---:|---|---|---|---|:---:|
| 1 | Sunny | Hot | High | Weak | No |
| 2 | Sunny | Hot | High | Strong | No |
| 3 | Overcast | Hot | High | Weak | **Yes** |
| 4 | Rain | Mild | High | Weak | **Yes** |
| 5 | Rain | Cool | Normal | Weak | **Yes** |
| 6 | Rain | Cool | Normal | Strong | No |
| 7 | Overcast | Cool | Normal | Strong | **Yes** |
| 8 | Sunny | Mild | High | Weak | No |
| 9 | Sunny | Cool | Normal | Weak | **Yes** |
| 10 | Rain | Mild | Normal | Weak | **Yes** |
| 11 | Sunny | Mild | Normal | Strong | **Yes** |
| 12 | Overcast | Mild | High | Strong | **Yes** |
| 13 | Overcast | Hot | Normal | Weak | **Yes** |
| 14 | Rain | Mild | High | Strong | No |

**Step 1 — entropy of the whole set.** 9 Yes, 5 No out of 14.

```
Entropy(S) = −(9/14) log₂(9/14) − (5/14) log₂(5/14)
           = −0.6429 × (−0.6374) − 0.3571 × (−1.4854)
           = 0.4098 + 0.5305
           = 0.9403 bits
```

**Step 2 — gain for Outlook.**

| Outlook | Yes | No | Total | Entropy |
|---|:---:|:---:|:---:|---|
| Sunny | 2 | 3 | 5 | −(2/5)log₂(2/5) − (3/5)log₂(3/5) = **0.9710** |
| Overcast | 4 | 0 | 4 | **0** — pure! |
| Rain | 3 | 2 | 5 | **0.9710** |

```
Weighted entropy = (5/14)(0.9710) + (4/14)(0) + (5/14)(0.9710)
                 = 0.3468 + 0 + 0.3468 = 0.6935

Gain(Outlook) = 0.9403 − 0.6935 = 0.2467
```

**Step 3 — gain for the others.**

*Temperature:* Hot (2Y, 2N, entropy 1.0), Mild (4Y, 2N, entropy 0.9183),
Cool (3Y, 1N, entropy 0.8113).

```
Weighted = (4/14)(1.0) + (6/14)(0.9183) + (4/14)(0.8113) = 0.9111
Gain(Temperature) = 0.9403 − 0.9111 = 0.0292
```

*Humidity:* High (3Y, 4N, entropy 0.9852), Normal (6Y, 1N, entropy 0.5917).

```
Weighted = (7/14)(0.9852) + (7/14)(0.5917) = 0.7885
Gain(Humidity) = 0.9403 − 0.7885 = 0.1518
```

*Wind:* Weak (6Y, 2N, entropy 0.8113), Strong (3Y, 3N, entropy 1.0).

```
Weighted = (8/14)(0.8113) + (6/14)(1.0) = 0.8922
Gain(Wind) = 0.9403 − 0.8922 = 0.0481
```

**Step 4 — choose.**

| Attribute | Gain |
|---|---:|
| **Outlook** | **0.2467** ← highest |
| Humidity | 0.1518 |
| Wind | 0.0481 |
| Temperature | 0.0292 |

**Outlook becomes the root.** Overcast is already pure (4 Yes, 0 No), so that
branch is a leaf immediately.

**Step 5 — recurse on the Sunny branch** (days 1, 2, 8, 9, 11 — 2 Yes, 3 No,
entropy 0.9710):

| Attribute | Split | Weighted entropy | Gain |
|---|---|---:|---:|
| **Humidity** | High (0Y,3N) pure, Normal (2Y,0N) pure | **0.0** | **0.9710** |
| Temperature | Hot (0Y,2N), Mild (1Y,1N), Cool (1Y,0N) | 0.4000 | 0.5710 |
| Wind | Weak (1Y,2N), Strong (1Y,1N) | 0.9510 | 0.0200 |

**Humidity** splits the Sunny branch **perfectly** — both children pure, gain
equal to the full entropy. Two leaves.

**Step 6 — recurse on the Rain branch** (days 4, 5, 6, 10, 14 — 3 Yes, 2 No,
entropy 0.9710):

| Attribute | Split | Weighted entropy | Gain |
|---|---|---:|---:|
| **Wind** | Weak (3Y,0N) pure, Strong (0Y,2N) pure | **0.0** | **0.9710** |
| Temperature | Mild (2Y,1N), Cool (1Y,1N) | 0.9510 | 0.0200 |
| Humidity | High (1Y,1N), Normal (2Y,1N) | 0.9510 | 0.0200 |

**Wind** splits it perfectly too.

**The final tree** — exactly the one drawn in §4.2:

```
                    [ Outlook ]
              ┌──────────┼──────────┐
          sunny       overcast     rain
            │            │           │
      [Humidity]      « Yes »     [ Wind ]
        ┌───┴───┐      (4/4)      ┌───┴───┐
      high    normal            strong   weak
        │        │                │        │
     « No »   « Yes »          « No »   « Yes »
     (3/3)    (2/2)            (2/2)    (3/3)
```

Every leaf is pure, so this tree classifies all 14 training records correctly.
**Note that Temperature never appears** — ID3 found it uninformative and
dropped it entirely, which is feature selection happening for free.

### ⚠️ ID3's bias toward many-valued attributes

Add a `Day` column with 14 distinct values. Splitting on it gives 14 branches
of one record each, all pure, so:

```
Gain(Day) = 0.9403 − 0 = 0.9403
```

**The highest possible gain** — and the resulting tree is a lookup table that
generalises to nothing. Information gain systematically favours attributes with
many values, because more branches means smaller, purer subsets *by
arithmetic*, not by informativeness.

This flaw is exactly what C4.5 fixes.

## 4.6 C4.5

Quinlan's 1993 successor to ID3, and the most influential decision-tree
algorithm ever written.

### 🔢 Gain ratio

Normalise the gain by how much information the *split itself* carries:

```
SplitInfo(D, A) = − Σᵥ (|Dᵥ|/|D|) log₂ (|Dᵥ|/|D|)

GainRatio(D, A) = Gain(D, A) / SplitInfo(D, A)
```

`SplitInfo` is the entropy of the *partition sizes* — it is large when an
attribute has many, evenly sized branches, which is precisely the case that
inflated the raw gain.

**Worked example — the Day attribute.**

```
SplitInfo(Day) = −14 × (1/14) log₂(1/14) = log₂ 14 = 3.8074

GainRatio(Day) = 0.9403 / 3.8074 = 0.2470
```

Compare with Outlook:

```
SplitInfo(Outlook) = −(5/14)log₂(5/14) − (4/14)log₂(4/14) − (5/14)log₂(5/14)
                   = 0.5305 + 0.5164 + 0.5305 = 1.5774

GainRatio(Outlook) = 0.2467 / 1.5774 = 0.1564
```

**Gain ratio still ranks Day above Outlook here** (0.2470 vs 0.1564), which is
worth being honest about: gain ratio *reduces* the many-valued bias, it does
not eliminate it. C4.5 therefore adds a rule — **consider only attributes whose
gain is at least the average gain**, then pick the best gain ratio among those.
Day's raw gain of 0.9403 passes that filter, so in practice C4.5 also relies on
pruning and on identifier columns being removed as part of preprocessing.

Comparing the four real attributes by gain ratio:

| Attribute | Gain | SplitInfo | Gain ratio |
|---|---:|---:|---:|
| Outlook | 0.2467 | 1.5774 | **0.1564** |
| Humidity | 0.1518 | 1.0000 | 0.1518 |
| Wind | 0.0481 | 0.9852 | 0.0488 |
| Temperature | 0.0292 | 1.5567 | 0.0188 |

Outlook still wins, but only just — Humidity's SplitInfo of exactly 1.0 (two
equal branches of 7) barely penalises it.

### C4.5's other improvements over ID3

| Feature | ID3 | C4.5 |
|---|---|---|
| Criterion | Information gain | **Gain ratio** |
| Numeric attributes | No | **Yes** — binary splits at a threshold |
| Missing values | No | **Yes** — fractional instances |
| Pruning | No | **Yes** — error-based post-pruning |
| Rules | No | **Can convert the tree to rules** |

**Numeric attributes.** C4.5 sorts the values, considers each midpoint between
adjacent values with *different* classes as a candidate threshold, and picks
the best `A ≤ t` split. So numeric splits are always **binary**, even though
categorical splits are multi-way.

**Missing values.** A record with a missing value for the split attribute is
sent down **all** branches, weighted by each branch's proportion — a
"fractional instance". Its class contribution is split accordingly.

**C5.0** is the commercial successor: faster, less memory, boosting, and
misclassification costs.

## 4.7 CART

**Classification And Regression Trees**, Breiman, Friedman, Olshen and Stone,
1984 — developed independently of Quinlan's line and equally influential.

| Property | CART |
|---|---|
| Criterion | **Gini index** (classification), **least squares** (regression) |
| Split type | **Strictly binary** — always exactly two children |
| Attributes | Numeric **and** categorical |
| Also does | **Regression** — leaves hold a mean, not a class |
| Pruning | **Cost-complexity pruning** with cross-validation |
| Missing values | **Surrogate splits** |

### 🔢 Binary splits on categorical attributes

Since CART must split into two, a categorical attribute with values
{Sunny, Overcast, Rain} is tested as a **subset** question:

- `Outlook ∈ {Sunny}` versus `{Overcast, Rain}`
- `Outlook ∈ {Overcast}` versus `{Sunny, Rain}`
- `Outlook ∈ {Rain}` versus `{Sunny, Overcast}`

For v values there are **2^(v−1) − 1** distinct binary partitions. With v = 3
that is 3; with v = 10 it is 511; with v = 20 it is 524,287 — which is why
high-cardinality categorical attributes are expensive in CART.

### 🔢 Gini worked on the same weather data

Whole set, 9 Yes and 5 No:

```
Gini(S) = 1 − (9/14)² − (5/14)² = 1 − 0.4133 − 0.1276 = 0.4592
```

Consider the binary split `Outlook ∈ {Overcast}` versus `{Sunny, Rain}`:

```
Overcast:      4 records, 4 Yes 0 No  → Gini = 1 − 1² − 0² = 0
Sunny ∪ Rain: 10 records, 5 Yes 5 No  → Gini = 1 − 0.5² − 0.5² = 0.5

Gini_split = (4/14)(0) + (10/14)(0.5) = 0.3571
Reduction  = 0.4592 − 0.3571 = 0.1020
```

Against `Humidity = Normal` versus `High`:

```
Normal: 7 records, 6 Yes 1 No → 1 − (6/7)² − (1/7)² = 1 − 0.7347 − 0.0204 = 0.2449
High:   7 records, 3 Yes 4 No → 1 − (3/7)² − (4/7)² = 1 − 0.1837 − 0.3265 = 0.4898

Gini_split = (7/14)(0.2449) + (7/14)(0.4898) = 0.3673
Reduction  = 0.4592 − 0.3673 = 0.0918
```

So `Outlook ∈ {Overcast}` (reduction 0.1020) beats Humidity (0.0918) — CART
would split there first. **Different criterion, similar answer**, which is the
usual outcome.

### 🔢 ID3 versus C4.5 versus CART

| | **ID3** | **C4.5** | **CART** |
|---|---|---|---|
| Author, year | Quinlan, 1986 | Quinlan, 1993 | Breiman et al., 1984 |
| Criterion | Information gain | **Gain ratio** | **Gini** |
| Splits | Multi-way | Multi-way (categorical), binary (numeric) | **Always binary** |
| Numeric attributes | ✗ | ✓ | ✓ |
| Missing values | ✗ | ✓ fractional instances | ✓ surrogate splits |
| Pruning | ✗ | Error-based | **Cost-complexity + CV** |
| Regression | ✗ | ✗ | **✓** |
| Bias | Many-valued attributes | Reduced | Many-valued (mildly) |
| Tree shape | Wide, shallow | Wide, shallow | Deep, narrow |

## 4.8 Overfitting and pruning

### ⚠️ Overfitting

A tree grown until every leaf is pure has memorised its training data,
including its noise. Training accuracy rises to 100% while **test accuracy
falls** — the model has learned the sample, not the population.

```
accuracy
   │            ╭──────────────── training
   │        ╭───╯
   │     ╭──╯    ╭─╮
   │   ╭─╯    ╭──╯ ╰──╮
   │ ╭─╯   ╭──╯       ╰────────── test
   │╭╯  ╭──╯
   └────┴──────────────────────► tree size
        ↑
   best size — stop here
```

The gap between the curves *is* the overfitting.

### Pre-pruning versus post-pruning

| | **Pre-pruning (early stopping)** | **Post-pruning** |
|---|---|---|
| When | Stop growing during construction | Grow fully, then cut back |
| Criteria | max depth, min samples per leaf, min gain, statistical test | Error estimate on a validation set |
| Speed | **Faster** | Slower — builds the full tree first |
| Risk | **Horizon effect** — stops before a good split that lies just beyond a poor one | None of that; more computation |
| Usual verdict | Convenient | **Generally more reliable** |

The **horizon effect** is pre-pruning's real weakness: a split may look
worthless on its own while enabling an excellent split at the next level. Stop
early and you never find out.

### Post-pruning methods

| Method | How |
|---|---|
| **Reduced-error pruning** | Replace a subtree with a leaf if that does not hurt accuracy on a *validation* set. Simple, but needs data held out. |
| **Cost-complexity (CART)** | Minimise `R(T) + α·|leaves(T)|`; sweep α and choose by cross-validation |
| **Pessimistic error (C4.5)** | Estimate error from the training set with a statistical correction, so no validation set is needed |
| **MDL** | Minimise the bits to encode the tree plus the bits to encode its errors |

Cost-complexity pruning's `α` is the price charged per leaf: α = 0 keeps the
full tree, and large α collapses it to the root. Cross-validation picks the α
that generalises best.

## 4.9 Comparing classifiers

### 🔢 The confusion matrix

|  | **Predicted Positive** | **Predicted Negative** |
|---|:---:|:---:|
| **Actual Positive** | **TP** true positive | **FN** false negative |
| **Actual Negative** | **FP** false positive | **TN** true negative |

FN is a **Type II error** (a miss); FP is a **Type I error** (a false alarm) —
the same terminology as Course 4's hypothesis testing, and worth connecting.

### 🔢 The metrics

```
Accuracy    = (TP + TN) / (TP + TN + FP + FN)
Error rate  = 1 − Accuracy
Precision   = TP / (TP + FP)          of those PREDICTED positive, how many were?
Recall      = TP / (TP + FN)          of the ACTUAL positives, how many were found?
   (= sensitivity = true positive rate)
Specificity = TN / (TN + FP)          true negative rate
F1          = 2 × (Precision × Recall) / (Precision + Recall)
FPR         = FP / (FP + TN) = 1 − Specificity
```

**F1 is the harmonic mean**, not the arithmetic mean, and the choice matters:
precision 1.0 with recall 0.0 gives an arithmetic mean of 0.5 but an F1 of
**0**. The harmonic mean punishes imbalance, which is exactly what you want.

### ⚠️ The accuracy paradox

99% of transactions are legitimate. A classifier that predicts "legitimate"
for **everything** achieves **99% accuracy** and catches no fraud at all.

```
              Pred Fraud    Pred Legit
Actual Fraud       0            10          ← every fraud missed
Actual Legit       0           990

Accuracy  = 990/1000 = 99.0%
Precision = 0/0      = undefined
Recall    = 0/10     = 0.0     ← the number that matters
```

**On imbalanced data, accuracy is worse than useless — it is misleading.**
Report precision, recall and F1, or use balanced accuracy. This is a guaranteed
exam question and a real-world catastrophe.

### 💡 The precision–recall trade-off

Lower the decision threshold and you catch more positives (recall ↑) at the
cost of more false alarms (precision ↓). Which you want depends entirely on the
**cost of each error**:

| Application | Costlier error | Optimise |
|---|---|---|
| Cancer screening | Missing a case (FN) | **Recall** |
| Spam filter | Binning a real email (FP) | **Precision** |
| Fraud detection | Depends on the cost of investigating | F1 or expected cost |
| Search results | Irrelevant results (FP) | Precision |

Saying "it depends on the relative cost of a false positive and a false
negative" is the answer the examiner wants.

### 🔢 A worked confusion matrix

A spam filter on 1,000 emails: 200 actual spam, 800 legitimate. It flags 180
as spam, of which 150 truly are.

```
TP = 150            (flagged spam, actually spam)
FP = 180 − 150 = 30 (flagged spam, actually legitimate)
FN = 200 − 150 = 50 (not flagged, actually spam)
TN = 800 − 30 = 770 (not flagged, actually legitimate)
```

|  | Pred Spam | Pred Ham | Total |
|---|:---:|:---:|:---:|
| **Actual Spam** | 150 | 50 | 200 |
| **Actual Ham** | 30 | 770 | 800 |
| **Total** | 180 | 820 | 1000 |

```
Accuracy    = (150 + 770) / 1000       = 0.920
Precision   = 150 / 180                = 0.8333
Recall      = 150 / 200                = 0.750
Specificity = 770 / 800                = 0.9625
F1          = 2(0.8333 × 0.750)/(0.8333 + 0.750) = 1.25/1.5833 = 0.7895
FPR         = 30 / 800                 = 0.0375
```

**Interpretation.** 92% accuracy sounds good; recall of 0.75 means **one spam
in four still reaches the inbox**, and precision of 0.83 means **17% of what is
sent to the spam folder is a real email**. For a spam filter, that FP rate is
the serious problem — losing a genuine email costs far more than seeing a spam.
The threshold should be raised to favour precision.

### ROC and AUC

The **ROC curve** plots TPR (recall) against FPR as the decision threshold
sweeps from 1 to 0.

```
TPR
 1 │       ╭────────── perfect (AUC = 1)
   │     ╭─╯      ╱
   │   ╭─╯      ╱  ← random guessing (AUC = 0.5)
   │ ╭─╯      ╱
   │╭╯      ╱
 0 └──────────────► FPR
   0              1
```

**AUC** — the area under it — is the probability that a randomly chosen
positive is ranked above a randomly chosen negative.

| AUC | Meaning |
|---|---|
| 1.0 | Perfect |
| 0.9–1.0 | Excellent |
| 0.8–0.9 | Good |
| 0.7–0.8 | Fair |
| 0.5 | **No better than chance** |
| < 0.5 | Worse than chance — invert the predictions |

**AUC is threshold-independent**, which is its value: it measures how well the
classifier *ranks*, separately from where you choose to cut. On heavily
imbalanced data, the **precision–recall curve** is more informative than ROC,
because a large TN count flatters the FPR.

### Estimating accuracy honestly

| Method | How | Note |
|---|---|---|
| **Holdout** | Split, typically 2/3 train, 1/3 test | Simple; high variance |
| **Random subsampling** | Repeat holdout k times, average | Better estimate |
| **k-fold cross-validation** | Split into k folds; each serves once as test | **The standard**; k = 10 usual |
| **Stratified k-fold** | Folds preserve the class proportions | **Preferred**, especially when imbalanced |
| **Leave-one-out (LOOCV)** | k = n | Nearly unbiased; expensive; high variance |
| **Bootstrap (.632)** | Sample n with replacement; test on the ~36.8% unsampled | Good for small datasets |

The bootstrap's 0.632 comes from the limit: the probability a given record is
*never* chosen in n draws with replacement is (1 − 1/n)ⁿ → 1/e ≈ 0.368, so
about 63.2% of records appear in each bootstrap sample.

### Comparing two classifiers

Do not simply compare two accuracy numbers. Use **paired k-fold
cross-validation** and a **paired t-test** (Course 4, Unit 5) on the per-fold
differences, or McNemar's test on the disagreements. A 2% difference on one
holdout split is noise.

**Also compare on more than accuracy:** training time, prediction time,
memory, interpretability, robustness to missing data, and the cost of the
errors each makes.

### 💡 Ensembles

| Method | Idea |
|---|---|
| **Bagging** | Train on bootstrap samples, vote — reduces **variance** |
| **Random Forest** | Bagging + a random attribute subset at each split |
| **Boosting (AdaBoost)** | Train sequentially, each learner weighting the previous one's errors — reduces **bias** |
| **Stacking** | A meta-model learns to combine base models' predictions |

**Random Forest is the answer to the single decision tree's instability.**
One tree changes completely if a few records change; 500 trees voting do not.
The cost is exactly what made trees attractive — you can no longer read the
model.

## 4.10 Rule-based classifiers

A model as a set of `IF condition THEN class` rules.

```
R1: IF Outlook = Overcast                      THEN Play = Yes
R2: IF Outlook = Sunny AND Humidity = Normal   THEN Play = Yes
R3: IF Outlook = Sunny AND Humidity = High     THEN Play = No
R4: IF Outlook = Rain AND Wind = Weak          THEN Play = Yes
R5: IF Outlook = Rain AND Wind = Strong        THEN Play = No
```

Those five rules are **exactly the five root-to-leaf paths** of §4.5's tree.
Any decision tree converts to rules mechanically — which is what C4.5rules
does, then simplifies each rule independently, often producing something
smaller and clearer than the tree.

### Rule quality

```
Coverage(R) = |records satisfying the antecedent| / |D|
Accuracy(R) = |records satisfying antecedent AND consequent| / |records satisfying antecedent|
```

### ⚠️ Mutually exclusive and exhaustive

| Property | Meaning | If violated |
|---|---|---|
| **Mutually exclusive** | No record triggers two rules | Need a **conflict resolution** strategy |
| **Exhaustive** | Every record triggers at least one rule | Need a **default class** |

Rules from a decision tree are automatically both, because tree paths
partition the space. Rules learned directly are usually neither, so:

**Conflict resolution:** *size ordering* (the most specific rule wins),
*rule ordering* (a fixed priority list — a **decision list**), or *class-based
ordering* (group by class).

### Direct rule induction

**Sequential covering** — RIPPER, CN2, PART:

```
rules = []
for each class c (rarest first):
    while positive examples of c remain:
        r = LearnOneRule(D, c)            ← greedily add conditions
        remove the records r covers
        rules.append(r)
add a default rule for the majority of what remains
```

**RIPPER** (Repeated Incremental Pruning to Produce Error Reduction) is the
standard, and is WEKA's `JRip`. **PART** builds a partial C4.5 tree, takes its
best leaf as a rule, discards the rest, and repeats — combining both approaches.

| | Decision tree | Rule-based |
|---|---|---|
| Structure | Hierarchical | Flat list |
| Coverage | Partitions the space | May overlap or leave gaps |
| Interpretability | Good | **Often better** — each rule stands alone |
| Attribute reuse | Repeated in every subtree | Only where needed |
| Handles disjunctions | Awkwardly — the **replicated subtree problem** | Naturally |

The **replicated subtree problem** is worth naming: a concept like
`(A AND B) OR (C AND D)` forces a tree to duplicate the same subtree in several
branches, while two rules express it directly.

## 4.11 Nearest neighbour classifiers

### 🎯 The big idea

**Do not build a model at all.** Store the training data; to classify a new
record, find the k most similar stored records and take a majority vote.

This is **lazy learning** — the opposite of everything else in this unit.

| | **Eager** (trees, Bayes, rules) | **Lazy** (k-NN) |
|---|---|---|
| Training | Builds a model — slow | **Stores the data — instant** |
| Prediction | Fast | **Slow — compares against everything** |
| Memory | Just the model | **The whole training set** |
| Adapts to new data | Retrain | Just add the record |
| Decision boundary | Global, committed at training | **Local, formed per query** |

### The algorithm

```
1. Choose k and a distance measure.
2. Compute the distance from the query to EVERY training record.
3. Take the k nearest.
4. Return their majority class (or a distance-weighted vote).
```

Distances from Unit 2 §2.11: Euclidean for numeric, Hamming for binary,
cosine for text, Gower for mixed.

### 🔢 A worked example

Training data, classifying by **height (cm)** and **weight (kg)**:

| Point | Height | Weight | Class |
|---|---:|---:|---|
| P1 | 158 | 58 | Small |
| P2 | 160 | 59 | Small |
| P3 | 163 | 61 | Small |
| P4 | 170 | 68 | Large |
| P5 | 175 | 72 | Large |
| P6 | 180 | 78 | Large |

Classify **q = (168, 65)** with k = 3, Euclidean distance:

```
P1: √((168−158)² + (65−58)²) = √(100 + 49)  = √149  = 12.207
P2: √((168−160)² + (65−59)²) = √(64 + 36)   = √100  = 10.000
P3: √((168−163)² + (65−61)²) = √(25 + 16)   = √41   =  6.403
P4: √((168−170)² + (65−68)²) = √(4 + 9)     = √13   =  3.606
P5: √((168−175)² + (65−72)²) = √(49 + 49)   = √98   =  9.899
P6: √((168−180)² + (65−78)²) = √(144 + 169) = √313  = 17.692
```

Three nearest: **P4 (3.606, Large)**, **P3 (6.403, Small)**, **P5 (9.899,
Large)**.

Vote: Large 2, Small 1 → **Large**.

With k = 1 it would be P4 alone → Large. With k = 5 the neighbours are P4, P3,
P5, P2, P1 → Large 2, Small 3 → **Small**. **The answer changes with k**, which
is why k must be chosen by cross-validation and not by guesswork.

### ⚠️ Three things that break k-NN

**1. Unscaled features.** Height in cm (range ~20) and income in rupees (range
~100,000) — income dominates every distance completely and height contributes
nothing. **k-NN requires normalisation**, unlike decision trees.

**2. Choosing k.**

| k | Effect |
|---|---|
| 1 | Sensitive to noise; overfits; jagged boundary |
| Large | Smooth boundary; may include irrelevant far-off points; underfits |
| = n | Always predicts the majority class |

Rules of thumb: k ≈ √n as a starting point, choose by cross-validation, and use
an **odd** k for two classes to avoid ties.

**3. The curse of dimensionality.** In high dimensions all points become nearly
equidistant, so "nearest" stops meaning anything (Unit 2, §2.7). k-NN degrades
badly beyond a few dozen dimensions.

### Variants

- **Distance-weighted voting** — weight each neighbour by 1/d², so closer
  neighbours count more. Makes large k safer.
- **k-d trees and ball trees** — reduce the search from O(n) to O(log n),
  though they lose their advantage in high dimensions.
- **Condensed nearest neighbour** — keep only the records near the boundary.

## 4.12 Bayesian classifiers

### 🔢 Bayes' theorem

```
P(C | X) = P(X | C) × P(C) / P(X)
```

| Term | Name | Meaning |
|---|---|---|
| `P(C \| X)` | **Posterior** | Probability of class C given the evidence |
| `P(X \| C)` | **Likelihood** | Probability of the evidence given the class |
| `P(C)` | **Prior** | Probability of the class before seeing evidence |
| `P(X)` | **Evidence** | Probability of the evidence overall |

Classify by choosing the class with the largest posterior. Since `P(X)` is the
same for every class, it can be ignored when comparing:

```
predict argmax_C  P(X | C) × P(C)
```

### 🎯 The naïve assumption

Computing `P(X | C)` for a full attribute vector requires counting every
combination of values — exponentially many, and almost all unobserved. **Naïve
Bayes assumes the attributes are conditionally independent given the class:**

```
P(X | C) = P(x₁ | C) × P(x₂ | C) × … × P(xₙ | C)
```

Now each factor needs only a single-attribute count.

**The assumption is almost always false** — height and weight are obviously
dependent — and Naïve Bayes works well anyway. The reason is that
classification only needs the **ranking** of the posteriors to be right, not
their values. The estimated probabilities are often badly wrong while the
argmax is still correct.

### 🔢 The complete worked example

Same weather data. Classify **X = (Sunny, Cool, High, Strong)**.

**Priors:**

```
P(Yes) = 9/14 = 0.6429
P(No)  = 5/14 = 0.3571
```

**Conditional probabilities from the table:**

| Attribute = value | Given Yes (9) | Given No (5) |
|---|---|---|
| Outlook = Sunny | 2/9 = 0.2222 | 3/5 = 0.6000 |
| Temperature = Cool | 3/9 = 0.3333 | 1/5 = 0.2000 |
| Humidity = High | 3/9 = 0.3333 | 4/5 = 0.8000 |
| Wind = Strong | 3/9 = 0.3333 | 3/5 = 0.6000 |

**Posteriors (unnormalised):**

```
P(X | Yes) × P(Yes) = 0.2222 × 0.3333 × 0.3333 × 0.3333 × 0.6429
                    = 0.008230 × 0.6429  ... let us do it in full:
                    = (2/9)(3/9)(3/9)(3/9)(9/14)
                    = (2 × 3 × 3 × 3 × 9) / (9 × 9 × 9 × 9 × 14)
                    = 486 / 91854
                    = 0.005291

P(X | No)  × P(No)  = (3/5)(1/5)(4/5)(3/5)(5/14)
                    = (3 × 1 × 4 × 3 × 5) / (5 × 5 × 5 × 5 × 14)
                    = 180 / 8750
                    = 0.020571
```

**0.020571 > 0.005291, so predict No.**

**Normalised, for a genuine probability:**

```
Total = 0.005291 + 0.020571 = 0.025862
P(No  | X) = 0.020571 / 0.025862 = 0.7954   (79.5%)
P(Yes | X) = 0.005291 / 0.025862 = 0.2046   (20.5%)
```

### ⚠️ The zero-frequency problem, and Laplace smoothing

If any single conditional probability is zero, the **whole product is zero**,
regardless of how strongly every other attribute votes. One unseen value
vetoes the entire class.

Classify **X = (Overcast, Hot, High, Strong)**: `P(Outlook = Overcast | No)` is
**0/5 = 0**, because no Overcast day has Play = No. So P(X | No) × P(No) = 0
exactly, and No is impossible however the other attributes look.

**Laplace (add-one) smoothing** fixes it by adding 1 to every count:

```
P(xᵢ | C) = (count(xᵢ, C) + 1) / (count(C) + k)
```

where k is the number of distinct values of that attribute.

Outlook has k = 3 values, so:

```
P(Overcast | No) = (0 + 1) / (5 + 3) = 1/8 = 0.125     (was 0)
P(Sunny    | No) = (3 + 1) / (5 + 3) = 4/8 = 0.500     (was 0.600)
P(Rain     | No) = (2 + 1) / (5 + 3) = 3/8 = 0.375     (was 0.400)
                                       ────
                                       8/8 = 1.0  ✓ still a distribution
```

The estimates shift slightly and no probability is ever zero. This is a
guaranteed exam question.

### 💡 Log probabilities

Multiplying 50 probabilities each around 0.1 gives 10⁻⁵⁰, which **underflows**
to zero in floating point. Every real implementation sums logarithms instead:

```
log P(X|C) + log P(C) = Σᵢ log P(xᵢ|C) + log P(C)
```

The argmax is unchanged because log is monotonic, and the arithmetic is stable.

### Variants and the comparison

| Variant | For | Assumes |
|---|---|---|
| **Multinomial NB** | Counts — word frequencies | Multinomial distribution |
| **Bernoulli NB** | Binary presence/absence | Bernoulli |
| **Gaussian NB** | Continuous attributes | Each attribute normal within a class |

**Gaussian NB** estimates μ and σ per attribute per class, then uses the normal
density — a direct application of Course 4, Unit 3.

A **Bayesian belief network** drops the naïve assumption: a directed acyclic
graph encodes which attributes actually depend on which, so only genuine
dependencies are modelled. More accurate and far more expensive, both to learn
and to compute.

| | Strengths | Weaknesses |
|---|---|---|
| **Naïve Bayes** | Fast, needs little data, handles many attributes, incremental | Independence assumption; zero-frequency; poor probability estimates |
| **Decision tree** | Interpretable, no scaling, mixed types | Unstable, overfits, axis-parallel |
| **k-NN** | No training, adapts instantly, complex boundaries | Slow prediction, needs scaling, curse of dimensionality |
| **Rule-based** | Very interpretable, handles disjunctions | Conflict resolution, may not be exhaustive |

---

## Practice problems

### Problem 1

For this dataset, compute the entropy of the whole set and the information gain
of each attribute, and say which becomes the root.

| ID | Age | Income | Student | Credit | Buys |
|:--:|---|---|---|---|:---:|
| 1 | Youth | High | No | Fair | No |
| 2 | Youth | High | No | Excellent | No |
| 3 | Middle | High | No | Fair | **Yes** |
| 4 | Senior | Medium | No | Fair | **Yes** |
| 5 | Senior | Low | Yes | Fair | **Yes** |
| 6 | Senior | Low | Yes | Excellent | No |
| 7 | Middle | Low | Yes | Excellent | **Yes** |
| 8 | Youth | Medium | No | Fair | No |
| 9 | Youth | Low | Yes | Fair | **Yes** |
| 10 | Senior | Medium | Yes | Fair | **Yes** |
| 11 | Youth | Medium | Yes | Excellent | **Yes** |
| 12 | Middle | Medium | No | Excellent | **Yes** |
| 13 | Middle | High | Yes | Fair | **Yes** |
| 14 | Senior | Medium | No | Excellent | No |

**Solution.** 9 Yes, 5 No, N = 14.

```
Entropy(S) = −(9/14)log₂(9/14) − (5/14)log₂(5/14) = 0.9403
```

**Age:**

| Age | Yes | No | n | Entropy |
|---|:-:|:-:|:-:|---|
| Youth | 2 | 3 | 5 | 0.9710 |
| Middle | 4 | 0 | 4 | **0** |
| Senior | 3 | 2 | 5 | 0.9710 |

```
Weighted = (5/14)(0.9710) + (4/14)(0) + (5/14)(0.9710) = 0.6935
Gain(Age) = 0.9403 − 0.6935 = 0.2467
```

**Income:** High (2Y,2N, e=1.0), Medium (4Y,2N, e=0.9183), Low (3Y,1N, e=0.8113)

```
Weighted = (4/14)(1.0) + (6/14)(0.9183) + (4/14)(0.8113) = 0.9111
Gain(Income) = 0.0292
```

**Student:** Yes (6Y,1N, e=0.5917), No (3Y,4N, e=0.9852)

```
Weighted = (7/14)(0.5917) + (7/14)(0.9852) = 0.7885
Gain(Student) = 0.1518
```

**Credit:** Fair (6Y,2N, e=0.8113), Excellent (3Y,3N, e=1.0)

```
Weighted = (8/14)(0.8113) + (6/14)(1.0) = 0.8922
Gain(Credit) = 0.0481
```

| Attribute | Gain |
|---|---:|
| **Age** | **0.2467** |
| Student | 0.1518 |
| Credit | 0.0481 |
| Income | 0.0292 |

**Age is the root**, and its Middle branch is already pure (4 Yes, 0 No).

*(This is the same arithmetic as §4.5 — the classic "buys computer" dataset has
the identical class distribution to the weather dataset, which is why the
numbers match exactly. Recognising that saves time in an exam.)*

### Problem 2

A medical test for a disease affecting 1% of the population has 95%
sensitivity and 90% specificity. Applied to 10,000 people, build the confusion
matrix and compute accuracy, precision, recall and F1. Comment.

**Solution.**

```
Actual diseased  = 1% of 10,000    = 100
Actual healthy   = 9,900

TP = 95% of 100      = 95        (sensitivity = recall = 0.95)
FN = 100 − 95        = 5
TN = 90% of 9,900    = 8,910     (specificity = 0.90)
FP = 9,900 − 8,910   = 990
```

|  | Pred Positive | Pred Negative | Total |
|---|:---:|:---:|:---:|
| **Actual Diseased** | 95 | 5 | 100 |
| **Actual Healthy** | 990 | 8,910 | 9,900 |
| **Total** | 1,085 | 8,915 | 10,000 |

```
Accuracy  = (95 + 8910) / 10000 = 9005/10000 = 0.9005   (90.05%)
Precision = 95 / 1085                        = 0.0876   (8.76%)
Recall    = 95 / 100                         = 0.9500   (95%)
F1        = 2(0.0876 × 0.95)/(0.0876 + 0.95) = 0.16644/1.0376 = 0.1604
```

**Comment — this is the base rate fallacy, and it is the point of the
question.** The test sounds excellent: 95% sensitivity, 90% specificity, 90%
accuracy. But **precision is 8.76%**: of everyone who tests positive, fewer
than one in eleven actually has the disease.

The reason is that the disease is rare. Even a 10% false-positive rate applied
to 9,900 healthy people produces **990 false alarms**, which swamp the 95 true
positives. F1 of 0.16 reflects the real picture that accuracy of 0.90 conceals.

This is why rare-disease screening uses a cheap sensitive test **followed by a
specific confirmatory test**, and it is why "90% accurate" is a meaningless
claim without the base rate.

### Problem 3

Using the weather dataset of §4.5 and Naïve Bayes, classify
**X = (Rain, Mild, Normal, Weak)**, showing every probability. Then apply
Laplace smoothing and say whether the answer changes.

**Solution.**

**Priors:** P(Yes) = 9/14, P(No) = 5/14.

**Counting from the table:**

| Value | Yes (of 9) | No (of 5) |
|---|---|---|
| Outlook = Rain | 3/9 = 0.3333 | 2/5 = 0.4000 |
| Temperature = Mild | 4/9 = 0.4444 | 2/5 = 0.4000 |
| Humidity = Normal | 6/9 = 0.6667 | 1/5 = 0.2000 |
| Wind = Weak | 6/9 = 0.6667 | 2/5 = 0.4000 |

```
P(X|Yes)·P(Yes) = (3/9)(4/9)(6/9)(6/9)(9/14)
                = (3 × 4 × 6 × 6 × 9) / (9 × 9 × 9 × 9 × 14)
                = 3888 / 91854 = 0.042328

P(X|No)·P(No)   = (2/5)(2/5)(1/5)(2/5)(5/14)
                = (2 × 2 × 1 × 2 × 5) / (5 × 5 × 5 × 5 × 14)
                = 40 / 8750 = 0.004571
```

**0.042328 > 0.004571, so predict Yes.**

```
Normalised: P(Yes|X) = 0.042328 / 0.046899 = 0.9025   (90.3%)
            P(No |X) = 0.004571 / 0.046899 = 0.0975    (9.7%)
```

**With Laplace smoothing** — Outlook has 3 values, the other three attributes
have 2 each:

| Value | Yes | No |
|---|---|---|
| Rain | (3+1)/(9+3) = 4/12 = 0.3333 | (2+1)/(5+3) = 3/8 = 0.3750 |
| Mild | (4+1)/(9+3) = 5/12 = 0.4167 | (2+1)/(5+3) = 3/8 = 0.3750 |
| Normal | (6+1)/(9+2) = 7/11 = 0.6364 | (1+1)/(5+2) = 2/7 = 0.2857 |
| Weak | (6+1)/(9+2) = 7/11 = 0.6364 | (2+1)/(5+2) = 3/7 = 0.4286 |

*(Temperature has 3 values — Hot, Mild, Cool — so its denominator is 9+3, while
Humidity and Wind have 2 values each and use 9+2.)*

```
P(X|Yes)·P(Yes) = 0.3333 × 0.4167 × 0.6364 × 0.6364 × 0.6429 = 0.036163
P(X|No) ·P(No)  = 0.3750 × 0.3750 × 0.2857 × 0.4286 × 0.3571 = 0.006149

P(Yes|X) = 0.036163 / 0.042312 = 0.8547   (85.5%)
P(No |X) = 0.006149 / 0.042312 = 0.1453   (14.5%)
```

**The answer does not change — still Yes.** Smoothing pulled the estimates
toward each other, so the confidence fell from 90.3% to 85.5%, but the argmax
is unchanged. **That is exactly the intended behaviour**: smoothing prevents
overconfidence from small counts, and it is precisely what keeps a single
zero-count value from vetoing a class entirely.

---

## Exam questions from this unit

**Two marks**

1. Define classification.
2. Distinguish classification from clustering.
3. What is entropy, and what is its maximum for c classes?
4. Distinguish information gain from gain ratio.
5. Why does ID3 favour attributes with many values?
6. Distinguish pre-pruning from post-pruning.
7. Define precision and recall.
8. What is the accuracy paradox?
9. Why is F1 the harmonic mean?
10. Distinguish eager from lazy learning.
11. What is the zero-frequency problem?
12. What is Laplace smoothing?
13. Why is Naïve Bayes called "naïve"?

**Five marks**

1. Explain the decision tree construction principle with the splitting indices.
2. Explain ID3 with a worked example.
3. Explain how C4.5 improves on ID3.
4. Explain CART and how it differs from C4.5.
5. Explain overfitting and the pruning methods.
6. Explain the confusion matrix and all metrics derived from it.
7. Explain ROC and AUC.
8. Explain k-NN with a worked example, and how k is chosen.
9. Explain Naïve Bayes with a worked example.
10. Explain rule-based classifiers and conflict resolution.

**Ten marks**

1. Build a complete decision tree for a given dataset using ID3, showing every
   entropy and gain calculation.
2. Classify a record with Naïve Bayes, showing all probabilities, and apply
   Laplace smoothing.
3. Compare decision trees, rule-based classifiers, k-NN and Naïve Bayes on
   principle, strengths, weaknesses and appropriate use.

## Mistakes that cost marks

- Quoting accuracy measured on the training set
- Forgetting the **weights** |Dᵥ|/|D| in the information gain formula
- Using log base e instead of base 2 for entropy
- Confusing precision (of the predicted) with recall (of the actual)
- Reporting accuracy alone on imbalanced data
- Averaging precision and recall arithmetically instead of harmonically
- Claiming CART can produce multi-way splits — it is always binary
- Forgetting to normalise features before k-NN
- Choosing an even k in a two-class k-NN problem
- Leaving a zero probability in a Naïve Bayes product
- Applying Laplace smoothing without adding k to the denominator
- Saying Naïve Bayes fails because the independence assumption is false
- Forgetting to divide by P(X), or dividing when comparing classes (unnecessary)
