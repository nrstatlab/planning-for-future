# Course 12 B — Practical Lab

**17 experiments**

Code lives in `labs/course-12b-bigdata/`.

## Read this before you read anything else

**This is the most environment-constrained course in the programme, and the
lab is split in two.**

| Half | Files | Status |
|---|---|---|
| **The tools you run on a cluster** | **15 files** | **`*** NOT EXECUTED ***`** in every header |
| **The verification** | **14 programs** | **Executed and asserted** by `tools/run_bigdata_labs.py` |

Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed here
— **the Debian repositories that host them are blocked by the egress policy**,
the same wall that stopped R in Course 6, WEKA in Course 8, `mongod` in
Course 10 and SWI-Prolog in Course 13 A.

```bash
pip install -r tools/requirements.txt
bash tools/setup_spark.sh          # optional; experiment 17 needs it
python3 tools/run_bigdata_labs.py
```

### 🎯 What genuinely runs, and it is more than you would expect

| Runs for real | How |
|---|---|
| **Apache Spark 4.2** | a genuine `SparkSession`, real RDDs, a real shuffle inside `reduceByKey` |
| **Avro** | `fastavro` — the files are byte-for-byte readable by Hadoop |
| **Parquet** | `pyarrow` — real column chunks, real row-group statistics |
| **Hive-style SQL** | DuckDB, running the same query text |
| **The Sqoop import** | a real SQLite database, real range queries, real Parquet out |
| **MapReduce** | an engine written out in full, with a **visible shuffle** |

**Nothing is claimed that was not executed.** Every file that cannot run says
so in its own header, names the tool it needs, and points at the runnable half
that verifies its logic. The runner asserts the marker is still there — strip
it without making the file runnable and the suite fails.

### The cross-course check

**Experiments 10, 14 and 17 all use Course 11's star schema, imported rather
than copied.** `fixtures.py` loads `labs/course-11-bi/fixtures.py` by path at
import time, so the two courses cannot drift.

**South = ₹10,360** is produced by Course 11's DAX `CALCULATE`, by DuckDB in
experiment 10, and by Spark in experiment 17. **If they ever disagree, one of
them is wrong and `verify_all.sh` says so.**

---

## Experiments 1–3 — Installation, commands, architecture

`01_install_hadoop.sh` ·
`02_hdfs_commands.sh` ·
`03_architecture.sh` —
**all NOT EXECUTED**

There is no query logic in an installation, so these three carry the commands
and the failure modes rather than an equivalent.

### The three installation failures everyone hits

1. **`JAVA_HOME` not set inside `hadoop-env.sh`.** Exporting it in your shell
   is not enough — the daemons do not inherit it.
2. **Re-running `hdfs namenode -format` after storing data.** The DataNode's
   `clusterID` no longer matches the NameNode's and it refuses to start. Fix:
   delete the datanode directory, or edit its `VERSION` file.
3. **`ssh localhost` prompting for a password.** `start-dfs.sh` hangs for ever.

`jps` should show **five processes**: NameNode, DataNode, SecondaryNameNode,
ResourceManager, NodeManager.

### 🎯 The four `hadoop fs` facts worth marks

1. **`hadoop fs` and `hdfs dfs` are the same command.** `hadoop fs` also works
   on local and S3 paths.
2. **There is no `cd`.** HDFS has no working directory — every path is
   absolute or relative to `/user/$USER`.
3. **`-rm` moves to `.Trash`** and still costs quota for a day.
4. **There is no in-place edit.** HDFS is write-once, append-only, and that
   single constraint is why it can drop file locking entirely.

### The log trace to follow in experiment 3

RM: application submitted → NM: AM container started → RM: map containers
assigned → NM: map tasks start → NameNode: block reads served **locally** →
RM: reduce containers assigned → **NM: reduce fetches map outputs, over HTTP**
→ RM: SUCCEEDED.

**The one line worth finding is the shuffle fetch.** It is the only step where
data crosses the network in bulk, and it is what the combiner in experiment 7
exists to shrink.

---

## Experiment 4 — Blocks, distribution and replication

`04_hdfs_store.sh` (NOT EXECUTED) ·
`04_blocks_replication.py` — **runs**

### 🔢 The block table

