# Course 14 B — Practice Questions with Worked Solutions

Every figure quoted here is produced by
`labs/course-14b-timeseries/` and
checked by
`tools/run_timeseries_labs.py`.

---

## Section A — Two-mark questions

**1. Define weak stationarity.**
Constant mean, constant variance, and an autocovariance that depends **only on
the gap k**, not on t.

**2. Name the four components of a time series.**
Trend, seasonality, cyclical, irregular.

**3. Give one difference between seasonality and a cycle.**
**Seasonality has a fixed, calendar-determined period; a cycle's period
varies.** That is why SARIMA can model the first and not the second.

**4. When do you use a multiplicative decomposition?**
When the **seasonal swing grows with the level**. Fix it with a **log
transform**, which turns a multiplicative series into an additive one.

**5. Why does classical decomposition lose observations?**
A centred 12-month moving average cannot be computed at the ends —
**12 of 120 points**, six at each end. STL loses none.

**6. Write the relation between γ(k) and ρ(k).**
ρ(k) = γ(k)/γ(0). The ACF is the autocovariance scaled so ρ(0) = 1.

**7. What does the PACF measure that the ACF does not?**
The correlation at lag k **with the effect of lags 1 … k−1 removed**.

**8. State the two identification rules.**
**ACF cuts off at q → MA(q). PACF cuts off at p → AR(p).** Both tail off →
ARMA.

**9. What is the ACF confidence band?**
**±1.96/√n** — on 400 observations, ±0.098.

**10. How many lags do you expect outside a 95% band by chance?**
About **1 in 20**. The lab measured 0 of 20 on white noise.

**11. Write the AR(p) equation.**
yₜ = c + φ₁yₜ₋₁ + … + φₚyₜ₋ₚ + εₜ

**12. State the stationarity condition for AR(1).**
**|φ| < 1.** φ = 1 is the random walk — a unit root.

**13. Which model needs invertibility, and why?**
**MA.** So it can be rewritten as an infinite AR, which makes its parameters
identifiable — otherwise θ and 1/θ give the same ACF.

**14. What is the maximum possible ρ(1) for an MA(1)?**
**0.5.** ρ(1) = θ/(1+θ²), maximised at θ = 1.

**15. An ACF has a lag-1 spike of 0.8. Can it be an MA(1)?**
**No** — 0.8 exceeds the 0.5 maximum.

**16. State the Ljung-Box null hypothesis.**
The first h autocorrelations are **jointly zero**. You want a **large**
p-value.

**17. Why does Ljung-Box test lags jointly?**
Because testing each against its own 95% band would flag one in twenty by
chance.

**18. Give the AIC and BIC formulas.**
AIC = −2 log L + 2k. BIC = −2 log L + k log n.

**19. Which of AIC and BIC picks smaller models, and why?**
**BIC.** With n = 108, log(n) = 4.68, so it charges more than twice AIC's rate
per parameter.

**20. Which suits forecasting?**
**AIC** — it is *efficient*, picking the best predictor. BIC is *consistent*,
picking the true model if it is in the set.

**21. State the ADF null hypothesis.**
**There IS a unit root** (non-stationary). A **small** p-value means
stationary.

**22. State the KPSS null hypothesis.**
**The series IS stationary.** A small p-value means non-stationary — the
reverse of ADF.

**23. What does `regression="ct"` do in the ADF test?**
Allows a **constant and a trend**, so it can detect **trend-stationarity**.

**24. How do you detect over-differencing?**
**The variance goes up.** Measured: 16.896 → 47.923 on the second difference.

**25. Write the backshift form of a seasonal difference.**
(1 − Bᵐ)yₜ = yₜ − yₜ₋ₘ

**26. Expand SARIMA(p,d,q)(P,D,Q)ₘ.**
Non-seasonal AR, differencing, MA; **seasonal** AR, differencing, MA; and m,
**the number of observations in one cycle**.

**27. What is m for quarterly data with an annual cycle?**
**4.** m is the length of one cycle, not the number of cycles.

**28. How many observations does D = 1 cost?**
**m.** For monthly data with an annual cycle, twelve.

**29. Name the airline model.**
**SARIMA(0,1,1)(0,1,1)₁₂** — two parameters, and the right first model for
seasonal monthly data.

**30. Why does SARIMA(1,0,0)(1,0,0)₁₂ have a lag-13 term?**
The polynomials **multiply**: (1−φB)(1−ΦB¹²) produces +φΦB¹³.

