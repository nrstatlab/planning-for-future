# Course 14 B — Practical Lab

**13 experiments**
*"Using R/Python statsmodels, pandas, forecast, or equivalent."*

Code lives in `labs/course-14b-timeseries/`.

## 🎯 Every experiment in this course runs

**There is no `NOT EXECUTED` file anywhere in Course 14 B.** Five courses in
the programme can say that of every experiment — **2** (C), **7** (Web
Technologies), **9** (Pandas), **12 A** (Machine Learning) and this one.
Everywhere else at least one thing is documented rather than run, because the
tool it needs cannot be installed here.

statsmodels implements everything the syllabus names, so decomposition, STL,
ACF/PACF, ADF, KPSS, ARMA, ARIMA, SARIMA, Ljung-Box, VAR, Granger causality,
the Kalman filter, periodograms and Holt-Winters are all **real calls against
real implementations**.

```bash
pip install -r tools/requirements.txt
python3 tools/run_timeseries_labs.py
```

### 💡 The discipline that makes it worth running

**The series are generated from KNOWN coefficients**, so every fit is checked
against the truth that produced it:

| Series | Built with | Checked against |
|---|---|---|
| AR(2) | φ = (0.6, −0.3) | the fitted coefficients and their intervals |
| MA(1) | θ = 0.7 | ρ(1) must equal θ/(1+θ²) = **0.4698** |
| monthly sales | slope 0.8, seasonal amplitude 25 | what decomposition recovers |
| macro system | GDP drives the other two, nothing drives GDP | **both** Granger directions |

**A model that merely converges has proved nothing.** This is the only way to
show that identification and estimation *work* — and it is how the labs caught
a coefficient estimate 2.5 standard errors from the truth, and could then
prove the estimator was fine and the draw unusual.

---

## Experiments 1 and 2 — Import, visualize, decompose

`01_explore_decompose.py`

**120 monthly observations**, 2016-01 to 2025-12, mean 145.24.

### The four questions to ask before any model

1. Is there a **trend**?
2. Is there **seasonality**, and at what period?
3. Is the **variance constant**, or growing with the level?
4. Are there **outliers** or **level shifts**?

**Answer these by looking at the plot.** Every failure to identify a model
correctly starts with skipping this step.

### 🔢 Decomposition recovers what the series was built from

| Component | Recovered | True |
|---|---:|---:|
| trend slope | **0.7294** | 0.8000 |
| seasonal amplitude | **24.9188** | 25.0000 |
| residual std | 3.7861 | — |

**That is the check worth doing.** On real data you cannot verify a
decomposition, so verify the *method* on data whose answer you know.

### 🔢 And the seasonal component sums to zero

```
   1     2     3     4     5     6     7     8     9    10    11    12
-0.3  10.4  19.7  25.0  22.7  13.2   1.0 -10.3 -21.0 -24.9 -22.2 -13.3
```

**Sum: 3.6 × 10⁻¹⁵.** An additive seasonal is *defined* to average out over a
cycle, which is why it can be subtracted without shifting the level.

### 🔢 Additive or multiplicative — decide from the swing

On a deliberately multiplicative series:

| | Peak-to-trough swing |
|---|---:|
| first two years | 59.6 |
| last two years | **98.0 (1.64×)** |
| **after log**, first two years | 0.5546 |
| **after log**, last two years | **0.5366 (0.97×)** |

**A growing swing is the whole diagnostic.** Fit an additive model to it and
the residuals are small early and large late — heteroscedasticity, which
invalidates every confidence interval the model produces.

### 💡 Classical decomposition against STL

**Classical lost 12 of 120 points** (six at each end — a centred 12-month
moving average cannot be computed there). **STL lost none**, lets the seasonal
shape evolve, and has a robust option for outliers.

**STL is the modern default.** Name it.

---

## Experiments 3 and 4 — ACF, PACF and stationarity

`03_acf_stationarity.py`

### 🔢 Both identification rules, checked against known truth

**AR(2), built with φ = (0.6, −0.3), n = 400, band = ±0.098:**

```
PACF significant at lags: [1, 2, 8]
```

**The PACF cut off after lag 2, and the true order is 2.** Lag 8 pokes out by
chance — with a 95% band, about 1 lag in 20 does.

**MA(1), built with θ = 0.7:**

```
ACF significant at lags: [1, 3]
ACF at lag 1 = 0.4879,  theory: theta/(1+theta^2) = 0.4698
```

