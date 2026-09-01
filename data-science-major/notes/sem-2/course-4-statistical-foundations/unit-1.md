# Unit 1 — Fundamentals of Probability and Basic Statistics

**Syllabus topics:** Probability — concept of uncertainty, axioms and
rules of probability, conditional probability. Measures of central tendency —
mean, median, mode. Measures of dispersion — range, interquartile range,
variance, standard deviation. Introduction to correlation and covariance. Data
representation — histograms, bar charts, scatter plots.

> **Plus Bayes' theorem**, which is examined but missing from the syllabus
> list — see [§1.6](#16-bayes-theorem--examined-but-not-in-the-syllabus) and
> review finding **D1**.

---

## 1.1 Probability — the big idea

### 🎯 The big idea

Probability is a number between 0 and 1 that measures how likely something is.
0 means it will never happen, 1 means it certainly will, and 0.5 means it is as
likely as not.

### 📖 The story

You are waiting for a bus. You cannot know whether it will arrive in the next
five minutes — but you are not *completely* ignorant either. You have taken
this bus a hundred times. It came within five minutes on about seventy of
those. That "about 70 out of 100" is a probability, and it is enough to decide
whether to wait or walk. Probability is the mathematics of acting sensibly
when you cannot be certain.

### 🔢 The basics

For **equally likely** outcomes:

> **P(A) = number of favourable outcomes / total number of outcomes**

Rolling a fair die and wanting an even number: favourable = {2, 4, 6} = 3,
total = 6, so P(even) = 3/6 = 0.5.

**Vocabulary you need:**

| Term | Meaning |
|---|---|
| **Experiment** | A process with an uncertain outcome (rolling a die) |
| **Sample space (S)** | Every possible outcome: {1, 2, 3, 4, 5, 6} |
| **Event** | A subset of the sample space: "even" = {2, 4, 6} |
| **Mutually exclusive** | Two events that cannot both happen |
| **Independent** | One event happening does not change the other's probability |
| **Exhaustive** | Events that between them cover the whole sample space |

### The three axioms (Kolmogorov)

1. **P(A) ≥ 0** — a probability is never negative
2. **P(S) = 1** — something in the sample space must happen
3. If A and B are mutually exclusive, **P(A ∪ B) = P(A) + P(B)**

Everything else is derived from these three.

### The rules

**Complement rule**

> **P(A′) = 1 − P(A)**

If the chance of rain is 0.3, the chance of no rain is 0.7. Often the easiest
route to an answer: "at least one" problems are usually solved as
1 − P(none).

**Addition rule** — for "A **or** B"

> **P(A ∪ B) = P(A) + P(B) − P(A ∩ B)**

Subtract the overlap, or you count it twice. When A and B are mutually
exclusive, P(A ∩ B) = 0 and it simplifies to P(A) + P(B).

*Example.* In a class of 100: 60 play cricket, 40 play football, 25 play both.
P(cricket or football) = 0.60 + 0.40 − 0.25 = **0.75**. Without subtracting the
25, you would get 1.00 — claiming every student plays a sport, which is false.

**Multiplication rule** — for "A **and** B"

> **P(A ∩ B) = P(A) × P(B|A)**
> and if A and B are independent, **P(A ∩ B) = P(A) × P(B)**

*Example.* Two cards drawn **without replacement** from a pack. P(both aces)
= (4/52) × (3/51) = 12/2652 ≈ **0.0045**. The second fraction is 3/51 because
one ace is already gone — the events are not independent.

**With replacement** they would be independent: (4/52) × (4/52) ≈ 0.0059.

## 1.2 Conditional probability

### 🎯 The big idea

Conditional probability is the probability of A **given that you already know**
B happened. New information changes the odds.

### 📖 The story

A friend rolls a die behind a screen and tells you the result is even. Before
that, P(6) was 1/6. Now you know the outcome is one of {2, 4, 6}, so P(6) has
risen to 1/3. Nothing about the die changed — only what you know did.

### 🔢 The formula

> **P(A|B) = P(A ∩ B) / P(B)**, provided P(B) > 0

In plain English:
- P(A|B) = "probability of A given B"
- P(A ∩ B) = probability that **both** happen
- P(B) = probability of the condition

Reading it as "restrict the world to B, then ask what fraction of that world is
also A" makes it obvious.

*Worked example.* Of 100 students, 40 study Python, 30 study R, 20 study both.
A student studies R. What is the probability they also study Python?

P(Python | R) = P(both) / P(R) = 0.20 / 0.30 = **0.667**

Compare with the unconditional P(Python) = 0.40. Knowing they study R raised
it from 0.40 to 0.67.

### Independence

A and B are **independent** when knowing one tells you nothing about the other:

> **P(A|B) = P(A)**, equivalently **P(A ∩ B) = P(A) × P(B)**

In the example above, 0.667 ≠ 0.40, so the two subjects are **not**
independent — students who take R are more likely to take Python.

**Do not confuse independent with mutually exclusive.** Mutually exclusive
events cannot both occur, so knowing one happened tells you the other did
*not* — which is a very strong dependence. Two mutually exclusive events with
non-zero probability are never independent.

## 1.3 Measures of central tendency

### 🎯 The big idea

One number that stands in for a whole set of numbers — where the data
"centres".

### 📖 The story

Someone asks how your class did in the statistics test. You could read out all
sixty marks. Instead you say "about 72". That single number is a measure of
central tendency, and it communicates more in one word than the full list does
in sixty.

### Mean

> **x̄ = Σxᵢ / n**

Add everything, divide by how many.

**Worked example.** Marks: 5, 8, 10, 12, 15

- Step 1: add them → 5 + 8 + 10 + 12 + 15 = 50
- Step 2: count them → n = 5
- Step 3: divide → 50 / 5 = **10**

### Median

Sort the data; take the middle value. With an even count, average the two
middle values.

**Same data:** 5, 8, **10**, 12, 15 → median = **10**

**With an even count:** 5, 8, **10, 12**, 15, 18 → (10 + 12)/2 = **11**

### Mode

The most frequent value. There may be none, one, or several.

3, 7, **7**, 9, 12 → mode = **7**

### 💡 The "aha!" moment

Add one outlier and watch what happens:

| Data | Mean | Median |
|---|---|---|
| 5, 8, 10, 12, 15 | 10.0 | 10 |
| 5, 8, 10, 12, **500** | **107.0** | 10 |

The mean moved from 10 to 107 — it now describes nobody in the dataset. The
median did not move at all.

**That is why incomes and house prices are always reported as medians.** A
handful of billionaires would drag the mean income far above what anyone
actually earns. When a question asks "which measure is appropriate and why",
this is the answer: use the median when the data is skewed or contains
outliers.

### Choosing between them

| Use | When |
|---|---|
| **Mean** | Data is roughly symmetric with no extreme outliers |
| **Median** | Data is skewed, or has outliers (income, house prices) |
| **Mode** | Data is categorical (most common blood group, shoe size) |

**Empirical relationship** for a moderately skewed distribution:

> **Mode ≈ 3 × Median − 2 × Mean**

## 1.4 Measures of dispersion

### 🎯 The big idea

The centre is only half the story. Dispersion says how *spread out* the values
are around it.

### 📖 The story

Two students both average 60 across five tests.

- Ravi: 58, 60, 61, 59, 62 — reliable, always around 60
- Priya: 20, 95, 40, 100, 45 — wildly inconsistent

Same mean. Completely different students. If you had to pick one for a team,
you would want to know the spread, not just the average. **The mean without a
measure of spread is close to useless.**

### Range

> **Range = maximum − minimum**

Ravi: 62 − 58 = 4. Priya: 100 − 20 = 80.

Simple, but it uses only two values — one outlier defines it entirely.

### Interquartile range (IQR)

> **IQR = Q₃ − Q₁**

Q₁ is the 25th percentile, Q₃ the 75th. The IQR is the spread of the middle
50%, so outliers cannot inflate it.

**Outlier rule:** anything below Q₁ − 1.5×IQR or above Q₃ + 1.5×IQR.

### Variance and standard deviation

The sequence matters — never skip a step:

1. Find the mean
2. Find each value's difference from the mean
3. **Square** each difference (so positives and negatives do not cancel)
4. Average the squares → **variance**
5. Take the square root → **standard deviation**

> **Population variance: σ² = Σ(xᵢ − μ)² / N**
> **Sample variance: s² = Σ(xᵢ − x̄)² / (n − 1)**

In plain English:
- σ² or s² = variance
- xᵢ = each value
- μ or x̄ = the mean
- N or n = how many values
- Σ = "add all of these up"

**Worked example.** Data: 5, 8, 10, 12, 15 (treat as a sample)

| xᵢ | xᵢ − x̄ | (xᵢ − x̄)² |
|---:|---:|---:|
| 5 | −5 | 25 |
| 8 | −2 | 4 |
| 10 | 0 | 0 |
| 12 | 2 | 4 |
| 15 | 5 | 25 |
| **Σ** | **0** | **58** |

- Step 1: mean = 10
- Step 2–3: differences and their squares, as above
- Step 4: s² = 58 / (5 − 1) = 58/4 = **14.5**
- Step 5: s = √14.5 = **3.81**

Notice the differences sum to **zero**. They always do — that is precisely why
we square them. It is also a free check on your arithmetic.

### 💡 Why n − 1? (Bessel's correction)

You measured the deviations from the *sample's own* mean, not the true
population mean. The sample mean sits, by construction, right in the middle of
your sample — so the deviations you observe are slightly smaller than the true
ones. Dividing by n−1 instead of n inflates the answer just enough to correct
for that bias.

**Rule for the exam:** dividing a sample by n instead of n−1 is the most
frequent arithmetic error in this course. If the question says "sample", use
n−1.

### Coefficient of variation

> **CV = (s / x̄) × 100%**

A unit-free measure, so it compares spread across different scales. Comparing
the variability of heights (cm) with weights (kg) requires CV; standard
deviation alone cannot do it.

## 1.5 Correlation and covariance (introduction)

*Full treatment in [Unit 4](unit-4.md); this is the introduction the syllabus
places here.*

**Covariance** measures whether two variables move together:

> **Cov(X,Y) = Σ(xᵢ − x̄)(yᵢ − ȳ) / (n − 1)**

Positive means they rise together; negative means one rises as the other
falls. But its **magnitude is meaningless** — it depends on the units.
Measure height in centimetres instead of metres and the covariance multiplies
by 100.

**Correlation** fixes that by standardising:

> **r = Cov(X,Y) / (sₓ × s_y)**

r is unit-free and always between **−1 and +1**, which is why it is the number
you report.

## 1.6 Bayes' theorem — examined but not in the syllabus

> Unit 1 lists only "conditional probability". Bayes' theorem appears in the
> prescribed activities ("quiz on probability, conditional probability,
> **Bayes**") and in lab experiment 2 — but in no unit. Study it.
> See review finding **D1**.

### 🎯 The big idea

Bayes' theorem lets you **reverse** a conditional probability. If you know the
chance of a positive test given the disease, Bayes gives you the chance of the
disease given a positive test — which is what you actually want to know.

This one trips up medical doctors, let alone students. Take it slowly.

### 📖 The story

A disease affects 1 in 100 people. A test is very good: it catches 99% of
people who have it, and correctly clears 95% of those who do not. You test
positive.

How worried should you be? Most people say "99% — the test is 99% accurate."

The real answer is about **17%**.

### 🔢 The formula

> **P(A|B) = P(B|A) × P(A) / P(B)**
>
> where **P(B) = P(B|A)×P(A) + P(B|A′)×P(A′)** — the law of total probability

In plain English:
- P(A) = the **prior** — what you believed before the evidence
- P(B|A) = the **likelihood** — how probable the evidence is if A is true
- P(A|B) = the **posterior** — your updated belief after seeing the evidence

**Worked solution.**

- Step 1: write down what you are given
  - P(D) = 0.01, so P(not D) = 0.99
  - P(+ | D) = 0.99 (sensitivity)
  - P(− | not D) = 0.95, so P(+ | not D) = 0.05 (false positive rate)

- Step 2: find P(+) using total probability
  - P(+) = (0.99 × 0.01) + (0.05 × 0.99)
  - = 0.0099 + 0.0495 = **0.0594**

- Step 3: apply Bayes
  - P(D | +) = 0.0099 / 0.0594 = **0.1667**, about **17%**

### 💡 The "aha!" moment

Think of 10,000 people:

| | Have the disease | Do not | Total |
|---|---:|---:|---:|
| **Test positive** | 99 | 495 | 594 |
| **Test negative** | 1 | 9,405 | 9,406 |
| **Total** | 100 | 9,900 | 10,000 |

Of the 594 who test positive, only 99 are genuinely ill — 99/594 = 17%.

The disease is **rare**. So the 5% of false positives, drawn from the enormous
healthy majority, vastly outnumber the true positives drawn from the tiny sick
minority. The test is excellent; the base rate is doing the damage.

Confusing P(D|+) with P(+|D) is called the **base rate fallacy**, and it is
the single most examined idea in this part of the course. Draw the
10,000-person table every time — it makes the answer obvious and it earns
marks.

## 1.7 Data representation

| Chart | Use for | Key point |
|---|---|---|
| **Bar chart** | Categorical data | Bars have **gaps**; order is arbitrary |
| **Histogram** | Continuous data | Bars **touch**; classes are adjacent intervals |
| **Scatter plot** | Two numeric variables | Points only — never join them with lines |
| **Pie chart** | Parts of a whole | Only when the parts sum to 100% |
| **Box plot** | Spread and outliers | Shows min, Q₁, median, Q₃, max |

**Bar chart vs histogram is a guaranteed two-mark question.** Bar chart:
categories, gaps between bars. Histogram: continuous intervals, no gaps.

### Reading the shape of a histogram

- **Symmetric** — mean ≈ median ≈ mode
- **Positively (right) skewed** — a tail to the right; mean > median
- **Negatively (left) skewed** — a tail to the left; mean < median

> **Pearson's skewness = 3(mean − median) / standard deviation**

---

## 📝 Practice problems

### Problem 1

A bag contains 5 red, 3 blue and 2 green balls. One ball is drawn at random.
Find (a) P(red), (b) P(not red), (c) P(red or blue).

**Solution.**

Total balls = 5 + 3 + 2 = 10.

(a) P(red) = 5/10 = **0.5**

(b) P(not red) = 1 − 0.5 = **0.5** (complement rule)

(c) Red and blue are mutually exclusive — one ball cannot be both — so the
overlap term is zero:
P(red or blue) = 5/10 + 3/10 = 8/10 = **0.8**

### Problem 2

The marks of 8 students are: 45, 52, 48, 60, 55, 49, 58, 51.
Find the mean, median, range, sample variance and sample standard deviation.

**Solution.**

- Step 1 — **Mean**: sum = 45+52+48+60+55+49+58+51 = 418; n = 8;
  x̄ = 418/8 = **52.25**

- Step 2 — **Median**: sorted → 45, 48, 49, **51, 52**, 55, 58, 60.
  n is even, so average the 4th and 5th: (51 + 52)/2 = **51.5**

- Step 3 — **Range**: 60 − 45 = **15**

- Step 4 — **Variance**:

| xᵢ | xᵢ − 52.25 | (xᵢ − 52.25)² |
|---:|---:|---:|
| 45 | −7.25 | 52.5625 |
| 52 | −0.25 | 0.0625 |
| 48 | −4.25 | 18.0625 |
| 60 | 7.75 | 60.0625 |
| 55 | 2.75 | 7.5625 |
| 49 | −3.25 | 10.5625 |
| 58 | 5.75 | 33.0625 |
| 51 | −1.25 | 1.5625 |
| **Σ** | **0.00** ✓ | **183.50** |

s² = 183.50 / (8 − 1) = 183.50 / 7 = **26.21**

- Step 5 — **Standard deviation**: s = √26.21 = **5.12**

(The deviations summing to zero confirms the mean is right.)

### Problem 3

In a factory, machine A makes 60% of the items and machine B makes 40%. Two
percent of A's output is defective, and 5% of B's. An item is picked at random
and found defective. What is the probability it came from machine B?

**Solution.**

- Step 1 — write down what you know
  - P(A) = 0.60, P(B) = 0.40
  - P(D|A) = 0.02, P(D|B) = 0.05

- Step 2 — total probability of a defective item
  - P(D) = (0.02 × 0.60) + (0.05 × 0.40)
  - = 0.012 + 0.020 = **0.032**

- Step 3 — apply Bayes
  - P(B|D) = P(D|B) × P(B) / P(D) = 0.020 / 0.032 = **0.625**

So there is a **62.5%** chance it came from machine B — even though B makes
only 40% of the output, because its defect rate is more than twice A's.

*Check:* P(A|D) = 0.012/0.032 = 0.375, and 0.625 + 0.375 = 1 ✓

---

## Exam questions from this unit

**Two marks**

1. State the axioms of probability.
2. Define mutually exclusive and independent events. Can an event be both?
3. When is the median preferred to the mean?
4. Distinguish a histogram from a bar chart.
5. Why is n−1 used in the sample variance?

**Five marks**

1. Explain the addition and multiplication rules with examples.
2. Explain the measures of central tendency and when each is appropriate.
3. Compute the mean, median, mode, variance and standard deviation for a given
   dataset.
4. Explain covariance and correlation, and why correlation is preferred.

**Ten marks**

1. State and prove Bayes' theorem, and solve a medical-testing problem with it.
2. Explain all measures of central tendency and dispersion with a fully worked
   dataset.

## Mistakes that cost marks

- Dividing by n instead of n−1 for a sample
- Forgetting to subtract P(A ∩ B) in the addition rule
- Treating dependent events as independent (drawing without replacement)
- Confusing P(A|B) with P(B|A) — the base rate fallacy
- Confusing mutually exclusive with independent
- Reporting a covariance magnitude as if it were meaningful
- Forgetting to sort the data before finding the median
