# Unit 2 — ARMA and Forecasting with ARMA

**Syllabus topics:** ARMA(p,q) models: definition, estimation, forecasting
approaches. Model identification: AIC, PACF/ACF, diagnostic checks. Practical
examples of fitting ARMA and generating forecasts.

---

## 2.1 The three models, in one place

### 📖 AR(p) — regress the series on its own past

$$y_t = c + \phi_1 y_{t-1} + \dots + \phi_p y_{t-p} + \varepsilon_t$$

**"Today is a weighted sum of recent days, plus a shock."** A shock enters and
then **decays geometrically** — it never fully leaves, but its influence
shrinks by a factor of φ each period.

**Stationarity condition:** the roots of the characteristic polynomial must
lie outside the unit circle. For AR(1) that reduces to **|φ| < 1**, and
**φ = 1 is exactly the random walk** — the unit root of Unit 1.

### 📖 MA(q) — regress on past *shocks*

$$y_t = \mu + \varepsilon_t + \theta_1\varepsilon_{t-1} + \dots + \theta_q\varepsilon_{t-q}$$

**"Today is this period's shock plus an echo of the last q shocks."** A shock
influences exactly q+1 periods and then **vanishes completely**.

**An MA(q) is always stationary** — it is a finite sum of finite-variance
terms. What it needs instead is **invertibility** (|θ| < 1), so that it can be
rewritten as an infinite AR, which is what makes its parameters identifiable.

### 🎯 The difference in one line

> **An AR shock decays forever. An MA shock stops dead after q periods.**

That is why the ACF of an MA(q) is **exactly zero** beyond lag q, and the ACF
of an AR decays but never quite reaches zero.

### ARMA(p,q) — both

$$y_t = c + \sum_{i=1}^{p}\phi_i y_{t-i} + \varepsilon_t + \sum_{j=1}^{q}\theta_j\varepsilon_{t-j}$$

**Why bother?** Parsimony. A process needing AR(8) alone often needs only
ARMA(1,1) — two parameters instead of eight, estimated from the same data.

---

## 2.2 Identification

### The rules again, because they are the whole unit

| Pattern | Model |
|---|---|
| ACF **cuts off** at q, PACF tails off | **MA(q)** |
| PACF **cuts off** at p, ACF tails off | **AR(p)** |
| Both tail off | **ARMA(p,q)** — use AIC |

### 🔢 The MA(1) theoretical ACF, verified

For MA(1), theory gives:

$$\rho(1) = \frac{\theta}{1+\theta^2}, \qquad \rho(k) = 0 \text{ for } k > 1$$

With θ = 0.7: **0.7/1.49 = 0.4698**. The lab measured **0.4879** on 400
observations.

**That agreement is the check.** It also gives you a useful backwards trick:
**ρ(1) for an MA(1) can never exceed 0.5**, so an ACF with a lag-1 spike of
0.8 is not an MA(1) whatever else it is.

### ⚠️ Why ARMA orders cannot be read off the plot

When both functions tail off, **the correlogram tells you it is ARMA and not
which one.** That is not a limitation of your eye — the information genuinely
is not there. Hence AIC.

---

## 2.3 Estimation

### 📖 Maximum likelihood, via the Kalman filter

statsmodels writes the ARMA in **state-space form** and runs the **Kalman
filter** to evaluate the likelihood, then maximises it numerically.

**So you have been using a Kalman filter since your first `ARIMA(...).fit()`**
— which is worth knowing before Unit 4 introduces it as if it were new.

### 🔢 Does estimation work? Check against known truth

An AR(2) generated with **φ = (0.6, −0.3)**, n = 400:

| Param | True | Estimate | Std err | 95% CI | Covers? |
|---|---:|---:|---:|---|---|
| φ₁ | 0.600 | **0.7062** | 0.0428 | [0.6223, 0.7901] | **NO** |
| φ₂ | −0.300 | −0.3661 | 0.0475 | [−0.4591, −0.2731] | yes |

**φ₁'s interval misses the truth by 2.5 standard errors.** Before concluding
anything: **is the method wrong, or is this draw unusual?**

### 🎯 Repeat the experiment — that is the only way to tell

200 independent series, same length, same true φ:

