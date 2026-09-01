# Unit 5 — Unsupervised Learning

**Syllabus topics:** Introduction of unsupervised learning; unsupervised vs
supervised learning; application of unsupervised learning; clustering and its
types; partitioning method — k-Means and k-Medoids; hierarchical clustering;
density-based methods — DBSCAN. Case studies of ML applications — image
recognition, speech recognition, email spam filtering, online fraud detection
and other.

---

## 5.1 A note on the overlap with Course 8

**Course 8 Unit 5 taught all four of these algorithms**, and traced K-Means to
convergence by hand.

| Topic | Course 8 | New here |
|---|---|---|
| K-Means, WCSS, the elbow | §5.2 — traced by hand to convergence | **Validation metrics** and the k=2/k=3 disagreement |
| k-Medoids / PAM | §5.3 | Nothing conceptually |
| Hierarchical, linkage, dendrograms | §5.4 | **Linkage compared numerically** |
| DBSCAN | §5.5 | **Measured against K-Means on non-convex data** |

**What is genuinely new is evaluation** — how you judge a clustering when there
is no correct answer. That is §5.7, and it is the hardest idea in the unit.

---

## 5.2 Unsupervised versus supervised learning

| | **Supervised** | **Unsupervised** |
|---|---|---|
| Input | Features **and labels** | **Features only** |
| Goal | Predict the label | **Find structure** |
| Ground truth | **Exists** | **Does not** |
| Evaluation | Straightforward — compare to held-out labels | **Hard** — §5.7 |
| Risk | Overfitting | **Finding structure that is not there** |
| Output can be | Verified | Only **judged** |

### ⚠️ The defining difficulty

**A clustering algorithm always returns clusters.** Ask K-Means for four groups
in pure random noise and it will give you four, with centroids, sizes and a
tidy plot. Nothing in the output says "there was no structure here."

That is why §5.7 exists, and why "how do you know the clustering is any good?"
is the ten-mark question in this unit.

### 🔢 The three families of unsupervised task

| Task | Finds | Algorithms | Where |
|---|---|---|---|
| **Clustering** | Groups of similar instances | K-Means, DBSCAN, hierarchical | This unit |
| **Dimensionality reduction** | A lower-dimensional representation | **PCA**, t-SNE, UMAP | **Unit 2 §2.10** |
| **Association rules** | Items that co-occur | Apriori, FP-Growth | **Course 8 Unit 3** |

Anomaly detection is often listed as a fourth — Isolation Forest, one-class
SVM, or simply "the small clusters and the noise points".

---

## 5.3 Applications of unsupervised learning

| Application | Task | Note |
|---|---|---|
| **Customer segmentation** | Clustering | The canonical business case |
| Market basket analysis | Association | Course 8's Apriori |
| **Anomaly / fraud detection** | Clustering, density | Fraud is a low-density region |
| Document / topic grouping | Clustering on TF-IDF | Course 8 experiment 15 |
| Image compression | Clustering colours | K-Means on pixel values |
| **Dimensionality reduction before a supervised model** | PCA | Unit 2 §2.10 |
| Recommender systems | Clustering, matrix factorisation | Course 6 §4.6 |
| Genomics | Hierarchical clustering | Dendrograms of gene expression |

---

## 5.4 Clustering and its types

| Type | Idea | Algorithms | Cluster shape |
|---|---|---|---|
| **Partitioning method** | Split into k non-overlapping groups | **K-Means, k-Medoids** | **Convex, roughly spherical** |
| **Hierarchical** | Build a tree of nested clusters | Agglomerative, divisive | Any, depending on linkage |
| **Density-based** | Clusters are dense regions separated by sparse ones | **DBSCAN**, OPTICS | **Arbitrary** |
| Grid-based | Quantise space into cells | STING, CLIQUE | Rectangular |
| Model-based | Assume a mixture of distributions | **GMM / EM** | Elliptical |

| | Hard | Soft (fuzzy) |
|---|---|---|
| Membership | One cluster per point | A **degree** of membership in each |
| Example | K-Means | Fuzzy c-means, **GMM** |

---

## 5.5 K-Means — the partitioning method

### 🔢 The algorithm

1. Choose **k**, and initialise k centroids.
2. **Assign** each point to its nearest centroid.
3. **Update** each centroid to the mean of its assigned points.
4. Repeat 2–3 until assignments stop changing.

It minimises **within-cluster sum of squares**:

