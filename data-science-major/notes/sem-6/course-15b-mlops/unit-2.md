# Unit 2 — Data Architecture and Distributed Systems

**Syllabus topics:** Enterprise and data architecture definitions.
Principles of good data architecture. Scalability, failure design, tiers,
microservices, monolith vs modular. Event-driven architecture, hybrid cloud,
multicloud, edge computing. Technology selection criteria: team size,
interoperability, cost, TCO.

---

## 2.1 The definitions

| Term | Definition |
|---|---|
| **Enterprise architecture** | the design of an organisation's whole technology estate, aligned to its strategy |
| **Data architecture** | the subset concerned with **how data is stored, moved, integrated and governed** |
| **Solution architecture** | the design of one system within it |

**Data architecture is a subset of enterprise architecture**, and the exam
answer distinguishes them by *scope*, not by subject matter.

---

## 2.2 The principles of good data architecture

| Principle | What it means in practice |
|---|---|
| **Choose common components wisely** | one object store and one warehouse, shared — not one per team |
| **Plan for failure** | it is not *if*; see 2.3 |
| **Architect for scalability** | and be able to scale **down**, which cloud makes possible and nobody does |
| **Architecture is leadership** | it is a set of decisions with reasons, not a diagram |
| **Always be architecting** | it is continuous; the estate changes under you |
| **Build loosely coupled systems** | a change in one part should not require changing another |
| **Make reversible decisions** | prefer choices you can undo — "one-way doors" deserve far more thought |
| **Prioritise security** | zero trust; the perimeter is not a boundary |
| **Embrace FinOps** | **cost is a design constraint**, and in the cloud it is a per-query one |

### 🎯 "Make reversible decisions" is the one worth internalising

**Choosing a file format is reversible — rewrite the files. Choosing a
partition key for a 40 TB table is nearly not.** Spend your design effort in
proportion to how hard the decision is to undo, and stop agonising over the
reversible ones.

---

## 2.3 Designing for failure

**Failure is the normal condition of a distributed system.** Four terms, and
the difference between them is examined:

| Term | Definition | Measured as |
|---|---|---|
| **Availability** | the fraction of time the system is usable | "three nines" = 99.9% |
| **Reliability** | it does the right thing when it is up | correctness, not uptime |
| **RTO** — recovery time objective | how long may recovery take? | hours, minutes |
| **RPO** — recovery point objective | **how much data may be lost?** | "up to 15 minutes" |

### 🔢 What the nines actually cost you

| Availability | Downtime per year |
|---|---|
| 99% | **3.65 days** |
| 99.9% | 8.8 hours |
| 99.99% | **53 minutes** |
| 99.999% | 5 minutes |

> **Each nine costs roughly ten times the last.** Reaching 99.999% requires
> multi-region redundancy, automated failover, and an on-call rota — and for a
> nightly analytics pipeline it is **pure waste**. Ask what downtime actually
> costs the business before choosing.

**RPO is the one people forget.** A system that recovers in five minutes but
loses an hour of transactions has an excellent RTO and an unacceptable RPO.
They are set independently and both belong in an SLA.

---

## 2.4 Tiers, and the monolith question

### 📖 Tiered architecture

| Architecture | Layers |
|---|---|
| **Single-tier** | everything on one machine |
| **Two-tier** | client and server |
| **Three-tier** | **presentation, application, data** — the classic |
| **N-tier** | further split, e.g. a caching or API-gateway tier |

**Tiers are about separation of concerns; they say nothing about deployment.**
A three-tier application can be one deployed unit — a monolith — or many.

### 🔢 Monolith against microservices, measured

