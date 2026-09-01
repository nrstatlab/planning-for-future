# Course 12 B — Practice Questions with Worked Solutions

Every figure quoted here is produced by
`labs/course-12b-bigdata/` and checked by
`tools/run_bigdata_labs.py`.

---

## Section A — Two-mark questions

**1. Define big data in one sentence.**
Data whose volume, velocity or variety breaks the assumptions of a single
machine — most usefully, **data whose cost to move exceeds its cost to
compute on**.

**2. Name the five Vs.**
Volume, Velocity, Variety, Veracity, Value.

**3. What are the four core components of Hadoop?**
**HDFS**, **YARN**, **MapReduce**, **Hadoop Common**. The last is the one most
answers forget.

**4. State the data locality principle.**
Moving computation is cheaper than moving data, so the scheduler sends the
task to the node holding the block.

**5. What is the default HDFS block size?**
**128 MB** (64 MB before Hadoop 2).

**6. How many blocks does a 260 MB file occupy?**
**Three** — 128 + 128 + **4**. The last block is short; HDFS does not pad.

**7. Why is the block size so large?**
So that **seek time is about 1% of transfer time**. At 10 ms seek and
100 MB/s, a 128 MB block spends its life transferring, not seeking.

**8. What does the NameNode hold in RAM but never write to disk?**
The **block map** — block → DataNode locations. It is rebuilt from block
reports at startup, which is why safe mode exists.

**9. What is the Secondary NameNode for?**
It **merges `fsimage` with the edit log** so restarts stay fast. **It is not a
standby and cannot take over.**

**10. How long before a DataNode is declared dead?**
`10 × 3 s + 2 × 5 min = ` **630 seconds**, deliberately long so a five-minute
reboot does not trigger a cluster-wide copy storm.

**11. State the default replica placement policy.**
Replica 1 on the writer's node; replica 2 on **another rack**; replica 3 on a
different node of **that same second rack**.

**12. Why two racks and not three?**
A third rack would double cross-rack write traffic to guard against losing
*two* racks, which is far rarer than losing one.

**13. Name the four YARN components.**
ResourceManager (one per cluster), NodeManager (one per node),
ApplicationMaster (**one per job**), Container (one per task).

**14. What single change defined YARN relative to Hadoop 1?**
**One ApplicationMaster per job**, splitting cluster scheduling from job
management — which is why YARN can run Spark and Flink, not only MapReduce.

**15. Which scheduler guarantees a queue a minimum share?**
The **Capacity Scheduler**.

**16. Give the map and reduce signatures.**
`map: (k1,v1) → list of (k2,v2)`; `reduce: (k2, list of v2) → list of (k3,v3)`.

**17. Where does map output go?**
**Local disk**, unreplicated, deleted when the job ends. Not HDFS.

**18. What is a combiner?**
A reducer run **map-side, inside one map task**, before the shuffle. It is an
optimisation and must not change the answer.

**19. Give one aggregate for which a combiner is unsafe.**
**Mean** — mean of means is not the mean. Measured: **6.6250** against a true
**4.6000**.

**20. What is the default partitioner?**
`(hash(key) & MAXINT) % numReduceTasks`.

**21. Is the MapReduce map key a line number?**
**No — a byte offset** within the split.

**22. How many times can the reduce `Iterable` be walked?**
**Once.** It streams from disk.

**23. In one sentence, what is Hive?**
**A compiler**: HiveQL in, a MapReduce/Tez/Spark job out.

**24. What is a Hive partition, physically?**
**An HDFS directory.** The partition column is a directory name, not a column
in the data files.

**25. Difference between a managed and an external Hive table.**
`DROP TABLE` on a **managed** table deletes **the data**; on an **external**
table it deletes only the metadata.

**26. What does `ILLUSTRATE` do, and what is its SQL equivalent?**
It pushes sample rows through **every step** of a Pig plan. **There is no SQL
equivalent.**

**27. What does `GROUP` produce in Pig?**
**A bag per key**, not an aggregate. `FOREACH … GENERATE` turns it into
numbers.

