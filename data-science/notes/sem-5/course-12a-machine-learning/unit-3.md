# Unit 3 — Supervised Learning: Regression

**Syllabus topics:** Regression — introduction to regression; regression
algorithms: simple linear regression, multiple linear regression, polynomial
regression model, logistic regression, maximum likelihood estimation.

---

## 3.1 A note on the overlap with Course 4

**If you took Course 4, you have already derived most of this unit.** Course 4
Unit 4 covered correlation, simple and multiple linear regression, least
squares, residuals, R² and ANOVA — with the arithmetic done by hand.

| Topic | Where taught | What is new here |
|---|---|---|
| Least squares, slope, intercept | **Course 4 §4.5** | Nothing — revise it |
| Residuals, R², adjusted R² | **Course 4 §4.6** | Nothing conceptually |
| Multiple regression | **Course 4 §4.7** | The **prediction** framing, and regularisation |
| Polynomial regression | — | **New** — §3.5 |
| **Logistic regression** | — | **New**, and the most examined part — §3.6 |
| **Maximum likelihood** | — | **New** — §3.7 |
| Regularisation (Ridge, Lasso) | — | **New** — §3.8 |

### 🎯 What actually changed: explanation became prediction

Course 4 fitted a line to **explain** a relationship — is the slope
significantly different from zero? Machine learning fits the same line to
**predict** a new value, and that shifts every judgement:

| | **Course 4 — statistics** | **Here — machine learning** |
|---|---|---|
| Goal | Explain, and **test a hypothesis** | **Predict** a new observation |
| Scored on | Significance, p-values, confidence intervals | **Test-set** RMSE, R² |
| Fitted on | All the data | **Training** data only |
| Danger | Wrong inference | **Overfitting** |
| A good model | Assumptions satisfied, coefficients interpretable | Generalises to unseen data |
| More predictors | Risk multicollinearity, inflate p-values | Risk **variance**; use regularisation |

**Same arithmetic, different question.** Both are examined, and confusing them
is a classic lost mark.

> The worked example below deliberately reuses **Course 4's exact dataset** —
> ten (hours, score) pairs — so the two courses can be checked against each
> other. The lab asserts that scikit-learn reproduces Course 4's hand-computed
> slope, intercept and R² to four decimal places. If they ever disagree, one of
> the two courses is wrong, and the test says so.

---

## 3.2 What regression is

**Regression predicts a continuous numeric target from one or more features.**

| | Regression | Classification |
|---|---|---|
| Target | A **number** | A **category** |
| Output | 75.3 marks; ₹42 lakh | spam / not spam |
| Metric | RMSE, MAE, R² | Accuracy, F1, AUC |

⚠️ **Logistic regression is classification**, despite its name. It is in this
unit because it is a *linear model* fitted like a regression — and the naming
trips up a large number of exam answers every year. §3.6.

---

## 3.3 Simple linear regression

### 🔢 The model

> **ŷ = β₀ + β₁x**

Fitted by **ordinary least squares** — choosing β₀ and β₁ to minimise the sum
of squared residuals:

> **minimise Σ(yᵢ − ŷᵢ)²**

> **β₁ = Σ(xᵢ − x̄)(yᵢ − ȳ) / Σ(xᵢ − x̄)²**
> **β₀ = ȳ − β₁x̄**

### 🔢 The worked example — Course 4's data, refitted

Ten students, hours studied against exam score:

```
hours  : 2  3  4  5  6  7  8  9 10 11
score  : 52 55 61 64 70 72 78 82 85 91
```

```python
from sklearn.linear_model import LinearRegression
X = df[["hours"]]          # 2-D
y = df["score"]            # 1-D
model = LinearRegression().fit(X, y)
```

| Quantity | Value | Course 4 said |
|---|---:|---:|
| Slope β₁ | **4.3030** | 4.3030 ✓ |
| Intercept β₀ | **43.0303** | 43.0303 ✓ |
| R² | **0.9958** | 0.9958 ✓ |
| RMSE | **0.8015** | — |
| MAE | **0.7394** | — |
| Prediction at x = 7.5 | **75.3030** | 75.30 ✓ |

