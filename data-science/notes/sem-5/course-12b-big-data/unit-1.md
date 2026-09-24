# Unit 1 — Foundations of Big Data and the Hadoop Ecosystem

**Syllabus topics:** Introduction to Big Data: characteristics (volume,
variety, velocity, veracity, value). Hadoop Ecosystem Overview: HDFS,
MapReduce, YARN, Hadoop Common. Hadoop architecture and use cases.

---

## 1.1 What "big data" actually means

Every **introduction to big data** starts with a definition, and most of them are wrong within five years. Here is one that is not.

### 🎯 The definition worth memorising

**Data is big when it no longer fits the assumptions of a single machine.**

Not when it exceeds a byte count. The number moves every year; the
*assumptions* do not. A dataset is big when at least one of these stops being
true:

- it fits in RAM
- it fits on one disk
- one CPU can process it in acceptable time
- it can be reliably stored on hardware you trust

### 📖 The textbook definition, for the exam

> Big data is data whose **volume, velocity and variety** demand new forms of
> processing to enable enhanced decision making, insight discovery and process
> optimisation. — Gartner, 2001

Note the date. **The concept predates Hadoop by five years** — Doug Cutting
started Hadoop in 2006 — which is a useful thing to know when an examiner
implies the tool created the problem.

---

## 1.2 The five Vs

The syllabus lists all five, and they are not equally important. Learn them
in this order of usefulness:

| V | What it means | The design consequence |
|---|---|---|
| **Volume** | more data than one machine holds | **distribute storage** → HDFS |
| **Velocity** | data arriving faster than you can batch it | **stream processing** → Flume, Kafka, Spark Streaming |
| **Variety** | structured, semi-structured and unstructured together | **schema on read** → Hive external tables, Avro |
| **Veracity** | some of it is wrong, late or duplicated | **validate and reconcile** → the checks in experiment 14 |
| **Value** | most of it is worthless | **know the question first** |

### ⚠️ The two Vs students get wrong

**Veracity is not "data quality" in the tidy sense.** It is the acceptance
that at scale you *cannot* clean everything, so you build pipelines that
tolerate bad records rather than pipelines that assume good ones. A Flume
agent that dies on one malformed log line is a broken design, not a strict one.

**Value is the one that matters commercially and gets one mark.** Storing
everything because storage is cheap produces a *data swamp*: petabytes nobody
can query because nobody documented what is in them. "We will find a use for
it later" is how that happens.

### 🔢 A sense of scale

| Unit | Bytes | Something that size |
|---|---|---|
| GB | 10⁹ | a two-hour film |
| TB | 10¹² | a laptop's disk |
| PB | 10¹⁵ | roughly what a large hospital chain holds |
| EB | 10¹⁸ | global internet traffic, in about two hours |

**At petabyte scale, reading the data once at 100 MB/s takes 116 days.** On
1,000 disks in parallel it takes under three hours. That arithmetic — not any
software feature — is why distributed storage exists.

---

## 1.3 Big data against a traditional database

| | **RDBMS** | **Hadoop / big data** |
|---|---|---|
| Data size | GB to a few TB | TB to PB |
| Schema | **on write** — declared before data | **on read** — imposed at query time |
| Structure | structured only | structured, semi-, unstructured |
| Updates | read and write, many times | **write once, read many** |
| Integrity | high — constraints enforced | low — enforced by convention |
| Scaling | **vertical** (a bigger box) | **horizontal** (more boxes) |
| Access | interactive, milliseconds | batch, minutes |
| Hardware | expensive, reliable | **commodity, expected to fail** |

### 🎯 The row that explains all the others

**"Hardware: commodity, expected to fail."**

Google's insight in 2003 was not that distributed storage was possible — it
was that on 10,000 cheap machines, *something is always broken*, so failure
must be **normal operation** rather than an exception. Replication, heartbeats,
speculative execution and re-running failed tasks all follow from treating
failure as the expected case.

### ⚠️ "Schema on read" is not "no schema"

The schema still exists — it moves from the *writer* to the *reader*. That
buys flexibility (you can land data before you know what it is) and costs
correctness (nothing stops you writing garbage, and you find out at query
time, months later). **Course 5's constraints were doing real work**; big data
systems drop them deliberately, and that trade should be stated as a trade.

---

## 1.4 The Hadoop ecosystem

### 📖 The four core components

Hadoop proper is only four things. Everything else is an ecosystem project
that sits on top.

| Component | What it is | Unit |
|---|---|---|
| **HDFS** | the distributed filesystem — storage | 2 |
| **YARN** | the resource manager — who gets to run | 2 |
| **MapReduce** | the batch processing framework — computation | 3 |
| **Hadoop Common** | the shared libraries, configuration and RPC | — |

