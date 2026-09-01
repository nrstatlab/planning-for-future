# Unit 5 — Advanced Topics and Forecast Evaluation

**Syllabus topics:** Spectral analysis: frequency-domain representation,
spectral density. Forecast performance: measures, monitoring, choosing models.

---

## 5.1 The frequency domain

### 🎯 The change of question

> **The time domain asks "what happened when?"**
> **The frequency domain asks "which cycles is this made of?"**

Same information, different question — and for a series with several
overlapping cycles the second is far easier to answer by eye.

### 📖 The spectral density

Any stationary series can be written as a sum of sines and cosines at
different frequencies. The **spectral density f(ω)** says how much of the
series' **variance** sits at each frequency.

Formally it is the Fourier transform of the autocovariance function:

$$f(\omega) = \frac{1}{2\pi}\sum_{k=-\infty}^{\infty}\gamma(k)e^{-i\omega k}$$

**The ACF and the spectral density carry exactly the same information.** They
are a Fourier pair — neither contains anything the other lacks. What differs
is which patterns are *visible*.

### 💡 Frequency and period

$$\text{period} = \frac{1}{\text{frequency}}$$

A frequency of 1/12 on monthly data is a **12-month period** — the annual
cycle. **Always convert to a period before saying anything out loud;** nobody
thinks in cycles per month.

### 🔢 The periodogram, recovering known cycles

A series built from a **period-12** cycle and a **period-4** cycle, plus
noise:

| Rank | Frequency | Period | Power |
|---:|---:|---:|---:|
| 1 | 0.08398 | **11.91** | 3.024 |
| 2 | 0.25000 | **4.00** | 1.047 |
| 3 | 0.08203 | 12.19 | 0.620 |
| 4 | 0.08594 | 11.64 | 0.180 |

**Both true cycles recovered, without being told they were there.**

**And note ranks 3 and 4** — 12.19 and 11.64, straddling 12. That is
**spectral leakage**: a cycle whose period does not divide the record length
exactly spreads across neighbouring frequencies. It is an artefact of the
finite sample, not a third cycle.

### 🎯 The practical use, and it is a good one

On the monthly sales series, detrended:

| Rank | Period (months) | Power |
|---:|---:|---:|
| **1** | **12.00** | **299.04** |
| 2 | 15.00 | 2.11 |
| 3 | 13.33 | 2.06 |

**The dominant period is 12 months — recovered from the data rather than
assumed.**

> **That is what a periodogram is for: it tells you what m should be in
> SARIMA(p,d,q)(P,D,Q)ₘ when you do not already know.**

Guessing m is the commonest seasonal-model error, and this is how you stop
guessing.

### ⚠️ Two warnings that belong with any periodogram

**1. Detrend first.** A trend is a very low frequency, and it dominates the
spectrum and hides everything else. **Undetrended, the lab's strongest period
was 120 months — the whole series length, which is the trend.**

**2. It assumes the cycle is stationary and fixed in period.** A cycle that
drifts smears across several frequencies and may not show a clean peak at all
— which is exactly why a *business cycle* (Unit 1) is hard to find this way.

---

## 5.2 Forecast accuracy measures

| Metric | Formula | Units | Watch for |
|---|---|---|---|
| **RMSE** | √(mean e²) | data's | **punishes large errors hard** |
| **MAE** | mean \|e\| | data's | treats all errors alike |
| **MAPE** | mean \|e/y\| × 100 | **percent** | **explodes near y = 0**, asymmetric |
| **sMAPE** | symmetric MAPE | percent | still asymmetric |
| **MASE** | MAE ÷ MAE of naive | **scale-free** | needs a stated baseline |

### 🔢 RMSE and MAE can rank two forecasts differently

| Forecast | RMSE | MAE |
|---|---:|---:|
| A: off by 2 every month | **2.000** | 2.000 |
| B: perfect, then off by 15 once | 4.743 | **1.500** |

**RMSE prefers A. MAE prefers B.**

**Neither is wrong — they answer different questions.** RMSE squares the
errors, so one large miss dominates; MAE does not.

> **Choose from the cost of being wrong.** If a single large stock-out is
> catastrophic, use RMSE. If the cost is proportional to the error, use MAE.
> **Deciding after seeing the results is how a comparison becomes a
> justification.**

### ⚠️ MAPE's two failures, both measured

Every forecast below is off by **exactly 1.0**:

| Actual | Forecast | Abs error | Pct error |
|---:|---:|---:|---:|
| 0.5 | 1.5 | 1.0 | **200.0%** |
| 1.0 | 2.0 | 1.0 | 100.0% |
| 100.0 | 101.0 | 1.0 | 1.0% |
| 200.0 | 201.0 | 1.0 | **0.5%** |

**MAE = 1.000** — which is the truth. **MAPE = 75.37%** — which is not.

**1. Near zero it explodes.** The same absolute miss is a 200% error against
an actual of 0.5 and a 0.5% error against an actual of 200, so the two small
months carry the whole average.

**2. It is asymmetric.** Over-forecasting by 200 gives MAPE 200%;
**under-forecasting can never exceed 100%**, because you cannot be more than
100% below a positive actual.

> **So MAPE systematically prefers models that under-forecast** — which on an
> inventory problem is exactly the wrong bias.

**Never use MAPE on data that goes near zero, or on data that can be
negative**, where it is meaningless.

### 🎯 MASE, the metric that fixes both

$$\text{MASE} = \frac{\text{MAE of your forecast}}{\text{MAE of the naive forecast, in-sample}}$$

**Scale-free, defined at zero, symmetric, and it reads directly:** below 1
beats naive, above 1 does not.

| Method | MAE | MASE | Reading |
|---|---:|---:|---|
| naive | 21.620 | 2.559 | worse than naive |
| seasonal naive | 12.422 | **1.470** | **worse than naive** |
| SARIMA(1,1,1)(1,1,1)₁₂ | 5.101 | **0.604** | beats naive |
| **Holt-Winters additive** | **3.874** | **0.458** | beats naive |

### ⚠️ And why seasonal naive scores above 1

**That is not a contradiction.** MASE's denominator is the **one-step
in-sample naive** error, not the seasonal one — so on a strongly seasonal
series the seasonal-naive forecast is expected to sit above 1.

**If you want a seasonal benchmark, divide by the seasonal naive instead — and
say which denominator you used.** A MASE quoted without it is not comparable
to anyone else's.

**MASE is the metric the M4 competition used**, and it is the right default
when comparing across series of different magnitudes, which MAE and RMSE
simply cannot do.

---

## 5.3 Comparing methods

### 🔢 Five methods, one held-out year

| Method | RMSE | MAE | MAPE % | vs seasonal naive |
|---|---:|---:|---:|---:|
| naive | 26.731 | 21.620 | 10.84 | **−89%** |
| seasonal naive | 14.152 | 12.422 | 6.47 | 0% |
| SARIMA(1,1,1)(1,1,1)₁₂ | 6.891 | 5.101 | 2.71 | **51%** |
| **Holt-Winters additive** | **5.259** | **3.874** | **2.04** | **63%** |
| linear regression on lags | 10.858 | 9.324 | 4.87 | 23% |
| gradient boosting on lags | 11.318 | 9.620 | 4.91 | 20% |

### 🎯 The classical model won, and the reason matters

**Best classical: Holt-Winters, RMSE 5.259. Best ML: linear regression on
lags, RMSE 10.858.**

**ARIMA and exponential smoothing encode the structure — trend, seasonality,
autocorrelation — as *assumptions*, so they need little data to fit.** A
gradient booster must **learn** that structure from examples, and 96 training
rows is not many.

> **The M4 and M5 competitions found the crossover sits at hundreds of series
> or thousands of observations.** Below that, statistical models are hard to
> beat, and *"we used machine learning"* is not an argument.

### 📖 Exponential smoothing, since it won

| Method | Models | Parameters |
|---|---|---|
| **Simple (SES)** | level | α |
| **Holt's linear** | level + trend | α, β |
| **Holt-Winters** | level + trend + **season** | α, β, γ |

Each is a weighted average with **geometrically decaying weights on the
past** — recent observations matter more, and α controls how fast the memory
fades.

**And it is a state-space model in disguise** (Unit 4): simple exponential
smoothing *is* the steady-state Kalman filter for a local-level model, with
α equal to the Kalman gain.

### ⚠️ The structural limit of a tree-based model

A strictly **increasing** series, 80 points, +2 per step:

| h | True continuation | Tree | Linear |
|---:|---:|---:|---:|
| 1 | 257.8 | **255.8** | 257.8 |
| 4 | 263.8 | **255.8** | 263.9 |
| 8 | 271.8 | **255.8** | 272.2 |
| 12 | 279.8 | **255.8** | 280.5 |

**The tree flat-lines at 255.8 — exactly the largest value it saw in
training — while the linear model tracks the truth.**