**Interpretation, which is where the marks are:**

- **Slope:** each additional hour of study **is associated with** about 4.30
  more marks. Not "causes" — regression fits a line, it does not establish
  causation.
- **Intercept:** a student studying zero hours is predicted to score 43.03.
  Treat it cautiously: x = 0 lies outside the observed range of 2 to 11, so the
  model has no evidence there.
- **R² = 0.9958:** 99.58% of the variation in scores is explained by hours.

### ⚠️ Never extrapolate

Predicting at x = 50 gives **258.18 marks**, which is impossible. The model is
only valid within the range it was fitted on, and nothing in the code will warn
you. The lab asserts this number precisely so the failure is concrete.

### 💡 Two free checks on your own arithmetic

1. **Residuals sum to zero** for a least-squares fit. The lab asserts
   Σ(y − ŷ) = 0.0000000000.
2. **For simple linear regression, R² = r².** Course 4 computed r = 0.9979, and
   0.9979² = 0.9958 ✓. *(This does not hold for multiple regression.)*

### 🔢 The assumptions — "LINE"

| | Assumption | Checked by | If violated |
|---|---|---|---|
| **L** | **Linearity** — the relationship is linear | Residual plot: random scatter | Transform, or use a non-linear model |
| **I** | **Independence** of errors | Domain knowledge; Durbin–Watson | Time-series methods |
| **N** | **Normality** of residuals | Q–Q plot | Inference is affected; prediction less so |
| **E** | **Equal variance** (homoscedasticity) | Residual plot: no funnel | Transform y, or weighted least squares |

**The residual plot is the single most informative diagnostic**, and Course 4
§4.6 has the pattern table: a curve means non-linearity, a funnel means
non-constant variance.

---

## 3.4 Multiple linear regression

> **ŷ = β₀ + β₁x₁ + β₂x₂ + … + βₚxₚ**

Each coefficient is the effect of **that** predictor **holding the others
constant** — and that phrase is what makes multiple regression different from
running p separate simple regressions.

### ⚠️ Multicollinearity

When predictors are strongly correlated with each other:

- Coefficients become **unstable** — they swing wildly with small data changes.
- Individual coefficients become **uninterpretable** — the model cannot
  attribute the effect between two features that move together.
- **Predictions are still fine.** This is a problem for *explanation*, not for
  *prediction* — which is exactly the Course 4 / Course 12 A distinction of
  §3.1.

**Detect it with the variance inflation factor:** VIF > 5 is a concern, VIF >
10 is serious. **Fix it** by dropping one of the pair, combining them, or using
**Ridge** (§3.8), which is designed for it.

### ⚠️ Use adjusted R², not R², to compare models

**R² never decreases when you add a predictor** — not even a column of random
noise. Adjusted R² penalises the extra parameter and can fall.

> **R²_adj = 1 − (1 − R²) · (n − 1)/(n − p − 1)**

---

## 3.5 Polynomial regression

> **ŷ = β₀ + β₁x + β₂x² + … + β_d x^d**