> **WCSS = Σ_clusters Σ_points ‖x − μ_cluster‖²**

Also called **inertia**. It never increases across iterations, so the algorithm
always converges — **to a local minimum**, not necessarily the best one.

### 🔢 The elbow method, on standardised iris

| k | WCSS | Silhouette |
|---:|---:|---:|
| 1 | **600.0000** | — |
| 2 | 222.3617 | **0.5818** |
| 3 | 139.8205 | 0.4599 |
| 4 | 114.0925 | 0.3869 |
| 5 | 90.9275 | 0.3459 |
| 6 | 81.5444 | 0.3171 |

**WCSS at k = 1 is exactly 600 = 150 × 4** — the number of points times the
number of standardised features, each contributing variance 1. That is a free
arithmetic check that the data really was standardised.

The big drops are to k = 2 (−377.6) and k = 3 (−82.5); after that it flattens.
**The elbow is at k = 2 or 3.**

### ⚠️ The most instructive result in this unit

**Silhouette says k = 2. The truth is k = 3.**

Iris has three species. Silhouette peaks at **k = 2 (0.5818)** and *falls* at
k = 3 (0.4599). The algorithm is not broken and the metric is not broken:
**setosa is cleanly separate, while versicolor and virginica overlap**, so by a
geometric measure two groups genuinely are tidier than three.

At k = 3, agreement with the true species is **ARI 0.6201** — decent, not
excellent, and that is the ceiling on this data.

**The lesson, and it is the answer to the ten-mark question:** an internal
metric measures *geometric tidiness*, not *correctness*. It cannot know what
the clusters are supposed to mean. **Never choose k from silhouette alone —
combine it with the elbow, with domain knowledge, and with whether the clusters
are actually useful.**

### ⚠️ K-Means's weaknesses — Course 8 §5.2 listed five

1. **k must be chosen in advance.**
2. **Sensitive to initialisation** — it finds a local minimum. Fixed by
   `k-means++` initialisation and `n_init` restarts, both defaults now.
3. **Assumes spherical, similarly-sized clusters.** §5.7 measures the failure.
4. **Sensitive to outliers** — the mean is not robust; one extreme point drags
   a centroid.
5. **Requires scaling**, since it is distance-based.

Add a sixth worth knowing: **it forces every point into a cluster.** There is
no "this point belongs to nothing", which is exactly what DBSCAN adds.

---

## 5.6 k-Medoids (PAM)

**The same idea, but each cluster centre is an actual data point — a medoid —
rather than a computed mean.**

| | **K-Means** | **k-Medoids (PAM)** |
|---|---|---|
| Centre | The **mean** — usually not a real point | An **actual data point** |
| Minimises | Sum of squared **Euclidean** distances | Sum of **any** distances |
| Distance metric | Euclidean, effectively | **Any** — including categorical or precomputed |
| Outliers | **Sensitive** | **Robust** |
| Cost | O(nkt) — **fast** | O(k(n−k)²) per iteration — **slow** |
| Interpretability | A centroid may be meaningless | The medoid is a **real, exhibitable example** |

**Two reasons to prefer medoids**, and both are exam answers:

1. **Robustness.** The mean of {1, 2, 3, 100} is 26.5; the medoid is 3.
2. **A representative you can show someone.** "This customer is the typical
   member of segment 2" is possible with a medoid and not with a centroid.

**CLARA** is PAM applied to samples, for large n.

---

## 5.7 Hierarchical clustering

### 🔢 Agglomerative and divisive

| | **Agglomerative** | **Divisive** |
|---|---|---|
| Direction | **Bottom-up** — each point its own cluster, merge | **Top-down** — one cluster, split |
| Common? | **Yes, almost always** | Rare |
| Cost | O(n³) naive, O(n² log n) tidy | Worse |

**The dendrogram** records the merge order; cutting it at a height gives a
clustering, and **k does not have to be chosen in advance** — that is
hierarchical clustering's main advantage.

### 🔢 Linkage — measured on iris

**Linkage defines the distance between two *clusters*.**

| Linkage | Distance between clusters | ARI vs species | Silhouette |
|---|---|---:|---:|
| **Ward** | Merge that minimises the increase in WCSS | **0.6153** | 0.4467 |
| **Complete** | The **farthest** pair | 0.5726 | 0.4496 |
| **Average** | The mean of all pairs | 0.5621 | 0.4803 |
| **Single** | The **closest** pair | 0.5584 | **0.5046** |

