// Experiment 15 -- The aggregation pipeline: $match, $group, $project, $sort.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 15_aggregation.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")

// Step 2: $match, $group, $sort: the whole pipeline
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

// Step 3: $group without a filter
db.students.aggregate([
  { $group: { _id: "$dept", avgMaths: { $avg: "$marks.maths" },
              n: { $sum: 1 } } },
  { $sort: { _id: 1 } }
])
// _id is MANDATORY in $group. It is the grouping key. And $group returns its
// groups in NO fixed order -- sort them whenever the order is shown.
// [Changed: the $sort was added; the groups came back in different orders.]

db.students.aggregate([ { $group: { _id: null, avg: { $avg: "$marks.maths" },
                                    n: { $sum: 1 } } } ])
// _id: null groups EVERYTHING into one bucket -- a grand total.

// Step 4: The accumulators
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
  } },
  { $set: { distinct: { $sortArray: { input: "$distinct", sortBy: 1 } } } },
  { $sort: { _id: 1 } }
])
// $addToSet keeps NO order, so the $set sorts that array before it is shown.
// [Changed: the $set and the $sort were added. The distinct names came back
// in a different order from one run to the next.]
// $push and $addToSet have no SQL equivalent, and are the reason MongoDB does
// not need GROUP_CONCAT.

// Step 5: $project: include, exclude, compute, rename
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

// Step 6: Put $match first
db.students.aggregate([ { $group: { _id: "$dept", n: { $sum: 1 } } },
                        { $match: { _id: "DS" } } ])       // SLOW: groups all
db.students.aggregate([ { $match: { dept: "DS" } },
                        { $group: { _id: "$dept", n: { $sum: 1 } } } ])   // fast
// Only the second can use an index on dept. Once documents have flowed through
// $group they are NEW documents, and no index describes them.

// Step 7: See what each stage does
db.students.aggregate([ { $match: { active: true } },
                        { $group: { _id: "$dept", n: { $sum: 1 } } } ],
                      { explain: true })
// Or truncate the pipeline and run the prefix -- the fastest way to find the
// stage that emptied your result. Compass's Aggregations tab does this for you.

// Step 8: Send the result to a collection
db.students.aggregate([
  { $group: { _id: "$dept", avg: { $avg: "$marks.maths" } } },
  { $merge: { into: "dept_summary", on: "_id",
              whenMatched: "replace", whenNotMatched: "insert" } }
])
// $out replaces the whole target collection; $merge updates it incrementally.
// Both must be the LAST stage.
