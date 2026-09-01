# Unit 3 — MapReduce and High-Level Tools

**Syllabus topics:** MapReduce programming model: map, shuffle, reduce
phases. Writing MapReduce applications in Hadoop. High-level abstractions:
Hive, Pig, Crunch, and introduction to Spark integration.

---

## 3.1 The MapReduce programming model

### 🎯 The whole model, in four lines

```
map    : (k1, v1)        -> list of (k2, v2)
shuffle: gather every (k2, v2) with the same k2 onto one reducer
reduce : (k2, list of v2) -> list of (k3, v3)
```

**You write `map` and `reduce`. The framework does the shuffle.** That is the
entire deal: you give up general programming and receive parallelism, fault
tolerance and data locality for free.

### 📖 The five phases, in order

| Phase | Where | What happens |
|---|---|---|
| **Input split** | per file | one split per block, by default |
| **Map** | on the block's node | your mapper runs; output goes to **local disk** |
| **Combine** *(optional)* | same node | a map-side mini-reduce, per task |
| **Partition** | same node | `hash(key) % numReduceTasks` picks a reducer |
| **Shuffle & sort** | **across the network** | reducers fetch their partitions and merge-sort |
| **Reduce** | on the reducer's node | your reducer runs; output goes to **HDFS** |

### ⚠️ Map output goes to LOCAL DISK, not HDFS

This is examined and widely got wrong. Map output is **intermediate** — it is
not replicated, not visible in HDFS, and deleted when the job ends. If a map
task's node dies before its output is fetched, **the map task is re-run**,
which is cheap. Replicating intermediate data would triple the cost of every
job for no benefit.

---

## 3.2 The shuffle is the only expensive step

### 💡 The sentence that frames the whole subject

> **Map and reduce are local and parallel. The shuffle moves every
> intermediate record across the network. Every optimisation in big data is an
> attempt to shuffle less.**

Combiners, partitioners, `reduceByKey` instead of `groupByKey`, bucketed
joins, broadcast joins, map-side joins, columnar formats — all of them.

### 🔢 Word count, measured

On six documents, 48 words
(`07_wordcount.py`):

| Phase | Records |
|---|---:|
| map output | **48** |
| shuffled | **48** |
| reduce output | **26** |

The counts sum back to 48. **Nothing is created or lost — reduce is a
regrouping**, and if your totals do not reconcile, your reducer is not
associative.

---

## 3.3 Combiners

### 📖 What a combiner is

**A reducer that runs on the map side, inside one map task, before the
shuffle.** It is an *optimisation*, and Hadoop may run it zero, one or several
times — so it must not change the answer.

### 🔢 The measured saving, and why it is small here

| | Shuffled records |
|---|---:|
| no combiner | **48** |
| with combiner | **39** |
| saving | **9 (18.75%)** |

**Note how small that is, and why.** These documents are 5 to 11 words, so
there is almost nothing to merge *within one split*. On a 128 MB split of real
text the same combiner cuts the shuffle by orders of magnitude.

**The combiner's value scales with split size** — which is a point this tiny
dataset makes precisely by failing to impress. Quoting a combiner saving from
a toy dataset is how people get caught in a viva.

### ⚠️ When a combiner is NOT safe

| Reducer computes | Combiner-safe? | Why |
|---|---|---|
| sum | **yes** | associative and commutative |
| max, min | **yes** | max of maxes is the max |
| count | **yes** | if the combiner emits partial counts |
| **mean** | **NO** | mean of means is not the mean |
| median | **NO** | needs every value at once |

**Demonstrated rather than asserted:** groups `[1,1,1,10]` and `[10]` give a
mean-of-means of **6.6250** against a true mean of **4.6000**.

To average safely, **emit `(sum, count)` pairs and divide only in the
reducer**. That is the same average-of-averages trap Course 11 met in DAX, in
a different costume — and Hadoop will not warn you.

---

## 3.4 Partitioning and skew

Hadoop's default partitioner is `(hash(key) & MAXINT) % numReduceTasks`.

With 3 reducers on the word-count data, the partitions hold **[20, 17, 11]**
records — a largest/smallest ratio of **1.82** on 26 keys.

### ⚠️ Skew, not volume, is what kills a MapReduce job

**Hash partitioning is only as balanced as the key distribution.** Natural
language is Zipfian, so a real corpus skews far worse: one reducer gets `the`
and finishes long after the rest. **The job's wall clock is that reducer.**

Fixes, in order of preference:

1. **Change the key.** Prefix a salt to the hot key and aggregate twice.
2. **A custom partitioner** that splits known hot keys across reducers.
3. **A combiner**, which shrinks the hot key's volume before it moves.
4. **More reducers** — which helps least, because the hot key still lands on
   exactly one of them.

