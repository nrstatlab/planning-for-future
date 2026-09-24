# Unit 1 — Foundations of Data Engineering

**Syllabus topics:** Data engineering: definition, lifecycle, skills,
activities. Evolution and roles of data engineers: technical vs business
responsibilities, internal vs external roles. Relationship between data
engineering and data science. Data lifecycle vs data engineering lifecycle.

---

## 1.1 What data engineering is

### 🎯 The definition to memorise

> **Data engineering is the development, implementation and maintenance of
> systems that take raw data and produce high-quality, consistent information
> that supports downstream use — analytics, machine learning and reporting.**

The load-bearing words are **systems** and **maintenance**. A data scientist's
notebook that produces a correct number once is not data engineering; a
pipeline that produces it correctly every morning at 06:00, with alerts when
it does not, is.

### 📖 The activities

| Activity | What it means |
|---|---|
| **Ingestion** | getting data out of source systems, in batch or as a stream |
| **Storage** | choosing where it lives — warehouse, lake, lakehouse |
| **Transformation** | cleaning, joining, aggregating, modelling |
| **Serving** | making it available to analysts, dashboards and models |
| **Orchestration** | running the steps in order, on a schedule, with retries |
| **Monitoring** | knowing when a pipeline failed, or worse, silently succeeded |

### ⚠️ The last row is the one this course exists for

**A pipeline that crashes is a nuisance. A pipeline that quietly reports the
wrong number is a disaster**, and only a cross-check catches it.

