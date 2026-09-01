# Unit 2 — HDFS and YARN

**Syllabus topics:** Deep dive into HDFS architecture: blocks,
NameNode, DataNodes, HDFS file operations, fault tolerance, replication. YARN
architecture: ResourceManager, NodeManager, application scheduling.

---

## The unit that carries the course

**Almost everything else in this course is a consequence of HDFS's design.**
Why Hive partitions by directory, why Flume's defaults are dangerous, why
HBase exists at all, why Spark caches — all of it traces back to decisions
made here. Spend the time.

---

## 2.1 HDFS architecture

### 📖 The shape

**One NameNode holds the namespace. Many DataNodes hold the blocks. They are
different kinds of thing, and conflating them is the commonest error.**

| | **NameNode** | **DataNode** |
|---|---|---|
| How many | one (plus a standby) | hundreds to thousands |
| Holds | the **metadata**: files, directories, permissions, block lists | the **blocks**, as ordinary files on local disk |
| In RAM | the **entire namespace** | nothing much |
| On disk | `fsimage` + `edits` | the block files and their checksums |
| Failure | the cluster is **unusable** | nothing happens |
| Talks to | clients (metadata only) | clients (data) and the NameNode (heartbeats) |

### 🎯 The NameNode never touches your data

A client asks the NameNode *where* a block is and then reads it **directly
from the DataNode**. If every byte flowed through the NameNode it would be the
bottleneck of the entire cluster.

**This single fact answers a surprising number of exam questions**, including
"why can HDFS scale to thousands of nodes with one master?"

---

## 2.2 Blocks

### 🔢 The arithmetic, which is examined constantly

**Default block size: 128 MB** (64 MB before Hadoop 2, and older textbooks
still say 64).

| File | Blocks | Last block |
|---|---:|---:|
| 1 MB | **1** | 1 MB |
| 128 MB | **1** | 128 MB |
| 129 MB | **2** | 1 MB |
| 260 MB | **3** | **4 MB** |
| 1 GB | **8** | 128 MB |
| 5,000 MB | **40** | 8 MB |

*(Every row computed in `04_blocks_replication.py`.)*

### ⚠️ An HDFS block is a maximum, not an allocation

**260 MB is 128 + 128 + 4, not three 128 MB blocks.** The last block occupies
only what it needs, on the DataNode's ordinary local filesystem. **HDFS wastes
no space on block padding** — the opposite of what "block" suggests from
operating-systems courses, and the single most common mistake in this unit.

**But one byte past the boundary costs a whole block object.** 128 MB is one
block; 129 MB is two. The extra block costs almost no disk and **~150 bytes of
NameNode RAM**, which is the scarce resource.

### 🎯 Why 128 MB and not 4 KB

Two competing pressures:

- **Smaller blocks** → more blocks → more NameNode memory, more map tasks,
  more scheduling overhead.
- **Larger blocks** → fewer, longer map tasks → poor parallelism on a small
  file, and a failed task re-runs more work.

128 MB is chosen so that **seek time is about 1% of transfer time**. At a 10 ms
seek and 100 MB/s transfer, 100 MB takes 1 s to read and 10 ms to find: the
disk spends its life transferring, not seeking. That derivation is worth full
marks when asked "why is the block size so large?"

### ⚠️ The small-files problem

The NameNode holds the whole namespace in RAM, roughly **150 bytes per file,
directory and block object**:

| Scenario | Files | Blocks | NameNode RAM |
|---|---:|---:|---:|
| one 1 GB file | 1 | 8 | **0.00 MB** (1,350 bytes) |
| 1,000 × 1 MB | 1,000 | 1,000 | 0.29 MB |
| 1,000,000 × 1 KB | 1,000,000 | 1,000,000 | **286.10 MB** |

**The same gigabyte costs 1,350 bytes as one file and 286 MB as a million
small ones — a factor of 222,222.** HDFS was built for few large files, and
this table is the whole reason.

It also explains things that look unrelated: Flume's default rollover settings
(experiment 12), Hive's advice not to over-partition (experiment 10), and the
existence of HAR archives and SequenceFiles.

---

## 2.3 Replication and rack awareness

### 📖 The default policy, replication factor 3

| Replica | Where | Why |
|---|---|---|
| 1 | the **writer's own node** (or a random node if the writer is off-cluster) | free write |
| 2 | a node on a **different rack** | survives losing a rack |
| 3 | a **different node on replica 2's rack** | cheap — one cross-rack hop already paid |

### 🎯 Why two racks and not three

