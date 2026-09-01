# Course 12 B — Big Data Technologies

**Semester V**

**This is a Track B course**, paired with
Course 13 B (Cloud Computing). Take one track
and you take it for Semester VI too.

---

## The one thing to understand before anything else

**"Big data" is not a size. It is the point at which the data does not fit on
one machine, and everything you know stops working.**

That threshold moves. In 2006 it was a few hundred gigabytes; a laptop now
holds two terabytes and a single cloud VM can be rented with 24 TB of RAM. So
the useful definition is not "more than N bytes" — it is:

> **Data is big when the cost of moving it exceeds the cost of computing on
> it.**

Every design decision in this course follows from that one sentence.

| The old assumption | What replaces it | Where you see it |
|---|---|---|
| Move data to the code | **Move the code to the data** | HDFS data locality, Unit 2 |
| Disks are reliable | **Disks fail constantly; replicate** | Replication factor 3, Unit 2 |
| One machine, scale UP | **Many machines, scale OUT** | YARN, Unit 2 |
| Schema before data | **Schema when you read it** | Hive external tables, Unit 3 |
| Update rows in place | **Write once, append only** | HDFS, Unit 2 |
| A transaction is atomic | **Eventual consistency is enough** | HBase, Unit 5 |

### ⚠️ The honest framing your syllabus does not give you

**This course teaches a stack that peaked around 2015.** MapReduce has been
superseded by Spark; Sqoop and Flume were retired to the Apache Attic in 2021;
Hadoop-on-premises is losing to object storage plus a query engine.

That is **not** a reason to skip it, and here is why:

- **The problems have not changed.** Partitioning, shuffling, skew, data
  locality, the small-files problem, schema evolution and the batch/stream
  split are exactly the same in Spark, BigQuery, Snowflake and Databricks.
  Hadoop is where they are visible, because Hadoop makes you do them by hand.
- **The vocabulary is universal.** "Partition", "shuffle", "predicate
  pushdown", "columnar format" mean the same thing everywhere.
- **Parquet, Avro and Spark are current.** Three of the things this course
  teaches are what the industry actually uses today, and this repository runs
  all three for real.

So learn the *concepts* as permanent and the *tools* as historical, and say so
in the exam — an answer that places Hadoop in time reads as understanding
rather than memorisation.

---

## What actually runs here, and what does not

This is the most environment-constrained course in the programme, and the
notes are explicit about it throughout.

| Runs for real | Documented, **NOT EXECUTED** |
|---|---|
| **Apache Spark** — a genuine `SparkSession`, real RDDs, a real shuffle | Hadoop / HDFS / YARN |
| **Avro** via `fastavro` — real files, real schema evolution | Hive, Pig |
| **Parquet** via `pyarrow` — real columnar files, real statistics | Sqoop, Flume |
| **DuckDB** for Hive-style SQL | HBase, ZooKeeper |
| **SQLite** as the RDBMS for the Sqoop import | the Java MapReduce jars |
| A MapReduce engine written out in full, with a visible shuffle | |

Every file that cannot run says **`*** NOT EXECUTED ***`** in its own header,
names the tool it needs, and points at the runnable half that verifies its
logic. `tools/run_bigdata_labs.py`
asserts that the marker is still there.

**The Debian repositories that host Hadoop are blocked by the egress policy** —
the same wall that stopped R in Course 6, WEKA in Course 8, `mongod` in
Course 10 and SWI-Prolog in Course 13 A.

---

## Course objectives (verbatim)

1. Introduce students to the concepts, characteristics, and challenges of Big
   Data.
2. Familiarize students with the Hadoop ecosystem and its core components
   (HDFS, YARN, MapReduce).
3. Develop practical knowledge of distributed storage and parallel processing
   in Hadoop.
4. Provide hands-on exposure to data ingestion tools (Sqoop, Flume) and
   serialization techniques.
5. Enable students to explore NoSQL databases (HBase), coordination services
   (ZooKeeper), and HadoopSpark integration for large-scale data analysis.

