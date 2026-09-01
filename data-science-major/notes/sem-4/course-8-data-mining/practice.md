# Course 8 — Practice Questions with Solutions

Data Mining is examined on **arithmetic**. Almost every ten-mark question is a
trace: run Apriori, build a tree, classify with Bayes, iterate K-Means. This
file works those traces end to end.

**Every number here has been machine-checked** against
`tools/run_data_labs.py`.

---

## Section A — Two-mark questions

### 1. Define a data warehouse.

Inmon: *a subject-oriented, integrated, time-variant, non-volatile collection
of data in support of management's decision-making process.* Subject-oriented
means organised around business subjects rather than applications; integrated
means reconciled into one format from many sources; time-variant means history
is kept with a time dimension; non-volatile means users read but do not update.

### 2. Distinguish OLTP from OLAP.

OLTP runs the business: many small read/write transactions on current,
normalised, detailed data, optimised for throughput. OLAP analyses the
business: few enormous read-only aggregate queries over historical,
denormalised data, optimised for response time. Running an OLAP query on an
OLTP database would lock tables and stall the operational workload — isolating
those workloads is why warehouses exist.

### 3. Distinguish slice from dice.

**Slice** fixes **one** dimension to a **single** value, reducing an
n-dimensional cube to n − 1 dimensions. **Dice** restricts **two or more**
dimensions to **ranges or sets**, producing a smaller sub-cube of the **same**
dimensionality.

### 4. What is a factless fact table?

A fact table with foreign keys but **no measures** — student attended class,
promotion was in effect. Counting the rows *is* the measurement.

### 5. Distinguish additive, semi-additive and non-additive measures.

**Additive** can be summed across every dimension (sales amount).
**Semi-additive** can be summed across some but **not time** (account balance —
summing Monday's and Tuesday's closing balance is meaningless). **Non-additive**
cannot be summed at all (ratios, percentages, unit price).

### 6. Distinguish KDD from data mining.

KDD is the whole discovery process — selection, preprocessing, transformation,
mining, evaluation. Data mining is **one step**, near the end. Preprocessing
and transformation take about 80% of the effort; mining about 10%.

### 7. Distinguish classification from clustering.

Classification is **supervised**: classes are known, training data is labelled,
and the model maps features to a known label. Clustering is **unsupervised**:
no labels exist and the groups are discovered. Classification puts records into
boxes you already have; clustering works out what the boxes should be.

### 8. What is the curse of dimensionality?

As dimensions grow, data becomes sparse, all pairwise distances converge toward
equality — so "nearest neighbour" loses meaning — and both computation and
overfitting risk grow. It breaks k-NN, K-Means and DBSCAN alike.

### 9. Distinguish feature selection from feature extraction.

**Selection** keeps a **subset of the original** attributes, so results stay
interpretable. **Extraction** (PCA) creates **new** attributes that are
combinations of the originals — more variance retained, no interpretability.

### 10. Distinguish SMC from the Jaccard coefficient.

SMC = (a + d)/(a + b + c + d) counts **joint absences (d)** as evidence of
similarity. Jaccard = a/(a + b + c) **ignores them**. For sparse asymmetric
data — market baskets, term vectors — joint absence is meaningless, so Jaccard
is correct. Use SMC only when 0 and 1 are equally informative.

### 11. Define support, confidence and lift.

```
support(X → Y)    = σ(X ∪ Y) / N
confidence(X → Y) = σ(X ∪ Y) / σ(X)
lift(X → Y)       = confidence(X → Y) / support(Y)
```

Support is frequency, confidence is reliability, lift is **interest**: > 1
positive association, = 1 independent, < 1 negative.

### 12. State the Apriori principle.

If an itemset is frequent, all its subsets are frequent. Contrapositively — and
this is the useful form — **if an itemset is infrequent, every superset is
infrequent**, so supersets need not be counted at all. This is the anti-monotone
property of support.

### 13. Why is confidence alone misleading?

Confidence is high whenever the **consequent is common**, regardless of any
real association. If 90% of all students study data science, then
`{cricket} → {data science}` has 90% confidence and a lift of exactly 1.00 —
the antecedent tells you nothing. Lift corrects for the consequent's base rate.

### 14. Distinguish a maximal from a closed frequent itemset.

**Maximal**: no **frequent** superset. **Closed**: no superset with the **same
support**. The maximal set tells you *which* itemsets are frequent but loses
their supports; the closed set is **lossless**. Every maximal itemset is
closed, not conversely.

