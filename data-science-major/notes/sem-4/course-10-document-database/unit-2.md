# Unit 2 — MongoDB Architecture, Data Modeling and Basics

**Syllabus topics:** MongoDB architecture — database, collection, document
concepts; BSON format; advantages of MongoDB over RDBMS; MongoDB datatypes
(String, Number, Date, Boolean, Array, ObjectId, Embedded Documents, Null).
Data modeling in MongoDB — schema design strategies, embedded vs referenced
documents. Database and collection management — create and drop database,
create and drop collection.

---

## 2.1 The hierarchy

```
mongod (the server process)
└── Database          collegeDB
    └── Collection    students          ← like a TABLE, but schema-free
        └── Document  { _id: 21, ... }  ← like a ROW, but nested
            └── Field  name: "Asha"     ← like a COLUMN, but per-document
```

| Level | Relational analogue | Difference |
|---|---|---|
| **Database** | Database | Essentially the same |
| **Collection** | Table | **No fixed schema**; documents may differ |
| **Document** | Row | **Nested** — may contain objects and arrays |
| **Field** | Column | Exists **per document**, not per collection |

### Limits worth knowing

| Limit | Value |
|---|---|
| **Maximum document size** | **16 MB** |
| Maximum nesting depth | 100 levels |
| Index key length | 1024 bytes |
| Indexes per collection | 64 |
| Database name length | 64 characters |

**The 16 MB limit is examinable and it drives design.** An "embed everything"
model fails the day one document grows past it — a blog post with unbounded
comments, a student with unbounded attendance records. §2.6 is largely about
recognising that case in advance. For genuinely large content there is
**GridFS**, which splits a file into 255 KB chunks across two collections.

### 🔢 The BSON format

The syllabus names **BSON format** as a topic in its own right here, and it
belongs in the architecture section rather than the type table: BSON is *how a
document is stored and sent*, not merely what its fields are called.

**BSON is Binary JSON.** Every document you write as JSON in the shell is
stored on disk and sent over the wire as BSON. Unit 1 §1.8 set out why it
exists; here is what it means for the architecture:

| Property | Consequence for the server |
|---|---|
| **Length-prefixed** | Each document and each sub-document records its own byte length, so the server can **skip a field it does not need** instead of parsing to the end. JSON must be read character by character |
| **Typed** | The type is one byte in the encoding, so `42`, `42.0` and `NumberLong(42)` are genuinely different on disk — see the traps in §2.3 |
| **Ordered** | Field order is preserved and is part of the document, which is why `{a:1, b:2}` and `{b:2, a:1}` are **not** equal as whole-document match filters |
| **Traversable** | The length prefixes make dot notation into a nested field an offset jump, not a re-parse |
| **Not human-readable** | Which is why the shell renders it back as JSON, and why `mongodump` output cannot be read in a text editor |

```
JSON on your screen        { "_id": 21, "name": "Asha" }
BSON on disk               \x1d\x00\x00\x00        <- 29 bytes, total length
                           \x10 _id \x00 \x15...    <- \x10 = int32
                           \x02 name \x00 ...       <- \x02 = string
                           \x00                     <- end of document
```

**The 16 MB limit is a BSON limit**, not a MongoDB whim: the total length is
stored as a signed 32-bit integer, and 16 MB is the size the designers capped
it at so a single document stays cheap to hold in memory and move over the
network.

## 2.2 Advantages of MongoDB over RDBMS

| Advantage | What it means in practice |
|---|---|
| **Flexible schema** | Add a field to one document without a migration |
| **No joins for the common read** | A whole order, with its lines, in one read |
| **Horizontal scaling** | Built-in sharding across commodity machines |
| **Natural mapping to objects** | A document is your program's object; no ORM impedance mismatch |
| **Nested structures are native** | Arrays and sub-documents are first-class and indexable |
| **Fast writes** | No multi-table coordination for one entity |
| **High availability** | Replica sets with automatic failover |
| **Rich queries** | Unlike key–value stores, you can query **any** field |

### ⚠️ State the disadvantages too

A ten-mark answer that lists only advantages is an incomplete answer.

