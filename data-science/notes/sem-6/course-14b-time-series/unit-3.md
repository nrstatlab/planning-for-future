# Unit 3 — Non-Stationary and Seasonal Models

**Syllabus topics:** Non-stationary time series: differencing, unit roots.
Seasonal models: SARIMA and multiplicative seasonal ARIMA. Identification,
estimation, and diagnostic checks for seasonal models.

---

## 3.1 Unit roots

### 🎯 What a unit root actually is

Write an AR(1) as **yₜ = φyₜ₋₁ + εₜ**. The characteristic equation is
**1 − φB = 0**, with root **B = 1/φ**.

- **|φ| < 1** → root outside the unit circle → **stationary**
- **φ = 1** → root **on** the unit circle → **a unit root**, the random walk
- **|φ| > 1** → explosive, and almost never seen in real data

### 💡 The consequence that matters

> **With |φ| < 1 a shock decays. With φ = 1 a shock is permanent.**

An AR(1) with φ = 0.99 and a random walk look identical over a hundred
observations and behave completely differently over a thousand. **That is why
you test rather than eyeball.**

And it is the economic difference between "GDP will return to trend after this
recession" and "this recession has permanently lowered the path" — the same
question, which is why unit-root testing is a large literature.

---

## 3.2 The Augmented Dickey–Fuller test

### ⚠️ The hypotheses run the opposite way from most tests

| Test | H₀ | Small p-value means |
|---|---|---|
| **ADF** | **there IS a unit root** (non-stationary) | **STATIONARY** |
| **KPSS** | the series **IS stationary** | **NON-stationary** |

**Two tests with opposite nulls.** Running both is standard practice —
precisely because *failing to reject* is not the same as *accepting*.

### 🔢 Measured

| Series | ADF stat | p | Verdict |
|---|---:|---:|---|
| white noise | −18.483 | 0.0000 | **stationary** |
| AR(2), stationary | −14.202 | 0.0000 | **stationary** |
| **random walk** | −2.164 | **0.2197** | **unit root** |
| **random walk, differenced** | −18.468 | **0.0000** | **stationary** |
| monthly sales | −0.640 | 0.8616 | unit root |
| sales, differenced | −8.633 | 0.0000 | stationary |
| sales, seasonally differenced | −3.514 | 0.0076 | stationary |

**The random walk is the point.** Undifferenced, p = 0.2197 — a unit root, as
it must be, since a random walk *is* the textbook unit-root process.
Differenced once, p = 0.0000.

> **That is where the d in ARIMA(p,d,q) comes from: d is how many differences
> it takes to reach stationarity.**

### 🎯 The `regression` argument, which decides the answer

`adfuller(x, regression=...)` chooses what the test allows for:

| Setting | Allows | Use when |
|---|---|---|
| `"c"` | a constant | the default; series has a non-zero mean |
| **`"ct"`** | a constant **and a trend** | **you suspect a deterministic trend** |
| `"n"` | nothing | rare; series is centred at zero |

### 🔢 And it flips the conclusion

| Series | ADF `c` | ADF `ct` | KPSS `c` | Conclusion |
|---|---:|---:|---:|---|
| white noise | 0.0000 | 0.0000 | 0.1000 | stationary — both agree |
| **random walk** | 0.2197 | **0.5576** | 0.0100 | **non-stationary** |
| **trend + noise** | **0.9086** | **0.0000** | 0.0100 | **TREND-stationary** |

**Read the third row.** "Trend + noise" looks non-stationary to the plain ADF
(p = 0.9086) and **stationary once the test is allowed a trend** (p = 0.0000).
It is **trend-stationary** — the right treatment is to **detrend, not
difference**.

**The random walk does not flip** — p = 0.5576 even under `"ct"` — because it
has a genuine unit root, and no amount of detrending removes one.

> **Deciding between a deterministic trend and a stochastic trend is what this
> pair of tests is for**, and it is the most examinable thing in Unit 3.

---

## 3.3 Differencing, and how much

### 📖 The operators