### 15. Why does ID3 favour attributes with many values?

More branches means smaller, purer subsets **by arithmetic**, not by
informativeness. A unique identifier column splits into n pure singletons and
scores the maximum possible gain, while generalising to nothing. C4.5's gain
ratio divides by SplitInfo — the entropy of the partition sizes — to penalise
exactly that.

### 16. Distinguish precision from recall.

**Precision** = TP/(TP + FP): of everything **predicted** positive, how much
was. **Recall** = TP/(TP + FN): of everything **actually** positive, how much
was found. Precision is about the predictions; recall is about the truth.

### 17. What is the accuracy paradox?

On imbalanced data, a classifier that always predicts the majority class scores
high accuracy while being useless. With 1% fraud, always predicting
"legitimate" gives 99% accuracy and 0% recall. Report precision, recall and F1.

### 18. Why is F1 the harmonic mean?

Because it punishes imbalance. Precision 1.0 with recall 0.0 gives an
arithmetic mean of 0.5 — flattering — but an F1 of **0**, which is the honest
answer. F1 is high only when *both* are high.

### 19. Distinguish eager from lazy learning.

**Eager** learners (trees, Bayes, rules) build a model at training time: slow to
train, fast to predict. **Lazy** learners (k-NN) merely store the data: instant
"training", slow prediction, and a decision boundary formed locally per query.

### 20. What is the zero-frequency problem, and how is it fixed?

If any conditional probability in a Naïve Bayes product is zero, the **whole
product is zero** — one unseen attribute value vetoes the class regardless of
all other evidence. **Laplace (add-one) smoothing** fixes it:
`P(xᵢ|C) = (count + 1)/(count(C) + k)` where k is the number of distinct values
of that attribute.

### 21. Why can K-Means not cluster categorical data?

It needs a **mean**, and the mean of {red, green, blue} does not exist.
Integer-encoding the categories makes green the average of red and blue, which
K-Means will act on as if it were true. Use **k-Modes**, or ROCK/CACTUS.

### 22. Define core, border and noise points.

**Core**: at least MinPts points within ε, counting itself. **Border**: fewer
than MinPts within ε, but within ε of a core point. **Noise**: neither —
assigned to no cluster.

### 23. Name one failure case each for K-Means and DBSCAN.

K-Means fails on **non-spherical clusters** — two concentric rings, since every
boundary it draws is a hyperplane. DBSCAN fails on **clusters of varying
density** — a single ε suited to a dense cluster fragments a sparse one into
noise. OPTICS addresses the second.

### 24. What is a Clustering Feature in BIRCH?

The triple **CF = (N, LS, SS)** — count, linear sum, square sum. Centroid and
radius follow from those three numbers alone, so the points need not be kept,
and CFs **add**: `CF₁ + CF₂ = (N₁+N₂, LS₁+LS₂, SS₁+SS₂)`. That additivity is
what makes BIRCH single-pass.

### 25. What is a "link" in ROCK?

The **number of common neighbours** of two points, where two points are
neighbours if their similarity exceeds θ. Two baskets sharing only one item
have low pairwise similarity, but if many other baskets neighbour both, the
link count is high. Links capture global evidence that pairwise similarity
cannot see.

---

## Section B — Five-mark questions

### 1. Explain the five OLAP operations with examples.

| Operation | Effect | Example |
|---|---|---|
| **Roll-up** | Aggregate up a hierarchy, or drop a dimension | Sales by city → by state |
| **Drill-down** | Descend a hierarchy | Sales by quarter → by month |
| **Slice** | Fix **one** dimension to **one** value | Only Q1-2026 |
| **Dice** | Restrict **several** dimensions to sets | Dairy+Bakery, in AP+TS, in Q1+Q2 |
| **Pivot** | Exchange the axes | Months-down becomes months-across |

Roll-up and drill-down are inverses and both change the level of aggregation.
Slice reduces dimensionality by one; dice keeps the dimensionality and shrinks
the cube. Pivot changes neither — it is presentation only.

Two more exist: **drill-across** queries two fact tables through conformed
dimensions, and **drill-through** goes past the cube to the underlying detail.

### 2. Compare star and snowflake schemas.

