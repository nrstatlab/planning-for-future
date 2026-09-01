# Course 15 B — Laboratory

**16 practicals**

Every number on this page was **printed by code in this repository**:

```bash
python3 tools/run_mlops_labs.py
```

---

## What ran, and what did not

**Eleven of the sixteen experiments run against the real tools.**

| # | Experiment | File | Status |
|---|---|---|---|
| 1 | Configure the environment | `01_environment_etl.py` | **runs** |
| 2 | Explore the data lifecycle | `01_environment_etl.py` | **runs** |
| 3 | ETL: CSV/JSON → relational database | `01_environment_etl.py` | **runs — real SQLite** |
| 4 | Batch vs event-driven ingestion | `04_kafka_rabbitmq.md` | ***NOT EXECUTED*** — needs a broker |
| 5 | HDFS operations | `05_hdfs.md` | ***NOT EXECUTED*** — needs a JVM and a NameNode |
| 6 | Microservices vs monolith | `01_environment_etl.py` | **runs — and is timed** |
| 7 | EDA + MLflow tracking | `07_mlflow_dvc.py` | **runs — real MLflow 3** |
| 8 | Reproducibility under version control | `07_mlflow_dvc.py` | **runs — real git** |
| 9 | Dataset versioning with DVC | `07_mlflow_dvc.py` | **runs — real DVC** |
| 10 | Containerize with Docker | `10_docker.md` | ***NOT EXECUTED*** — no daemon |
| 11 | GitHub Actions CI/CD | `11_github_actions.md` | ***NOT EXECUTED*** — needs a runner |
| 12 | Deploy as a REST API | `12_serve_drift_govern.py` | **runs — real Flask on a real socket** |
| 13 | Drift detection | `12_serve_drift_govern.py` | **runs — and is scored** |
| 14 | Feedback loop and retraining | `12_serve_drift_govern.py` | **runs** |
| 15 | Prometheus / Grafana | `15_prometheus_grafana.md` | ***NOT EXECUTED*** — both are servers |
| 16 | GDPR / Responsible AI audit | `12_serve_drift_govern.py` | **runs** |

Each blocked file names a runnable half, and
`04_batch_vs_event.py` implements experiment 4's comparison over a real
in-process queue. `tools/run_mlops_labs.py` asserts all five
`*** NOT EXECUTED ***` markers survive.

---

## Experiment 1 — the environment

| Component | Version | For |
|---|---|---|
| Python | 3.11 | the runtime |
| pandas | 2.3.3 | transformation |
| scikit-learn | 1.9.0 | the model |
| scipy | 1.17.1 | the drift tests |
| sqlite3 | — | the warehouse, **with real constraints** |
| **mlflow** | **3.15.2** | experiment 7 |
| **dvc** | **3.67.1** | experiment 9 |
| flask | 3.1.3 | experiment 12 |

**Pin these with `==`, not `>=`.** An unpinned environment is not
reproducible, and "it worked on my machine" is the failure this course exists
to prevent.

---

## Experiment 2 — the data lifecycle

4,000 loan applications, profiled column by column: dtype, nulls, distinct
count, mean, standard deviation.

**Base rate: 0.4462 approved.** Recorded before anything is fitted, because it
is the majority-class baseline every accuracy figure is read against.

| Data lifecycle | Data **engineering** lifecycle |
|---|---|
| created → stored → used → archived → destroyed | generation → storage → ingestion → transformation → serving |
| about the **data** | about the **pipeline** |

With five **undercurrents** running underneath every stage: security, data
management, DataOps, architecture, orchestration.

---

## Experiment 3 — ETL into a warehouse

Sources: a CSV and a JSON file, **deliberately messy**:

- `south` in lowercase where the rest say `South`
- a price written `Rs 140` with a currency prefix
- order 6 appearing **twice**
- order 10 with a **null** units field

| Stage | Result |
|---|---|
| **EXTRACT** | 8 rows from CSV + 3 from JSON = 11, **all as text** |
| **TRANSFORM** | 11 in, **9 out** — title-cased regions, stripped prefixes, dropped 1 null and 1 duplicate |
| **LOAD** | 9 rows into a star schema, 1 fact + 2 dimensions |

| Region | Revenue |
|---|---|
| **South** | **₹10,360** |
| North | ₹2,520 |

### ⚠️ The naive total, with no cleaning: ₹10,500

**Wrong by ₹140 — about one percent — and nothing raised an error.**

Three defects worth **−₹1,680, −₹700 and +₹2,520 nearly cancelled.**

