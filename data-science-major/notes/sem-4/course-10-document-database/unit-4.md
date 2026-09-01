# Unit 4 — Data Modelling and Aggregation

**Syllabus topics:** Data models — introduction to embedded vs normalized
models, advantages and trade-offs. Embedded data models: use cases, benefits
and limitations. Normalized data models: references between documents, when to
normalize data. Relationships between documents. Data model using an embedded
document. Data model using document references. Aggregation basics —
introduction to the MongoDB aggregation framework, simple pipelines and
operators.

---

## 4.1 A note on the overlap

**This unit's first half repeats Unit 2 §§2.5–2.6 almost exactly.** The
syllabus lists embedded-versus-referenced modelling in both units, and
"relationships between documents" is Unit 2's one-to-one / one-to-many /
many-to-many material under a different heading.

Rather than repeat it, §4.2 summarises the decision and adds the **design
patterns** the earlier unit did not cover. The genuinely new material in this
unit is **the aggregation framework**, from §4.4 onward — and that is where
your study time should go.

## 4.2 Embedded and normalized models — the summary

| | **Embedded** | **Normalized (referenced)** |
|---|---|---|
| Structure | Child inside the parent | Separate collections, linked by `_id` |
| Reads | **One** | Two, or a `$lookup` |
| Atomicity | **Guaranteed** — one document | Needs a transaction |
| Duplication | Likely | Avoided |
| Size risk | **16 MB ceiling** | None |
| Update cost | Rewrites the parent | Touches one place |
| Use when | One-to-one, one-to-few, read together, bounded | One-to-many, many-to-many, shared, unbounded, independently updated |

**The rule, restated:** embed when the child is **small, bounded, and always
read with the parent**; reference when it is **large, unbounded, shared, or
changes independently**.

### 🔢 Embedded models — use cases, benefits and limitations

The syllabus asks for these three separately, so answer them separately.

**Use cases**

| Case | Example |
|---|---|
| One-to-one | A student and their address |
| One-to-few, **bounded** | A student's phone numbers; a book's authors |
| Read together, always | An order and its line items |
| Written together, atomically | A survey and its answers |
| The child has no independent life | A comment that exists only on its post |

**Benefits**

- **One read returns everything.** No join, no second round trip, no
  `$lookup`. This is the whole reason the model exists.
- **Atomic writes for free.** A single-document update is atomic in MongoDB
  with no transaction, so parent and child can never be half-updated.
- **Data locality.** Parent and child are contiguous on disk, so one seek
  fetches both.
- **Fewer collections and fewer indexes** to design and maintain.

**Limitations**

- **The 16 MB ceiling.** An unbounded array eventually breaks the document,
  and it breaks it in production, not in testing.
- **Rewrites the parent.** Growing an embedded array can force the whole
  document to be relocated on disk.
- **Duplication.** Embedding a course's title in 300 students means 300
  updates when the title changes.
- **Awkward to query alone.** Counting comments across all posts needs
  `$unwind` over every post; as a separate collection it is one
  `countDocuments`.
- **No sub-document uniqueness.** Nothing stops the same course appearing
  twice in one student's array; a referenced model gets a unique index.

### 🔢 Normalized models — when to normalize

Reference — do **not** embed — when **any one** of these is true:

| Signal | Why | Example |
|---|---|---|
| The child set is **unbounded** | It will pass 16 MB | Sensor → readings |
| The child is **shared** | Embedding duplicates it | Many students → one course |
| The child changes **independently** | You would rewrite the parent to touch the child | A product's price, on 10,000 orders |
| The child is **large** | It bloats every read of the parent | A document body, a scanned image |
| You query the child **on its own** | Embedded, it needs `$unwind` first | "All grade-A enrolments this year" |
| The relationship has its **own attributes** | They belong to neither side | Enrolment date, grade → a junction collection |

**And the counter-rule, which earns the other half of the mark:** normalizing
in MongoDB is **not** free the way it is in SQL. There is no foreign key, no
`ON DELETE CASCADE`, and no query planner that will join for you cheaply.
Every reference you add is a `$lookup` on the read path and an integrity rule
the *application* must enforce. So normalize for the reasons above, not out of
relational habit — and if you find yourself normalizing everything, the data
may genuinely be relational, and Course 5's database may be the right tool.