| | Star | Snowflake |
|---|---|---|
| Dimensions | **Denormalised** | **Normalised** into sub-dimensions |
| Joins | Fewest — one per dimension | More — one per hierarchy level |
| Query speed | **Faster** | Slower |
| Redundancy | High | Low |
| Storage | More | Less |
| Complexity | Simple | Moderate |

The star deliberately violates Course 5's normalisation teaching. That is
correct, and saying why earns the marks: **normalisation optimises for writes**,
and a warehouse barely writes. It loads on a schedule and then serves millions
of reads, so the update anomalies that normalisation prevents never arise. The
denormalised design trades cheap storage for fewer joins, and a query with
three joins beats one with nine.

A **fact constellation** has multiple fact tables sharing **conformed
dimensions**, which is what makes cross-process analysis possible.

### 3. Explain the methods of handling missing data.

| Method | When | Danger |
|---|---|---|
| Ignore the tuple | Few rows, MCAR | Loses data; biased if MNAR |
| Fill manually | Small, valuable data | Infeasible at scale |
| Global constant | "Missing" is itself meaningful | Treated as a real category |
| Attribute **mean** | Numeric, symmetric | **Shrinks variance** |
| Attribute **median** | Numeric, **skewed** | Same, but robust |
| Class-conditional mean | Supervised setting | Leaks the label if done before splitting |
| Predict it (regression, k-NN, EM) | Most accurate | Costly; can invent structure |

Three points earn the extra marks. **Why the value is missing matters**: MCAR
is safe to drop, MNAR is not — high earners decline to state income, so
dropping them biases the mean downward and nothing in the data reveals it.
**Mean imputation shrinks the variance**, weakening every correlation and
making subsequent tests overconfident. And **impute after splitting**, never
before, or the training set encodes test information.

### 4. Explain PCA and how many components to retain.

PCA finds new orthogonal axes — principal components — that are linear
combinations of the originals, ordered by variance captured.

1. **Standardise** each attribute to mean 0, variance 1.
2. Compute the covariance matrix.
3. Find its eigenvalues and eigenvectors.
4. Sort by eigenvalue descending; keep the top k.
5. Project the data onto them.

Each eigenvalue is the variance along its component, so the proportion explained
is λᵢ/Σλ.

**Three stopping rules:** a cumulative-variance threshold (90% or 95%);
**Kaiser's criterion** (keep λ > 1 on standardised data); and the **scree plot
elbow**.

**Standardising is not optional.** PCA maximises variance, and variance depends
on units — leave income in rupees beside age in years and PC1 will be income
almost exactly, whatever the real structure.

The cost is **interpretability**: the components are combinations of every
original attribute, so no component is "age" any more. Where explanation
matters, use feature *selection* instead.

### 5. Explain the Apriori algorithm with an example.

Two steps: find all frequent itemsets (expensive), then generate strong rules
from them (cheap). With d items there are 2ᵈ − 1 possible itemsets, so brute
force is impossible; the **Apriori principle** makes it feasible.

```
L₁ = frequent 1-itemsets
while L(k-1) not empty:
    Cₖ = apriori_gen(L(k-1))          join, then PRUNE
    count Cₖ in one database pass
    Lₖ = candidates meeting minsup
```

`apriori_gen` **joins** two (k−1)-itemsets sharing their first k−2 items, then
**prunes** any candidate having a (k−1)-subset not in L(k−1).

With minsup count 3 on T1={A,C,D}, T2={B,C,E}, T3={A,B,C,E}, T4={B,E},
T5={A,B,C,E}:

```
L₁ = {A}:3 {B}:4 {C}:4 {E}:4        ({D}:1 pruned — and with it 15 itemsets)
L₂ = {A,C}:3 {B,C}:3 {B,E}:4 {C,E}:3
L₃ = {B,C,E}:3
```

At k=3 the candidate {A,C,E} arises from the join but **{A,E} ∉ L₂**, so it is
eliminated **without a single count**. That is the principle earning its keep.

### 6. Compare Apriori and FP-Growth.

| | Apriori | FP-Growth |
|---|---|---|
| Candidates | **Generated** — the bottleneck | **None** |
| Scans | k + 1 | **2** |
| Structure | Hash tree of candidates | **FP-tree** |
| Strategy | Breadth-first, level-wise | **Depth-first**, divide and conquer |
| Memory | Candidate set | **The whole tree** |
| Dense data | Poor | **Excellent** compression |
| Sparse data | Acceptable | Tree barely compresses |
| Implementation | Simple | Complex |

