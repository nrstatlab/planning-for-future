# Practical Lab

**17 experiments**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.

Code lives in `labs/course-12b-bigdata/`.

## Read this before you read anything else

**Every file in this lab runs, on a real Hadoop 3.3.6 cluster.** Most experiments have two halves:

| Half | Files | Status |
|---|---|---|
| **The tool you run on a cluster** | **15 files** — shell scripts of `hdfs`, `yarn`, `sqoop` and `zkCli.sh` commands, Pig, HiveQL, the HBase shell, a Flume agent, Java and Scala | **Run**, each on a fresh cluster, by `tools/data-science/hadoop_lab.py`; what it printed is under **5. Execution and Results** |
| **The check** | **14 programs** | **Executed and asserted** by `tools/data-science/run_bigdata_labs.py`, which also runs the tool files and checks their answers |

*(Updated October 2026: Hadoop, Pig, Hive, HBase, ZooKeeper, Sqoop and Flume could not be
installed where these labs are checked, and every tool file said NOT EXECUTED. They now install
from archive.apache.org, with MariaDB from the Ubuntu archive for Sqoop, and running the files
found faults that reading them had not — a Pig keyword used as a field name, two Hive statements
that stop the script, a Sqoop query with two columns of one name, a Flume agent that dropped its
HDFS sink and routed nothing, an HBase filter that let rows through, a Spark scan that saw no
rows. Each is corrected in its file and noted under its experiment.)*

```bash
bash tools/data-science/setup_hadoop.sh         # Hadoop, Pig, Hive, HBase, ZooKeeper, Sqoop, Flume
bash tools/data-science/setup_spark.sh          # PySpark, for experiment 17
pip install -r tools/requirements.txt
python3 tools/data-science/run_bigdata_labs.py  # about half an hour; --audit-only skips the cluster
```

<div class="example" markdown="1">
<span class="label">HOW THE TOOL FILES WERE RUN</span>

`hadoop_lab.py` formats and starts a cluster in a temporary folder for each file — a NameNode,
**four DataNodes** (so replication 3 can survive the loss of one, and a block can be
re-replicated), a SecondaryNameNode, a ResourceManager, a NodeManager and the JobHistory server
— then runs the file as a student types it, printing `$ command` before each command, and stops
everything at the end.

Where a file assumes something is already there — the sales file in HDFS, a database for Sqoop,
HBase running — a `_drive_` script beside it does that first, and those commands are printed
too, so the transcript shows everything that ran. One setting differs from a default cluster,
and the experiment that depends on it says so: a DataNode is declared dead after **60 s, not
630 s**.

A cluster makes new ids, ports and times on every run — block ids, application ids, the port
a DataNode took, how long a job ran. The output shown is one run's, unchanged;
`capture_lab_outputs.py --check` compares a rerun with those values masked, and every other
line must repeat exactly.
</div>

### The cross-course check

**Experiments 10, 14 and 17 all use Business Intelligence Tools' star schema, imported rather
than copied.** `fixtures.py` loads `labs/course-11-bi/fixtures.py` by path at
import time, so the two courses cannot drift.

**South = ₹10,360** is produced by Business Intelligence Tools' DAX `CALCULATE`, by DuckDB and by
**Hive** in experiment 10, and by Spark — reading **HBase** — in experiment 17. **If they ever
disagree, one of them is wrong and `verify_all.sh` says so.**

---

## Experiment 1 — Installation and setup of a Hadoop single-node cluster

### 1. Question

Install Hadoop on one machine, configure it, and start its daemons.

### 2. Aim

Download Hadoop, write its four configuration files, format HDFS, start the five daemons and check each one is up.

### 3. Steps

**On the cluster**, `01_install_hadoop.sh`:

1. **Check the prerequisites.**
2. **Download and unpack Hadoop.**
3. **Write the four configuration files.**
4. **Format HDFS, and start the five daemons.**
5. **Stop them.**

<div class="formula" markdown="1">
<span class="label">THE THREE INSTALLATION FAILURES EVERYONE HITS</span>

- **`JAVA_HOME` not set inside `hadoop-env.sh`.** Exporting it in your shell
  is not enough — the daemons do not inherit it.
- **Re-running `hdfs namenode -format` after storing data.** The DataNode's
  `clusterID` no longer matches the NameNode's and it refuses to start. Fix:
  delete the datanode directory, or edit its `VERSION` file.
- **`ssh localhost` prompting for a password.** `start-dfs.sh` hangs for ever.

`jps` should show **five processes**: NameNode, DataNode, SecondaryNameNode,
ResourceManager, NodeManager.
</div>


### 4. Programme

**On the cluster**, `01_install_hadoop.sh`:

{{programme: course-12b-bigdata/01_install_hadoop.sh}}

### 5. Execution and Results

**On the cluster**, `01_install_hadoop.sh`:

{{output: course-12b-bigdata/01_install_hadoop.sh}}

This one runs alone, not on the lab's cluster: `_drive_01_install_hadoop.py` gives it an
empty home directory and the Hadoop tarball, and the script does everything else — unpacks,
configures, formats, starts, checks and stops. Where it was run there is no ssh server, so the
daemons are started one by one with `hdfs --daemon start`, the command `start-dfs.sh` runs on
each host over ssh.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Hadoop 3.3.6 installed in an empty home directory, HDFS formatted, the five daemons running — `jps` lists all five — one live DataNode, and both web interfaces answering 200. Two corrections: the download moved to archive.apache.org, and MapReduce needs `HADOOP_MAPRED_HOME` passed to its containers.
</div>


## Experiment 2 — Hadoop's directory structure and basic commands

### 1. Question

Explore the Hadoop directory structure and its basic commands — the `hadoop fs` operations.

### 2. Aim

Make, list, copy, move and remove files in HDFS; count the space they use; set permissions and replication; and ask where a file's blocks are.

### 3. Steps

**On the cluster**, `02_hdfs_commands.sh`:

1. **Make a directory, and list it.**
2. **Put a file in, and read it back.**
3. **Copy, move and remove.**
4. **Count the space used.**
5. **Set permissions and replication.**
6. **Ask where the blocks are, and how the cluster is.**

<div class="formula" markdown="1">
<span class="label">THE FOUR HADOOP FS FACTS WORTH MARKS</span>

- **`hadoop fs` and `hdfs dfs` are the same command.** `hadoop fs` also works
  on local and S3 paths.
- **There is no `cd`.** HDFS has no working directory — every path is
  absolute or relative to `/user/$USER`.
- **`-rm` moves to `.Trash`** and still costs quota for a day.
- **There is no in-place edit.** HDFS is write-once, append-only, and that
  single constraint is why it can drop file locking entirely.
</div>


### 4. Programme

**On the cluster**, `02_hdfs_commands.sh`:

{{programme: course-12b-bigdata/02_hdfs_commands.sh}}

### 5. Execution and Results

**On the cluster**, `02_hdfs_commands.sh`:

{{output: course-12b-bigdata/02_hdfs_commands.sh}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Every `hdfs dfs` operation ran against the cluster. A removed file goes to `.Trash`, and `fsck` and `dfsadmin -report` show where each block lives and what each DataNode holds.
</div>


## Experiment 3 — Hadoop's architecture, from its logs

### 1. Question

Demonstrate the Hadoop architecture components — HDFS, YARN and MapReduce — using sample logs.

### 2. Aim

Run one MapReduce job over a sample log, then follow it through the logs of the daemons that ran it.

### 3. Steps

**On the cluster**, `03_architecture.sh`:

1. **List the daemons.**
2. **Run a job, and find it.**
3. **Read each daemon's log.**

<div class="formula" markdown="1">
<span class="label">THE LOG TRACE TO FOLLOW</span>

RM: application submitted → NM: AM container started → RM: map containers
assigned → NM: map tasks start → NameNode: block reads served **locally** →
RM: reduce containers assigned → **NM: reduce fetches map outputs, over HTTP**
→ RM: SUCCEEDED.

**The one line worth finding is the shuffle fetch.** It is the only step where
data crosses the network in bulk, and it is what the combiner in experiment 7
exists to shrink.
</div>


### 4. Programme

**On the cluster**, `03_architecture.sh`:

{{programme: course-12b-bigdata/03_architecture.sh}}

### 5. Execution and Results

**On the cluster**, `03_architecture.sh`:

{{output: course-12b-bigdata/03_architecture.sh}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

One job, traced through four daemons: the ResourceManager admitted it and allocated its containers, the NodeManager launched them, the NameNode served the blocks, and the reduce fetched the map outputs over HTTP — the shuffle.
</div>


## Experiment 4 — Storing a large file in HDFS: blocks and replication

### 1. Question

Store and retrieve a large file in HDFS, and demonstrate its block distribution and replication factor.

### 2. Aim

Put a 300 MB file into HDFS, find its blocks and where each replica is, change its replication, and work out the block arithmetic and the small-files cost.

### 3. Steps

**On the cluster**, `04_hdfs_store.sh`:

1. **Make a 300 MB file.**
2. **Put it in HDFS.**
3. **Find its blocks and their replicas.**
4. **Change its replication.**
5. **Write it again with 64 MB blocks.**
6. **Get it back, and compare.**

**The Python check**, `04_blocks_replication.py`:

1. **Size the blocks.**
2. **Place a 1 GB file's replicas.**
3. **Count the small-files cost.**

<div class="formula" markdown="1">
<span class="label">THE BLOCK TABLE</span>

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
</div>


### 4. Programme

**On the cluster**, `04_hdfs_store.sh`:

{{programme: course-12b-bigdata/04_hdfs_store.sh}}

**The Python check**, `04_blocks_replication.py`:

{{programme: course-12b-bigdata/04_blocks_replication.py}}

### 5. Execution and Results

**On the cluster**, `04_hdfs_store.sh`:

{{output: course-12b-bigdata/04_hdfs_store.sh}}

**The Python check**, `04_blocks_replication.py`:

{{output: course-12b-bigdata/04_blocks_replication.py}}

<div class="example" markdown="1">
<span class="label">REPLICA PLACEMENT, 1 GB OVER 6 NODES IN 2 RACKS</span>

| Block | Replicas | Racks |
|---:|---|---:|
| 0 | n0/r0, n1/r1, n3/r1 | 2 |
| 1 | n2/r0, n3/r1, n5/r1 | 2 |
| 2 | n4/r0, n5/r1, n1/r1 | 2 |
| … | … | 2 |

**Every block spans exactly two racks** — one replica on the writer's rack,
two on another. Asserted for all 8 blocks.
</div>

<div class="example" markdown="1">
<span class="label">THE SMALL-FILES TABLE</span>

| Scenario | Files | Blocks | NameNode RAM |
|---|---:|---:|---:|
| one 1 GB file | 1 | 8 | **0.00 MB** (1,350 bytes) |
| 1,000 × 1 MB | 1,000 | 1,000 | 0.29 MB |
| 1,000,000 × 1 KB | 1,000,000 | 1,000,000 | **286.10 MB** |

**A factor of 222,222 for the same gigabyte.**
</div>

<div class="formula" markdown="1">
<span class="label">AND THE STORAGE TRADE</span>

1 GB at replication 3 occupies **3,072 MB**; under RS-6-3 erasure coding,
**1,536 MB** — 200% overhead against 50%, at the cost of expensive
reconstruction reads.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A 300 MB file is 128 + 128 + 44 MB, three blocks, each on three of the four DataNodes; the same file in 64 MB blocks is five. The arithmetic agrees: 260 MB is 128 + 128 + 4, and a million 1 KB files cost the NameNode 222,222 times the memory of one 1 GB file.
</div>


## Experiment 5 — Fault tolerance and recovery

### 1. Question

Simulate NameNode and DataNode failure, and observe fault tolerance and recovery.

### 2. Aim

Kill a DataNode and read the file anyway; wait for the NameNode to declare it dead and re-replicate; kill the NameNode and watch it recover from its image and edits; then work out which failures lose data.

### 3. Steps

**On the cluster**, `05_fault_tolerance.sh`:

1. **Have the 300 MB file.**
2. **Kill a DataNode, and read the file.**
3. **Wait for it to be declared dead.**
4. **Bring it back.**
5. **Kill the NameNode, and restart it.**
6. **Read what recovery reads.**

**The Python check**, `05_fault_tolerance.py`:

1. **Fail nodes and racks.**
2. **Find the worst case.**
3. **Re-replicate.**
4. **Lose the NameNode.**
5. **Compare the three answers.**

<div class="formula" markdown="1">
<span class="label">WHICH FAILURES LOSE DATA</span>

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
</div>


### 4. Programme

**On the cluster**, `05_fault_tolerance.sh`:

{{programme: course-12b-bigdata/05_fault_tolerance.sh}}

**The Python check**, `05_fault_tolerance.py`:

{{programme: course-12b-bigdata/05_fault_tolerance.py}}

### 5. Execution and Results

**On the cluster**, `05_fault_tolerance.sh`:

{{output: course-12b-bigdata/05_fault_tolerance.sh}}

**The Python check**, `05_fault_tolerance.py`:

{{output: course-12b-bigdata/05_fault_tolerance.py}}

<div class="example" markdown="1">
<span class="label">THE HONEST VERSION, BY BRUTE FORCE</span>

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
</div>

<div class="formula" markdown="1">
<span class="label">THE 630-SECOND DELAY</span>

`10 × 3 s + 2 × 5 min = 630 s` before a DataNode is declared dead. **The delay
is deliberate** — a node that reboots in five minutes should not trigger a
cluster-wide copy storm. The lab's cluster sets the recheck interval to 15 s, so
`10 × 3 s + 2 × 15 s = 60 s`, and the script waits 75 s rather than eleven minutes; the
formula is the same.
</div>

<div class="warn" markdown="1">
<span class="label">THE NAMENODE'S BLOCK MAP IS NEVER PERSISTED</span>

| Component | Holds | Lost on crash? |
|---|---|---|
| `fsimage` (disk) | the namespace at a checkpoint | no |
| `edits` (disk) | changes since | no |
| **block map (RAM)** | block → DataNode locations | **YES** |

Rebuilt from block reports at startup, which is why a large NameNode takes
minutes to leave safe mode — the `safemode get` above caught it there. **And the Secondary
NameNode is a checkpointer, not a standby** — the most misleadingly named component in Hadoop.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

With a DataNode killed the 300 MB file was still read in full; the node was declared dead and its blocks re-replicated to the three still alive; with the NameNode killed nothing was reachable, and after its restart and safe mode every byte was there. In the model, any two failures are survivable and 6 of the 20 three-node failures lose data.
</div>


## Experiment 6 — YARN: the ResourceManager, the NodeManager and the schedulers

### 1. Question

Configure YARN and run sample applications, observing the roles of the ResourceManager and the NodeManager.

### 2. Aim

Set up two Capacity Scheduler queues, run the sample applications into each, observe the nodes and queues, and kill a running job; then compare FIFO, fair and capacity scheduling on one workload.

### 3. Steps

**On the cluster**, `06_yarn.sh`:

1. **Read the configuration that matters.**
2. **Set up the queues.**
3. **Run the sample applications.**
4. **Submit to a named queue.**
5. **Observe the nodes and queues.**
6. **Kill a job.**

**The Python check**, `06_yarn_scheduling.py`:

1. **Set out the workload.**
2. **Schedule first in, first out.**
3. **Schedule fairly.**
4. **Schedule by capacity.**
5. **Name who does what.**

<div class="formula" markdown="1">
<span class="label">THE SCHEDULERS, ON ONE WORKLOAD</span>

The workload: an 8-container cluster; `big_etl` needs all 8 for 10 s;
`small_q1` and `small_q2` need 1 container for 2 s; `medium` needs 4 for 5 s.

| Job | FIFO | Fair | Capacity (75/25) |
|---|---:|---:|---:|
| `big_etl` | **10** | 14 | 20 |
| `small_q1` | **11** | **1** | **2** |
| `small_q2` | 12 | 1 | 3 |
| `medium` | 16 | 5 | 22 |
| **total turnaround** | **49** | **21** | — |
</div>


### 4. Programme

**On the cluster**, `06_yarn.sh`:

{{programme: course-12b-bigdata/06_yarn.sh}}

**The Python check**, `06_yarn_scheduling.py`:

{{programme: course-12b-bigdata/06_yarn_scheduling.py}}

### 5. Execution and Results

**On the cluster**, `06_yarn.sh`:

{{output: course-12b-bigdata/06_yarn.sh}}

**The Python check**, `06_yarn_scheduling.py`:

{{output: course-12b-bigdata/06_yarn_scheduling.py}}

<div class="example" markdown="1">
<span class="label">WHAT THE NUMBERS SAY, STATED CAREFULLY</span>

- **`small_q1` waits 11 s under FIFO for 2 s of work.** Head-of-line blocking.
- **Fair sharing did not make the cluster faster.** `big_etl` finished *later*,
  10 → 14. Latency moved from the small jobs to the big one.
- **The work is identical: 104 container-seconds either way**, which on 8
  containers cannot finish before second 13.
- **Total turnaround still halved**, 49 → 21, because FIFO left three jobs
  idle in a queue. Scheduling cannot create throughput, but idle-while-queued
  is real waste.
</div>

<div class="formula" markdown="1">
<span class="label">THE CAPACITY SCHEDULER'S GUARANTEE</span>

The adhoc queue holds **25% of the cluster whatever else is running**, so a short
query has a guarantee rather than a hope — the queues the script set up report 75% and 25%,
with adhoc allowed to grow to 50%. The cost: that share sits idle when adhoc is empty, unless
`maximum-capacity` is raised to allow **elasticity** — which is exactly the difference between
"capacity" and "fair".
</div>

**One ApplicationMaster per job** is the change that defined YARN. Hadoop 1's
JobTracker did both scheduling and per-job management, so it was the
bottleneck *and* the single point of failure, and it could run only MapReduce.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Pi, TeraGen, TeraSort and TeraValidate ran in the production queue and Pi again in adhoc, each SUCCEEDED; a long Pi job was killed by its id and finished KILLED. In the model, fair sharing halves total turnaround, 49 s to 21 s, on the same 104 container-seconds of work.
</div>


## Experiment 7 — Word count in MapReduce

### 1. Question

Write a simple MapReduce program for word count.

### 2. Aim

Count the words in six documents with a Java MapReduce job, with a combiner; then make the shuffle visible with a MapReduce engine in Python, and see when a combiner is safe.

### 3. Steps

**On the cluster**, `WordCount.java`:

1. **Map each word to 1.**
2. **Reduce by summing.**
3. **Configure the job, with a combiner.**

**The Python check**, `07_wordcount.py`:

1. **Map, shuffle and reduce the documents.**
2. **Read the top words.**
3. **Add a combiner.**
4. **See when a combiner is not safe.**
5. **Partition the keys.**

<div class="formula" markdown="1">
<span class="label">THE SHUFFLE, MADE VISIBLE</span>

`mapreduce.py`, which `07_wordcount.py` imports, is a MapReduce engine in forty lines, written
out in full. **The point is that it makes the shuffle visible**, and the shuffle is the part
students never see and the part that costs the money.

| Phase | Records |
|---|---:|
| map output | **48** |
| shuffled | **48** |
| reduce output | **26** |

Top words: `the` 5, `big` 4, `data` 4, `dog` 4, `quick` 3, `fox` 3.
**The counts sum back to 48** — reduce is a regrouping, and if your totals do
not reconcile, your reducer is not associative.
</div>


### 4. Programme

**On the cluster**, `WordCount.java`:

{{programme: course-12b-bigdata/WordCount.java}}

**The Python check**, `07_wordcount.py`:

{{programme: course-12b-bigdata/07_wordcount.py}}

### 5. Execution and Results

**On the cluster**, `WordCount.java`:

{{output: course-12b-bigdata/WordCount.java}}

**The Python check**, `07_wordcount.py`:

{{output: course-12b-bigdata/07_wordcount.py}}

<div class="example" markdown="1">
<span class="label">THE COMBINER, AND WHY ITS SAVING IS SMALL HERE</span>

| | Shuffled |
|---|---:|
| no combiner | **48** |
| with combiner | **39** |
| saving | **9 (18.75%)** |

**Note how small that is, and why it is honest.** The combiner runs **per map
task**, and these documents are 5 to 11 words — there is almost nothing to
merge within one split. On a 128 MB split the same combiner cuts the shuffle
by orders of magnitude. **The cluster agrees**: its counters show the same 48 map output
records and 39 combine output records.

**The combiner's value scales with split size**, which is the point this tiny
dataset makes precisely by failing to impress.
</div>

<div class="warn" markdown="1">
<span class="label">THE COMBINER THAT IS WRONG</span>

| Reducer computes | Safe? |
|---|---|
| sum, max, count | **yes** |
| **mean** | **NO** |
| median | **NO** |

Demonstrated: `[1,1,1,10]` and `[10]` give **mean of means 6.6250** against
**true mean 4.6000**. Emit `(sum, count)` and divide only in the reducer —
the same average-of-averages trap Business Intelligence Tools met in DAX.
</div>

**Partitioning.** 3 reducers give partitions of **[20, 17, 11]**, ratio 1.82. Hash partitioning
is only as balanced as the key distribution, and **skew, not volume, is what
usually kills a MapReduce job**.

**The three Java details.** **The map key is a byte offset, not a line number.** **Reuse the
`Writable` objects** — a `new Text()` per word makes GC the job. **The reduce `Iterable`
can be walked once** — it streams from disk.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

48 words in, 26 distinct words out, on the cluster and in the engine alike; the combiner cut the 48 shuffled records to 39 — 18.75%, small because each split is one short document. A combiner for a mean is wrong: 6.6250 against the true 4.6000.
</div>


## Experiment 8 — An inverted index in MapReduce

### 1. Question

Develop a MapReduce job for inverted index creation.

### 2. Aim

Build, with a Java MapReduce job, an index from each word to the documents it occurs in and how often; then answer queries from the index alone, and measure its size and skew.

### 3. Steps

**On the cluster**, `InvertedIndex.java`:

1. **Map each word to its document.**
2. **Reduce to a posting list.**
3. **Configure the job.**

**The Python check**, `08_inverted_index.py`:

1. **Build the index.**
2. **Read a slice of it.**
3. **Answer queries from it.**
4. **Weigh its size.**
5. **See why it is a MapReduce job.**
6. **Measure the skew.**

<div class="formula" markdown="1">
<span class="label">THE INDEX</span>

| Term | Postings |
|---|---|
| `dog` | doc1:1, doc2:1, doc3:1, doc6:1 |
| `quick` | doc1:1, **doc3:2** |
| `big` | doc4:2, doc5:2 |

**`quick` appears twice in doc3, and the posting records it.** Frequency is
the difference between "does this word occur" and "how relevant is this
document" — boolean retrieval against ranked retrieval, in one number.
</div>


### 4. Programme

**On the cluster**, `InvertedIndex.java`:

{{programme: course-12b-bigdata/InvertedIndex.java}}

**The Python check**, `08_inverted_index.py`:

{{programme: course-12b-bigdata/08_inverted_index.py}}

### 5. Execution and Results

**On the cluster**, `InvertedIndex.java`:

{{output: course-12b-bigdata/InvertedIndex.java}}

**The Python check**, `08_inverted_index.py`:

{{output: course-12b-bigdata/08_inverted_index.py}}

<div class="example" markdown="1">
<span class="label">QUERIES ANSWERED FROM THE INDEX ALONE</span>

| Query | Result |
|---|---|
| `quick AND fox` | doc1, doc3 |
| `big AND data` | doc4, doc5 |
| `dog AND machine` | **no match** |
| `dog OR machine` | doc1, doc2, doc3, doc4, doc6 |

**Not one document was read.** Query cost depends on the number of **matches**,
not on the size of the corpus — which is the entire point of an inverted index.
</div>

**The index is not free.** 226 characters of corpus → 26 terms, **39 postings**. A full-text
index typically runs 20–40% of the corpus size, before positions. Search is a space-for-time
trade.

**The skew, measured.** Largest posting list: `the`, with 5. Singleton terms: 15 of 26. `the`
would be the biggest list on any English corpus, and one reducer holding it is the job's
critical path.

<div class="warn" markdown="1">
<span class="label">THE JAVA DETAIL THAT IS EXAMINED</span>

**The filename is in neither the key nor the value.** It comes from the input
split — `((FileSplit) context.getInputSplit()).getPath().getName()`.

And **this job cannot use a combiner**: the reducer's output type (a posting
string) differs from its input type (a document id), and a combiner must match
the reducer on both — the cluster's counters show `Combine input records=0`.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

6 documents in, 26 index terms out, from 48 postings — on the cluster and in the engine alike; `quick` is `doc1:1, doc3:2`. Boolean queries are answered without reading a document, and the largest posting list is `the`, 5 occurrences in 3 documents.
</div>


## Experiment 9 — Data analysis with Pig Latin

### 1. Question

Perform data analysis using Pig Latin scripts.

### 2. Aim

Load the sales, filter, group and total them by category, order the result, join the stores map-side and flatten the tags; then walk the same dataflow one operator at a time.

### 3. Steps

**On the cluster**, `09_analysis.pig`:

1. **Load the sales.**
2. **Build the dataflow, a relation per step.**
3. **Describe, illustrate and explain it.**
4. **Store the result.**
5. **Join the stores, map-side.**
6. **Flatten the tags.**

**The Python check**, `09_pig_equivalent.py`:

1. **Load the sales.**
2. **Filter the bulk orders.**
3. **Group by category.**
4. **Total each group.**
5. **Order by revenue.**
6. **Join the stores.**
7. **Map the operators to SQL.**
8. **See lazy evaluation.**

<div class="formula" markdown="1">
<span class="label">THE DATAFLOW</span>

The Python half walks the dataflow **one operator at a time**, which is how you
debug a Pig script anyway — that is what `ILLUSTRATE` does.

```
A = LOAD 'sales'                 -- 9 rows
B = FILTER A BY qty >= 6         -- 7 rows
C = GROUP B BY category          -- 3 groups: Grocery {4}, Personal {1}, Stationery {2}
D = FOREACH C GENERATE group, SUM(B.qty), SUM(B.revenue)
E = ORDER D BY revenue DESC      -- top category: Grocery
```
</div>


### 4. Programme

**On the cluster**, `09_analysis.pig`:

{{programme: course-12b-bigdata/09_analysis.pig}}

**The Python check**, `09_pig_equivalent.py`:

{{programme: course-12b-bigdata/09_pig_equivalent.py}}

### 5. Execution and Results

**On the cluster**, `09_analysis.pig`:

{{output: course-12b-bigdata/09_analysis.pig}}

**The Python check**, `09_pig_equivalent.py`:

{{output: course-12b-bigdata/09_pig_equivalent.py}}

<div class="warn" markdown="1">
<span class="label">GROUP PRODUCES A BAG, NOT AN AGGREGATE</span>

`(Grocery, {4 tuples})` — the bag is the value, and `FOREACH … GENERATE` turns
it into numbers. **Hive fuses the two; Pig keeps them apart**, which is why Pig
can do things to a group that SQL cannot express without a window function.
</div>

**The two operators with no SQL equivalent.** **`LOAD`** reads a semi-structured file with no
schema declared in advance — SQL assumes a table exists. **`ILLUSTRATE`** pushes sample rows
through *every step* of the plan. Those two are the reason to reach for Pig on ETL.

**Lazy evaluation.** **Nothing runs until `STORE` or `DUMP`.** Pig sees the whole dataflow first,
so it merges the `FILTER` into the `LOAD` and fuses consecutive `FOREACH`es into one job — the
`EXPLAIN` above shows the plan it made. **Writing the steps separately costs nothing** — which
is the whole argument against nesting sub-queries "to avoid extra passes".

**The join hint that matters.** `USING 'replicated'` is a **map-side join**: the small relation
loads into every mapper's memory and there is **no shuffle**. It dies with an `OutOfMemoryError`
if the relation does not fit — which is why broadcast joins have a size threshold.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Pig, on the cluster, gives Grocery 4 orders, 36 units, ₹8,680; Stationery 2, 35, ₹1,400; Personal 1, 7, ₹980 — the bulk orders by category, revenue first. `store` is a Pig keyword and cannot name a field.
</div>


## Experiment 10 — Hive: tables, partitions and buckets

### 1. Question

Execute Hive queries for structured data analysis, with tables and partitions.

### 2. Aim

Lay a table over the sales file, load a partitioned and bucketed table from it, aggregate by region, prune a partition and rank with a window function; then check each figure in DuckDB.

### 3. Steps

**On the cluster**, `10_hive.hql`:

1. **Create the database.**
2. **Lay an external table over the file.**
3. **Create the partitioned, bucketed table.**
4. **Load it with dynamic partitions.**
5. **Aggregate by region.**
6. **Prune a partition.**
7. **Rank with a window function.**
8. **Tune, and compute statistics.**

**The Python check**, `10_hive_duckdb.py`:

1. **Aggregate by region.**
2. **Partition by quarter.**
3. **Bucket by store.**
4. **Compare managed with external tables.**
5. **Join, as Hive does.**
6. **See what Hive is not.**

<div class="formula" markdown="1">
<span class="label">THE CROSS-COURSE CHECK</span>

| Region | Revenue | Profit | Margin |
|---|---:|---:|---:|
| South | **10,360** | 2,760 | 26.64% |
| North | **2,520** | 765 | 30.36% |

**South = ₹10,360 is the same number Business Intelligence Tools' DAX `CALCULATE` measure
produced**, and the same one Spark produces in experiment 17. Hive printed it from the cluster;
DuckDB, running the same query text, asserts it. Three engines, two languages, one dataset —
asserted, so drift fails the suite.
</div>


### 4. Programme

**On the cluster**, `10_hive.hql`:

{{programme: course-12b-bigdata/10_hive.hql}}

**The Python check**, `10_hive_duckdb.py`:

{{programme: course-12b-bigdata/10_hive_duckdb.py}}

### 5. Execution and Results

**On the cluster**, `10_hive.hql`:

{{output: course-12b-bigdata/10_hive.hql}}

**The Python check**, `10_hive_duckdb.py`:

{{output: course-12b-bigdata/10_hive_duckdb.py}}

<div class="example" markdown="1">
<span class="label">PARTITION PRUNING</span>

| Partition | Rows | Revenue | Scanned for Q2 |
|---|---:|---:|---:|
| `quarter=Q1` | 5 | 7,660 | **0** |
| `quarter=Q2` | 4 | 5,220 | **4** |
| total | 9 | 12,880 | **4 of 9** |

**A partition is an HDFS directory**, so `WHERE quarter='Q2'` reads one
directory — decided before a byte is read; Hive's `EXPLAIN DEPENDENCY` above lists the one
partition it will read. The partition column is a directory *name*, so it costs no storage.

**The trap:** partitioning by `date_key` here would make 4 directories for 9
rows — the small-files problem, created on purpose.
</div>

<div class="example" markdown="1">
<span class="label">BUCKETING, AND AN HONEST RESULT</span>

`CLUSTERED BY (store) INTO 3 BUCKETS` over three stores:

```
bucket 0: ['Guntur', 'Hyderabad']
bucket 1: (empty)
bucket 2: ['Vijayawada']
```

**Bucket 1 is empty.** Hashing does not distribute small key sets evenly, and
an empty bucket is still a file the job opens. Reporting that is worth more
than pretending the hash was balanced.
</div>

**Managed against external.** **`DROP TABLE` on a MANAGED table deletes the data.** Use
`EXTERNAL` for anything you did not produce and cannot recreate — the classic Hive accident.

**`HAVING` against `WHERE`.** Four products clear ₹1,000 (Grocery total ₹9,800). **`WHERE`
filters rows, `HAVING` filters groups** — and in Hive that is a job-plan difference: a `WHERE` on
a partition column prunes directories before the job starts, a `HAVING` cannot.

<div class="warn" markdown="1">
<span class="label">WHAT HIVE IS NOT</span>

| Expectation | Reality |
|---|---|
| row-level `UPDATE`/`DELETE` | only with ACID + ORC + buckets |
| sub-second queries | seconds to minutes — it plans a **job** |
| indexes | **removed in Hive 3** |
| a server holding data | metadata only |
| enforced constraints | declarative, **not enforced** |

**Hive is a compiler.** Everything surprising follows from that sentence.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Hive, on the cluster, gives South ₹10,360 from 48 units and North ₹2,520 from 39 — the number Business Intelligence Tools' DAX produced — and its query for Q2 reads one partition. DuckDB agrees on every figure.
</div>


## Experiment 11 — Importing from a relational database with Sqoop

### 1. Question

Import data from an RDBMS into Hadoop using Sqoop.

### 2. Aim

Import a MySQL table into HDFS in parallel, import a query and a table into Hive, import only the new rows, save the import as a job, and export a summary back; then model the split queries Sqoop runs.

### 3. Steps

**On the cluster**, `11_sqoop.sh`:

1. **Store the password.**
2. **List the databases and tables.**
3. **Import a table, in parallel.**
4. **Import a query.**
5. **Import into Hive.**
6. **Import only what is new.**
7. **Export back to the database.**

**The Python check**, `11_sqoop_equivalent.py`:

1. **Build the source table.**
2. **Find the split boundaries.**
3. **Split by a skewed column.**
4. **Write the target.**
5. **Import incrementally.**

<div class="formula" markdown="1">
<span class="label">SPLITTING BY THE PRIMARY KEY</span>

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
wrote yourself. The Python half has a real SQLite database at one end and a real Parquet file
at the other. The cluster's run prints the first step: `BoundingValsQuery: SELECT
MIN(order_id), MAX(order_id) FROM orders`.
</div>


### 4. Programme

**On the cluster**, `11_sqoop.sh`:

{{programme: course-12b-bigdata/11_sqoop.sh}}

**The Python check**, `11_sqoop_equivalent.py`:

{{programme: course-12b-bigdata/11_sqoop_equivalent.py}}

### 5. Execution and Results

**On the cluster**, `11_sqoop.sh`:

{{output: course-12b-bigdata/11_sqoop.sh}}

**The Python check**, `11_sqoop_equivalent.py`:

{{output: course-12b-bigdata/11_sqoop_equivalent.py}}

The database is MariaDB, made by `_drive_11_sqoop.py`: `retail.orders` with 90 rows — ten
copies of the nine sales rows, **₹128,800**, exactly ten times Business Intelligence Tools'
₹12,880 — and `retail.customers`, with no primary key. Running the script found three faults,
noted in it: comments after the line-continuing backslashes, which ended each command early; the
query's two columns named `region`; and Hive's jars on the classpath, needed for the Hive import
— but only its `HiveConf`, or the import fails inside Sqoop's own security manager. And Sqoop
1.4.7 does not ship the `org.json` jar its saved jobs need; `setup_hadoop.sh` adds it.

<div class="warn" markdown="1">
<span class="label">SPLITTING BY A SKEWED COLUMN</span>

| Mapper | `qty` range | Rows |
|---:|---|---:|
| 0 | 4..7 | **40** |
| 1 | 8..11 | 20 |
| 2 | 12..15 | 20 |
| 3 | 16..20 | **10** |

**Forty against ten.** Sqoop assumes the split column is uniformly distributed
between min and max. The job's wall clock is the slowest mapper, so a bad
`--split-by` wastes three quarters of your parallelism.
</div>

**The import is verified two ways.** **90 rows and ₹128,800 both check out.** Counting rows alone
would not catch a truncated numeric type — an Oracle `NUMBER(38)` silently becoming a Java
`double` is the classic Sqoop corruption bug.

<div class="example" markdown="1">
<span class="label">NEITHER INCREMENTAL MODE CATCHES A DELETE</span>

`--last-value 90` selects the new rows — 10 on the cluster, 1 in the model. **But Sqoop has no
way to see a row that is gone**, so an incrementally imported table drifts from its source. The
fix is a periodic full re-import — and knowing that is the difference between having used Sqoop
and having read about it.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

From MariaDB: 90 orders imported by four mappers, 90 rows of a join, the customers table into Hive — South 4, North 2 — 10 new rows incrementally, 100 by a saved job that then remembers 100, and 3 summary rows exported back. In the model, the four range queries split 22, 23, 22, 23, and a skewed column splits 40 against 10.
</div>


## Experiment 12 — Capturing log data with Flume

### 1. Question

Capture and store log or streaming data using Flume.

### 2. Aim

Run a Flume agent that tails a web server's access log, adds headers with interceptors, routes server errors to an alert sink and the rest to HDFS; then model its channel and back-pressure.

### 3. Steps

**On the cluster**, `12_flume.conf`:

1. **Name the agent's parts.**
2. **Tail the log files.**
3. **Add headers with interceptors.**
4. **Route on a header.**
5. **Set up the channels.**
6. **Set up the sinks.**
7. **Wire it together.**

**The Python check**, `12_flume_equivalent.py`:

1. **Intercept an event.**
2. **Run a healthy agent.**
3. **Slow the sink.**
4. **Fix it.**
5. **Compare the channel types.**
6. **Read what the sink writes.**
7. **Set the rollover.**

<div class="formula" markdown="1">
<span class="label">THE INTERCEPTOR</span>

```
headers {'host': '10.0.0.1', 'status': '200'}
body    (unchanged, 78 chars)
```

**An interceptor adds headers and leaves the body alone.** Headers are what a
multiplexing selector routes on, so "send 500s to the alert sink" is a header
rule, not code.
</div>


### 4. Programme

**On the cluster**, `12_flume.conf`:

{{programme: course-12b-bigdata/12_flume.conf}}

**The Python check**, `12_flume_equivalent.py`:

{{programme: course-12b-bigdata/12_flume_equivalent.py}}

### 5. Execution and Results

**On the cluster**, `12_flume.conf`:

{{output: course-12b-bigdata/12_flume.conf}}

**The Python check**, `12_flume_equivalent.py`:

{{output: course-12b-bigdata/12_flume_equivalent.py}}

`_drive_12_flume.py` puts the lab's 40 access-log lines where the agent looks, runs it for 45
seconds, and counts what reached each sink. Running the configuration found two faults, both
from its being a Java properties file:

- **No comment can follow a value.** `rollInterval = 600  # 10 min` made the value the whole
  rest of the line; the agent refused it — `NumberFormatException: For input string: "600 …"` —
  and dropped the HDFS sink.
- **A backslash escapes the next character, and is dropped.** The regex `^\S+ … (\d{3})` became
  `^S+ … (d{3})`, matched nothing, and every event went to the default channel. Every regex
  backslash is doubled.

<div class="example" markdown="1">
<span class="label">THE CHANNEL, AND BACK-PRESSURE</span>

| Configuration | Delivered | Rejected | Peak depth |
|---|---:|---:|---:|
| capacity 100, batch 10, fast sink | 40 | **0** | ≤10 |
| capacity 8, batch 4, **slow sink** | 40 | **8** | **8** |
| capacity 20, slow sink | 40 | **0** | 16 |
| capacity 100, slow sink | 40 | **0** | 16 |

**Eight events refused** because the sink could not drain the channel. In a
real agent the source then **blocks** — back-pressure travelling back to the
web server. **"Flume lost my events" almost always means "the channel was full
and the source gave up".** And a bigger channel absorbs a longer burst and buys
nothing once the sink is permanently slower. **Buffers smooth bursts; they
cannot fix a throughput deficit.**
</div>

**What landed.** `{'200': 24, '404': 8, '500': 8}`, evenly over four hosts (10 each) — the
agent on the cluster split them the same way. **Those same numbers appear in experiments 14 and
17** — three code paths, one set of figures.

<div class="warn" markdown="1">
<span class="label">THE DEFAULTS MANUFACTURE THE SMALL-FILES PROBLEM</span>

`rollInterval` 30 s, `rollSize` 1024 bytes, `rollCount` 10 events → **40 events
produce ~4 HDFS files**, each a few hundred bytes. Left alone, Flume generates
the Unit 2 small-files problem at two files a minute. With the configuration's settings the 32
events made one file.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The agent read the 40 log lines, sent the 8 with status 500 to the logger sink and the other 32 — 24 of 200, 8 of 404 — to one HDFS file under `dt=`/`hr=`. Before two corrections it delivered nothing to HDFS and routed nothing.
</div>


## Experiment 13 — Avro and Parquet

### 1. Question

Serialize and store datasets in Avro and Parquet formats.

### 2. Aim

Write the sales in Avro and in Parquet, read them back, evolve the Avro schema, read only some Parquet columns, and compare the sizes honestly.

### 3. Steps

**The Python check**, `13_avro_parquet.py`:

1. **Write and read Avro.**
2. **Evolve the schema.**
3. **Write Parquet, and read only some columns.**
4. **Compare the two formats.**
5. **Test the claim at size.**

<div class="formula" markdown="1">
<span class="label">THE REAL FORMATS</span>

`fastavro` and `pyarrow` are real implementations, so **the files written here
are byte-for-byte readable by Hadoop, Hive and Spark.**

**Avro: self-describing.** 9 records, **938 bytes**, round-trip exact. The writer's schema is in
the file header — full name `in.ac.datascience.sales.Sale`, namespace included.
</div>


### 4. Programme

**The Python check**, `13_avro_parquet.py`:

{{programme: course-12b-bigdata/13_avro_parquet.py}}

### 5. Execution and Results

**The Python check**, `13_avro_parquet.py`:

{{output: course-12b-bigdata/13_avro_parquet.py}}

<div class="example" markdown="1">
<span class="label">SCHEMA EVOLUTION, DEMONSTRATED</span>

```
read 9 OLD records with a NEW nine-field schema
the added field 'channel' comes back as None -- its DEFAULT
```

**The old file was not rewritten.** Avro resolves writer's schema against
reader's, field by field. **A field added without a default breaks exactly
this**, and that is the one rule to remember.
</div>

<div class="example" markdown="1">
<span class="label">PARQUET: COLUMN PROJECTION</span>

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
</div>

<div class="warn" markdown="1">
<span class="label">THE COMPRESSION CLAIM, TOLD HONESTLY</span>

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
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

938 bytes of Avro and an exact round trip; old records read with a new schema get the added field's default; `SELECT revenue` reads 143 of 949 Parquet column bytes. On nine rows Parquet is 4.8 times larger than CSV, and the 303× ratio holds only for repetitive data — 12.0× once the rows vary.
</div>


## Experiment 14 — An end-to-end ingestion workflow, batch and streaming

### 1. Question

Build an end-to-end ingestion workflow combining batch (Sqoop) and streaming (Flume).

### 2. Aim

Import the orders in a batch leg and the log events in a stream leg, both to Parquet, then join them in DuckDB — first wrongly, then at a common grain.

### 3. Steps

**The Python check**, `14_pipeline.py`:

1. **Run the batch leg and the stream leg.**
2. **Join them.**
3. **Fix the join.**
4. **Compare the two legs.**
5. **Set lambda against kappa.**
6. **Reconcile.**

<div class="formula" markdown="1">
<span class="label">THE FAN TRAP</span>

SQLite → Parquet (batch), log events → Parquet (streaming), then a real DuckDB
query across both. The batch leg is experiment 11's import and the stream leg experiment 12's
agent, each done here in Python so the two legs can be joined in one program; experiments 11
and 12 ran the real tools on the cluster.

```
events counted through the join: 90
events actually ingested       : 40
```

**Each host appears in several orders, so every event is counted once per
matching order.** This is **the same fan trap Business Intelligence Tools found in a Power BI
model** — not a SQL problem, a **grain** problem, appearing wherever two fact
tables are joined directly.
</div>


### 4. Programme

**The Python check**, `14_pipeline.py`:

{{programme: course-12b-bigdata/14_pipeline.py}}

### 5. Execution and Results

**The Python check**, `14_pipeline.py`:

{{output: course-12b-bigdata/14_pipeline.py}}

<div class="example" markdown="1">
<span class="label">THE FIX</span>

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
</div>

**The row that changes the design.** **"Late data is normal."** A streaming aggregate for 09:00
is not final at 10:00, so either you accept eventual correctness or you keep a watermark and
re-emit. The batch leg has no such problem — which is exactly why the **Lambda architecture**
keeps both, and why **Kappa** removes the batch layer by making the stream replayable.

**Lambda's real cost is not machines — it is the same business rule living in
two codebases and drifting.**

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Joined directly, the 40 events are counted 90 times — the fan trap. Aggregated to the host first, then joined, both sides reconcile: 9 orders, ₹12,880, 40 events, 8 errors.
</div>


## Experiment 15 — HBase: tables and CRUD

### 1. Question

Create and manage tables in HBase, with CRUD operations.

### 2. Aim

Create a table with two column families, put, get and scan cells, update and delete them, count atomically, alter and truncate the table and pre-split another; then model row keys, versions and tombstones.

### 3. Steps

**On the cluster**, `15_hbase.rb`:

1. **Create the table.**
2. **Put cells.**
3. **Get a row.**
4. **Scan.**
5. **Update and delete.**
6. **Count atomically.**
7. **Alter, and truncate.**
8. **Pre-split a table.**

**The Python check**, `15_hbase_model.py`:

1. **Create the table and put rows.**
2. **Get a row.**
3. **Keep versions.**
4. **Delete, with a tombstone.**
5. **Scan by prefix.**
6. **Design the row key.**
7. **Compare HBase with what it is confused with.**

<div class="formula" markdown="1">
<span class="label">THE ROW KEY THAT SILENTLY LOSES A SALE</span>

```
row key 'region#store#date' over 9 fact rows
produces only 8 DISTINCT KEYS -- 1 row would be overwritten
```

Vijayawada sold Rice **and** Shampoo on D1. **HBase would not complain** — it
would version one over the other. **A row key must be unique at the grain**,
and in HBase nothing checks that for you.
</div>


### 4. Programme

**On the cluster**, `15_hbase.rb`:

{{programme: course-12b-bigdata/15_hbase.rb}}

**The Python check**, `15_hbase_model.py`:

{{programme: course-12b-bigdata/15_hbase_model.py}}

### 5. Execution and Results

**On the cluster**, `15_hbase.rb`:

{{output: course-12b-bigdata/15_hbase.rb}}

**The Python check**, `15_hbase_model.py`:

{{output: course-12b-bigdata/15_hbase_model.py}}

`_drive_15_hbase.py` starts HBase in standalone mode — its own ZooKeeper, data in a local
folder — with the Java Snappy codec configured, since the table asks for `COMPRESSION =>
'SNAPPY'` and the native library is not there; then types the file into `hbase shell`.

**Versions.** A `put` to an existing cell adds a version; it does not overwrite. The shell's
`get` with `VERSIONS => 3` above shows both values of `sales:qty`, newest first; the model:

```
ts=38   111
ts=37    99
ts=19    20
```

<div class="warn" markdown="1">
<span class="label">A DELETE MAKES THE TABLE BIGGER</span>

```
DELETE info:category   readable? no    cells: 38 -> 39
```

**A tombstone.** Data and marker disappear only at major compaction — the
answer to "I deleted a billion rows and disk usage went up".
</div>

**Scans.** `SCAN 'South'..'South~'` → 6 rows in the model's nine, and `'North'..'North~'` → 3;
in the shell's two-row table, 1. **A prefix
scan reads exactly the rows you want, sequentially** — and works only because `region` is the
*first* component of the key. **Ask it the wrong way** — `category = 'Grocery'` — and it is a
**full table scan**. HBase has no secondary index.

<div class="example" markdown="1">
<span class="label">ROW KEY DESIGN</span>

| Key | Writes go to | Verdict |
|---|---|---|
| timestamp | the last region | **HOTSPOT** |
| sequential id | the last region | **HOTSPOT** |
| `md5(id) + id` | everywhere | good — **scans lost** |
| `region#store#date#product` | by region | good — **prefix scans work** |

**You cannot have even write distribution and range scans on the same
dimension. Choosing is what row-key design means.**
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

In the HBase shell every operation ran: a second `put` kept both versions of the cell, a prefix scan and a value filter each found the one South row, the counter counted to 1. The filter needed two more arguments, or rows without the column passed it. In the model, the row key `region#store#date` loses a sale.
</div>


## Experiment 16 — Coordination with ZooKeeper

### 1. Question

Demonstrate coordination with ZooKeeper.

### 2. Aim

Start a three-server ensemble, see which server leads, build a tree of znodes, make ephemeral and sequential nodes, and run the leader-election recipe; then model election, locking and ensemble sizing.

### 3. Steps

**On the cluster**, `16_zookeeper.sh`:

1. **Configure three servers.**
2. **Start them, and see the leader.**
3. **Build the tree.**
4. **Make an ephemeral node.**
5. **Make sequential nodes.**
6. **Elect a leader.**
7. **Look for the systems that use it.**

**The Python check**, `16_zookeeper_model.py`:

1. **Elect a leader.**
2. **Take a distributed lock.**
3. **Rely on an atomic create.**
4. **Size the ensemble.**
5. **See what ZooKeeper is not.**
6. **Name who uses it.**

<div class="formula" markdown="1">
<span class="label">LEADER ELECTION</span>

```
nn1 -> lock-0000000000     LEADER: nn1
nn2 -> lock-0000000001
nn3 -> lock-0000000002

nn1's session expires:  new LEADER: nn2
```

**Nobody ran a failover script.** The ephemeral node was deleted **by the
server**, the watch fired, and nn2 saw itself at the head of the queue. **That
is how HDFS NameNode HA works** — the link back to experiment 5.
</div>


### 4. Programme

**On the cluster**, `16_zookeeper.sh`:

{{programme: course-12b-bigdata/16_zookeeper.sh}}

**The Python check**, `16_zookeeper_model.py`:

{{programme: course-12b-bigdata/16_zookeeper_model.py}}

### 5. Execution and Results

**On the cluster**, `16_zookeeper.sh`:

{{output: course-12b-bigdata/16_zookeeper.sh}}

**The Python check**, `16_zookeeper_model.py`:

{{output: course-12b-bigdata/16_zookeeper_model.py}}

The script starts and stops its own ensemble, three servers on one machine. Which of them wins
the election differs from run to run; exactly one says `Mode: leader`.

<div class="warn" markdown="1">
<span class="label">WATCH YOUR PREDECESSOR, NOT THE LEADER</span>

Watching the leader wakes **every** candidate on one failure — the **herd
effect**. Watching your immediate predecessor wakes exactly one.
</div>

**The lock is the same recipe.**

```
jobA holds the lock
jobA CRASHES -- lock passes to jobB automatically
```

**Released by the session dying, not by the client remembering.** A database
lock survives its holder's crash and deadlocks the system; an ephemeral znode
cannot.

<div class="example" markdown="1">
<span class="label">ENSEMBLE SIZING</span>

| Servers | Quorum | Can lose | Verdict |
|---:|---:|---:|---|
| 3 | 2 | **1** | good |
| **4** | 3 | **1** | **same as 3** |
| 5 | 3 | 2 | good |
| 6 | 4 | 2 | same as 5 |
| 7 | 4 | 3 | good |

**Four servers tolerate one failure — exactly what three tolerate.** The fourth
machine buys nothing and adds a write to every quorum. **3, 5 or 7.**
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Three servers elected one leader; every server held the same tree; an ephemeral node vanished when its session ended; the sequence numbers started at 1, not 0, because the parent counts every child it has had. In the model, four servers tolerate one failure, as three do.
</div>


## Experiment 17 — Spark over HBase

### 1. Question

Process HBase datasets using Spark integration with Hadoop.

### 2. Aim

Read an HBase table into Spark as an RDD, a partition per region, and query it with Spark SQL; then, in PySpark, count words with RDDs, compare `reduceByKey` with `groupByKey`, query the star schema and cache.

### 3. Steps

**On the cluster**, `17_spark_hbase.scala`:

1. **Configure the HBase connection and scan.**
2. **Read the table as an RDD, a partition per region.**
3. **Map each row to a case class.**
4. **Query it with Spark SQL.**

**The Python check**, `17_spark.py`:

1. **Start a SparkSession.**
2. **Count words with RDDs.**
3. **Compare reduceByKey with groupByKey.**
4. **See lazy evaluation and the DAG.**
5. **Query the star schema with DataFrames.**
6. **Analyse the logs.**
7. **Compare Spark with MapReduce.**
8. **Cache, and measure it.**

<div class="formula" markdown="1">
<span class="label">TWO REAL ENGINES</span>

```
real SparkSession: version 4.2.0, master local[2]
```

PySpark installs from PyPI and Java 21 is present, so a genuine session
starts, real RDDs are built, and a **real shuffle** happens inside
`reduceByKey`. The Scala half runs in `spark-shell` against HBase, with HBase's
own jars on the classpath and its `TableInputFormat` — the connector Hadoop ships —
so no separate connector is needed.
</div>


### 4. Programme

**On the cluster**, `17_spark_hbase.scala`:

{{programme: course-12b-bigdata/17_spark_hbase.scala}}

**The Python check**, `17_spark.py`:

{{programme: course-12b-bigdata/17_spark.py}}

### 5. Execution and Results

**On the cluster**, `17_spark_hbase.scala`:

{{output: course-12b-bigdata/17_spark_hbase.scala}}

**The Python check**, `17_spark.py`:

{{output: course-12b-bigdata/17_spark.py}}

`_drive_17_spark_hbase.py` starts HBase as for experiment 15, puts the nine sales rows into
`sales` with the row key `region#store#date#product`, and flushes the table — a scan through
`TableInputFormat` reads the store files, and the rows still in memory were not seen until the
flush; the file says so. `spark-shell` runs on Java 21 and HBase on Java 8.

`17_spark.py`'s output is what it printed to stdout. Spark's JVM logs to stderr — a timestamped
line per event and a progress bar — and that is left out. Among it is one warning worth knowing:
PySpark 4.2 *"does not yet fully support pandas >= 3.0.0"*. The program uses pandas only to load
the shared fixtures, and every figure it prints is asserted.

**The RDD word count.** 26 distinct words, 48 total — identical to experiment 7's MapReduce
answer, on a real distributed engine.

<div class="example" markdown="1">
<span class="label">REDUCEBYKEY AGAINST GROUPBYKEY</span>

| | What crosses the network |
|---|---|
| `groupByKey` | **all 48 pairs**, then counts |
| `reduceByKey` | combines to **35** map-side — `[11, 14, 10]` per partition |

**Note 35, not experiment 7's 39.** Spark's three partitions each hold two
documents, so more merging happens per task. **The combiner's saving depends
on the split**, exactly as Unit 3 said — and this is the same measurement made
two ways.
</div>

**Lazy evaluation.** Three transformations queued; **`.collect()` is the action** that submits
the DAG. That is why a typo in a `map()` surfaces at `collect()`.

<div class="example" markdown="1">
<span class="label">THE CROSS-COURSE CHECK, FOURTH ENGINE</span>

| Region | Revenue | Profit |
|---|---:|---:|
| South | **10,360** | 2,760 |
| North | **2,520** | 765 |

**Business Intelligence Tools' DAX, DuckDB, Hive and Spark all produce ₹10,360.**
</div>

**The logs from experiment 12.** `HTTP 200: 24, 404: 8, 500: 8` — **the same 24 / 8 / 8 the Flume
agent produced.** Ingest with Flume, analyse with Spark, on bytes never transformed in between.

**`cache()`.**

```
two actions over the same RDD, sum = 39,999,800,000
storage level: Memory Serialized 1x Replicated
```

**Without `cache()` the second action recomputes the whole lineage.** Caching
is the highest-value Spark optimisation and the one students forget —
**because nothing fails without it; the job is merely twice as slow.**

<div class="warn" markdown="1">
<span class="label">THE SPARK-OVER-HBASE CAVEAT</span>

**One Spark partition per HBase region** is the whole integration — the nine rows are one
region, so one partition. But **never `put()` per row from a Spark job** — write HFiles and
bulk-load them.

And: **a full-table Spark scan of HBase is slower than the same data in
Parquet**, because HBase stores every cell with its row key, family, qualifier
and timestamp. **If every job is a full scan, the data is in the wrong store.**
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Spark read the nine rows from HBase in one partition — one region — and Spark SQL gave South ₹10,360 from 48 units, as DAX, Hive and DuckDB did. The scan saw nothing until the table was flushed. In PySpark the word count is 26 words and 48 in all, and `reduceByKey` shuffles 35 records against `groupByKey`'s 48.
</div>


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

**Plus the 15 tool files, run on the cluster**, each checked for the answers it must print —
Pig's three categories, Hive's South ₹10,360, Sqoop's 90 imported and 3 exported, Flume's 8
routed events — and none may still say NOT EXECUTED.

**Experiment 17's PySpark half skips loudly** if the PySpark environment is absent, and the tool
files are only audited if the Hadoop stack is — the same graceful-skip pattern Web Technologies
uses for jsdom. A skip is not a pass, and the runner says so.

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
- **₹10,360 from four engines.** The check that makes the rest believable.
