// Experiment 8 -- Sorting documents, limiting output, skipping records.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

db.students.find().sort({ "marks.maths": -1 })              // -1 descending
db.students.find().sort({ dept: 1, "marks.maths": -1 })     // multi-key
db.students.find().sort({ "marks.maths": -1 }).limit(3)     // top 3
db.students.find().skip(2).limit(2)                         // "page 2"

// The server ALWAYS applies sort, then skip, then limit -- whatever order you
// chain them in. So .limit(3).sort(...) sorts EVERYTHING and then takes three.
db.students.find().limit(3).sort({ "marks.maths": -1 })

// --- skip does not scale ----------------------------------------------------
// skip(100000) makes the server WALK AND DISCARD 100,000 documents.
// Range pagination uses the index to jump straight there:
db.students.find().sort({ _id: 1 }).limit(2)                       // page 1
db.students.find({ _id: { $gt: lastSeenId } }).sort({ _id: 1 }).limit(2)

db.students.find().sort({ "marks.maths": -1 }).limit(1).next().name   // topper
