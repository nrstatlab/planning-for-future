// Experiment 3 -- Basic queries using find(), filtering with comparison
// operators.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 03_find_compare.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")

// Step 2: Find by equality, and findOne
db.students.find()                                  // everything
db.students.find({ dept: "DS" })                    // equality
db.students.find({ dept: "DS", age: 20 })           // implicit AND
db.students.findOne({ _id: 21 })                    // ONE document, or null

// Step 3: Use the comparison operators
db.students.find({ age: { $gt:  20 } })             // Ravi, Kiran, Bhanu
db.students.find({ age: { $gte: 21 } })
db.students.find({ age: { $lt:  21 } })             // Asha, Meena
db.students.find({ age: { $lte: 20 } })
db.students.find({ age: { $ne:  20 } })
db.students.find({ dept: { $in:  ["DS", "CS"] } })
db.students.find({ dept: { $nin: ["Stats"] } })

// A RANGE goes in ONE object. Written as two keys it is a JavaScript object
// with a duplicate key -- the first is SILENTLY DISCARDED.
db.students.find({ age: { $gte: 20, $lte: 21 } })   // correct
db.students.find({ age: { $gte: 20 }, age: { $lte: 21 } })   // WRONG, silently

// Step 4: Query a sub-document with dot notation
db.students.find({ "marks.maths": { $gte: 90 } })   // Meena
db.students.find({ "marks.maths": { $gt: 60, $lt: 90 } })

// Step 5: See $ne match a missing field
db.students.insertOne({ _id: 26, name: "NoDept" })
db.students.find({ dept: { $ne: "DS" } })           // Stats students AND _id 26
db.students.find({ dept: { $ne: "DS", $exists: true } })   // only real depts

// Step 6: Count, and find the distinct values
db.students.countDocuments({ dept: "DS" })
db.students.distinct("dept")