**31. Write the VAR(p) equation.**
yₜ = c + A₁yₜ₋₁ + … + Aₚyₜ₋ₚ + εₜ, with yₜ a k-vector and each Aᵢ a k×k
matrix.

**32. How many coefficients has a VAR(2) with 4 variables?**
k²p + k = 16 × 2 + 4 = **36**, plus 10 in the covariance matrix.

**33. State the Granger causality null.**
Past values of X **do not help predict** Y, given Y's own past.

**34. What does "Granger causes" actually mean?**
**"Helps predict", nothing more.** Ice cream sales Granger-cause drownings.

**35. Why is VARMA rarely used?**
**Identification** — different parameterisations give identical dynamics. A
VAR with enough lags approximates any VARMA and is identified.

**36. What is cointegration, and what do you do about it?**
Two non-stationary series whose linear combination is stationary. Differencing
them separately **destroys the long-run relationship** — use a **VECM**.

**37. Write the two state-space equations.**
State: xₜ = Txₜ₋₁ + Rηₜ. Observation: yₜ = Zxₜ + εₜ.

**38. What is the Kalman gain?**
The weight given to a **new observation** against the model's prediction.
Small measurement noise → large gain → follow the data.

**39. Give one difference between the Kalman filter and smoother.**
The **filter** uses data up to t (causal, real-time); the **smoother** uses
all the data (retrospective, more accurate).

**40. How does a state-space model handle missing data?**
**It skips the update and keeps predicting the state forward.** No imputation
is needed — the lab's six-point gap cost RMSE 8.745 against a series SD of
31.08.

**41. What does a zero variance estimate mean in an unobserved-components
model?**
That the component is **deterministic** — it does not vary. It is a result,
not a convergence failure.

**42. What does a spectral density measure?**
How much of the series' **variance** sits at each frequency.

**43. Convert a frequency of 0.25 to a period.**
Period = 1/0.25 = **4**.

**44. Why must you detrend before a periodogram?**
A trend is a **very low frequency** and dominates the spectrum. Undetrended,
the lab's strongest "period" was 120 months — the series length.

**45. What is spectral leakage?**
A cycle whose period does not divide the record length exactly **spreads
across neighbouring frequencies** — the 12.19 and 11.64 sidelobes around 12.

**46. Give the MASE formula.**
MAE of your forecast ÷ MAE of the **in-sample one-step naive** forecast.

**47. Name two failures of MAPE.**
**Undefined/explosive near zero**, and **asymmetric** — capped at 100% for
under-forecasts, unbounded for over-forecasts.

**48. Why is k-fold CV invalid on a time series?**
It puts **future observations in the training set**, so the model interpolates
rather than forecasts.

**49. What replaces it?**
**Rolling-origin cross-validation** — train on [0,t), forecast h ahead, score,
move t forward.

**50. Why can a decision tree not extrapolate a trend?**
It predicts the **mean of a leaf**, and no average can exceed the largest
value it averaged. The lab's tree flat-lined at exactly its training maximum.

---

## Section B — Five-mark questions

### 1. Explain stationarity and why every model here needs it

**Weak stationarity:** constant mean, constant variance, and an autocovariance
γ(k) that depends only on the gap k.

**Why it is needed, in one line:** *you cannot learn a rule from the past that
applies to the future unless the rule is the same in both.* A model fitted to
a series whose mean is drifting has learned a mean that no longer exists.

**What breaks it, and the treatment of each:**

| Cause | Fix |
|---|---|
| deterministic trend | **detrend** |
| stochastic trend (unit root) | **difference** |
| seasonality | seasonal difference at lag m |
| growing variance | **log** or Box-Cox |
| structural break | split, or add a dummy |

**And the distinction that is examined:** a deterministic and a stochastic
trend look identical on a plot and need opposite treatments. **ADF with
`regression="ct"` tells them apart** — the lab's trend-stationary series went
from p = 0.9086 under `"c"` to p = 0.0000 under `"ct"`, while the random walk
did not flip (0.5576).

### 2. Explain the ACF and PACF and how they identify a model

**ρ(k)** is the total correlation between yₜ and yₜ₊ₖ, **including everything
transmitted through the points in between**. **φ_kk** is what remains after
removing lags 1 … k−1.

**In an AR(1) with φ = 0.8, ρ(2) = 0.64** — but not because y₋₂ acts
directly. It acts on y₋₁, which acts on y. **The PACF at lag 2 is therefore
0**, and that zero identifies the order.