| Disadvantage | Consequence |
|---|---|
| **No enforced referential integrity** | The application must maintain it |
| **Duplication** | Denormalised data must be updated in several places |
| **Joins are expensive** | `$lookup` exists but is slow; multi-way joins are painful |
| **16 MB document ceiling** | Unbounded arrays are a design bug |
| **Memory-hungry** | The working set wants to fit in RAM |
| **Weaker ad-hoc reporting** | BI tools speak SQL |
| **Schema drift** | Without validation, the same field appears three ways |

## 2.3 MongoDB data types

| Type | Example | Notes |
|---|---|---|
| **String** | `"Asha"` | UTF-8 |
| **Double** | `3.14` | The default for a decimal |
| **Int32 / Int64** | `NumberInt(5)`, `NumberLong(5)` | The shell defaults to Double, so ask explicitly |
| **Decimal128** | `NumberDecimal("19.99")` | **Exact decimal — use it for money** |
| **Boolean** | `true` | |
| **Date** | `ISODate("2026-08-26")`, `new Date()` | Milliseconds since the epoch, UTC |
| **Timestamp** | `Timestamp()` | **Internal, for replication — not for your data** |
| **ObjectId** | `ObjectId("...")` | 12 bytes; the default `_id` |
| **Array** | `["DS", "Stats"]` | May mix types; indexable |
| **Object** | `{ maths: 88 }` | An embedded document |
| **Null** | `null` | The field exists and is empty |
| **Undefined** | — | Deprecated; do not use |
| **Regex** | `/^A/` | |
| **BinData** | | Binary blobs |
| **MinKey / MaxKey** | | Sort below/above everything |

### ⚠️ Three type traps

**1. The shell stores whole numbers as Double.**

```js
db.c.insertOne({ n: 5 })                  // stored as a DOUBLE
db.c.insertOne({ n: NumberInt(5) })       // an int32
db.c.insertOne({ n: NumberLong(5) })      // an int64
```

Harmless until you need exact integer arithmetic or compact storage.

**2. Never store money as a Double.**

```js
{ price: 19.99 }                     // a double -- cannot represent 19.99 exactly
{ price: NumberDecimal("19.99") }    // exact
{ priceInPaise: NumberInt(1999) }    // or work in the smallest unit
```

This is Course 2's and Course 9's floating-point lesson again: binary floating
point cannot represent most decimal fractions exactly, so sums of prices drift.

**3. `null`, missing and `undefined` are three different things.**

```js
{ _id: 1, phone: "9876543210" }     // present, with a value
{ _id: 2, phone: null }             // present, explicitly empty
{ _id: 3 }                          // ABSENT

db.c.find({ phone: null })          // matches BOTH _id 2 AND _id 3
db.c.find({ phone: { $exists: false } })   // matches ONLY _id 3
db.c.find({ phone: { $type: "null" } })    // matches ONLY _id 2
```

**`{ field: null }` matches missing fields as well as null ones**, which is
almost never what a beginner intends. This is a guaranteed exam question and a
real source of wrong query results.

### Dates

```js
db.students.insertOne({ name: "Asha", dob: ISODate("2005-04-03") })
db.students.find({ dob: { $lt: ISODate("2006-01-01") } })      // works
db.students.insertOne({ name: "Ravi", dob: "2005-04-03" })     // a STRING
```

**A date stored as a string cannot be compared or sorted reliably** — string
ordering only coincides with date ordering in ISO `YYYY-MM-DD` form, and breaks
for any other format. Store dates as dates. MongoDB stores them as **UTC**;
timezone handling is the application's job.

## 2.4 Database and collection management

```js
// --- databases -------------------------------------------------------------
use collegeDB               // switch to it; CREATES NOTHING yet
db                          // the current database
show dbs                    // list -- an EMPTY database will not appear
db.dropDatabase()           // drop the CURRENT database

// --- collections -----------------------------------------------------------
db.createCollection("students")
db.createCollection("logs", { capped: true, size: 100000, max: 1000 })
db.createCollection("students", {                 // with schema validation
  validator: { $jsonSchema: { /* see 2.7 */ } }
})

show collections
db.getCollectionNames()
db.students.drop()                                // drop ONE collection
db.students.renameCollection("learners")
db.students.countDocuments()                      // an ACCURATE count
db.students.estimatedDocumentCount()              // fast, from metadata
db.students.stats()
```

### ⚠️ Lazy creation, again

```js
use brandNewDB
show dbs                     // brandNewDB is ABSENT
db.things.insertOne({ x: 1 })
show dbs                     // now it exists
```

