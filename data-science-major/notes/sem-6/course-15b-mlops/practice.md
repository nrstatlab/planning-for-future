# Course 15 B — Practice Questions with Worked Solutions

Grouped by unit. **Attempt each before reading the solution.** Numeric answers
name the file that printed them.

---

## Unit 1 — Foundations

### Q1. Distinguish the data lifecycle from the data engineering lifecycle. *(5 marks)*

<details><summary>Solution</summary>

| | **Data lifecycle** | **Data engineering lifecycle** |
|---|---|---|
| About | **the data itself** | **the pipeline that moves it** |
| Stages | created → stored → used → archived → destroyed | generation → storage → ingestion → transformation → serving |
| Owned by | the business and the regulator | the data engineering team |

**And the five undercurrents**, which run *underneath* every stage rather than
between them: **security, data management, DataOps, data architecture,
orchestration.**

**Remember which are undercurrents by asking: is this true of ingestion AND of
serving?** Security is. Orchestration is. That is why they are drawn
underneath.
</details>

### Q2. Why is a silently-wrong pipeline worse than one that crashes? Give a measured example. *(6 marks)*

<details><summary>Solution</summary>

**A crash is loud and gets fixed. A wrong number is trusted.**

`01_environment_etl.py` runs an ETL job on data with three defects — a
lowercase region, a price with a currency prefix, a duplicated order:

| | Value |
|---|---|
| Correct South revenue | **₹10,360** |
| Uncleaned total | **₹10,500** |
| Error | **₹140, about 1%** |

The three defects were worth **−₹1,680, −₹700 and +₹2,520** and **nearly
cancelled**.

> **That is the dangerous case.** A figure that is wildly wrong gets noticed;
> a figure 1% wrong gets reported to the board. The errors cancelled by luck.

**The only reliable check is an independently computed figure**, which is why
this repository has five engines agreeing on ₹10,360.
</details>

### Q3. Explain ETL against ELT and why ELT became dominant. *(5 marks)*

<details><summary>Solution</summary>

| | **ETL** | **ELT** |
|---|---|---|
| Order | Extract → **Transform** → Load | Extract → Load → **Transform** |
| Transform runs | in a separate engine | **in the warehouse, in SQL** |
| Raw data kept | usually not | **yes** |

**ELT won because cloud warehouse compute became cheap and elastic.** Keeping
the raw data means a transformation bug is fixed by re-running the
transformation, rather than re-extracting from a source system that may no
longer hold the history.
</details>

---

## Unit 2 — Architecture

### Q4. Distinguish availability, reliability, RTO and RPO. Give the downtime for three nines. *(6 marks)*

<details><summary>Solution</summary>

| Term | Definition |
|---|---|
| **Availability** | the fraction of time the system is usable |
| **Reliability** | it does the **right thing** when it is up |
| **RTO** | how long recovery may take |
| **RPO** | **how much data may be lost** |

| Availability | Downtime per year |
|---|---|
| 99% | 3.65 days |
| **99.9%** | **8.8 hours** |
| 99.99% | 53 minutes |

**Each nine costs roughly ten times the last**, so ask what downtime actually
costs before choosing.

**RPO is the one people forget.** A system that recovers in five minutes but
loses an hour of transactions has an excellent RTO and an unacceptable RPO.
</details>

### Q5. Microservices are slower than a monolith for the same work. So why use them? *(6 marks)*

<details><summary>Solution</summary>

**Start by conceding the point.** `01_environment_etl.py` times both: every
boundary adds serialisation, a network hop and a new failure mode, so the
microservices version is **measurably slower**.

**What you buy is not speed. It is independent deployment and independent
scaling**, and they only pay when the parts genuinely differ:

| Strategy | Instances | Wasted capacity |
|---|---|---|
| monolith, scaled 4× | 4 | **4× of every component** |
| microservices, scale the scorer 4× | 4 + 1 + 1 | **none** |

**That is an argument about cost at scale, not elegance.**

**And the hidden cost:** one database per service. If two services share a
database they are not independent, so the data must be split too — **and a
join you used to write in SQL becomes an API call and an in-memory merge.**

**The rule:** start with a well-structured monolith; split a service out when
you can name the specific scaling or deployment problem it solves.
</details>

### Q6. Compare batch and event-driven ingestion. Give measured latencies. *(6 marks)*

<details><summary>Solution</summary>

`04_batch_vs_event.py`, 300 records, 2 ms work each, 250 ms batch interval:

| Mode | p50 latency | p95 |
|---|---|---|
| **batch** | **355.4 ms** | 519.8 ms |
| **event-driven** | **2.2 ms** | 2.3 ms |

