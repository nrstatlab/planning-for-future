// Experiment 7 -- Using projection to display selective fields.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 07_projection.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")

// Step 2: Include and exclude fields
db.students.find({}, { name: 1, dept: 1 })            // these fields PLUS _id
db.students.find({}, { name: 1, _id: 0 })             // exclude _id
db.students.find({}, { marks: 0, subjects: 0 })       // everything EXCEPT these
// Step 3: Project a nested field
db.students.find({}, { "marks.maths": 1, _id: 0 })    // one nested field
// Step 4: Project arrays
db.students.find({}, { subjects: { $slice: 2 } })     // first 2 array elements
db.students.find({}, { subjects: { $slice: -1 } })    // the LAST element
db.students.find({ subjects: "DS" }, { "subjects.$": 1 })   // the MATCHING one

// You cannot MIX inclusion and exclusion...
// Step 5: See that inclusion and exclusion cannot mix
db.students.find({}, { name: 1, dept: 0 })            // ERROR
// ...except for _id, which is the one exception.
db.students.find({}, { name: 1, _id: 0 })             // fine
