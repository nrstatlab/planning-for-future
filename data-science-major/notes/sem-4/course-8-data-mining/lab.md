# Course 8 — Practical Lab

**15 experiments**
Recommended datasets: `weather.arff`, `iris.arff`, `supermarket.arff`,
`vote.arff`, `contact-lenses.arff`, or custom CSV.

Code lives in `labs/course-8-datamining/`.

> **On the tooling.** The syllabus prescribes **WEKA**, which cannot be
> installed in the verification environment — it needs a host the egress policy
> blocks. So each experiment has two halves:
>
> - **The WEKA click-path**, written out step by step (tab, filter, parameters,
>   what to read off the output). Marked **NOT EXECUTED** — it is documentation
>   for your lab exam, not something that ran here.
> - **A scikit-learn / mlxtend equivalent that does run**, executed and asserted
>   by `tools/run_data_labs.py`, with results
>   checked against the hand-computed values in Units 3–5.
>
> Learn the WEKA path — that is what the examiner will ask you to demonstrate.
> Read the Python to understand what WEKA is doing underneath.

```bash
pip install -r tools/requirements.txt
python3 tools/run_data_labs.py
```

## WEKA in five minutes

The **Explorer** is the interface you will be examined on.

| Tab | Purpose |
|---|---|
| **Preprocess** | Load data, apply filters, view attribute statistics |
| **Classify** | Build and evaluate classifiers |
| **Cluster** | Build and evaluate clusterers |
| **Associate** | Association rule mining |
| **Select attributes** | Feature selection |
| **Visualize** | Scatter-plot matrix |

**Filters** are the heart of the Preprocess tab, and they divide two ways:

```
weka.filters
├── supervised          ← uses the class attribute
│   ├── attribute/      (Discretize, AttributeSelection)
│   └── instance/       (Resample, SMOTE)
└── unsupervised        ← ignores the class
    ├── attribute/      (Normalize, Standardize, Discretize,
    │                    ReplaceMissingValues, Remove, PrincipalComponents,
    │                    NumericToNominal, StringToWordVector)
    └── instance/       (RemoveWithValues, Randomize)
```

**Choosing supervised versus unsupervised Discretize is itself an exam
question:** the supervised version uses the class label to place cut points
where they best separate classes (Fayyad–Irani MDL), and generally produces
better bins for a subsequent classifier.

### The ARFF format

```
@relation weather

@attribute outlook     {sunny, overcast, rainy}
@attribute temperature numeric
@attribute humidity    numeric
@attribute windy       {TRUE, FALSE}
@attribute play        {yes, no}

@data
sunny,85,85,FALSE,no
sunny,80,90,TRUE,no
overcast,83,86,FALSE,yes
?,70,96,FALSE,yes          % '?' is a missing value
```

| Part | Meaning |
|---|---|
| `@relation` | Dataset name |
| `@attribute name {a,b}` | **Nominal** — the brace list is the domain |
| `@attribute name numeric` | Numeric |
| `@attribute name string` | Free text |
| `@attribute name date` | Date, with an optional format |
| `@data` | Rows follow, comma-separated |
| `?` | **Missing value** |
| `%` | Comment |

**The last attribute is the class by default.** Sparse ARFF, using
`{index value, index value}`, stores only non-zero entries — which is what
`supermarket.arff` uses.

---

## Experiment 1 — Load datasets and explore ARFF/CSV

**WEKA — NOT EXECUTED**

1. Explorer → **Preprocess** → *Open file* → `data/weather.nominal.arff`
2. Read off: **Instances** 14, **Attributes** 5.
3. Click each attribute. The right pane shows, for a **nominal** attribute, the
   label counts; for a **numeric** one, minimum, maximum, mean and standard
   deviation.
4. *Edit…* opens the data as a table.
5. To load CSV: *Open file* → change *Files of Type* to **CSV data files**.
6. *Save as…* with an `.arff` extension converts it.

**What to state in the viva.** WEKA infers types from a CSV — a column of
digits becomes numeric, anything else nominal. If a numeric-looking column is
really a category (a pin code, a class ID), you **must** convert it with
`NumericToNominal` or every algorithm will treat it as a magnitude. That
conversion step is the most commonly forgotten part of this experiment.