**Hadoop Common is the one nobody can name**, and it is worth one mark: the
Java libraries, the filesystem abstraction (which is why `hadoop fs` also
talks to S3), the configuration system and the RPC layer that all the others
share.

### The ecosystem, by the job it does

| Layer | Projects | Why |
|---|---|---|
| **Ingestion** | Sqoop, Flume, Kafka, NiFi | get the data in |
| **Storage** | HDFS, HBase, S3 | keep it |
| **Serialisation** | Avro, Parquet, ORC, SequenceFile | *how* to keep it |
| **Processing** | MapReduce, Spark, Tez, Flink | compute over it |
| **Query** | Hive, Pig, Impala, Drill | ask questions in a language |
| **Coordination** | ZooKeeper | agree on who is in charge |
| **Workflow** | Oozie, Airflow | run things in order |
| **Security** | Kerberos, Ranger, Knox | who may see what |

### 💡 Learn the layers, not the list

An examiner asking "describe the Hadoop ecosystem" wants the *shape*, not
twenty product names. Answer with the layers, name two or three per layer, and
say which ones this syllabus covers. That reads as understanding; a memorised
list does not.

---

## 1.5 Hadoop architecture

### The two-cluster view

Hadoop runs **two independent master/worker systems on the same machines**:

```
        STORAGE                          COMPUTE
  ┌──────────────────┐            ┌──────────────────────┐
  │    NameNode      │            │  ResourceManager     │
  │  (the namespace) │            │  (the scheduler)     │
  └────────┬─────────┘            └──────────┬───────────┘
           │                                 │
  ┌────────┴─────────┐            ┌──────────┴───────────┐
  │    DataNodes     │  ── same ──│    NodeManagers      │
  │  (the blocks)    │  machines  │  (the containers)    │
  └──────────────────┘            └──────────────────────┘
```

**They are deliberately separate**, and co-located deliberately. Separate,
because you can run Spark on YARN without MapReduce, or run HDFS with no YARN
at all. Co-located, because a task that runs on the machine holding its block
reads from local disk instead of over the network.

### 🎯 Data locality — the idea the whole design is built around

> **Moving computation is cheaper than moving data.**

A 128 MB block takes about a second to read from a local disk and rather
longer to pull across a shared network. So the scheduler asks the NameNode
where each block lives and **sends the task there**.

YARN's locality preferences, in order:

1. **NODE_LOCAL** — the same machine as the block. Free.
2. **RACK_LOCAL** — a different machine, same rack. One switch hop.
3. **OFF_SWITCH** — anywhere. Crosses the core network.

This is also why the replica placement policy in Unit 2 puts one replica on
the writer's rack: it creates *three* chances for a task to run locally.

### ⚠️ Data locality is nearly gone in the cloud

On AWS EMR or Databricks the data lives in S3 and the compute is on separate
EC2 instances, so **every read is off-switch by definition**. Cloud
architectures accept that because networks got fast (25–100 Gbit/s) and
separating storage from compute lets you scale them independently.

Saying this in an exam is worth more than reciting locality as gospel: the
principle was correct in 2008 and the trade has since moved.

---

## 1.6 Use cases

| Domain | Use | Which V dominates |
|---|---|---|
| **Retail** | market basket analysis, recommendation | Volume |
| **Telecom** | call detail records, churn prediction | Volume + Velocity |
| **Banking** | fraud detection, risk | Velocity + Veracity |
| **Healthcare** | genomics, imaging archives | Volume + Variety |
| **Web** | clickstream, search indexing, A/B tests | Volume + Velocity |
| **IoT / manufacturing** | sensor telemetry, predictive maintenance | Velocity |
| **Government** | census, weather, satellite imagery | Volume + Variety |

### 🎯 The use case to give if asked for one

