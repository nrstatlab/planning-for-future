# Lab — Data Science with R

**18 practicals**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.

## Two versions of every experiment

| | Location | Status |
|---|---|---|
| **R** — as the exam tests it | `labs/course-6-r/` | ✅ executed, with R 4.3.3 |
| **Python equivalents** | `labs/course-6-r/python/` | ✅ executed, with assertions |

**Every R script is run**, and under **5. Execution and Results** is what it printed, with the
plots it drew. Two cannot simply be run in a terminal: `17_plotly.R` builds charts meant for
RStudio's Viewer, and `18_shiny_app.R` is a web app. Their drivers, `_drive_17_plotly.py` and
`_drive_18_shiny_app.py`, open them in Chromium, use them as you would, and take the screenshots.

Until October 2026 R could not be installed where this material is verified, and these scripts
were desk-checked only, with the numbers in their comments taken from the Python equivalents.
Running them found four comments whose numbers R does not give, in experiments 4, 10, 13 and 16;
each is corrected, with a note in the file and on this page.

What the Python side buys you: **the same calculation, done a second way.** When
`04_regression.R` says the slope is 4.3030, R prints it, and
`04_regression.py` computes it again from the sums, asserts it, and cross-checks it against
Statistical Foundations for Data Science Unit 4, where the same data was worked by hand.

```bash
python3 tools/data-science/run_r_equivalents.py
```

That runs all 14 Python equivalents and 17 of the R scripts (the Shiny app is a server, which
`capture_lab_outputs.py` runs instead), and checks all 18 for balanced delimiters.

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

## Experiment 1 — Mean, median, mode, variance, SD

### 1. Question

Find the mean, median, mode, variance and standard deviation of twenty students' marks.

### 2. Aim

Describe the centre and the spread of a set of marks in R, and know which variance R gives.

### 3. Steps

**In R**, `01_descriptive.R`:

1. **Enter the marks.**
2. **Find the centre: mean, median and mode.**
3. **Measure the spread: variance, SD, range and quartiles.**
4. **Convert to the population variance.**
5. **Summarise everything at once.**

**In Python**, `python/01_descriptive.py`:

1. **Compute the centre and the spread.**
2. **Print them, against the R function for each.**
3. **Check them against the statistics module.**

<div class="formula" markdown="1">
<span class="label">SAMPLE OR POPULATION</span>

R's `var()` and `sd()` divide by **n − 1**: they are the *sample* versions. For the
population variance, multiply by (n − 1)/n, as the script does. R also has no function for the
statistical mode — `mode()` reports how a value is stored — so the script writes one.
</div>


### 4. Programme

**In R**, `01_descriptive.R`:

{{programme: course-6-r/01_descriptive.R}}

**In Python**, `python/01_descriptive.py`:

{{programme: course-6-r/python/01_descriptive.py}}

### 5. Execution and Results

**In R**, `01_descriptive.R`:

{{output: course-6-r/01_descriptive.R}}

**In Python**, `python/01_descriptive.py`:

{{output: course-6-r/python/01_descriptive.py}}

Every one of the twenty marks occurs once, so the mode function rightly returns all
twenty. The Python equivalent gets the same mean, 70.05, and the same sample variance,
202.8921.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The mean is 70.05 and the median 70; there is no single mode. The sample variance is 202.89 and the SD 14.24; the population variance is 192.75 and its SD 13.88.
</div>


## Experiment 2 — Binomial, normal, Poisson

### 1. Question

Plot the Binomial(10, 0.3), Poisson(3) and Normal(100, 15) distributions, and find probabilities from each.

### 2. Aim

Draw three distributions in R, and find their probabilities with the d, p and q functions.

### 3. Steps

**In R**, `02_distributions.R`:

1. **Plot Binomial(10, 0.3), and find P(X = 3) and P(X <= 3).**
2. **Plot Poisson(3), and find P(X = 3) and P(X <= 3).**
3. **Plot Normal(100, 15), and find the areas within 1, 2 and 3 SD.**

**In Python**, `python/02_distributions.py`:

1. **Tabulate Binomial(10, 0.3).**
2. **Tabulate Poisson(3).**
3. **Find the normal's areas within 1, 2 and 3 SD.**
4. **Check the figures the R comments quote.**

<div class="formula" markdown="1">
<span class="label">THE D/P/Q/R NAMING CONVENTION</span>

Worth memorising once, because it applies to every distribution in R:

| Prefix | Gives | Example |
|---|---|---|
| `d` | density / PMF | `dbinom(3, 10, 0.3)` = 0.2668 |
| `p` | cumulative (CDF) | `pbinom(3, 10, 0.3)` = 0.6496 |
| `q` | quantile (inverse) | `qnorm(0.95, 100, 15)` = 124.67 |
| `r` | random generation | `rnorm(100, 100, 15)` |
</div>


### 4. Programme

**In R**, `02_distributions.R`:

{{programme: course-6-r/02_distributions.R}}

**In Python**, `python/02_distributions.py`:

{{programme: course-6-r/python/02_distributions.py}}

### 5. Execution and Results

**In R**, `02_distributions.R`:

{{output: course-6-r/02_distributions.R}}

**In Python**, `python/02_distributions.py`:

{{output: course-6-r/python/02_distributions.py}}

The three plots are the binomial's and the Poisson's bar charts and the normal curve.
The areas within 1, 2 and 3 SD are 0.6827, 0.9545 and 0.9973: the 68–95–99.7 rule.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

P(X = 3) is 0.2668 for the binomial and 0.2240 for the Poisson; P(X ≤ 3) is 0.6496 and 0.6472. For the normal, P(X ≤ 115) = 0.8413, and the 95th percentile is 124.67.
</div>


## Experiment 3 — t-test and chi-square

### 1. Question

Test whether two groups' mean scores differ, by the t-test, and whether region and purchase type are associated, by the chi-square test.

### 2. Aim

Run the t-test in its variants and the chi-square test of independence in R, and read their output.

### 3. Steps

**In R**, `03_hypothesis_tests.R`:

1. **Enter the two groups.**
2. **Run the pooled two-sample t-test.**
3. **Run Welch's test, and check the equal-variance assumption.**
4. **Run the one-sample and paired t-tests.**
5. **Test region against purchase type by chi-square.**
6. **Check the expected counts and the residuals.**

**In Python**, `python/03_hypothesis_tests.py`:

1. **Run the pooled two-sample t-test.**
2. **Run the chi-square test.**
3. **Check against Course 4 Unit 5.**

<div class="formula" markdown="1">
<span class="label">VAR.EQUAL CHANGES THE TEST</span>

`t.test(a, b, var.equal = TRUE)` is the **pooled** t-test from Statistical Foundations for Data Science Unit 5.
Omit it and R runs **Welch's** test, which does not assume equal variances and
reports fractional degrees of freedom. Both are defensible; know which you ran.
Check the assumption first with `var.test()` — on the lab data it gives
F = 1.8618, p = 0.3682, so equal variances are reasonable.
</div>


### 4. Programme

**In R**, `03_hypothesis_tests.R`:

{{programme: course-6-r/03_hypothesis_tests.R}}

**In Python**, `python/03_hypothesis_tests.py`:

{{programme: course-6-r/python/03_hypothesis_tests.py}}

### 5. Execution and Results

**In R**, `03_hypothesis_tests.R`:

{{output: course-6-r/03_hypothesis_tests.R}}

**In Python**, `python/03_hypothesis_tests.py`:

{{output: course-6-r/python/03_hypothesis_tests.py}}

The pooled test has 18 degrees of freedom and Welch's 16.503: the same t, 4.7541, read
against a slightly different distribution. The chi-square test's expected counts are all 33.33
or 66.67, so none is below 5.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The two means, 81.2 and 73.5, differ significantly (t = 4.7541, df = 18, p = 0.00016). Region and purchase type are associated (χ² = 9.75, df = 2, p = 0.0076).
</div>


## Experiment 4 — Correlation and regression

