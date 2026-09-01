# Course 10 — Practical Lab

**20 experiments**

Code lives in `labs/course-10-mongodb/`.

> **On the tooling.** `mongod` cannot be installed in the verification
> environment — the Debian repositories that host `mongodb-org` are blocked by
> the egress policy. So each experiment comes in two halves:
>
> - **`NN_name.js`** — the `mongosh` script you would actually run. Marked
>   **NOT EXECUTED** in its own header. **This is what the lab examiner will
>   ask you to demonstrate.**
> - **`NN_name.py`** — the same query logic executed through **mongomock** and
>   asserted, verified by
>   `tools/run_mongo_labs.py`.
>
> **Sixteen of the twenty experiments have a runnable half; four do not.**
> Experiment 1 is installing the server and opening the shell — there is no
> query logic to run. mongomock implements the query and aggregation language
> but is not a server, so **replication (17), GridFS (18) and transactions
> (19) genuinely cannot be executed here** either. Those four are documented
> only, the runner asserts that list against what is on disk, and **every one
> of the twenty `mongosh` scripts says NOT EXECUTED in its first lines** —
> not just the four. Nothing in this course implies a test that did not run.

```bash
pip install -r tools/requirements.txt
python3 tools/run_mongo_labs.py
```

## Setting up for real

For the lab exam you need a real server. Three routes:

| Route | Command |
|---|---|
| **MongoDB Atlas** | Free tier, no install — and it gives you a **real replica set**, which a local install does not |
| **Docker** | `docker run -d -p 27017:27017 --name mongo mongo` |
| Local package | `apt install mongodb-org`, or the platform installer |

```bash
mongosh                                    # localhost:27017
mongosh "mongodb+srv://user:pass@cluster.mongodb.net/collegeDB"
```

**Use Atlas or Docker.** A local install commits you to managing a service, and
Atlas is the only one of the three that gives you a replica set — which
experiments 17 and 19 both require.

---

## Experiment 1 — Installation, Mongo Shell and Compass

**NOT EXECUTED** — needs a server.

```js
db.version()
db.serverStatus().host
show dbs
db.hostInfo()
db.adminCommand({ listDatabases: 1 })
```

**MongoDB Compass** is the official GUI: browse collections, build queries
without typing them, and read `explain()` output as a diagram rather than
JSON. Worth installing for the `explain` visualiser alone.

**Know for the viva:** the default port is **27017**; `mongosh` is a full
**JavaScript** REPL, so loops and variables work in it; and `show dbs` will not
list a database until something has been written to it.

## Experiment 2 — Databases, collections, inserting documents

**Both halves.** `02_create_insert.js` / `.py`

```js
use collegeDB
db.createCollection("students")
db.students.insertOne({ _id: 21, name: "Asha", dept: "DS" })
db.students.insertMany([ /* ... */ ], { ordered: false })
show collections
db.students.countDocuments()
```

The Python half asserts the two behaviours that are examinable:

- **Lazy creation** — the database does not exist until the first write.
- **`ordered: true` (the default) stops at the first error**, so documents
  after a duplicate `_id` are never attempted; `ordered: false` inserts them.

## Experiment 3 — `find()` and comparison operators

**Both halves.** `03_find_compare.js` / `.py`

```js
db.students.find({ dept: "DS" })
db.students.find({ age: { $gt: 20 } })
db.students.find({ age: { $gte: 20, $lte: 21 } })      // ONE object
db.students.find({ dept: { $in: ["DS", "CS"] } })
db.students.find({ "marks.maths": { $gte: 90 } })      // dot notation
```

Asserted: every comparison operator, dot notation into a sub-document, and the
two traps — **a range must be one object**, and **`$ne` also matches documents
where the field is missing**.

## Experiment 4 — Logical operators

**Both halves.** `04_logical.js` / `.py`

```js
db.students.find({ $or:  [ { dept: "Stats" }, { "marks.maths": { $gt: 85 } } ] })
db.students.find({ $and: [ { age: { $gte: 20 } }, { age: { $lte: 21 } } ] })
db.students.find({ $nor: [ { dept: "DS" }, { age: 20 } ] })
db.students.find({ age: { $not: { $gt: 21 } } })
```

Asserted: `$nor: [A, B]` equals `(NOT A) AND (NOT B)` — De Morgan from Course 1
— and that **`$not` cannot take a plain value**, only an operator expression.

## Experiment 5 — Updating with `$set`, `$unset`, `$inc`, `$rename`

**Both halves.** `05_update.js` / `.py`

