# Unit 4 — Correlation and Regression

**Syllabus topics:** Bivariate data and scatter plots. Correlation — Pearson
and Spearman coefficients, interpretation. Simple linear regression — model,
estimation, properties and analysis of variance. Multiple linear regression
basics (conceptual understanding). Residuals and goodness of fit.

---

## 4.1 Bivariate data and scatter plots

### 🎯 The big idea

Until now you studied one variable at a time. Bivariate analysis asks whether
**two** variables move together — and if so, whether one can predict the other.

### 📖 The story

A teacher suspects students who study more score higher. She records, for each
student, hours studied and exam score. Each student is now a **pair** of
numbers, and plotting those pairs as points gives a **scatter plot**. If the
cloud of points slopes upwards, her suspicion has support.

**Scatter plot rules:** points only, never joined by lines. The **independent**
variable (the cause, or the thing you control) goes on the x-axis; the
**dependent** variable on the y-axis.

**Reading a scatter plot:**

| Pattern | Meaning |
|---|---|
| Points rise left to right | Positive relationship |
| Points fall left to right | Negative relationship |
| No pattern, a shapeless blob | No relationship |
| A tight band | Strong relationship |
| A wide scatter | Weak relationship |
| A curve | Non-linear — correlation will understate it |

That last row matters: **always plot before computing r.** A perfect parabola
can have r = 0, and reporting "no relationship" would be badly wrong.

## 4.2 Covariance

> **Cov(X,Y) = Σ(xᵢ − x̄)(yᵢ − ȳ) / (n − 1)**

**Why the product works.** When both values are above their means, both
deviations are positive and the product is positive. When both are below, both
are negative and the product is *still* positive. Only when one is above and
the other below is the product negative. Add them all up: a positive total
means the variables move together.

**Its flaw:** the magnitude depends entirely on the units. Measure height in
centimetres instead of metres and the covariance multiplies by 100, though
nothing about the relationship changed. So the **sign is meaningful, the size
is not**.

## 4.3 Pearson's correlation coefficient

### 🔢 The formula

> **r = Σ(xᵢ − x̄)(yᵢ − ȳ) / √[Σ(xᵢ − x̄)² · Σ(yᵢ − ȳ)²]**

or equivalently **r = Cov(X,Y) / (sₓ · s_y)**

Dividing by both standard deviations cancels the units, so r is **always
between −1 and +1**.

### Interpreting r

| r | Strength |
|---|---|
| +1.0 | Perfect positive — every point on one rising line |
| +0.7 to +0.9 | Strong positive |
| +0.4 to +0.7 | Moderate positive |
| 0 to +0.4 | Weak positive |
| 0 | No **linear** relationship |
| negative values | Same strengths, opposite direction |

### Worked example

Hours studied (x) and exam score (y):

| x | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|
| y | 52 | 55 | 61 | 64 | 70 | 72 | 78 | 82 | 85 | 91 |

- Step 1: x̄ = 65/10 = **6.5**; ȳ = 710/10 = **71.0**
- Step 2: compute the three sums of products and squares
  - Σ(x−x̄)(y−ȳ) = **355.00**
  - Σ(x−x̄)² = **82.50**
  - Σ(y−ȳ)² = **1534.00**
- Step 3: r = 355.00 / √(82.50 × 1534.00) = 355.00 / √126555 = 355.00 / 355.75
- Step 4: **r = 0.9979**

A very strong positive linear relationship.

### 💡 Correlation is not causation

Ice cream sales and drowning deaths are strongly correlated. Ice cream does not
cause drowning — **summer** causes both. That third variable is a
**confounder**.

Three explanations for any correlation between X and Y:

1. X causes Y
2. Y causes X
3. Some Z causes both — or it is coincidence

Correlation alone cannot tell you which. **Say this in every interpretation
question.** It is a reliable mark, and it is the single most important idea in
the unit.

## 4.4 Spearman's rank correlation

Pearson measures *linear* association. **Spearman** replaces the values with
their **ranks**, so it measures any **monotonic** relationship — consistently
increasing or decreasing, whether or not it is a straight line.

> **ρ = 1 − (6 Σd²) / (n(n² − 1))**

where d is the difference in ranks for each pair.

**When to use it:**

| Use Pearson when | Use Spearman when |
|---|---|
| The relationship looks linear | The relationship is curved but monotonic |
| Data is roughly normal | Data is skewed or ordinal |
| No serious outliers | Outliers are present |
| Data is numeric | Data is ranked (positions, grades) |

Spearman is **resistant to outliers**, because turning values into ranks
destroys the extremity: a value of 500 among values near 50 becomes simply
"rank 10", no more influential than 60 would be.

**Ties** get the average of the ranks they would have occupied. Use Excel's
`RANK.AVG`, not `RANK`.

## 4.5 Simple linear regression

### 🎯 The big idea

Correlation says *whether* two variables move together. Regression fits the
actual **line**, so you can predict.

### 🔢 The model

> **y = β₀ + β₁x + ε**

