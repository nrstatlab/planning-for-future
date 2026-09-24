# Unit 2 — Model Preparation, Evaluation and Feature Engineering

**Syllabus topics:** Data pre-processing; model selection and training (for
supervised learning); model representation and interpretability; evaluating
machine learning algorithms and performance enhancement of models. What is
feature engineering?; feature transformation; feature subset selection;
principal component analysis.

> **This is the most important unit in the course and the one students skip.**
> Units 3, 4 and 5 are a catalogue of algorithms, each three lines of
> scikit-learn. This unit is what makes any of them mean something.
>
> Every figure below is computed by
> `labs/course-12a-ml/` with a fixed random
> seed, so you can reproduce all of it.

---

## 2.1 Data pre-processing — the order matters

### 🎯 The big idea

**Preprocessing is a pipeline with a fixed order, and getting the order wrong
silently corrupts your evaluation.**

```
 1. Split off the test set      ← FIRST. Before anything else touches the data
 2. Handle missing values
 3. Handle outliers
 4. Encode categorical features
 5. Scale numeric features
 6. Balance classes (training set only)
```

### ⚠️ Step 1 is first, and this is the single most consequential rule in the unit

**Split before you preprocess.** If you impute means, scale, or select features
using the whole dataset, information from the test set leaks into training, and
your test score is no longer an estimate of anything.

**The concrete case:** you fill missing ages with the mean of *all* rows. That
mean was computed partly from test rows. The model has now seen a summary of
data it is supposed to be judged on, and its test score is optimistic — by a
little, or by a lot, and you cannot tell which.

**The fix is `Pipeline`**, and it is not a stylistic preference:

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

model = make_pipeline(StandardScaler(), LogisticRegression())
model.fit(X_train, y_train)      # the scaler learns from TRAIN only
model.score(X_test, y_test)      # and is merely APPLIED to test
```

Inside a pipeline, `fit_transform` runs on training data and `transform` on
test data — automatically, and inside every cross-validation fold. **Doing it
by hand across folds is where leakage actually happens in practice.**

### 🔢 Missing values

| Strategy | When | Watch for |
|---|---|---|
| **Drop rows** | Very few, and missing at random | Losing data, and biasing if they are not random |
| **Drop the column** | Mostly missing (say >50%) | The missingness itself may be informative |
| **Mean / median impute** | Numeric; median if skewed | **Shrinks the variance** and weakens correlations |
| **Mode impute** | Categorical | Over-represents the commonest value |
| **A "Missing" category** | Categorical | Often the best answer — it keeps the information |
| **Model-based (kNN, iterative)** | Enough data, missingness related to other columns | Slow, and can leak if fitted before the split |
| **Add a `was_missing` flag** | **Almost always worth it** | Costs one column and preserves the signal |

### 💡 Missingness is data

**Why a value is missing often matters more than what it was.** Income missing
on a loan form is not random — the people who decline to state it differ
systematically from those who do. Imputing the mean erases exactly the signal
you wanted.

Adding a binary `income_was_missing` column keeps it, and costs one feature.

### 🔢 Outliers

| Method | Rule | Note |
|---|---|---|
| **Z-score** | \|z\| > 3 | Assumes roughly normal; the outlier inflates σ and hides itself |
| **IQR** | Outside Q1 − 1.5·IQR or Q3 + 1.5·IQR | **Robust**, and the default in a box plot. Course 4 §4.2 |
| **Isolation Forest** | A model of anomaly | Multivariate — catches points normal on every axis but odd in combination |

**Do not delete outliers reflexively.** In fraud detection the outliers *are*
the target. Investigate first: a data error should be fixed, a genuine extreme
value should usually be kept and handled with a robust model or a log
transform.

### 🔢 Encoding categorical features

| Encoding | For | Produces |
|---|---|---|
| **One-hot** | **Nominal** | One 0/1 column per category |
| **Ordinal** | **Ordinal** | One integer column, order preserved |
| Target / mean encoding | High-cardinality nominal | The class mean per category — **leaks badly unless fitted inside CV folds** |
| Frequency encoding | High-cardinality nominal | How often each category appears |
| Binary / hashing | Very high cardinality | Fewer columns than one-hot |

**The dummy variable trap:** one-hot encoding k categories into k columns makes
them perfectly collinear (they always sum to 1). Drop one — `drop_first=True`,
or `drop="first"` — for **linear and logistic regression**. Tree models and
regularised models do not care. Course 9 Unit 4 made the same point.

### 🔢 Feature scaling

| Method | Formula | Result | Use when |
|---|---|---|---|
| **Standardisation** (Z-score) | (x − μ) / σ | Mean 0, sd 1 | **The default.** Assumes roughly normal |
| **Min–max normalisation** | (x − min) / (max − min) | Range [0, 1] | Bounded input needed; **sensitive to outliers** |
| **Robust scaling** | (x − median) / IQR | Median 0 | **Outliers present** |
| Log transform | log(1 + x) | Compresses the tail | Right-skewed data — income, counts |

### ⚠️ Which algorithms need scaling — a favourite two-mark question

| Needs scaling | Does not |
|---|---|
| **k-NN**, K-Means, DBSCAN — distance-based | **Decision trees**, random forest |
| **SVM** — the kernel is a distance | Naive Bayes |
| **PCA** — it maximises variance, and variance has units | Gradient boosting |
| Neural networks — for convergence | |
| **Regularised** linear models (Ridge, Lasso) | Plain linear regression (coefficients rescale) |

**The rule:** if the algorithm measures a distance or penalises coefficient
size, scale. If it splits on thresholds, do not bother.

**Why PCA needs it:** PCA finds directions of maximum variance. Income in
rupees has a variance millions of times larger than age in years, so
unstandardised PCA would report "the first component is income" — a fact about
your units, not your data.

---

## 2.2 Model selection and training

### 🔢 The three-way split

```
   All data (100%)
        │
        ├──────── Training set (60%)   ── fit the model
        ├──────── Validation set (20%) ── choose hyperparameters, compare models
        └──────── Test set (20%)       ── touched ONCE, at the very end
