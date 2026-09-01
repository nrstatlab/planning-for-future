# Course 13 B — Practical Lab

**15 experiments**

Code lives in `labs/course-13b-cloud/`.

## Read this before you read anything else

> **There is no cloud account for this repository, and none will be created.**

Signing up for AWS, Azure or GCP requires a payment card and accepts a
billing relationship. That is not a thing a study repository should do on
anyone's behalf, so **no provider was ever contacted** and no claim in these
notes about a provider's behaviour was demonstrated here.

| Half | Files | Status |
|---|---|---|
| **The console and CLI steps** | **14 Markdown files** | **`*** NOT EXECUTED ***`** at the top of every one |
| **The verification** | **7 programs** | **Executed and asserted** by `tools/run_cloud_labs.py` |

```bash
pip install -r tools/requirements.txt
python3 tools/run_cloud_labs.py
```

### 🎯 And yet a surprising amount really runs

Most of what this course teaches is **not proprietary**:

| Runs for real | What it is |
|---|---|
| **IAM policy evaluation** | the actual algorithm, in `iam.py` |
| **Object-store semantics** | prefixes, no directories, copy-plus-delete, versioning |
| **All the pricing arithmetic** | storage classes, egress, per-TB, per-node-hour |
| **Hypervisor overcommit** | and the point at which it fails |
| **A real web server** | serving a real page over TCP, fetched back |
| **A real ETL pipeline** | SQLite → transform → DuckDB, with an audit trail |
| **An autoscaling control loop** | measured, including where it loses |
| **A real model and a real AutoML search** | scikit-learn, 25 real fits |
| **A real REST endpoint** | serving that model, called over the network |

**Nothing is claimed that was not executed.** Every `.md` file names the
service it needs and the runnable half that verifies its logic, and the runner
asserts the marker is still present.

### The cross-course check

Experiments 8, 9 and 12 use **Course 11's star schema, imported not copied**.
**₹10,360 for South** is now produced by Course 11's DAX, Course 12 B's Hive,
Course 12 B's Spark and this course's DuckDB — **four engines, nine facts**,
and `verify_all.sh` fails if any of them drifts.

---

## Experiment 1 — Create a virtual machine

`01_create_vm.md` (NOT EXECUTED) ·
`01_vm_and_hosting.py` — **runs**

### The three wizard choices that get people

1. **Memory.** A type 2 hypervisor does not balloon aggressively, so the
   overcommit that works in a datacentre does not work on a laptop. Give a
   16 GB laptop's VM 12 GB and the whole machine swaps.
2. **Disk: pre-allocate or grow.** Pre-allocating writes 40 GB immediately
   and is faster after; growing on demand is what you want on a laptop.
3. **NAT, Bridged or Host-only.** **NAT means the LAN cannot reach the
   guest** — and that is experiment 2's most common failure.

### 🔢 Overcommit, measured

A 32 GB / 8 vCPU host with four guests:

```
allocated RAM  : 48 GB on a 32 GB host   (1.50x)
allocated vCPU : 20 on 8                 (2.50x)
RAM actually touched     : 22.8 GB
reclaimed by ballooning  : 25.2 GB
swapping                 : 0.0 GB
```

**48 GB allocated on 32 GB, and nothing is swapping**, because the guests
only *touch* 22.8 GB. Overcommit works on the same bet an airline makes.

Then the batch job wakes up (20% → 95% active):

```
RAM actually touched : 34.8 GB
swapping             : 2.8 GB
```

**Now every guest is slow — not just the batch job.**

### 🎯 The asymmetry to remember

> **CPU overcommit degrades gracefully. Memory overcommit fails as a cliff.**

CPU is time-sliced, so twice the demand means half the speed for everyone.
A memory page is either resident or on disk, and the difference is a factor of
thousands. **That is the "noisy neighbour" problem**, and it is why cloud
instance types quote dedicated memory and only burstable CPU.

---

## Experiment 2 — Host a page on the server