### 1. Question

Find the correlation between study hours and exam scores, fit a regression line, and predict the score for 7.5 hours.

### 2. Aim

Fit and read a simple linear regression in R with `lm()`.

### 3. Steps

**In R**, `04_regression.R`:

1. **Enter the hours and scores.**
2. **Measure the correlation, and plot the points.**
3. **Fit the regression line.**
4. **Use the model: coefficients, intervals, a prediction, residuals.**
5. **Read the ANOVA table.**

**In Python**, `python/04_regression.py`:

1. **Compute r, the line and the ANOVA from the sums.**
2. **Print the results.**
3. **Check that R-squared = r^2 and F = t^2.**

<div class="formula" markdown="1">
<span class="label">TWO FREE CHECKS</span>

For a simple regression, R² is the square of r, and the F statistic is the square of the
slope's t. Both hold here: 0.997904² = 0.995812, and 43.615² = 1902.26.
</div>


### 4. Programme

**In R**, `04_regression.R`:

{{programme: course-6-r/04_regression.R}}

**In Python**, `python/04_regression.py`:

{{programme: course-6-r/python/04_regression.py}}

### 5. Execution and Results

**In R**, `04_regression.R`:

{{output: course-6-r/04_regression.R}}

**In Python**, `python/04_regression.py`:

{{output: course-6-r/python/04_regression.py}}

**Corrected:** the comment under `summary(model)` gave the intercept's standard error as
1.0847, and its t as 39.671. R prints 0.70111 and 61.38, and by hand
SE = 0.8961 × √(1/10 + 6.5²/82.5) = 0.7011. The slope's figures were right. The second plot is the
four diagnostic plots, from `plot(model)`.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

r = 0.9979, and the fitted line is score = 43.0303 + 4.3030 × hours, with R² = 0.9958. At 7.5 hours it predicts 75.30.
</div>


## Experiment 5 — EDA on a real dataset

### 1. Question

Explore a dataset: its structure, summary statistics, missing values, categories, distributions, outliers and correlations.

### 2. Aim

Carry out the steps of exploratory data analysis in R, on the iris data.

### 3. Steps

**In R**, `05_eda.R`:

1. **Load the data.**
2. **Look at its structure and summary.**
3. **Check for missing values.**
4. **Count the categories.**
5. **Plot the distributions, and find the outliers.**
6. **Find the correlations.**
7. **Judge the skew from the mean and median.**

**In Python**, `python/05_eda.py`:

1. **Show the structure.**
2. **Summarise the numeric columns.**
3. **Count the missing values and the categories.**
4. **Draw a text histogram, and find the outliers.**
5. **Find the correlation.**

### 4. Programme

**In R**, `05_eda.R`:

{{programme: course-6-r/05_eda.R}}

**In Python**, `python/05_eda.py`:

{{programme: course-6-r/python/05_eda.py}}

### 5. Execution and Results

**In R**, `05_eda.R`:

{{output: course-6-r/05_eda.R}}

**In Python**, `python/05_eda.py`:

{{output: course-6-r/python/05_eda.py}}

The R script uses R's built-in `iris` data; the Python equivalent, which has no `iris`
without a package, explores the ten students the other experiments use. The four plots are the
histogram, the boxplot by species, the boxplot of all sepal lengths, and the scatterplot matrix.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

iris has 150 rows and 5 columns, no missing values, and 50 flowers of each species. Petal length and width are the most correlated (0.963). Sepal length's mean, 5.843, is just above its median, 5.8: a slight right skew.
</div>


## Experiment 6 — Feature engineering

### 1. Question

Normalise, standardise, encode and bin a column of marks and a column of sections.

### 2. Aim

Prepare features for modelling in R: scale them, encode categories, and bin a number.

### 3. Steps

**In R**, `06_feature_engineering.R`:

1. **Enter the marks and sections.**
2. **Normalise to [0, 1] by min-max.**
3. **Standardise to mean 0 and SD 1.**
4. **One-hot encode the sections.**
5. **Encode an ordered category, and avoid the factor trap.**
6. **Bin the marks into classes.**

