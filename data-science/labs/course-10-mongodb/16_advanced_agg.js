// Experiment 16 -- $lookup, $unwind and $bucket.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 16_advanced_agg.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")

// =============================================================================
// $unwind -- one output document per array element
// =============================================================================
// Step 2: $unwind, and count the subjects
db.students.aggregate([ { $unwind: "$subjects" } ])
// 5 students with 3+2+2+1+1 subjects -> 9 documents out.

// The only way to count array CONTENTS:
db.students.aggregate([
  { $unwind: "$subjects" },
  { $group:  { _id: "$subjects", n: { $sum: 1 },
               who: { $push: "$name" } } },
  { $sort:   { n: -1, _id: 1 } }
])
// DS 3, Stats 3, Python 2, R 1

// Step 3: See $unwind drop empty and missing arrays
db.students.insertOne({ _id: 26, name: "Latha", dept: "DS", subjects: [] })
db.students.insertOne({ _id: 27, name: "Mohan", dept: "DS" })    // no field
db.students.aggregate([ { $unwind: "$subjects" },
                        { $count: "rows" } ])       // Latha and Mohan are GONE

db.students.aggregate([
  { $unwind: { path: "$subjects", preserveNullAndEmptyArrays: true } },
  { $count: "rows" }
])                                                  // both come back, subjects unset

// includeArrayIndex gives you the position, which $unwind otherwise loses:
db.students.aggregate([
  { $unwind: { path: "$subjects", includeArrayIndex: "pos" } },
  { $match:  { pos: 0 } }                           // each student's FIRST subject
])

// $unwind on a NON-array behaves as if it were a one-element array -- it does
// NOT error. That is why a typo'd path silently returns nothing instead.

// =============================================================================
// $lookup -- the left outer join
// =============================================================================
db.enrollments.aggregate([
  { $lookup: { from: "students", localField: "student_id",
               foreignField: "_id", as: "student" } },
  { $lookup: { from: "courses",  localField: "course_id",
               foreignField: "_id", as: "course" } },
  { $unwind: "$student" },
  { $unwind: "$course" },
  { $project: { _id: 0, name: "$student.name",
                title: "$course.title", grade: 1 } }
])

// as: ALWAYS an array, even for a one-to-one match -- hence the $unwind.
// LEFT OUTER: an unmatched document keeps its row with an EMPTY array, which
// is exactly why the $unwind after it silently deletes the unmatched rows.
// If you want them, preserveNullAndEmptyArrays: true.

// Step 4: $lookup, and count enrolments per course
db.courses.aggregate([
  { $lookup: { from: "enrollments", localField: "_id",
               foreignField: "course_id", as: "enrolled" } },
  { $project: { _id: 0, title: 1,
                n: { $size: "$enrolled" } } },       // $size, no $unwind needed
  { $sort: { n: -1 } }
])
// $size on the joined array beats $unwind + $group when you only want a count.

// Step 5: Filter the joined side first, with $lookup's pipeline
db.courses.aggregate([
  { $lookup: {
      from: "enrollments",
      let:  { cid: "$_id" },
      pipeline: [
        { $match: { $expr: { $and: [ { $eq: ["$course_id", "$$cid"] },
                                     { $eq: ["$grade", "A"] } ] } } },
        { $project: { _id: 0, student_id: 1 } }
      ],
      as: "aGrades" } }
])
// $$cid is the OUTER variable; $course_id the inner field. Two dollars means
// "from let". This form is how you avoid dragging 10,000 rows in to keep 3.

// =============================================================================
// $bucket and $bucketAuto -- histograms
// =============================================================================
// Step 6: $bucket and $facet
db.students.aggregate([
  { $bucket: {
      groupBy: "$marks.maths",
      boundaries: [0, 40, 60, 75, 101],
      default: "Other",
      output: { count: { $sum: 1 }, names: { $push: "$name" } } } }
])
// Boundaries are [lower, upper) -- CLOSED below, OPEN above.
// The last one is 101, NOT 100: with 100 as the top boundary a student who
// scored exactly 100 falls outside every bucket and lands in "Other".
// Without a `default`, an out-of-range value is an ERROR, not a silent drop.

db.students.aggregate([
  { $bucketAuto: { groupBy: "$marks.maths", buckets: 3 } }
])
// $bucketAuto picks the boundaries to even out the COUNTS. Good for
// exploration; useless for a report, because the boundaries move when the
// data does and yesterday's chart is not comparable with today's.

// $facet runs several pipelines over the SAME input, in one pass:
db.students.aggregate([
  { $facet: {
      byDept:    [ { $group: { _id: "$dept", n: { $sum: 1 } } }, { $sort: { _id: 1 } } ],
      byBand:    [ { $bucket: { groupBy: "$marks.maths",
                                boundaries: [0, 40, 60, 75, 101],
                                default: "Other",
                                output: { n: { $sum: 1 } } } } ],
      topThree:  [ { $sort: { "marks.maths": -1 } }, { $limit: 3 },
                   { $project: { _id: 0, name: 1 } } ] } }
])
// [Changed: the $sort in byDept was added. $group returns its groups in no fixed
// order, and they came back in a different order from one run to the next.]