### Relationships, in one table

| Relationship | Model | Example |
|---|---|---|
| **One-to-one** | Embed | Student → address |
| **One-to-few** | Embed as an array | Student → phone numbers |
| **One-to-many** | Reference from the **child** | Course → enrolments |
| **One-to-squillions** | Reference from the child, **never** an array on the parent | Sensor → readings |
| **Many-to-many** | Array of ids, or a junction collection | Students ↔ courses |

**When the relationship itself has attributes — a grade, an enrolment date — use
a junction collection.** That is Course 5's junction table, and the reasoning
survives the translation unchanged.

## 4.3 Document model design patterns

The named patterns are what this unit adds beyond Unit 2, and each is the
answer to a specific problem.

### 🔢 The patterns worth knowing

| Pattern | Problem it solves |
|---|---|
| **Subset** | An unbounded array; embed the few you display, reference the rest |
| **Extended reference** | A `$lookup` on every read; copy the two or three fields you actually show |
| **Computed** | Recomputing an aggregate on every read; store the total and update it on write |
| **Bucket** | Millions of tiny documents; group them by time or range |
| **Attribute** | Many rarely-queried, varying fields; store them as an array of key/value pairs |
| **Polymorphic** | Similar entities with different shapes in one collection |
| **Schema versioning** | Migrating a live schema; keep a version field and handle both |
| **Outlier** | A few documents that break the pattern; flag and handle them separately |

**Subset** — the fix for the unbounded array of Unit 2 §2.6:

```js
{ _id: 1, title: "Post", commentCount: 50000,
  recentComments: [ /* newest 5, for the preview */ ] }
```

**Extended reference** — copy only the fields the parent's view needs:

```js
{ _id: ObjectId(), student_id: 21, course_id: "DSC301", grade: "A",
  student_name: "Asha Kumari",       // duplicated ON PURPOSE
  course_title: "Data Science with R" }
```

The cost is stated plainly: **renaming a student must update the enrolments
too.** Copy only fields that rarely change — a name, a title — never a price or
a status.

**Computed** — pay once on write instead of every read:

```js
{ _id: "DSC301", title: "Data Science with R",
  enrolledCount: 42, averageGrade: 7.8, lastComputed: ISODate() }
```

**Bucket** — the answer to millions of tiny time-series documents. Instead of
one document per reading:

```js
{ sensor: "A", hour: ISODate("2026-08-26T09:00Z"),
  count: 60, sum: 1342.5,
  readings: [ { t: 0, v: 22.1 }, { t: 1, v: 22.3 }, /* ... */ ] }
```

One document per **hour** rather than per reading: 60× fewer documents, 60×
fewer index entries, and the sums are precomputed. This is exactly Course 8's
Clustering Feature idea — keep `count` and `sum`, not the raw points.

**Attribute** — for a product catalogue where every category has different
fields:

```js
// instead of colour, size, isbn, voltage... as separate fields
{ _id: 1, name: "T-Shirt",
  specs: [ { k: "size", v: "L" }, { k: "colour", v: "navy" } ] }
```

One compound index on `specs.k, specs.v` then serves **every** attribute, where
separate fields would need an index each.

## 4.4 The aggregation framework

### 🎯 The big idea

**A pipeline of stages, each transforming the stream of documents and passing
it to the next.** It is Unix pipes for documents, and it is MongoDB's answer to
SQL's `GROUP BY`, `HAVING`, `JOIN` and window functions all at once.

```
collection ──► $match ──► $group ──► $sort ──► $project ──► result
              (filter)  (aggregate) (order)   (reshape)
```

```js
db.students.aggregate([
  { $match:   { active: true } },
  { $group:   { _id: "$dept", avgMaths: { $avg: "$marks.maths" },
                n: { $sum: 1 } } },
  { $sort:    { avgMaths: -1 } },
  { $project: { _id: 0, dept: "$_id", avgMaths: { $round: ["$avgMaths", 2] },
                n: 1 } }
])
```

### 🔢 The stages