> **That is the dangerous case.** A figure that is wildly wrong gets noticed;
> a figure that is 1% wrong gets reported to the board. The errors cancelled
> by luck, and next month they will not.

### The constraints are not decoration

| Attempted insert | Result |
|---|---|
| `units = 0` | **rejected — IntegrityError** |
| unknown `region_id` | **rejected — IntegrityError** |
| duplicate `order_id` | **rejected — IntegrityError** |

**Put the constraints in the database, not only in the pipeline.** The
database is the last line of defence against every *other* program that will
ever write to it.

### 🎯 Cross-course check

**₹10,360 is the same South total** that Course 11 computes in DAX,
Course 12 B in Hive and in Spark, and Course 13 B in its warehouse. **Five
independent engines agree** — which is worth more than any one of them being
carefully written.

---

## Experiment 4 — batch against event-driven

300 records, 2 ms of work each, arriving every 3 ms; batch interval 250 ms.

| Mode | Wall clock | **p50 latency** | p95 | max |
|---|---|---|---|---|
| **batch** | 1.38 s | **355.4 ms** | 519.8 ms | 535.3 ms |
| **event-driven** | 0.94 s | **2.2 ms** | 2.3 ms | 2.5 ms |

**Batch median latency is about 160× the event-driven one**, because a batch
record waits for the next tick.

> **The wall-clock difference is an artefact of polling, not a throughput
> result** — the batch loop sleeps a full interval before checking. Real batch
> systems amortise setup across the batch and usually win on per-record
> *cost*; this toy does not model that, and claiming it did would be
> dishonest.

The real Kafka and RabbitMQ code — with `acks`, consumer groups, offset replay
and delivery semantics — is in
`04_kafka_rabbitmq.md`.

---

## Experiment 6 — monolith against microservices

Same three units of work, 40 applications:

| | Result |
|---|---|
| **monolith** | faster |
| **microservices** | **slower — every boundary is a network hop** |

**Microservices are slower for the same work.** What you buy is independent
deployment and independent scaling:

| Strategy | Instances | Wasted capacity |
|---|---|---|
| monolith, scaled 4× | 4 | **4× of every component** |
| microservices, scale the scorer 4× | 4 + 1 + 1 | **none** |

**And the row that surprises people:** one database per service, so **a join
you used to write in SQL becomes an API call and an in-memory merge.**

---

## Experiment 7 — MLflow

Six runs logged to a **SQLite** backend (MLflow 3 refuses the old file store)
and queried back, ordered by AUC.

| Run | Accuracy | AUC | **Train − test gap** |
|---|---|---|---|
| **baseline-majority** | **0.5540** | 0.5000 | −0.0003 |
| **logreg-C0.01** | 0.7060 | **0.7752** | −0.0083 |
| logreg-C1 | 0.7080 | 0.7752 | −0.0100 |
| logreg-C100 | 0.7080 | 0.7752 | −0.0100 |
| rf-depth3 | 0.6880 | 0.7526 | 0.0153 |
| **rf-depth12** | 0.6850 | 0.7463 | **0.2783** |

**`rf-depth12` has a gap of 0.2783 — it memorised the training set.** The gap
column is the only thing in the table that says *why* a model underperformed,
and it costs one extra `log_metric` call.

---

## Experiment 8 — reproducibility

The pinned pipeline, run **twice**:

| | AUC |
|---|---|
| run 1 | **0.793326** |
| run 2 | **0.793326** |
| identical | **True** |

### The fitted coefficients against the **known** truth

| Feature | Fitted | True | Error |
|---|---|---|---|
| income | 0.8749 | 0.9000 | −0.0251 |
| loan_amount | −0.6898 | −0.7000 | +0.0102 |
| credit_years | 0.4542 | 0.5000 | −0.0458 |

**A model that converges has proved nothing. A model that recovers the
parameters which produced the data has.**

### ⚠️ And the failure, demonstrated

The same code with **only the split's `random_state` removed**, run three
times: **three different AUCs.**

The model was still seeded. That is enough to make every number in a report
unrepeatable, and it is **the most common reproducibility bug in student
projects.**

### The four things that must be pinned

| # | Pin | How |
|---|---|---|
| 1 | the **code** | a git commit |
| 2 | the **data** | a seed, or DVC |
| 3 | the **environment** | `requirements.txt` with `==` |
| 4 | the **randomness** | `random_state` on the estimator **and the split** |

---

## Experiment 9 — DVC

