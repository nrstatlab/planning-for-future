# Unit 5 — Statistical Inference, Estimation and Hypothesis Testing

**Syllabus topics:** Population and sample, parameters and statistics.
Sampling distributions. Point and interval estimation (confidence intervals).
Tests of significance — z-test, t-test, chi-square test and F-test. p-values
and errors (Type I and II). Power of a statistical test.

---

## 5.1 Population, sample, parameter, statistic

### 🎯 The big idea

You almost never measure everyone. You measure a few and reason about the rest.
Statistical inference is the discipline of doing that reasoning honestly, with
a stated degree of uncertainty.

### 📖 The story

A company claims its packets contain 500 g of rice. You cannot open every
packet in the country. So you weigh 40 of them, find an average of 496 g, and
ask: is the company lying, or is 496 just the sort of thing that happens when
you weigh only 40 packets? That question — and the machinery for answering it —
is this entire unit.

### The four terms

| Term | Meaning | Notation |
|---|---|---|
| **Population** | Every member of the group of interest | size N |
| **Sample** | The subset actually measured | size n |
| **Parameter** | A number describing the **population** | μ, σ, P |
| **Statistic** | A number computed from the **sample** | x̄, s, p̂ |

**Greek letters for parameters, Roman letters for statistics.** The parameter
is fixed but unknown; the statistic is known but varies from sample to sample.
Inference uses the second to estimate the first.

## 5.2 Sampling distributions

If you take many samples of the same size and compute the mean of each, those
means form their own distribution — the **sampling distribution of the mean**.

From the Central Limit Theorem (Unit 3):

> **Mean of x̄ = μ**
> **Standard error = σ/√n**
> **Shape → normal as n grows**

**The standard error is not the standard deviation.**

| | Standard deviation (σ or s) | Standard error (σ/√n) |
|---|---|---|
| Describes | Spread of individual values | Spread of **sample means** |
| Depends on n? | No | **Yes — shrinks as √n** |
| Used for | Describing data | Inference |

Confusing them is one of the most common errors in this unit. The standard
error is always the smaller of the two (for n > 1), and it is what appears in
every confidence interval and test statistic below.

## 5.3 Estimation

### Point estimation

A **single number** as the best guess for a parameter: x̄ estimates μ, s
estimates σ, p̂ estimates P.

Properties of a good estimator:

| Property | Meaning |
|---|---|
| **Unbiased** | Its expected value equals the parameter: E(x̄) = μ |
| **Consistent** | It converges to the parameter as n grows |
| **Efficient** | It has the smallest variance among unbiased estimators |
| **Sufficient** | It uses all the relevant information in the sample |

*(This is why the sample variance divides by n−1: doing so makes it unbiased.
See Unit 1.)*

The flaw of a point estimate is that it is almost certainly not exactly right,
and it says nothing about how far off it might be.

### Interval estimation — confidence intervals

> **Estimate ± (critical value × standard error)**

**When σ is known** (or n is large):

> **x̄ ± z(α/2) · σ/√n**

**When σ is unknown** (the usual case):

> **x̄ ± t(α/2, n−1) · s/√n**

**Critical values worth memorising:**

| Confidence | α | z(α/2) |
|---|---|---|
| 90% | 0.10 | 1.645 |
| **95%** | **0.05** | **1.96** |
| 99% | 0.01 | 2.576 |

**Worked example.** n = 25, x̄ = 68, s = 5. Build a 95% confidence interval.

- Step 1: σ is unknown, so use t with df = 25 − 1 = **24**
- Step 2: t(0.025, 24) = **2.064**
- Step 3: standard error = 5/√25 = 5/5 = **1.0**
- Step 4: margin of error = 2.064 × 1.0 = **2.064**
- Step 5: interval = 68 ± 2.064 = **(65.94, 70.06)**

### 💡 What "95% confident" actually means

> If we repeated this sampling procedure many times and built an interval each
> time, about **95% of those intervals** would contain the true population
> mean.

It does **not** mean "there is a 95% probability that μ lies in this
particular interval". The true mean is a fixed number, not a random one — it is
either in this interval or it is not. What is random is the interval, not μ.

Stating this correctly is worth marks; stating it the wrong way loses them.

**Two behaviours to note and explain:**

- **Higher confidence → wider interval.** Certainty costs precision. A 100%
  confidence interval would be (−∞, +∞) and tell you nothing.
- **Larger n → narrower interval**, in proportion to 1/√n. To halve the width
  you need **four times** the data.

## 5.4 Hypothesis testing — the procedure

Follow these six steps every single time. Marks are given for each.

