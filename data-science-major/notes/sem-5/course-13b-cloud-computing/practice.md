# Course 13 B — Practice Questions with Worked Solutions

Every figure quoted here is produced by
`labs/course-13b-cloud/` and checked by
`tools/run_cloud_labs.py`.

---

## Section A — Two-mark questions

**1. State the NIST definition of cloud computing.**
On-demand network access to a shared pool of configurable computing resources
that can be **rapidly provisioned and released** with minimal management
effort.

**2. Name the five essential characteristics.**
On-demand self-service, broad network access, resource pooling, rapid
elasticity, measured service.

**3. Distinguish elasticity from scalability.**
Scalability is *can it get bigger*. **Elasticity is can it get bigger and then
smaller again, automatically.** The test: what does it cost when nobody is
using it?

**4. What is utility computing?**
Compute billed as a metered utility, like electricity. **The cloud is utility
computing that finally worked**, because virtualization made the meter
fine-grained.

**5. Give one difference between grid and cloud computing.**
**A grid shares work; a cloud sells capacity.**

**6. Expand IaaS, PaaS, SaaS, and give the boundary.**
Infrastructure, Platform, Software as a Service. **The boundary is where "you
manage it" stops** — IaaS at the OS, PaaS at the runtime, SaaS at the
application.

**7. Which service model has the worst lock-in?**
**PaaS.** Your code targets their runtime, build system and scaling
semantics. Moving a VM is a disk image; moving a PaaS app is a rewrite.

**8. Distinguish type 1 from type 2 hypervisors.**
Type 1 runs **on the hardware** (ESXi, KVM, Nitro — the cloud). Type 2 runs
**on a host OS** (VirtualBox, VMware Workstation).

**9. Give one difference between a VM and a container.**
A VM virtualizes **hardware** and has its own kernel; a container virtualizes
**the OS** and shares the host kernel.

**10. Why can CPU be overcommitted more safely than memory?**
CPU is **time-sliced** and degrades gracefully; a memory page is either
resident or on disk, so memory overcommit **fails as a cliff**.

**11. Name the six types of virtualization.**
Server, storage, network, desktop, application, data.

**12. What is a VPC, in virtualization terms?**
**Network virtualization** — a private network over shared physical switches.
It is what makes multi-tenancy safe.

**13. Name the four deployment models.**
Public, private, community, hybrid.

**14. Does "private cloud" mean on-premises?**
**No.** It means **single-tenant**. AWS Outposts and dedicated hosts are
private clouds in someone else's building.

**15. Name the three cloud storage types.**
Block (EBS), file (EFS), object (S3).

**16. Which has no directories?**
**Object storage.** `raw/2026/sales.csv` is one key with two slashes; the
folder tree is **common prefixes computed at list time**.

**17. Why is there no rename in an object store?**
**The key is the identity.** A rename is a **copy plus a delete** — a full
read and a full write.

**18. What is the minimum billing duration for Glacier Deep Archive?**
**180 days.** Delete after 10 and you are billed for 180.

**19. Is ingress or egress charged?**
**Egress.** Ingress is free.

**20. How much does 1 TB of egress cost, relative to storing it?**
**$92.16 — as much as storing that terabyte for 3.9 months.**

**21. What does a delete do to a versioned S3 object?**
Writes a **delete marker**. The data is still there and **still billed**.

**22. State RPO and RTO.**
**RPO** — how much data you can afford to lose. **RTO** — how long you can
afford to be down.

**23. Name one limitation of a key-value database.**
**No query by value** without a secondary index — any query not beginning with
the partition key is a full scan.

**24. Give one difference between a cloud data warehouse and an RDBMS.**
**Columnar, indexless, and billed on bytes scanned** rather than on the box.

**25. What is BigQuery billed on?**
**Bytes scanned** — $6.25 per TB on demand.

**26. Does `LIMIT 10` make a BigQuery query cheap?**
**No.** It limits rows *returned*, not bytes *scanned*.

**27. Why did ELT replace ETL?**
**Warehouse compute got cheap and elastic.** Landing raw data means a bug is
fixed by re-running SQL, not by re-extracting from a source that may have
changed.

**28. State IAM's three evaluation rules.**
1. An **explicit deny** anywhere wins. 2. Otherwise an **allow** grants.
3. Otherwise **implicit deny**.

