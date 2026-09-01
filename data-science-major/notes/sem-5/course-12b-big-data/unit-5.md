# Unit 5 — NoSQL and Ecosystem Enhancements

**Syllabus topics:** Overview of NoSQL within the Hadoop ecosystem:
HBase. Configuration and usage of ZooKeeper for coordination. Hadoop
integration with Spark for data processing.

---

## 5.1 Why HBase exists

### 🎯 The gap it fills

HDFS is **write-once, append-only, and optimised for scanning**. It cannot
update a row, and it cannot fetch one record by key without reading a file.

Some workloads need exactly that: a user profile fetched in 5 ms, a counter
incremented a million times a second, a message store where individual rows
change.

**HBase is the random-access layer over HDFS**, modelled on Google's Bigtable.

| | **HDFS** | **HBase** |
|---|---|---|
| Access | sequential scan | **random read/write by key** |
| Latency | seconds | **milliseconds** |
| Update a row | rewrite the file | **yes** |
| Good for | analytics | **serving** |

---

## 5.2 The HBase data model

### 📖 The one sentence to memorise

> **HBase is a sparse, distributed, persistent, multidimensional sorted map,
> indexed by (row key, column family, column qualifier, timestamp).**

Every word earns its place:

- **sparse** — a row with no value for a column stores *nothing*, not a null
- **sorted** — by row key, always, which is what makes range scans fast
- **multidimensional** — the fourth dimension is **time**: a cell holds
  several versions
- **map** — you get, put and scan. There is no query language.

### 🔢 The model, implemented and run

`15_hbase_model.py`
builds the map, with real versioning, real tombstones and real range scans.

**Versions:** after two more `put`s to the same cell, `VERSIONS => 3` keeps
three:

```
ts=38   111
ts=37    99
ts=19    20
```

**A `put` to an existing cell does not overwrite — it adds a version**, and the
old value is still readable.

### ⚠️ A delete makes the table BIGGER

```
DELETE info:category
  readable? no
  cells:    38 -> 39
```

**A delete writes a tombstone marker.** The data and the marker both disappear
only at a **major compaction**. This is the answer to "I deleted a billion rows
and disk usage went up".

### ⚠️ Column families are fixed; columns are free

`CREATE` declares the **families**. Qualifiers inside a family need no
declaration and cost nothing — which is what "schema-less" means in HBase, and
it is only half true.

**Keep families to two or three.** Each family is a separate store file, and a
memstore flush of one flushes all of them.

---

## 5.3 Row key design — the whole job

### 🔢 The uniqueness trap, demonstrated

Keying the nine shared fact rows by `region#store#date`:

```
9 fact rows -> only 8 DISTINCT KEYS -- 1 row would be overwritten
```

Vijayawada sold Rice **and** Shampoo on D1, so those two facts collide.
**HBase would not complain** — it would version one over the other and lose a
sale.

**A row key must be unique at the grain.** In an RDBMS the primary key
declaration catches this; **in HBase nothing does**, and that is the failure
mode to remember. Adding the product to the key restores all nine rows.

### 🎯 The hotspot, and the trade you cannot escape

| Row key | Writes go to | Verdict |
|---|---|---|
| a **timestamp** | the last region, always | **HOTSPOT** |
| a **sequential id** | the last region, always | **HOTSPOT** |
| `md5(id) + id` | everywhere, evenly | good — **range scans lost** |
| `region#store#date#product` | by region | good — **prefix scans work** |

**A monotonically increasing row key sends every write to the same
RegionServer**, so a 50-node cluster runs at the speed of one node.

Salting or hashing fixes the hotspot **and destroys range scans**.

> **You cannot have even write distribution and range scans on the same
> dimension. Choosing between them *is* row-key design.**

### 🔢 What a prefix scan buys

```
SCAN 'South' .. 'South~'  -> 6 rows
SCAN 'North' .. 'North~'  -> 3 rows
```

A range scan on the row-key prefix reads **exactly the rows you want,
sequentially, from one or two regions** — the fastest thing HBase does. It
works **only because `region` is the first component of the key**.

### ⚠️ HBase has no secondary index

Asking the same question the wrong way:

```
find category = 'Grocery' -> 4 rows, after scanning all 9
```

**Filtering on a value means a full table scan** with a server-side filter —
correct, and O(table). If you need that query, **you build a second table
keyed by category and keep it in sync yourself**.

### 💡 Pre-splitting

Without pre-splits a table starts as **one region on one RegionServer**, so a
bulk load runs single-threaded until the first split. `SPLITS => ['East',
'North', 'South', 'West']` at create time avoids it — and you cannot easily
retrofit it later.

---

## 5.4 HBase against what it is confused with

