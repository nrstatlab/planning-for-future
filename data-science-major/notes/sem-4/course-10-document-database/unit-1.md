# Unit 1 — Introduction to NoSQL and Fundamentals of MongoDB

**Syllabus topics:** What is NoSQL DB? History and evolution of NoSQL,
features of NoSQL databases, CAP theorem and BASE properties, types of NoSQL
(key-value, document, column, graph), difference between RDBMS and NoSQL, why
and when to use NoSQL, NoSQL database misconceptions, benefits and real-world
use cases of NoSQL, comparison of popular NoSQL systems (Redis, Cassandra,
CouchDB, Neo4j), introduction to JSON and BSON. Installation and setup,
connecting via Mongo shell or GUI.

> The syllabus prints this unit's last topic as "Installation & Setupservice),
> connecting via Mongo shell or GUI" — text has been lost mid-sentence, and a
> stray `)` remains. Recorded in [SYLLABUS-REVIEW.md](../../../SYLLABUS-REVIEW.md).

---

## 1.1 What NoSQL is

### 🎯 The big idea

**NoSQL means "Not Only SQL"**, not "no SQL". It is a family of databases that
relax one or more relational guarantees in exchange for **horizontal scale**,
**flexible schemas**, or **a data model that fits the problem better**.

The name is unhelpful — it says what these databases are *not*. What unites
them is that each one **gave something up on purpose**.

### History

| Period | What happened |
|---|---|
| 1970s | Codd's relational model; SQL follows |
| 1970s–2000s | Relational databases dominate essentially everything |
| ~2000s | Web-scale traffic outgrows what one machine can serve |
| 2004–2007 | Google's **BigTable** and Amazon's **Dynamo** papers |
| 2009 | The term "NoSQL" is reused for a meetup; the movement gets a name |
| 2009 | **MongoDB**, Cassandra, Redis and Neo4j all appear |
| 2010s | The hype peaks, then settles: NoSQL is *a* tool, not *the* tool |
| Present | **Polyglot persistence** — several databases in one system, each where it fits |

**The driver was scale, not dissatisfaction with SQL.** Google and Amazon had
data that would not fit on one machine and traffic one machine could not
serve. Sharding a relational database across hundreds of nodes while
preserving joins and ACID is extremely hard; the NoSQL answer was to stop
requiring it.

### Features of NoSQL databases

| Feature | Meaning |
|---|---|
| **Schema-flexible** | Documents in one collection need not share a shape |
| **Horizontally scalable** | Add machines, not a bigger machine |
| **Distributed** | Data is partitioned and replicated across nodes |
| **High availability** | Replication means node failure is survivable |
| **No joins** (usually) | Related data is stored together instead |
| **Eventually consistent** (often) | Replicas converge rather than agreeing instantly |
| **Optimised for a pattern** | Each type is fast at its own access pattern |
| **Commodity hardware** | Many cheap machines, not one expensive one |

## 1.2 The CAP theorem

### 🔢 The statement

**Brewer's CAP theorem**: a **distributed** data store can guarantee at most
**two** of:

| | Meaning |
|---|---|
| **C — Consistency** | Every read returns the most recent write, or an error |
| **A — Availability** | Every request gets a non-error response |
| **P — Partition tolerance** | The system keeps working when messages between nodes are lost |

```
                     C
                    / \
              CA   /   \   CP
                  /     \
                 /       \
                A ------- P
                    AP
```

### ⚠️ You do not actually get to choose all three pairs

This is the part that is usually taught badly, and stating it correctly earns
marks.

**Network partitions are not optional.** Cables fail, switches reboot, packets
are lost. In any real distributed system, **P is a fact of the environment, not
a design choice**. So the real decision, *when a partition happens*, is:

- **CP** — refuse to answer rather than answer wrongly (sacrifice availability)
- **AP** — answer with possibly stale data rather than refuse (sacrifice
  consistency)

**"CA" is not a meaningful choice for a distributed system.** A single-node
database is CA by default — there is nothing to partition — but as soon as you
replicate, you must pick CP or AP.

| System | Choice |
|---|---|
| **MongoDB** | **CP** — with a default replica set, writes go to the primary; if it is unreachable, writes fail until a new one is elected |
| **Cassandra** | **AP** — always accepts writes, resolves conflicts later |
| **CouchDB** | **AP** |
| **HBase** | **CP** |
| **Traditional RDBMS (single node)** | CA, trivially |

