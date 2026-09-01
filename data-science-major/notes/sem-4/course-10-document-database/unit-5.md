# Unit 5 — Advanced Query Processing and Optimization

**Syllabus topics:** Query optimization and operations — projection, limiting
and skipping records, sorting records. Indexing in MongoDB (single field,
compound, multikey, text index). Aggregation framework (pipelines, stages,
operators). Replication concepts — replica sets, failover, consistency.

---

## 5.1 Projection, sorting, limiting and skipping

These were introduced in Unit 3 §§3.12–3.13; here they matter for **performance**.

```js
db.students.find({ dept: "DS" }, { name: 1, "marks.maths": 1, _id: 0 })
          .sort({ "marks.maths": -1 })
          .skip(0)
          .limit(10)
```

**The server always applies sort, then skip, then limit** — regardless of the
order you chain them. So `.limit(3).sort(...)` sorts the entire result and then
takes three; it does not sort three arbitrary documents.

### 🔢 Why each one matters for speed

| Operation | Performance effect |
|---|---|
| **Projection** | Fewer bytes read and sent; can make a query **covered** (§5.5) |
| **`limit`** | Lets the server stop early — **only if the sort is indexed** |
| **`skip`** | **Walks and discards**; linear in the skip distance |
| **`sort`** | Free with an index; otherwise an in-memory sort with a **100 MB ceiling** |

### ⚠️ An unindexed sort fails outright past 100 MB

```js
db.students.find().sort({ score: -1 })
// QueryExceededMemoryLimitNoDiskUseAllowed, if the result exceeds 100 MB
```

An in-memory sort is capped at 100 MB. The fixes, in order of preference:
**create an index on the sort key** (then the sort is free, because the index
is already ordered); or pass `allowDiskUse: true` and accept that it will be
slow.

An indexed sort also lets `limit` stop early: the server reads ten index
entries and stops, instead of sorting a million documents to discard all but
ten.

### ⚠️ `skip` does not scale

`skip(100000)` makes the server walk and throw away 100,000 documents. Page 500
of a listing is genuinely, linearly slower than page 2.

**Range pagination** uses the index to jump straight there:

```js
// page 1
db.students.find().sort({ _id: 1 }).limit(20)
// next page: remember the last _id you saw
db.students.find({ _id: { $gt: lastSeenId } }).sort({ _id: 1 }).limit(20)
```

Every page then costs the same. The trade is that you cannot jump to an
arbitrary page number — which is why infinite-scroll interfaces are common and
"page 500" links are not.

## 5.2 Why indexes

### 🎯 The big idea

**Without an index, MongoDB reads every document in the collection.** That is a
`COLLSCAN`, and it is O(n). An index is a **B-tree of sorted keys**, so a lookup
is O(log n).

The textbook analogy is exact: an index at the back of a book. Finding
"aggregation" means one lookup, not reading all 700 pages.

```js
db.students.createIndex({ dept: 1 })              // 1 ascending, -1 descending
db.students.createIndex({ dept: 1, "marks.maths": -1 })   // compound
db.students.createIndex({ email: 1 }, { unique: true })
db.students.createIndex({ name: "text" })
db.students.createIndex({ dept: 1 }, { name: "dept_idx" })
db.students.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 })  // TTL
db.students.createIndex({ email: 1 },
  { unique: true, partialFilterExpression: { email: { $exists: true } } })

db.students.getIndexes()
db.students.dropIndex("dept_1")
db.students.totalIndexSize()
```

**`_id` is indexed automatically and the index cannot be dropped.**

### ⚠️ Indexes are not free

| Cost | Why |
|---|---|
| **Slower writes** | Every insert, update and delete must maintain every index |
| **Disk and RAM** | An index is a real data structure, and it wants to be in memory |
| **Build time** | Creating one on a large collection takes minutes and consumes I/O |

**The rule: index what you query, not everything.** A collection with fifteen
indexes on a write-heavy workload can be slower overall than one with three.
The limit is 64 per collection, and reaching it means something is wrong with
the design.

## 5.3 Index types

### 🔢 Single field

```js
db.students.createIndex({ dept: 1 })
```

