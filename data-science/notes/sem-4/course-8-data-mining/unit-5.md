# Unit 5 — Clustering Techniques

**Syllabus topics:** Clustering Paradigms, Partitioning Algorithms
(K-Means), k-Medoid Algorithms, Hierarchical Clustering: DBSCAN, BIRCH,
Categorical Clustering Algorithms: STIRR, ROCK, CACTUS.

> The syllabus groups DBSCAN and BIRCH under "Hierarchical Clustering". That is
> **wrong**: DBSCAN is density-based and BIRCH is hierarchical only in its first
> phase. The correct taxonomy is in §5.1, and the misclassification is recorded
> in [SYLLABUS-REVIEW.md](../../../SYLLABUS-REVIEW.md).

---

## 5.1 Clustering paradigms

### 🎯 The big idea

**Clustering groups records so that records within a group are similar to each
other and dissimilar to those in other groups** — with no labels to learn from.

It is **unsupervised**. Nobody says what the groups should be; the algorithm
proposes them, and a human decides whether they mean anything.

| | Classification | Clustering |
|---|---|---|
| Labels | Given | **None** |
| Learning | Supervised | **Unsupervised** |
| Goal | Assign to known classes | **Discover** the groups |
| Evaluation | Accuracy against truth | Cohesion, separation, interpretation |
| "Correct" answer | Exists | **Often does not** |

That last row is the one students underestimate. There is frequently **no
single right clustering** — customers can be validly grouped by spending, by
geography, or by product category, and the algorithm cannot know which you
meant.

### 🔢 What makes a clustering good

| Property | Meaning |
|---|---|
| **Cohesion (intra-cluster)** | Points within a cluster are close — **minimise** |
| **Separation (inter-cluster)** | Clusters are far apart — **maximise** |

**Silhouette coefficient** combines both, per point:

```
s(i) = (b(i) − a(i)) / max(a(i), b(i))

  a(i) = mean distance from i to the other points in ITS cluster
  b(i) = mean distance from i to the points of the NEAREST OTHER cluster
```

| s(i) | Meaning |
|---|---|
| ≈ +1 | Well clustered — far from other clusters |
| ≈ 0 | On a boundary between two clusters |
| ≈ −1 | **Probably in the wrong cluster** |

The mean silhouette over all points measures the whole clustering, and
comparing it across values of k is the standard way to choose k.

**Davies–Bouldin index** — the average, over clusters, of the worst-case ratio
of within-cluster scatter to between-cluster separation. **Lower is better**,
which is the opposite of silhouette and a frequent source of confusion.

### The paradigms

| Paradigm | Idea | Algorithms |
|---|---|---|
| **Partitioning** | Divide into k non-overlapping groups; iterate to improve | K-Means, K-Medoids (PAM, CLARA) |
| **Hierarchical** | Build a tree of nested clusters | AGNES, DIANA, BIRCH, CURE, Chameleon |
| **Density-based** | Clusters are dense regions separated by sparse ones | **DBSCAN**, OPTICS, DENCLUE |
| **Grid-based** | Quantise the space into cells, cluster the cells | STING, CLIQUE, WaveCluster |
| **Model-based** | Assume the data comes from a mixture of distributions | EM, Gaussian mixtures, SOM |
| **Categorical** | Designed for non-numeric data | **STIRR, ROCK, CACTUS**, k-Modes |

### Other distinctions

| Distinction | Meaning |
|---|---|
| **Hard vs soft (fuzzy)** | Each point in exactly one cluster, versus a membership degree in each |
| **Exclusive vs overlapping** | Whether a point may belong to several |
| **Complete vs partial** | Whether every point must be assigned — DBSCAN leaves **noise** unassigned |

## 5.2 K-Means

### 🎯 The algorithm

```
1. Choose k. Initialise k centroids (randomly, or with k-means++).
2. ASSIGN:  put each point in the cluster of its nearest centroid.
3. UPDATE:  recompute each centroid as the MEAN of its assigned points.
4. Repeat 2–3 until no assignment changes (or a max iteration count).
```

It minimises the **within-cluster sum of squares** (WCSS), also called
inertia or SSE:

```
WCSS = Σⱼ Σ(x in Cⱼ) ‖x − μⱼ‖²
```

**Why the *mean*?** Because the mean is precisely the point minimising the sum
of squared distances to a set of points — so the update step is the optimal
move given the current assignment. That is also why K-Means is tied to squared
Euclidean distance and does not straightforwardly generalise to other metrics.

### 🔢 A full worked trace

Eight one-dimensional points: **2, 4, 10, 12, 3, 20, 30, 11**, with **k = 2**
and initial centroids **c₁ = 2, c₂ = 4**.

**Iteration 1 — assign**

| Point | \|x − 2\| | \|x − 4\| | Cluster |
|---:|---:|---:|:---:|
| 2 | 0 | 2 | C1 |
| 4 | 2 | 0 | C2 |
| 10 | 8 | 6 | C2 |
| 12 | 10 | 8 | C2 |
| 3 | 1 | 1 | C1 (tie → lower index) |
| 20 | 18 | 16 | C2 |
| 30 | 28 | 26 | C2 |
| 11 | 9 | 7 | C2 |