**29. Does adding an `s3:*` allow policy defeat an existing deny?**
**No.** Verified: still denied. There is **no "more specific allow wins"
rule**.

**30. Does IAM policy order matter?**
**No.** Unlike a firewall list, it is not first-match — every statement is
evaluated, then the three rules decide.

**31. Give one difference between an IAM user and a role.**
A user has **long-lived credentials**; a role provides **temporary,
auto-rotated** ones and is assumed by a service.

**32. Why does a SageMaker notebook not need an access key?**
It has an **execution role attached**, so no credential is ever written to
disk.

**33. What do AIaaS and GPUaaS actually mean?**
**SaaS for a model** and **IaaS for a GPU**. They are not new service models.

**34. What is a feature store for?**
**One definition of a feature, served to training and serving** — it prevents
training/serving skew.

**35. What does AutoML actually do?**
Fits many models, cross-validates each, and **ranks them**. It is a search.

**36. Name two things AutoML cannot do.**
Notice that your target leaks; choose a threshold fitting the business cost of
an error. (Also: decide the target, explain a prediction, notice unfairness.)

**37. Distinguish scale-up from scale-out.**
**Up** = a bigger machine, no code changes, near-perfect efficiency.
**Out** = more machines, distributed code, sub-linear returns.

**38. What must `/ping` not do?**
**Run the model.** A health check doing real inference kills healthy
containers whenever the model is merely slow.

**39. Why alarm on p99 rather than the mean?**
Measured: twenty latencies with one 900 ms outlier gave a **mean of 85 ms and
a p99 of 737.5 ms**. The mean never fires.

**40. Name the metric that catches a dead endpoint.**
**`Invocations == 0`** for an hour. Every performance metric looks perfect and
it still bills.

**41. Distinguish data drift from concept drift.**
**Data drift** — the input distribution changed. **Concept drift** — the
relationship between input and output changed.

**42. Name the three deployment shapes and their idle cost.**
Real-time (**the full instance**), serverless (**zero**), batch (**zero**).

**43. What does an `ml.m5.large` endpoint cost when nothing calls it?**
About **$70/month**.

**44. Why is a 4xx not a 5xx?**
**5xx means your service is broken and should page someone.** Returning 500
for malformed input poisons your error alarm.

**45. Give the measured cost of calling an endpoint per row.**
**37×** — 181.85 ms for 100 single-row requests against 4.90 ms for one
batched request.

---

## Section B — Five-mark questions

### 1. Explain the five essential characteristics, with a failure mode for each

| Characteristic | Fails when |
|---|---|
| **On-demand self-service** | provisioning goes through a ticket queue |
| **Broad network access** | it needs a special client |
| **Resource pooling** | the hardware is dedicated to you |
| **Rapid elasticity** | you can add nodes but not remove them |
| **Measured service** | it is a flat monthly fee |

**Use them as a test, which is what they are for.** A virtualized datacentre
where developers raise a ticket and wait two days has resource pooling and
nothing else. **It is a virtualized datacentre, which is useful, and calling
it a private cloud is marketing.**

**And elasticity is the one most often misread:** it includes scaling *in*. A
system that scales out and never back in has scalability without elasticity,
and it costs you the peak at 3 a.m.

### 2. Compare IaaS, PaaS and SaaS by what the customer manages

| Layer | On-prem | IaaS | PaaS | SaaS |
|---|---|---|---|---|
| Application | you | you | **you** | provider |
| Data | you | you | **you** | provider |
| Runtime | you | you | provider | provider |
| **OS** | you | **you** | provider | provider |
| Virtualization ↓ | you | provider | provider | provider |

**Read the table by finding where "you" stops.** IaaS gives a machine and you
patch it; PaaS gives a runtime and you deploy code; SaaS gives an application.

**And the counter-intuitive part:** lock-in is worst at **PaaS**, the middle
option — because your code targets their runtime, their build and their
scaling model. **Moving a VM is a disk image; moving a PaaS application is a
rewrite.**

### 3. Explain overcommitment and the CPU/memory asymmetry

**Overcommit** is allocating more virtual resource than the host physically
has, betting that guests will not all use their allocation at once.

**Measured, on a 32 GB / 8 vCPU host with four guests:**

```
allocated RAM  : 48 GB  (1.50x)      allocated vCPU : 20 on 8  (2.50x)
RAM actually touched : 22.8 GB       swapping : 0.0 GB
```

**Then one guest goes from 20% to 95% active:**