| Operator | Written | Removes |
|---|---|---|
| **first difference** | ∇yₜ = (1−B)yₜ = yₜ − yₜ₋₁ | a **linear trend** |
| **second difference** | ∇²yₜ = (1−B)²yₜ | a **quadratic trend** |
| **seasonal difference** | ∇ₘyₜ = (1−Bᵐ)yₜ = yₜ − yₜ₋ₘ | **seasonality** |

**B is the backshift operator: Byₜ = yₜ₋₁.** Every ARIMA equation in every
textbook is written with it, so learn it once.

### ⚠️ Over-differencing, measured

| Series | ADF p | Variance |
|---|---:|---:|
| original (trend + noise) | 0.9086 | 3351.744 |
| **differenced once** | 0.0000 | **16.896** |
| **differenced TWICE** | 0.0000 | **47.923** |

**Differencing twice made the variance nearly three times larger.**

> **That is the signature of over-differencing.** Each unnecessary difference
> injects noise and adds a spurious negative MA term.

**The rule: difference until the ADF rejects, then stop.** If the variance
goes up, you have gone one too far — and **d is almost never more than 2**.

### 🎯 The two differences do different jobs

| Difference | Removes | Costs you |
|---|---|---|
| **d = 1** | the trend — the level drifts | 1 observation |
| **D = 1** | the seasonality — January to January | **m observations** |

**Measured on the sales series:**

| Series | std | ADF p |
|---|---:|---:|
| original | 30.949 | 0.8616 |
| d = 1 | 10.144 | 0.0000 |
| **D = 1 (lag 12)** | **5.729** | 0.0076 |
| d = 1 **and** D = 1 | **6.133** | 0.0000 |

### ⚠️ And an honest tension in that table

**Adding d = 1 on top of D = 1 raised the standard deviation, 5.729 → 6.133.**
By the over-differencing rule, the seasonal difference alone had already done
the job.

**Yet the airline model, which uses both, forecast best.**

**Report both facts.** The variance rule is a guide, not a proof, and the
held-out error is the arbiter. Two *seasonal* differences would be
indefensible; one extra regular difference is a judgement call that the test
set settled.

---

## 3.4 SARIMA

### 📖 The full specification

$$\text{SARIMA}(p,d,q)(P,D,Q)_m$$

| Part | Meaning |
|---|---|
| **p, d, q** | the non-seasonal AR order, differencing, MA order |
| **P, D, Q** | the **seasonal** AR order, differencing, MA order |
| **m** | the **number of periods in a season** |

**In backshift form**, and this is the equation the exam may ask you to write:

$$\phi_p(B)\,\Phi_P(B^m)\,(1-B)^d(1-B^m)^D y_t = \theta_q(B)\,\Theta_Q(B^m)\,\varepsilon_t$$

### 🎯 It is multiplicative, and that is the whole idea

The seasonal polynomials are in **Bᵐ**, and they **multiply** the non-seasonal
ones. A SARIMA(1,0,0)(1,0,0)₁₂ expands to:

$$(1-\phi B)(1-\Phi B^{12})y_t = \varepsilon_t
\;\Rightarrow\; y_t = \phi y_{t-1} + \Phi y_{t-12} - \phi\Phi y_{t-13} + \varepsilon_t$$

**Note the lag-13 term nobody put there.** It falls out of the multiplication,
and it is exactly right: if this month depends on last month, and on this
month last year, then it depends on *last month last year* too.

**That interaction term is what "multiplicative seasonal ARIMA" means**, and
it is why the model needs three coefficients' worth of structure while
estimating only two.

### ⚠️ Getting m wrong

**m is the number of observations in one full cycle**, not the number of
cycles:

| Data | m |
|---|---:|
| monthly, annual cycle | **12** |
| quarterly, annual cycle | **4** |
| daily, weekly cycle | **7** |
| hourly, daily cycle | **24** |
| **daily, annual cycle** | **365** — and SARIMA cannot handle it |

**That last row is worth knowing.** At m = 365 a seasonal difference costs a
year of data and the model becomes unusable. Long seasonality needs Fourier
terms with a regression model, or a method like Prophet or TBATS.

### 🔢 SARIMA against ARIMA, measured