| Stage | Does | SQL analogue |
|---|---|---|
| **`$match`** | Filter documents | `WHERE` |
| **`$group`** | Group and aggregate | `GROUP BY` |
| **`$project`** | Reshape — include, exclude, compute | `SELECT` |
| **`$sort`** | Order | `ORDER BY` |
| **`$limit`** / **`$skip`** | Take / discard | `LIMIT` / `OFFSET` |
| **`$unwind`** | **One output document per array element** | — |
| **`$lookup`** | Join another collection | `LEFT OUTER JOIN` |
| `$addFields` / `$set` | Add a field, keeping the rest | — |
| `$unset` | Remove fields | — |
| `$count` | Count the documents | `COUNT(*)` |
| `$bucket` / `$bucketAuto` | Group into ranges | `CASE` + `GROUP BY` |
| `$facet` | Several pipelines over the same input | — |
| `$out` / `$merge` | Write the result to a collection | `CREATE TABLE AS` |
| `$sample` | A random sample | `TABLESAMPLE` |
| `$sortByCount` | `$group` + `$sort` in one | — |

### ⚠️ Put `$match` first — it is the single biggest optimisation

```js
// SLOW: groups every document, then throws most of the result away
db.students.aggregate([
  { $group: { _id: "$dept", avg: { $avg: "$marks.maths" } } },
  { $match: { _id: "DS" } }
])

// FAST: filters first, so $group sees 3 documents instead of 5,000,000
db.students.aggregate([
  { $match: { dept: "DS" } },
  { $group: { _id: "$dept", avg: { $avg: "$marks.maths" } } }
])
```

**Only an early `$match` can use an index.** Once `$group` has run, the
documents are computed values with no index behind them, so a later `$match` is
a linear scan of the group results. The same applies to `$sort`: before
`$group` it can use an index, after it cannot.

MongoDB's optimiser moves some `$match` stages earlier automatically, but it
cannot always prove the move is safe — so write it first yourself.

### 🔢 Accumulator operators, for `$group`

| Accumulator | Computes |
|---|---|
| `$sum` | Total. **`{ $sum: 1 }` counts** |
| `$avg` | Mean |
| `$min` / `$max` | Extremes |
| `$first` / `$last` | First/last in the group — **depends on the sort order** |
| `$push` | An array of **every** value |
| `$addToSet` | An array of **distinct** values |
| `$count` | Count (MongoDB 5.0+) |
| `$stdDevPop` / `$stdDevSamp` | Standard deviation — **population and sample**, the Course 4 distinction again |

```js
db.students.aggregate([
  { $group: {
      _id: "$dept",
      n:        { $sum: 1 },                 // COUNT(*)
      totalM:   { $sum: "$marks.maths" },
      avgM:     { $avg: "$marks.maths" },
      best:     { $max: "$marks.maths" },
      names:    { $push: "$name" },
      subjects: { $addToSet: "$dept" },
      sd:       { $stdDevSamp: "$marks.maths" }
  } }
])
```

### ⚠️ `_id` in `$group` is the grouping key, and it is compulsory

```js
{ $group: { _id: "$dept", ... } }                    // group BY dept
{ $group: { _id: null, ... } }                       // ONE group: the grand total
{ $group: { _id: { d: "$dept", y: "$year" }, ... } } // COMPOSITE key
```

**`_id: null` groups everything into one**, which is how you get an overall
total — the equivalent of `SELECT AVG(x) FROM t` with no `GROUP BY`. Omitting
`_id` entirely is an error.

And note the `$` prefix: **`"$dept"` means "the value of the field `dept`"**,
while `"dept"` is the literal string. Forgetting the `$` is the commonest
aggregation typo, and it silently groups every document under the string
`"dept"`.

### `$project` and expression operators

```js
{ $project: {
    _id: 0,
    name: 1,
    dept: 1,
    total:   { $add: ["$marks.maths", "$marks.stats"] },
    average: { $divide: [ { $add: ["$marks.maths", "$marks.stats"] }, 2 ] },
    rounded: { $round: ["$marks.maths", 1] },
    upper:   { $toUpper: "$name" },
    initial: { $substr: ["$name", 0, 1] },
    grade:   { $cond: { if: { $gte: ["$marks.maths", 75] },
                        then: "Distinction", else: "Pass" } },
    band:    { $switch: {
                 branches: [
                   { case: { $gte: ["$marks.maths", 75] }, then: "Distinction" },
                   { case: { $gte: ["$marks.maths", 60] }, then: "First" },
                   { case: { $gte: ["$marks.maths", 40] }, then: "Pass" }
                 ],
                 default: "Fail" } },
    nSubjects: { $size: "$subjects" },
    year:      { $year: "$dob" }
} }
```