**About 160×**, because a batch record waits for the next tick — its latency
is dominated by the *interval*, not the 2 ms of processing.

> **Batching does not make you faster. It makes you efficient per record at
> the cost of latency per record.**

| | Batch | Event-driven |
|---|---|---|
| Triggered by | a schedule | an arrival |
| Per-record cost | **low — amortised setup** | higher |
| **Failure** | **retry the whole batch** | retry one message |

**The failure row decides real architectures.** Re-running a whole batch
requires every step to be **idempotent**, which is most of the work in writing
an ETL job. A stream consumer retries one message but needs a **dead-letter
queue** for one that fails for ever.
</details>

### Q7. Compute a TCO and explain why the licence fee is not it. *(5 marks)*

<details><summary>Solution</summary>

| Component | Often forgotten |
|---|---|
| Licence or subscription | — |
| Infrastructure | |
| **Engineering time to operate it** | **usually the largest line** |
| Training | |
| Migration | |
| **Opportunity cost** | what your engineers are not building instead |

> **"Free" open-source software with a full-time engineer maintaining it costs
> more than a managed service at ₹40,000 a month.**

**And the related distinction:** CapEx (buy servers) against OpEx (rent them).
The move to cloud shifts one to the other, changing the accounting as much as
the engineering.
</details>

---

## Unit 3 — MLOps fundamentals

### Q8. Give three ways MLOps differs from DevOps. *(6 marks)*

<details><summary>Solution</summary>

| | **DevOps** | **MLOps** |
|---|---|---|
| Artefacts | code | **code + data + model** |
| "It works" | tests pass | **tests pass AND the metric is good enough** |
| Degrades over time | **no** — code does not rot | **yes** — the world moves |
| Rollback | redeploy the old build | **the old model AND its preprocessing** |

**The rollback row causes real incidents.** Deploying an old model with new
preprocessing produces predictions that are silently wrong — no error, no
crash, just worse decisions.
</details>

### Q9. What is training/serving skew and what fixes it? *(5 marks)*

<details><summary>Solution</summary>

**The transformation applied at training differs from the one applied at
serving.**

Example: you train on a DataFrame where a missing value became the column
mean; you serve from a Flask endpoint where a missing value becomes zero.
**The model is fine; the input is not**, and nothing raises an error.

**The fix is architectural, not a test:** one implementation of the
transformation, called from both paths. That is what a feature store is for,
and a shared module is enough at small scale.
</details>

### Q10. List the four things that must be pinned for reproducibility, and demonstrate the one people forget. *(6 marks)*

<details><summary>Solution</summary>

| # | Pin | How |
|---|---|---|
| 1 | **code** | a git commit |
| 2 | **data** | a seed, or DVC |
| 3 | **environment** | `requirements.txt` with `==`, not `>=` |
| 4 | **randomness** | `random_state` on every estimator **AND on the split** |

**Number 4 is the one people forget.** `07_mlflow_dvc.py` demonstrates it: the
same code with the model still seeded and **only `train_test_split`'s
`random_state` removed**, run three times, gives **three different AUCs**.

**That is enough to make every number in a report unrepeatable.**

The pinned version runs twice and gives **byte-identical** results —
0.793326 both times.
</details>

### Q11. What does DVC store in git, and what does it not? *(5 marks)*

<details><summary>Solution</summary>

**Git tracks the pointer; DVC keeps the data.**

The `.dvc` file is a few hundred bytes holding an **md5 and a size**. The data
file itself is in `.gitignore` and lives in the DVC cache or a remote.

| | git alone | **git + DVC** |
|---|---|---|
| Stores | every version **in full** | a hash |
| Repo size | grows with every data change | **stays small** |
| Diff | useless on a binary | compares hashes |
| **Reproduce** | code only | **code AND data** |

**The two-command workflow:**

```bash
git checkout <sha>     # moves the code AND the pointer
dvc checkout           # reads the pointer, restores the data
```

`07_mlflow_dvc.py` verifies this: committing a drifted v2, checking out v1,
and confirming the income mean returns from **1.4805 to −0.0195**.

**Why it matters:** when a production model behaves oddly, the question is
"what did it see when it was trained". Without data versioning that question
has no answer.
</details>

### Q12. Why should a tracking table log the training score as well as the test score? *(4 marks)*

<details><summary>Solution</summary>

**Because the gap is the only column that says *why* a model underperformed.**

From `07_mlflow_dvc.py`:

| Run | Accuracy | AUC | **Gap** |
|---|---|---|---|
| logreg-C1 | 0.7080 | 0.7752 | −0.0100 |
| **rf-depth12** | 0.6850 | 0.7463 | **0.2783** |

