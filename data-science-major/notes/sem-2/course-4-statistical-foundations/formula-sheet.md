# Course 4 — Formula Sheet

Everything from the five units on one page. Print it, and use it for the last
week before the exam. Each section links back to the unit that explains it.

---

## Unit 1 — Probability and descriptive statistics

### Probability rules

| | Formula |
|---|---|
| Classical probability | P(A) = favourable outcomes / total outcomes |
| Complement | **P(A′) = 1 − P(A)** |
| Addition | **P(A ∪ B) = P(A) + P(B) − P(A ∩ B)** |
| Addition, mutually exclusive | P(A ∪ B) = P(A) + P(B) |
| Multiplication | **P(A ∩ B) = P(A) · P(B\|A)** |
| Multiplication, independent | P(A ∩ B) = P(A) · P(B) |
| Conditional | **P(A\|B) = P(A ∩ B) / P(B)** |
| Independence test | P(A ∩ B) = P(A) · P(B) |

### Bayes' theorem *(examined but not in the syllabus — finding D1)*

> **P(A\|B) = P(B\|A) · P(A) / P(B)**
>
> **P(B) = P(B\|A)·P(A) + P(B\|A′)·P(A′)**   *(law of total probability)*

### Central tendency

| | Formula |
|---|---|
| Mean | **x̄ = Σxᵢ / n** |
| Median | middle value when sorted; average the two middle if n is even |
| Mode | most frequent value |
| Empirical relation | Mode ≈ 3·Median − 2·Mean |

### Dispersion

| | Formula |
|---|---|
| Range | max − min |
| IQR | **Q₃ − Q₁** |
| Outlier fences | Q₁ − 1.5·IQR and Q₃ + 1.5·IQR |
| Population variance | **σ² = Σ(xᵢ − μ)² / N** |
| Sample variance | **s² = Σ(xᵢ − x̄)² / (n − 1)** |
| Standard deviation | σ = √σ²  or  s = √s² |
| Coefficient of variation | **CV = (s / x̄) × 100%** |
| Pearson skewness | 3(mean − median) / s |

**The n vs n−1 rule:** population → divide by n; sample → divide by **n − 1**.
This is the most common arithmetic error in the course.

---

## Unit 2 — Random variables and expectation

| | Discrete | Continuous |
|---|---|---|
| Distribution | PMF p(x) = P(X = x) | PDF f(x) |
| Total probability | Σ p(x) = 1 | ∫ f(x) dx = 1 |
| CDF | F(x) = Σ_{t ≤ x} p(t) | F(x) = ∫_{−∞}^{x} f(t) dt |
| Expectation | **E(X) = Σ x·p(x)** | **E(X) = ∫ x·f(x) dx** |

### Variance

> **Var(X) = E[(X − μ)²] = E(X²) − [E(X)]²**   ← use the shortcut
> **SD(X) = √Var(X)**

### Properties

| Expectation | Variance |
|---|---|
| E(c) = c | Var(c) = **0** |
| E(aX) = a·E(X) | Var(aX) = **a²**·Var(X) |
| **E(aX + b) = a·E(X) + b** | **Var(aX + b) = a²·Var(X)** |
| E(X + Y) = E(X) + E(Y) *(always)* | Var(X + Y) = Var(X) + Var(Y) *(independent only)* |
| E(XY) = E(X)·E(Y) *(independent only)* | |

### Moments

| Moment | Meaning |
|---|---|
| μ′₁ = E(X) | Mean |
| μ₂ = E[(X−μ)²] | Variance |
| μ₃ | Skewness |
| μ₄ | Kurtosis |

- β₁ = μ₃²/μ₂³ (skewness) · β₂ = μ₄/μ₂² (kurtosis)
- β₂ = 3 mesokurtic · > 3 leptokurtic (peaked) · < 3 platykurtic (flat)
- MGF: **Mₓ(t) = E(e^{tX})**, and μ′ᵣ = d^r M/dt^r at t = 0

---

## Unit 3 — Distributions

### Discrete