| File | Blocks | Last block | Disk used |
|---:|---:|---:|---:|
| 1 MB | 1 | 1.00 MB | 1 MB |
| 128 MB | **1** | 128.00 MB | 128 MB |
| 129 MB | **2** | 1.00 MB | 129 MB |
| **260 MB** | **3** | **4.00 MB** | 260 MB |
| 1024 MB | 8 | 128.00 MB | 1024 MB |
| 5000 MB | 40 | 8.00 MB | 5000 MB |

**A 260 MB file is 128 + 128 + 4.** HDFS wastes no space on block padding, and
this is the most examined calculation in the course.

**But 128 MB → 1 block and 129 MB → 2.** One byte past the boundary costs a
whole block *object* in NameNode RAM, though almost no disk.

### 🔢 Replica placement, 1 GB over 6 nodes in 2 racks

| Block | Replicas | Racks |
|---:|---|---:|
| 0 | n0/r0, n1/r1, n3/r1 | 2 |
| 1 | n2/r0, n3/r1, n5/r1 | 2 |
| 2 | n4/r0, n5/r1, n1/r1 | 2 |
| … | … | 2 |

**Every block spans exactly two racks** — one replica on the writer's rack,
two on another. Asserted for all 8 blocks.

### 🔢 The small-files table

| Scenario | Files | Blocks | NameNode RAM |
|---|---:|---:|---:|
| one 1 GB file | 1 | 8 | **0.00 MB** (1,350 bytes) |
| 1,000 × 1 MB | 1,000 | 1,000 | 0.29 MB |
| 1,000,000 × 1 KB | 1,000,000 | 1,000,000 | **286.10 MB** |

**A factor of 222,222 for the same gigabyte.**

### And the storage trade

1 GB at replication 3 occupies **3,072 MB**; under RS-6-3 erasure coding,
**1,536 MB** — 200% overhead against 50%, at the cost of expensive
reconstruction reads.

---

## Experiment 5 — Fault tolerance and recovery

`05_fault_tolerance.sh` (NOT EXECUTED) ·
`05_fault_tolerance.py` — **runs**

| Failure | Blocks live | Blocks lost |
|---|---:|---:|
| 1 DataNode (n1) | 8 | **0** |
| 2 DataNodes (n1, n3) | 8 | **0** |
| 3 DataNodes (n1, n3, n5) | 8 | **0** |
| **3 DataNodes (n0, n1, n3)** | 6 | **2** |
| a whole rack (r1) | 8 | **0** |
| both racks | 0 | 8 |

**Rows 3 and 4 are the point.** `n1, n3, n5` **are** rack 1, so rows 3 and 5
are the same failure written two ways — and both are survivable. **Three
failures only hurt when they straddle the racks.**

### 🔢 The honest version, by brute force

| Nodes down | Combinations losing data |
|---:|---|
| 1 | **0 of 6** |
| 2 | **0 of 15** |
| 3 | **6 of 20** |
| 4 | 12 of 15 |
| 5 | 6 of 6 |

**Any two failures are survivable; 14 of the 20 three-node combinations are
still fine.** "Replication 3 fails at 3 nodes" is the worst case, not the rule,
and stating it that way is the honest answer.

### The 630-second delay

`10 × 3 s + 2 × 5 min = 630 s` before a DataNode is declared dead. **The delay
is deliberate** — a node that reboots in five minutes should not trigger a
cluster-wide copy storm.

### ⚠️ The NameNode's block map is never persisted

| Component | Holds | Lost on crash? |
|---|---|---|
| `fsimage` (disk) | the namespace at a checkpoint | no |
| `edits` (disk) | changes since | no |
| **block map (RAM)** | block → DataNode locations | **YES** |

Rebuilt from block reports at startup, which is why a large NameNode takes
minutes to leave safe mode. **And the Secondary NameNode is a checkpointer,
not a standby** — the most misleadingly named component in Hadoop.

---

## Experiment 6 — YARN

`06_yarn.sh` (NOT EXECUTED) ·
`06_yarn_scheduling.py` — **runs**

The workload: an 8-container cluster; `big_etl` needs all 8 for 10 s;
`small_q1` and `small_q2` need 1 container for 2 s; `medium` needs 4 for 5 s.

