// Experiment 4 -- Logical operators ($and, $or, $not, $nor) for complex
// queries.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 04_logical.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")

// Implicit AND -- the usual form
// Step 2: AND, implicit and explicit
db.students.find({ dept: "DS", age: { $lt: 22 } })          // Asha, Ravi

// Explicit $and -- needed only for two conditions on the SAME field
db.students.find({ $and: [ { age: { $gte: 20 } }, { age: { $lte: 21 } } ] })

// Step 3: OR
db.students.find({ $or: [ { dept: "Stats" },
                          { "marks.maths": { $gt: 85 } } ] })

// $nor: NONE of the conditions. De Morgan: NOT(A OR B) = (NOT A) AND (NOT B)
// Step 4: NOR
db.students.find({ $nor: [ { dept: "DS" }, { age: 20 } ] })  // Bhanu

// $not inverts ONE OPERATOR EXPRESSION -- never a plain value
// Step 5: NOT, on an operator expression
db.students.find({ age: { $not: { $gt: 21 } } })            // NOT over 21
db.students.find({ age: { $not: 21 } })                     // ERROR

// Combining them
// Step 6: Combine them
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