**A database or collection springs into existence on the first write.** So does
a collection: `db.anything.insertOne({})` creates `anything`. `createCollection`
is only needed when you want *options* — validation, capping, a custom
collation.

### ⚠️ `count()` versus `countDocuments()`

`db.c.count()` is **deprecated** and could be inaccurate on a sharded cluster
or after an unclean shutdown, because it read cached metadata.
**`countDocuments()`** actually counts and is correct;
**`estimatedDocumentCount()`** is the fast, approximate one, and its name says
so honestly.

### Capped collections

A fixed-size collection that **overwrites its oldest documents** when full,
preserving insertion order. Useful for logs and caches. You cannot delete from
one, and you cannot grow a document beyond its original size.

## 2.5 Schema design strategies

### 🎯 The central shift

**In Course 5 you designed for the data. Here you design for the queries.**

Relational modelling asks "what *is* the data, and how do I remove redundancy?"
— and the answer is the same whatever you later query. Document modelling asks
**"what will I read, and how often?"** — and the answer changes the model.

**The design rule: data that is accessed together should be stored together.**

### The steps

1. **List the queries** the application will run, and how often.
2. Identify the **entities** and their relationships.
3. For each relationship, decide **embed or reference** (§2.6).
4. Consider **read/write ratio** — reads favour embedding, frequent independent
   writes favour referencing.
5. Watch the **16 MB limit** and unbounded growth.
6. Add **indexes** for the query patterns (Unit 5).
7. Add **validation** where consistency matters (§2.7).

**Step 1 is the one people skip, and it is the one that determines the answer.**
You cannot design a MongoDB schema without knowing the queries; there is no
"neutral" normalised form to fall back on.

## 2.6 Embedded versus referenced

### 🔢 The two models

**Embedded** — related data inside the parent document:

```js
{
  _id: 21,
  name: "Asha Kumari",
  address: { city: "Vijayawada", state: "AP", pin: "520010" },
  enrollments: [
    { course: "Data Science", grade: "A", credits: 4 },
    { course: "Statistics",   grade: "B", credits: 3 }
  ]
}
```

One read gets everything. **No join, ever.**

**Referenced** — related data in another collection, linked by `_id`:

```js
// students
{ _id: 21, name: "Asha Kumari", course_ids: [101, 102] }

// courses
{ _id: 101, title: "Data Science", credits: 4, instructor: "Dr. Rao" }
{ _id: 102, title: "Statistics",   credits: 3, instructor: "Dr. Devi" }
```

Two reads, or a `$lookup`. **This is Course 5's foreign key, unenforced.**

### 🔢 The decision table

| Consider | **Embed** | **Reference** |
|---|---|---|
| Relationship | **One-to-one**, one-to-few | One-to-many, **many-to-many** |
| Accessed | **Always together** | Independently |
| Child size | Small and **bounded** | Large or **unbounded** |
| Change frequency | Rarely | Often |
| Duplication | Acceptable | Must be avoided |
| Reads | **One** | Two, or a `$lookup` |
| Atomicity | **Guaranteed** — a single document write is atomic | Needs a transaction |
| Document growth | Must stay under 16 MB | Unbounded is fine |

### 💡 The rule, in one sentence

> **Embed when the child is small, bounded, and always read with the parent.
> Reference when it is large, unbounded, shared, or changes independently.**

### ⚠️ The unbounded-array trap

This is the classic MongoDB design failure and it is worth a mark to name.

```js
// WRONG -- comments grow without limit
{ _id: 1, title: "Post", comments: [ /* ...50,000 of them... */ ] }
```

Three things go wrong, and only the first is obvious:

1. The document eventually **exceeds 16 MB** and writes start failing.
2. Every read of the post drags **all** the comments over the network, even
   when you wanted the title.
3. Every *write* rewrites the whole document, and once it outgrows its
   allocated space it must be **moved on disk**, invalidating index entries.

The fix is the **extended reference** or **subset** pattern: embed the few you
show, reference the rest.

```js
{ _id: 1, title: "Post",
  commentCount: 50000,
  recentComments: [ /* the newest 5, for the preview */ ] }

// comments collection, one document each
{ _id: ..., post_id: 1, text: "...", author: "..." }
```

### 🔢 Modelling the three relationship types

**One-to-one → embed, almost always.**

```js
{ _id: 21, name: "Asha",
  address: { city: "Vijayawada", pin: "520010" } }
```