> ### ⚠️ "HadoopSpark" is two words
>
> Objective 5 and Outcome 5 both read **HadoopSpark**, with the space lost.
> They mean **Hadoop and Spark** — two systems, and the distinction is the
> whole point of Unit 5. See review finding **D24**.

## The five units, and how they fit together

| Unit | Question it answers |
|---|---|
| **[1](unit-1.md)** | What is big data, and what is in the Hadoop box? |
| **[2](unit-2.md)** | Where does the data live, and who decides what runs? |
| **[3](unit-3.md)** | How do you compute over it? |
| **[4](unit-4.md)** | How does it get in, and in what format? |
| **[5](unit-5.md)** | What if you need random access, coordination or speed? |

Read them in order. Unit 2 is the load-bearing one: **HDFS's design decisions
explain almost everything else in the course**, and a student who understands
blocks, replication and the NameNode's memory can derive most of Units 3–5.

---

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 17 experiments
- `labs/course-12b-bigdata/` — the code, and the runner that asserts every figure
  these notes quote
- `data/course-12b-bigdata/` — **practice datasets**, CSV: `web-logs.csv`, `wordcount-corpus.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.
  Also `sales-transactions.csv` in `data/shared/`, which several courses
  analyse so their answers can be compared.

## Cross-course connections

This course does not stand alone, and the labs make the links checkable.

| From | To | What is shared |
|---|---|---|
| **Course 11 (BI)** | experiments 10, 14, 17 | The **same nine-row star schema**, imported not copied. South = **₹10,360** is produced by DAX, DuckDB and Spark, and the suite fails if they disagree. |
| **Course 5 (DBMS)** | Units 3 and 5 | Hive is SQL that compiles to a job; HBase is what you get when you drop joins, indexes and transactions. |
| **Course 10 (MongoDB)** | Unit 5 | Two NoSQL stores, compared directly. The sharpest difference: **MongoDB has secondary indexes; HBase does not.** |
| **Course 9 (Python)** | throughout | pandas is the single-machine version of every operation here. |
| **Course 12 A (ML)** | Unit 3 | Spark's `MLlib` is the same algorithms, distributed — and the reason Spark beat MapReduce is *iterative* ML jobs. |

---

## Textbooks

- White, *Hadoop: The Definitive Guide*, 4th edition, O'Reilly — the reference
  for Units 1–3. The syllabus gives "4th" and then stops, without a publisher.
- Damji, Wenig, Das & Lee, *Learning Spark*, 2nd edition, O'Reilly, 2020 —
  Unit 5, and free from Databricks.

**References:** *BIG DATA, Black Book*, DreamTech Press, 2016 · Acharya &
Chellappan, *Big Data and Analytics*, Wiley, 2016.

> ### ⚠️ The reference list starts at 3
>
> The syllabus numbers its two textbooks 1 and 2, then numbers the reference
> books **3 and 4** rather than restarting — so the four titles read as one
> list and the distinction between prescribed and recommended is lost. See
> review finding **D21**.

## How to study this course

1. **Draw the HDFS write path once, from memory.** Client → NameNode →
   pipeline of DataNodes → acknowledgement. If you can draw it, Unit 2 is done.
2. **Do the block arithmetic by hand.** 260 MB at a 128 MB block size is
   128 + 128 + 4, not three full blocks. This is the most examined calculation
   in the course.
3. **Write word count and the inverted index without looking.** Map, shuffle,
   reduce — and be able to say what crosses the network at each step.
4. **Learn one comparison table per unit.** HDFS vs a normal filesystem; FIFO
   vs Fair vs Capacity; Hive vs Pig vs Spark; Avro vs Parquet; HBase vs Hive vs
   MongoDB. Examiners ask for these directly.
5. **Run the labs.** Fourteen of the seventeen execute, including real Spark.
   Numbers you have watched appear are numbers you remember.

### 💡 The single highest-value fact in the course

**The shuffle is the only step that costs real money.** Map and reduce are
local and parallel; the shuffle moves every intermediate record across the
network. Combiners, partitioners, `reduceByKey` instead of `groupByKey`,
bucketed joins, broadcast joins — **every optimisation in big data is an
attempt to shuffle less.**

Say that in an exam and you have framed the whole subject.