`rf-depth12` scored worst *and* has a gap of 0.2783 — it **memorised the
training set**. Without the gap column you know only that it was worse, not
that the fix is regularisation rather than more features.

**It costs one extra `log_metric` call.**
</details>

---

## Unit 4 — Deployment and CI/CD

### Q13. What separates a demo endpoint from a production one? Give the measured responses. *(6 marks)*

<details><summary>Solution</summary>

**Handling the requests that are wrong.**

`12_serve_drift_govern.py` runs a real Flask server and calls it:

| Request | Status |
|---|---|
| `GET /health` | **200** |
| valid `POST /predict` | **200** — with a `model_version` in the response |
| two features missing | **400**, `{"error":"missing features","missing":[...]}` |
| a string where a float belongs | **400**, `{"error":"features must be numeric"}` |

> **Returning 400 with a reason — rather than a 500, or a confidently wrong
> prediction on garbage input — is the difference.** The model itself is three
> lines of that file.

**Also required:** a health endpoint, a version string in the response,
structured logging, and a latency budget.
</details>

### Q14. What is a metric gate and why does an ML pipeline need one? *(5 marks)*

<details><summary>Solution</summary>

**A CI step that fails the build when the trained model is not good enough.**

```python
if metrics["auc"] < MIN_AUC:
    sys.exit(f"AUC {metrics['auc']:.4f} below threshold")
```

> **This is what makes it an *ML* pipeline rather than a software one.**
> Ordinary CI asks "does the code work?". ML CI must also ask **"is the model
> good enough?"** — a pipeline can run perfectly and produce a model worse
> than the one in production.

**Compare against the current production model, not a fixed number.**

**And the prerequisite:** the training must be **deterministic**, or the
metric moves between runs and the gate becomes a coin toss. That is exactly
what `07_mlflow_dvc.py` verifies.
</details>

### Q15. Compare canary, blue-green, A/B and shadow deployment. *(6 marks)*

<details><summary>Solution</summary>

| Strategy | Mechanism | Risk |
|---|---|---|
| **Blue-green** | two environments, switch traffic | low — instant rollback |
| **Canary** | 1% → 10% → 100%, watching errors | **low — the default for anything risky** |
| **A/B test** | split traffic, compare a **business** metric | needs statistical power |
| **Shadow** | run both, log both, **serve only the old one** | **zero** |

**Shadow is the one to know beyond the syllabus.** Running the new model on
real production traffic while serving the old one's answer is the only way to
see production behaviour at **zero user risk** — you find the training/serving
skew, the unexpected nulls and the latency problem before anybody is affected.

**The A/B trap:** you are testing a **business outcome**, not an accuracy. A
model with better AUC can produce worse revenue.
</details>

### Q16. Explain the requirements-before-code ordering in a Dockerfile. *(4 marks)*

