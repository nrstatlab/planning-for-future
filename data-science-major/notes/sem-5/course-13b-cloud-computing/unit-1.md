# Unit 1 — Introduction to Cloud Computing

**Syllabus topics:** Definition and evolution of cloud computing.
Service-Oriented Architecture (SOA) and web services. Utility and grid
computing concepts. Characteristics of cloud computing. Cloud computing
architecture: front-end, back-end, networking, delivery models. Cloud service
models: SaaS, PaaS, IaaS. Continuous delivery using PaaS.

---

## 1.1 Definition and scope of cloud computing

### 🎯 The definition worth memorising

The NIST definition is the one examiners expect, and it is genuinely good:

> Cloud computing is a model for enabling **ubiquitous, convenient,
> on-demand network access** to a **shared pool of configurable computing
> resources** that can be **rapidly provisioned and released** with **minimal
> management effort or service provider interaction**.

**Learn the four emphasised phrases**, because each one is a design claim you
can test a service against.

### 💡 And the sentence that explains why any of it matters

> **Capacity you no longer need can be given back.**

You could always rent a server. What was new in 2006 was giving it back an
hour later and stopping paying. Every characteristic below is a consequence.

---

## 1.2 The evolution of cloud computing — where it came from

| Era | Idea | What survived |
|---|---|---|
| 1960s | **Time-sharing** — one mainframe, many terminals | the economics: share an expensive machine |
| 1990s | **Grid computing** — many machines, one scientific problem | job scheduling, federation |
| 1990s | **Utility computing** — compute billed like electricity | **the billing model** |
| 2000s | **Virtualization** matures (VMware, Xen) | **the enabling technology** |
| 2002–06 | Amazon S3 and EC2 | the modern cloud |

### 🎯 Utility and grid computing, which the syllabus names explicitly

**Utility computing** is the *idea* — compute as a metered utility, like
electricity: you do not own a generator, you do not size one, and you pay for
what you draw. **The cloud is utility computing that finally worked**, because
virtualization made the meter fine-grained enough.

**Grid computing** is *many machines cooperating on one large problem*,
usually across institutions (SETI@home, the LHC computing grid).

| | **Grid** | **Cloud** |
|---|---|---|
| Purpose | one big scientific problem | **many unrelated tenants** |
| Ownership | federated, several institutions | **one provider** |
| Resources | heterogeneous | homogeneous, virtualized |
| Billing | none, or an allocation | **per second** |
| Elastic | no — you queue | **yes** |

**The examinable difference: a grid shares work; a cloud sells capacity.**

### ⚠️ Why time-sharing is not just a historical note

Time-sharing and cloud computing are the same economic bet — an expensive
machine is cheaper when shared — separated by the technology that makes
sharing *safe*. **Virtualization is what changed**, and that is why Unit 2
sits where it does.

---

## 1.3 Characteristics of cloud computing — the five essential ones

NIST lists five, and each has a failure mode worth knowing.

| Characteristic | What it means | When it is not true |
|---|---|---|
| **On-demand self-service** | you provision without asking a human | an internal "cloud" with a ticket queue |
| **Broad network access** | reachable over standard protocols | a service needing a special client |
| **Resource pooling** | multi-tenant, location-independent | dedicated hardware you rented |
| **Rapid elasticity** | scale out and **back in**, quickly | you can add nodes but not remove them |
| **Measured service** | metered, transparent, per unit | a flat monthly fee |

### 🎯 Elasticity is the one people get wrong

**Elasticity is not scalability.** Scalability is *can it get bigger*.
Elasticity is *can it get bigger and then smaller again, automatically,
without a human*.

A system that scales out and never scales back in has **scalability without
elasticity**, and it costs you the peak all day. Course 13 B's experiment 13
measures exactly that.

### ⚠️ "We have a private cloud" is often false

A virtualized datacentre where provisioning takes a ticket and two days has
**resource pooling** and nothing else. It is virtualization, which is useful,
and calling it a cloud is marketing. **Test any claim against the five
characteristics** — that is what they are for.