1. **State H₀ and H₁** — in symbols and in words
2. **Choose α** — usually 0.05
3. **Compute the test statistic**
4. **Find the p-value**, or compare with the critical value
5. **Decide** — p < α means reject H₀
6. **Conclude in the words of the original problem**

### The two hypotheses

| | Null H₀ | Alternative H₁ |
|---|---|---|
| Says | No effect, no difference | There is an effect |
| Contains | Always `=` | `≠`, `<` or `>` |
| Status | Assumed true until evidence says otherwise | What you are trying to show |

**The courtroom analogy:** H₀ is "innocent". You do not prove innocence; you
either find enough evidence to reject it or you do not. **"Fail to reject H₀"
is not "accept H₀"** — a jury returns "not guilty", never "innocent". Writing
"accept H₀" is a standard mark deduction.

### One-tailed vs two-tailed

| | Two-tailed | One-tailed |
|---|---|---|
| H₁ | μ ≠ μ₀ | μ > μ₀ or μ < μ₀ |
| Question | "Is it different?" | "Is it bigger?" / "Is it smaller?" |
| α split | α/2 in each tail | all α in one tail |
| z at α = 0.05 | ±1.96 | 1.645 |

Decide the direction **before** seeing the data. Choosing a one-tailed test
after looking at which way the result went is a form of cheating.

### The p-value

> **The p-value is the probability of observing a result at least as extreme as
> the one you got, assuming H₀ is true.**

A small p-value means your data would be surprising if H₀ were true — so H₀ is
doubtful.

| p-value | Reading |
|---|---|
| p < 0.01 | Very strong evidence against H₀ |
| p < 0.05 | Strong evidence against H₀ |
| 0.05 < p < 0.10 | Weak evidence |
| p > 0.10 | Little or no evidence against H₀ |

**What a p-value is not:** it is *not* the probability that H₀ is true, and
*not* the probability that your result happened by chance. Those
misinterpretations are examined precisely because they are so common.

## 5.5 The four tests

### The decision tree

1. Comparing one mean to a known value, σ known or n > 30 → **z-test**
2. Comparing one mean to a known value, σ unknown and n small → **one-sample t-test**
3. Comparing two group means → **two-sample t-test**
4. Same subjects measured twice → **paired t-test**
5. Two categorical variables → **chi-square test of independence**
6. Comparing two variances → **F-test**
7. Comparing three or more means → **ANOVA** *(uses F; beyond this syllabus)*

### z-test

**Use when:** σ is known, or n > 30.

> **z = (x̄ − μ₀) / (σ/√n)**

**Worked example.** Packets should average 70 g with a known σ of 3 g. A sample
of 40 averages 71.2 g. Test at α = 0.05.

- Step 1: H₀: μ = 70; H₁: μ ≠ 70 (two-tailed)
- Step 2: α = 0.05, so critical values are ±1.96
- Step 3: standard error = 3/√40 = 3/6.325 = 0.4743
- Step 4: z = (71.2 − 70)/0.4743 = **2.5298**
- Step 5: |2.53| > 1.96, and p = **0.0114** < 0.05 → **reject H₀**
- Step 6: **Conclusion:** the mean fill weight differs significantly from 70 g.

### t-test

**Use when:** σ is unknown (the normal situation).

**One-sample:**
> **t = (x̄ − μ₀) / (s/√n)**, df = n − 1

**Two-sample, equal variances (pooled):**
> **t = (x̄₁ − x̄₂) / √(s²ₚ(1/n₁ + 1/n₂))**, df = n₁ + n₂ − 2
>
> where **s²ₚ = [(n₁−1)s₁² + (n₂−1)s₂²] / (n₁ + n₂ − 2)**

**Paired:**
> **t = d̄ / (s_d/√n)**, df = n − 1, where d is the difference within each pair

**Worked example (two-sample).** Two teaching methods:

- Group A: n = 10, mean 81.20, variance 17.0667
- Group B: n = 10, mean 73.50, variance 9.1667

- Step 1: H₀: μ_A = μ_B; H₁: μ_A ≠ μ_B
- Step 2: α = 0.05
- Step 3: pooled variance = [9(17.0667) + 9(9.1667)]/18 = **13.1167**
- Step 4: standard error = √(13.1167 × (1/10 + 1/10)) = √2.6233 = **1.6197**
- Step 5: t = (81.20 − 73.50)/1.6197 = 7.70/1.6197 = **4.7541** on df = 18
- Step 6: p = **0.000159** < 0.05 → **reject H₀**
- Conclusion: the two methods differ significantly in mean score.