**Direction does not matter for a single-field index** — MongoDB can walk a
B-tree in either direction, so `{ dept: 1 }` serves both ascending and
descending sorts. Direction only matters in a compound index (§5.4).

### Compound

```js
db.students.createIndex({ dept: 1, "marks.maths": -1 })
```

Covered in detail in §5.4 — the prefix rule is the examinable part.

### 🔢 Multikey — an index on an array

```js
db.students.createIndex({ subjects: 1 })
```

When the indexed field is an **array**, MongoDB creates **one index entry per
element**. A student with three subjects contributes three entries, so
`db.students.find({ subjects: "DS" })` uses the index.

MongoDB does this automatically; there is no "multikey" keyword. Two
consequences worth knowing:

- **The index is larger** — proportional to total array elements, not documents.
- **You cannot compound two array fields.** `{ subjects: 1, tags: 1 }` where
  both are arrays is rejected, because the number of entries would be the
  *product* of the two array lengths.

### 🔢 Text

```js
db.articles.createIndex({ title: "text", body: "text" })
db.articles.find({ $text: { $search: "mongodb aggregation" } })
db.articles.find({ $text: { $search: "\"exact phrase\"" } })
db.articles.find({ $text: { $search: "mongodb -mysql" } })      // - EXCLUDES

db.articles.find({ $text: { $search: "mongodb" } },
                 { score: { $meta: "textScore" } })
          .sort({ score: { $meta: "textScore" } })
```

A text index tokenises the field, applies **stemming** ("running" matches
"run") and removes **stop words**, then indexes the terms.

**The key restriction: one text index per collection.** It may cover several
fields — that is what the two-field example above does — but you cannot have
two separate text indexes. Use `weights` to make a match in the title count for
more than one in the body:

```js
db.articles.createIndex({ title: "text", body: "text" },
                        { weights: { title: 10, body: 1 } })
```

For anything demanding, MongoDB Atlas Search (built on Lucene) replaces this
entirely — the built-in text index is deliberately basic.

### The others

| Type | For |
|---|---|
| **Hashed** | Sharding by hash — even distribution, but **no range queries** |
| **Geospatial** (`2dsphere`) | Coordinates; "within 5 km of here" |
| **Wildcard** (`"$**"`) | Unknown or highly variable field names |
| **TTL** | Automatic expiry — sessions, logs, caches |
| **Partial** | Index only documents matching a filter — smaller |
| **Sparse** | Skip documents missing the field |
| **Unique** | Enforce uniqueness |

### ⚠️ Unique indexes and missing fields

```js
db.students.createIndex({ email: 1 }, { unique: true })
db.students.insertOne({ name: "A" })          // ok -- email is missing (null)
db.students.insertOne({ name: "B" })          // DUPLICATE KEY ERROR
```

**A missing field indexes as `null`, and two nulls collide.** So a unique index
allows *one* document without the field, then rejects every other. The fix is a
**partial** index, which excludes them from the index entirely:

```js
db.students.createIndex({ email: 1 },
  { unique: true, partialFilterExpression: { email: { $exists: true } } })
```

(A `sparse: true` unique index does the same job and is the older idiom;
partial indexes are more general and are now preferred.)

## 5.4 Compound indexes and the prefix rule

### 🔢 The ESR rule

For a compound index, order the fields:

> **E**quality first, then **S**ort, then **R**ange.

```js
// Query: dept = "DS", maths > 70, sorted by age
db.students.createIndex({ dept: 1, age: 1, "marks.maths": 1 })
//                        ^equality  ^sort   ^range
```

An equality field narrows the scan to one contiguous section of the index; a
range field leaves the entries after it unordered, so any sort field must come
**before** the range field or the sort cannot use the index.

### 🔢 The prefix rule

An index on `{ a: 1, b: 1, c: 1 }` can serve queries on:

| Query fields | Uses the index? |
|---|---|
| `a` | ✅ |
| `a, b` | ✅ |
| `a, b, c` | ✅ |
| `b` | ❌ |
| `c` | ❌ |
| `b, c` | ❌ |
| `a, c` | ⚠️ Partially — `a` for the scan, `c` filtered afterwards |

