# Unit 3 — Cloud Storage and Data Management

**Syllabus topics:** Cloud storage: introduction, benefits, use cases
(backup, archiving, disaster recovery, content delivery). Cloud storage
systems: block-based, file-based, object-based. Key-value databases: features
and limitations. Batch against streaming data for ML pipelines. Cloud data
warehouses: AWS Redshift, Google BigQuery.

---

## The unit where the money is

**Storage decisions are where cloud bills are made and lost**, and they are
the most examinable arithmetic in the course. Every figure below is computed
in `04_storage.py` and
`09_etl_warehouse.py`.

---

## 3.1 The three storage types — block-based, file-based, object-based

The **benefits** of cloud storage are durability you do not engineer, capacity you do not provision, and access from anywhere. What you choose between is the *shape*.

### 🎯 Learn them by what the unit of access is

| | **Block (EBS)** | **File (EFS)** | **Object (S3)** |
|---|---|---|---|
| Looks like | **a raw disk** | a mounted filesystem | **an HTTP API** |
| Unit of access | a 512-byte block | a file, or a byte range | **a whole object** |
| Attached to | **one instance** * | **many instances** | anything, anywhere |
| In-place edit | yes | yes | **NO — rewrite it** |
| Directories | whatever the filesystem does | real | **NONE — prefixes** |
| Latency | sub-millisecond | low millisecond | tens of ms |
| Capacity | **provisioned, fixed** | elastic | **unlimited** |
| Metadata | none | POSIX | **arbitrary, per object** |
| $/GB-month | 0.080 | **0.30** | **0.023** |

\* EBS Multi-Attach exists for io1/io2 and needs a cluster filesystem.

### 🔢 The same terabyte, for a month

| | Cost |
|---|---:|
| EFS Standard | **$307.20** |
| EBS gp3 | $81.92 |
| S3 Standard | **$23.55** |

**EFS costs 13× what S3 does and 3.8× what EBS does** — and it is worth it
precisely when several instances must share a POSIX filesystem. **Paying 13×
for a dataset that one batch job reads once is the mistake**; that dataset
belongs in S3.

> **Choose by access pattern, not by price:** block for a database or a boot
> disk, file for shared POSIX, object for everything a data pipeline reads.

### 🔢 And provisioned against consumed

A 1 TB EBS volume holding 200 GB:

| | Billed |
|---|---:|
| EBS, on **provisioned** size | **$81.92**/month |
| S3, on **stored** bytes | $4.60/month |

**A factor of 18.** EBS bills the volume you asked for, empty or not. **"Just
make it 1 TB to be safe" is an expensive habit**, and it is invisible on every
dashboard that reports utilisation rather than spend.

---

## 3.2 Object storage, in detail

### ⚠️ There are no directories. None.

```
LIST prefix 'raw/' with delimiter '/':
  objects at this level : (none)
  common prefixes       : ['raw/2026/']

LIST prefix 'raw/' with NO delimiter:
  raw/2026/01/sales.csv
  raw/2026/02/sales.csv
  raw/2026/03/sales.csv
```

**`raw/2026/01/sales.csv` is ONE KEY containing three slashes.** The console's
folder tree is drawn from **common prefixes computed at list time**. Delete
every object under a "folder" and the folder is gone, because it never
existed.

**And a prefix scan is the only query an object store supports.** No `WHERE`,
no index, no search by content.

### ⚠️ There is no rename

```
'rename' README.md -> docs/README.md
  bytes read 1,024, bytes written 1,024, API calls 2
```

**It is a copy plus a delete.** Renaming a 5 TB dataset "to tidy up the
folders" moves 10 TB and is billed for it — and on a filesystem it would have
been a metadata edit.

### ⚠️ Versioning bills for every version

```
versioning ON, then overwrite and delete:
  older versions kept : 2
  current object      : DeleteMarker
```

**A delete with versioning on writes a delete marker; the data is still there
and still billed.** That is the feature (you can undelete) and the bill (you
pay for every version until a lifecycle rule removes them).

**Set the lifecycle rule when you enable versioning, not later.**

---

## 3.3 Storage classes, and the arithmetic that decides

### 🔢 1 TB stored for a year, retrieved once

