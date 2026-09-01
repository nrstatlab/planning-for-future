# Course 4 Lab — Excel / PSPP walkthroughs

The official lab is headed **"Advanced Spreadsheets/Excel
Lab/PSPP Open Source"**. All 15 experiments are spreadsheet exercises, and the
practical exam tests them in a spreadsheet — so learn these first.

Then do each one again in Python. See
[`SYLLABUS-REVIEW.md`](../../SYLLABUS-REVIEW.md) finding **D8**: this lab never
touches Python even though Python is taught in the same semester, and that gap
is worth closing yourself. The Python versions live in
`python/` and every number below was cross-checked against them.

> **Experiment 2 is reconstructed.** The official text survives only as the
> fragment "a positive result." — see review findings **D1** and **D3**.

**Before you start:** turn on the Analysis ToolPak, which several experiments
need. File → Options → Add-ins → Manage: Excel Add-ins → Go → tick *Analysis
ToolPak*. In LibreOffice the equivalents live under Data → Statistics.

---

## Experiment 1 — Contingency table and conditional probability

**Task:** build a contingency table from sales data, compute conditional
probabilities, and check whether the variables are independent.

1. Enter the raw data in columns: `Region` in A, `Purchase` in B.
2. Select the range, then **Insert → PivotTable**.
3. Drag `Region` to Rows, `Purchase` to Columns, and `Purchase` to Values
   (set it to **Count**). That is your contingency table.
4. Add the margins: **Design → Grand Totals → On for Rows and Columns**.
5. Joint probability of each cell: `=cell / $grand_total$` — anchor the grand
   total with `$` so it does not shift when you fill across.
6. Conditional probability P(Premium | North): `=cell / row_total`.
7. **Independence check.** In a spare block compute `=row_total*col_total/grand_total`
   for each cell. If those expected values match the observed counts, the
   variables are independent. They rarely do exactly — Experiment 15's
   chi-square test tells you whether the gap is bigger than chance.

**Key formulas:** `COUNTIFS(A:A,"North",B:B,"Premium")` gives one cell directly
without a pivot table.

---

## Experiment 2 — Bayes' theorem *(reconstructed)*

**Task (reconstructed):** a disease affects 1% of the population. A test is 99%
sensitive and 95% specific. Given a positive result, what is the probability
the person has the disease?

Lay it out as a table:

| Cell | Formula | Value |
|---|---|---|
| B1 `P(D)` | typed | `0.01` |
| B2 `P(not D)` | `=1-B1` | `0.99` |
| B3 `P(+ \| D)` sensitivity | typed | `0.99` |
| B4 `P(- \| not D)` specificity | typed | `0.95` |
| B5 `P(+ \| not D)` | `=1-B4` | `0.05` |
| B6 `P(+)` | `=B3*B1+B5*B2` | `0.0594` |
| B7 **`P(D \| +)`** | `=B3*B1/B6` | **`0.1667`** |

**The point:** a 99%-sensitive test, yet a positive result means only a **16.7%**
chance of having the disease. Out of 10,000 people, 99 true positives are
swamped by 495 false positives. Confusing P(D|+) with P(+|D) is the **base rate
fallacy** and it is the most examined idea in this part of the syllabus.

Build the 10,000-person table in the sheet — it makes the result obvious.

---

## Experiment 3 — Measures of central tendency

Marks in `A2:A21`.

| Measure | Formula |
|---|---|
| Mean | `=AVERAGE(A2:A21)` |
| Median | `=MEDIAN(A2:A21)` |
| Mode | `=MODE.SNGL(A2:A21)` (single) or `=MODE.MULT(A2:A21)` (several) |
| Count | `=COUNT(A2:A21)` |

**Then demonstrate why it matters:** add one mark of 500 in `A22` and watch the
mean lurch while the median barely moves. Write that comparison in the sheet —
it is the interpretation marks, not the formula, that examiners reward.

`MODE.SNGL` returns `#N/A` when every value is unique. That is correct
behaviour, not an error to hide — say "no mode" in your answer.

---

## Experiment 4 — Measures of dispersion

