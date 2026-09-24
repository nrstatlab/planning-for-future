# Unit 4 — Applications and Case Studies in Data Science

**Syllabus topics:** Simple linear regression. Multiple regression. Model
evaluation method — accuracy, confusion matrix, ROC. K-Means clustering. Text
mining and word clouds. Recommender systems basics. Ethical issues in data
science.

---

This unit is where Course 4's statistics becomes machine learning. Regression,
you already know — Unit 4 of Statistical Foundations. What is new is
**evaluating** a model honestly, which is the part that separates a useful
result from a misleading one.

## 4.1 Simple linear regression in R

You derived this in Course 4. Here is how R does it in one line.

```r
model <- lm(marks ~ hours, data = students)
summary(model)
```

`marks ~ hours` is a **formula**: read `~` as "is modelled by". The response
goes on the left, the predictors on the right.

### Reading `summary()` output

```
Coefficients:
            Estimate Std. Error t value Pr(>|t|)
(Intercept)  43.0303     1.0847  39.671  1.8e-10 ***
hours         4.3030     0.0987  43.615  8.4e-11 ***

Residual standard error: 0.896 on 8 degrees of freedom
Multiple R-squared: 0.9958,  Adjusted R-squared: 0.9953
F-statistic: 1902 on 1 and 8 DF,  p-value: 8.425e-11
```

| Line | Meaning | Course 4 reference |
|---|---|---|
| `(Intercept) Estimate` | b₀ | §4.5 |
| `hours Estimate` | b₁, the slope | §4.5 |
| `Std. Error` | SE(b₁) | §4.6 |
| `t value` | b₁ / SE(b₁) | §4.6 |
| `Pr(>\|t\|)` | p-value for H₀: β₁ = 0 | §4.6 |
| `Multiple R-squared` | proportion of variance explained | §4.6 |
| `F-statistic` | overall model significance | §4.6 |

**Those are exactly the numbers you computed by hand in Course 4** — the same
worked example, in fact. R prints in one line what took a page of arithmetic.
That is the point of this course.

```r
coef(model)                  # just the coefficients
predict(model, newdata = data.frame(hours = 7.5))
residuals(model)
plot(model)                  # four diagnostic plots
confint(model)               # confidence intervals for coefficients
```

`plot(model)` gives the residual diagnostics from Course 4 §4.6 — residuals vs
fitted (look for curvature), Q-Q (look for non-normality), scale-location, and
leverage.

## 4.2 Multiple regression

```r
model <- lm(marks ~ hours + attendance + prev_cgpa, data = students)
summary(model)

lm(marks ~ ., data = students)          # . means "all other columns"
lm(marks ~ hours + I(hours^2))          # polynomial term
lm(marks ~ hours * section)             # main effects AND interaction
```

### Interpretation changes

β₁ is now the effect of `hours` **holding attendance and prev_cgpa constant**.
That phrase is the whole difference from simple regression, and exams expect it
verbatim.

**Use adjusted R², not R²**, to compare models with different numbers of
predictors. R² never decreases when you add a variable — even a column of random
numbers. Adjusted R² penalises the extra parameter and can fall.

### Factors become dummy variables automatically

```r
lm(marks ~ section, data = students)     # section is a factor with 3 levels
# R creates sectionB and sectionC; sectionA is the reference level
```

The omitted level is the **baseline**, and every coefficient is a difference
from it. `relevel(students$section, ref = "C")` changes which.

### Multicollinearity

```r
car::vif(model)      # variance inflation factor
```

**VIF > 5 (or 10) signals a problem.** When predictors are strongly correlated
with each other the model cannot separate their effects; coefficients become
unstable and their signs may flip. Course 4 §4.7 introduced this — here is how
you detect it.

## 4.3 Model evaluation

### 🎯 The big idea

A model's accuracy on the data it was trained on tells you almost nothing. What
matters is performance on data it has never seen — and even then, accuracy alone
can be badly misleading.

### 📖 The story

A hospital builds a model to detect a rare disease affecting 1% of patients. It
reports **99% accuracy** and everyone celebrates.

Then someone checks what it actually predicts. It says "healthy" to every single
patient. It is right 99% of the time — and it has never once detected the
disease it was built to find.

**This is the accuracy paradox**, and it is why the confusion matrix exists.

### Train/test split

```r
set.seed(42)                                   # reproducibility
idx <- sample(seq_len(nrow(df)), size = 0.8 * nrow(df))
train <- df[idx, ]
test  <- df[-idx, ]                            # note: negative index EXCLUDES
```

**`set.seed()` matters.** Without it, every run gives a different split and your
results are not reproducible — which in an exam or a report is a real fault.