| Class | Storage/yr | Retrieve 1 TB | Total | Min days |
|---|---:|---:|---:|---:|
| Standard | $282.62 | $0.00 | **$282.62** | 0 |
| Standard-IA | $153.60 | $10.24 | $163.84 | 30 |
| One Zone-IA | $122.88 | $10.24 | $133.12 | 30 |
| Glacier Instant | $49.15 | $30.72 | $79.87 | 90 |
| Glacier Flexible | $44.24 | $10.24 | $54.48 | 90 |
| **Glacier Deep Archive** | **$12.17** | $20.48 | **$32.65** | **180** |

### 🎯 Read the two ratios separately

**Deep Archive *storage* is 23× cheaper than Standard.** Add one retrieval a
year and the all-in saving falls to **8.7×**, because the retrieval fee
($20.48) exceeds a whole year of its storage ($12.17).

**The headline discount is not the discount.**

And it carries a **180-day minimum billing duration** plus a retrieval that
takes up to 12 hours: delete an object after 10 days and you are billed for
180.

### ⚠️ And the reversal that catches people

The same 1 TB, retrieved **twice a month**:

| Class | Storage/yr | Retrieval/yr | Total |
|---|---:|---:|---:|
| **Standard** | $282.62 | $0.00 | **$282.62** |
| Standard-IA | $153.60 | $245.76 | $399.36 |
| Glacier Instant | $49.15 | $737.28 | $786.43 |

**Standard is now the cheapest, by a wide margin.** The "cheap" tiers charge
per GB retrieved, and at two retrievals a month the retrieval fee exceeds
everything the storage discount saved.

> **"We moved everything to IA to save money" is how a bill goes UP.**

**Storage class is a bet on your access pattern**, and the minimum durations
and retrieval fees are what make the bet real.

---

## 3.4 Egress, and data gravity

| Transfer | Cost |
|---|---:|
| 1 TB **in** from the internet | **$0.00** |
| 1 TB **out** to the internet | **$92.16** |
| 1 TB between availability zones | $20.48 |
| 1 TB S3 → EC2, same region | **$0.00** |

### 🎯 The asymmetry is the economic shape of the cloud

**Downloading 1 TB once costs as much as storing it for 3.9 months.**

Ingress is free; egress is not. **That is the mechanism behind vendor
lock-in:** your data is not held hostage, it is simply expensive to move —
which is a much harder thing to argue with.

**And it is why "move the compute to the data" survived from Course 12 B into
the cloud era.** Run the job in the region holding the bucket and the transfer
is free.

---

## 3.5 Use cases

| Use case | What it needs | Right service |
|---|---|---|
| **Backup** | cheap, write-mostly, occasional restore | S3 Standard-IA → Glacier by lifecycle |
| **Archiving** | very cheap, rarely read, long retention | **Glacier Deep Archive** |
| **Disaster recovery** | cross-region, tested restores | S3 Cross-Region Replication |
| **Content delivery** | low latency, high egress volume | **S3 + CloudFront** |
| **Data lake** | cheap, queryable in place | S3 + Parquet + Athena/Glue |

### 🎯 Content delivery is where egress becomes the whole cost

A CDN is not primarily about speed. **CloudFront's egress is cheaper than
S3's, and cached responses do not touch S3 at all** — so for a popular file,
a CDN pays for itself on transfer alone, and the latency improvement is
almost a side effect.

### ⚠️ The DR distinction that is examined

| Term | Means |
|---|---|
| **RPO** — Recovery Point Objective | **how much data you can afford to lose** |
| **RTO** — Recovery Time Objective | **how long you can afford to be down** |

**An RPO of zero requires synchronous replication**, which costs latency on
every write. **An RTO of minutes requires a warm standby**, which costs money
while nothing is wrong. Both are business decisions with a price, and "we back
up nightly" is an RPO of 24 hours whether or not anyone said so.

**And a backup you have never restored is not a backup.** It is an untested
hypothesis.

---

## 3.6 Key-value databases

### 📖 The model

**A hash map with durability.** `get(key)`, `put(key, value)`, `delete(key)` —
and, in the better ones, a **sort key** allowing range queries within a
partition.