---

## 3.5 Writing MapReduce applications in Hadoop

The canonical Java is in
`WordCount.java` and
`InvertedIndex.java`,
both marked NOT EXECUTED. Three details are examinable.

### 🎯 The map key is a byte offset, not a line number

```java
public void map(LongWritable key, Text value, Context context)
```

`key` is the **byte offset of the line within the split**. Students routinely
assume it is a line number and write code that breaks on the second split.

### 🎯 Reuse the Writable objects

```java
private final static IntWritable ONE = new IntWritable(1);
private final Text word = new Text();
```

Allocating a `new Text()` per word creates one object **per word in the
corpus**, and the garbage collection pause becomes the job. This idiom is the
single most important thing about MapReduce Java.

### ⚠️ The reduce Iterable can be walked ONCE

```java
for (IntWritable val : values) { sum += val.get(); }
```

`values` is **streamed from disk**. Calling `values.iterator()` a second time
yields nothing — the classic bug when someone tries to compute both a sum and
a count in one reducer. Accumulate everything you need in the single pass.

### The inverted index adds one more

**The filename is in neither the key nor the value.** It comes from the input
split:

```java
FileSplit split = (FileSplit) context.getInputSplit();
fileName = split.getPath().getName();
```

And the inverted index **cannot use a combiner**, because the reducer's output
type (a posting string) differs from its input type (a document id) — a
combiner must have the same input and output types as the reducer.

---

## 3.6 Hive

### 📖 The one sentence that explains Hive

> **Hive is a compiler: HiveQL in, a MapReduce/Tez/Spark job out.**

Everything surprising about it follows.

| Expectation | Reality |
|---|---|
| row-level `UPDATE`/`DELETE` | only with ACID tables + ORC + buckets |
| sub-second queries | seconds to minutes — it plans a **job** |
| indexes | **removed in Hive 3**; use partitions and columnar formats |
| a server holding data | metadata only; the data is **files in HDFS** |
| enforced constraints | declarative only, **not enforced** |

### 🔢 Partitioning, measured

The same nine-row star schema as Course 11
(`10_hive_duckdb.py`):

| Partition | Rows | Revenue | Scanned for `WHERE quarter='Q2'` |
|---|---:|---:|---:|
| `quarter=Q1` | 5 | 7,660 | **0** |
| `quarter=Q2` | 4 | 5,220 | **4** |
| total | 9 | 12,880 | **4 of 9** |

**A partition is an HDFS directory.** `WHERE quarter = 'Q2'` reads one
directory instead of the table — **partition pruning**, decided before a byte
is read. The partition column is a *directory name*, not a column in the data
files, so it costs no storage.

### ⚠️ The partitioning trap

**Partition on something with FEW distinct values.** Partitioning by date on a
small table makes four directories for nine rows — the small-files problem
from Unit 2, created on purpose.

Rule of thumb: **partition by quarter or month; bucket by customer id.**

### Bucketing

`CLUSTERED BY (store) INTO 3 BUCKETS` puts rows into **files** inside a
partition by a hash of the column. Two tables bucketed the same way on the
same column can be joined **bucket to bucket with no shuffle** — a sort-merge
bucket join, and the reason bucketing exists.

**Measured, and worth noting honestly:** three stores over three buckets left
**bucket 1 empty**. Hashing does not distribute small key sets evenly, and an
empty bucket is still a file the job opens.

### Managed against external tables

| | Data lives | `DROP TABLE` deletes |
|---|---|---|
| **MANAGED** | `/user/hive/warehouse` | **the data too** |
| **EXTERNAL** | wherever you point it | **only the metadata** |

**Use `EXTERNAL` for anything you did not produce and cannot recreate.** A
`DROP TABLE` on a managed table sitting over the company's only copy of a
dataset is the classic Hive accident.

### 🎯 The cross-course check

Hive-style SQL gives **South = ₹10,360, North = ₹2,520** on the shared star
schema — **the same numbers Course 11's DAX `CALCULATE` measure produced**, and
the same ones Spark produces in experiment 17. Three engines, three languages,
one dataset. If they ever disagree, the suite fails.

---

## 3.7 Pig

### 📖 Pig is a dataflow language

Where Hive gives you SQL, Pig gives you **named intermediate relations**:

```pig
sales    = LOAD 'sales.csv' USING PigStorage(',') AS (...);
priced   = FOREACH sales GENERATE *, qty * list_price AS revenue;
bulk     = FILTER priced BY qty >= 6;
by_cat   = GROUP bulk BY category;
totals   = FOREACH by_cat GENERATE group, SUM(bulk.revenue);
STORE totals INTO 'out';
```