### The confusion matrix

For a binary classifier:

| | **Predicted Positive** | **Predicted Negative** |
|---|---|---|
| **Actual Positive** | True Positive (TP) | False Negative (FN) |
| **Actual Negative** | False Positive (FP) | True Negative (TN) |

> **Accuracy = (TP + TN) / (TP + TN + FP + FN)**
>
> **Precision = TP / (TP + FP)** — of those predicted positive, how many were?
>
> **Recall (Sensitivity) = TP / (TP + FN)** — of the actual positives, how many did we catch?
>
> **Specificity = TN / (TN + FP)** — of the actual negatives, how many did we clear?
>
> **F1 = 2 × (Precision × Recall) / (Precision + Recall)** — their harmonic mean

**Precision vs recall — which matters more depends entirely on the cost of each
error:**

| Situation | Optimise | Because |
|---|---|---|
| Cancer screening | **Recall** | Missing a case is far worse than a false alarm |
| Spam filtering | **Precision** | Losing a real email is worse than seeing spam |
| Fraud detection | **Recall**, then precision | Missed fraud costs money; false alarms cost goodwill |

**Type I and Type II errors** from Course 4 §5.6 are the same thing: a false
positive is Type I, a false negative is Type II.

**F1 is the harmonic mean, not the arithmetic mean**, precisely because the
harmonic mean punishes imbalance. Precision 1.0 with recall 0.0 gives F1 = 0,
not 0.5.

```r
library(caret)
confusionMatrix(factor(predicted), factor(actual), positive = "1")
```

### ROC and AUC

A classifier usually outputs a **probability**, and you choose a threshold to
turn it into a decision. The ROC curve shows what happens across *every* possible
threshold.

- **x-axis:** False Positive Rate = FP/(FP+TN) = 1 − specificity
- **y-axis:** True Positive Rate = TP/(TP+FN) = recall

| AUC | Interpretation |
|---|---|
| 1.0 | Perfect |
| 0.9–1.0 | Excellent |
| 0.8–0.9 | Good |
| 0.7–0.8 | Fair |
| 0.5 | **No better than random** — the diagonal line |
| < 0.5 | Worse than random; invert your predictions |

**AUC is the probability that the model ranks a randomly chosen positive above
a randomly chosen negative.** That interpretation is worth stating — it explains
why AUC is threshold-independent, which is its main advantage over accuracy.

```r
library(pROC)
r <- roc(test$actual, predicted_probabilities)
auc(r); plot(r)
```

## 4.4 K-Means clustering

### 🎯 The big idea

K-Means splits data into k groups by repeatedly assigning each point to its
nearest group centre, then moving each centre to the middle of its points.

### The algorithm — examinable step by step

1. Choose **k** and place k centroids (randomly, or with k-means++)
2. **Assign** each point to the nearest centroid (usually Euclidean distance)
3. **Update** each centroid to the mean of its assigned points
4. **Repeat** 2–3 until assignments stop changing (convergence)

```r
set.seed(42)
km <- kmeans(scale(data[, c("income", "spending")]), centers = 3, nstart = 25)
km$cluster; km$centers; km$tot.withinss
```

**`scale()` is not optional.** K-Means uses distance, so a variable measured in
rupees (range 100,000) will completely dominate one measured in years (range
50). Forgetting to scale is the single most common K-Means error and it silently
produces meaningless clusters.

**`nstart = 25`** runs the algorithm 25 times from different random starts and
keeps the best. K-Means converges to a *local* optimum that depends on
initialisation, so a single run can be poor.

### Choosing k — the elbow method

Plot total within-cluster sum of squares against k and look for the "elbow"
where the improvement flattens.

```r
wss <- sapply(1:10, function(k) kmeans(scaled, k, nstart = 10)$tot.withinss)
plot(1:10, wss, type = "b", xlab = "k", ylab = "Within-cluster SS")
```

WSS always falls as k rises — at k = n every point is its own cluster with WSS 0.
The elbow is where extra clusters stop buying much. The **silhouette score** is
a less subjective alternative.

### Limitations, which exams ask for

1. **k must be chosen in advance**
2. Sensitive to **initial centroids** — hence `nstart`
3. Assumes **spherical, similarly sized** clusters
4. Sensitive to **outliers**, because it uses means
5. Struggles with **non-convex** shapes — DBSCAN handles those (Course 8)
6. Requires **scaled** numeric data

## 4.5 Text mining and word clouds