- β₀ = the **intercept** — predicted y when x = 0
- β₁ = the **slope** — the change in y for a one-unit increase in x
- ε = the **error term** — everything the line does not capture

### Estimation by least squares

The best line is the one minimising the sum of the **squared vertical
distances** from the points to the line. Squaring stops positive and negative
errors from cancelling, and penalises large misses heavily.

> **b₁ = Σ(xᵢ − x̄)(yᵢ − ȳ) / Σ(xᵢ − x̄)²**
> **b₀ = ȳ − b₁x̄**

**Continuing the worked example:**

- Step 1: b₁ = 355.00 / 82.50 = **4.3030**
- Step 2: b₀ = 71.00 − 4.3030 × 6.5 = 71.00 − 27.97 = **43.0303**
- Step 3: the fitted line is **ŷ = 43.03 + 4.30x**

**Interpretation — where the marks are:**

- **Slope:** each additional hour of study is associated with about **4.3 more
  marks**.
- **Intercept:** a student studying zero hours is predicted to score 43.03.
  Treat this cautiously — x = 0 lies outside the observed range of 2 to 11
  hours, so the model has no evidence there.

Note the wording "**is associated with**", not "causes". Regression fits a
line; it does not establish causation.

### Prediction

For x = 7.5 hours: ŷ = 43.03 + 4.30(7.5) = **75.30 marks**

**Never extrapolate.** Predicting for x = 50 hours gives 258 marks, which is
impossible. The model is only valid within the range of the data you fitted it
to.

## 4.6 Residuals and goodness of fit

### Residuals

> **eᵢ = yᵢ − ŷᵢ**   (observed minus fitted)

Properties of least-squares residuals: they **sum to zero**, and the line
always passes through the point (x̄, ȳ).

**The residual plot** — residuals against fitted values — is the diagnostic:

| Pattern | Meaning |
|---|---|
| Random scatter around zero | The model is appropriate ✓ |
| A curve | The relationship is non-linear — a straight line is wrong |
| A funnel (spreading out) | Non-constant variance (heteroscedasticity) |
| One point far from the rest | An outlier worth investigating |

### Coefficient of determination R²

> **R² = SS_regression / SS_total = 1 − (SS_residual / SS_total)**

**R² is the proportion of the variation in y that the model explains.**

For the worked example: SS_total = 1534.00, SS_residual = 6.42, so
SS_regression = 1527.58.

R² = 1527.58 / 1534.00 = **0.9958**

So **99.58%** of the variation in exam scores is explained by hours studied.

**For simple linear regression, R² = r².** Check: 0.9979² = 0.9958 ✓ — a free
arithmetic check on your own work. (This does **not** hold for multiple
regression.)

### Analysis of variance for regression

| Source | SS | df | MS | F |
|---|---:|---:|---:|---:|
| Regression | 1527.58 | 1 | 1527.58 | 1902.26 |
| Residual | 6.42 | 8 | 0.80 | |
| **Total** | **1534.00** | **9** | | |

- df for regression = k = 1 (one predictor)
- df for residual = n − k − 1 = 10 − 1 − 1 = 8
- df total = n − 1 = 9
- **F = MS_regression / MS_residual = 1527.58 / 0.80 = 1902.26**

F is enormous, so the model explains far more variation than chance would.
The p-value is 8.4 × 10⁻¹¹ — reject the hypothesis that the slope is zero.

### Testing the slope

> **H₀: β₁ = 0** (x has no linear effect on y) **vs H₁: β₁ ≠ 0**
>
> **t = b₁ / SE(b₁)**, where **SE(b₁) = √(MS_residual / Σ(x − x̄)²)**

- SE(b₁) = √(0.8030 / 82.50) = **0.0987**
- t = 4.3030 / 0.0987 = **43.61** on 8 degrees of freedom
- p ≈ 8.4 × 10⁻¹¹ → reject H₀

**For simple regression, t² = F**: 43.61² = 1902.26 ✓ — another built-in check.

All of these figures are computed in
`04_correlation_regression.py`.

## 4.7 Multiple linear regression (conceptual)

The syllabus asks for conceptual understanding only.

> **y = β₀ + β₁x₁ + β₂x₂ + … + βₖxₖ + ε**

Several predictors instead of one. Exam score might be predicted from hours
studied **and** attendance **and** previous CGPA.

**Interpretation changes in an important way.** β₁ is now the effect of x₁
**holding all the other predictors constant**. That phrase is the whole
difference between simple and multiple regression, and it is what makes the
technique useful: it isolates one variable's contribution.

### Adjusted R²

Adding *any* predictor — even a column of random numbers — never decreases R².
So R² alone will always favour the bigger model.

> **Adjusted R² = 1 − [(1 − R²)(n − 1) / (n − k − 1)]**

This penalises extra predictors, and *can* decrease when a useless one is
added. **Compare models by adjusted R², not R².**

### Multicollinearity

