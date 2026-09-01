// Experiment 2 -- Creating and using databases, creating collections,
// inserting documents.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in 02_create_insert.py, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

// --- databases are created LAZILY -------------------------------------------
use collegeDB          // switches, but creates NOTHING yet
show dbs               // collegeDB is ABSENT until the first write

// --- collections ------------------------------------------------------------
db.createCollection("students")        // only needed for OPTIONS
show collections

// --- insertOne --------------------------------------------------------------
db.students.insertOne({
  _id: 21, name: "Asha", dept: "DS",
  marks: { maths: 88, stats: 91 },
  subjects: ["DS", "Stats", "Python"],
  age: 20, active: true
})
// -> { acknowledged: true, insertedId: 21 }

// --- insertMany -------------------------------------------------------------
db.students.insertMany([
  { _id: 22, name: "Ravi",  dept: "DS",    marks: { maths: 65, stats: 58 },
    subjects: ["DS", "Python"], age: 21, active: true },
  { _id: 23, name: "Meena", dept: "Stats", marks: { maths: 94, stats: 89 },
    subjects: ["Stats", "R"],   age: 20, active: true },
  { _id: 24, name: "Kiran", dept: "DS",    marks: { maths: 71, stats: 66 },
    subjects: ["DS"],           age: 22, active: false },
  { _id: 25, name: "Bhanu", dept: "Stats", marks: { maths: 52, stats: 47 },
    subjects: ["Stats"],        age: 21, active: true }
])

show dbs                          // NOW collegeDB appears
db.students.countDocuments()      // 5

// --- ordered: the default is TRUE, and it STOPS at the first error -----------
db.students.insertMany([
  { _id: 30, name: "X" },
  { _id: 21, name: "DUPLICATE" },   // _id 21 exists -> error
  { _id: 31, name: "Y" }
])
// ordered (default): 30 inserted, 21 fails, 31 NEVER ATTEMPTED

db.students.insertMany([
  { _id: 40, name: "P" },
  { _id: 21, name: "DUPLICATE" },
  { _id: 41, name: "Q" }
], { ordered: false })
// unordered: 40 AND 41 inserted; only 21 fails

// --- an ObjectId is generated when you omit _id ------------------------------
db.students.insertOne({ name: "Devi", dept: "Stats" })
db.students.findOne({ name: "Devi" })._id.getTimestamp()   // its creation time

// --- clean up ---------------------------------------------------------------
db.students.drop()
db.dropDatabase()