**The reason is structural.** A decision tree predicts the **mean of a leaf**,
and every leaf is an average of training targets. **No average of numbers can
exceed the largest of them**, so a tree ensemble **cannot extrapolate a
trend** — not badly, at all.

> **Say this whenever someone proposes XGBoost for a trending series. It is
> the one criticism that is not a matter of taste.**

**The fix:** model the **differences**, or detrend first and let the tree learn
only the remainder — which is, in effect, rebuilding ARIMA by hand.

### 💡 Recursive against direct forecasting

An ML model trained to predict one step ahead must **eat its own predictions**
to reach twelve. The textbook expectation is that error compounds.

**Measured here, it did not** — the mean absolute error was **15.1 over the
first three months and 6.4 over the last three**.

**Report that honestly, and read it correctly:** the model is biased low
throughout, and the series happens to dip in months 9–11, so the gap narrows
for reasons that have nothing to do with the model improving.

> **A per-horizon error curve on ONE test window of 12 points is far too noisy
> to show a trend either way.** To measure compounding you need many rolling
> origins.

**The alternative is DIRECT forecasting:** train a separate model for each
horizon. Twelve models, no dependence on your own predictions, twelve times
the fitting. **SARIMA needs neither** — it has a closed-form h-step forecast.

---

## 5.4 Monitoring a forecast in production

### 🎯 Rolling-origin cross-validation

**The only valid CV for a time series.** Train on [0, t), forecast the next h,
score, move t forward. **The lab used 6 folds**, each training only on the
past.

**k-fold cross-validation is invalid**: randomly held-out folds put future
observations in the training set, so the model interpolates a gap it has seen
both sides of — which is not forecasting, and scores far too well.

### What to monitor once it is deployed

| Signal | Alarm when | Because |
|---|---|---|
| **Rolling RMSE** | it drifts above its historical band | the model is decaying |
| **Mean error** | it is significantly non-zero | **bias**, which a business feels first |
| **Interval coverage** | far from nominal | the uncertainty is misreported |
| **Residual ACF** | structure appears | something new is happening |
| **Skill vs naive** | approaches zero | the model has stopped earning its keep |

### 🔢 The bias check, which almost nobody runs

**Mean forecast error: +2.2898 (t = 1.604, p = 0.1370) — no evidence of
bias.**

> **A forecast can have a small RMSE and still be biased** — consistently 5%
> low, say — **and a business will feel the bias long before it feels the
> variance.** Test the mean error, not only its magnitude.

### ⚠️ And the thing that ends every forecasting model

**A structural break.** A model fitted before a pandemic, a policy change or a
new competitor is fitted to a world that no longer exists, and no amount of
retraining on a window that spans the break will help.

**Detect it** by watching rolling error for a step change, not a drift. **Then
decide** whether to refit on post-break data only — which means throwing away
history you may not be able to spare.

---

## Practice problems

**1. A periodogram of daily sales shows a strong peak at frequency 0.1429 and
a smaller one at 0.0027. What are they?**

**1/0.1429 = 7.0 → a weekly cycle.** Expected on daily retail data — weekends
differ from weekdays.

**1/0.0027 = 370 ≈ 365 → an annual cycle.** Weaker in the spectrum, which is
usual: it is diffuse rather than sharp because the annual pattern is not
identical year to year, and there are few complete cycles in the record.

**What to do about it:** SARIMA can take **one** m, so set m = 7 for the
strong weekly cycle. **The annual cycle needs Fourier terms** in a regression
with ARIMA errors — Unit 3's answer to multiple seasonalities.

**And check the record length before believing the annual peak:** with two
years of data you have two cycles, which is not enough to distinguish a real
annual pattern from a slow trend.

**2. Two models: A has RMSE 10 and MAE 6; B has RMSE 12 and MAE 5. Which do
you deploy?**

**It depends on the cost of an error, and you should have decided before
looking.**

- **B has the lower MAE** — it is closer on a typical day.
- **A has the lower RMSE** — it has fewer large misses. Note that B's
  RMSE/MAE ratio is 2.4 against A's 1.67, which says **B's errors are more
  spread out**: mostly small, occasionally large.

**Deploy A if** a large miss is disproportionately expensive — a stock-out
that loses a customer, a staffing shortfall, a grid failure.

**Deploy B if** the cost is proportional — inventory holding cost, where being
off by 20 twice is the same as being off by 10 four times.

**And before deploying either:** check both against **seasonal naive**, check
the **mean error** for bias, and compare on **rolling-origin CV** rather than
one window. Two numbers from one held-out year is not enough to choose.