**Why t and not z?** The t distribution has heavier tails, accounting for the
extra uncertainty in estimating σ from the sample. As n grows, t approaches z —
by df = 30 they are nearly identical, which is where the "n > 30" rule of thumb
comes from.

### Chi-square test

Two uses. Both compare **observed** counts with **expected** counts.

> **χ² = Σ (O − E)² / E**

**Test of independence:** are two categorical variables related?
- **E = (row total × column total) / grand total**
- **df = (rows − 1)(columns − 1)**

**Goodness of fit:** does the data follow a claimed distribution?
- df = categories − 1

**Worked example.** Is region related to purchase type?

| Region | Premium (O) | Standard (O) | Total |
|---|---:|---:|---:|
| North | 30 | 70 | 100 |
| South | 45 | 55 | 100 |
| East | 25 | 75 | 100 |
| **Total** | **100** | **200** | **300** |

- Step 1: H₀: region and purchase type are independent
- Step 2: expected = (100 × 100)/300 = **33.33** for each Premium cell,
  (100 × 200)/300 = **66.67** for each Standard cell
- Step 3: χ² = (30−33.33)²/33.33 + (70−66.67)²/66.67 + (45−33.33)²/33.33
  + (55−66.67)²/66.67 + (25−33.33)²/33.33 + (75−66.67)²/66.67 = **9.75**
- Step 4: df = (3−1)(2−1) = **2**; critical value at α = 0.05 is **5.991**
- Step 5: 9.75 > 5.991, p = **0.0076** → **reject H₀**
- Step 6: **Conclusion:** region and purchase type are associated.

**Assumption:** every expected frequency should be **at least 5**. State that
you checked it — here the smallest expected value is 33.33, so it holds.

Chi-square is always **right-tailed**: a large χ² means observed and expected
differ a lot, which is the evidence against H₀.

### F-test

**Use when:** comparing two variances — often to check the equal-variance
assumption of the pooled t-test.

> **F = s₁² / s₂²**, with the **larger variance on top**
> df = (n₁ − 1, n₂ − 1)

**Worked example**, using the two groups above:

- Step 1: H₀: σ²_A = σ²_B
- Step 2: F = 17.0667 / 9.1667 = **1.8618** on df = (9, 9)
- Step 3: two-tailed p = **0.3682** > 0.05 → **fail to reject H₀**
- Step 4: **Conclusion:** the variances are not significantly different, so the
  pooled t-test above was appropriate.

Putting the larger variance on top makes F ≥ 1 and lets you use the standard
right-tail tables.

*(All of these worked figures are computed in
`05_inference_hypothesis_tests.py`.)*

## 5.6 Type I and Type II errors

| | H₀ is **true** | H₀ is **false** |
|---|---|---|
| **Reject H₀** | **Type I error** (probability α) | Correct — **power** (1 − β) |
| **Fail to reject H₀** | Correct (1 − α) | **Type II error** (probability β) |

**In the courtroom analogy:**
- **Type I** — convicting an innocent person (a false positive)
- **Type II** — acquitting a guilty one (a false negative)

**α is chosen by you.** Setting α = 0.05 says you accept a 5% chance of
rejecting a true H₀.

**β follows from the design** — the sample size, the effect size and α
together determine it.

### The trade-off

Lower α → fewer Type I errors, but **more** Type II errors. Tighten the
standard of proof and more guilty people go free.

**The only way to reduce both at once is to increase n.**

Which error matters more depends on the context:
- Testing a new drug for harmful side effects: a Type II error (missing the
  harm) is far worse
- Convicting someone of a crime: a Type I error is the one the legal system is
  built to avoid

### Power

> **Power = 1 − β = P(rejecting H₀ when it is genuinely false)**

The probability of detecting a real effect. Conventionally, aim for **0.80**.

**Power increases when:**

| Factor | Effect on power |
|---|---|
| Larger sample size n | ↑ |
| Larger true effect size | ↑ |
| Smaller population variance | ↑ |
| Larger α (e.g. 0.10 instead of 0.01) | ↑ (but more Type I errors) |
| One-tailed instead of two-tailed | ↑ (only if the direction is right) |

A **power analysis** before collecting data tells you what sample size you
need. Running an underpowered study wastes everyone's time: it will probably
fail to detect a real effect, and you will not know whether the effect was
absent or merely invisible.

---

## 📝 Practice problems

### Problem 1

A sample of 36 students has mean height 168 cm with sample standard deviation
6 cm. Construct a 95% confidence interval for the population mean height.

**Solution.**