FP-Growth builds the tree in two scans: count items and sort them by descending
frequency (the F-list), then insert each transaction as a path, sharing
prefixes. Mining is recursive — for each item, take its **conditional pattern
base** (the prefix paths ending at it), build a conditional FP-tree, and recurse.

**Descending order is what makes it work**: frequent items share prefixes near
the root, keeping the tree small. Ascending order gives a tree the size of the
database.

**FP-Growth's weakness is memory** — the tree must fit in RAM, and on sparse
data with little prefix sharing it barely compresses. **Both algorithms always
produce the same frequent itemsets**; they differ only in how they get there.

### 7. Explain how C4.5 improves on ID3.

| Feature | ID3 | C4.5 |
|---|---|---|
| Criterion | Information gain | **Gain ratio** |
| Numeric attributes | ✗ | **✓** binary threshold splits |
| Missing values | ✗ | **✓** fractional instances |
| Pruning | ✗ | **✓** pessimistic error-based |
| Rule extraction | ✗ | ✓ |

**Gain ratio** = Gain / SplitInfo, where SplitInfo is the entropy of the
partition sizes. It penalises attributes with many, evenly sized branches —
precisely the case that inflated raw gain.

For a 14-value identifier: Gain = 0.9403 (the maximum), SplitInfo = log₂14 =
3.8074, so gain ratio = 0.2470. Be honest that this **reduces but does not
eliminate** the bias — 0.2470 still exceeds Outlook's 0.1564. C4.5 therefore
also requires an attribute's raw gain to be at least the average gain before
its ratio is considered, and relies on pruning and on identifiers being removed
in preprocessing.

**Numeric attributes** are split binarily: sort the values, test each midpoint
between adjacent values of differing class, take the best `A ≤ t`.

**Missing values** send the record down **all** branches, weighted by each
branch's proportion — a "fractional instance".

### 8. Explain overfitting and pruning.

A tree grown until every leaf is pure has memorised its training data including
its noise: training accuracy reaches 100% while **test accuracy falls**. The
gap between the two curves *is* the overfitting.

| | Pre-pruning | Post-pruning |
|---|---|---|
| When | Stop during construction | Grow fully, then cut back |
| Criteria | Max depth, min samples, min gain | Error on a validation set |
| Speed | Faster | Slower |
| Risk | **Horizon effect** | None |

The **horizon effect** is pre-pruning's real weakness: a split may look
worthless alone while enabling an excellent split one level deeper. Stop early
and you never find out — which is why post-pruning is generally preferred.

Post-pruning methods: **reduced-error** (replace a subtree with a leaf if
validation accuracy does not fall), **cost-complexity** (CART: minimise
`R(T) + α·|leaves|`, choosing α by cross-validation), **pessimistic error**
(C4.5, needs no validation set), and **MDL**.

### 9. Explain k-NN with a worked example.

Lazy learning: store the training data, and classify a query by majority vote
of its k nearest neighbours.

Training points by (height, weight): P1(158,58) Small, P2(160,59) Small,
P3(163,61) Small, P4(170,68) Large, P5(175,72) Large, P6(180,78) Large.
Classify q = (168, 65), k = 3:

```
P1: √(100+49)  = 12.207        P4: √(4+9)     =  3.606  ← nearest
P2: √(64+36)   = 10.000        P5: √(49+49)   =  9.899
P3: √(25+16)   =  6.403        P6: √(144+169) = 17.692
```

Three nearest: P4 (Large), P3 (Small), P5 (Large) → **Large** by 2–1.

**Note that k matters**: k = 1 gives Large; k = 5 adds P2 and P1, both Small,
giving **Small** by 3–2. Choose k by cross-validation, keep it **odd** for two
classes, and start around √n.

**k-NN requires normalisation** — unscaled features let the largest-range
attribute dominate every distance — and it degrades badly in high dimensions.

### 10. Explain DBSCAN with a worked example.

Density-based: clusters are dense regions, and sparse points are **noise**. Two
parameters — **ε** (neighbourhood radius) and **MinPts** — and three point
types: core (≥ MinPts within ε, counting itself), border (fewer, but within ε
of a core point), and noise.

On 1, 2, 3, 8, 9, 10, 25 with ε = 2, MinPts = 3:

| Point | Neighbours | Count | Type |
|---:|---|:---:|---|
| 1, 2, 3 | each other | 3 | Core |
| 8, 9, 10 | each other | 3 | Core |
| 25 | itself | 1 | **Noise** |

```
Cluster 1 = {1, 2, 3}   Cluster 2 = {8, 9, 10}   Noise = {25}
```

**Advantages over K-Means:** no k required, arbitrary cluster shapes, and
outliers identified rather than forced into a cluster. K-Means with k = 2 must
put 25 somewhere, dragging a centroid away from every real point.

**Its failure case is varying density** — a single ε that suits a dense cluster
fragments a sparse one into noise. OPTICS solves this by producing an ordering
across a range of ε.

---

## Section C — Ten-mark questions

### 1. Full Apriori trace with rules

**Question.** minsup count = 2, minconf = 70%. Find all frequent itemsets and
all strong rules with support, confidence and lift.

| TID | Items | | TID | Items |
|:---:|---|---|:---:|---|
| 1 | A, B, E | | 6 | B, C |
| 2 | B, D | | 7 | A, C |
| 3 | B, C | | 8 | A, B, C, E |
| 4 | A, B, D | | 9 | A, B, C |
| 5 | A, C | | | |

**Solution.** N = 9, minsup count = 2.

**Pass 1**

| Itemset | TIDs | Count |
|---|---|:---:|
| {A} | 1,4,5,7,8,9 | 6 ✓ |
| {B} | 1,2,3,4,6,8,9 | 7 ✓ |
| {C} | 3,5,6,7,8,9 | 6 ✓ |
| {D} | 2,4 | 2 ✓ |
| {E} | 1,8 | 2 ✓ |

**Pass 2** — all 10 pairs:

| Itemset | TIDs | Count | ✓ |
|---|---|:---:|:-:|
| {A,B} | 1,4,8,9 | 4 | ✓ |
| {A,C} | 5,7,8,9 | 4 | ✓ |
| {A,D} | 4 | 1 | ✗ |
| {A,E} | 1,8 | 2 | ✓ |
| {B,C} | 3,6,8,9 | 4 | ✓ |
| {B,D} | 2,4 | 2 | ✓ |
| {B,E} | 1,8 | 2 | ✓ |
| {C,D} | — | 0 | ✗ |
| {C,E} | 8 | 1 | ✗ |
| {D,E} | — | 0 | ✗ |

**Pass 3** — the join gives seven candidates; **five are pruned without being
counted**:

| Candidate | Failing subset | |
|---|---|:-:|
| {A,B,C} | none | count 2 ✓ |
| {A,B,E} | none | count 2 ✓ |
| {A,B,D} | {A,D} ✗ | **pruned** |
| {A,C,E} | {C,E} ✗ | **pruned** |
| {B,C,E} | {C,E} ✗ | **pruned** |
| {B,C,D} | {C,D} ✗ | **pruned** |
| {B,D,E} | {D,E} ✗ | **pruned** |

**Pass 4** — {A,B,C,E} needs {A,C,E} ∉ L₃, so pruned. C₄ = ∅, stop.

**13 frequent itemsets:** {A} {B} {C} {D} {E} {A,B} {A,C} {A,E} {B,C} {B,D}
{B,E} {A,B,C} {A,B,E}

**Rules from the 3-itemsets** (2³ − 2 = 6 each, support 2/9 = 0.222):

From {A,B,C} — every confidence is at most 0.50, so **no strong rules**:
{A,B}→{C} 0.50, {A,C}→{B} 0.50, {B,C}→{A} 0.50, {A}→{B,C} 0.333,
{B}→{A,C} 0.286, {C}→{A,B} 0.333.

From {A,B,E}:

| Rule | Confidence | Lift | Strong? |
|---|---|---|:-:|
| {A,B} → {E} | 2/4 = 0.500 | 2.250 | ✗ |
| **{A,E} → {B}** | 2/2 = **1.000** | 1.286 | ✓ |
| **{B,E} → {A}** | 2/2 = **1.000** | 1.500 | ✓ |
| {A} → {B,E} | 2/6 = 0.333 | 1.500 | ✗ |
| {B} → {A,E} | 2/7 = 0.286 | 1.286 | ✗ |
| **{E} → {A,B}** | 2/2 = **1.000** | 2.250 | ✓ |