Reference only if the sub-document is large or genuinely accessed alone.

**One-to-many → depends on the "many".**

- **One-to-few** (bounded, small): embed as an array — a person's phone
  numbers, a student's three addresses.
- **One-to-many** (many, but bounded): reference from the *child*, holding a
  parent id.
- **One-to-squillions** (unbounded): reference from the child, **never** an
  array on the parent.

```js
// one-to-few: embed
{ _id: 21, name: "Asha", phones: ["98765...", "98764..."] }

// one-to-squillions: the CHILD points at the parent
{ _id: 1, name: "Sensor A" }                        // devices
{ _id: ..., device_id: 1, at: ISODate(), value: 22.5 }   // readings
```

**Many-to-many → reference, from whichever side you query.**

Students take many courses; courses have many students.

```js
// Option A: array of ids on the student (query "which courses does X take?")
{ _id: 21, name: "Asha", course_ids: [101, 102] }

// Option B: both sides (fast both ways, TWO places to update)
{ _id: 101, title: "Data Science", student_ids: [21, 22, 23] }

// Option C: a separate enrolment collection -- Course 5's JUNCTION TABLE
{ _id: ..., student_id: 21, course_id: 101, grade: "A", enrolled: ISODate() }
```

**Option C is usually right when the relationship itself has attributes.** A
grade belongs to the *enrolment*, not to the student and not to the course —
exactly the reasoning that produces a junction table in Course 5, and it
survives the translation.

### 💡 The relational comparison

| | Course 5 (relational) | Course 10 (document) |
|---|---|---|
| Goal | **Eliminate** redundancy | **Manage** redundancy |
| Design driven by | The data's structure | **The queries** |
| One-to-one | Same table, or a joined table | **Embed** |
| One-to-many | Foreign key on the child | Embed if few, reference if many |
| Many-to-many | **Junction table** | Array of ids, or a junction collection |
| Reading a whole entity | Several joins | **One read** |
| Updating shared data | One place | **Several places** |

**Denormalisation is a deliberate trade, not a mistake** — Course 8's star
schema made the same one for the same reason. The difference is that a
warehouse denormalises data that is *loaded and never updated*, while a
MongoDB application denormalises data that *is* updated, and must then keep the
copies in step. That is the real cost.

## 2.7 Schema validation

Flexible does not have to mean unconstrained.

```js
db.createCollection("students", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["roll", "name", "dept"],
      properties: {
        roll: { bsonType: "int", minimum: 1,
                description: "required integer roll number" },
        name: { bsonType: "string", minLength: 3, maxLength: 80 },
        dept: { enum: ["DS", "Stats", "CS"],
                description: "must be one of the three departments" },
        marks: {
          bsonType: "object",
          properties: {
            maths: { bsonType: "int", minimum: 0, maximum: 100 },
            stats: { bsonType: "int", minimum: 0, maximum: 100 }
          }
        },
        email: { bsonType: "string", pattern: "^[^@]+@[^@]+\\.[^@]{2,}$" }
      }
    }
  },
  validationLevel: "strict",       // "strict" | "moderate" | "off"
  validationAction: "error"        // "error" | "warn"
})

db.runCommand({ collMod: "students", validator: { /* ... */ } })   // add later
```

| Setting | Effect |
|---|---|
| `validationLevel: "strict"` | Applies to **all** inserts and updates |
| `validationLevel: "moderate"` | Applies to inserts, and to updates of documents that **already** conform — so existing bad data can stay |
| `validationAction: "error"` | **Reject** the write |
| `validationAction: "warn"` | Log it and **accept** |

**`moderate` plus `warn` is how you add validation to a live collection**:
start by logging violations, fix the existing data, then tighten to `strict`
and `error`. Turning on strict validation over dirty data simply breaks the
application.

### 💡 Use it

"Schemaless" is a feature of the *engine*, not advice about your *design*. In
any collection where the fields are genuinely known — and that is most of them
— **validation costs one block of JSON and prevents a whole class of bug**:
the `colour`/`color`/`Colour` drift, the mark of 150, the missing required
field. Course 5's database enforced these for free; here you have to ask.

---

## Practice problems

### Problem 1

Design a MongoDB schema for a **student–course enrolment** system. Students have
a roll number, name, department and address; courses have a code, title,
credits and instructor; a student enrols in many courses with a grade. State
what you embed and what you reference, and justify each.