**The ACF cut off after lag 1 and landed on the theoretical value.** An MA(q)
has **exactly zero** autocorrelation beyond lag q — not small, zero.

**ARMA(1,1):** both tail off, neither cuts. **That is the ARMA signature**,
and it is why ARMA orders go to AIC.

**White noise, 20 lags: 0 outside the band.** You expect about one. Reading
structure into a stray spike is the commonest correlogram mistake — and the
reason Ljung-Box tests lags **jointly**.

### 🔢 The ADF test

| Series | ADF stat | p | Verdict |
|---|---:|---:|---|
| white noise | −18.483 | 0.0000 | stationary |
| **random walk** | −2.164 | **0.2197** | **unit root** |
| **random walk, differenced** | −18.468 | **0.0000** | **stationary** |
| monthly sales | −0.640 | 0.8616 | unit root |
| sales, differenced | −8.633 | 0.0000 | stationary |
| sales, seasonally differenced | −3.514 | 0.0076 | stationary |

> **That is where the d in ARIMA(p,d,q) comes from.**

### ⚠️ Over-differencing, measured

| | ADF p | Variance |
|---|---:|---:|
| original (trend + noise) | 0.9086 | 3351.744 |
| differenced once | 0.0000 | **16.896** |
| differenced **twice** | 0.0000 | **47.923** |

**The variance nearly tripled.** Difference until the ADF rejects, then stop.

### 🔢 ADF and KPSS together — and the `regression` term

| Series | ADF `c` | ADF `ct` | KPSS `c` | Conclusion |
|---|---:|---:|---:|---|
| white noise | 0.0000 | 0.0000 | 0.1000 | stationary |
| random walk | 0.2197 | **0.5576** | 0.0100 | non-stationary |
| **trend + noise** | **0.9086** | **0.0000** | 0.0100 | **TREND-stationary** |

**The third row flips.** "Trend + noise" is non-stationary to the plain ADF
and stationary once the test is allowed a trend — so **detrend, do not
difference**.

**The random walk does not flip**, because no amount of detrending removes a
genuine unit root.

---

## Experiments 5 and 6 — ARMA, ARIMA and SARIMA

`05_arma_arima_sarima.py`

### ⚠️ The estimate that missed, and what it taught

| Param | True | Estimate | Std err | 95% CI | Covers? |
|---|---:|---:|---:|---|---|
| φ₁ | 0.600 | **0.7062** | 0.0428 | [0.6223, 0.7901] | **NO** |
| φ₂ | −0.300 | −0.3661 | 0.0475 | [−0.4591, −0.2731] | yes |

**2.5 standard errors out.** Is the *method* wrong, or is this *draw* unusual?
**One realisation cannot tell you.**

**200 independent series later:**

| Param | True | Mean estimate | SD | Bias |
|---|---:|---:|---:|---:|
| φ₁ | 0.600 | **0.5980** | 0.0457 | **−0.0020** |

**The estimator is unbiased, and only 1 of 200 draws was further out.** The
method is right; seed 42 gave an unusual series.

**And with more data** — 0.6935 at n = 200, **0.6117 at n = 16,000** — the
estimator is consistent.

> **400 monthly observations is 33 years of data and still leaves two-decimal
> uncertainty.** Time series are data-poor by nature; you cannot collect more
> of the past.

### 🔢 Residual diagnostics

| Check | Value | Verdict |
|---|---:|---|
| residual mean ≈ 0 | −0.00067 | ok |
| **Ljung-Box p (10 lags)** | **0.7615** | **no structure left** |
| Jarque-Bera p | 0.6417 | ok |
| variance ratio, halves | 1.0149 | ok |

**And the deliberately wrong model:**

| Model | AIC | Ljung-Box p |
|---|---:|---:|
| AR(1) — **wrong** | 1193.12 | **0.0000** |
| AR(2) — correct | **1138.31** | 0.7615 |

**Both signals agree.** A model chosen by AIC alone, with no residual check,
can be the best of a bad set.

### 🔢 SARIMA against ARIMA

| Model | AIC | BIC | LB p | **Test RMSE** |
|---|---:|---:|---:|---:|
| ARIMA(1,1,1) | 727.50 | 735.46 | **0.0000** | **20.359** |
| ARIMA(2,1,2) | 615.04 | 628.27 | 0.0555 | 9.330 |
| SARIMA(1,1,1)(1,1,1)₁₂ | **476.32** | 488.29 | 0.5117 | 6.891 |
| **SARIMA(0,1,1)(0,1,1)₁₂** | 485.76 | **492.95** | **0.8590** | **6.530** |

