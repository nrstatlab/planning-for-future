# Unit 2 — Random Variables, Expectation and Variance

**Syllabus topics:** Random variables — definition, types (discrete and
continuous), and properties. Probability mass function (PMF) and probability
density function (PDF). Cumulative distribution function (CDF). Mathematical
expectation (mean), variance and standard deviation. Moments and
moment-generating functions.

---

## 2.1 Random variables

### 🎯 The big idea

A random variable is a rule that attaches a **number** to each outcome of a
random experiment. It turns "heads, heads, tails" into "2 heads", so you can do
arithmetic with chance.

### 📖 The story

You toss a coin three times. The outcomes are things like HHT and THH — not
numbers, so you cannot average them. But if you count the heads, every outcome
becomes a number: 0, 1, 2 or 3. Now you can ask "on average, how many heads?"
That counting rule is a random variable, and it is what makes probability
computable.

### 🔢 Formally

A random variable X is a function from the sample space to the real numbers.

**Sample space for three coin tosses (8 outcomes):**

| Outcome | HHH | HHT | HTH | THH | HTT | THT | TTH | TTT |
|---|---|---|---|---|---|---|---|---|
| X = heads | 3 | 2 | 2 | 2 | 1 | 1 | 1 | 0 |

Collecting the values:

| x | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| P(X = x) | 1/8 | 3/8 | 3/8 | 1/8 |

That table is the **probability distribution** of X. Notice the probabilities
sum to 1 — always check this first; if they do not, something is wrong.

### Discrete vs continuous

| | Discrete | Continuous |
|---|---|---|
| Values | Countable — 0, 1, 2, … | Any value in an interval |
| Examples | Number of heads, defects, customers | Height, weight, time, temperature |
| Described by | **PMF** — P(X = x) | **PDF** — f(x) |
| P(X = a exactly) | Can be positive | **Always zero** |
| Total probability | Σ P(x) = 1 | ∫ f(x) dx = 1 |

**Why is P(X = a) zero for a continuous variable?** Ask for the probability
that someone is *exactly* 170.000000… cm tall, to infinite precision. There are
infinitely many possible heights, so any single one has probability zero. Only
*intervals* have positive probability: P(169.5 < X < 170.5) is a sensible
question.

A useful consequence: for continuous variables **P(X ≤ a) = P(X < a)**, because
the endpoint contributes nothing. For discrete variables they differ, and
mixing them up is a common error.

## 2.2 PMF, PDF and CDF

### Probability mass function (PMF) — discrete

> **p(x) = P(X = x)**

Properties: p(x) ≥ 0 for all x, and Σ p(x) = 1.

### Probability density function (PDF) — continuous

> **P(a ≤ X ≤ b) = ∫ₐᵇ f(x) dx**

Properties: f(x) ≥ 0, and ∫ over all x of f(x) dx = 1.

**f(x) is not a probability.** It is a *density* — probability per unit of x —
and it can exceed 1. Probability is the **area under** the curve, not the
height of it. This is worth stating explicitly in an exam answer.

### Cumulative distribution function (CDF)

> **F(x) = P(X ≤ x)**

The CDF works for both kinds of variable, which is why it matters.

- Discrete: F(x) = Σ p(t) for all t ≤ x — a step function
- Continuous: F(x) = ∫ f(t) dt from −∞ to x — a smooth curve

**Properties of any CDF:**

1. F(−∞) = 0 and F(+∞) = 1
2. Non-decreasing — it never goes down
3. P(a < X ≤ b) = F(b) − F(a)
4. For continuous X, f(x) = dF(x)/dx — the PDF is the derivative of the CDF

**Worked example.** For the coin-toss variable above:

| x | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| p(x) | 1/8 | 3/8 | 3/8 | 1/8 |
| **F(x)** | 1/8 | 4/8 | 7/8 | 8/8 = 1 |

So P(X ≤ 2) = 7/8, and P(1 < X ≤ 3) = F(3) − F(1) = 1 − 4/8 = **4/8**.

## 2.3 Mathematical expectation

### 🎯 The big idea

The expected value is the long-run average — what you would get per trial if
you repeated the experiment an enormous number of times.

### 📖 The story

A carnival game costs ₹10 to play. You roll a die and win ₹60 if you get a six,
nothing otherwise. Is it worth playing?

Your expected winnings are 60 × (1/6) = ₹10. The game costs ₹10. So on average
you break exactly even — play a thousand times and you finish roughly where you
started. Now suppose the prize is ₹50: expected winnings ₹8.33 against a ₹10
cost, so you lose ₹1.67 per play on average. That is how every casino, lottery
and insurance company is designed.

### 🔢 The formula

> **Discrete: E(X) = Σ xᵢ · p(xᵢ)**
> **Continuous: E(X) = ∫ x · f(x) dx**

