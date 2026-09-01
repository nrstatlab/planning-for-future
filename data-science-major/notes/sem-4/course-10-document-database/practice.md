# Course 10 — Practice Questions with Solutions

Every query here has been **executed through mongomock** and its result
asserted by `tools/run_mongo_labs.py`. The
three topics mongomock cannot execute — replication, GridFS and transactions —
are answered from the documentation and say so.

---

## Section A — Two-mark questions

### 1. What does NoSQL stand for, and what does it mean?

**Not Only SQL.** A family of databases that each relax some relational
guarantee in exchange for horizontal scale, schema flexibility, or a data model
that fits the problem better. It does not mean "no SQL" — Cassandra's CQL looks
like SQL, and MongoDB's aggregation framework does what `GROUP BY` does.

### 2. State the CAP theorem, and say why "CA" is not a real choice.

A **distributed** data store can guarantee at most two of **Consistency**
(every read returns the latest write, or an error), **Availability** (every
request gets a non-error response) and **Partition tolerance** (it keeps
working when the network drops messages).

**Partitions are a fact of the environment, not a design decision** — cables
fail whatever you choose. So P is compulsory, and the real question is what
happens *during* a partition: **CP** refuses to serve rather than serve stale
data; **AP** serves stale data rather than refuse. A single-node database is CA
trivially, because there is nothing to partition.

**MongoDB is CP**; Cassandra is AP.

### 3. Give the MongoDB terms for table, row, column and primary key.

Collection, document, field, `_id`.

### 4. Distinguish JSON from BSON.

JSON is **text** with 6 types; BSON is **binary** with ~20. BSON adds native
**dates**, distinct **numeric types** (`int32`, `int64`, `double`,
`decimal128`) and **binary data**, and each element stores its own length so a
parser can skip fields. It is usually **slightly larger** than JSON but faster
to traverse.

### 5. What is an ObjectId?

The 12-byte default `_id`: **4 bytes timestamp, 5 bytes random per process, 3
bytes counter**. It is unique without coordination between clients, it embeds
its creation time (`getTimestamp()`), and it sorts roughly by creation order.

### 6. What is the maximum document size, and why does it matter?

**16 MB.** It is what makes an unbounded embedded array a design bug: a post
embedding all its comments eventually fails to write.

### 7. Distinguish `null`, a missing field and `undefined`.

`null` means the field **exists and is empty**; missing means it is **absent**;
`undefined` is deprecated and should not be used.

**`{ field: null }` matches both null and missing.** Use
`{ field: { $exists: false } }` for missing only, and
`{ field: { $type: "null" } }` for explicit nulls only.

### 8. Distinguish `$in` from `$all`.

`$in` matches if the field equals **any** of the listed values. `$all` matches
if an **array field contains all** of them, in any order.

### 9. What does `$elemMatch` do, and when is it needed?

It requires **one single array element** to satisfy **all** the given
conditions. Needed whenever you place **two or more conditions on an array of
sub-documents** — without it, MongoDB checks each condition against the whole
array independently and different elements may satisfy different conditions.

### 10. Distinguish `updateOne` from `replaceOne`.

`updateOne` with `$set` modifies the named fields and **preserves the rest**;
`replaceOne` **replaces the entire document**, keeping only `_id`.

### 11. Distinguish `$push` from `$addToSet`.

`$push` always appends; `$addToSet` appends **only if the value is not already
present** — a set rather than a list.

### 12. What is an upsert?

`{ upsert: true }` updates the matching document, or **inserts it if none
matches** — atomically, which is what makes it the correct way to implement a
counter. `$setOnInsert` applies only on the insert branch.

### 13. Why can a projection not mix inclusion and exclusion?

A projection is either a list of fields to **include** or a list to
**exclude**; mixing them is ambiguous. **`_id` is the one exception** — it is
included by default and may be excluded alongside inclusions.

### 14. What does `$unwind` do, and what does it silently drop?

It outputs **one document per array element**. It **silently drops** documents
whose array is empty or whose field is missing — use
`{ path: "$arr", preserveNullAndEmptyArrays: true }` to keep them.

### 15. Why must `$unwind` usually follow `$lookup`?

