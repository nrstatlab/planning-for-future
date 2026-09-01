# Course 12 A — Practice Questions with Worked Solutions

Every figure quoted here is produced by
`labs/course-12a-ml/` and checked by
`tools/run_ml_labs.py`.

---

## Section A — Two-mark questions

**1. State Mitchell's definition of machine learning.**
A program learns from experience **E** with respect to tasks **T** and
performance measure **P** if its performance at T, as measured by P, improves
with E.

**2. Give one difference between classification and regression.**
Classification predicts a **category**; regression predicts a **number**.

**3. Is logistic regression a regression or a classification method?**
**Classification.** It is a *linear model fitted like* a regression, which is
where the name comes from.

**4. What shape does scikit-learn expect `X` to be?**
**2-D**, n × p. `y` is 1-D. A single feature still needs double brackets:
`df[["hours"]]`.

**5. Why must the test set be split off before preprocessing?**
Otherwise the transformer learns from test rows, and the test score stops being
an estimate of performance on unseen data.

**6. Give the formula for precision and for recall.**
Precision = TP/(TP+FP). Recall = TP/(TP+FN).

**7. What does AUC = 0.5 mean?**
No better than random.

**8. What is the difference between a parameter and a hyperparameter?**
Parameters are **learned by fitting**; hyperparameters are **set by you** and
chosen on validation folds.

**9. Which algorithms require feature scaling?**
Anything measuring a **distance** or penalising **coefficient size** — k-NN,
K-Means, DBSCAN, SVM, PCA, Ridge/Lasso, neural networks. Trees and Naive Bayes
do not.

**10. What is the dummy variable trap?**
One-hot encoding k categories into k columns makes them sum to 1 and therefore
collinear with the intercept. Drop one for linear and logistic regression.

**11. Why does R² never decrease when a predictor is added?**
Least squares can always set the new coefficient to zero, so the fit can only
improve or stay the same. Use adjusted R² to compare models of different sizes.

**12. What does "naive" mean in Naive Bayes?**
Every feature is assumed **conditionally independent** of every other, given
the class.

**13. What is Laplace smoothing for?**
The **zero-frequency problem** — one unseen feature value gives a probability of
0, and since the likelihood is a **product**, that zeroes the whole posterior.

**14. Why is k-NN called a lazy learner?**
Fitting only stores the data; all computation happens at prediction time.

**15. What is a support vector?**
A training point lying on the margin. **They alone define the hyperplane** —
remove any other point and the solution is unchanged.

**16. What does C control in an SVM?**
The penalty for margin violations. **Large C = narrow margin, less
regularised, higher variance.** It runs in the opposite direction to `alpha`.

**17. What fraction of rows is out of bag, and why?**
About **36.8%**. The chance of never drawing a row in n draws with replacement
is (1 − 1/n)ⁿ → 1/e ≈ 0.368.

**18. Why does K-Means always converge?**
WCSS never increases across iterations — but it converges to a **local**
minimum.

**19. What does a negative silhouette value mean?**
The point is **closer to a neighbouring cluster than to its own** — it is in the
wrong cluster.

**20. Why is ARI preferred to the Rand Index?**
ARI is **corrected for chance**, so a random clustering scores 0. The
unadjusted index gives random clusterings a score well above zero.

---

## Section B — Five-mark questions

### 1. Compare machine learning with traditional programming

**Solution.** Draw the contrast:

```
TRADITIONAL PROGRAMMING              MACHINE LEARNING
   data ──┐                             data ──┐
          ├──► program ──► output              ├──► algorithm ──► MODEL
  rules ──┘                         answers ──┘                     │
                                                  new data ──► prediction
```

| | Traditional | Machine learning |
|---|---|---|
| You write | The **rules** | The objective, plus examples |
| Computer produces | The output | **The rules** |
| Input | Data + rules | Data + **answers** |
| Good for | Rules you can state | Rules you **cannot** state |
| When data changes | Rewrite the code | **Retrain** |
| Debug by reading | Yes | Not really |

Add **when not to use it**: known stable rules, very little data, decisions that
must be explained, or a simple baseline that already suffices.

