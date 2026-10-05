# Practical Lab

**12 experiments**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.

Code lives in `labs/course-12a-ml/`.

> **Everything in this course runs.** scikit-learn, NumPy, pandas, SciPy and
> matplotlib are all installed, so **all 12 practicals execute** and every
> figure in these notes is asserted by
> `tools/data-science/run_ml_labs.py`. Under **5. Execution and Results** is what each one
> printed, on the versions in `output/VERSIONS.txt`; Experiment 4's charts are shown as it drew
> them.
>
> **There is no "NOT EXECUTED" file anywhere in Machine Learning.** Nothing this
> course needs is blocked by the verification environment.
>
> Eleven courses run every experiment: **Problem Solving Using C**,
> **Python Programming and Data Structures**, **Data Science with R**,
> **Web Technologies**, **Data Mining**, **Python for Data Analysis and Visualization**,
> **Document Oriented Database**, **Machine Learning**, **Big Data Technologies**,
> **Artificial Intelligence** and **Time Series Analysis and Forecasting**. *(Updated October
> 2026: this said five; R, MongoDB and WEKA became installable here, and the Tkinter programs run
> under a virtual display. Then nine; the Hadoop stack and SWI-Prolog became installable too.)*
>
> Every script fixes `random_state`, so **the numbers below reproduce on your
> machine**. If you get something different, something differs — that is the
> point of fixing the seed.

```bash
pip install -r tools/requirements.txt
python3 tools/data-science/run_ml_labs.py
```

## Two cross-course checks run as part of the suite

| Check | Asserts |
|---|---|
| **Experiment 6 against Statistical Foundations for Data Science** | scikit-learn reproduces Statistical Foundations for Data Science's *hand-computed* regression — slope **4.3030**, intercept **43.0303**, R² **0.9958**, prediction at 7.5 = **75.3030** |
| **Experiments 8 and 9 against Data Mining** | The same entropy and information gain (**0.2467**) and the same Naive Bayes posteriors (**0.005291** and **0.020571**) |

**If the two courses ever disagree, one of them is wrong, and the suite says
so.** That is the point of reusing the datasets rather than inventing new ones.

## The three datasets

| Name | What | Why |
|---|---|---|
| `STUDY` | Statistical Foundations for Data Science's ten (hours, score) pairs | Cross-course verification, and small enough to check by hand |
| `iris` | 150 flowers, 4 features, 3 species | Small, clean, famous — and the same data Data Mining used in WEKA |
| `churn` | 400 customers, **15% positive** | Built, not loaded, so the **base rate is exactly known** — which is what makes Unit 2's accuracy argument measurable |

---

## Experiment 1 — Import and export data with pandas

### 1. Question

Import and export data in CSV, Excel, JSON and Parquet with pandas.

### 2. Aim

Round-trip a frame through each format, and catch what each one silently changes.

### 3. Steps

1. **Write a CSV and read it back.**
2. **See what the default index does.**
3. **See which types a CSV loses.**
4. **Write and read Excel, with several sheets.**
5. **Compare the JSON orientations.**
6. **Round-trip through Parquet.**
7. **Read part of a large file.**

<div class="formula" markdown="1">
<span class="label">THE TRAPS</span>

Every format has a way of silently changing your data, and each one is demonstrated
failing and then fixed:

| Trap | What happens |
|---|---|
| `to_csv()` with the default index | Comes back as a junk **`Unnamed: 0`** column |
| CSV stores text | `"001", "002", "010"` returns as **`[1, 2, 10]`** — leading zeros gone |
| Dates through CSV | Come back as **strings**, not dates |
| JSON `orient` | Five orientations produce five different files; read with the wrong one and the frame is transposed or empty |

**Fixes asserted:** `index=False`, `dtype={"id": str}`, `parse_dates=[...]`,
and **Parquet**, which preserves every dtype exactly. Also `nrows`, `usecols`
and `chunksize` for files that will not fit in memory.
</div>