| Param | True | Mean estimate | SD of estimate | Bias |
|---|---:|---:|---:|---:|
| φ₁ | 0.600 | **0.5980** | 0.0457 | **−0.0020** |
| φ₂ | −0.300 | −0.2991 | 0.0472 | +0.0009 |

**The estimator is unbiased**, and only **1 of 200** draws landed further out
than the one we used.

> **The method is right; that one series was unusual.** From a single dataset
> those two are indistinguishable — which is why nobody should quote a time
> series coefficient without its standard error.

### 🔢 And consistency, with more data

| n | φ₁ | φ₂ |
|---:|---:|---:|
| 200 | 0.6935 | −0.4483 |
| 400 | 0.7062 | −0.3661 |
| 1,000 | 0.6752 | −0.3477 |
| 4,000 | 0.6309 | −0.3208 |
| **16,000** | **0.6117** | **−0.3134** |

**The error shrinks at the usual 1/√n rate.** And the unglamorous practical
lesson: **400 monthly observations is 33 years of data and still leaves
two-decimal uncertainty.** Time series are data-poor by nature — you cannot
collect more of the past.

---

## 2.4 Diagnostic checking

### 📖 The four checks, in order of importance

| # | Check | Test | Pass means |
|---|---|---|---|
| **1** | **residuals are white noise** | **Ljung-Box** | no structure left to model |
| 2 | mean is zero | t-test | the forecast is unbiased |
| 3 | variance is constant | plot, or split-half ratio | intervals are trustworthy |
| 4 | normality | Jarque-Bera | intervals are exactly right |

### 🎯 The Ljung-Box test is the one that matters

$$Q = n(n+2)\sum_{k=1}^{h}\frac{\hat\rho_k^2}{n-k} \sim \chi^2_{h-p-q}$$

**H₀: the first h autocorrelations are jointly zero.** A **large** p-value is
what you want — the opposite of most tests.

**Measured on the correct AR(2) fit:** p = **0.7615**. No structure left.

**And note "jointly".** Checking each lag against its own 95% band flags one
in twenty by chance; testing them together does not.

### 🔢 What a mis-specified model looks like

| Model | AIC | Ljung-Box p | Verdict |
|---|---:|---:|---|
| AR(1) — **wrong order** | 1193.12 | **0.0000** | **structure remains** |
| AR(2) — correct | **1138.31** | 0.7615 | ok |

**Both signals point the same way**, and that agreement is what you want.

> **A model chosen by AIC alone, with no residual check, can be the best of a
> bad set.** The AIC comparison is *relative*; Ljung-Box is *absolute*.

---

## 2.5 Model selection by information criterion

$$\text{AIC} = -2\log L + 2k \qquad\qquad \text{BIC} = -2\log L + k\log n$$

**Both are (badness of fit) + (penalty for complexity).** Lower is better, and
**the absolute value is meaningless** — only differences between models fitted
to *the same data* mean anything.

### 🎯 The difference between them, and it is the whole comparison

With n = 108, **log(108) = 4.68** — so **BIC penalises each parameter more
than twice as hard as AIC**, and therefore picks smaller models.

| | Property | Use when |
|---|---|---|
| **AIC** | **efficient** — picks the best *predictor* | **forecasting** |
| **BIC** | **consistent** — picks the *true* model if it is in the set | explanation |

**For this course, AIC.** You are forecasting, and you have no reason to
believe the true model is in your grid.

### 🔢 The measured comparison

| Model | k | AIC | BIC | CV RMSE |
|---|---:|---:|---:|---:|
| SARIMA(0,1,1)(0,1,1)₁₂ | 3 | 485.76 | 492.95 | 4.019 |
| **SARIMA(1,1,1)(0,1,1)₁₂** | 4 | **472.49** | **482.07** | 3.966 |
| **SARIMA(1,1,1)(1,1,1)₁₂** | 5 | 476.32 | 488.29 | **3.799** |
| SARIMA(2,1,1)(1,1,1)₁₂ | 6 | 478.28 | 492.65 | 3.836 |
| SARIMA(2,1,2)(1,1,1)₁₂ | 7 | 474.66 | 491.33 | 3.927 |

**AIC and BIC agreed here**, on the 4-parameter model. That happens when one
specification is clearly better than its neighbours — the heavier BIC penalty
only bites when two models fit almost equally well.

