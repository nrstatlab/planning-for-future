// Experiment 9 -- Designing an Embedded Data Model for a student-course
// enrollment system.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 09_embedded.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)

// Step 1: Insert two students, with their address and enrolments embedded
use collegeDB
db.embedded.drop()

db.embedded.insertMany([
  { _id: 21, name: "Asha Kumari", dept: "DS",
    address: { city: "Vijayawada", state: "AP", pin: "520010" },   // 1-to-1
    enrollments: [                                                 // 1-to-few
      { course: "DSC301", title: "Data Science with R", grade: "A", credits: 4 },
      { course: "STA302", title: "Statistical Foundations", grade: "B", credits: 3 }
    ] },
  { _id: 22, name: "Ravi Teja", dept: "DS",
    address: { city: "Guntur", state: "AP", pin: "522002" },
    enrollments: [
      { course: "DSC301", title: "Data Science with R", grade: "C", credits: 4 }
    ] }
])

// ONE read gets the student, their address and every enrolment. No join.
// Step 2: Read everything in one query
db.embedded.findOne({ _id: 21 })

// Step 3: Query nested fields and arrays
db.embedded.find({ "address.city": "Vijayawada" })
db.embedded.find({ "enrollments.grade": "A" })

// TWO conditions on an array of sub-documents NEED $elemMatch, or different
// elements may satisfy different conditions.
// Step 4: Use $elemMatch for two conditions on one element
db.embedded.find({ enrollments: { $elemMatch: { course: "DSC301", grade: "A" } } })
db.embedded.find({ "enrollments.course": "DSC301", "enrollments.grade": "A" })  // WRONG

// Updating one element: the POSITIONAL operator $
// Step 5: Update one array element, and push another
db.embedded.updateOne({ _id: 21, "enrollments.course": "STA302" },
                      { $set: { "enrollments.$.grade": "A" } })

db.embedded.updateOne({ _id: 22 },
  { $push: { enrollments: { course: "WEB303", title: "Web Technologies",
                            grade: "B", credits: 3 } } })

// Total credits, per student -- needs $unwind
// Step 6: Total the credits
db.embedded.aggregate([
  { $unwind: "$enrollments" },
  { $group: { _id: "$name", credits: { $sum: "$enrollments.credits" } } },
  { $sort: { _id: 1 } }
])
// [Changed: the $sort was added. $group returns its groups in no fixed order, and
// they came back in a different order from one run to the next.]