MongoDB is **tunable**: read and write concerns let you move along the
spectrum. `w: "majority"` is stronger, `w: 1` is faster, and
`readPreference: secondary` trades consistency for read scale.

### 🔢 ACID versus BASE

| | **ACID** (relational) | **BASE** (many NoSQL) |
|---|---|---|
| **A** | Atomicity — all or nothing | **Basically Available** — responds, perhaps with stale data |
| **C** | Consistency — constraints always hold | **Soft state** — state may change without input, as replicas sync |
| **I** | Isolation — concurrent transactions do not interfere | **Eventually consistent** — replicas converge, given time |
| **D** | Durability — committed means committed | |
| Priority | **Correctness** | **Availability** |

**BASE is a deliberately jokey backronym** (acid/base), and knowing that is
worth saying — it signals you understand it is a *stance*, not a theorem.

**Eventual consistency means:** if no new writes arrive, all replicas will
eventually return the same value. It does **not** promise how long that takes,
and it does mean a read can return a value that has since been overwritten.

**MongoDB is not BASE.** Since version 4.0 it has **multi-document ACID
transactions**, and a single-document write has always been atomic. Saying
"NoSQL means BASE, not ACID" is a common exam answer and it is out of date.

## 1.3 The four types of NoSQL database

### 🔢 The comparison

| Type | Model | Query by | Examples | Best for |
|---|---|---|---|---|
| **Key-value** | `key → opaque blob` | **Key only** | **Redis**, DynamoDB, Riak | Caching, sessions, counters |
| **Document** | `key → structured document` | Key **or any field** | **MongoDB**, **CouchDB** | Content, catalogues, user profiles |
| **Column-family** | Row key → column families | Key, column range | **Cassandra**, HBase | Time series, huge writes, analytics |
| **Graph** | Nodes and edges, both with properties | Traversal | **Neo4j**, JanusGraph | Networks, recommendations, fraud rings |

### Key-value

```
"session:8842"  →  <opaque bytes>
"cart:21"       →  <opaque bytes>
```

The simplest and fastest model. The store does not know or care what the value
contains, so **you cannot query by its contents** — only by key. Redis holds
everything in memory, which makes it superb for caching and unsuitable as a
system of record without care.

### Document

```json
{ "_id": 21, "name": "Asha", "dept": "DS",
  "marks": { "maths": 88, "stats": 91 },
  "subjects": ["DS", "Stats"] }
```

**The step up from key–value is that the database understands the value.** It
can index `dept`, filter on `marks.maths`, and reach inside the `subjects`
array. That is the whole difference, and it is why document stores are the most
generally useful of the four.

### Column-family

Not "a column store" in the analytics sense, despite the name. Data is stored
by **row key**, with columns grouped into families, and **each row may have
different columns**. Optimised for enormous write throughput and for reading
ranges of rows.

### Graph

Stores **relationships as first-class objects**. "Friends of friends who like
jazz" is a three-hop traversal in Neo4j and a three-way self-join with a
recursive CTE in SQL — the graph database is dramatically faster because the
edges are pointers, not values to be matched.

### 💡 How to choose, in one line each

- Only ever fetch by a single key, and want it very fast → **key–value**
- Fetch one whole entity at a time, and query its fields → **document**
- Enormous write volume, queries by time or range → **column-family**
- The *relationships* are the thing you query → **graph**

## 1.4 Popular systems compared

| | **Redis** | **MongoDB** | **Cassandra** | **CouchDB** | **Neo4j** |
|---|---|---|---|---|---|
| Type | Key-value | **Document** | Column-family | Document | Graph |
| Storage | **In-memory** (with persistence) | Disk | Disk | Disk | Disk |
| CAP | CP | **CP** | **AP** | **AP** | CA/CP |
| Query language | Commands | **MQL** | CQL (SQL-like) | MapReduce / Mango | **Cypher** |
| Interface | TCP protocol | Driver / shell | Driver | **HTTP/REST** | Driver / HTTP |
| Format | Strings, lists, sets, hashes | **BSON** | Rows | **JSON** | Nodes and edges |
| Scaling | Cluster | **Sharding** | **Masterless ring** | Replication | Clustering |
| Killer feature | Speed; rich data structures | Flexible querying | Linear write scale; no single point of failure | Multi-master sync, offline-first | Traversal speed |
| Weak at | Anything not keyed | Very high write volume | Ad-hoc queries — you design tables per query | Ad-hoc queries | Sharding a graph |