In plain English: multiply each value by its probability, then add everything
up. It is a **weighted average**, where the weights are the probabilities.

**Worked example.** X = number of heads in three tosses.

| x | p(x) | x·p(x) |
|---:|---:|---:|
| 0 | 1/8 | 0 |
| 1 | 3/8 | 3/8 |
| 2 | 3/8 | 6/8 |
| 3 | 1/8 | 3/8 |
| **Σ** | **1** ✓ | **12/8 = 1.5** |

E(X) = **1.5 heads**.

### 💡 The "aha!" moment

You can never actually get 1.5 heads. The expected value need not be a possible
outcome at all — it is the **balance point** of the distribution, the place
where the probability weights would sit level on a see-saw. "Expected" is a
technical term, not a prediction of what will happen.

### Properties of expectation

| Property | Statement |
|---|---|
| Constant | E(c) = c |
| Scaling | E(aX) = a·E(X) |
| Linearity | **E(aX + b) = a·E(X) + b** |
| Additivity | **E(X + Y) = E(X) + E(Y)** — always, even if dependent |
| Products | E(XY) = E(X)·E(Y) **only if X and Y are independent** |

Linearity holding regardless of independence is genuinely useful and often
tested.

## 2.4 Variance and standard deviation

> **Var(X) = E[(X − μ)²]**
>
> **Shortcut: Var(X) = E(X²) − [E(X)]²**

The shortcut is faster in every exam. Use it.

> **SD(X) = σ = √Var(X)**

**Worked example**, continuing with the coin tosses:

| x | p(x) | x·p(x) | x²·p(x) |
|---:|---:|---:|---:|
| 0 | 1/8 | 0 | 0 |
| 1 | 3/8 | 3/8 | 3/8 |
| 2 | 3/8 | 6/8 | 12/8 |
| 3 | 1/8 | 3/8 | 9/8 |
| **Σ** | 1 | **1.5** | **24/8 = 3.0** |

- E(X) = 1.5
- E(X²) = 3.0
- Var(X) = 3.0 − (1.5)² = 3.0 − 2.25 = **0.75**
- SD(X) = √0.75 = **0.866**

*Check against the binomial formula* (Unit 3): np(1−p) = 3 × 0.5 × 0.5 = 0.75 ✓

### Properties of variance

| Property | Statement |
|---|---|
| Constant | Var(c) = **0** |
| Adding a constant | **Var(X + b) = Var(X)** |
| Scaling | **Var(aX) = a²·Var(X)** |
| General | Var(aX + b) = a²·Var(X) |
| Sum | Var(X + Y) = Var(X) + Var(Y) **only if independent** |

Two of these are examined constantly:

- **Adding a constant does not change the variance.** Shift every mark up by 5
  and the spread is identical — everyone moved together.
- **Scaling multiplies the variance by a².** Double every value and the
  variance quadruples, because variance is in *squared* units.

## 2.5 Moments

### 🎯 The big idea

Moments are a family of numbers that describe a distribution's shape —
successively capturing where it sits, how wide it is, how lopsided, and how
heavy-tailed.

### The rth moment

**About the origin:**  μ′ᵣ = E(Xʳ)
**About the mean (central):**  μᵣ = E[(X − μ)ʳ]

| Moment | Formula | What it describes |
|:---:|---|---|
| 1st about origin | μ′₁ = E(X) | **Mean** — location |
| 2nd central | μ₂ = E[(X−μ)²] | **Variance** — spread |
| 3rd central | μ₃ | **Skewness** — asymmetry |
| 4th central | μ₄ | **Kurtosis** — tail weight and peakedness |

**Relationships worth memorising:**

- μ₂ = μ′₂ − (μ′₁)²   *(the variance shortcut, in moment notation)*
- β₁ = μ₃² / μ₂³ — skewness coefficient
- β₂ = μ₄ / μ₂² — kurtosis coefficient

### Interpreting skewness and kurtosis

| Skewness | Shape |
|---|---|
| = 0 | Symmetric |
| > 0 | Positively skewed — tail to the **right**, mean > median |
| < 0 | Negatively skewed — tail to the **left**, mean < median |

| Kurtosis β₂ | Name | Shape |
|---|---|---|
| = 3 | **Mesokurtic** | Like the normal distribution |
| > 3 | **Leptokurtic** | Sharper peak, heavier tails |
| < 3 | **Platykurtic** | Flatter, thinner tails |

A memory aid: **lepto**kurtic *leaps* up (tall and peaked); **platy**kurtic is
*plateau*-like (flat).

## 2.6 Moment-generating function (MGF)

> **Mₓ(t) = E(e^tX)**

The trick that makes it useful: **differentiate and set t = 0** to extract each
moment.

