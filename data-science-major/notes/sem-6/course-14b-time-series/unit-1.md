# Unit 1 — Fundamentals and Stationary Processes

**Syllabus topics:** Introduction to time series: types, components,
forecasting process. Stationary processes: definitions, autocovariance,
autocorrelation functions (ACF/PACF). Model evaluation metrics. ACF/PACF
example analyses.

---

## 1.1 What makes a time series different

### 🎯 The one sentence

**In a time series, the observations are not independent — and every method
you learned before this course assumed they were.**

| Assumption you have been making | Status here |
|---|---|
| Observations are independent | **false** — that dependence *is* the signal |
| Order does not matter | **false** — order is the data |
| Shuffle then split | **invalid** — it lets the model see the future |
| k-fold cross-validation | **invalid** — folds train on later data |
| Bootstrap resampling | **invalid** — destroys the ordering |

### 📖 The formal object

A time series is a sequence **{y₁, y₂, …, y_T}** indexed by time, where the
spacing is (usually) regular and the index is meaningful.

**One realisation, not a sample.** This is the philosophical difference and it
has a practical consequence: you observe *one* path of the process, and you
cannot re-run history to get another. Everything you estimate is estimated
from a single draw.

**Measured in the lab:** an AR(2) built with φ = (0.6, −0.3) gave an estimate
of **0.7062 — 2.5 standard errors from the truth.** Across 200 independent
draws the estimator is unbiased (mean 0.5980), and only 1 draw in 200 was
further out. **The method was right; that one series was unusual** — and from
a single dataset you cannot tell those apart.

---

## 1.2 The four components

| Component | Symbol | What it is | Period |
|---|---|---|---|
| **Trend** | T | long-run direction | none |
| **Seasonality** | S | a **fixed, known** period | 12 months, 7 days, 24 hours |
| **Cyclical** | C | wave-like, **variable** period | business cycles, 3–10 years |
| **Irregular** | R | what is left | none |

### ⚠️ Seasonality and cycle are not the same thing

**Seasonality has a fixed, calendar-determined period.** Retail sales peak
every December — you know the period before you look.

**A cycle has a variable period.** A business cycle lasts somewhere between
three and ten years and nobody knows which in advance.

**The practical consequence:** SARIMA can model seasonality because you can
tell it m = 12. **It cannot model a cycle**, because there is no fixed m to
give it. Confusing the two is why people fit SARIMA to economic data and are
disappointed.

### The two decomposition models

| | Additive | Multiplicative |
|---|---|---|
| Form | **y = T + S + R** | **y = T × S × R** |
| Use when | the seasonal swing is **constant** | the swing **grows with the level** |
| Fix | — | **take logs** — log(T×S×R) = log T + log S + log R |

### 🔢 Measured, in the lab

On a deliberately multiplicative series, the peak-to-trough swing was **59.6
in the first two years and 98.0 in the last two — 1.64×**. After a log
transform: **0.5546 and 0.5366, a ratio of 0.97.**

**Decide from the plot, not from a rule.** A growing swing fitted with an
additive model produces residuals that are small early and large late, which
is heteroscedasticity — and it invalidates every confidence interval the model
produces.

### 🔢 And the decomposition recovers what you put in

The lab's series was built from a **trend of +0.8 per month** and a **seasonal
amplitude of 25**. `seasonal_decompose` recovered a slope of **0.7294** and an
amplitude of **24.9188**.

**That is the check worth doing.** On real data you cannot verify a
decomposition — so verify the *method* on data whose answer you already know.

**And the twelve monthly seasonal values summed to 3.6 × 10⁻¹⁵ — zero.** An
additive seasonal component is *defined* to average out over a full cycle,
which is why it can be subtracted without shifting the level.

### 💡 Classical decomposition against STL

| | Classical | **STL** |
|---|---|---|
| Seasonal pattern | **one, repeated identically** | may **evolve** |
| Outliers | distort it | **robust option** |
| Missing at the ends | **yes — 12 of 120 points** | **none** |
| Speed | fast | fast |

