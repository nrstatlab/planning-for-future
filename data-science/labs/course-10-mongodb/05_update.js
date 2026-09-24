// Experiment 5 -- Updating documents with $set, $unset, $inc, $rename.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

db.students.updateOne({ _id: 21 }, { $set: { age: 21 } })
db.students.updateOne({ _id: 21 }, { $set: { "marks.python": 85 } })  // nested
db.students.updateMany({ dept: "DS" }, { $inc: { "marks.maths": 5 } })
db.students.updateOne({ _id: 21 }, { $inc: { age: -1 } })             // subtract
db.students.updateOne({ _id: 21 }, { $unset: { active: "" } })        // value ignored
db.students.updateMany({}, { $rename: { "dept": "department" } })
db.students.updateOne({ _id: 21 }, { $mul: { "marks.maths": 1.1 } })
db.students.updateOne({ _id: 21 }, { $max: { "marks.maths": 95 } })   // only if higher
db.students.updateOne({ _id: 21 }, { $currentDate: { updated: true } })

// Several operators in ONE update
db.students.updateOne({ _id: 22 }, {
  $set:   { grade: "B" },
  $inc:   { age: 1 },
  $unset: { active: "" }
})

// --- updateOne changes ONE document even when many match --------------------
db.students.updateOne({ dept: "DS" }, { $set: { flag: true } })   // ONE of three
db.students.updateMany({ dept: "DS" }, { $set: { flag: true } })  // all three

// --- replaceOne DESTROYS every other field ----------------------------------
db.students.replaceOne({ _id: 21 }, { name: "Asha K" })
// the document is now { _id: 21, name: "Asha K" } -- everything else is GONE

// --- upsert: update if found, insert if not, ATOMICALLY ---------------------
db.counters.updateOne(
  { _id: "visits" },
  { $inc: { count: 1 }, $setOnInsert: { created: new Date() } },
  { upsert: true }
)

db.students.findOneAndUpdate({ _id: 21 }, { $set: { age: 22 } },
                             { returnDocument: "after" })