[Experiment 3](lab.md#experiment-3) demonstrates this exactly: three defects
in the source data — a lowercase region, a price with a currency prefix, a
duplicated order — produce a revenue total that is **wrong by 1%** and raises
no error at all.

---

## 1.2 The data lifecycle against the data engineering lifecycle

**This distinction is examined and is routinely confused.**

| | **Data lifecycle** | **Data engineering lifecycle** |
|---|---|---|
| Is about | **the data itself** | **the pipeline that moves it** |
| Stages | created → stored → used → archived → destroyed | generation → storage → ingestion → transformation → serving |
| Ends when | the data is deleted | the data is served |
| Owned by | the business, and the regulator | the data engineering team |

### 📖 The five stages, and what happens in each

| Stage | The question it answers |
|---|---|
| **Generation** | where does the data come from? An application database, an API, a sensor, a file drop |
| **Storage** | where does it rest? And it is not one place — raw, cleaned and served layers differ |
| **Ingestion** | how does it move? **Batch or streaming** — the trade-off [experiment 4](lab.md#experiment-4) measures |
| **Transformation** | what shape does it need to be in? Cleaned, typed, joined, modelled |
| **Serving** | who consumes it? Analytics, dashboards, ML, or another system |

### 🎯 The undercurrents — the part that is easy to skip and gets examined

**Five concerns run underneath every stage rather than sitting between them:**

| Undercurrent | What it means at every stage |
|---|---|
| **Security** | who may read this, at each stage? Encryption at rest and in transit |
| **Data management** | governance, lineage, quality, master data |
| **DataOps** | automation, monitoring, incident response — DevOps for data |
| **Data architecture** | the design decisions of [Unit 2](unit-2.md) |
| **Orchestration** | dependencies, scheduling, retries, backfills |

**Remember the list by asking: what is true of ingestion AND of serving?**
Security is. Orchestration is. That is why they are drawn underneath rather
than in the chain.

---

## 1.3 The evolution of the role

| Era | What the role was |
|---|---|
| 1970s–90s | **DBA and ETL developer** — hand-written pipelines into a warehouse |
| 2000s | **Big data engineer** — Hadoop, MapReduce, scale-out (Course 12 B) |
| 2010s | **Cloud data engineer** — managed services, ELT instead of ETL |
| Now | **Analytics/ML engineer** — the pipeline extends into the model, which is this course |

### 📖 ETL against ELT, which the shift to cloud caused

| | **ETL** | **ELT** |
|---|---|---|
| Order | Extract → **Transform** → Load | Extract → Load → **Transform** |
| Transform happens | in a separate engine, before loading | **in the warehouse, in SQL** |
| Needs | transformation infrastructure | a warehouse that is cheap and fast |
| Raw data kept | usually not | **yes — reprocess without re-extracting** |
| Suits | limited warehouse capacity | cloud warehouses billed by query |

> **ELT won because warehouse compute became cheap and elastic.** Keeping the
> raw data means a transformation bug can be fixed by re-running the
> transformation instead of re-extracting from a source system that may not
> hold the history any more.
>
> **[Experiment 3](lab.md#experiment-3) is deliberately ETL** — transform in
> pandas, load the clean rows — because it is easier to see the steps that
> way. The same job as ELT would load the messy rows and clean them in SQL.

---

## 1.4 The roles and responsibilities, and how they split

| | **Technical** | **Business** |
|---|---|---|
| Does | builds pipelines, models data, tunes queries | gathers requirements, defines metrics, sets SLAs |
| Measures | latency, cost, uptime, freshness | does the number mean what the business thinks? |
| Fails by | a broken pipeline | **a correct pipeline computing the wrong thing** |

### ⚠️ The second failure mode is the expensive one

A pipeline that computes "revenue" correctly according to a definition nobody
agreed is worse than one that crashes, because **it is trusted**. Getting the
definition written down — *is revenue net of returns? which date does it use?*
— is a business responsibility that lands on the engineer.

| | **Internal** | **External** |
|---|---|---|
| Serves | analysts and data scientists in your own organisation | customers, or another company |
| Data | usually trusted at the source | **must be validated — you do not control it** |
| Failure means | a dashboard is stale | a contract is breached |
| SLA | informal | **written, with penalties** |

---

## 1.5 Data engineering and data science

### 🎯 The one-line relationship

> **Data engineering makes the data usable; data science makes it useful.**

| | **Data engineering** | **Data science** |
|---|---|---|
| Optimises for | reliability, cost, freshness | accuracy, insight |
| Output | a pipeline and a table | a model and a finding |
| Time horizon | **runs every day for years** | **an analysis, often once** |
| Cares about | schema changes, retries, backfills | features, algorithms, evaluation |
| Fails by | the pipeline breaks | the conclusion is wrong |

### 📖 The hierarchy-of-needs argument

The much-cited version: **you cannot do machine learning until the data is
collected, cleaned, stored, and reliably available.** Most organisations that
believe they need a data scientist need a data engineer.

### ⚠️ And the honest counterweight

Data engineering built to no purpose is also waste. **A warehouse nobody
queries** is as much a failure as a model with no data. The right sequence is
*a question, then the pipeline that answers it* — not a platform in the hope
that questions arrive.

**The role this course prepares you for sits in between**, and that is why the
syllabus pairs data engineering with MLOps in one course rather than two.

---

## 1.6 The skills

| Skill | Where it appears in this programme |
|---|---|
| **SQL** | Course 5, and every experiment in this course that touches the warehouse |
| **Python** | Courses 3 and 9 |
| **Distributed systems** | Course 12 B — HDFS, MapReduce, Spark |
| **Cloud** | Course 13 B — storage classes, costs, managed services |
| **Data modelling** | Course 8's star and snowflake schemas, used in [experiment 3](lab.md#experiment-3) |
| **Orchestration** | Airflow, Dagster, Prefect — the scheduling layer |
| **Version control** | git, and DVC for data — [experiments 8 and 9](lab.md#experiment-8) |
| **Testing and monitoring** | this course's Units 3 and 5 |

> ### 💡 The skill students underrate
>
> **SQL.** Not writing a `SELECT`, but understanding the execution plan, why a
> join is slow, what a window function does, and why `SELECT *` into a
> dashboard is a maintenance problem. **Most data engineering is SQL**, and
> the fashionable parts are a smaller share of the job than they appear.

---

## What to be able to do after this unit

- [ ] Define data engineering, with **systems** and **maintenance** in the definition
- [ ] **Distinguish the data lifecycle from the data engineering lifecycle**
- [ ] Name the five stages and the five undercurrents, and say why the undercurrents are drawn underneath
- [ ] **Explain ETL against ELT and why ELT won**
- [ ] Give the technical/business and internal/external splits
- [ ] State the relationship between data engineering and data science, in both directions
- [ ] Explain why a silently-wrong pipeline is worse than one that crashes

**Cross-check yourself:** run
`01_environment_etl.py`.