**Only a left-hand prefix works.** The reason is the phone book: entries sorted
by *(surname, forename)* let you find everyone called Kumari, and everyone
called Kumari Asha — but finding everyone whose *forename* is Asha means
reading the whole book.

So `{ dept: 1, age: 1 }` serves `{dept: …}` and `{dept: …, age: …}` but **not**
`{age: …}` alone. If you need both, you need a second index — or you reorder so
that the more selective, more frequently queried field comes first.

### Direction, in a compound index

```js
db.students.createIndex({ dept: 1, marks: -1 })
```

serves `sort({ dept: 1, marks: -1 })` **and** its exact reverse
`sort({ dept: -1, marks: 1 })` — because walking the index backwards produces
the opposite of every field. It does **not** serve
`sort({ dept: 1, marks: 1 })`, because that is neither the index order nor its
reverse.

## 5.5 `explain()`

```js
db.students.find({ dept: "DS" }).explain("executionStats")
```

| Verbosity | Shows |
|---|---|
| `"queryPlanner"` (default) | The chosen plan, without running it |
| `"executionStats"` | The plan **and** what it actually did |
| `"allPlansExecution"` | Every candidate plan considered |

### 🔢 What to read

| Field | Meaning |
|---|---|
| **`stage`** | `COLLSCAN` = full scan, **bad**; `IXSCAN` = index scan, **good** |
| `totalDocsExamined` | Documents read |
| `totalKeysExamined` | Index entries read |
| `nReturned` | Documents returned |
| `executionTimeMillis` | Time taken |
| `SORT` stage present | An **in-memory** sort — the index did not cover it |
| `PROJECTION_COVERED` | A **covered** query — the documents were never read |

**The number that matters is the ratio `totalDocsExamined / nReturned`.**

```
1     ideal -- every document examined was returned
10    acceptable
1000  the index is wrong, or missing
```

Examining 100,000 documents to return 10 means the query is doing 10,000× more
work than necessary, whatever the wall-clock time says on a small dataset.

### 💡 Covered queries

```js
db.students.createIndex({ dept: 1, name: 1 })
db.students.find({ dept: "DS" }, { _id: 0, dept: 1, name: 1 })
```

If **every field in the query and the projection is in the index**, MongoDB
answers from the index alone and **never touches the documents**. `explain`
reports `totalDocsExamined: 0`, which is as fast as it gets.

Note the `_id: 0` — it is required, because `_id` is returned by default and is
not in that index.

## 5.6 Query optimization in practice

| Do | Why |
|---|---|
| **Index the fields you filter and sort on** | Turns `COLLSCAN` into `IXSCAN` |
| **Project only what you need** | Fewer bytes; may make the query covered |
| **`$match` first in a pipeline** | Only an early `$match` uses an index |
| **Follow ESR in compound indexes** | Equality, Sort, Range |
| **Use `explain()`** | Measure; do not guess |
| **Range-paginate instead of `skip`** | `skip` is linear |
| **Anchor and case-match regexes** | Only `/^x/` without `i` uses an index |
| **Avoid `$where`** | Runs JavaScript per document; no index; injection risk |
| **Avoid unbounded arrays** | Document moves and 16 MB failures |
| **Keep the working set in RAM** | Disk is orders of magnitude slower |

### ⚠️ Operators that cannot use an index

| Operator | Why |
|---|---|
| `$where` | Arbitrary JavaScript |
| `$regex` unanchored, or with `i` | No contiguous range to scan |
| `$ne`, `$nin` | Must scan everything **except** a section — usually most of it |
| `$exists: false` | Missing fields have no index entry |
| `$nor` | Same reasoning as `$ne` |

**`$ne` is the surprising one.** An index makes "find x" fast by jumping to a
contiguous range; "find everything that is *not* x" is the entire index minus
one range, so scanning it is no better than scanning the collection.

## 5.7 Replication

### 🎯 What a replica set is

**A group of `mongod` processes holding the same data.** One is the
**primary** and takes all writes; the others are **secondaries** and replicate
from it.