**28. What SQL does Sqoop run before launching mappers?**
`SELECT MIN(col), MAX(col) FROM table` — then it splits that range.

**29. What does `--split-by` assume?**
That the column is **uniformly distributed** between its min and max.

**30. Name the two incremental import modes and what neither catches.**
`append` and `lastmodified`. **Neither catches a `DELETE`.**

**31. Name the three parts of a Flume agent.**
**Source, channel, sink** (plus interceptors and a channel selector).

**32. What does a Flume interceptor modify?**
**Headers only.** It never touches the event body.

**33. Which Flume source should you use, and which should you avoid?**
Use **`TAILDIR`** (it has a position file). Avoid `exec tail -F` — it loses
everything on restart.

**34. Which of Avro and Parquet is columnar?**
**Parquet.** Avro is a row format.

**35. Where does Avro store its schema?**
**In the file header** — so an Avro file is self-describing.

**36. What breaks Avro schema evolution?**
**Adding a field without a default.**

**37. Give the one-sentence HBase data model.**
A **sparse, distributed, persistent, multidimensional sorted map** indexed by
row key, column family, column qualifier and timestamp.

**38. What does a `put` to an existing cell do?**
**Adds a version.** It does not overwrite.

**39. Why does a delete make an HBase table bigger?**
It writes a **tombstone**. Data and marker disappear only at **major
compaction**.

**40. Does HBase have secondary indexes?**
**No.** A query on a non-key column is a full table scan with a server-side
filter.

**41. Name the two special znode types.**
**Ephemeral** (vanishes when the session dies) and **sequential** (numbered by
a single authority).

**42. Why are ZooKeeper ensembles 3, 5 or 7?**
**Four servers tolerate one failure — exactly what three tolerate**, while
adding a write to every quorum.

**43. In leader election, which node do you watch?**
**Your immediate predecessor**, not the leader — otherwise one failure wakes
every candidate (the **herd effect**).

**44. What is an RDD's lineage for?**
**Recomputing a lost partition.** Fault tolerance without replication.

**45. Give one difference between `reduceByKey` and `groupByKey`.**
`reduceByKey` combines **map-side** before the shuffle; `groupByKey` moves
every record. Measured: **35 records against 48**.

**46. What did Spark replace?**
**MapReduce** — not Hadoop. It runs on YARN over HDFS.

**47. Qualify the "Spark is 100× faster" claim.**
It is a claim about **iterative** jobs, where MapReduce writes to HDFS between
every pass and Spark does not.

**48. What happens if you forget `cache()`?**
The next action **recomputes the whole lineage**. Nothing fails — the job is
merely twice as slow.

---

## Section B — Five-mark questions

### 1. Explain the HDFS write path, and why a pipeline

```
1. Client → NameNode:  create /path/f
2. NameNode: checks permissions and non-existence, writes the edit log,
             returns the DataNode PIPELINE
3. Client → DN1 → DN2 → DN3    in 64 KB packets, each forwarding as it receives
4. acknowledgements travel BACK up the pipeline
5. Client → NameNode:  complete
```

**Why a pipeline and not three parallel copies:** if the client sent three
copies, **its upload bandwidth would be the bottleneck** and it would carry 3×
the data. In a pipeline it sends once and each DataNode forwards while
receiving, so total time is roughly **one** transfer.

**And it is fault tolerant mid-write:** if a DataNode dies, it is removed from
the pipeline, the write continues with the survivors, and the NameNode
re-replicates later. **The client sees no error.**

### 2. Explain the small-files problem with figures

The NameNode holds the whole namespace in RAM at roughly **150 bytes per
file, directory and block object**.

| Scenario | Files | Blocks | NameNode RAM |
|---|---:|---:|---:|
| one 1 GB file | 1 | 8 | **1,350 bytes** |
| 1,000 × 1 MB | 1,000 | 1,000 | 0.29 MB |
| 1,000,000 × 1 KB | 1,000,000 | 1,000,000 | **286.10 MB** |