When two predictors are themselves strongly correlated — height in centimetres
and height in inches, say — the model cannot separate their individual effects.
The coefficients become unstable and their signs may flip. This is
**multicollinearity**, and it is why you check the correlations among your
predictors before fitting.

---

## 📝 Practice problems

### Problem 1

For the data below, compute Pearson's r and interpret it.

| x | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| y | 2 | 4 | 5 | 4 | 5 |

**Solution.**

- Step 1: x̄ = 15/5 = **3**; ȳ = 20/5 = **4**

- Step 2:

| x | y | x−x̄ | y−ȳ | (x−x̄)(y−ȳ) | (x−x̄)² | (y−ȳ)² |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | −2 | −2 | 4 | 4 | 4 |
| 2 | 4 | −1 | 0 | 0 | 1 | 0 |
| 3 | 5 | 0 | 1 | 0 | 0 | 1 |
| 4 | 4 | 1 | 0 | 0 | 1 | 0 |
| 5 | 5 | 2 | 1 | 2 | 4 | 1 |
| | | **0** ✓ | **0** ✓ | **6** | **10** | **6** |

- Step 3: r = 6 / √(10 × 6) = 6 / √60 = 6 / 7.746 = **0.7746**

**Interpretation:** a strong positive linear relationship. As x increases, y
tends to increase. This does not establish that x causes y.

### Problem 2

Using the same data, find the regression line and predict y when x = 6.

**Solution.**

- Step 1: b₁ = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)² = 6/10 = **0.6**
- Step 2: b₀ = ȳ − b₁x̄ = 4 − 0.6(3) = 4 − 1.8 = **2.2**
- Step 3: the line is **ŷ = 2.2 + 0.6x**
- Step 4: at x = 6, ŷ = 2.2 + 0.6(6) = 2.2 + 3.6 = **5.8**

**Caution:** the observed x values run from 1 to 5. Predicting at x = 6 is
extrapolation — just outside the data — so the prediction is less reliable than
one made inside the range. Say so.

- Step 5 — **R²**: R² = r² = 0.7746² = **0.60**, so 60% of the variation in y
  is explained by x.

### Problem 3

Eight students were ranked by two judges. Compute Spearman's rank correlation.

| Student | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| Judge 1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| Judge 2 | 2 | 1 | 4 | 3 | 6 | 5 | 8 | 7 |

**Solution.**

- Step 1: find d = rank₁ − rank₂ and d² for each student

| Student | R₁ | R₂ | d | d² |
|---|---:|---:|---:|---:|
| A | 1 | 2 | −1 | 1 |
| B | 2 | 1 | 1 | 1 |
| C | 3 | 4 | −1 | 1 |
| D | 4 | 3 | 1 | 1 |
| E | 5 | 6 | −1 | 1 |
| F | 6 | 5 | 1 | 1 |
| G | 7 | 8 | −1 | 1 |
| H | 8 | 7 | 1 | 1 |
| | | | **0** ✓ | **8** |

- Step 2: n = 8, so n(n²−1) = 8 × 63 = **504**
- Step 3: ρ = 1 − (6 × 8)/504 = 1 − 48/504 = 1 − 0.0952 = **0.9048**

**Interpretation:** the two judges agree very closely — each pair of adjacent
students is merely swapped, never moved far. A ρ of 0.90 reflects that strong
agreement.

*(Check: d should always sum to zero. It does.)*

---

## Exam questions from this unit

**Two marks**

1. What is the range of the correlation coefficient?
2. State one difference between Pearson and Spearman correlation.
3. What does R² measure?
4. Why is covariance's magnitude not interpretable?
5. What is extrapolation, and why is it dangerous?

**Five marks**

1. Compute Pearson's r for a given dataset and interpret it.
2. Explain the least-squares method for fitting a regression line.
3. Explain residuals and what a residual plot reveals.
4. Distinguish correlation from regression.
5. Explain adjusted R² and why it is preferred for multiple regression.

**Ten marks**

1. For a given bivariate dataset, compute the correlation coefficient, fit the
   regression line, construct the ANOVA table and interpret all results.
2. Explain correlation and regression fully — types, formulas, interpretation,
   goodness of fit, and the distinction between association and causation.

## Correlation vs regression — a standard comparison

| | Correlation | Regression |
|---|---|---|
| Purpose | Measure the strength of association | Predict one variable from another |
| Symmetry | r(X,Y) = r(Y,X) | Regressing Y on X ≠ X on Y |
| Output | A single number in [−1, +1] | An equation |
| Variables | Both treated equally | One dependent, one independent |
| Units | Unit-free | In the units of the variables |

## Mistakes that cost marks

- Reporting r without interpreting it
- Claiming causation from a correlation
- Computing r on obviously curved data and concluding "no relationship"
- Swapping x and y in the regression formula
- Extrapolating beyond the data range without a caveat
- Confusing R² with r — remember R² = r² for **simple** regression only
- Using `RANK` instead of `RANK.AVG` in Excel when there are ties
- Forgetting that the residuals must sum to zero (a free check)