- Step 1: n = 36, x̄ = 168, s = 6. σ is unknown, but n = 36 > 30, so z is an
  acceptable approximation. (Using t with df = 35 gives 2.030 instead of 1.96 —
  practically the same.)
- Step 2: z(0.025) = **1.96**
- Step 3: standard error = 6/√36 = 6/6 = **1.0**
- Step 4: margin = 1.96 × 1.0 = **1.96**
- Step 5: CI = 168 ± 1.96 = **(166.04, 169.96)**

**Interpretation:** if we repeated this sampling many times, about 95% of the
intervals so constructed would contain the true mean height.

### Problem 2

A machine is supposed to fill bottles with 500 ml. A sample of 25 bottles gives
a mean of 495 ml with a sample standard deviation of 8 ml. Test at α = 0.05
whether the machine is under-filling.

**Solution.**

- Step 1 — **Hypotheses.** This asks specifically about *under*-filling, so it
  is one-tailed:
  - H₀: μ = 500 (the machine fills correctly)
  - H₁: μ < 500 (the machine under-fills)

- Step 2 — **Significance level.** α = 0.05, one-tailed.

- Step 3 — **Test statistic.** σ is unknown and n = 25 is small, so use t with
  df = 24:
  - standard error = 8/√25 = 8/5 = **1.6**
  - t = (495 − 500)/1.6 = −5/1.6 = **−3.125**

- Step 4 — **Critical value.** t(0.05, 24) one-tailed = **−1.711**

- Step 5 — **Decision.** −3.125 < −1.711, so **reject H₀**. (p ≈ 0.0023.)

- Step 6 — **Conclusion.** There is strong evidence that the machine is
  under-filling bottles. The mean fill is significantly below 500 ml.

### Problem 3

A survey of 200 people asks whether they prefer tea or coffee, split by gender.
Test at α = 0.05 whether preference is independent of gender.

| | Tea | Coffee | Total |
|---|---:|---:|---:|
| Male | 40 | 60 | 100 |
| Female | 60 | 40 | 100 |
| **Total** | **100** | **100** | **200** |

**Solution.**

- Step 1 — **Hypotheses.**
  - H₀: preference is independent of gender
  - H₁: preference depends on gender

- Step 2 — **Expected frequencies.** E = (row × column)/grand total:
  every cell = (100 × 100)/200 = **50**

| | Tea (O, E) | Coffee (O, E) |
|---|---|---|
| Male | 40, 50 | 60, 50 |
| Female | 60, 50 | 40, 50 |

  All expected frequencies are 50 ≥ 5 ✓

- Step 3 — **Test statistic.**
  - χ² = (40−50)²/50 + (60−50)²/50 + (60−50)²/50 + (40−50)²/50
  - = 100/50 + 100/50 + 100/50 + 100/50
  - = 2 + 2 + 2 + 2 = **8.0**

- Step 4 — **Critical value.** df = (2−1)(2−1) = **1**;
  χ²(0.05, 1) = **3.841**

- Step 5 — **Decision.** 8.0 > 3.841, so **reject H₀**. (p ≈ 0.0047.)

- Step 6 — **Conclusion.** Beverage preference is significantly associated with
  gender. Men in this sample favoured coffee and women favoured tea, by more
  than chance would explain.

---

## Exam questions from this unit

**Two marks**

1. Distinguish a parameter from a statistic.
2. What is the standard error, and how does it differ from the standard deviation?
3. Define a Type I and a Type II error.
4. What is the power of a test?
5. State the correct interpretation of a 95% confidence interval.
6. When do you use a t-test rather than a z-test?

**Five marks**

1. Explain the steps of hypothesis testing.
2. Construct a confidence interval for given sample data and interpret it.
3. Explain Type I and Type II errors with the error table and the trade-off.
4. Explain the chi-square test of independence with a worked example.
5. Explain point and interval estimation, and the properties of a good
   estimator.

**Ten marks**

1. Explain hypothesis testing in full — hypotheses, significance level, test
   statistics, p-values, errors and power — with a worked example.
2. Explain the four tests of significance (z, t, chi-square, F) with their
   conditions, formulas and examples.

## Mistakes that cost marks

- Writing "accept H₀" instead of "fail to reject H₀"
- Using σ instead of σ/√n in a test statistic
- Using z when σ is unknown and n is small
- Forgetting to halve α for a two-tailed test
- Using the wrong degrees of freedom — n−1, n₁+n₂−2, or (r−1)(c−1)
- Choosing a one-tailed test after seeing which way the data went
- Interpreting the p-value as the probability that H₀ is true
- Forgetting to check that expected frequencies are at least 5 for chi-square
- Stopping at the decision without stating a conclusion in context
