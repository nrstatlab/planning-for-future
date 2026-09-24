// Experiment 13 -- Creating and testing single-field and compound indexes.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

db.students.createIndex({ dept: 1 })
db.students.createIndex({ dept: 1, "marks.maths": -1 })
db.students.createIndex({ email: 1 }, { unique: true })
db.students.createIndex({ dept: 1 }, { name: "dept_idx" })
db.students.getIndexes()
db.students.totalIndexSize()

// --- MEASURE. Do not guess. -------------------------------------------------
db.students.find({ dept: "DS" }).explain("executionStats")
// stage:              COLLSCAN (bad)  vs  IXSCAN (good)
// totalDocsExamined / nReturned:  1 is ideal, 1000 means the index is wrong

// --- the PREFIX rule: an index on {a,b,c} serves a, a+b, a+b+c only ---------
db.students.createIndex({ dept: 1, year: 1, cgpa: 1 })
db.students.find({ dept: "DS" })                        // uses it
db.students.find({ dept: "DS", year: 4 })               // uses it
db.students.find({ year: 4 })                           // does NOT -- COLLSCAN
db.students.createIndex({ year: 1 })                    // so this is needed too

// --- ESR: Equality, Sort, Range ---------------------------------------------
// Query: dept = "DS", maths > 70, sorted by age
db.students.createIndex({ dept: 1, age: 1, "marks.maths": 1 })
//                        ^equality ^sort   ^range
// A range predicate leaves everything AFTER it unordered, so a sort field
// placed after a range field cannot use the index.

// --- a COVERED query: every field is in the index, so no document is read ---
db.students.createIndex({ dept: 1, name: 1 })
db.students.find({ dept: "DS" }, { _id: 0, dept: 1, name: 1 })
          .explain("executionStats")     // totalDocsExamined: 0

// --- a unique index treats a MISSING field as null, and two nulls collide ---
db.students.createIndex({ email: 1 }, { unique: true })
db.students.insertOne({ name: "A" })       // ok -- email missing
db.students.insertOne({ name: "B" })       // DUPLICATE KEY ERROR
db.students.createIndex({ email: 1 },
  { unique: true, partialFilterExpression: { email: { $exists: true } } })

db.students.dropIndex("dept_1")
