# Unit 5 — Training and Deployment of ML on the Cloud

**Syllabus topics:** Factors for selecting cloud ML platforms: ETL/ELT
pipeline support, scale-up/scale-out training, ML frameworks, pre-tuned
services. Steps for training ML models in the cloud: data source
identification, feature engineering, training, validation, deployment,
monitoring. Monitoring and improving cloud-deployed ML models. Case studies
and industry applications.

---

## 5.1 Factors for selecting cloud ML platforms

The syllabus names four factors. Each is a real question with a real answer.

### 1. ETL/ELT pipeline support

**Can the platform get the data to the model without you writing a
pipeline?**

| Question | Why it matters |
|---|---|
| Does it read your warehouse natively? | Vertex reads BigQuery directly; SageMaker needs an export |
| Is there a managed transform service? | Glue, Data Factory, Dataflow |
| Can training read from object storage in place? | otherwise every job starts with a copy |
| Is there a **feature store**? | one definition, served to training *and* serving |

**The deciding question is where your data already lives.** A team on BigQuery
has a real reason to prefer Vertex; a team on S3 has a real reason to prefer
SageMaker. That is a better answer than a feature comparison.

### 2. Scale-up against scale-out

| | **Scale UP** | **Scale OUT** |
|---|---|---|
| Means | a bigger machine | more machines |
| Good for | data that fits in RAM; most tabular ML | data that does not; deep learning |
| Code changes | **none** | distributed training, sharding, all-reduce |
| Efficiency | **near-perfect** | sub-linear — communication overhead |
| Fails at | the largest instance available | never, but with diminishing returns |

### 🎯 Scale up first, and much further than you expect

**A single cloud instance can have 24 TB of RAM and 128 cores.** Most "we need
distributed training" conversations are really "our dataset is 40 GB and we
have not tried a bigger machine".

**Distributed training costs code complexity and communication overhead**, and
below a few hundred gigabytes it usually loses to one large machine.
Course 12 B's Spark makes the same point from the other direction.

### 3. ML frameworks — version and container support

| Ask | Because |
|---|---|
| Which framework **versions** are pinned? | your code targets one, and the platform may not have it |
| Can you bring your own container? | the escape hatch when the answer is no |
| Is there a managed distributed-training story? | Horovod, DDP, or their own |
| Does inference support your format? | ONNX, TorchScript, a `.joblib` |

**"Bring your own container" is the row that matters**, because it is the
answer to every future incompatibility — at the cost of maintaining the
container.

### 4. Pre-tuned services

**Does a good-enough model already exist?** Unit 4's AIaaS discussion applies:
generic tasks are already solved better than you will solve them, and specific
ones are not.

### ⚠️ And the factor the syllabus omits

**Lock-in, and the cost of leaving.** A SageMaker Pipeline does not run on
Vertex. The mitigations are ordinary engineering: keep the training code in a
plain container, keep the data in an open format (Parquet), keep the artefact
in an open format (ONNX or joblib), and treat the platform as a scheduler.

---

## 5.2 The six steps

The syllabus lists them. Here is what actually goes wrong at each.

```
  1. IDENTIFY      2. ENGINEER     3. TRAIN      4. VALIDATE
     the data         features        the model     it
        │                │               │             │
        └────────────────┴───────────────┴─────────────┘
                              │
                    5. DEPLOY  →  6. MONITOR
                              ↑          │
                              └──────────┘
                             (and retrain)
```

### Step 1 — Data source identification

| Do | Why |
|---|---|
| Find where it **already** lives | moving data is the expensive part |
| Check **freshness** — how late is the newest row? | it caps how current the model can be |
| Check **access** — an IAM role, not keys | the notebook must not hold credentials |
| Check **legality** — residency, consent, retention | this cannot be fixed later |

**And the one that ends projects:** *does a label exist?* An enormous number
of "machine learning projects" are really "we would need to label 50,000
examples first" projects, and discovering that in week six is expensive.

### Step 2 — Feature engineering

**This is where the time goes, and it is Course 12 A's material unchanged.**

The cloud-specific additions:

- **Compute features where the data is.** A `GROUP BY` in the warehouse beats
  exporting a terabyte and doing it in pandas.