| Pattern | Model |
|---|---|
| ACF **cuts off** at q | **MA(q)** |
| PACF **cuts off** at p | **AR(p)** |
| both tail off | **ARMA — use AIC** |

**Both rules verified on generated data:** an AR(2) built with φ = (0.6, −0.3)
had a PACF significant at lags [1, 2, 8] — cutting off after 2, with lag 8 a
chance spike. An MA(1) with θ = 0.7 gave **ρ(1) = 0.4879 against a theoretical
0.4698**.

**And the band is ±1.96/√n**, so about one lag in twenty falls outside by
chance. **Reading structure into a stray spike is the commonest mistake here.**

### 3. Explain the residual diagnostic checks

| # | Check | Test | Pass means |
|---|---|---|---|
| 1 | **white noise** | **Ljung-Box** | no structure left |
| 2 | mean zero | t-test | unbiased |
| 3 | constant variance | plot / split ratio | intervals trustworthy |
| 4 | normality | Jarque-Bera | intervals exact |

**Ljung-Box is the one that matters**, and it tests the first h lags
**jointly** — because checking each against its own band flags one in twenty
by chance.

**Measured:** the correct AR(2) fit gave **p = 0.7615**; a deliberately
under-specified AR(1) on the same data gave **p = 0.0000** and an AIC 54.8
higher. **Both signals agreed.**

> **A model chosen by AIC alone, with no residual check, can be the best of a
> bad set.** AIC is relative; Ljung-Box is absolute.

**And on seasonal data, test at least 2m lags** — Ljung-Box at 10 lags on
monthly data never looks at lag 12.

### 4. Explain over-differencing and how to detect it

**Each unnecessary difference injects noise and adds a spurious negative MA
term.**

| Series | ADF p | Variance |
|---|---:|---:|
| original | 0.9086 | 3351.744 |
| differenced once | 0.0000 | **16.896** |
| differenced **twice** | 0.0000 | **47.923** |

**The variance nearly tripled** — that is the signature.

**The rule: difference until the ADF rejects, then stop.** A smaller p-value
is not a better answer; stationarity is a threshold, not a score.

**And d is almost never more than 2.** If you find yourself at d = 3, the
problem is a variance issue needing a log, or a structural break.

**One honest caveat from the lab:** on the sales series, adding d = 1 on top
of D = 1 raised the standard deviation from 5.729 to 6.133 — yet the airline
model, which uses both, forecast best. **The variance rule is a guide; the
held-out error is the arbiter.**

### 5. Explain multiplicative seasonality and derive the lag-13 term

$$\phi_p(B)\,\Phi_P(B^m)\,(1-B)^d(1-B^m)^D y_t = \theta_q(B)\,\Theta_Q(B^m)\,\varepsilon_t$$

**The seasonal polynomials are in Bᵐ and they multiply the non-seasonal
ones.** For SARIMA(1,0,0)(1,0,0)₁₂:

$$(1-\phi B)(1-\Phi B^{12}) = 1 - \phi B - \Phi B^{12} + \phi\Phi B^{13}$$

so

$$y_t = \phi y_{t-1} + \Phi y_{t-12} - \phi\Phi y_{t-13} + \varepsilon_t.$$

**The lag-13 term is right, not an artefact.** If this month depends on last
month, and on the same month last year, then it must also depend on *last
month last year* — and the model captures that with **no extra parameter**,
since the coefficient is the product of two it already has.

**That is the argument for multiplicative seasonality:** the additive
alternative needs a third free parameter to say the same thing, and is free to
say something inconsistent.

### 6. Explain Granger causality and its limitations

**H₀: past X does not help predict Y, given Y's own past.** Fit Y on its own
lags, then on its own lags plus X's, and test whether the second fits
significantly better.

**Verified in both directions** on data with a known structure:

| X → Y | p | Result | Matches truth? |
|---|---:|---|---|
| gdp → inflation | 0.0000 | causes | **as built** |
| inflation → gdp | 0.6910 | no evidence | **as built** |

**All four directions matched** — including the two non-causal ones, which is
the harder half.

**The three limitations:**

1. **It is about prediction, not mechanism.**
2. **A common third driver produces exactly this pattern.** If Z drives both
   and reaches X first, X Granger-causes Y with no link between them.
3. **It is sensitive to omitted variables** — add the missing one and the
   relationship can vanish, which a real causal effect would not.

**And on non-stationary data it produces spurious significance.** Difference
first, or use a VECM if the series are cointegrated.

