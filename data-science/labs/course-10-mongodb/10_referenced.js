// Experiment 10 -- Designing a Normalized Data Model using document
// references.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

db.students.insertOne({ _id: 21, name: "Asha Kumari", dept: "DS" })
db.courses.insertMany([
  { _id: "DSC301", title: "Data Science with R", credits: 4, instructor: "Dr. Rao" },
  { _id: "STA302", title: "Statistical Foundations", credits: 3, instructor: "Dr. Devi" }
])
db.enrollments.insertMany([
  { student_id: 21, course_id: "DSC301", grade: "A" },
  { student_id: 21, course_id: "STA302", grade: "B" }
])

// Two reads, application-side
const s = db.students.findOne({ _id: 21 })
const e = db.enrollments.find({ student_id: 21 }).toArray()

// Or one $lookup. Note: 'as' is ALWAYS an array, even for a 1-to-1 match,
// which is why $unwind almost always follows.
db.enrollments.aggregate([
  { $lookup: { from: "courses", localField: "course_id",
               foreignField: "_id", as: "course" } },
  { $unwind: "$course" },
  { $project: { _id: 0, course: "$course.title", grade: 1 } }
])

// $lookup is a LEFT OUTER JOIN -- an unmatched document gets an EMPTY ARRAY
db.enrollments.insertOne({ student_id: 21, course_id: "GONE", grade: "F" })
db.enrollments.aggregate([
  { $lookup: { from: "courses", localField: "course_id",
               foreignField: "_id", as: "course" } }
])   // the GONE row has course: []

// NOTHING stops a reference pointing at a document that does not exist.
// In Course 5 a foreign key would. Here the application must check.
db.courses.deleteOne({ _id: "DSC301" })     // the enrolments still reference it

// Index the foreignField, or every input document causes a collection scan
db.enrollments.createIndex({ course_id: 1 })
db.enrollments.createIndex({ student_id: 1 })
