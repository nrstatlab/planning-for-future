// Experiment 6 -- Deleting documents using deleteOne() and deleteMany().
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 06_delete.py, through
// mongomock. (Until October 2026 mongod could not be installed where these labs
// are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")

// Step 2: deleteOne and deleteMany
db.students.deleteOne({ _id: 25 })
db.students.deleteOne({ dept: "DS" })          // ONE of the three
db.students.deleteMany({ dept: "DS" })         // all of them
// Step 3: findOneAndDelete
db.students.findOneAndDelete({ _id: 23 })      // returns the deleted document
// [Corrected: this deleted _id 21, Asha -- already gone, as one of the three DS
// students deleted above -- so it returned null, not a document. Meena, 23, is
// the one student left.]

// deleteMany({}) removes EVERY document. No confirmation, no undo.
// Step 4: deleteMany({}) against drop()
load("00_sample_data.js")                      // five students again, to delete
db.students.deleteMany({})                     // the COLLECTION remains
db.getCollectionNames().sort()                 // students is still listed
db.students.drop()                             // the collection AND its indexes
db.getCollectionNames().sort()                 // and now it is not
// [Changed: the load and the two getCollectionNames() lines were added, so that
// deleteMany({}) has something to delete and the difference from drop() shows.
// The names are sorted because the server lists them in no fixed order.]