`$lookup` always writes its result into an **array**, even for a one-to-one
match. `$unwind` turns that one-element array into a sub-document so
`"$student.name"` is a name rather than an array of names.

### 16. Why must `$match` come first in a pipeline?

Two reasons. It reduces the volume every later stage processes; and **only a
`$match` at the start can use an index** — after `$group`, the documents are
computed values with no index behind them.

### 17. State the index prefix rule.

An index on `{a, b, c}` serves queries on `a`, `a+b` and `a+b+c` — **left-hand
prefixes only**. It does **not** serve `b` alone, or `c` alone. The phone book
sorted by *(surname, forename)* finds everyone called Kumari, but finding
everyone whose forename is Asha means reading the whole book.

### 18. State the ESR rule.

In a compound index, order the fields **Equality, Sort, Range**. A range
predicate leaves everything after it unordered, so a sort field placed after a
range field cannot use the index.

### 19. What is a covered query?

One where **every field in the filter and the projection is in the index**, so
MongoDB answers from the index and never reads the documents.
`totalDocsExamined` is 0. Remember `_id: 0`, or `_id` breaks the coverage.

### 20. Why must a replica set have an odd number of members?

A primary needs a **majority** of votes. With an even number, a partition can
split the set into two equal halves, **neither with a majority**, so no primary
is elected and the set goes read-only. **Four members survive no more failures
than three.**

### 21. Distinguish `w: 1` from `w: "majority"`.

`w: 1` acknowledges once the **primary** has the write; `w: "majority"` waits
for a majority of members. **A `w: 1` write that has not replicated is rolled
back if the primary fails** — genuinely lost. `w: "majority"` cannot be.

### 22. Why is replication not a backup?

It copies **every** operation, including `deleteMany({})`, to all members within
milliseconds. It protects against **hardware failure**, not **mistakes**.

### 23. What is GridFS, and when do you need it?

A convention for storing files larger than 16 MB by splitting them into 255 KB
chunks across `fs.files` (metadata) and `fs.chunks` (the data). Needed for large
files, or when you want to read **ranges** of one — seeking into a video fetches
a few chunks, not the whole file.

### 24. Does MongoDB support transactions?

**Yes.** Single-document writes have always been atomic; **multi-document ACID
transactions** have existed since **4.0** (replica sets) and **4.2** (sharded
clusters). Saying "NoSQL cannot do ACID" is out of date.

---

## Section B — Five-mark questions

### 1. Compare RDBMS and MongoDB.

| | RDBMS | MongoDB |
|---|---|---|
| Unit | Row, split across tables | **Document**, whole |
| Schema | Fixed, enforced on write | **Flexible**, optional validation |
| Language | SQL | MQL + aggregation pipeline |
| Relationships | Joins, enforced foreign keys | Embedding, or **unenforced** references |
| Redundancy | Eliminated | **Accepted** for read speed |
| Transactions | ACID across tables | Per document; multi-document since 4.0 |
| Scaling | Vertical | **Horizontal** (sharding) |
| Best at | Complex queries, integrity, reporting | Scale, flexibility, whole-entity reads |

**The vocabulary map:** database → database, table → **collection**, row →
**document**, column → **field**, primary key → **`_id`**, JOIN → embedding or
`$lookup`, `GROUP BY` → `$group`.

**The row that matters most:** a MongoDB reference is **not enforced**. It will
store an id pointing at nothing, and will not stop you deleting the target.
Course 5's database guaranteed referential integrity for free; here the
application must.

### 2. Explain embedded and referenced models with the decision criteria.

**Embedded** puts the child inside the parent; **referenced** puts it in another
collection, linked by `_id`.

| Consider | Embed | Reference |
|---|---|---|
| Relationship | One-to-one, one-to-few | One-to-many, many-to-many |
| Accessed | **Always together** | Independently |
| Child size | Small, **bounded** | Large, **unbounded** |
| Changes | Rarely | Often |
| Reads to assemble | **One** | Two, or `$lookup` |
| Atomicity | **Guaranteed** | Needs a transaction |

**The rule:** embed when the child is **small, bounded and always read with the
parent**; reference when it is **large, unbounded, shared or independently
updated**.