### 7. Explain the Kalman filter's predict–update cycle

```
PREDICT: x̂ₜ|ₜ₋₁ = T x̂ₜ₋₁         where do I think the state is?
         Pₜ|ₜ₋₁ = T Pₜ₋₁ Tᵀ + Q    how sure am I?

observe yₜ

UPDATE:  Kₜ = Pₜ|ₜ₋₁ Zᵀ (Z Pₜ|ₜ₋₁ Zᵀ + R)⁻¹     the KALMAN GAIN
         x̂ₜ = x̂ₜ|ₜ₋₁ + Kₜ(yₜ − Z x̂ₜ|ₜ₋₁)
         Pₜ  = (I − Kₜ Z) Pₜ|ₜ₋₁
```

**The gain is the whole idea.** It is a weighted average of prediction and
observation whose weights are chosen optimally: small measurement noise →
large gain → follow the data; large measurement noise → small gain → trust the
model.

**Two consequences worth stating:**

- **Missing data is free.** Skip the update and keep predicting. The lab
  deleted six points and estimated them at RMSE 8.745 against a series SD of
  31.08, **with no imputation step**.
- **Updating is recursive** — one step per new observation, not a refit. That
  is why Kalman filters run in navigation systems and anything tracking a live
  state.

**And you have been using one since Unit 2:** statsmodels writes every ARIMA
in state-space form and runs the filter to evaluate the likelihood.

### 8. Compare RMSE, MAE, MAPE and MASE

| Metric | Units | Failure mode |
|---|---|---|
| RMSE | data's | **punishes large errors hard** |
| MAE | data's | treats all errors alike |
| MAPE | percent | **explodes near 0; asymmetric** |
| MASE | **scale-free** | needs a stated baseline |

**RMSE and MAE can rank two forecasts differently:**

| Forecast | RMSE | MAE |
|---|---:|---:|
| A: off by 2 every month | **2.000** | 2.000 |
| B: perfect, then off by 15 once | 4.743 | **1.500** |

**Choose from the cost of being wrong — before you look at the results.**

**MAPE's failure, on a uniform absolute error of 1.0:** MAE reports 1.000, the
truth; **MAPE reports 75.37%**, because being off by 1 against an actual of
0.5 is a 200% error. **And it is asymmetric** — capped at 100% for
under-forecasts, unbounded for over-forecasts, so **it prefers models that
under-forecast**.

**MASE fixes both:** scale-free, defined at zero, symmetric, and it reads
directly — below 1 beats naive.

---

## Section C — Ten-mark questions

### 1. Explain the Box–Jenkins methodology in full

```
1. PLOT        <- never skip; four questions answer themselves
2. TRANSFORM   log if the variance grows with the level
3. DIFFERENCE  ADF and KPSS decide d and D
4. IDENTIFY    ACF and PACF give p and q
5. ESTIMATE    maximum likelihood, via the Kalman filter
6. DIAGNOSE ───fails──┘  Ljung-Box on the residuals
7. FORECAST    with intervals
8. EVALUATE    against seasonal naive
```

**Step 1** answers: is there a trend? seasonality, at what period? constant
variance? outliers? *Every failure to identify a model starts with skipping
this.*

**Step 2:** a growing swing is the diagnostic. The lab measured a
peak-to-trough swing of 59.6 rising to 98.0 (**1.64×**) on a multiplicative
series, falling to a ratio of **0.97** after a log.

**Step 3:** difference until ADF rejects, then stop — the variance rising is
the over-differencing signal (16.896 → 47.923). **Use `regression="ct"`** to
distinguish a deterministic from a stochastic trend.

**Step 4:** ACF cuts off → MA(q); PACF cuts off → AR(p). Verified against
generated truth: PACF cut off after lag 2 on an AR(2), ACF after lag 1 on an
MA(1) landing on θ/(1+θ²) = 0.4698.

**Step 5:** maximum likelihood. **Check the estimate against its standard
error** — the lab's φ₁ landed 2.5 SE from the truth on one draw, and only a
200-draw Monte Carlo could establish that the estimator was unbiased and the
draw unusual.

**Step 6 loops back.** A model that fails Ljung-Box is not tuned, it is
re-identified. The under-specified AR(1) gave p = 0.0000 and AIC 54.8 higher.

**Step 7:** intervals, always. And **report the coverage** — nominal 95%,
empirical 75% here.

**Step 8:** against **seasonal naive**, which scored RMSE 14.152 where the
model scored 6.891 — **51% better**. *An RMSE means nothing without it.*