**Still a *linear* model** — linear in the **coefficients**, which is all that
"linear model" means. You are fitting a straight line in a transformed feature
space, so ordinary least squares still applies.

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
```

### 🔢 Degree, measured on the ten study points

| Degree | R² (training) |
|---:|---:|
| 1 | 0.995812 |
| 2 | 0.995817 |
| 3 | 0.995865 |
| 5 | 0.996327 |
| **9** | **1.000000** |

**Degree 9 on ten points fits perfectly** — nine coefficients plus an intercept
for ten data points is exact interpolation. That is not a good model; it is a
model with no freedom left, which will swing wildly between the points and
predict nonsense anywhere else.

**This is overfitting made visible**, and it is the clearest illustration in
the course: R² of exactly 1.0000 on training data.

### ⚠️ A real numerical trap worth knowing

Fitting degree 9 **without standardising first** gives R² = **0.981546** —
*worse* than a straight line. The powers of x span such different magnitudes
that the design matrix becomes ill-conditioned:

| Degree | Condition number |
|---:|---:|
| 1 | 1.79 × 10¹ |
| 3 | 8.16 × 10³ |
| **9** | **2.69 × 10¹³** |

At 10¹³ the least-squares solve loses most of its precision. **Standardise
before generating polynomial features** — the same rule as PCA, for the same
reason, and both numbers are asserted in the lab.

---

## 3.6 Logistic regression

### ⚠️ Logistic regression is a CLASSIFIER

It is in the regression unit because it is a **linear model fitted like a
regression**, but it predicts a **class**. Saying "logistic regression predicts
a continuous value" is a guaranteed lost mark.

### 🎯 Why linear regression cannot do classification

Fit a straight line to a 0/1 target and it will predict −0.3 and 1.4, which are
not probabilities. The fix is to squash the linear output through a function
bounded in (0, 1).

### 🔢 The sigmoid

> **p = σ(z) = 1 / (1 + e^−z)**, where **z = β₀ + β₁x₁ + … + βₚxₚ**

```
 p │        ______
1.0│      ⟋
   │    ⟋
0.5│  ⟋        ← z = 0  ⇒  p = 0.5
   │⟋
0.0│______
   └──────────────► z