**The same gigabyte costs a factor of 222,222 more** as a million small files.

**And it appears in places that look unrelated:** Flume's default rollover
(30 s / 1 KB / 10 events) manufactures it continuously; over-partitioning a
Hive table creates it deliberately; SequenceFiles and HAR archives exist to
undo it.

### 3. Explain combiners, including when one is unsafe

A combiner is **the reducer run map-side, inside one map task**, before the
shuffle. Hadoop may run it zero, one or several times, so it must be
associative and commutative and must not change the answer.

**Measured on the lab corpus:** shuffle falls from **48 to 39 records —
18.75%**.

**And the honest caveat:** that saving is small because the documents are 5 to
11 words, so there is almost nothing to merge *within one split*. **The
combiner's value scales with split size.** On a 128 MB split of real text it
cuts the shuffle by orders of magnitude.

| Reducer computes | Safe? | Why |
|---|---|---|
| sum, max, min, count | **yes** | associative |
| **mean** | **NO** | mean of means is not the mean |
| median | **NO** | needs every value at once |

**Demonstrated:** `[1,1,1,10]` and `[10]` give mean-of-means **6.6250** against
a true mean of **4.6000**. The fix is to emit `(sum, count)` pairs and divide
only in the reducer — which also satisfies Hadoop's requirement that the
combiner's input and output types match the reducer's.

### 4. Compare the three YARN schedulers, with figures

Measured on an 8-container cluster, four jobs, 104 container-seconds of work:

| Job | FIFO | Fair |
|---|---:|---:|
| `big_etl` (8 containers, 10 s) | **10** | 14 |
| `small_q1` (1 container, 2 s) | **11** | **1** |
| `small_q2` | 12 | 1 |
| `medium` | 16 | 5 |
| **total turnaround** | **49** | **21** |

- **FIFO** — `small_q1` waits 11 s for 2 s of work. Head-of-line blocking.
- **Fair** — equal share among running jobs. `big_etl` finished *later*
  (10 → 14): latency moved, it was not removed.
- **Capacity** — queues with guaranteed percentages. The adhoc queue holds 2
  containers whatever else runs, so a short query has a **guarantee**; the cost
  is idle capacity unless elasticity is enabled.

**The honest framing:** the work is **104 container-seconds either way**, which
on 8 containers cannot finish before second 13. Scheduling **cannot create
throughput** — but idle-while-queued is real waste, which is why the total
still halved.

### 5. Explain partitioning and bucketing in Hive, with the trap in each

**Partitioning** puts each value in its own HDFS **directory**, so a `WHERE`
on the partition column prunes directories before the job starts.

| Partition | Rows | Scanned for Q2 |
|---|---:|---:|
| `quarter=Q1` | 5 | **0** |
| `quarter=Q2` | 4 | **4** |

**The trap:** partition on something with **few** distinct values. Partitioning
nine rows by date makes four directories — the small-files problem, on purpose.

**Bucketing** hashes a column into a fixed number of **files** inside a
partition. Two tables bucketed identically join **bucket to bucket with no
shuffle**.

**The trap, measured:** three stores into three buckets left **bucket 1
empty**. Hashing does not distribute small key sets evenly, and an empty
bucket is still a file the job opens.

**The rule:** partition by quarter or month; bucket by customer id.

### 6. Explain Avro schema evolution

Avro stores the **writer's schema in the file header**, and resolves it
against the **reader's** schema field by field at read time.

**Demonstrated:** nine records written with an eight-field schema were read
back with a nine-field schema adding `channel` with a default of `null`:

```
read 9 OLD records with a NEW schema
'channel' comes back as None -- its DEFAULT
```

**The old file was not rewritten**, which is the whole point: you can add a
field today without touching five years of history.

**The one rule:** a field added **without** a default breaks exactly this,
because the reader has no value to substitute. Removing a field is safe if it
had a default; renaming requires an `aliases` entry.

### 7. Explain column projection and predicate pushdown in Parquet

Parquet stores each **column** contiguously, with statistics per row group.