---

## 1.4 SOA and web services

### 📖 What SOA actually says

**Service-Oriented Architecture** decomposes a system into services that:

- are **loosely coupled** — one can be replaced without touching the others
- expose a **contract**, not an implementation
- are **discoverable** and reusable
- communicate over a **network**, in a standard format

**The cloud is SOA industrialised.** S3 is a service with a contract; you have
no idea what runs it, and that is the point.

### The web-services stack, and what replaced it

| Era | Protocol | Format | Contract | Discovery |
|---|---|---|---|---|
| **SOAP** (1998–) | SOAP over HTTP | XML | **WSDL** | UDDI |
| **REST** (2000–) | HTTP verbs | JSON | OpenAPI | none, mostly |
| **gRPC** (2015–) | HTTP/2 | Protobuf | `.proto` | service mesh |

### 🎯 Why REST won, in one line

**SOAP put the semantics in the envelope; REST put them in HTTP.** A REST API
uses `GET`, `POST`, `PUT`, `DELETE` and HTTP status codes, so every cache,
proxy, load balancer and browser already understands it. SOAP tunnelled
everything through `POST` and had to reinvent the rest.

**And it matters for this course** because every cloud API — including the
model endpoint in experiment 15 — is REST over HTTPS, with the status codes
carrying real meaning. `4xx` is your caller's fault; `5xx` is yours.

---

## 1.5 Cloud computing architecture

### 📖 The four parts the syllabus names — front-end, networking, back-end, delivery models

The **front-end** is what you hold; the **back-end** is what the provider runs; the network joins them; and the delivery models say how the whole thing is packaged.

```
   FRONT END                NETWORK                 BACK END
 ┌──────────────┐      ┌──────────────┐      ┌─────────────────────┐
 │ browser      │      │ the internet │      │ compute (VMs)       │
 │ CLI / SDK    │◄────►│ CDN, DNS     │◄────►│ storage             │
 │ mobile app   │      │ load balancer│      │ databases           │
 │ API client   │      │ VPC          │      │ the CONTROL PLANE   │
 └──────────────┘      └──────────────┘      └─────────────────────┘
```

- **Front end** — whatever you hold: the console, the CLI, an SDK, an app.
- **Network** — the internet, plus the provider's own: DNS, CDN, load
  balancers, and the **VPC** that isolates your resources from other tenants'.
- **Back end** — the servers, storage and databases, plus the **control
  plane**: the software that provisions, meters and bills.
- **Delivery models** — how it is packaged, which is §1.6 and §2.3.

### 🎯 The control plane is the actual product

Anyone can rack servers. **What AWS sells is the API that turns "I want a
machine" into a running machine in 40 seconds, meters it per second, and
charges you.** The control plane is why "someone else's computer" is a
misleading description.

**The practical consequence:** the control plane and the data plane fail
independently. An EC2 instance keeps serving traffic during an API outage;
you simply cannot launch a new one. That distinction explains most cloud
status-page reports.

---

## 1.6 The three service models

### 🎯 Learn them by WHO MANAGES WHAT

Examples change. The boundary does not.

| Layer | On-premises | **IaaS** | **PaaS** | **SaaS** |
|---|---|---|---|---|
| Application | you | you | **you** | provider |
| Data | you | you | **you** | provider |
| Runtime | you | you | provider | provider |
| Middleware | you | you | provider | provider |
| OS | you | **you** | provider | provider |
| Virtualization | you | provider | provider | provider |
| Servers | you | provider | provider | provider |
| Storage | you | provider | provider | provider |
| Networking | you | provider | provider | provider |

**Read the table by finding the line where "you" stops.**

- **IaaS** — you get a machine. You patch the OS. *EC2, Azure VMs, Compute
  Engine.*
- **PaaS** — you get a runtime. You deploy code. *App Engine, Elastic
  Beanstalk, Heroku, Azure App Service.*