```
RAM actually touched : 34.8 GB       swapping : 2.8 GB
```

**And now every guest is slow, not just the greedy one.**

**The asymmetry:** a vCPU is a *scheduling entity*, so 4:1 means everyone runs
at a quarter speed — **linear and graceful**. A memory page is either resident
or on disk, and a swapped page costs roughly 100,000× a resident one — **a
cliff**.

**That is the "noisy neighbour" problem**, and it is why cloud instance types
quote **dedicated memory** and only **burstable CPU**.

### 4. Explain the three storage types and how to choose

| | **Block** | **File** | **Object** |
|---|---|---|---|
| Access unit | a 512 B block | a file or byte range | **a whole object** |
| Attached to | **one instance** | **many** | anything |
| In-place edit | yes | yes | **no** |
| $/GB-month | 0.080 | **0.30** | **0.023** |

**Measured, per terabyte per month:** EFS **$307.20**, EBS **$81.92**, S3
**$23.55**. **EFS costs 13× S3** — worth it precisely when several instances
must share a POSIX filesystem, and a mistake for a dataset one job reads once.

**And provisioned against consumed:** a 1 TB EBS volume holding 200 GB bills
**$81.92** against S3's **$4.60** — a factor of **18**, because EBS bills the
volume you asked for.

> **Choose by access pattern, not price:** block for a database or boot disk,
> file for shared POSIX, object for everything a pipeline reads.

### 5. Explain S3 storage classes and the trap in the cheap tiers

**1 TB for a year, retrieved once:**

| Class | Total | Min days |
|---|---:|---:|
| Standard | $282.62 | 0 |
| Standard-IA | $163.84 | 30 |
| **Deep Archive** | **$32.65** | **180** |

**Read the two ratios separately.** Deep Archive **storage** is **23×**
cheaper; add one retrieval and the all-in saving is **8.7×**, because the
retrieval fee ($20.48) exceeds a year of its storage ($12.17). **The headline
discount is not the discount.**

**And the reversal — the same TB retrieved twice a month:**

| Class | Total/yr |
|---|---:|
| **Standard** | **$282.62** |
| Standard-IA | $399.36 |
| Glacier Instant | $786.43 |

**Standard is now cheapest.** *"We moved everything to IA to save money" is
how a bill goes up.*

**Plus the minimum durations**: delete a Deep Archive object after 10 days and
you are billed for 180. **A storage class is a bet on your access pattern, and
the penalties are what make it a bet.**

### 6. Explain IAM's evaluation algorithm

**Three rules, in order:**

1. **An explicit `Deny` anywhere wins.** Always, unconditionally.
2. Otherwise, a matching **`Allow`** grants access.
3. Otherwise, **deny** — the implicit deny, which is why a new principal can
   do nothing.

**Verified against a realistic policy set:**

| Action | Resource | Result |
|---|---|---|
| `s3:GetObject` | `retail-lake/raw/…` | **Allow** |
| `s3:PutObject` | `retail-lake/raw/…` | **Deny** — explicit |
| `s3:PutObject` | `retail-lake/models/…` | **Allow** |
| `s3:GetObject` | `other-bucket/…` | **Deny** — implicit |

**Rows 2 and 3 together are the lesson:** a Deny scoped to one prefix beats an
Allow scoped to the bucket. **That is how a data lake keeps a raw zone
immutable.**

**And the demonstration that matters:** attach a policy granting `s3:*` on
`*`, and `s3:PutObject` on `raw/` is **still denied**. There is **no "more
specific allow wins" rule**; to lift a Deny you must remove it.

**Policy order is irrelevant** — reversed, the answer is identical. IAM is not
first-match.

### 7. Explain batch against streaming for an ML pipeline

| | Batch | Streaming |
|---|---|---|
| Completeness | a whole period | **whatever has landed** |
| **Late data** | **impossible** | **normal** |
| Re-runnable | **yes** | no |
| Failure means | re-run | **a gap** |

**"Late data is normal" is the row that changes the design.** A streaming
aggregate for 09:00 is not final at 10:00, so either you accept eventual
correctness or you keep a **watermark** and re-emit.

**The batch leg has no such problem, which is exactly why Lambda keeps
both** — and why **Kappa** removes the batch layer by making the stream
replayable. **Lambda's real cost is the same rule living in two codebases and
drifting.**