| | **HBase** | **Hive** | **MongoDB** (Course 10) |
|---|---|---|---|
| Model | sparse sorted map | tables over files | documents |
| Latency | **milliseconds** | seconds to minutes | milliseconds |
| Random writes | **yes** | no | yes |
| **Secondary index** | **no** | no | **YES** |
| Query language | get/put/scan only | HiveQL | MQL |
| Schema | families fixed, columns free | fixed | free |
| Transactions | single-row atomic | none (mostly) | multi-document |

### 🎯 Two comparisons worth making explicitly

**HBase and Hive both sit on HDFS and answer completely different questions.**
Hive scans everything slowly; HBase fetches one row instantly. A cluster
usually runs both, over the same data, for different consumers.

**HBase against MongoDB is the sharper comparison**, because both are NoSQL
stores this programme teaches. The row students get wrong is **secondary
index**: MongoDB has them and HBase does not, which is why a MongoDB query on
any field is reasonable and an HBase query on a non-key field is a full scan.

### 📖 CAP, and where HBase sits

| System | Chooses | Meaning |
|---|---|---|
| **HBase** | **CP** | on a partition it refuses reads rather than serve stale data |
| Cassandra | **AP** | on a partition it serves possibly-stale data |
| an RDBMS | CA | it assumes no partitions, which is why it is one machine |

**Each row key is served by exactly one RegionServer**, which is what makes
HBase strongly consistent and what makes a region unavailable during a
failover. Cassandra's multiple replicas serve reads always, and the price is
eventual consistency.

---

## 5.5 ZooKeeper

### 🎯 What ZooKeeper actually is

**A small, strongly-consistent tree of nodes** — and it is interesting for
exactly two properties:

1. **Ephemeral nodes vanish when the session that made them dies.**
2. **Sequential nodes are numbered by a single authority.**

**Every recipe is built from those two facts.** ZooKeeper is not a database,
not a queue and not a cache.

### 🔢 Leader election, the standard recipe

Each candidate creates an **ephemeral sequential** znode; the **lowest**
sequence number is the leader
(`16_zookeeper_model.py`):

```
nn1 -> lock-0000000000        LEADER: nn1
nn2 -> lock-0000000001
nn3 -> lock-0000000002

nn1's session expires (its JVM was killed):
  lock-0000000000 vanished; new LEADER: nn2
```

**Nobody ran a failover script.** The ephemeral node was deleted **by the
server** when the heartbeat stopped, the watch fired, and nn2 saw itself at the
head of the queue.

**That is how HDFS NameNode HA chooses its active node** — the link straight
back to Unit 2.

### ⚠️ Watch the node BELOW you, not the leader

If every candidate watches the leader, **every candidate is woken by one
failure** — the **herd effect**. Watching your immediate predecessor wakes
exactly **one** client per failure.

**The recipe is not arbitrary; it is a thundering-herd fix**, and saying so is
worth the mark.

### A distributed lock is the same recipe

```
jobA and jobB both asked; jobA holds the lock
jobA CRASHES -- lock passes to jobB automatically
```

**The lock is released by the session dying, not by the client remembering to
release it.** A lock in a normal database survives the crash of whoever held
it and deadlocks the system; an ephemeral znode cannot.

### Atomic create

```
create /config "v1"   -> ok
create /config "v2"   -> FileExistsError
```

**Exactly one client wins a create, cluster-wide, with no further
negotiation.** "Whoever creates `/master` is the master" is a complete
election algorithm in one line — and it works only because ZooKeeper
**linearises** writes.

### 🔢 Ensemble sizing — why the number is always odd

| Servers | Quorum | Can lose | Verdict |
|---:|---:|---:|---|
| 1 | 1 | **0** | no fault tolerance |
| 2 | 2 | **0** | no fault tolerance |
| **3** | 2 | **1** | good |
| 4 | 3 | **1** | **same tolerance as 3** |
| **5** | 3 | **2** | good |
| 6 | 4 | 2 | same tolerance as 5 |
| **7** | 4 | **3** | good |

**Four servers tolerate one failure — exactly what three tolerate.** The
fourth machine buys nothing and adds a write to every quorum. That is the
whole reason ensembles are **3, 5 or 7**, and it is a two-line exam answer.

### ⚠️ What ZooKeeper is not

| Misuse | Why it fails |
|---|---|
| a message queue | no ordering guarantees across znodes |
| a data store | **1 MB per znode**, whole tree in RAM |
| a cache | every write is a quorum round trip |
| a registry for 10,000 nodes | watch storms |

**ZooKeeper stores coordination state** — who is the leader, who holds the
lock, what is the config — and it is small, consistent and slow on purpose.

### Who depends on it in this course

| Who | For what |
|---|---|
| **HDFS NameNode HA** | elects the active NameNode (Unit 2) |
| **YARN ResourceManager HA** | elects the active RM (Unit 2) |
| **HBase** | tracks the master and the RegionServers (this unit) |
| Kafka (before 3.x) | broker membership and the controller |

