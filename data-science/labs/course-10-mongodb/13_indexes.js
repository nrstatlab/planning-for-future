// Experiment 13 -- Creating and testing single-field and compound indexes.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 13_indexes.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")

// Step 2: Create and list indexes
db.students.createIndex({ dept: 1 })
db.students.createIndex({ dept: 1, "marks.maths": -1 })
db.students.createIndex({ email: 1 }, { unique: true })   // FAILS here: see below
db.students.createIndex({ dept: 1 }, { name: "dept_idx" })   // FAILS: see below
// Both fail, and both failures are worth knowing. None of the five students
// has an email, so all five index as email: null -- five duplicates of null.
// And { dept: 1 } is already indexed, as dept_1: the same keys under a second
// name are refused. [Note added: these two lines were written expecting both
// to succeed. Run, they fail, as above.]
db.students.getIndexes()
db.students.totalIndexSize()

// Step 3: Measure with explain()
db.students.find({ dept: "DS" }).explain("executionStats")
// stage:              COLLSCAN (bad)  vs  IXSCAN (good)
// totalDocsExamined / nReturned:  1 is ideal, 1000 means the index is wrong

// Step 4: Apply the prefix rule
db.students.createIndex({ dept: 1, year: 1, cgpa: 1 })
db.students.find({ dept: "DS" })                        // uses it
db.students.find({ dept: "DS", year: 4 })               // uses it
db.students.find({ year: 4 })                           // does NOT -- COLLSCAN
db.students.createIndex({ year: 1 })                    // so this is needed too

// Step 5: Apply the ESR rule
// Query: dept = "DS", maths > 70, sorted by age
db.students.createIndex({ dept: 1, age: 1, "marks.maths": 1 })
//                        ^equality ^sort   ^range
// A range predicate leaves everything AFTER it unordered, so a sort field
// placed after a range field cannot use the index.

// Step 6: Cover a query
db.students.createIndex({ dept: 1, name: 1 })
db.students.find({ dept: "DS" }, { _id: 0, dept: 1, name: 1 }).explain("executionStats")
// totalDocsExamined: 0
// [Corrected: the .explain(...) began its own line. Typed into mongosh, a line that
// starts with a dot does not continue the one above -- the shell ran the
// find() without it, then rejected ".explain(...)" as an invalid command.]

// Step 7: See two missing fields collide in a unique index
db.people.drop()
db.people.createIndex({ email: 1 }, { unique: true })
db.people.insertOne({ name: "A" })         // ok -- email missing, indexed as null
db.people.insertOne({ name: "B" })         // DUPLICATE KEY ERROR -- a second null
db.people.dropIndex("email_1")
db.people.createIndex({ email: 1 },
  { unique: true, partialFilterExpression: { email: { $exists: true } } })
db.people.insertOne({ name: "B" })         // ok now: missing emails are not indexed
// [Corrected: this used db.students, whose five students already have no email,
// so the unique index could not be built at all, and the insert of B, commented
// DUPLICATE KEY ERROR, succeeded. A new collection, as in 13_indexes.py,
// shows what the comment says.]

db.students.dropIndex("dept_1")
