// Experiment 4 -- Logical operators ($and, $or, $not, $nor) for complex
// queries.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

// Implicit AND -- the usual form
db.students.find({ dept: "DS", age: { $lt: 22 } })          // Asha, Ravi

// Explicit $and -- needed only for two conditions on the SAME field
db.students.find({ $and: [ { age: { $gte: 20 } }, { age: { $lte: 21 } } ] })

db.students.find({ $or: [ { dept: "Stats" },
                          { "marks.maths": { $gt: 85 } } ] })

// $nor: NONE of the conditions. De Morgan: NOT(A OR B) = (NOT A) AND (NOT B)
db.students.find({ $nor: [ { dept: "DS" }, { age: 20 } ] })  // Bhanu

// $not inverts ONE OPERATOR EXPRESSION -- never a plain value
db.students.find({ age: { $not: { $gt: 21 } } })            // NOT over 21
db.students.find({ age: { $not: 21 } })                     // ERROR

// Combining them
db.students.find({
  dept: "DS",
  $or: [ { "marks.maths": { $gt: 80 } }, { "marks.stats": { $gt: 80 } } ]
})

// Nested
db.students.find({
  $and: [
    { $or: [ { dept: "DS" }, { dept: "Stats" } ] },
    { $or: [ { age: 20 }, { "marks.maths": { $gt: 70 } } ] }
  ]
})