**3. Explain why MAPE is a bad choice for forecasting daily demand for a
product that sometimes sells zero units.**

**Because MAPE divides by the actual, and the actual is sometimes zero.**

- **At y = 0 it is undefined** — a division by zero, and most implementations
  return infinity or drop the observation silently, which is worse because the
  metric then quietly ignores exactly the days you got wrong.
- **Near zero it explodes.** Predicting 2 when the actual is 1 is a 100%
  error; the lab measured a uniform absolute error of 1.0 producing a MAPE of
  **75%**.
- **It is asymmetric**, capped at 100% for under-forecasts and unbounded for
  over-forecasts, so it **rewards systematic under-forecasting** — the worst
  possible bias for stock levels.

**Use MASE instead**, or MAE if all the series are on the same scale.
Intermittent demand also has its own literature — Croston's method — precisely
because ordinary metrics and models both fail on it.

**4. Your model's rolling RMSE has been stable for two years and doubled last
month. Diagnose it.**

**Distinguish a break from decay first — the shape tells you which.** A step
change points to an event; a gradual drift points to slow model decay.
Doubling in one month is a **step**.

**Then work through, in order:**

1. **Did the data change?** A new source system, a changed unit, a column
   silently renamed. This is the most common cause and the easiest to fix.
2. **Was there a real event?** A promotion, a competitor, a policy change, a
   supply shock. Check the series against the calendar before touching the
   model.
3. **Is it one series or all of them?** All at once points at the pipeline;
   one points at that series' world.
4. **Are the residuals autocorrelated again?** New structure means the model
   is missing something it used to capture.
5. **Is the error biased or just larger?** A shifted mean is a level break; a
   wider spread is increased volatility. **They need different fixes.**

**And what not to do first:** retrain. If the cause is a broken pipeline,
retraining bakes the corruption into the model.

**5. Why is rolling-origin CV expensive, and what would you do about it on a
large problem?**

**Because it refits the model once per fold** — the lab's 6 folds meant 6 full
maximum-likelihood fits per candidate specification, and it evaluated 5
candidates, so 30 fits for one table.

**The costs scale badly:** (number of folds) × (number of candidates) ×
(cost of one fit), and for a SARIMA that cost is a numerical optimisation.

**What to do:**

1. **Fewer, larger folds.** Six folds of 6 months tells you nearly as much as
   twenty folds of 1 month, at a third of the cost.
2. **Use AIC to shortlist, CV to choose.** AIC is one fit per candidate; run
   it over the full grid, then CV only the top three. **This is the standard
   compromise.**
3. **A fixed rolling window** instead of an expanding one — each fit sees the
   same amount of data, so cost per fold is constant rather than growing.
4. **Parallelise.** The folds are independent, so it is embarrassingly
   parallel — Course 12 B's territory.
5. **For many series, sample them.** Selecting a specification on 200
   representative series and applying it to 10,000 is what large-scale
   forecasting systems actually do.

---

## Exam questions from this unit

**Two marks**

1. What does a spectral density measure?
2. Convert a frequency of 0.25 to a period.
3. Why must you detrend before a periodogram?
4. What is spectral leakage?
5. Give the MASE formula.
6. Name two failures of MAPE.
7. Why is k-fold CV invalid on a time series?
8. Why can a decision tree not extrapolate a trend?

**Five marks**

1. Explain the frequency-domain representation and the use of a periodogram.
2. Compare RMSE, MAE, MAPE and MASE, with the failure mode of each.
3. Explain rolling-origin cross-validation and why it replaces k-fold.
4. Compare classical forecasting methods with machine-learning approaches.
5. Describe what to monitor for a forecast running in production.

**Ten marks**

1. Explain spectral analysis in full and show how it identifies the seasonal
   period, with worked figures.
2. Compare ARIMA, exponential smoothing and machine-learning forecasting on a
   seasonal series, and explain how you would choose between them and evaluate
   the winner.

---

## Mistakes that cost marks

- **Quoting a frequency instead of a period.** Convert before you speak.
- **Running a periodogram without detrending.** The trend dominates and hides
  everything.
- **Reading leakage sidelobes as separate cycles.**
- **Using MAPE on data near zero.** Undefined, explosive and asymmetric.
- **Choosing the metric after seeing the results.**
- **Quoting an RMSE with no baseline.** Seasonal naive scored 14.152.
- **Using k-fold CV.**
- **Proposing a tree ensemble for a trending series** without differencing.
- **Claiming ML beats classical methods** without saying how much data you
  had.
- **Monitoring only the error magnitude and never the bias.**