| Distribution | PMF | Mean | Variance |
|---|---|---|---|
| **Binomial**(n, p) | ⁿCₖ pᵏ(1−p)ⁿ⁻ᵏ | **np** | **np(1−p)** |
| **Poisson**(λ) | e^{−λ} λᵏ / k! | **λ** | **λ** |
| **Geometric**(p) | (1−p)^{k−1} p | **1/p** | (1−p)/p² |
| **Negative binomial**(r, p) | ^{k−1}C_{r−1} pʳ(1−p)^{k−r} | **r/p** | r(1−p)/p² |

### Continuous

| Distribution | PDF | Mean | Variance |
|---|---|---|---|
| **Uniform**(a, b) | 1/(b−a) | **(a+b)/2** | **(b−a)²/12** |
| **Normal**(μ, σ) | (1/(σ√(2π)))e^{−(x−μ)²/(2σ²)} | **μ** | **σ²** |
| **Exponential**(λ) | λe^{−λx} | **1/λ** | **1/λ²** |
| **Gamma**(α, λ) | (λ^α/Γ(α))x^{α−1}e^{−λx} | **α/λ** | **α/λ²** |

### Normal distribution essentials

> **z = (x − μ) / σ**

| Interval | Probability |
|---|---|
| μ ± 1σ | 68.27% |
| μ ± 2σ | 95.45% |
| μ ± 3σ | 99.73% |

**Exponential CDF:** F(x) = 1 − e^{−λx}, so P(X > x) = e^{−λx}
**Memorylessness:** P(X > s+t | X > s) = P(X > t) — exponential and geometric only

### Joint distributions

- Marginal: p(x) = Σ_y p(x, y)
- Conditional: p(y|x) = p(x, y) / p(x)
- Independent when **p(x, y) = p(x)·p(y)** for every pair

### Central Limit Theorem

> Mean of x̄ = **μ** · Standard error = **σ/√n** · Shape → normal as n grows
> Rule of thumb: **n ≥ 30**

---

## Unit 4 — Correlation and regression

| | Formula |
|---|---|
| Covariance | Cov(X,Y) = Σ(xᵢ−x̄)(yᵢ−ȳ)/(n−1) |
| **Pearson r** | **r = Σ(x−x̄)(y−ȳ) / √[Σ(x−x̄)²·Σ(y−ȳ)²]** |
| equivalently | r = Cov(X,Y)/(sₓ·s_y) |
| **Spearman ρ** | **ρ = 1 − 6Σd² / [n(n²−1)]** |
| Regression slope | **b₁ = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)²** |
| Regression intercept | **b₀ = ȳ − b₁x̄** |
| Fitted line | ŷ = b₀ + b₁x |
| Residual | eᵢ = yᵢ − ŷᵢ |
| **R²** | SS_reg/SS_total = 1 − SS_res/SS_total |
| Adjusted R² | 1 − [(1−R²)(n−1)/(n−k−1)] |
| SE of slope | SE(b₁) = √(MS_res / Σ(x−x̄)²) |
| t for slope | t = b₁ / SE(b₁), df = n − 2 |

**Checks that catch arithmetic errors:**
- Σ(x − x̄) = 0 and Σ(y − ȳ) = 0 always
- Residuals sum to zero
- For **simple** regression: **R² = r²** and **t² = F**

### Regression ANOVA

| Source | SS | df | MS | F |
|---|---|---|---|---|
| Regression | SS_reg | k | SS_reg/k | MS_reg/MS_res |
| Residual | SS_res | n−k−1 | SS_res/(n−k−1) | |
| Total | SS_tot | n−1 | | |

---

## Unit 5 — Inference and hypothesis testing

### Confidence intervals

> **σ known:  x̄ ± z(α/2)·σ/√n**
> **σ unknown: x̄ ± t(α/2, n−1)·s/√n**

### Test statistics