**Solution.**

**First, the queries** — because in MongoDB they determine the model:

1. Show a student's profile with the courses they take. *(very frequent)*
2. Show a course with its enrolled students. *(frequent)*
3. Record or change a grade. *(frequent)*
4. Edit a course's title or instructor. *(rare)*
5. Report the average grade per course. *(periodic)*

**The design — three collections:**

```js
// students
{ _id: 21,
  name: "Asha Kumari",
  dept: "DS",
  address: { city: "Vijayawada", state: "AP", pin: "520010" }   // EMBEDDED
}

// courses
{ _id: "DSC301",
  title: "Data Science with R",
  credits: 4,
  instructor: "Dr. Rao"
}

// enrollments -- the junction collection
{ _id: ObjectId(),
  student_id: 21,
  course_id: "DSC301",
  grade: "A",
  enrolled_on: ISODate("2026-07-01"),
  student_name: "Asha Kumari",     // DENORMALISED, for query 2
  course_title: "Data Science with R"
}
```

**Justification, decision by decision:**

| Decision | Why |
|---|---|
| **Address embedded** | One-to-one, small, bounded, always read with the student, and never queried alone. Textbook embed. |
| **Courses referenced** | Shared by many students. Embedding a course inside each student would duplicate the title and instructor across hundreds of documents, and query 4 would then have to update all of them. |
| **A separate `enrollments` collection** | **The relationship has its own attributes** — `grade` and `enrolled_on` belong to neither the student nor the course. This is Course 5's junction table, and the reasoning survives translation exactly. |
| **`course_id` as a string** | `"DSC301"` is a natural key: meaningful, already unique, and it saves a lookup just to display it. Better than an ObjectId when a real key exists. |
| **`student_name` duplicated** | Query 2 lists a course's students; without this it needs a `$lookup` on every page load. One duplicated field is a fair price. |

**And what I would watch:** `student_name` is denormalised, so **renaming a
student must update the enrolments too**. That is the cost of the choice, and
naming it is what distinguishes a complete answer. If names changed often I
would drop the duplication and accept the `$lookup`; they do not, so I keep it.

**Why not embed enrolments in the student?**

```js
{ _id: 21, name: "Asha", enrollments: [ { course_id: "DSC301", grade: "A" } ] }
```

This is defensible, and for a **read-only transcript** it is better — one read
gets everything. It fails on query 2: finding every student on DSC301 means
scanning every student document and unwinding the array. Given that both
directions are queried frequently, the junction collection wins.

### Problem 2

Explain the difference between embedded and referenced models. Give a case
where each is clearly correct, and explain the unbounded-array problem.

**Solution.**

**Embedded** stores related data inside the parent document; **referenced**
stores it separately and links by `_id`.

| | Embed | Reference |
|---|---|---|
| Reads to assemble | **One** | Two, or a `$lookup` |
| Atomic update | **Yes** — one document | Needs a transaction |
| Duplication | Likely | Avoided |
| Size risk | **Bounded by 16 MB** | None |
| Best for | One-to-one, one-to-few, read together | One-to-many, many-to-many, shared, independently updated |

**Embed is clearly right:** a person's address. One-to-one, a few small fields,
never queried on its own, never shared. Referencing it would mean a second
collection and a join for no benefit whatever.

**Reference is clearly right:** a course taken by 300 students. Embedding the
course document inside every student duplicates the title, credits and
instructor 300 times, and correcting the instructor's name becomes 300 updates
that must all succeed.

**The unbounded-array problem.** A document that embeds a collection which
grows without limit — comments on a post, readings from a sensor — fails in
three ways:

1. It eventually **exceeds the 16 MB document limit**, and writes start
   failing outright.
2. Every read pulls the **entire array** across the network, even when the
   caller wanted one field.
3. Every write **rewrites the whole document**; once it outgrows its allocated
   space it is moved on disk, and every index entry pointing at it must be
   updated.

The **subset pattern** is the fix: embed the handful you actually display, and
reference the rest.

```js
{ _id: 1, title: "Post", commentCount: 50000,
  recentComments: [ /* newest 5 */ ] }
```

The rule to state: **embed one-to-few, reference one-to-squillions.** The
question to ask of any array is "can this grow without limit?" — and if the
answer is yes, it must not be an embedded array.

### Problem 3

