// Experiment 10 -- Designing a Normalized Data Model using document
// references.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 10_referenced.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)

// Step 1: Insert a student, the courses and the enrolments, as references
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
// Step 2: Two reads, or one $lookup
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
// Step 3: See $lookup keep an unmatched row, as a left outer join
db.enrollments.insertOne({ student_id: 21, course_id: "GONE", grade: "F" })
db.enrollments.aggregate([
  { $lookup: { from: "courses", localField: "course_id",
               foreignField: "_id", as: "course" } }
])   // the GONE row has course: []

// NOTHING stops a reference pointing at a document that does not exist.
// In Course 5 a foreign key would. Here the application must check.
// Step 4: See references not enforced
db.courses.deleteOne({ _id: "DSC301" })     // the enrolments still reference it

// Index the foreignField, or every input document causes a collection scan
// Step 5: Index the foreign fields
db.enrollments.createIndex({ course_id: 1 })
db.enrollments.createIndex({ student_id: 1 })
