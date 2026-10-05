# Practical Lab

**15 experiments**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.

Code lives in `labs/course-13b-cloud/`.

## Read this before you read anything else

> **There is no cloud account for this repository, and none will be created.**

Signing up for AWS, Azure or GCP requires a payment card and accepts a
billing relationship. That is not a thing a study repository should do on
anyone's behalf, so **no provider was ever contacted** and no claim in these
notes about a provider's behaviour was demonstrated here.

| Half | Files | Status |
|---|---|---|
| **The console and CLI steps** | **14 Markdown files** | **NOT EXECUTED**, at the top of every one: each experiment's **4. Programme** is its procedure, and **5. Execution and Results** says so in a box |
| **The verification** | **7 programs** | **Executed and asserted** by `tools/data-science/run_cloud_labs.py`; what each printed is under the experiment it is named for |

```bash
pip install -r tools/requirements.txt
python3 tools/data-science/run_cloud_labs.py
```

<div class="example" markdown="1">
<span class="label">AND YET A SURPRISING AMOUNT REALLY RUNS</span>

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
</div>

Three of the programs time something — a training job, a model search, an endpoint's latency.
A timing measures the machine at a moment, so those lines differ from run to run, and
`capture_lab_outputs.py --check` sets them aside; every other line must repeat exactly.

### The cross-course check

Experiments 8, 9 and 12 use **Business Intelligence Tools' star schema, imported not copied**.
**₹10,360 for South** is now produced by Business Intelligence Tools' DAX, Big Data Technologies' Hive,
Big Data Technologies' Spark and this course's DuckDB — **four engines, nine facts**,
and `verify_all.sh` fails if any of them drifts.

---

## Experiment 1 — Create a virtual machine

### 1. Question

Create a virtual machine in VMware Workstation.

### 2. Aim

Run the new-VM wizard, make the three choices that matter, and see where memory overcommit fails.

### 3. Steps

**The procedure, on the console and CLI**, `01_create_vm.md`:

1. **Run the wizard.**
2. **Make the three choices that matter.**
3. **Finish the install.**

**The Python model, which runs**, `01_vm_and_hosting.py`, for experiments 1, 2 and 7:

1. **Experiment 1: allocate the guests, and overcommit.**
2. **Experiment 2: serve a page.**
3. **Experiment 7: run the notebook's cells.**

<div class="formula" markdown="1">
<span class="label">THE THREE WIZARD CHOICES THAT GET PEOPLE</span>

- **Memory.** A type 2 hypervisor does not balloon aggressively, so the
  overcommit that works in a datacentre does not work on a laptop. Give a
  16 GB laptop's VM 12 GB and the whole machine swaps.
- **Disk: pre-allocate or grow.** Pre-allocating writes 40 GB immediately
  and is faster after; growing on demand is what you want on a laptop.
- **NAT, Bridged or Host-only.** **NAT means the LAN cannot reach the
  guest** — and that is experiment 2's most common failure.
</div>


### 4. Programme

**The procedure, on the console and CLI**, `01_create_vm.md`:

{{programme: course-13b-cloud/01_create_vm.md}}

**The Python model, which runs**, `01_vm_and_hosting.py`, for experiments 1, 2 and 7:

{{programme: course-13b-cloud/01_vm_and_hosting.py}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `01_create_vm.md`:

{{not-run: course-13b-cloud/01_create_vm.md | it needs a cloud account, and this repository has none}}

**The Python model, which runs**, `01_vm_and_hosting.py`, for experiments 1, 2 and 7:

{{output: course-13b-cloud/01_vm_and_hosting.py}}

**Overcommit, measured.** A 32 GB / 8 vCPU host with four guests:

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

<div class="example" markdown="1">
<span class="label">THE ASYMMETRY TO REMEMBER</span>

> **CPU overcommit degrades gracefully. Memory overcommit fails as a cliff.**

CPU is time-sliced, so twice the demand means half the speed for everyone.
A memory page is either resident or on disk, and the difference is a factor of
thousands. **That is the "noisy neighbour" problem**, and it is why cloud
instance types quote dedicated memory and only burstable CPU.
</div>

**Changed:** the program printed the temporary document root's full name and the web server's
port, which the system picks afresh on every run; it now says what they are.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

48 GB allocated on a 32 GB host swaps nothing while the guests touch 22.8 GB; when the batch job wakes, 2.8 GB swaps and every guest slows.
</div>


## Experiment 2 — Host a page on the server

### 1. Question

Install and configure Apache (or XAMPP) on the VM, and host a page.

### 2. Aim

Serve a page, check the header that decides whether a browser shows it, and compare a VM with an object store.

### 3. Steps

**The procedure, on the console and CLI**, `02_web_server.md`:

1. **Install Apache, on Linux.**
2. **Or install XAMPP, on Windows.**
3. **Configure it.**
4. **Enable TLS.**
5. **Compare it with an object store.**

<div class="formula" markdown="1">
<span class="label">WHAT RUNS</span>

**The page is really served, in `01_vm_and_hosting.py`'s experiment 2:**

```
GET /          -> 200, text/html, 225 bytes
GET /data.json -> 200, application/json, {'South': 10360.0, 'North': 2520.0}
GET /missing   -> 404
```

A page was written to a document root, **served over TCP**, fetched back, and
its **Content-Type** checked. That is the whole of experiment 2; Apache under
XAMPP adds virtual hosts, `.htaccess`, PHP and TLS, and the shape is identical.
</div>


### 4. Programme

**The procedure, on the console and CLI**, `02_web_server.md`:

{{programme: course-13b-cloud/02_web_server.md}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `02_web_server.md`:

{{not-run: course-13b-cloud/02_web_server.md | it needs a cloud account, and this repository has none}}

<div class="warn" markdown="1">
<span class="label">THE HEADER THAT DECIDES WHETHER YOUR SITE WORKS</span>

**A browser renders `index.html` because the server *said* `text/html`.** Get
`AddType` wrong and the browser downloads your page instead of showing it —
the commonest "my site is broken" on a fresh VM, and the reason the runnable
half asserts the header rather than just the body.
</div>

**And the comparison that ends the experiment:**

| | This VM | S3 + CloudFront |
|---|---|---|
| Patch Apache | **you, monthly** | not your problem |
| TLS certificate | certbot, and renewals | issued and rotated |
| Survives your laptop closing | **no** | yes |
| A static page costs | a VM, hourly | **cents per GB** |

**A static site on a VM is a general-purpose computer doing an object store's
job**, and the experiment makes the point by having you do it the hard way
once.

The Python model for this experiment, `01_vm_and_hosting.py`, is shown in full under Experiment 1, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A page written to a document root was served over TCP and fetched back as text/html; a missing page gave 404.
</div>


## Experiment 3 — Create and configure a cloud account

### 1. Question

Create and configure a cloud account on the AWS, Azure or GCP free tier.

### 2. Aim

Set the account up safely, and see exactly how IAM decides each request.

### 3. Steps

**The procedure, on the console and CLI**, `03_account_setup.md`:

1. **Do the six things first.**
2. **Use an IAM user, not root.**
3. **Stay within the free tier.**
4. **Know the equivalents.**
5. **Clean up.**

**The Python model, which runs**, `03_iam_and_account.py`, for experiments 3 and 10:

1. **Evaluate the attached policies.**
2. **Add full S3 admin.**
3. **Reverse the policy order.**
4. **Compare a role with a user.**
5. **Compare least privilege with *:*.**
6. **Price the free tier.**

<div class="formula" markdown="1">
<span class="label">THE THREE RULES, AND THEY ARE THE WHOLE SUBJECT</span>

1. An **explicit DENY** anywhere wins — always, unconditionally.
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
</div>


### 4. Programme

**The procedure, on the console and CLI**, `03_account_setup.md`:

{{programme: course-13b-cloud/03_account_setup.md}}

**The Python model, which runs**, `03_iam_and_account.py`, for experiments 3 and 10:

{{programme: course-13b-cloud/03_iam_and_account.py}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `03_account_setup.md`:

{{not-run: course-13b-cloud/03_account_setup.md | it needs a cloud account, and this repository has none}}

**The Python model, which runs**, `03_iam_and_account.py`, for experiments 3 and 10:

{{output: course-13b-cloud/03_iam_and_account.py}}

<div class="warn" markdown="1">
<span class="label">NOW ADD FULL S3 ADMIN</span>

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
</div>

**And policy order does not matter** — reversed, the answer is identical.
Unlike a firewall rule list, IAM is **not first-match**: every statement is
evaluated, then the three rules decide.

**Least privilege, made concrete:**

| Action | `*:*` policy | scoped policy |
|---|---|---|
| `s3:GetObject` on train/ | Allow | **Allow** |
| `s3:PutObject` on models/ | Allow | **Allow** |
| `iam:CreateUser` | **Allow** | **Deny** |
| `ec2:TerminateInstances` | **Allow** | **Deny** |

**Both policies let the training job run.** One of them also lets it create
IAM users and terminate every instance in the account. **"`*:*` made it work"
is not a solution, it is a postponed incident.**

<div class="concept" markdown="1">
<span class="label">RESULT</span>

An explicit Deny on raw/ beats every Allow, even full S3 admin; policy order changes nothing; a scoped policy runs the job and refuses everything else.
</div>


## Experiment 4 — Create and manage storage buckets

### 1. Question

Create and manage storage buckets, and upload and access datasets.

### 2. Aim

Store and list objects, and see that an object store has no directories, no rename and a bill for every version.

### 3. Steps

**The procedure, on the console and CLI**, `04_buckets.md`:

1. **Create a bucket and copy data, with the CLI.**
2. **Name it uniquely.**
3. **Turn on versioning and a lifecycle rule.**
4. **Block public access.**
5. **Encrypt it.**

**The Python model, which runs**, `04_storage.py`, for experiments 4, 5 and 6:

1. **Experiment 4: list a bucket by prefix.**
2. **Rename an object.**
3. **Version it.**
4. **Price the storage classes.**
5. **Read it twice a month.**
6. **Price the egress.**
7. **Experiments 5 and 6: compare block, file and object storage.**
8. **Provision against consumption.**

<div class="formula" markdown="1">
<span class="label">THERE ARE NO DIRECTORIES</span>

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
</div>


### 4. Programme

**The procedure, on the console and CLI**, `04_buckets.md`:

{{programme: course-13b-cloud/04_buckets.md}}

**The Python model, which runs**, `04_storage.py`, for experiments 4, 5 and 6:

{{programme: course-13b-cloud/04_storage.py}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `04_buckets.md`:

{{not-run: course-13b-cloud/04_buckets.md | it needs a cloud account, and this repository has none}}

**The Python model, which runs**, `04_storage.py`, for experiments 4, 5 and 6:

{{output: course-13b-cloud/04_storage.py}}

<div class="warn" markdown="1">
<span class="label">THERE IS NO RENAME</span>

```
'rename' README.md -> docs/README.md
  bytes read 1,024, bytes written 1,024, API calls 2
```

**Copy plus delete.** Renaming a 5 TB dataset "to tidy the folders" moves
10 TB and is billed for it.
</div>

<div class="warn" markdown="1">
<span class="label">VERSIONING BILLS FOR EVERY VERSION</span>

```
versioning ON, overwrite, then delete:
  older versions kept : 2
  current object      : DeleteMarker
```

**A delete writes a marker; the data is still there and still billed.** Set
the lifecycle rule when you enable versioning, not later.
</div>

**Storage classes — 1 TB for a year, retrieved once:**

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

<div class="warn" markdown="1">
<span class="label">AND THE REVERSAL</span>

The same 1 TB, retrieved **twice a month**:

| Class | Total/yr |
|---|---:|
| **Standard** | **$282.62** |
| Standard-IA | $399.36 |
| Glacier Instant | $786.43 |

**Standard is now the cheapest.** *"We moved everything to IA to save money"
is how a bill goes UP.*
</div>

**Egress:**

| Transfer | Cost |
|---|---:|
| 1 TB **in** | **$0.00** |
| 1 TB **out** | **$92.16** |
| 1 TB S3 → EC2, same region | **$0.00** |

**Downloading 1 TB once costs as much as storing it for 3.9 months.** Ingress
is free; egress is not — **and that is the mechanism behind lock-in: your data
is not held hostage, it is simply expensive to move.**

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A listing by prefix finds no objects at raw/, only a common prefix; a rename is a copy and a delete; Deep Archive is 23× cheaper to store and 8.7× cheaper all-in.
</div>


## Experiment 5 — Block storage

### 1. Question

Launch an instance and configure block storage (EBS).

### 2. Aim

Attach, format and mount a volume, and price block storage against file and object storage.

### 3. Steps

**The procedure, on the console and CLI**, `05_ebs.md`:

1. **Launch, attach, format and mount.**
2. **Avoid the three mistakes.**
3. **Keep it in one zone.**
4. **Choose a volume type.**
5. **Snapshot it.**

<div class="formula" markdown="1">
<span class="label">BLOCK, FILE AND OBJECT</span>

| | EBS gp3 | EFS Standard | S3 Standard |
|---|---:|---:|---:|
| 1 TB/month | $81.92 | **$307.20** | **$23.55** |

**And provisioned against consumed:** a 1 TB EBS volume holding 200 GB bills
**$81.92** where S3 bills **$4.60** — a factor of **18**. *"Just make it 1 TB
to be safe" is an expensive habit.*
</div>


### 4. Programme

**The procedure, on the console and CLI**, `05_ebs.md`:

{{programme: course-13b-cloud/05_ebs.md}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `05_ebs.md`:

{{not-run: course-13b-cloud/05_ebs.md | it needs a cloud account, and this repository has none}}

The Python model for this experiment, `04_storage.py`, is shown in full under Experiment 4, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

1 TB costs $81.92 a month on EBS; a 1 TB volume holding 200 GB bills $81.92 where S3 would bill $4.60.
</div>


## Experiment 6 — File storage

### 1. Question

Create and configure file storage on a cloud VM (EFS).

### 2. Aim

Create and mount a shared file system, and decide when it is worth its price.

### 3. Steps

**The procedure, on the console and CLI**, `06_efs.md`:

1. **Create and mount.**
2. **Open the security group.**
3. **Decide what EFS is for.**
4. **Count the cost.**
5. **Know the equivalents.**

<div class="formula" markdown="1">
<span class="label">THE PRICE</span>

**EFS costs 13× S3 and 3.8× EBS** — worth it precisely when several instances
must share a POSIX filesystem, and a mistake for a dataset one batch job reads
once. The figures are the table under Experiment 5.
</div>


### 4. Programme

**The procedure, on the console and CLI**, `06_efs.md`:

{{programme: course-13b-cloud/06_efs.md}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `06_efs.md`:

{{not-run: course-13b-cloud/06_efs.md | it needs a cloud account, and this repository has none}}

The Python model for this experiment, `04_storage.py`, is shown in full under Experiment 4, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

EFS costs 13× S3 and 3.8× EBS: worth it when several instances share a POSIX file system.
</div>


## Experiment 7 — The notebook environment

### 1. Question

Set up Jupyter Notebook or Colab on a cloud VM.

### 2. Aim

Run a notebook's cells in order and assert their outputs, and never publish it unauthenticated.

### 3. Steps

**The procedure, on the console and CLI**, `07_notebook.md`:

1. **Start the notebook on the VM.**
2. **Avoid the mistake that matters.**
3. **Or use a managed notebook.**
4. **Set the lifecycle configuration.**
5. **Compare it with Colab.**

<div class="formula" markdown="1">
<span class="label">WHAT RUNS</span>

**Cells executed and asserted in `01_vm_and_hosting.py`:**

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
</div>


### 4. Programme

**The procedure, on the console and CLI**, `07_notebook.md`:

{{programme: course-13b-cloud/07_notebook.md}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `07_notebook.md`:

{{not-run: course-13b-cloud/07_notebook.md | it needs a cloud account, and this repository has none}}

<div class="warn" markdown="1">
<span class="label">THE MISTAKE THAT MATTERS</span>

```bash
jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.token=''
```

**That publishes a root shell on the internet.** A notebook executes arbitrary
code by design, so an unauthenticated one is not "an insecure notebook" — it
is a remote code execution endpoint. Scanners find these in minutes.

**Always an SSH tunnel, or a managed notebook behind IAM.**
</div>

<div class="example" markdown="1">
<span class="label">AND THE ROW THAT COSTS MONEY</span>

| | Colab | Cloud notebook |
|---|---|---|
| Stops when | idle ~90 min | **never — you stop it** |
| State on stop | lost | kept on the volume |

**An m5.xlarge notebook left running costs about $140/month.** Colab
disconnecting is an annoyance; a cloud notebook *not* disconnecting is a bill.
**Set an idle-shutdown lifecycle policy on day one.**
</div>

The Python model for this experiment, `01_vm_and_hosting.py`, is shown in full under Experiment 1, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Four cells executed in order, every output asserted: South ₹10,360 and ₹12,880 in all.
</div>


## Experiment 8 — Cloud-hosted databases

### 1. Question

Connect to cloud-hosted database services: RDS, BigQuery and Cosmos DB.

### 2. Aim

Query a managed database and a serverless warehouse, and see what a query costs.

### 3. Steps

**The procedure, on the console and CLI**, `08_cloud_db.md`:

1. **Create a managed database.**
2. **Query BigQuery.**
3. **Try Cosmos DB.**
4. **Compare managed with self-hosted.**

<div class="formula" markdown="1">
<span class="label">WHAT A QUERY COSTS</span>

**BigQuery, at $6.25 per TB scanned:**

| Query | TB scanned | Cost |
|---|---:|---:|
| `SELECT * FROM events` | 10.00 | **$62.50** |
| `SELECT user_id FROM events` | 0.40 | $2.50 |
| `SELECT user_id … WHERE dt = '…'` | **0.02** | **$0.12** |

**The same question, 500× the price.** Column projection and partition
pruning — **Big Data Technologies' techniques, saving money here instead of time**.
That is why `SELECT *` is a *billing incident* on a serverless warehouse and
merely rude on a server you already own.
</div>


### 4. Programme

**The procedure, on the console and CLI**, `08_cloud_db.md`:

{{programme: course-13b-cloud/08_cloud_db.md}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `08_cloud_db.md`:

{{not-run: course-13b-cloud/08_cloud_db.md | it needs a cloud account, and this repository has none}}

The Python model for this experiment, `09_etl_warehouse.py`, is shown in full under Experiment 9, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The same question costs $62.50 as SELECT * and $0.12 with a column list and a partition filter.
</div>


## Experiment 9 — A batch ETL pipeline

### 1. Question

Build a batch ETL pipeline: extract from an operational database, transform, and load a warehouse.

### 2. Aim

Run the pipeline end to end, with an audit trail at every step, and check South against three other engines.

### 3. Steps

**The Python model, which runs**, `09_etl_warehouse.py`, for experiments 8, 9 and 12:

1. **Extract from the operational database.**
2. **Transform, with an audit trail.**
3. **Load into the warehouse.**
4. **Set ETL against ELT.**
5. **See what makes a cloud warehouse different.**
6. **Price the queries.**

<div class="formula" markdown="1">
<span class="label">THE PIPELINE, WITH AN AUDIT TRAIL</span>

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
</div>


### 4. Programme

**The Python model, which runs**, `09_etl_warehouse.py`, for experiments 8, 9 and 12:

{{programme: course-13b-cloud/09_etl_warehouse.py}}

### 5. Execution and Results

**The Python model, which runs**, `09_etl_warehouse.py`, for experiments 8, 9 and 12:

{{output: course-13b-cloud/09_etl_warehouse.py}}

This experiment has no console procedure: SQLite stands in for the operational database
(RDS) and DuckDB for the warehouse, and the pipeline between them runs end to end. Experiment
12's procedure does the same with Glue and Redshift or BigQuery.

<div class="example" markdown="1">
<span class="label">THE FOUR-ENGINE CHECK</span>

| Region | Revenue | Profit | Margin |
|---|---:|---:|---:|
| South | **10,360** | 2,760 | 26.64% |
| North | 2,520 | 765 | 30.36% |

**₹12,880 total, ₹10,360 for South** — Business Intelligence Tools' DAX, Big Data Technologies' Hive,
Big Data Technologies' Spark and this. **Four engines, one set of nine facts.**
</div>

**And the break-even:** Redshift at $1.086/node-hour: 2 nodes is **$1,585.56/month**.
**Break-even against on-demand BigQuery: about 254 TB scanned per month.**
Below that, serverless is cheaper and costs nothing when idle. Above it, a
cluster is cheaper and an extra query is free at the margin. **A calculation,
not a preference.**

<div class="concept" markdown="1">
<span class="label">RESULT</span>

11 rows in, 9 loaded, and the pipeline says where the other two went; South is ₹10,360, as in DAX, Hive and Spark.
</div>


## Experiment 10 — A SageMaker notebook with an IAM role

### 1. Question

Launch a SageMaker notebook, and attach an IAM role and an S3 bucket.

### 2. Aim

Give the notebook a role rather than keys, and know what an idle endpoint costs.

### 3. Steps

**The procedure, on the console and CLI**, `10_sagemaker_notebook.md`:

1. **Create the role first.**
2. **Then the notebook.**
3. **Avoid what not to do.**
4. **Stop it when you are done.**

<div class="formula" markdown="1">
<span class="label">A ROLE IS NOT A USER</span>

| | User | Role |
|---|---|---|
| Credentials | long-lived access key | **temporary, auto-rotated** |
| In a notebook | keys in a file — **bad** | attached; **no keys exist** |
| If leaked | valid until revoked | expires in minutes to hours |

**A SageMaker notebook gets an execution role, so no access key is ever
written to disk.** That is why experiment 10 says "attach IAM role" rather
than "paste your credentials", and "I put my keys in the notebook" is the
answer that loses the marks.
</div>


### 4. Programme

**The procedure, on the console and CLI**, `10_sagemaker_notebook.md`:

{{programme: course-13b-cloud/10_sagemaker_notebook.md}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `10_sagemaker_notebook.md`:

{{not-run: course-13b-cloud/10_sagemaker_notebook.md | it needs a cloud account, and this repository has none}}

<div class="warn" markdown="1">
<span class="label">THE ENDPOINT TRAP</span>

**A forgotten `ml.m5.large` endpoint costs about $70/month.** A training job
ends and stops billing; **an endpoint runs until you delete it**, at hourly
rates, whether or not anything calls it.

**Set a budget alarm on day one, before anything else.**
</div>

The Python model for this experiment, `03_iam_and_account.py`, is shown in full under Experiment 3, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A role's credentials are temporary and never written to disk; a forgotten endpoint costs about $70 a month.
</div>


## Experiment 11 — Train a model on a managed platform

### 1. Question

Build a classification or regression model on a managed ML platform.

### 2. Aim

Train a model, quote the dummy first, save the artefact, and price the instance.

### 3. Steps

**The procedure, on the console and CLI**, `11_sagemaker_train.md`:

1. **Call the SDK.**
2. **See what makes it managed.**
3. **Follow the train.py contract.**
4. **Train on spot.**
5. **Choose the instance.**

**The Python model, which runs**, `11_train_and_automl.py`, for experiments 11 and 14:

1. **Make the data.**
2. **Experiment 11: run the training job.**
3. **Save the artefact, and reload it.**
4. **See what the cloud changes.**
5. **Price the instance.**
6. **Experiment 14: run AutoML.**
7. **List what AutoML cannot do.**
8. **Price the search.**

<div class="formula" markdown="1">
<span class="label">QUOTE THE DUMMY FIRST, ALWAYS</span>

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| `DummyClassifier` | **0.8433** | **0.0000** | 0.5000 |
| GradientBoosting | 0.9467 | 0.8095 | 0.9029 |

**94.67% sounds excellent until you see 84.33% for predicting "never
churns".** The real gain is 10.3 percentage points, and the **F1 of 0.8095
against 0.0000** is what shows the model found anything.

**Machine Learning's argument, and it does not stop being true because the model
trained on somebody else's computer.**
</div>


### 4. Programme

**The procedure, on the console and CLI**, `11_sagemaker_train.md`:

{{programme: course-13b-cloud/11_sagemaker_train.md}}

**The Python model, which runs**, `11_train_and_automl.py`, for experiments 11 and 14:

{{programme: course-13b-cloud/11_train_and_automl.py}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `11_sagemaker_train.md`:

{{not-run: course-13b-cloud/11_sagemaker_train.md | it needs a cloud account, and this repository has none}}

**The Python model, which runs**, `11_train_and_automl.py`, for experiments 11 and 14:

{{output: course-13b-cloud/11_train_and_automl.py}}

**The artefact is the deliverable.** **138,945 bytes**, written to disk, reloaded, and
predicting identically. A SageMaker training job writes exactly this to `s3://bucket/models/`,
and the deploy step reads it back. **Training and serving are separate systems joined by one
file in object storage** — which is why the IAM role in experiment 10 needs `s3:PutObject` on
`models/` and nothing else.

**The instance choice, priced:**

| Instance | $/hour | 10-min job |
|---|---:|---:|
| m5.xlarge | 0.1920 | **0.0320** |
| p3.2xlarge (1 GPU) | 3.0600 | 0.5100 |
| **p4d.24xlarge (8 GPU)** | **32.7726** | **5.4621** |

**171× for the same ten minutes — and gradient boosting on tabular data has
no GPU code path.** It would run at exactly the same speed.

> **"Which instance?" is answered by the algorithm, not by ambition.**

The three times the program prints — the training job, the 25 fits, and one fit — measure this
machine at one moment and differ from run to run. **Corrected:** this page said one fit takes
0.127 s; that was one run's figure.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Gradient boosting reaches 94.67% against the dummy's 84.33%, F1 0.8095 against 0; the artefact reloads and predicts identically.
</div>


## Experiment 12 — An ETL job into a cloud warehouse

### 1. Question

Run a simple ETL job: extract, transform, and load into a cloud warehouse.

### 2. Aim

Build the job in Glue, load Redshift or BigQuery, and reconcile the counts.

### 3. Steps

**The procedure, on the console and CLI**, `12_etl_to_warehouse.md`:

1. **Build a Glue job.**
2. **Run the crawler.**
3. **Load Redshift.**
4. **Load BigQuery.**
5. **Reconcile the counts.**
6. **Orchestrate it.**

<div class="formula" markdown="1">
<span class="label">ETL AGAINST ELT</span>

**ELT won because warehouse compute got cheap and elastic.** Landing raw data
means a transformation bug is fixed by re-running SQL rather than
re-extracting from a production database that may no longer hold the old rows
— **exactly the `DELETE` problem Big Data Technologies found in Sqoop**.
</div>


### 4. Programme

**The procedure, on the console and CLI**, `12_etl_to_warehouse.md`:

{{programme: course-13b-cloud/12_etl_to_warehouse.md}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `12_etl_to_warehouse.md`:

{{not-run: course-13b-cloud/12_etl_to_warehouse.md | it needs a cloud account, and this repository has none}}

The Python model for this experiment, `09_etl_warehouse.py`, is shown in full under Experiment 9, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The same pipeline as Experiment 9, on managed services; ELT won because warehouse compute got cheap.
</div>


## Experiment 13 — Monitoring, alarms and auto-scaling

### 1. Question

Use CloudWatch or Stackdriver to monitor endpoints, set alarms and configure auto-scaling.

### 2. Aim

Simulate a day of traffic, autoscale it, tune the thresholds, and choose what to alarm on.

### 3. Steps

**The procedure, on the console and CLI**, `13_monitoring.md`:

1. **Create an alarm.**
2. **Set the billing alarm first.**
3. **Autoscale an endpoint.**
4. **Read what the runnable half shows.**
5. **Choose the six metrics.**

**The Python model, which runs**, `13_monitoring_autoscale.py`, for experiment 13:

1. **Read a day of traffic.**
2. **Fix the capacity at the peak.**
3. **Autoscale.**
4. **Read it honestly.**
5. **Tune the thresholds.**
6. **Choose what to alarm on.**
7. **Price the day.**

<div class="formula" markdown="1">
<span class="label">THE DAY</span>

A day of traffic: peak **1,000 req/s**, trough **164**; instances serve 150
req/s; the group is 2–12.

| Strategy | Instance-hours | Dropped |
|---|---:|---:|
| fixed at peak (7) | **168** | **0** |
| autoscaled, 70%/40%, cooldown 1 | **129** | **1,014** |
</div>


### 4. Programme

**The procedure, on the console and CLI**, `13_monitoring.md`:

{{programme: course-13b-cloud/13_monitoring.md}}

**The Python model, which runs**, `13_monitoring_autoscale.py`, for experiment 13:

{{programme: course-13b-cloud/13_monitoring_autoscale.py}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `13_monitoring.md`:

{{not-run: course-13b-cloud/13_monitoring.md | it needs a cloud account, and this repository has none}}

**The Python model, which runs**, `13_monitoring_autoscale.py`, for experiment 13:

{{output: course-13b-cloud/13_monitoring_autoscale.py}}

<div class="warn" markdown="1">
<span class="label">AUTOSCALING DROPPED 1,014 REQUESTS AND FIXED CAPACITY DROPPED NONE</span>

The worst hour is **hour 9**: demand jumped to 1,000 against 4 instances,
because **the group was sized for the previous hour**.

> **Autoscaling does not track demand. It CHASES demand, and it is always one
> observation behind.**

That lag is the cost of the 23% saving.
</div>

**The tuning curve:**

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

<div class="warn" markdown="1">
<span class="label">AND READ THE LAST ROW AGAINST FIXED CAPACITY</span>

**188 instance-hours against 168.** Scaling out at 50% with no cooldown drops
nothing — **and costs more than simply buying the peak.**

> **Autoscaling made it MORE expensive.** Chase demand hard enough and the
> group overshoots on the way up and lingers on the way down.
>
> **"Autoscaling saves money" is a claim about a *tuned* autoscaler.**
</div>

**The cooldown row:** 3 ticks gives 4 scaling changes instead of 8, at
**+1,079** dropped requests. A long cooldown stops **flapping** — which costs
boot time and stabilises nothing. *Scale out eagerly, scale in reluctantly.*

**Alarm on the tail:**

```
20 latencies, one of them 900 ms:
  mean 85.0 ms   p50 42.0 ms   p95 87.8 ms   p99 737.5 ms
```

**An alarm on the mean never fires.** Alarm on p95 or p99 — **the tail is
where users live**, and 5% of requests is a lot of users.

<div class="example" markdown="1">
<span class="label">THE METRIC NOBODY SETS</span>

| Metric | Alarm when | The trap |
|---|---|---|
| `ModelLatency` p99 | > 500 ms | the mean hides it; the unit is **microseconds** |
| `Invocation5XXErrors` | > 0 | these are **yours** |
| `Invocation4XXErrors` | > 1% | a **rate**, never a count |
| `EstimatedCharges` | > budget | lags ~6 h, `us-east-1` only |
| **`Invocations` == 0** | for 1 hour | **a dead endpoint still bills** |

**The last row is the one people miss.** An endpoint serving nothing looks
perfect on every performance metric and costs the same as a busy one.
</div>

**And what the day cost:**

| | Per month |
|---|---:|
| fixed at peak, on-demand | $483.84 |
| autoscaled, on-demand | $371.52 |
| fixed, **reserved** (−40%) | $290.30 |
| autoscaled, **spot** (−70%) | **$111.46** |

**The real answer is usually both:** a reserved baseline for the floor, spot
or on-demand for the peak.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Autoscaling saved 23% of instance-hours and dropped 1,014 requests that fixed capacity kept; tuned hard enough, it cost more than fixed capacity.
</div>


## Experiment 14 — AutoML

### 1. Question

Use a cloud AutoML service for a prediction task.

### 2. Aim

Run a model search, read its leaderboard, and see what it does not do.

### 3. Steps

**The procedure, on the console and CLI**, `14_automl.md`:

1. **Run SageMaker Autopilot.**
2. **Or Vertex AI AutoML.**
3. **Or Azure Automated ML.**
4. **See what they do.**
5. **And what they do not.**
6. **Read the explainability report.**

<div class="formula" markdown="1">
<span class="label">AUTOML, ACTUALLY RUN</span>

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
</div>


### 4. Programme

**The procedure, on the console and CLI**, `14_automl.md`:

{{programme: course-13b-cloud/14_automl.md}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `14_automl.md`:

{{not-run: course-13b-cloud/14_automl.md | it needs a cloud account, and this repository has none}}

<div class="warn" markdown="1">
<span class="label">AND THE TOP TWO ARE INSIDE THE NOISE</span>

**0.9334 against 0.9288 is a gap of 0.0047, with standard deviations of
0.0210 and 0.0196.** Declaring a winner is not supported by the data, and
**"AutoML picked X" is not a reason to prefer X**.
</div>

**What the search costs.** One fit here takes a fraction of a second — too small to cost
anything. **Scale to a realistic four minutes per fit:**

| Search | Fits | Compute | m5.xlarge |
|---|---:|---:|---:|
| this search | 25 | 1.7 h | $0.32 |
| a modest managed search | 250 | 16.7 h | $3.20 |
| **a full AutoML run** | **2,000** | **133.3 h** | **$25.60** |

**A straight multiple of one fit — exactly 2,000×** — because that is all it
is. And managed services charge a premium on top.

<div class="example" markdown="1">
<span class="label">WHAT AUTOML DOES NOT DO</span>

decide the target · notice leakage · tell you the base rate matters more ·
know last year's data no longer applies · choose a threshold that fits the
business cost · explain a prediction · notice unfairness

**Every one of those is the actual job.** AutoML automates the afternoon and
leaves the weeks untouched.
</div>

The Python model for this experiment, `11_train_and_automl.py`, is shown in full under Experiment 11, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Five candidates, 25 real fits: random forest leads gradient boosting by 0.0047, inside the noise.
</div>


## Experiment 15 — Deploy the model as a REST endpoint

### 1. Question

Deploy a trained ML model as a REST API endpoint.

### 2. Aim

Serve the model over HTTP, check health, predictions and errors, and measure latency and batching.

### 3. Steps

**The procedure, on the console and CLI**, `15_deploy.md`:

1. **Deploy.**
2. **Invoke it.**
3. **Follow the container contract.**
4. **Choose real-time, serverless or batch.**
5. **Delete it.**
6. **Monitor it.**

**The Python model, which runs**, `15_deploy_endpoint.py`, for experiment 15:

1. **Train the model, and save it.**
2. **Serve it.**
3. **Check its health.**
4. **Ask for a prediction.**
5. **Send a batch.**
6. **Send bad requests.**
7. **Measure the latency.**
8. **Batch, against one at a time.**
9. **Read the metrics.**
10. **Compare with a managed endpoint.**

<div class="formula" markdown="1">
<span class="label">THE EQUALITY THAT IS THE DEPLOYMENT TEST</span>

```
artefact loaded from disk: 138,945 bytes

GET /ping        -> 200 {'status': 'healthy', 'model_loaded': True}
POST /invocations (3 rows)  -> 200
  predictions   : [0, 0, 0]
  probabilities : [0.015383, 0.008643, 0.014492]
POST /invocations (300 rows) -> 200, accuracy 0.9467
```

**The endpoint's answers are identical to calling the model in-process.**
Serving must not change predictions — and **a preprocessing step that lives in
your notebook rather than in the pipeline is exactly how it does.**
</div>


### 4. Programme

**The procedure, on the console and CLI**, `15_deploy.md`:

{{programme: course-13b-cloud/15_deploy.md}}

**The Python model, which runs**, `15_deploy_endpoint.py`, for experiment 15:

{{programme: course-13b-cloud/15_deploy_endpoint.py}}

### 5. Execution and Results

**The procedure, on the console and CLI**, `15_deploy.md`:

{{not-run: course-13b-cloud/15_deploy.md | it needs a cloud account, and this repository has none}}

**The Python model, which runs**, `15_deploy_endpoint.py`, for experiment 15:

{{output: course-13b-cloud/15_deploy_endpoint.py}}

<div class="warn" markdown="1">
<span class="label">/PING MUST NOT RUN THE MODEL</span>

**A health check that does real inference marks the container unhealthy
whenever the model is merely slow — and the platform then kills a container
that was working.** A self-inflicted outage, and a classic one.
</div>

**Error handling, which is most of a real endpoint:**

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

**Latency, over 200 real requests, and the batching result**, are the timed lines above: they
measure this machine at one moment and differ from run to run. What does not change is their
shape — p99 above p50 even on an idle machine serving one model, and one request of 100 rows far
faster than 100 requests of one row, none of the difference being the model: it is per-request
overhead, HTTP, JSON parsing, and a NumPy call whose fixed cost is paid 100 times instead of
once. **Corrected:** this page gave "p99 is 1.8× p50" and "37×" as if fixed; they were one
run's figures, and three runs made here gave batching factors of 47×, 57× and 68×. Under load the p99 ratio grows — which is why experiment 13's alarm is on p99.

> **If you are scoring a million rows, calling an endpoint a million times is
> the expensive way to do arithmetic.**

**What SageMaker adds that this server does not have:**

| | This script | A managed endpoint |
|---|---|---|
| TLS | no | terminated for you |
| Authentication | **NONE — anyone** | IAM-signed requests |
| Load balancing | one process | across instances and AZs |
| Autoscaling | no | on `InvocationsPerInstance` |
| Blue/green | no | traffic shifted gradually |
| **Cost** | electricity | **$70/month, called or not** |

**Deleting the endpoint is a step in the experiment, not an afterthought.**

**Changed:** the program printed the port it listened on, which the system picks afresh on
every run; it now says so.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The endpoint's predictions equal the model's in-process; bad input gets a 4xx, never a 5xx; batching beat one row per request many times over.
</div>


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

Plus the audit: **14 Markdown files, every one carrying NOT EXECUTED**, each naming the service
it needs.

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
- **The 500× BigQuery difference**, and naming it as Big Data Technologies' column
  projection and partition pruning saving money instead of time.
- **The 254 TB break-even.** Serverless against provisioned as a calculation.
- **"171× for the same speed."** Instance choice as an engineering decision.
- **"The AutoML gap is inside the noise."** 0.0047 against standard
  deviations of 0.02.
- **"Autoscaling made it more expensive."** 188 instance-hours against 168 —
  reporting the result that contradicts the slogan.
- **Batching against one row per request**, argued with the number your run measured.
- **₹10,360 from four engines.** The check that makes the rest believable.