```r
library(tm); library(wordcloud)

corpus <- Corpus(VectorSource(reviews)) %>%
  tm_map(content_transformer(tolower)) %>%
  tm_map(removePunctuation) %>%
  tm_map(removeNumbers) %>%
  tm_map(removeWords, stopwords("english")) %>%
  tm_map(stripWhitespace) %>%
  tm_map(stemDocument)

dtm  <- TermDocumentMatrix(corpus)
freq <- sort(rowSums(as.matrix(dtm)), decreasing = TRUE)
wordcloud(names(freq), freq, max.words = 100, colors = brewer.pal(8, "Dark2"))
```

### The preprocessing pipeline — every step earns marks

| Step | Removes / does | Why |
|---|---|---|
| **Lowercase** | Case distinctions | "The" and "the" are one word |
| **Remove punctuation** | `.,!?` | "data." and "data" are one word |
| **Remove numbers** | Digits | Rarely meaningful in topic analysis |
| **Remove stop words** | the, is, at, which | Frequent but carry no topic signal |
| **Strip whitespace** | Extra spaces | Tidiness |
| **Stemming** | running → run | Collapses inflections |
| **Lemmatisation** | better → good | Smarter than stemming; uses a dictionary |

**Stemming vs lemmatisation** is a standard two-mark question. Stemming chops
suffixes mechanically and can produce non-words ("studies" → "studi").
Lemmatisation uses vocabulary and grammar to return a real word ("studies" →
"study"). Stemming is faster; lemmatisation is more accurate.

**Term-Document Matrix**: rows are terms, columns are documents, cells are
counts. **TF-IDF** weights each term by how distinctive it is:

> **TF-IDF(t,d) = TF(t,d) × log(N / DF(t))**

A word appearing in every document has DF = N, so log(N/N) = 0 and it is
weighted out entirely. That is TF-IDF's whole trick, and it is why it beats raw
counts.

## 4.6 Recommender systems

| Type | Basis | Example |
|---|---|---|
| **Content-based** | Item features similar to what you liked | "You watched a thriller, here is another thriller" |
| **Collaborative filtering** | What similar *users* liked | "Users like you also bought…" |
| — *user-based* | Find similar users, recommend their items | |
| — *item-based* | Find items co-liked with yours | Amazon's approach |
| **Hybrid** | Both combined | Netflix |

```r
library(recommenderlab)
r <- Recommender(train_matrix, method = "UBCF")     # user-based CF
predict(r, test_matrix, n = 5)
```

### The two problems every recommender has

**Cold start** — a new user has no history and a new item has no ratings, so
collaborative filtering has nothing to work with. Content-based methods handle
new *items* better; new *users* usually get popular-item defaults until they
interact.

**Sparsity** — with a million users and a million items, the ratings matrix is
almost entirely empty. Matrix factorisation (SVD) is the standard response.

**Similarity measures:** cosine similarity, Pearson correlation, Jaccard index.
Cosine is the most common because it ignores magnitude — a user who rates
everything highly and one who rates everything low can still be recognised as
having the same *taste*.

## 4.7 Ethical issues in data science

The syllabus lists this last; treat it as examinable rather than decorative.

### The six issues to know

**1. Bias and fairness.** A model trained on historical hiring data learns
historical discrimination. Amazon scrapped a recruiting tool that penalised CVs
containing the word "women's". The model was working correctly — it faithfully
reproduced the bias in its training data. *Garbage in, gospel out.*

**2. Privacy.** Aggregated data can re-identify individuals. Netflix released
"anonymised" ratings; researchers matched them to public IMDb reviews and
de-anonymised users. Anonymisation is much harder than removing names.

**3. Transparency and explainability.** A model that denies someone a loan
should be able to say why. "The neural network decided" is not an acceptable
answer, and in several jurisdictions is not a legal one either.

**4. Consent.** Data collected for one purpose being reused for another —
Cambridge Analytica being the standard example.

**5. Accountability.** When an autonomous system causes harm, who is
responsible — the developer, the deployer, the data provider?

**6. Environmental cost.** Training large models consumes substantial energy.

### Regulation worth naming

- **GDPR** (EU) — consent, the right to erasure, the right to an explanation
- **DPDP Act 2023** (India) — the Digital Personal Data Protection Act
- **Sector rules** — HIPAA for health data in the US, RBI norms for Indian
  financial data

### 💡 The point to make in an exam

The technical question is *can we build this?* The ethical question is *should
we?* — and they are genuinely separate. A model can be statistically excellent
and socially harmful at the same time; accuracy is not a defence.

Concretely: always ask **who is in the training data and who is missing from
it**. A face-recognition system trained mostly on light-skinned faces performs
worse on dark-skinned ones. That is not a bug in the algorithm; it is a bug in
the dataset, and no amount of tuning fixes it.