**Three strong rules**, all with confidence 1.00. **Lift is what separates
them**: `{E} → {A,B}` at 2.25 is by far the most interesting — E buyers are
2.25× more likely than average to buy A and B together — while `{A,E} → {B}` at
1.286 is barely above independence despite the identical confidence.

Note the symmetry check: lift({A,B}→{E}) = lift({E}→{A,B}) = 2.250, as lift
must be, while their confidences differ (0.500 vs 1.000).

**A completeness note.** The question asked for rules from the *largest*
frequent itemsets. Mining the whole lattice also yields three strong rules from
**2-itemsets** — `{D} → {B}` (confidence 1.00, lift 1.286), `{E} → {A}` (1.00,
1.500) and `{E} → {B}` (1.00, 1.286). A real Apriori run reports these too, so
say "from the 3-itemsets" when your answer is scoped that way.

### 2. Full ID3 trace

**Question.** Build a decision tree with ID3 for the weather data of Unit 4,
showing every entropy and gain.

**Solution.** 9 Yes, 5 No, N = 14.

```
Entropy(S) = −(9/14)log₂(9/14) − (5/14)log₂(5/14)
           = 0.4098 + 0.5305 = 0.9403
```

**Root — gain for each attribute:**

| Attribute | Partition | Weighted entropy | **Gain** |
|---|---|---:|---:|
| **Outlook** | Sunny(2Y,3N) e=0.9710; Overcast(4Y,0N) e=0; Rain(3Y,2N) e=0.9710 | 0.6935 | **0.2467** |
| Humidity | High(3Y,4N) e=0.9852; Normal(6Y,1N) e=0.5917 | 0.7885 | 0.1518 |
| Wind | Weak(6Y,2N) e=0.8113; Strong(3Y,3N) e=1.0 | 0.8922 | 0.0481 |
| Temperature | Hot(2Y,2N) e=1.0; Mild(4Y,2N) e=0.9183; Cool(3Y,1N) e=0.8113 | 0.9111 | 0.0292 |

**Outlook is the root.** Overcast (4Y, 0N) is pure → leaf **Yes**.

**Sunny branch** (2Y, 3N, entropy 0.9710):

| Attribute | Partition | Weighted | Gain |
|---|---|---:|---:|
| **Humidity** | High(0Y,3N); Normal(2Y,0N) — both pure | **0.0** | **0.9710** |
| Temperature | Hot(0Y,2N); Mild(1Y,1N); Cool(1Y,0N) | 0.4000 | 0.5710 |
| Wind | Weak(1Y,2N); Strong(1Y,1N) | 0.9510 | 0.0200 |

**Humidity** splits it perfectly.

**Rain branch** (3Y, 2N, entropy 0.9710):

| Attribute | Partition | Weighted | Gain |
|---|---|---:|---:|
| **Wind** | Weak(3Y,0N); Strong(0Y,2N) — both pure | **0.0** | **0.9710** |
| Temperature | Mild(2Y,1N); Cool(1Y,1N) | 0.9510 | 0.0200 |
| Humidity | High(1Y,1N); Normal(2Y,1N) | 0.9510 | 0.0200 |

**Wind** splits it perfectly.

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

**Two observations worth stating.** Every leaf is pure, so the tree classifies
all 14 training records correctly — which is exactly the condition under which
you should suspect overfitting, and why C4.5 would prune. And **Temperature
never appears**: ID3 found it uninformative and dropped it, performing feature
selection for free.

As rules:

```
R1: IF Outlook = Overcast                    THEN Yes
R2: IF Outlook = Sunny AND Humidity = Normal THEN Yes
R3: IF Outlook = Sunny AND Humidity = High   THEN No
R4: IF Outlook = Rain AND Wind = Weak        THEN Yes
R5: IF Outlook = Rain AND Wind = Strong      THEN No
```

These five rules are exactly the five root-to-leaf paths, and are automatically
mutually exclusive and exhaustive because tree paths partition the space.

### 3. Naïve Bayes with Laplace smoothing

**Question.** Using the same weather data, classify
X = (Sunny, Cool, High, Strong). Then explain what happens for
(Overcast, Hot, High, Strong) and fix it.

**Solution.**

Priors: P(Yes) = 9/14 = 0.6429, P(No) = 5/14 = 0.3571.

| Value | P(·\|Yes) | P(·\|No) |
|---|---|---|
| Outlook = Sunny | 2/9 | 3/5 |
| Temperature = Cool | 3/9 | 1/5 |
| Humidity = High | 3/9 | 4/5 |
| Wind = Strong | 3/9 | 3/5 |

