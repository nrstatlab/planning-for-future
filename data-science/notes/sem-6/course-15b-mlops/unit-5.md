# Unit 5 — Monitoring, Feedback Loops and Governance

**Syllabus topics:** Monitoring models in production: drift detection,
ground truth evaluation. Feedback loops: retraining workflows, online
evaluation. Logging, monitoring frameworks. Governance: regulations (GDPR,
CCPA, GxP), Responsible AI principles. Templates for governance, compliance
and model risk management.

---

## 5.1 The three kinds of drift

**This is the most examinable material in the course, and the three are
routinely conflated.**

| Kind | What changes | Detectable from | Effect on accuracy |
|---|---|---|---|
| **Data drift** (covariate shift) | **P(X)** — the inputs | **the inputs alone, immediately** | **often none** |
| **Concept drift** | **P(y\|X)** — the relationship | **labels only** | **direct — this is the damaging one** |
| **Label drift** (prior shift) | **P(y)** — the base rate | labels | depends |

### 🎯 The asymmetry that defines production monitoring

> **Data drift is detectable immediately and often harmless. Concept drift is
> damaging and cannot be detected without labels** — which, in lending, arrive
> months later when the loan defaults or does not.
>
> **So you monitor the thing you can see as a proxy for the thing you cannot.**
> That is the whole design of production ML monitoring, and it is why input
> monitoring is not optional.

### 🔢 The lab proves the first half of that claim

