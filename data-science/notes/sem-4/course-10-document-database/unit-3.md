# Unit 3 — CRUD Operations and Querying in MongoDB

**Syllabus topics:** CRUD operations — insert documents (insertOne,
insertMany), query documents (find, operators, conditions), update documents
(updateOne, updateMany, replaceOne), delete documents (deleteOne, deleteMany).
Query operators (`$gt`, `$lt`, `$in`, `$nin`, `$and`, `$or`, `$not`), regular
expression queries, bulk operations, working with arrays.

---

## 3.1 The sample data

Everything below runs against this collection.

```js
db.students.insertMany([
  { _id: 21, name: "Asha",  dept: "DS",    marks: { maths: 88, stats: 91 },
    subjects: ["DS", "Stats", "Python"], age: 20, active: true },
  { _id: 22, name: "Ravi",  dept: "DS",    marks: { maths: 65, stats: 58 },
    subjects: ["DS", "Python"],          age: 21, active: true },
  { _id: 23, name: "Meena", dept: "Stats", marks: { maths: 94, stats: 89 },
    subjects: ["Stats", "R"],            age: 20, active: true },
  { _id: 24, name: "Kiran", dept: "DS",    marks: { maths: 71, stats: 66 },
    subjects: ["DS"],                    age: 22, active: false },
  { _id: 25, name: "Bhanu", dept: "Stats", marks: { maths: 52, stats: 47 },
    subjects: ["Stats"],                 age: 21, active: true }
])
```

## 3.2 Create

```js
db.students.insertOne({ _id: 26, name: "Devi", dept: "Stats" })
db.students.insertMany([ { name: "A" }, { name: "B" } ])
db.students.insertMany(docs, { ordered: false })     // keep going after an error
```

| Method | Returns |
|---|---|
| `insertOne` | `{ acknowledged, insertedId }` |
| `insertMany` | `{ acknowledged, insertedIds }` |

### ⚠️ `ordered: true` is the default, and it stops on the first error

```js
db.students.insertMany([
  { _id: 30, name: "X" },
  { _id: 21, name: "DUPLICATE" },     // _id 21 already exists -> error
  { _id: 31, name: "Y" }
])
// ordered (default): 30 inserted, 21 fails, 31 NEVER ATTEMPTED
// { ordered: false }: 30 and 31 inserted, only 21 fails
```

`ordered: false` also lets the server insert in parallel, so it is faster for a
bulk load — at the cost of losing insertion order. This exact behaviour is a
guaranteed exam question.

`insert()` (without One/Many) is **deprecated**; use the explicit forms.

## 3.3 Read

```js
db.students.find()                                    // everything
db.students.find({ dept: "DS" })                      // equality
db.students.find({ dept: "DS", age: 20 })             // implicit AND
db.students.findOne({ _id: 21 })                      // ONE document, or null
db.students.find({ "marks.maths": { $gt: 80 } })      // DOT NOTATION for nesting
db.students.find().pretty()
db.students.countDocuments({ dept: "DS" })
db.students.distinct("dept")                          // ["DS", "Stats"]
```

### ⚠️ `find` returns a cursor; `findOne` returns a document

`find()` gives a **cursor** — lazy, batched, and iterable. `findOne()` gives
the document itself, or `null`. So `db.c.find({_id:1}).name` is `undefined`
while `db.c.findOne({_id:1}).name` works. In `mongosh` the cursor prints its
first 20 documents, which hides the distinction until it bites.

### Dot notation

```js
db.students.find({ "marks.maths": { $gte: 90 } })     // into a sub-document
db.students.find({ "subjects.0": "DS" })              // the FIRST array element
db.students.find({ subjects: "DS" })                  // ANY element equals "DS"
```

**Quote the key when it contains a dot.** `{ marks.maths: ... }` is a
JavaScript syntax error; `{ "marks.maths": ... }` is correct.

## 3.4 Comparison operators