| Step | Result |
|---|---|
| `dvc add data/applicants.csv` | git tracks `applicants.csv.dvc`, **a few hundred bytes** |
| `git ls-files` | contains the `.dvc` pointer, **not the CSV** |
| commit v2 (drifted data) | a **different md5** in the pointer |
| `git checkout <v1>` + `dvc checkout` | **income mean back to −0.0195** from v2's 1.4805 |

**Git tracks the pointer, not the data.**

| | git alone | **git + DVC** |
|---|---|---|
| Stores | every version in full | a hash; data in a cache |
| Repo size | grows with every data change | **stays small** |
| Reproduce | code only | **code AND data** |

---

## Experiment 12 — the REST API

A **real Flask server on a real socket**, called over HTTP:

| Request | Status | Response |
|---|---|---|
| `GET /health` | **200** | `{"status":"ok","model":"logreg",...}` |
| `POST /predict`, valid | **200** | `{"approved":true,"probability":0.836858,"model_version":"1.0.0"}` |
| `POST /predict`, 2 features missing | **400** | `{"error":"missing features","missing":["loan_amount","credit_years"]}` |
| `POST /predict`, a string for a float | **400** | `{"error":"features must be numeric"}` |

**The two error cases are the experiment.** Returning 400 with a reason —
rather than a 500 or a confidently wrong prediction — is what separates a demo
from a service.

### `/metrics`, in Prometheus exposition format

```
model_requests_total 3
model_errors_total 2
model_latency_seconds 0.160414
```

**Parsed back and verified: 3 metrics.** This is experiment 15's runnable
half.

---

## Experiment 13 — drift detection, scored

Ten daily batches of 500. Batches 0–4 clean; income shifts from batch 5,
ramping to 1.5 sd.

| Batch | True drift | KS p | **PSI** | Accuracy | Alert |
|---|---|---|---|---|---|
| 0 | 0.00 | 0.9132 | 0.0125 | 0.7360 | — |
| 4 | 0.00 | 0.5758 | 0.0169 | 0.6960 | — |
| **5** | 0.30 | **0.0000** | 0.1255 | 0.6840 | — |
| **6** | 0.60 | 0.0000 | **0.5540** | 0.7060 | **YES** |
| 9 | 1.50 | 0.0000 | 2.1407 | 0.7460 | YES |

**4 of 5 drifted batches caught, 0 false alarms, one-batch lag.**

> **Statistical significance is not operational significance.** The KS
> p-value hits 0.0000 at batch 5, long before PSI crosses 0.2 — with 500
> samples, KS detects a shift far too small to matter. That is why the
> industry uses PSI with a magnitude threshold.

**Accuracy on clean batches 0.7060, on drifted 0.7172** — the drifted batches
scored *higher*, which experiment 14 explains.

---

## Experiment 14 — the retraining loop

Retrained at batches **6, 7, 8, 9**.

| | Mean accuracy |
|---|---|
| static model | 0.7116 |
| retraining model | 0.7132 |
| **difference** | **+0.0016** |

> ### ⚠️ Retraining barely helped, and that is the result
>
> The drift shifted **P(X)** — incomes moved. **P(y|X)** did not, because the
> generating coefficients are unchanged. **A model that learned the true
> relationship is still correct on shifted inputs.**
>
> **Alert on data drift, investigate, and retrain only if the labels confirm
> the relationship moved.**

---

## Experiment 16 — the GDPR and fairness audit

Region is **not** a model input, and the approval rates still differ:

| Region | n | Approval rate | True rate | Accuracy |
|---|---|---|---|---|
| East | 1,561 | 0.4049 | 0.4504 | 0.7047 |
| North | 1,453 | 0.4150 | 0.4611 | 0.7378 |
| **South** | 1,518 | **0.4374** | 0.4690 | 0.7128 |
| **West** | 1,468 | **0.4087** | 0.4496 | 0.7003 |

**Spread: 0.0325.**

> **That is the control condition.** The regions were drawn from the same
> distribution, so the spread is **sampling noise, not bias** — and knowing
> that is only possible because the data was constructed. **On real data the
> same table would not tell you either.**

Plus the GDPR article-by-article audit, with **Article 17** identified as the
one that breaks ML systems, and the facial-recognition case analysed in five
rows.

---

## Running it yourself

```bash
pip install -r tools/requirements.txt
python3 tools/run_mlops_labs.py
```

MLflow, git and DVC all write to a temporary directory that is removed
afterwards. The whole suite takes about a minute.