**Classical decomposition lost six observations at each end**, because a
centred 12-month moving average cannot be computed there. **STL covers the
whole series**, which is why it is the modern default — and worth naming.

---

## 1.3 Stationarity

### 🎯 The definition, and it is examined verbatim

A series is **weakly (covariance) stationary** if:

1. **E[yₜ] = μ** — constant mean, no trend
2. **Var(yₜ) = σ²** — constant variance
3. **Cov(yₜ, yₜ₊ₖ) = γ(k)** — the autocovariance depends **only on the gap k**,
   not on t

**Strict stationarity** requires the whole joint distribution to be
time-invariant. It is stronger, rarely testable, and almost never what is
meant. **Say "weakly stationary" and you are right.**

### 💡 Why it matters, in one line

> **You cannot learn a rule from the past that applies to the future unless
> the rule is the same in both.**

Stationarity is exactly that assumption written formally. A model fitted to a
series whose mean is drifting has learned a mean that no longer exists.

### What makes a series non-stationary

| Cause | Fix |
|---|---|
| **Trend** (deterministic) | **detrend** — regress on t and keep the residuals |
| **Trend** (stochastic, a unit root) | **difference** |
| **Seasonality** | **seasonal difference** at lag m |
| **Changing variance** | **log or Box-Cox** transform |
| **Structural break** | split the series, or add a dummy |

### ⚠️ The distinction the exam wants

**A deterministic trend and a stochastic trend need different treatments**,
and they look identical on a plot.

- `y = a + bt + ε` — **trend-stationary.** Detrend it. Shocks die out.
- `y = y₋₁ + ε` — **a unit root.** Difference it. **Shocks are permanent.**

**Difference a trend-stationary series and you over-difference it.** Detrend a
unit-root series and it is still non-stationary. Unit 3 shows how the two
tests together tell them apart.

---

## 1.4 Autocovariance and autocorrelation

### 📖 The definitions

$$\gamma(k) = \text{Cov}(y_t,\, y_{t+k}) \qquad
\rho(k) = \frac{\gamma(k)}{\gamma(0)}$$

**ρ(k) is just γ(k) scaled so ρ(0) = 1**, which makes it comparable across
series with different units. That is the only difference, and it is why the
ACF and not the autocovariance is what you plot.

### The PACF, which is the harder one

**ρ(k) measures the total correlation between yₜ and yₜ₊ₖ — including
everything transmitted through the points in between.**

**The partial autocorrelation φ_kk measures the correlation that remains after
removing the effect of lags 1 … k−1.**

> **In an AR(1) with φ = 0.8, ρ(2) = 0.64 — but not because y₋₂ influences y
> directly. It influences y₋₁, which influences y. The PACF at lag 2 is
> therefore 0, and that zero is what identifies the order.**

### 🎯 The two identification rules — the whole of Unit 2's preparation

| Pattern | Model |
|---|---|
| **ACF cuts off** after lag q, PACF tails off | **MA(q)** |
| **PACF cuts off** after lag p, ACF tails off | **AR(p)** |
| **Both tail off** | **ARMA(p,q)** |
| Neither decays | **non-stationary — difference first** |

**"Cuts off"** means drops inside the confidence band and stays there.
**"Tails off"** means decays gradually.

### 🔢 Both rules, checked against known truth

On an **AR(2) built with φ = (0.6, −0.3)**, 400 observations:

```
PACF significant at lags: [1, 2, 8]
```

**The PACF cut off after lag 2, and the true order is 2.** Lag 8 pokes outside
by chance — with a 95% band, about 1 lag in 20 does.

On an **MA(1) built with θ = 0.7**:

```
ACF significant at lags: [1, 3]
ACF at lag 1 = 0.4879,  theory says theta/(1+theta^2) = 0.4698
```

**The ACF cut off after lag 1, and landed on the value theory predicts.** An
MA(q) has **exactly zero** autocorrelation beyond lag q — not small, zero —
because yₜ and yₜ₋q₋₁ share no shocks at all.

On an **ARMA(1,1)**: both tail off, neither cuts. **That is the ARMA
signature**, and it is why ARMA orders are chosen by AIC rather than by eye.