| Job | FIFO | Fair | Capacity (75/25) |
|---|---:|---:|---:|
| `big_etl` | **10** | 14 | 20 |
| `small_q1` | **11** | **1** | **2** |
| `small_q2` | 12 | 1 | 3 |
| `medium` | 16 | 5 | 22 |
| **total turnaround** | **49** | **21** | — |

### 🎯 What the numbers say, stated carefully

- **`small_q1` waits 11 s under FIFO for 2 s of work.** Head-of-line blocking.
- **Fair sharing did not make the cluster faster.** `big_etl` finished *later*,
  10 → 14. Latency moved from the small jobs to the big one.
- **The work is identical: 104 container-seconds either way**, which on 8
  containers cannot finish before second 13.
- **Total turnaround still halved**, 49 → 21, because FIFO left three jobs
  idle in a queue. Scheduling cannot create throughput, but idle-while-queued
  is real waste.

### The Capacity Scheduler's guarantee

The adhoc queue holds **2 containers whatever else is running**, so a short
query has a guarantee rather than a hope. The cost: those 2 sit idle when
adhoc is empty, unless `maximum-capacity` is raised to allow **elasticity** —
which is exactly the difference between "capacity" and "fair".

### And the row about Hadoop 1

**One ApplicationMaster per job** is the change that defined YARN. Hadoop 1's
JobTracker did both scheduling and per-job management, so it was the
bottleneck *and* the single point of failure, and it could run only MapReduce.

---

## Experiment 7 — Word count in MapReduce

`WordCount.java` (NOT EXECUTED) ·
`07_wordcount.py` +
`mapreduce.py` — **run**

`mapreduce.py` is a MapReduce engine in forty lines, written out in full. **The
point is that it makes the shuffle visible**, and the shuffle is the part
students never see and the part that costs the money.

| Phase | Records |
|---|---:|
| map output | **48** |
| shuffled | **48** |
| reduce output | **26** |

Top words: `the` 5, `big` 4, `data` 4, `dog` 4, `quick` 3, `fox` 3.
**The counts sum back to 48** — reduce is a regrouping, and if your totals do
not reconcile, your reducer is not associative.

### 🔢 The combiner, and why its saving is small here

| | Shuffled |
|---|---:|
| no combiner | **48** |
| with combiner | **39** |
| saving | **9 (18.75%)** |

**Note how small that is, and why it is honest.** The combiner runs **per map
task**, and these documents are 5 to 11 words — there is almost nothing to
merge within one split. On a 128 MB split the same combiner cuts the shuffle
by orders of magnitude.

**The combiner's value scales with split size**, which is the point this tiny
dataset makes precisely by failing to impress.

### ⚠️ The combiner that is wrong

| Reducer computes | Safe? |
|---|---|
| sum, max, count | **yes** |
| **mean** | **NO** |
| median | **NO** |

Demonstrated: `[1,1,1,10]` and `[10]` give **mean of means 6.6250** against
**true mean 4.6000**. Emit `(sum, count)` and divide only in the reducer —
the same average-of-averages trap Course 11 met in DAX.

### Partitioning

3 reducers give partitions of **[20, 17, 11]**, ratio 1.82. Hash partitioning
is only as balanced as the key distribution, and **skew, not volume, is what
usually kills a MapReduce job**.

### The three Java details

**The map key is a byte offset, not a line number.** **Reuse the `Writable`
objects** — a `new Text()` per word makes GC the job. **The reduce `Iterable`
can be walked once** — it streams from disk.

---

## Experiment 8 — Inverted index

`InvertedIndex.java` (NOT EXECUTED) ·
`08_inverted_index.py` — **runs**

6 documents in, **26 index terms** out, from **48 postings**.

| Term | Postings |
|---|---|
| `dog` | doc1:1, doc2:1, doc3:1, doc6:1 |
| `quick` | doc1:1, **doc3:2** |
| `big` | doc4:2, doc5:2 |

**`quick` appears twice in doc3, and the posting records it.** Frequency is
the difference between "does this word occur" and "how relevant is this
document" — boolean retrieval against ranked retrieval, in one number.

### Queries answered from the index alone