A third rack would **double the cross-rack write traffic** to protect against
losing *two* racks — which is far rarer than losing one. Cross-rack bandwidth
is the scarce resource in a datacentre, so the policy buys the important
guarantee and stops.

**Measured**, on a 1 GB file over 6 DataNodes in 2 racks
(`05_fault_tolerance.py`):

| Failure | Blocks lost |
|---|---:|
| 1 DataNode | **0** |
| 2 DataNodes | **0** |
| a whole rack (3 nodes) | **0** |
| 3 DataNodes *straddling both racks* | **2** |

### 🔢 The honest version of "replication 3 survives 2 failures"

By brute force over every combination:

| Nodes down | Combinations losing data |
|---:|---|
| 1 | **0 of 6** |
| 2 | **0 of 15** |
| 3 | **6 of 20** |
| 4 | 12 of 15 |
| 5 | 6 of 6 |

**Any two failures are survivable. Only *some* threes are fatal** — 14 of the
20 three-node combinations still lose nothing, because a whole rack going down
is one of the safe cases. "Replication R tolerates R−1 arbitrary failures" is
the correct statement; "it fails at 3 nodes" is the worst case, not the rule.

### 💡 The storage cost, and its alternative

| Scheme | 1 GB of data occupies | Overhead |
|---|---:|---:|
| replication 3 | **3,072 MB** | 200% |
| erasure coding RS-6-3 | **1,536 MB** | **50%** |

Erasure coding (HDFS 3.0+) gives comparable durability for a quarter of the
overhead, and costs expensive **reconstruction reads** when a block is missing
— you must read six blocks to rebuild one. So it is used for **cold** data and
replication for hot. That trade is a good five-mark answer.

---

## 2.4 HDFS file operations — the read and write paths

Two paths, and the design decision in each is the examinable part.

### The write path

```
1. Client → NameNode:  create /user/x/f.dat
2. NameNode: checks permissions, checks it does not exist,
             records it in the edit log, returns the DataNode PIPELINE
3. Client → DN1 → DN2 → DN3        (a PIPELINE, not three parallel sends)
   data flows in 64 KB packets, each node forwarding as it receives
4. acknowledgements travel BACK up the pipeline
5. Client → NameNode:  complete
```

### 🎯 Why a pipeline and not three copies from the client

If the client sent three copies, its **upload bandwidth would be the
bottleneck** and would carry 3× the data. In a pipeline the client sends once,
and each DataNode forwards while receiving. **Total time is roughly one
transfer, not three.**

If a DataNode in the pipeline dies mid-write, it is removed, the write
continues with the survivors, and the NameNode re-replicates later. **The
client sees no error.**

### The read path

```
1. Client → NameNode:  open /user/x/f.dat
2. NameNode returns, for EACH block, the DataNodes holding it,
   SORTED BY NETWORK DISTANCE from the client
3. Client reads each block DIRECTLY from the nearest DataNode
4. Checksum verified; on mismatch, the next replica is tried and the
   NameNode is told the block is corrupt
```

**The sorting in step 2 is data locality doing its work** — the client
transparently reads from the closest copy.

### ⚠️ HDFS is write-once, append-only

There is **no random write and no `cd`**. To change one byte you rewrite the
file. That constraint is what lets HDFS drop file locking and distributed
write coordination entirely — and it is why **HBase exists** (Unit 5), because
some workloads genuinely need to update a row.

---

## 2.5 Fault tolerance

### DataNode failure

| Step | Timing |
|---|---|
| heartbeat interval | **3 s** |
| declared dead after | 10 × 3 s + 2 × 5 min = **630 s** (10 min 30 s) |
| blocks marked under-replicated | immediately after |
| re-replication | scheduled from surviving replicas |

### 🎯 Why the 10-minute delay is deliberate

A node that reboots in five minutes should **not** trigger a cluster-wide copy
storm. HDFS trades a longer window of reduced redundancy for far less needless
network traffic — and on a large cluster the copy storm is genuinely worse
than the risk.

### NameNode failure — a different kind of problem

| What it holds | Where | Survives a crash? |
|---|---|---|
| `fsimage` — the namespace at a checkpoint | disk | **yes** |
| `edits` — changes since the checkpoint | disk | **yes** |
| the **block map** — block → DataNode locations | **RAM only** | **NO** |

**The block map is never persisted.** It is rebuilt from DataNode block
reports at startup, which is why a large NameNode takes minutes to leave
**safe mode**. The namespace survives; the *locations* are reconstructed.

### ⚠️ The Secondary NameNode is not a backup