**Every HA story in the Hadoop ecosystem ends at ZooKeeper**, which is why an
experiment that looks like a detour is actually the keystone.

---

## 5.6 Hadoop integration with Spark

### 📖 The core abstraction

An **RDD** is an immutable, partitioned collection with a **lineage** — a
record of how it was computed from its parents. That lineage is what makes
Spark fault tolerant: a lost partition is **recomputed**, not fetched from a
replica.

### 🎯 Transformations and actions

**Transformations are lazy; actions run the job.**

| Transformations | Actions |
|---|---|
| `map`, `filter`, `flatMap` | `collect`, `count`, `take` |
| `reduceByKey`, `groupByKey`, `join` | `saveAsTextFile`, `foreach` |
| `distinct`, `sortBy`, `union` | `reduce`, `first` |

**This is why a typo in a `map()` surfaces at `collect()`** and not where you
wrote it — and why Spark can fuse the whole chain into one pass over the data.

### 🔢 `reduceByKey` against `groupByKey` — the most examined Spark question

Measured on a real `SparkSession`
(`17_spark.py`, 48 words in
3 partitions):

| | What crosses the network |
|---|---|
| `groupByKey` | **all 48 pairs**, then counts |
| `reduceByKey` | combines to **35** map-side (11 + 14 + 10 per partition), then shuffles |

**Same output, different job.** `groupByKey` moves every record;
`reduceByKey` moves one per key per partition. On a real corpus `groupByKey`
is how you produce an `OutOfMemoryError` on a single hot key.