**In Python**, `python/06_feature_engineering.py`:

1. **Normalise by min-max.**
2. **Standardise.**
3. **One-hot encode.**
4. **Bin the marks.**
5. **Check the ranges.**

<div class="formula" markdown="1">
<span class="label">R AND PYTHON SCALE DIFFERENTLY</span>

`scale()` uses `sd()`, which divides by **n−1**. scikit-learn's
`StandardScaler` divides by **n**. The standardised values therefore differ
slightly between R and scikit-learn. Harmless for modelling,
but do not expect identical numbers, and say so if asked.
</div>


### 4. Programme

**In R**, `06_feature_engineering.R`:

{{programme: course-6-r/06_feature_engineering.R}}

**In Python**, `python/06_feature_engineering.py`:

{{programme: course-6-r/python/06_feature_engineering.py}}

### 5. Execution and Results

**In R**, `06_feature_engineering.R`:

{{output: course-6-r/06_feature_engineering.R}}

**In Python**, `python/06_feature_engineering.py`:

{{output: course-6-r/python/06_feature_engineering.py}}

**Corrected:** this note said the standardised values differ between the R script and its
Python equivalent. The Python equivalent divides by n − 1, as R does, so they agree: 85 becomes
0.9185 in both. It is scikit-learn's `StandardScaler` that would differ.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Min-max puts the marks in [0, 1]; standardising gives mean 0 and SD 1 (R's mean is 3.5 × 10⁻¹⁶, zero to rounding). One-hot encoding gives three columns, or two with an intercept, and binning gives Pass 2, Second 1, First 3 and Distinction 4.
</div>


## Experiment 7 — Variables, control structures, functions

### 1. Question

Use R's variable types, vectors, control structures, apply family and functions.

### 2. Aim

Write R's basic constructs, and see where R differs from other languages.

### 3. Steps

1. **Make a variable of each type.**
2. **Index and compute on vectors.**
3. **Branch with if and ifelse().**
4. **Loop with for, while and repeat.**
5. **Apply a function across a matrix or a list.**
6. **Write functions, with default and variadic arguments.**

### 4. Programme

{{programme: course-6-r/07_r_basics.R}}

### 5. Execution and Results

{{output: course-6-r/07_r_basics.R}}

Two of R's habits show in the output: indexing starts at 1, so `v[1]` is 10, and `v[-1]`
leaves the first element out rather than taking the last.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The vector operations, branches, loops and functions all behave as their comments say: `grade(85)` is "B", and `total(1, 2, 3, 4)` is 10.
</div>


## Experiment 8 — CSV, Excel, JSON, XML

### 1. Question

Read and write data as CSV, Excel, JSON and XML files.

### 2. Aim

Move a data frame in and out of R in each common file format.

### 3. Steps

**In R**, `08_file_io.R`:

1. **Make a small data frame.**
2. **Write and read CSV.**
3. **Load the Excel packages.**
4. **Write and read JSON.**
5. **Load the XML package.**
6. **Save and load R's own formats.**

**In Python**, `python/08_file_io.py`:

1. **Write and read back CSV, JSON and XML.**
2. **Compare the types that come back.**

### 4. Programme

**In R**, `08_file_io.R`:

{{programme: course-6-r/08_file_io.R}}

**In Python**, `python/08_file_io.py`:

{{programme: course-6-r/python/08_file_io.py}}

### 5. Execution and Results

**In R**, `08_file_io.R`:

{{output: course-6-r/08_file_io.R}}

**In Python**, `python/08_file_io.py`:

{{output: course-6-r/python/08_file_io.py}}

The Excel and XML reads and writes are comments in the file, as the steps say: only their
packages are loaded. JSON brings the marks back as numbers; CSV and XML bring everything back as
text, as the Python equivalent shows.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The data frame is written and read back unchanged as CSV, JSON and R's own formats.
</div>


## Experiment 9 — dplyr and tidyr

### 1. Question

Filter, select, create, sort, summarise, join and reshape a table of students.