**The worst-named component in Hadoop.** It periodically merges `fsimage` with
`edits` so that restarts stay fast — and **it cannot take over**. A student who
says "the Secondary NameNode takes over" has lost the mark.

| Mechanism | Recovers | Automatic? |
|---|---|---|
| **Secondary NameNode** | checkpoint only | **no — not a standby** |
| **NameNode HA** (two NameNodes) | full | yes, via **ZooKeeper** |
| **HDFS Federation** | — scales the namespace | — |

HA needs two NameNodes, a shared edit log (the **Quorum Journal Manager**) and
**ZooKeeper** for failover — which is why experiment 16 exists and why Unit 5
matters.

---

## 2.6 YARN architecture

### 📖 The four pieces

| Component | One per | Responsibility |
|---|---|---|
| **ResourceManager** | **cluster** | global scheduling; hands out containers |
| **NodeManager** | **node** | launches and monitors containers, reports health |
| **ApplicationMaster** | **JOB** | negotiates containers, retries failed tasks |
| **Container** | **task** | a bounded slice of CPU and RAM on one node |

### 🎯 One ApplicationMaster per job — the change that defined YARN

In Hadoop 1, a single **JobTracker** did both cluster scheduling *and*
per-job management for every job. It was simultaneously the **bottleneck** and
the **single point of failure**, and it could only run MapReduce.

YARN split those two responsibilities:

- the **ResourceManager** does scheduling only, for the whole cluster
- an **ApplicationMaster** does job management, one per job, running *inside a
  container* like any other task

**That split is why YARN can run Spark, Tez and Flink** and not only
MapReduce. If a question asks "what is the difference between Hadoop 1 and
Hadoop 2", this is the answer.

### Application scheduling — the submission sequence

```
1. Client → RM:              submit application
2. RM → a NodeManager:       launch the ApplicationMaster container
3. AM  → RM:                 register, then request N containers
                             (with locality preferences)
4. RM → AM:                  here are containers on nodes n3, n7, n9
5. AM  → NodeManagers:       launch my tasks in them
6. tasks → AM:               progress and heartbeats
7. AM  → RM:                 unregister; RM reclaims everything
```

**Step 3 is where data locality enters**: the AM asks for containers *on the
nodes holding its blocks*, and the RM honours the preference when it can.

---

## 2.7 The three schedulers

Measured on one workload — an 8-container cluster, four jobs, `big_etl`
needing the whole cluster for 10 s
(`06_yarn_scheduling.py`):

| Job | FIFO turnaround | Fair turnaround |
|---|---:|---:|
| `big_etl` | **10** | 14 |
| `small_q1` | **11** | **1** |
| `small_q2` | 12 | 1 |
| `medium` | 16 | 5 |
| **total** | **49** | **21** |

### 🔢 What those numbers actually say

**`small_q1` needs one container for two seconds and waits eleven under
FIFO** — head-of-line blocking, and the reason nobody runs FIFO on a shared
cluster.

**The work is identical either way: 104 container-seconds**, which on 8
containers cannot finish before second 13. Fair sharing did not make the
cluster faster — `big_etl` finished *later*, 10 → 14 — it moved latency from
the small jobs to the big one.

**Total turnaround still halved, 49 → 21**, because FIFO made three jobs sit
idle in a queue. Scheduling cannot create throughput, but idle-while-queued is
real waste.

### The three, compared

| | **FIFO** | **Fair** | **Capacity** |
|---|---|---|---|
| Idea | first come, first served | equal share among running jobs | queues with guaranteed % |
| Small job behind a big one | **waits** | runs now | runs now, if its queue has room |
| Guarantees | none | eventual fairness | **a hard minimum per queue** |
| Idle capacity | used | used | **wasted unless elasticity is on** |
| Typical user | nobody | Facebook (its origin) | Yahoo (its origin), most enterprises |
| Default in | very old Hadoop | CDH | **Apache Hadoop 3, HDP** |

**Capacity Scheduler, production 75% / adhoc 25%:** the adhoc queue holds 2
containers whatever else is running, so a short query has a **guarantee**
rather than a hope. The cost is that those 2 containers sit idle when adhoc is
empty — unless `maximum-capacity` is raised above `capacity` to allow
**elasticity**, which is precisely the difference between "capacity" and
"fair".

---

## Practice problems

**1. A 700 MB file is stored with the default block size and replication 3.
How many blocks, how much disk, and how many block objects in NameNode RAM?**