| Operator | Meaning |
|---|---|
| `$eq` | Equal (implicit when you write a bare value) |
| `$ne` | Not equal |
| `$gt`, `$gte` | Greater than, or equal |
| `$lt`, `$lte` | Less than, or equal |
| `$in` | In an array of values |
| `$nin` | Not in |

```js
db.students.find({ age: { $gt: 20 } })                       // 22, 24, 25
db.students.find({ age: { $gte: 20, $lte: 21 } })            // a RANGE
db.students.find({ dept: { $in: ["DS", "CS"] } })
db.students.find({ dept: { $nin: ["Stats"] } })
db.students.find({ "marks.maths": { $ne: 88 } })
```

**Two conditions on one field go in the same object**, as the range above
shows. Writing `{ age: { $gte: 20 }, age: { $lte: 21 } }` is a JavaScript
object with a duplicate key — **the first is silently discarded** and you get
everything under 21. That is a real and invisible bug.

### ⚠️ `$ne` and `$nin` also match missing fields

```js
db.students.find({ dept: { $ne: "DS" } })
```

This returns Stats students **and any document with no `dept` field at all** —
because "not equal to DS" is true of a field that does not exist. Combine with
`$exists: true` when that matters.

## 3.5 Logical operators

| Operator | Meaning |
|---|---|
| `$and` | All conditions |
| `$or` | Any condition |
| `$not` | Inverts **one operator expression** |
| `$nor` | **None** of the conditions |

```js
// Implicit AND -- the usual form
db.students.find({ dept: "DS", age: { $lt: 22 } })

// Explicit $and -- needed only for two conditions on the SAME field
db.students.find({ $and: [ { age: { $gte: 20 } }, { age: { $lte: 21 } } ] })

db.students.find({ $or: [ { dept: "Stats" }, { "marks.maths": { $gt: 85 } } ] })

db.students.find({ $nor: [ { dept: "DS" }, { age: 20 } ] })
// neither DS nor aged 20 -> Bhanu (Stats, 21)

db.students.find({ age: { $not: { $gt: 21 } } })      // NOT greater than 21

// Combining them
db.students.find({
  dept: "DS",
  $or: [ { "marks.maths": { $gt: 80 } }, { "marks.stats": { $gt: 80 } } ]
})
```

### ⚠️ `$not` cannot take a plain value

```js
db.students.find({ age: { $not: 21 } })              // ERROR
db.students.find({ age: { $not: { $eq: 21 } } })     // correct
db.students.find({ age: { $ne: 21 } })               // simpler
```

`$not` inverts an **operator expression**, not a value. And like `$ne`, it
matches documents where the field is **missing**.

### 🔢 `$nor` versus `$not`

`$nor` takes an **array of conditions** and matches documents satisfying
**none** of them. `$not` inverts a **single** operator expression on **one**
field. `$nor: [A, B]` is `NOT (A OR B)`, which is `(NOT A) AND (NOT B)` — De
Morgan's law, from Course 1.

## 3.6 Element and evaluation operators

| Operator | Matches |
|---|---|
| `$exists` | Whether the field is present |
| `$type` | The BSON type |
| `$regex` | A regular expression |
| `$expr` | Compares **two fields** of the same document |
| `$mod` | `value % divisor == remainder` |
| `$text` | A full-text search (needs a text index — Unit 5) |
| `$where` | Arbitrary JavaScript — **avoid** |

```js
db.students.find({ email: { $exists: false } })
db.students.find({ age: { $type: "int" } })
db.students.find({ age: { $type: ["int", "double"] } })

// Compare two fields of the SAME document -- impossible without $expr
db.students.find({ $expr: { $gt: ["$marks.maths", "$marks.stats"] } })
```

**`$expr` is the one worth remembering.** A normal query compares a field to a
*constant*; only `$expr` compares a field to **another field**, and it is the
answer to "find students who scored higher in maths than in statistics".