| Model | AIC | BIC | Ljung-Box p | **Test RMSE** |
|---|---:|---:|---:|---:|
| ARIMA(1,1,1) | 727.50 | 735.46 | **0.0000** | **20.359** |
| ARIMA(2,1,2) | 615.04 | 628.27 | 0.0555 | 9.330 |
| SARIMA(1,1,1)(1,1,1)₁₂ | **476.32** | 488.29 | 0.5117 | 6.891 |
| **SARIMA(0,1,1)(0,1,1)₁₂** | 485.76 | **492.95** | **0.8590** | **6.530** |

**The seasonal models win by a wide margin** — best SARIMA RMSE **6.530**
against the best plain ARIMA's **9.330**, and the naive ARIMA(1,1,1) fails its
Ljung-Box outright.

> **A non-seasonal ARIMA on a series with an annual cycle has no mechanism to
> represent that cycle.** It can only average it away.

---

## 3.5 The airline model

$$\text{SARIMA}(0,1,1)(0,1,1)_{12}$$

**Two parameters.** Fitted in the lab:

| Parameter | Estimate | Std err |
|---|---:|---:|
| `ma.L1` | **−0.3223** | 0.1016 |
| `ma.S.L12` | **−0.6044** | 0.1168 |
| `sigma2` | 21.4354 | 3.6285 |

### 💡 Why it deserves a name

Box and Jenkins fitted it to international airline passenger numbers, and it
turns out to fit a remarkable share of monthly business series **with no
tuning at all**.

**It is the right *first* model for seasonal monthly data.** Quote it by name,
start there, and make anything larger earn its place against it on held-out
error.

**And it had the best held-out RMSE here**, against four specifications with
up to seven parameters.

---

## 3.6 Identifying a seasonal model

### The procedure, in order

1. **Plot it.** Confirm the seasonality and read m off the plot — or off a
   periodogram (Unit 5).
2. **Stabilise the variance** if the swing grows: take logs.
3. **Seasonal difference** (D = 1) if the seasonality is strong.
4. **Regular difference** (d = 1) if a trend remains after step 3.
5. **Read the ACF/PACF of the differenced series**, at two scales:
   - **lags 1, 2, 3 …** → the non-seasonal p and q
   - **lags m, 2m, 3m …** → the **seasonal** P and Q
6. **Fit, then check Ljung-Box at lag ≥ 2m** — the residual test must reach
   past the seasonal lags or it cannot see seasonal structure.

### 🎯 Step 5 is the one that is examined

**Read the correlogram at two scales.** A spike at lag 12 alone identifies a
seasonal MA(1); a spike at lag 1 alone identifies a non-seasonal MA(1); both
identify the airline model.

### ⚠️ And step 6's detail

**Ljung-Box at 10 lags on monthly data cannot detect seasonal structure**,
because it never looks at lag 12. Use **at least 2m lags** on seasonal data.

---

## Practice problems

**1. A monthly series has ADF p = 0.42. After one difference, p = 0.03. After
two, p = 0.001 but the variance has doubled. What is d?**

**d = 1.**

The rule is *difference until the ADF rejects, then stop*. It rejected at
d = 1 (p = 0.03 < 0.05), so the job is done.

**The doubled variance at d = 2 is the diagnostic that confirms it** — that is
exactly the over-differencing signature the lab measured (16.896 → 47.923).
The second difference also introduces a spurious negative MA term, so you
would find yourself fitting a θ near −1 to undo damage you caused.

**A smaller p-value is not a better answer.** Stationarity is a threshold, not
a score to maximise.

**2. Write out SARIMA(1,1,0)(0,1,1)₁₂ in backshift form and say how many
observations you lose.**

$$(1-\phi B)(1-B)(1-B^{12})y_t = (1 + \Theta B^{12})\varepsilon_t$$

**Observations lost: d + D×m = 1 + 12 = 13.** From 60 monthly observations
that leaves 47 to fit 2 parameters.

**Parameters: φ, Θ, and σ² — three estimated quantities.**

**3. Your SARIMA residuals show a clear spike at lag 12. What did you get
wrong?**