```js
db.students.updateOne({ _id: 21 }, { $set: { age: 21 } })
db.students.updateMany({ dept: "DS" }, { $inc: { "marks.maths": 5 } })
db.students.updateOne({ _id: 21 }, { $unset: { active: "" } })
db.students.updateMany({}, { $rename: { "dept": "department" } })
db.students.updateOne({ _id: 99 }, { $inc: { n: 1 } }, { upsert: true })
```

The Python half asserts the destructive one: **`replaceOne` keeps only `_id`**
and discards every other field, while `updateOne` with `$set` preserves them.
It also asserts that `updateOne` changes **exactly one** document when three
match — the commonest CRUD mistake, and silent.

## Experiment 6 — Deleting

**Both halves.** `06_delete.js` / `.py`

```js
db.students.deleteOne({ _id: 21 })
db.students.deleteMany({ dept: "DS" })
db.students.deleteMany({})            // EVERY document; the collection remains
db.students.drop()                    // the collection AND its indexes
```

Asserted: `deleteMany({})` empties the collection but **keeps** it, its indexes
and its validator; `drop()` removes all three.

**There is no confirmation and no undo.** In Course 5, `DELETE FROM t` at least
sat inside a transaction you could roll back.

## Experiment 7 — Projection

**Both halves.** `07_projection.js` / `.py`

```js
db.students.find({}, { name: 1, dept: 1 })
db.students.find({}, { name: 1, _id: 0 })
db.students.find({}, { marks: 0 })
db.students.find({}, { "marks.maths": 1 })
db.students.find({}, { subjects: { $slice: 2 } })
```

Asserted: **mixing inclusion and exclusion raises an error**, and **`_id` is
the one exception** — it may be excluded alongside inclusions.

## Experiment 8 — Sorting, limiting, skipping

**Both halves.** `08_sort_limit.js` / `.py`

```js
db.students.find().sort({ "marks.maths": -1 }).limit(3)
db.students.find().sort({ dept: 1, "marks.maths": -1 })
db.students.find().skip(2).limit(2)
```

Asserted: **the server applies sort, then skip, then limit**, regardless of the
chaining order — so `.limit(3).sort(...)` sorts everything and then takes
three.

The script also demonstrates **range pagination** (`{ _id: { $gt: last } }`) as
the fix for `skip`'s linear cost.

## Experiment 9 — An embedded data model

**Both halves.** `09_embedded.js` / `.py`

```js
db.students.insertOne({
  _id: 21, name: "Asha Kumari",
  address: { city: "Vijayawada", state: "AP", pin: "520010" },
  enrollments: [ { course: "DSC301", grade: "A", credits: 4 },
                 { course: "STA302", grade: "B", credits: 3 } ]
})
db.students.find({ "address.city": "Vijayawada" })
db.students.find({ "enrollments.grade": "A" })
```

Asserted: **one read returns everything** — no join anywhere — and the
`$elemMatch` requirement for two conditions on the enrolment array.

## Experiment 10 — A normalized model with references

**Both halves.** `10_referenced.js` / `.py`

```js
db.students.insertOne({ _id: 21, name: "Asha", course_ids: ["DSC301"] })
db.courses.insertOne({ _id: "DSC301", title: "Data Science with R" })

db.enrollments.aggregate([
  { $lookup: { from: "courses", localField: "course_id",
               foreignField: "_id", as: "course" } },
  { $unwind: "$course" }
])
```

Asserted: `$lookup` produces an **array** even for a one-to-one match, which is
why `$unwind` follows it; and that it is a **left outer join** — an unmatched
document gets an empty array, not nothing.

## Experiment 11 — One-to-one, one-to-many, many-to-many

**Both halves.** `11_relationships.js` / `.py`

All three modelled and queried:

| Relationship | Model | Query direction |
|---|---|---|
| One-to-one | Embed the address | Both, from the student |
| One-to-many | Reference from the **child** | Course → its enrolments |
| Many-to-many | A junction collection | Both directions |

Asserted: querying both directions of the many-to-many, and that the junction
collection is what carries the **grade** — an attribute of the *relationship*,
belonging to neither entity.

## Experiment 12 — Schema validation with JSON Schema

**Both halves.** `12_validation.js` / `.py`

```js
db.createCollection("students", {
  validator: { $jsonSchema: {
    bsonType: "object",
    required: ["roll", "name", "dept"],
    properties: {
      roll: { bsonType: "int", minimum: 1 },
      name: { bsonType: "string", minLength: 3 },
      dept: { enum: ["DS", "Stats", "CS"] }
    } } },
  validationLevel: "strict", validationAction: "error"
})
```