`02_web_server.md` (NOT EXECUTED) ·
**the page is really served, in `01_vm_and_hosting.py`**

```
document root : /tmp/cloud13b_www_...
serving       : http://127.0.0.1:PORT/   (a REAL server)
GET /          -> 200, text/html, 225 bytes
GET /data.json -> 200, application/json, {'South': 10360.0, 'North': 2520.0}
GET /missing   -> 404
```

A page was written to a document root, **served over TCP**, fetched back, and
its **Content-Type** checked. That is the whole of experiment 2; Apache under
XAMPP adds virtual hosts, `.htaccess`, PHP and TLS, and the shape is identical.

### ⚠️ The header that decides whether your site works

**A browser renders `index.html` because the server *said* `text/html`.** Get
`AddType` wrong and the browser downloads your page instead of showing it —
the commonest "my site is broken" on a fresh VM, and the reason the runnable
half asserts the header rather than just the body.

### And the comparison that ends the experiment

| | This VM | S3 + CloudFront |
|---|---|---|
| Patch Apache | **you, monthly** | not your problem |
| TLS certificate | certbot, and renewals | issued and rotated |
| Survives your laptop closing | **no** | yes |
| A static page costs | a VM, hourly | **cents per GB** |

**A static site on a VM is a general-purpose computer doing an object store's
job**, and the experiment makes the point by having you do it the hard way
once.

---

## Experiments 3 and 10 — Accounts, roles and IAM

`03_account_setup.md` ·
`10_sagemaker_notebook.md` (NOT EXECUTED) ·
`03_iam_and_account.py` — **runs**

### 🎯 The three rules, and they are the whole subject

1. **An explicit DENY anywhere wins — always, unconditionally.**
2. Otherwise, an **ALLOW** that matches grants access.
3. Otherwise **DENY** — the **implicit deny**.

Evaluated against a realistic policy set:

| Action | Resource | Result | Why |
|---|---|---|---|
| `s3:GetObject` | `retail-lake/raw/sales.csv` | **Allow** | `DataScientistRead` |
| `s3:PutObject` | `retail-lake/raw/sales.csv` | **Deny** | **explicit deny** in `ProtectRawZone` |
| `s3:PutObject` | `retail-lake/models/model.pkl` | **Allow** | `SageMakerExecution` |
| `s3:GetObject` | `other-bucket/secret.csv` | **Deny** | **implicit** — nothing matched |

**Read rows 2 and 3 together.** The same action on the same bucket is denied
under `raw/` and allowed under `models/`, because a Deny scoped to one prefix
beats an Allow scoped to the bucket. **That is how a data lake keeps a raw
zone immutable while the rest stays writable.**

### ⚠️ Now add full S3 admin

```
add a policy granting s3:* on *
s3:PutObject on raw/  ->  Deny   (EXPLICIT DENY in ProtectRawZone)
```

**Still denied.** An explicit Deny cannot be out-voted, out-numbered or
out-scoped — **there is no "more specific allow wins" rule**. To lift it you
must *remove* the Deny.

**This is the single most common IAM misunderstanding, and it is also the
feature:** a Deny is how an organisation *guarantees* something rather than
hoping nobody granted otherwise.

**And policy order does not matter** — reversed, the answer is identical.
Unlike a firewall rule list, IAM is **not first-match**: every statement is
evaluated, then the three rules decide.

### Least privilege, made concrete

| Action | `*:*` policy | scoped policy |
|---|---|---|
| `s3:GetObject` on train/ | Allow | **Allow** |
| `s3:PutObject` on models/ | Allow | **Allow** |
| `iam:CreateUser` | **Allow** | **Deny** |
| `ec2:TerminateInstances` | **Allow** | **Deny** |

**Both policies let the training job run.** One of them also lets it create
IAM users and terminate every instance in the account. **"`*:*` made it work"
is not a solution, it is a postponed incident.**

### 🎯 A role is not a user

