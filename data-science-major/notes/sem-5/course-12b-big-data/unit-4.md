# Unit 4 — Data Ingestion and Serialization

**Syllabus topics:** Data ingestion pipelines: Sqoop (for RDBMS), Flume
(streaming). Data formats and serialization: Avro, Parquet, SequenceFile.
Practical ingestion workflows — batch and streaming.

---

## The unit where the syllabus has aged, and it matters

**Sqoop and Flume were both retired to the Apache Attic in 2021.** Kafka,
Debezium and NiFi replaced them, and every serious pipeline built after about
2018 uses one of those.

**They are still worth learning**, and this is the honest reason: the
*problems* they solve have not gone anywhere. Splitting a table for parallel
reads, incremental imports and what they miss, back-pressure, channel
durability, the small-files problem at the sink — every one of those appears
identically in Kafka Connect and NiFi. Sqoop and Flume are simple enough that
the problems are visible.

**Avro and Parquet, by contrast, are entirely current** and are what this
repository actually runs.

---

## 4.1 Data ingestion, part one: Sqoop and the batch leg

### 🎯 Sqoop's whole trick, in two lines of SQL

```sql
SELECT MIN(order_id), MAX(order_id) FROM orders;   -- then split that range
SELECT * FROM orders WHERE order_id >= 23 AND order_id <= 45;  -- per mapper
```

**Sqoop is a MapReduce job with no reducer**, where each mapper runs one range
query against the database and writes its results to HDFS.

Everything confusing about Sqoop follows from that: why `--split-by` matters,
why a text primary key breaks it, why four mappers can produce wildly unequal
files, and why `-m 20` against a production OLTP box is a denial of service
you wrote yourself.

### 🔢 A real import, measured

90 rows, 4 mappers
(`11_sqoop_equivalent.py`):

| Mapper | `WHERE` clause | Rows |
|---:|---|---:|
| 0 | `order_id >= 1 AND order_id <= 22` | 22 |
| 1 | `order_id >= 23 AND order_id <= 45` | 23 |
| 2 | `order_id >= 46 AND order_id <= 67` | 22 |
| 3 | `order_id >= 68 AND order_id <= 90` | 23 |

Near-perfect balance, because `order_id` is a dense integer key.

### ⚠️ Now split by a column that is not uniform

Splitting the same 90 rows by `qty` instead:

| Mapper | Range | Rows |
|---:|---|---:|
| 0 | 4..7 | **40** |
| 1 | 8..11 | 20 |
| 2 | 12..15 | 20 |
| 3 | 16..20 | **10** |

**Forty rows for one mapper and ten for another.** Sqoop assumes the split
column is **uniformly distributed between its min and max**, and `qty` is not.
The job's wall clock is the slowest mapper, so a bad `--split-by` wastes three
quarters of your parallelism.

**Split on the primary key unless you have measured otherwise.**

### ⚠️ `--split-by` on a text column

Sqoop needs an **ordered, numeric** column to compute ranges. On text it either
refuses or requires
`-Dorg.apache.sqoop.splitter.allow_text_splitter=true`, which splits on string
ordering and skews horribly.

**A table with a UUID or composite primary key has no natural split column,
and the honest answer is `-m 1`** — one mapper, no parallelism, correct
results.

### Incremental imports

| Mode | `--check-column` | Catches |
|---|---|---|
| `append` | an increasing id | **new rows only** |
| `lastmodified` | a timestamp | **new and updated rows** |

A **saved job** (`sqoop job --create`) remembers `--last-value` for you, which
is what makes incremental imports operable.

### 🎯 Neither mode catches a DELETE

**Sqoop has no way to see a row that is gone.** An incrementally imported
table therefore **drifts away from its source over time**, and the only fix is
a periodic full re-import.