- **SaaS** — you get an application. You use it. *Gmail, Salesforce, Office
  365.*

### 💡 The pizza analogy, which is worth the marks

| | You do |
|---|---|
| **On-prem** | make it at home — everything |
| **IaaS** | take-and-bake — they make it, you bake it |
| **PaaS** | delivery — they cook and deliver, you supply the table and drinks |
| **SaaS** | eat at the restaurant |

**The dividing question is always: what is the smallest thing you still have
to look after?**

### ⚠️ The "aaS" the syllabus adds later

Unit 4 names **AIaaS** and **GPUaaS**, and they are not new layers — they are
**SaaS for a model** and **IaaS for a GPU** respectively. Saying that is worth
more than treating them as a separate taxonomy.

### The trade, stated plainly

| | Control | Operational burden | Lock-in |
|---|---|---|---|
| IaaS | **most** | **most** | least — a VM is a VM |
| PaaS | some | some | **most** — you wrote to their runtime |
| SaaS | least | **least** | your data is in their format |

**PaaS has the worst lock-in**, and that is counter-intuitive: it is the
middle option, but the code you wrote targets their runtime, their build
system and their scaling model. Moving a VM is a disk image; moving an App
Engine application is a rewrite.

---

## 1.7 Continuous delivery using PaaS

### 📖 What PaaS actually automates

```
  git push
     │
     ▼
  [ build ]  →  [ test ]  →  [ package ]  →  [ deploy ]  →  [ route traffic ]
     └────────── all of this is the PLATFORM's job ──────────┘
```

On IaaS you build that pipeline. On PaaS it exists, and `git push` is the
whole deployment.

### 🎯 The two deployment strategies to know

**Blue/green** — run the new version alongside the old, switch traffic all at
once, and switch back instantly if it breaks.

**Canary** — send 5% of traffic to the new version, watch the error rate,
increase gradually.

| | Blue/green | Canary |
|---|---|---|
| Traffic during rollout | 100% old, then 100% new | **split** |
| Rollback | instant — flip back | reduce the percentage |
| Cost | **two full environments** | one plus a little |
| Detects a subtle bug | no — you find out at 100% | **yes, at 5%** |
| Needs | a load balancer | **traffic splitting and good metrics** |

**Canary needs metrics you trust**, which is why Unit 5's monitoring is not a
separate topic — a canary without a reliable error signal is just a slower
outage.

### ⚠️ Continuous delivery is not continuous deployment

- **Continuous delivery** — every commit is *deployable*. A human decides
  when.
- **Continuous deployment** — every commit that passes tests *is deployed*,
  automatically.

The second requires the first plus real confidence in your tests. **Most
organisations that say they do continuous deployment do continuous
delivery**, and the distinction is examinable.

---

## Practice problems

**1. A company runs a virtualized datacentre where developers request VMs by
raising a ticket, fulfilled within two working days. Is this a private
cloud?**

**No, and name the characteristic it fails.** It has **resource pooling** and
probably **measured service**, but it lacks **on-demand self-service** — the
defining test is whether a human is in the loop. It almost certainly also
lacks **rapid elasticity**, since nothing gives capacity back automatically.

**It is a virtualized datacentre**, which is a genuinely useful thing. Calling
it a private cloud is marketing, and the five characteristics exist precisely
to settle this argument.

**2. Classify each of these and justify: Gmail, Heroku, EC2, Google
BigQuery, Google Colab.**

| Service | Model | Why |
|---|---|---|
| Gmail | **SaaS** | you use the application; you manage nothing |
| Heroku | **PaaS** | you deploy code; no OS, no runtime |
| EC2 | **IaaS** | you get a machine and patch it |
| BigQuery | **SaaS-ish PaaS** | see below |
| Colab | **SaaS** | a hosted notebook application |

