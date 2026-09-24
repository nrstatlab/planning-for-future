# Unit 3 — Probability Distributions

**Syllabus topics:** Discrete distributions — Binomial, Poisson, Geometric,
Negative Binomial: definitions, properties and examples. Continuous
distributions — Uniform, Normal (Gaussian), Exponential, Gamma: definitions,
properties and applications. Joint, marginal and conditional distributions.
Introduction to the Central Limit Theorem.

---

## 3.0 Why distributions matter

### 🎯 The big idea

A probability distribution is a **ready-made pattern** for how a certain kind
of randomness behaves. Recognise which pattern fits your situation and every
probability you need is a formula away, instead of counting outcomes by hand.

### 📖 The story

You could work out the chance of getting exactly 7 heads in 10 coin tosses by
listing all 1,024 possible sequences and counting. Or you could notice that
this is a *fixed number of independent yes/no trials with a constant success
probability* — a binomial situation — and get the answer in one line.

The skill this unit tests is **recognising the pattern**. The formulas are on
the formula sheet; knowing which one applies is what earns the marks.

### The recognition table — learn this first

| Situation | Distribution |
|---|---|
| Fixed number of yes/no trials, count successes | **Binomial** |
| Count rare events in a fixed interval of time or space | **Poisson** |
| Trials until the **first** success | **Geometric** |
| Trials until the **rth** success | **Negative binomial** |
| Every value in a range equally likely | **Uniform** |
| Measurements clustering around an average, bell-shaped | **Normal** |
| Waiting time until the next event | **Exponential** |
| Waiting time until the rth event | **Gamma** |

---

# Part A — Discrete distributions

## 3.1 Binomial distribution

### 📖 The story

A basketball player makes 70% of her free throws. She takes 10. What is the
chance she makes exactly 8? Each throw is independent, has the same success
probability, and has only two outcomes. That is a binomial situation.

### The four conditions — all must hold

1. A **fixed** number of trials, n
2. Each trial has exactly **two** outcomes (success/failure)
3. Trials are **independent**
4. The success probability p is **constant** across trials

### 🔢 The formula

> **P(X = k) = ⁿCₖ · pᵏ · (1−p)ⁿ⁻ᵏ**

In plain English:
- n = number of trials
- k = number of successes you are asking about
- p = probability of success on one trial
- ⁿCₖ = n! / (k!(n−k)!) — the number of ways to arrange k successes among n trials

| | Formula |
|---|---|
| Mean | **μ = np** |
| Variance | **σ² = np(1−p)** |
| SD | σ = √(np(1−p)) |

**Worked example.** n = 10, p = 0.7, find P(X = 8).

- Step 1: ¹⁰C₈ = 10!/(8!·2!) = (10 × 9)/2 = **45**
- Step 2: p⁸ = 0.7⁸ = 0.05765
- Step 3: (1−p)² = 0.3² = 0.09
- Step 4: P = 45 × 0.05765 × 0.09 = **0.2335**

About a 23% chance. Mean = np = 7, so 8 is slightly above average — plausible,
and the arithmetic agrees.

Excel: `=BINOM.DIST(8, 10, 0.7, FALSE)`

## 3.2 Poisson distribution

### 📖 The story

A call centre receives about 3 calls per minute. What is the chance of exactly
5 calls in the next minute? There is no fixed number of "trials" here — a call
can arrive at any instant. You are counting **rare events in a fixed
interval**. That is Poisson.

### 🔢 The formula

> **P(X = k) = e^(−λ) · λᵏ / k!**

- λ (lambda) = the average number of events per interval
- k = the count you are asking about
- e ≈ 2.71828

| | Formula |
|---|---|
| Mean | **μ = λ** |
| Variance | **σ² = λ** |

### 💡 The "aha!" moment

**For a Poisson distribution the mean and the variance are equal.** No other
common distribution does this, so it is the signature to look for — and a
standard two-mark question.

**Worked example.** λ = 3, find P(X = 5).

- Step 1: e^(−3) = 0.049787
- Step 2: 3⁵ = 243
- Step 3: 5! = 120
- Step 4: P = 0.049787 × 243 / 120 = **0.1008**

### Poisson as a limit of the binomial

When n is **large** and p is **small**, with np = λ moderate, the binomial is
very well approximated by the Poisson. Rule of thumb: n ≥ 20 and p ≤ 0.05.

