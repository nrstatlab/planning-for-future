# Practical Lab

**15 experiments**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.
Recommended datasets: `weather.arff`, `iris.arff`, `supermarket.arff`,
`vote.arff`, `contact-lenses.arff`, or custom CSV.

Code lives in `labs/course-8-datamining/`.

> **Both halves run.** The syllabus prescribes **WEKA**, and WEKA 3.8.7 runs here, with the
> datasets that come with it. Each experiment has:
>
> - **The WEKA click-path** in the Explorer, step by step (tab, filter, parameters, what to
>   read off the output) — what the examiner will ask you to demonstrate.
> - **The same in WEKA from the command line**, `NN_name_weka.sh`. Each command runs the WEKA
>   class the Explorer runs for that choice, and prints what the Explorer's output pane shows,
>   so its output is the output you will see.
> - **A scikit-learn / mlxtend equivalent**, `NN_name.py`, which reproduces the hand-computed
>   values in Units 2–5 and asserts them, run by `tools/data-science/run_data_labs.py`.
>
> Until October 2026 WEKA could not be installed where these labs are checked, and the
> click-paths were marked NOT EXECUTED. WEKA's own site still cannot be reached; Maven Central
> serves its jar, and the Waikato repository its datasets, and
> `tools/data-science/setup_weka.sh` fetches both and checks each file's SHA-256.
> **Experiment 7 has no WEKA half**: WEKA has no multilevel association miner, as it says.

```bash
pip install -r tools/data-science/requirements.txt
tools/data-science/setup_weka.sh                  # WEKA and its datasets, in /tmp/weka
python3 tools/data-science/run_data_labs.py       # the Python halves, asserted
bash data-science/labs/course-8-datamining/11_decision_tree_weka.sh   # one WEKA half
```

WEKA reports how long each model took to build; those lines differ on every run, and
`capture_lab_outputs.py --check` sets them aside.

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

Every Explorer choice is a WEKA class, and the command line names it: the
Classify tab's `trees/J48` is `weka.classifiers.trees.J48`, the Preprocess filter
`unsupervised/attribute/Normalize` is `weka.filters.unsupervised.attribute.Normalize`.
That is how the `_weka.sh` scripts repeat a click-path.

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

### 1. Question

Load datasets in ARFF and CSV formats, and explore their attributes.

### 2. Aim

Load data into WEKA, read its attribute summary, and convert between ARFF and CSV.

### 3. Steps

**In WEKA**, from the command line, `01_load_explore_weka.sh`:

1. **Load the data, and read the Preprocess panel's summary (Open file...).**
2. **Load the numeric version, whose temperature and humidity are numbers.**
3. **Save it as CSV, and load the CSV back (Save..., then Open file... as CSV).**
4. **Turn a numeric attribute into a nominal one (filter NumericToNominal).**

**In Python**, `01_load_explore.py`:

1. **Parse the ARFF file, and check its instances and attributes.**
2. **Describe the data, as WEKA's Preprocess panel does.**
3. **Write it as CSV and read it back.**
4. **Turn a numeric-looking code into a category.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

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
</div>


### 4. Programme

**In WEKA**, from the command line, `01_load_explore_weka.sh`:

{{programme: course-8-datamining/01_load_explore_weka.sh}}

**In Python**, `01_load_explore.py`:

{{programme: course-8-datamining/01_load_explore.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `01_load_explore_weka.sh`:

{{output: course-8-datamining/01_load_explore_weka.sh}}

**In Python**, `01_load_explore.py`:

{{output: course-8-datamining/01_load_explore.py}}

WEKA's summary is the Preprocess panel as a table: **Nom**, **Int** and **Real** are the
shares of each attribute's values that are nominal, whole numbers and decimals. Loaded back from
CSV, `temperature` is numeric (Int 100%, 12 distinct values); after `NumericToNominal` it is
nominal, with one label per value. The Python half parses the same ARFF and checks the round
trip.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

weather.nominal has 14 instances and 5 nominal attributes, the class last. CSV keeps the data but not its types, and NumericToNominal turns a number into a category.
</div>


## Experiment 2 — Data cleaning and missing values

### 1. Question

Clean a dataset that has missing values.

### 2. Aim

Find and replace missing values in WEKA, and see what mean imputation does to the data.

### 3. Steps

**In WEKA**, from the command line, `02_missing_values_weka.sh`:

1. **Load labor.arff, and count its missing values (the Missing column).**
2. **Replace them, by mean and mode (filter ReplaceMissingValues).**
3. **Count them again.**

**In Python**, `02_missing_values.py`:

1. **Impute the worked example's missing ages.**
2. **See mean imputation shrink the variance.**
3. **Compare the imputation strategies.**
4. **Flag the missing values before imputing.**
5. **Impute after splitting, not before.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

1. Load a dataset with missing values (`labor.arff`, or `weather` with `?`
   inserted).
2. **Preprocess** → *Choose* →
   `filters/unsupervised/attribute/ReplaceMissingValues` → *Apply*.
3. Read the attribute panel: the **Missing** count falls to 0.

WEKA's `ReplaceMissingValues` uses the **mean** for numeric attributes and the
**mode** for nominal ones. To drop rows instead, use
`filters/unsupervised/instance/RemoveWithValues` with
`matchMissingValues = True`.
</div>


### 4. Programme

**In WEKA**, from the command line, `02_missing_values_weka.sh`:

{{programme: course-8-datamining/02_missing_values_weka.sh}}

**In Python**, `02_missing_values.py`:

{{programme: course-8-datamining/02_missing_values.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `02_missing_values_weka.sh`:

{{output: course-8-datamining/02_missing_values_weka.sh}}

**In Python**, `02_missing_values.py`:

{{output: course-8-datamining/02_missing_values.py}}

`labor.arff` has missing values in 16 of its 17 attributes — 42 of 57 in
`wage-increase-third-year`, 48 in `standby-pay`. After the filter, every Missing count is 0.

The Python half implements mean, median, mode and k-NN imputation on the same idea and
**demonstrates the variance shrinkage** from Unit 2 §2.5 numerically: imputing 30% of a column
with its mean measurably lowers the standard deviation, and the script asserts it.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

ReplaceMissingValues fills every gap in labor.arff, by mean and mode; the Python half shows the cost, a smaller spread, and asserts it.
</div>


## Experiment 3 — Normalization and discretization

### 1. Question

Normalise and discretise numeric attributes.

### 2. Aim

Scale attributes to a common range, and turn numbers into bins three ways.

### 3. Steps

**In WEKA**, from the command line, `03_normalize_discretize_weka.sh`:

1. **Normalise every numeric attribute to [0, 1] (filter Normalize).**
2. **Discretise into 3 equal-width bins (filter Discretize, bins = 3).**
3. **And into 3 equal-frequency bins (useEqualFrequency = True).**
4. **Discretise using the class, by Fayyad-Irani MDL (the supervised Discretize).**

**In Python**, `03_normalize_discretize.py`:

1. **Normalise by min-max and by z-score.**
2. **See one outlier crush min-max scaling.**
3. **Smooth by equal-frequency binning.**
4. **Discretise the ages into three bins.**
5. **Binarise a category, rather than numbering it.**
6. **Find which algorithms need scaling.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

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
</div>


### 4. Programme

**In WEKA**, from the command line, `03_normalize_discretize_weka.sh`:

{{programme: course-8-datamining/03_normalize_discretize_weka.sh}}

**In Python**, `03_normalize_discretize.py`:

{{programme: course-8-datamining/03_normalize_discretize.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `03_normalize_discretize_weka.sh`:

{{output: course-8-datamining/03_normalize_discretize_weka.sh}}

**In Python**, `03_normalize_discretize.py`:

{{output: course-8-datamining/03_normalize_discretize.py}}

The three discretisations of `petallength` show the difference. Equal width cuts at
2.97 and 4.93, a third of the range each; equal frequency at 2.45 and 4.85, so each bin holds
about 50 flowers; the supervised version cuts at 2.45 and 4.75, where the
species change.

The Python half reproduces Unit 2's worked examples exactly: min–max of 25 in that
twelve-value set is **0.1477**; equal-width bins of the ages have edges 27.67 and 47.33; and
equal-frequency bins hold three values each. All asserted.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Normalize maps every measurement to [0, 1]; Discretize makes three bins by width or by frequency, and the supervised version places its cuts by the class.
</div>


## Experiment 4 — Attribute selection and PCA

### 1. Question

Select the most useful attributes, by a filter and by a wrapper, and reduce the data with PCA.

### 2. Aim

Rank and select attributes in WEKA, and transform them into principal components.

### 3. Steps

**In WEKA**, from the command line, `04_feature_selection_weka.sh`:

1. **Rank the attributes by information gain (InfoGainAttributeEval, Ranker).**
2. **Choose a subset with a wrapper round J48 (WrapperSubsetEval, BestFirst).**
3. **Principal components of the four measurements, with their eigenvalues.**
4. **Replace the attributes by the components, as the Preprocess filter does.**

**In Python**, `04_feature_selection.py`:

1. **Rank the attributes by information gain.**
2. **Select a subset with a wrapper.**
3. **Read the worked example's eigenvalues.**
4. **Count the components for 90% of the variance.**
5. **Standardise before PCA.**
6. **See what PCA costs in interpretability.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

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
  `-0.581petallength-0.566petalwidth-0.522sepallength+0.263sepalwidth`

**Read that attribute name carefully in the viva** — it is the eigenvector, and
it is exactly why PCA costs you interpretability.
</div>


### 4. Programme

**In WEKA**, from the command line, `04_feature_selection_weka.sh`:

{{programme: course-8-datamining/04_feature_selection_weka.sh}}

**In Python**, `04_feature_selection.py`:

{{programme: course-8-datamining/04_feature_selection.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `04_feature_selection_weka.sh`:

{{output: course-8-datamining/04_feature_selection_weka.sh}}

**In Python**, `04_feature_selection.py`:

{{output: course-8-datamining/04_feature_selection.py}}

Information gain ranks `petallength` (1.418) and `petalwidth` (1.378) far above the
sepal measurements; the wrapper, asking J48 itself, keeps `petalwidth` alone. Two principal
components, with eigenvalues 2.911 and 0.921, cover 95.8% of the variance of the four
measurements.

**Corrected:** this page gave the component's name as
`0.348petallength+0.318petalwidth-0.221sepalwidth...`; WEKA 3.8.7's is the one above. The
script removes the class before the Select-attributes PCA: given it, that evaluator mixes the
three species into the components as numbers, which the Preprocess filter does not.

The Python half ranks the iris attributes by information gain, runs PCA, and checks the
cumulative variance against Unit 2's worked eigenvalue table.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Petal length and width carry the information; two components keep 95.8% of the variance, at the cost of names that are no longer measurements.
</div>


## Experiment 5 — Summarize and visualize

### 1. Question

Summarise a dataset and visualise it, comparing the classes.

### 2. Aim

Describe each attribute, and compare the classes on each.

### 3. Steps

**In WEKA**, from the command line, `05_summarize_weka.sh`:

1. **Summarise every attribute (the Preprocess panel).**
2. **Summarise each class on its own (filter RemoveWithValues, one species at a time).**

**In Python**, `05_summarize.py`:

1. **Load the iris data.**
2. **Summarise each attribute.**
3. **Compare the classes.**
4. **Find the attribute that separates them.**
5. **Find the correlations.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

1. **Preprocess** → click each attribute for its statistics.
2. *Visualize All* → a histogram per attribute, coloured by class.
3. **Visualize** tab → the scatter-plot matrix; set *Colour* to the class.
4. Click any cell to enlarge it; *Jitter* separates overlapping points.

**Class-wise comparison:** set *Class* as the colour, then look for an
attribute whose histogram separates the colours. In iris, `petallength`
separates setosa completely — which is the visual form of "petallength has the
highest information gain".
</div>


### 4. Programme

**In WEKA**, from the command line, `05_summarize_weka.sh`:

{{programme: course-8-datamining/05_summarize_weka.sh}}

**In Python**, `05_summarize.py`:

{{programme: course-8-datamining/05_summarize.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `05_summarize_weka.sh`:

{{output: course-8-datamining/05_summarize_weka.sh}}

**In Python**, `05_summarize.py`:

{{output: course-8-datamining/05_summarize.py}}

The plots are the Explorer's to draw; the command line gives their numbers. One
summary per species shows how far apart they are: setosa's petal lengths take only 9 distinct
values, all small.

The Python half prints per-class means and standard deviations and confirms the separation
numerically.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Petal length separates setosa from the other two species completely.
</div>


## Experiment 6 — Association rules with Apriori

### 1. Question

Mine association rules from transaction data with Apriori.

### 2. Aim

Find frequent itemsets and strong rules with Apriori, and read support, confidence and lift.

### 3. Steps

**In WEKA**, from the command line, `06_apriori_weka.sh`:

1. **Mine the supermarket data with Apriori, for the 10 best rules (Associate tab).**
2. **The same data, ranked by lift instead of confidence (metricType = Lift).**

**In Python**, `06_apriori.py`:

1. **Trace Apriori on the five transactions.**
2. **Mine the nine transactions of Practice Problem 1.**
3. **See where confidence misleads, and lift does not.**
4. **Find the negative association in tea and coffee.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

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
</div>


### 4. Programme

**In WEKA**, from the command line, `06_apriori_weka.sh`:

{{programme: course-8-datamining/06_apriori_weka.sh}}

**In Python**, `06_apriori.py`:

{{programme: course-8-datamining/06_apriori.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `06_apriori_weka.sh`:

{{output: course-8-datamining/06_apriori_weka.sh}}

**In Python**, `06_apriori.py`:

{{output: course-8-datamining/06_apriori.py}}

Every one of the ten best rules by confidence ends in `bread and cake`: with
confidence 0.91–0.92 and lift 1.26–1.27, a large basket that holds biscuits and fruit almost
always holds bread too. Ranked by lift instead, the rules change — `fruit` with `bread and cake`
and `vegetables` comes first, at lift 1.22 but confidence only 0.6.

The Python half uses `mlxtend` and reproduces **Unit 3 §3.4's trace exactly** — the same five
transactions, minsup 0.6, giving the nine frequent itemsets and the two strong rules
`{B,C}→{E}` and `{C,E}→{B}`, each with confidence 1.00 and lift 1.25. It also runs Unit 3's
Practice Problem 1 and asserts all thirteen frequent itemsets and all three strong rules.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

On the supermarket data the strongest rules predict bread and cake; Unit 3's hand traces are reproduced exactly.
</div>


## Experiment 7 — Multilevel association rules

### 1. Question

Mine multilevel association rules over a product hierarchy.

### 2. Aim

Mine rules at more than one level of a hierarchy, and drop the redundant ones.

### 3. Steps

1. **Try one support threshold at every level.**
2. **Lower the threshold at the deeper levels.**
3. **Drop a rule its ancestor already explains.**
4. **Check an ancestor's support against its children's.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

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
</div>


### 4. Programme

{{programme: course-8-datamining/07_multilevel.py}}

### 5. Execution and Results

{{output: course-8-datamining/07_multilevel.py}}

There is no `_weka.sh` for this experiment: there is no WEKA class to run.

`07_multilevel.py` builds a small product taxonomy, expands each transaction with its
ancestors, mines at two levels with different thresholds, and demonstrates the redundancy test:
a descendant rule is reported only when its confidence **deviates** from what the ancestor rule
predicts.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

One support threshold cannot serve every level; reduced support finds the deeper rules, and the redundancy test keeps only those that add something.
</div>


## Experiment 8 — K-Means clustering

### 1. Question

Cluster a dataset with K-Means, and compare the clusters with the classes.

### 2. Aim

Run K-Means in WEKA, read its centroids and error, and see the seed change the answer.

### 3. Steps

**In WEKA**, from the command line, `08_kmeans_weka.sh`:

1. **Cluster iris into 3, ignoring the class, then compare with it (SimpleKMeans, classes to clusters).**
2. **The same with another seed, which can change the answer (seed = 31). Most.**

**In Python**, `08_kmeans.py`:

1. **Run K-Means by hand on the eight 1-D points.**
2. **Run it on the eight 2-D points of Practice Problem 1.**
3. **Check that scikit-learn agrees.**
4. **See the starting centroids change the answer.**
5. **Choose k by the elbow and the silhouette.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

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

On the command line, `-c last` does steps 2 and 4 together: the class is left out of the
clustering and used to evaluate it.
</div>


### 4. Programme

**In WEKA**, from the command line, `08_kmeans_weka.sh`:

{{programme: course-8-datamining/08_kmeans_weka.sh}}

**In Python**, `08_kmeans.py`:

{{programme: course-8-datamining/08_kmeans.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `08_kmeans_weka.sh`:

{{output: course-8-datamining/08_kmeans_weka.sh}}

**In Python**, `08_kmeans.py`:

{{output: course-8-datamining/08_kmeans.py}}

With seed 10 the clusters match the species but for 17 flowers (11.3%), all versicolor
and virginica, with a squared error of 7.00. Seed 31 stops in a worse local optimum, error
10.91: it splits setosa in two and merges the other species. Most seeds find the first answer.

The Python half reproduces **Unit 5 §5.2's 1-D trace** (final centroids 3.0 and 16.6, WCSS
289.2) and **Practice Problem 1's 2-D trace** (centroids (3.25, 8.0) and (5.5, 3.75), WCSS
54.50), both asserted, then runs the elbow and silhouette methods on iris.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

K-Means recovers the three species with 17 errors from a good start, and finds a worse clustering from a bad one.
</div>


## Experiment 9 — Hierarchical clustering and dendrograms

### 1. Question

Cluster a dataset hierarchically, and draw the dendrogram.

### 2. Aim

Build a hierarchical clustering in WEKA, and compare single and complete linkage.

### 3. Steps

**In WEKA**, from the command line, `09_hierarchical_weka.sh`:

1. **Cluster iris by single linkage, and print the tree (HierarchicalClusterer, printNewick).**
2. **The same by complete linkage.**

**In Python**, `09_hierarchical.py`:

1. **Build the worked example's dendrogram.**
2. **Build Practice Problem 2's.**
3. **Compare single and complete linkage.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

1. **Cluster** → *Choose* → `HierarchicalClusterer`
   - `numClusters = 3`
   - `linkType` = SINGLE / COMPLETE / AVERAGE / WARD / CENTROID / MEAN /
     ADJCOMPLETE / NEIGHBOR_JOINING
   - `printNewick = True` to print the tree
2. **Right-click the result in the Result list → *Visualize tree*** for the
   dendrogram. That step is easy to miss and is the whole point of the
   experiment.
</div>


### 4. Programme

**In WEKA**, from the command line, `09_hierarchical_weka.sh`:

{{programme: course-8-datamining/09_hierarchical_weka.sh}}

**In Python**, `09_hierarchical.py`:

{{programme: course-8-datamining/09_hierarchical.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `09_hierarchical_weka.sh`:

{{output: course-8-datamining/09_hierarchical_weka.sh}}

**In Python**, `09_hierarchical.py`:

{{output: course-8-datamining/09_hierarchical.py}}

The dendrogram is the Explorer's to draw; `printNewick` prints the same tree as text.
Single linkage **chains**: it puts versicolor and virginica in one cluster and leaves a single
setosa flower as a cluster of its own, 51 errors (34%). Complete linkage gives three real groups,
18 errors (12%).

The Python half reproduces **Unit 5 §5.4's worked dendrogram** — merges at heights 2, 3, 4, 5
under single linkage — and **Practice Problem 2** (heights 2, 3, 5, 6, giving {P1,P3,P5} and
{P2,P4} at a cut of 5). It also shows complete linkage on the same matrix so the difference in
merge heights is visible.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Single linkage chains the two close species together; complete linkage separates all three, with 18 errors.
</div>


## Experiment 10 — EM clustering

### 1. Question

Cluster a dataset with EM, and compare it with K-Means.

### 2. Aim

Fit a mixture model with EM, let it choose the number of clusters, and compare with K-Means.

### 3. Steps

**In WEKA**, from the command line, `10_em_clustering_weka.sh`:

1. **Let EM choose the number of clusters by cross-validation (EM, numClusters = -1).**
2. **EM with 3 clusters, to compare with K-Means.**

**In Python**, `10_em_clustering.py`:

1. **Compare soft and hard assignment.**
2. **Fit elliptical clusters with EM.**
3. **Choose k by BIC.**
4. **See K-Means as a special case of EM.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

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
</div>


### 4. Programme

**In WEKA**, from the command line, `10_em_clustering_weka.sh`:

{{programme: course-8-datamining/10_em_clustering_weka.sh}}

**In Python**, `10_em_clustering.py`:

{{programme: course-8-datamining/10_em_clustering.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `10_em_clustering_weka.sh`:

{{output: course-8-datamining/10_em_clustering_weka.sh}}

**In Python**, `10_em_clustering.py`:

{{output: course-8-datamining/10_em_clustering.py}}

Left to choose, EM picks **5** clusters on iris by cross-validation — more than the
three species, and 40% "incorrectly clustered" against them, because the likelihood rewards
splitting a species. Told 3, it does better than K-Means: 14 errors (9.3%) against 17.

The Python half fits a `GaussianMixture`, prints the responsibilities for a few boundary
points to make "soft assignment" concrete, and selects k by **BIC**.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

EM chose 5 clusters by itself; with 3 it misplaced 14 flowers, three fewer than K-Means.
</div>


## Experiment 11 — Decision tree with J48

### 1. Question

Build a decision tree classifier with J48, and evaluate it.

### 2. Aim

Build and read a J48 tree, and evaluate it by cross-validation.

### 3. Steps

**In WEKA**, from the command line, `11_decision_tree_weka.sh`:

1. **Build J48 on the weather data, and cross-validate it 10 ways (Classify tab).**
2. **The same tree, unpruned (unpruned = True).**

**In Python**, `11_decision_tree.py`:

1. **Trace ID3 on the weather data.**
2. **Compute C4.5's gain ratio.**
3. **Check that scikit-learn picks the same root.**
4. **Watch the tree overfit as it deepens.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

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
</div>


### 4. Programme

**In WEKA**, from the command line, `11_decision_tree_weka.sh`:

{{programme: course-8-datamining/11_decision_tree_weka.sh}}

**In Python**, `11_decision_tree.py`:

{{programme: course-8-datamining/11_decision_tree.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `11_decision_tree_weka.sh`:

{{output: course-8-datamining/11_decision_tree_weka.sh}}

**In Python**, `11_decision_tree.py`:

{{output: course-8-datamining/11_decision_tree.py}}

The root is **outlook**, as Unit 4 §4.5's information gains say it must be: 5 leaves,
every training day classified correctly. Cross-validated, it gets 7 of 14 right — 50%, worse
than always saying "yes" (64%). Fourteen days are too few to learn from and test on.

The Python half builds a tree with `criterion='entropy'` on the weather data and asserts that
the **root split is Outlook** with information gain **0.2467** — matching Unit 4 §4.5's hand
calculation exactly. It also demonstrates overfitting by plotting train versus test accuracy
against `max_depth`.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

J48's root is outlook, as the hand calculation says; on 14 instances its cross-validated accuracy is 50%.
</div>


## Experiment 12 — Naïve Bayes, compared with the tree

### 1. Question

Classify with Naive Bayes, and compare it with the decision tree.

### 2. Aim

Build a Naive Bayes classifier in WEKA, and compare it with J48 fairly.

### 3. Steps

**In WEKA**, from the command line, `12_naive_bayes_weka.sh`:

1. **Naive Bayes on the weather data, cross-validated 10 ways.**
2. **J48 and Naive Bayes on the vote data, the same 10 folds (seed 1), for a fair comparison.**

**In Python**, `12_naive_bayes.py`:

1. **Classify by hand, as the notes do.**
2. **Classify Practice Problem 3's day.**
3. **See one unseen value zero the product, and smooth it.**
4. **Work in logs, to avoid underflow.**
5. **Check that scikit-learn agrees.**
6. **Compare with the tree by a paired t-test.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

1. **Classify** → *Choose* → `bayes/NaiveBayes`
   - `useSupervisedDiscretization = True` often helps on numeric data
2. Same 10-fold cross-validation. *Start*.
3. Compare with Experiment 11's numbers.
4. **Use the Experimenter for a proper comparison:** *Experimenter* → New →
   add both classifiers → add the dataset → Run → *Analyse* → **Paired T-Tester**.

That last step is what separates a good answer from a complete one. Comparing
two accuracy figures from a single run proves nothing; **a paired t-test over
the cross-validation folds** is the correct method, and it is exactly Statistical Foundations for Data Science
Unit 5's paired t-test applied here.
</div>


### 4. Programme

**In WEKA**, from the command line, `12_naive_bayes_weka.sh`:

{{programme: course-8-datamining/12_naive_bayes_weka.sh}}

**In Python**, `12_naive_bayes.py`:

{{programme: course-8-datamining/12_naive_bayes.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `12_naive_bayes_weka.sh`:

{{output: course-8-datamining/12_naive_bayes_weka.sh}}

**In Python**, `12_naive_bayes.py`:

{{output: course-8-datamining/12_naive_bayes.py}}

On the weather data Naive Bayes gets 8 of 14 by cross-validation (57%), one more than
J48. On the 435-vote data, with the same 10 folds for both, J48 gets 96.3% and Naive Bayes
90.1% — a clear difference, and the Experimenter's paired t-test is how to say whether it is
significant. The Experimenter is a GUI; the Python half runs the same paired t-test.

The Python half reproduces **Unit 4 §4.12's hand calculation** — for X = (Sunny, Cool, High,
Strong) the unnormalised posteriors are 0.005291 for Yes and 0.020571 for No, giving
P(No|X) = 0.7954 — then demonstrates the **zero-frequency problem** and fixes it with Laplace
smoothing, and finally runs a paired t-test between the tree and Naïve Bayes across 10
folds.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

On the vote data J48 beats Naive Bayes, 96.3% to 90.1%, on the same folds.
</div>


## Experiment 13 — Rule-based classification

### 1. Question

Classify with rules, and compare them with a baseline.

### 2. Aim

Learn rules with OneR, JRip and PART, and measure them against ZeroR.

### 3. Steps

**In WEKA**, from the command line, `13_rules_weka.sh`:

1. **ZeroR first, the baseline (rules/ZeroR).**
2. **OneR, the single best attribute (rules/OneR).**
3. **RIPPER (rules/JRip).**
4. **PART, rules from partial trees (rules/PART).**

**In Python**, `13_rules.py`:

1. **Write the rules, and measure their coverage and accuracy.**
2. **Check that they classify every day correctly.**
3. **Run ZeroR first, as the baseline.**
4. **See the accuracy paradox on imbalanced data.**
5. **Order rules that overlap.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

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
</div>


### 4. Programme

**In WEKA**, from the command line, `13_rules_weka.sh`:

{{programme: course-8-datamining/13_rules_weka.sh}}

**In Python**, `13_rules.py`:

{{programme: course-8-datamining/13_rules.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `13_rules_weka.sh`:

{{output: course-8-datamining/13_rules_weka.sh}}

**In Python**, `13_rules.py`:

{{output: course-8-datamining/13_rules.py}}

ZeroR says "yes" every time and scores 64%. OneR's rule is on outlook; JRip learns two
rules for "no" — sunny and humid, rainy and windy — and "yes" otherwise; PART a three-rule list.
Cross-validated on 14 days, none beats ZeroR: OneR gets 6, JRip 9, PART 8. That is the baseline's
lesson in its plainest form.

The Python half extracts rules from a decision tree (Unit 4 §4.10's five weather rules),
computes each rule's coverage and accuracy, and compares against a
`DummyClassifier(strategy='most_frequent')` — the scikit-learn ZeroR.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

On the weather data no rule learner beats ZeroR's 64% by cross-validation; the rules themselves match the tree's.
</div>


## Experiment 14 — Compare classifiers: confusion matrix, accuracy, ROC

### 1. Question

Compare several classifiers by their confusion matrices, accuracy and ROC.

### 2. Aim

Evaluate five classifiers the same way, and read accuracy, the confusion matrix and the ROC area.

### 3. Steps

**In WEKA**, from the command line, `14_compare_weka.sh`:

1. **Five classifiers on the same data, the same 10 folds (seed 1): accuracy, the confusion matrix, ROC area.**

**In Python**, `14_compare.py`:

1. **Read the spam filter's confusion matrix.**
2. **Work Practice Problem 2's base rate.**
3. **Compare five classifiers.**
4. **Test whether the differences are significant.**
5. **Compare them by ROC and AUC.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

1. Run J48, NaiveBayes, IBk (k-NN), JRip and ZeroR on the same data with the
   same 10-fold cross-validation and the same seed.
2. For each, record accuracy, precision, recall, F-measure and ROC area.
3. **Right-click a result → *Visualize threshold curve* → select the positive
   class** for the ROC curve. The AUC is printed in its title bar.
4. Use the **Experimenter** with the Paired T-Tester for significance.
</div>


### 4. Programme

**In WEKA**, from the command line, `14_compare_weka.sh`:

{{programme: course-8-datamining/14_compare_weka.sh}}

**In Python**, `14_compare.py`:

{{programme: course-8-datamining/14_compare.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `14_compare_weka.sh`:

{{output: course-8-datamining/14_compare_weka.sh}}

**In Python**, `14_compare.py`:

{{output: course-8-datamining/14_compare.py}}

On the vote data, by 10-fold cross-validation with seed 1:

| Classifier | Accuracy | ROC area |
|---|---|---|
| ZeroR | 61.4% | 0.491 |
| J48 | 96.3% | 0.971 |
| Naive Bayes | 90.1% | 0.973 |
| IBk | 92.4% | 0.965 |
| JRip | 95.4% | 0.942 |

Two things to say. IBk scores 99.8% on its training data and 92.4% cross-validated: one
neighbour remembers every instance. And Naive Bayes has the best ROC area with the worst of the
four accuracies — it ranks well and thresholds badly.

The Python half runs five classifiers under stratified 10-fold cross-validation, prints a full
comparison table, computes ROC/AUC, and reproduces **Unit 4 §4.9's spam confusion matrix**
(accuracy 0.920, precision 0.8333, recall 0.750, F1 0.7895) and **Practice Problem 2's medical
screening example** (accuracy 0.9005 but precision only **0.0876**) — the base rate fallacy,
asserted.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

J48 is the most accurate on the vote data, 96.3%; Naive Bayes has the best ROC area, 0.973.
</div>


## Experiment 15 — Text preprocessing, TF-IDF and K-Means

### 1. Question

Preprocess text into TF-IDF vectors, and cluster the documents.

### 2. Aim

Turn documents into word vectors in WEKA, weight them by TF-IDF, and cluster them.

### 3. Steps

**In WEKA**, from the command line, `15_text_clustering_weka.sh`:

1. **Turn the documents into TF-IDF vectors (filter StringToWordVector).**
2. **Cluster the vectors into 2 with K-Means, and compare with the class (SimpleKMeans).**

**In Python**, `15_text_clustering.py`:

1. **Check that a word in every document weighs zero.**
2. **Compute TF-IDF by hand and with scikit-learn.**
3. **Compare raw counts with TF-IDF.**
4. **Cluster the documents.**
5. **Cross-check with Course 6's TF-IDF.**

<div class="formula" markdown="1">
<span class="label">IN THE EXPLORER</span>

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
</div>


### 4. Programme

**In WEKA**, from the command line, `15_text_clustering_weka.sh`:

{{programme: course-8-datamining/15_text_clustering_weka.sh}}

**In Python**, `15_text_clustering.py`:

{{programme: course-8-datamining/15_text_clustering.py}}

### 5. Execution and Results

**In WEKA**, from the command line, `15_text_clustering_weka.sh`:

{{output: course-8-datamining/15_text_clustering_weka.sh}}

**In Python**, `15_text_clustering.py`:

{{output: course-8-datamining/15_text_clustering.py}}

StringToWordVector moves the class to the front, so the clusterer is told `-c first`.
Two clusters do not find "about corn" and "not": 42% of the 1,554 articles fall on the wrong side,
because K-Means groups articles by their commonest words, and those are not about corn. Only 45
of the articles are.

The Python half implements TF-IDF from first principles alongside scikit-learn's
`TfidfVectorizer`, asserting the two agree, then clusters. **It reproduces Data Science with R's
TF-IDF lab result**, so the two courses' answers are checked against each other.

The demonstration is built so that **a term appearing in every document gets an IDF of exactly
zero** — the property that makes TF-IDF work — and the script asserts it rather than merely
stating it.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

TF-IDF vectors cluster by topic in general, not by the one topic the class marks: 42% of the Reuters articles are on the wrong side.
</div>


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
