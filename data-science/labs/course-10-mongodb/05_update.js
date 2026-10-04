// Experiment 5 -- Updating documents with $set, $unset, $inc, $rename.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 05_update.py, through
// mongomock. (Until October 2026 mongod could not be installed where these labs
// are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")

// Step 2: $set, $inc, $unset and $rename
db.students.updateOne({ _id: 21 }, { $set: { age: 21 } })
db.students.updateOne({ _id: 21 }, { $set: { "marks.python": 85 } })  // nested
db.students.updateMany({ dept: "DS" }, { $inc: { "marks.maths": 5 } })
db.students.updateOne({ _id: 21 }, { $inc: { age: -1 } })             // subtract
db.students.updateOne({ _id: 21 }, { $unset: { active: "" } })        // value ignored
db.students.updateMany({}, { $rename: { "dept": "department" } })
db.students.updateMany({}, { $rename: { "department": "dept" } })   // and back again
// [Corrected: the second $rename was missing. Without it every later query on
// dept matched nothing -- the updateOne below, commented ONE of three, and the
// updateMany, all three, both reported matchedCount: 0.]
// Step 3: $mul, $max and $currentDate
db.students.updateOne({ _id: 21 }, { $mul: { "marks.maths": 1.1 } })
db.students.updateOne({ _id: 21 }, { $max: { "marks.maths": 95 } })   // only if higher
db.students.updateOne({ _id: 21 }, { $currentDate: { updated: true } })

// Several operators in ONE update
// Step 4: Several operators at once
db.students.updateOne({ _id: 22 }, {
  $set:   { grade: "B" },
  $inc:   { age: 1 },
  $unset: { active: "" }
})

// Step 5: See updateOne change exactly one
db.students.updateOne({ dept: "DS" }, { $set: { flag: true } })   // ONE of three
db.students.updateMany({ dept: "DS" }, { $set: { flag: true } })  // all three

// Step 6: See replaceOne drop every other field
db.students.replaceOne({ _id: 21 }, { name: "Asha K" })
// the document is now { _id: 21, name: "Asha K" } -- everything else is GONE

// Step 7: Upsert
db.counters.updateOne(
  { _id: "visits" },
  { $inc: { count: 1 }, $setOnInsert: { created: new Date() } },
  { upsert: true }
)

// Step 8: findOneAndUpdate
db.students.findOneAndUpdate({ _id: 21 }, { $set: { age: 22 } },
                             { returnDocument: "after" })