| Feature | Present? |
|---|---|
| Lookup by key | **yes, single-digit ms at any scale** |
| Range scan within a partition | yes, if there is a sort key |
| **Query by value** | **NO** — unless you build a secondary index |
| Joins | **no** |
| Multi-item transactions | limited, and expensive |
| Aggregations | **no** |

### 🎯 Why they scale, and what it costs

**The partition key determines which physical node holds the item.** That is
what makes lookups O(1) at any size — and it is exactly the constraint:

> **Any query that does not begin with the partition key is a full scan.**

This is Course 12 B's HBase row-key lesson in a different product, and the
same trade-off applies: **an evenly distributed key avoids hotspots and
destroys range queries; a meaningful key enables range queries and risks
hotspots.**

### ⚠️ The limitations that decide against it

| Limitation | Consequence |
|---|---|
| No ad-hoc queries | every access pattern must be designed **in advance** |
| No joins | you denormalise, and maintain consistency yourself |
| No aggregation | counts and sums are maintained as counters, or exported |
| Item size caps | DynamoDB 400 KB, Cosmos 2 MB |
| Secondary indexes cost | storage and write throughput, per index |

**Design the access patterns first, then the key.** In a relational database
you design the schema and the queries follow; in a key-value store the queries
come first, and getting that backwards is the most common failure.

### The comparison across the programme

| | **DynamoDB** | **MongoDB** (Course 10) | **HBase** (Course 12 B) |
|---|---|---|---|
| Model | key-value + document | document | sparse sorted map |
| Query by value | with a GSI | **yes, natively** | **no** |
| Managed | fully | Atlas, or self-hosted | self-hosted, mostly |
| Scales by | partition key | shard key | region split |
| Billed on | **read/write units** | instance | instance |

---

## 3.7 Batch against streaming for ML pipelines

| | **Batch** | **Streaming** |
|---|---|---|
| Arrives | on a schedule | continuously |
| Completeness | a whole period, consistent | **whatever has landed** |
| Late data | impossible | **normal, and must be handled** |
| Re-runnable | **yes, idempotent** | no — events are consumed |
| Latency | minutes to hours | seconds |
| Failure means | re-run the job | **a gap in the data** |
| Cost | bursty, predictable | continuous |
| Services | Glue, Dataflow batch, EMR | Kinesis, Pub/Sub, Dataflow |

### 🎯 "Late data is normal" is the row that changes the design

**A streaming aggregate for 09:00 is not final at 10:00.** Either you accept
eventual correctness, or you keep a **watermark** and re-emit corrected
results.

**The batch leg has no such problem**, which is exactly why the **Lambda
architecture** keeps both — and why **Kappa** removes the batch layer by
making the stream replayable from a durable log.

**Lambda's real cost is not machines: it is the same business rule living in
two codebases and drifting.**

### ⚠️ And the failure that has no error message

**Training on batch and serving on streaming is how training/serving skew
happens.** The batch job computes a feature over a complete day; the streaming
path computes it over whatever arrived. The model then sees, at serving time,
a feature distribution it never trained on — and every metric stays green.

**A feature store exists to solve exactly this**: one definition of a feature,
computed once, served to both.

---

## 3.8 Cloud data warehouses

### 📖 What makes one different from Course 5's RDBMS

| | **RDBMS (Course 5)** | **Cloud DW** |
|---|---|---|
| Storage layout | **row** | **columnar** |
| Workload | many small transactions | **few huge scans** |
| Indexes | central to performance | **usually none** |
| Scaling | a bigger box | add nodes, or serverless |
| Compute & storage | coupled | **separated** |
| Billed on | the box, hourly | **bytes scanned**, or node-hours |
| A bad query costs | time | **time and money** |

### 🎯 The last row is the one that is new

### 🔢 BigQuery, at $6.25 per TB scanned

| Query | TB scanned | Cost |
|---|---:|---:|
| `SELECT * FROM events` | 10.00 | **$62.50** |
| `SELECT user_id FROM events` | 0.40 | $2.50 |
| `SELECT user_id … WHERE dt = '2026-08-01'` | **0.02** | **$0.12** |

**The same question, 500× the price.**

Selecting one column instead of all reads a fraction of the bytes — **Course
12 B's column projection** — and a partition filter removes almost all of the
rest — **Course 12 B's partition pruning**.

