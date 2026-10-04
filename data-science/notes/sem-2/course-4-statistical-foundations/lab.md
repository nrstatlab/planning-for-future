# Lab — Statistical Foundations for Data Science

**15 experiments**, done in five Python programs, each set out as 1. Question, 2. Aim, 3. Steps,
4. Programme, 5. Execution and Results.

The prescribed lab is headed **"Advanced Spreadsheets/Excel Lab/PSPP Open
Source"**. Every experiment is a spreadsheet exercise, and the practical exam
tests it in a spreadsheet.

## Do each experiment twice

**Once in Excel** — that is what the exam marks.
**Once in Python** — that is what the course is for.

The prescribed lab never uses Python, even though Python Programming and Data Structures teaches the language; Python-based analysis is taught in Python for Data Analysis and Visualization.
That gap is worth closing yourself. See
[`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D8**.

| | Where |
|---|---|
| Excel walkthroughs, all 15 | [`labs/course-4-stats/excel-walkthroughs.md`](../../../labs/course-4-stats/excel-walkthroughs.md) |
| Python equivalents | `labs/course-4-stats/python/` |
| Distribution functions | `statlib.py` |
| Table-value checks | `test_statlib.py` |

```bash
bash tools/data-science/run_stats_labs.sh                       # verify everything
cd labs/course-4-stats/python && python3 test_statlib.py
```

The Python programs share one file, so the experiments are set out below by program, in the
order of their first experiment; each program's steps follow its experiments.

---

## The experiments

| # | Experiment | Unit | Python file |
|:---:|---|:---:|---|
| 1 | Contingency table, conditional probability, independence | 1 | `01_probability_contingency.py` |
| 2 | Bayes' theorem *(reconstructed)* | 1 | same file |
| 3 | Measures of central tendency | 1 | `02_descriptive_stats.py` |
| 4 | Measures of dispersion | 1 | same file |
| 5 | Histogram and distribution shape | 1 | same file |
| 6 | Bar charts of categorical data | 1 | same file |
| 7 | Scatter plot, correlation, covariance | 1, 4 | `04_correlation_regression.py` |
| 8 | Simulating random variables | 2 | `03_random_variables_distributions.py` |
| 9 | Expectation and variance | 2 | same file |
| 10 | Binomial and Poisson distributions | 3 | same file |
| 11 | Normal and exponential distributions | 3 | same file |
| 12 | Correlation analysis (Pearson and Spearman) | 4 | `04_correlation_regression.py` |
| 13 | Linear regression | 4 | same file |
| 14 | Confidence intervals | 5 | `05_inference_hypothesis_tests.py` |
| 15 | Hypothesis testing (z, t, chi-square, F) | 5 | same file |

---

## Experiment 2 is reconstructed

The official text of experiment 2 survives only as the fragment **"a positive
result."** — the question stem is missing from the PDF. See review findings
**D1** and **D3**.

Reconstructed question:

> A disease affects 1% of a population. A test is 99% sensitive and 95%
> specific. Given a positive result, what is the probability the person has the
> disease?

**Answer: about 16.7%**, not 99%. Of 10,000 people, 99 true positives are
outnumbered by 495 false positives. Build that 10,000-person table in your
sheet — it makes the result obvious and it earns marks.

This is the **base rate fallacy**, and Bayes' theorem is examined despite being
absent from the syllabus units. Do not skip it.

---

## Experiments 1 and 2 — Contingency tables and Bayes' theorem

### 1. Question

Unit 1. **Experiment 1:** from sales data, build the contingency table of region against
purchase type, and find the joint, marginal and conditional probabilities; are region and
purchase independent? **Experiment 2** *(reconstructed)*: a disease affects 1% of a population,
and a test is 99% sensitive and 95% specific; given a positive result, what is the probability
that the person has the disease?

### 2. Aim

Read probabilities off a contingency table, and turn a test's accuracy into the chance that a positive result is right.

### 3. Steps

1. **Experiment 1: the contingency table.**
2. **Joint probabilities.**
3. **Marginal probabilities.**
4. **Conditional probabilities.**
5. **The independence check.**
6. **Experiment 2: the medical test.**
7. **The law of total probability.**
8. **Bayes' theorem.**

<div class="formula" markdown="1">
<span class="label">IN EXCEL</span>

Build the table with a PivotTable, then compute joint, marginal and conditional
probabilities from it. The independence check compares each observed cell with
`row_total × column_total / grand_total`. They will rarely match exactly —
experiment 15's chi-square test is what tells you whether the gap is larger
than chance.
</div>


### 4. Programme

{{programme: course-4-stats/python/01_probability_contingency.py}}

### 5. Execution and Results

{{output: course-4-stats/python/01_probability_contingency.py}}

The dataset used in the Python version gives χ² = 9.75 on 2 df (p = 0.0076), so
region and purchase type are genuinely associated. Experiments 1 and 15 are
answering the same question at two levels of rigour.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Region and purchase type are dependent: knowing the region changes the probability of a premium purchase. A positive result means the disease with probability 0.1667, about 16.7% — not 99%.
</div>


## Experiments 3 to 6 — Central tendency, dispersion, the histogram and the bar chart

### 1. Question

Unit 1. For a set of marks: **3**, find the mean, median and mode; **4**, the range,
quartiles, variance, standard deviation and coefficient of variation; **5**, draw a histogram
and describe the shape of the distribution; **6**, draw a bar chart of categorical data.

### 2. Aim

Summarise a data set by its centre, its spread and its shape, and know which summary to quote.

### 3. Steps

1. **Experiment 3: the mean.**
2. **The median.**
3. **The mode.**
4. **Which one to use.**
5. **Experiment 4: range and quartiles.**
6. **Variance and standard deviation.**
7. **Coefficient of variation, and outliers.**
8. **Experiment 5: the histogram and its shape.**
9. **Experiment 6: a bar chart of categories.**

<div class="formula" markdown="1">
<span class="label">IN EXCEL</span>

**`.S` or `.P`?** `VAR.S`/`STDEV.S` divide by n − 1 (sample); `VAR.P`/`STDEV.P` divide by n
(population). Almost every exercise here uses a **sample**, so almost always
`.S`. Choosing wrongly is the most common error in this lab, and it changes the
answer.
</div>


### 4. Programme

{{programme: course-4-stats/python/02_descriptive_stats.py}}

### 5. Execution and Results

{{output: course-4-stats/python/02_descriptive_stats.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The twenty marks have mean 70.05 and median 70.0, and no mode, since every mark occurs once. The IQR is 20.25, the sample standard deviation 14.24 (divisor n − 1) and the coefficient of variation 20.33%; there are no outliers, and the distribution is close to symmetric (Pearson skewness 0.011). One extra mark of 500 would move the mean from 70.05 to 90.52 and the median hardly at all.
</div>


## Experiments 7, 12 and 13 — Covariance, correlation and regression

### 1. Question

Units 1 and 4. For hours studied against exam score: **7**, draw the scatter plot and find
the covariance and correlation; **12**, find Pearson's and Spearman's correlation;
**13**, fit the simple linear regression of score on hours, and test it.

### 2. Aim

Measure how closely two variables move together, and fit the line that predicts one from the other.

### 3. Steps

1. **The data, and the deviations from the means.**
2. **Covariance.**
3. **Pearson's r.**
4. **Spearman's rank correlation.**
5. **Experiment 13: the regression line.**
6. **Residuals.**
7. **The analysis of variance, and R squared.**
8. **Testing the slope.**
9. **Prediction.**

<div class="formula" markdown="1">
<span class="label">IN EXCEL</span>

**Reading the regression output.** Excel's Regression tool produces a lot of output. The rows
that matter:

| Output | Meaning |
|---|---|
| `R Square` | fraction of variance explained |
| `Coefficients: Intercept` | b₀ |
| `Coefficients: X Variable 1` | b₁, the slope |
| `Significance F` | the p-value for the whole model |
| `P-value` (for X Variable 1) | the p-value for the slope |

**Interpret the slope in context** — "each extra hour of study is associated
with about 4.3 more marks" — not just "b₁ = 4.3".

Two arithmetic checks that come free: **R² = r²** and **t² = F** for simple
regression. Use them.
</div>


### 4. Programme

{{programme: course-4-stats/python/04_correlation_regression.py}}

### 5. Execution and Results

{{output: course-4-stats/python/04_correlation_regression.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

r = 0.9979, a very strong positive linear relationship. The fitted line has slope 4.30: each extra hour of study is associated with about 4.30 more marks. R² = 0.9958 = r², and the slope's t² equals F (p = 8.4 × 10⁻¹¹). The data cannot show that studying causes the marks.
</div>


## Experiments 8 to 11 — Random variables and the probability distributions

### 1. Question

Units 2 and 3. **8**, simulate a discrete and a continuous random variable; **9**, find the
expectation and variance of a probability distribution; **10**, work with the binomial and
Poisson distributions; **11**, with the normal and exponential distributions.

### 2. Aim

Generate random variables, and compute probabilities from the four distributions the syllabus names.

### 3. Steps

1. **Experiment 8: a die rolled 1000 times.**
2. **1000 draws from a normal distribution.**
3. **Experiment 9: expectation and variance.**
4. **Experiment 10: the binomial.**
5. **The Poisson.**
6. **Experiment 11: the normal.**
7. **The exponential.**

<div class="formula" markdown="1">
<span class="label">IN EXCEL</span>

**Experiment 8 — freeze your random numbers.** `RAND()` and `RANDBETWEEN()` are **volatile** —
they recalculate on every edit, so your statistics change while you are computing them. Generate
the column, then copy it and **Paste Special → Values** before doing anything else. (The Python
version fixes its seed, so it prints the same numbers every time.)

**Experiment 10 — the `FALSE`/`TRUE` argument.** `BINOM.DIST(k, n, p, FALSE)` gives P(X = k);
`TRUE` gives P(X ≤ k). Getting this backwards is the single most common error in this experiment.
Same for `POISSON.DIST`.

**Experiment 11 — verify the empirical rule.** Compute P(μ−σ ≤ X ≤ μ+σ) and confirm it comes to
0.6827, then ±2σ → 0.9545 and ±3σ → 0.9973. Doing this once makes the rule stick, and it
validates that your `NORM.DIST` arguments are in the right order.

Also demonstrate **memorylessness** for the exponential: show that
P(X > 5 | X > 2) equals P(X > 3) by computing both sides.
</div>


### 4. Programme

{{programme: course-4-stats/python/03_random_variables_distributions.py}}

### 5. Execution and Results

{{output: course-4-stats/python/03_random_variables_distributions.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The simulated die and normal draws come close to their theoretical values; Var(X) = E(X²) − [E(X)]² gives the variance; the binomial and Poisson tables add to 1; P(85 ≤ X ≤ 115) = 0.6827 for the normal; and P(X > 5 | X > 2) = P(X > 3) = 0.22313 for the exponential.
</div>


## Experiments 14 and 15 — Confidence intervals and hypothesis tests

### 1. Question

Unit 5. **14**, from a sample of heights, find confidence intervals for the mean;
**15**, carry out a one-sample z-test, a two-sample t-test, a chi-square test of independence and
an F-test for two variances.

### 2. Aim

Estimate a mean with a stated confidence, and test hypotheses with the test the situation calls for.

### 3. Steps

1. **Experiment 14: the sample.**
2. **Confidence intervals, with t.**
3. **Experiment 15: the steps of every test.**
4. **One-sample z-test.**
5. **Two-sample t-test.**
6. **Chi-square test of independence.**
7. **F-test for two variances.**
8. **Type I and Type II errors, and power.**

<div class="formula" markdown="1">
<span class="label">IN EXCEL</span>

**Experiment 15 — which test?**

| Situation | Test | Excel |
|---|---|---|
| One mean, σ known or n > 30 | z-test | `NORM.S.DIST` |
| One mean, σ unknown, small n | one-sample t | `T.DIST.2T` |
| Two group means | two-sample t | `T.TEST(r1, r2, 2, 2)` |
| Same subjects measured twice | paired t | `T.TEST(r1, r2, 2, 1)` |
| Two categorical variables | chi-square | `CHISQ.TEST(obs, exp)` |
| Two variances | F-test | `F.TEST(r1, r2)` |

**`CHISQ.TEST` and `F.TEST` return p-values, not test statistics.** Reporting a
`CHISQ.TEST` result as χ² is a standard mistake.
</div>


### 4. Programme

{{programme: course-4-stats/python/05_inference_hypothesis_tests.py}}

### 5. Execution and Results

{{output: course-4-stats/python/05_inference_hypothesis_tests.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The 95% interval for the mean height is (71.060, 73.140); the 90% and 99% intervals are narrower and wider. The two teaching methods differ (t = 4.7541 on 18 df, p = 0.000159); region and purchase type are associated (χ² = 9.75 on 2 df, p = 0.0076); and the two variances may be taken as equal (F on (9, 9) df, p = 0.3682), so the pooled t-test was appropriate.
</div>


---

## PSPP

PSPP is the free SPSS alternative named in the syllabus, and may be what your
lab has installed.

| Task | Menu path |
|---|---|
| Descriptive statistics | Analyze → Descriptive Statistics → Descriptives |
| Frequencies and histogram | Analyze → Descriptive Statistics → Frequencies |
| Contingency table + chi-square | Analyze → Descriptive Statistics → Crosstabs |
| Correlation | Analyze → Bivariate Correlation |
| Regression | Analyze → Linear Regression |
| t-tests | Analyze → Compare Means |

Enter variable definitions in **Variable View** first, then data in **Data
View** — the opposite order to a spreadsheet, and the usual source of
confusion.

---

## Lab exam tips

1. **Label everything.** Chart titles, axis labels, legends. Marks are given
   for a readable output, not just a correct number.
2. **Show the formula**, not only the result. Examiners often ask you to widen
   a column or press Ctrl+` to reveal formulas.
3. **Interpret in a text box** next to each result. "r = 0.87, a strong
   positive linear relationship; this does not establish causation" earns more
   than the number alone.
4. **State H₀ and H₁ in the sheet** for every test, then the statistic, then
   the p-value, then the decision, then a conclusion in words.
5. **Check the assumptions and say you did** — expected frequencies ≥ 5 for
   chi-square, approximate normality for t-tests.
6. **Round sensibly.** Two or three decimals. Copying fifteen digits from the
   cell looks careless.
7. **Save frequently** under a filename with your roll number.

## What the practical record should contain

For each experiment, the five parts set out above: **1. Question**, the task as set; **2. Aim**, in
one line; **3. Steps**, the method, with the Excel functions; **4. Programme**, the program (or the
sheet's formulas); **5. Execution and Results**, what it gave, and the result in words.