**mongomock does not enforce `$jsonSchema`.** Rather than pretend, the Python
half implements the **same rules in code** and asserts that conforming
documents pass and each kind of violation is caught — a missing required field,
a wrong type, a value outside the enum. The header says exactly this.

It also demonstrates the migration path for a live collection:
`moderate` + `warn`, find the offenders with
`{ $nor: [ { $jsonSchema: … } ] }`, fix them, then tighten to
`strict` + `error`.

## Experiment 13 — Single-field and compound indexes

**Both halves.** `13_indexes.js` / `.py`

```js
db.students.createIndex({ dept: 1 })
db.students.createIndex({ dept: 1, "marks.maths": -1 })
db.students.getIndexes()
db.students.find({ dept: "DS" }).explain("executionStats")
db.students.dropIndex("dept_1")
```

mongomock records indexes but does not report `IXSCAN`, so the Python half
asserts that the indexes are **created and listed** correctly and that a
**unique** index rejects a duplicate. The **prefix rule** and **ESR** are
demonstrated as a table of which queries each index serves.

**On a real server, run `explain("executionStats")` and read
`totalDocsExamined / nReturned`** — that ratio, not the wall-clock time, is
what tells you whether the index is right.

## Experiment 14 — Text search and multikey indexes

**Both halves.** `14_text_multikey.js` / `.py`

```js
db.articles.createIndex({ title: "text", body: "text" },
                        { weights: { title: 10, body: 1 } })
db.articles.find({ $text: { $search: "mongodb aggregation" } })
db.students.createIndex({ subjects: 1 })          // MULTIKEY, automatically
```

Asserted for multikey: an index on an array field creates **one entry per
element**, so `{ subjects: "DS" }` matches any student whose array contains it.

**Only one text index is allowed per collection** — it may span several fields,
but you cannot have two. The Python half asserts the multikey behaviour and
documents the text-index rules, since mongomock does not implement `$text`.

## Experiment 15 — `$match`, `$group`, `$project`, `$sort`

**Both halves.** `15_aggregation.js` / `.py`

```js
db.students.aggregate([
  { $match:   { active: true } },
  { $group:   { _id: "$dept", avg: { $avg: "$marks.maths" },
                n: { $sum: 1 } } },
  { $match:   { n: { $gt: 1 } } },                 // HAVING
  { $sort:    { avg: -1 } },
  { $project: { _id: 0, dept: "$_id", avg: { $round: ["$avg", 2] }, n: 1 } }
])
```

Asserted twice, and the pair is the point. **With** the `active: true`
filter, Kiran (DS, 71, inactive) is excluded, so DS is (88+65)/2 = **76.5**
over 2 and Stats (94+52)/2 = **73** over 2. **Without** it — Unit 4's
Problem 1(a) — DS is (88+65+71)/3 = **74.667** over 3. Same grouping, and the
`$match` before it moves the DS average *up*.

The script also asserts that **`$match` before and after `$group` are `WHERE`
and `HAVING`** — the same stage in different positions — and that `$round` and
`$stdDevPop` are the two operators mongomock does not implement, so the
standard deviations are computed in Python and labelled as such.

## Experiment 16 — `$lookup`, `$unwind`, `$bucket`

**Both halves.** `16_advanced_agg.js` / `.py`

```js
db.students.aggregate([ { $unwind: "$subjects" },
                        { $group: { _id: "$subjects", n: { $sum: 1 } } } ])

db.students.aggregate([ { $bucket: {
  groupBy: "$marks.maths", boundaries: [0, 40, 60, 75, 101],
  default: "Other", output: { count: { $sum: 1 }, names: { $push: "$name" } } } } ])
```

Asserted: subject counts DS 3, Stats 3, Python 2, R 1; and the bucket
distribution — with the top boundary at **101, not 100**, because buckets are
`[lower, upper)` and 100 as the boundary would lose a perfect scorer to
`default`.

Also asserted: **`$unwind` silently drops empty and missing arrays**, and
`preserveNullAndEmptyArrays: true` keeps them. That one is worth seeing fail.

## Experiment 17 — Replication with a replica set

**NOT EXECUTED — needs three `mongod` processes.** `17_replication.js`

```js
rs.initiate({ _id: "rs0", members: [
  { _id: 0, host: "mongo1:27017" },
  { _id: 1, host: "mongo2:27017" },
  { _id: 2, host: "mongo3:27017" } ] })

rs.status()
rs.stepDown()                             // force a failover, then watch
rs.printSecondaryReplicationInfo()        // lag per secondary
db.c.insertOne(doc, { writeConcern: { w: "majority", j: true } })
```