```

| z | p |
|---:|---:|
| −∞ | 0 |
| 0 | **0.5** |
| +∞ | 1 |

### 🔢 Odds and the log-odds — the interpretation that earns marks

> **odds = p / (1 − p)**
> **log-odds (logit) = ln(p / (1 − p)) = z = β₀ + β₁x₁ + …**

**The model is linear in the log-odds.** So:

- **β₁ is the change in log-odds** for a one-unit increase in x₁.
- **e^β₁ is the odds ratio** — the multiplicative change in the odds.

**Example:** β₁ = 0.693 for `support_calls`. Then e^0.693 = **2.0**, so each
extra support call **doubles the odds** of churning.

⚠️ **Odds are not probability.** Odds of 2.0 means p = 2/3, not 2.

### 🔢 The decision threshold is a choice, not part of the model

The model outputs a probability; converting it to a class needs a cut-off,
conventionally 0.5. **Moving that threshold trades precision against recall**
(Unit 2 §2.5) and is often the cheapest way to fix an imbalanced problem —
cheaper than resampling and easier to explain.

### 🔢 Multi-class logistic regression

| Strategy | How |
|---|---|
| **One-vs-Rest (OvR)** | k binary classifiers, one per class against all others |
| **Multinomial (softmax)** | One model, probabilities across all k summing to 1 |

Softmax is generally preferred and is scikit-learn's default for multi-class.

---

## 3.7 Maximum likelihood estimation

### 🎯 The big idea

**Choose the parameters that make the data you actually observed as likely as
possible.**

Least squares asks *which line is closest to the points?* MLE asks *which
parameters make these observations least surprising?* They are different
questions with — under normal errors — the same answer.

### 🔢 The method

1. Write the **likelihood**: L(θ) = P(data | θ) = ∏ P(xᵢ | θ), assuming
   independence.
2. Take the **log**: ℓ(θ) = Σ ln P(xᵢ | θ). Products become sums, which are
   easier to differentiate and numerically stable.
3. **Differentiate**, set to zero, and solve for θ.

**Why the log:** it is monotonic, so it has the same maximum; and multiplying
1,000 probabilities each below 1 underflows to zero in floating point, while
adding their logarithms does not.

### 🔢 Worked example — a coin

Ten flips, seven heads. What is the MLE of p, the probability of heads?

- L(p) = p⁷(1 − p)³
- ℓ(p) = 7 ln p + 3 ln(1 − p)
- dℓ/dp = 7/p − 3/(1 − p) = 0
- 7(1 − p) = 3p → 7 = 10p → **p̂ = 0.7**

**The MLE is the sample proportion** — which is reassuring, and is exactly the
point: MLE recovers the estimator common sense already suggested, and gives a
principled reason for it.

### 💡 Where MLE appears in this course

| Model | Fitted by |
|---|---|
| **Linear regression** | Least squares — **which is the MLE under normally distributed errors** |
| **Logistic regression** | **MLE** — there is no closed form, so it is solved iteratively (gradient descent, Newton–Raphson) |
| **Naive Bayes** | MLE of the class and feature probabilities |
| **Gaussian mixture models** | MLE via the EM algorithm — Course 8 §5.4 |

**The connection worth stating:** minimising squared error and maximising
likelihood are *the same thing* when errors are normal. That is why least
squares is not an arbitrary choice — it falls out of an assumption about the
noise.

---

## 3.8 Regularisation — Ridge and Lasso

**Regularisation adds a penalty on coefficient size to the loss**, trading a
little bias for a large reduction in variance.

| | **Ridge (L2)** | **Lasso (L1)** | **Elastic Net** |
|---|---|---|---|
| Penalty | λ Σβⱼ² | λ Σ\|βⱼ\| | Both |
| Shrinks coefficients | Toward zero | **To exactly zero** | Both |
| Feature selection | **No** | **Yes** — an embedded method (Unit 2 §2.9) | Yes |
| Use when | Many correlated predictors | Many irrelevant predictors | Both problems |
| Handles multicollinearity | **Well** | Picks one of a correlated pair arbitrarily | Better |

### ⚠️ Regularisation requires scaling

The penalty is on coefficient **magnitude**, and magnitude depends on units. A
feature in rupees gets a tiny coefficient and is barely penalised; the same
feature in lakhs gets a large one and is crushed. **Standardise first**, always.

**λ (`alpha` in scikit-learn) is a hyperparameter** — tune it on validation
folds. λ = 0 gives ordinary least squares; λ → ∞ shrinks everything to zero.

---

## Practice problems

### Problem 1

Explain simple linear regression. Fit it to the data below, interpret the
result, and state the assumptions. *(10 marks)*

```
hours : 2  3  4  5  6  7  8  9 10 11
score : 52 55 61 64 70 72 78 82 85 91
```

**Solution.**

**The model:** ŷ = β₀ + β₁x, fitted by **ordinary least squares** — minimising
Σ(yᵢ − ŷᵢ)². Give both formulas.

**The fit:** β₁ = 4.3030, β₀ = 43.0303, so **ŷ = 43.03 + 4.30x**, with R² =
0.9958 and RMSE = 0.8015.

**Interpretation, which is where the marks are:**

- Each additional hour **is associated with** about 4.30 more marks — *not*
  "causes".
- The intercept 43.03 is the prediction at zero hours, but x = 0 is outside the
  observed range 2–11, so treat it cautiously.
- R² = 0.9958 means 99.58% of the variation in scores is explained.
- At x = 7.5, ŷ = **75.30**.
- **At x = 50, ŷ = 258.18 marks — impossible. Never extrapolate.**

**The assumptions — LINE:** Linearity, Independence of errors, Normality of
residuals, Equal variance. Say that the **residual plot** checks two of them at
once: a curve means non-linearity, a funnel means heteroscedasticity.

**Two free checks:** residuals sum to zero, and R² = r² for simple regression
(0.9979² = 0.9958).

### Problem 2

Explain logistic regression. Why is linear regression unsuitable for
classification? *(10 marks)*

**Solution.**

**State first that logistic regression is a classifier** despite its name — it
sits in the regression unit because it is a linear model fitted like one.

**Why linear regression fails:** fitting a straight line to a 0/1 target
produces predictions like −0.3 and 1.4, which are not probabilities; the
model is unbounded, and it is also very sensitive to points far along the x
axis.

**The fix — the sigmoid:** p = 1/(1 + e^−z) with z = β₀ + β₁x₁ + … Sketch it:
bounded in (0, 1), and p = 0.5 exactly when z = 0.

**The interpretation, which carries the marks:**

- odds = p/(1 − p); logit = ln(odds) = z
- **the model is linear in the log-odds**
- β is the change in log-odds per unit of x
- **e^β is the odds ratio.** If β = 0.693 then e^0.693 = 2.0, so each unit
  **doubles the odds**

Warn that **odds are not probability** — odds of 2.0 means p = 2/3.

**Fitting:** by **maximum likelihood**, not least squares, and with no closed
form — solved iteratively.

**The threshold:** 0.5 is a convention, not part of the model. Moving it trades
precision against recall and is often the cheapest fix for imbalance.

**Multi-class:** one-vs-rest, or multinomial softmax.

### Problem 3

What is maximum likelihood estimation? Derive the MLE for a coin from ten
flips with seven heads. *(10 marks)*

**Solution.**

**Definition:** MLE chooses the parameter values that make the observed data
most probable. Least squares asks which line is closest to the points; MLE asks
which parameters make these observations least surprising.

**The method:** write the likelihood L(θ) = ∏P(xᵢ|θ); take logs to get ℓ(θ) =
ΣlnP(xᵢ|θ); differentiate, set to zero, solve.

**Why the log:** it is monotonic so the maximum is unchanged, products become
sums which differentiate easily, and multiplying a thousand probabilities below
1 underflows to zero in floating point while summing their logs does not.

**The derivation:**

- L(p) = p⁷(1 − p)³
- ℓ(p) = 7 ln p + 3 ln(1 − p)
- dℓ/dp = 7/p − 3/(1 − p) = 0
- 7(1 − p) = 3p ⟹ 7 = 10p ⟹ **p̂ = 0.7**

**The MLE is the sample proportion** — which is the point: MLE gives a
principled derivation of the estimator intuition already suggested.

**Where it appears:** logistic regression is fitted by MLE; Naive Bayes
estimates its probabilities by MLE; and — the connection worth stating —
**least squares *is* the MLE for linear regression when the errors are normally
distributed.** Minimising squared error and maximising likelihood are the same
thing under that assumption, which is why least squares is not an arbitrary
choice.

---

## Exam questions from this unit

**Two marks**

1. Write the least-squares formulas for slope and intercept.
2. What does R² measure?
3. Why is adjusted R² needed?
4. Give the sigmoid function.
5. What is an odds ratio?
6. Is logistic regression a regression or a classification method?
7. What does the L1 penalty do that L2 does not?

**Five marks**

1. Distinguish simple and multiple linear regression.
2. What is multicollinearity, how is it detected, and does it matter?
3. Explain polynomial regression and when it overfits.
4. Compare Ridge and Lasso.
5. State and explain the assumptions of linear regression.
6. Explain maximum likelihood estimation.

**Ten marks**

1. Explain simple linear regression with a worked example and its assumptions.
2. Explain logistic regression and why linear regression cannot classify.
3. Explain MLE and derive the estimator for a coin.
4. Explain regularisation and its role in the bias–variance trade-off.

---

## Mistakes that cost marks

- **Calling logistic regression a regression method.** It classifies.
- **Saying the slope means "causes".** *Is associated with.*
- **Extrapolating.** 50 hours predicts 258 marks.
- **Confusing odds with probability.** Odds 2.0 is p = 2/3.
- **Saying polynomial regression is non-linear.** It is linear in the
  **coefficients**, which is what the term means.
- **Comparing models of different sizes with R².** It never decreases; use
  adjusted R².
- **Regularising without standardising.** The penalty is on magnitude, and
  magnitude depends on units.
- **Claiming multicollinearity ruins predictions.** It ruins *interpretation*;
  predictions are usually fine.
- **Forgetting that least squares is the MLE under normal errors.** That
  connection is worth a mark and is rarely given.
