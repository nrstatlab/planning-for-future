// Experiment 2 -- Creating and using databases, creating collections,
// inserting documents.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 02_create_insert.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)

// Step 1: Switch to a database, which creates nothing yet
use collegeDB          // switches, but creates NOTHING yet
show dbs               // collegeDB is ABSENT until the first write

// Step 2: Create a collection
db.createCollection("students")        // only needed for OPTIONS
show collections

// Step 3: Insert one document
db.students.insertOne({
  _id: 21, name: "Asha", dept: "DS",
  marks: { maths: 88, stats: 91 },
  subjects: ["DS", "Stats", "Python"],
  age: 20, active: true
})
// -> { acknowledged: true, insertedId: 21 }

// Step 4: Insert many
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

// Step 5: See ordered stop at an error, and unordered carry on
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

// Step 6: Let MongoDB generate an ObjectId
db.students.insertOne({ name: "Devi", dept: "Stats" })
db.students.findOne({ name: "Devi" })._id.getTimestamp()   // its creation time

// Step 7: Clean up
db.students.drop()
db.dropDatabase()