**Avoid `$where`.** It runs JavaScript per document, cannot use indexes, and is
an injection risk. Almost anything it can do, `$expr` does faster and safely.

## 3.7 Regular expression queries

```js
db.students.find({ name: /^A/ })                       // starts with A
db.students.find({ name: { $regex: "^A" } })           // the same
db.students.find({ name: { $regex: "asha", $options: "i" } })   // case-insensitive
db.students.find({ name: /a$/i })                      // ends with a
db.students.find({ name: { $regex: "^(A|M)" } })       // A or M
db.students.find({ subjects: { $regex: "^P" } })       // matches ANY array element
```

| Option | Meaning |
|---|---|
| `i` | Case-insensitive |
| `m` | `^`/`$` match line boundaries |
| `x` | Ignore whitespace in the pattern |
| `s` | `.` matches newline |

### ⚠️ Only an anchored, case-sensitive regex can use an index

```js
db.students.find({ name: /^Asha/ })       // CAN use an index on name
db.students.find({ name: /Asha/ })        // full COLLECTION SCAN
db.students.find({ name: /^Asha/i })      // full scan -- 'i' defeats the index
```

An index stores values in sorted order, so a prefix match (`^Asha`) is a range
scan. A pattern that can match anywhere, or that ignores case, has no range to
scan and every document must be examined. **For case-insensitive search at
scale, use a text index or a collation, not `$options: "i"`.**

## 3.8 Array queries

### 🔢 The operators

| Operator | Matches |
|---|---|
| `{ arr: v }` | **Any** element equals `v` |
| `{ arr: [a, b] }` | The array is **exactly** `[a, b]`, in order |
| `$all` | Contains **all** of these, in any order |
| `$size` | Has exactly this many elements |
| `$elemMatch` | **One single element** satisfies all the criteria |
| `arr.N` | The element at index N |

```js
db.students.find({ subjects: "DS" })                    // any element is "DS"
db.students.find({ subjects: ["DS", "Python"] })        // EXACTLY that array
db.students.find({ subjects: { $all: ["DS", "Python"] } })  // both, any order
db.students.find({ subjects: { $size: 3 } })            // exactly 3 subjects
db.students.find({ "subjects.0": "DS" })                // FIRST subject is DS
```

### ⚠️ `$elemMatch` — the array query that catches everyone

Consider an array of sub-documents:

```js
{ name: "Asha", scores: [ { subject: "maths", mark: 45 },
                          { subject: "stats", mark: 91 } ] }
```

Now: *"find students with a score above 80 in maths."*

```js
// WRONG -- matches Asha!
db.c.find({ "scores.subject": "maths", "scores.mark": { $gt: 80 } })

// RIGHT
db.c.find({ scores: { $elemMatch: { subject: "maths", mark: { $gt: 80 } } } })
```

The first query asks "does **some** element have subject maths?" **and**
"does **some** element have a mark above 80?" — and Asha satisfies both, using
**different elements**. `$elemMatch` requires **one single element** to satisfy
every condition, which is what the question meant.

**This is the most examinable array behaviour in the unit**, and the mistake is
invisible without test data that exposes it.

### Array update operators

| Operator | Effect |
|---|---|
| `$push` | Append an element |
| `$addToSet` | Append **only if absent** |
| `$pop` | Remove the first (`-1`) or last (`1`) |
| `$pull` | Remove **every** element matching a condition |
| `$pullAll` | Remove every listed value |
| `$each` | Push several at once |
| `$slice` | Cap the array's length |
| `$sort` | Keep the array sorted |
| `$` | The **first matching** element |
| `$[]` | **All** elements |
| `$[<id>]` | Elements matching an `arrayFilters` condition |