| | User | Role |
|---|---|---|
| Credentials | long-lived access key | **temporary, auto-rotated** |
| In a notebook | keys in a file — **bad** | attached; **no keys exist** |
| If leaked | valid until revoked | expires in minutes to hours |

**A SageMaker notebook gets an execution role, so no access key is ever
written to disk.** That is why experiment 10 says "attach IAM role" rather
than "paste your credentials", and "I put my keys in the notebook" is the
answer that loses the marks.

### ⚠️ The endpoint trap

**A forgotten `ml.m5.large` endpoint costs about $70/month.** A training job
ends and stops billing; **an endpoint runs until you delete it**, at hourly
rates, whether or not anything calls it.

**Set a budget alarm on day one, before anything else.**

---

## Experiments 4, 5 and 6 — Object, block and file storage

`04_buckets.md` ·
`05_ebs.md` ·
`06_efs.md` (NOT EXECUTED) ·
`04_storage.py` — **runs**

### ⚠️ There are no directories

```
LIST prefix 'raw/' with delimiter '/':
  objects at this level : (none)
  common prefixes       : ['raw/2026/']
```

**`raw/2026/01/sales.csv` is ONE KEY containing three slashes.** The console's
folder tree is drawn from **common prefixes computed at list time**. Delete
every object under a "folder" and the folder is gone, because it never
existed.

**And a prefix scan is the only query an object store supports.**

### ⚠️ There is no rename

```
'rename' README.md -> docs/README.md
  bytes read 1,024, bytes written 1,024, API calls 2
```

**Copy plus delete.** Renaming a 5 TB dataset "to tidy the folders" moves
10 TB and is billed for it.

### ⚠️ Versioning bills for every version

```
versioning ON, overwrite, then delete:
  older versions kept : 2
  current object      : DeleteMarker
```

**A delete writes a marker; the data is still there and still billed.** Set
the lifecycle rule when you enable versioning, not later.

### 🔢 Storage classes — 1 TB for a year, retrieved once

| Class | Storage/yr | Retrieve | Total | Min days |
|---|---:|---:|---:|---:|
| Standard | $282.62 | $0.00 | **$282.62** | 0 |
| Standard-IA | $153.60 | $10.24 | $163.84 | 30 |
| Glacier Instant | $49.15 | $30.72 | $79.87 | 90 |
| **Deep Archive** | **$12.17** | $20.48 | **$32.65** | **180** |

**Read the two ratios separately.** Deep Archive **storage** is **23×**
cheaper. Add one retrieval a year and the all-in saving falls to **8.7×**,
because the retrieval fee ($20.48) exceeds a whole year of its storage
($12.17). **The headline discount is not the discount.**

### ⚠️ And the reversal

The same 1 TB, retrieved **twice a month**:

| Class | Total/yr |
|---|---:|
| **Standard** | **$282.62** |
| Standard-IA | $399.36 |
| Glacier Instant | $786.43 |

**Standard is now the cheapest.** *"We moved everything to IA to save money"
is how a bill goes UP.*

### 🔢 Egress

| Transfer | Cost |
|---|---:|
| 1 TB **in** | **$0.00** |
| 1 TB **out** | **$92.16** |
| 1 TB S3 → EC2, same region | **$0.00** |

**Downloading 1 TB once costs as much as storing it for 3.9 months.** Ingress
is free; egress is not — **and that is the mechanism behind lock-in: your data
is not held hostage, it is simply expensive to move.**

### 🔢 Block, file and object

| | EBS gp3 | EFS Standard | S3 Standard |
|---|---:|---:|---:|
| 1 TB/month | $81.92 | **$307.20** | **$23.55** |

**EFS costs 13× S3 and 3.8× EBS** — worth it precisely when several instances
must share a POSIX filesystem, and a mistake for a dataset one batch job reads
once.

**And provisioned against consumed:** a 1 TB EBS volume holding 200 GB bills
**$81.92** where S3 bills **$4.60** — a factor of **18**. *"Just make it 1 TB
to be safe" is an expensive habit.*