**Column projection**, measured on the lab file:

| Column | Bytes |
|---|---:|
| **revenue** | **143** |
| everything else | 806 |
| **total** | **949** |

`SELECT revenue` reads **143 of 949 column bytes — 15.1%**. A row format must
read every row in full and discard seven fields.

**Predicate pushdown:** the row-group statistics for `revenue` are **min 600,
max 2,800**. A query for `revenue > 5000` **skips the entire row group without
decoding a byte**. On a partitioned dataset this is often a bigger win than
the compression.

**Together these are what replaced indexes** — which is why Hive dropped them
in version 3.

### 8. Explain back-pressure in Flume

The channel is a **bounded buffer**. When the sink cannot drain it as fast as
the source fills it, the channel refuses events and **the source blocks** —
back-pressure travelling back up the pipe to the web server.

| Configuration | Rejected | Peak depth |
|---|---:|---:|
| capacity 8, slow sink | **8** | 8 |
| capacity 20, slow sink | **0** | 16 |
| capacity 100, slow sink | **0** | 16 |

**"Flume lost my events" almost always means "the channel was full and the
source gave up".**

**And the last two rows are the lesson:** a bigger channel absorbs a longer
**burst** and buys nothing once the sink is permanently slower. **Buffers
smooth bursts; they cannot fix a throughput deficit.** The real fixes are a
larger sink `batchSize`, more sinks, or a faster sink.

---

## Section C — Ten-mark questions

### 1. Describe HDFS architecture in full

**The shape.** One **NameNode** holds the namespace in RAM; many **DataNodes**
hold the blocks as ordinary files on local disk. **The NameNode never touches
your data** — a client asks it *where* a block is and reads it directly from
the DataNode, which is why one master can serve thousands of nodes.

**Blocks.** Default **128 MB**, chosen so seek is ~1% of transfer. A block is a
logical **maximum**: 260 MB is **128 + 128 + 4**, and HDFS wastes no space on
padding. But 128 MB is one block and 129 MB is two — one byte past the
boundary costs a whole block *object*.

**The small-files problem.** ~150 bytes per object in NameNode RAM, so a
gigabyte costs **1,350 bytes** as one file and **286 MB** as a million small
ones — a factor of **222,222**.

**Replication and rack awareness.** Replica 1 on the writer's node, replica 2
on another rack, replica 3 on that second rack. **Every block spans exactly two
racks**, so a whole-rack failure loses nothing. A third rack would double
cross-rack write traffic for a far rarer failure.

**The write path** is a **pipeline** (client → DN1 → DN2 → DN3), not three
parallel copies, so the client's upload bandwidth is not the bottleneck. **The
read path** returns DataNodes **sorted by network distance**, which is data
locality doing its work.

**Fault tolerance, honestly.** Measured over every combination on 6 nodes in
2 racks:

| Nodes down | Combinations losing data |
|---:|---|
| 1 | 0 of 6 |
| 2 | **0 of 15** |
| 3 | **6 of 20** |

**Any two failures are survivable; only some threes are fatal** — 14 of 20
three-node combinations still lose nothing, because a whole-rack failure is
one of the safe cases. A DataNode is declared dead after **630 s**,
deliberately long.

**NameNode failure is different in kind.** `fsimage` and `edits` are on disk
and survive; **the block map is RAM-only** and is rebuilt from block reports,
which is why a large NameNode takes minutes to leave safe mode. **The
Secondary NameNode is a checkpointer, not a standby** — HA needs two
NameNodes, a Quorum Journal Manager and **ZooKeeper**.

**Write once, append only.** There is no random write and no `cd`. That single
constraint lets HDFS drop file locking entirely — and it is why **HBase
exists**.

### 2. Explain the MapReduce model in full, with word count traced

**The model in four lines:**

```
map    : (k1, v1)         -> list of (k2, v2)
shuffle: gather every (k2, v2) with the same k2 onto one reducer
reduce : (k2, list of v2)  -> list of (k3, v3)
```