| Query | Result |
|---|---|
| `quick AND fox` | doc1, doc3 |
| `big AND data` | doc4, doc5 |
| `dog AND machine` | **no match** |
| `dog OR machine` | doc1, doc2, doc3, doc4, doc6 |

**Not one document was read.** Query cost depends on the number of **matches**,
not on the size of the corpus — which is the entire point of an inverted index.

### The index is not free

226 characters of corpus → 26 terms, **39 postings**. A full-text index
typically runs 20–40% of the corpus size, before positions. Search is a
space-for-time trade.

### 🎯 The skew, measured

**Largest posting list: `the`, with 5. Singleton terms: 15 of 26.** `the` would
be the biggest list on any English corpus, and one reducer holding it is the
job's critical path.

### The Java detail that is examined

**The filename is in neither the key nor the value.** It comes from the input
split — `((FileSplit) context.getInputSplit()).getPath().getName()`.

And **this job cannot use a combiner**: the reducer's output type (a posting
string) differs from its input type (a document id), and a combiner must match
the reducer on both.

---

## Experiment 9 — Pig Latin

`09_analysis.pig` (NOT EXECUTED) ·
`09_pig_equivalent.py` — **runs**

The Python half walks the dataflow **one operator at a time**, which is how you
debug a Pig script anyway — that is what `ILLUSTRATE` does.

```
A = LOAD 'sales'                 -- 9 rows
B = FILTER A BY qty >= 6         -- 7 rows
C = GROUP B BY category          -- 3 groups: Grocery {4}, Personal {1}, Stationery {2}
D = FOREACH C GENERATE group, SUM(B.qty), SUM(B.revenue)
E = ORDER D BY revenue DESC      -- top category: Grocery
```

### ⚠️ `GROUP` produces a bag, not an aggregate

`(Grocery, {4 tuples})` — the bag is the value, and `FOREACH … GENERATE` turns
it into numbers. **Hive fuses the two; Pig keeps them apart**, which is why Pig
can do things to a group that SQL cannot express without a window function.

### 🎯 The two operators with no SQL equivalent

**`LOAD`** reads a semi-structured file with no schema declared in advance —
SQL assumes a table exists. **`ILLUSTRATE`** pushes sample rows through *every
step* of the plan.

Those two are the reason to reach for Pig on ETL.

### Lazy evaluation

**Nothing runs until `STORE` or `DUMP`.** Pig sees the whole dataflow first, so
it merges the `FILTER` into the `LOAD` and fuses consecutive `FOREACH`es into
one job. **Writing the steps separately costs nothing** — which is the whole
argument against nesting sub-queries "to avoid extra passes".

### The join hint that matters

`USING 'replicated'` is a **map-side join**: the small relation loads into
every mapper's memory and there is **no shuffle**. It dies with an
`OutOfMemoryError` if the relation does not fit — which is why broadcast joins
have a size threshold.

---

## Experiment 10 — Hive

`10_hive.hql` (NOT EXECUTED) ·
`10_hive_duckdb.py` — **runs**

### 🎯 The cross-course check

| Region | Revenue | Profit | Margin |
|---|---:|---:|---:|
| South | **10,360** | 2,760 | 26.64% |
| North | **2,520** | 765 | 30.36% |

**South = ₹10,360 is the same number Course 11's DAX `CALCULATE` measure
produced**, and the same one Spark produces in experiment 17. Two engines, two
languages, one dataset — asserted, so drift fails the suite.

### 🔢 Partition pruning

| Partition | Rows | Revenue | Scanned for Q2 |
|---|---:|---:|---:|
| `quarter=Q1` | 5 | 7,660 | **0** |
| `quarter=Q2` | 4 | 5,220 | **4** |
| total | 9 | 12,880 | **4 of 9** |

**A partition is an HDFS directory**, so `WHERE quarter='Q2'` reads one
directory — decided before a byte is read. The partition column is a directory
*name*, so it costs no storage.

**The trap:** partitioning by `date_key` here would make 4 directories for 9
rows — the small-files problem, created on purpose.

### 🔢 Bucketing, and an honest result

`CLUSTERED BY (store) INTO 3 BUCKETS` over three stores:

```
bucket 0: ['Guntur', 'Hyderabad']
bucket 1: (empty)
bucket 2: ['Vijayawada']
```