**Cassandra's masterless design is the real contrast with MongoDB.** Every node
is equal and accepts writes, so there is no primary to fail over — that is what
makes it AP and what makes it linearly scalable for writes. The price is that
you must know your queries **before** designing the tables, because there is no
flexible ad-hoc querying.

## 1.5 RDBMS versus NoSQL

### 🔢 The comparison

| | **RDBMS** | **NoSQL** |
|---|---|---|
| Model | Tables, rows, columns | Documents, key–value, columns, graphs |
| Schema | **Fixed**, declared before data | **Flexible**, per record |
| Language | **SQL** — standardised | Per product |
| Relationships | **Joins** and foreign keys | Embedding, or application-side lookup |
| Normalisation | Central | Deliberately relaxed |
| Transactions | **ACID**, across tables | Per record; multi-record where supported |
| Scaling | **Vertical** (mostly) | **Horizontal** |
| Consistency | Strong | Strong or eventual, per product |
| Maturity | 50 years | ~15 years |
| Tooling | Enormous | Growing |
| Good at | Complex queries, integrity, reporting | Scale, flexibility, one-entity reads |

### The vocabulary map — learn this table

| RDBMS | MongoDB |
|---|---|
| Database | Database |
| **Table** | **Collection** |
| **Row / tuple** | **Document** |
| **Column / attribute** | **Field** |
| Primary key | **`_id`** |
| Index | Index |
| **JOIN** | Embedding, or **`$lookup`** |
| `GROUP BY` | Aggregation pipeline `$group` |
| Foreign key | A reference, **not enforced** |
| View | View |
| Schema (enforced) | JSON Schema validator (**optional**) |

**"Foreign key: a reference, not enforced" is the row that matters.** MongoDB
will happily store an `ObjectId` pointing at a document that does not exist and
will not stop you deleting the target. In Course 5 the database guaranteed
referential integrity; here **your application must**.

## 1.6 When to use NoSQL — and when not

### ✅ Use a document database when

- You read and write **one whole entity at a time** — a user profile, a product
  page, an order with its lines
- The schema **varies** or evolves fast — a product catalogue where a book has
  an ISBN and a shirt has a size
- You need **horizontal scale** beyond one machine
- The data is **naturally hierarchical** — JSON from an API, nested
  configuration, event payloads
- **Write throughput** matters more than complex ad-hoc queries
- You are prototyping and the schema is not settled

### ❌ Do **not** use one when

- The data is **highly relational** and queried from many directions —
  a banking ledger, an ERP
- You need **complex ad-hoc joins** across many entities
- **Strong multi-entity transactional guarantees** are central — money, stock
  ledgers, seat reservations
- Reporting and BI tools must connect (they speak SQL)
- The team knows SQL and the data fits comfortably on one machine
- **You are choosing it because it is fashionable** — the honest and commonest
  wrong reason

### ⚠️ The misconceptions

The syllabus names this topic explicitly, and each of these is a
frequently-marked answer.

| Misconception | The truth |
|---|---|
| "NoSQL means no SQL" | It means **Not Only SQL**; MongoDB even has a SQL-ish aggregation interface, and Cassandra's CQL looks like SQL |
| "NoSQL is always faster" | Faster **for its access pattern**. A join-heavy analytical query is far slower |
| "NoSQL has no schema" | It has a **flexible** schema. There is always a schema — it lives in your application code instead of the database, which is a *worse* place for it to hide |
| "NoSQL cannot do ACID" | **MongoDB has had multi-document ACID transactions since 4.0** (2018) |
| "NoSQL replaces relational databases" | It complements them. **Polyglot persistence** — the right store for each job — is what real systems do |
| "Schemaless means no design needed" | The opposite. **Because the database will not stop you, design matters more, not less** |
| "MongoDB loses data" | Historically it defaulted to unacknowledged writes, which was a real and fair criticism. It has defaulted to acknowledged writes since 2012 |