| k | Binomial(1000, 0.003) | Poisson(3) |
|---:|---:|---:|
| 0 | 0.049385 | 0.049787 |
| 1 | 0.148600 | 0.149361 |
| 2 | 0.223347 | 0.224042 |
| 3 | 0.223570 | 0.224042 |

Nearly identical — and the Poisson is far easier to compute, since ¹⁰⁰⁰C₃ is
unpleasant by hand. (These figures are computed in
`03_random_variables_distributions.py`.)

## 3.3 Geometric distribution

**The number of trials until the first success.**

> **P(X = k) = (1−p)^(k−1) · p**

You fail k−1 times, then succeed.

| | Formula |
|---|---|
| Mean | **μ = 1/p** |
| Variance | **σ² = (1−p)/p²** |

*Example.* Rolling a die until the first six: p = 1/6, so on average it takes
1/(1/6) = **6 rolls**. That matches intuition, which is a good sign.

P(first six on the 3rd roll) = (5/6)² × (1/6) = 25/216 = **0.1157**

**Memorylessness:** the geometric is the only *discrete* distribution with this
property. Having failed ten times does not improve your chances on the
eleventh — the die has no memory.

## 3.4 Negative binomial distribution

**The number of trials until the rth success** — the geometric generalised.

> **P(X = k) = ^(k−1)C_(r−1) · pʳ · (1−p)^(k−r)**

| | Formula |
|---|---|
| Mean | **μ = r/p** |
| Variance | **σ² = r(1−p)/p²** |

When r = 1 this reduces exactly to the geometric distribution.

*Example.* P(the 3rd six occurs on the 10th roll), p = 1/6:
⁹C₂ × (1/6)³ × (5/6)⁷ = 36 × 0.00463 × 0.2791 = **0.0465**

---

# Part B — Continuous distributions

## 3.5 Uniform distribution

Every value in [a, b] is equally likely.

> **f(x) = 1/(b−a) for a ≤ x ≤ b**

| | Formula |
|---|---|
| Mean | **μ = (a+b)/2** |
| Variance | **σ² = (b−a)²/12** |

The density is a flat rectangle of height 1/(b−a) and width (b−a) — so its area
is exactly 1, as every PDF's must be.

*Example.* A bus arrives uniformly between 0 and 20 minutes from now. Expected
wait = 10 minutes. P(waiting less than 5) = 5/20 = **0.25**.

## 3.6 Normal (Gaussian) distribution

**The most important distribution in statistics.**

### 📖 The story

Measure the heights of a thousand students. A few are very short, a few very
tall, and most cluster near the average, tapering off symmetrically in both
directions. Plot it and you get the bell curve. Heights, weights, measurement
errors, exam scores, blood pressure — an enormous range of natural quantities
follow this shape, and Section 3.9 explains why.

### 🔢 The formula

> **f(x) = (1 / (σ√(2π))) · e^(−(x−μ)²/(2σ²))**

You will rarely use this directly — you use tables or software. What you must
know is its **properties**:

1. **Bell-shaped and symmetric** about μ
2. **Mean = median = mode = μ**
3. Total area under the curve = 1
4. Defined for all real x; the curve approaches but never touches the axis
5. Completely determined by just two parameters, **μ and σ**
6. **Points of inflection** at μ ± σ

### The empirical rule — 68-95-99.7

| Interval | Contains |
|---|---|
| μ ± 1σ | **68.27%** of the data |
| μ ± 2σ | **95.45%** |
| μ ± 3σ | **99.73%** |

Worth committing to memory: it lets you sanity-check any normal calculation in
seconds.

### Standardisation — the z-score

Every normal distribution can be converted to the **standard normal**
(μ = 0, σ = 1):

> **z = (x − μ) / σ**

A z-score says **how many standard deviations from the mean** a value lies.
z = 2 means "two standard deviations above average", regardless of the original
units. That is what makes different scales comparable.

**Worked example.** IQ scores are Normal(100, 15).

- P(X ≤ 115): z = (115 − 100)/15 = 1.00, so P = **0.8413**
- P(X > 130): z = 2.00, so P = 1 − 0.9772 = **0.0228**
- P(85 ≤ X ≤ 115): z from −1 to +1, so P = 0.8413 − 0.1587 = **0.6827** ✓
  (matching the empirical rule)

**Critical values worth memorising:**

| Confidence | z |
|---|---|
| 90% | 1.645 |
| 95% | **1.96** |
| 99% | 2.576 |

Excel: `=NORM.DIST(x, mean, sd, TRUE)` for the CDF, `=NORM.INV(p, mean, sd)`
for the inverse.