**You write map and reduce; the framework does the shuffle.** You give up
general programming and receive parallelism, fault tolerance and data locality.

**The five phases:** input split (one per block) → **map** (output to **local
disk**, unreplicated) → optional **combine** (per map task) → **partition**
(`hash(key) % reducers`) → **shuffle and sort** (**the network step**) →
**reduce** (output to HDFS).

**Traced on `["a b a", "b c"]` with two reducers:**

```
MAP        (a,1)(b,1)(a,1)   |   (b,1)(c,1)
COMBINE    (a,2)(b,1)        |   (b,1)(c,1)      -- per task
PARTITION  a,c -> R0;  b -> R1
SHUFFLE    R0: (a,2)(c,1)    |   R1: (b,1)(b,1)
REDUCE     a=2, c=1          |   b=2
```

**Note what the combiner could and could not do:** it merged split1's two
`a`s and could do nothing for `b`, which appears once in each split. That is
exactly why combiner savings depend on split size.

**Measured on the lab corpus:** map output **48**, shuffled **48**, reduce
output **26** — and the counts sum back to 48, because **reduce is a
regrouping**. With a combiner, shuffled falls to **39 (18.75%)**.

**The shuffle is the only expensive step.** Map and reduce are local and
parallel; the shuffle moves every intermediate record across the network.
**Every optimisation in big data — combiners, partitioners, `reduceByKey`,
bucketed joins, columnar formats — is an attempt to shuffle less.**

**Skew, not volume, kills jobs.** Three reducers gave partitions of
**[20, 17, 11]** on 26 keys; on a real corpus one reducer gets `the` and the
job's wall clock is that reducer. Fixes, in order: change the key (salt the
hot one), a custom partitioner, a combiner. **More reducers does not help** —
the hot key still lands on one.

**Three Java details that are examined:** the map key is a **byte offset**;
**reuse the `Writable` objects** or GC becomes the job; the reduce `Iterable`
**streams and can be walked once**.

### 3. Compare Avro, Parquet and SequenceFile, and explain why quoted compression ratios mislead

**The one distinction:** a **row** format stores record 1 in full then record
2; a **column** format stores every value of column 1 then every value of
column 2. Everything else follows.

| | **Avro** (row) | **Parquet** (column) | **SequenceFile** (row) |
|---|---|---|---|
| Schema | **in the file** | in the footer | external |
| Write one record | **cheap** | expensive — buffers a row group | cheap |
| Read one column | expensive | **cheap** | expensive |
| Evolution | **first class** | limited | none |
| Predicate skip | no | **yes, row-group stats** | no |
| Status | **current** | **current** | legacy |
| Use for | ingestion, streaming | **analytics** | packing small files |

**Avro's property that matters** is the embedded schema: nine old records were
read back with a nine-field schema and the added field came back as its
default, **without rewriting the file**. A field added without a default
breaks exactly this.

**Parquet's are column projection and pushdown:** `SELECT revenue` read
**143 of 949 column bytes (15.1%)**, and row-group statistics
(`revenue` min 600, max 2,800) let `revenue > 5000` skip the group entirely.

**Now the honest part.** Measured on the *same* schema:

| Data | CSV | Parquet | Ratio |
|---|---:|---:|---:|
| **9 rows** | 533 | **2,584** | **0.2× — Parquet is LARGER** |
| 108,000 rows, **repetitive** | 5,700,058 | 18,790 | **303.4×** |
| 108,000 rows, **varied** | 6,269,519 | 522,264 | **12.0×** |

Three things to say:

1. **At nine rows Parquet loses**, because the footer, schema and per-column
   metadata are fixed overhead that nine rows cannot amortise.
2. **The 303× is an artefact** — 12,000 identical copies of nine rows
   dictionary-encode to almost nothing.
3. **12.0× is the defensible figure, and even it is optimistic**, because date,
   region and category are still repetitive. Production ratios land between
   **3× and 10×**.