That last row is worth knowing: MongoDB's early reputation for data loss was
earned by a **default setting**, `w: 0`, which acknowledged a write before it
was stored. The default is now `w: 1` (and `w: "majority"` for replica sets).
Being able to say *what* the criticism was and *that it was fixed* is a better
answer than either defending or repeating it.

## 1.7 Real-world use cases

| Domain | Use | Why a document store |
|---|---|---|
| **E-commerce** | Product catalogue | Every category has different attributes |
| **Content management** | Articles, pages | Nested, varied structure |
| **Gaming** | Player state, inventories | One entity read and written whole |
| **IoT / sensors** | Readings | Huge write volume, schema drift |
| **Mobile apps** | User profiles, sync | JSON end to end |
| **Real-time analytics** | Event streams | Fast writes, aggregation pipeline |
| **Personalisation** | Recommendations, preferences | Varied per user |

**MongoDB's own headline users** — Forbes, Toyota, Adobe, eBay — mostly use it
for exactly this: catalogue and content data, read one entity at a time, where
the schema varies by category.

## 1.8 JSON and BSON

### 🔢 BSON

**BSON** — **B**inary **JSON** — is how MongoDB actually stores and transmits
documents. It is a binary encoding of a JSON-like structure, with two additions
that matter.

| | **JSON** | **BSON** |
|---|---|---|
| Encoding | Text | **Binary** |
| Readable | **Yes** | No |
| Size | Smaller for small values | Slightly larger (it stores lengths and types) |
| Parse speed | Slower | **Faster** — lengths let a parser skip |
| Types | 6 | **~20** |
| Dates | **No date type** — an ISO string | **Native `Date`** |
| Integers | One `number` type | `int32`, `int64`, `double`, `decimal128` |
| Binary data | Base64 in a string | **Native `BinData`** |
| Ordered fields | Not guaranteed | **Guaranteed** |

**The two additions that matter are types and traversability.**

**Types:** JSON has one numeric type, so it cannot distinguish the integer 5
from the float 5.0, and it has no date at all. BSON has `int32`, `int64`,
`double`, `decimal128`, `Date`, `ObjectId`, `BinData` and `Regex`. That means
`{ dob: ISODate("2005-04-03") }` can be **compared and sorted as a date**,
which a string cannot be reliably.

**Traversability:** every BSON element records its own length, so a driver
skipping to the fifth field does not have to parse the first four. That is what
makes BSON faster to scan despite being larger.

`decimal128` deserves a mention: it is **exact decimal arithmetic**, and it is
what you use for money. A `double` cannot represent 0.1 exactly — Course 9
§1.3 and Course 2 met the same problem — so financial amounts stored as doubles
accumulate error.

### The `_id` field

Every document has one, and it is the primary key.

```js
{ "_id": ObjectId("66cd12f4a1b2c3d4e5f60718"), "name": "Asha" }
```

If you do not supply one, MongoDB generates an **ObjectId**: 12 bytes, made of

```
| 4 bytes timestamp | 5 bytes random per-process | 3 bytes counter |
```

Three consequences worth knowing:

1. **It is unique without coordination.** Any client can generate one without
   asking the server, which is what makes it work in a distributed system.
2. **It embeds a creation time** — `ObjectId.getTimestamp()` — so you often do
   not need a separate `createdAt` field.
3. **It sorts roughly by creation time**, because the timestamp is the leading
   bytes. Sorting by `_id` descending is a cheap "newest first".

You may use your own value instead — a roll number, an email — and it will be
enforced unique. That is often better than an ObjectId when a natural key
exists.

## 1.9 Installation and connecting

> The syllabus text for this topic is damaged (see the note at the top). This
> section covers what it evidently intended.

### Installing

| Route | Notes |
|---|---|
| **MongoDB Atlas** | A free cloud tier. **No install at all** — the fastest way to start, and what most courses now use |
| **Docker** | `docker run -d -p 27017:27017 mongo` — one command, no system changes |
| Local package | `apt install mongodb-org` / the macOS or Windows installer |

**Atlas or Docker is the recommendation.** A local install commits you to
managing a service; the free Atlas tier gives you a real replica set, which the
local install does not.

*(The verification environment for these notes can do none of the three: the
Debian repositories that host `mongodb-org` are blocked by the egress policy.
That is why the labs pair each `mongosh` script with a mongomock equivalent —
see [lab.md](lab.md).)*

