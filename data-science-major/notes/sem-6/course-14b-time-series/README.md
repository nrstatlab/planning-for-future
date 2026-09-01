# Course 14 B — Time Series Analysis and Forecasting

**Semester VI**

**This is a Track B course**, paired with
Course 15 B (Data Engineering & MLOps), and it
continues the track you began in Semester V with Big Data and Cloud Computing.

---

## The one thing to understand before anything else

**Everything you learned in Courses 4, 8 and 12 A assumed your observations
were independent. In a time series they are not, and that single fact breaks
almost every technique you know.**

| What you learned | Why it fails here |
|---|---|
| Shuffle, then split 80/20 | **A random split lets the model see the future** |
| k-fold cross-validation | Every fold trains on data that comes *after* the validation fold |
| The standard error of the mean | Assumes independent draws; correlated data has far less information than n suggests |
| Bootstrap resampling | Destroys the ordering, which *is* the signal |
| "More data is more information" | 400 correlated points carry the information of far fewer |

**The ordering is not metadata. It is the data**, and every method in this
course exists to model dependence between an observation and the ones before
it.

### 🎯 The single most examinable idea

> **Stationarity.** A stationary series has a constant mean, a constant
> variance, and an autocovariance that depends only on the *gap* between two
> points and not on *when* they are.

Almost every model here requires it. **Units 1 and 3 are about testing for it
and getting there**, and once you have it, the modelling in Unit 2 is
comparatively easy.

---

## What runs here

**Everything.** This is one of only two courses in the whole programme with no
`NOT EXECUTED` file anywhere — the other is Course 12 A.

statsmodels 0.14 implements every technique the syllabus names:

| Technique | Real call |
|---|---|
| Decomposition, STL | `seasonal_decompose`, `STL` |
| ACF, PACF | `acf`, `pacf` |
| Stationarity | `adfuller`, `kpss` |
| ARMA, ARIMA, SARIMA | `ARIMA`, `SARIMAX` |
| Diagnostics | `acorr_ljungbox` |
| Multivariate | `VAR`, `test_causality` |
| State space | `UnobservedComponents` (Kalman filter) |
| Spectral | `scipy.signal.periodogram` |
| Exponential smoothing | `ExponentialSmoothing` |

```bash
pip install -r tools/requirements.txt
python3 tools/run_timeseries_labs.py
```

### 💡 And the discipline that makes it worth running

**The series are generated from KNOWN coefficients**, so every fit can be
checked against the truth that produced it:

- an AR(2) built with **φ = (0.6, −0.3)**
- an MA(1) whose lag-1 ACF must equal **θ/(1+θ²) = 0.4698**
- a macro system where **GDP causes the other two and neither causes GDP**

**A model that merely converges has proved nothing.** Checking against a known
answer is the only way to show that identification and estimation *work*, and
it is why the labs found — and report — a coefficient estimate 2.5 standard
errors from the truth on one draw.

---

## Course objectives (verbatim)

The course aims to:

1. Provide fundamental understanding of time series data, components, and
   characteristics.
2. Train students in identifying, modeling, and forecasting using
   ARMA/ARIMA/SARIMA models.
3. Introduce state-space and multivariate approaches for complex data.
4. Familiarize students with modern forecasting methods, including spectral and
   evaluation techniques.
5. Enable hands-on practice with real-world datasets using R/Python statistical
   libraries.

> ### ⚠️ Objective 5 says R **or** Python, and never chooses
>
> The evaluation method names both languages, and the practicals assume
> whichever you have. These notes use **Python throughout** and say so; a
> student following the syllabus literally has no basis for the choice. See
> review finding **D30**.

## The five units

| Unit | Question it answers |
|---|---|
| **[1](unit-1.md)** | What is a time series, and is this one stationary? |
| **[2](unit-2.md)** | How do I model a stationary series, and forecast it? |
| **[3](unit-3.md)** | What if it is not stationary, or it has a season? |
| **[4](unit-4.md)** | What if there are several series, or the state is hidden? |
| **[5](unit-5.md)** | Which cycles is it made of, and which forecast is best? |

**Units 1–3 are the spine.** Unit 4 is two genuinely different frameworks
bolted on, and Unit 5 is where you learn that the answer to "which model is
best?" depends on a metric you should have chosen first.

---

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 13 experiments
- `labs/course-14b-timeseries/` — the code, and the runner that asserts every figure
  these notes quote
- `data/course-14b-timeseries/` — **practice datasets**, CSV: `ar2-series.csv`, `macro-indicators.csv`, `seasonal-sales.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.

## Cross-course connections

| From | To | What is shared |
|---|---|---|
| **Course 4 (Statistics)** | Units 1, 2 | Hypothesis tests, p-values and confidence intervals — used constantly, and the ADF's reversed null is where they bite |
| **Course 12 A (ML)** | Unit 5 | The bias–variance trade-off, arriving as AIC against held-out RMSE — and a train/test split you must do differently |
| **Course 9 (Pandas)** | throughout | Every series here is a pandas object; `resample`, `shift` and `rolling` are the working tools |
| **Course 6 (R)** | the lab | The syllabus says "R/Python". R's `forecast` package is the reference implementation; statsmodels is what runs here |
| **Course 15 B (MLOps)** | Unit 5 | Rolling-origin backtesting is what monitoring a deployed forecast actually means |

---

## Textbooks

- Brockwell & Davis, *Introduction to Time Series and Forecasting*, 2nd edition,
  Springer — the prescribed text, and it covers Units 1–4 closely.

**References:** Box, Jenkins & Reinsel, *Time Series Analysis: Forecasting and
Control* — the origin of the ARIMA notation this course uses · Montgomery,
Jennings & Kulahci, *Introduction to Time Series Analysis and Forecasting*,
Wiley · Shumway & Stoffer, *Time Series Analysis and Its Applications: With R
Examples*.

**Free and current:** Hyndman & Athanasopoulos, *Forecasting: Principles and
Practice*, is open access at [otexts.com/fpp3](https://otexts.com/fpp3/). It is
not on the syllabus, and it is the book most working forecasters actually use.

## How to study this course

1. **Learn the two identification rules and be able to apply them.** ACF cuts
   off → MA(q); PACF cuts off → AR(p). Everything in Unit 2 hangs on them.
2. **Draw an ACF by hand** for white noise, an AR(1) with φ = 0.8, and an
   MA(1). If you can sketch those three, you can read any correlogram.
3. **Know the ADF's null by heart.** It is the reverse of what you expect, and
   getting it backwards inverts every conclusion you draw.
4. **Do the differencing arithmetic.** d for trend, D for season, and stop as
   soon as the ADF rejects.
5. **Run the labs.** Thirteen experiments, all executable, all checked against
   generated truth.

### ⚠️ The four sentences that carry the most marks

- **"The ADF's null is that a unit root is present, so a small p-value means
  stationary."**
- **"The PACF cuts off at lag p for an AR(p); the ACF cuts off at lag q for an
  MA(q)."**
- **"k-fold cross-validation is invalid on a time series; use rolling
  origin."**
- **"Granger causality means 'helps predict', not 'causes'."**