[Experiment 6](lab.md#experiment-6) implements the same three units of work
both ways and times them:

| | 40 applications |
|---|---|
| **monolith** | faster |
| **microservices** | **slower — every boundary is a network hop** |

> ### ⚠️ Microservices are SLOWER for the same work
>
> Any honest comparison starts there. Each boundary you draw adds
> serialisation, a network hop, and a new failure mode.

**So what do you get?** Not speed. **Independent deployment and independent
scaling**, which pay only when the parts genuinely differ:

| Strategy | Instances | Wasted capacity |
|---|---|---|
| monolith, scaled 4× | 4 | **4× of every component** |
| microservices, scale the scorer 4× | 4 + 1 + 1 | **none** |

**That is an argument about cost at scale, not about elegance.**

| | **Monolith** | **Microservices** |
|---|---|---|
| Deploy | all or nothing | per service |
| Scale | the whole thing | **the hot part only** |
| Failure | one crash, all down | degraded, **if you designed for it** |
| Debugging | one stack trace | distributed tracing, or nothing |
| **Data** | **one database, joins work** | **one per service, joins do NOT** |
| Team | coordination on release | independent teams |

### 🎯 The data row is the one that surprises people

**If two services share a database they are not independent** — a schema
change breaks both — so the pattern requires splitting the data too. **A join
you used to write in SQL becomes an API call and an in-memory merge.**

> That is the real cost, and it is why the ETL in
> [experiment 3](lab.md#experiment-3) puts everything in **one warehouse**:
> analytics wants joins, and the microservices argument does not apply to the
> analytical plane at all.

### 💡 The rule the industry learned the hard way

> **Start with a well-structured monolith. Split a service out when you can
> name the specific scaling or deployment problem it solves.**
>
> A team of four does not need eleven services. "We use microservices" is not
> an architecture, and the modular monolith — clean internal boundaries, one
> deployed unit — is the right answer far more often than its reputation
> suggests.

---

## 2.5 Event-driven architecture

Components communicate by **publishing events** rather than calling each
other.

| | **Request/response** | **Event-driven** |
|---|---|---|
| Coupling | the caller knows the callee | **the producer does not know the consumers** |
| Adding a consumer | change the caller | **subscribe; change nothing** |
| Failure | the caller waits or fails | the event is buffered |
| Debugging | one call stack | **hard — no single trace** |
| Ordering | trivial | needs partition keys |

### 🔢 Batch against event-driven ingestion, measured

[Experiment 4](lab.md#experiment-4) runs 300 records through both modes:

| Mode | p50 latency |
|---|---|
| batch (250 ms interval) | **~354 ms** |
| event-driven | **~2 ms** |

**A factor of about 160.** A batch record waits for the next tick, so its
latency is dominated by the *interval*, not by the 2 ms of processing.

> **Batching does not make you faster. It makes you efficient per record, at
> the cost of latency per record.** Raise the interval and per-record cost
> falls further while latency rises linearly.

| | **Batch** | **Event-driven** |
|---|---|---|
| Triggered by | a schedule | an arrival |
| Latency | up to the interval | milliseconds |
| Per-record cost | **low — amortised setup** | higher |
| **Failure** | **retry the whole batch** | retry one message |
| Right for | reports, ETL, billing | fraud, alerts, personalisation |

### ⚠️ The failure row decides real architectures

**A batch job that fails at record 9,000 of 10,000 usually re-runs the whole
batch**, which requires every step to be **idempotent** — and making an ETL
job idempotent is most of the work in writing one.

**A stream consumer retries one message**, but must then handle a message that
fails for ever: that is what a **dead-letter queue** is for, and it is the
first thing missing from a student project.

---

## 2.6 Cloud shapes

| Shape | What it is | Chosen for |
|---|---|---|
| **Public cloud** | one provider's infrastructure | speed, elasticity |
| **Private cloud** | your own datacentre, cloud-style | regulation, existing investment |
| **Hybrid cloud** | both, deliberately connected | keep regulated data on-premises, burst to the cloud |
| **Multicloud** | more than one provider | avoid lock-in, or use the best service of each |
| **Edge** | compute at the data source | **latency and bandwidth** |

### ⚠️ Multicloud costs more than it saves, usually

**The lowest common denominator problem:** to stay portable you can use only
what every provider offers, which means giving up the managed services that
made the cloud worth using. **And egress between clouds is charged**, often
heavily — Course 13 B measures exactly this.

> **Multicloud for resilience is usually a poor trade.** Multicloud because
> one provider has a service you genuinely need is a good reason. Be honest
> about which one you have.

### 📖 Edge computing, and the one number that justifies it

**Bandwidth.** A camera producing 4 Mbit/s, sent to a datacentre continuously,
costs far more than a device that runs the model locally and uploads only the
detections. **Latency is the other reason** — a vehicle cannot wait 80 ms for
a round trip.

---

## 2.7 Technology selection

| Criterion | The question |
|---|---|
| **Team size and skills** | can the team you have operate this? |
| **Speed to market** | managed service now, or self-hosted in three months? |
| **Interoperability** | does it read and write open formats? |
| **Cost and TCO** | see below |
| **Reversibility** | how hard is it to leave? |
| **Build vs buy** | is this your differentiator, or plumbing? |

### 🔢 TCO — the calculation people get wrong

**Total cost of ownership is not the licence fee.**

| Component | Often forgotten |
|---|---|
| Licence or subscription | — |
| Infrastructure | |
| **Engineering time to operate it** | **usually the largest line** |
| Training | |
| Migration cost | |
| **Opportunity cost** | what your engineers are not building instead |

> **"Free" open-source software with a full-time engineer maintaining it costs
> more than a managed service at ₹40,000 a month.** Comparing licence fees
> alone is the standard mistake, and TCO exists to name it.
>
> **And the related distinction:** CapEx (buy the servers) against OpEx (rent
> them). The move to cloud is a shift from one to the other, which changes the
> accounting as much as the engineering.

### 💡 The criterion that dominates in practice

**Team size.** A three-person team running Kubernetes, Kafka, Airflow and a
data lake will spend all its time on operations and none on data. **Choose the
boring, managed option until you can name what it is costing you.**

---

## What to be able to do after this unit

- [ ] Distinguish enterprise, data and solution architecture
- [ ] Name five principles of good data architecture and explain **reversibility**
- [ ] **Distinguish availability, reliability, RTO and RPO** — and give the downtime for three nines
- [ ] Explain tiers, and why they are not the same as deployment units
- [ ] **Give the honest cost of microservices**, and the case where they pay
- [ ] Explain why "one database per service" is the hard part
- [ ] **Compare batch and event-driven ingestion on latency, cost and failure**
- [ ] Say what a dead-letter queue is for
- [ ] Explain why multicloud usually costs more than it saves
- [ ] Justify edge computing with bandwidth and latency
- [ ] **Compute a TCO and say why the licence fee is not it**

**Cross-check yourself:** run
`01_environment_etl.py`
and
`04_batch_vs_event.py`.
