# Unit 2 — Virtualization and Deployment Models

**Syllabus topics:** Concept and importance of virtualization. Types of
virtualization: application, network, desktop, storage, server, data. Cloud
deployment models: public, private, community, hybrid. Role of cloud
computing in data science. Advantages of cloud in machine learning.

---

## 2.1 Why virtualization is the enabling technology

### 🎯 The one sentence

**You cannot hand back half a physical server. You can hand back half a
virtual one.**

Everything in Unit 1 — on-demand self-service, elasticity, measured service —
requires that a physical machine be divisible, and virtualization is what
divides it. **The cloud is not possible without it**, which is why it is the
first thing Unit 2 covers.

### The three things a hypervisor gives you

| Property | What it means | Why it matters |
|---|---|---|
| **Partitioning** | one machine runs many isolated guests | multi-tenancy, and therefore pooling |
| **Isolation** | a crash or a breach in one guest does not reach another | you can sell to strangers |
| **Encapsulation** | a whole machine is **a file** | snapshots, cloning, live migration, images |

**Encapsulation is the underrated one.** A machine that is a file can be
copied, versioned, snapshotted before a risky change, moved to another host
while running, and launched a thousand times from one image. *An AMI is a
file.* That is why an EC2 instance starts in forty seconds.

---

## 2.2 Type 1 and type 2 hypervisors

| | **Type 1 (bare metal)** | **Type 2 (hosted)** |
|---|---|---|
| Runs on | **the hardware directly** | on top of a host OS |
| Examples | ESXi, Hyper-V, KVM, Xen, **AWS Nitro** | VMware Workstation, VirtualBox |
| Overhead | a few percent | noticeably more |
| Used for | **datacentres, the cloud** | a laptop, experiment 1 |
| Boots | instead of an OS | as an application |

**Every EC2 instance, Azure VM and GCE instance is a guest on a type 1
hypervisor.** The cloud is experiment 1 at rack scale, with the wizard
replaced by an API call.

### 📖 Containers, which the syllabus omits and the exam may not

| | **Virtual machine** | **Container** |
|---|---|---|
| Virtualizes | **hardware** | **the operating system** |
| Contains | a full guest OS | just the process and its libraries |
| Size | gigabytes | megabytes |
| Starts in | tens of seconds | **milliseconds** |
| Isolation | **strong** — separate kernels | weaker — a shared kernel |
| Runs a different OS | yes | **no** — same kernel family |

**A container is not a lightweight VM; it is an isolated process.** It shares
the host kernel, which is why it starts instantly and why a kernel
vulnerability crosses container boundaries in a way it does not cross VM
boundaries.

**Both, in practice:** cloud providers run containers *inside* VMs, so
tenants get the VM's isolation and the container's density.

---

## 2.3 The six types of virtualization

The syllabus names six. Learn them by **what is being pretended**.

| Type | The pretence | Example |
|---|---|---|
| **Server** | one machine looks like many | ESXi, KVM, EC2 |
| **Storage** | many disks look like one pool | SAN, RAID, EBS |
| **Network** | one physical network looks like many | **VLAN, VPC**, SDN |
| **Desktop** | your desktop runs elsewhere | VDI, Citrix, WorkSpaces |
| **Application** | an app runs without being installed | Docker, App-V, ThinApp |
| **Data** | many sources look like one database | Denodo, federated query |

### 🎯 The two that matter most in this course

**Network virtualization** is what a **VPC** is, and it is why multi-tenancy
is safe. Your instances see a private network with your own address range,
your own subnets and your own routing — running over the same physical
switches as thousands of other tenants. **Without it, "shared pool" would mean
"shared broadcast domain", and the cloud would be unsellable.**

**Data virtualization** is the one students skip, and it is the most relevant
to data science: a query layer that presents several sources — a warehouse, a
lake, an operational database — as one schema, without copying anything.
**Athena over S3, BigQuery external tables and Denodo are all this.** The
trade is obvious once stated: no copy means no staleness and no ETL, but the
query runs at the speed of the slowest source.

---

## 2.4 Overcommitment, and where it breaks