```
                 ┌───────────┐
   writes ──────►│  PRIMARY  │
                 └─────┬─────┘
                       │ oplog
            ┌──────────┴──────────┐
            ▼                     ▼
     ┌─────────────┐       ┌─────────────┐
     │ SECONDARY 1 │       │ SECONDARY 2 │
     └─────────────┘       └─────────────┘
```

| Purpose | How replication provides it |
|---|---|
| **High availability** | A secondary is elected if the primary fails |
| **Durability** | The data exists on several machines |
| **Read scaling** | Secondaries can serve reads |
| **Disaster recovery** | Members can sit in different data centres |
| **Zero-downtime maintenance** | Upgrade one member at a time |

### ⚠️ Replication is not backup

A replica set copies **every** operation, including `deleteMany({})`. A
mistaken deletion propagates to all three members within milliseconds.
Replication protects against **hardware failure**, not against **mistakes** —
you still need backups and, ideally, a **delayed member** that lags by an hour.

### The oplog

The **oplog** (operations log) is a **capped collection** on the primary
recording every write. Secondaries tail it and replay the operations.

Its operations are **idempotent** — `$inc: {n: 1}` is rewritten as
`$set: {n: 5}` — so replaying one twice is harmless, which is what makes
recovery after a crash safe.

**Oplog size is what limits how long a secondary can be offline.** If a
secondary is down longer than the oplog's window, the operations it missed have
been overwritten and it must resynchronise from scratch.

### 🔢 Elections and failover

```
1. The primary stops responding to heartbeats (default: 10 seconds).
2. A secondary calls an election.
3. Members vote. A candidate needs a MAJORITY of votes.
4. The winner becomes primary; the others follow it.
5. The old primary, on returning, becomes a SECONDARY and rolls back
   any writes that were never replicated.
```

Typical failover is **10–30 seconds**, during which **writes fail** — MongoDB's
CP choice from Unit 1 §1.2, visible in practice.

### ⚠️ Why the number of members should be odd

**A majority is required to elect a primary.** With an even number, a network
partition can split the set into two equal halves, **neither of which has a
majority**, so no primary is elected and the whole set becomes read-only.

| Members | Majority | Failures survived |
|---|:---:|:---:|
| 3 | 2 | **1** |
| 4 | 3 | **1** — no better than 3, and more to run |
| 5 | 3 | **2** |
| 6 | 4 | 2 |

**Four members survive no more failures than three.** That is why the
recommendation is three or five, and why an **arbiter** exists — a member that
votes but holds no data, used to make an even set odd cheaply.

### Member types

| Type | Holds data | Votes | Can become primary |
|---|:---:|:---:|:---:|
| **Primary** | Yes | Yes | Is |
| **Secondary** | Yes | Yes | Yes |
| **Arbiter** | **No** | **Yes** | No |
| **Hidden** | Yes | Yes | **No** — invisible to clients, for backups |
| **Delayed** | Yes | Yes | No — lags deliberately, for mistake recovery |
| **Priority 0** | Yes | Yes | No |

### 🔢 Write concern

**How many members must acknowledge a write before it is reported as
successful.**

```js
db.students.insertOne(doc, { writeConcern: { w: "majority", j: true, wtimeout: 5000 } })
```

| `w` | Meaning |
|---|---|
| `0` | **No acknowledgement** — fire and forget |
| `1` | The primary only (**the default**) |
| `"majority"` | A majority of voting members |
| `n` | n members |

| Option | Meaning |
|---|---|
| `j: true` | Written to the **journal** on disk, not just memory |
| `wtimeout` | Give up after this many milliseconds |

**`w: "majority"` is what makes a write survive a failover.** With `w: 1`, a
write acknowledged by the primary that has not yet reached any secondary is
**rolled back** if that primary fails — it is genuinely lost. This is the
setting behind MongoDB's early reputation for losing data (Unit 1 §1.6): the
old default was `w: 0`, which acknowledged before writing anything at all.

### Read preference and read concern

```js
db.students.find().readPref("secondaryPreferred")
db.students.find().readConcern("majority")
```

