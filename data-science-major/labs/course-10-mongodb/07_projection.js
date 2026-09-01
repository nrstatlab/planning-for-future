// Experiment 7 -- Using projection to display selective fields.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

db.students.find({}, { name: 1, dept: 1 })            // these fields PLUS _id
db.students.find({}, { name: 1, _id: 0 })             // exclude _id
db.students.find({}, { marks: 0, subjects: 0 })       // everything EXCEPT these
db.students.find({}, { "marks.maths": 1, _id: 0 })    // one nested field
db.students.find({}, { subjects: { $slice: 2 } })     // first 2 array elements
db.students.find({}, { subjects: { $slice: -1 } })    // the LAST element
db.students.find({ subjects: "DS" }, { "subjects.$": 1 })   // the MATCHING one

// You cannot MIX inclusion and exclusion...
db.students.find({}, { name: 1, dept: 0 })            // ERROR
// ...except for _id, which is the one exception.
db.students.find({}, { name: 1, _id: 0 })             // fine