Write a JSON Schema validator for a `students` collection requiring: an integer
roll number of at least 1, a name of 3–80 characters, a department from a fixed
list, marks between 0 and 100, and a plausible email. Explain
`validationLevel` and `validationAction`, and how you would add this to a
collection that already holds messy data.

**Solution.**

```js
db.createCollection("students", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["roll", "name", "dept"],
      additionalProperties: true,
      properties: {
        roll: { bsonType: "int", minimum: 1,
                description: "required int, >= 1" },
        name: { bsonType: "string", minLength: 3, maxLength: 80 },
        dept: { enum: ["DS", "Stats", "CS"],
                description: "must be DS, Stats or CS" },
        marks: {
          bsonType: "object",
          properties: {
            maths: { bsonType: "int", minimum: 0, maximum: 100 },
            stats: { bsonType: "int", minimum: 0, maximum: 100 }
          }
        },
        email: { bsonType: "string",
                 pattern: "^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
})
```

**The two settings:**

| `validationLevel` | Applies to |
|---|---|
| `"strict"` | **Every** insert and update |
| `"moderate"` | Inserts, and updates of documents that **already conform** |
| `"off"` | Nothing |

| `validationAction` | On a violation |
|---|---|
| `"error"` | **Reject** the write |
| `"warn"` | **Log** it and accept the write |

**Adding it to a collection with messy data — this is the examinable part.**
Turning on `strict` + `error` over dirty data breaks the application
immediately: any update to a non-conforming document is refused, even an update
that was fixing it.

The migration is four steps:

```js
// 1. Attach the validator in the SAFEST mode: log, do not block.
db.runCommand({ collMod: "students",
                validator: { $jsonSchema: { /* as above */ } },
                validationLevel: "moderate",
                validationAction: "warn" })

// 2. FIND the offenders -- $nor + $jsonSchema inverts the match
db.students.find({ $nor: [ { $jsonSchema: { /* as above */ } } ] })

// 3. Fix them, then confirm the count is zero.

// 4. Tighten.
db.runCommand({ collMod: "students",
                validationLevel: "strict",
                validationAction: "error" })
```

`moderate` is what makes step 1 safe: existing bad documents may still be
updated, so the application keeps working while you clean up. Step 2's
`$nor: [{ $jsonSchema: ... }]` is the idiom for "find everything that does
**not** match the schema", and it is the only practical way to get the list.

**Note `additionalProperties: true`.** Leaving it true keeps MongoDB's
flexibility for fields you have not thought of, while constraining the ones you
have. Setting it `false` would reject any unexpected field — occasionally what
you want, and a significant loss of the model's main advantage.

---

## Exam questions from this unit

**Two marks**

1. Give the MongoDB terms for database, table, row and column.
2. What is the maximum document size?
3. Distinguish embedded from referenced documents.
4. Why should money not be stored as a Double?
5. Distinguish `null`, a missing field and `undefined`.
6. Why does `{ field: null }` match documents where the field is absent?
7. What is a capped collection?
8. Distinguish `countDocuments()` from `estimatedDocumentCount()`.
9. What is the unbounded-array problem?
10. Distinguish `validationLevel: "strict"` from `"moderate"`.

**Five marks**

1. Explain the MongoDB architecture with a diagram.
2. Explain MongoDB's data types with examples.
3. Explain the advantages **and disadvantages** of MongoDB over an RDBMS.
4. Explain database and collection management commands.
5. Explain schema design strategies in MongoDB.
6. Explain embedded and referenced models with the decision criteria.
7. Explain schema validation with JSON Schema.

**Ten marks**

1. Design a complete schema for a given application, justifying every embed and
   reference decision, and stating what you would watch.
2. Explain data modelling in MongoDB exhaustively — the three relationship
   types, embedding versus referencing, and the design patterns.
3. Compare relational and document data modelling with worked examples of the
   same system in both.

## Mistakes that cost marks

- Saying a collection enforces a schema by default
- Forgetting the 16 MB document limit
- Embedding an unbounded array
- Storing money as a Double
- Storing a date as a string and then trying to sort by it
- Expecting `{ f: null }` to match only explicit nulls
- Using `count()` instead of `countDocuments()`
- Believing `use dbName` creates the database
- Listing only the advantages of MongoDB and none of the costs
- Designing the schema before listing the queries
- Saying "schemaless means no design is needed" — the opposite is true