| Measure | Formula | Note |
|---|---|---|
| Range | `=MAX(A2:A21)-MIN(A2:A21)` | |
| Q1 | `=QUARTILE.INC(A2:A21,1)` | |
| Q3 | `=QUARTILE.INC(A2:A21,3)` | |
| IQR | `=QUARTILE.INC(A2:A21,3)-QUARTILE.INC(A2:A21,1)` | |
| **Sample** variance | `=VAR.S(A2:A21)` | divides by n−1 |
| **Population** variance | `=VAR.P(A2:A21)` | divides by n |
| **Sample** sd | `=STDEV.S(A2:A21)` | |
| **Population** sd | `=STDEV.P(A2:A21)` | |
| Coefficient of variation | `=STDEV.S(A2:A21)/AVERAGE(A2:A21)` | format as % |

**`.S` or `.P` is the decision that costs marks.** Use `.S` when your data is a
sample from a larger population — which it almost always is in these exercises.
Using `.P` on a sample understates the spread.

**Outlier fences:** `=Q1-1.5*IQR` and `=Q3+1.5*IQR`, then flag values outside
them with conditional formatting.

---

## Experiment 5 — Histogram

1. Create a bin column, e.g. `40, 50, 60, 70, 80, 90, 100` in `C2:C8`.
2. **Data → Data Analysis → Histogram**. Input range `A2:A21`, bin range
   `C2:C8`, tick *Chart Output*.
3. Right-click the bars → **Format Data Series → Gap Width = 0**. Histogram bars
   must touch; that is what distinguishes a histogram from a bar chart.

**Comment on the shape** — the question asks for it:

- `mean > median` → tail to the right, **positively skewed**
- `mean < median` → tail to the left, **negatively skewed**
- `mean ≈ median ≈ mode` → symmetric

Quantify it: `=3*(AVERAGE(range)-MEDIAN(range))/STDEV.S(range)` is Pearson's
skewness coefficient. Excel also has `=SKEW(range)`.

---

## Experiment 6 — Bar chart of categorical data

1. Build a two-way count with `COUNTIFS`, e.g.
   `=COUNTIFS($A:$A,$E2,$B:$B,F$1)` filled across a small grid.
2. Select the grid → **Insert → Column Chart → Clustered Column**.
3. Add axis titles, a legend and a chart title. Marks are given for labelling.

**Histogram vs bar chart** — state the difference in your answer: a bar chart
shows *categories* with gaps between bars in any order; a histogram shows
*continuous* data in adjacent intervals with no gaps. Drawing the wrong one is
a routine way to lose marks.

---

## Experiment 7 — Scatter plot, correlation and covariance

Hours studied in `A`, exam score in `B`.

1. Select both columns → **Insert → Scatter (Markers only)**. Never join the
   points with lines.
2. Right-click a point → **Add Trendline** → Linear → tick *Display Equation*
   and *Display R-squared*.
3. Correlation: `=CORREL(A2:A11,B2:B11)` or `=PEARSON(A2:A11,B2:B11)`.
4. Covariance: `=COVARIANCE.S(A2:A11,B2:B11)` for a sample,
   `=COVARIANCE.P(...)` for a population.

**Interpretation, which is where the marks are:**

| \|r\| | Reading |
|---|---|
| 0.9 – 1.0 | very strong |
| 0.7 – 0.9 | strong |
| 0.4 – 0.7 | moderate |
| below 0.4 | weak |

Covariance tells you only the *direction*; its size depends on the units, so
converting hours to minutes multiplies it by 60. Correlation is unit-free and
bounded by ±1, which is why it is the one you report.

**Always add:** correlation is not causation.

---

## Experiment 8 — Simulating random variables

**Discrete:** `=RANDBETWEEN(1,6)` filled down 1000 rows simulates a die. Tally
with `=COUNTIF($A$2:$A$1001,D2)` and chart it.

**Continuous:** `=NORM.INV(RAND(),100,15)` draws from Normal(100, 15).

`RAND()` and `RANDBETWEEN()` are **volatile** — they recalculate on every edit.
To freeze a sample, copy the column and **Paste Special → Values**. Do this
before computing anything from it, or your statistics will change as you work.