- **Use a feature store** if one exists, for the training/serving skew reason.
- **Version the feature definitions** with the model. A model is only
  reproducible if its inputs are.

### ⚠️ Step 2 is also where leakage happens

**Any feature computed using information not available at prediction time is
leakage** — and in a cloud pipeline it is easy to introduce, because the
training job reads a warehouse table that has been updated since.

The classic form: a feature like `total_orders_this_month` computed from a
table that already includes the outcome month. **The model scores brilliantly
and fails in production**, and no infrastructure metric will tell you.

### Step 3 — Training

The job is declarative:

```python
estimator = SKLearn(entry_point="train.py", role=role,
                    instance_type="ml.m5.xlarge",
                    hyperparameters={"n_estimators": 100},
                    output_path=f"s3://{bucket}/models/")
estimator.fit({"train": f"s3://{bucket}/train/"})
```

**Three conventions are the whole interface:** hyperparameters arrive as
command-line arguments, channels arrive as environment variables
(`SM_CHANNEL_TRAIN`), and **the model must be written to `SM_MODEL_DIR`**.
Getting the last one wrong is why a job "succeeds" and produces no artefact.

**Spot training** is up to 70% cheaper and interruptible. `max_wait` must
exceed `max_run`, and **without `checkpoint_s3_uri` an interrupted job
restarts from zero** — free money for a 20-minute job, a trap for a 20-hour
one.

### Step 4 — Validation

**Everything from Course 12 A applies**, and the cloud adds nothing except the
temptation to skip it because a leaderboard exists.

The measured baseline, again:

| Model | Accuracy | F1 |
|---|---:|---:|
| `DummyClassifier` | **0.8433** | **0.0000** |
| GradientBoosting | 0.9467 | 0.8095 |

**Quote the dummy. Hold out a test set before preprocessing. Report
cross-validated mean and standard deviation.** In the AutoML run, the top two
models differed by 0.0047 with standard deviations around 0.02 — **inside the
noise**, and not a basis for a decision.

### Step 5 — Deployment

**The artefact is the deliverable.** In
`15_deploy_endpoint.py`
a 138,945-byte model file is written, reloaded and served — and the endpoint's
answers are **identical** to calling the model in-process.

> **That equality is the deployment test worth writing.** Serving must not
> change predictions, and a preprocessing step that lives in your notebook
> rather than in the pipeline is exactly how it does.

**The container contract is two routes:**

| Route | Must |
|---|---|
| `GET /ping` | return 200 quickly, **without running the model** |
| `POST /invocations` | run inference |

**A health check that does real inference marks the container unhealthy
whenever the model is merely slow — and the platform then kills a container
that was working.** A self-inflicted outage, and a classic one.

### 🎯 Three deployment shapes, and the arithmetic

| | **Real-time** | **Serverless** | **Batch transform** |
|---|---|---|---|
| Latency | ms | ms, **after a cold start** | minutes to hours |
| Billed | **per hour, always** | per request | per job |
| Idle cost | **the full instance** | **zero** | zero |
| Good for | steady traffic | spiky or occasional | scoring a whole file |

**An `ml.m5.large` endpoint is about $70/month whether or not anything calls
it.**

And the measured argument for batch:

```
one request of 100 rows :    4.90 ms
100 requests of one row : 181.85 ms   (37x)
```

**37×, and none of it is the model** — it is per-request overhead: HTTP, JSON
parsing, and a NumPy call whose fixed cost is paid 100 times instead of once.
**If you are scoring a million rows, calling an endpoint a million times is
the expensive way to do arithmetic.**

### ⚠️ And the error codes matter operationally

Every malformed request in the lab returns a **4xx, not a 5xx**:

| Case | Status |
|---|---:|
| wrong feature count | 400 |
| body not a list | 400 |
| empty body | 400 |
| wrong route | 404 |

**5xx means *your* service is broken and should page someone.** If malformed
client input returns 500, your error alarm fires for other people's bugs and
you stop trusting it.

### Step 6 — Monitoring

Covered in §5.3.

---

## 5.3 Monitoring, alarms and autoscaling

### 🔢 Alarm on the tail, not the mean

Twenty request latencies, one of them 900 ms:

```
mean 85.0 ms   p50 42.0 ms   p95 87.8 ms   p99 737.5 ms
```