---

## Experiment 7 — The notebook environment

`07_notebook.md` (NOT EXECUTED) ·
**cells executed and asserted in `01_vm_and_hosting.py`**

```
In  [1]: import pandas as pd; import fixtures as f
In  [2]: df.shape                       -> (9, 19)
In  [3]: df.groupby('region')['revenue'].sum()  -> South 10360.0
In  [4]: df['revenue'].sum()            -> 12880.0
```

Four cells, executed in order, **every output asserted**. That is what a
notebook *test* looks like — `papermill` and `nbconvert --execute` do exactly
this in CI, and **a notebook nobody executes in CI is a notebook that has
already drifted**.

### ⚠️ The mistake that matters

```bash
jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.token=''
```

**That publishes a root shell on the internet.** A notebook executes arbitrary
code by design, so an unauthenticated one is not "an insecure notebook" — it
is a remote code execution endpoint. Scanners find these in minutes.

**Always an SSH tunnel, or a managed notebook behind IAM.**

### 💡 And the row that costs money

| | Colab | Cloud notebook |
|---|---|---|
| Stops when | idle ~90 min | **never — you stop it** |
| State on stop | lost | kept on the volume |

**An m5.xlarge notebook left running costs about $140/month.** Colab
disconnecting is an annoyance; a cloud notebook *not* disconnecting is a bill.
**Set an idle-shutdown lifecycle policy on day one.**

---

## Experiments 8, 9 and 12 — Cloud DB, batch ETL, warehouse load

`08_cloud_db.md` ·
`12_etl_to_warehouse.md` (NOT EXECUTED) ·
`09_etl_warehouse.py` — **runs end to end**

### 🔢 The pipeline, with an audit trail

| Step | Rows |
|---|---:|
| extracted | **11** |
| after dedup | 10 |
| dropped, null region | 1 |
| **loaded** | **9** |

**11 in, 9 out, and the pipeline can say where the other two went.** A
transformation that silently drops rows is worse than one that fails: **the
numbers still look plausible**. Every ETL job should emit these counts, and a
monitoring rule should alarm when the drop rate moves.

### 🎯 The four-engine check

| Region | Revenue | Profit | Margin |
|---|---:|---:|---:|
| South | **10,360** | 2,760 | 26.64% |
| North | 2,520 | 765 | 30.36% |

**₹12,880 total, ₹10,360 for South** — Course 11's DAX, Course 12 B's Hive,
Course 12 B's Spark and this. **Four engines, one set of nine facts.**

### 🔢 BigQuery, at $6.25 per TB scanned

| Query | TB scanned | Cost |
|---|---:|---:|
| `SELECT * FROM events` | 10.00 | **$62.50** |
| `SELECT user_id FROM events` | 0.40 | $2.50 |
| `SELECT user_id … WHERE dt = '…'` | **0.02** | **$0.12** |

**The same question, 500× the price.** Column projection and partition
pruning — **Course 12 B's techniques, saving money here instead of time**.
That is why `SELECT *` is a *billing incident* on a serverless warehouse and
merely rude on a server you already own.

### 🔢 And the break-even

Redshift at $1.086/node-hour: 2 nodes is **$1,585.56/month**.

**Break-even against on-demand BigQuery: about 254 TB scanned per month.**
Below that, serverless is cheaper and costs nothing when idle. Above it, a
cluster is cheaper and an extra query is free at the margin. **A calculation,
not a preference.**

### ETL against ELT

**ELT won because warehouse compute got cheap and elastic.** Landing raw data
means a transformation bug is fixed by re-running SQL rather than
re-extracting from a production database that may no longer hold the old rows
— **exactly the `DELETE` problem Course 12 B found in Sqoop**.

---

## Experiments 11 and 14 — Training and AutoML

`11_sagemaker_train.md` ·
`14_automl.md` (NOT EXECUTED) ·
`11_train_and_automl.py` — **runs**