> **In Course 12 B those techniques saved TIME. Here they save MONEY, on the
> same mechanism.**

That is why `SELECT *` is a **billing incident** on a serverless warehouse and
merely rude on a server you already own.

### 🔢 Redshift, and the break-even

At $1.086 per node-hour:

| Nodes | Per month |
|---:|---:|
| 2 | $1,585.56 |
| 4 | $3,171.12 |
| 8 | $6,342.24 |

**Break-even against on-demand BigQuery: about 254 TB scanned per month.**

- **Below that**, on-demand is cheaper and you pay **nothing when idle**.
- **Above it**, a provisioned cluster is cheaper and an extra query costs
  nothing at the margin.

**That is the whole provisioned-against-serverless decision, and it is a
calculation rather than a preference.**

### ETL against ELT

| | **ETL** | **ELT** |
|---|---|---|
| Transform runs | on separate compute | **in the warehouse** |
| Lands in the DW | clean data only | **raw data, then transformed** |
| Fix a transformation bug | re-extract from source | **re-run SQL on raw** |
| Needs | an ETL server, or Glue | a warehouse that scales |
| Suits | limited warehouse capacity | cheap elastic compute |

**ELT won because warehouse compute got cheap and elastic.** Landing raw data
means a bug is fixed by re-running SQL rather than re-extracting from a
production database that may no longer hold the old rows — **which is exactly
the `DELETE` problem Course 12 B found in Sqoop**.

### 🔢 The pipeline, run end to end

`09_etl_warehouse.py`
extracts from SQLite, transforms with an audit trail, and loads DuckDB:

| Step | Rows |
|---|---:|
| extracted | **11** |
| after dedup | 10 |
| dropped, null region | 1 |
| **loaded** | **9** |

**11 in, 9 out, and the pipeline can say where the other two went.** A
transformation that silently drops rows is worse than one that fails: the
numbers still look plausible. **Every ETL job should emit these counts, and a
monitoring rule should alarm when the drop rate moves.**

And the warehouse total is **₹12,880**, with **South = ₹10,360** — Course 11's
DAX, Course 12 B's Hive, Course 12 B's Spark and this. **Four engines, one set
of nine facts**, and the suite fails if any of them drifts.

---

## Practice problems

**1. A 50 TB dataset is written once and read about twice a year. Which
storage class, and what would you check first?**

**Glacier Flexible or Deep Archive**, and the thing to check first is the
**retrieval pattern**, not the size.

Per year, per TB: Deep Archive storage is $12.17 and one retrieval is $20.48.
At **two** retrievals, retrieval already costs 3.4× the storage. Scaling to
50 TB:

- Deep Archive: 50 × ($12.17 + 2 × $20.48) ≈ **$2,657/year**
- Glacier Flexible: 50 × ($44.24 + 2 × $10.24) ≈ **$3,236/year**
- Standard: 50 × $282.62 ≈ **$14,131/year**

**Deep Archive wins**, but check two things first: the **180-day minimum**
(fine here — data is kept for years) and the **12-hour retrieval time**. If a
read must complete in minutes, Deep Archive is disqualified regardless of
price, and Glacier Instant is the answer.

**2. Explain why an object store cannot rename a file, and what to do about
it.**

**Because the key is the identity.** An object store is a flat map from key
to bytes; there is no directory entry to edit and no inode to relink.
"Renaming" means writing the object under a new key and deleting the old one —
a full read and a full write.

**Measured:** a rename of a 1 KB object read 1,024 bytes, wrote 1,024 bytes
and made 2 API calls. Scale that to 5 TB and it moves 10 TB.

**What to do:**

- **Get the key layout right at write time.** Partition prefixes
  (`dt=2026-08-01/`) should be decided before the first write.
- **Never restructure a lake by renaming.** Write to the new layout from the
  pipeline, and expire the old prefix by lifecycle rule.
- **Use a table format** — Iceberg, Delta, Hudi — where the layout is
  metadata and reorganisation does not move bytes.

**3. Your BigQuery bill jumped from $40 to $900 in one month with no new
data. What do you look at?**

**Bytes scanned, per query, per user.** The `INFORMATION_SCHEMA.JOBS` view
gives `total_bytes_billed` by query.

The usual causes, in order of likelihood:

1. **A dashboard on auto-refresh.** A `SELECT *` on a 10 TB table costs
   $62.50; every 15 minutes for a month is 2,880 runs.
2. **A new query without a partition filter.** The 500× difference measured
   above is entirely partition pruning and column projection.
3. **A view hiding a `SELECT *`.** The view looks cheap; what it scans is not.
4. **`SELECT *` in a `LIMIT 10` query.** `LIMIT` does **not** reduce bytes
   scanned in a columnar store — it reduces bytes *returned*.

**The fixes:** `--maximum_bytes_billed` on every automated job, `--dry_run`
before every large one, `require_partition_filter` on large tables, and
materialised views for dashboards.

**4. Design the storage for a model-training pipeline: raw logs arrive
continuously, features are computed nightly, and eight workers train in
parallel.**

- **Raw logs → S3 Standard**, partitioned by date, in Avro or Parquet. Cheap,
  append-only, and the pipeline reads them once. A **lifecycle rule** moves
  them to Standard-IA at 30 days and Glacier at 90.
- **Nightly features → S3, Parquet, partitioned.** Column projection and
  predicate pushdown make the training reads cheap, and the same files serve
  ad-hoc analysis through Athena.
- **The eight training workers → read from S3 directly.** Not EFS. Each
  worker reads its shard; there is no shared-write requirement, so the 13×
  EFS premium buys nothing.
- **Checkpoints during training → S3**, so a spot interruption does not lose
  the run.
- **EBS** only for each worker's OS disk and scratch space.

**The decision that carries it:** *is there a shared-write POSIX
requirement?* There is not, so the answer is object storage throughout — and
"we put it on EFS because it was easy to mount" is the mistake this question
is testing.

**5. When would you choose provisioned Redshift over serverless BigQuery?**

**When you scan more than about 254 TB a month** — the measured break-even —
because above that a fixed cluster is cheaper and each extra query is free at
the margin.

**And four non-price reasons:**

1. **Predictable spend.** A fixed monthly cost is easier to budget than a
   variable one, even if the variable one is lower on average.
2. **No per-query blast radius.** A careless query on a provisioned cluster
   costs time; on on-demand it costs money.
3. **Sustained, concurrent workloads.** Hundreds of dashboard users hitting
   the same tables all day is exactly the profile a cluster suits.
4. **Data locality with the rest of an AWS estate**, avoiding cross-cloud
   egress.

**And the counter:** if the workload is spiky — heavy month-end, quiet
otherwise — serverless costs nothing during the quiet weeks, and a cluster
costs the same every hour.

---

## Exam questions from this unit

**Two marks**

1. Name the three cloud storage types.
2. Which of them has no directories?
3. Why is there no rename in an object store?
4. What is the minimum billing duration for Glacier Deep Archive?
5. Is ingress or egress charged?
6. State RPO and RTO.
7. Name one limitation of a key-value database.
8. What is BigQuery billed on?

**Five marks**

1. Compare block, file and object storage on access unit, sharing and cost.
2. Explain storage classes and the trap in the "cheap" tiers.
3. Explain egress pricing and data gravity.
4. Explain the features and limitations of key-value databases.
5. Compare batch and streaming ingestion for an ML pipeline.

**Ten marks**

1. Explain cloud storage in full — the three types, the classes, the use
   cases and the cost model — with worked arithmetic.
2. Compare a cloud data warehouse with a traditional RDBMS, explain
   serverless against provisioned pricing, and work out the break-even.

---

## Mistakes that cost marks

- **Saying an object store has folders.** It has prefixes.
- **Treating `s3 mv` as a rename.** It is a copy plus a delete.
- **Recommending Infrequent Access without asking how often it is read.**
  Standard beat both IA tiers at two retrievals a month.
- **Quoting a storage-class discount without the retrieval fee** or the
  minimum duration.
- **Forgetting egress** in a migration or hybrid design.
- **Putting a read-once dataset on EFS.** 13× S3, for a feature you are not
  using.
- **Saying `LIMIT 10` makes a BigQuery query cheap.** It limits rows
  returned, not bytes scanned.
- **Designing a key-value schema before the access patterns.** The queries
  come first.
- **Calling a backup a disaster-recovery plan.** An untested restore is a
  hypothesis.