**But rolling-origin CV chose a different model**, the 5-parameter one. **AIC
estimates out-of-sample error from a formula and an assumption; CV measures
it.** When you can afford the refits, measure.

### ⚠️ AIC and held-out error can disagree

On the experiment 6 grid, **lowest AIC was SARIMA(1,1,1)(1,1,1)₁₂** and
**lowest test RMSE was SARIMA(0,1,1)(0,1,1)₁₂** — the smaller model.

**They ask different questions.** AIC measures in-sample fit with a penalty;
test RMSE measures error on data the model never saw. **When they disagree,
the held-out error answers "will this forecast well?"**

That is **Course 12 A's bias–variance trade-off** arriving in a new costume:
the larger model fits the training data better and generalises worse.

---

## 2.6 Forecasting

### 📖 How an ARMA forecast is computed

**Recursively, replacing what you do not know with its expectation:**

- future **y** values → their forecasts
- future **ε** shocks → **zero** (their expectation)
- past ε shocks → the model's residuals

**For an AR(1), ŷₜ₊ₕ = μ + φʰ(yₜ − μ).** As h grows, φʰ → 0 and the forecast
**converges on the unconditional mean**. A stationary series forgets where it
started.

### 🔢 Prediction intervals, and why they widen

Measured, SARIMA on the sales series:

| h | Actual | Forecast | 95% interval | Width |
|---:|---:|---:|---|---:|
| 1 | 181.73 | 178.89 | [170.71, 187.07] | **16.36** |
| 6 | 200.10 | 200.27 | [190.95, 209.60] | 18.66 |
| 12 | 190.48 | 175.11 | [165.77, 184.44] | **18.67** |

**The interval widens because Var(yₜ₊ₕ | data) accumulates every shock between
now and t+h.** That is not a defect — it is the model correctly reporting that
it knows less about next December than about next month.

### 🔢 Two shapes of widening, both measured

| h | Random walk width | ÷ √h × width(1) | AR(1) width |
|---:|---:|---:|---:|
| 1 | 3.455 | **1.0000** | 3.921 |
| 4 | 6.909 | **1.0000** | 4.541 |
| 9 | 10.364 | **1.0000** | 4.551 |
| 16 | 13.819 | **1.0000** | **4.551** |

**The random walk's interval is exactly √h times its one-step width** — the
ratio column is 1.0000 at every horizon, because a unit root accumulates
variance linearly.

**The AR(1)'s stops growing** at the unconditional variance. **That contrast
is the difference between a series you can forecast far ahead and one you
cannot.**

### ⚠️ And the coverage, reported honestly

**Nominal 95%, empirical 9/12 = 75%.** Two things are going on:

1. **Twelve points is a tiny sample.** Under a true 95% interval, 9 or fewer
   hits out of 12 has probability **0.020** — unusual, not damning.
2. **SARIMA intervals are known to be too narrow.** They treat the fitted
   parameters as if they were the true ones, pricing in *shock* uncertainty
   and ignoring **estimation** uncertainty. With 108 observations and 5
   parameters, that omission is not small.

**If the interval matters for a decision, widen it — or get it by bootstrap or
backtesting rather than from the formula.**

---

## Practice problems

**1. An ACF has a single spike of 0.45 at lag 1 and nothing after. The PACF
decays with alternating signs. Identify the model and estimate its parameter.**

**MA(1)** — ACF cuts off at lag 1, PACF tails off.

**And you can recover θ from the plot.** Solve ρ(1) = θ/(1+θ²) = 0.45:

$$0.45\theta^2 - \theta + 0.45 = 0 \;\Rightarrow\; \theta = \frac{1 \pm \sqrt{1-0.81}}{0.9}$$

giving **θ ≈ 0.6** or **θ ≈ 1.67**. Take **0.6** — the other root is not
invertible, and for every MA(1) there is a θ and a 1/θ producing an identical
ACF. **Invertibility is what picks one.**

**Sanity check:** ρ(1) for an MA(1) can never exceed 0.5, and 0.45 is
comfortably under.

**2. Your ARMA(1,1) fit has Ljung-Box p = 0.003. What do you do, in order?**

**p = 0.003 rejects white noise — structure remains. Do not tune; re-identify.**

1. **Plot the residual ACF and PACF.** *Which* lags are significant? A spike
   at lag 12 on monthly data means you have missed **seasonality**, not that
   you need a larger p.