**Python equivalent — `01_load_explore.py`** — loads the same data and prints
the same summary, so you can compare WEKA's panel against the numbers.

---

## Experiment 2 — Data cleaning and missing values

**WEKA — NOT EXECUTED**

1. Load a dataset with missing values (`labor.arff`, or `weather` with `?`
   inserted).
2. **Preprocess** → *Choose* →
   `filters/unsupervised/attribute/ReplaceMissingValues` → *Apply*.
3. Read the attribute panel: the **Missing** count falls to 0.

WEKA's `ReplaceMissingValues` uses the **mean** for numeric attributes and the
**mode** for nominal ones. To drop rows instead, use
`filters/unsupervised/instance/RemoveWithValues` with
`matchMissingValues = True`.

**Python equivalent — `02_missing_values.py`** — implements mean, median, mode
and k-NN imputation on the same data and **demonstrates the variance shrinkage**
from Unit 2 §2.5 numerically: imputing 30% of a column with its mean measurably
lowers the standard deviation, and the script asserts it.

---

## Experiment 3 — Normalization and discretization

**WEKA — NOT EXECUTED**

*Normalize:* `filters/unsupervised/attribute/Normalize` → scales every numeric
attribute to [0, 1] (min–max). `Standardize` gives mean 0, variance 1
(z-score).

*Discretize:* `filters/unsupervised/attribute/Discretize`
- `bins = 3`
- `useEqualFrequency = False` → **equal-width**; `True` → **equal-frequency**
- Apply, then click the attribute: it is now nominal, with labels like
  `'(-inf-52.5]'`, `'(52.5-63)'`, `'(63-inf)'`

Supervised discretization (`filters/supervised/attribute/Discretize`) uses the
class to place the cuts and often produces **fewer, better** bins — sometimes
one bin, meaning the attribute is useless.

**Python equivalent — `03_normalize_discretize.py`** reproduces Unit 2's worked
examples exactly: min–max of 25 in that twelve-value set is **0.1477**;
equal-width bins of the ages have edges 27.67 and 47.33; and equal-frequency
bins hold three values each. All asserted.

---

## Experiment 4 — Attribute selection and PCA

**WEKA — NOT EXECUTED**

*Filter approach:* **Select attributes** tab
- *Attribute Evaluator*: `InfoGainAttributeEval`
- *Search Method*: `Ranker`
- Output ranks attributes by information gain.

*Wrapper approach:*
- *Attribute Evaluator*: `WrapperSubsetEval` (choose a classifier inside it)
- *Search Method*: `BestFirst` or `GreedyStepwise`

*PCA:* **Preprocess** →
`filters/unsupervised/attribute/PrincipalComponents`
- `varianceCovered = 0.95`
- Apply. The attributes are replaced by components named
  `0.348petallength+0.318petalwidth-0.221sepalwidth...`

**Read that attribute name carefully in the viva** — it is the eigenvector, and
it is exactly why PCA costs you interpretability.

**Python equivalent — `04_feature_selection.py`** ranks the iris attributes by
information gain, runs PCA, and checks the cumulative variance against Unit 2's
worked eigenvalue table.

---

## Experiment 5 — Summarize and visualize

**WEKA — NOT EXECUTED**

1. **Preprocess** → click each attribute for its statistics.
2. *Visualize All* → a histogram per attribute, coloured by class.
3. **Visualize** tab → the scatter-plot matrix; set *Colour* to the class.
4. Click any cell to enlarge it; *Jitter* separates overlapping points.

**Class-wise comparison:** set *Class* as the colour, then look for an
attribute whose histogram separates the colours. In iris, `petallength`
separates setosa completely — which is the visual form of "petallength has the
highest information gain".

**Python equivalent — `05_summarize.py`** prints per-class means and standard
deviations and confirms the separation numerically.

---

## Experiment 6 — Association rules with Apriori

**WEKA — NOT EXECUTED**