| Category | Operators |
|---|---|
| Arithmetic | `$add`, `$subtract`, `$multiply`, `$divide`, `$mod`, `$round`, `$abs`, `$pow`, `$sqrt` |
| String | `$concat`, `$substr`, `$toUpper`, `$toLower`, `$split`, `$strLenCP`, `$trim`, `$regexMatch` |
| Array | `$size`, `$slice`, `$arrayElemAt`, `$filter`, `$map`, `$reduce`, `$in`, `$concatArrays` |
| Comparison | `$eq`, `$gt`, `$lt`, `$cmp` |
| Conditional | `$cond`, `$switch`, `$ifNull` |
| Date | `$year`, `$month`, `$dayOfMonth`, `$dateToString`, `$dateDiff` |
| Type | `$toInt`, `$toString`, `$toDate`, `$convert`, `$type` |

**`$addFields` versus `$project`** is a two-mark distinction: `$project`
outputs **only** what you list (plus `_id`), while `$addFields` **keeps
everything** and adds to it. Use `$addFields` when you want one more field and
`$project` when you want to control the whole shape.

## 4.5 `$unwind`

### 🎯 What it does

**Turns one document with an N-element array into N documents**, each holding
one element. It is how you aggregate *across* array contents.

```js
{ _id: 21, name: "Asha", subjects: ["DS", "Stats", "Python"] }
```

```js
db.students.aggregate([ { $unwind: "$subjects" } ])
```

```js
{ _id: 21, name: "Asha", subjects: "DS" }
{ _id: 21, name: "Asha", subjects: "Stats" }
{ _id: 21, name: "Asha", subjects: "Python" }
```

Note `subjects` is now a **scalar**, not an array, and `_id` **repeats**.

**The classic use — count how many students take each subject:**

```js
db.students.aggregate([
  { $unwind: "$subjects" },
  { $group: { _id: "$subjects", students: { $sum: 1 } } },
  { $sort:  { students: -1 } }
])
```

Without `$unwind` this is impossible: `$group` on `"$subjects"` would group by
the **whole array**, so `["DS","Stats"]` and `["DS"]` would be different groups.

### ⚠️ `$unwind` silently drops empty and missing arrays

```js
{ $unwind: "$subjects" }
// a document with subjects: [] or no subjects field VANISHES

{ $unwind: { path: "$subjects", preserveNullAndEmptyArrays: true } }
// it survives, with subjects absent
```

**A student taking no subjects disappears from the result entirely**, and the
count is quietly wrong. This is the single most common `$unwind` bug.

`includeArrayIndex: "i"` adds the element's original position, which is useful
after an unwind that you intend to re-`$group`.

## 4.6 `$lookup`

### 🎯 The join

```js
db.enrollments.aggregate([
  { $lookup: {
      from: "students",           // the OTHER collection
      localField: "student_id",   // field in THIS pipeline
      foreignField: "_id",        // field in the other collection
      as: "student"               // the output ARRAY field
  } },
  { $unwind: "$student" }         // usually needed: turn the 1-element array
])                                //   into a sub-document
```

**`as` always produces an array**, even for a one-to-one match — which is why
`$unwind` almost always follows. That pairing is worth memorising.

`$lookup` is a **left outer join**: unmatched documents get an **empty array**,
not nothing.

### The pipeline form

For anything more than an equality match:

```js
{ $lookup: {
    from: "enrollments",
    let: { sid: "$_id" },
    pipeline: [
      { $match: { $expr: { $and: [ { $eq: ["$student_id", "$$sid"] },
                                   { $gte: ["$grade_points", 8] } ] } } },
      { $project: { course_id: 1, grade: 1 } }
    ],
    as: "goodGrades"
} }
```

Note the `$$` prefix: **`$field` is a field of the current document; `$$var` is
a variable declared in `let`.** Getting these the wrong way round is the usual
error in a pipeline lookup.

### ⚠️ `$lookup` is not a cheap join

It executes roughly as a loop, running a lookup **per input document**. So:

- **Index the `foreignField`**, always — without it, every input document
  causes a full collection scan of the other collection.
