// Experiment 9 -- Designing an Embedded Data Model for a student-course
// enrollment system.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

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
db.embedded.findOne({ _id: 21 })

db.embedded.find({ "address.city": "Vijayawada" })
db.embedded.find({ "enrollments.grade": "A" })

// TWO conditions on an array of sub-documents NEED $elemMatch, or different
// elements may satisfy different conditions.
db.embedded.find({ enrollments: { $elemMatch: { course: "DSC301", grade: "A" } } })
db.embedded.find({ "enrollments.course": "DSC301", "enrollments.grade": "A" })  // WRONG

// Updating one element: the POSITIONAL operator $
db.embedded.updateOne({ _id: 21, "enrollments.course": "STA302" },
                      { $set: { "enrollments.$.grade": "A" } })

db.embedded.updateOne({ _id: 22 },
  { $push: { enrollments: { course: "WEB303", title: "Web Technologies",
                            grade: "B", credits: 3 } } })

// Total credits, per student -- needs $unwind
db.embedded.aggregate([
  { $unwind: "$enrollments" },
  { $group: { _id: "$name", credits: { $sum: "$enrollments.credits" } } }
])