A twelve-step transformation reads top to bottom instead of nesting twelve
sub-queries. **That is the argument for Pig**, and on ETL it is a real one.

### The operator mapping

| Pig Latin | SQL |
|---|---|
| `FILTER` | `WHERE` |
| `FOREACH … GENERATE` | `SELECT` |
| `GROUP` | `GROUP BY` — **but the bag is kept** |
| `JOIN`, `ORDER`, `DISTINCT` | the same |
| `FLATTEN` | `UNNEST` / `LATERAL VIEW explode` |
| **`LOAD` / `STORE`** | **no equivalent** |
| **`ILLUSTRATE`** | **no equivalent** |

### 🎯 The two with no SQL equivalent are the reason to use Pig

- **`LOAD`** lets a script read a semi-structured file with no schema declared
  in advance — SQL assumes a table already exists.
- **`ILLUSTRATE`** pushes a few representative rows through *every step* of the
  plan, so you can see where a twelve-stage pipeline went wrong. Nothing in
  SQL does this.

### ⚠️ `GROUP` in Pig produces a bag, not an aggregate

```
C = GROUP B BY category  ->  (Grocery, {4 tuples})
                             (Personal, {1 tuple})
                             (Stationery, {2 tuples})
```

The bag is the value; `FOREACH … GENERATE` turns it into numbers. **Hive fuses
the two steps; Pig keeps them apart**, which is why Pig can do things to a
group that SQL cannot express without a window function.

### 💡 Lazy evaluation

**Nothing runs until `STORE` or `DUMP`.** Because Pig sees the whole dataflow
before executing, it merges the `FILTER` into the `LOAD` and fuses consecutive
`FOREACH`es into one job.

**So writing the steps separately costs nothing** — which is the entire
argument against nesting sub-queries "to avoid extra passes".

### Join strategies, which is where Pig gets specific

```pig
joined = JOIN priced BY store, stores BY store USING 'replicated';
```

| Hint | What it does | Fails when |
|---|---|---|
| *(default)* | reduce-side join, full shuffle | never — just slow |
| **`'replicated'`** | **map-side**: the small relation is loaded into every mapper's memory. **No shuffle.** | the right relation does not fit in RAM |
| `'skewed'` | samples the key distribution and splits one hot key | — |
| `'merge'` | both inputs already sorted on the key | they are not |

---

## 3.8 Crunch, and the abstraction ladder

**Apache Crunch** is a Java library giving typed `PCollection` pipelines over
MapReduce or Spark — closer to the code than Pig, more structured than raw
MapReduce. It is in the syllabus, it is effectively dead (last release 2017),
and the honest thing to say is that **Spark's RDD API occupies its niche and
won**.

The ladder is worth drawing:

| Level | You write | You control |
|---|---|---|
| **MapReduce** | map and reduce, in Java | everything, painfully |
| **Crunch** | typed pipelines, in Java | most things |
| **Pig** | a dataflow script | join strategies, step order |
| **Hive** | SQL | almost nothing — the optimiser decides |
| **Spark** | RDDs or DataFrames | as much or as little as you want |

**Higher is not better.** Higher is *faster to write and harder to tune*. Hive
is the right default; you drop a level when the optimiser gets it wrong.

---

## 3.9 Spark, introduced

Unit 5 covers Spark integration properly. What belongs here is **why it
replaced MapReduce**.

| | **MapReduce** | **Spark** |
|---|---|---|
| **Between stages** | **writes to HDFS** | **keeps in memory** |
| Iterative jobs | re-reads every pass | `cache()` once |
| API | map and reduce only | ~80 operators |
| Interactive | no | yes — a shell |
| Fault tolerance | re-run the task | recompute from **lineage** |
| Streaming | no | structured streaming |
| Runs on YARN | yes | yes — the same cluster |

### 🎯 The decisive row is the first

**A ten-iteration machine-learning job writes to HDFS nine times under
MapReduce and zero times under Spark.** That is where the "100× faster"
headline comes from — and it is a claim about **iterative** jobs. Quoting it
for a single-pass job is wrong, and saying so is worth marks.

---

## Practice problems

**1. Write the map and reduce functions for computing the average temperature
per city, and explain why the obvious combiner is wrong.**

```
map(record)    -> (city, temperature)
reduce(city, temps) -> (city, sum(temps) / len(temps))
```

**The obvious combiner — the reducer itself — is wrong**, because mean of
means is not the mean unless every group is the same size.

**The fix:**

```
map(record)          -> (city, (temp, 1))
combine(city, pairs) -> (city, (sum of temps, sum of counts))
reduce(city, pairs)  -> (city, total_sum / total_count)
```