- **`$match` before the `$lookup`**, never after, so it runs on 10 documents
  rather than 10,000.
- **Sharded collections have restrictions**, and multi-way joins get slow fast.

**If you find yourself writing three `$lookup` stages, the data model is
probably wrong.** That is a relational query, and either the model should embed
what is being joined, or the data belongs in a relational database. Saying that
in an exam earns marks: the right answer is not always "write a bigger
pipeline".

## 4.7 `$bucket` and `$facet`

```js
// Fixed boundaries -- a grade distribution
db.students.aggregate([
  { $bucket: {
      groupBy: "$marks.maths",
      boundaries: [0, 40, 60, 75, 101],
      default: "Other",
      output: { count: { $sum: 1 }, students: { $push: "$name" } }
  } }
])
```

**`boundaries` must be sorted ascending, and each bucket is
`[lower, upper)`** — lower inclusive, upper **exclusive**. That is why the last
boundary above is 101 and not 100: with 100 the top boundary, a student scoring
exactly 100 would fall into `default`. Getting this wrong loses exactly the
top student, which is easy to miss.

`$bucketAuto` chooses the boundaries itself to produce roughly equal-sized
buckets — the `qcut` to `$bucket`'s `cut`, in Course 9's terms.

```js
// Several pipelines over the SAME input, in one pass
db.students.aggregate([
  { $facet: {
      byDept:  [ { $group: { _id: "$dept", n: { $sum: 1 } } } ],
      topFive: [ { $sort: { "marks.maths": -1 } }, { $limit: 5 } ],
      overall: [ { $group: { _id: null, avg: { $avg: "$marks.maths" } } } ]
  } }
])
```

**`$facet` is how a dashboard gets all its numbers in one round trip.** Each
sub-pipeline sees the same input; the output is one document with a field per
facet.

## 4.8 Aggregation and SQL, side by side

| SQL | Aggregation pipeline |
|---|---|
| `SELECT` | `$project` |
| `FROM` | The collection |
| `WHERE` | **`$match`** (before `$group`) |
| `GROUP BY` | **`$group`** with `_id` |
| `HAVING` | **`$match`** (after `$group`) |
| `ORDER BY` | `$sort` |
| `LIMIT` / `OFFSET` | `$limit` / `$skip` |
| `JOIN` | `$lookup` |
| `COUNT(*)` | `{ $sum: 1 }` |
| `SUM(x)` | `{ $sum: "$x" }` |
| `CASE WHEN` | `$cond` / `$switch` |
| `UNION ALL` | `$unionWith` |
| (no equivalent) | **`$unwind`** |

**`WHERE` and `HAVING` are the same stage in different positions**, which is a
neat way to remember why stage order matters. And **`$unwind` has no SQL
equivalent**, because SQL has no arrays inside a column.

```sql
SELECT dept, AVG(maths) AS avg_maths, COUNT(*) AS n
FROM   students
WHERE  active = true
GROUP  BY dept
HAVING COUNT(*) > 1
ORDER  BY avg_maths DESC;
```

```js
db.students.aggregate([
  { $match: { active: true } },
  { $group: { _id: "$dept", avg_maths: { $avg: "$marks.maths" },
              n: { $sum: 1 } } },
  { $match: { n: { $gt: 1 } } },              // HAVING
  { $sort:  { avg_maths: -1 } }
])
```

---

## Practice problems

### Problem 1

Using the `students` collection from Unit 3, write pipelines for:

(a) the average maths mark per department
(b) departments whose average exceeds 70, sorted descending
(c) how many students take each subject
(d) each student with their total, and a grade band
(e) a grade distribution in the bands 0–39, 40–59, 60–74, 75–100

**Solution.**