**An alarm on the mean never fires.** One request in twenty took 900 ms and
the average absorbed it. **Alarm on p95 or p99, because the tail is where
users live** — and 5% of requests is a lot of users.

### The six metrics worth alarming on

| Metric | Alarm when | The trap |
|---|---|---|
| `ModelLatency` p99 | > 500 ms for 3 min | the mean hides it; the unit is **microseconds** |
| `Invocation5XXErrors` | > 0 for 1 min | these are **yours** |
| `Invocation4XXErrors` | > 1% of requests | a **rate**, never a raw count |
| `CPUUtilization` | > 70% for 5 min | an I/O-bound app never reaches it |
| `EstimatedCharges` | > your budget | lags ~6 h, `us-east-1` only |
| **`Invocations` == 0** | for 1 hour | **a dead endpoint still bills** |

### 💡 The last row is the one people miss

**An endpoint serving nothing looks perfect on every performance metric and
costs exactly the same as a busy one.** Alarm on the **absence** of traffic,
and alarm on **spend** — those two catch the failures that performance
dashboards are blind to.

### 🔢 Autoscaling, measured honestly

A day of traffic (peak 1,000 req/s, trough 164), instances serving 150 req/s
each, in
`13_monitoring_autoscale.py`:

| Strategy | Instance-hours | Dropped |
|---|---:|---:|
| fixed at peak (7 instances) | **168** | **0** |
| autoscaled, out at 70% / in at 40% | **129** | **1,014** |

**Autoscaling saved 23% of the instance-hours and dropped 1,014 requests.**

The worst hour is hour 9, where demand jumped to 1,000 against 4 instances —
**the group was sized for the previous hour**.

> **Autoscaling does not track demand. It CHASES demand, and it is always one
> observation behind.**

### 🔢 The tuning curve, and the result that is not flattering

| Out/in | Cooldown | Instance-hours | Dropped | Changes |
|---|---:|---:|---:|---:|
| 70%/40% | 1 | 129 | 1,014 | 8 |
| 50%/30% | 1 | 158 | 358 | 10 |
| 85%/60% | 1 | **114** | **1,380** | 7 |
| 70%/40% | 3 | **96** | **2,093** | **4** |
| **50%/30%** | **0** | **188** | **0** | 11 |

**Read the last row against fixed capacity.** Scaling out at 50% with no
cooldown drops nothing — and costs **188 instance-hours against fixed
capacity's 168**.

> **Autoscaling made it MORE expensive.** Chase demand hard enough and the
> group overshoots on the way up and lingers on the way down, so you buy more
> than the peak.

**"Autoscaling saves money" is a claim about a *tuned* autoscaler, not about
autoscaling.**

**And the cooldown row:** 3 ticks gives 4 scaling changes instead of 8, at
+1,079 dropped requests. A long cooldown stops **flapping** — scaling out and
back in repeatedly around a threshold — which costs boot time and stabilises
nothing.

**Scale out eagerly (short cooldown), scale in reluctantly (long cooldown).**

### 🔢 And what the day cost

| | Per month |
|---|---:|
| fixed at peak, on-demand | $483.84 |
| autoscaled, on-demand | $371.52 |
| fixed, **reserved** (−40%) | $290.30 |
| autoscaled, **spot** (−70%) | **$111.46** |

**The real answer is usually both:** a **reserved baseline** for the floor you
always need, plus **autoscaled on-demand or spot** for the peak. That beats
either pure strategy — which is why every cost-optimisation review starts by
asking what your floor is.

---

## 5.4 Improving a deployed model

### ⚠️ The failure that has no error message

**A model does not break. It decays.** The endpoint keeps returning 200 and
the predictions quietly stop being right.

| Kind of drift | What changed | Detect by |
|---|---|---|
| **Data drift** | the input distribution | compare production inputs to the training baseline |
| **Concept drift** | the input→output relationship | monitor the metric, once labels arrive |
| **Upstream change** | a column's meaning or units | schema and range checks |
| **Feedback loop** | the model changed the world it predicts | hold out a control group |

### 🎯 The feedback loop is the subtle one

A churn model triggers retention offers; the customers it flags stop
churning; the model now looks wrong and the training data no longer contains
the behaviour it was built to detect. **The intervention destroyed the
signal.**