**And the failure with no error message:** training on batch and serving on
streaming produces **training/serving skew** — the model sees a feature
distribution it never trained on, and every metric stays green. **A feature
store exists for exactly this.**

### 8. Explain why autoscaling can cost more than fixed capacity

**Measured**, over a day with peak 1,000 req/s and instances serving 150:

| Strategy | Instance-hours | Dropped |
|---|---:|---:|
| fixed at peak (7) | 168 | **0** |
| autoscaled 70%/40%, cooldown 1 | **129** | **1,014** |
| autoscaled 50%/30%, **no cooldown** | **188** | **0** |

**The third row costs 12% MORE than fixed capacity while dropping nothing.**

**The mechanism:** a scaling decision takes effect one observation late, so
the group **overshoots on the way up** and, with a short scale-in cooldown,
**oscillates** rather than settling. You buy more than the peak, plus every
extra instance's boot time.

> **Autoscaling does not track demand. It chases demand, always one
> observation behind.**

**"Autoscaling saves money" is a claim about a *tuned* autoscaler.** The fix
is a higher scale-out threshold, a longer scale-in cooldown, a capped
maximum — and measuring, because the curve is specific to your traffic.

---

## Section C — Ten-mark questions

### 1. Explain cloud storage in full, with worked arithmetic

**The three types, by access unit:**

| | Block (EBS) | File (EFS) | Object (S3) |
|---|---|---|---|
| Looks like | a raw disk | a filesystem | **an HTTP API** |
| Attached to | one instance | many | anything |
| In-place edit | yes | yes | **no** |
| Directories | the FS's | real | **none — prefixes** |
| $/GB-month | 0.080 | **0.30** | **0.023** |
| Billed on | **provisioned** | used | **used** |

**Per terabyte per month: EFS $307.20, EBS $81.92, S3 $23.55.** EFS is 13× S3
and earns it only when several instances share a POSIX filesystem. And a 1 TB
EBS volume holding 200 GB bills **$81.92** against S3's **$4.60** — because
EBS bills what you asked for.

**Object storage has no directories.** `raw/2026/01/sales.csv` is one key with
three slashes; a listing with a delimiter returns **common prefixes** computed
at list time. **A prefix scan is the only query it supports** — no `WHERE`, no
index.

**And no rename.** Measured: a rename read 1,024 bytes, wrote 1,024 and made
2 API calls. At 5 TB that is 10 TB moved for a tidier folder name.

**Storage classes are a bet on access frequency:**

| | Retrieved once/yr | Retrieved 2×/month |
|---|---:|---:|
| Standard | $282.62 | **$282.62** |
| Standard-IA | **$163.84** | $399.36 |
| Deep Archive | **$32.65** | — |

**Standard wins outright at two retrievals a month**, because the "cheap"
tiers charge per GB retrieved. And Deep Archive's 23× *storage* discount
becomes **8.7×** all-in after one retrieval, with a **180-day minimum** and a
12-hour restore.

**Egress is the line nobody predicts:** 1 TB in is **free**; 1 TB out is
**$92.16**, or **3.9 months of storing it**. **That asymmetry is the mechanism
behind lock-in** — your data is not held hostage, it is simply expensive to
move — and it is why "move the compute to the data" survived into the cloud.

**Use cases follow from the arithmetic:** backup → IA with a lifecycle to
Glacier; archive → Deep Archive; DR → cross-region replication with a tested
restore; content delivery → CDN, where **cheaper egress, not latency, is the
real saving**.

### 2. Explain the full lifecycle of training and deploying a model on the cloud

**The six steps, and what goes wrong at each.**

**1. Identify the data.** Find where it already lives — moving data is the
expensive part. Check freshness, access (an **IAM role, not keys**), and
legality. **And ask whether a label exists**: many "ML projects" are really
"label 50,000 examples first" projects, and finding that out in week six is
expensive.

**2. Feature engineering.** Compute features **where the data is** — a
`GROUP BY` in the warehouse beats exporting a terabyte. Use a feature store,
because the alternative is training/serving skew. **And this is where leakage
happens**: a feature computed from a table already containing the outcome
scores brilliantly and fails in production, with no error message.

**3. Training.** The job is declarative. **Three conventions are the whole
interface:** hyperparameters as arguments, channels as environment variables,
and **the model written to `SM_MODEL_DIR`** — get the last wrong and the job
"succeeds" with no artefact. Spot training is up to 70% cheaper, and
**without `checkpoint_s3_uri` an interruption restarts from zero**.