### ⚠️ The confidence band, and the mistake it causes

The band is **±1.96/√n**. On 400 observations that is **±0.098**.

**Measured on white noise: 0 of 20 lags fell outside.** You *expect* about one
in twenty by chance. **Reading structure into one stray spike is the commonest
correlogram mistake**, and it is why the Ljung-Box test (Unit 2) tests the
lags **jointly**.

---

## 1.5 The forecasting process

### 📖 The Box–Jenkins loop

```
   1. PLOT the series          <- never skip this
        │
   2. TRANSFORM if needed      (log for growing variance)
        │
   3. DIFFERENCE to stationary (ADF/KPSS decide)
        │
   4. IDENTIFY p and q         (ACF and PACF)
        │
   5. ESTIMATE                 (maximum likelihood)
        │
   6. DIAGNOSE  ────── fails ──┘  (Ljung-Box on residuals)
        │ passes
   7. FORECAST, with intervals
        │
   8. EVALUATE against a baseline
```

**Step 6 loops back.** A model that fails its residual check is not a model
you tune — it is a model you re-identify.

### 🎯 And the step everyone skips

**Step 1.** Every failure to identify a model correctly starts with not
looking at the plot. Four questions answer themselves in five seconds:

1. Is there a **trend**?
2. Is there **seasonality**, and at what period?
3. Is the **variance constant**, or does it grow with the level?
4. Are there **outliers** or **level shifts**?

---

## 1.6 Model evaluation metrics

Covered in depth in Unit 5, but the shapes belong here.

| Metric | Formula | Units | Watch for |
|---|---|---|---|
| **RMSE** | √(mean e²) | the data's | **punishes large errors hard** |
| **MAE** | mean \|e\| | the data's | treats all errors alike |
| **MAPE** | mean \|e/y\| × 100 | **percent** | **explodes near y = 0** |
| **MASE** | MAE / MAE of naive | **scale-free** | needs a stated baseline |

### 🔢 RMSE and MAE can rank two forecasts differently

| Forecast | RMSE | MAE |
|---|---:|---:|
| A: off by 2 every month | **2.000** | 2.000 |
| B: perfect, then off by 15 once | 4.743 | **1.500** |

**RMSE prefers A; MAE prefers B.** Neither is wrong — they answer different
questions. **Choose from the cost of being wrong**, and choose *before* you
see the results.

### ⚠️ And the baseline you must beat

**Naive:** ŷₜ₊ₕ = yₜ. **Seasonal naive:** ŷₜ₊ₕ = yₜ₊ₕ₋ₘ.

**Measured:** seasonal naive scored **RMSE 14.152** on the lab's held-out year;
the fitted SARIMA scored **6.891**, a **51% improvement**.

> **An RMSE means nothing until you know what repeating last year scores.**
> Seasonal naive is this course's `DummyClassifier`, and a surprising number
> of published forecasting models fail to beat it.

---

## Practice problems

**1. Is the daily closing price of a stock stationary? Is its daily return?**

**The price: no.** It is close to a random walk — a unit root, so shocks are
permanent and the variance grows without bound. The lab's random walk gave
**ADF p = 0.2197**, failing to reject a unit root as it must.

**The return: approximately yes.** rₜ = log(pₜ) − log(pₜ₋₁) is the differenced
log price. Differencing removes the unit root, and the lab's differenced
random walk gave **ADF p = 0.0000**.

**But not fully stationary**, and this is worth the extra mark: returns show
**volatility clustering** — quiet periods and turbulent periods — so the
*variance* is not constant. The mean is stationary and the variance is not,
which is exactly why GARCH models exist.

**2. An ACF decays slowly and almost linearly, still above 0.5 at lag 20. What
does that tell you, and what do you do?**

**The series is non-stationary.** A stationary process has an ACF that decays
geometrically to zero; one that stays high for twenty lags is the signature of
a trend or a unit root.

**Do not try to identify p and q from it** — the identification rules assume
stationarity and are meaningless here.