---

## 📝 Practice problems

### Problem 1

A classifier tested on 1000 patients gives: TP = 80, FP = 20, FN = 40, TN = 860.
Compute accuracy, precision, recall, specificity and F1, and comment.

**Solution.**

- **Accuracy** = (80 + 860)/1000 = **0.940** → 94%
- **Precision** = 80/(80 + 20) = 80/100 = **0.800**
- **Recall** = 80/(80 + 40) = 80/120 = **0.667**
- **Specificity** = 860/(860 + 20) = 860/880 = **0.977**
- **F1** = 2(0.800 × 0.667)/(0.800 + 0.667) = 2(0.5336)/1.467 = **0.727**

**Comment.** Accuracy of 94% looks strong, but recall is only 67% — the model
**misses a third of actual cases**. For a disease screening test that is
unacceptable; you would lower the decision threshold, accepting more false
positives to catch more true ones. Precision would fall and recall rise.

This is exactly why accuracy alone is insufficient: 88% of these patients are
healthy, so predicting "healthy" for everyone would already score 88%.

### Problem 2

Explain why K-Means requires scaling, with a concrete example.

**Solution.**

Consider clustering customers on **annual income** (₹200,000–₹2,000,000) and
**age** (20–70).

Take two customers:

| | Income | Age |
|---|---|---|
| A | 500,000 | 25 |
| B | 500,010 | 65 |

Euclidean distance without scaling:

√[(500,010 − 500,000)² + (65 − 25)²] = √[100 + 1600] = √1700 ≈ **41.2**

The income difference of ₹10 contributes 100 to the squared distance; the
40-year age gap contributes 1600. That seems fine — but now compare A with
someone earning ₹600,000 at the same age 25:

√[(600,000 − 500,000)² + 0] = **100,000**

Income differences dwarf age differences by three orders of magnitude, so the
clustering is effectively **on income alone**. Age is present in the data and
invisible to the algorithm.

After `scale()`, both variables have mean 0 and sd 1, and each contributes
comparably. **Any distance-based method — K-Means, KNN, hierarchical clustering,
DBSCAN — requires this.** Tree-based methods do not, because they split on one
variable at a time.

### Problem 3

You build a loan-default model with 96% accuracy. The bank wants to deploy it.
What do you check first?

**Solution.**

**1. The class balance.** If only 4% of loans default, predicting "no default"
for everyone scores 96%. Check the confusion matrix, not the accuracy.

**2. Recall on the minority class.** The whole purpose is catching defaults. If
recall is near zero the model is worthless regardless of accuracy.

**3. Whether the split was honest.** Was the test set genuinely held out? Was
scaling fitted on training data only? Fitting a scaler on the full dataset leaks
test information into training and inflates every metric.

**4. Fairness across groups.** Does it reject applicants from particular
regions, castes or genders at different rates? Check performance per subgroup,
not just overall. A model can be accurate overall and discriminatory in
practice.

**5. Explainability.** Under lending regulation the bank may be required to give
a reason for refusal. A model that cannot supply one may not be deployable at
all.

**6. Temporal validity.** Was the model tested on a *later* time period than it
trained on? Random splitting on time-series data leaks the future into the past
and produces optimistic results that collapse in production.

**Recommendation:** do not deploy on accuracy alone. Report the confusion
matrix, per-class recall, AUC and a subgroup fairness analysis first.

---

## Exam questions from this unit

**Two marks**

1. What is the accuracy paradox?
2. Define precision and recall.
3. Why must data be scaled before K-Means?
4. What does AUC measure?
5. Distinguish stemming from lemmatisation.
6. What is the cold-start problem?

**Five marks**

1. Explain the confusion matrix and the metrics derived from it.
2. Explain the K-Means algorithm step by step, with its limitations.
3. Explain the text mining preprocessing pipeline.
4. Explain content-based and collaborative filtering with examples.
5. Explain any four ethical issues in data science.

**Ten marks**

1. Explain model evaluation in detail — train/test split, confusion matrix,
   precision, recall, F1, ROC and AUC — with a worked example.
2. Explain regression in R, from `lm()` through to interpreting `summary()`
   output and diagnostics.

## Mistakes that cost marks

- Reporting accuracy alone on imbalanced data
- Confusing precision with recall
- Forgetting `scale()` before K-Means
- Evaluating on the training set
- Fitting a scaler on the full dataset before splitting — this leaks
- Treating AUC = 0.5 as acceptable; it is random guessing
- Comparing multiple regression models by R² instead of adjusted R²
- Answering an ethics question with only a technical answer