1. Load `supermarket.arff` (4,627 transactions, 217 items, sparse ARFF).
2. **Associate** tab → *Choose* → `Apriori`.
3. Click the name to set parameters:

| Parameter | Meaning | Typical |
|---|---|---|
| `lowerBoundMinSupport` | Minimum support | 0.1 |
| `upperBoundMinSupport` | Starting support; WEKA works **downwards** | 1.0 |
| `delta` | Step by which support is reduced | 0.05 |
| `metricType` | Confidence / Lift / Leverage / Conviction | Confidence |
| `minMetric` | Threshold for that metric | 0.9 |
| `numRules` | How many to report | 10 |
| `car` | Class association rules only | False |

**WEKA's Apriori works downwards from `upperBoundMinSupport`**, reducing by
`delta` until it has found `numRules` rules or hits the lower bound. That is
unusual and is worth knowing: setting `numRules` too low stops the search early
at a high support.

**Python equivalent — `06_apriori.py`** uses `mlxtend` and reproduces **Unit 3
§3.4's trace exactly** — the same five transactions, minsup 0.6, giving the
nine frequent itemsets and the two strong rules `{B,C}→{E}` and `{C,E}→{B}`,
each with confidence 1.00 and lift 1.25. It also runs Unit 3's Practice Problem
1 and asserts all thirteen frequent itemsets and all three strong rules.

---

## Experiment 7 — Multilevel association rules

**WEKA — NOT EXECUTED**

WEKA has **no built-in multilevel association miner**. Say so — it is the
honest answer and the examiner knows it. The standard approach is to encode the
hierarchy into the data:

1. Add ancestor attributes to each transaction: a basket containing
   `amul_milk` also gets `milk` and `dairy`.
2. Run `Apriori` on the extended data.
3. Filter out **redundant ancestor rules** afterwards (Unit 3 §3.9).

Alternatively, run Apriori separately at each level with a **different minsup
per level** — reduced support, since one threshold cannot serve both the leaf
and the root.

**Python equivalent — `07_multilevel.py`** builds a small product taxonomy,
expands each transaction with its ancestors, mines at two levels with
different thresholds, and demonstrates the redundancy test: a descendant rule
is reported only when its confidence **deviates** from what the ancestor rule
predicts.

---

## Experiment 8 — K-Means clustering

**WEKA — NOT EXECUTED**

1. Load `iris.arff`.
2. **Preprocess** → remove the class attribute
   (`filters/unsupervised/attribute/Remove`, `attributeIndices = last`).
   *Clustering is unsupervised — leaving the class in is a form of leakage.*