<details><summary>Solution</summary>

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py model.pkl ./
```

**Docker caches each layer and invalidates every layer after the first
change.** Copying the code *before* installing means a one-line edit
invalidates the `pip install` layer and reinstalls everything.

With this ordering, **the expensive layer is rebuilt only when the
dependencies change.**

**And the related trap:** without a `.dockerignore`, `COPY . .` ships the
whole `.git` directory and every cached dataset as build context — a 40 MB
project becomes a 2 GB build.
</details>

### Q17. Distinguish readiness and liveness probes. What goes wrong if you swap them? *(5 marks)*

<details><summary>Solution</summary>

| Probe | Question | Failing it means |
|---|---|---|
| **Readiness** | should this pod receive traffic? | **removed from the load balancer** |
| **Liveness** | is this pod broken? | **restarted** |

**Swapping them gives you a pod that is restarted every time it is briefly
slow**, which turns a latency spike into an outage — the restart drops
in-flight requests and the replacement starts cold, making the latency worse.

**Related:** `resources.requests` is what the scheduler reserves; `limits` is
where the container is **killed**. A container with no memory limit can take
down its node, and an ML container loading a large model is exactly the kind
that does.
</details>

---

## Unit 5 — Monitoring and governance

### Q18. Distinguish data drift, concept drift and label drift. Which can you detect early? *(6 marks)*

<details><summary>Solution</summary>

| Kind | What changes | Detectable from | Effect on accuracy |
|---|---|---|---|
| **Data drift** | **P(X)** — the inputs | **the inputs alone, immediately** | often none |
| **Concept drift** | **P(y\|X)** — the relationship | **labels only** | **direct — the damaging one** |
| **Label drift** | **P(y)** — the base rate | labels | depends |

> **The asymmetry that defines production monitoring:** data drift is
> detectable immediately and often harmless; concept drift is damaging and
> **cannot be detected without labels** — which in lending arrive months later.
>
> **So you monitor what you can see as a proxy for what you cannot.**
</details>

### Q19. An automatic retraining loop fires four times and improves accuracy by 0.0016. Explain. *(6 marks)*

<details><summary>Solution</summary>

| | Mean accuracy |
|---|---|
| static model | 0.7116 |
| retraining model | 0.7132 |

**The drift shifted P(X) — incomes moved up. It did not shift P(y|X)** —
the generating coefficients were unchanged. **A model that learned the true
relationship is still correct on shifted inputs.**

That is why `12_serve_drift_govern.py` also reports accuracy on the *drifted*
batches as slightly **higher** (0.7172) than on the clean ones (0.7060).

> **The operational rule: alert on data drift, INVESTIGATE, and retrain only
> if the labels confirm the relationship moved.** Retraining on every input
> shift is expensive and can make things worse — you fit a smaller, more
> recent, noisier window.
</details>

### Q20. Give the PSI thresholds and explain why PSI is preferred to a KS test. *(6 marks)*

<details><summary>Solution</summary>

| PSI | Reading |
|---|---|
| < 0.1 | no significant change |
| **0.1 – 0.2** | moderate — investigate |
| **> 0.2** | **significant — act** |

**Why PSI rather than KS:** the KS test gives a **p-value**, and with enough
samples any shift is statistically significant.

From `12_serve_drift_govern.py`:

| Batch | True drift | **KS p** | **PSI** | Alert |
|---|---|---|---|---|
| 5 | 0.30 | **0.0000** | 0.1255 | — |
| 6 | 0.60 | 0.0000 | **0.5540** | **YES** |

**The KS p-value hits 0.0000 at batch 5**, detecting a shift far too small to
matter operationally.

> **Statistical significance is not operational significance.** PSI measures a
> **magnitude**, so a threshold on it means something. This is the same point
> Course 4 makes about p-values and effect sizes.

**Result: 4 of 5 drifted batches caught, 0 false alarms, one-batch lag** —
and every detector trades lag against false alarms.
</details>

### Q21. Why is GDPR Article 17 hard for a trained model, and what is the practical answer? *(6 marks)*

<details><summary>Solution</summary>

**Article 17 is the right to erasure.**

**Deleting the row from the database is easy. The model trained on that row
still contains information derived from it**, and there is **no way to
subtract one example from fitted coefficients.**

**The practical answer: retrain on a schedule from current data**, so an
erased record leaves the model within one retraining cycle.

> **Which means your retraining pipeline is a compliance control, not just an
> accuracy one.** That is not obvious and it is exactly the kind of connection
> an examiner is looking for.

**Related, Article 22:** a decision with legal effect — a loan approval is one
— requires a **human review route** and an **explanation**. That constrains
model choice *before* you fit anything: logistic regression can tell an
applicant which factors weighed against them; a deep ensemble cannot.
</details>

### Q22. A model shows approval rates of 0.4049, 0.4150, 0.4374 and 0.4087 across four regions, and region is not an input. Is the model biased? *(6 marks)*

<details><summary>Solution</summary>

**You cannot tell from this table, and saying so is the correct answer.**

In `12_serve_drift_govern.py` the regions were **generated from the same
distribution**, so the spread of **0.0325 is sampling noise** — and knowing
that is only possible because the data was constructed.

**On real data the same table would not tell you either.** A spread could be:

1. sampling noise,
2. a genuine difference in the applicant pool, or
3. the model.

> **Deciding which is not a statistical question — it needs the domain.**

**And note that excluding the protected attribute does not prevent bias.**
Proxies remain: a postcode, an employer, a name. Removing `region` from the
feature list removes your ability to *measure* the disparity, not the
disparity.
</details>

### Q23. Why must latency be a histogram rather than a gauge? *(4 marks)*

<details><summary>Solution</summary>

**A gauge holding "the mean latency" cannot be aggregated.**

Averaging the means of four instances is **not** the mean — it is only correct
if all four served identical request counts. And **p95 cannot be recovered
from a mean at all.**

**A histogram ships bucket counts**, which sum correctly across instances, and
`histogram_quantile()` computes the percentile over the summed buckets.

`12_serve_drift_govern.py` uses a gauge for simplicity and its output **says
`gauge` honestly** — that is a simplification, not a recommendation.
</details>

### Q24. What does `for: 10m` do in a Prometheus alert, and why does it matter? *(4 marks)*

<details><summary>Solution</summary>

**It requires the condition to hold continuously for ten minutes before the
alert fires.**

**Without it, one slow request pages somebody at 03:00.**

> Choosing it is the whole craft of alerting: **too short and you train people
> to ignore alerts; too long and you find out from a customer.**

**Drift alerts use `for: 1h`** — drift is a slow phenomenon and one noisy
batch should not page anyone.
</details>

---

## Long-answer questions

### L1. Design the MLOps setup for a loan-approval model. *(15 marks)*

<details><summary>Solution outline</summary>

**1. Data.** Versioned with DVC alongside the code. Validation before every
training run: schema, ranges, null rates, distribution, volume.

**2. Training.** Deterministic — pin the code, the data, the environment and
**both** random states. Track every run in MLflow with parameters, metrics
**including the train/test gap**, and the git commit.

**3. Model choice constrained by regulation.** A loan approval has legal
effect under Article 22, so it must be **explainable and appealable**.
Logistic regression can answer "why"; that constraint comes before accuracy.

**4. CI/CD.** Lint → test → validate data → train → **metric gate against the
current production model** → build → deploy behind a manual approval. Never
deploy from a pull request.

**5. Serving.** A REST endpoint with input validation returning **400 with a
reason**, a version string in every response, a health endpoint, and
structured JSON logs carrying a hashed subject id.

**6. Release.** Shadow first, then canary at 1%, watching error rate and the
**prediction distribution**.

**7. Monitoring.** PSI per feature against the training distribution, alerting
above 0.2 with `for: 1h`. Plus latency as a **histogram**, error rate, and the
panel nobody builds — the **approval rate over time**.

**8. Feedback.** Drift alert → **human investigation** → wait for labels →
retrain on a window → validate against the incumbent → shadow → deploy.

**9. Governance.** A model card with **per-group metrics**; a named owner; an
appeal route; a retention policy; and scheduled retraining as the **Article 17
erasure mechanism**.

**10. The honest caveat.** Retraining on data drift alone may not help — the
lab measured **+0.0016** — so the loop must gate on labels, not on PSI alone.
</details>

### L2. "Automating retraining is the goal of MLOps." Discuss. *(15 marks)*

<details><summary>Solution outline</summary>

**The claim is a reasonable target and a poor summary, and the measurements in
this course say why.**

**Where it holds.** Manual retraining does not happen. A model degrades slowly
and nobody notices until a business metric moves, so the automation of
*monitoring* and the plumbing of retraining is real progress.

**Where it fails:**

| Objection | Evidence |
|---|---|
| **Retraining on drift may not help** | the lab's loop fired four times for **+0.0016**, because P(X) moved and P(y\|X) did not |
| **The alert is often an upstream bug** | a unit switched from rupees to thousands; retraining bakes the bug in |
| **Labels are late and partial** | you only learn outcomes for applications you **approved** — the model's own decisions shape its next training set |
| **Some retraining is a compliance act** | Article 17 erasure, which has nothing to do with accuracy |

**The reframing that earns the marks:** the goal of MLOps is **not automation
but knowing whether the system still works** — reproducibility, monitoring,
governance and the ability to roll back. Automation is one means to that end
and is actively harmful when it removes the human from step 3.

> **The honest summary: automate the detection, keep a human in the
> decision.**
</details>

---

## Quick self-test

| # | Question | Unit |
|---|---|---|
| 1 | Name the five undercurrents | 1 |
| 2 | Why did ELT displace ETL? | 1 |
| 3 | What was the ETL job wrong by, and why is that worse than a big error? | 1 |
| 4 | Downtime per year at 99.9%? | 2 |
| 5 | What does RPO measure? | 2 |
| 6 | Why are microservices slower, and what do they buy? | 2 |
| 7 | Which is larger in a TCO than the licence fee? | 2 |
| 8 | What is training/serving skew? | 3 |
| 9 | The four things that must be pinned | 3 |
| 10 | What does git store when you `dvc add` a file? | 3 |
| 11 | Why log the train score as well as the test score? | 3 |
| 12 | What makes a CI pipeline an *ML* pipeline? | 4 |
| 13 | Which deployment strategy has zero user risk? | 4 |
| 14 | Readiness or liveness — which restarts the pod? | 4 |
| 15 | Which drift is undetectable without labels? | 5 |
| 16 | PSI threshold for "act" | 5 |
| 17 | Why not use a KS p-value as the drift alarm? | 5 |
| 18 | Why is GDPR Article 17 hard for a model? | 5 |
| 19 | Why can't latency be a gauge? | 5 |
| 20 | Which feedback-loop step must stay human? | 5 |
