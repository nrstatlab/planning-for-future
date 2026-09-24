# Unit 4 — State-Space and Multivariate Time Series

**Syllabus topics:** Multivariate time series: Vector ARMA models (VARMA),
estimation, forecasting. State-space representation: formulation, Kalman
filter basics, forecasting in state-space models.

---

## The unit that is two units

**These are two genuinely different frameworks that happen to share a page.**

- **Multivariate** asks: *what if several series influence each other?*
- **State-space** asks: *what if the thing I want to model is hidden, and I
  only see noisy evidence of it?*

They meet at one point — a VAR can be written in state-space form — but learn
them separately.

---

## 4.1 Vector autoregression

### 📖 The model

A **VAR(p)** puts every lag of every variable into every equation:

$$\mathbf{y}_t = \mathbf{c} + \mathbf{A}_1\mathbf{y}_{t-1} + \dots + \mathbf{A}_p\mathbf{y}_{t-p} + \boldsymbol{\varepsilon}_t$$

where **yₜ is a k-vector** and each **Aᵢ is a k×k matrix**.

### ⚠️ Count the parameters before you fit one

**k²p + k**, plus **k(k+1)/2** in the covariance matrix.

| k | p | Coefficients |
|---:|---:|---:|
| 3 | 1 | **12** |
| 3 | 4 | **39** |
| 5 | 4 | **105** |
| 10 | 4 | **410** |

**This is why VARs are limited to three or four variables in practice.** The
parameter count grows with the *square* of the number of series, and a
macroeconomic dataset has 200 quarterly observations at best.

### 🔢 Does it recover a known structure?

The lab generated three series with a **known** lag structure:

```
gdp[t]          = 0.6*gdp[t-1] + e
inflation[t]    = 0.3*inflation[t-1] + 0.5*gdp[t-1] + e
unemployment[t] = 0.5*unemp[t-1] - 0.4*gdp[t-1] + e
```

**So GDP drives the other two, and nothing drives GDP.** The fitted VAR(1):

| Equation ↓ / lagged ↓ | gdp | inflation | unemployment |
|---|---:|---:|---:|
| **gdp** | 0.6336 | **0.0214** | **0.0707** |
| **inflation** | **0.4275** | 0.3154 | 0.0457 |
| **unemployment** | **−0.4312** | 0.1197 | 0.5224 |

**It recovered the structure — including the two zeros it was never told
about.** A VAR is *atheoretical*: it puts everything in and lets the data
decide, which is its strength and the reason it needs so much data.

### 🎯 Granger causality

**H₀: past values of X do not help predict Y, given Y's own past.**

| X | → | Y | p-value | Result | Matches truth? |
|---|---|---|---:|---|---|
| gdp | → | inflation | **0.0000** | causes | **as built** |
| gdp | → | unemployment | **0.0000** | causes | **as built** |
| inflation | → | gdp | 0.6910 | no evidence | **as built** |
| unemployment | → | gdp | 0.1367 | no evidence | **as built** |

**All four match, including both non-causal directions.** That is the harder
half — *a test that only ever finds effects is not a test.*

### ⚠️ The warning that belongs with every Granger result

> **"Granger causes" means "helps predict", and nothing more.**

It cannot distinguish a real cause from a **common third driver** that moves
one series before the other, and it says nothing about what would happen if
you *intervened*.

**Ice cream sales Granger-cause drownings.** Both are driven by summer.

**Say "X Granger-causes Y" out loud. Never "X causes Y".** Clive Granger
himself was explicit about this, and examiners look for it.

### 🔢 When a VAR helps, and when it does not

| Series | VAR RMSE | Univariate AR(1) RMSE | Winner |
|---|---:|---:|---|
| **gdp** | 1.0782 | **1.0574** | **univariate** |
| inflation | **1.1248** | 1.1949 | VAR |
| unemployment | **1.3192** | 1.3663 | VAR |

**The VAR lost on GDP and won on the other two — and that is exactly right.**

GDP was built as a pure AR(1) with **nothing feeding into it**, so the VAR's
extra coefficients are estimating zeros: pure variance, no signal. Inflation
and unemployment **do** depend on lagged GDP, and there the VAR has real
information the univariate model cannot see.

> **A VAR helps only where cross-series information exists.** Fitting one to
> unrelated series buys you k²p parameters and nothing else.

### VARMA, and why nobody uses it

The syllabus says **VARMA**. It exists — add a moving-average matrix
polynomial — and it is **almost never used**, for one good reason:
**identification**. Different VARMA parameterisations can produce identical
dynamics, so the estimates are not unique without extra restrictions.

**A VAR with enough lags approximates any VARMA**, and it is identified. Say
that if asked why practice is all VAR.

### 📖 And two things a VAR needs that a univariate model does not

**Cointegration.** If two series are individually non-stationary but a linear
combination of them is stationary, differencing them separately **throws away
the long-run relationship**. Use a **VECM** (vector error correction model)
instead. Testing for it is the **Johansen procedure**.

**Ordering, for impulse responses.** A VAR's shocks are correlated across
equations, so to interpret "a shock to GDP" you must decide which variable
moves first — a **Cholesky ordering**, and it is an assumption you impose, not
one the data supplies.