### 2. Explain cross-validation and its variants

**Solution.** k-fold splits the training data into k parts; each part serves
once as validation while the rest train. The score is the mean of the k runs.

| Variant | Use |
|---|---|
| **k-fold** (5 or 10) | The default |
| **Stratified** | **Classification** — preserves class balance in each fold |
| Leave-one-out | Tiny datasets; expensive, high variance |
| **TimeSeriesSplit** | **Time-ordered data** — never shuffle time |
| GroupKFold | Repeated measurements on one subject |

**Why it matters, with the number:** a depth-3 tree over 5 stratified folds
scores `[0.975, 0.9625, 0.925, 0.900, 0.950]` — **mean 0.9425, sd 0.0269**. A
single split could have reported anything from 0.90 to 0.975, which is why you
quote **mean ± sd** and not one number.

### 3. Distinguish bagging from boosting

**Solution.**

| | **Bagging** | **Boosting** |
|---|---|---|
| Models trained | **In parallel**, independently | **Sequentially**, each on the last's errors |
| Data per model | A **bootstrap sample** | The full set, **reweighted** |
| Reduces | **Variance** | **Bias** |
| Base learner | Deep, low-bias trees | **Shallow**, high-bias stumps |
| Overfits? | Rarely | **Yes, if run too long** |
| Example | **Random forest** | AdaBoost, gradient boosting, XGBoost |

**One line: bagging averages away variance; boosting chips away at bias.**

### 4. Explain the three families of feature selection

**Solution.**

| Family | How | Examples | Interactions? |
|---|---|---|---|
| **Filter** | Score each feature against the target, model-free | Correlation, chi-square, mutual information | **No** |
| **Wrapper** | Search subsets, training a model on each | Forward, backward, **RFE** | **Yes** |
| **Embedded** | Selection happens during fitting | **Lasso**, tree importance | Partly |

**The distinction that earns the mark:** filters **miss interactions**. Two
features individually uncorrelated with the target can be jointly predictive —
XOR is the classic case, where each alone carries zero information. A filter
drops both.

Add that **selection must happen inside cross-validation folds**, or it leaks.

### 5. Explain data leakage with examples and how to prevent it

**Solution.** Leakage is information from outside the training data reaching
the model, producing a score that cannot be reproduced in production.

1. **Target leakage** — a feature unavailable at prediction time.
   `total_amount_paid` predicting default; `discharge_date` predicting length of
   stay.
2. **Train–test contamination** — imputing or scaling before splitting.
3. **Temporal leakage** — shuffling time-ordered data so the model trains on
   the future.

**Prevention:** split first; put every transformer in a `Pipeline`;
`TimeSeriesSplit` for time data; and for each feature ask *would I know this at
the moment I need the prediction?*

**The symptom is a suspiciously excellent score.** AUC 1.0 is nearly always a
leak.

### 6. How would you handle class imbalance?

**Solution.** First **measure the base rate**, because it decides everything: on
15%-positive data a `DummyClassifier` scores **0.8500 accuracy and 0.0000
recall**.

| Method | Does |
|---|---|
| **`class_weight="balanced"`** | Weights the loss by inverse frequency. **Try first** |
| Random undersampling | Discards majority rows |
| Random oversampling | Duplicates minority rows; risks overfitting them |
| **SMOTE** | Synthesises new minority points between neighbours |
| **Threshold tuning** | Move the 0.5 cut-off — often the cheapest real fix |

**Resample the training folds only, never the test set** — the test set must
keep the real distribution.

**Change the metric too:** precision, recall, F1 or AUC-PR, not accuracy.

---

## Section C — Ten-mark questions

### 1. Why is accuracy inadequate? Explain the confusion matrix and derive precision, recall and F1

**Solution.**

**Open with the base rate and a number.** On 15%-positive data, a
`DummyClassifier` predicting the majority class scores **accuracy 0.8500 and
recall 0.0000** — 85% accurate, and it identifies not one positive case. In
fraud detection, where positives are ~0.1%, "never fraud" is **99.9% accurate
and catches nothing**.