```js
db.students.updateOne({ _id: 21 }, { $push: { subjects: "R" } })
db.students.updateOne({ _id: 21 }, { $addToSet: { subjects: "DS" } })   // no-op
db.students.updateOne({ _id: 21 },
  { $push: { subjects: { $each: ["ML", "AI"], $slice: -5, $sort: 1 } } })
db.students.updateOne({ _id: 21 }, { $pull: { subjects: "Python" } })
db.students.updateOne({ _id: 21 }, { $pop: { subjects: 1 } })           // last

// The positional operator: update the element the QUERY matched
db.c.updateOne({ _id: 1, "scores.subject": "maths" },
               { $set: { "scores.$.mark": 95 } })

// All elements
db.c.updateOne({ _id: 1 }, { $inc: { "scores.$[].mark": 5 } })

// Only elements meeting a condition
db.c.updateOne({ _id: 1 }, { $inc: { "scores.$[low].mark": 5 } },
               { arrayFilters: [ { "low.mark": { $lt: 50 } } ] })
```

**`$push` versus `$addToSet`** is a two-mark question: `$push` always appends,
`$addToSet` appends only if the value is not already present — a set, not a
list.

**`$slice: -5` after `$each`** is how you keep "the most recent five" — it caps
the array from the end, and it is the practical answer to the unbounded-array
problem of Unit 2 §2.6.

## 3.9 Update

```js
db.students.updateOne({ _id: 21 }, { $set: { age: 21 } })
db.students.updateMany({ dept: "DS" }, { $inc: { "marks.maths": 5 } })
db.students.replaceOne({ _id: 21 }, { name: "Asha", dept: "DS" })
db.students.updateOne({ _id: 99 }, { $set: { name: "New" } }, { upsert: true })
db.students.findOneAndUpdate({ _id: 21 }, { $set: { age: 22 } },
                             { returnDocument: "after" })
```

### 🔢 The update operators

| Operator | Effect |
|---|---|
| `$set` | Set a field, creating it if absent |
| `$unset` | **Remove** a field |
| `$inc` | Add (a negative value subtracts) |
| `$mul` | Multiply |
| `$rename` | Rename a field |
| `$min` / `$max` | Set only if the new value is lower / higher |
| `$currentDate` | Set to now |
| `$setOnInsert` | Apply **only** when an upsert actually inserts |

```js
db.students.updateOne({ _id: 21 }, {
  $set:   { "marks.python": 85, updated: true },
  $unset: { active: "" },                       // the value is ignored
  $inc:   { age: 1, "marks.maths": -3 },
  $rename:{ "dept": "department" },
  $currentDate: { lastModified: true }
})
```

`$unset`'s value is ignored entirely — `""` is the convention.

### ⚠️ `updateOne` versus `replaceOne`

```js
db.students.updateOne({ _id: 21 }, { $set: { name: "Asha K" } })
// every other field SURVIVES

db.students.replaceOne({ _id: 21 }, { name: "Asha K" })
// the document is now { _id: 21, name: "Asha K" } -- EVERYTHING ELSE IS GONE
```

**`replaceOne` replaces the whole document**, keeping only `_id`. Passing a
bare document to `updateOne` without an operator is an error in modern
MongoDB — which is a mercy, because in very old versions it silently replaced.

### ⚠️ `updateOne` updates **one** document, even if many match

```js
db.students.updateOne({ dept: "DS" }, { $set: { active: false } })
// exactly ONE DS student changes -- and which one is not guaranteed
db.students.updateMany({ dept: "DS" }, { $set: { active: false } })
// all three
```

Using `updateOne` where `updateMany` was meant is a silent partial update, and
it is the commonest CRUD mistake.

### Upsert

```js
db.counters.updateOne(
  { _id: "visits" },
  { $inc: { count: 1 }, $setOnInsert: { created: new Date() } },
  { upsert: true }
)
```

Update if it exists, insert if it does not — **atomically**, which is what
makes it the right way to implement a counter. `$setOnInsert` applies only on
the insert branch, so `created` is not overwritten on later increments.

## 3.10 Delete