### 🔢 Measured, on a 32 GB / 8 vCPU host

Four guests, in
`01_vm_and_hosting.py`:

| VM | RAM | vCPU | Active |
|---|---:|---:|---:|
| web-1 | 8 GB | 4 | 35% |
| web-2 | 8 GB | 4 | 30% |
| db-1 | 16 GB | 4 | 90% |
| batch | 16 GB | 8 | 20% |

```
allocated RAM  : 48 GB on a 32 GB host   (1.50x)
allocated vCPU : 20 on 8                 (2.50x)
RAM actually touched     : 22.8 GB
reclaimed by ballooning  : 25.2 GB
swapping                 : 0.0 GB
```

**48 GB allocated on a 32 GB host, and nothing is swapping**, because the
guests only *touch* 22.8 GB. Overcommit works on the same bet an airline
makes, and it is why a provider can sell more capacity than it owns.

### ⚠️ Then the batch job wakes up

```
batch: 20% -> 95% active
RAM actually touched : 34.8 GB
swapping             : 2.8 GB
```

**Now every guest is slow — not just the batch job.**

### 🎯 The asymmetry to remember

> **CPU overcommit degrades gracefully. Memory overcommit fails as a cliff.**

CPU is **time-sliced**, so twice the demand means everyone runs at half speed.
Memory is not: a page is either resident or it is on disk, and the difference
is a factor of thousands.

**That is the "noisy neighbour" problem**, and it is why cloud instance types
quote **dedicated memory** and only **burstable CPU**. A `t3.micro` shares CPU
credits with neighbours; its gigabyte of RAM is its own.

---

## 2.5 The four deployment models

| | **Public** | **Private** | **Community** | **Hybrid** |
|---|---|---|---|---|
| Who owns it | a provider | **one organisation** | a group with shared concerns | both |
| Who uses it | anyone | that organisation | that group | that organisation |
| Where | provider's datacentre | on-prem **or** hosted | either | both |
| Cost model | **operational, per second** | **capital**, plus staff | shared capital | both |
| Elasticity | **effectively unlimited** | bounded by what you bought | bounded | burst to public |
| Examples | AWS, Azure, GCP | VMware/OpenStack estate | NHS, government, banking clouds | most large enterprises |

### 🎯 The distinction that is actually tested

**"Private cloud" does not mean "on our premises".** A private cloud is
**single-tenant** — the hardware serves one organisation. AWS Outposts and
dedicated hosts are private clouds in someone else's building.

**And a virtualized datacentre with a ticket queue is not a private cloud at
all** — it fails on-demand self-service, as Unit 1's practice problem sets out.

### Hybrid, and why almost everyone is there

**Hybrid is the default outcome, not a design choice.** Organisations arrive
at it because:

- some data cannot legally leave the country or the building
- a mainframe or a licensed appliance cannot be moved
- a five-year-old capital purchase has not finished depreciating
- **cloud bursting** — steady load on-prem, peaks in the public cloud

**The hard part of hybrid is not compute, it is data gravity.** Egress
charges (Unit 3) mean that once a dataset is large and in one place, the
compute comes to it — and a hybrid architecture that moves terabytes across
the boundary daily is expensive in a way the design diagram does not show.

### ⚠️ The community cloud is not a fifth wheel

It is genuinely used where a **regulator** is the common concern: government
clouds (AWS GovCloud), health-sector clouds, banking consortia. The shared
requirement is **compliance certification**, which is expensive enough that
sharing the cost is the whole reason.

---

## 2.6 The role of cloud computing in data science

### 🎯 The four things that actually change

**1. Storage stops being a constraint on the question you ask.** On-prem, "we
only keep 90 days" is a disk decision. At $0.023/GB-month, keeping everything
is cheap enough that the constraint moves to whether it is *worth* querying.

**2. Compute is elastic and matched to the job.** A model that needs 64 GB
for four hours a month needs a 64 GB machine for four hours, not for a year.

**3. Managed services remove undifferentiated work.** Nobody's competitive
advantage is patching PostgreSQL.