**Do this instead:** run the ADF *and* KPSS. If ADF fails to reject and KPSS
rejects, difference once and re-plot. If ADF rejects under `regression="ct"`
but not under `"c"`, the series is **trend-stationary** — detrend, do not
difference.

**3. Sketch the ACF and PACF for white noise, AR(1) with φ = 0.8, and MA(1)
with θ = 0.5.**

| | ACF | PACF |
|---|---|---|
| **White noise** | ρ(0) = 1, then **all ≈ 0** | **all ≈ 0** |
| **AR(1), φ = 0.8** | **geometric decay**: 0.8, 0.64, 0.512, 0.41 … | **spike of 0.8 at lag 1, then 0** |
| **MA(1), θ = 0.5** | **spike at lag 1 only**: θ/(1+θ²) = **0.4** | **decays, alternating sign** |

**The AR(1) ACF is φ^k exactly** — that is worth memorising, because it lets
you read φ straight off the plot.

**4. Why is a random split invalid, and what replaces it?**

**Because a random split puts future observations in the training set.** The
model then interpolates a gap it has seen both sides of, which is not
forecasting — and it scores far too well, so the error you report is not the
error you will get.

**Replace it with:**

- a **held-out tail** — the last h observations, never a random h
- **rolling-origin cross-validation** for model selection: train on [0, t),
  forecast the next h, score, move t forward. The lab used **6 rolling folds**.

**Every fold trains only on the past.** That is the whole requirement.

**5. Your series has 60 monthly observations. Can you fit SARIMA(2,1,2)(1,1,1)₁₂?**

**Technically yes; sensibly no.**

Count what you are asking for: **2 + 2 + 1 + 1 = 6 ARMA parameters plus a
variance = 7.** Then d = 1 costs one observation and D = 1 costs twelve, so
you are fitting 7 parameters to **47 usable observations** — and the seasonal
terms are estimated from **fewer than 4 complete annual cycles**.

**The rules of thumb worth quoting:**

- at least **2–3 full seasonal cycles** to estimate a seasonal component at all
- at least **10 observations per parameter**, and more is better
- **60 monthly points is 5 years**, which is thin for anything seasonal

**What to do instead:** fit the airline model, **SARIMA(0,1,1)(0,1,1)₁₂** —
two parameters — and let a rolling-origin CV tell you whether anything larger
earns its keep. In the lab it did not: the airline model had the **best
held-out RMSE of all four specifications tried**.

---

## Exam questions from this unit

**Two marks**

1. Define weak stationarity.
2. Name the four components of a time series.
3. Give one difference between seasonality and a cycle.
4. When do you use a multiplicative decomposition?
5. Write the relation between γ(k) and ρ(k).
6. What does the PACF measure that the ACF does not?
7. State the two identification rules.
8. What is the ACF confidence band?

**Five marks**

1. Explain stationarity and why it is required.
2. Distinguish a deterministic from a stochastic trend, and the treatment of
   each.
3. Explain the ACF and PACF and how they identify AR and MA orders.
4. Describe the Box–Jenkins forecasting process.
5. Compare classical decomposition with STL.

**Ten marks**

1. Explain the components of a time series and both decomposition models with
   worked reasoning, and describe how you would decide between them.
2. Explain stationarity, autocovariance and autocorrelation in full, and show
   how the ACF and PACF identify a model, with sketches for white noise, AR(1)
   and MA(1).

---

## Mistakes that cost marks

- **Using a random train/test split.** It is the defining error of the course.
- **Confusing seasonality with a cycle.** Fixed period against variable.
- **Saying "stationary" without saying which kind.** Weak, unless you mean
  strict and can defend it.
- **Reading order from an ACF that has not decayed.** Difference first.
- **Treating one lag outside the band as structure.** One in twenty is
  expected.
- **Saying the PACF measures "correlation at lag k".** So does the ACF; the
  PACF removes the intervening lags.
- **Quoting an RMSE with no baseline.** Seasonal naive scored 14.152.
- **Forgetting that you observe one realisation.** A single coefficient
  estimate 2.5 standard errors out is a draw, not a refutation.