## 3.7 Exponential distribution

**The waiting time until the next event**, when events occur at a constant
average rate λ. It is the continuous partner of the Poisson: if events per hour
are Poisson(λ), the gap between events is Exponential(λ).

> **f(x) = λe^(−λx) for x ≥ 0**
> **F(x) = 1 − e^(−λx)**

| | Formula |
|---|---|
| Mean | **μ = 1/λ** |
| Variance | **σ² = 1/λ²** |

*Example.* Buses arrive at 0.5 per minute (λ = 0.5). Mean wait = 1/0.5 = 2
minutes. P(waiting more than 3 minutes) = e^(−0.5 × 3) = e^(−1.5) = **0.2231**.

### 💡 Memorylessness

> **P(X > s + t | X > s) = P(X > t)**

You have already waited 2 minutes. The probability of waiting 3 more is exactly
the same as it was at the start. The bus does not "become due".

The exponential is the **only** continuous distribution with this property, and
it is a favourite exam question. It is also why it models the lifetime of
components that fail randomly rather than by wearing out — a fuse, not a tyre.

## 3.8 Gamma distribution

**The waiting time until the rth event.** The exponential generalised, exactly
as the negative binomial generalises the geometric.

> **f(x) = (λ^α / Γ(α)) · x^(α−1) · e^(−λx) for x > 0**

| | Formula |
|---|---|
| Mean | **μ = α/λ** |
| Variance | **σ² = α/λ²** |

Special cases worth naming:
- **α = 1** → the exponential distribution
- **λ = 1/2, α = k/2** → the **chi-square** distribution with k degrees of
  freedom, which you meet again in Unit 5

**The Γ function** extends factorials to non-integers: Γ(n) = (n−1)! for
positive integers, and Γ(1/2) = √π.

### The four-way symmetry — a good exam observation

| | One event | r events |
|---|---|---|
| **Discrete** (count trials) | Geometric | Negative binomial |
| **Continuous** (measure time) | Exponential | Gamma |

## 3.9 Joint, marginal and conditional distributions

When two random variables are considered together.

**Joint distribution:** p(x, y) = P(X = x and Y = y)

**Marginal distribution:** sum out the other variable —
p(x) = Σ_y p(x, y). It is called "marginal" because it was traditionally
written in the margins of the joint table.

**Conditional distribution:** p(y|x) = p(x, y) / p(x)

**Independence:** X and Y are independent when
**p(x, y) = p(x) × p(y)** for every pair.

**Worked example.**

| | Y=0 | Y=1 | **Marginal of X** |
|---|---:|---:|---:|
| **X=0** | 0.2 | 0.3 | **0.5** |
| **X=1** | 0.1 | 0.4 | **0.5** |
| **Marginal of Y** | **0.3** | **0.7** | **1.0** ✓ |

- P(X=0) = 0.2 + 0.3 = 0.5 (the row total)
- P(Y=1 | X=0) = 0.3 / 0.5 = 0.6
- **Independent?** P(X=0)×P(Y=0) = 0.5 × 0.3 = 0.15, but the joint
  probability is 0.2. Since 0.15 ≠ 0.20, they are **not independent**.

## 3.10 The Central Limit Theorem

### 🎯 The big idea

Take samples of reasonable size from **any** population, whatever its shape,
and the distribution of the sample means will be approximately **normal**.

### 📖 The story

Roll one die: every outcome from 1 to 6 is equally likely — a flat, uniform
distribution, nothing bell-shaped about it. Now roll thirty dice and record the
average. Do that many times and plot the averages. You get a bell curve.

The population was uniform. The distribution of **averages** is normal. That is
the Central Limit Theorem, and it is the reason the normal distribution appears
everywhere in nature: most measurable quantities are the sum of many small
independent influences.

### 🔢 Formally

For a population with mean μ and standard deviation σ, the sampling
distribution of the mean x̄ for sample size n has:

> **Mean of x̄ = μ**
> **SD of x̄ = σ/√n**  — this is the **standard error**
> **Shape → normal as n grows**, whatever the population's shape

**Rule of thumb: n ≥ 30** is enough for most populations. A population that is
already normal gives a normal sampling distribution at any n.

### 💡 Why this is the most important theorem in the course

It is what makes inference possible. You take **one** sample, and the CLT tells
you how the mean of that sample behaves relative to the population mean — so
you can build a confidence interval or run a hypothesis test. Every technique
in Unit 5 rests on it.