| `readPreference` | Reads from |
|---|---|
| `primary` (default) | The primary only — **strongly consistent** |
| `primaryPreferred` | Primary if available, else a secondary |
| `secondary` | Secondaries only |
| `secondaryPreferred` | Secondaries if available |
| `nearest` | Lowest latency |

| `readConcern` | Returns |
|---|---|
| `local` (default) | The node's most recent data, **which may be rolled back** |
| `majority` | Only data acknowledged by a majority — **cannot be rolled back** |
| `linearizable` | Reflects all writes acknowledged before it began |
| `snapshot` | A consistent point-in-time view, for transactions |

**Reading from a secondary trades consistency for throughput.** A secondary may
be milliseconds or seconds behind, so `secondaryPreferred` can return stale
data. That is the AP end of the tunable spectrum, and it is fine for a
dashboard and wrong for a balance check.

### Setting one up

```js
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})

rs.status()          rs.conf()          rs.isMaster()
rs.add("mongo4:27017")                  rs.remove("mongo4:27017")
rs.stepDown()                           // force a failover, for testing
rs.printSecondaryReplicationInfo()      // replication LAG per secondary
```

## 5.8 Sharding, briefly

Replication copies the **same** data to every member; **sharding splits
different data across machines**. They are complementary, and each production
shard is itself a replica set.

```
        mongos (router)
       /      |       \
  Shard A   Shard B   Shard C          ← each a replica set
  (a–h)     (i–p)     (q–z)
```

**The shard key is the decision that matters**, and it is very hard to change
later. It should have high cardinality, even distribution and match your
queries. A monotonically increasing key such as a timestamp is the classic
mistake: every new document goes to the same shard, so writes do not scale at
all. A **hashed** shard key fixes the distribution and gives up range queries.

## 5.9 Transactions and GridFS

### Multi-document transactions

```js
const session = db.getMongo().startSession()
session.startTransaction()
try {
  const accounts = session.getDatabase("bank").accounts
  accounts.updateOne({ _id: "A" }, { $inc: { balance: -500 } })
  accounts.updateOne({ _id: "B" }, { $inc: { balance:  500 } })
  session.commitTransaction()
} catch (e) {
  session.abortTransaction()
  throw e
} finally {
  session.endSession()
}
```

**A single-document write has always been atomic.** Transactions add
**multi-document** ACID guarantees, available since **4.0** for replica sets
and **4.2** across shards.

**They are not free**, and knowing that is the mark: transactions hold locks,
have a default 60-second limit, and are slower than a single-document write.
**A schema that needs transactions for its common operations is usually a
schema that should have embedded.** The transfer above genuinely needs one; a
student and their address do not.

### GridFS

The 16 MB document limit means a large file cannot be a document. **GridFS
splits it into 255 KB chunks** across two collections:

| Collection | Holds |
|---|---|
| `fs.files` | Metadata — filename, length, upload date, chunk size |
| `fs.chunks` | The binary chunks, each with `files_id` and `n` |

```bash
mongofiles -d mydb put video.mp4
mongofiles -d mydb get video.mp4
mongofiles -d mydb list
```

**Use GridFS when a file exceeds 16 MB, or when you need to read *ranges* of
it** — seeking to the middle of a video means fetching a few chunks, not the
whole file. For smaller files, or where a CDN is available, **object storage
such as S3 is usually the better answer**; GridFS's advantage is that the files
live in the database, replicated and backed up with everything else.

---

## Practice problems

### Problem 1

A `students` collection of 10 million documents runs these queries:

```js
db.students.find({ dept: "DS" })
db.students.find({ dept: "DS", year: 4 })
db.students.find({ dept: "DS" }).sort({ cgpa: -1 }).limit(10)
db.students.find({ year: 4 })
```

Design the indexes, and say which queries each serves.

**Solution.**

**Index 1 — the compound index, following ESR:**

```js
db.students.createIndex({ dept: 1, cgpa: -1 })
```

- Query 1 (`dept`) — ✅ uses it, `dept` is a left-hand prefix.
- Query 3 (`dept` + sort by `cgpa`) — ✅ **and the sort is free**, because the
  index already holds `cgpa` in descending order within each `dept`. The
  `limit(10)` then stops after ten index entries instead of sorting ten million
  documents.