**Search indexing**, because it is the problem Hadoop was *built* for. Yahoo
needed to invert the web: every word on every page, mapped to the pages
containing it. That is [experiment 8](lab.md#experiment-8) at a scale of
billions of documents, and it is the honest origin story — MapReduce came from
Google's need to rebuild its index, not from a general theory of computation.

### ⚠️ When Hadoop is the wrong answer

| Situation | Why not Hadoop | Use instead |
|---|---|---|
| Data fits in RAM | the coordination overhead exceeds the work | **pandas** (Course 9) |
| You need sub-second answers | it plans and submits a *job* | an RDBMS, or a cache |
| Many small files | NameNode RAM is the limit | concatenate, or object storage |
| Row-level updates | HDFS is append-only | an RDBMS, or HBase |
| ACID transactions | there are none | an RDBMS |
| Fewer than ~5 machines | you cannot amortise the complexity | one big machine |

**"How much data do you have?" is the first question**, and if the answer is
under a terabyte the honest recommendation is usually a single server with a
lot of RAM. Being able to say that is a sign of judgement, not of ignorance.

---

## Practice problems

**1. A dataset is 400 GB and grows 10 GB a day. Is it big data?**

**No, and say why.** It fits comfortably on one machine's disk today and will
for years. A single server with 512 GB of RAM would hold it *in memory*. The
correct recommendation is PostgreSQL or DuckDB, not a Hadoop cluster —
the complexity of a distributed system is a cost you pay only when you must.

**Where it changes:** if those 400 GB are 40 million small images (Variety),
or arrive as 200,000 events per second (Velocity), the size is no longer the
deciding factor.

**2. Explain why "commodity hardware" changes the software design.**

On 1,000 cheap machines with a 3-year mean time to failure, **something fails
roughly every 8 hours**. So the software must:

- **replicate** — so one disk dying loses nothing
- **detect** — heartbeats, so failure is noticed in seconds not days
- **recover automatically** — re-replicate, re-run the task, elect a new leader
- **be idempotent** — a re-run task must produce the same answer

Every one of those is a Hadoop feature, and every one exists because the
hardware assumption changed.

**3. A company wants to store 8 TB of scanned invoices as PDFs, searchable by
customer. Which parts of the ecosystem, and why?**

- **HDFS** for the PDFs — large files, write once, read many. A good fit.
- **A metadata store** — extracted text and customer IDs. This is a *random
  read by key*, so **HBase**, not HDFS.
- **Spark** for the extraction batch job, converting PDFs to text.
- **Parquet** for the extracted text table, since the queries are analytical.

**The trap:** searching PDFs by scanning HDFS is a full scan of 8 TB per
query. The index is what makes it work, exactly as in experiment 8.

**4. Why is "schema on read" both an advantage and a liability?**

**Advantage:** you can land data before you know its structure, which means
ingestion never blocks on a schema negotiation, and one dataset can be read
with different schemas by different teams.

**Liability:** nothing validates the write. A field that silently changes type
upstream is discovered by a failing query months later, and by then the bad
data is in every derived table. Course 5's `NOT NULL` and `CHECK` constraints
were doing work that a big-data pipeline must do explicitly, in code, or not at
all.

**5. Rank the five Vs by how often they actually drive a design decision, and
defend the ranking.**

**Volume, Velocity, Variety, Value, Veracity.**

Volume and Velocity decide the *architecture* — batch or stream, one machine or
many. Variety decides the *storage format*. Value decides whether the project
should exist. Veracity influences everything but rarely determines the shape.

**Defending it matters more than the order.** An answer that ranks them and
gives reasons beats one that lists all five as equally important.

---

## Exam questions from this unit

**Two marks**

1. Define big data in one sentence.
2. Name the five Vs.
3. What are the four core components of Hadoop?
4. What is Hadoop Common?
5. State the data locality principle.
6. Give one difference between schema on read and schema on write.
7. Who created Hadoop, and what was it named after?
8. Name two ingestion tools in the Hadoop ecosystem.

**Five marks**

1. Explain the five Vs with one example each.
2. Compare an RDBMS with Hadoop on six dimensions.
3. Describe the Hadoop ecosystem by layer.
4. Explain data locality and why the cloud has weakened it.
5. Give three situations where Hadoop is the wrong tool, with reasons.

**Ten marks**

1. Explain the characteristics of big data and describe the Hadoop
   architecture, with a diagram, covering all four core components.
2. A retail chain has 2,000 stores generating 50 GB of transactions daily and
   wants both nightly reports and real-time fraud alerts. Design the pipeline
   and justify each component.

---

## Mistakes that cost marks

- **Defining big data by a byte count.** Any number you give is wrong within
  five years. Define it by the failure of single-machine assumptions.
- **Listing the ecosystem as twenty product names** instead of layers.
- **Saying "Hadoop is a database".** It is a filesystem plus a scheduler plus
  a processing framework. HBase is the database, and it is not Hadoop.
- **Claiming schema on read means no schema.**
- **Forgetting Hadoop Common** when asked for the four components — most
  answers name three.
- **Reciting data locality without noting it is nearly gone in the cloud.**
  The principle is 2008; the trade has moved, and saying so shows you
  understand *why* it existed.
- **Treating Value as filler.** "Most stored data is never queried" is a real
  and examinable point about data swamps.