### ⚠️ The same disagreement again, and it is worth noticing

**Ward has the best agreement with the truth (ARI 0.6153) and the worst
silhouette (0.4467). Single linkage is the reverse.**

Once more: an internal metric rewards geometric tidiness, and geometric
tidiness is not correctness. **Ward is the sensible default** — it is the only
linkage that optimises the same quantity as K-Means — and single linkage
suffers from **chaining**, where a thread of intermediate points merges two
genuinely distinct clusters.

---

## 5.8 DBSCAN

### 🎯 The idea

**Clusters are dense regions separated by sparse ones.** Points in sparse
regions are labelled **noise** and belong to no cluster.

### 🔢 The two parameters, and three kinds of point

| Parameter | Meaning |
|---|---|
| **eps (ε)** | The radius of a point's neighbourhood |
| **minPts** | How many points must be within ε for a point to be *core* |

| Point type | Definition |
|---|---|
| **Core** | Has at least minPts neighbours within ε |
| **Border** | Within ε of a core point, but not core itself |
| **Noise** | Neither — **assigned to no cluster** |

**Heuristics:** minPts ≥ p + 1, often 2p. Choose ε from a **k-distance plot** —
sort every point's distance to its k-th neighbour and take the elbow.

### 🔢 DBSCAN against K-Means on non-convex clusters — measured

Two interleaved crescents ("two moons"), 300 points, which are obviously two
clusters to any human eye:

| Algorithm | ARI against the truth |
|---|---:|
| **K-Means (k=2)** | **0.2475** |
| **DBSCAN (eps=0.25, minPts=5)** | **1.0000** |

**DBSCAN recovers the two crescents perfectly, with zero noise points.
K-Means scores 0.2475 — barely better than random.**

The reason is structural, not a matter of tuning: **K-Means partitions space
with straight boundaries** (each point goes to the nearest centroid, so the
boundaries are perpendicular bisectors). A crescent cannot be carved out that
way at any k. **DBSCAN follows density**, so shape does not matter.

**This is the cleanest experiment in the unit**, and the answer to "when would
you prefer DBSCAN?"

### 🔢 The comparison

| | **K-Means** | **DBSCAN** | **Hierarchical** |
|---|---|---|---|
| k in advance | **Yes** | **No** | No — cut the dendrogram |
| Cluster shape | **Convex only** | **Arbitrary** | Depends on linkage |
| Outliers | Forced into a cluster | **Labelled noise** | Forced in |
| Varying density | Fine | **Struggles** — one ε for all | Fine |
| Complexity | O(nkt) — **fast** | O(n log n) with an index | O(n²)–O(n³) — **slow** |
| Parameters | k | **eps, minPts** — harder to set | Linkage, cut height |
| Deterministic | No (initialisation) | **Yes**, except for border points | Yes |

⚠️ **DBSCAN's real weakness is varying density.** A single ε cannot suit a
dataset with both dense and sparse genuine clusters — it will merge the dense
ones or call the sparse ones noise. **OPTICS** is the fix.

---

## 5.9 Evaluating a clustering

### 🎯 The hard part of unsupervised learning

**With no labels there is no accuracy.** Metrics fall into two kinds, and
knowing the difference is the point.

### 🔢 Internal metrics — geometry only, no labels needed

| Metric | Measures | Good is |
|---|---|---|
| **Silhouette** | (b − a)/max(a, b) per point: how much closer to its own cluster than the next | **Near +1**; 0 = on a boundary; negative = **in the wrong cluster** |
| **Davies–Bouldin** | Average similarity of each cluster to its most similar one | **Low** |
| Calinski–Harabasz | Between-cluster over within-cluster dispersion | **High** |
| **WCSS / inertia** | Compactness | Low — but it **always** falls with k, so it needs the elbow |

### 🔢 External metrics — when labels do exist, for validation only

| Metric | Note |
|---|---|
| **Adjusted Rand Index (ARI)** | Agreement between two partitions, **corrected for chance**. 0 = random, 1 = identical |
| Normalized Mutual Information | Shared information between the partitions |
| Homogeneity / completeness / V-measure | Each cluster one class / each class one cluster / their harmonic mean |

⚠️ **Use the plain Rand Index and a random clustering scores well above zero.**
ARI subtracts the expected agreement, which is why it is the one to quote.

### 💡 The honest summary