*(Note the 35, not the 39 from experiment 7's MapReduce run — Spark's three
partitions each hold two documents, so more merging happens per task. The
combiner's saving depends on the split, exactly as Unit 3 said.)*

### 🎯 The cross-course check, for the third time

Spark's DataFrame aggregate over the shared star schema:

| Region | Revenue | Profit |
|---|---:|---:|
| South | **10,360** | 2,760 |
| North | **2,520** | 765 |

**Course 11's DAX, experiment 10's DuckDB and Spark all produce ₹10,360.**
Three engines, one dataset — and if they ever disagree, `verify_all.sh` fails.

### 💡 `cache()`, and why nothing fails without it

```
cache(): two actions over the same RDD, sum = 39,999,800,000
storage level after cache(): Memory Serialized 1x Replicated
```

**Without `cache()` the second action recomputes the whole lineage from the
source.** With it, only the first pays.

Caching is the single highest-value Spark optimisation and the one students
forget — **because nothing fails without it. The job is merely twice as slow**,
which is far harder to notice than an error.

### Spark on the Hadoop stack

| | MapReduce | Spark |
|---|---|---|
| **Between stages** | **writes to HDFS** | **keeps in memory** |
| Iterative jobs | re-reads every pass | `cache()` once |
| API | map and reduce only | ~80 operators |
| Interactive | no | yes — a shell |
| Fault tolerance | re-run the task | recompute from **lineage** |
| Streaming | no | structured streaming |
| Runs on YARN | yes | **yes — the same cluster** |

**The last row matters:** Spark did not replace Hadoop. It replaced
**MapReduce**, and it runs on YARN over HDFS. "Hadoop is dead, use Spark" is a
category error, and saying so is worth marks.

### HBase and Spark together

`17_spark_hbase.scala`
(NOT EXECUTED — the connector needs a live HBase) shows the integration, and
two points from it are examinable:

**One Spark partition per HBase region.** That is the whole integration: Spark
reads regions in parallel, locally, pushing the scan range down so it reads one
region rather than the table.

**Never `put()` per row from a Spark job** — that is one RPC per record and it
will overwhelm the RegionServers. Write **HFiles** and bulk-load them, which
bypasses the write path entirely (no WAL, no memstore, no flush) and is one to
two orders of magnitude faster.

### ⚠️ When not to put Spark over HBase

**A full-table Spark scan of HBase is slower than the same data in Parquet**,
because HBase stores every cell with its row key, family, qualifier and
timestamp. HBase is for random access; Parquet is for scans.

**If every job you run is a full scan, the data is in the wrong store.**

---

## Practice problems

**1. Design a row key for a table of sensor readings queried as "all readings
from sensor X between two times".**

**`sensorId#reverseTimestamp`** or `sensorId#timestamp`.

- `sensorId` first, so all of one sensor's readings are **contiguous** and the
  query is a single range scan.
- `timestamp` second, so the time range is a prefix scan within that sensor.
- **Not `timestamp#sensorId`** — that hotspots every write onto the last
  region *and* makes the query a full scan.

**Reverse timestamp** (`Long.MAX_VALUE - ts`) puts the newest reading first,
which is right if the common query is "the latest N readings".

**The remaining risk:** if one sensor produces far more data than the others,
that sensor's region becomes a hotspot. Salting with `hash(sensorId) % 16` in
front fixes it and costs you cross-sensor scans — the same trade as always.

**2. Your ZooKeeper ensemble has 5 servers. Two fail. What happens? Three fail?**

**Two fail:** quorum is 3, three remain, so **the ensemble keeps working**.
Writes still commit; nothing external notices.

**Three fail:** two remain and quorum is 3, so **the ensemble stops accepting
writes entirely.** Reads may still be served stale by the survivors, but no
write can commit.

**The consequence is what matters:** HDFS HA cannot fail over, YARN HA cannot
fail over, and HBase cannot assign regions. **A ZooKeeper outage does not
corrupt anything — it freezes every coordination decision in the cluster**,
which is why the ensemble is the most carefully operated part of the stack.

**3. Explain why HBase is CP rather than AP, and what that costs.**

**Each row key is served by exactly one RegionServer.** There is no second
replica of a *region* that can answer, so during a failover the rows in that
region are **unavailable** — HBase refuses rather than serving stale data.

**What it buys:** strong consistency. A read always sees the most recent
committed write, so read-modify-write and atomic counters are correct.

**What it costs:** availability during failover, typically tens of seconds
while ZooKeeper detects the failure and the master reassigns the region. HDFS
still holds three copies of the *data*, so nothing is lost — only unreachable.

**Cassandra chose the other side**, serving from any replica always, and pays
in eventual consistency.

**4. A Spark job runs in 4 minutes the first time and 4 minutes the second
time on the same data. What is probably wrong?**

**The RDD or DataFrame is not cached.** Spark recomputed the entire lineage
from source on the second action.

**Diagnose:** look at the Spark UI's stage list. If the same stages re-run with
the same input, add `.cache()` (or `.persist()`) before the first action and
call an action once to materialise it.

**The trap in the diagnosis:** `cache()` is also lazy. Calling it and then
running the second action immediately still recomputes the first time — it is
the *first action after* `cache()` that populates the cache.

**And the counter-case:** if the data does not fit in memory, `MEMORY_ONLY`
silently recomputes the partitions that were evicted, and you see exactly this
symptom with `cache()` already in place. Then you want `MEMORY_AND_DISK`.

**5. Compare HBase and MongoDB for storing 500 million user profiles queried
by user id, and occasionally by email.**

**By user id:** both are excellent. HBase with `userId` as the row key,
MongoDB with `_id`.

**By email is the deciding question.**

- **MongoDB** — create a secondary index on `email`. The query is fast, and
  this is a routine thing to do.
- **HBase** — there is no secondary index. You either scan 500 million rows
  with a filter, or build and maintain **a second table keyed by email**,
  keeping the two in sync in application code with no transaction spanning
  them.

**So MongoDB wins here**, and the honest reason is the access pattern, not
general superiority. If the workload were "500 billion rows, one access
pattern, extreme write throughput", HBase would win on scale.

---

## Exam questions from this unit

**Two marks**

1. Give the one-sentence definition of the HBase data model.
2. What does a `put` to an existing cell do?
3. Why does a delete make an HBase table bigger?
4. Does HBase have secondary indexes?
5. What are the two special znode types?
6. Why are ZooKeeper ensembles always odd-sized?
7. What is an RDD's lineage for?
8. Give one difference between `reduceByKey` and `groupByKey`.

**Five marks**

1. Explain HBase row-key design and the hotspot/scan trade-off.
2. Explain leader election in ZooKeeper, including why you watch your
   predecessor.
3. Compare HBase, Hive and MongoDB.
4. Explain lazy evaluation and lineage in Spark.
5. Explain why Spark replaced MapReduce, with the correct qualification of the
   "100× faster" claim.

**Ten marks**

1. Describe the HBase architecture and data model in full, and design a row
   key for a given access pattern, justifying it.
2. Explain the role of ZooKeeper in the Hadoop ecosystem, with leader election
   and distributed locking, and say what breaks when the ensemble loses quorum.

---

## Mistakes that cost marks

- **Saying HBase is a relational database with a different name.** No joins, no
  secondary indexes, no query language, no multi-row transactions.
- **Saying a delete frees space.** It writes a tombstone; space returns at
  major compaction.
- **Designing a row key on a timestamp** — a guaranteed hotspot.
- **Claiming you can have both even write distribution and range scans.** You
  choose.
- **Calling ZooKeeper a database or a queue.**
- **Recommending a 4-server ensemble.** Same tolerance as 3, slower writes.
- **Saying Spark replaced Hadoop.** It replaced MapReduce, and it runs on YARN
  over HDFS.
- **Using `groupByKey` when `reduceByKey` will do.**
- **Forgetting `cache()`** — and not noticing, because nothing fails.