> **μ′ᵣ = d^r Mₓ(t)/dt^r evaluated at t = 0**

So:
- M′(0) = E(X) — the mean
- M″(0) = E(X²), from which Var(X) = M″(0) − [M′(0)]²

**Worked example.** For X ~ Binomial(n, p), Mₓ(t) = (q + peᵗ)ⁿ where q = 1−p.

- M′(t) = n(q + peᵗ)ⁿ⁻¹ · peᵗ
- At t = 0: eᵗ = 1 and q + p = 1, so M′(0) = n · 1ⁿ⁻¹ · p = **np** ✓

That is the binomial mean, obtained without summing an infinite series.

### Why the MGF matters

1. **It generates all moments** by differentiation — no messy summation
2. **It uniquely determines the distribution** — if two variables have the same
   MGF, they have the same distribution
3. **Sums become products**: if X and Y are independent,
   M_{X+Y}(t) = Mₓ(t) · M_y(t). This is how you prove that the sum of two
   independent Poisson variables is Poisson.

The MGF does not always exist (the Cauchy distribution has none), which is why
the characteristic function E(e^{itX}) is used in more advanced work.

---

## 📝 Practice problems

### Problem 1

A random variable X has the distribution:

| x | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| p(x) | 0.1 | 0.3 | 0.4 | k |

Find k, then E(X), E(X²), Var(X) and SD(X).

**Solution.**

- Step 1 — **Find k.** Probabilities must sum to 1:
  0.1 + 0.3 + 0.4 + k = 1, so **k = 0.2**

- Step 2 — build the table:

| x | p(x) | x·p(x) | x²·p(x) |
|---:|---:|---:|---:|
| 1 | 0.1 | 0.1 | 0.1 |
| 2 | 0.3 | 0.6 | 1.2 |
| 3 | 0.4 | 1.2 | 3.6 |
| 4 | 0.2 | 0.8 | 3.2 |
| **Σ** | **1.0** ✓ | **2.7** | **8.1** |

- Step 3 — E(X) = **2.7**
- Step 4 — E(X²) = **8.1**
- Step 5 — Var(X) = 8.1 − (2.7)² = 8.1 − 7.29 = **0.81**
- Step 6 — SD(X) = √0.81 = **0.9**

### Problem 2

If E(X) = 5 and Var(X) = 4, find E(3X + 2) and Var(3X + 2).

**Solution.**

- E(3X + 2) = 3·E(X) + 2 = 3(5) + 2 = **17**  *(linearity)*
- Var(3X + 2) = 3²·Var(X) = 9(4) = **36**  *(the +2 shifts, it does not spread)*

The constant vanishes from the variance because adding 2 to every value moves
the whole distribution without changing its width.

### Problem 3

A continuous random variable has PDF f(x) = 3x² for 0 ≤ x ≤ 1, and 0 elsewhere.
Verify it is a valid PDF, then find E(X) and P(X ≤ 0.5).

**Solution.**

- Step 1 — **Validity.** f(x) = 3x² ≥ 0 on [0,1] ✓ and
  ∫₀¹ 3x² dx = [x³]₀¹ = 1 − 0 = **1** ✓ — it is a valid PDF.

- Step 2 — **Expectation.**
  E(X) = ∫₀¹ x · 3x² dx = ∫₀¹ 3x³ dx = [3x⁴/4]₀¹ = **0.75**

- Step 3 — **Probability.**
  P(X ≤ 0.5) = ∫₀^0.5 3x² dx = [x³]₀^0.5 = 0.125 = **0.125**

Note the mean is 0.75, well right of the midpoint 0.5 — the density 3x² puts
far more weight near 1 than near 0.

---

## Exam questions from this unit

**Two marks**

1. Define a random variable and state its two types.
2. Why is P(X = a) = 0 for a continuous random variable?
3. State two properties of a CDF.
4. What is the relationship between a PDF and a CDF?
5. State the shortcut formula for variance.

**Five marks**

1. Explain PMF, PDF and CDF with examples of each.
2. State and explain the properties of expectation and variance.
3. Find the mean and variance of a given discrete distribution.
4. Explain moments and what the first four describe.

**Ten marks**

1. Explain random variables in full — types, PMF/PDF, CDF, expectation and
   variance — with worked examples.
2. Explain the moment-generating function, its properties, and use it to derive
   the mean and variance of the binomial distribution.

## Mistakes that cost marks

- Forgetting to check that probabilities sum to 1
- Treating f(x) as a probability rather than a density
- Using P(X = a) > 0 for a continuous variable
- Forgetting the square in Var(aX) = a²Var(X)
- Subtracting the constant in Var(X + b) — it has no effect
- Assuming E(XY) = E(X)E(Y) without independence
- Using E(X²) = [E(X)]² — they are equal only when the variance is zero