**The unbounded-array trap** is what the rule exists to prevent. Embedding
comments in a post fails three ways: the document eventually exceeds **16 MB**;
every read pulls all 50,000 comments; and every write rewrites the whole
document and may move it on disk, invalidating index entries. The **subset
pattern** is the fix — embed the five you display, reference the rest.

### 3. Explain the CRUD operations with examples.

```js
// CREATE
db.students.insertOne({ _id: 26, name: "Devi", dept: "Stats" })
db.students.insertMany([...], { ordered: false })   // continue past errors

// READ
db.students.find({ dept: "DS", age: { $gt: 20 } })
db.students.findOne({ _id: 21 })
db.students.find({ "marks.maths": { $gte: 90 } })   // dot notation

// UPDATE
db.students.updateOne({ _id: 21 }, { $set: { age: 21 } })
db.students.updateMany({ dept: "DS" }, { $inc: { "marks.maths": 5 } })
db.students.replaceOne({ _id: 21 }, { name: "Asha" })   // DESTROYS the rest
db.students.updateOne({ _id: 99 }, { $inc: { n: 1 } }, { upsert: true })

// DELETE
db.students.deleteOne({ _id: 21 })
db.students.deleteMany({ dept: "DS" })
db.students.deleteMany({})              // EVERY document
```

**Three points worth stating.** `ordered: true` is the default for
`insertMany`, so it **stops at the first error** and later documents are never
attempted; `ordered: false` continues. `updateOne` changes **one** document
even when many match — which one is not guaranteed. And `replaceOne` keeps only
`_id`; modern MongoDB rejects a bare document passed to `updateOne` precisely
to stop this being an accident.

### 4. Explain the query operators.

| Category | Operators |
|---|---|
| **Comparison** | `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin` |
| **Logical** | `$and`, `$or`, `$not`, `$nor` |
| **Element** | `$exists`, `$type` |
| **Evaluation** | `$regex`, `$expr`, `$mod`, `$text` |
| **Array** | `$all`, `$size`, `$elemMatch` |

```js
db.students.find({ age: { $gte: 20, $lte: 21 } })       // a range: ONE object
db.students.find({ dept: { $in: ["DS", "CS"] } })
db.students.find({ $or: [ { dept: "Stats" }, { age: 20 } ] })
db.students.find({ $expr: { $gt: ["$marks.maths", "$marks.stats"] } })
db.students.find({ subjects: { $all: ["DS", "Python"] } })
```

**Three traps.** Two conditions on one field go in **the same object** —
writing them as two keys gives a JavaScript object with a duplicate key and the
first is silently discarded. **`$ne`, `$nin` and `$not` also match documents
where the field is missing.** And **only `$expr` compares two fields of the
same document**; an ordinary query compares a field to a constant.

### 5. Explain the aggregation pipeline with the SQL mapping.

A **sequence of stages**, each transforming the stream and passing it on.

| SQL | Stage |
|---|---|
| `WHERE` | **`$match`** (before `$group`) |
| `GROUP BY` | **`$group`** |
| `HAVING` | **`$match`** (after `$group`) |
| `SELECT` | `$project` |
| `ORDER BY` | `$sort` |
| `LIMIT` | `$limit` |
| `JOIN` | `$lookup` |
| — | **`$unwind`** (no SQL equivalent) |

```js
db.students.aggregate([
  { $match: { active: true } },                          // WHERE
  { $group: { _id: "$dept", n: { $sum: 1 },
              avg: { $avg: "$marks.maths" } } },          // GROUP BY
  { $match: { n: { $gt: 1 } } },                          // HAVING
  { $sort:  { avg: -1 } }                                 // ORDER BY
])
```

**`WHERE` and `HAVING` are the same stage in different positions**, which is
the neatest way to remember why order matters — and why `$match` belongs first
whenever it can be.

### 6. Explain indexing with the index types.

An index is a **B-tree of sorted keys** turning an O(n) collection scan into an
O(log n) lookup. `_id` is indexed automatically.