```js
db.students.deleteOne({ _id: 21 })
db.students.deleteMany({ dept: "DS" })
db.students.deleteMany({})                       // EVERY document -- kept collection
db.students.findOneAndDelete({ _id: 21 })        // returns the deleted document
db.students.drop()                               // the collection AND its indexes
```

| Command | Removes | Keeps |
|---|---|---|
| `deleteMany({})` | All documents | The collection, its indexes, its validator |
| `drop()` | The collection entirely | Nothing |

**`deleteMany({})` with an empty filter deletes everything** — there is no
confirmation and no undo. In Course 5, `DELETE FROM t` at least sat inside a
transaction you could roll back; here it does not.

`drop()` is far faster for emptying a large collection, because it does not
process documents one at a time — but it also discards the indexes and the
validator, which then have to be recreated.

## 3.11 Bulk operations

```js
db.students.bulkWrite([
  { insertOne: { document: { _id: 30, name: "New", dept: "DS" } } },
  { updateOne: { filter: { _id: 21 }, update: { $inc: { age: 1 } } } },
  { updateMany: { filter: { dept: "DS" }, update: { $set: { active: true } } } },
  { replaceOne: { filter: { _id: 22 }, replacement: { name: "Ravi T" } } },
  { deleteOne: { filter: { _id: 25 } } }
], { ordered: false })
```

**One round trip instead of five.** For a bulk load this is the difference
between minutes and seconds, because network latency dominates when each
operation is a separate request.

As with `insertMany`, `ordered: true` (the default) stops at the first error;
`ordered: false` continues and may execute in parallel.

## 3.12 Cursor methods

```js
db.students.find().sort({ "marks.maths": -1 })       // -1 descending, 1 ascending
db.students.find().sort({ dept: 1, "marks.maths": -1 })
db.students.find().limit(3)
db.students.find().skip(2).limit(3)                  // "page 2", 3 per page
db.students.find().count()
db.students.find().toArray()
db.students.find().forEach(d => print(d.name))
db.students.find().explain("executionStats")         // Unit 5
```

**The order is fixed regardless of how you chain them**: the server always
applies **sort, then skip, then limit**. So `.limit(3).sort(...)` sorts the
whole result and then takes three — it does **not** sort three arbitrary
documents.

### ⚠️ `skip` does not scale

`skip(100000)` makes the server walk and discard 100,000 documents. Deep
pagination gets linearly slower, and page 500 of a listing is genuinely slow.

**Range-based pagination** is the fix:

```js
// Page 1
db.students.find().sort({ _id: 1 }).limit(20)
// Next page: remember the last _id seen
db.students.find({ _id: { $gt: lastSeenId } }).sort({ _id: 1 }).limit(20)
```

This uses the index to jump straight to the position, so page 500 costs the
same as page 2.

## 3.13 Projection

```js
db.students.find({}, { name: 1, dept: 1 })            // these fields + _id
db.students.find({}, { name: 1, _id: 0 })             // exclude _id
db.students.find({}, { marks: 0, subjects: 0 })       // everything EXCEPT these
db.students.find({}, { "marks.maths": 1 })            // one nested field
db.students.find({}, { subjects: { $slice: 2 } })     // first 2 array elements
db.students.find({ subjects: "DS" },
                 { "subjects.$": 1 })                 // the MATCHING element
```

### ⚠️ You cannot mix inclusion and exclusion

```js
db.students.find({}, { name: 1, dept: 0 })       // ERROR
db.students.find({}, { name: 1, _id: 0 })        // ALLOWED -- _id is the exception
```

A projection is either a list of what to **include** or a list of what to
**exclude**. **`_id` is the single exception**: it is included by default and
may be excluded alongside inclusions.