### 🎯 Quote the dummy first, always

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| `DummyClassifier` | **0.8433** | **0.0000** | 0.5000 |
| GradientBoosting | 0.9467 | 0.8095 | 0.9029 |

**94.67% sounds excellent until you see 84.33% for predicting "never
churns".** The real gain is 10.3 percentage points, and the **F1 of 0.8095
against 0.0000** is what shows the model found anything.

**Course 12 A's argument, and it does not stop being true because the model
trained on somebody else's computer.**

### The artefact is the deliverable

**138,945 bytes**, written to disk, reloaded, and predicting identically. A
SageMaker training job writes exactly this to `s3://bucket/models/`, and the
deploy step reads it back. **Training and serving are separate systems joined
by one file in object storage** — which is why the IAM role in experiment 10
needs `s3:PutObject` on `models/` and nothing else.

### 🔢 The instance choice, priced

| Instance | $/hour | 10-min job |
|---|---:|---:|
| m5.xlarge | 0.1920 | **0.0320** |
| p3.2xlarge (1 GPU) | 3.0600 | 0.5100 |
| **p4d.24xlarge (8 GPU)** | **32.7726** | **5.4621** |

**171× for the same ten minutes — and gradient boosting on tabular data has
no GPU code path.** It would run at exactly the same speed.

> **"Which instance?" is answered by the algorithm, not by ambition.**

### 🔢 AutoML, actually run

Five candidates, 5-fold CV, **25 real fits**:

| Rank | Model | CV AUC | std |
|---:|---|---:|---:|
| 1 | RandomForest(100) | **0.9334** | 0.0210 |
| 2 | GradientBoosting | **0.9288** | 0.0196 |
| 3 | DecisionTree(depth=None) | 0.8213 | 0.0425 |
| 4 | LogisticRegression | 0.8154 | 0.0606 |
| 5 | DecisionTree(depth=3) | 0.8025 | 0.0364 |

**The leaderboard is the whole of AutoML.** Fit many models, cross-validate,
rank. **There is no intelligence in it — it is a search.**

### ⚠️ And the top two are inside the noise

**0.9334 against 0.9288 is a gap of 0.0047, with standard deviations of
0.0210 and 0.0196.** Declaring a winner is not supported by the data, and
**"AutoML picked X" is not a reason to prefer X**.

### 🔢 What the search costs

One fit here takes 0.127 s — too small to cost anything. **Scale to a
realistic four minutes per fit:**

| Search | Fits | Compute | m5.xlarge |
|---|---:|---:|---:|
| this search | 25 | 1.7 h | $0.32 |
| a modest managed search | 250 | 16.7 h | $3.20 |
| **a full AutoML run** | **2,000** | **133.3 h** | **$25.60** |

**A straight multiple of one fit — exactly 2,000×** — because that is all it
is. And managed services charge a premium on top.

### 🎯 What AutoML does not do

decide the target · notice leakage · tell you the base rate matters more ·
know last year's data no longer applies · choose a threshold that fits the
business cost · explain a prediction · notice unfairness

**Every one of those is the actual job.** AutoML automates the afternoon and
leaves the weeks untouched.

---

## Experiment 13 — Monitoring, alarms and auto-scaling

`13_monitoring.md` (NOT EXECUTED) ·
`13_monitoring_autoscale.py` — **runs**

A day of traffic: peak **1,000 req/s**, trough **164**; instances serve 150
req/s; the group is 2–12.

| Strategy | Instance-hours | Dropped |
|---|---:|---:|
| fixed at peak (7) | **168** | **0** |
| autoscaled, 70%/40%, cooldown 1 | **129** | **1,014** |

### ⚠️ Autoscaling dropped 1,014 requests and fixed capacity dropped none

The worst hour is **hour 9**: demand jumped to 1,000 against 4 instances,
because **the group was sized for the previous hour**.

> **Autoscaling does not track demand. It CHASES demand, and it is always one
> observation behind.**