[Experiment 14](lab.md#experiment-14) builds an automatic retraining loop on
injected drift and reports:

| | Mean accuracy |
|---|---|
| static model | 0.7116 |
| retraining model | 0.7132 |
| **difference** | **+0.0016** |

**Retraining barely helped**, and that is the honest result.

> **The reason is in the fixture.** The drift shifts **P(X)** — incomes move
> up. But **P(y|X)** did not change, because the generating coefficients are
> the same. **A model that learned the true relationship is still correct on
> shifted inputs.**
>
> **The operational rule:** alert on data drift, **investigate**, and retrain
> only if the labels confirm the relationship moved. Retraining on every input
> shift is expensive and can make things worse — you are fitting a smaller,
> more recent, noisier window.

---

## 5.2 Drift detection

### 📖 The tests, and what each is for

| Test | Measures | Note |
|---|---|---|
| **KS (Kolmogorov–Smirnov)** | the largest gap between two CDFs | a **hypothesis test** — gives a p-value |
| **PSI (Population Stability Index)** | binned distributional distance | a **magnitude** — the industry standard |
| Chi-square | categorical distributions | for discrete features |
| Wasserstein | "earth mover's" distance | interpretable in the feature's units |

### 🔢 The PSI thresholds to memorise

| PSI | Reading |
|---|---|
| < 0.1 | no significant change |
| **0.1 – 0.2** | **moderate — investigate** |
| **> 0.2** | **significant — act** |

### 🔢 The measurement, scored against known drift

[Experiment 13](lab.md#experiment-13) runs ten daily batches. Batches 0–4 are
clean; the income distribution shifts from batch 5, ramping to 1.5 sd.

| Batch | True drift | KS p | **PSI** | Alert |
|---|---|---|---|---|
| 0–4 | 0.00 | 0.21 – 1.00 | 0.005 – 0.017 | — |
| **5** | 0.30 | **0.0000** | 0.1255 | — |
| **6** | 0.60 | 0.0000 | **0.5540** | **YES** |
| 7 | 0.90 | 0.0000 | 0.9526 | YES |
| 8 | 1.20 | 0.0000 | 1.3519 | YES |
| 9 | 1.50 | 0.0000 | 2.1407 | YES |

**4 of 5 drifted batches caught, 0 false alarms on clean ones, with a
one-batch detection lag.**

### 🎯 Two lessons from that table

> **1. The detection lag is real and unavoidable.** Drift began at batch 5 and
> the alert fired at batch 6, because the shift ramps in and a small shift is
> genuinely hard to distinguish from noise. **Every detector trades lag
> against false alarms**; lowering the threshold catches batch 5 and starts
> alerting on clean batches too.
>
> **2. Statistical significance is not operational significance.** The KS
> p-value hits **0.0000 at batch 5**, long before PSI crosses its threshold.
> With 500 samples, KS detects a shift far too small to matter. **That is
> exactly why the industry uses PSI with a magnitude threshold rather than a
> hypothesis test** — and it is the same point Course 4 makes about p-values
> and effect sizes.

### 📖 What else to monitor, beyond the inputs

| Signal | Why |
|---|---|
| **the prediction distribution** | the approval rate moving from 45% to 90% is visible here and nowhere else |
| prediction confidence | rising uncertainty precedes accuracy loss |
| feature nulls and ranges | an upstream pipeline changed |
| latency and error rate | the service, as opposed to the model |
| **ground truth, when it arrives** | the only real measure |

---

## 5.3 Ground truth evaluation

**The hard problem: labels are late, expensive, or biased.**

| Difficulty | Example |
|---|---|
| **Delayed** | a loan default is known in months |
| **Expensive** | a human must label it |
| **Partial** | you only learn the outcome for applications you **approved** |

### ⚠️ The last one is a feedback loop, and it is a trap

> **You approve a loan and learn whether it defaults. You decline a loan and
> learn nothing.** So your future training data contains only approvals — and
> the model's own decisions determine what it will next be trained on.
>
> **The model's mistakes become invisible to it.** A declined applicant who
> would have repaid never appears in the data as a missed opportunity.

**The mitigations are uncomfortable and necessary:**

| Mitigation | Cost |
|---|---|
| **approve a small random sample** you would have declined | real money, deliberately lost |
| use a **held-out policy** on a fraction of traffic | some bad decisions |
| model the selection explicitly (reject inference) | statistically hard, and assumption-heavy |

**Every one costs something.** Deciding that the cost is worth paying is a
business decision, not a technical one — but naming the problem is the
engineer's job.

---

## 5.4 The feedback loop and online evaluation

```
1. MONITOR      input distributions, continuously
2. ALERT        when a magnitude threshold is crossed
3. INVESTIGATE  a human looks — is the shift REAL?
4. LABEL        wait for ground truth, or buy it
5. RETRAIN      on a window, with the SAME pipeline
6. VALIDATE     against the old model, on a held-out set
7. DEPLOY       shadow, then canary, then full
```

### ⚠️ Step 3 gets automated away and should not be

> **The most common cause of a drift alert is not the world changing but an
> upstream pipeline changing** — a unit switched from rupees to thousands, a
> null becoming a zero, a new source system with a different encoding.
>
> **Retraining on that corrupts the model with the bug**, and does it
> automatically, at scale, without anyone noticing.

### 📖 Online evaluation

**Online evaluation** measures the model on live traffic rather than on a
held-out set: a canary's error rate, an A/B test's business metric, or a
shadow deployment's logged disagreement with the incumbent. It is the only
evaluation that reflects the data the model actually meets.

### 📖 Retraining triggers, and their trade-offs

| Trigger | Pro | Con |
|---|---|---|
| **Scheduled** (weekly) | simple, predictable | retrains when nothing changed |
| **Drift-triggered** | responsive | can fire on an upstream bug |
| **Performance-triggered** | the right signal | **needs labels — often too late** |
| Hybrid | scheduled floor, drift ceiling | **what most teams end up with** |

---

## 5.5 Logging and monitoring frameworks

### 📖 Metrics against logs

| | **Metrics** | **Logs** |
|---|---|---|
| Answer | **that** something is wrong | **what** is wrong |
| Shape | numeric time series | structured events |
| Cost | cheap, aggregated | expensive at volume |
| Tool | Prometheus, Grafana | ELK, Loki, CloudWatch |

### 📖 Prometheus, and the contract

**Prometheus does not need an agent inside your application. It *scrapes* a
plain-text HTTP endpoint on a schedule**, and that format is the entire
contract:

```
# HELP model_requests_total Total prediction requests.
# TYPE model_requests_total counter
model_requests_total 3
```

[Experiment 12](lab.md#experiment-12) serves exactly this, calls it over HTTP,
and **parses the response back** to confirm the format is valid.

### 🔢 The four metric types

| Type | Only ever | Use for |
|---|---|---|
| **Counter** | goes up (or resets) | requests, errors |
| **Gauge** | up and down | queue depth, PSI, memory |
| **Histogram** | buckets, summed server-side | **latency** |
| Summary | client-side quantiles | rarely right |

### ⚠️ Use a histogram for latency, not a gauge

> **A gauge holding "the mean latency" cannot be aggregated.** Averaging the
> means of four instances is not the mean, and **p95 cannot be recovered at
> all.** A histogram ships bucket counts, and `histogram_quantile()` computes
> the percentile correctly across every instance.

### 🎯 `for: 10m` — the most important line in an alert

```yaml
- alert: HighErrorRate
  expr: rate(errors[5m]) / rate(requests[5m]) > 0.05
  for: 10m
```

**Without it, one slow request pages somebody at 03:00.** The `for` clause
requires the condition to hold continuously, and choosing it is the whole
craft of alerting: **too short and you train people to ignore alerts; too long
and you find out from a customer.**

**Drift alerts use `for: 1h`** — drift is slow, and one noisy batch should not
page anyone.

### 💡 The dashboard panel nobody builds

**The prediction distribution over time.** Every other panel monitors the
*service*; that one monitors the *model*. A model can be fast, error-free and
approving 90% of applications when it used to approve 45% — **and only this
panel shows it.**

---

## 5.6 Governance and regulation

| Regulation | Scope | The point |
|---|---|---|
| **GDPR** | EU personal data | consent, access, erasure, **automated decisions** |
| **CCPA/CPRA** | California residents | disclosure, opt-out of sale, deletion |
| **GxP** | pharma, medical devices | validation, audit trails, **change control** |
| **DPDP Act 2023** | India | consent, purpose limitation, a Data Protection Board |
| **EU AI Act** | AI systems by risk tier | credit scoring is **high-risk** |

### 🔢 GDPR against a real system

[Experiment 16](lab.md#experiment-16) audits the loan model article by
article:

| Article | Against this system |
|---|---|
| **Art. 5** minimisation | the model uses 4 features — do you need `age`? |
| **Art. 15** access | return everything held about one applicant — needs a subject id on **every row, including logs** |
| **Art. 17** erasure | **the hard one** |
| **Art. 22** automated decisions | loan approval has legal effect — **a human review route is required, not optional** |
| **Art. 22** explanation | logistic regression can answer; a deep network cannot |
| **Art. 35** DPIA | before deployment, not after |

### 🎯 Article 17 is the one that breaks ML systems

> **Deleting a row from the database is easy. The model trained on that row
> still contains information derived from it, and there is no way to subtract
> one example from fitted coefficients.**
>
> The practical answer is to **retrain on a schedule from current data**, so
> an erased record leaves the model within one cycle — which means **your
> retraining pipeline is a compliance control, not just an accuracy one.**
>
> That is not obvious and it is exactly the sort of thing an examiner asks.

### ⚠️ Article 22 and explainability, together

**A high-risk automated decision must be explainable and appealable.** That
constrains the model *before* you choose it: a logistic regression can tell an
applicant which factors weighed against them; a gradient-boosted ensemble
cannot, without a post-hoc method whose faithfulness is itself contested.

**Course 15 A measured a version of this**: attention weights matched the
decisive word only **92.5%** of the time. **Every post-hoc explanation
produces a plausible story, and plausibility is not correctness.**

---

## 5.7 Responsible AI: fairness, measured

[Experiment 16](lab.md#experiment-16) reports approval rates by region, with
region **not** a model input:

| Region | Approval rate |
|---|---|
| four regions | spread **< 0.05** |

> ### 🎯 That is the control condition, and it is why the data is generated
>
> The regions were drawn from the same distribution, so **the spread is
> sampling noise rather than bias** — and knowing that is only possible
> because the data was constructed.
>
> **On real data the same table would not tell you either.** A spread could be
> noise, could be a genuine difference in the applicant pool, or could be the
> model. **Deciding which is not a statistical question** — it needs the
> domain.

### 📖 The facial-recognition case the syllabus names

| | |
|---|---|
| The data | scraped photographs — no consent, so **Art. 6 has no lawful basis** |
| Special category | biometric identification is **Art. 9** — a higher bar |
| The error rates | documented to be far worse on darker skin and on women |
| The consequence | a false match in policing costs someone their liberty |
| **The asymmetry** | **those most likely to be misidentified are least able to contest it** |

> **The point is not that the technology is bad.** It is that **accuracy is not
> a single number**: a system at 99% overall can be at 80% for one group, and
> if the cost of an error falls unequally then the aggregate figure **hides
> the harm rather than measuring it**.
>
> **Report per-group metrics.** That is the whole recommendation.

---

## 5.8 Model risk management

**A governance template, as a checklist that is actually answerable:**

| Item | Question |
|---|---|
| **Owner** | who is accountable, by name? |
| **Purpose** | what decision does it make, for whom? |
| **Data** | source, licence, consent basis, retention period |
| **Metrics** | **overall and per group**, against a baseline |
| **Limitations** | where does it not work? |
| **Human oversight** | who reviews, and how does an appeal work? |
| **Monitoring** | which signals, which thresholds, who is paged |
| **Rollback** | how, and how long does it take? |
| **Review date** | when is this reassessed? |

**That is a model card plus an operational plan**, and every row is a question
a regulator can ask and a student can answer about their own project.

---

## What to be able to do after this unit

- [ ] **Distinguish data, concept and label drift**, and say which is detectable early
- [ ] Explain why retraining on data drift may not help — with the measured +0.0016
- [ ] Give the PSI thresholds and compare PSI with the KS test
- [ ] **Explain why statistical significance is not operational significance**
- [ ] Explain the detection lag and the trade-off behind it
- [ ] Describe the partial-label feedback loop and three mitigations
- [ ] Give the seven steps of the feedback loop, and say **which must stay human**
- [ ] Compare metrics with logs, and the four Prometheus metric types
- [ ] **Say why latency needs a histogram, not a gauge**
- [ ] Explain what `for:` does in an alert
- [ ] Name the panel that monitors the model rather than the service
- [ ] **Explain why GDPR Article 17 is hard for a trained model**, and the practical answer
- [ ] Say what Article 22 requires and how it constrains model choice
- [ ] **Explain why a per-group accuracy table can be noise, bias, or a real difference**
- [ ] List the rows of a model risk management template

**Cross-check yourself:** run
`12_serve_drift_govern.py`.