```js
// (a)
db.students.aggregate([
  { $group: { _id: "$dept", avgMaths: { $avg: "$marks.maths" },
              n: { $sum: 1 } } }
])
// DS: (88+65+71)/3 = 74.667 over 3 students
// Stats: (94+52)/2 = 73 over 2

// (b) -- the HAVING clause is a SECOND $match, after $group
db.students.aggregate([
  { $group: { _id: "$dept", avgMaths: { $avg: "$marks.maths" } } },
  { $match: { avgMaths: { $gt: 70 } } },
  { $sort:  { avgMaths: -1 } },
  { $project: { _id: 0, dept: "$_id",
                avgMaths: { $round: ["$avgMaths", 2] } } }
])
// -> DS 74.67, Stats 73

// (c) -- IMPOSSIBLE without $unwind
db.students.aggregate([
  { $unwind: "$subjects" },
  { $group:  { _id: "$subjects", students: { $sum: 1 } } },
  { $sort:   { students: -1, _id: 1 } }
])
// DS 3 (Asha, Ravi, Kiran), Stats 3 (Asha, Meena, Bhanu),
// Python 2 (Asha, Ravi), R 1 (Meena)

// (d)
db.students.aggregate([
  { $project: {
      _id: 0, name: 1,
      total: { $add: ["$marks.maths", "$marks.stats"] },
      band: { $switch: {
        branches: [
          { case: { $gte: ["$marks.maths", 75] }, then: "Distinction" },
          { case: { $gte: ["$marks.maths", 60] }, then: "First" },
          { case: { $gte: ["$marks.maths", 40] }, then: "Pass" }
        ], default: "Fail" } }
  } },
  { $sort: { total: -1 } }
])

// (e) -- note the upper boundary of 101
db.students.aggregate([
  { $bucket: {
      groupBy: "$marks.maths",
      boundaries: [0, 40, 60, 75, 101],
      default: "Other",
      output: { count: { $sum: 1 }, names: { $push: "$name" } }
  } }
])
// 0-39: 0 | 40-59: 1 (Bhanu 52) | 60-74: 2 (Ravi 65, Kiran 71)
// 75-100: 2 (Asha 88, Meena 94)
```

**Three points earn the marks.** In (b), `HAVING` is simply a `$match` placed
**after** `$group` — the same stage in a different position, which is the neat
way to remember why order matters. In (c), `$unwind` is not optional: grouping
on `"$subjects"` directly would group by the **whole array**, making
`["DS","Stats"]` and `["DS"]` separate groups. And in (e), the last boundary is
**101, not 100**, because buckets are `[lower, upper)` — with 100 as the
boundary, a student scoring exactly 100 would fall into `default` and be lost.

### Problem 2

Given `students`, `courses` and `enrollments`, write a pipeline listing every
student with the courses they take and their grades. Explain why `$unwind`
follows `$lookup`, and what could make this slow.

**Solution.**

```js
db.enrollments.aggregate([
  { $lookup: { from: "students", localField: "student_id",
               foreignField: "_id", as: "student" } },
  { $unwind: "$student" },
  { $lookup: { from: "courses", localField: "course_id",
               foreignField: "_id", as: "course" } },
  { $unwind: "$course" },
  { $project: {
      _id: 0,
      student: "$student.name",
      dept:    "$student.dept",
      course:  "$course.title",
      credits: "$course.credits",
      grade: 1
  } },
  { $sort: { student: 1, course: 1 } }
])
```

**Why `$unwind` follows `$lookup`.** `$lookup` always writes its result into an
**array** — even when exactly one document matches, because in general several
could. So after the first stage each document holds
`student: [ { _id: 21, name: "Asha", ... } ]`, and referring to
`"$student.name"` would give an **array of names**, not a name. `$unwind`
turns the single-element array into a plain sub-document, after which
`"$student.name"` is a string. That `$lookup` + `$unwind` pairing is close to
universal for a one-to-one reference.

**What could make it slow, in order of severity:**

1. **No index on the `foreignField`.** `$lookup` runs a lookup per input
   document; without an index on `students._id` and `courses._id` each one is
   a full collection scan. (`_id` is indexed automatically, so in this case it
   is fine — but the same pipeline joining on `students.roll_no` would need
   that index created explicitly.)

2. **No `$match` before the lookups.** As written, every enrolment is joined.
   If the report only covers one department or one semester, filtering first
   turns 100,000 lookups into 200:

   ```js
   { $match: { semester: 4 } },      // FIRST
   { $lookup: { ... } }
   ```

3. **Two `$lookup` stages is already a warning sign.** This is a three-table
   relational join expressed in a document database. If this report is run
   constantly, the **extended reference pattern** — storing `student_name` and
   `course_title` on the enrolment — removes both lookups entirely, at the cost
   of updating those copies when a name changes. If it is run nightly for a
   report, the pipeline is fine.