**The seasonal models win by a wide margin.** A non-seasonal ARIMA has no
mechanism to represent an annual cycle — it can only average it away.

### ⚠️ And an honest tension

| Series | std | ADF p |
|---|---:|---:|
| **D = 1 (lag 12)** | **5.729** | 0.0076 |
| d = 1 **and** D = 1 | **6.133** | 0.0000 |

**Adding d = 1 on top of D = 1 raised the standard deviation** — the
over-differencing signal. **Yet the airline model, which uses both, forecast
best.**

**Report both.** The variance rule is a guide; the held-out error is the
arbiter.

### The airline model

**SARIMA(0,1,1)(0,1,1)₁₂**, two parameters:

| Parameter | Estimate | Std err |
|---|---:|---:|
| `ma.L1` | −0.3223 | 0.1016 |
| `ma.S.L12` | −0.6044 | 0.1168 |

**It is the right first model for seasonal monthly data.** Start there.

---

## Experiments 7 and 8 — Selection and forecasting

`07_selection_forecast.py`

### 🔢 AIC, BIC and rolling-origin CV

| Model | k | AIC | BIC | CV RMSE |
|---|---:|---:|---:|---:|
| SARIMA(0,1,1)(0,1,1)₁₂ | 3 | 485.76 | 492.95 | 4.019 |
| **SARIMA(1,1,1)(0,1,1)₁₂** | 4 | **472.49** | **482.07** | 3.966 |
| **SARIMA(1,1,1)(1,1,1)₁₂** | 5 | 476.32 | 488.29 | **3.799** |
| SARIMA(2,1,1)(1,1,1)₁₂ | 6 | 478.28 | 492.65 | 3.836 |
| SARIMA(2,1,2)(1,1,1)₁₂ | 7 | 474.66 | 491.33 | 3.927 |

**AIC and BIC agreed** here, on the 4-parameter model — that happens when one
specification is clearly better than its neighbours.

**But rolling-origin CV chose a different model.** **AIC estimates
out-of-sample error from a formula and an assumption; CV measures it.** When
you can afford the refits, measure.

**The CV used 6 rolling folds**, each training only on the past. **k-fold is
invalid** — it puts future observations in the training set.

### 🔢 Forecasts and intervals

| h | Actual | Forecast | 95% interval | Width | In? |
|---:|---:|---:|---|---:|---|
| 1 | 181.73 | 178.89 | [170.71, 187.07] | 16.36 | yes |
| 2 | 201.56 | 189.45 | [180.39, 198.51] | 18.11 | **NO** |
| 7 | 182.57 | 192.70 | [183.37, 202.04] | 18.66 | **NO** |
| 12 | 190.48 | 175.11 | [165.77, 184.44] | 18.67 | **NO** |

**RMSE 6.891, MAE 5.101, coverage 9/12 = 75%.**

### ⚠️ Report the coverage, do not round it up

**Nominal 95%, empirical 75%.** Two things are going on:

1. **Twelve points is a tiny sample** — 9 or fewer hits out of 12 under a true
   95% interval has probability **0.020**. Unusual, not damning.
2. **SARIMA intervals are known to be too narrow.** They treat the fitted
   parameters as if they were the true ones, pricing in *shock* uncertainty
   and ignoring **estimation** uncertainty.

**If the interval matters for a decision, widen it or get it by bootstrap.**

### 🔢 Two shapes of widening

| h | Random walk width | ÷ √h × width(1) | AR(1) width |
|---:|---:|---:|---:|
| 1 | 3.455 | **1.0000** | 3.921 |
| 4 | 6.909 | **1.0000** | 4.541 |
| 16 | 13.819 | **1.0000** | **4.551** |

**The random walk's interval is exactly √h times its one-step width.** The
AR(1)'s **flattens** — a stationary process forgets where it started.

**That contrast is the difference between a series you can forecast far ahead
and one you cannot.**

### 🎯 The baselines

| Method | RMSE | MAE |
|---|---:|---:|
| naive (last value) | 26.731 | 21.620 |
| **seasonal naive** | **14.152** | 12.422 |
| SARIMA(1,1,1)(1,1,1)₁₂ | **6.891** | 5.101 |

**The model beats seasonal naive by 51%.** Quote that comparison, not the RMSE
alone — **an RMSE of 6.89 means nothing until you know repeating last year
scores 14.15.**