| Type | For |
|---|---|
| **Single field** | One field; direction is irrelevant |
| **Compound** | Several fields; **prefix rule** and **ESR** apply |
| **Multikey** | An array field — **one entry per element**, created automatically |
| **Text** | Full-text search; **only one per collection** |
| **Hashed** | Sharding; no range queries |
| **Geospatial** | Coordinates |
| **TTL** | Automatic expiry |
| **Partial / sparse** | Index a subset of documents |
| **Unique** | Enforce uniqueness |

**The cost:** every insert, update and delete maintains **every** index, and
each index consumes disk and wants to be in RAM. **Index what you query, not
everything.**

**One gotcha worth stating:** a unique index treats a **missing field as
`null`**, so it allows one document without the field and rejects every other.
Use a partial index with `{ $exists: true }`.

### 7. Explain replica sets, elections and failover.

A **replica set** is a group of `mongod` processes holding the same data: one
**primary** taking all writes, and **secondaries** replaying its **oplog** — a
capped collection of idempotent operations.

**Election:** heartbeats every 2 seconds; after 10 seconds of silence a
secondary calls an election; a candidate needs a **majority**; the winner
becomes primary; the old primary returns as a secondary and **rolls back** any
writes that never replicated.

**Failover takes 10–30 seconds, during which writes fail** — MongoDB's CP choice
made visible.

**Odd numbers matter** because a majority is required: an even set can split
into two equal halves with no majority in either, leaving the whole set
read-only. Three or five; an **arbiter** (votes, holds no data) makes an even
set odd cheaply.

**Write concern** controls how many members must acknowledge: `w: 1` (the
primary only, the default) versus `w: "majority"`. **Only `w: "majority"`
survives a failover** — a `w: 1` write that has not replicated is rolled back.

### 8. Explain query optimization.

1. **Measure with `explain("executionStats")`.** Look for `stage: COLLSCAN`
   (bad) versus `IXSCAN` (good), and the ratio
   **`totalDocsExamined / nReturned`** — 1 is ideal, 1000 means the index is
   wrong or missing.
2. **Index the fields you filter and sort on**, following **ESR**.
3. **Project only what you need** — fewer bytes, and possibly a **covered**
   query with `totalDocsExamined: 0`.
4. **`$match` first** in a pipeline; only an early `$match` uses an index.
5. **Range-paginate instead of `skip`** — `skip(100000)` walks and discards
   100,000 documents.
6. **Anchor regexes and match case** — only `/^x/` without `i` uses an index.
7. **Know what cannot use an index**: `$ne`, `$nin`, `$exists: false`,
   unanchored `$regex`, `$where`.

An **unindexed sort fails outright past 100 MB** — index the sort key, or pass
`allowDiskUse: true` and accept it will be slow.

---

## Section C — Ten-mark questions

### 1. Design a complete schema for a library management system

**Question.** Books have an ISBN, title, author, publisher and copies; members
have an id, name, contact details and address; a member borrows a book on a date
and returns it. Design the collections, justify every embed and reference
decision, and write the main queries.

**Solution.**

**Step 1 — list the queries, because in MongoDB they determine the model:**

1. Look up a book by ISBN and see how many copies are available. *(constant)*
2. Show a member's profile and what they currently have out. *(constant)*
3. Issue and return a book. *(constant)*
4. Find overdue loans. *(daily)*
5. Report the most-borrowed books this year. *(monthly)*

**Step 2 — the collections:**

```js
// books
{ _id: "978-1491954461",                    // the ISBN: a NATURAL key
  title: "MongoDB: The Definitive Guide",
  authors: ["Shannon Bradshaw", "Kristina Chodorow"],   // one-to-few: EMBED
  publisher: { name: "O'Reilly", year: 2019 },          // one-to-one: EMBED
  subjects: ["databases", "nosql"],
  totalCopies: 5,
  availableCopies: 3                        // COMPUTED pattern
}

// members
{ _id: "M2026001",
  name: "Asha Kumari",
  email: "asha@nri.ac.in",
  phones: ["9876543210"],                                // one-to-few: EMBED
  address: { city: "Vijayawada", state: "AP", pin: "520010" },  // EMBED
  joined: ISODate("2026-07-01"),
  active: true,
  currentLoanCount: 2                       // COMPUTED, for the limit check
}

// loans -- the junction collection
{ _id: ObjectId(),
  member_id: "M2026001",
  isbn: "978-1491954461",
  book_title: "MongoDB: The Definitive Guide",   // EXTENDED REFERENCE
  member_name: "Asha Kumari",                    // EXTENDED REFERENCE
  issued: ISODate("2026-08-01"),
  due:    ISODate("2026-08-15"),
  returned: null,                                // null until returned
  fine: 0
}
```