### 2. Aim

Wrangle data with dplyr's verbs and tidyr's pivots.

### 3. Steps

**In R**, `09_wrangling.R`:

1. **Make the students data frame.**
2. **Filter, select, mutate and arrange in one pipe.**
3. **Summarise by section.**
4. **Count, find distinct values, take the top three, rename.**
5. **Join to the teachers table.**
6. **Reshape from wide to long and back.**

**In Python**, `python/09_wrangling.py`:

1. **Filter, select, mutate and arrange.**
2. **Group and summarise.**
3. **Pivot longer and wider.**
4. **Check the shapes.**

### 4. Programme

**In R**, `09_wrangling.R`:

{{programme: course-6-r/09_wrangling.R}}

**In Python**, `python/09_wrangling.py`:

{{programme: course-6-r/python/09_wrangling.py}}

### 5. Execution and Results

**In R**, `09_wrangling.R`:

{{output: course-6-r/09_wrangling.R}}

**In Python**, `python/09_wrangling.py`:

{{output: course-6-r/python/09_wrangling.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Seven students scored over 60; section B has the highest average, 78. Section D has no students, so `anti_join()` returns it, and the wide table of 2 students becomes 6 rows when made long.
</div>


## Experiment 10 — Missing data and outliers

### 1. Question

Find the missing values and the outliers in a column of marks, and handle them.

### 2. Aim

Detect and impute missing values, and find outliers by the IQR and z-score rules.

### 3. Steps

**In R**, `10_missing_outliers.R`:

1. **Enter the data, with missing values and an outlier.**
2. **Find the missing values.**
3. **Impute them by the mean or the median.**
4. **Find outliers by the IQR rule.**
5. **Find outliers by the z-score rule.**
6. **Add a second outlier, and see masking.**

**In Python**, `python/10_missing_outliers.py`:

1. **Find the missing values.**
2. **Compare mean and median imputation.**
3. **Find outliers by the IQR rule.**
4. **Find outliers by the z-score rule.**
5. **Add a second outlier, and see masking.**

<div class="formula" markdown="1">
<span class="label">MASKING, WHICH THE LAB ACTUALLY DEMONSTRATES</span>

Both the IQR and z-score rules catch a single outlier of 250. Add a second at
260 and the standard deviation inflates from 46.40 to 61.97 — enough that the
z-score rule flags **nothing**, while the IQR rule still catches both.

That is **masking**, and it is why the IQR rule is preferred when outliers may
cluster. The Python equivalent asserts this, so the claim is tested rather than
asserted.
</div>


### 4. Programme

**In R**, `10_missing_outliers.R`:

{{programme: course-6-r/10_missing_outliers.R}}

**In Python**, `python/10_missing_outliers.py`:

{{programme: course-6-r/python/10_missing_outliers.py}}

### 5. Execution and Results

**In R**, `10_missing_outliers.R`:

{{output: course-6-r/10_missing_outliers.R}}

**In Python**, `python/10_missing_outliers.py`:

{{output: course-6-r/python/10_missing_outliers.py}}

**Corrected:** the comments gave the mean and median, without the missing values, as 79.06
and 68.00. R and the Python equivalent both give 79.35 and 69.00.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

3 of the 20 values (15%) are missing. Median imputation, 69, is the safer choice, as the 250 pulls the mean up to 79.35. Both rules find the 250 (fences 22 and 118; z = 3.677); with a second outlier, only the IQR rule finds them.
</div>


## Experiment 11 — Dates and times

### 1. Question

Parse, format, take apart and do arithmetic on dates, and sort them.

### 2. Aim

Handle dates in base R and with lubridate, and see why dates must not be stored as text.

### 3. Steps

**In R**, `11_dates.R`:

1. **Make dates in base R, and format them.**
2. **Do arithmetic on dates.**
3. **Do the same with lubridate.**
4. **Sort dates as text and as dates.**

**In Python**, `python/11_dates.py`:

1. **Parse the dates.**
2. **Take a date apart.**
3. **Do arithmetic on dates.**
4. **Format them.**
5. **Sort dates as text and as dates.**

### 4. Programme

**In R**, `11_dates.R`:

{{programme: course-6-r/11_dates.R}}

**In Python**, `python/11_dates.py`:

{{programme: course-6-r/python/11_dates.py}}

### 5. Execution and Results

**In R**, `11_dates.R`:

{{output: course-6-r/11_dates.R}}

**In Python**, `python/11_dates.py`:

{{output: course-6-r/python/11_dates.py}}

The first two lines are today's date and time: the output shown was made with the clock set
to 4 October 2026, 12:00 UTC.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

26 August 2026 is a Wednesday, and 121 days before Christmas. Sorted as text, 21/12/2025 comes last; sorted as dates, first.
</div>


## Experiment 12 — ggplot2

### 1. Question

Draw a scatter plot, a bar chart, a column chart, a histogram and boxplots of the students' data with ggplot2.

### 2. Aim

Build charts with ggplot2's grammar of layers.

### 3. Steps

1. **Make the students data frame.**
2. **Draw a scatter plot with a fitted line.**
3. **Draw a bar chart of counts.**
4. **Draw a column chart of means.**
5. **Draw a histogram.**
6. **Draw boxplots, split by gender.**
7. **Save a plot as PNG and PDF.**

### 4. Programme

{{programme: course-6-r/12_ggplot.R}}

### 5. Execution and Results

{{output: course-6-r/12_ggplot.R}}

The five plots are in the order the script draws them. The one line it prints is ggplot2's
note that `geom_smooth()` fitted a straight line. The two saved files, `marks_plot.png` and
`marks_plot.pdf`, are not shown.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

All five charts draw; `geom_bar()` counts the students in each section, and `geom_col()` plots the mean marks given to it.
</div>


## Experiment 13 — K-Means clustering

### 1. Question

Segment 60 customers into three clusters by income and age.

### 2. Aim

Cluster with K-Means in R, choose k, and see why the data must be scaled first.

### 3. Steps

**In R**, `13_kmeans.R`:

1. **Make the customer data, after setting the seed.**
2. **Scale it, and cluster into three.**
3. **Read the clusters.**
4. **Profile the clusters, and plot them.**
5. **Choose k by the elbow method.**
6. **Cluster without scaling, and compare.**

**In Python**, `python/13_kmeans.py`:

1. **Make the customer data, from a seeded generator.**
2. **Cluster without scaling.**
3. **Cluster with scaling.**
4. **Choose k by the elbow method.**
5. **Compare the two clusterings, and the variances.**

<div class="formula" markdown="1">
<span class="label">SCALING IS THE WHOLE EXPERIMENT</span>

The lab data has an income:age variance ratio of about **3.5 billion to 1**.
Without `scale()`, K-Means clusters on income alone and age contributes nothing
measurable. Run it both ways and compare `table(km$cluster, km_raw$cluster)` —
seeing the two solutions disagree is more convincing than being told they will.
</div>


### 4. Programme

**In R**, `13_kmeans.R`:

{{programme: course-6-r/13_kmeans.R}}

**In Python**, `python/13_kmeans.py`:

{{programme: course-6-r/python/13_kmeans.py}}

### 5. Execution and Results

**In R**, `13_kmeans.R`:

{{output: course-6-r/13_kmeans.R}}

**In Python**, `python/13_kmeans.py`:

{{output: course-6-r/python/13_kmeans.py}}

Here the two solutions disagree on 2 of the 60 customers: the income groups are far enough
apart that income alone nearly finds them. **Corrected:** the ratio was given as 4 billion. R's
data gives 3.48 billion; the Python equivalent's own random data gives 4.36 billion.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The three clusters have 20, 18 and 22 customers, and explain 85% of the variance. They average about 3.1, 15.0 and 9.4 lakh rupees, at ages 29, 37 and 46.
</div>


## Experiment 14 — Confusion matrix, accuracy, ROC

### 1. Question

Evaluate a classifier from its confusion matrix (TP 80, FP 20, FN 40, TN 860), and draw an ROC curve.

### 2. Aim

Compute and read a classifier's metrics with caret and pROC, and see the accuracy paradox.

### 3. Steps

**In R**, `14_evaluation.R`:

1. **Make the actual and predicted labels.**
2. **Build the confusion matrix and its metrics.**
3. **Make scores for the ROC curve.**
4. **Draw the ROC curve, and find the AUC.**
5. **Find the best threshold.**

**In Python**, `python/14_evaluation.py`:

1. **Make the labels from the Unit 4 counts.**
2. **Build the confusion matrix and its metrics.**
3. **Compare with the trivial baseline.**
4. **Make scores, and find the AUC.**
5. **Check against Unit 4 Problem 1.**

### 4. Programme

**In R**, `14_evaluation.R`:

{{programme: course-6-r/14_evaluation.R}}

**In Python**, `python/14_evaluation.py`:

{{programme: course-6-r/python/14_evaluation.py}}

### 5. Execution and Results

**In R**, `14_evaluation.R`:

{{output: course-6-r/14_evaluation.R}}

**In Python**, `python/14_evaluation.py`:

{{output: course-6-r/python/14_evaluation.py}}

Accuracy, 0.94, beats always predicting "healthy", 0.88, by only 0.06, and the model
misses 40 of the 120 real cases. The AUC is for scores simulated to separate the classes.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Accuracy 0.94, sensitivity (recall) 0.6667, specificity 0.9773, precision 0.80 and F1 0.7273. The AUC is 0.9633, and the best threshold is 0.519.
</div>


## Experiment 15 — Text mining and word cloud

### 1. Question

Clean five course reviews, count their terms, draw a word cloud, and weight the terms by TF-IDF.

### 2. Aim

Mine text in R with tm: clean it, build a term-document matrix, and weight it.

### 3. Steps

**In R**, `15_text_mining.R`:

1. **Enter the reviews.**
2. **Clean the text: case, punctuation, numbers, stop words, stems.**
3. **Count the terms.**
4. **Draw the word cloud and a bar chart.**
5. **Weight the terms by TF-IDF.**
6. **Find the frequent and the associated terms.**

**In Python**, `python/15_text_mining.py`:

1. **Clean the text.**
2. **Count the terms.**
3. **Build the term-document matrix.**
4. **Weight the terms by TF-IDF.**
5. **Check that a term in every document weighs zero.**

### 4. Programme

**In R**, `15_text_mining.R`:

{{programme: course-6-r/15_text_mining.R}}

**In Python**, `python/15_text_mining.py`:

{{programme: course-6-r/python/15_text_mining.py}}

### 5. Execution and Results

**In R**, `15_text_mining.R`:

{{output: course-6-r/15_text_mining.R}}

**In Python**, `python/15_text_mining.py`:

{{output: course-6-r/python/15_text_mining.py}}

The "transformation drops documents" warnings are tm's, printed each time `tm_map()` runs
on this kind of corpus; nothing is dropped, and the matrix still has all 5 documents. Stemming
turns "excellent" into "excel", which is why "excel" is a frequent term.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The most frequent stems are cours (5), data, excel and practic (4 each). "cours" is in every review, so its TF-IDF weight is zero.
</div>


## Experiment 16 — ARIMA forecasting

### 1. Question

Model the monthly airline passenger series, 1949–1960, and forecast it two years ahead.

### 2. Aim

Decompose, difference, identify, fit, check and forecast a seasonal series with ARIMA in R.

### 3. Steps

**In R**, `16_arima.R`:

1. **Load and plot the series, and take logs.**
2. **Decompose it.**
3. **Test for stationarity.**
4. **Difference it.**
5. **Read the ACF and PACF.**
6. **Fit the model.**
7. **Check the residuals.**
8. **Forecast two years ahead.**

**In Python**, `python/16_arima.py`:

1. **Make and show the series.**
2. **Find the trend by a moving average.**
3. **Difference it.**
4. **Read the ACF before and after differencing.**
5. **Read the PACF.**
6. **Check what the series must show.**

<div class="formula" markdown="1">
<span class="label">DIFFERENCE BEFORE YOU READ THE ACF</span>

On the raw airline series the ACF decays slowly — the trend dominates — and the
seasonality shows only as a ripple on that decay: it falls to 0.66 at lag 8 and rises again to
0.76 at lag 12. After one difference the oscillation stands out, peaking at lag 12 (0.83). Reading
ACF/PACF on a trending series tells you little except "there is a trend".
</div>


### 4. Programme

**In R**, `16_arima.R`:

{{programme: course-6-r/16_arima.R}}

**In Python**, `python/16_arima.py`:

{{programme: course-6-r/python/16_arima.py}}

### 5. Execution and Results

**In R**, `16_arima.R`:

{{output: course-6-r/16_arima.R}}

**In Python**, `python/16_arima.py`:

{{output: course-6-r/python/16_arima.py}}

**Corrected:** this note said the raw ACF shows no seasonality at all, the trend dominating
completely; so did the script's comment. That is true of the Python equivalent's series, not of
the airline data. Also corrected: the script's comment expected a large ADF p-value on the raw
series. `adf.test()` allows for a linear trend, and gives p below 0.01, while KPSS rejects a
constant level, also p below 0.01: the series is trend-stationary.

The script's ACF after differencing is of `d12`, after both the ordinary and the seasonal
difference. What is left is a spike at lag 1 (−0.34) and one at lag 12 (−0.39): the pattern of an
MA(1) and a seasonal MA(1) term, which is the model `auto.arima()` then picks.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

auto.arima() chooses ARIMA(0,1,1)(0,1,1)[12] on the log series, with AIC −483.4. The Ljung-Box p of 0.233 leaves no pattern in the residuals, and the forecast for July 1962 is 738 thousand passengers.
</div>


## Experiment 17 — Interactive plots with plotly

### 1. Question

Make the students' charts interactive with plotly.

### 2. Aim

Make a ggplot2 chart interactive, and draw plotly charts directly.

### 3. Steps

1. **Make the students data frame.**
2. **Make a ggplot2 chart interactive.**
3. **Draw a native plotly scatter, with hover text.**
4. **Draw a bar chart of the means.**

### 4. Programme

{{programme: course-6-r/17_plotly.R}}

### 5. Execution and Results

{{output: course-6-r/17_plotly.R}}

The screenshots are the three charts, in order, and the second again with the pointer over
a point, showing its hover text. R itself prints only the packages' start-up messages.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

All three charts draw, and hovering over Ananya's point shows "Name: Ananya, Marks: 85": the hover text the script builds.
</div>


## Experiment 18 — Shiny app with CSV upload

### 1. Question

Build a Shiny app that lets a user upload a CSV file and explore it.

### 2. Aim

Write a Shiny app with an upload, a reactive data source and three output tabs.

### 3. Steps

1. **Lay out the page: the upload, the options and three tabs.**
2. **Read the uploaded file once, in a reactive.**
3. **Build the column picker from the file.**
4. **Fill the data, summary and plot tabs.**
5. **Run the app.**

<div class="formula" markdown="1">
<span class="label">THE THREE SHINY RULES</span>

1. **Call a reactive with parentheses** — `data()`, never `data`.
2. **`input$x` only inside a reactive context** — `reactive()`, `observe()` or
   `render*()`.
3. **Output IDs must match** between `ui` and `server`. A typo gives a blank
   panel and **no error message**, so check spelling first.

`req(input$file)` is the idiomatic way to wait for an upload — it silently
pauses the reactive rather than erroring on `NULL`.
</div>


### 4. Programme

{{programme: course-6-r/18_shiny_app.R}}

### 5. Execution and Results

{{output: course-6-r/18_shiny_app.R}}

Before the upload the Data tab is empty: `req()` holds every output back. The summary is
R's `summary()` of the uploaded file, printed by the app.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The app reads the uploaded file, lists its two numeric columns, summarises it, and redraws the histogram when the column or the number of bins changes.
</div>


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