**BigQuery is the interesting one**, and saying so earns the mark. You do not
manage servers, runtimes or scaling — that is beyond PaaS — but you do write
the queries and own the data, which is not SaaS. It is usually called
**serverless**, and *serverless is a fourth position on the same axis*: the
provider manages everything including capacity, and you are billed per
request rather than per hour.

**3. Explain the difference between scalability and elasticity, with an
example where a system has one and not the other.**

**Scalability** — the system can handle more load by adding resources.
**Elasticity** — it adds and **removes** them automatically, in response to
demand.

**Scalable but not elastic:** a Hadoop cluster where you add nodes by hand.
It handles ten times the data; it costs the same at 3 a.m.

**Elastic but not scalable:** a Lambda function that scales to a thousand
concurrent executions but writes to a single-node database. It elastically
scales the part that was never the bottleneck.

**The practical test: what does it cost when nobody is using it?** Elastic
systems approach zero. Scalable ones do not.

**4. Why does PaaS have worse lock-in than IaaS, when IaaS is "lower level"?**

Because **lock-in is proportional to how much of the provider's own
abstraction you wrote against**.

- **IaaS** — you have a Linux VM running your code. Moving it means copying
  a disk image and changing an IP.
- **PaaS** — your code calls their datastore API, uses their build system,
  relies on their scaling semantics and their request lifecycle. Moving means
  a rewrite.

**The general rule: the more the platform does for you, the more your code
assumes about it.** That is not an argument against PaaS — it is the price,
and it should be a decision rather than a surprise.

**5. A team wants to deploy a new version of an API serving 10,000 requests
per minute. Blue/green or canary? What do you need in place first?**

**Canary**, at this volume — 5% is 500 requests per minute, enough to see an
elevated error rate within a minute or two.

**What must exist first:**

1. **A reliable error metric**, and specifically **p99 latency and the 5xx
   rate**, not the mean. Unit 5's monitoring section shows a mean absorbing a
   900 ms outlier completely.
2. **Traffic splitting** at the load balancer or service mesh.
3. **An automatic rollback rule** — a threshold that reverts without waiting
   for a human.
4. **Session handling**, if the API is stateful: a user bounced between
   versions mid-session sees inconsistent behaviour.

**Blue/green would be right** if the change includes a database migration that
cannot serve both versions at once — then a split is impossible, and you
accept the all-at-once switch.

---

## Exam questions from this unit

**Two marks**

1. State the NIST definition of cloud computing.
2. Name the five essential characteristics.
3. Distinguish elasticity from scalability.
4. What is utility computing?
5. Give one difference between grid and cloud computing.
6. Expand IaaS, PaaS, SaaS.
7. Name the four parts of cloud architecture.
8. Distinguish continuous delivery from continuous deployment.

**Five marks**

1. Explain the five essential characteristics, with a failure mode for each.
2. Compare IaaS, PaaS and SaaS by what the customer manages.
3. Explain SOA and why REST replaced SOAP.
4. Explain blue/green and canary deployment, and when each is right.
5. Compare grid, utility and cloud computing.

**Ten marks**

1. Define cloud computing, trace its evolution from time-sharing, and explain
   its architecture and service models with examples.
2. A mid-sized retailer wants to move from an on-premises datacentre to the
   cloud. Recommend a service model for each of: their website, their
   customer database, their email, and their nightly analytics batch — with
   justification.

---

## Mistakes that cost marks

- **Defining the cloud as "the internet" or "someone else's computer".** Give
  the NIST definition, or at minimum the on-demand, elastic, metered triple.
- **Confusing elasticity with scalability.** Elasticity includes scaling
  **in**.
- **Listing service models by example only.** Name the boundary: who manages
  the OS, the runtime, the application.
- **Saying grid computing is old cloud computing.** A grid shares *work*; a
  cloud sells *capacity*.
- **Claiming IaaS has the worst lock-in.** It has the least; PaaS has the
  most.
- **Forgetting the control plane** when describing the architecture. It is
  the actual product.
- **Treating "serverless" as a synonym for PaaS.** It is a further position:
  no capacity to manage at all, billed per request.