**The confusion matrix**, naming all four cells, and noting **FP is Course 4's
Type I error and FN is Type II**:

```
                    PREDICTED
                 Positive   Negative
        Positive    TP         FN
ACTUAL
        Negative    FP         TN
```

**Derive the metrics** on 20 countable cases — 6 positive, giving TP 4, FP 4,
FN 2, TN 10:

| Metric | Formula | Value |
|---|---|---:|
| Accuracy | (4+10)/20 | 0.7000 |
| Precision | 4/8 | **0.5000** |
| Recall | 4/6 | **0.6667** |
| Specificity | 10/14 | 0.7143 |
| F1 | 2(0.5)(0.6667)/1.1667 | **0.5714** |

Explain each in words: *of those flagged, how many were real* versus *of the
real ones, how many did we catch*.

**Choose the metric by which error costs more:** cancer screening optimises
**recall** (a miss is fatal); a spam filter optimises **precision** (a real
email lost is worse than spam let through).

**F1 is the harmonic mean**, precisely so a model cannot win by maximising one
and abandoning the other — precision 1.0 with recall 0.0 gives F1 = **0**, not
0.5.

**Finish with AUC.** It is threshold-independent and so survives imbalance
better: on the worked data, **0.9882 against the dummy's 0.5**, where accuracy
compressed the same difference into 9 points. On severely imbalanced data
prefer the **precision–recall curve**.

### 2. Explain the bias–variance trade-off; how would you detect and fix overfitting?

**Solution.**

**Expected error = bias² + variance + irreducible error.** Bias is error from
wrong assumptions (too simple); variance is sensitivity to the particular
training sample (too complex); irreducible error is noise no model removes.

Draw the U-shaped curve — bias falls and variance rises with complexity.

**Detect it:**

| Train | Test | Diagnosis |
|---|---|---|
| Low | Low | Underfitting |
| **High** | **Low** | **Overfitting** |
| High | High | Good |
| Low | High | A bug — usually leakage |

**Then the measured example**, which earns the top marks. A decision tree,
varying only `max_depth`:

| depth | train | test |
|---:|---:|---:|
| 3 | 0.9800 | 0.9400 |
| **5** | 0.9967 | **0.9500** |
| 10 | **1.0000** | 0.9400 |
| None | **1.0000** | 0.9400 |

**Training accuracy reaches a perfect 1.0000 while test accuracy falls.** A
training accuracy of 1.0 is a warning, not an achievement.

**Fixes:** more data; regularisation (L1/L2); pruning; ensembling — bagging
averages variance away; early stopping; fewer features. And **cross-validation
is how you detect it reliably**, because on this data a single split ranges
from 0.90 to 0.975.

### 3. Explain PCA with a worked example and its limitations

**Solution.**

**Definition:** an **unsupervised** technique finding new axes — linear
combinations of the original features — ordered by the variance they capture.

**The algorithm:** standardise; compute the covariance/correlation matrix; find
its eigenvalues and eigenvectors; sort by eigenvalue descending; project onto
the top k. **Eigenvectors are the directions, eigenvalues the variance along
them**, and the explained variance ratio is eigenvalue ÷ total.

**Worked on iris:**

| Component | Eigenvalue | Explained | Cumulative |
|---|---:|---:|---:|
| PC1 | 2.9185 | 72.96% | 72.96% |
| PC2 | 0.9140 | 22.85% | **95.81%** |
| PC3 | 0.1468 | 3.67% | 99.48% |
| PC4 | 0.0207 | 0.52% | 100.00% |

**The eigenvalues sum to exactly 4 = p** — a free check on your arithmetic.
Two components carry **95.81%**, so four dimensions become two losing 4.19%.

**And that 4.19% is literal:** the reconstruction MSE at k=2 is **0.0419**,
exactly 1 minus the variance kept.

**How many to keep:** the 95% rule says 2; **Kaiser (eigenvalue > 1) says 1**.
They disagree, which is normal — Kaiser under-selects when p is small.

**The four limitations:**