Knowing that is the difference between having used Sqoop and having read about
it — and it is exactly the problem **change data capture** (Debezium, reading
the database's own write-ahead log) was invented to solve.

### ⚠️ The other three that bite

| Problem | What happens | Fix |
|---|---|---|
| `--password` on the command line | lands in `ps` and shell history | `--password-file` on HDFS, mode 400 |
| no null handling | SQL `NULL` becomes the string `"null"` | `--null-string '\N' --null-non-string '\N'` |
| `$CONDITIONS` omitted from `--query` | the import fails | it is **mandatory** — Sqoop substitutes each mapper's range there |

### Verifying an import

**Check the row count *and* the sum of a money column.** Counting rows alone
would not catch a truncated numeric type — an Oracle `NUMBER(38)` silently
becoming a Java `double` is the classic Sqoop data-corruption bug.

In the lab, 90 rows carrying **₹128,800** go in and 90 rows carrying
**₹128,800** come out, which is exactly ten times Course 11's ₹12,880.

---

## 4.2 Flume — the streaming leg

### 📖 The agent, in three parts

```
   SOURCE  ──►  CHANNEL  ──►  SINK
  (tail a       (a bounded    (write to
   log file)     buffer)       HDFS)
```

Plus **interceptors**, which add **headers** to events and never touch the
body, and a **channel selector**, which routes on those headers.

### 🔢 What the channel capacity actually does

Running the agent over 40 log events
(`12_flume_equivalent.py`):

| Configuration | Delivered | Rejected | Peak depth |
|---|---:|---:|---:|
| capacity 100, batch 10, fast sink | **40** | **0** | ≤10 |
| capacity 8, batch 4, **slow sink** | 40 | **8** | **8** |
| capacity 20, batch 4, slow sink | 40 | **0** | 16 |
| capacity 100, batch 4, slow sink | 40 | **0** | 16 |

### 🎯 Back-pressure, which looks like a bug and is not

**Eight events were refused by the channel because the sink could not drain
it.** In a real agent the source then **blocks** rather than dropping, and the
back-pressure travels back up the pipe to the web server.

**"Flume lost my events" almost always means "the channel was full and the
source gave up".**

And note the last two rows: **a bigger channel absorbs a longer burst and buys
nothing once the sink is permanently slower than the source.** Buffers smooth
*bursts*; they cannot fix a throughput deficit. That sentence answers most
Flume tuning questions.

### Channel types — the choice that is actually being made

| Channel | Survives a crash? | Throughput |
|---|---|---|
| **memory** | **NO — events lost** | highest |
| **file** | yes — a write-ahead log on disk | roughly 10× slower |
| **Kafka** | yes — replicated | high, but another cluster to run |

**A memory channel plus "we must not lose events" is a contradiction**, and it
is the most common Flume misconfiguration. Choose the channel from the
durability requirement, then size the cluster for whatever throughput that
leaves.

### ⚠️ The source everyone gets wrong

Use **`TAILDIR`**, not `exec tail -F`. An `exec` source has **no position
file**, so on a restart it loses everything it had not yet delivered. This is
the single most common Flume data-loss bug.

### ⚠️ The defaults manufacture the small-files problem

| Setting | Default | What it does |
|---|---|---|
| `hdfs.rollInterval` | **30 s** | close the file on a timer |
| `hdfs.rollSize` | **1024 bytes** | close it at a size |
| `hdfs.rollCount` | **10 events** | close it after N events |

**At the defaults, 40 events produce about 4 HDFS files**, each a few hundred
bytes. Left alone, Flume produces a file every few seconds, and the NameNode
pays 150 bytes for every one — the Unit 2 small-files problem, generated
continuously at a rate of two per minute.

**Always override:** `rollCount = 0`, `rollSize` = one HDFS block,
`rollInterval` = 10 minutes.

---

## 4.3 Serialization formats

### 📖 The one distinction that matters

**Row format** stores record 1 in full, then record 2 in full. **Column
format** stores every value of column 1, then every value of column 2.

Everything else follows:

| | **Row (Avro, SequenceFile)** | **Column (Parquet, ORC)** |
|---|---|---|
| Write one record | **cheap** | expensive — must buffer |
| Read one record whole | **cheap** | expensive — touch every column |
| Read one column of many | expensive | **cheap** |
| Compression | per record | **per column, by type** |
| Skip on a predicate | no | **yes — row-group statistics** |
| Good for | ingestion, streaming | **analytics** |

### Avro — measured, and really written

`13_avro_parquet.py`
uses `fastavro`, so the files are byte-for-byte readable by Hadoop, Hive and
Spark. **Nothing here is simulated.**

**The property that matters: the writer's schema is stored in the file
header.** An Avro file is **self-describing** — a reader five years later needs
no external metadata, which is exactly what a CSV cannot promise.

*(A detail worth knowing: the schema's stored name is the **full** name,
namespace included — `in.ac.datascience.sales.Sale`, not `Sale`.)*

### 🎯 Schema evolution, demonstrated

Nine records were written with an eight-field schema, then **read back with a
nine-field schema** that adds `channel` with a default of `null`:

```
read 9 OLD records with a NEW schema
the added field 'channel' comes back as None -- its DEFAULT
```

**The old file was not rewritten.** Avro resolves the writer's schema against
the reader's, field by field, and fills in defaults for anything missing.

**A field added WITHOUT a default breaks exactly this**, and that is the one
rule to remember about evolving an Avro schema.

### Parquet — column projection, measured

Bytes stored **per column** inside the nine-row Parquet file:

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

**`SELECT revenue` reads 143 of 949 column bytes — 15.1%.** That is column
projection, and it is why Parquet wins on analytical queries. A row format has
to read every row in full and discard seven fields.

### 🎯 Predicate pushdown

Parquet stores min/max **statistics per row group**. For `revenue` here:
**min 600, max 2,800**.

A query for `revenue > 5000` can **skip the entire row group without decoding
a byte**. On a partitioned Parquet dataset this is often a bigger win than the
compression.

### ⚠️ The compression claim, told honestly

| Size | CSV | Avro | Parquet | CSV/Parquet |
|---|---:|---:|---:|---:|
| **9 rows** | 533 | 938 | **2,584** | **0.2×** — Parquet is *larger* |
| 108,000 rows, **repetitive** | 5,700,058 | 5,924,190 | 18,790 | **303.4×** |
| 108,000 rows, **varied** | 6,269,519 | 6,380,506 | 522,264 | **12.0×** |

**Read all three rows.**

- On **nine rows Parquet is 4.8× LARGER than CSV** — the footer, the schema
  and per-column metadata are fixed overhead that nine rows cannot amortise.
- The **303×** figure is an **artefact**: 12,000 identical copies of nine rows
  dictionary-encode to almost nothing.
- Give every row a distinct store and revenue and it falls to **12.0×** — and
  even that is optimistic, because date, region and category are still
  repetitive. **In production, Parquet against CSV usually lands between 3×
  and 10×.**

**A columnar format's headline compression number is mostly a statement about
how repetitive your data is.** Quoting a ratio from a benchmark on duplicated
rows says nothing at all, and this is precisely how people get caught in a
viva.

### SequenceFile

A flat binary file of key/value `Writable` pairs, with three compression
modes: none, **record** (compress each value) and **block** (compress groups —
better ratio, splittable).

It exists to solve the small-files problem — pack many small files into one
SequenceFile keyed by filename — and it is **legacy**. Use Avro for new work.

### 🎯 The comparison, and the architecture that uses both

| Need | Format |
|---|---|
| row-by-row writes, whole-record reads | **Avro** |
| column aggregates over billions of rows | **Parquet** |
| a landing zone that survives schema changes for years | **Avro** |
| the table Hive and Spark actually query | **Parquet** |

**The standard architecture uses both:** Avro at the edge, where records
arrive one at a time and schemas drift; then a batch job converts to Parquet
for the query layer. That is the answer worth full marks on "compare Avro and
Parquet".

---

## 4.4 Batch and streaming together

### 🔢 The fan trap, in a data pipeline

Joining the batch table (9 orders) to the stream table (40 events) on `host`
(`14_pipeline.py`):

```
events counted through the join: 90
events actually ingested       : 40
```

**The join inflated the event count.** Each host appears in several orders, so
every event is counted **once per matching order**.

**This is the same fan trap Course 11 found in a Power BI model.** It is not a
Spark problem, a Hive problem or a SQL problem — **it is a grain problem**, and
it appears wherever two fact tables are joined directly.

### 🎯 The fix, and the rule

**Aggregate each side to a common grain first, then join.**

| host | orders | revenue | events | errors |
|---|---:|---:|---:|---:|
| 10.0.0.1 | 3 | 4,200 | 10 | 2 |
| 10.0.0.2 | 2 | 3,220 | 10 | 2 |
| 10.0.0.3 | 2 | 2,800 | 10 | 2 |
| 10.0.0.4 | 2 | 2,660 | 10 | 2 |
| **total** | **9** | **12,880** | **40** | **8** |

**40 events and ₹12,880 — both reconcile with the sources.** That single rule
prevents most wrong numbers in a data warehouse, and it is worth stating in
exactly those words.

### The two legs are not interchangeable

| | **Batch (Sqoop)** | **Streaming (Flume)** |
|---|---|---|
| Arrives | on a schedule | continuously |
| Completeness | a whole table, consistent | whatever has landed |
| **Late data** | **impossible** | **normal — and must be handled** |
| Re-runnable | yes, idempotent | no — events are consumed |
| Catches `DELETE`s | on a full re-import | never |
| File sizes | large, controllable | small unless you roll |
| Failure means | re-run the import | **a gap in the data** |

### 🎯 "Late data is normal" is the row that changes the design

A streaming aggregate for 09:00 is **not final at 10:00**. Either you accept
eventual correctness, or you keep a **watermark** and re-emit corrected
results. The batch leg has no such problem — which is exactly why the **Lambda
architecture** keeps both.

| | Layers | Cost |
|---|---|---|
| **Lambda** | batch + speed + serving | **the same business logic is written twice** |
| **Kappa** | one streaming path, replayable | needs a durable log like Kafka |

**Lambda's real cost is not machines — it is that the same rule exists in two
codebases and they drift.** Kappa removes the batch layer by making the stream
replayable, which is why **Kafka replaced Flume** in most of these pipelines
after about 2016. Saying that places the whole syllabus in time.

---

## Practice problems

**1. A 500 GB MySQL table with an auto-increment primary key must land in
HDFS nightly as Parquet. Write the plan, and name three things that could go
wrong.**

```bash
sqoop import --connect jdbc:mysql://db:3306/app \
  --table events --split-by event_id --num-mappers 8 \
  --target-dir /raw/events --as-parquetfile \
  --compress --compression-codec snappy \
  --null-string '\N' --null-non-string '\N' \
  --password-file /user/etl/.pw
```

**What goes wrong:**

1. **Eight concurrent range scans against a production OLTP database** during
   the night's batch window. Import from a read replica, or throttle to fewer
   mappers.
2. **Deleted rows are never removed.** Nightly full imports handle it; an
   incremental import would drift.
3. **Auto-increment ids with gaps** (rolled-back transactions) produce uneven
   mapper loads — Sqoop assumes a dense range.

**2. Explain why Avro is preferred for ingestion and Parquet for analytics,
with figures.**

**Avro is a row format with the schema in the file.** A record arriving one at
a time can be appended immediately, and a reader who does not know the
schema can still read it. Schema evolution is resolved at read time, so adding
a field does not require rewriting years of history — demonstrated by reading
nine old records with a new nine-field schema and getting the default back.

**Parquet is columnar.** `SELECT revenue` read **143 of 949 column bytes** in
the lab, and row-group statistics (`revenue` min 600, max 2,800) let a query
for `revenue > 5000` skip the group entirely.

**Writing one record to Parquet is expensive** because the writer must buffer a
row group before it can encode columns — which is exactly why it is the wrong
format for the landing zone.

**3. Your Flume agent shows `ChannelFullException` in its logs. Diagnose it.**

**The sink cannot drain the channel as fast as the source fills it.** Work
through, in order:

1. **Is the sink actually slow, or stalled?** An HDFS sink blocked on a
   NameNode in safe mode looks identical to a slow one.
2. **Increase `batchSize`** on the sink — the commonest real fix, since a sink
   writing 10 events per transaction is dominated by round trips.
3. **Increase channel capacity** *only if the burst is temporary*. If the sink
   is permanently slower, a bigger buffer just delays the same error.
4. **Add sinks** in a sink group, or shard the agent.

**What it is not:** it is not a bug and not data loss in itself. It is
back-pressure working correctly, and the events are still in the channel.

**4. A team reports that their nightly report and their real-time dashboard
disagree by about 2%. Explain the likely cause.**

**Late data.** The streaming path aggregated whatever had landed by midnight;
the batch path re-read the source table and got everything, including events
that arrived late or were retried.

**This is not a bug — it is the defining property of the two legs**, and it is
why the Lambda architecture treats the batch layer as the source of truth and
the speed layer as an approximation that gets overwritten.

**The fixes:** a watermark with re-emission, or move to a Kappa architecture
where the stream is replayable and there is only one answer.

**5. You must join a 2 TB event stream to a 40 MB customer dimension. Which
format for each, and which join?**

- **Events: Parquet**, partitioned by date. Analytical queries touch a few
  columns of very many rows.
- **Dimension: Parquet too**, but the format barely matters at 40 MB.
- **The join: broadcast.** 40 MB fits in every executor's memory, so there is
  **no shuffle** of the 2 TB side.

**And note the grain:** if the dimension has one row per customer per *version*
(a slowly changing dimension), joining it directly fans out the events. Filter
to the current version, or join on `(customer_id, valid_from ≤ event_time <
valid_to)`.

---

## Exam questions from this unit

**Two marks**

1. What SQL does Sqoop run before launching mappers?
2. What is `--split-by` for?
3. Name the two incremental import modes.
4. What does neither incremental mode catch?
5. Name the three parts of a Flume agent.
6. What does a Flume interceptor modify?
7. Which of Avro and Parquet is columnar?
8. Where does Avro store its schema?

**Five marks**

1. Explain how Sqoop parallelises an import, and what goes wrong with a
   skewed split column.
2. Explain Flume's channel, back-pressure and the memory/file trade.
3. Explain Avro schema evolution with an example.
4. Explain column projection and predicate pushdown in Parquet.
5. Compare batch and streaming ingestion on five dimensions.

**Ten marks**

1. Design an end-to-end ingestion pipeline for a retail chain with nightly
   RDBMS extracts and continuous point-of-sale events. Justify every tool and
   format, and say what could go wrong.
2. Compare Avro, Parquet and SequenceFile in detail, with the situations in
   which each is correct, and explain why compression ratios quoted from
   benchmarks are usually misleading.

---

## Mistakes that cost marks

- **Saying Sqoop is a streaming tool.** It is a batch MapReduce job with no
  reducer.
- **Forgetting `$CONDITIONS`** in a `--query` import. It is mandatory.
- **Claiming incremental imports keep the table in sync.** They never see a
  `DELETE`.
- **Using `exec tail -F`** as a Flume source — no position file, data loss on
  restart.
- **Pairing a memory channel with a durability requirement.**
- **Leaving Flume's HDFS rollover at the defaults** — you have built a
  small-files generator.
- **Saying Avro is columnar.** It is a row format; Parquet and ORC are
  columnar.
- **Quoting a Parquet compression ratio without saying what the data looked
  like.** 303× on repeated rows, 12× on varied, and 0.2× on nine rows.
- **Joining two fact tables directly** and reporting the fanned-out count.