### 2. Explain SARIMA completely, with identification and a comparison

**The specification:** SARIMA(p,d,q)(P,D,Q)ₘ, where the seasonal polynomials
are in Bᵐ and **multiply** the non-seasonal ones:

$$\phi_p(B)\,\Phi_P(B^m)\,(1-B)^d(1-B^m)^D y_t = \theta_q(B)\,\Theta_Q(B^m)\,\varepsilon_t$$

**m is the length of one cycle** — 12 for monthly data with an annual pattern,
4 for quarterly, 7 for daily-with-weekly. **Setting m to the number of cycles
is the commonest error.**

**The multiplication produces cross terms.** SARIMA(1,0,0)(1,0,0)₁₂ expands to
include **+φΦ B¹³** — last month last year — with no extra parameter.

**The two differences do different jobs:**

| | Removes | Costs |
|---|---|---|
| d = 1 | the trend | 1 observation |
| D = 1 | the seasonality | **m observations** |

**Measured:** original std 30.949 → d=1 gives 10.144 → **D=1 gives 5.729**.

**Identification, in order:** plot; log if needed; seasonal difference; then
regular difference if a trend remains; then read the ACF/PACF **at two
scales** — lags 1,2,3 for p and q, lags m, 2m, 3m for **P and Q**; fit; and
**check Ljung-Box at ≥ 2m lags**, or it cannot see seasonal structure at all.

**The comparison that justifies all this:**

| Model | AIC | LB p | **Test RMSE** |
|---|---:|---:|---:|
| ARIMA(1,1,1) | 727.50 | **0.0000** | **20.359** |
| ARIMA(2,1,2) | 615.04 | 0.0555 | 9.330 |
| SARIMA(1,1,1)(1,1,1)₁₂ | **476.32** | 0.5117 | 6.891 |
| **SARIMA(0,1,1)(0,1,1)₁₂** | 485.76 | **0.8590** | **6.530** |

**The seasonal models win by a wide margin, and the naive ARIMA fails its
residual test outright.** A non-seasonal model has no mechanism to represent
an annual cycle — it can only average it away.

**And the winner is the airline model**, two parameters, which Box and Jenkins
fitted to airline passengers and which fits a remarkable share of monthly
business series untuned. **Start there.**

**Its limitation:** SARIMA holds **one** m. Daily data with both weekly and
annual cycles needs **Fourier terms in a regression with ARIMA errors**, or
TBATS, or Prophet.

### 3. Compare classical and machine-learning forecasting, and evaluate

**Five methods, one held-out year of a 120-month series:**

| Method | RMSE | MAE | vs seasonal naive |
|---|---:|---:|---:|
| naive | 26.731 | 21.620 | −89% |
| seasonal naive | 14.152 | 12.422 | 0% |
| SARIMA(1,1,1)(1,1,1)₁₂ | 6.891 | 5.101 | **51%** |
| **Holt-Winters additive** | **5.259** | **3.874** | **63%** |
| linear regression on lags | 10.858 | 9.324 | 23% |
| gradient boosting on lags | 11.318 | 9.620 | 20% |

**The classical models won, and the reason is structural rather than
accidental.** ARIMA and exponential smoothing **encode** trend, seasonality
and autocorrelation as assumptions, so they need little data to fit. A booster
must **learn** that structure from examples, and 96 training rows is not many.

**The M4 and M5 competitions put the crossover at hundreds of series or
thousands of observations.** Below that, statistical models are hard to beat —
and *"we used machine learning"* is not an argument.

**Three specific weaknesses of the ML approach here:**

1. **You must build the lags yourself.** Nothing in scikit-learn knows what
   time is.
2. **Recursive multi-step forecasting feeds predictions back as inputs.** The
   alternative is *direct* forecasting — one model per horizon, twelve times
   the fitting.
3. **A tree cannot extrapolate a trend.** Measured on a strictly increasing
   series: the tree flat-lined at **255.8, exactly its training maximum**,
   for every horizon from 1 to 12, while a linear model tracked the truth to
   within 0.7. A tree predicts the mean of a leaf, and no average exceeds its
   largest input. **This is the one criticism that is not a matter of taste.**

**Evaluating the winner:**

- **Against a baseline.** 63% better than seasonal naive is the number to
  quote.
- **With the right metric.** RMSE and MAE can rank two forecasts differently;
  **choose from the cost of being wrong, before you look.** MASE if the series
  differ in scale.
