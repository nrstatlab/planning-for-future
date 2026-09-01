// Experiment 15 -- The aggregation pipeline: $match, $group, $project, $sort.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

// --- 1. The whole pipeline, and its SQL twin ---------------------------------
//   SELECT   dept, ROUND(AVG(maths),2) AS avg, COUNT(*) AS n
//   FROM     students
//   WHERE    active = true          -- $match BEFORE $group
//   GROUP BY dept
//   HAVING   COUNT(*) > 1           -- $match AFTER  $group
//   ORDER BY avg DESC;
db.students.aggregate([
  { $match:   { active: true } },
  { $group:   { _id: "$dept", avg: { $avg: "$marks.maths" },
                n: { $sum: 1 } } },
  { $match:   { n: { $gt: 1 } } },
  { $sort:    { avg: -1 } },
  { $project: { _id: 0, dept: "$_id", avg: { $round: ["$avg", 2] }, n: 1 } }
])

// WHERE and HAVING are THE SAME STAGE in different positions. Say that in the
// viva; it is the sentence that shows you understand pipelines.

// --- 2. $group without a filter ----------------------------------------------
db.students.aggregate([
  { $group: { _id: "$dept", avgMaths: { $avg: "$marks.maths" },
              n: { $sum: 1 } } }
])
// _id is MANDATORY in $group. It is the grouping key.

db.students.aggregate([ { $group: { _id: null, avg: { $avg: "$marks.maths" },
                                    n: { $sum: 1 } } } ])
// _id: null groups EVERYTHING into one bucket -- a grand total.

// --- 3. The accumulators -----------------------------------------------------
db.students.aggregate([
  { $group: {
      _id: "$dept",
      n:        { $sum: 1 },                    // COUNT(*)
      totMaths: { $sum: "$marks.maths" },       // SUM
      avgMaths: { $avg: "$marks.maths" },       // AVG
      best:     { $max: "$marks.maths" },       // MAX
      worst:    { $min: "$marks.maths" },       // MIN
      sd:       { $stdDevPop: "$marks.maths" }, // Course 4's population sd
      everyone: { $push: "$name" },             // ALL values, as an array
      distinct: { $addToSet: "$name" },         // DISTINCT values
      anyone:   { $first: "$name" }             // needs a $sort to be meaningful
  } }
])
// $push and $addToSet have no SQL equivalent, and are the reason MongoDB does
// not need GROUP_CONCAT.

// --- 4. $project: include, exclude, compute, rename ---------------------------
db.students.aggregate([
  { $project: {
      _id: 0,
      name: 1,                                       // include
      total: { $add: ["$marks.maths", "$marks.stats"] },
      pct:   { $round: [ { $divide: [ { $add: ["$marks.maths", "$marks.stats"] },
                                      2 ] }, 1 ] },
      dept:  "$dept",                                // rename by re-assigning
      band:  { $switch: { branches: [
                 { case: { $gte: ["$marks.maths", 75] }, then: "Distinction" },
                 { case: { $gte: ["$marks.maths", 60] }, then: "First" },
                 { case: { $gte: ["$marks.maths", 40] }, then: "Pass" } ],
               default: "Fail" } }
  } }
])

// $addFields (alias: $set) keeps everything and adds -- usually what you meant.
db.students.aggregate([
  { $addFields: { total: { $add: ["$marks.maths", "$marks.stats"] } } },
  { $sort: { total: -1 } },
  { $limit: 3 }
])

// --- 5. Why $match must come first -------------------------------------------
db.students.aggregate([ { $group: { _id: "$dept", n: { $sum: 1 } } },
                        { $match: { _id: "DS" } } ])       // SLOW: groups all
db.students.aggregate([ { $match: { dept: "DS" } },
                        { $group: { _id: "$dept", n: { $sum: 1 } } } ])   // fast
// Only the second can use an index on dept. Once documents have flowed through
// $group they are NEW documents, and no index describes them.

// --- 6. Seeing what each stage does ------------------------------------------
db.students.aggregate([ { $match: { active: true } },
                        { $group: { _id: "$dept", n: { $sum: 1 } } } ],
                      { explain: true })
// Or truncate the pipeline and run the prefix -- the fastest way to find the
// stage that emptied your result. Compass's Aggregations tab does this for you.

// --- 7. Sending the result somewhere ----------------------------------------
db.students.aggregate([
  { $group: { _id: "$dept", avg: { $avg: "$marks.maths" } } },
  { $merge: { into: "dept_summary", on: "_id",
              whenMatched: "replace", whenNotMatched: "insert" } }
])
// $out replaces the whole target collection; $merge updates it incrementally.
// Both must be the LAST stage.