| Test | Statistic | df |
|---|---|---|
| **z-test** | z = (x̄ − μ₀)/(σ/√n) | — |
| **One-sample t** | t = (x̄ − μ₀)/(s/√n) | n − 1 |
| **Two-sample t** (pooled) | t = (x̄₁−x̄₂)/√(s²ₚ(1/n₁+1/n₂)) | n₁+n₂−2 |
| pooled variance | s²ₚ = [(n₁−1)s₁² + (n₂−1)s₂²]/(n₁+n₂−2) | |
| **Paired t** | t = d̄/(s_d/√n) | n − 1 |
| **Chi-square** | χ² = Σ(O−E)²/E | (r−1)(c−1) |
| expected frequency | E = (row total × column total)/grand total | |
| **F-test** | F = s₁²/s₂², larger on top | (n₁−1, n₂−1) |

### Errors and power

| | H₀ true | H₀ false |
|---|---|---|
| **Reject H₀** | Type I error (**α**) | Correct — **power = 1 − β** |
| **Fail to reject** | Correct (1 − α) | Type II error (**β**) |

**Decision rule:** p < α → reject H₀. Otherwise **fail to reject** — never
"accept".

---

## Critical values

### Standard normal (z)

| Confidence | α | Two-tailed z(α/2) | One-tailed z(α) |
|---|---|---|---|
| 90% | 0.10 | 1.645 | 1.282 |
| **95%** | **0.05** | **1.960** | **1.645** |
| 99% | 0.01 | 2.576 | 2.326 |

### Student's t — two-tailed at α = 0.05

| df | t | df | t |
|---|---|---|---|
| 5 | 2.571 | 18 | **2.101** |
| 8 | 2.306 | 20 | 2.086 |
| 10 | 2.228 | 24 | **2.064** |
| 12 | 2.179 | 30 | 2.042 |
| 15 | 2.131 | ∞ | 1.960 |

*(One-tailed at α = 0.05: df 10 → 1.812, df 24 → 1.711.)*

### Chi-square — right tail at α = 0.05

| df | χ² | df | χ² |
|---|---|---|---|
| 1 | **3.841** | 5 | 11.070 |
| 2 | **5.991** | 6 | 12.592 |
| 3 | 7.815 | 8 | 15.507 |
| 4 | 9.488 | 10 | 18.307 |

### F — right tail at α = 0.05

| df₁ \ df₂ | 5 | 9 | 10 |
|---|---|---|---|
| **1** | 6.61 | 5.12 | 4.96 |
| **2** | 5.79 | 4.26 | 4.10 |
| **3** | 5.41 | 3.86 | 3.71 |

> These table values were used to verify
> `statlib.py` — all 23 checks
> in `test_statlib.py`
> pass, so the numbers here and the code agree.

---

## Excel functions

| Task | Function |
|---|---|
| Mean, median, mode | `AVERAGE`, `MEDIAN`, `MODE.SNGL` |
| Sample sd / variance | `STDEV.S`, `VAR.S` |
| Population sd / variance | `STDEV.P`, `VAR.P` |
| Quartile | `QUARTILE.INC(range, 1 or 3)` |
| Correlation | `CORREL`, `PEARSON` |
| Covariance | `COVARIANCE.S`, `COVARIANCE.P` |
| Rank (for Spearman) | `RANK.AVG` |
| Regression | `SLOPE`, `INTERCEPT`, `RSQ`, `FORECAST.LINEAR` |
| Binomial | `BINOM.DIST(k, n, p, cumulative)` |
| Poisson | `POISSON.DIST(k, λ, cumulative)` |
| Normal | `NORM.DIST(x, μ, σ, TRUE)`, `NORM.INV(p, μ, σ)` |
| Standard normal | `NORM.S.DIST(z, TRUE)`, `NORM.S.INV(p)` |
| Exponential | `EXPON.DIST(x, λ, TRUE)` |
| Confidence margin | `CONFIDENCE.T(α, s, n)`, `CONFIDENCE.NORM(α, σ, n)` |
| t-test | `T.TEST(r1, r2, tails, type)` |
| Chi-square | `CHISQ.TEST(observed, expected)` → **p-value** |
| F-test | `F.TEST(r1, r2)` → **p-value** |

**The last two return p-values, not test statistics.** Reporting a `CHISQ.TEST`
result as χ² is a standard mistake.