```
P(X|Yes)·P(Yes) = (2/9)(3/9)(3/9)(3/9)(9/14) =  486/91854 = 0.005291
P(X|No) ·P(No)  = (3/5)(1/5)(4/5)(3/5)(5/14) =  180/8750  = 0.020571
```

**0.020571 > 0.005291 → predict No.**

```
Normalised: P(No|X) = 0.020571/0.025862 = 0.7954   (79.5%)
            P(Yes|X)= 0.005291/0.025862 = 0.2046   (20.5%)
```

**Now X = (Overcast, Hot, High, Strong).** No Overcast day has Play = No, so
`P(Overcast | No) = 0/5 = 0` and therefore

```
P(X|No)·P(No) = 0 × (2/5) × (4/5) × (3/5) × (5/14) = 0   exactly
```

**One unseen value has vetoed the entire class**, however strongly the other
three attributes might have argued for it. That is the **zero-frequency
problem**.

**Laplace smoothing** adds 1 to every count, with k added to the denominator
where k is the number of distinct values of that attribute. Outlook has k = 3:

```
P(Overcast | No) = (0+1)/(5+3) = 1/8 = 0.125     (was 0)
P(Sunny    | No) = (3+1)/(5+3) = 4/8 = 0.500     (was 0.600)
P(Rain     | No) = (2+1)/(5+3) = 3/8 = 0.375     (was 0.400)
                                       ────
                                        8/8 = 1.0 ✓
```

The estimates shift slightly, still sum to 1, and **no probability is ever
zero**, so no single unseen value can veto a class.

Two further points worth a mark each. Real implementations sum **logarithms**
rather than multiplying probabilities, because a product of fifty values around
0.1 underflows to zero in floating point; log is monotonic so the argmax is
unchanged. And the independence assumption is **almost always false**, yet
Naïve Bayes works well anyway — because classification needs only the
**ranking** of the posteriors to be right, not their values.

### 4. Comparing four classifiers

**Question.** Compare decision trees, rule-based classifiers, k-NN and Naïve
Bayes on principle, strengths, weaknesses and appropriate use.

**Solution.**

| | **Decision tree** | **Rule-based** | **k-NN** | **Naïve Bayes** |
|---|---|---|---|---|
| Principle | Recursive purity-maximising splits | IF–THEN rules from sequential covering | Majority vote of nearest neighbours | Bayes' theorem + conditional independence |
| Learning | **Eager** | Eager | **Lazy** | Eager |
| Training cost | Moderate | Moderate | **None** | **Very low** |
| Prediction cost | **Very low** | Low | **High** — scans all data | Very low |
| Memory | The tree | The rule list | **The whole dataset** | Counts only |
| Interpretable | **Good** | **Best** | Poor | Moderate |
| Needs scaling | **No** | No | **Yes** | No |
| Handles categorical | **Yes** | Yes | Awkwardly | **Yes** |
| Handles missing | C4.5 does | Yes | Poorly | **Yes** — skip the term |
| Incremental | No | No | **Yes** — just add a record | **Yes** |
| Decision boundary | Axis-parallel rectangles | Rectangles | **Arbitrary, local** | Quadratic/linear |
| Main weakness | Unstable; overfits | Conflict resolution | Curse of dimensionality | Independence assumption |

**When to use each.**

**Decision tree** when you must *explain* the decision — credit scoring,
medical triage, anything a regulator will audit. Its instability (a few changed
records give a different tree) is fixed by **Random Forest**, at the cost of
exactly the interpretability you chose it for.

**Rule-based** when the concept is disjunctive. A tree handles
`(A AND B) OR (C AND D)` only by duplicating a subtree in several branches —
the **replicated subtree problem** — while two rules state it directly.

**k-NN** when the boundary is complex and irregular, the dataset is small, and
new data arrives continually. Never in high dimensions, and never without
normalising first.

**Naïve Bayes** when there are very many attributes and little training data —
text classification is the canonical case, since it estimates one parameter per
word per class rather than modelling any interaction. It is also the natural
choice when predictions must be updated incrementally.

**The honest closing point:** on tabular data, none of these four is usually
the best-performing model — gradient-boosted trees are. These four are taught
because each embodies a distinct and comprehensible principle, and because
understanding them is what lets you diagnose the ones that follow.