```

| Set | Used for | How often |
|---|---|---|
| **Train** | Learning parameters | Every fit |
| **Validation** | Choosing hyperparameters and comparing models | Many times |
| **Test** | The **final, honest** estimate | **Once** |

### ⚠️ Why the test set is touched once

**Every time you look at the test score and change something, you fit yourself
to the test set.** Try twenty models, pick the one with the best test score, and
that score is now the maximum of twenty noisy numbers — biased upward, and no
longer an estimate of performance on new data.

The validation set exists to absorb that. **Report the test score, and report
it after you have stopped making decisions.**

### 🔢 Cross-validation

**k-fold cross-validation** splits training data into k parts, fits k times,
and each part serves once as validation.

```
 fold 1  [ V ][ T ][ T ][ T ][ T ]
 fold 2  [ T ][ V ][ T ][ T ][ T ]
 fold 3  [ T ][ T ][ V ][ T ][ T ]
 fold 4  [ T ][ T ][ T ][ V ][ T ]
 fold 5  [ T ][ T ][ T ][ T ][ V ]
                                     score = mean of the 5
```

| Variant | Use |
|---|---|
| **k-fold** (k = 5 or 10) | The default |
| **Stratified k-fold** | **Classification** — preserves the class balance in every fold |
| Leave-one-out (k = n) | Tiny datasets; expensive, and high variance |
| **TimeSeriesSplit** | **Time-ordered data** — never shuffle time |
| GroupKFold | Repeated measurements on the same subject |

### 💡 Cross-validation reports a mean *and a spread*, and the spread is the point

On the churn data, a depth-3 tree over 5 stratified folds scores:

```
0.9750   0.9625   0.9250   0.9000   0.9500
mean 0.9425      standard deviation 0.0269
```

**A single train/test split could have reported anything from 0.90 to 0.975.**
That range is why one split is not evidence, and why you quote **mean ± sd**
rather than a single number.

### ⚠️ Never shuffle time series

With time-ordered data, a random split lets the model train on the future and
predict the past. The score will be excellent and completely meaningless. Use
`TimeSeriesSplit`, which only ever validates on data *after* the training fold.

### 🔢 Hyperparameters vs parameters

| | **Parameters** | **Hyperparameters** |
|---|---|---|
| Learned from data? | **Yes**, by fitting | **No** — you set them |
| Examples | Regression coefficients, tree split thresholds | `k` in k-NN, `max_depth`, `C`, learning rate |
| Chosen by | The optimiser | **Validation** — grid search, random search |

```python
from sklearn.model_selection import GridSearchCV
grid = GridSearchCV(DecisionTreeClassifier(random_state=42),
                    {"max_depth": [1, 2, 3, 5, 10, None]},
                    cv=5, scoring="f1")
grid.fit(X_train, y_train)
grid.best_params_        # chosen on VALIDATION folds, not on test
```

---

## 2.3 The bias–variance trade-off

### 🎯 The one picture that explains the whole unit

> **Expected error = bias² + variance + irreducible error**

| | **Bias** | **Variance** |
|---|---|---|
| Is | Error from **wrong assumptions** | Error from **sensitivity to the training sample** |
| Model is | Too simple | Too complex |
| Symptom | **Underfitting** — bad on train *and* test | **Overfitting** — great on train, bad on test |
| Example | A straight line through a curve | A tree grown until every leaf is pure |
| Fix | More features, a more flexible model | More data, regularisation, pruning, ensembling |

```
error
  │╲                                    ╱  total error
  │ ╲                                 ╱
  │  ╲___                          ╱
  │      ╲___              ______╱      variance ──►
  │          ╲____   _____╱
  │  bias ──►      ╳                    ← the sweet spot
  └──────────────────────────────────► model complexity