**Step 3 — justify each decision:**

| Decision | Why |
|---|---|
| **ISBN as `_id`** | A real, unique, meaningful key. Saves a lookup just to display it, and enforces uniqueness for free. Better than an ObjectId when a natural key exists. |
| **`authors` embedded as an array** | One-to-few, bounded (a book has a handful of authors), always shown with the book, never queried alone. Textbook embed. |
| **`publisher` embedded** | One-to-one, three small fields. Referencing would mean a second collection and a join for no benefit. *(If the library needed a publisher catalogue with its own attributes, this would become a reference.)* |
| **`address` embedded** | One-to-one, small, bounded, always read with the member. |
| **A separate `loans` collection** | **The relationship has its own attributes** — issue date, due date, fine. Those belong to neither the book nor the member. Course 5's junction table, and the reasoning survives exactly. |
| **Loans NOT embedded in the member** | The array is **unbounded** — a member borrows for years. This is precisely the 16 MB trap, and query 4 (overdue across all members) would have to scan every member and unwind. |
| **`availableCopies` stored** | The **computed pattern**: query 1 runs constantly, and counting unreturned loans each time would be a full scan of `loans`. Update it on issue and return. |
| **`book_title` and `member_name` duplicated** | The **extended reference pattern**: the overdue report (query 4) shows both, and without them it needs two `$lookup` stages on every run. |

**Step 4 — the indexes:**

```js
db.books.createIndex({ title: "text", authors: "text" })   // search
db.books.createIndex({ subjects: 1 })                      // multikey
db.loans.createIndex({ member_id: 1, returned: 1 })        // query 2
db.loans.createIndex({ returned: 1, due: 1 })              // query 4, ESR
db.loans.createIndex({ isbn: 1, issued: -1 })              // query 5
db.members.createIndex({ email: 1 }, { unique: true })
```

`{ returned: 1, due: 1 }` follows **ESR**: `returned: null` is the equality
predicate, `due` the range.

**Step 5 — the queries:**

```js
// 1. availability
db.books.findOne({ _id: "978-1491954461" }, { title: 1, availableCopies: 1 })

// 2. a member's current loans
db.loans.find({ member_id: "M2026001", returned: null })

// 3. issue -- two writes that must both succeed
const session = db.getMongo().startSession()
session.startTransaction()
try {
  db.loans.insertOne({ member_id, isbn, book_title, member_name,
                       issued: new Date(), due: dueDate, returned: null, fine: 0 })
  db.books.updateOne({ _id: isbn, availableCopies: { $gt: 0 } },
                     { $inc: { availableCopies: -1 } })
  session.commitTransaction()
} catch (e) { session.abortTransaction(); throw e }

// 4. overdue
db.loans.find({ returned: null, due: { $lt: new Date() } })
        .sort({ due: 1 })

// 5. most borrowed this year
db.loans.aggregate([
  { $match: { issued: { $gte: ISODate("2026-01-01") } } },   // FIRST
  { $group: { _id: "$isbn", title: { $first: "$book_title" },
              times: { $sum: 1 } } },
  { $sort:  { times: -1 } },
  { $limit: 10 }
])
```

**Step 6 — what I would still watch, which is what earns the last marks:**

- **The denormalised fields must be maintained.** Renaming a member updates
  their open loans too. Acceptable because names rarely change; if they changed
  often I would drop the duplication and accept the `$lookup`.
- **`availableCopies` can drift** if a write fails halfway. Query 3 uses a
  **transaction** for exactly this reason — and note the guard
  `availableCopies: { $gt: 0 }` in the filter, which makes the decrement
  **atomically conditional** and prevents lending the sixth copy of a five-copy
  book under concurrency.
- **Nothing enforces that `isbn` points at a real book.** In Course 5 a foreign
  key would. Here the application must check, and a nightly integrity job is
  worth having.
