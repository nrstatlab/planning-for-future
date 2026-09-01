# Course 4 — Practice Problems with Solutions

Mixed problems across all five units, in the order an exam paper would ask
them. Work each one fully before reading the solution — statistics is the one
subject where reading a solution feels like understanding and is not.

Every numeric answer here has been checked against
`statlib.py`.

---

## Section A — Two-mark questions

**1. State the three axioms of probability.**

P(A) ≥ 0 for every event; P(S) = 1 for the sample space S; and for mutually
exclusive A and B, P(A ∪ B) = P(A) + P(B).

**2. When would you report the median rather than the mean?**

When the data is skewed or contains outliers. The mean is dragged by extreme
values; the median is not. This is why incomes and house prices are quoted as
medians.

**3. Why does the sample variance divide by n − 1?**

Deviations are measured from the sample's own mean, which sits in the middle of
the sample by construction, so they understate the true deviations from the
population mean. Dividing by n − 1 corrects that bias — Bessel's correction.

**4. What is special about the Poisson distribution's moments?**

Its mean and variance are both equal to λ. No other common distribution has
this property, so it is the signature to look for.

**5. State the correct interpretation of a 95% confidence interval.**

If the sampling procedure were repeated many times and an interval built each
time, about 95% of those intervals would contain the true population mean. It
is *not* a 95% probability that this particular interval contains it — the
population mean is fixed, not random.

**6. Distinguish a Type I from a Type II error.**

Type I is rejecting a true H₀ (a false positive, probability α). Type II is
failing to reject a false H₀ (a false negative, probability β).

**7. What does R² measure, and what is its relationship to r?**

The proportion of variance in y explained by the model. For **simple** linear
regression R² = r²; this does not hold for multiple regression.

**8. Why is the magnitude of a covariance not interpretable?**

It depends on the units of both variables. Changing height from metres to
centimetres multiplies the covariance by 100 though nothing about the
relationship changed. Correlation standardises this away.

---

## Section B — Five-mark problems

### Problem 1 — Descriptive statistics

The daily sales (in thousands) of a shop over 10 days were:
12, 15, 18, 22, 15, 20, 25, 18, 15, 20

Find the mean, median, mode, range, sample variance, sample standard deviation
and the coefficient of variation.

**Solution.**

- **Step 1 — Mean.** Sum = 12+15+18+22+15+20+25+18+15+20 = **180**;
  n = 10; x̄ = 180/10 = **18.0**

- **Step 2 — Median.** Sorted: 12, 15, 15, 15, 18, **18**, 20, 20, 22, 25.
  n is even, so average the 5th and 6th: (18 + 18)/2 = **18.0**

- **Step 3 — Mode.** 15 appears three times, more than any other value.
  Mode = **15**

- **Step 4 — Range.** 25 − 12 = **13**

- **Step 5 — Variance.**

| xᵢ | xᵢ − 18 | (xᵢ − 18)² |
|---:|---:|---:|
| 12 | −6 | 36 |
| 15 | −3 | 9 |
| 18 | 0 | 0 |
| 22 | 4 | 16 |
| 15 | −3 | 9 |
| 20 | 2 | 4 |
| 25 | 7 | 49 |
| 18 | 0 | 0 |
| 15 | −3 | 9 |
| 20 | 2 | 4 |
| **Σ** | **0** ✓ | **136** |

  s² = 136 / (10 − 1) = 136/9 = **15.11**

- **Step 6 — Standard deviation.** s = √15.11 = **3.888**

- **Step 7 — Coefficient of variation.** CV = (3.888/18.0) × 100 = **21.6%**

Note that mean = median = 18 while the mode is 15 — the distribution is close
to symmetric, with a slight cluster at the lower end.

### Problem 2 — Binomial

A multiple-choice test has 12 questions, each with 4 options. A student guesses
every answer. Find the probability of (a) exactly 5 correct, (b) at most 2
correct, and (c) the mean and variance of the number correct.

**Solution.** Binomial with n = 12, p = 1/4 = 0.25.