```

**Irreducible error** is noise in the data itself. No model removes it, and a
model claiming zero error on a noisy problem is memorising, not learning.

### 🔢 Overfitting, measured

A decision tree on the churn data, varying only `max_depth`:

| `max_depth` | Train accuracy | Test accuracy | Gap |
|---:|---:|---:|---:|
| 1 | 0.9533 | 0.9200 | +0.0333 |
| 2 | 0.9633 | 0.9300 | +0.0333 |
| 3 | 0.9800 | 0.9400 | +0.0400 |
| **5** | 0.9967 | **0.9500** | +0.0467 |
| 10 | **1.0000** | 0.9400 | +0.0600 |
| None | **1.0000** | 0.9400 | +0.0600 |

**Read the last two rows.** Training accuracy reaches a perfect 1.0000 and the
test accuracy *falls*. The tree has memorised the training set, including its
noise, and generalises worse than a depth-5 tree that never got training
perfect.

**A training accuracy of 1.0 is a warning, not an achievement.** It is the
clearest signal of overfitting there is, and it is what to point at in an exam
answer.

### 💡 The diagnosis table

| Train | Test | Diagnosis | Do |
|---|---|---|---|
| Low | Low | **Underfitting** (high bias) | More features, a more flexible model, train longer |
| **High** | **Low** | **Overfitting** (high variance) | More data, regularise, prune, simplify, ensemble |
| High | High | Good | Ship it, then monitor for drift |
| Low | High | **Something is wrong** | Usually a leak, or a test set that is not representative |

That last row is worth knowing: **test better than train is not good news**, it
is a bug.

---

## 2.4 Model representation and interpretability

### 🔢 The trade-off

| Model | Interpretability | Typical accuracy |
|---|---|---|
| **Linear / logistic regression** | **High** — read the coefficients | Moderate |
| **Decision tree** (shallow) | **High** — read the rules | Moderate |
| k-NN | Moderate — "because these neighbours" | Moderate |
| Naive Bayes | Moderate — per-feature probabilities | Moderate |
| **Random forest** | Low — hundreds of trees | **High** |
| **Gradient boosting** | Low | **Highest**, on tabular data |
| Neural network | **Very low** | Highest on images, text, audio |

### 💡 Interpretability is a requirement, not a preference

In credit, insurance, hiring and medicine, **you may be legally required to
explain a decision.** A model you cannot explain may be unusable regardless of
its accuracy — which is why a logistic regression at 0.91 sometimes beats a
boosted ensemble at 0.94.

**Tools that partly recover interpretability:**

| Tool | Gives |
|---|---|
| **Feature importance** | Which features the model relies on overall |
| **Permutation importance** | The same, measured by shuffling each feature — **more trustworthy** than tree impurity importance, which is biased toward high-cardinality features |
| Partial dependence | The average effect of one feature across its range |
| **SHAP / LIME** | Per-prediction attribution — *why this row* |
| Surrogate model | A shallow tree fitted to the black box's predictions |

---

## 2.5 Evaluating models — and why accuracy usually lies

### ⚠️ Start here: the base rate

**Accuracy alone is nearly meaningless without the base rate.**

The churn dataset is 15% positive. Fitting a `DummyClassifier` that always
predicts the majority class:

| Model | Accuracy | Recall on the positive class |
|---|---:|---:|
| **Dummy — "nobody churns"** | **0.8500** | **0.0000** |
| Logistic regression | 0.9400 | 0.7333 |

**The dummy is 85% accurate and identifies not one churner.** It is worthless,
and its accuracy is only 9 points below a real model's.

**Always fit a `DummyClassifier` first.** It costs one line, and it converts
"94% accuracy" from an impressive-sounding number into a measurable 9-point
improvement over doing nothing.

```python
from sklearn.dummy import DummyClassifier
DummyClassifier(strategy="most_frequent").fit(X_train, y_train).score(X_test, y_test)
```

In fraud detection, where positives are ~0.1%, this argument becomes overwhelming:
**"never fraud" is 99.9% accurate and catches nothing.**

### 🔢 The confusion matrix

```
                    PREDICTED
                 Positive   Negative
        Positive    TP         FN        ← actual positives
ACTUAL
        Negative    FP         TN        ← actual negatives