**The seasonal part is under-specified.** The regular terms have handled the
short lags and left the annual structure untouched.

**In order:**

1. **Add a seasonal term** — raise Q to 1 if the *ACF* spikes at 12, or P to 1
   if the *PACF* does.
2. **Check D.** If lags 12, 24 and 36 are *all* significant and decaying
   slowly, the series needs a seasonal difference you have not applied.
3. **Check m is right.** A spike at 12 on quarterly data means m should be 4
   and your cycle is three years, not one.

**And check that your Ljung-Box reached lag 12 at all.** At 10 lags it never
looked.

**4. Explain why SARIMA(1,0,0)(1,0,0)₁₂ has a lag-13 term.**

**Because the seasonal and non-seasonal polynomials multiply.**

$$(1-\phi B)(1-\Phi B^{12}) = 1 - \phi B - \Phi B^{12} + \phi\Phi B^{13}$$

so

$$y_t = \phi y_{t-1} + \Phi y_{t-12} - \phi\Phi y_{t-13} + \varepsilon_t.$$

**And it is right, not an artefact.** If this month depends on last month, and
on the same month last year, then it must also depend on *last month last
year* — the model captures that interaction with **no extra parameter**, since
the coefficient is the product of two it already has.

**That is the argument for multiplicative seasonality**: the additive
alternative would need a third free parameter to say the same thing, and would
be free to say something inconsistent.

**5. You have five years of daily sales with both a weekly and an annual
pattern. Can SARIMA handle it?**

**No — SARIMA has room for exactly one seasonal period.**

You could set **m = 7** and capture the weekly cycle, but the annual cycle
would be left in the residuals. Setting **m = 365** is worse: the seasonal
difference costs a full year of the five you have, and Bᶟ⁶⁵ makes the model
enormous and unstable.

**What to do instead:**

- **Fourier terms in a regression with ARIMA errors.** Add sin/cos pairs at
  both frequencies as regressors and let ARIMA model what is left. This is the
  standard answer, and it handles **multiple** seasonalities with few
  parameters.
- **TBATS**, which was designed for exactly this.
- **Prophet**, which decomposes into trend plus multiple Fourier seasonalities
  plus holidays.
- **A regression on calendar features** — day of week, week of year, holiday
  flags — with a machine-learning model, remembering Unit 5's warning that a
  tree cannot extrapolate a trend.

**The exam answer:** name the limitation (one m), name Fourier terms as the
fix, and say why (many periods, few parameters, no data loss).

---

## Exam questions from this unit

**Two marks**

1. What is a unit root?
2. State the ADF null hypothesis.
3. State the KPSS null hypothesis.
4. What does the `regression="ct"` option do?
5. Write the backshift form of a seasonal difference.
6. Expand SARIMA(p,d,q)(P,D,Q)ₘ.
7. What is m for quarterly data with an annual cycle?
8. How many observations does D = 1 cost?

**Five marks**

1. Explain unit roots and the ADF test, including its reversed null.
2. Explain over-differencing and how to detect it.
3. Explain why ADF and KPSS are run together, with the four possible outcomes.
4. Explain multiplicative seasonality and derive the lag-13 term.
5. Describe the procedure for identifying a seasonal model.

**Ten marks**

1. Explain non-stationarity in full — its causes, its tests, and its
   treatments — and distinguish a deterministic from a stochastic trend.
2. Explain SARIMA completely, with the backshift equation, the identification
   procedure, and a worked comparison against a non-seasonal ARIMA.

---

## Mistakes that cost marks

- **Getting the ADF null backwards.** It inverts every conclusion.
- **Differencing until the p-value is smallest.** Stop at the first rejection.
- **Differencing a trend-stationary series.** Detrend it — and use `"ct"` to
  find out which it is.
- **Setting m to the number of cycles.** It is the length of one cycle.
- **Two seasonal differences.** D is 0 or 1.
- **Ljung-Box at 10 lags on monthly data.** It never sees lag 12.
- **Saying seasonal ARIMA is additive.** It is multiplicative, and the lag-13
  term proves it.
- **Trying SARIMA on daily data with an annual cycle.** Name Fourier terms
  instead.