**4. Cost becomes visible per experiment.** That is a double edge: it enables
"was this worth it?" and it also means a careless query has a price.

### ⚠️ What the cloud does not fix

| Problem | Still yours |
|---|---|
| The data is wrong | **entirely** |
| Nobody knows what the columns mean | **entirely** |
| The model is unfair | **entirely** |
| The target leaks | **entirely** |
| The base rate is 85% and accuracy is meaningless | **entirely** |

**A bad model trained on eight GPUs is still a bad model.** The runnable half
of experiment 11 makes this concrete: a `DummyClassifier` scores **84.33%**
and the trained model **94.67%**, and no amount of hardware moves the
baseline.

---

## 2.7 Advantages of cloud in machine learning

| Advantage | The mechanism | The catch |
|---|---|---|
| **Elastic training capacity** | rent a GPU for an hour | **only helps if the algorithm uses one** |
| **Managed platforms** | SageMaker, Vertex, Azure ML | lock-in, and a premium on compute |
| **Pre-trained services** | vision, speech, translation APIs | a black box you cannot audit |
| **AutoML** | search over models, automatically | it automates the easy part |
| **Deployment as a call** | `estimator.deploy()` | **the endpoint bills until deleted** |
| **Reproducibility** | jobs are declarative and logged | only if you use it that way |
| **Collaboration** | shared notebooks, shared data | governance becomes essential |

### 🔢 The catch that is measured

From `11_train_and_automl.py`,
for the same ten-minute job:

| Instance | $/hour | 10 min |
|---|---:|---:|
| m5.xlarge | 0.1920 | **0.0320** |
| p3.2xlarge (1 GPU) | 3.0600 | 0.5100 |
| p4d.24xlarge (8 GPU) | **32.7726** | **5.4621** |

**The 8-GPU box costs 171× the general-purpose one — and gradient boosting on
tabular data has no GPU code path.** It would run at the same speed for 171
times the price.

> **"Which instance?" is answered by the algorithm, not by ambition.**

GPUs earn their price on **dense matrix multiplication** — deep learning.
Tree-based models on tabular data do not use them.

### 🎯 And the argument to give in an exam

The cloud's real contribution to machine learning is not speed. It is that
**training becomes reproducible, deployment becomes routine, and cost becomes
visible**. Those three change how teams work; a faster GPU changes how long
you wait.

---

## Practice problems

**1. A hypervisor host has 64 GB of RAM. You want to run ten VMs with 8 GB
each. Is that possible, and what determines whether it works?**

**It is possible to allocate** — 80 GB on a 64 GB host, a 1.25× overcommit —
and whether it *works* depends on the **working set**, not the allocation.

- If the guests collectively touch under about 60 GB, ballooning and page
  sharing reclaim the difference and nothing swaps.
- If they touch more, the host swaps, and **every guest slows down, not just
  the greedy one**.

**The measured version:** 48 GB allocated on 32 GB ran fine at 22.8 GB
touched, and began swapping 2.8 GB when one guest went from 20% to 95%
active.

**And CPU is different:** 20 vCPUs on 8 physical is fine, because time-slicing
degrades gracefully.

**2. A hospital must keep patient records in the country and wants to run
large analytics jobs. Which deployment model, and where does each piece go?**

**Hybrid**, with the boundary drawn by the legal constraint rather than by
technology.

- **Private (or in-country public region):** the identifiable patient records.
- **Public:** the analytics compute, operating on **de-identified or
  aggregated** extracts.
- **The boundary itself:** an anonymisation or tokenisation step, which is the
  actual engineering.

**The trap:** if the analytics need row-level identifiable data, the boundary
cannot be drawn there and the whole workload stays private. And **data
gravity** applies — if the extract is terabytes and moves daily, egress makes
the hybrid design expensive in a way the diagram hides.

**A community cloud** is also a real answer if a health-sector cloud with the
right certification exists in-country, and saying so is worth the mark.

**3. Explain why CPU can be overcommitted 4:1 but memory usually cannot.**

**CPU is a rate; memory is a quantity.**