---

## Experiments 9, 10 and 11 — VAR, state-space, spectral

`09_var_statespace_spectral.py`

### 🔢 The VAR recovered a known structure

| Equation ↓ | gdp | inflation | unemployment |
|---|---:|---:|---:|
| gdp | 0.6336 | **0.0214** | **0.0707** |
| inflation | **0.4275** | 0.3154 | 0.0457 |
| unemployment | **−0.4312** | 0.1197 | 0.5224 |

**Including the two zeros it was never told about.** True values: 0.500,
−0.400 and 0.000.

### 🔢 Granger causality, in both directions

| X → Y | p-value | Result | Matches truth? |
|---|---:|---|---|
| gdp → inflation | **0.0000** | causes | **as built** |
| gdp → unemployment | **0.0000** | causes | **as built** |
| inflation → gdp | 0.6910 | no evidence | **as built** |
| unemployment → gdp | 0.1367 | no evidence | **as built** |

**All four match — including both non-causal directions.** *A test that only
ever finds effects is not a test.*

> **"Granger causes" means "helps predict", nothing more.** Ice cream sales
> Granger-cause drownings.

### ⚠️ And the VAR lost on one series

| Series | VAR RMSE | Univariate AR(1) | Winner |
|---|---:|---:|---|
| **gdp** | 1.0782 | **1.0574** | **univariate** |
| inflation | **1.1248** | 1.1949 | VAR |
| unemployment | **1.3192** | 1.3663 | VAR |

**Exactly right, not a disappointment.** GDP has nothing feeding into it, so
the VAR's extra coefficients estimate zeros — pure variance, no signal.

**A VAR helps only where cross-series information exists.**

### 🔢 The Kalman filter recovered the components

| Component | Variance |
|---|---:|
| `sigma2.irregular` | 6.5360 |
| `sigma2.level` | 8.4278 |
| **`sigma2.trend`** | **0.0000** |
| **`sigma2.seasonal`** | **0.0000** |

**The two zeros are a result.** The filter is saying those components do not
vary — and the series was built with a fixed slope and a fixed sine.

**Implied trend slope: 0.8378 against a true 0.8** — the same answer
experiment 2 gave, reached a completely different way.

### 🔢 Missing data, handled natively

Six observations deleted; **RMSE over the gap 8.745** against a series
standard deviation of **31.08**.

**No imputation step was run.** The filter skips the update at a missing time
and keeps predicting the state forward.

> **Every other method here would need the hole filled first — and filling it
> with the mean injects a fake observation the model then trusts.**

### 🔢 Spectral analysis found the cycles

A series built from period-12 and period-4 cycles:

| Rank | Period | Power |
|---:|---:|---:|
| 1 | **11.91** | 3.024 |
| 2 | **4.00** | 1.047 |
| 3 | 12.19 | 0.620 |
| 4 | 11.64 | 0.180 |

**Both recovered.** Ranks 3 and 4 straddling 12 are **spectral leakage**, not
a third cycle.

**On the sales series: dominant period 12.00 months, power 299.04** — the
annual cycle, recovered rather than assumed.

> **That is how you stop guessing m in SARIMA(p,d,q)(P,D,Q)ₘ.**

**And undetrended, the strongest period was 120 months — the whole series
length, which is the trend.** Detrend first.

---

## Experiments 12 and 13 — Comparison and evaluation

`12_compare_evaluate.py`

### 🔢 Five methods, one held-out year

| Method | RMSE | MAE | MAPE % | vs snaive |
|---|---:|---:|---:|---:|
| naive | 26.731 | 21.620 | 10.84 | −89% |
| seasonal naive | 14.152 | 12.422 | 6.47 | 0% |
| SARIMA(1,1,1)(1,1,1)₁₂ | 6.891 | 5.101 | 2.71 | **51%** |
| **Holt-Winters additive** | **5.259** | **3.874** | **2.04** | **63%** |
| linear regression on lags | 10.858 | 9.324 | 4.87 | 23% |
| gradient boosting on lags | 11.318 | 9.620 | 4.91 | 20% |

**The classical model won, on 108 observations.** ARIMA and exponential
smoothing encode the structure as *assumptions*; a booster must **learn** it,
and 96 training rows is not many.

**The M4 and M5 competitions put the crossover at hundreds of series or
thousands of observations.**

### ⚠️ The textbook claim that did not hold here

**Mean absolute error over the first three months: 15.142. Over the last
three: 6.384 — it FELL.**

