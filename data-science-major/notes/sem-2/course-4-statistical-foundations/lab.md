# Course 4 Lab — Statistical Foundations for Data Science

**15 experiments**

The prescribed lab is headed **"Advanced Spreadsheets/Excel Lab/PSPP Open
Source"**. Every experiment is a spreadsheet exercise, and the practical exam
tests it in a spreadsheet.

## Do each experiment twice

**Once in Excel** — that is what the exam marks.
**Once in Python** — that is what the degree is for.

The prescribed lab never uses Python, even though you are learning Python in
Course 3 the same semester; Python-based analysis waits until Semester IV.
That gap is worth closing yourself. See
[`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D8**.

| | Where |
|---|---|
| Excel walkthroughs, all 15 | `labs/course-4-stats/excel-walkthroughs.md` |
| Python equivalents | `labs/course-4-stats/python/` |
| Distribution functions | `statlib.py` |
| Table-value checks | `test_statlib.py` |

```bash
bash tools/run_stats_labs.sh                       # verify everything
cd labs/course-4-stats/python && python3 test_statlib.py
```

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

## Notes on the harder experiments

### Experiment 1 — Contingency tables

Build the table with a PivotTable, then compute joint, marginal and conditional
probabilities from it. The independence check compares each observed cell with
`row_total × column_total / grand_total`. They will rarely match exactly —
experiment 15's chi-square test is what tells you whether the gap is larger
than chance.

The dataset used in the Python version gives χ² = 9.75 on 2 df (p = 0.0076), so
region and purchase type are genuinely associated. Experiments 1 and 15 are
answering the same question at two levels of rigour.

### Experiment 4 — `.S` or `.P`?

`VAR.S`/`STDEV.S` divide by n − 1 (sample); `VAR.P`/`STDEV.P` divide by n
(population). Almost every exercise here uses a **sample**, so almost always
`.S`. Choosing wrongly is the most common error in this lab, and it changes the
answer.

### Experiment 8 — Freeze your random numbers

`RAND()` and `RANDBETWEEN()` are **volatile** — they recalculate on every edit,
so your statistics change while you are computing them. Generate the column,
then copy it and **Paste Special → Values** before doing anything else.

### Experiment 10 — The `FALSE`/`TRUE` argument

`BINOM.DIST(k, n, p, FALSE)` gives P(X = k); `TRUE` gives P(X ≤ k). Getting
this backwards is the single most common error in this experiment. Same for
`POISSON.DIST`.

### Experiment 11 — Verify the empirical rule

Compute P(μ−σ ≤ X ≤ μ+σ) and confirm it comes to 0.6827, then ±2σ → 0.9545 and
±3σ → 0.9973. Doing this once makes the rule stick, and it validates that your
`NORM.DIST` arguments are in the right order.

Also demonstrate **memorylessness** for the exponential: show that
P(X > 5 | X > 2) equals P(X > 3) by computing both sides.

### Experiment 13 — Reading the regression output

Excel's Regression tool produces a lot of output. The rows that matter:

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

### Experiment 15 — Which test?

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
