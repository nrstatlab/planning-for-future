# Course 15 B — Data Engineering and MLOps

**Semester VI**

**This is a Track B course**, paired with
Course 14 B (Time Series Analysis), and it is
the last course of the track you began in Semester V.

---

## The one thing to understand before anything else

**Every other course in this programme ends when the model works. This one
starts there.**

| The rest of the programme asks | This course asks |
|---|---|
| does the model fit? | **can somebody else reproduce it?** |
| what is the test accuracy? | **is it still that accurate six months from now?** |
| which algorithm is best? | **what happens at 3 a.m. when it stops responding?** |
| — | **can you delete one person's data from it?** |
| — | **who is accountable when it is wrong?** |

### 🎯 The single most examinable idea

> **A model in production is a system, not an artefact.** It has inputs that
> change, dependencies that drift, users who complain, regulators who ask, and
> an owner who must be nameable. The model file is the smallest part of it.

### ⚠️ The measurement that makes the point

[Experiment 3](lab.md#experiment-3) runs an ETL job on deliberately messy
data. Three defects — a region spelled in lowercase, a price written with a
currency prefix, a duplicated order — produce errors of **−₹1,680, −₹700 and
+₹2,520**, which **nearly cancel**. The uncleaned total comes out at **₹10,500
against a true ₹10,360: wrong by about one percent.**

> **That is the dangerous case.** A figure that is wildly wrong gets noticed;
> a figure that is 1% wrong gets reported to the board. The errors cancelled
> by luck, and next month they will not.
>
> **The only reliable check is an independently computed figure**, which is
> why this repository has five engines agreeing on that number.

---

## What runs here

**Eleven of the sixteen experiments run against the real tools**, not
descriptions of them:

| Tool | What is real here |
|---|---|
| **MLflow 3** | six runs logged to a SQLite backend and **queried back**, ordered by AUC |
| **git + DVC** | two data versions committed, `dvc checkout` restoring the earlier one, verified by comparing the recovered column |
| **Flask** | a server on a real socket, called over HTTP, including both error paths |
| **SQLite** | real constraints, which **reject** the three bad inserts the lab attempts |
| **scipy** | KS test and PSI, scored against drift injected at a known magnitude |

### The five that do not run, and why

| # | Experiment | Reason | Its runnable half |
|---|---|---|---|
| 4 | Kafka / RabbitMQ | needs a **broker process** | `04_batch_vs_event.py` — both modes over a real queue, **latency measured** |
| 5 | HDFS | needs a **JVM and a NameNode** | the ETL job, plus Course 12 B's block arithmetic |
| 10 | Docker | the client is installed; **the daemon is not** | the Flask app the container would package, **running** |
| 11 | GitHub Actions | needs a **GitHub runner** | the determinism check CI exists to protect |
| 15 | Prometheus / Grafana | both are **server processes** | a real `/metrics` endpoint, **parsed back** as valid exposition format |

**None of those halves is filler.** In each case the part that this
environment blocks is the infrastructure, and the part you actually write is
verified.

`tools/run_mlops_labs.py` asserts all five `*** NOT EXECUTED ***` markers are
still present.

### 📖 Why the data is generated

**You cannot verify a drift detector on data whose drift you do not know.**

So the loan dataset here is built from **known coefficients**, and the drift
is **injected at a known magnitude on a known feature at a known time**. That
makes two things checkable that otherwise could only be reported:

| Claim | How it is checked |
|---|---|
| the model fitted correctly | its coefficients are compared against the ones that generated the data |
| the drift detector works | **4 of 5 drifted batches caught, 0 false alarms**, with a one-batch lag |

---

## Course objectives (verbatim)

1. To introduce the lifecycle and roles in Data Engineering.
2. To explore data architecture principles, distributed systems, and technology
   choices.
3. To analyze MLOps features, risks, and challenges in developing ML systems.
4. To design CI/CD pipelines and deployment strategies for ML models.
5. To understand monitoring, governance, and Responsible AI compliance in
   production ML.

## The five units

| Unit | Topic | Notes | Hardest part |
|---|---|---|---|
| 1 | Foundations of data engineering | [unit-1.md](unit-1.md) | the data lifecycle vs the data *engineering* lifecycle |
| 2 | Data architecture and distributed systems | [unit-2.md](unit-2.md) | when microservices are wrong |
| 3 | MLOps fundamentals | [unit-3.md](unit-3.md) | the four things that must be pinned |
| 4 | Deployment and CI/CD | [unit-4.md](unit-4.md) | the metric gate, and canary vs shadow |
| 5 | Monitoring, feedback loops and governance | [unit-5.md](unit-5.md) | why data drift is not concept drift |

Plus [lab.md](lab.md) and [practice.md](practice.md).

---

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 16 practicals
- `labs/course-15b-mlops/` — the code, and the runner that asserts every figure
  these notes quote
- `data/course-15b-mlops/` — **practice datasets**, CSV: `loan-current.csv`, `loan-reference.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.
  Also `sales-transactions.csv` in `data/shared/`, which several courses
  analyse so their answers can be compared.

## The result that surprised the lab

[Experiment 14](lab.md#experiment-14) builds an automatic retraining loop:
detect drift, retrain, deploy. It fires at four batches — and improves
accuracy by **+0.0016**, which is nothing.

> **The reason is the distinction the whole of Unit 5 turns on.** The drift
> shifted **P(X)** — incomes moved up. It did not shift **P(y|X)** — the
> relationship between income and approval was unchanged. **A model that
> learned the true relationship is still correct on shifted inputs.**
>
> So: **alert on data drift, investigate, and retrain only when the labels
> confirm the relationship moved.** Retraining on every input shift is
> expensive and can make things worse.

That is a more useful lesson than a demo where retraining rescues the model,
and it is the honest result of the code as written.

---

## How this course connects to the rest of the programme

| Course | What it gives you here |
|---|---|
| **Course 5** (DBMS) | schemas, keys, constraints — the warehouse in experiment 3 |
| **Course 9** (Python for Data Analysis) | the pipeline and the profiling |
| **Course 12 A** (Machine Learning) | the model being deployed, and the baselines |
| **Course 12 B** (Big Data) | HDFS, Kafka, the distributed layer |
| **Course 13 B** (Cloud Computing) | where all of this is deployed, and what it costs |
| **Course 14 B** (Time Series) | drift is distribution change over time |

**Cross-check:** the South-region revenue total of **₹10,360** is computed
here by a fifth independent engine, after Course 11's DAX, Course 12 B's Hive
and Spark, and Course 13 B's warehouse.

---

## Textbooks

The syllabus prescribes a single combined **Text / Reference** list, and it has
exactly one book in it:

- Reis & Housley, *Fundamentals of Data Engineering*, O'Reilly, 2022 — Units 1
  and 2. The publisher and year are **not** in the syllabus; they are supplied
  here so you can find the book.

**Web resources named in the syllabus:** IBM's data-engineering topic page ·
Martin Fowler on microservices · a *Towards Data Science* introduction to
MLOps.

> ### ⚠️ One incomplete citation, and one resource behind a paywall
>
> The reading list ends "Fundamentals of Data Engineering, Joe Reis & Matt
> Housley**,**" — the trailing comma is where the publisher and year should
> be, and item 2 turns out to be the heading "Web Resources" rather than a
> book. Course 15 B is the only Semester VI course whose students cannot
> locate their single prescribed text from the syllabus alone. See review
> finding **D31**.
>
> *Towards Data Science* moved to a Medium members-only model, so the third
> web resource may be **paywalled**. See review finding **D32**. Google's
> *Practitioners Guide to MLOps* and Microsoft's MLOps documentation cover the
> same ground and are free.

## How to study this course

1. **Run MLflow locally in week 3.** `mlflow ui` against a SQLite backend takes
   five minutes and makes Unit 3 concrete. Reading about experiment tracking
   teaches nothing; losing a good result because you did not track it teaches
   it permanently.
2. **Put one real project under version control, data included.** DVC's whole
   idea — the pointer is in git, the bytes are not — only lands once you have
   seen a repository stay small while the dataset changes.
3. **Learn the lifecycle as a sequence you can name.** Units 1 and 2 are
   vocabulary questions: ingestion, storage, transformation, serving, and the
   architecture choices behind each. They are the easy marks.
4. **Build the smallest possible CI/CD pipeline.** A workflow that runs the
   tests and refuses to deploy when a metric drops is the whole of Unit 4 in
   about thirty lines.
5. **Understand what drift is *not*.** Retraining on the drift in these notes
   gained 0.0016 accuracy, because the inputs moved and the relationship did
   not. Knowing when retraining will not help is the Unit 5 answer worth
   having.
6. **Read Unit 5's governance material properly.** GDPR, CCPA and Responsible
   AI are examinable, they are the part with no code, and they are what makes
   this course different from Course 12 A.

## If you read one thing

**Unit 5's section on the three kinds of drift**, and then run
`12_serve_drift_govern.py`.

Data drift, concept drift and label drift are routinely conflated, they need
different detectors, and only one of them is detectable before the damage is
done. **The experiment demonstrates the distinction rather than asserting
it** — which is why the retraining loop it builds barely helps.