**No metric tells you a clustering is correct**, because correctness is not
defined without a purpose. This unit gives two measured demonstrations of
exactly that:

- Silhouette prefers **k = 2** on iris, where the truth is **3**.
- Silhouette prefers **single linkage**, where **Ward** agrees best with the
  truth.

**The real test is usefulness:** are the segments actionable? do they persist
in new data? can a domain expert name them? Say that, and give the two
numerical examples as evidence — that is a full ten-mark answer.

---

## 5.10 Case studies

The syllabus names four, and each illustrates a different difficulty.

| Case study | Task | The interesting part |
|---|---|---|
| **Image recognition** | Multi-class classification | Raw pixels are poor features. Classical ML needs engineered features (edges, HOG); this is why deep learning took over — it learns the features. **Course 14 A** |
| **Speech recognition** | Sequence classification | The input is a **variable-length time series**, so a fixed feature matrix does not fit. Needs MFCC features plus a sequence model |
| **Email spam filtering** | Binary classification | **Naive Bayes' home ground** (§4.4). Also **adversarial** — spammers adapt, so the model decays faster than most: concept drift with an opponent |
| **Online fraud detection** | Binary classification, **extremely imbalanced** | Positives ~0.1%, so **accuracy is useless** (Unit 2 §2.5). Optimise recall at an acceptable precision; costs are asymmetric and known in rupees; decisions must be made in milliseconds and be explainable to a regulator |

### 💡 Fraud detection is the best case study to prepare

It exercises nearly every idea in the course: extreme imbalance, the base-rate
argument, precision–recall over accuracy, threshold tuning, cost-sensitive
learning, **anomaly detection as an unsupervised alternative when fraud
patterns are unknown**, interpretability for regulators, and concept drift
because fraudsters adapt.

**If you prepare one case study in depth, prepare this one.**

---

## Practice problems

### Problem 1

Distinguish supervised from unsupervised learning. Explain the types of
clustering. *(10 marks)*

**Solution.**

Give the comparison table — input, goal, whether ground truth exists, how each
is evaluated, and the characteristic risk of each.

**Then the sentence that shows understanding:** *a clustering algorithm always
returns clusters.* Ask K-Means for four groups in pure noise and it produces
four, with centroids and a tidy plot, and nothing in the output says there was
no structure. That is why evaluation is the hard part.

**Types of clustering:** partitioning (K-Means, k-Medoids — convex clusters,
k chosen in advance); hierarchical (agglomerative or divisive, producing a
dendrogram, k chosen afterwards); density-based (DBSCAN — arbitrary shapes,
explicit noise); grid-based; model-based (GMM/EM — soft membership). Add the
hard/soft distinction.

Mention the other two unsupervised tasks — **dimensionality reduction** (PCA,
Unit 2) and **association rules** (Course 8) — since the syllabus's
"unsupervised learning" is broader than clustering alone.

### Problem 2

Explain K-Means. How is k chosen, and what are its weaknesses? *(10 marks)*

**Solution.**

**The algorithm** in four steps — initialise k centroids, assign each point to
the nearest, recompute centroids as means, repeat to convergence — and the
objective it minimises, **WCSS = Σ‖x − μ‖²**, noting that WCSS never increases
so convergence is guaranteed, **to a local minimum**.

**Choosing k — the elbow method**, with the worked figures on standardised
iris:

| k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| WCSS | 600.00 | 222.36 | 139.82 | 114.09 | 90.93 | 81.54 |

Note that **WCSS at k=1 is exactly 600 = 150 × 4**, a free check that the data
was standardised. The big drops are to k=2 and k=3; then it flattens.

**Then the result worth the top marks:** silhouette peaks at **k = 2 (0.5818)**
and falls at k = 3 (0.4599) — but iris has **three** species. Nothing is
broken: setosa is cleanly separate while versicolor and virginica overlap, so
geometrically two groups really are tidier. **An internal metric measures
tidiness, not correctness.** Never choose k from silhouette alone.

**The weaknesses:** k must be chosen in advance; sensitive to initialisation
(fixed by k-means++ and multiple restarts); assumes **spherical, similarly
sized** clusters; sensitive to outliers because the mean is not robust;
requires scaling; and **forces every point into a cluster** — there is no
"belongs to nothing", which is what DBSCAN adds.

### Problem 3

Compare K-Means, hierarchical clustering and DBSCAN. When would you prefer
each? *(10 marks)*