3. **Cluster** tab → *Choose* → `SimpleKMeans`
   - `numClusters = 3`
   - `distanceFunction = EuclideanDistance`
   - `seed = 10` (changing it changes the result — that is §5.2's weakness 2)
4. *Cluster mode* → **Classes to clusters evaluation** (re-select the class) to
   see how the clusters line up with the true species.
5. Read off: cluster centroids, **Within cluster sum of squared errors**, and
   the incorrectly clustered instance count.

**Python equivalent — `08_kmeans.py`** reproduces **Unit 5 §5.2's 1-D trace**
(final centroids 3.0 and 16.6, WCSS 289.2) and **Practice Problem 1's 2-D
trace** (centroids (3.25, 8.0) and (5.5, 3.75), WCSS 54.50), both asserted,
then runs the elbow and silhouette methods on iris.

---

## Experiment 9 — Hierarchical clustering and dendrograms

**WEKA — NOT EXECUTED**

1. **Cluster** → *Choose* → `HierarchicalClusterer`
   - `numClusters = 3`
   - `linkType` = SINGLE / COMPLETE / AVERAGE / WARD / CENTROID / MEAN /
     ADJCOMPLETE / NEIGHBOR_JOINING
   - `printNewick = True` to print the tree
2. **Right-click the result in the Result list → *Visualize tree*** for the
   dendrogram. That step is easy to miss and is the whole point of the
   experiment.

**Python equivalent — `09_hierarchical.py`** reproduces **Unit 5 §5.4's worked
dendrogram** — merges at heights 2, 3, 4, 5 under single linkage — and
**Practice Problem 2** (heights 2, 3, 5, 6, giving {P1,P3,P5} and {P2,P4} at a
cut of 5). It also shows complete linkage on the same matrix so the difference
in merge heights is visible.

---

## Experiment 10 — EM clustering

**WEKA — NOT EXECUTED**

1. **Cluster** → *Choose* → `EM`
   - `numClusters = -1` → **WEKA chooses k by cross-validation**. That
     automatic selection is EM's distinctive feature in WEKA and is worth
     stating.
   - `maxIterations = 100`
2. The output gives, per cluster and per attribute, the **mean and standard
   deviation** (numeric) or the **probability of each value** (nominal), plus
   the **log likelihood**.

**EM versus K-Means** is the exam question:

| | K-Means | EM |
|---|---|---|
| Assignment | **Hard** — one cluster each | **Soft** — a probability of each |
| Model | Centroids | A **mixture of distributions** |
| Cluster shape | Spherical, equal size | **Elliptical**, any covariance |
| Output | Labels | Labels **and** membership probabilities |
| Objective | Minimise WCSS | Maximise **log likelihood** |

K-Means is in fact a limiting case of EM with spherical equal-variance
Gaussians and hard assignment.

**Python equivalent — `10_em_clustering.py`** fits a `GaussianMixture`, prints
the responsibilities for a few boundary points to make "soft assignment"
concrete, and selects k by **BIC**.

---

## Experiment 11 — Decision tree with J48

**WEKA — NOT EXECUTED**

**J48 is WEKA's implementation of C4.5.** State that; it is a two-mark question.

1. Load `weather.nominal.arff`.
2. **Classify** → *Choose* → `trees/J48`
   - `confidenceFactor = 0.25` — **lower means more pruning**
   - `minNumObj = 2` — minimum instances per leaf
   - `unpruned = False`
   - `binarySplits = False`
3. *Test options* → **Cross-validation, Folds 10**
4. *Start*. Then **right-click the result → *Visualize tree***.

Read from the output: the tree itself, `Number of Leaves`, `Size of the tree`,
`Correctly Classified Instances`, the confusion matrix, and per-class
precision, recall, F-measure and ROC area.

`(n/m)` at a leaf means **n instances reached it and m were misclassified**.

**Python equivalent — `11_decision_tree.py`** builds a tree with
`criterion='entropy'` on the weather data and asserts that the **root split is
Outlook** with information gain **0.2467** — matching Unit 4 §4.5's hand
calculation exactly. It also demonstrates overfitting by plotting train versus
test accuracy against `max_depth`.

---

## Experiment 12 — Naïve Bayes, compared with the tree

**WEKA — NOT EXECUTED**

1. **Classify** → *Choose* → `bayes/NaiveBayes`
   - `useSupervisedDiscretization = True` often helps on numeric data
2. Same 10-fold cross-validation. *Start*.
3. Compare with Experiment 11's numbers.
4. **Use the Experimenter for a proper comparison:** *Experimenter* → New →
   add both classifiers → add the dataset → Run → *Analyse* → **Paired T-Tester**.

That last step is what separates a good answer from a complete one. Comparing
two accuracy figures from a single run proves nothing; **a paired t-test over
the cross-validation folds** is the correct method, and it is exactly Course 4
Unit 5's paired t-test applied here.

**Python equivalent — `12_naive_bayes.py`** reproduces **Unit 4 §4.12's hand
calculation** — for X = (Sunny, Cool, High, Strong) the unnormalised posteriors
are 0.005291 for Yes and 0.020571 for No, giving P(No|X) = 0.7954 — then
demonstrates the **zero-frequency problem** and fixes it with Laplace
smoothing, and finally runs a paired t-test between the tree and Naïve Bayes
across 10 folds.

---

## Experiment 13 — Rule-based classification

**WEKA — NOT EXECUTED**

1. **Classify** → *Choose* → `rules/JRip` (this is **RIPPER**)
   - `folds = 3` — used for the pruning split
   - `minNo = 2`
2. Or `rules/PART`, which builds partial C4.5 trees and takes the best leaf as
   a rule each round.
3. Also try `rules/ZeroR` (always predicts the majority class) and `rules/OneR`
   (a single best attribute).

**Always run ZeroR first.** It is your **baseline**: if your sophisticated
classifier does not beat "always guess the majority", it has learned nothing.
On an imbalanced dataset ZeroR alone can score 95%, which is the accuracy
paradox of Unit 4 §4.9 made concrete in one click.

**Python equivalent — `13_rules.py`** extracts rules from a decision tree
(Unit 4 §4.10's five weather rules), computes each rule's coverage and
accuracy, and compares against a `DummyClassifier(strategy='most_frequent')` —
the scikit-learn ZeroR.

---

## Experiment 14 — Compare classifiers: confusion matrix, accuracy, ROC

**WEKA — NOT EXECUTED**

1. Run J48, NaiveBayes, IBk (k-NN), JRip and ZeroR on the same data with the
   same 10-fold cross-validation and the same seed.
2. For each, record accuracy, precision, recall, F-measure and ROC area.
3. **Right-click a result → *Visualize threshold curve* → select the positive
   class** for the ROC curve. The AUC is printed in its title bar.
4. Use the **Experimenter** with the Paired T-Tester for significance.

**Python equivalent — `14_compare.py`** runs five classifiers under stratified
10-fold cross-validation, prints a full comparison table, computes ROC/AUC, and
reproduces **Unit 4 §4.9's spam confusion matrix** (accuracy 0.920, precision
0.8333, recall 0.750, F1 0.7895) and **Practice Problem 2's medical screening
example** (accuracy 0.9005 but precision only **0.0876**) — the base rate
fallacy, asserted.

---

## Experiment 15 — Text preprocessing, TF-IDF and K-Means

**WEKA — NOT EXECUTED**

1. Load a text dataset (`ReutersCorn-train.arff`, or build one with the
   *TextDirectoryLoader*).
2. **Preprocess** → `filters/unsupervised/attribute/StringToWordVector`
   - `IDFTransform = True`, `TFTransform = True` → **TF-IDF**
   - `lowerCaseTokens = True`
   - `stopwordsHandler = Rainbow` (or supply a stopword file)
   - `stemmer = IteratedLovinsStemmer` or `SnowballStemmer`
   - `wordsToKeep = 1000`
   - `tokenizer = WordTokenizer` (or `NGramTokenizer` for n-grams)
3. Then **Cluster** → `SimpleKMeans` on the resulting vectors.

**Python equivalent — `15_text_clustering.py`** implements TF-IDF from first
principles alongside scikit-learn's `TfidfVectorizer`, asserting the two agree,
then clusters. **It reproduces Course 6's TF-IDF lab result**, so the two
courses' answers are checked against each other.

The demonstration is built so that **a term appearing in every document gets an
IDF of exactly zero** — the property that makes TF-IDF work — and the script
asserts it rather than merely stating it.

---

## Lab examination

The examiner gives you a dataset, an experiment number, and about an hour.

**What costs marks:**

- Forgetting to **remove the class attribute** before clustering
- Reporting **training-set** accuracy instead of cross-validated accuracy
- Quoting accuracy alone on an imbalanced dataset
- Not knowing that **J48 is C4.5** and **JRip is RIPPER**
- Confusing supervised with unsupervised Discretize
- Leaving a numeric-looking identifier column as numeric
- Being unable to explain what `(9/2)` at a J48 leaf means
- Comparing two classifiers by a single accuracy figure

**What earns them:**

- Run **ZeroR first**, every time, and state the baseline.
- Use **10-fold stratified cross-validation** and say why: one holdout split is
  high-variance, and stratification matters when classes are imbalanced.
- Read the **confusion matrix**, not just the accuracy line, and say which
  error costs more in this application.
- Use the **Experimenter and a paired t-test** when asked to compare.
- When you set a parameter, say what it does — `confidenceFactor = 0.25` means
  *more* pruning at *lower* values, which is counter-intuitive and worth
  demonstrating that you know.
- Connect back to the theory: the root of your J48 tree should be the attribute
  with the highest information gain, and you can verify that by hand on the
  weather data in two minutes.