1. **Components are uninterpretable.** PC1 is a weighted blend of all four
   measurements and has no name.
2. **It is unsupervised** — it maximises variance, not separation. On two
   dimensions **LDA scores 0.9800 against PCA's 0.9133**.
3. **It assumes linearity.** Curved manifolds need kernel PCA, t-SNE or UMAP.
4. **It requires standardising.** Rescale one iris column to micrometres and
   **PC1 explains 100.0000%** — a fact about your units, not your data.

**Close with the distinction from feature selection:** PCA creates new features
and **still needs every original at prediction time**. If the aim is to stop
collecting an expensive measurement, you need *selection*, not PCA.

### 4. Explain logistic regression and why linear regression cannot classify

**Solution.**

**State first that logistic regression is a classifier**, despite its name.

**Why linear regression fails:** fitted to a 0/1 target it predicts −0.3 and
1.4, which are not probabilities, and it is unbounded.

**The sigmoid:** p = 1/(1 + e^−z), z = β₀ + β₁x₁ + …, bounded in (0, 1) with
p = 0.5 exactly at z = 0. Sketch it.

**The interpretation, which carries the marks:** odds = p/(1−p);
logit = ln(odds) = z, so **the model is linear in the log-odds**. β is the
change in log-odds per unit, and **e^β is the odds ratio**.

**With the worked figure:** `support_calls` has coefficient **2.2656**, so
e^2.2656 = **9.6367** — one extra standard deviation of calls multiplies the
**odds** of churning by 9.64. **Odds are not probability**: odds of 2.0 means
p = 2/3.

**Fitted by maximum likelihood**, not least squares, with no closed form.

**The threshold is a choice.** Show the table:

| threshold | precision | recall |
|---:|---:|---:|
| 0.10 | 0.7143 | **1.0000** |
| 0.50 | 0.8462 | 0.7333 |
| 0.90 | **1.0000** | 0.2667 |

**One model, three different classifiers.** Choose the cut-off from the cost of
each error.

Finish with multi-class: one-vs-rest, or multinomial softmax.

### 5. Explain Naive Bayes, the naive assumption and the zero-frequency problem

**Solution.**

**Bayes' theorem:** P(C|X) = P(X|C)P(C)/P(X), naming posterior, likelihood,
prior and evidence — and noting the evidence is the same across classes, so it
is dropped for comparison.

**"Naive" is the conditional independence assumption:**
P(x₁,…,xₚ|C) = ∏P(xᵢ|C).

**Say plainly that it is false**, and show it: iris feature correlations reach
**0.9629**, with three pairs above 0.8 — and GaussianNB still scores **0.9533**
CV accuracy. **Classification needs only the correct class to rank highest**,
not the probabilities to be right.

**Worked posteriors:** P(Yes) × likelihoods = **0.005291**, P(No) × likelihoods
= **0.020571**, normalising to **79.54% No**.

**The zero-frequency problem:** one unseen feature value gives P(xᵢ|C) = 0, and
because the likelihood is a **product**, that single zero drives the posterior
to **0.000000** regardless of how strongly the other features support the class.

**Laplace smoothing** — P(xᵢ|C) = (count + α)/(total + α·k), with α = 1 —
restores it to **0.001443**.

**The variants:** Gaussian (continuous), **Multinomial** (counts — text),
Bernoulli (binary). And **why it owns spam filtering**: linear in the number of
features, one training pass, little data needed, updates incrementally.

### 6. Compare K-Means, hierarchical clustering and DBSCAN

**Solution.**

| | **K-Means** | **DBSCAN** | **Hierarchical** |
|---|---|---|---|
| k in advance | **Yes** | **No** | No — cut the dendrogram |
| Cluster shape | **Convex only** | **Arbitrary** | Depends on linkage |
| Outliers | Forced into a cluster | **Labelled noise** | Forced in |
| Varying density | Fine | **Struggles** | Fine |
| Complexity | O(nkt) — **fast** | O(n log n) | O(n²)–O(n³) |
| Deterministic | No | **Yes**, except border points | Yes |