- **(a)** P(X = 5) = ¹²C₅ × 0.25⁵ × 0.75⁷
  - ¹²C₅ = 792
  - 0.25⁵ = 0.0009766
  - 0.75⁷ = 0.1334839
  - P = 792 × 0.0009766 × 0.1334839 = **0.1032**

- **(b)** P(X ≤ 2) = P(0) + P(1) + P(2)
  - P(0) = 0.75¹² = 0.031676
  - P(1) = 12 × 0.25 × 0.75¹¹ = 0.126705
  - P(2) = 66 × 0.0625 × 0.75¹⁰ = 0.232292
  - P(X ≤ 2) = **0.3907**

- **(c)** Mean = np = 12 × 0.25 = **3.0**;
  Variance = np(1−p) = 12 × 0.25 × 0.75 = **2.25**

So a guesser expects 3 right out of 12, and has about a 39% chance of getting
2 or fewer.

### Problem 3 — Normal distribution

The lifetime of a bulb is normally distributed with mean 1200 hours and
standard deviation 150 hours. Find (a) P(lifetime > 1400), (b) P(1000 <
lifetime < 1300), and (c) the lifetime below which 10% of bulbs fail.

**Solution.**

- **(a)** z = (1400 − 1200)/150 = 200/150 = **1.3333**
  P(Z > 1.3333) = 1 − 0.9088 = **0.0912**, about 9.1%

- **(b)** z₁ = (1000 − 1200)/150 = **−1.3333**;
  z₂ = (1300 − 1200)/150 = **0.6667**
  P = 0.7475 − 0.0912 = **0.6563**, about 65.6%

- **(c)** The 10th percentile has z = **−1.2816**
  x = μ + zσ = 1200 + (−1.2816)(150) = 1200 − 192.2 = **1007.8 hours**

So 10% of bulbs fail before about 1008 hours.

### Problem 4 — Correlation

Compute Pearson's r for the following and interpret it.

| Advertising (₹ lakh) | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|
| Sales (₹ lakh) | 15 | 25 | 30 | 42 | 48 |

**Solution.**

- **Step 1.** x̄ = 30/5 = **6**; ȳ = 160/5 = **32**

- **Step 2.**

| x | y | x−x̄ | y−ȳ | (x−x̄)(y−ȳ) | (x−x̄)² | (y−ȳ)² |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 15 | −4 | −17 | 68 | 16 | 289 |
| 4 | 25 | −2 | −7 | 14 | 4 | 49 |
| 6 | 30 | 0 | −2 | 0 | 0 | 4 |
| 8 | 42 | 2 | 10 | 20 | 4 | 100 |
| 10 | 48 | 4 | 16 | 64 | 16 | 256 |
| | | **0** ✓ | **0** ✓ | **166** | **40** | **698** |

- **Step 3.** r = 166 / √(40 × 698) = 166 / √27920 = 166 / 167.09 = **0.9935**

**Interpretation:** a very strong positive linear relationship — as advertising
spend rises, sales rise almost proportionally. This does **not** prove that
advertising causes the sales; both could be driven by seasonal demand.

---

## Section C — Ten-mark problems

### Problem 5 — Full regression analysis

Using the advertising data from Problem 4:
(a) fit the regression line, (b) predict sales for ₹7 lakh of advertising,
(c) compute R², (d) construct the ANOVA table, (e) test whether the slope is
significantly different from zero at α = 0.05.

**Solution.**

**(a) The regression line.**

- b₁ = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)² = 166/40 = **4.15**
- b₀ = ȳ − b₁x̄ = 32 − 4.15(6) = 32 − 24.9 = **7.1**
- **ŷ = 7.1 + 4.15x**

*Interpretation:* each additional ₹1 lakh of advertising is associated with
about ₹4.15 lakh more sales. The intercept of 7.1 suggests ₹7.1 lakh of sales
with no advertising — but x = 0 is outside the observed range of 2 to 10, so
treat it cautiously.

**(b) Prediction at x = 7.**