- **Add schema validation** on all three collections. The fields here are
  genuinely known, so the flexibility buys nothing and costs consistency.

### 2. Given a collection, write queries covering every operator category

**Question.** Using the `students` collection of Unit 3, demonstrate
comparison, logical, element, evaluation and array operators, plus updates and
an aggregation.

**Solution.**

```js
// --- COMPARISON ------------------------------------------------------------
db.students.find({ age: { $gt: 20 } })                    // Ravi, Kiran, Bhanu
db.students.find({ age: { $gte: 20, $lte: 21 } })         // ONE object = a range
db.students.find({ dept: { $in: ["DS", "CS"] } })         // Asha, Ravi, Kiran
db.students.find({ dept: { $nin: ["Stats"] } })
db.students.find({ "marks.maths": { $ne: 88 } })

// --- LOGICAL ---------------------------------------------------------------
db.students.find({ dept: "DS", age: { $lt: 22 } })        // implicit AND
db.students.find({ $or: [ { dept: "Stats" },
                          { "marks.maths": { $gt: 85 } } ] })
db.students.find({ $nor: [ { dept: "DS" }, { age: 20 } ] })   // Bhanu only
db.students.find({ age: { $not: { $gt: 21 } } })

// --- ELEMENT ---------------------------------------------------------------
db.students.find({ email: { $exists: false } })
db.students.find({ age: { $type: "int" } })

// --- EVALUATION ------------------------------------------------------------
db.students.find({ name: /^A/ })                          // Asha
db.students.find({ name: { $regex: "asha", $options: "i" } })
db.students.find({ $expr: { $gt: ["$marks.maths", "$marks.stats"] } })
//   -> Ravi, Meena, Kiran, Bhanu   (only $expr compares two FIELDS)

// --- ARRAY -----------------------------------------------------------------
db.students.find({ subjects: "DS" })                      // ANY element
db.students.find({ subjects: { $all: ["DS", "Python"] } }) // BOTH: Asha, Ravi
db.students.find({ subjects: { $size: 3 } })              // Asha
db.students.find({ "subjects.0": "DS" })                  // FIRST is DS

// --- UPDATES ---------------------------------------------------------------
db.students.updateOne({ _id: 21 }, {
  $set:   { "marks.python": 85 },
  $inc:   { age: 1 },
  $unset: { active: "" },
  $currentDate: { updated: true }
})
db.students.updateMany({ dept: "DS" }, { $inc: { "marks.maths": 5 } })
db.students.updateOne({ _id: 21 }, { $addToSet: { subjects: "R" } })
db.students.updateOne({ _id: 21 }, { $pull: { subjects: "Python" } })

// --- AGGREGATION -----------------------------------------------------------
db.students.aggregate([
  { $unwind: "$subjects" },
  { $group:  { _id: "$subjects", n: { $sum: 1 } } },
  { $sort:   { n: -1, _id: 1 } }
])
// DS 3, Stats 3, Python 2, R 1
```

**The five points that earn the marks:**

1. **A range is one object.** `{ age: { $gte: 20, $lte: 21 } }`. Written as two
   keys it is a JavaScript object with a duplicate key — the first is silently
   discarded and the query is wrong with no error.
2. **`$in` versus `$all`.** `$in` is "any of these"; `$all` is "contains all of
   these". Different questions.
3. **Only `$expr` compares two fields** of the same document.
4. **`$addToSet` is idempotent** where `$push` would append a duplicate every
   time it ran.
5. **`$unwind` is mandatory** before grouping on array contents — grouping on
   `"$subjects"` directly would group by the **whole array**.

### 3. Compare relational and document modelling of the same system

**Question.** Model a student–course enrolment system relationally and as
documents. Compare the two on schema, queries, performance and integrity.

**Solution.**

**Relational (Course 5):**

```sql
CREATE TABLE students (
  roll INT PRIMARY KEY, name VARCHAR(80), dept VARCHAR(20),
  city VARCHAR(50), state VARCHAR(50), pin CHAR(6));

CREATE TABLE courses (
  code VARCHAR(10) PRIMARY KEY, title VARCHAR(100),
  credits INT, instructor VARCHAR(80));

CREATE TABLE enrollments (
  roll INT REFERENCES students(roll),
  code VARCHAR(10) REFERENCES courses(code),
  grade CHAR(1), enrolled_on DATE,
  PRIMARY KEY (roll, code));
```