**The measured demonstration.** Two interleaved crescents:

| Algorithm | ARI |
|---|---:|
| K-Means (k=2) | **0.2475** |
| DBSCAN | **1.0000** |

**And it is not a tuning problem** — the best K-Means manages over k = 2…10 is
**0.2938**. K-Means assigns each point to the nearest centroid, so its
boundaries are straight perpendicular bisectors; **no k carves out a crescent**.

**Then DBSCAN's own weakness, honestly.** A dense blob and a sparse one, 3 units
apart: eps = 0.30 discards the sparse blob as **60 noise points**; eps = 1.50
**merges them** (ARI 0.0178). No single eps recovers both, and **K-Means scores
0.8335** here because both blobs are convex.

**Neither algorithm is better in general** — that is the answer to give.

### 7. How do you evaluate a clustering when there are no labels?

**Solution.**

**The difficulty first:** with no labels there is no accuracy, and **a
clustering algorithm always returns clusters** — ask K-Means for four groups in
pure noise and it gives four, with centroids and a tidy plot.

**Internal metrics** (geometry only): **silhouette** ((b−a)/max(a,b); near +1
good, negative means wrong cluster), Davies–Bouldin (low), Calinski–Harabasz
(high), and WCSS, which always falls with k and so needs the elbow.

**External metrics** (labels, for validation only): **ARI**, corrected for
chance; NMI; homogeneity and completeness.

**Then the two measured demonstrations that internal metrics are not
correctness:**

1. On iris, silhouette prefers **k = 2 (0.5818)** over k = 3 (0.4599) — but
   there are **three** species, and k=3's ARI (0.6201) is the higher. Setosa is
   cleanly separate; versicolor and virginica overlap.
2. **Ward linkage agrees best with the truth (ARI 0.6153) and has the worst
   silhouette (0.4467)**; single linkage is the reverse.

**Conclude honestly:** no metric establishes correctness, because correctness is
undefined without a purpose. The real tests are whether the clusters are
**actionable**, **stable in new data**, and **nameable by a domain expert**.

### 8. Explain random forest, its two sources of randomness, and out-of-bag error

**Solution.**

**The algorithm:** many decision trees, each on a bootstrap sample, each
choosing splits from a **random subset of features**; majority vote.

**The two sources of randomness:**

1. **Bootstrap sampling** — n rows drawn with replacement, so each tree sees
   about **63.2%** of the distinct rows.
2. **Random feature subsets at every split** — √p features for classification.

**Why the second matters, and it is the half most answers omit:** with one
strongly predictive feature, every bagged tree splits on it first and all the
trees look alike. **Averaging near-identical trees reduces nothing.** Forcing
each split to consider only a subset **decorrelates** them, and the
decorrelation is what makes averaging work.

**Out-of-bag error:** each sample omits about **36.8%** of rows — because
(1 − 1/n)ⁿ → 1/e ≈ 0.368. Predicting each row using only the trees that did not
see it gives an unbiased estimate **for free**.

**Then the caution that shows judgement.** On iris a 100-tree forest scored
**0.8889** on the test split against **0.9778** for a single depth-3 tree — a
small clean dataset gives an ensemble nothing to fix, and a 45-row test set is
noise. The CV figures (0.9467 ± 0.0267 against 0.9600 ± 0.0249) **overlap
almost entirely**, so the honest conclusion is that the models are not
distinguishable here.

---

## The six things most likely to be examined

1. **Accuracy is inadequate — the confusion matrix, precision, recall, F1.**
   Lead with a base rate: 85% accuracy, 0% recall.
2. **Bias–variance and overfitting**, with the `max_depth` table where training
   accuracy hits 1.0000 and test accuracy falls.
3. **PCA** — the algorithm, the worked eigenvalues, and the four limitations.
4. **Logistic regression** — the sigmoid, the odds ratio, and that it
   classifies.
5. **Naive Bayes** — the naive assumption (false, and it works anyway) and the
   zero-frequency problem.
6. **Clustering comparison** — K-Means against DBSCAN on non-convex data, and
   how you evaluate without labels.
