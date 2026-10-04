// Experiment 11 -- Modeling relationships: One-to-One, One-to-Many,
// Many-to-Many in MongoDB.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 11_relationships.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)

use collegeDB

// Step 1: One-to-one: embed
// Small, bounded, always read together, never queried alone.
db.people.insertOne({
  _id: 21, name: "Asha Kumari",
  address: { city: "Vijayawada", state: "AP", pin: "520010" }
})
db.people.find({ "address.pin": "520010" })

// Step 2: One-to-many: reference from the child
// A course has many enrolments. The array must NOT live on the course, because
// it is unbounded -- that is the 16 MB trap.
db.courses.insertOne({ _id: "DSC301", title: "Data Science with R" })
db.enrollments.insertMany([
  { course_id: "DSC301", student_id: 21, grade: "A" },
  { course_id: "DSC301", student_id: 22, grade: "C" }
])
db.enrollments.find({ course_id: "DSC301" })          // the "many" side

// Step 3: One-to-few: embed an array
db.people.updateOne({ _id: 21 },
  { $set: { phones: ["9876543210", "9876543211"] } })

// Step 4: Many-to-many: reference both ways
// Option A: an array of ids on one side
db.students.updateOne({ _id: 21 },
  { $set: { name: "Asha Kumari", course_ids: ["DSC301", "STA302"] } },
  { upsert: true })
// [Corrected: this was an updateOne without upsert, on a student 21 who exists
// only if Experiment 10 has just been run in the same database. On its own it
// matched nothing, and the find below returned no one.]
db.students.find({ course_ids: "DSC301" })            // who takes DSC301?

// Option C: a junction collection -- REQUIRED when the relationship itself
// has attributes. The grade belongs to neither the student nor the course.
db.enrollments.find({ student_id: 21 })               // this student's courses
db.enrollments.find({ course_id: "DSC301" })          // this course's students
