# Experiment 5 — deploy a dataset on HDFS and perform simple operations

## *** NOT EXECUTED ***

**Hadoop cannot be installed here.** It needs a JVM and the Debian
repositories this environment's egress policy blocks, and HDFS needs a
NameNode and at least one DataNode running. **Nothing in this file has been
run**, and nothing in the notes claims an output for it.

**This is the same block Course 12 B hit**, and its
`labs/course-12b-bigdata/` files record it in the same way. **What did run
there** is the part that matters for this course: **the HDFS block
arithmetic**, computed and asserted, plus a real MapReduce implementation and
real Apache Spark. Read that first — this file adds only the commands.

The relevant runnable material here is
`01_environment_etl.py`, which does the same
extract-transform-load into a warehouse that a Hadoop job would, at a scale
where the distributed machinery earns nothing.

---

## The commands

```bash
# is it up?
hdfs dfsadmin -report

# put the data in
hdfs dfs -mkdir -p /user/student/loans
hdfs dfs -put applicants.csv /user/student/loans/
hdfs dfs -ls -h /user/student/loans

# read it back
hdfs dfs -cat /user/student/loans/applicants.csv | head -5
hdfs dfs -tail /user/student/loans/applicants.csv

# where are the blocks, and on which machines?
hdfs fsck /user/student/loans/applicants.csv -files -blocks -locations

# replication
hdfs dfs -setrep -w 2 /user/student/loans/applicants.csv

# space
hdfs dfs -du -h /user/student/loans
hdfs dfs -df -h

# and out again
hdfs dfs -get /user/student/loans/applicants.csv ./recovered.csv
hdfs dfs -rm -r /user/student/loans
```

---

## The arithmetic that is the actual experiment

**HDFS's default block size is 128 MB and the default replication factor
is 3.**

| File size | Blocks | Blocks stored (×3) | Disk used |
|---|---|---|---|
| 100 MB | **1** | 3 | **300 MB** |
| 200 MB | **2** (128 + 72) | 6 | **600 MB** |
| 1 GB | **8** | 24 | **3 GB** |
| **1 KB** | **1** | 3 | **3 KB**, not 384 MB |

> ### 🎯 The last row is the one that gets examined
>
> **A block is an upper bound, not an allocation.** A 1 KB file occupies 1 KB
> on disk (times replication), not 128 MB. HDFS is not like a filesystem with
> fixed-size clusters.
>
> **But it does consume one block's worth of NameNode memory** — roughly 150
> bytes of metadata per block, held in RAM. **That is the small-files
> problem**: a million 1 KB files cost almost nothing on disk and can exhaust
> the NameNode's heap, while one 1 GB file costs the same disk and 8 blocks of
> metadata.
>
> **The fix is to combine small files** — into sequence files, Avro or
> Parquet, which is exactly what Course 12 B's serialization experiments do.

### Why 128 MB, and not 4 KB

**To make seek time negligible against transfer time.** If a disk seeks in
~10 ms and transfers at ~100 MB/s, a 128 MB block takes ~1.3 s to read and
0.01 s to find — under 1% overhead. A 4 KB block would be almost all seek.

### Why replication 3

One copy on the writer's node (**data locality** — move the computation to the
data), one on another node in the same rack (fast), and one on a **different
rack** (survives a rack switch failing). Two would survive a disk; three
survives a rack.

---

## If you are running this yourself

The single-node "pseudo-distributed" setup is enough for every command above:

```bash
# after installing Hadoop and setting JAVA_HOME
hdfs namenode -format
start-dfs.sh
jps          # expect NameNode, DataNode, SecondaryNameNode
```

The web UI is at `http://localhost:9870` and its **Utilities → Browse the file
system** page shows block placement graphically, which is worth a screenshot
for the record.

## What goes in the lab record

| Item | Value |
|---|---|
| `hdfs dfsadmin -report`: live nodes, capacity, used | |
| File size and block count from `fsck` | |
| **Block locations** — which DataNodes hold which block | |
| Disk used before and after `-setrep -w 2` | |
| Your own version of the block-arithmetic table above | |
| A screenshot of the NameNode UI showing the blocks | |

One paragraph: **your file is smaller than one block. Explain what that costs
on disk and what it costs the NameNode, and why those two answers differ.**