- Query 2 (`dept` + `year`) — ⚠️ partially: `dept` narrows the scan, then
  `year` is filtered afterwards.

**Index 2 — for query 2, if it is frequent:**

```js
db.students.createIndex({ dept: 1, year: 1 })
```

Now query 2 is fully served, and this index *also* covers query 1 — but keeping
both is still right, because index 1 is what makes query 3's sort free.

**Index 3 — for query 4:**

```js
db.students.createIndex({ year: 1 })
```

**This one is not optional.** `{ dept: 1, year: 1 }` does **not** serve
`{ year: 4 }` alone, because `year` is not a left-hand prefix — the phone-book
rule. Without this index, query 4 is a full scan of ten million documents.

**Verify, do not assume:**

```js
db.students.find({ year: 4 }).explain("executionStats")
// stage: IXSCAN (not COLLSCAN)
// totalDocsExamined / nReturned should be close to 1
```

**And the cost:** three indexes means every insert and update maintains three
B-trees. If writes dominate and query 2 is rare, drop index 2 and accept the
partial scan. **Index what you query, not everything.**

### Problem 2

Explain replica set elections. Why should a replica set have an odd number of
members, and what happens during a failover?

**Solution.**

**A replica set is a group of `mongod` processes holding the same data:** one
**primary** taking all writes, and **secondaries** replaying the primary's
**oplog**.

**The election process:**

1. Members exchange **heartbeats** every 2 seconds. If the primary is
   unreachable for `electionTimeoutMillis` (default **10 seconds**), the set
   considers it down.
2. An eligible secondary **calls an election**.
3. Members vote. **A candidate needs a majority of all voting members** — not a
   majority of those reachable.
4. The winner becomes primary and begins accepting writes.
5. When the old primary returns it becomes a **secondary**, and **rolls back**
   any writes it accepted that never reached the new primary.

**Why odd — the important part.** A majority is required, and a majority is
counted against the **configured** number of members. With an **even** number,
a network partition can split the set into two equal halves, and **neither half
has a majority**. No primary is elected, and the entire set becomes read-only —
the worst outcome, since both halves are healthy.

| Members | Majority needed | Failures survived |
|---|:---:|:---:|
| 3 | 2 | **1** |
| **4** | 3 | **1** — no better than 3 |
| 5 | 3 | **2** |
| 6 | 4 | 2 |

**Four members survive no more failures than three**, while costing more to run
and adding a partition risk. That is why the recommendation is three or five,
and why an **arbiter** exists: a voting member with no data, used to make an
even set odd cheaply. (An arbiter is a last resort — it adds a vote but no
durability, so a 2+arbiter set loses data if either data member fails.)

**What happens during failover, from the application's point of view:**

- **Writes fail** for the 10–30 seconds the election takes. This is MongoDB's
  **CP** choice made visible: it would rather refuse a write than accept one it
  cannot guarantee.
- **Reads continue** if `readPreference` allows secondaries.
- Modern drivers **retry** automatically (`retryWrites: true`), so a brief
  failover is often invisible to the application.
- **Writes made with `w: 1` that had not replicated are rolled back** — genuinely
  lost. `w: "majority"` prevents this, because a write is only acknowledged once
  a majority holds it, and a majority is exactly what the new primary must have
  been elected by.

**And the point students miss: replication is not backup.** A `deleteMany({})`
replicates to every member in milliseconds. Replication protects against
hardware failure, not against mistakes — for those you need backups, or a
**delayed member** lagging by an hour.

### Problem 3

A query is slow. Walk through diagnosing and fixing it.

```js
db.orders.find({ status: "shipped", total: { $gt: 1000 } })
         .sort({ orderDate: -1 })
         .limit(20)
```

**Solution.**

**Step 1 — measure. Do not guess.**

```js
db.orders.find({ status: "shipped", total: { $gt: 1000 } })
         .sort({ orderDate: -1 }).limit(20)
         .explain("executionStats")
```

Look for:

