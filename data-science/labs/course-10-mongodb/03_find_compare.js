// Experiment 3 -- Basic queries using find(), filtering with comparison
// operators.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

db.students.find()                                  // everything
db.students.find({ dept: "DS" })                    // equality
db.students.find({ dept: "DS", age: 20 })           // implicit AND
db.students.findOne({ _id: 21 })                    // ONE document, or null

// --- comparison operators ---------------------------------------------------
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

// --- dot notation into a sub-document ---------------------------------------
db.students.find({ "marks.maths": { $gte: 90 } })   // Meena
db.students.find({ "marks.maths": { $gt: 60, $lt: 90 } })

// --- $ne and $nin ALSO match documents where the field is MISSING ------------
db.students.insertOne({ _id: 26, name: "NoDept" })
db.students.find({ dept: { $ne: "DS" } })           // Stats students AND _id 26
db.students.find({ dept: { $ne: "DS", $exists: true } })   // only real depts

db.students.countDocuments({ dept: "DS" })
db.students.distinct("dept")
