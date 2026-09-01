// Experiment 6 -- Deleting documents using deleteOne() and deleteMany().
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

db.students.deleteOne({ _id: 25 })
db.students.deleteOne({ dept: "DS" })          // ONE of the three
db.students.deleteMany({ dept: "DS" })         // all of them
db.students.findOneAndDelete({ _id: 21 })      // returns the deleted document

// deleteMany({}) removes EVERY document. No confirmation, no undo.
db.students.deleteMany({})                     // the COLLECTION remains
db.students.drop()                             // the collection AND its indexes