| Field | Bad value | Meaning |
|---|---|---|
| `stage` | **`COLLSCAN`** | No index is being used at all |
| `SORT` stage present | — | The sort is happening **in memory** |
| `totalDocsExamined` | 2,000,000 | |
| `nReturned` | 20 | |
| ratio | **100,000 : 1** | 100,000× more work than necessary |

**Step 2 — design the index using ESR.**

- **E**quality: `status`
- **S**ort: `orderDate`
- **R**ange: `total`

```js
db.orders.createIndex({ status: 1, orderDate: -1, total: 1 })
```

**Why that order specifically.** `status` first narrows the index to one
contiguous section. `orderDate` **must come before** `total`, because a range
predicate leaves everything after it unordered in the index — put `total`
second and the sort can no longer use the index, and you are back to an
in-memory sort.

`orderDate: -1` matches the query's sort direction. (`1` would also work here,
since walking the index backwards gives the reverse — but matching is clearer.)

**Step 3 — re-measure.**

```
stage: IXSCAN
SORT stage: ABSENT          ← the index provided the order
totalDocsExamined: ~25
nReturned: 20
ratio: ~1.25
```

The `limit(20)` now stops after about 20 index entries, instead of sorting two
million documents to discard all but twenty.

**Step 4 — consider a covered query.** If the application only displays a few
fields:

```js
db.orders.createIndex({ status: 1, orderDate: -1, total: 1, customer: 1 })
db.orders.find({ status: "shipped", total: { $gt: 1000 } },
               { _id: 0, orderDate: 1, total: 1, customer: 1 })
         .sort({ orderDate: -1 }).limit(20)
// totalDocsExamined: 0 -- the documents are never read at all
```

Note the `_id: 0`: `_id` is returned by default and is not in the index, so
without excluding it the query cannot be covered.

**Step 5 — what else to check if it is still slow:**

- **Is the working set in RAM?** A high `WiredTiger` cache-miss rate means the
  index is being read from disk, which is orders of magnitude slower.
- **Are there too many indexes?** If writes are also slow, the collection may be
  maintaining a dozen B-trees on every insert.
- **Is `skip` involved elsewhere?** Deep pagination is linear; range-paginate
  instead.
- **Is this a `$ne` or unanchored `$regex` in disguise?** Those cannot use an
  index at all.

---

## Exam questions from this unit

**Two marks**

1. What is an index, and what does it cost?
2. Distinguish `COLLSCAN` from `IXSCAN`.
3. What is a multikey index?
4. How many text indexes may a collection have?
5. State the ESR rule.
6. State the index prefix rule.
7. What is a covered query?
8. Why does an unindexed sort fail past 100 MB?
9. Why must a replica set have an odd number of members?
10. What is the oplog?
11. Distinguish `w: 1` from `w: "majority"`.
12. Why is replication not a backup?
13. What is GridFS, and when is it needed?

**Five marks**

1. Explain indexing in MongoDB with all the index types.
2. Explain compound indexes, the prefix rule and ESR.
3. Explain `explain()` and what to read from it.
4. Explain query optimization techniques.
5. Explain replica sets, elections and failover.
6. Explain write concern and read preference.
7. Explain sharding and the choice of shard key.
8. Explain transactions and when they should be avoided.

**Ten marks**

1. Given a collection and its queries, design the indexes and justify each.
2. Explain replication exhaustively — members, oplog, elections, failover,
   write concern and read preference.
3. Diagnose and optimise a slow query, step by step.

## Mistakes that cost marks

- Believing an index is free — it slows every write
- Expecting `{ a: 1, b: 1 }` to serve a query on `b` alone
- Putting a range field before a sort field in a compound index
- Forgetting `_id: 0` and breaking a covered query
- Creating two text indexes on one collection
- Expecting `$ne`, `$nin` or an unanchored regex to use an index
- Using an even number of replica set members
- Saying four members survive two failures
- Treating replication as a backup
- Claiming a `w: 1` write cannot be lost in a failover
- Saying MongoDB has no transactions — it has had them since 4.0
- Reaching for transactions where the schema should have embedded
- Using GridFS for small files where object storage would be better