**Divide only in the reducer.** The combiner and reducer now have the same
input and output types, which is also the condition Hadoop requires.

**2. A word count over 1 TB of text produces a job where 99 reducers finish in
2 minutes and one runs for 3 hours. Diagnose and fix it.**

**Diagnosis: key skew.** One reducer holds a stop word — almost certainly
`the` — whose posting count is a large fraction of the corpus.

**Fixes, in order:**

1. **Drop stop words in the mapper.** Correct here, since nobody wants a count
   of `the`, and it removes the problem rather than managing it.
2. **Salt the hot keys**: emit `(the#0, 1) … (the#9, 1)` from the mapper,
   aggregate, then sum the ten partials in a second job.
3. **A custom partitioner** routing known hot keys to dedicated reducers.

**What does not work:** raising the reducer count. The hot key still lands on
exactly one reducer.

**3. You have a 2 TB fact table and a 40 MB dimension table to join. What do
you do, and what would go wrong with the default?**

**Use a map-side (broadcast/replicated) join.** The 40 MB dimension is loaded
into every mapper's memory and the join happens with **no shuffle at all**.

- Pig: `USING 'replicated'`
- Hive: `SET hive.auto.convert.join = true` (on by default in modern Hive)
- Spark: `broadcast(smallDf)`

**The default reduce-side join would shuffle all 2 TB** across the network so
that matching keys meet — for a table that fits in RAM on every node.

**The failure mode:** if the "small" table is actually 4 GB, every mapper
tries to hold 4 GB and the job dies with `OutOfMemoryError`. Broadcast joins
have a size threshold for a reason.

**4. Why does Hive have no indexes, and what replaces them?**

Hive removed indexes in version 3 because they were **expensive to maintain
and rarely faster than a full scan** on a columnar format. What replaces them:

- **Partition pruning** — skip whole directories
- **Bucketing** — skip files, and enable shuffle-free joins
- **Columnar formats** (ORC, Parquet) — read only the columns needed
- **Row-group statistics** — skip blocks whose min/max cannot match
- **Vectorised execution** — process a thousand rows per call

**Together these do what an index does, without a structure to keep in sync**
— and the underlying reason is that analytical queries touch a large fraction
of rows, where an index loses to a scan anyway.

**5. Trace word count on `["a b a", "b c"]` through all five phases with two
reducers.**

```
INPUT SPLITS   split1 = "a b a"          split2 = "b c"

MAP            (a,1) (b,1) (a,1)         (b,1) (c,1)

COMBINE        (a,2) (b,1)               (b,1) (c,1)
   per task, so split1's two a's merge and split2's cannot help

PARTITION      hash(a)%2, hash(b)%2, hash(c)%2  -- say a,c -> R0; b -> R1

SHUFFLE        R0 gets (a,2) (c,1)
               R1 gets (b,1) (b,1)

REDUCE         R0: a=2, c=1             R1: b=2
```

**The point to make:** the combiner merged `a` twice within split1 and could
do nothing for `b`, which appears once in each split. That is exactly why
combiner savings depend on split size.

---

## Exam questions from this unit

**Two marks**

1. State the map and reduce signatures.
2. Where does map output go?
3. What is a combiner?
4. Give one aggregate for which a combiner is unsafe.
5. What is the default partitioner?
6. What does `ILLUSTRATE` do?
7. Give one difference between a managed and an external Hive table.
8. Why does Spark beat MapReduce on iterative jobs?

**Five marks**

1. Explain the five phases of a MapReduce job.
2. Explain combiners, with an example where one is unsafe.
3. Explain partitioning and skew, and three ways to fix skew.
4. Compare Hive and Pig, and say when you would choose each.
5. Explain partitioning and bucketing in Hive, with the trap in each.

**Ten marks**

1. Explain the MapReduce programming model in full, with word count traced
   through every phase, and discuss the shuffle's cost.
2. Compare MapReduce, Hive, Pig and Spark as ways of processing the same
   dataset, with the strengths and limitations of each.

---

## Mistakes that cost marks

- **Saying map output goes to HDFS.** Local disk, unreplicated, deleted after.
- **Setting a combiner for a mean.** Silently wrong, and Hadoop will not warn
  you.
- **Assuming the map key is a line number.** It is a byte offset.
- **Iterating the reduce `Iterable` twice.** It streams; the second pass is
  empty.
- **Saying more reducers fixes skew.** The hot key still lands on one.
- **Calling Hive "a database".** It is a compiler over files.
- **Forgetting that `DROP TABLE` on a managed table deletes the data.**
- **Quoting "Spark is 100× faster" without saying "on iterative jobs".**
- **Over-partitioning a Hive table** — you have recreated the small-files
  problem deliberately.
