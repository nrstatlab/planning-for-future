// Experiment 8 -- Sorting documents, limiting output, skipping records.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 08_sort_limit.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")

// Step 2: Sort
db.students.find().sort({ "marks.maths": -1 })              // -1 descending
db.students.find().sort({ dept: 1, "marks.maths": -1 })     // multi-key
// Step 3: Limit and skip
db.students.find().sort({ "marks.maths": -1 }).limit(3)     // top 3
db.students.find().skip(2).limit(2)                         // "page 2"

// The server ALWAYS applies sort, then skip, then limit -- whatever order you
// chain them in. So .limit(3).sort(...) sorts EVERYTHING and then takes three.
// Step 4: See sort apply before limit, whatever the order written
db.students.find().limit(3).sort({ "marks.maths": -1 })

// Step 5: Paginate by range, not by skip
// skip(100000) makes the server WALK AND DISCARD 100,000 documents.
// Range pagination uses the index to jump straight there:
db.students.find().sort({ _id: 1 }).limit(2)                       // page 1
const lastSeenId = 22                                              // the last _id on page 1
db.students.find({ _id: { $gt: lastSeenId } }).sort({ _id: 1 }).limit(2)   // page 2
// [Corrected: lastSeenId was never set, so this line failed with
// "ReferenceError: lastSeenId is not defined".]

// Step 6: Take the top document from the cursor
db.students.find().sort({ "marks.maths": -1 }).limit(1).next().name   // topper