**The only reliable answer is a holdout group** who receive no intervention —
which is an ethical and commercial decision, not a technical one.

### Model Monitor, in outline

```python
monitor.suggest_baseline(baseline_dataset="s3://bucket/train/train.csv")
monitor.create_monitoring_schedule(endpoint_input=predictor.endpoint_name,
                                   schedule_cron_expression="cron(0 * ? * * *)")
```

**Baseline the training distribution, then compare production inputs against
it hourly.** A drift alarm is the only thing that catches a model that has
stopped working while every infrastructure metric stays green.

### Retraining

| Trigger | Suits |
|---|---|
| **Scheduled** (weekly, monthly) | stable domains; simple, predictable |
| **Drift-triggered** | volatile domains; needs a reliable drift signal |
| **Performance-triggered** | when labels arrive quickly enough to measure |
| Never | a model nobody is accountable for |

**And retraining must be a pipeline, not a person.** If retraining is a
notebook someone runs, it will stop happening when that person changes team.

**Deploy the retrained model with a canary**, and Unit 1's requirement
applies: a canary needs a metric you trust, which is why monitoring comes
first.

---

## 5.5 Case studies and industry applications

| Industry | Application | The cloud-specific point |
|---|---|---|
| **Retail** | recommendation, demand forecasting | traffic is seasonal; elasticity is the whole argument |
| **Banking** | fraud detection | real-time endpoints, and **explainability is regulated** |
| **Healthcare** | imaging triage, readmission risk | data residency and consent dominate the architecture |
| **Telecom** | churn prediction | the feedback-loop problem, in its clearest form |
| **Manufacturing** | predictive maintenance | streaming from the edge; models often run **on** the edge |
| **Media** | content recommendation | **egress and CDN** are the cost, not the model |
| **Agriculture** | yield prediction from imagery | GPU training, batch inference — never a real-time endpoint |

### 🎯 The pattern across all of them

**The model is rarely the hard part.** The recurring difficulties are:

1. **Getting the data**, legally and freshly
2. **Labels** — who produces them, and how late
3. **Serving latency** against **cost**
4. **Explaining** the decision to whoever must defend it
5. **Noticing when it stops working**

**Points 1, 2, 4 and 5 are not machine-learning problems**, which is why a
good answer to a case-study question spends most of its space on them.

---

## Practice problems

**1. Your endpoint's mean latency is 60 ms and users complain it is slow.
Explain and diagnose.**

**The mean is hiding the tail.** In the measured example, twenty requests with
a mean of 85 ms had a **p99 of 737.5 ms** — one request in twenty took 900 ms.
If 5% of your users wait most of a second, they will complain and the
dashboard will look fine.

**Diagnose:**

1. **Look at p50, p95 and p99, not the mean.**
2. **Separate `ModelLatency` from `OverheadLatency`.** The first is inference;
   the second is the platform's serialisation and routing.
3. **Check for cold starts** if the endpoint is serverless or recently scaled.
4. **Check the payload size.** Large JSON bodies parse slowly, and the
   measured batching result showed per-request overhead dominating the model.
5. **Check garbage collection or model reloading** in the container.

**And fix the alarm**: threshold on p99, and remember `ModelLatency` is in
**microseconds**.

**2. Autoscaling is enabled and your bill went up. How is that possible?**

**Measured, exactly:** the most aggressive configuration (scale out at 50%, no
cooldown) used **188 instance-hours against fixed capacity's 168** — 12% more
— while dropping nothing.

**The mechanism:** a scaling decision takes effect one observation late, so
the group **overshoots on the way up** and, with a short scale-in cooldown,
**oscillates** rather than settling. You end up buying more than the peak,
plus the boot time of every extra instance.

**The fixes:** raise the scale-out threshold, lengthen the scale-in cooldown,
cap `max-capacity`, and — most importantly — **measure**, because the
trade-off curve is specific to your traffic shape.

**3. Design monitoring for a fraud-detection endpoint. What do you alarm on
and why?**

**Infrastructure:**

- `Invocation5XXErrors > 0` for 1 min — a fraud endpoint failing means
  transactions go unchecked