2. **Check stationarity again.** If the original was under-differenced, no
   ARMA order will fix it.
3. **Increase p or q by one**, guided by which function is significant, and
   re-check.
4. **Look for outliers or a level shift.** One intervention can create
   apparent autocorrelation in the residuals.

**What not to do:** raise p and q together until the test passes. That is
fitting noise, and AIC will tell you so.

**3. Explain why an AR(1) forecast converges to the mean but a random walk
forecast does not.**

**AR(1):** ŷₜ₊ₕ = μ + φʰ(yₜ − μ). With |φ| < 1, **φʰ → 0**, so the forecast
decays to μ. The process is *mean-reverting* — shocks decay geometrically.

**Random walk (φ = 1):** ŷₜ₊ₕ = yₜ **for every h**. φʰ = 1 always, so the best
forecast of every future value is today's value. **Shocks are permanent** —
there is no mean to revert to, and the unconditional variance is infinite.

**Measured consequence:** the AR(1)'s interval flattened at width 4.551; the
random walk's grew as **exactly √h**, reaching 13.819 by h = 16.

**4. Why is an ARMA(1,1) sometimes preferable to an AR(8)?**

**Parsimony, and the standard errors that follow from it.**

An ARMA(1,1) has **2 parameters**; an AR(8) has **8**. Fitted to the same 200
observations, that is 25 observations per parameter against 100 — and the
standard errors scale accordingly.

**The deeper reason:** an ARMA(1,1) is an **infinite AR** with geometrically
decaying weights. If the true process has that shape, an AR(8) is a truncated
approximation to it, spending eight parameters to imitate what two describe
exactly.

**AIC will usually say so**, because it penalises the six extra parameters
that bought almost no extra likelihood.

**5. You fit ARMA(2,1) and one coefficient has a t-statistic of 0.4. What does
that mean and what do you do?**

**|t| = 0.4 means the coefficient is indistinguishable from zero** — its 95%
interval comfortably contains 0, and it is contributing noise rather than
signal.

**Drop it and refit** — but drop *one* term, not both, and check:

- Does **AIC fall**? It usually does, since you removed a parameter that
  bought no likelihood.
- Does **Ljung-Box still pass**? If removing it leaves structure in the
  residuals, it was doing something after all.

**The exception worth knowing:** in a SARIMA you do not drop an intermediate
lag to "tidy up" — dropping φ₁ while keeping φ₂ gives a model whose
interpretation and stationarity conditions are much less standard. Reduce the
order, do not punch holes in it.

---

## Exam questions from this unit

**Two marks**

1. Write the AR(p) equation.
2. Write the MA(q) equation.
3. State the stationarity condition for AR(1).
4. What is invertibility, and which model needs it?
5. What is the maximum possible ρ(1) for an MA(1)?
6. State the Ljung-Box null hypothesis.
7. Give the AIC and BIC formulas.
8. Why does a prediction interval widen with the horizon?

**Five marks**

1. Compare AR and MA models on shock persistence and ACF shape.
2. Explain the Box–Jenkins identification rules with sketches.
3. Explain the residual diagnostic checks and why Ljung-Box is joint.
4. Compare AIC and BIC, and say which suits forecasting.
5. Explain how an ARMA forecast is computed and why it converges to the mean.

**Ten marks**

1. Explain ARMA models in full — definition, identification, estimation,
   diagnostics and forecasting — with worked reasoning at each step.
2. Given an ACF and PACF, identify a model, justify the order, describe how
   you would validate it, and explain what you would do if the validation
   failed.

---

## Mistakes that cost marks

- **Saying an MA(q) needs a stationarity condition.** It is always stationary;
  it needs *invertibility*.
- **Reading ρ(1) = 0.8 as an MA(1).** Impossible — the maximum is 0.5.
- **Wanting a small Ljung-Box p-value.** You want a large one.
- **Testing each ACF lag separately.** Ljung-Box is joint for a reason.
- **Comparing AIC across different datasets or different differencing.** Only
  same-data comparisons mean anything.
- **Choosing by AIC with no residual check.** Best of a bad set.
- **Quoting a coefficient without its standard error.** The lab's φ₁ landed
  2.5 SE from the truth on one draw.
- **Reporting a nominal 95% interval as if it were the measured coverage.**
  Here it was 75%.