---

## Experiment 9 — Expectation and variance

Values in `A`, probabilities in `B`.

1. First check `=SUM(B2:B6)` equals exactly 1. If not, stop — the data is wrong.
2. `C2: =A2*B2`, filled down. Then `E(X) = =SUM(C2:C6)`.
3. `D2: =A2^2*B2`, filled down. Then `E(X²) = =SUM(D2:D6)`.
4. `Var(X) = =SUM(D2:D6)-SUM(C2:C6)^2`
5. `SD(X) = =SQRT(variance)`

The shortcut **Var(X) = E(X²) − [E(X)]²** is faster than E[(X−μ)²] and gives an
identical answer. Use it under time pressure.

---

## Experiment 10 — Binomial and Poisson distributions

**Binomial**, n = 10, p = 0.3, with k in `A2:A12`:

- PMF `P(X = k)`: `=BINOM.DIST(A2,10,0.3,FALSE)`
- CDF `P(X ≤ k)`: `=BINOM.DIST(A2,10,0.3,TRUE)`
- Mean `=10*0.3`, variance `=10*0.3*0.7`

**Poisson**, λ = 3:

- PMF: `=POISSON.DIST(A2,3,FALSE)`
- CDF: `=POISSON.DIST(A2,3,TRUE)`
- Mean = variance = λ — that equality is the signature of a Poisson.

The last argument, `FALSE`/`TRUE`, switches between PMF and CDF. Getting it
backwards is the most common error in this experiment.

Chart both as column charts and describe the shapes: the binomial is symmetric
at p = 0.5 and skewed otherwise; the Poisson is right-skewed for small λ and
approaches a normal shape as λ grows.

---

## Experiment 11 — Normal and Exponential distributions

**Normal(100, 15):**

| Quantity | Formula |
|---|---|
| PDF | `=NORM.DIST(x,100,15,FALSE)` |
| CDF `P(X ≤ x)` | `=NORM.DIST(x,100,15,TRUE)` |
| `P(X > x)` | `=1-NORM.DIST(x,100,15,TRUE)` |
| `P(a ≤ X ≤ b)` | `=NORM.DIST(b,...,TRUE)-NORM.DIST(a,...,TRUE)` |
| Inverse (percentile) | `=NORM.INV(0.95,100,15)` |
| Standard normal | `=NORM.S.DIST(z,TRUE)`, `=NORM.S.INV(p)` |

**Verify the empirical rule** in the sheet: ±1 sd ≈ 68.27%, ±2 ≈ 95.45%,
±3 ≈ 99.73%.

**Exponential(λ = 0.5):** `=EXPON.DIST(x,0.5,FALSE)` for the PDF,
`TRUE` for the CDF. Mean = 1/λ, variance = 1/λ².

Demonstrate **memorylessness**: P(X > 5 | X > 2) = P(X > 3). Compute both
sides and show they match.

---

## Experiment 12 — Correlation analysis

Extends Experiment 7 with Spearman's rank correlation.

1. Pearson: `=CORREL(A2:A11,B2:B11)`.
2. Rank each column: `=RANK.AVG(A2,$A$2:$A$11,1)`. Use `RANK.AVG`, not `RANK`,
   so that ties get averaged ranks.
3. Spearman: `=CORREL(rank_x_range, rank_y_range)`, or use the formula
   `ρ = 1 − 6Σd² / n(n²−1)` where `d` is the difference in ranks.
4. For several variables at once: **Data → Data Analysis → Correlation** builds
   the whole correlation matrix.

**When to use which:** Pearson measures *linear* association and assumes roughly
normal data. Spearman works on ranks, so it catches any *monotonic*
relationship and shrugs off outliers.

---

## Experiment 13 — Linear regression

1. **Data → Data Analysis → Regression**.
2. Input Y range = scores, Input X range = hours, tick *Labels*, *Residuals*
   and *Line Fit Plots*.
3. Read the output:

| Output | Meaning |
|---|---|
| `Multiple R` | \|r\|, the correlation |
| `R Square` | fraction of variance in y explained by x |
| `Adjusted R Square` | R² penalised for extra predictors |
| `Standard Error` | typical size of a residual |
| `Coefficients: Intercept` | b₀ |
| `Coefficients: X Variable 1` | b₁, the slope |
| `Significance F` / `P-value` | tests whether the slope is really non-zero |

**Formula shortcuts:** `=SLOPE(y,x)`, `=INTERCEPT(y,x)`, `=RSQ(y,x)`,
`=FORECAST.LINEAR(new_x, y, x)`.

**Interpret the slope in context** — "each extra hour of study is associated
with about 4.3 more marks" — not just "b₁ = 4.3". Check the residual plot for
patterns: a curve means a straight line was the wrong model. And never predict
outside the range of x you observed; that is extrapolation.

For simple regression, **R² = r²** and **t² = F**. Use both as arithmetic
checks on your own work.

---

## Experiment 14 — Confidence intervals

1. `=AVERAGE(range)`, `=STDEV.S(range)`, `=COUNT(range)`.
2. Standard error: `=STDEV.S(range)/SQRT(COUNT(range))`.
3. Margin of error, population sd **unknown** (the usual case):
   `=CONFIDENCE.T(0.05, STDEV.S(range), COUNT(range))`
4. Population sd **known**: `=CONFIDENCE.NORM(0.05, sigma, n)`
5. Interval: `mean ± margin`.

Build all three of 90%, 95% and 99% and note in the sheet that the interval
**widens** as confidence rises — more certainty costs precision — and
**narrows** as n grows, in proportion to 1/√n.

**Write the interpretation carefully.** "If we repeated this sampling many
times, about 95% of the intervals so constructed would contain the true
population mean." *Not* "there is a 95% probability the true mean is in this
interval" — the true mean is a fixed number, not a random one.

---

## Experiment 15 — Hypothesis testing

State H₀ and H₁, then α, then the statistic, then the p-value, then the
decision, then a conclusion **in the words of the original problem**. Every
step earns marks.

**z-test** (population sd known):
`=(xbar-mu0)/(sigma/SQRT(n))`, p-value `=2*(1-NORM.S.DIST(ABS(z),TRUE))`

**t-test** (population sd unknown):
`=T.TEST(range1, range2, tails, type)` where `tails` is 1 or 2 and `type` is
1 = paired, 2 = equal variances, 3 = unequal variances. Or use
**Data Analysis → t-Test: Two-Sample Assuming Equal Variances**.

**Chi-square test of independence:**
1. Build the observed table.
2. Build the expected table: `=row_total*col_total/grand_total`.
3. `=CHISQ.TEST(observed_range, expected_range)` returns the **p-value**
   directly — not the statistic. For the statistic use
   `=CHISQ.INV.RT(p, df)` or sum `(O−E)²/E` by hand.
4. Check every expected frequency is at least 5, and say so.

**F-test for equal variances:** `=F.TEST(range1, range2)` gives a two-tailed
p-value. By hand, put the larger variance on top:
`F = s₁²/s₂²` with df = (n₁−1, n₂−1).

**Decision rule:** p < α → reject H₀. Otherwise *fail to reject* H₀ — never
"accept H₀", which claims more than the test can support.

| | H₀ true | H₀ false |
|---|---|---|
| **Reject H₀** | Type I error (α) | Correct (power) |
| **Fail to reject** | Correct | Type II error (β) |

Lowering α makes Type I errors rarer and Type II errors more likely. Only a
bigger sample reduces both.

---

## PSPP notes

PSPP is the free alternative to SPSS named in the syllabus, and may be what
your lab has installed.

| Task | PSPP menu path |
|---|---|
| Descriptive statistics | Analyze → Descriptive Statistics → Descriptives |
| Frequencies / histogram | Analyze → Descriptive Statistics → Frequencies |
| Contingency table + chi-square | Analyze → Descriptive Statistics → Crosstabs |
| Correlation | Analyze → Bivariate Correlation |
| Regression | Analyze → Linear Regression |
| One-sample / independent t-test | Analyze → Compare Means |

Enter variables in **Variable View** first, then data in **Data View** — the
opposite order to a spreadsheet, and the usual source of confusion.