---

## 4.2 State-space models

### 🎯 The framework, in two equations

$$\begin{aligned}
\textbf{state:} \quad & \mathbf{x}_t = \mathbf{T}\mathbf{x}_{t-1} + \mathbf{R}\boldsymbol{\eta}_t \\
\textbf{observation:} \quad & \mathbf{y}_t = \mathbf{Z}\mathbf{x}_t + \boldsymbol{\varepsilon}_t
\end{aligned}$$

- **xₜ is the state** — unobserved, and what you actually want to know
- **yₜ is the observation** — what you get to see, contaminated by noise
- **T** says how the world evolves; **Z** says how it is measured

**The state is hidden. The filter's job is to infer it from noisy
observations, optimally, one step at a time.**

### 💡 You have been using one since Unit 2

**statsmodels writes every ARIMA in state-space form and runs the Kalman
filter to evaluate its likelihood.** So the framework is not new machinery
bolted on at the end — it is what has been underneath all along.

### 📖 The Kalman filter, as a loop

```
   for each t:
     PREDICT:  x̂ₜ|ₜ₋₁ = T x̂ₜ₋₁       (where do I think the state is?)
               Pₜ|ₜ₋₁ = T Pₜ₋₁ Tᵀ + Q  (how sure am I?)

     observe yₜ

     UPDATE:   Kₜ = Pₜ|ₜ₋₁ Zᵀ (Z Pₜ|ₜ₋₁ Zᵀ + R)⁻¹      <- the KALMAN GAIN
               x̂ₜ = x̂ₜ|ₜ₋₁ + Kₜ(yₜ − Z x̂ₜ|ₜ₋₁)
               Pₜ  = (I − Kₜ Z) Pₜ|ₜ₋₁
```

### 🎯 The Kalman gain is the whole idea

**K decides how much to trust the new observation against your prediction.**

- **measurement noise small** → K large → **follow the data**
- **measurement noise large** → K small → **trust the model**

It is a weighted average whose weights are chosen optimally, and it updates
itself as the uncertainty changes. **That is the sentence to write in an
exam.**

### 🔢 What it recovered, measured

An unobserved-components model — local linear trend plus seasonal — fitted to
the sales series:

| Component | Variance |
|---|---:|
| `sigma2.irregular` | 6.5360 |
| `sigma2.level` | 8.4278 |
| **`sigma2.trend`** | **0.0000** |
| **`sigma2.seasonal`** | **0.0000** |

**The two zeros are a result, not a failure.** The filter is saying those
components **do not vary** — the slope is a fixed number and the seasonal
pattern repeats exactly. **Which is true: the series was built that way.**

**And the estimated level implies a trend slope of 0.8378 against a true
0.8** — the same answer Unit 1's decomposition gave, reached a completely
different way.

> **Decomposition splits a series after the fact. A state-space model treats
> the components as unobserved states and estimates them jointly with the
> parameters.**

### 🔢 Missing observations, handled natively

Six observations were deleted from the middle of the series:

| t | True | Estimate | Error |
|---:|---:|---:|---:|
| 40 | 154.10 | 149.62 | −4.48 |
| 41 | 149.24 | 138.22 | −11.02 |
| 42 | 138.29 | 123.89 | −14.39 |
| 43 | 120.92 | 119.18 | −1.74 |
| 44 | 114.22 | 107.78 | −6.44 |
| 45 | 111.92 | 103.81 | −8.11 |

**RMSE over the gap: 8.745, against a series standard deviation of 31.08.**

**No imputation step was run.** The filter simply skips the update at a
missing time and keeps predicting the state forward, so **a gap costs
precision and nothing else**.

> **Every other method in this course would need the hole filled first — and
> filling it with the mean, which is the usual reflex, injects a fake
> observation the model then trusts.**

### What state-space does that ARIMA cannot

| Capability | ARIMA | State-space |
|---|---|---|
| **missing observations** | refit around them | **handled natively** |
| time-varying parameters | no | **yes** |
| components you can inspect | no | **yes** |
| real-time updating | refit | **one recursion** |
| several related series | no | yes |

### 💡 And the property that matters in production

**The filter is recursive.** A new observation costs **one update step**, not
a refit — so a state-space model updates in constant time as data arrives,
which is why Kalman filters run in navigation systems, on satellites, and in
anything that must track a state live.

---

## Practice problems

**1. You have 8 quarterly macro series and 25 years of data. Can you fit a
VAR(4)?**

**No.** Count first:

- Observations: 25 × 4 = **100**
- Coefficients: k²p + k = 64 × 4 + 8 = **264**
- Plus a covariance matrix: k(k+1)/2 = **36**

**264 coefficients from 100 observations is not estimable** — the system is
badly under-determined, and even VAR(1) at 72 coefficients is hopeless.

**What to do:**

1. **Reduce k.** Pick the 3–4 series the question is actually about. This is
   the standard answer and usually the right one.
2. **Reduce p.** Let AIC choose; quarterly data often needs only 1–2.
3. **Use a Bayesian VAR**, whose priors shrink distant lags toward zero — the
   standard tool in macroeconomics for exactly this problem.