```
C1 = {2, 3}                      → new c₁ = 5/2       = 2.5
C2 = {4, 10, 12, 20, 30, 11}     → new c₂ = 87/6      = 14.5
```

**Iteration 2 — assign with c₁ = 2.5, c₂ = 14.5**

| Point | \|x − 2.5\| | \|x − 14.5\| | Cluster |
|---:|---:|---:|:---:|
| 2 | 0.5 | 12.5 | C1 |
| 4 | 1.5 | 10.5 | C1 |
| 10 | 7.5 | 4.5 | C2 |
| 12 | 9.5 | 2.5 | C2 |
| 3 | 0.5 | 11.5 | C1 |
| 20 | 17.5 | 5.5 | C2 |
| 30 | 27.5 | 15.5 | C2 |
| 11 | 8.5 | 3.5 | C2 |

```
C1 = {2, 4, 3}              → new c₁ = 9/3   = 3.0
C2 = {10, 12, 20, 30, 11}   → new c₂ = 83/5  = 16.6
```

**Iteration 3 — assign with c₁ = 3.0, c₂ = 16.6**

| Point | \|x − 3\| | \|x − 16.6\| | Cluster |
|---:|---:|---:|:---:|
| 2 | 1 | 14.6 | C1 |
| 4 | 1 | 12.6 | C1 |
| 10 | 7 | 6.6 | C2 |
| 12 | 9 | 4.6 | C2 |
| 3 | 0 | 13.6 | C1 |
| 20 | 17 | 3.4 | C2 |
| 30 | 27 | 13.4 | C2 |
| 11 | 8 | 5.6 | C2 |

**Assignments are unchanged from iteration 2. The algorithm has converged.**

```
Final: C1 = {2, 3, 4} with centroid 3.0
       C2 = {10, 11, 12, 20, 30} with centroid 16.6

WCSS = [(2−3)² + (3−3)² + (4−3)²]
     + [(10−16.6)² + (11−16.6)² + (12−16.6)² + (20−16.6)² + (30−16.6)²]
     = [1 + 0 + 1] + [43.56 + 31.36 + 21.16 + 11.56 + 179.56]
     = 2 + 287.2
     = 289.2
```

Notice that **30 is dragging c₂ upward** — it contributes 179.56 of the 287.2,
which is 62.5% of the total error from one of eight points. That is the outlier
sensitivity of §5.3 in action.

### 🔢 Choosing k

**The elbow method.** Plot WCSS against k. WCSS always falls as k rises (at
k = n it is zero), so you look for the **elbow** — the point after which the
improvement flattens.

```
WCSS
   │╲
   │ ╲
   │  ╲
   │   ●───  ← elbow at k = 3
   │       ╲___
   │           ╲______
   └────────────────────► k
   1  2  3  4  5  6  7
```

**The silhouette method** is more objective: compute the mean silhouette for
each k and take the maximum. The **gap statistic** compares WCSS against what
a uniform random dataset would give.

**No method is definitive.** The elbow is often ambiguous, and the honest
answer includes domain knowledge: if marketing can run four campaigns, k = 4.

### ⚠️ K-Means's five weaknesses

Each is examined, and each has a standard remedy.

**1. k must be chosen in advance.** → Elbow, silhouette, or domain knowledge.