That lag is the cost of the 23% saving.

### 🔢 The tuning curve

| Out/in | Cool | Inst-hrs | Dropped | Changes |
|---|---:|---:|---:|---:|
| 70%/40% | 1 | 129 | 1,014 | 8 |
| 50%/30% | 1 | 158 | 358 | 10 |
| 85%/60% | 1 | **114** | **1,380** | 7 |
| 70%/40% | 3 | **96** | **2,093** | **4** |
| **50%/30%** | **0** | **188** | **0** | 11 |

**This is a trade-off curve, not a leaderboard.** You are choosing between
spare capacity and dropped requests, and only a business can say which is
worse.

### ⚠️ And read the last row against fixed capacity

**188 instance-hours against 168.** Scaling out at 50% with no cooldown drops
nothing — **and costs more than simply buying the peak.**

> **Autoscaling made it MORE expensive.** Chase demand hard enough and the
> group overshoots on the way up and lingers on the way down.
>
> **"Autoscaling saves money" is a claim about a *tuned* autoscaler.**

**The cooldown row:** 3 ticks gives 4 scaling changes instead of 8, at
**+1,079** dropped requests. A long cooldown stops **flapping** — which costs
boot time and stabilises nothing. *Scale out eagerly, scale in reluctantly.*

### 🔢 Alarm on the tail

```
20 latencies, one of them 900 ms:
  mean 85.0 ms   p50 42.0 ms   p95 87.8 ms   p99 737.5 ms
```

**An alarm on the mean never fires.** Alarm on p95 or p99 — **the tail is
where users live**, and 5% of requests is a lot of users.

### 💡 The metric nobody sets

| Metric | Alarm when | The trap |
|---|---|---|
| `ModelLatency` p99 | > 500 ms | the mean hides it; the unit is **microseconds** |
| `Invocation5XXErrors` | > 0 | these are **yours** |
| `Invocation4XXErrors` | > 1% | a **rate**, never a count |
| `EstimatedCharges` | > budget | lags ~6 h, `us-east-1` only |
| **`Invocations` == 0** | for 1 hour | **a dead endpoint still bills** |

**The last row is the one people miss.** An endpoint serving nothing looks
perfect on every performance metric and costs the same as a busy one.

### 🔢 And what the day cost

| | Per month |
|---|---:|
| fixed at peak, on-demand | $483.84 |
| autoscaled, on-demand | $371.52 |
| fixed, **reserved** (−40%) | $290.30 |
| autoscaled, **spot** (−70%) | **$111.46** |

**The real answer is usually both:** a reserved baseline for the floor, spot
or on-demand for the peak.

---

## Experiment 15 — Deploy the model as a REST endpoint

`15_deploy.md` (NOT EXECUTED) ·
`15_deploy_endpoint.py` —
**a REAL HTTP server, serving a REAL model**

```
artefact loaded from disk: 138,945 bytes
endpoint listening on http://127.0.0.1:PORT   (a REAL HTTP server)

GET /ping        -> 200 {'status': 'healthy', 'model_loaded': True}
POST /invocations (3 rows)  -> 200
  predictions   : [0, 0, 0]
  probabilities : [0.015383, 0.008643, 0.014492]
POST /invocations (300 rows) -> 200, accuracy 0.9467
```

### 🎯 The equality that is the deployment test

**The endpoint's answers are identical to calling the model in-process.**
Serving must not change predictions — and **a preprocessing step that lives in
your notebook rather than in the pipeline is exactly how it does.**

### ⚠️ `/ping` must not run the model

**A health check that does real inference marks the container unhealthy
whenever the model is merely slow — and the platform then kills a container
that was working.** A self-inflicted outage, and a classic one.

### Error handling, which is most of a real endpoint

| Case | Status |
|---|---:|
| wrong feature count | **400** |
| body not a list | **400** |
| empty body | **400** |
| wrong route (POST and GET) | **404** |