The expectation is that recursive forecasting compounds error. **It did not on
this window**, and the honest reading is that the model is biased low
throughout while the series dips in months 9–11.

> **A per-horizon error curve on ONE test window of 12 points is far too noisy
> to show a trend either way.**

### 🔢 The structural limit of a tree

A strictly increasing series, +2 per step:

| h | True | Tree | Linear |
|---:|---:|---:|---:|
| 1 | 257.8 | **255.8** | 257.8 |
| 8 | 271.8 | **255.8** | 272.2 |
| 12 | 279.8 | **255.8** | 280.5 |

**The tree flat-lines at exactly the largest value it saw in training.**

A tree predicts the **mean of a leaf**, and no average can exceed the largest
of its inputs. **A tree ensemble cannot extrapolate a trend — not badly, at
all.**

### 🔢 RMSE and MAE disagree

| Forecast | RMSE | MAE |
|---|---:|---:|
| A: off by 2 every month | **2.000** | 2.000 |
| B: perfect, then off by 15 once | 4.743 | **1.500** |

**Choose from the cost of being wrong, before you look at the results.**

### ⚠️ MAPE, on a uniform error of 1.0

| Actual | Forecast | Abs err | Pct err |
|---:|---:|---:|---:|
| 0.5 | 1.5 | 1.0 | **200.0%** |
| 200.0 | 201.0 | 1.0 | **0.5%** |

**MAE 1.000 — the truth. MAPE 75.37% — not.**

**And it is asymmetric:** 200 too high gives MAPE 200%; you can never be more
than 100% too low. **So MAPE prefers models that under-forecast.**

### 🎯 MASE

| Method | MAE | MASE |
|---|---:|---:|
| naive | 21.620 | 2.559 |
| seasonal naive | 12.422 | **1.470** |
| SARIMA | 5.101 | 0.604 |
| **Holt-Winters** | **3.874** | **0.458** |

**Seasonal naive above 1 is not a contradiction** — MASE's denominator is the
**one-step in-sample naive** error. Say which denominator you used.

### And the bias check

**Mean forecast error +2.2898 (t = 1.604, p = 0.1370) — no evidence of bias.**

**A forecast can have a small RMSE and still be biased, and a business feels
bias first.**

---

## What the runner asserts

| Script | Experiments | Checked against |
|---|---|---|
| `01_explore_decompose.py` | 1, 2 | the true slope 0.8 and amplitude 25 |
| `03_acf_stationarity.py` | 3, 4 | the true AR/MA orders, and θ/(1+θ²) |
| `05_arma_arima_sarima.py` | 5, 6 | true coefficients, plus a 200-draw Monte Carlo |
| `07_selection_forecast.py` | 7, 8 | interval coverage and the √h widening law |
| `09_var_statespace_spectral.py` | 9, 10, 11 | Granger causality in **both** directions; the true cycles |
| `12_compare_evaluate.py` | 12, 13 | that a tree cannot exceed its training max |

**6 programs, 13 experiments, 0 marked NOT EXECUTED.**

---

## Lab examination

Two hours in Python or R, one experiment number, then a viva.

**What costs marks:**

- A random train/test split
- k-fold cross-validation
- Getting the ADF null backwards
- Differencing until the p-value is smallest
- Differencing a trend-stationary series
- Reading order off an ACF that has not decayed
- Ljung-Box at 10 lags on monthly data
- Setting m to the number of cycles
- Saying "Granger causes" as "causes"
- A periodogram without detrending
- MAPE on data near zero
- Quoting an RMSE with no baseline

**What earns them:**

- **"The ADF's null is a unit root, so small p means stationary."**
- **The two identification rules**, applied to a plot rather than recited.
- **"ρ(1) for an MA(1) cannot exceed 0.5"** — a sanity check nobody expects.
- **The over-differencing signal: variance 16.896 → 47.923.**
- **The ADF `ct` flip** — p 0.9086 → 0.0000, which distinguishes a
  deterministic from a stochastic trend.
- **The lag-13 term**, derived from the multiplicative expansion.
- **"51% better than seasonal naive"** rather than "RMSE 6.891".
- **"Coverage was 75%, not 95%"** — and both reasons why.
- **"The VAR lost on GDP, and that is correct."**
- **"A tree cannot extrapolate a trend"** — with the flat-line table.
- **The Monte Carlo distinction:** a wrong estimator against an unlucky draw,
  and the only way to tell them apart.