**Projection is not just cosmetic** — it reduces the bytes read from disk and
sent over the network, and a query whose projection is fully covered by an
index need not touch the documents at all (Unit 5's covered query).

---

## Practice problems

### Problem 1

Using the sample collection, write queries for:

(a) DS students older than 20
(b) students scoring above 85 in maths **or** above 85 in statistics
(c) students taking both DS and Python
(d) name and maths mark only, sorted by maths descending, top 3
(e) students whose maths mark exceeds their statistics mark
(f) increase every DS student's maths mark by 5
(g) add "R" to Asha's subjects only if it is not already there

**Solution.**

```js
// (a)
db.students.find({ dept: "DS", age: { $gt: 20 } })
// -> Ravi (21), Kiran (22)

// (b)
db.students.find({ $or: [ { "marks.maths": { $gt: 85 } },
                          { "marks.stats": { $gt: 85 } } ] })
// -> Asha (88, 91), Meena (94, 89)

// (c) BOTH, in any order -- $all, not $in
db.students.find({ subjects: { $all: ["DS", "Python"] } })
// -> Asha, Ravi

// (d)
db.students.find({}, { _id: 0, name: 1, "marks.maths": 1 })
          .sort({ "marks.maths": -1 })
          .limit(3)
// -> Meena 94, Asha 88, Kiran 71

// (e) comparing two FIELDS of the same document needs $expr
db.students.find({ $expr: { $gt: ["$marks.maths", "$marks.stats"] } })
// -> Ravi (65 > 58), Meena (94 > 89), Kiran (71 > 66), Bhanu (52 > 47)

// (f) updateMANY -- updateOne would change exactly one
db.students.updateMany({ dept: "DS" }, { $inc: { "marks.maths": 5 } })

// (g) $addToSet, not $push
db.students.updateOne({ _id: 21 }, { $addToSet: { subjects: "R" } })
```

**The four decisions that earn the marks.** In (c), `$all` means "contains all
of these" while `$in` would mean "contains **any** of these" — a different
question. In (e), only `$expr` can compare two fields; a plain query compares a
field to a constant. In (f), `updateMany` — `updateOne` would silently update
one of the three. And in (g), `$addToSet` is idempotent where `$push` would
append a duplicate "R" every time it ran.

### Problem 2

Given this collection, explain why the first query is wrong and the second is
right.

```js
db.results.insertMany([
  { name: "Asha",  scores: [ { subject: "maths", mark: 45 },
                             { subject: "stats", mark: 91 } ] },
  { name: "Ravi",  scores: [ { subject: "maths", mark: 88 },
                             { subject: "stats", mark: 40 } ] }
])

// A
db.results.find({ "scores.subject": "maths", "scores.mark": { $gt: 80 } })
// B
db.results.find({ scores: { $elemMatch: { subject: "maths",
                                          mark: { $gt: 80 } } } })
```

**Solution.**

The question is *"who scored above 80 in maths?"* The answer is **Ravi only**
(maths 88). Asha scored 45 in maths.

**Query A returns both**, which is wrong.

A asks two **independent** questions of the array:

- Does **some** element have `subject: "maths"`? — For Asha, yes: her first
  element.
- Does **some** element have `mark > 80`? — For Asha, yes: her *second*
  element, which is statistics.

Both are satisfied, so Asha matches — **using two different array elements**.
MongoDB applies each condition across the whole array independently, and
nothing ties them to the same element.

**Query B returns only Ravi**, which is right. `$elemMatch` requires **one
single element** to satisfy **every** condition simultaneously. Asha has no
element that is both maths and above 80, so she does not match.

**The rule:** whenever you place **two or more conditions on an array of
sub-documents** and they must apply to the same element, you need
`$elemMatch`. With a single condition it is unnecessary —
`{ "scores.mark": { $gt: 80 } }` alone is fine — which is why the mistake is
easy to make: the query works until you add the second condition.

### Problem 3

Explain `updateOne`, `updateMany`, `replaceOne` and `upsert`, giving a case
where each is the right choice, and say what goes wrong if you confuse them.

**Solution.**

| Method | Affects | Preserves other fields |
|---|---|---|
| `updateOne` | **One** matching document | Yes |
| `updateMany` | **All** matching documents | Yes |
| `replaceOne` | One matching document | **No — replaces it entirely** |
| `upsert: true` | Updates if found, **inserts if not** | Yes |

**`updateOne`** — when the filter identifies exactly one document, typically by
`_id`. *"Change Asha's age to 21."*

```js
db.students.updateOne({ _id: 21 }, { $set: { age: 21 } })
```

**`updateMany`** — a bulk change across a group. *"Add 5 marks to every DS
student."*

```js
db.students.updateMany({ dept: "DS" }, { $inc: { "marks.maths": 5 } })
```

**`replaceOne`** — when you have a whole new document and genuinely want the
old one gone. *"Overwrite this cached record with the freshly fetched one."*

```js
db.cache.replaceOne({ _id: key }, freshDocument)
```

**`upsert`** — when the document may not exist yet, and creating it must be
atomic. *"Increment the visit counter."*

```js
db.counters.updateOne({ _id: "visits" },
                      { $inc: { count: 1 },
                        $setOnInsert: { created: new Date() } },
                      { upsert: true })
```

Without `upsert`, the first visit would need a check-then-insert, which two
concurrent requests can both pass — and you lose a count. The upsert is a
single atomic operation, so it cannot race.

**What goes wrong when they are confused:**

**`updateOne` where `updateMany` was meant** is the commonest error. Exactly
one of the three DS students changes, **and which one is not guaranteed**. The
command succeeds, reports `modifiedCount: 1`, and the data is now silently
inconsistent — there is no error to notice.

**`replaceOne` where `updateOne` was meant** is the most destructive.

```js
db.students.replaceOne({ _id: 21 }, { name: "Asha K" })
// the document is now { _id: 21, name: "Asha K" }
// dept, marks, subjects, age, active -- ALL GONE
```

Only `_id` survives. This is why modern MongoDB **rejects** a bare document
passed to `updateOne` without an operator: it forces you to say which you
meant. Very old versions silently replaced, which destroyed a great deal of
data over the years.

---

## Exam questions from this unit

**Two marks**

1. Distinguish `insertOne` from `insertMany`.
2. What does `ordered: false` do?
3. Distinguish `find` from `findOne`.
4. Distinguish `$in` from `$all`.
5. Distinguish `$push` from `$addToSet`.
6. What does `$elemMatch` do, and when is it needed?
7. Distinguish `updateOne` from `replaceOne`.
8. What is an upsert?
9. Why can a projection not mix inclusion and exclusion?
10. Distinguish `deleteMany({})` from `drop()`.
11. Why does `skip()` not scale?
12. Which regular expressions can use an index?

**Five marks**

1. Explain the CRUD operations with examples.
2. Explain the comparison and logical query operators.
3. Explain array queries and array update operators.
4. Explain the update operators with examples.
5. Explain projection, sorting, limiting and skipping.
6. Explain bulk operations and why they are faster.
7. Explain regular expression queries and their index behaviour.

**Ten marks**

1. Given a collection, write and explain queries covering every operator
   category.
2. Explain CRUD exhaustively with examples of every method and its options.
3. Explain array handling in MongoDB — querying, `$elemMatch`, the positional
   operators and array updates.

## Mistakes that cost marks

- Using `updateOne` where `updateMany` was meant
- Using `replaceOne` and destroying every other field
- Writing two conditions on one field as two keys of the same object
- Omitting `$elemMatch` for multiple conditions on an array of sub-documents
- Confusing `$in` (any of) with `$all` (all of)
- Forgetting that `$ne`, `$nin` and `$not` also match **missing** fields
- Passing a plain value to `$not`
- Mixing inclusion and exclusion in a projection
- Forgetting dot notation for nested fields, or leaving the key unquoted
- Expecting `.limit(3).sort()` to sort only three documents
- Using `skip()` for deep pagination
- Expecting an unanchored or case-insensitive regex to use an index