A vCPU is a *scheduling entity*. Four vCPUs on one core means each gets
roughly a quarter of the core's time when all are busy — everyone is slower,
and everyone still runs. **Degradation is linear and graceful.**

A page of memory is either **resident** or **on disk**. There is no "half
resident". When the working set exceeds physical RAM, the hypervisor swaps,
and a swapped page costs roughly 100,000× a resident one. **Degradation is a
cliff.**

**Mitigations exist and are limited:** ballooning reclaims pages a guest is
not using, transparent page sharing deduplicates identical pages, and memory
compression buys a little. All of them fail once the *active* set genuinely
exceeds RAM.

**4. Your team wants to move a 40 TB dataset to the cloud for analysis. What
do you need to think about before the technical design?**

**Egress, in both directions, and data gravity.**

1. **Ingress is free**, so getting it in costs transfer time, not money. At
   1 Gbit/s, 40 TB takes about **four days** of saturated link. AWS Snowball
   exists for exactly this.
2. **Egress is not free.** Getting it back out costs roughly 40,000 GB ×
   $0.09 ≈ **$3,600**, once. That is not ruinous, but it is the mechanism of
   lock-in: your data is not held hostage, it is simply expensive to move.
3. **So the compute must come to the data.** Run the analysis in the region
   holding the bucket, and same-region S3-to-EC2 transfer is free.
4. **And storage class matters at this size.** 40 TB in Standard is about
   **$942/month**; in Glacier Flexible about **$147** — but with a 90-day
   minimum and a retrieval fee that reverses the saving if you touch it often.

**The pre-technical question is: how often will this be read?** That single
answer determines the class, the architecture and the bill.

**5. When is a GPU instance the wrong choice for a machine-learning job?**

**Whenever the algorithm has no GPU code path**, which covers most tabular
data science:

- scikit-learn's tree ensembles, linear models, clustering
- XGBoost/LightGBM in their CPU modes
- any pandas-based feature engineering

**And even when it does have one**, a GPU is wrong if:

- the dataset is small enough that **data transfer to the GPU dominates**
- the model is tiny, so the GPU is idle between kernel launches
- you are doing **inference** on single requests, where a CPU is cheaper per
  prediction

**The measured figure:** 171× the hourly price for a job that would run at
the same speed. Choosing an instance is an engineering decision with a price
attached, and "we used GPUs" is not by itself evidence of anything.

---

## Exam questions from this unit

**Two marks**

1. Why is virtualization necessary for cloud computing?
2. Distinguish type 1 from type 2 hypervisors.
3. Name the six types of virtualization.
4. What is network virtualization, in the cloud?
5. Name the four deployment models.
6. Does "private cloud" mean on-premises?
7. Give one difference between a VM and a container.
8. Why can CPU be overcommitted more safely than memory?

**Five marks**

1. Explain the three properties a hypervisor provides and why encapsulation
   matters.
2. Explain the six types of virtualization with an example of each.
3. Compare the four deployment models on ownership, cost and elasticity.
4. Explain overcommitment and the difference between CPU and memory
   overcommit.
5. Explain the advantages of the cloud for machine learning, and two limits.

**Ten marks**

1. Explain virtualization in full — hypervisor types, the six kinds, and
   overcommitment — and say why the cloud depends on it.
2. Compare the four deployment models and recommend one for a bank, a
   university and a startup, with justification.

---

## Mistakes that cost marks

- **Saying a container is a lightweight VM.** It virtualizes the OS, not the
  hardware, and shares the kernel.
- **Equating private cloud with on-premises.** Private means single-tenant.
- **Calling a ticket-driven virtualized datacentre a private cloud.**
- **Forgetting network virtualization** when listing the six types — the VPC
  is the one that makes multi-tenancy safe.
- **Claiming memory overcommit works like CPU overcommit.** One degrades, the
  other falls off a cliff.
- **Saying the cloud makes models better.** It makes training reproducible,
  deployment routine and cost visible.
- **Recommending GPUs for tabular machine learning.** 171× the price for the
  same speed.
- **Ignoring egress in a hybrid design.** Data gravity is the reason hybrid
  architectures cost more than they look.