ŷ = 7.1 + 4.15(7) = 7.1 + 29.05 = **₹36.15 lakh**

x = 7 lies inside the observed range, so this is interpolation and is
reasonably safe.

**(c) Residuals and R².**

| x | y | ŷ = 7.1 + 4.15x | e = y − ŷ | e² |
|---:|---:|---:|---:|---:|
| 2 | 15 | 15.40 | −0.40 | 0.160 |
| 4 | 25 | 23.70 | 1.30 | 1.690 |
| 6 | 30 | 32.00 | −2.00 | 4.000 |
| 8 | 42 | 40.30 | 1.70 | 2.890 |
| 10 | 48 | 48.60 | −0.60 | 0.360 |
| | | | **0.00** ✓ | **9.10** |

- SS_total = Σ(y−ȳ)² = **698.00**
- SS_residual = **9.10**
- SS_regression = 698.00 − 9.10 = **688.90**
- **R² = 688.90/698.00 = 0.9870**

So 98.70% of the variation in sales is explained by advertising spend.

*Check:* r² = 0.9935² = 0.9870 ✓

**(d) ANOVA table.**

| Source | SS | df | MS | F |
|---|---:|---:|---:|---:|
| Regression | 688.90 | 1 | 688.90 | **227.11** |
| Residual | 9.10 | 3 | 3.0333 | |
| **Total** | **698.00** | **4** | | |

- df_regression = k = 1; df_residual = n − 2 = 3; df_total = n − 1 = 4
- F = 688.90 / 3.0333 = **227.11**

**(e) Testing the slope.**

- H₀: β₁ = 0 (advertising has no linear effect on sales)
- H₁: β₁ ≠ 0
- α = 0.05, df = 3

- SE(b₁) = √(MS_res / Σ(x−x̄)²) = √(3.0333/40) = √0.075833 = **0.27538**
- t = b₁ / SE(b₁) = 4.15 / 0.27538 = **15.0703**
- Critical value t(0.025, 3) = **3.182**
- p-value = **0.000634**

Since |15.07| > 3.182 and p < 0.05, **reject H₀**.

*Check:* t² = 15.0703² = 227.11 = F ✓

**Conclusion.** There is very strong evidence of a linear relationship between
advertising spend and sales. The model explains 98.7% of the variation, and the
slope is highly significant.

### Problem 6 — Hypothesis test, full six steps

A company claims its light bulbs last 1000 hours on average. A consumer group
tests 16 bulbs and finds a mean of 960 hours with a sample standard deviation
of 80 hours. Test the company's claim at α = 0.05.

**Solution.**

