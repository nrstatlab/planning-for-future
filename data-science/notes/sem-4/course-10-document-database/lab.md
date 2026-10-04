# Practical Lab

**20 experiments**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.

Code lives in `labs/course-10-mongodb/`.

> **Both halves run.** Every experiment has a **`mongosh` script**, `NN_name.js` — **what the lab
> examiner will ask you to demonstrate** — and it is run on **MongoDB 8.3.7**, typed into
> **mongosh 2.12.0** line by line as you would at the prompt, on a fresh server each time.
> Under **5. Execution and Results** is the session: each statement after its prompt, then what
> the shell printed. Sixteen also have a **Python half**, `NN_name.py`, the same query logic
> through **mongomock**, asserted by `tools/data-science/run_mongo_labs.py`.
>
> Experiment 17 runs on a real **three-member replica set** (three `mongod` processes, as its
> section 0 describes, and a fourth as an arbiter), Experiment 18 with the real **`mongofiles`**,
> and Experiment 19 on a replica set, which transactions need.
>
> Until October 2026 `mongod` could not be installed where these labs are checked, and every
> script said NOT EXECUTED. MongoDB's own download hosts are still blocked; conda-forge's builds
> of the same server can be reached, and `tools/data-science/setup_mongodb.sh` installs them.
> Running the scripts found eleven of them doing something other than what their comments said
> — a placeholder that is a syntax error, a variable never set, lines that start with a dot,
> statements on data that was not there, MongoDB 8 refusing two old forms — each corrected in
> its file, with a note, and listed under its experiment below.

```bash
tools/data-science/setup_mongodb.sh               # mongod and mongofiles, in /tmp/mongodb
npm --prefix tools/data-science install           # mongosh
python3 tools/data-science/run_mongo_labs.py      # both halves of every experiment
```

Two things in the output change from run to run: the ObjectIds, dates and UUIDs a server makes
new each time, and everything about a replica set's election. `capture_lab_outputs.py --check`
compares every other character of a session exactly; for Experiment 17 it reruns the
replica set and checks what the experiment shows, as the driver's assertions.

## The sample data

Every experiment from 3 onwards starts from the same five students, with the courses and
enrolments Experiment 16 joins. `00_sample_data.js` loads them: each script that needs them runs
`load("00_sample_data.js")` straight after `use collegeDB`, so it can be run on its own, as often
as you like. Start `mongosh` in the labs folder for `load()` to find it. The data is exactly that
in `fixtures.py`, which the Python halves load, and `run_mongo_labs.py` checks that the two agree.

{{programme: course-10-mongodb/00_sample_data.js}}

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

### 1. Question

Install MongoDB, and use the Mongo Shell and Compass.

### 2. Aim

Prove a server is running, find your way round mongosh, and know what Compass adds.

### 3. Steps

1. **Connect.**
2. **Prove the install worked.**
3. **Use the shell as a JavaScript REPL.**
4. **Run the administrative commands.**
5. **Clean up.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

**MongoDB Compass** is the official GUI: browse collections, build queries
without typing them, and read `explain()` output as a diagram rather than
JSON. Worth installing for the `explain` visualiser alone.

**Know for the viva:** the default port is **27017**; `mongosh` is a full
**JavaScript** REPL, so loops and variables work in it; and `show dbs` will not
list a database until something has been written to it.
</div>


### 4. Programme

{{programme: course-10-mongodb/01_install_shell.js}}

### 5. Execution and Results

{{output: course-10-mongodb/01_install_shell.js}}

`db.version()` reports the server, 8.3.7. **Changed:** `db.hostInfo()`,
`db.serverStatus().uptime`, `db.stats()` and `db.students.stats()` printed hundreds of lines of
machine and storage counters, which differ by the second; the script now asks each for the
figures its comment is about. Experiment 1 has no Python half: there is no query logic in it.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The server is MongoDB 8.3.7 on port 27017; mongosh runs JavaScript, so the loop and the function count and find as they should.
</div>


## Experiment 2 — Databases, collections, inserting documents

### 1. Question

Create a database and a collection, and insert documents into it.

### 2. Aim

Insert one and many documents, and see what ordered and unordered inserts do on an error.

### 3. Steps

**In mongosh**, `02_create_insert.js`:

1. **Switch to a database, which creates nothing yet.**
2. **Create a collection.**
3. **Insert one document.**
4. **Insert many.**
5. **See ordered stop at an error, and unordered carry on.**
6. **Let MongoDB generate an ObjectId.**
7. **Clean up.**

**In Python, through mongomock**, `02_create_insert.py`:

1. **See the database appear on the first write.**
2. **Insert one and many.**
3. **See ordered stop and unordered carry on.**
4. **Look at a generated ObjectId.**
5. **Manage the collections.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

The two behaviours that are examinable, shown in the session and asserted by the Python half:

- **Lazy creation** — the database does not exist until the first write.
- **`ordered: true` (the default) stops at the first error**, so documents
  after a duplicate `_id` are never attempted; `ordered: false` inserts them.
</div>


### 4. Programme

**In mongosh**, `02_create_insert.js`:

{{programme: course-10-mongodb/02_create_insert.js}}

**In Python, through mongomock**, `02_create_insert.py`:

{{programme: course-10-mongodb/02_create_insert.py}}

### 5. Execution and Results

**In mongosh**, `02_create_insert.js`:

{{output: course-10-mongodb/02_create_insert.js}}

**In Python, through mongomock**, `02_create_insert.py`:

{{output: course-10-mongodb/02_create_insert.py}}

The ordered insert's error reports `insertedCount: 1` — `X` went in, the duplicate
stopped it, `Y` was never tried; the unordered one inserted both `P` and `Q`. The ObjectId and
the time it carries are the server's, and differ every run.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

collegeDB appears in show dbs only after the first write; the ordered insert stops at the duplicate _id, and the unordered one carries on past it.
</div>


## Experiment 3 — find() and comparison operators

### 1. Question

Query documents with find(), filtering with the comparison operators.

### 2. Aim

Filter with every comparison operator, and avoid the two traps.

### 3. Steps

**In mongosh**, `03_find_compare.js`:

1. **Load the sample data.**
2. **Find by equality, and findOne.**
3. **Use the comparison operators.**
4. **Query a sub-document with dot notation.**
5. **See $ne match a missing field.**
6. **Count, and find the distinct values.**

**In Python, through mongomock**, `03_find_compare.py`:

1. **Find by equality, and findOne.**
2. **Use the comparison operators.**
3. **Write a range as one object.**
4. **Query a sub-document with dot notation.**
5. **See $ne match a missing field.**
6. **Count, and find the distinct values.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

Every comparison operator, dot notation into a sub-document, and the
two traps — **a range must be one object**, and **`$ne` also matches documents
where the field is missing**.
</div>


### 4. Programme

**In mongosh**, `03_find_compare.js`:

{{programme: course-10-mongodb/03_find_compare.js}}

**In Python, through mongomock**, `03_find_compare.py`:

{{programme: course-10-mongodb/03_find_compare.py}}

### 5. Execution and Results

**In mongosh**, `03_find_compare.js`:

{{output: course-10-mongodb/03_find_compare.js}}

**In Python, through mongomock**, `03_find_compare.py`:

{{output: course-10-mongodb/03_find_compare.py}}

The range written as two keys returns more than the range: the first key is discarded,
silently, and only `$lte: 21` is applied.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Every operator returns the students its comment names; $ne returns the document with no dept at all.
</div>


## Experiment 4 — Logical operators

### 1. Question

Combine query conditions with the logical operators.

### 2. Aim

Combine conditions with $and, $or, $nor and $not.

### 3. Steps

**In mongosh**, `04_logical.js`:

1. **Load the sample data.**
2. **AND, implicit and explicit.**
3. **OR.**
4. **NOR.**
5. **NOT, on an operator expression.**
6. **Combine them.**

**In Python, through mongomock**, `04_logical.py`:

1. **AND, implicit and explicit.**
2. **OR.**
3. **NOR, by De Morgan.**
4. **NOT, on an operator expression.**
5. **Combine them.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

`$nor: [A, B]` equals `(NOT A) AND (NOT B)` — De Morgan from Computer Fundamentals and Office
Automation — and **`$not` cannot take a plain value**, only an operator expression. Both shown,
and asserted by the Python half.
</div>


### 4. Programme

**In mongosh**, `04_logical.js`:

{{programme: course-10-mongodb/04_logical.js}}

**In Python, through mongomock**, `04_logical.py`:

{{programme: course-10-mongodb/04_logical.py}}

### 5. Execution and Results

**In mongosh**, `04_logical.js`:

{{output: course-10-mongodb/04_logical.js}}

**In Python, through mongomock**, `04_logical.py`:

{{output: course-10-mongodb/04_logical.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

$nor returns Bhanu alone, as (NOT DS) AND (NOT 20) does; $not with a plain value is an error.
</div>


## Experiment 5 — Updating with $set, $unset, $inc, $rename

### 1. Question

Update documents with the update operators.

### 2. Aim

Change documents with $set, $unset, $inc and $rename, and see what replaceOne and upsert do.

### 3. Steps

**In mongosh**, `05_update.js`:

1. **Load the sample data.**
2. **$set, $inc, $unset and $rename.**
3. **$mul, $max and $currentDate.**
4. **Several operators at once.**
5. **See updateOne change exactly one.**
6. **See replaceOne drop every other field.**
7. **Upsert.**
8. **findOneAndUpdate.**

**In Python, through mongomock**, `05_update.py`:

1. **$set, $unset, $inc and $rename.**
2. **Several operators at once.**
3. **See updateOne change exactly one.**
4. **See replaceOne drop every other field.**
5. **Upsert.**
6. **findOneAndUpdate.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

**`replaceOne` keeps only `_id`** and discards every other field, while `updateOne`
with `$set` preserves them. And `updateOne` changes **exactly one** document when three match —
the commonest CRUD mistake, and silent.
</div>


### 4. Programme

**In mongosh**, `05_update.js`:

{{programme: course-10-mongodb/05_update.js}}

**In Python, through mongomock**, `05_update.py`:

{{programme: course-10-mongodb/05_update.py}}

### 5. Execution and Results

**In mongosh**, `05_update.js`:

{{output: course-10-mongodb/05_update.js}}

**In Python, through mongomock**, `05_update.py`:

{{output: course-10-mongodb/05_update.py}}

**Corrected:** the `$rename` of `dept` to `department` was never undone, so every
later query on `dept` matched nothing — the `updateOne` commented "ONE of three" and the
`updateMany` "all three" both reported `matchedCount: 0`. A second `$rename` now puts it back.
The Python half had passed, because each of its functions starts from fresh data.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

updateOne changed one of the three DS students and updateMany all three; replaceOne left Asha only a name; the upsert inserted the counter.
</div>


## Experiment 6 — Deleting

### 1. Question

Delete documents, and a collection.

### 2. Aim

Delete one, many and all documents, and tell deleting them from dropping the collection.

### 3. Steps

**In mongosh**, `06_delete.js`:

1. **Load the sample data.**
2. **deleteOne and deleteMany.**
3. **findOneAndDelete.**
4. **deleteMany({}) against drop().**

**In Python, through mongomock**, `06_delete.py`:

1. **deleteOne and deleteMany.**
2. **findOneAndDelete.**
3. **Tell deleteMany({}) from drop().**
4. **See an empty filter delete everything.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

`deleteMany({})` empties the collection but **keeps** it, its indexes
and its validator; `drop()` removes all three.

**There is no confirmation and no undo.** In Database Management Systems, `DELETE FROM t` at least
sat inside a transaction you could roll back.
</div>


### 4. Programme

**In mongosh**, `06_delete.js`:

{{programme: course-10-mongodb/06_delete.js}}

**In Python, through mongomock**, `06_delete.py`:

{{programme: course-10-mongodb/06_delete.py}}

### 5. Execution and Results

**In mongosh**, `06_delete.js`:

{{output: course-10-mongodb/06_delete.js}}

**In Python, through mongomock**, `06_delete.py`:

{{output: course-10-mongodb/06_delete.py}}

**Corrected:** `findOneAndDelete` was on `_id` 21, Asha, already deleted as one of
the DS students, so it returned `null`; it is now on Meena, the one student left, and returns her.
**Changed:** the sample data is loaded again before `deleteMany({})`, which otherwise had one
document left to delete, and `getCollectionNames()` shows the collection before and after
`drop()`.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

deleteMany({}) deleted all five and left the collection listed; drop() removed it.
</div>


## Experiment 7 — Projection

### 1. Question

Choose which fields a query returns, with a projection.

### 2. Aim

Include and exclude fields, nested ones and array elements.

### 3. Steps

**In mongosh**, `07_projection.js`:

1. **Load the sample data.**
2. **Include and exclude fields.**
3. **Project a nested field.**
4. **Project arrays.**
5. **See that inclusion and exclusion cannot mix.**

**In Python, through mongomock**, `07_projection.py`:

1. **Include and exclude fields.**
2. **See that the two cannot mix.**
3. **Project nested fields.**
4. **Project arrays.**
5. **See projection reduce the work.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

**Mixing inclusion and exclusion raises an error**, and **`_id` is
the one exception** — it may be excluded alongside inclusions.
</div>


### 4. Programme

**In mongosh**, `07_projection.js`:

{{programme: course-10-mongodb/07_projection.js}}

**In Python, through mongomock**, `07_projection.py`:

{{programme: course-10-mongodb/07_projection.py}}

### 5. Execution and Results

**In mongosh**, `07_projection.js`:

{{output: course-10-mongodb/07_projection.js}}

**In Python, through mongomock**, `07_projection.py`:

{{output: course-10-mongodb/07_projection.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Inclusion and exclusion cannot be mixed, except for _id; $slice and the positional $ cut arrays down.
</div>


## Experiment 8 — Sorting, limiting, skipping

### 1. Question

Sort, limit and skip the results of a query.

### 2. Aim

Order results and page through them, the slow way and the fast way.

### 3. Steps

**In mongosh**, `08_sort_limit.js`:

1. **Load the sample data.**
2. **Sort.**
3. **Limit and skip.**
4. **See sort apply before limit, whatever the order written.**
5. **Paginate by range, not by skip.**
6. **Take the top document from the cursor.**

**In Python, through mongomock**, `08_sort_limit.py`:

1. **Sort.**
2. **Limit and skip.**
3. **See sort, skip and limit apply in a fixed order.**
4. **Paginate by range, not by skip.**
5. **Tell a cursor from a document.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

**The server applies sort, then skip, then limit**, regardless of the
chaining order — so `.limit(3).sort(...)` sorts everything and then takes
three.

The script also demonstrates **range pagination** (`{ _id: { $gt: last } }`) as
the fix for `skip`'s linear cost.
</div>


### 4. Programme

**In mongosh**, `08_sort_limit.js`:

{{programme: course-10-mongodb/08_sort_limit.js}}

**In Python, through mongomock**, `08_sort_limit.py`:

{{programme: course-10-mongodb/08_sort_limit.py}}

### 5. Execution and Results

**In mongosh**, `08_sort_limit.js`:

{{output: course-10-mongodb/08_sort_limit.js}}

**In Python, through mongomock**, `08_sort_limit.py`:

{{output: course-10-mongodb/08_sort_limit.py}}

**Corrected:** `lastSeenId` was used but never set, so the range query failed with
"ReferenceError: lastSeenId is not defined". It is now set to 22, the last `_id` on page 1.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

limit(3).sort(...) gives the top three, not three sorted; page 2 by range is Meena and Kiran.
</div>


## Experiment 9 — An embedded data model

### 1. Question

Design and query an embedded data model.

### 2. Aim

Store a student's address and enrolments inside the student, and query them.

### 3. Steps

**In mongosh**, `09_embedded.js`:

1. **Insert two students, with their address and enrolments embedded.**
2. **Read everything in one query.**
3. **Query nested fields and arrays.**
4. **Use $elemMatch for two conditions on one element.**
5. **Update one array element, and push another.**
6. **Total the credits.**

**In Python, through mongomock**, `09_embedded.py`:

1. **Read everything in one query.**
2. **Query nested fields and arrays.**
3. **Use $elemMatch for two conditions on one element.**
4. **Update one array element.**
5. **Push, and aggregate.**
6. **State the model's limitation.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

**One read returns everything** — no join anywhere — and the `$elemMatch`
requirement for two conditions on the enrolment array.
</div>


### 4. Programme

**In mongosh**, `09_embedded.js`:

{{programme: course-10-mongodb/09_embedded.js}}

**In Python, through mongomock**, `09_embedded.py`:

{{programme: course-10-mongodb/09_embedded.py}}

### 5. Execution and Results

**In mongosh**, `09_embedded.js`:

{{output: course-10-mongodb/09_embedded.js}}

**In Python, through mongomock**, `09_embedded.py`:

{{output: course-10-mongodb/09_embedded.py}}

**Changed:** the credits total now ends with a `$sort`. `$group` returns its groups in
no fixed order, and on the real server Asha and Ravi came back in a different order from one run
to the next.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

One findOne returns the student with everything; $elemMatch finds Asha's A in DSC301 where the two separate conditions match wrongly.
</div>


## Experiment 10 — A normalized model with references

### 1. Question

Design and query a normalised model, with documents that reference each other.

### 2. Aim

Join referenced collections with $lookup, and see what references do not guarantee.

### 3. Steps

**In mongosh**, `10_referenced.js`:

1. **Insert a student, the courses and the enrolments, as references.**
2. **Two reads, or one $lookup.**
3. **See $lookup keep an unmatched row, as a left outer join.**
4. **See references not enforced.**
5. **Index the foreign fields.**

**In Python, through mongomock**, `10_referenced.py`:

1. **Two reads, or one $lookup.**
2. **See $lookup always give an array.**
3. **See $lookup is a left outer join.**
4. **See references are not enforced.**
5. **Index the foreign field.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

`$lookup` produces an **array** even for a one-to-one match, which is
why `$unwind` follows it; and it is a **left outer join** — an unmatched
document gets an empty array, not nothing.
</div>


### 4. Programme

**In mongosh**, `10_referenced.js`:

{{programme: course-10-mongodb/10_referenced.js}}

**In Python, through mongomock**, `10_referenced.py`:

{{programme: course-10-mongodb/10_referenced.py}}

### 5. Execution and Results

**In mongosh**, `10_referenced.js`:

{{output: course-10-mongodb/10_referenced.js}}

**In Python, through mongomock**, `10_referenced.py`:

{{output: course-10-mongodb/10_referenced.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

$lookup returns an array, and keeps the GONE enrolment with an empty one; deleting a course leaves its enrolments pointing at nothing.
</div>


## Experiment 11 — One-to-one, one-to-many, many-to-many

### 1. Question

Model one-to-one, one-to-many and many-to-many relationships.

### 2. Aim

Model each kind of relationship, and query it from both ends.

### 3. Steps

**In mongosh**, `11_relationships.js`:

1. **One-to-one: embed.**
2. **One-to-many: reference from the child.**
3. **One-to-few: embed an array.**
4. **Many-to-many: reference both ways.**

**In Python, through mongomock**, `11_relationships.py`:

1. **One-to-one: embed.**
2. **One-to-few: embed an array.**
3. **One-to-many: reference from the child.**
4. **Many-to-many: reference both ways.**
5. **Give the relationship's own data to a junction collection.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

All three modelled and queried:

| Relationship | Model | Query direction |
|---|---|---|
| One-to-one | Embed the address | Both, from the student |
| One-to-many | Reference from the **child** | Course → its enrolments |
| Many-to-many | A junction collection | Both directions |

The junction collection is what carries the **grade** — an attribute of the *relationship*,
belonging to neither entity.
</div>


### 4. Programme

**In mongosh**, `11_relationships.js`:

{{programme: course-10-mongodb/11_relationships.js}}

**In Python, through mongomock**, `11_relationships.py`:

{{programme: course-10-mongodb/11_relationships.py}}

### 5. Execution and Results

**In mongosh**, `11_relationships.js`:

{{output: course-10-mongodb/11_relationships.js}}

**In Python, through mongomock**, `11_relationships.py`:

{{output: course-10-mongodb/11_relationships.py}}

**Corrected:** the many-to-many's `updateOne` was on student 21, who exists only if
Experiment 10 has just been run in the same database; on its own it matched nothing, and "who
takes DSC301?" returned no one. It is now an upsert, which works either way.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Each relationship is modelled and queried both ways; the junction collection holds the grade.
</div>


## Experiment 12 — Schema validation with JSON Schema

### 1. Question

Validate documents against a JSON Schema.

### 2. Aim

Enforce a schema on a collection, and add one to a collection that already holds data.

### 3. Steps

**In mongosh**, `12_validation.js`:

1. **Load the sample data.**
2. **Write the schema.**
3. **Create a collection that enforces it.**
4. **Insert a conforming document, and four that are not.**
5. **Add validation to data already there, in stages.**

**In Python, through mongomock**, `12_validation.py`:

1. **Pass a conforming document.**
2. **Catch each violation.**
3. **Find the documents that do not conform.**
4. **Tighten validation in stages.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

Attach the schema in the safest mode first — `moderate` + `warn` — find the
offenders with `{ $nor: [ { $jsonSchema: … } ] }`, fix them, then tighten to `strict` + `error`.

**mongomock does not enforce `$jsonSchema`**, so the Python half implements the same rules in
code and asserts that conforming documents pass and each kind of violation is caught — among them a missing
required field, a wrong type, a value outside the enum. The real server enforces them, and its
error names the rule that failed.
</div>


### 4. Programme

**In mongosh**, `12_validation.js`:

{{programme: course-10-mongodb/12_validation.js}}

**In Python, through mongomock**, `12_validation.py`:

{{programme: course-10-mongodb/12_validation.py}}

### 5. Execution and Results

**In mongosh**, `12_validation.js`:

{{output: course-10-mongodb/12_validation.js}}

**In Python, through mongomock**, `12_validation.py`:

{{output: course-10-mongodb/12_validation.py}}

**Corrected:** the second part read `{ $jsonSchema: { /* as above */ } }`, an empty
schema, which every document passes, so no offender could be found. The schema is now a `const`,
written once and used three times.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The conforming document goes in and each of the four violations is refused, by MongoDB itself; all five sample students fail the schema, having no roll.
</div>


## Experiment 13 — Single-field and compound indexes

### 1. Question

Create single-field and compound indexes, and measure their effect.

### 2. Aim

Create indexes, read explain(), and apply the prefix and ESR rules.

### 3. Steps

**In mongosh**, `13_indexes.js`:

1. **Load the sample data.**
2. **Create and list indexes.**
3. **Measure with explain().**
4. **Apply the prefix rule.**
5. **Apply the ESR rule.**
6. **Cover a query.**
7. **See two missing fields collide in a unique index.**

**In Python, through mongomock**, `13_indexes.py`:

1. **Create and list indexes.**
2. **See a unique index enforced.**
3. **See two missing fields collide.**
4. **Apply the prefix rule.**
5. **Apply the ESR rule.**
6. **Cover a query.**
7. **Count what indexes cost.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

**Run `explain("executionStats")` and read `totalDocsExamined / nReturned`** — that
ratio, not the wall-clock time, is what tells you whether the index is right. mongomock records
indexes but has no planner, so the Python half asserts that the indexes are **created and
listed** correctly and that a **unique** index rejects a duplicate. The **prefix rule** and
**ESR** are demonstrated as a table of which queries each index serves; the server shows the
plans.
</div>


### 4. Programme

**In mongosh**, `13_indexes.js`:

{{programme: course-10-mongodb/13_indexes.js}}

**In Python, through mongomock**, `13_indexes.py`:

{{programme: course-10-mongodb/13_indexes.py}}

### 5. Execution and Results

**In mongosh**, `13_indexes.js`:

{{output: course-10-mongodb/13_indexes.js}}

**In Python, through mongomock**, `13_indexes.py`:

{{output: course-10-mongodb/13_indexes.py}}

The covered query's plan is `PROJECTION_COVERED` with `totalDocsExamined: 0`, as its
comment says.

Corrected or noted, from running it: the unique index on `email` and the `dept_idx` index fail at
the top, and the file now says why — none of the five students has an email, so all five index
as null, and `{ dept: 1 }` already exists as `dept_1`. The demonstration that two missing fields
collide used `db.students`, where the unique index could not be built at all, so the insert
commented DUPLICATE KEY ERROR succeeded; it now uses a new collection, as the Python half does.
And `.explain(...)` began its own line, which mongosh does not join to the line above.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

find({ dept: "DS" }) is an IXSCAN examining 3 documents for 3 returned; the covered query examines none.
</div>


## Experiment 14 — Text search and multikey indexes

### 1. Question

Search text with a text index, and index an array with a multikey index.

### 2. Aim

Index arrays and text, and search by words with relevance.

### 3. Steps

**In mongosh**, `14_text_multikey.js`:

1. **Load the sample data.**
2. **Index an array, which makes it multikey.**
3. **Meet the restrictions.**
4. **Index an array of sub-documents, and fall into the trap.**
5. **Create a text index.**
6. **Search.**
7. **Rank by relevance.**

**In Python, through mongomock**, `14_text_multikey.py`:

1. **See an index on an array become multikey.**
2. **Count one entry per element.**
3. **Use $all, $size and the positional operator.**
4. **Store the length to query it.**
5. **Fall into the $elemMatch trap.**
6. **State the compound restriction.**
7. **Note that mongomock has no $text.**
8. **Work out what a real server returns.**
9. **Search by regex instead.**
10. **State the text index rules.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

An index on an array field creates **one entry per element**, so `{ subjects: "DS" }`
matches any student whose array contains it. **Only one text index is allowed per collection**
— it may span several fields, but you cannot have two.

mongomock does not implement `$text`, so the Python half asserts the multikey behaviour and works
out by hand what a server's text search returns; the session shows the server's.
</div>


### 4. Programme

**In mongosh**, `14_text_multikey.js`:

{{programme: course-10-mongodb/14_text_multikey.js}}

**In Python, through mongomock**, `14_text_multikey.py`:

{{programme: course-10-mongodb/14_text_multikey.py}}

### 5. Execution and Results

**In mongosh**, `14_text_multikey.js`:

{{output: course-10-mongodb/14_text_multikey.js}}

**In Python, through mongomock**, `14_text_multikey.py`:

{{output: course-10-mongodb/14_text_multikey.py}}

**Corrected:** the `$elemMatch` trap queried `db.students`, whose documents have no
enrolments, so both queries found nothing; it now has a document to find, in which Asha has a B
in DSC301 and an A in STA302. And the ranking's `.sort(...)` began its own line, so the search ran
unsorted and the shell rejected the sort.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The array index is multikey; $text matches whole words and ranks by score; without $elemMatch, Asha is found for an A in DSC301 she does not have.
</div>


## Experiment 15 — $match, $group, $project, $sort

### 1. Question

Aggregate documents with $match, $group, $project and $sort.

### 2. Aim

Build an aggregation pipeline, and see each stage's SQL counterpart.

### 3. Steps

**In mongosh**, `15_aggregation.js`:

1. **Load the sample data.**
2. **$match, $group, $sort: the whole pipeline.**
3. **$group without a filter.**
4. **The accumulators.**
5. **$project: include, exclude, compute, rename.**
6. **Put $match first.**
7. **See what each stage does.**
8. **Send the result to a collection.**

**In Python, through mongomock**, `15_aggregation.py`:

1. **$match then $group: WHERE and HAVING.**
2. **See the filter change the answer.**
3. **Group by a key, or by null for a total.**
4. **Use the accumulators.**
5. **Note the operators mongomock lacks.**
6. **$project: compute and rename.**
7. **$addFields: keep everything.**
8. **$match first.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

Shown twice, and the pair is the point. **With** the `active: true`
filter, Kiran (DS, 71, inactive) is excluded, so DS is (88+65)/2 = **76.5**
over 2 and Stats (94+52)/2 = **73** over 2. **Without** it — Unit 4's
Problem 1(a) — DS is (88+65+71)/3 = **74.667** over 3. Same grouping, and the
`$match` before it moves the DS average *up*.

**`$match` before and after `$group` are `WHERE` and `HAVING`** — the same stage in different
positions. mongomock lacks `$round` and `$stdDevPop`, so the Python half computes those in Python
and says so; the server has both.
</div>


### 4. Programme

**In mongosh**, `15_aggregation.js`:

{{programme: course-10-mongodb/15_aggregation.js}}

**In Python, through mongomock**, `15_aggregation.py`:

{{programme: course-10-mongodb/15_aggregation.py}}

### 5. Execution and Results

**In mongosh**, `15_aggregation.js`:

{{output: course-10-mongodb/15_aggregation.js}}

**In Python, through mongomock**, `15_aggregation.py`:

{{output: course-10-mongodb/15_aggregation.py}}

**Changed:** two `$group`s now end with a `$sort`, and the `$addToSet` list of names is
sorted with `$sortArray`. `$group` and `$addToSet` keep no order, and the names came back in a
different order from one run to the next.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

With the active filter DS averages 76.5 over 2 and Stats 73 over 2; without it, DS averages 74.67 over 3.
</div>


## Experiment 16 — $lookup, $unwind, $bucket

### 1. Question

Aggregate across collections and arrays with $lookup, $unwind and $bucket.

### 2. Aim

Unwind arrays, join collections, and bucket values into ranges.

### 3. Steps

**In mongosh**, `16_advanced_agg.js`:

1. **Load the sample data.**
2. **$unwind, and count the subjects.**
3. **See $unwind drop empty and missing arrays.**
4. **$lookup, and count enrolments per course.**
5. **Filter the joined side first, with $lookup's pipeline.**
6. **$bucket and $facet.**

**In Python, through mongomock**, `16_advanced_agg.py`:

1. **$unwind: one document per element.**
2. **Count what the arrays hold.**
3. **See $unwind drop empty and missing arrays.**
4. **includeArrayIndex, and fields that are not arrays.**
5. **$lookup: an array, by a left outer join.**
6. **Join both ways.**
7. **Note that mongomock lacks $lookup's pipeline form.**
8. **$bucket: closed below, open above.**
9. **See why the top boundary is 101.**
10. **Note that mongomock lacks $bucketAuto.**
11. **$facet: several pipelines in one pass.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

Subject counts DS 3, Stats 3, Python 2, R 1; and the bucket
distribution — with the top boundary at **101, not 100**, because buckets are
`[lower, upper)` and 100 as the boundary would lose a perfect scorer to
`default`.

**`$unwind` silently drops empty and missing arrays**, and
`preserveNullAndEmptyArrays: true` keeps them. That one is worth seeing fail.
</div>


### 4. Programme

**In mongosh**, `16_advanced_agg.js`:

{{programme: course-10-mongodb/16_advanced_agg.js}}

**In Python, through mongomock**, `16_advanced_agg.py`:

{{programme: course-10-mongodb/16_advanced_agg.py}}

### 5. Execution and Results

**In mongosh**, `16_advanced_agg.js`:

{{output: course-10-mongodb/16_advanced_agg.js}}

**In Python, through mongomock**, `16_advanced_agg.py`:

{{output: course-10-mongodb/16_advanced_agg.py}}

Latha (an empty subjects array) and Mohan (none at all) have no maths mark either, so
`$bucket` puts them in `Other`. **Changed:** the `$facet`'s count by department now ends with a
`$sort`, for the same reason as Experiment 15.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Subject counts are DS 3, Stats 3, Python 2, R 1; $unwind drops Latha and Mohan; the buckets use 101 as the top boundary so a perfect score is kept.
</div>


## Experiment 17 — Replication with a replica set

### 1. Question

Set up a replica set, and watch it replicate and fail over.

### 2. Aim

Initiate a three-member replica set, read from a secondary, force a failover, and configure the members.

### 3. Steps

1. **Get three servers.**
2. **Initiate the set, and read its status.**
3. **Write on the primary, and read on a secondary.**
4. **Look at the oplog.**
5. **Step the primary down.**
6. **Set the write concern and the read concern.**
7. **Make a member hidden and delayed, and add an arbiter.**

<div class="formula" markdown="1">
<span class="label">WHAT TO DEMONSTRATE</span>

**What to demonstrate:** `rs.status()` showing one PRIMARY and two SECONDARY;
`rs.stepDown()` triggering an election; writes failing during it; and `w: "majority"` versus
`w: 1`. The theory is Unit 5 §5.7 — and the question "why an odd number of members?" is asked
every year.

`_drive_17_replication.py` starts three `mongod` processes on ports 27017–27019 and a fourth on
27020, as section 0's route without Docker describes, and types each part of the script into a
shell on the member it names. It waits where you would wait — for the election after
`rs.initiate()`, and for a new primary after `rs.stepDown()` — and asserts what the experiment
shows. An election, the oplog and every time in `rs.status()` differ on every run, so this is
one run's output, recorded.

To do this on your own machine, `docker compose` with three `mongo` services is the easiest
route, or use Atlas — its free tier **is** a three-member replica set.
</div>


### 4. Programme

{{programme: course-10-mongodb/17_replication.js}}

### 5. Execution and Results

{{output: course-10-mongodb/17_replication.js}}

Four corrections, each found by running it:

- **The secondary read.** The script said `db.students.find()` on a secondary fails, "not primary
  and secondaryOk=false", until `setReadPref()`. That was the old `mongo` shell: mongosh 2,
  connected straight to a secondary, reads from it whatever the read preference says, as the
  session shows. It is a connection to the whole set that sends reads to the primary. The
  secondary's session also lacked `use collegeDB`, so it looked in `test`.
- **`use collegeDB` before section 5.** After section 3's `use local`, the inserts went into the
  `local` database, which is never replicated.
- **`slaveDelay` is now `secondaryDelaySecs`.** MongoDB 5.0 renamed it, and MongoDB 8 rejects the
  old name.
- **`rs.addArb()` needs `setDefaultRWConcern` first**, in MongoDB 5 and later; without it the
  arbiter is refused.

And the hosts: `rs.initiate` named `mongo1`–`mongo3`, which exist only on the Docker network; it
now names the local route's three processes, with the Docker form in a comment.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

One PRIMARY and two SECONDARY; Asha replicated to the secondary; after rs.stepDown() a new primary was elected; the hidden delayed member and the arbiter were accepted.
</div>


## Experiment 18 — GridFS

### 1. Question

Store and retrieve a large file with GridFS.

### 2. Aim

Put a file into GridFS, see how it is stored, and get it back.

### 3. Steps

1. **Put a file in GridFS with mongofiles.**
2. **Look at what it stored, and count the chunks.**
3. **Do it from a driver.**
4. **Query by metadata.**
5. **Delete it, with its chunks.**

<div class="formula" markdown="1">
<span class="label">WHAT TO DEMONSTRATE</span>

**What to demonstrate:** that a file appears as **one** document in `fs.files`
and **many** in `fs.chunks`, and that `chunks == ceil(bytes / 261120)`. The
point to state: GridFS is for files over 16 MB, or where you need to read
**ranges** — for smaller files, object storage is usually better.

`_drive_18_gridfs.py` makes a 10 MB file and runs section 1's `mongofiles` commands for real —
`put`, `list`, and `get` to a copy, compared byte for byte — then types sections 2 to 4 into
mongosh, and deletes the file with `mongofiles delete`, as section 5 recommends.
</div>


### 4. Programme

{{programme: course-10-mongodb/18_gridfs.js}}

### 5. Execution and Results

{{output: course-10-mongodb/18_gridfs.js}}

`mongofiles` cannot attach metadata, so section 4's queries on `metadata.course` find
nothing, as they would after any `mongofiles put`; a driver upload, as in section 3, sets it.

**Corrected:** the chunk count read `{ files_id: <the _id from fs.files> }`, a placeholder that
mongosh rejects as a syntax error; the line before it now looks the `_id` up. **Changed:** the
metadata `$group` ends with a `$sort`.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The 10 MB file is one document in fs.files and 41 in fs.chunks, as ceil(10485760 / 261120) says; the copy back is identical; mongofiles delete removes both.
</div>


## Experiment 19 — Transactions

### 1. Question

Make a multi-document transaction, committed and aborted.

### 2. Aim

Transfer money between two accounts in a transaction, and see an abort undo everything.

### 3. Steps

1. **Set up two accounts.**
2. **Transfer, and commit.**
3. **Overdraw, and abort.**
4. **Retry on a transient error.**

<div class="formula" markdown="1">
<span class="label">WHAT TO DEMONSTRATE</span>

**Transactions are unavailable on a standalone `mongod`** — they depend on the
oplog and majority commit, so a replica set is required. That fact is itself a
five-mark answer. This experiment runs on a one-member replica set, which is enough.

**What to demonstrate:** a transfer that commits, and one that aborts midway
leaving **both** balances unchanged. And the point from Unit 5 §5.9: a schema
that needs transactions for its *common* operations is usually one that should
have embedded.
</div>


### 4. Programme

{{programme: course-10-mongodb/19_transactions.js}}

### 5. Execution and Results

{{output: course-10-mongodb/19_transactions.js}}

**Corrected:** the script quoted a standalone server's refusal as "Transaction numbers
are only allowed on a replica set member or mongos". MongoDB 8 with mongosh 2 says instead "This
MongoDB deployment does not support retryable writes. Please add retryWrites=false to your
connection string" — and says it again with `retryWrites=false`. **Added:** a `find()` at the end
reads the balances back; both were only printed as text.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The transfer committed, A 4500 and B 3500; the overdraft aborted, and both balances are unchanged, read back from the database.
</div>


## Experiment 20 — Case study: a mini-application

### 1. Question

Build a mini-application: a library management system.

### 2. Aim

Implement the library schema, issue and return books, run the reports, and check the stock counts stay true.

### 3. Steps

**In mongosh**, `20_case_study.js`:

1. **Seed the books and members.**
2. **Create the indexes.**
3. **Issue books, with a conditional decrement.**
4. **Return them, and charge the fines.**
5. **Run the five reports.**
6. **Check the stock counts against the loans.**

**In Python, through mongomock**, `20_case_study.py`:

1. **Seed the books, members and loans.**
2. **Issue and return a book.**
3. **Refuse a sixth copy of a five-copy book.**
4. **Return on time and late.**
5. **Run the five reports.**
6. **Break the stock count, and catch it.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

A **library management system** — the schema designed in
[practice.md](practice.md) Section C question 1 — exercising CRUD, aggregation
and indexing together:

1. Seed books, members and loans.
2. **Issue** a book: insert a loan and decrement `availableCopies`
   **conditionally** (`availableCopies: { $gt: 0 }`), so a third copy of a
   two-copy book cannot be lent.
3. **Return** it: set `returned`, compute any fine, increment the count back.
4. **Overdue report** — `{ returned: null, due: { $lt: asAt } }`.
5. **Most-borrowed** — an aggregation with `$match` first.
6. Check `availableCopies` is **consistent** with the count of unreturned
   loans.

That last check is the point of the experiment: the **computed pattern**
speeds up the hottest query and introduces a value that can drift, and the only
defence is to check it. The Python half asserts it at every step.
</div>


### 4. Programme

**In mongosh**, `20_case_study.js`:

{{programme: course-10-mongodb/20_case_study.js}}

**In Python, through mongomock**, `20_case_study.py`:

{{programme: course-10-mongodb/20_case_study.py}}

### 5. Execution and Results

**In mongosh**, `20_case_study.js`:

{{output: course-10-mongodb/20_case_study.js}}

**In Python, through mongomock**, `20_case_study.py`:

{{output: course-10-mongodb/20_case_study.py}}

**Changed:** loans were issued at `new Date()`, the moment the script ran, so no return
could be late and the overdue report could never find anything. The script now issues on a fixed
day, 26 August 2026, as the Python half does, and returns one book on time and one six days late.
**Corrected:** the overdue report's `.sort(...)` began its own line, which mongosh rejected. And
this page said the refused loan was "the sixth copy of a five-copy book"; it is the third of
*Effective Java*'s two copies.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A third loan of a two-copy book is refused; returns on day 10 and day 20 are fined Rs 0 and Rs 12; two loans are overdue at day 20; the integrity check finds no drift.
</div>


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
- Starting a line with `.sort(...)` or `.explain(...)` at the shell: mongosh runs the line above
  on its own, and rejects this one

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
  deleted document. In Database Management Systems the database guaranteed it; here the
  application must.
- **When asked to demonstrate replication, GridFS or transactions, say what
  they require** — three `mongod` processes, and a replica set for
  transactions. Knowing *why* transactions need one (they depend on the oplog
  and majority commit) is worth more than a script you cannot run.