**Bucket 1 is empty.** Hashing does not distribute small key sets evenly, and
an empty bucket is still a file the job opens. Reporting that is worth more
than pretending the hash was balanced.

### Managed against external

**`DROP TABLE` on a MANAGED table deletes the data.** Use `EXTERNAL` for
anything you did not produce and cannot recreate — the classic Hive accident.

### `HAVING` against `WHERE`

Four products clear ₹1,000 (Grocery total ₹9,800). **`WHERE` filters rows,
`HAVING` filters groups** — and in Hive that is a job-plan difference: a
`WHERE` on a partition column prunes directories before the job starts, a
`HAVING` cannot.

### 🎯 What Hive is not

| Expectation | Reality |
|---|---|
| row-level `UPDATE`/`DELETE` | only with ACID + ORC + buckets |
| sub-second queries | seconds to minutes — it plans a **job** |
| indexes | **removed in Hive 3** |
| a server holding data | metadata only |
| enforced constraints | declarative, **not enforced** |

**Hive is a compiler.** Everything surprising follows from that sentence.

---

## Experiment 11 — Sqoop

`11_sqoop.sh` (NOT EXECUTED) ·
`11_sqoop_equivalent.py` — **runs**

**A real SQLite database at one end and a real Parquet file at the other.**
Only the cluster is missing.

Source: 90 rows, **₹128,800** — exactly ten times Course 11's ₹12,880.

### 🔢 Splitting by the primary key

```
step 1: SELECT MIN(order_id), MAX(order_id) -> 1, 90
step 2: four ranges, one per mapper
```

| Mapper | `WHERE` | Rows |
|---:|---|---:|
| 0 | `order_id >= 1 AND <= 22` | 22 |
| 1 | `order_id >= 23 AND <= 45` | 23 |
| 2 | `order_id >= 46 AND <= 67` | 22 |
| 3 | `order_id >= 68 AND <= 90` | 23 |

**Four TCP connections to the database.** Sqoop's parallelism is *database*
parallelism — `-m 20` against a production OLTP box is a denial of service you
wrote yourself.

### ⚠️ Splitting by a skewed column

| Mapper | `qty` range | Rows |
|---:|---|---:|
| 0 | 4..7 | **40** |
| 1 | 8..11 | 20 |
| 2 | 12..15 | 20 |
| 3 | 16..20 | **10** |

**Forty against ten.** Sqoop assumes the split column is uniformly distributed
between min and max. The job's wall clock is the slowest mapper, so a bad
`--split-by` wastes three quarters of your parallelism.

### The import is verified two ways

**90 rows and ₹128,800 both check out.** Counting rows alone would not catch a
truncated numeric type — an Oracle `NUMBER(38)` silently becoming a Java
`double` is the classic Sqoop corruption bug.

### 🎯 Neither incremental mode catches a DELETE

`--last-value 90` selects the 1 new row. **But Sqoop has no way to see a row
that is gone**, so an incrementally imported table drifts from its source. The
fix is a periodic full re-import — and knowing that is the difference between
having used Sqoop and having read about it.

---

## Experiment 12 — Flume

`12_flume.conf` (NOT EXECUTED) ·
`12_flume_equivalent.py` — **runs**

### The interceptor

```
headers {'host': '10.0.0.1', 'status': '200'}
body    (unchanged, 78 chars)
```

**An interceptor adds headers and leaves the body alone.** Headers are what a
multiplexing selector routes on, so "send 500s to the alert sink" is a header
rule, not code.

### 🔢 The channel, and back-pressure

| Configuration | Delivered | Rejected | Peak depth |
|---|---:|---:|---:|
| capacity 100, batch 10, fast sink | 40 | **0** | ≤10 |
| capacity 8, batch 4, **slow sink** | 40 | **8** | **8** |
| capacity 20, slow sink | 40 | **0** | 16 |
| capacity 100, slow sink | 40 | **0** | 16 |

**Eight events refused** because the sink could not drain the channel. In a
real agent the source then **blocks** — back-pressure travelling back to the
web server. **"Flume lost my events" almost always means "the channel was full
and the source gave up".**