**And instance choice is answered by the algorithm:**

| Instance | 10-min job |
|---|---:|
| m5.xlarge | **$0.0320** |
| p4d.24xlarge (8 GPU) | **$5.4621** |

**171× — and gradient boosting on tabular data has no GPU code path.**

**4. Validation.** Everything from Course 12 A. **Quote the dummy:**

| Model | Accuracy | F1 |
|---|---:|---:|
| `DummyClassifier` | **0.8433** | **0.0000** |
| GradientBoosting | 0.9467 | 0.8095 |

**94.67% is 10.3 points over a dummy**, and the F1 is what shows anything was
learned.

**5. Deployment.** The artefact — 138,945 bytes here — is the deliverable.
**The endpoint's predictions must be identical to the model in-process**, and
that equality is the test worth writing. `/ping` must **not** run the model.
Malformed input must be **4xx, not 5xx**, or your error alarm fires for other
people's bugs.

**Choose the shape from the duty cycle:**

| | Idle cost |
|---|---|
| Real-time | **the full instance — ~$70/month** |
| Serverless | **zero** |
| Batch transform | **zero** |

**And measured: 100 single-row requests took 37× one batched request**, none
of it the model. Scoring a file through an endpoint is the expensive way to
do arithmetic.

**6. Monitoring.** Alarm on **p99, not the mean** — twenty latencies with one
900 ms outlier gave a mean of 85 ms and a p99 of 737.5 ms. Alarm on **5xx**,
on **spend**, and on **`Invocations == 0`**, because a dead endpoint looks
perfect and bills the same.

**Then retrain**, triggered by schedule, drift or performance — as a
**pipeline, not a person**, promoted through a champion/challenger gate and a
canary.

### 3. Compare a cloud data warehouse with an RDBMS, and work out the break-even

| | **RDBMS (Course 5)** | **Cloud DW** |
|---|---|---|
| Layout | **row** | **columnar** |
| Workload | many small transactions | **few huge scans** |
| Indexes | central | **usually none** |
| Scaling | a bigger box | nodes, or serverless |
| Compute & storage | coupled | **separated** |
| Billed on | the box | **bytes scanned** or node-hours |
| A bad query costs | time | **time and money** |

**The last row is what is new.** BigQuery at $6.25/TB scanned:

| Query | TB | Cost |
|---|---:|---:|
| `SELECT * FROM events` | 10.00 | **$62.50** |
| `SELECT user_id …` | 0.40 | $2.50 |
| `SELECT user_id … WHERE dt = '…'` | 0.02 | **$0.12** |

**The same question, 500× the price** — column projection and partition
pruning, which are **Course 12 B's techniques saving money instead of time**.
That is why `SELECT *` is a billing incident on serverless and merely rude on
a server you own. **And `LIMIT 10` does not help**: it limits rows returned,
not bytes scanned.

**Redshift at $1.086/node-hour: 2 nodes is $1,585.56/month.**

$$\text{break-even} = \frac{1585.56}{6.25} \approx \textbf{254 TB scanned per month}$$

**Below it**, on-demand is cheaper and costs nothing when idle. **Above it**,
the cluster is cheaper and an extra query is free at the margin.

**And four non-price reasons for provisioned:** predictable spend; no
per-query blast radius; sustained concurrent dashboard load; data locality
with the rest of the estate. **The counter:** a spiky workload pays nothing
during quiet weeks on serverless and the full rate every hour on a cluster.

**ELT replaced ETL** because warehouse compute got cheap and elastic — a
transformation bug is then fixed by re-running SQL on raw data rather than
re-extracting from a source that may no longer hold the old rows, **exactly
the `DELETE` problem Course 12 B found in Sqoop.**

### 4. Design a secure, cost-controlled cloud setup for a student data-science team

**Identity, first.**

1. **MFA on root, then never use root.** Create IAM users, or better, federate
   with the college's identity provider.
2. **Roles, not keys.** Notebooks get an execution role; nothing writes an
   access key to disk. `git` history is where access keys go to be found.
3. **Least privilege, scoped by prefix.** The measured comparison: a `*:*`
   policy and a two-statement scoped policy both let the training job run, but
   only one also permits `iam:CreateUser` and `ec2:TerminateInstances`.