**2. Sensitive to initialisation.** Different random starts give different
final clusterings, because K-Means only finds a **local** optimum of WCSS.
→ **k-means++** seeds centroids far apart probabilistically; or run it 10 times
and keep the lowest WCSS (scikit-learn's `n_init` does exactly this).

**3. Sensitive to outliers.** The mean is not robust — one extreme point pulls
its centroid far from the cluster's body, as the 30 does above.
→ **K-Medoids**, or remove outliers first.

**4. Assumes spherical, equally sized clusters.** K-Means partitions the space
into a Voronoi diagram, so every boundary is a straight line (a hyperplane).
It **cannot** find two concentric rings, two crescents, or one small dense
cluster beside one large diffuse one.
→ **DBSCAN** for arbitrary shapes; spectral clustering; Gaussian mixtures for
unequal covariances.

**5. Needs numeric data and scaled features.** The mean is undefined for
categories, and unscaled features let the largest-range attribute dominate.
→ **k-Modes** for categorical; normalise first.

**Complexity:** O(n · k · d · i) for n points, k clusters, d dimensions, i
iterations — **linear in n**, which is why it scales to enormous datasets and
remains the most used clustering algorithm in the world despite all five
weaknesses.

## 5.3 K-Medoids

### 🎯 The idea

Use an **actual data point** as each cluster's centre — a **medoid** — instead
of a computed mean.

| | K-Means | K-Medoids |
|---|---|---|
| Centre | The **mean** — usually not a real point | An **actual data point** |
| Minimises | Sum of squared distances | Sum of **absolute** distances |
| Outliers | **Sensitive** | **Robust** |
| Distance measure | Effectively Euclidean | **Any** — including Manhattan, cosine, Gower |
| Complexity per iteration | O(nkd) | **O(k(n−k)²)** |
| Scales to large n | **Yes** | Poorly — CLARA samples to cope |
| Interpretable centre | No | **Yes** — a real, exhibitable record |

**PAM** — Partitioning Around Medoids — is the standard algorithm:

```
1. Select k initial medoids.
2. Assign every point to its nearest medoid.
3. For each medoid m and each non-medoid o:
       compute the change in total cost if m were swapped for o
4. Perform the swap with the largest cost reduction.
5. Repeat 3–4 until no swap improves the cost.
```

### 🔢 Why the medoid is robust

Take the points **1, 2, 3, 4, 100**.

```
Mean   = 110/5 = 22    ← lies in an empty region; no data anywhere near it
Median = 3             ← the medoid, a real point, in the middle of the mass
```

The mean of 22 is not close to any point in the data. This is exactly what
happens to a K-Means centroid when a cluster contains an outlier — and it is
why the medoid version resists it.

**The trade-off is cost.** Each PAM iteration evaluates k(n−k) possible swaps,
each requiring a cost recomputation — **quadratic in n**, against K-Means's
linear. **CLARA** applies PAM to samples, and **CLARANS** searches the swap
space randomly, both to recover scalability.

## 5.4 Hierarchical clustering

### 🎯 The idea

Build a **tree of nested clusters** — a **dendrogram** — instead of a flat
partition. **You do not have to choose k in advance**: cut the tree at any
height to get any number of clusters.

| Approach | Direction | Starts with | Also called |
|---|---|---|---|
| **Agglomerative** | Bottom-up | n singleton clusters | **AGNES** |
| **Divisive** | Top-down | one cluster of everything | **DIANA** |

Agglomerative is far more common: divisive must choose, at every step, how to
split a cluster — a search over 2^(n−1) − 1 possibilities.

```
Agglomerative:
    each point is its own cluster
    repeat until one cluster remains:
        find the two CLOSEST clusters
        merge them
        record the merge height
```

### 🔢 Linkage criteria — "closest" means what?

| Linkage | Distance between clusters | Produces |
|---|---|---|
| **Single** (MIN) | Closest pair of points | Long, straggly chains; finds non-elliptical shapes; **sensitive to noise** |
| **Complete** (MAX) | Farthest pair of points | Compact, roughly equal-diameter clusters; breaks large ones |
| **Average** | Mean of all pairwise distances | A compromise; the usual default |
| **Centroid** | Distance between centroids | Can produce **inversions** in the dendrogram |
| **Ward's** | Increase in total WCSS from merging | Compact, similar-sized clusters; the most used in practice |

**Single linkage's chaining effect** is its defining property, good and bad: it
can follow a curved band of points that no other linkage would find, and it
will also merge two well-separated clusters if a single stray point bridges
them.

### 🔢 A worked dendrogram

Five points with this distance matrix:

|  | A | B | C | D | E |
|---|:-:|:-:|:-:|:-:|:-:|
| **A** | 0 | 2 | 6 | 10 | 9 |
| **B** | 2 | 0 | 5 | 9 | 8 |
| **C** | 6 | 5 | 0 | 4 | 5 |
| **D** | 10 | 9 | 4 | 0 | 3 |
| **E** | 9 | 8 | 5 | 3 | 0 |

**Single linkage** — merge the closest pair each time.

*Step 1:* the smallest entry is **d(A,B) = 2**. Merge → **{A,B}** at height 2.

New distances, taking the **minimum** to each remaining point:

```
d({A,B}, C) = min(6, 5) = 5
d({A,B}, D) = min(10, 9) = 9
d({A,B}, E) = min(9, 8) = 8
```

|  | {A,B} | C | D | E |
|---|:-:|:-:|:-:|:-:|
| **{A,B}** | 0 | 5 | 9 | 8 |
| **C** | 5 | 0 | 4 | 5 |
| **D** | 9 | 4 | 0 | 3 |
| **E** | 8 | 5 | 3 | 0 |

*Step 2:* smallest is **d(D,E) = 3**. Merge → **{D,E}** at height 3.

```
d({A,B}, {D,E}) = min(9, 8) = 8
d(C, {D,E})     = min(4, 5) = 4
```

*Step 3:* smallest is **d(C, {D,E}) = 4**. Merge → **{C,D,E}** at height 4.

```
d({A,B}, {C,D,E}) = min(5, 8) = 5
```

*Step 4:* merge everything at height **5**.

```
height
  5 ┤        ┌────────────────────┐
  4 ┤        │           ┌────────┐│
  3 ┤        │           │   ┌───┐││
  2 ┤   ┌───┐│           │   │   │││
  0 ┴───A   B───────────C────D   E
```

**Cutting the dendrogram** at height 4.5 crosses two lines, giving
**{A,B}** and **{C,D,E}** — two clusters. Cutting at 3.5 gives three:
{A,B}, {C}, {D,E}.

**Complete linkage** on the same data would take the **maximum** at each merge:
d({A,B},C) = max(6,5) = 6, and so on. The merge *order* happens to be the same
here, but the merge *heights* are larger — a general property, since complete
linkage always reports the farthest pair.

### ⚠️ Hierarchical clustering's limitations

| | |
|---|---|
| **Complexity** | O(n³) time, O(n²) memory in the naive form — **impractical beyond a few thousand points** |
| **No undo** | A merge is never reconsidered; a bad early merge is permanent |
| **Sensitive to noise** | Especially single linkage |
| **Interpretation** | Where to cut the dendrogram is a judgement call |

The O(n²) memory is the hard limit in practice: 100,000 points needs a
distance matrix of 10¹⁰ entries. **That is exactly what BIRCH was built to
solve.**

## 5.5 DBSCAN

**Density-Based Spatial Clustering of Applications with Noise** (Ester et al.,
1996) — and, contrary to the syllabus's grouping, it is **not hierarchical**.

### 🎯 The idea

**A cluster is a dense region.** Points in dense neighbourhoods belong
together; points in sparse regions are **noise**. No k, and clusters may be any
shape.

### 🔢 The two parameters and three point types

| Parameter | Meaning |
|---|---|
| **ε (eps)** | Radius of a point's neighbourhood |
| **MinPts** | Minimum points within ε for a point to be **core** |

| Point type | Definition |
|---|---|
| **Core point** | Has **≥ MinPts** points within ε (**including itself**) |
| **Border point** | Fewer than MinPts within ε, **but** is within ε of a core point |
| **Noise point** | Neither — belongs to no cluster |

```
         ●   ← noise: sparse neighbourhood, not near any core

    ○ ○ ○ ○
  ○ ● ● ● ● ○      ● = core point
  ○ ● ● ● ● ○      ○ = border point (in a core point's neighbourhood,
    ○ ○ ○ ○              but not dense enough itself)
```

### Reachability

| Relation | Definition |
|---|---|
| **Directly density-reachable** | q is within ε of p, **and p is a core point** |
| **Density-reachable** | A chain p → p₁ → … → q of direct reachabilities |
| **Density-connected** | Some core point o reaches both p and q |

A **cluster** is a maximal set of density-connected points. Note that
density-reachability is **not symmetric** — a border point does not reach a
core point — which is why the definition uses density-*connectedness*.

### The algorithm

```
for each unvisited point p:
    mark p visited
    N = points within eps of p
    if |N| < MinPts:  mark p NOISE          (may later become a border point)
    else:
        start a new cluster C; add p
        for each q in N (N grows as we go):
            if q unvisited:
                mark visited; N' = neighbours of q
                if |N'| >= MinPts: N = N ∪ N'      ← expand through core points
            if q is not yet in any cluster: add q to C
```

### 🔢 A worked example

Points on a line: **1, 2, 3, 8, 9, 10, 25**, with **ε = 2** and
**MinPts = 3**.

| Point | Neighbours within ε = 2 (inclusive) | Count | Type |
|---:|---|:---:|---|
| 1 | 1, 2, 3 | 3 | **Core** |
| 2 | 1, 2, 3 | 3 | **Core** |
| 3 | 1, 2, 3 | 3 | **Core** |
| 8 | 8, 9, 10 | 3 | **Core** |
| 9 | 8, 9, 10 | 3 | **Core** |
| 10 | 8, 9, 10 | 3 | **Core** |
| 25 | 25 | 1 | **Noise** |

```
Cluster 1 = {1, 2, 3}       (all mutually density-connected)
Cluster 2 = {8, 9, 10}
Noise     = {25}
```

**K-Means with k = 2 would be forced to put 25 somewhere**, dragging a centroid
far from every real point. DBSCAN identifies it as noise and leaves it out —
which is often the single most useful thing about the algorithm.

Change MinPts to 4 and *every* point becomes noise, since no neighbourhood
holds four points. **The parameters are that sensitive**, which is DBSCAN's
main practical difficulty.

### 🔢 DBSCAN versus K-Means

| | **K-Means** | **DBSCAN** |
|---|---|---|
| Needs k? | **Yes** | **No** |
| Parameters | k | ε, MinPts |
| Cluster shape | **Spherical only** | **Arbitrary** |
| Outliers | Forced into a cluster | **Identified as noise** |
| Cluster sizes | Prefers similar sizes | Any |
| Varying density | Handles it | **Fails** — one ε cannot suit all |
| Complexity | O(nkdi) | O(n log n) with an index, O(n²) without |
| Deterministic | **No** — depends on initialisation | Almost — only border-point assignment varies |
| High dimensions | Degrades | **Degrades worse** |

**DBSCAN's failure case is varying density**, and it is the exam answer: a
single ε that is right for a dense cluster is too small for a sparse one, so
the sparse cluster fragments into noise. **OPTICS** solves this by producing an
ordering across a range of ε rather than one clustering.

**Choosing the parameters:** MinPts ≥ d + 1, commonly 2d; then plot the sorted
distance from each point to its MinPts-th nearest neighbour (the **k-distance
graph**) and take ε at the knee.

## 5.6 BIRCH

**Balanced Iterative Reducing and Clustering using Hierarchies** (Zhang et al.,
1996).

### 🎯 The idea

Hierarchical clustering is O(n²) in memory, so it cannot touch large data.
**BIRCH compresses the data into a summary tree in ONE pass**, then clusters
the summary.

Its defining claim: it can cluster a dataset **larger than main memory**, with
a **single scan**.

### 🔢 The Clustering Feature

Every sub-cluster is summarised by a triple:

```
CF = (N, LS, SS)

  N  = number of points
  LS = LINEAR SUM of the points     (a vector)   Σ xᵢ
  SS = SQUARE SUM of the points     (a scalar)   Σ ‖xᵢ‖²
```

From those three numbers alone you can compute the centroid, radius and
diameter — **without keeping any of the points**:

```
centroid = LS / N
radius   = √( SS/N − ‖LS/N‖² )
```

**That formula is the whole trick**, and it is the same identity as the
computational formula for variance in Course 4:
`Var = E[X²] − (E[X])²`.

### 🔢 CF additivity

```
CF₁ + CF₂ = (N₁ + N₂,  LS₁ + LS₂,  SS₁ + SS₂)
```

Merging two sub-clusters is **three additions**. This is what makes BIRCH
incremental and single-pass: a new point is a CF of (1, x, ‖x‖²), and absorbing
it into a leaf is just addition.

**Worked example.** Points 2, 4, 6 in one dimension:

```
N  = 3
LS = 2 + 4 + 6           = 12
SS = 4 + 16 + 36         = 56

centroid = 12/3          = 4
radius   = √(56/3 − 4²)  = √(18.667 − 16) = √2.667 = 1.633
```

Add the point 8 — no need to revisit 2, 4, 6:

```
N = 4, LS = 20, SS = 120
centroid = 5
radius   = √(120/4 − 25) = √5 = 2.236
```

### The CF-tree

A height-balanced tree, like a B+-tree, with two parameters:

| Parameter | Meaning |
|---|---|
| **Branching factor B** | Maximum children per internal node |
| **Threshold T** | Maximum radius (or diameter) of a leaf entry |

```
                 [ root CF ]
                 /         \
        [ CF ]              [ CF ]           ← internal: CFs of their subtrees
        /    \              /    \
   [CF][CF] [CF][CF]  [CF][CF] [CF][CF]      ← leaves: CFs of sub-clusters
```

**Inserting a point:** descend to the closest leaf; if absorbing it keeps that
entry's radius ≤ T, absorb it (three additions); otherwise create a new entry,
splitting nodes upward if they exceed B.

**If memory runs out**, BIRCH **increases T** and rebuilds a smaller tree from
the existing leaf CFs — no rescan of the data required. That is the mechanism
behind the single-pass claim.

### The four phases

| Phase | What it does |
|---|---|
| **1** | Scan the data once, build the CF-tree |
| **2** *(optional)* | Condense — rebuild into a smaller tree |
| **3** | Apply a **global clustering algorithm** (usually agglomerative or K-Means) to the **leaf CFs**, not the data |
| **4** *(optional)* | Refine — one more pass reassigning points to the resulting centroids |

Phase 3 is where the syllabus's "hierarchical" label comes from — but it is
hierarchical clustering applied to a *compressed summary*, not to the data.

### ⚠️ BIRCH's limitations

- **Numeric data only** — LS and SS require arithmetic on the values.
- **Order-dependent** — a different insertion order gives a different tree.
- **Spherical bias** — the radius/diameter threshold assumes roughly round
  sub-clusters, so it shares K-Means's shape limitation.
- **T is hard to choose** — too small and the tree exhausts memory; too large
  and distinct clusters are merged into one leaf.

| | BIRCH | Standard hierarchical |
|---|---|---|
| Scans | **1** | Needs the full distance matrix |
| Memory | **Bounded** — a tree, not the data | O(n²) |
| Complexity | **O(n)** | O(n³) |
| Data larger than RAM | **Yes** | No |
| Shapes | Spherical | Any (with the right linkage) |

## 5.7 Categorical clustering

### ⚠️ Why numeric algorithms fail on categories

K-Means needs a **mean**. What is the mean of {red, green, blue}? There is
none. And Unit 2 §2.9's warning applies with full force: encoding
`red=1, green=2, blue=3` makes green the average of red and blue, which is
nonsense that K-Means will act on.

Euclidean distance is equally meaningless. Categorical data needs measures
built on **co-occurrence** and **overlap** rather than magnitude — which is
what the three algorithms below provide.

**k-Modes** is the simplest fix: replace the mean with the **mode** and
Euclidean distance with a **simple matching** count of mismatched attributes.
The syllabus does not name it, but it is the natural first answer and worth
mentioning.

### 🔢 STIRR

**Sieving Through Iterated Relational Reinforcement** (Gibson, Kleinberg,
Raghavan, 1998).

**The idea:** represent the data as a graph whose nodes are **attribute
values**, then propagate weights between values that co-occur, until the
weights stabilise. Values that reinforce each other end up sharing a sign or
magnitude, and those groups are the clusters.

```
Each distinct attribute VALUE is a node with a weight.
A tuple is a hyperedge joining the values it contains.

repeat until the weights converge:
    for each node v:
        new weight(v) = Σ over tuples containing v of
                        (combining function of the OTHER nodes' weights)
    normalise the weight vector
```

The system is a set of weight vectors called **basins**. The **principal
basin** carries the dominant structure; **non-principal basins**, especially
their positive and negative components, separate the data into groups.

**Its character:** STIRR is a *spectral* method — it is effectively finding
eigenvectors of a co-occurrence operator — and its output is **not a hard
partition**. A human must interpret the weight groupings. That is both its
distinctive feature and its practical drawback.

### 🔢 ROCK

**RObust Clustering using linKs** (Guha, Rastogi, Shim, 1999). The most
examinable of the three because its central idea is concrete.

**The idea:** do not cluster on similarity between *pairs*. Cluster on the
number of **common neighbours**, which ROCK calls **links**.

```
neighbours: p and q are neighbours if sim(p, q) ≥ θ
            (θ is a user threshold; sim is usually Jaccard)

link(p, q) = the NUMBER OF COMMON NEIGHBOURS of p and q
```

**Why links beat pairwise similarity** — this is the exam answer. Two market
baskets `{bread, butter}` and `{bread, jam}` share only one item, so their
Jaccard similarity is low (1/3). But if many *other* baskets are neighbours of
both, they clearly belong together. **Links capture that global evidence;
pairwise similarity cannot see it.**

The algorithm is agglomerative, maximising a **goodness measure**:

```
                    link(Cᵢ, Cⱼ)
g(Cᵢ, Cⱼ) = ─────────────────────────────────────────────
            (nᵢ+nⱼ)^(1+2f(θ)) − nᵢ^(1+2f(θ)) − nⱼ^(1+2f(θ))
```

with `f(θ) = (1 − θ)/(1 + θ)` for market-basket data. The denominator is the
*expected* number of links if the clusters merged by chance, so the ratio
measures how much the observed linkage exceeds chance — normalising away the
bias toward merging large clusters.

**Worked example.** With θ = 0.5 and Jaccard similarity, are `{a, b, c}` and
`{a, b, d}` neighbours?

```
Jaccard = |intersection| / |union| = |{a,b}| / |{a,b,c,d}| = 2/4 = 0.5 ≥ 0.5  ✓
```

Yes — just. And `{a,b,c}` versus `{a,d,e}`: Jaccard = 1/5 = 0.2 < 0.5, not
neighbours. If both are nonetheless neighbours of many common baskets, ROCK
may still merge them; single-link on Jaccard would not.

### 🔢 CACTUS

**Clustering Categorical Data Using Summaries** (Ganti, Gehrke, Ramakrishnan,
1999).

**The idea:** summarise the data so it fits in memory, then find clusters
inside the summaries. Like BIRCH, it is a summarisation strategy — but for
categorical data.

**Strong connections.** Two attribute values from *different* attributes are
**strongly connected** if they co-occur **significantly more often than
expected under independence**:

```
support(aᵢ, bⱼ)  >  α × expected support under independence

expected = (|aᵢ| / |A|) × (|bⱼ| / |B|) × N
```

That comparison against an independence baseline is exactly the **lift** idea
from Unit 3 §3.2, applied to attribute values instead of items.

**The three phases:**

| Phase | What happens |
|---|---|
| **1. Summarisation** | One data scan builds **inter-attribute summaries** (co-occurrence counts between values of different attributes) and **intra-attribute summaries** (similarity between values of the same attribute) |
| **2. Clustering** | Find **cluster projections** on each attribute from the summaries, then combine them into candidate clusters |
| **3. Validation** | One more scan to confirm each candidate meets the support threshold |

**Its strengths:** typically **two data scans**, works on summaries that fit in
memory, and it can find clusters in **subspaces** — clusters defined by only
some of the attributes, which matters in high dimensions.

**Its weakness:** the candidate-generation step can produce spurious clusters
that phase 3 must discard, and the α threshold is another parameter to guess.

### 🔢 The three compared

| | **STIRR** | **ROCK** | **CACTUS** |
|---|---|---|---|
| Approach | **Spectral** — iterated weight propagation | **Agglomerative** on links | **Summary**-based |
| Key concept | Weight basins on a co-occurrence graph | **Links** = common neighbours | **Strong connections** between values |
| Data scans | Several (until convergence) | Needs the link matrix | **Two** |
| Output | Weight groupings — **needs interpretation** | A hard hierarchical clustering | Hard clusters, possibly in subspaces |
| Number of clusters | Emerges | **Specified** | Emerges from the thresholds |
| Scalability | Moderate | **Poor** — O(n²) links, O(n² log n) time | **Good** |
| Subspace clusters | No | No | **Yes** |
| Main strength | No distance measure needed at all | Robust to sparse, high-dimensional baskets | Fast, memory-bounded |
| Main weakness | Output is not a partition | Does not scale; θ must be chosen | Spurious candidates; α must be chosen |

---

## Practice problems

### Problem 1

Apply K-Means with k = 2 to the two-dimensional points
A(2,10), B(2,5), C(8,4), D(5,8), E(7,5), F(6,4), G(1,2), H(4,9),
with initial centroids **A(2,10)** and **C(8,4)**. Use Euclidean distance.
Show two iterations and the final WCSS.

**Solution.**

**Iteration 1** — distances to c₁ = (2,10) and c₂ = (8,4):

| Point | to c₁(2,10) | to c₂(8,4) | Cluster |
|---|---:|---:|:---:|
| A(2,10) | 0 | **8.485** | C1 |
| B(2,5) | 5.000 | 6.083 | C1 |
| C(8,4) | 8.485 | 0 | C2 |
| D(5,8) | 3.606 | 5.000 | C1 |
| E(7,5) | 7.071 | 1.414 | C2 |
| F(6,4) | 7.211 | 2.000 | C2 |
| G(1,2) | 8.062 | 7.280 | C2 |
| H(4,9) | 2.236 | 6.403 | C1 |

```
C1 = {A, B, D, H}   centroid = ((2+2+5+4)/4, (10+5+8+9)/4) = (13/4, 32/4) = (3.25, 8.0)
C2 = {C, E, F, G}   centroid = ((8+7+6+1)/4, (4+5+4+2)/4)  = (22/4, 15/4) = (5.5, 3.75)
```

**Iteration 2** — distances to c₁ = (3.25, 8.0) and c₂ = (5.5, 3.75):

| Point | to c₁ | to c₂ | Cluster |
|---|---:|---:|:---:|
| A(2,10) | 2.358 | 7.163 | C1 |
| B(2,5) | 3.250 | 3.717 | C1 |
| C(8,4) | 6.210 | 2.512 | C2 |
| D(5,8) | 1.750 | 4.279 | C1 |
| E(7,5) | 4.802 | 1.953 | C2 |
| F(6,4) | 4.854 | 0.559 | C2 |
| G(1,2) | 6.408 | 4.828 | C2 |
| H(4,9) | 1.250 | 5.460 | C1 |

**Assignments unchanged — converged.**

```
Final centroids: c₁ = (3.25, 8.0), c₂ = (5.5, 3.75)

WCSS = [2.358² + 3.250² + 1.750² + 1.250²] + [2.512² + 1.953² + 0.559² + 4.828²]
     = [5.5625 + 10.5625 + 3.0625 + 1.5625] + [6.3125 + 3.8125 + 0.3125 + 23.3125]
     = 20.75 + 33.75
     = 54.50
```

**Note G(1,2).** It is 4.83 from its own centroid and contributes 23.31 —
**42.8% of the total WCSS** — while sitting far from both clusters. DBSCAN
would likely call it noise; K-Means has no such option.

### Problem 2

Perform single-linkage agglomerative clustering on:

|  | P1 | P2 | P3 | P4 | P5 |
|---|:-:|:-:|:-:|:-:|:-:|
| **P1** | 0 | 9 | 3 | 6 | 11 |
| **P2** | 9 | 0 | 7 | 5 | 10 |
| **P3** | 3 | 7 | 0 | 9 | 2 |
| **P4** | 6 | 5 | 9 | 0 | 8 |
| **P5** | 11 | 10 | 2 | 8 | 0 |

Draw the dendrogram and give the clusters at a cut of height 5.

**Solution.**

*Step 1:* smallest distance is **d(P3,P5) = 2**. Merge → **{P3,P5}** at
height 2.

```
d({P3,P5}, P1) = min(3, 11) = 3
d({P3,P5}, P2) = min(7, 10) = 7
d({P3,P5}, P4) = min(9,  8) = 8
```

|  | {P3,P5} | P1 | P2 | P4 |
|---|:-:|:-:|:-:|:-:|
| **{P3,P5}** | 0 | 3 | 7 | 8 |
| **P1** | 3 | 0 | 9 | 6 |
| **P2** | 7 | 9 | 0 | 5 |
| **P4** | 8 | 6 | 5 | 0 |

*Step 2:* smallest is **d({P3,P5}, P1) = 3**. Merge → **{P1,P3,P5}** at
height 3.

```
d({P1,P3,P5}, P2) = min(7, 9) = 7
d({P1,P3,P5}, P4) = min(8, 6) = 6
```

|  | {P1,P3,P5} | P2 | P4 |
|---|:-:|:-:|:-:|
| **{P1,P3,P5}** | 0 | 7 | 6 |
| **P2** | 7 | 0 | 5 |
| **P4** | 6 | 5 | 0 |

*Step 3:* smallest is **d(P2,P4) = 5**. Merge → **{P2,P4}** at height 5.

```
d({P1,P3,P5}, {P2,P4}) = min(7, 6) = 6
```

*Step 4:* merge all at height **6**.

```
height
  6 ┤   ┌────────────────────────┐
  5 ┤   │                    ┌───┐
  3 ┤ ┌─┴──┐                 │   │
  2 ┤ │ ┌─┐│                 │   │
  0 ┴─P1 P3 P5───────────────P2  P4
```

**Cut at height 5.** A cut at exactly 5 is ambiguous, so take just above 5 —
the lines crossed are the {P1,P3,P5} branch and the {P2,P4} branch:

**Two clusters: {P1, P3, P5} and {P2, P4}.**

Cut just below 5 instead and you get three: {P1,P3,P5}, {P2}, {P4}. **State
which side of the tie you are taking** — examiners accept either with the
reasoning shown.

### Problem 3

Apply DBSCAN with **ε = 2** and **MinPts = 3** to the two-dimensional points
A(1,1), B(1,2), C(2,1), D(2,2), E(8,8), F(8,9), G(9,8), H(15,15).

Classify each point and give the clusters.

**Solution.**

Euclidean distances within the first group: A–B = 1, A–C = 1, A–D = √2 ≈ 1.414,
B–C = √2, B–D = 1, C–D = 1. All ≤ 2, so **A, B, C, D are all within ε of each
other**.

| Point | Neighbours within ε = 2 (inclusive) | Count | Type |
|---|---|:---:|---|
| A(1,1) | A, B, C, D | 4 | **Core** |
| B(1,2) | A, B, C, D | 4 | **Core** |
| C(2,1) | A, B, C, D | 4 | **Core** |
| D(2,2) | A, B, C, D | 4 | **Core** |
| E(8,8) | E, F, G | 3 | **Core** |
| F(8,9) | E, F, G | 3 | **Core** |
| G(9,8) | E, F, G | 3 | **Core** |
| H(15,15) | H | 1 | **Noise** |

For E: d(E,F) = 1, d(E,G) = 1, so with itself the count is 3 ≥ MinPts. For F:
d(F,G) = √((8−9)² + (9−8)²) = √2 ≈ 1.414 ≤ 2, so F's neighbours are E, F, G —
count 3. Same for G.

H's nearest point is G, at √((15−9)² + (15−8)²) = √85 ≈ 9.22, far beyond ε.

```
Cluster 1 = {A, B, C, D}
Cluster 2 = {E, F, G}
Noise     = {H}
```

**There are no border points in this example** — every clustered point is core.
That is what a clean, well-separated dataset looks like to DBSCAN.

**Compare with K-Means, k = 2.** K-Means must assign H somewhere. Its nearest
cluster is {E,F,G}, whose centroid would move from (8.33, 8.33) to
(10, 10) — pulled two units away from all three of its actual members by one
outlier. **DBSCAN's ability to say "this point belongs to nothing" is the
practical difference between the two algorithms.**

---

## Exam questions from this unit

**Two marks**

1. Define clustering, and distinguish it from classification.
2. What is the silhouette coefficient, and what does a negative value mean?
3. Why does K-Means use the mean as the centre?
4. Why is K-Medoids more robust than K-Means?
5. Distinguish agglomerative from divisive clustering.
6. Distinguish single from complete linkage.
7. What is the chaining effect?
8. Define core, border and noise points.
9. What is a Clustering Feature in BIRCH?
10. What is a "link" in ROCK?
11. Why can K-Means not cluster categorical data?
12. Name one failure case each for K-Means and DBSCAN.

**Five marks**

1. Explain the clustering paradigms with an algorithm for each.
2. Explain K-Means with a worked example, and its weaknesses.
3. Explain how to choose k.
4. Explain K-Medoids and PAM, comparing with K-Means.
5. Explain agglomerative hierarchical clustering and the linkage criteria.
6. Explain DBSCAN with a worked example.
7. Explain BIRCH and the CF-tree.
8. Explain ROCK and why links beat pairwise similarity.
9. Explain STIRR and CACTUS.

**Ten marks**

1. Apply K-Means to a given dataset, showing every iteration and the final
   WCSS.
2. Perform agglomerative clustering on a given distance matrix, draw the
   dendrogram, and give the clusters at a stated cut.
3. Compare K-Means, hierarchical, DBSCAN and BIRCH on principle, parameters,
   complexity, cluster shape, outlier handling and scalability.
4. Explain categorical clustering and compare STIRR, ROCK and CACTUS.

## Mistakes that cost marks

- Calling clustering supervised
- Forgetting that K-Means finds only a **local** optimum
- Claiming K-Means can find non-spherical clusters
- Using K-Means on categorical data, or integer-encoding categories first
- Forgetting to normalise before any distance-based clustering
- Saying WCSS falling with k proves a better clustering — it always falls
- Confusing silhouette (higher is better) with Davies–Bouldin (lower is better)
- Excluding the point itself from its own ε-neighbourhood count in DBSCAN
- Claiming DBSCAN needs k — it does not
- Saying DBSCAN handles clusters of varying density — it does not
- Calling DBSCAN hierarchical
- Saying BIRCH stores the data points — it stores CF triples
- Confusing single linkage (minimum) with complete linkage (maximum)
- Saying ROCK uses pairwise similarity — it uses common neighbours