**And the last two rows:** a bigger channel absorbs a longer burst and buys
nothing once the sink is permanently slower. **Buffers smooth bursts; they
cannot fix a throughput deficit.**

### What landed

`{'200': 24, '404': 8, '500': 8}`, evenly over four hosts (10 each).
**Those same numbers appear in experiments 14 and 17** — three code paths, one
set of figures.

### ⚠️ The defaults manufacture the small-files problem

`rollInterval` 30 s, `rollSize` 1024 bytes, `rollCount` 10 events → **40 events
produce ~4 HDFS files**, each a few hundred bytes. Left alone, Flume generates
the Unit 2 small-files problem at two files a minute.

---

## Experiment 13 — Avro and Parquet

`13_avro_parquet.py` —
**fully runs, on the real formats**

`fastavro` and `pyarrow` are real implementations, so **the files written here
are byte-for-byte readable by Hadoop, Hive and Spark.**

### Avro: self-describing

9 records, **938 bytes**, round-trip exact. The writer's schema is in the file
header — full name `in.ac.datascience.sales.Sale`, namespace included.

### 🎯 Schema evolution, demonstrated

```
read 9 OLD records with a NEW nine-field schema
the added field 'channel' comes back as None -- its DEFAULT
```

**The old file was not rewritten.** Avro resolves writer's schema against
reader's, field by field. **A field added without a default breaks exactly
this**, and that is the one rule to remember.

### Parquet: column projection

| Column | Bytes |
|---|---:|
| profit | 150 |
| qty | 144 |
| **revenue** | **143** |
| product | 125 |
| category | 111 |
| store | 110 |
| date_key | 83 |
| region | 83 |
| **total** | **949** |

**`SELECT revenue` reads 143 of 949 column bytes — 15.1%.**

**Predicate pushdown:** row-group statistics for `revenue` are **min 600, max
2,800**, so a query for `revenue > 5000` skips the entire row group without
decoding a byte.

### ⚠️ The compression claim, told honestly

| Data | CSV | Avro | Parquet | CSV/Parquet |
|---|---:|---:|---:|---:|
| **9 rows** | 533 | 938 | **2,584** | **0.2×** |
| 108,000 rows, **repetitive** | 5,700,058 | 5,924,190 | 18,790 | **303.4×** |
| 108,000 rows, **varied** | 6,269,519 | 6,380,506 | 522,264 | **12.0×** |

**On nine rows Parquet is 4.8× LARGER than CSV.** The 303× is an artefact of
12,000 identical copies. Give every row a distinct store and revenue and it
falls to **12.0×** — and even that is optimistic. In production, 3× to 10×.

**A columnar format's headline ratio is mostly a statement about how
repetitive your data is**, and a benchmark on duplicated rows says nothing at
all.

---

## Experiment 14 — Batch and streaming, joined

`14_pipeline.py` — **runs
end to end**

SQLite → Parquet (batch), log events → Parquet (streaming), then a real DuckDB
query across both.

### 🔢 The fan trap

```
events counted through the join: 90
events actually ingested       : 40
```

**Each host appears in several orders, so every event is counted once per
matching order.** This is **the same fan trap Course 11 found in a Power BI
model** — not a SQL problem, a **grain** problem, appearing wherever two fact
tables are joined directly.

### 🎯 The fix

| host | orders | revenue | events | errors |
|---|---:|---:|---:|---:|
| 10.0.0.1 | 3 | 4,200 | 10 | 2 |
| 10.0.0.2 | 2 | 3,220 | 10 | 2 |
| 10.0.0.3 | 2 | 2,800 | 10 | 2 |
| 10.0.0.4 | 2 | 2,660 | 10 | 2 |
| **total** | **9** | **12,880** | **40** | **8** |

**Aggregate each side to a common grain first, then join.** Both totals now
reconcile with the sources. That single rule prevents most wrong numbers in a
data warehouse.

### The row that changes the design

**"Late data is normal."** A streaming aggregate for 09:00 is not final at
10:00, so either you accept eventual correctness or you keep a watermark and
re-emit. The batch leg has no such problem — which is exactly why the **Lambda
architecture** keeps both, and why **Kappa** removes the batch layer by making
the stream replayable.

**Lambda's real cost is not machines — it is the same business rule living in
two codebases and drifting.**

---

