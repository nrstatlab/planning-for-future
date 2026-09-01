# Course 13 B — Cloud Computing for Data Science

**Semester V**

**This is a Track B course**, paired with
Course 12 B (Big Data Technologies). Take one
track and you take it for Semester VI too.

---

## The one thing to understand before anything else

**The cloud is not "someone else's computer". It is someone else's computer
billed by the second, and that changes what is worth building.**

Every technical decision in this course is downstream of one economic fact:

> **Capacity you no longer need can be given back.**

That is the whole thing. It is why virtualization matters (you cannot hand
back half a physical server), why autoscaling exists, why serverless exists,
why storage has six price tiers, and why "just leave it running" is the most
expensive habit in the subject.

| The old assumption | What replaces it |
|---|---|
| Buy for the peak, own it for three years | **Rent the peak, hourly** |
| Capacity is a capital decision | **Capacity is an API call** |
| An idle server is sunk cost | **An idle server is a bill** |
| Storage is a disk you bought | **Storage is six tiers with penalties** |
| Security is a perimeter | **Security is identity** |

### ⚠️ The honest framing

**This course names specific products, and the products change.** SageMaker
Studio replaced SageMaker Notebooks, Stackdriver became Cloud Operations, and
the syllabus's product list will read as dated within a few years.

**What does not change** is underneath: service models, virtualization,
storage classes, identity and policy evaluation, the batch/stream split, and
the cost arithmetic. Learn those as permanent and the products as examples,
and say so in the exam.

---

## What runs here, and what does not

**There is no cloud account for this repository, and none will be created.**
Signing up requires a payment card and accepts a billing relationship, which
is not something a study repository should do on anyone's behalf.

So this course is the most explicitly split of the ten:

| Runs for real | Documented, **NOT EXECUTED** |
|---|---|
| **IAM's policy evaluation algorithm**, implemented and exercised | AWS, Azure, GCP consoles |
| **Object-store key semantics** — prefixes, no directories, copy-plus-delete | S3, Blob, Cloud Storage |
| **All the pricing arithmetic** — storage classes, egress, per-TB, per-node-hour | the billing console |
| **Hypervisor overcommit**, and where it breaks | VMware Workstation |
| **A real web server** serving a real page over TCP | Apache on a cloud VM |
| **A real ETL pipeline** into a real columnar warehouse | Glue, Redshift, BigQuery |
| **An autoscaling control loop**, measured honestly | CloudWatch |
| **A real model, and a real AutoML search** | SageMaker, Vertex, Azure ML |
| **A real HTTP endpoint** serving that model, called over the network | a SageMaker endpoint |

**That is more than it sounds**, because most of what this course teaches is
not proprietary. IAM's three evaluation rules, the fact that an object store
has no directories, and the arithmetic that decides between serverless and
provisioned are all implementable — and all implemented, in
`labs/course-13b-cloud/`.

Every file that cannot run says **`*** NOT EXECUTED ***`** at the top, names
the service it needs, and points at the runnable half.
`tools/run_cloud_labs.py` asserts the
marker is still there.

---

## Course objectives (verbatim)

1. Introduce the fundamentals of cloud computing and its role in data science.
2. Provide understanding of virtualization, service, and deployment models.
3. Familiarize students with cloud storage, data management, and databases.
4. Expose students to cloud-based big data and machine learning platforms.
5. Train students in building, deploying, and monitoring ML pipelines on the
   cloud.

## The five units

| Unit | Question it answers |
|---|---|
| **[1](unit-1.md)** | What is the cloud, and what are you actually renting? |
| **[2](unit-2.md)** | How is one machine turned into many, and whose machine is it? |
| **[3](unit-3.md)** | Where does the data live, and what does each choice cost? |
| **[4](unit-4.md)** | What does a managed ML platform actually give you? |
| **[5](unit-5.md)** | How do you train, deploy and keep it working? |

**Unit 3 is the load-bearing one.** Storage decisions are where cloud bills
are made and lost, and they are the most examinable arithmetic in the course.

---

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 15 experiments
- `labs/course-13b-cloud/` — the code, and the runner that asserts every figure
  these notes quote
- `data/course-13b-cloud/` — **practice datasets**, CSV: `iam-policies.csv`, `storage-costs.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.

## Cross-course connections

| From | To | What is shared |
|---|---|---|
| **Course 11 (BI)** | Unit 3, experiment 12 | The **same nine-row star schema**, imported not copied. **₹10,360** for South is now produced by four engines. |
| **Course 12 B (Big Data)** | Units 3 and 4 | Column projection and partition pruning saved *time* there; here they save **money**, on the same mechanism. |
| **Course 12 A (ML)** | Units 4 and 5 | Identical scikit-learn. The cloud changes the packaging, not the algorithm — and the base-rate argument survives intact. |
| **Course 10 (MongoDB)** | Unit 3 | Cosmos DB's consistency levels are CAP as a dropdown, with a price per level. |
| **Course 5 (DBMS)** | Unit 3 | A cloud warehouse is columnar, indexless, and billed per byte scanned. Every row of that comparison is a departure from Course 5. |

---

## Textbooks

The syllabus gives a single combined **Text / Reference** list:

- Nayyar, *Handbook of Cloud Computing*, BPB Publications, 2019 — the closest
  match to Units 1–3.
- Velte, Velte & Elsenpeter, *Cloud Computing: A Practical Approach*,
  McGraw Hill.
- Gift & Deza, *Cloud Computing for Data Analysis*, Pragmatic AI Labs — the one
  that actually addresses Units 4 and 5.
- Mishra, *Machine Learning in the AWS Cloud: Amazon SageMaker*, Wiley.

> ### ⚠️ Item 4 of the list is empty
>
> The prescribed list runs 1, 2, 3, **4**, 5 with nothing beside the 4 — a
> title has been lost, and the four books above are items 1, 2, 3 and 5. See
> review finding **D22**.
>
> None of the four is free. **AWS, Azure and Google Cloud all publish their own
> documentation and free tiers**, and for Units 4 and 5 the vendor
> documentation is more current than any of these books.

## How to study this course

1. **Learn the three service models by what YOU manage**, not by examples.
   The examples change; the boundary does not.
2. **Do the cost arithmetic by hand.** 1 TB egress, 1 TB in each storage
   class, a serverless-vs-provisioned break-even. These are the calculations
   that get examined.
3. **Learn IAM's three rules and be able to apply them.** Explicit deny wins;
   otherwise allow; otherwise deny. Almost every access question is these
   three.
4. **Learn one comparison table per unit.** IaaS/PaaS/SaaS; the four
   deployment models; block/file/object; real-time/serverless/batch.
5. **Run the labs.** Seven programs, including a real web server, a real ETL
   into a real warehouse, and a real model served over a real HTTP endpoint.

### 💡 The two sentences that carry the course

> **Capacity you no longer need can be given back.** That is why the cloud
> exists.
>
> **Nothing you forget to switch off will switch itself off.** That is why
> cloud bills surprise people, and it is worth a mark in almost any question
> about cost.