```

| Cell | Name | Also called |
|---|---|---|
| **TP** | True positive | Correctly caught |
| **TN** | True negative | Correctly ignored |
| **FP** | False positive | **Type I error** — a false alarm |
| **FN** | False negative | **Type II error** — a miss |

**Course 4's Type I and Type II errors are these two cells**, and the naming
carries over exactly.

### 🔢 The metrics, worked on 20 hand-countable cases

Twenty cases, six of them genuinely positive, giving **TP 4, FP 4, FN 2,
TN 10**:

| Metric | Formula | Here | Reads as |
|---|---|---:|---|
| **Accuracy** | (TP+TN)/n | (4+10)/20 = **0.7000** | How often right overall |
| **Precision** | TP/(TP+FP) | 4/8 = **0.5000** | *Of those flagged, how many were real?* |
| **Recall** (sensitivity, TPR) | TP/(TP+FN) | 4/6 = **0.6667** | *Of the real ones, how many did we catch?* |
| **Specificity** (TNR) | TN/(TN+FP) | 10/14 = **0.7143** | *Of the negatives, how many left alone?* |
| **F1** | 2PR/(P+R) | 2(0.5)(0.6667)/1.1667 = **0.5714** | Harmonic mean of P and R |

**Note that precision and recall differ here.** That is deliberate — a
confusion matrix where they come out equal teaches nothing, because the whole
reason both exist is that they can disagree.

### 💡 Which metric — decided by which error costs more

| Situation | Optimise | Because a false negative means |
|---|---|---|
| **Cancer screening** | **Recall** | A missed cancer. A false alarm costs a second test |
| **Spam filter** | **Precision** | A real email in the spam folder is worse than a spam in the inbox |
| **Fraud detection** | **Recall**, with precision watched | A missed fraud costs money; a false alarm costs a phone call |
| Balanced classes, symmetric costs | Accuracy | — |
| Imbalanced, both matter | **F1** or **AUC-PR** | — |

**F1 is the harmonic mean, not the arithmetic one**, precisely so that a model
cannot score well by maximising one and abandoning the other. Precision 1.0 and
recall 0.0 gives F1 = 0, where the arithmetic mean would give 0.5.

### 🔢 ROC, AUC, and the threshold

A classifier outputs a **probability**; the 0.5 cut-off is a *choice*, not part
of the model. The **ROC curve** plots TPR against FPR as that threshold sweeps
from 1 to 0, and **AUC** is the area under it.

| AUC | Means |
|---|---|
| 0.5 | No better than random |
| 0.7–0.8 | Acceptable |
| 0.8–0.9 | Good |
| > 0.9 | Excellent — or check for leakage |
| 1.0 | **Almost certainly a leak** |

**AUC is threshold-independent**, which is why it survives class imbalance
better than accuracy. On the churn data, logistic regression scores **AUC
0.9882** against the dummy's 0.5 — a far more informative gap than 0.94 against
0.85.

⚠️ **On severely imbalanced data prefer the precision–recall curve (AUC-PR).**
ROC's false-positive rate has a huge denominator when negatives dominate, so
ROC-AUC can look excellent while precision is terrible.

### 🔢 Regression metrics

| Metric | Formula | Units | Note |
|---|---|---|---|
| **MAE** | mean\|y − ŷ\| | y's units | **Robust** to outliers |
| **MSE** | mean(y − ŷ)² | y² | Penalises large errors heavily |
| **RMSE** | √MSE | **y's units** | The usual reporting choice |
| **R²** | 1 − SS_res/SS_tot | none | Proportion of variance explained |
| **Adjusted R²** | penalises extra predictors | none | **Use when comparing models with different p** |

⚠️ **R² never decreases when you add a predictor**, even a random one. That is
why adjusted R² exists, and why R² alone cannot compare models of different
sizes. Course 4 §4.6 made the same point.

---

## 2.6 Performance enhancement

| Technique | Attacks | How |
|---|---|---|
| **More data** | Variance | The most reliable fix, and usually unavailable |
| **Feature engineering** | Bias | Better inputs beat better algorithms |
| **Hyperparameter tuning** | Both | Grid or random search on validation folds |
| **Regularisation** | Variance | L1 (Lasso), L2 (Ridge) — Unit 3 §3.7 |
| **Pruning** | Variance | Limit `max_depth`, `min_samples_leaf` |
| **Bagging** | **Variance** | Many models on bootstrap samples → **random forest** |
| **Boosting** | **Bias** | Sequential models each fixing the last one's errors |
| **Stacking** | Both | A meta-model over several base models |
| **Class weighting / resampling** | Imbalance | `class_weight="balanced"`, SMOTE |
| **Early stopping** | Variance | Stop when validation error rises |

### 💡 Bagging and boosting — the distinction that gets asked

| | **Bagging** | **Boosting** |
|---|---|---|
| Models trained | **In parallel**, independently | **Sequentially**, each on the last's errors |
| Data per model | A **bootstrap sample** | The full set, **reweighted** |
| Reduces | **Variance** | **Bias** |
| Base learner | Deep, low-bias trees | **Shallow**, high-bias stumps |
| Overfits? | Rarely — averaging is stabilising | **Yes, if run too long** |
| Example | **Random forest** | AdaBoost, gradient boosting, XGBoost |

**Bagging averages away variance; boosting chips away at bias.** That one line
answers the five-mark question.

### ⚠️ Handling imbalance — and where to apply it

| Method | Does |
|---|---|
| **`class_weight="balanced"`** | Weights the loss by inverse class frequency. **Try this first** — one argument, no resampling |
| **Random undersampling** | Discards majority rows. Throws data away |
| **Random oversampling** | Duplicates minority rows. Risks overfitting them |
| **SMOTE** | Synthesises new minority points between neighbours |
| **Threshold tuning** | Move the 0.5 cut-off. Often the cheapest real fix |

**Resample the training folds only, never the test set.** The test set must
keep the real class distribution, or your metrics describe a world that does
not exist. Inside cross-validation, that means resampling *within* each fold —
which is another reason to use a `Pipeline`.

---

## 2.7 Feature engineering

### 🎯 The big idea

> **Better features beat better algorithms.**

Feature engineering is creating inputs that make the pattern easier for the
model to see. It is where domain knowledge enters, and it is usually worth more
than any amount of tuning.

| Technique | Example |
|---|---|
| **Domain ratios** | `debt / income` rather than both separately |
| **Date parts** | Day of week, month, is-holiday, days-since-last-purchase |
| **Aggregations** | Mean spend per customer, count of prior claims |
| **Binning** | Age → age band, when the effect is genuinely non-linear |
| **Interactions** | `price × quantity`; polynomial terms |
| **Text** | Bag of words, TF-IDF, length, punctuation counts |
| **Cyclical encoding** | Hour → (sin, cos), so 23:00 is near 00:00 |

### 💡 Cyclical encoding, because it is the neat one

Hour 23 and hour 0 are one hour apart, but numerically 23 apart. Encoding
`sin(2πh/24)` and `cos(2πh/24)` puts them next to each other on a circle, which
is what the model needs to see.

### ⚠️ Target leakage — the most damaging mistake in this course

**A feature that would not be available at prediction time, or that encodes the
answer.**

| Leaked feature | Why |
|---|---|
| `total_amount_paid` predicting default | Only known *after* the outcome |
| `discharge_date` predicting length of stay | It is the answer |
| A row id correlated with the label | Sorted data leaks through the index |
| Mean-encoding fitted before the split | Test labels entered the training features |

**The symptom is a suspiciously excellent score** — 0.99 accuracy, AUC 1.0. If
a result looks too good, look for the leak before celebrating. It is almost
always there.

**The test:** *would I know this value at the moment I need the prediction?* If
not, drop it.

---

## 2.8 Feature transformation

### 🎯 Transformation and selection are different operations

The syllabus lists **feature transformation** and **feature subset selection**
as separate topics, and they genuinely are:

| | **Transformation** | **Selection** |
|---|---|---|
| Does | **Changes** the features — rescales, combines, derives | **Discards** features |
| Output | New or altered columns | A **subset** of the originals |
| Count of features | May go up, down or stay | Always **down** |
| Original features needed at prediction time | **Yes** | **No** |
| Examples | Scaling, log, Box–Cox, one-hot, **PCA** | Filter, wrapper, embedded |

**PCA is a transformation, not a selection** — §2.10 makes the point again,
because it is the distinction most often got wrong.

### 🔢 The kinds of transformation

| Kind | Operation | Why |
|---|---|---|
| **Scaling** | Standardise, min–max, robust | §2.1 — distance and penalty methods need it |
| **Non-linear** | log(1+x), √x, **Box–Cox**, Yeo–Johnson | Compress a right-skewed tail; make a multiplicative relationship additive |
| **Discretisation** | Continuous → bins | When the effect is genuinely stepped (age bands, income brackets) |
| **Encoding** | One-hot, ordinal, target | §2.1 — categories into numbers |
| **Construction** | Ratios, differences, interactions, date parts | §2.7 — where domain knowledge enters |
| **Extraction** | **PCA**, LDA, autoencoders | Many correlated features → few uncorrelated ones |

### 💡 The log transform, and why it is the one to know

Income, prices, counts and durations are almost always **right-skewed** — a
long tail of large values. A linear model fitted to raw income is dominated by
the tail; fitted to `log(income)` it is not.

Two extra reasons worth stating:

1. **It turns a multiplicative relationship into an additive one.** If
   y = a·x₁·x₂ then log y = log a + log x₁ + log x₂, which is exactly the shape
   linear regression can fit.
2. **A coefficient on a logged predictor reads as a percentage.** A coefficient
   of 0.05 on `log(x)` means roughly "a 1% rise in x is associated with a 0.05%
   rise in y" — often more meaningful than the raw units.

⚠️ Use **`log1p`** (log of 1+x), not `log`, whenever zeros are possible.
`log(0)` is −∞ and will silently poison the column.

### ⚠️ Transformations are fitted, so they leak

A log is a fixed function and is safe anywhere. **Anything that learns a
parameter from the data — the mean and standard deviation for standardising,
the min and max for min–max, the Box–Cox λ, the PCA components — must be fitted
on the training set only.** That is §2.1's rule, and it is why every one of
them belongs inside a `Pipeline`.

## 2.9 Feature subset selection

### 🎯 Why fewer features can be better

Fewer features means less overfitting, faster training, easier explanation, and
cheaper data collection. The curse of dimensionality (Unit 1 §1.7) makes it
necessary rather than merely tidy.

### 🔢 The three families

| Family | How | Examples | Cost | Uses the model? |
|---|---|---|---|---|
| **Filter** | Score each feature against the target, independently of any model | Correlation, chi-square, mutual information, variance threshold | **Cheap** | No |
| **Wrapper** | Search subsets, training a model on each | Forward selection, backward elimination, **RFE** | **Expensive** | Yes |
| **Embedded** | Selection happens *during* fitting | **Lasso (L1)**, tree feature importance | Moderate | Built in |

| | Filter | Wrapper | Embedded |
|---|---|---|---|
| Speed | Fast | Slow | Medium |
| Considers feature **interactions** | **No** | **Yes** | Partly |
| Overfitting risk | Low | **High** — select inside CV folds | Low |
| Model-specific | No | Yes | Yes |

### ⚠️ Filter methods miss interactions

Two features individually uncorrelated with the target can be strongly
predictive together — the classic case being XOR, where each feature alone
carries zero information. A filter drops both. **A wrapper or an embedded
method finds them**, and knowing this distinction is the five-mark answer.

### ⚠️ Selection must happen inside cross-validation

Selecting features on the whole dataset and *then* cross-validating is leakage,
and it produces optimistic scores that will not survive contact with new data.
Put the selector in a `Pipeline` so it is refitted inside every fold.

---

## 2.10 Principal Component Analysis

### 🎯 The big idea

**PCA finds new axes — linear combinations of the original features — ordered
by how much variance they capture, and lets you keep only the first few.**

It is **unsupervised**: it never looks at the target. It reduces dimensions by
discarding directions along which the data barely varies.

### 🔢 The algorithm

1. **Standardise** the features. *(Not optional — see below.)*
2. Compute the **covariance (or correlation) matrix**.
3. Compute its **eigenvalues and eigenvectors**.
4. Sort eigenvectors by eigenvalue, descending. These are the **principal
   components**.
5. Keep the first k. **Project** the data onto them.

- The **eigenvectors** are the directions (the components).
- The **eigenvalues** are the variance captured along each.
- **Explained variance ratio** = eigenvalue ÷ sum of eigenvalues.

### 🔢 Worked on iris — asserted in the lab

Four standardised features. The eigenvalues of the correlation matrix, and the
share of variance each explains:

| Component | Eigenvalue | Explained variance | Cumulative |
|---|---:|---:|---:|
| **PC1** | 2.9185 | **72.96%** | 72.96% |
| **PC2** | 0.9140 | **22.85%** | **95.81%** |
| PC3 | 0.1468 | 3.67% | 99.48% |
| PC4 | 0.0207 | 0.52% | 100.00% |

**The eigenvalues sum to exactly 4** — the number of standardised features,
each contributing variance 1. That is a free arithmetic check on your working.

**Two components carry 95.81% of the variance**, so iris can be drawn on a flat
page losing 4.19% of its information. That is the result to quote.

> *(scikit-learn's `explained_variance_` prints 2.9381, 0.9202, 0.1477, 0.0209
> — slightly larger, because it divides by n−1 while standardisation divided by
> n. The **ratios are identical**, which is why the ratio is what you report.)*

### 🔢 How many components to keep

| Rule | Says | On iris |
|---|---|---|
| **Cumulative variance ≥ 90–95%** | Keep enough to reach the threshold | **2 components** (95.81%) |
| **Kaiser criterion** — eigenvalue > 1 | Keep components explaining more than one original feature would | **1 component** |
| **Scree plot elbow** | Keep up to the bend | 2 |
| Downstream performance | Tune k like any hyperparameter | — |

⚠️ **The rules disagree here — Kaiser says 1, the variance rule says 2** — and
that is normal. Kaiser is known to under-select on small p. Quote the rule you
used and say why; the honest answer is that k is a hyperparameter and should be
validated.

### ⚠️ PCA's four limitations

1. **Components are not interpretable.** PC1 is 0.52×sepal length − 0.26×sepal
   width + 0.58×petal length + 0.56×petal width. That is not a thing anyone can
   name, and it is why PCA is a poor choice when you must explain the model.
2. **It is unsupervised.** It maximises *variance*, not *class separation* — so
   a direction with little variance but perfect separating power gets discarded.
   **LDA** is the supervised alternative when separation is the goal.
3. **It assumes linearity.** Data on a curved manifold needs kernel PCA, t-SNE
   or UMAP.
4. **It requires standardisation.** Without it, PCA reports whichever feature
   has the largest units.

### 💡 PCA vs feature selection

| | **PCA** | **Feature selection** |
|---|---|---|
| Output | **New** features (combinations) | A **subset** of the originals |
| Interpretability | **Lost** | **Kept** |
| Uses the target | No | Usually yes |
| Original features still needed at prediction time | **Yes — all of them** | **No** |

**That last row decides real projects.** PCA does not save you from collecting
any data — every original feature is still needed to compute the components.
If the goal is to stop measuring something expensive, you need *selection*, not
PCA.

---

## Practice problems

### Problem 1

Why is accuracy an inadequate metric? Explain the confusion matrix and derive
precision, recall and F1 with an example. *(10 marks)*

**Solution.**

**Open with the base rate argument and a number.** On a dataset that is 15%
positive, a `DummyClassifier` predicting the majority class scores **0.8500
accuracy and 0.0000 recall** — it is 85% accurate and identifies not one
positive case. In fraud detection, where positives are ~0.1%, "never fraud" is
**99.9% accurate and catches nothing**.

Draw the confusion matrix and name all four cells, noting that **FP is Course
4's Type I error and FN is Type II**.

**Then derive the metrics on countable numbers** — 20 cases, 6 positive, giving
TP 4, FP 4, FN 2, TN 10:

| Metric | Formula | Value |
|---|---|---:|
| Accuracy | (4+10)/20 | 0.7000 |
| Precision | 4/(4+4) | **0.5000** |
| Recall | 4/(4+2) | **0.6667** |
| Specificity | 10/(10+4) | 0.7143 |
| F1 | 2(0.5)(0.6667)/(0.5+0.6667) | **0.5714** |

Explain each in words — *of those flagged, how many were real* (precision)
versus *of the real ones, how many did we catch* (recall).

**Then the choice of metric**, which is the last three marks: cancer screening
optimises **recall** because a miss is fatal; a spam filter optimises
**precision** because a real email lost to the spam folder is worse than spam
in the inbox. Note that **F1 is the harmonic mean** precisely so a model cannot
win by maximising one and abandoning the other — precision 1.0 with recall 0.0
gives F1 = 0, not 0.5.

Finish with **AUC**, which is threshold-independent and therefore survives
imbalance better — 0.9882 against the dummy's 0.5 on the worked data — and the
warning that on severely imbalanced data the **precision–recall curve** is more
informative than ROC.

### Problem 2

Explain the bias–variance trade-off. How would you detect and fix overfitting?
*(10 marks)*

**Solution.**

Give the decomposition — **expected error = bias² + variance + irreducible
error** — and define each: bias is error from wrong assumptions (too simple),
variance is sensitivity to the particular training sample (too complex),
irreducible error is noise no model removes.

Draw the U-shaped curve: bias falls and variance rises with complexity, and
total error is minimised between them.

**Detect it with the diagnosis table:**

| Train | Test | Diagnosis |
|---|---|---|
| Low | Low | Underfitting |
| **High** | **Low** | **Overfitting** |
| High | High | Good |
| Low | High | A bug — usually leakage |

**Then the measured example**, which is what earns the top marks. A decision
tree on the same data, varying only `max_depth`:

| depth | train | test |
|---:|---:|---:|
| 5 | 0.9967 | **0.9500** |
| 10 | **1.0000** | 0.9400 |
| None | **1.0000** | 0.9400 |

Training accuracy reaches a perfect 1.0000 while test accuracy *falls*.
**A training accuracy of 1.0 is a warning, not an achievement.**

**Fixes:** more data; regularisation (L1/L2); pruning (`max_depth`,
`min_samples_leaf`); ensembling — bagging averages variance away; early
stopping; and simplifying the feature set. Add that **cross-validation is how
you detect it reliably**, because a single split on this data varies from 0.90
to 0.975.

### Problem 3

What is PCA? Explain the algorithm, and interpret it on a worked example.
*(10 marks)*

**Solution.**

**Definition:** an unsupervised technique that finds new axes — linear
combinations of the original features — ordered by the variance they capture,
allowing the first few to replace all of them.

**The algorithm in five steps:** standardise; compute the covariance or
correlation matrix; find its eigenvalues and eigenvectors; sort by eigenvalue
descending; project onto the top k. State that **eigenvectors are the
directions and eigenvalues are the variance along them**, and that the
explained variance ratio is eigenvalue ÷ total.

**The worked result on iris** (four standardised features):

| Component | Eigenvalue | Explained | Cumulative |
|---|---:|---:|---:|
| PC1 | 2.9185 | 72.96% | 72.96% |
| PC2 | 0.9140 | 22.85% | **95.81%** |
| PC3 | 0.1468 | 3.67% | 99.48% |
| PC4 | 0.0207 | 0.52% | 100.00% |

**Two components carry 95.81%**, so four dimensions become two, losing 4.19%.
Note the eigenvalues sum to exactly **4** — the number of standardised features
— which is a free check on the arithmetic.

**How many to keep:** the 95% rule says 2, **Kaiser (eigenvalue > 1) says 1**,
and they disagree — which is normal, and the honest answer is that k is a
hyperparameter to validate.

**Then the limitations, which is where answers thin out:** components are not
interpretable; it is unsupervised so it maximises variance rather than class
separation (**LDA** is the supervised alternative); it assumes linearity; and
it requires standardisation, or it simply reports whichever feature has the
largest units.

Close with the distinction from feature selection: **PCA still needs every
original feature at prediction time.** If the aim is to stop collecting an
expensive measurement, you need selection, not PCA.

### Problem 4

Explain data leakage with examples, and how to prevent it. *(5 marks)*

**Solution.**

**Definition:** leakage is information from outside the training data — usually
from the test set or from the future — reaching the model, producing a score
that cannot be reproduced in production.

**Three kinds, with an example each:**

1. **Target leakage** — a feature that would not exist at prediction time.
   `total_amount_paid` predicting loan default is only known after the outcome;
   `discharge_date` predicting length of stay *is* the answer.
2. **Train–test contamination** — preprocessing fitted on the whole dataset.
   Imputing with the overall mean, or scaling before splitting, puts a summary
   of the test data into training.
3. **Temporal leakage** — shuffling time-ordered data, so the model trains on
   the future.

**Prevention:** split first, before anything touches the data; put every
transformer in a `Pipeline` so `fit` sees only training folds; use
`TimeSeriesSplit` for time-ordered data; and for each feature ask *would I know
this at the moment I need the prediction?*

**The symptom:** a suspiciously excellent score. AUC 1.0 is nearly always a
leak, not a triumph.

---

## Exam questions from this unit

**Two marks**

1. Why must the test set be split off before preprocessing?
2. Give the formula for precision and for recall.
3. What is the difference between a parameter and a hyperparameter?
4. Which algorithms require feature scaling?
5. What does AUC = 0.5 mean?
6. What is the dummy variable trap?
7. Why does R² never decrease when a predictor is added?

**Five marks**

1. Explain the data preprocessing pipeline and why order matters.
2. Explain cross-validation and its variants.
3. Distinguish bagging from boosting.
4. Explain the three families of feature selection.
5. Explain data leakage with examples.
6. How would you handle class imbalance?

**Ten marks**

1. Why is accuracy inadequate? Explain the confusion matrix and derive
   precision, recall and F1.
2. Explain the bias–variance trade-off, and how to detect and fix overfitting.
3. Explain PCA with a worked example and its limitations.
4. Explain feature engineering and feature selection, with examples of each.

---

## Mistakes that cost marks

- **Preprocessing before splitting.** The test score stops meaning anything.
- **Reporting accuracy on imbalanced data with no base rate.** 85% can be zero
  recall.
- **Tuning on the test set.** That is what the validation set is for.
- **Calling F1 the average of precision and recall.** It is the **harmonic**
  mean, and the difference is the whole point.
- **Saying PCA selects features.** It **creates** new ones, and you still need
  every original at prediction time.
- **Running PCA without standardising.** It then reports your units.
- **Claiming training accuracy of 1.0 is a good result.** It is the clearest
  symptom of overfitting.
- **Shuffling a time series.** The model trains on the future.
- **Not mentioning a baseline.** "94% accuracy" means nothing until you say the
  dummy scored 85%.
- **Scaling a decision tree's inputs "to be safe".** Harmless, but it shows you
  do not know why scaling exists.