**Every one is a 4xx, not a 5xx**, and the distinction is operational rather
than pedantic: **5xx means *your* service is broken and should page someone.**
If malformed client input returns 500, your error alarm fires for other
people's bugs and you stop trusting it.

### 🔢 Latency, over 200 real requests

```
mean 0.895 ms   p50 0.848 ms   p95 1.337 ms   p99 1.491 ms
```

**p99 is 1.8× p50 on an idle machine serving one model.** Under load that
ratio grows — which is why experiment 13's alarm is on p99.

### 🔢 And the batching result

```
one request of 100 rows :    4.90 ms
100 requests of one row : 181.85 ms   (37x)
```

**37×, and none of it is the model** — it is per-request overhead: HTTP, JSON
parsing, and a NumPy call whose fixed cost is paid 100 times instead of once.

> **If you are scoring a million rows, calling an endpoint a million times is
> the expensive way to do arithmetic.**

### What SageMaker adds that this server does not have

| | This script | A managed endpoint |
|---|---|---|
| TLS | no | terminated for you |
| Authentication | **NONE — anyone** | IAM-signed requests |
| Load balancing | one process | across instances and AZs |
| Autoscaling | no | on `InvocationsPerInstance` |
| Blue/green | no | traffic shifted gradually |
| **Cost** | electricity | **$70/month, called or not** |

**Deleting the endpoint is a step in the experiment, not an afterthought.**

---

## What the runner asserts

| Script | Experiments | Real? |
|---|---|---|
| `01_vm_and_hosting.py` | 1, 2, 7 | **a real web server**; overcommit modelled |
| `03_iam_and_account.py` | 3, 10 | **the real IAM algorithm** |
| `04_storage.py` | 4, 5, 6 | real key semantics, real arithmetic |
| `09_etl_warehouse.py` | 8, 9, 12 | **real SQLite → real DuckDB** |
| `11_train_and_automl.py` | 11, 14 | **a real model, a real 25-fit search** |
| `13_monitoring_autoscale.py` | 13 | a real control loop |
| `15_deploy_endpoint.py` | 15 | **a real HTTP endpoint, called over TCP** |

Plus the audit: **14 Markdown files, every one carrying `*** NOT EXECUTED
***`**, each naming the service it needs.

---

## Lab examination

Two hours on a console, one experiment number, then a viva.

**What costs marks:**

- Using the root account for anything
- `*:*` in an IAM policy, and calling it "it works now"
- Saying a more specific Allow beats a Deny
- Claiming an object store has folders
- Treating `s3 mv` as a rename
- Recommending Infrequent Access without asking how often it is read
- Forgetting egress in a migration estimate
- Putting a read-once dataset on EFS
- Saying `LIMIT 10` makes a BigQuery query cheap
- Alarming on mean latency
- Recommending GPUs for tabular machine learning
- **Leaving the endpoint running**

**What earns them:**

- **The three IAM rules, applied.** Explicit deny; else allow; else deny —
  and the demonstration that adding S3 admin changes nothing.
- **"Prefix-scoped Deny beats bucket-scoped Allow."** One sentence that
  explains a data lake's raw zone.
- **The two storage-class ratios: 23× on storage, 8.7× all-in.** And Standard
  winning outright at two retrievals a month.
- **"1 TB out costs what 3.9 months of storage costs."** Egress, data
  gravity and lock-in in one figure.
- **The 500× BigQuery difference**, and naming it as Course 12 B's column
  projection and partition pruning saving money instead of time.
- **The 254 TB break-even.** Serverless against provisioned as a calculation.
- **"171× for the same speed."** Instance choice as an engineering decision.
- **"The AutoML gap is inside the noise."** 0.0047 against standard
  deviations of 0.02.
- **"Autoscaling made it more expensive."** 188 instance-hours against 168 —
  reporting the result that contradicts the slogan.
- **"37× for calling an endpoint per row."** Batch transform, argued with a
  number.
- **₹10,360 from four engines.** The check that makes the rest believable.