### 4. Programme

{{programme: course-12a-ml/01_import_export.py}}

### 5. Execution and Results

{{output: course-12a-ml/01_import_export.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Every trap is shown failing and then fixed; Parquet alone returns every dtype unchanged.
</div>


## Experiment 2 — Data pre-processing techniques

### 1. Question

Apply data pre-processing techniques: scaling, encoding and imputation.

### 2. Aim

Scale, encode and impute, and measure what each choice does to the data and to a model.

### 3. Steps

1. **Compare the scalers, with an outlier.**
2. **Encode the categories.**
3. **Meet the dummy variable trap.**
4. **See mean imputation shrink the variance.**
5. **Keep a was-missing flag.**
6. **Scale after splitting, in a pipeline.**

<div class="formula" markdown="1">
<span class="label">THE RESULTS</span>

| Result | Figure |
|---|---|
| **Min-max vs robust scaling** with one outlier | Min-max squeezes six normal points into a **0.0125-wide band**; robust keeps them **160× further apart** |
| **Mean imputation shrinks variance** | 30% missing: mean preserved *exactly*, standard deviation falls **16.3%** |
| **A `was_missing` flag** when missingness is informative | CV accuracy **0.4550 → 0.7575**, a gain of **+0.3025** from one binary column |
| **Label-encoding a nominal feature** | Invents distances — Red is "nearer" Green than Blue, which is a fact about alphabetical order |
| **The dummy variable trap** | Every full one-hot row sums to 1, so it is collinear with the intercept |
</div>


### 4. Programme

{{programme: course-12a-ml/02_preprocessing.py}}

### 5. Execution and Results

{{output: course-12a-ml/02_preprocessing.py}}

<div class="example" markdown="1">
<span class="label">THE LEAKAGE DEMONSTRATION IS DELIBERATELY HONEST</span>

Scaling before splitting versus a `Pipeline` gives **0.9400 either way** on this
data. The script says so rather than manufacturing a gap:

> the point is **not** that leakage always inflates the number, but that the
> leaky score **is not an estimate of anything**, because the transformer saw
> the test rows.

The mechanism is asserted instead — the two scalers learn measurably different
means.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Robust scaling keeps the normal points apart where min-max crushes them; a was-missing flag lifts accuracy from 0.4550 to 0.7575.
</div>


## Experiment 3 — Dimensionality reduction with PCA

### 1. Question

Reduce the dimensions of the iris data with Principal Component Analysis.

### 2. Aim

Compute the components and their explained variance, choose how many to keep, and see what PCA cannot do.

### 3. Steps

1. **Compute the explained variance.**
2. **See why scikit-learn's variances sum to more than 4.**
3. **Choose the number of components.**
4. **Compare PCA with LDA.**
5. **Standardise before PCA.**
6. **Measure the reconstruction error.**

<div class="formula" markdown="1">
<span class="label">THE COMPONENTS</span>

| Component | Eigenvalue | Explained | Cumulative |
|---|---:|---:|---:|
| PC1 | 2.9185 | 72.96% | 72.96% |
| PC2 | 0.9140 | 22.85% | **95.81%** |
| PC3 | 0.1468 | 3.67% | 99.48% |
| PC4 | 0.0207 | 0.52% | 100.00% |

**The eigenvalues sum to exactly 4** = p, a free arithmetic check.
</div>


### 4. Programme

{{programme: course-12a-ml/03_pca.py}}

### 5. Execution and Results

{{output: course-12a-ml/03_pca.py}}

Also asserted:

- **Reconstruction MSE equals 1 − variance kept, exactly.** At k=2 the MSE is
  **0.0419** against 0.9581 kept. "Losing 4.19% of the variance" is literally
  the squared error of rebuilding the four original columns.
- **Kaiser says 1 component, the 95% rule says 2.** They disagree, and that is
  normal.
- **PCA is unsupervised.** On two dimensions, LDA scores **0.9800** against
  PCA's **0.9133** — and all four raw features score 0.9600.
- **PCA without standardising reports your units.** Rescale sepal length to
  micrometres and PC1 explains **100.0000%** with a loading of 1.0000 on that
  one column.
- sklearn's `explained_variance_` sums to 4.0268 rather than 4.0 because it
  divides by n−1 — **exactly a factor of 150/149**. The ratios are identical.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Two components keep 95.81% of the variance; the eigenvalues sum to 4; reconstruction error equals the variance lost.
</div>


## Experiment 4 — Data visualization techniques

### 1. Question

Apply data visualization techniques to explore a dataset.

### 2. Aim

Compute what each chart shows and check it, starting with Anscombe's quartet.

### 3. Steps

1. **Plot Anscombe's quartet.**
2. **Vary the histogram's bin count.**
3. **Find outliers with a boxplot.**
4. **Read the scatter matrix and the correlations.**
5. **Plot the class balance first.**
6. **Sort x before a line plot.**

<div class="formula" markdown="1">
<span class="label">THE CENTREPIECE</span>

**Anscombe's quartet**, with the precision stated honestly:

| set | mean x | mean y | var y | r | slope | intercept |
|---|---:|---:|---:|---:|---:|---:|
| I | 9.00 | 7.50 | 4.13 | 0.816 | 0.500 | 3.00 |
| II | 9.00 | 7.50 | 4.13 | 0.816 | 0.500 | 3.00 |
| III | 9.00 | 7.50 | 4.12 | 0.816 | 0.500 | 3.00 |
| IV | 9.00 | 7.50 | 4.12 | 0.817 | 0.500 | 3.00 |

**Mean x is identical, the slope agrees to three decimals, and mean y,
intercept and r to two** — the folklore "identical to two decimals" overstates
the variance, which matches only to one. The four datasets look nothing alike.
</div>


### 4. Programme

{{programme: course-12a-ml/04_visualization.py}}

### 5. Execution and Results

{{output: course-12a-ml/04_visualization.py}}

**Also measured:** the histogram bin count changes the conclusion *in both
directions* — 2 bins show no structure, 5 and 15 find both real modes, and
**60 bins find fifteen**, which are sampling noise. Plus the IQR outlier rule,
iris correlations (petal length ~ petal width **0.9629**), and the class
balance plot that should be the first thing you make.

The three charts above are Anscombe's quartet, the histogram at four bin counts, and the
scatter with its fitted line. **Changed:** they were written to `output/`, which now holds what
each program printed; the program writes them to `plots/`.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Four datasets with the same summary statistics look nothing alike; 60 histogram bins find fifteen modes that are noise.
</div>


## Experiment 5 — Maximum likelihood estimation

### 1. Question

Estimate parameters by maximum likelihood.

### 2. Aim

Find the MLE of a coin's p two ways, and connect least squares to likelihood.

### 3. Steps

1. **Estimate a coin's p by grid search and by calculus.**
2. **See why logs are taken.**
3. **Show least squares is the MLE under normal errors.**
4. **Estimate a normal mean and variance.**

<div class="formula" markdown="1">
<span class="label">THE RESULTS</span>

- **The coin:** 7 heads in 10 gives p̂ = **0.7000** by calculus and by grid
  search. The MLE is the sample proportion.
- **Why logs:** `0.5 ** 2000` is **exactly 0.0** in floating point; `2000 ×
  ln(0.5)` is −1386.2944 and finite.
- **The connection worth knowing:** least squares and maximum likelihood, fitted
  independently on the study data, agree to **6.7 × 10⁻⁹**. Minimising squared
  error *is* maximising likelihood when the errors are normal.
- **MLE is not automatically unbiased:** the MLE of variance divides by n, and
  the ratio to the unbiased estimate is exactly √(n/(n−1)).
</div>


### 4. Programme

{{programme: course-12a-ml/05_mle.py}}

### 5. Execution and Results

{{output: course-12a-ml/05_mle.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

p̂ = 0.7000 by calculus and by grid search; least squares and maximum likelihood agree to 6.7 × 10⁻⁹.
</div>


## Experiment 6 — Simple and multiple linear regression

### 1. Question

Fit simple and multiple linear regression models.

### 2. Aim

Reproduce Statistical Foundations' regression, then see extrapolation, multicollinearity and overfitting go wrong.

### 3. Steps

1. **Fit the simple regression, and check it against Statistical Foundations.**
2. **Predict, and see the extrapolation trap.**
3. **Fit a multiple regression with collinear predictors.**
4. **Compare R² with adjusted R².**
5. **Raise the polynomial degree.**
6. **Compare Ridge with Lasso.**

<div class="formula" markdown="1">
<span class="label">THE RESULTS</span>

Reproduces Statistical Foundations for Data Science exactly (slope 4.3030, intercept 43.0303, R² 0.9958,
residuals summing to 7.1e-15, and R² = r²), then:

| Result | Figure |
|---|---|
| **Extrapolation** | x = 50 predicts **258.1818 marks** out of 100 |
| **Multicollinearity** | Two predictors correlating 0.9983: R² unchanged at **0.9767**, but the x₁ coefficient moves from 2.9887 to **3.4200** and x₂ picks up **−0.4419**. Prediction fine, interpretation destroyed |
| **Polynomial degree 9 on 10 points** | R² = **1.000000** — exact interpolation, overfitting made visible |
| **…without standardising** | R² = **0.9815**, *worse than a straight line*, because the condition number reaches **2.69 × 10¹³** |
| **Lasso vs Ridge** | With 12 predictors of which 3 matter: Ridge zeroes **0**, Lasso zeroes **9** |
</div>


### 4. Programme

{{programme: course-12a-ml/06_linear_regression.py}}

### 5. Execution and Results

{{output: course-12a-ml/06_linear_regression.py}}

<div class="example" markdown="1">
<span class="label">THE R² DEMONSTRATION IS DONE PROPERLY</span>

One dataset proves nothing, because adjusted R² can rise by chance. Over **300
random datasets**, adding 5 columns of pure noise:

| | Rose in | Mean change |
|---|---:|---:|
| **R²** | **300/300 (100%)** | **+0.005016** |
| **Adjusted R²** | 119/300 (39.7%) | −0.000171 |

**R² rose every single time.** The smallest change seen was still +0.000299.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The slope 4.3030, intercept 43.0303 and R² 0.9958 reproduce exactly; R² rose in 300 of 300 datasets when noise was added, adjusted R² in 119.
</div>


## Experiment 7 — Logistic regression

### 1. Question

Classify customers as churners with logistic regression.

### 2. Aim

Score the baseline first, fit the model, read its odds ratios, and move the threshold.

### 3. Steps

1. **Score the baseline first.**
2. **Fit the logistic regression.**
3. **Read the odds ratios.**
4. **Move the decision threshold.**
5. **Find the ROC curve's endpoints.**

<div class="formula" markdown="1">
<span class="label">THE RESULTS</span>

**The baseline first**, as Unit 2 §2.5 insists:

| Model | Accuracy | Recall |
|---|---:|---:|
| `DummyClassifier("most_frequent")` | **0.8500** | **0.0000** |
| Logistic regression | 0.9400 | 0.7333 |

**85% accurate and it identifies not one churner.**

Confusion matrix **TP 11, FP 2, FN 4, TN 83**, with precision 0.8462 (11/13),
recall 0.7333 (11/15), F1 0.7857 and **AUC 0.9882** — each recomputed by hand
from the four counts.

**Odds ratios:** `support_calls` has coefficient **2.2656**, so
e^2.2656 = **9.6367** — one extra standard deviation of calls multiplies the
**odds** of churning by 9.64. `tenure_months` gives 0.0988, i.e. ×0.10.
</div>


### 4. Programme

{{programme: course-12a-ml/07_logistic_regression.py}}

### 5. Execution and Results

{{output: course-12a-ml/07_logistic_regression.py}}

<div class="example" markdown="1">
<span class="label">THE THRESHOLD TABLE IS THE BEST ARTEFACT IN THIS EXPERIMENT</span>

| threshold | accuracy | precision | recall | F1 |
|---:|---:|---:|---:|---:|
| 0.10 | 0.9400 | 0.7143 | **1.0000** | 0.8333 |
| 0.30 | 0.9300 | 0.7857 | 0.7333 | 0.7586 |
| **0.50** | 0.9400 | 0.8462 | 0.7333 | 0.7857 |
| 0.70 | 0.9400 | **1.0000** | 0.6000 | 0.7500 |
| 0.90 | 0.8900 | **1.0000** | 0.2667 | 0.4211 |

**One model, five different classifiers.** At 0.10 it catches *every* churner;
at 0.90 it is never wrong about the ones it flags. The 0.5 cut-off is a
convention, not part of the model.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

85% accuracy from the baseline catches no churner; the model reaches 0.9400 accuracy, recall 0.7333 and AUC 0.9882.
</div>


## Experiment 8 — Decision tree classification

### 1. Question

Classify with a decision tree, and control its depth.

### 2. Aim

Compute entropy and gain by hand, then watch depth trade training accuracy against test accuracy.

### 3. Steps

1. **Compute entropy and gain by hand.**
2. **Vary max_depth.**
3. **Print a shallow tree.**
4. **Read the feature importances.**
5. **Cross-validate.**
6. **Grow a tree on iris.**

<div class="formula" markdown="1">
<span class="label">THE RESULTS</span>

Data Mining's entropy arithmetic first — parent 0.9403, weighted children 0.6935,
**gain 0.2467** — then the machine-learning question:

| `max_depth` | train | test | gap | leaves |
|---:|---:|---:|---:|---:|
| 1 | 0.9533 | 0.9200 | +0.0333 | 2 |
| 3 | 0.9800 | 0.9400 | +0.0400 | 5 |
| **5** | 0.9967 | **0.9500** | +0.0467 | 10 |
| 10 | **1.0000** | 0.9400 | +0.0600 | 11 |
| None | **1.0000** | 0.9400 | +0.0600 | 11 |

**Training accuracy reaches a perfect 1.0000 and test accuracy falls.**
</div>


### 4. Programme

{{programme: course-12a-ml/08_decision_tree.py}}

### 5. Execution and Results

{{output: course-12a-ml/08_decision_tree.py}}

The **noise feature gets importance exactly 0.0000**, and 5-fold CV gives
`[0.975, 0.9625, 0.925, 0.9, 0.95]` — mean 0.9425, sd 0.0269. A single split
could have reported anything from 0.90 to 0.975.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Gain 0.2467, as in Data Mining; training accuracy reaches 1.0000 while test accuracy falls; the noise column scores importance 0.0000.
</div>


## Experiment 9 — Naive Bayes classification

### 1. Question

Classify with Naive Bayes.

### 2. Aim

Reproduce Data Mining's posteriors, then see the zero-frequency problem and the false independence assumption.

### 3. Steps

1. **Compute the posteriors by hand.**
2. **See one zero destroy the posterior, and smooth it.**
3. **Measure how false independence is.**
4. **Compare Gaussian with multinomial.**
5. **Classify text.**

<div class="formula" markdown="1">
<span class="label">THE RESULTS</span>

Data Mining's posteriors reproduced — **0.005291** for Yes and **0.020571** for
No, normalising to 79.54% / 20.46% — then the two ideas that matter:

- **One zero destroys everything.** Posterior 0.005291 → **0.000000** when a
  single feature value was never seen with that class. Laplace smoothing
  restores it to **0.001443**. The likelihood is a *product*.
- **The independence assumption is measurably false.** Iris feature
  correlations reach **0.9629**, with three pairs above 0.8 — and GaussianNB
  still scores **0.9533** CV accuracy. Classification needs only the correct
  class to score highest.

Plus `MultinomialNB` on a toy spam corpus, and the note that scikit-learn's
`alpha=1.0` **is** Laplace smoothing, on by default.
</div>


### 4. Programme

{{programme: course-12a-ml/09_naive_bayes.py}}

### 5. Execution and Results

{{output: course-12a-ml/09_naive_bayes.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Posteriors 0.005291 and 0.020571, as in Data Mining; one zero sends a posterior to 0, and Laplace smoothing restores it to 0.001443.
</div>


## Experiment 10 — K-Means clustering

### 1. Question

Cluster the iris data with K-Means, and choose k.

### 2. Aim

Choose k by the elbow and the silhouette, and compare the clusters with the species.

### 3. Steps

1. **Find the elbow.**
2. **Compare the silhouette with the truth.**
3. **See where the errors fall.**
4. **Vary the initialisation.**
5. **Add an outlier.**

<div class="formula" markdown="1">
<span class="label">THE ELBOW</span>

| k | WCSS | drop | silhouette |
|---:|---:|---:|---:|
| 1 | **600.0000** | — | — |
| 2 | 222.3617 | 377.64 | **0.5818** |
| 3 | 139.8205 | 82.54 | 0.4599 |
| 4 | 114.0925 | 25.73 | 0.3869 |
| 6 | 81.5444 | 9.38 | 0.3171 |

**WCSS at k=1 is exactly 600 = 150 × 4** — a free check that the data was
standardised.
</div>


### 4. Programme

{{programme: course-12a-ml/10_kmeans.py}}

### 5. Execution and Results

{{output: course-12a-ml/10_kmeans.py}}

<div class="warn" markdown="1">
<span class="label">THE MOST INSTRUCTIVE RESULT IN THE COURSE</span>

**Silhouette prefers k = 2 (0.5818). Iris has three species.** At k=3 the ARI
against the truth is **0.6201**, better than k=2's 0.5681 — the geometric
metric and the ground truth disagree.

The confusion table shows why: **all 50 setosa land in one cluster**, while
versicolor (39/11) and virginica (14/36) bleed into each other. It is a
property of the flowers, not a bug.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The silhouette prefers k = 2; iris has three species, and at k = 3 the ARI is 0.6201.
</div>


## Experiment 11 — k-Nearest Neighbour classification

### 1. Question

Classify with k-Nearest Neighbours.

### 2. Aim

See when scaling matters and when it does not, and choose k.

### 3. Steps

1. **Scale features whose units differ.**
2. **Scale features whose units do not.**
3. **Choose k.**
4. **Compare distance metrics.**
5. **Time the lazy learner.**

<div class="formula" markdown="1">
<span class="label">THE RESULTS</span>

**Scaling, when units genuinely differ** — age in years against income in
rupees, where the true rule depends on age alone:

| | Test accuracy |
|---|---:|
| Unscaled | **0.5500** |
| Scaled | **0.9750** |

Income's standard deviation is **42,669×** age's.

**Scaling, when they do not** — iris, all four features in centimetres with a
spread ratio of only **4.05×**: unscaled **0.9778**, scaled **0.9111**.
**Scaling made it slightly worse.** The rule is about differing units, not
ritual.

**Choosing k:** k=1 scores 1.0000 on training by construction; at
k = n_train = 105 every query sees the same 105 votes and returns one fixed
class — **0.3333** on three balanced species.
</div>


### 4. Programme

{{programme: course-12a-ml/11_knn.py}}

### 5. Execution and Results

{{output: course-12a-ml/11_knn.py}}

Step 5's two times measure this machine at one moment, so they differ from run to run;
`capture_lab_outputs.py --check` sets those two lines aside and compares every other line
exactly. What they show does not change: fitting only stores the rows, and the work is done at
prediction.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Scaling lifts accuracy from 0.5500 to 0.9750 when the units differ, and lowers it slightly on iris, where they do not.
</div>


## Experiment 12 — DBSCAN

### 1. Question

Cluster with DBSCAN, and compare it with K-Means.

### 2. Aim

Cluster non-convex shapes, label core, border and noise points, choose eps, and find DBSCAN's own weakness.

### 3. Steps

1. **Cluster the crescents with DBSCAN and K-Means.**
2. **Try every k.**
3. **Label core, border and noise points.**
4. **Choose eps from the k-distance plot.**
5. **Cluster blobs of different density.**
6. **Compare hierarchical linkage.**

<div class="formula" markdown="1">
<span class="label">THE HEADLINE</span>

**The headline:** two interleaved crescents, 300 points.

| Algorithm | ARI |
|---|---:|
| K-Means (k=2) | **0.2475** |
| **DBSCAN** (eps 0.25, minPts 5) | **1.0000** |

And it is **not a tuning problem** — the best ARI K-Means achieves over
k = 2…10 is **0.2938**. Its boundaries are straight perpendicular bisectors, so
no k carves out a crescent.
</div>


### 4. Programme

{{programme: course-12a-ml/12_dbscan.py}}

### 5. Execution and Results

{{output: course-12a-ml/12_dbscan.py}}

<div class="warn" markdown="1">
<span class="label">DBSCAN'S OWN WEAKNESS, DEMONSTRATED HONESTLY</span>

A dense blob and a sparse one, centres 3 units apart:

| eps | clusters | noise | ARI | outcome |
|---:|---:|---:|---:|---|
| 0.30 | 1 | **60** | 1.0000 | sparse blob **discarded as noise** |
| 0.80 | 3 | 26 | 0.9307 | sparse blob fragmented |
| 1.50 | 1 | 1 | 0.0178 | the two **merged** |
| 2.50 | 1 | 0 | 0.0000 | the two **merged** |

**No single eps recovers both**, and K-Means scores 0.8335 here because both
blobs are convex. Neither algorithm is better in general.

**Note the ARI of 1.0000 at eps = 0.30** — a metric artefact. All 60 sparse
points got the single label −1, which ARI scores as a consistent group. **A
cluster of noise is not a cluster**, which is why you read the counts too.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

DBSCAN recovers the crescents exactly (ARI 1.0000) where no k lets K-Means pass 0.2938; no single eps recovers a dense and a sparse blob together.
</div>


---

## Lab examination

An hour, a dataset, one experiment number, then a viva.

**What costs marks:**

- Reporting accuracy without the base rate
- Preprocessing before splitting
- Passing a 1-D array as `X` (`Expected 2D array, got 1D array instead`)
- Forgetting to scale for k-NN, SVM or PCA
- Scaling for a decision tree "to be safe" — harmless, but it shows you do not
  know why scaling exists
- Reporting the training accuracy
- Tuning on the test set
- Claiming a winner from a single train/test split

**What earns them:**

- **Fit a `DummyClassifier` first and quote it.** One line, and it converts
  "94% accuracy" into a measurable 9-point gain.
- **Use a `Pipeline`.** Then leakage cannot happen inside cross-validation
  folds, and say that is why you used it.
- **Quote mean ± standard deviation from cross-validation.** On this data a
  single split ranges from 0.90 to 0.975, so one number is not evidence.
- **Name the assumption before the algorithm.** "Naive Bayes assumes
  conditional independence — which is false here, and it works anyway because
  classification only needs the right class to rank first."
- **Say when a difference is not meaningful.** Random forest scored 0.8889 to a
  single tree's 0.9778 on a 45-row iris split; the CV figures overlap almost
  entirely. The honest conclusion is that the models are not distinguishable on
  this data.
- **Explain a coefficient in odds, not log-odds.** "e^2.27 = 9.6, so one extra
  standard deviation of support calls multiplies the *odds* of churning by 9.6
  — and odds are not probability."