- Blocks: ⌈700 / 128⌉ = **6** (128 × 5 = 640, last block **60 MB**)
- Disk: 700 × 3 = **2,100 MB**
- Block objects in RAM: 6 × 3 = **18 replicas**, but the NameNode holds **one
  block object with three locations**, so **6 objects** plus 1 file object ≈
  **7 × 150 = 1,050 bytes**.

**The trap:** disk multiplies by the replication factor; NameNode *metadata*
does not.

**2. Why does HDFS not simply use a 4 KB block like a normal filesystem?**

Two reasons, and give both:

- **Metadata.** A 1 TB file at 4 KB is 268 million blocks × 150 bytes ≈ **40 GB
  of NameNode RAM for one file.**
- **Seek time.** At 10 ms seek and 100 MB/s, a 4 KB read is 99.99% seek. A
  128 MB block makes seek ~1% of the transfer, so the disk transfers instead
  of seeking.

**3. Your cluster has 8 DataNodes in 2 racks. Rack 2 loses power. What
happens, in order?**

1. **Reads and writes continue immediately.** Every block has a replica on
   rack 1 by policy, so nothing is unavailable.
2. After **630 s** the four nodes are declared dead.
3. Every block is now **under-replicated** (1 or 2 of 3).
4. The NameNode schedules re-replication from the survivors — **onto rack 1**,
   since it is the only rack up. Cross-rack placement is impossible and HDFS
   accepts that rather than refusing.
5. When rack 2 returns, blocks are **over-replicated**, and the NameNode
   deletes excess replicas, preferring to keep the rack spread.

**The subtle point:** during step 4 the cluster is genuinely less safe, and
network and disk are saturated by the copying. This is why rack failures are
operationally worse than the "no data loss" headline suggests.

**4. Explain why an ApplicationMaster runs in a container rather than on the
ResourceManager.**

Because a per-job manager on the RM is exactly what Hadoop 1 did, and it made
the JobTracker the bottleneck. Putting the AM in a container means:

- the RM's work per job is **constant** — one container allocation — so it
  scales to thousands of concurrent jobs
- an AM crash kills **one job**, not the cluster
- each framework ships **its own** AM, so YARN needs to know nothing about
  MapReduce, Spark or Flink

**5. A job's map phase finishes in 2 minutes but the job takes 40. Where do you
look, and why?**

**The reduce phase, and specifically skew.** The likely causes in order:

1. **Key skew** — one reducer holds most of the records. In word count that
   is `the`. Check the per-reducer counters.
2. **Too few reducers** — the default is often 1.
3. **No combiner** where one is safe, so the shuffle is moving far more data
   than necessary.

**The job's wall clock is its slowest reducer**, so a perfectly parallel map
phase tells you nothing about the total. Skew, not volume, is what usually
kills a MapReduce job.

---

## Exam questions from this unit

**Two marks**

1. What is the default HDFS block size?
2. How many blocks does a 260 MB file occupy?
3. What does the NameNode keep in RAM that it never writes to disk?
4. What is the Secondary NameNode for?
5. How long before a DataNode is declared dead, and why so long?
6. Name the four YARN components.
7. What is a container?
8. Which scheduler guarantees a queue a minimum share?

**Five marks**

1. Explain the HDFS write path, including the pipeline.
2. Explain the default replica placement policy and justify two racks.
3. Explain the small-files problem with figures.
4. Compare the three YARN schedulers.
5. Explain what happens when a NameNode restarts, and why it takes minutes.

**Ten marks**

1. Describe HDFS architecture in full — blocks, NameNode, DataNodes, the read
   and write paths, replication and fault tolerance — with a diagram.
2. Explain YARN's architecture and the submission sequence, and say what
   problem it solved relative to Hadoop 1.

---

## Mistakes that cost marks

- **Saying a 260 MB file occupies 384 MB.** The last block is short.
- **Multiplying NameNode metadata by the replication factor.** Disk multiplies;
  metadata does not.
- **Calling the Secondary NameNode a standby.** It is a checkpointer.
- **Saying the NameNode stores block locations on disk.** It does not — they
  are rebuilt from block reports, and that is why safe mode exists.
- **Describing the write as three parallel copies from the client.** It is a
  pipeline, and the reason is the client's upload bandwidth.
- **Claiming replication 3 "fails at 3 node failures".** It survives *any* two;
  only some threes are fatal, and a whole-rack failure is one of the safe cases.
- **Confusing the ResourceManager with the ApplicationMaster.** One per
  cluster, one per job — and the split is the whole point of YARN.
- **Saying Fair Scheduling makes the cluster faster.** It moves latency; the
  container-seconds of work are identical.