### Connecting

```bash
mongosh                                        # localhost:27017
mongosh "mongodb://localhost:27017"
mongosh "mongodb+srv://user:pass@cluster.mongodb.net/mydb"   # Atlas
```

The syllabus calls it the **Mongo shell**, and you will meet both names: the
old shell was the `mongo` command, and it was replaced in MongoDB 5.0 by
**`mongosh`**. They are the same thing for exam purposes — the Mongo shell —
and `mongosh` is the one you actually type.

| Client | What it is |
|---|---|
| **`mongosh`** | The **Mongo shell** — a full JavaScript REPL. **This is what the lab exam uses** |
| **MongoDB Compass** | The official GUI — browse collections, build queries visually, read `explain()` output as a diagram |
| **Drivers** | PyMongo, the Node driver, and one for every language |

`mongosh` is a **JavaScript** environment, which is genuinely useful:

```js
use collegeDB                       // switch database (creates it lazily)
db                                  // the current database
show dbs                            // list databases
show collections
db.students.find()

for (let i = 1; i <= 5; i++) {      // real JavaScript, in the shell
  db.counters.insertOne({ n: i, square: i * i })
}
```

### ⚠️ Databases and collections are created lazily

```js
use brandNewDB          // switches, but creates NOTHING
show dbs                // brandNewDB is ABSENT
db.things.insertOne({ x: 1 })
show dbs                // now it appears
```

**A database or collection does not exist until the first document is written
to it.** `show dbs` omitting the database you just "created" is not a bug, and
it surprises everyone once.

### The default port

**27017**. Worth knowing for the viva; 27018 and 27019 are the conventional
ports for shard members and config servers.

---

## Practice problems

### Problem 1

Explain the CAP theorem, and state which two properties MongoDB and Cassandra
each choose. Why is "CA" not really an option?

**Solution.**

CAP states that a **distributed** data store can guarantee at most two of
**Consistency** (every read returns the latest write, or an error),
**Availability** (every request receives a non-error response) and **Partition
tolerance** (the system keeps working when the network drops messages between
nodes).

**"CA" is not a meaningful choice for a distributed system**, and this is the
part usually got wrong. Network partitions are a **fact of the environment**,
not a design decision — cables fail and switches reboot whatever you choose.
So P is compulsory, and the real question is what you do *during* a partition:

- **CP** — refuse to serve rather than serve stale data.
- **AP** — serve possibly stale data rather than refuse.

A single-node database is CA trivially, because there is nothing to partition.

**MongoDB is CP.** In a replica set, writes go to the primary; if the primary
is unreachable, writes **fail** until an election produces a new one — the
system chose consistency over availability. It is tunable: `w: "majority"` and
`readConcern: "majority"` strengthen consistency, while reading from
secondaries weakens it for more throughput.

**Cassandra is AP.** Every node accepts writes with no primary at all, so
writes always succeed; conflicting versions are resolved afterwards
(last-write-wins, or by vector clocks). That masterless design is why it scales
writes linearly and has no single point of failure — and why you cannot get a
strongly consistent read cheaply.

### Problem 2

Distinguish JSON from BSON, and explain why MongoDB uses BSON. Give two things
BSON can represent that JSON cannot.

**Solution.**

JSON is a **text** format with six types; BSON is a **binary** encoding of the
same structure with about twenty. MongoDB stores and transmits BSON, and shows
you JSON.

| | JSON | BSON |
|---|---|---|
| Encoding | Text | Binary |
| Human-readable | Yes | No |
| Types | 6 | ~20 |
| Parse speed | Slower | **Faster** |
| Size | Usually smaller | Slightly larger |

**Two things BSON can represent and JSON cannot:**

1. **A native date.** JSON has no date type, so `"2005-04-03"` is just a
   string; you cannot sort or compare it as a date reliably, and any date
   arithmetic must parse it first. BSON's `Date` is a real 64-bit timestamp.

2. **Distinct numeric types.** JSON has one `number`. BSON distinguishes
   `int32`, `int64`, `double` and **`decimal128`** — the last being exact
   decimal arithmetic, which is what you must use for money, because a `double`
   cannot represent 0.1 exactly.

(A third, if asked: **binary data**. JSON must base64-encode it into a string,
inflating it by a third; BSON has `BinData`.)