4. **Use a factor model.** Extract 2–3 principal components from the 8 series
   and fit a VAR to those.

**2. Explain the difference between the Kalman filter and the Kalman
smoother.**

| | Uses | Answers |
|---|---|---|
| **Filter** | data up to **t** | "what is the state **now**?" |
| **Smoother** | **all** the data | "what **was** the state at t?" |

**The filter is causal and real-time** — it is what a navigation system runs,
because it cannot use observations that have not happened.

**The smoother is a backward pass after the forward one**, and it is strictly
more accurate at every interior point because it uses future observations too.

**Which to use:** the filter for live estimation and forecasting; the smoother
for **retrospective analysis** — decomposing a historical series, or
estimating the gap in the lab's missing-data demonstration.

**3. Your VAR says X Granger-causes Y with p < 0.001. A colleague concludes X
causes Y. What do you say?**

**That the test does not support that conclusion, and three specific reasons
why.**

1. **Granger causality is about prediction, not mechanism.** All it establishes
   is that X's past improves a forecast of Y beyond Y's own past.
2. **A common driver produces exactly this pattern.** If Z drives both, and
   reaches X before Y, then X Granger-causes Y with no causal link between
   them at all.
3. **It is sensitive to what you left out.** Add the omitted variable and the
   relationship can disappear — which is not true of a real causal effect.

**And a fourth, if the series are non-stationary:** Granger tests on
non-stationary data produce **spurious significance**. Difference first, or
use a VECM if the series are cointegrated.

**What would support a causal claim:** an intervention, a natural experiment,
or an instrument — none of which a VAR provides.

**4. Why is a local-level model equivalent to exponential smoothing?**

**The local-level model is:**

$$y_t = \mu_t + \varepsilon_t, \qquad \mu_t = \mu_{t-1} + \eta_t$$

**Its steady-state Kalman filter update is:**

$$\hat\mu_t = \hat\mu_{t-1} + K(y_t - \hat\mu_{t-1}) = K y_t + (1-K)\hat\mu_{t-1}$$

**which is simple exponential smoothing with α = K.**

**So they are the same model**, and the equivalence is useful in both
directions: it gives exponential smoothing a **statistical foundation** —
prediction intervals, likelihood, AIC — that the ad-hoc version lacks, and it
gives the state-space model an **interpretation** anyone can follow.

**And it explains α.** The smoothing constant is not arbitrary: it is the
Kalman gain, determined by the ratio of state noise to measurement noise. A
noisy sensor gives small α; a reliable one gives large α.

**5. When is a state-space model worth the extra complexity over ARIMA?**

**Five situations, in rough order of how often they arise:**

1. **Missing data.** ARIMA needs a complete series; the filter handles gaps
   natively, as the lab measured.
2. **You need the components.** If someone will ask "how much of that rise was
   trend and how much was seasonal?", ARIMA cannot answer and an
   unobserved-components model can.
3. **Parameters that change over time.** A relationship that drifts — a
   changing seasonal shape, a slope that shifts after an intervention — needs
   time-varying coefficients, which ARIMA does not have.
4. **Real-time updating.** One recursion per new observation instead of a
   refit.
5. **Irregular spacing or mixed frequency.** Monthly and quarterly series in
   one model is routine in state space and awkward otherwise.

**When ARIMA is enough:** a complete, regularly-spaced, single series where
you want a forecast and nothing else. **Which is most of the time** — and
"use the simpler model that answers the question" is a defensible exam
position, provided you can name what you would gain by not doing so.

---

## Exam questions from this unit

**Two marks**

1. Write the VAR(p) equation.
2. How many coefficients has a VAR(2) with 4 variables?
3. State the Granger causality null hypothesis.
4. Why is VARMA rarely used?
5. Write the two state-space equations.
6. What is the Kalman gain?
7. Give one difference between the Kalman filter and smoother.
8. How does a state-space model handle missing data?

**Five marks**

1. Explain VAR models and their parameter-count problem.
2. Explain Granger causality and its limitations.
3. Explain the state-space formulation and the role of each matrix.
4. Explain the Kalman filter's predict–update cycle.
5. Say when a state-space model is preferable to ARIMA, with reasons.

**Ten marks**

1. Explain multivariate time-series modelling in full — VAR, estimation,
   Granger causality, forecasting — and discuss when it beats a univariate
   model and when it does not.
2. Explain state-space models and the Kalman filter completely, with the
   equations, and relate them to models covered earlier in the course.

---

## Mistakes that cost marks

- **Saying Granger causality is causality.** It is predictability.
- **Fitting a VAR to eight series.** Count k²p first.
- **Assuming a VAR always beats a univariate model.** It lost on GDP.
- **Differencing cointegrated series separately.** Use a VECM.
- **Saying the Kalman filter needs complete data.** It is the one method that
  does not.
- **Treating state-space as unrelated to ARIMA.** Every ARIMA fit in this
  course ran a Kalman filter.
- **Confusing the filter with the smoother.** Causal against retrospective.
- **Reading a zero variance estimate as a convergence failure.** It means the
  component is deterministic.