**A columnar format's headline compression number is mostly a statement about
how repetitive the data is.** A benchmark on duplicated rows says nothing at
all, and quoting one is how people get caught in a viva.

**The architecture uses both formats:** Avro at the edge, where records arrive
one at a time and schemas drift; a batch job converts to Parquet for the query
layer.

### 4. Design an end-to-end ingestion pipeline for a retail chain

**Requirement:** 2,000 stores, nightly RDBMS extracts of orders and customers,
continuous point-of-sale events, nightly reports and real-time fraud alerts.

**The batch leg.** Sqoop (or, today, a CDC tool) imports `orders` and
`customers` nightly:

```bash
sqoop import --table orders --split-by order_id -m 8 \
  --as-parquetfile --compress --compression-codec snappy \
  --null-string '\N' --null-non-string '\N' --password-file /user/etl/.pw
```

**Split by the primary key**, because Sqoop assumes uniform distribution:
splitting the lab's 90 rows by `order_id` gave **22/23/22/23**, and splitting
by `qty` gave **40/20/20/10**. **Import from a read replica** — eight mappers
are eight concurrent range scans against a production OLTP box.

**The streaming leg.** Point-of-sale events through Flume (today, Kafka) with a
**`TAILDIR`** source, a **file channel** (fraud alerts must not be lost, so a
memory channel is disqualified), and an HDFS sink with **`rollCount = 0`,
`rollSize` = one block, `rollInterval` = 10 min** — because the defaults
(30 s / 1 KB / 10 events) manufacture the small-files problem at two files a
minute.

**Formats.** **Avro** in the landing zone: records arrive one at a time,
schemas will change, and the schema must travel with the file. **Parquet** in
the query layer, partitioned by date, because every report is a column
aggregate.

**Query.** Hive over the Parquet tables, partitioned by `dt` and bucketed by
`store_id` — so nightly reports prune directories and store-level joins avoid
a shuffle. Spark for the fraud model, because it is iterative.

**What can go wrong, and it is the half that earns marks:**

1. **The fan trap.** Joining the orders table to the events table directly
   inflated the event count from **40 to 90** in the lab — the same defect
   Course 11 found in a Power BI model. **Aggregate each side to a common
   grain, then join**; both totals then reconciled at 40 events and ₹12,880.
2. **Deleted rows.** Neither incremental mode sees a `DELETE`, so the imported
   table drifts. Schedule a periodic full re-import.
3. **Late data.** The streaming aggregate for 09:00 is not final at 10:00, so
   the nightly report and the dashboard will disagree by a percent or two.
   **That is not a bug** — it is the defining property of the two legs, and it
   is why the **Lambda architecture** treats batch as the source of truth.
4. **Truncated numerics.** Verify imports by **row count *and* the sum of a
   money column** — an Oracle `NUMBER(38)` becoming a Java `double` is the
   classic silent corruption.

**And the architectural conclusion:** Lambda's real cost is that the same
business rule lives in two codebases and drifts. **Kappa** removes the batch
layer by making the stream replayable — which is why Kafka replaced Flume in
these pipelines after about 2016.

### 5. Explain HBase's data model and design a row key

**The definition:** a **sparse, distributed, persistent, multidimensional
sorted map**, indexed by `(row key, column family, column qualifier,
timestamp)`.

- **sparse** — a missing value stores nothing, not a null
- **sorted** — by row key, always, which makes range scans fast
- **multidimensional** — the fourth dimension is **time**
- **map** — get, put, scan. No query language, no joins.

**Column families are fixed at create time; qualifiers are free.** Keep
families to two or three: each is a separate store file and a flush of one
flushes all.

**Versions and deletes, measured:** a `put` to an existing cell **adds a
version** (`VERSIONS => 3` caps it). A **delete writes a tombstone and the
table gets BIGGER** — 38 cells to 39. Both disappear only at **major
compaction**. That is the answer to "I deleted a billion rows and disk usage
went up".

**Row key design is the whole job.**