- **On rolling-origin CV**, not one window — the lab used 6 folds.
- **Checking the bias**, not just the magnitude: mean error +2.2898,
  t = 1.604, p = 0.1370 — no evidence of bias.
- **Reporting the interval coverage honestly** — nominal 95%, empirical 75%.

### 4. A retailer gives you 5 years of monthly sales and wants a 12-month forecast

**Step 1 — Plot it and answer four questions.** Trend? Seasonality, at what
period? Constant variance? Outliers or level shifts? **60 observations is 5
years, which is thin for anything seasonal** — you have five annual cycles,
and the rule of thumb wants at least 2–3 to estimate a seasonal component at
all.

**Step 2 — Confirm m with a periodogram** rather than assuming 12. The lab's
detrended sales series showed a dominant period of **12.00 months with power
299.04**, next-strongest 15.00 at power 2.11. **Detrend first**, or the trend
dominates the spectrum.

**Step 3 — Transform if the swing grows.** Retail sales usually do, so expect
to work in logs and remember to back-transform the forecast *and* the
interval.

**Step 4 — Difference.** Seasonal difference first (D = 1, costing 12
observations, leaving 47). Regular difference only if a trend remains. Check
the variance does not rise.

**Step 5 — Start with the airline model, SARIMA(0,1,1)(0,1,1)₁₂.** Two
parameters against 47 usable observations is defensible;
SARIMA(2,1,2)(1,1,1)₁₂ at seven parameters is not. **Let rolling-origin CV
decide whether anything larger earns its place** — in the lab it did not.

**Step 6 — Diagnose.** Ljung-Box at **at least 24 lags**, or it cannot see the
seasonal structure.

**Step 7 — Forecast with intervals, and back-transform.**

**Step 8 — Compare against seasonal naive**, and report the improvement rather
than the raw RMSE.

**What to warn the retailer about, and this earns the marks:**

- **The interval is probably too narrow.** SARIMA prices in shock uncertainty
  and ignores estimation uncertainty; the lab measured 75% coverage from a
  nominal 95%.
- **A promotion, a competitor or a new store is a structural break**, and no
  model fitted before it will survive it. Ask what is planned.
- **Twelve months is a long horizon on five years of data.** The interval at
  h = 12 is the honest answer to "how confident are you?"
- **Monitor the rolling error and the mean error**, and re-fit when either
  moves.

### 5. Explain everything that changes when observations are not independent

**Five things you learned earlier stop working, and each has a replacement.**

**1. The train/test split.** A random 80/20 split lets the model see the
future. **Replace with a held-out tail** — the last h observations — and
**rolling-origin CV** for model selection: train on [0,t), forecast h, score,
move t forward. Every fold trains only on the past.

**2. Cross-validation.** k-fold is invalid for the same reason, doubly so: it
trains on data that comes *after* the validation fold, so the model
interpolates a gap it has seen both sides of. It scores far too well.

**3. Standard errors and the effective sample size.** The usual σ/√n assumes
independent draws. **Correlated observations carry less information than n
suggests** — with positive autocorrelation the effective sample size can be a
small fraction of n, and every confidence interval computed the naive way is
too narrow.

**4. Resampling.** The bootstrap destroys the ordering, which *is* the signal.
Time-series bootstraps exist — **block bootstrap**, which resamples contiguous
blocks to preserve local dependence — and they are not the same procedure.

**5. "More data is more information."** Measured: an AR(2) at n = 400 gave
φ₁ = 0.7062 against a true 0.600; at n = 16,000 it gave 0.6117. **400 monthly
observations is 33 years and still leaves two-decimal uncertainty**, and you
cannot collect more of the past.

**And one thing that becomes possible rather than impossible:** because the
observations are dependent, **the past predicts the future at all.** The
dependence that breaks your tools is the same dependence that makes
forecasting work — which is the sentence to end on.

---

## The six things most likely to be examined

1. **The ADF's reversed null**, and the `"ct"` flip that separates a
   deterministic from a stochastic trend — p 0.9086 → 0.0000.
2. **The two identification rules**, with ρ(1) = θ/(1+θ²) = 0.4698 as the
   check.
3. **The over-differencing signal:** variance 16.896 → 47.923.
4. **The lag-13 term**, derived from the multiplicative expansion.
5. **"Granger causes means helps predict"** — and the VAR that lost on GDP
   because nothing fed into it.
6. **"A tree cannot extrapolate a trend"** — flat-lining at 255.8, its exact
   training maximum, at every horizon.
