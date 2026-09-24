// Experiment 11 -- Modeling relationships: One-to-One, One-to-Many,
// Many-to-Many in MongoDB.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

// ---------- ONE-TO-ONE: EMBED ----------------------------------------------
// Small, bounded, always read together, never queried alone.
db.people.insertOne({
  _id: 21, name: "Asha Kumari",
  address: { city: "Vijayawada", state: "AP", pin: "520010" }
})
db.people.find({ "address.pin": "520010" })

// ---------- ONE-TO-MANY: reference from the CHILD ---------------------------
// A course has many enrolments. The array must NOT live on the course, because
// it is unbounded -- that is the 16 MB trap.
db.courses.insertOne({ _id: "DSC301", title: "Data Science with R" })
db.enrollments.insertMany([
  { course_id: "DSC301", student_id: 21, grade: "A" },
  { course_id: "DSC301", student_id: 22, grade: "C" }
])
db.enrollments.find({ course_id: "DSC301" })          // the "many" side

// ---------- ONE-TO-FEW: embed as an array -----------------------------------
db.people.updateOne({ _id: 21 },
  { $set: { phones: ["9876543210", "9876543211"] } })

// ---------- MANY-TO-MANY ----------------------------------------------------
// Option A: an array of ids on one side
db.students.updateOne({ _id: 21 }, { $set: { course_ids: ["DSC301", "STA302"] } })
db.students.find({ course_ids: "DSC301" })            // who takes DSC301?

// Option C: a junction collection -- REQUIRED when the relationship itself
// has attributes. The grade belongs to neither the student nor the course.
db.enrollments.find({ student_id: 21 })               // this student's courses
db.enrollments.find({ course_id: "DSC301" })          // this course's students