**The honest closing point:** if the application's main queries look like this,
the data is relational and a relational database would serve it better. Course
5's design was not wrong; it was designed for a different access pattern.

### Problem 3

Explain the aggregation pipeline, why `$match` should come first, and translate
this SQL:

```sql
SELECT   dept, COUNT(*) AS n, AVG(maths) AS avg_maths
FROM     students
WHERE    active = true
GROUP BY dept
HAVING   COUNT(*) > 1
ORDER BY avg_maths DESC
LIMIT    5;
```

**Solution.**

The aggregation framework processes documents through a **sequence of stages**,
each consuming the previous stage's output — Unix pipes for documents. It is
MongoDB's equivalent of `GROUP BY`, `HAVING`, `JOIN` and more.

**The translation:**

```js
db.students.aggregate([
  { $match: { active: true } },                        // WHERE
  { $group: { _id: "$dept",                            // GROUP BY
              n: { $sum: 1 },                          // COUNT(*)
              avg_maths: { $avg: "$marks.maths" } } },  // AVG(maths)
  { $match: { n: { $gt: 1 } } },                       // HAVING
  { $sort:  { avg_maths: -1 } },                       // ORDER BY ... DESC
  { $limit: 5 },                                       // LIMIT
  { $project: { _id: 0, dept: "$_id", n: 1,
                avg_maths: { $round: ["$avg_maths", 2] } } }
])
```

**Note that `WHERE` and `HAVING` are the same stage** — `$match` — in different
**positions**. Before `$group` it filters documents; after `$group` it filters
groups. That single observation explains most of what is confusing about
pipeline order.

**Why `$match` must come first.** Two reasons, and the second is the important
one:

1. **Volume.** Every later stage processes fewer documents. Filtering 5,000,000
   down to 3 before grouping is the difference between seconds and milliseconds.

2. **Indexes.** **Only a `$match` at the start of the pipeline can use an
   index.** Once `$group` has run, its output consists of computed values that
   exist only in memory — there is no index behind them, so a later `$match`
   must scan every group linearly. The same is true of `$sort`: before `$group`
   it can use an index; after it, it must sort in memory, and it will fail
   outright past 100 MB unless `allowDiskUse: true` is set.

MongoDB's optimiser does move some `$match` stages earlier automatically, but
it can only do so when it can **prove** the move does not change the result —
which it often cannot. Writing it first yourself is both clearer and reliable.

---

## Exam questions from this unit

**Two marks**

1. Distinguish embedded from normalized data models.
2. When should data be normalized in MongoDB?
3. What is the subset pattern?
4. What is the extended reference pattern, and what does it cost?
5. What is an aggregation pipeline?
6. What does `$unwind` do?
7. Why must `$unwind` usually follow `$lookup`?
8. Distinguish `$project` from `$addFields`.
9. What does `_id: null` mean in `$group`?
10. Why must `$match` come first?
11. Why does `$unwind` drop documents, and how do you stop it?

**Five marks**

1. Explain embedded and normalized models with use cases and trade-offs.
2. Explain how to model one-to-one, one-to-many and many-to-many relationships.
3. Explain the document design patterns.
4. Explain the aggregation pipeline stages with examples.
5. Explain the `$group` accumulators with examples.
6. Explain `$lookup`, including its cost and how to make it fast.
7. Compare the aggregation pipeline with SQL.

**Ten marks**

1. Design a complete data model for a given application and justify every
   decision.
2. Write and explain a full aggregation pipeline answering a business question.
3. Explain the aggregation framework exhaustively, with the SQL mapping.

## Mistakes that cost marks

- Forgetting the `$` before a field name in an aggregation expression
- Omitting `_id` from `$group`
- Placing `$match` after `$group` when it could have come first
- Forgetting `$unwind` before grouping on array contents
- Forgetting that `$unwind` drops empty and missing arrays
- Forgetting `$unwind` after `$lookup`, and getting an array where you wanted a value
- Confusing `$$variable` with `$field` in a pipeline `$lookup`
- Setting `$bucket`'s top boundary to the maximum value and losing it
- Not indexing the `foreignField` of a `$lookup`
- Writing three `$lookup` stages instead of reconsidering the model
- Using `$project` where `$addFields` was meant, and dropping every other field