To do this for real, `docker compose` with three `mongo` services is the
easiest route, or use Atlas — its free tier **is** a three-member replica set.

**What to demonstrate:** `rs.status()` showing one PRIMARY and two SECONDARY;
`rs.stepDown()` triggering an election; writes failing for 10–30 seconds during
it; and `w: "majority"` versus `w: 1`. The theory is Unit 5 §5.7 — and the
question "why an odd number of members?" is asked every year.

## Experiment 18 — GridFS

**NOT EXECUTED — mongomock does not implement GridFS.** `18_gridfs.js`

```bash
mongofiles -d collegeDB put lecture.mp4
mongofiles -d collegeDB list
mongofiles -d collegeDB get lecture.mp4
```

```js
db.fs.files.find()          // metadata: filename, length, chunkSize, uploadDate
db.fs.chunks.countDocuments()   // ceil(length / 255KB)
```

**What to demonstrate:** that a file appears as **one** document in `fs.files`
and **many** in `fs.chunks`, and that `chunks == ceil(bytes / 261120)`. The
point to state: GridFS is for files over 16 MB, or where you need to read
**ranges** — for smaller files, object storage is usually better.

## Experiment 19 — Transactions

**NOT EXECUTED — transactions require a replica set**, which mongomock is not.
`19_transactions.js`

```js
const session = db.getMongo().startSession()
session.startTransaction()
try {
  accounts.updateOne({ _id: "A" }, { $inc: { balance: -500 } })
  accounts.updateOne({ _id: "B" }, { $inc: { balance:  500 } })
  session.commitTransaction()
} catch (e) {
  session.abortTransaction()
  throw e
} finally { session.endSession() }
```

**Transactions are unavailable on a standalone `mongod`** — they depend on the
oplog and majority commit, so a replica set is required. That fact is itself a
five-mark answer.

**What to demonstrate:** a transfer that commits, and one that aborts midway
leaving **both** balances unchanged. And the point from Unit 5 §5.9: a schema
that needs transactions for its *common* operations is usually one that should
have embedded.

## Experiment 20 — Case study: a mini-application

**Both halves.** `20_case_study.js` / `.py`

A **library management system** — the schema designed in
[practice.md](practice.md) Section C question 1 — exercising CRUD, aggregation
and indexing together.

The Python half runs the whole workflow and asserts it:

1. Seed books, members and loans.
2. **Issue** a book: insert a loan and decrement `availableCopies`
   **conditionally** (`availableCopies: { $gt: 0 }`), so the sixth copy of a
   five-copy book cannot be lent.
3. **Return** it: set `returned`, compute any fine, increment the count back.
4. **Overdue report** — `{ returned: null, due: { $lt: now } }`.
5. **Most-borrowed** — an aggregation with `$match` first.
6. Assert `availableCopies` is **consistent** with the count of unreturned
   loans at every step.

That last assertion is the point of the experiment: the **computed pattern**
speeds up the hottest query and introduces a value that can drift, and the only
defence is to check it.

---

## Lab examination

An hour, a dataset, one experiment number, then a viva.

**What costs marks:**

- Using `updateOne` where `updateMany` was meant — silent, and reports success
- `replaceOne` destroying every other field
- Writing a range as two keys of one object
- Omitting `$elemMatch` for two conditions on an array of sub-documents
- Forgetting `$unwind` before grouping on array contents
- Forgetting `$unwind` after `$lookup` and getting an array
- Mixing inclusion and exclusion in a projection
- Putting `$match` after `$group` when it could have come first
- Setting `$bucket`'s top boundary to the maximum value and losing it
- Not knowing that `{ f: null }` matches missing fields too

**What earns them:**

- **Translate to SQL out loud.** "This `$group` is a `GROUP BY`, and this second
  `$match` is the `HAVING`." It shows you understand the pipeline rather than
  having memorised it.
- **Run `explain("executionStats")`** and quote
  `totalDocsExamined / nReturned`. That ratio is the answer to "is this query
  fast?", and wall-clock time on a five-document collection is not.
- **State the embed-or-reference decision and its cost.** "I embedded the
  address because it is one-to-one and bounded; I referenced the courses
  because embedding would duplicate the title across 300 students, and renaming
  the instructor would then be 300 updates."
- **Say what is *not* enforced.** Nothing stops a reference pointing at a
  deleted document. In Course 5 the database guaranteed it; here the
  application must.
- **When asked to demonstrate replication, GridFS or transactions, say what
  they require** — three `mongod` processes, and a replica set for
  transactions. Knowing *why* transactions need one (they depend on the oplog
  and majority commit) is worth more than a script you cannot run.
