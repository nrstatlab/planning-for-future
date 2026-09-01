# Course 6 Lab — Data Science with R

**18 practicals**

## Two versions of every experiment

| | Location | Status |
|---|---|---|
| **R** — as the exam tests it | `labs/course-6-r/` | ⚠ desk-checked, not executed |
| **Python equivalents** | `labs/course-6-r/python/` | ✅ executed, with assertions |

**R could not be installed** in the environment where this repository is
verified — the Debian package repositories are blocked by the network policy,
and R is not on PyPI or npm. Every R script says so in its own header rather
than implying a test that never ran.

What the Python side buys you: **the statistics are machine-checked even though
the R syntax is not.** When `04_regression.R` says the slope is 4.3030, that
number came from
`04_regression.py`, which
runs and asserts it — and which cross-checks against Course 4 Unit 4, where the
same data was worked by hand.

```bash
python3 tools/run_r_equivalents.py
```

That runs all 14 Python equivalents and structurally checks all 18 R scripts
(balanced delimiters, and that the "not executed" header is still present).

---

## The experiments

| # | Experiment | R file | Python | Unit |
|:---:|---|---|:---:|:---:|
| 1 | Mean, median, mode, variance, SD | `01_descriptive.R` | ✅ | 1 |
| 2 | Binomial, normal, Poisson | `02_distributions.R` | ✅ | 1 |
| 3 | t-test and chi-square | `03_hypothesis_tests.R` | ✅ | 1 |
| 4 | Correlation and regression | `04_regression.R` | ✅ | 4 |
| 5 | EDA on a real dataset | `05_eda.R` | ✅ | 1 |
| 6 | Feature engineering | `06_feature_engineering.R` | ✅ | 1 |
| 7 | Variables, control structures, functions | `07_r_basics.R` | — | 2 |
| 8 | CSV, Excel, JSON, XML | `08_file_io.R` | ✅ | 2 |
| 9 | dplyr and tidyr | `09_wrangling.R` | ✅ | 3 |
| 10 | Missing data and outliers | `10_missing_outliers.R` | ✅ | 3 |
| 11 | Dates and times | `11_dates.R` | ✅ | 3 |
| 12 | ggplot2 | `12_ggplot.R` | — | 3 |
| 13 | K-Means clustering | `13_kmeans.R` | ✅ | 4 |
| 14 | Confusion matrix, accuracy, ROC | `14_evaluation.R` | ✅ | 4 |
| 15 | Text mining and word cloud | `15_text_mining.R` | ✅ | 4 |
| 16 | ARIMA forecasting | `16_arima.R` | ✅ | 5 |
| 17 | Interactive plots with plotly | `17_plotly.R` | — | 5 |
| 18 | Shiny app with CSV upload | `18_shiny_app.R` | — | 5 |

Experiments 7, 12, 17 and 18 have no Python equivalent: they demonstrate R
*syntax*, ggplot2's *grammar*, plotly's R *interface* and the Shiny *framework*.
A translation would teach nothing.

---

## Notes on the harder ones

### 2 — The d/p/q/r naming convention

Worth memorising once, because it applies to every distribution in R:

| Prefix | Gives | Example |
|---|---|---|
| `d` | density / PMF | `dbinom(3, 10, 0.3)` = 0.2668 |
| `p` | cumulative (CDF) | `pbinom(3, 10, 0.3)` = 0.6496 |
| `q` | quantile (inverse) | `qnorm(0.95, 100, 15)` = 124.67 |
| `r` | random generation | `rnorm(100, 100, 15)` |

### 3 — `var.equal` changes the test

`t.test(a, b, var.equal = TRUE)` is the **pooled** t-test from Course 4 Unit 5.
Omit it and R runs **Welch's** test, which does not assume equal variances and
reports fractional degrees of freedom. Both are defensible; know which you ran.
Check the assumption first with `var.test()` — on the lab data it gives
F = 1.8618, p = 0.3682, so equal variances are reasonable.

### 6 — R and Python scale differently

`scale()` uses `sd()`, which divides by **n−1**. scikit-learn's
`StandardScaler` divides by **n**. The standardised values therefore differ
slightly between the R script and its Python equivalent. Harmless for modelling,
but do not expect identical numbers, and say so if asked.

### 10 — Masking, which the lab actually demonstrates

Both the IQR and z-score rules catch a single outlier of 250. Add a second at
260 and the standard deviation inflates from 46.40 to 61.97 — enough that the
z-score rule flags **nothing**, while the IQR rule still catches both.

That is **masking**, and it is why the IQR rule is preferred when outliers may
cluster. The Python equivalent asserts this, so the claim is tested rather than
asserted.

### 13 — Scaling is the whole experiment

The lab data has an income:age variance ratio of about **4 billion to 1**.
Without `scale()`, K-Means clusters on income alone and age contributes nothing
measurable. Run it both ways and compare `table(km$cluster, km_raw$cluster)` —
seeing the two solutions disagree is more convincing than being told they will.

### 16 — Difference before you read the ACF

On the raw airline series the ACF decays smoothly and shows **no seasonality at
all** — the trend dominates completely. Only after differencing does the
oscillation appear, peaking at lag 12. Reading ACF/PACF on a trending series
tells you nothing except "there is a trend".

### 18 — The three Shiny rules

1. **Call a reactive with parentheses** — `data()`, never `data`.
2. **`input$x` only inside a reactive context** — `reactive()`, `observe()` or
   `render*()`.
3. **Output IDs must match** between `ui` and `server`. A typo gives a blank
   panel and **no error message**, so check spelling first.

`req(input$file)` is the idiomatic way to wait for an upload — it silently
pauses the reactive rather than erroring on `NULL`.

---

## Lab exam tips

1. **Install R and RStudio at home.** You cannot revise R from notes alone.
2. **`set.seed()` before anything random** — clustering, sampling, simulation.
   Without it your results are not reproducible, which is a fault in itself.
3. **`str()` and `summary()` first**, always. Know your data before analysing it.
4. **Comment the interpretation, not the syntax.** `# r = 0.99, very strong
   positive` earns marks; `# compute correlation` does not.
5. **Label every plot** — title, axis labels, legend.
6. **Expect a viva.** "Why `var.equal = TRUE`?", "what happens without
   `scale()`?", "why difference before reading the ACF?"
