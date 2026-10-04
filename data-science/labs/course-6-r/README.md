# Lab overview — R and the Python equivalents

**18 practicals**

## Two versions of every experiment

| Directory | Language | Status |
|---|---|---|
| this one | **R** — as the exam tests it | ✅ **Executed** with R 4.3.3 |
| `python/` | Python equivalents | ✅ **Executed and verified** |

Every R script is run with R 4.3.3, and the lab page shows what each printed and
the plots it drew; `17_plotly.R`'s charts and `18_shiny_app.R` are opened in
Chromium by their drivers, `_drive_17_plotly.py` and `_drive_18_shiny_app.py`.
Until October 2026 R could not be installed where this material is verified,
and the scripts were desk-checked only. Running them found four comments whose
numbers R does not give (in `04_regression.R`, `10_missing_outliers.R`,
`13_kmeans.R` and `16_arima.R`); each is corrected, with a note.

What the Python equivalents buy you: the **same calculation done a second way**.
When `02_distributions.R` says a Binomial(10, 0.3) has mean 3 and variance 2.1,
`python/02_distributions.py` computes it from the formula, and asserts it.

Run both sides yourself (it runs the R scripts too, if `Rscript` is installed):

```bash
pip install -r tools/data-science/requirements.txt
python3 tools/data-science/run_r_equivalents.py
```

Or run one R script, as the exam will, in RStudio or with
`Rscript 04_regression.R`.

## The experiments

| # | Experiment | R | Python |
|:---:|---|---|---|
| 1 | Mean, median, mode, variance, SD | `01_descriptive.R` | `python/01_descriptive.py` |
| 2 | Visualise binomial, normal, Poisson | `02_distributions.R` | `python/02_distributions.py` |
| 3 | t-test and chi-square test | `03_hypothesis_tests.R` | `python/03_hypothesis_tests.py` |
| 4 | Correlation and simple linear regression | `04_regression.R` | `python/04_regression.py` |
| 5 | EDA on a real dataset | `05_eda.R` | `python/05_eda.py` |
| 6 | Feature engineering — scaling, encoding | `06_feature_engineering.R` | `python/06_feature_engineering.py` |
| 7 | Variables, control structures, functions | `07_r_basics.R` | — *(syntax demo)* |
| 8 | Read/write CSV, Excel, JSON, XML | `08_file_io.R` | `python/08_file_io.py` |
| 9 | Wrangling with dplyr and tidyr | `09_wrangling.R` | `python/09_wrangling.py` |
| 10 | Missing data and outliers | `10_missing_outliers.R` | `python/10_missing_outliers.py` |
| 11 | Dates and times | `11_dates.R` | `python/11_dates.py` |
| 12 | ggplot2 — bar, scatter, histogram, boxplot | `12_ggplot.R` | — *(plotting)* |
| 13 | K-Means clustering | `13_kmeans.R` | `python/13_kmeans.py` |
| 14 | Confusion matrix, accuracy, ROC | `14_evaluation.R` | `python/14_evaluation.py` |
| 15 | Text mining and word cloud | `15_text_mining.R` | `python/15_text_mining.py` |
| 16 | ARIMA forecasting | `16_arima.R` | `python/16_arima.py` |
| 17 | Interactive plots with plotly | `17_plotly.R` | — *(plotting)* |
| 18 | Shiny app with CSV upload | `18_shiny_app.R` | — *(web app)* |

Experiments 7, 12, 17 and 18 have no Python equivalent because they demonstrate
R *syntax*, R *plotting* or the Shiny *framework* — a translation would teach
nothing.

## Setting up R on your own machine

```r
install.packages(c("tidyverse", "readxl", "jsonlite", "XML",
                   "forecast", "tseries", "plotly", "shiny",
                   "tm", "wordcloud", "caret", "pROC"))
```

`tidyverse` brings `dplyr`, `tidyr`, `ggplot2`, `readr` and `lubridate` in one
install.