## Experiment 15 — HBase

`15_hbase.rb` (NOT EXECUTED) ·
`15_hbase_model.py` — **runs**

### ⚠️ The row key that silently loses a sale

```
row key 'region#store#date' over 9 fact rows
produces only 8 DISTINCT KEYS -- 1 row would be overwritten
```

Vijayawada sold Rice **and** Shampoo on D1. **HBase would not complain** — it
would version one over the other. **A row key must be unique at the grain**,
and in HBase nothing checks that for you.

### Versions

```
ts=38   111
ts=37    99
ts=19    20
```

**A `put` to an existing cell adds a version; it does not overwrite.**

### ⚠️ A delete makes the table bigger

```
DELETE info:category   readable? no    cells: 38 -> 39
```

**A tombstone.** Data and marker disappear only at major compaction — the
answer to "I deleted a billion rows and disk usage went up".

### Scans

`SCAN 'South'..'South~'` → 6 rows; `'North'..'North~'` → 3. **A prefix scan
reads exactly the rows you want, sequentially** — and works only because
`region` is the *first* component of the key.

**Ask it the wrong way** — `category = 'Grocery'` — and it is a **full table
scan**. HBase has no secondary index.

### 🎯 Row key design

| Key | Writes go to | Verdict |
|---|---|---|
| timestamp | the last region | **HOTSPOT** |
| sequential id | the last region | **HOTSPOT** |
| `md5(id) + id` | everywhere | good — **scans lost** |
| `region#store#date#product` | by region | good — **prefix scans work** |

**You cannot have even write distribution and range scans on the same
dimension. Choosing is what row-key design means.**

---

## Experiment 16 — ZooKeeper

`16_zookeeper.sh` (NOT EXECUTED) ·
`16_zookeeper_model.py` — **runs**

### Leader election

```
nn1 -> lock-0000000000     LEADER: nn1
nn2 -> lock-0000000001
nn3 -> lock-0000000002

nn1's session expires:  new LEADER: nn2
```

**Nobody ran a failover script.** The ephemeral node was deleted **by the
server**, the watch fired, and nn2 saw itself at the head of the queue. **That
is how HDFS NameNode HA works** — the link back to experiment 5.

### ⚠️ Watch your predecessor, not the leader

Watching the leader wakes **every** candidate on one failure — the **herd
effect**. Watching your immediate predecessor wakes exactly one.

### The lock is the same recipe

```
jobA holds the lock
jobA CRASHES -- lock passes to jobB automatically
```

**Released by the session dying, not by the client remembering.** A database
lock survives its holder's crash and deadlocks the system; an ephemeral znode
cannot.

### 🔢 Ensemble sizing

| Servers | Quorum | Can lose | Verdict |
|---:|---:|---:|---|
| 3 | 2 | **1** | good |
| **4** | 3 | **1** | **same as 3** |
| 5 | 3 | 2 | good |
| 6 | 4 | 2 | same as 5 |
| 7 | 4 | 3 | good |

**Four servers tolerate one failure — exactly what three tolerate.** The fourth
machine buys nothing and adds a write to every quorum. **3, 5 or 7.**

---

## Experiment 17 — Spark

`17_spark_hbase.scala` (NOT EXECUTED) ·
`17_spark.py` — **runs on a
REAL SparkSession**

```
real SparkSession: version 4.2.0, master local[2]
```

PySpark installs from PyPI and Java 21 is present, so a genuine session
starts, real RDDs are built, and a **real shuffle** happens inside
`reduceByKey`. **What is not real is HBase** — the connector code is in the
Scala file.

### The RDD word count

**26 distinct words, 48 total — identical to experiment 7's MapReduce answer**,
on a real distributed engine.

### 🎯 `reduceByKey` against `groupByKey`

| | What crosses the network |
|---|---|
| `groupByKey` | **all 48 pairs**, then counts |
| `reduceByKey` | combines to **35** map-side — `[11, 14, 10]` per partition |

**Note 35, not experiment 7's 39.** Spark's three partitions each hold two
documents, so more merging happens per task. **The combiner's saving depends
on the split**, exactly as Unit 3 said — and this is the same measurement made
two ways.

### Lazy evaluation