**Document (Course 10):**

```js
// students -- address EMBEDDED
{ _id: 21, name: "Asha Kumari", dept: "DS",
  address: { city: "Vijayawada", state: "AP", pin: "520010" } }

// courses
{ _id: "DSC301", title: "Data Science with R", credits: 4,
  instructor: "Dr. Rao" }

// enrollments -- the junction, with extended references
{ _id: ObjectId(), student_id: 21, course_id: "DSC301",
  grade: "A", enrolled_on: ISODate("2026-07-01"),
  student_name: "Asha Kumari", course_title: "Data Science with R" }
```

**The comparison:**

| | Relational | Document |
|---|---|---|
| **Address** | Three columns, or a fourth table | **One embedded sub-document** |
| **Adding a field** | `ALTER TABLE`, a migration, downtime | Write it; no migration |
| **A student's profile** | 1 query | 1 query |
| **A student with their courses** | 1 query, 2 joins | 1 query on `enrollments` (thanks to the extended reference) |
| **Everyone on a course** | 1 query, 2 joins | 1 query on `enrollments` |
| **Renaming a student** | **1 update** | **1 + N updates** — the copies |
| **Referential integrity** | **Enforced by the database** | **The application's job** |
| **Atomic multi-table change** | Free, in a transaction | Needs an explicit transaction |
| **Average grade per course** | `GROUP BY`, mature optimiser | Aggregation pipeline |
| **Reporting tools** | Every BI tool | Few |
| **Scaling to 100M enrolments** | Vertical, then hard | **Sharding, built in** |

**Where each wins, plainly:**

**Relational wins on integrity and ad-hoc querying.** The foreign keys mean an
enrolment cannot reference a student who does not exist — the database
guarantees it, permanently, regardless of which application writes. And a
question nobody anticipated is one join away.

**Document wins on read shape and evolution.** The address needs no join ever;
the extended reference removes the join from the two hottest queries; and a new
field costs nothing.

**The honest conclusion.** This particular system is **relational in nature**:
the entities are well defined, the schema is stable, the relationships are
queried from several directions, and integrity matters. Course 5's design is
the better fit, and a document model here mostly reimplements joins in
application code.

MongoDB would win if the requirements changed to: a **product catalogue** with
different attributes per category; **event or sensor data** with enormous write
volume; data that arrives as **JSON** and is read back whole; or a scale that
requires sharding.

**The professional answer is polyglot persistence** — the enrolment system in
PostgreSQL, the course content and media in MongoDB, the session cache in
Redis. "Which database is better?" is the wrong question; "which access pattern
does this data have?" is the right one.

---

## Section D — The three topics that could not be executed

The lab runner uses **mongomock**, which implements the query and aggregation
language but is **not a server**. These three therefore have no runnable
equivalent, and the answers below are from the documentation.

### Replication (experiment 17)

Requires three `mongod` processes and `rs.initiate()`. The concepts —
oplog, elections, majority voting, write concern, read preference, rollback —
are in Unit 5 §5.7, and the failover demonstration (`rs.stepDown()`, watch
`rs.status()`) needs a real cluster.

### GridFS (experiment 18)

Requires the `fs.files` / `fs.chunks` machinery and the `mongofiles` tool.
mongomock does not implement it. Unit 5 §5.9 covers the 255 KB chunking and
when GridFS is the right choice over object storage.

### Transactions (experiment 19)

Requires a **replica set** — transactions are unavailable on a standalone
`mongod`, and mongomock has no session support. Unit 5 §5.9 gives the
`startSession` / `commitTransaction` / `abortTransaction` pattern and, more
importantly, the point that **a schema needing transactions for its common
operations is usually a schema that should have embedded**.

**Say this in the viva if asked to demonstrate any of the three.** Knowing that
transactions need a replica set — and *why*, because they rely on the oplog and
majority commit — is itself the answer to a five-mark question.