| Key | Writes go to | Verdict |
|---|---|---|
| timestamp | the last region | **HOTSPOT** |
| sequential id | the last region | **HOTSPOT** |
| `md5(id) + id` | everywhere | good — **range scans lost** |
| `region#store#date#product` | by region | good — **prefix scans work** |

**A monotonic row key sends every write to one RegionServer**, so a 50-node
cluster runs at the speed of one node. Salting fixes it and destroys range
scans. **You cannot have both, and choosing is what row-key design means.**

**And uniqueness is not checked for you.** Keying the lab's nine facts by
`region#store#date` produced **only 8 distinct keys** — Vijayawada sold Rice
*and* Shampoo on the same day, and HBase would silently version one over the
other. **In an RDBMS the primary key declaration catches this; in HBase
nothing does.**

**For "all readings from sensor X between two times":** use
`sensorId#timestamp` — sensor first so one sensor's readings are contiguous
and the query is a single range scan; timestamp second so the range is a
prefix. **Not `timestamp#sensorId`**, which hotspots writes *and* makes the
query a full scan. Reverse the timestamp if "the latest N" is the common query.
If one sensor dominates, salt with `hash(sensorId) % 16` — and accept that
cross-sensor scans are then gone.

**Finally, the query it cannot do:** `category = 'Grocery'` is a **full table
scan** with a server-side filter, because **HBase has no secondary index**.
You build a second table keyed by category and keep it in sync yourself.

### 6. Explain ZooKeeper's role, and what breaks when it loses quorum

**What it is:** a small, strongly-consistent tree, interesting for exactly two
properties — **ephemeral nodes vanish when their session dies**, and
**sequential nodes are numbered by a single authority**. Every recipe is built
from those two facts.

**Leader election.** Each candidate creates an ephemeral sequential znode; the
**lowest sequence number leads**. Measured:

```
nn1 -> lock-0000000000    LEADER: nn1
nn1's session expires  →  new LEADER: nn2
```

**Nobody ran a failover script.** The server deleted the node when the
heartbeat stopped, the watch fired, and nn2 saw itself at the head.

**Watch your predecessor, not the leader** — otherwise one failure wakes every
candidate. The recipe is a **thundering-herd fix**, not an arbitrary
convention.

**Distributed locking is the same recipe**, and the lock is released **by the
session dying**, not by the client remembering. A database lock survives its
holder's crash and deadlocks the system; an ephemeral znode cannot.

**Atomic create** gives "whoever creates `/master` is the master" — a complete
election algorithm in one line, working only because ZooKeeper **linearises**
writes.

**Quorum arithmetic:**

| Servers | Quorum | Can lose |
|---:|---:|---:|
| 3 | 2 | 1 |
| **4** | 3 | **1 — same as 3** |
| 5 | 3 | 2 |
| 7 | 4 | 3 |

**Ensembles are 3, 5 or 7.** The fourth machine buys nothing and adds a write
to every quorum.

**What breaks on quorum loss.** With 5 servers, losing 2 is fine; **losing 3
stops all writes**. Then:

- **HDFS HA cannot fail over** — a NameNode crash becomes an outage
- **YARN RM HA cannot fail over**
- **HBase cannot assign regions** — any RegionServer failure leaves its rows
  unavailable

**Nothing is corrupted; every coordination decision in the cluster freezes.**
That is why the ensemble is the most carefully operated part of the stack, and
why "every HA story in the Hadoop ecosystem ends at ZooKeeper" is the sentence
to write.

---

## The six things most likely to be examined

1. **The block table.** 260 MB → **128 + 128 + 4**, and 129 MB → 2 blocks.
2. **The small-files factor: 222,222.** One number that justifies HDFS's whole
   design.
3. **"Any two failures survive; 6 of 20 threes are fatal."** The honest form
   of the replication claim.
4. **The combiner that is wrong.** Mean of means **6.6250** against a true
   **4.6000**, and the `(sum, count)` fix.
5. **The three Parquet ratios — 0.2×, 303×, 12×** — and which one to quote.
6. **"You cannot have even write distribution and range scans."** HBase
   row-key design in one sentence.