- `ModelLatency` p99 > the payment timeout — a late answer is a missed
  decision
- `Invocations == 0` for 10 min — silence means the caller is broken

**Model:**

- **Input drift** against the training baseline, hourly
- **Score distribution shift** — if the fraction flagged moves sharply,
  something changed upstream
- **Precision on confirmed cases**, weekly — labels arrive late here, so this
  is the lagging indicator

**Business:**

- **Flagged rate** against the historical band — a model flagging 30% instead
  of 0.3% is an incident regardless of what the metrics say

**And the fraud-specific problem:** labels arrive weeks late (chargebacks), so
**you cannot monitor accuracy in real time**. Drift monitoring is not a
convenience here — it is the only fast signal you have.

**4. A model is retrained monthly on the last 12 months of data. What could
go wrong?**

1. **Feedback loops.** If the model's decisions changed behaviour, the last 12
   months contain its own effects. A holdout control group is the only clean
   fix.
2. **A regime change is diluted.** A sharp shift three months ago is a
   quarter of the window; the model averages across a break rather than
   adapting to it.
3. **The retraining pipeline drifts from the serving pipeline.** If features
   are computed differently in the two places, every retrain is trained on a
   distribution it will not see.
4. **Nothing validates the retrained model before it ships.** A monthly
   automatic retrain that deploys without a gate will eventually deploy a
   worse model.
5. **Label latency.** If labels take six weeks, the last six weeks of the
   window are unlabelled or wrongly labelled.

**The mitigations:** a **champion/challenger gate** — the new model must beat
the current one on a held-out set before promotion — a canary rollout, and a
holdout group.

**5. Choose a deployment shape for each: a fraud check during checkout; a
nightly credit score for 20 million customers; a demo used a few times a
week.**

| Case | Shape | Why |
|---|---|---|
| **Fraud at checkout** | **real-time endpoint**, provisioned | latency budget is tens of ms; traffic is steady; a cold start is a lost sale |
| **20 M nightly scores** | **batch transform** | no latency requirement; the 37× batching measurement makes an endpoint indefensible |
| **Occasional demo** | **serverless inference** | idle cost is **zero**; a cold start is acceptable when nobody is waiting on a payment |

**The deciding questions are: what is the latency budget, and what is the
duty cycle?** Steady and urgent → provisioned. Occasional → serverless. No
latency requirement → batch. **An `ml.m5.large` endpoint at $70/month for a
weekly demo is the case this question exists to catch.**

---

## Exam questions from this unit

**Two marks**

1. Name the four factors for selecting a cloud ML platform.
2. Distinguish scale-up from scale-out.
3. Name the six steps of training a model in the cloud.
4. What must a container's `/ping` route not do?
5. Why alarm on p99 rather than the mean?
6. Give one metric that catches a dead endpoint.
7. Distinguish data drift from concept drift.
8. Name the three deployment shapes.

**Five marks**

1. Explain the four platform-selection factors with a question for each.
2. Explain the six steps, and one failure mode at each.
3. Compare real-time, serverless and batch inference with cost figures.
4. Explain autoscaling and why it can increase cost.
5. Explain model drift and how it is detected.

**Ten marks**

1. Describe the full lifecycle of training and deploying a model on the
   cloud, from data source to monitoring, with the failure modes at each step.
2. Design and justify a monitoring and retraining strategy for a
   cloud-deployed churn model, covering infrastructure, model and business
   metrics.

---

## Mistakes that cost marks

- **Distributing training before trying a bigger machine.** One instance can
  have 24 TB of RAM.
- **Running inference in `/ping`.** It kills healthy containers.
- **Alarming on mean latency.** The mean absorbed a 900 ms outlier
  completely.
- **Saying autoscaling saves money**, unqualified. The measured aggressive
  configuration cost 12% more than fixed capacity.
- **Short scale-in cooldowns.** They cause flapping.
- **Calling an endpoint a million times to score a file.** 37× the cost of
  batching, measured.
- **Returning 5xx for a malformed request.** It poisons your error alarm.
- **Forgetting `checkpoint_s3_uri`** on a long spot training job.
- **Treating drift as an infrastructure problem.** Every infrastructure
  metric stays green while the model decays.
- **Forgetting to delete the endpoint.** $70/month, called or not.