**Solution.**

Give the comparison table — k in advance, cluster shape, outlier handling,
varying density, complexity, parameters, determinism.

**Then the measured demonstration, which is what earns the top marks.** On two
interleaved crescents that any human sees as two clusters:

| Algorithm | ARI |
|---|---:|
| K-Means (k=2) | **0.2475** |
| DBSCAN | **1.0000** |

**DBSCAN recovers them perfectly; K-Means is barely better than random.** The
reason is structural: K-Means assigns each point to the nearest centroid, so
its boundaries are straight perpendicular bisectors, and **no value of k carves
out a crescent**. DBSCAN follows density, so shape is irrelevant.

**When to prefer each:**

- **K-Means** — large n, roughly spherical clusters, k known or guessable,
  speed matters. The default first attempt.
- **Hierarchical** — small n, k unknown, and you want the **dendrogram** to see
  structure at every level. Use **Ward** linkage; single linkage suffers from
  chaining.
- **DBSCAN** — arbitrary shapes, outliers that should be *labelled* rather than
  forced into a cluster, k unknown. **Its weakness is varying density**, since
  one ε must serve the whole dataset; OPTICS fixes that.

### Problem 4

How do you evaluate a clustering when there are no labels? *(10 marks)*

**Solution.**

**Start with the difficulty:** with no labels there is no accuracy, and a
clustering algorithm always returns clusters whether or not structure exists.

**Internal metrics** — computed from geometry alone: **silhouette**
((b − a)/max(a, b) per point; near +1 good, negative means the point is in the
wrong cluster), **Davies–Bouldin** (low is good), **Calinski–Harabasz** (high),
and **WCSS**, which always falls with k and so needs the elbow.

**External metrics** — only when labels exist, for validation: **Adjusted Rand
Index**, corrected for chance so random scores 0; NMI; homogeneity and
completeness. Note that the *unadjusted* Rand Index gives a random clustering a
score well above zero, which is why ARI is the one to quote.

**Then the two measured demonstrations that internal metrics are not
correctness:**

1. On iris, silhouette prefers **k = 2 (0.5818)** over **k = 3 (0.4599)**, but
   there are three species — because versicolor and virginica overlap.
2. On the same data, **Ward linkage agrees best with the truth (ARI 0.6153) yet
   has the worst silhouette (0.4467)**, while single linkage is the reverse.

**Conclude honestly:** no metric establishes that a clustering is correct,
because correctness is undefined without a purpose. The real tests are whether
the clusters are **actionable**, **stable in new data**, and **nameable by a
domain expert** — with the internal metrics as evidence, not verdicts.

---

## Exam questions from this unit

**Two marks**

1. What does WCSS measure?
2. Why does K-Means converge?
3. Give one advantage of k-Medoids over K-Means.
4. What are DBSCAN's two parameters?
5. What is a border point?
6. What does a negative silhouette value mean?
7. Why is ARI preferred to the Rand Index?

**Five marks**

1. Distinguish supervised from unsupervised learning.
2. Explain the elbow method.
3. Compare K-Means and k-Medoids.
4. Explain agglomerative clustering and linkage criteria.
5. Explain DBSCAN's core, border and noise points.
6. Explain any two applications of unsupervised learning.

**Ten marks**

1. Explain K-Means, choosing k, and its weaknesses.
2. Compare K-Means, hierarchical clustering and DBSCAN with a worked example.
3. How do you evaluate a clustering with no labels?
4. Explain one case study — fraud detection is the richest — and the machine
   learning decisions it requires.

---

## Mistakes that cost marks

- **Saying WCSS chooses k.** It falls monotonically with k; only the *elbow*
  says anything.
- **Trusting silhouette as ground truth.** It prefers k = 2 on iris, where the
  answer is 3.
- **Saying DBSCAN "handles outliers better".** It **labels them as noise** and
  assigns them to no cluster — that is a different and stronger claim.
- **Claiming K-Means fails on the moons because k was wrong.** k = 2 is
  correct; the boundaries are straight, and no k fixes that.
- **Forgetting to scale before clustering.** All three are distance-based.
- **Calling hierarchical clustering parameter-free.** Linkage and cut height
  are both choices.
- **Using accuracy on a clustering.** Cluster labels are arbitrary integers;
  use ARI.
- **Saying fraud detection is "just classification".** 0.1% positives makes
  accuracy useless and changes every methodological decision.