Notice too that the standard error is σ/**√n**, not σ/n. **To halve your
uncertainty you need four times the data.** That single fact governs the cost
of every survey and experiment ever run.

**Worked example.** A population has μ = 100, σ = 20. For samples of n = 25:

- Mean of x̄ = 100
- Standard error = 20/√25 = 20/5 = **4**
- P(x̄ > 108): z = (108 − 100)/4 = 2.00 → P = 1 − 0.9772 = **0.0228**

---

## 📝 Practice problems

### Problem 1

A factory's items are 5% defective. In a random sample of 20, find the
probability that (a) exactly 2 are defective, (b) at most 1 is defective.
Also find the mean and variance.

**Solution.** Binomial with n = 20, p = 0.05.

(a) P(X = 2) = ²⁰C₂ × 0.05² × 0.95¹⁸
- ²⁰C₂ = (20 × 19)/2 = 190
- 0.05² = 0.0025
- 0.95¹⁸ = 0.39721
- P = 190 × 0.0025 × 0.39721 = **0.1887**

(b) P(X ≤ 1) = P(0) + P(1)
- P(0) = 0.95²⁰ = 0.35849
- P(1) = 20 × 0.05 × 0.95¹⁹ = 20 × 0.05 × 0.37735 = 0.37735
- P(X ≤ 1) = **0.7358**

Mean = np = 20 × 0.05 = **1.0**; Variance = np(1−p) = 1 × 0.95 = **0.95**

*(Since n is largish and p small, Poisson(λ = 1) gives P(X=2) = 0.1839 — close
to 0.1887, as expected.)*

### Problem 2

Heights are normally distributed with mean 165 cm and standard deviation 8 cm.
Find (a) P(height > 175), (b) P(160 < height < 170), (c) the height exceeded by
only 5% of people.

**Solution.**

(a) z = (175 − 165)/8 = 1.25
P(Z > 1.25) = 1 − 0.8944 = **0.1056**, about 10.6%

(b) z₁ = (160 − 165)/8 = −0.625; z₂ = (170 − 165)/8 = 0.625
P = 0.7340 − 0.2660 = **0.4680**, about 46.8%

(c) The 95th percentile has z = 1.645
x = μ + zσ = 165 + 1.645(8) = 165 + 13.16 = **178.16 cm**

### Problem 3

A website receives 4 visitors per minute on average. Find the probability of
(a) exactly 6 visitors in a minute, (b) no visitors in a minute, (c) more than
2 visitors.

**Solution.** Poisson with λ = 4.

(a) P(X=6) = e^(−4) × 4⁶ / 6! = 0.018316 × 4096 / 720 = **0.1042**

(b) P(X=0) = e^(−4) × 4⁰ / 0! = **0.0183**

(c) P(X > 2) = 1 − [P(0) + P(1) + P(2)]
- P(0) = 0.018316
- P(1) = 0.018316 × 4 = 0.073263
- P(2) = 0.018316 × 16/2 = 0.146525
- Sum = 0.238104
- P(X > 2) = 1 − 0.238104 = **0.7619**

Using the complement is far quicker than summing P(3), P(4), P(5), … to
infinity. Always look for that shortcut on "more than" questions.

---

## Exam questions from this unit

**Two marks**

1. State the conditions for a binomial distribution.
2. What is special about the mean and variance of a Poisson distribution?
3. State the empirical rule for the normal distribution.
4. Define a z-score.
5. Which distributions have the memoryless property?

**Five marks**

1. Explain the binomial distribution with its mean, variance and an example.
2. Explain the normal distribution and its properties.
3. Explain the relationship between binomial and Poisson with an example.
4. State the Central Limit Theorem and explain its significance.
5. Explain joint, marginal and conditional distributions with a table.

**Ten marks**

1. Explain the discrete probability distributions — binomial, Poisson,
   geometric and negative binomial — with formulas, moments and examples.
2. Explain the continuous distributions — uniform, normal, exponential and
   gamma — with their properties and applications.

## Mistakes that cost marks

- Using the binomial when there is no fixed number of trials
- Forgetting the ⁿCₖ term in the binomial formula
- Using λ per the wrong interval (per hour when the question asks per minute)
- Forgetting to subtract from 1 for "greater than" normal probabilities
- Dividing by σ² instead of σ when computing a z-score
- Using σ instead of σ/√n for a sampling distribution — the commonest CLT error
- Assuming two variables are independent without checking p(x,y) = p(x)p(y)