**Step 1 — Hypotheses.**
- H₀: μ = 1000 (the company's claim is correct)
- H₁: μ ≠ 1000 (the mean lifetime differs from the claim)

Two-tailed, because the question asks whether the claim is *wrong*, not
specifically whether bulbs last *less*.

**Step 2 — Significance level.** α = 0.05.

**Step 3 — Choose the test.** The population standard deviation is unknown and
n = 16 is small, so use the **one-sample t-test** with df = 16 − 1 = **15**.

**Step 4 — Test statistic.**
- standard error = s/√n = 80/√16 = 80/4 = **20**
- t = (x̄ − μ₀)/SE = (960 − 1000)/20 = −40/20 = **−2.00**

**Step 5 — Decision.**
- Critical values: t(0.025, 15) = **±2.131**
- p-value = **0.0639**

|−2.00| = 2.00 < 2.131, and p = 0.0639 > 0.05 → **fail to reject H₀**.

**Step 6 — Conclusion.** At the 5% significance level there is not enough
evidence to reject the company's claim. The observed shortfall of 40 hours
could plausibly arise from sampling variation in a sample of only 16 bulbs.

**Two things worth adding, which earn marks:**

- Note how close this is. At α = 0.10 the critical value is 1.753 and we
  *would* reject. The conclusion depends on a threshold chosen in advance —
  which is exactly why α must be fixed before seeing the data.
- "Fail to reject H₀" is not "the claim is true". A larger sample might well
  detect a real shortfall. With n = 16 the test simply lacks the power.

### Problem 7 — Chi-square test of independence

400 students were surveyed on their preferred programming language, by year of
study. Test at α = 0.05 whether preference is independent of year.

| | Python | Java | C++ | Total |
|---|---:|---:|---:|---:|
| First year | 60 | 30 | 30 | 120 |
| Second year | 80 | 40 | 40 | 160 |
| Third year | 60 | 30 | 30 | 120 |
| **Total** | **200** | **100** | **100** | **400** |

**Solution.**

**Step 1 — Hypotheses.**
- H₀: language preference is independent of year of study
- H₁: they are associated

**Step 2 — α = 0.05.**

**Step 3 — Expected frequencies.** E = (row total × column total)/grand total

| | Python | Java | C++ |
|---|---:|---:|---:|
| First year | 120×200/400 = **60** | 120×100/400 = **30** | **30** |
| Second year | 160×200/400 = **80** | **40** | **40** |
| Third year | **60** | **30** | **30** |

All expected frequencies are ≥ 5 ✓

**Step 4 — Test statistic.**

Every observed value equals its expected value exactly, so every term
(O − E)²/E is zero:

χ² = 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 = **0.00**

**Step 5 — Decision.**
- df = (3 − 1)(3 − 1) = **4**
- Critical value χ²(0.05, 4) = **9.488**
- p-value = **1.000**

0.00 < 9.488 → **fail to reject H₀**.

**Step 6 — Conclusion.** There is no evidence whatsoever of an association.
Language preference is independent of year of study.

**Why this problem is instructive:** the proportions are identical in every
row — each year splits 50% Python, 25% Java, 25% C++. Perfect independence
gives χ² = 0 exactly. Real data never does this, so if you compute χ² = 0 on an
exam question, check whether the data really is proportionally identical (as
here) or whether you have made an arithmetic slip.

---

## Section D — Mixed quick problems

**Q8.** If E(X) = 4 and Var(X) = 9, find E(2X − 3) and Var(2X − 3).

E(2X − 3) = 2(4) − 3 = **5**.
Var(2X − 3) = 2²(9) = **36**. The −3 shifts the distribution without changing
its spread.

**Q9.** A Poisson process averages 2 accidents per week. Find the probability of
no accidents in a given week, and of more than 3.

- P(X = 0) = e⁻² = **0.1353**
- P(X > 3) = 1 − [P(0)+P(1)+P(2)+P(3)]
  = 1 − [0.135335 + 0.270671 + 0.270671 + 0.180447]
  = 1 − 0.857123 = **0.1429**

**Q10.** A sample of 64 has mean 52 and sample standard deviation 8. Build a 95%
confidence interval for μ.

- SE = 8/√64 = 8/8 = **1.0**
- n = 64 > 30, so z = 1.96 is acceptable
- margin = 1.96 × 1.0 = **1.96**
- CI = 52 ± 1.96 = **(50.04, 53.96)**

**Q11.** Two machines produce items with sample variances 25 (n = 13) and 10
(n = 16). Test whether their variances differ at α = 0.05.

- H₀: σ₁² = σ₂²
- F = 25/10 = **2.50** on df = (12, 15)
- Two-tailed p = **0.0964** > 0.05 → **fail to reject H₀**

The variances are not significantly different at the 5% level.

---

## Exam strategy

1. **Write all six steps of a hypothesis test**, even when you can see the
   answer. Each step carries marks.
2. **Check Σ(x − x̄) = 0** whenever you build a deviation table. It costs five
   seconds and catches most arithmetic slips.
3. **Use R² = r² and t² = F** for simple regression as free verification.
4. **State the conclusion in the words of the problem**, not just "reject H₀".
5. **Say "fail to reject"**, never "accept".
6. **Add "correlation does not imply causation"** to every correlation
   interpretation.
7. **Check expected frequencies ≥ 5** before a chi-square test, and say you did.
8. **Watch n vs n−1.** If the question says "sample", divide by n − 1.