4. **A `Deny` on the raw zone**, which cannot be defeated by any later Allow —
   demonstrated: adding full S3 admin left `s3:PutObject` on `raw/` still
   denied.

**Cost control, second, and on day one.**

1. **A budget alarm** at 50%, 80%, 100%.
2. **`EstimatedCharges`** alarm — remembering it lives only in `us-east-1` and
   lags about six hours.
3. **`Invocations == 0`** on every endpoint — a dead endpoint bills $70/month
   and looks perfect on every performance metric.
4. **Idle-shutdown lifecycle policies** on notebooks. An m5.xlarge left
   running is ~$140/month.
5. **Lifecycle rules** on every versioned bucket, including
   `AbortIncompleteMultipartUpload` — abandoned parts are invisible in
   `s3 ls` and billed for ever.
6. **Tag everything** by student and project, so Cost Explorer can attribute
   spend.

**Storage, third.**

- **Raw data → S3**, partitioned, Parquet, with a lifecycle to IA at 30 days.
- **Not EFS**, unless several instances genuinely share a POSIX filesystem —
  13× S3 for a feature nobody is using.
- **One region**, so nothing bills invisibly elsewhere and no cross-region
  egress appears.

**Compute, fourth.**

- **Spot for training** with checkpoints; **on-demand for anything
  interactive**.
- **Instance chosen by the algorithm**, not ambition — 171× for the same
  speed is the figure to quote.
- **A weekly sweep**: `describe-instances`, `s3 ls`, `list-endpoints`. Nothing
  else in the course saves as much money.

**And the operational rule that matters most:** **nothing you forget to
switch off will switch itself off.**

### 5. Explain virtualization and the four deployment models, with a recommendation

**Virtualization is what makes the cloud possible**, because you cannot hand
back half a physical server. A hypervisor gives three properties:

- **Partitioning** — one machine, many isolated guests → multi-tenancy
- **Isolation** — a breach in one does not reach another → you can sell to
  strangers
- **Encapsulation** — **a whole machine is a file** → snapshots, cloning, live
  migration, images

**Encapsulation is the underrated one.** An AMI is a file, which is why an EC2
instance starts in forty seconds.

**Type 1 (ESXi, KVM, Nitro) runs on the hardware and is what the cloud uses;
type 2 (VirtualBox) runs on a host OS.** Containers are a third thing: they
virtualize **the OS**, share the kernel, start in milliseconds and isolate
less. **Providers run containers inside VMs** to get both.

**Overcommit, measured:** 48 GB allocated on a 32 GB host ran with zero
swapping at 22.8 GB touched, and began swapping 2.8 GB when one guest went
from 20% to 95% active — **slowing every guest, not just the greedy one**.
**CPU degrades gracefully; memory falls off a cliff.**

**The four deployment models:**

| | Public | Private | Community | Hybrid |
|---|---|---|---|---|
| Tenancy | shared | **single** | a defined group | both |
| Cost | operational | **capital** | shared capital | both |
| Elasticity | unlimited | bounded | bounded | burst |

**Private means single-tenant, not on-premises.**

**Recommendations:**

- **A bank** — **hybrid**. Identifiable customer data and the core ledger stay
  private, for residency and audit; analytics and development run public. The
  hard part is **data gravity**: a design that moves terabytes across the
  boundary daily is expensive in a way the diagram hides.
- **A university** — **public, plus a community cloud** where one exists for
  research data with shared compliance requirements. Teaching workloads are
  bursty and seasonal, which is exactly the elasticity argument.
- **A startup** — **public, entirely.** There is no capital to spend, no
  operations team, and the requirement is to move fast and stop paying for
  what fails. A private cloud for a startup is a capital purchase in place of
  a product.

---

## The six things most likely to be examined

1. **IAM's three rules**, and the demonstration that adding `s3:*` does not
   defeat an explicit Deny.
2. **The storage-class reversal.** Standard beats both IA tiers at two
   retrievals a month; Deep Archive's 23× becomes 8.7× after one retrieval.
3. **Egress: 1 TB out = 3.9 months of storing it** — data gravity and lock-in
   in one figure.
4. **The 500× BigQuery difference**, and the **254 TB** serverless/provisioned
   break-even.
5. **"Autoscaling made it more expensive"** — 188 instance-hours against 168.
   The measured result that contradicts the slogan.
6. **The dummy at 84.33%**, and **171× for the same training speed.** The
   cloud changes the packaging, not the algorithm.