**Why MongoDB uses it.** Two reasons. **Types** — indexes, comparisons and
sorting need to know that a field is a date or an integer, not text. And
**traversability** — every BSON element stores its own length, so a driver can
skip a field without parsing it. That is what makes BSON faster to scan despite
being the larger format, and it is the trade MongoDB chose deliberately: a
little more disk for much faster access.

### Problem 3

A startup is building a product catalogue for an e-commerce site. Books have an
ISBN, author and page count; shirts have a size, colour and material;
electronics have a warranty and voltage. New categories are added monthly.
Would you use MongoDB or a relational database? Justify it, and say what you
would still worry about.

**Solution.**

**MongoDB, and the reason is the varying schema.**

In a relational design there are three unattractive options:

1. **One wide table** with a column per attribute of every category — mostly
   NULLs, and a schema migration every month.
2. **A table per category** — `books`, `shirts`, `electronics` — which means a
   new table and new code for every category, and a painful UNION for "search
   all products".
3. **Entity–attribute–value** — one row per attribute. Infinitely flexible,
   and it makes every query a self-join; it is widely regarded as an
   anti-pattern for exactly this reason.

A document model has none of these problems:

```js
{ _id: 1, name: "MongoDB: The Definitive Guide", category: "book",
  price: 2400, isbn: "978-1491954461", author: "Chodorow", pages: 514 }

{ _id: 2, name: "College T-Shirt", category: "shirt",
  price: 599, size: "L", colour: "navy", material: "cotton" }
```

Both live in one collection, both are queryable by `price` or `category`, and
adding a category needs **no migration at all**.

The access pattern fits too: a product page reads **one whole product**, which
is exactly what a document store is fast at.

**What I would still worry about, and this is what earns the last marks:**

- **"Flexible schema" is not "no schema".** Without discipline you will
  accumulate `colour`, `color` and `Colour` in one collection. Use
  **JSON Schema validation** (Unit 2 §2.7) to enforce the fields that are
  genuinely common, and keep the flexibility only where it is needed.
- **Orders and payments should probably not live here** — or should use
  transactions if they do. A catalogue is a good document-store fit; a ledger
  is a relational one. **Polyglot persistence** is the right answer, not
  "MongoDB for everything".
- **Reporting.** BI tools speak SQL. Either accept the aggregation pipeline, or
  plan to export to a warehouse (Course 8 Unit 1).
- **Referential integrity is now the application's job.** Nothing stops a
  `category` value that no category document matches.

---

## Exam questions from this unit

**Two marks**

1. What does NoSQL stand for?
2. State the CAP theorem.
3. Why is "CA" not a real choice for a distributed system?
4. What does BASE stand for?
5. Name the four types of NoSQL database with an example of each.
6. Distinguish JSON from BSON.
7. What is an ObjectId, and what is it made of?
8. Give the MongoDB term for a table, a row and a column.
9. What is MongoDB's default port?
10. Name two NoSQL misconceptions.

**Five marks**

1. Explain the CAP theorem with a diagram and classify three systems.
2. Explain ACID and BASE, and compare them.
3. Explain the four types of NoSQL database with examples and use cases.
4. Compare RDBMS and NoSQL.
5. Compare Redis, MongoDB, Cassandra, CouchDB and Neo4j.
6. Explain JSON and BSON and why MongoDB uses BSON.
7. Explain when NoSQL should and should not be used.

**Ten marks**

1. Explain NoSQL exhaustively — history, features, types, CAP, BASE and use
   cases — with examples.
2. Compare RDBMS with MongoDB across every dimension, with the vocabulary map.
3. Given a business scenario, choose a database type and justify the choice
   fully, including what you would still be careful about.

## Mistakes that cost marks

- Saying NoSQL means "no SQL"
- Claiming a distributed system can choose "CA"
- Saying MongoDB is AP — it is **CP**
- Saying NoSQL cannot do ACID — MongoDB has had transactions since 4.0
- Saying NoSQL has "no schema" rather than a flexible one
- Confusing column-family stores with analytical column stores
- Saying BSON is smaller than JSON — it is usually slightly larger
- Claiming JSON has a date type
- Forgetting that a MongoDB foreign-key reference is **not enforced**
- Expecting `show dbs` to list a database before anything is written to it