Three transformations queued; **`.collect()` is the action** that submits the
DAG. That is why a typo in a `map()` surfaces at `collect()`.

### 🎯 The cross-course check, third engine

| Region | Revenue | Profit |
|---|---:|---:|
| South | **10,360** | 2,760 |
| North | **2,520** | 765 |

**Course 11's DAX, DuckDB and Spark all produce ₹10,360.**

### The logs from experiment 12

`HTTP 200: 24, 404: 8, 500: 8` — **the same 24 / 8 / 8 the Flume agent
produced.** Ingest with Flume, analyse with Spark, on bytes never transformed
in between.

### `cache()`

```
two actions over the same RDD, sum = 39,999,800,000
storage level: Memory Serialized 1x Replicated
```

**Without `cache()` the second action recomputes the whole lineage.** Caching
is the highest-value Spark optimisation and the one students forget —
**because nothing fails without it; the job is merely twice as slow.**

### ⚠️ The Spark-over-HBase caveat

**One Spark partition per HBase region** is the whole integration. But **never
`put()` per row from a Spark job** — write HFiles and bulk-load them.

And: **a full-table Spark scan of HBase is slower than the same data in
Parquet**, because HBase stores every cell with its row key, family, qualifier
and timestamp. **If every job is a full scan, the data is in the wrong store.**

---

## What the runner asserts

| Script | Experiments | Real tool? |
|---|---|---|
| `04_blocks_replication.py` | 4 | arithmetic |
| `05_fault_tolerance.py` | 5 | model |
| `06_yarn_scheduling.py` | 6 | model |
| `07_wordcount.py` | 7 | **explicit MapReduce engine** |
| `08_inverted_index.py` | 8 | same engine |
| `09_pig_equivalent.py` | 9 | dataflow, step by step |
| `10_hive_duckdb.py` | 10 | **real SQL, DuckDB** |
| `11_sqoop_equivalent.py` | 11 | **real SQLite + real Parquet** |
| `12_flume_equivalent.py` | 12 | agent semantics |
| `13_avro_parquet.py` | 13 | **real Avro + real Parquet** |
| `14_pipeline.py` | 14 | **real end-to-end** |
| `15_hbase_model.py` | 15 | model |
| `16_zookeeper_model.py` | 16 | model |
| `17_spark.py` | 17 | **REAL APACHE SPARK** |

Plus the audit: **15 files, every one carrying `*** NOT EXECUTED ***`.**

**Experiment 17 skips loudly** if the PySpark environment is absent — the same
graceful-skip pattern Course 7 uses for jsdom. A skip is not a pass, and the
runner says so.

---

## Lab examination

Two hours on a cluster, one experiment number, then a viva.

**What costs marks:**

- Saying a 260 MB file occupies three full blocks
- Multiplying NameNode metadata by the replication factor
- Calling the Secondary NameNode a standby
- Setting a combiner for a mean
- Assuming the map key is a line number
- Iterating the reduce `Iterable` twice
- `--split-by` on a skewed or text column
- `exec tail -F` as a Flume source
- Leaving Flume's rollover at the defaults
- Designing an HBase row key on a timestamp
- Recommending a 4-server ZooKeeper ensemble
- Saying "Spark replaced Hadoop"

**What earns them:**

- **The block table from memory.** 260 MB → 128 + 128 + 4.
- **The small-files factor: 222,222.** One number that justifies HDFS's whole
  design.
- **"Any two failures survive; only some threes are fatal."** 6 of 20, not
  "it breaks at three".
- **"104 container-seconds either way."** Scheduling moves latency, it does
  not create throughput.
- **"The combiner saved 18.75% here because the splits are tiny."** Naming why
  a result is unimpressive is stronger than quoting an impressive one.
- **Reporting the empty bucket.** Hashing three keys into three buckets left
  one empty, and saying so beats pretending otherwise.
- **The three compression ratios: 0.2×, 303×, 12×** — and saying which one to
  quote and why.
- **"Aggregate to a common grain, then join."** Nine words that prevent the
  fan trap.
- **"You cannot have even write distribution and range scans."** The one
  sentence of HBase row-key design.
- **"3, 5 or 7 — four tolerates what three does."**
- **₹10,360 from three engines.** The check that makes the rest believable.
