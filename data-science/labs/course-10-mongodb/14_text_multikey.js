// Experiment 14 -- Text search and multikey indexes.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 14_text_multikey.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")

// =============================================================================
// Step 2: Index an array, which makes it multikey
// PART A -- MULTIKEY INDEXES (an index on an array field)
// =============================================================================
// There is no "createMultikeyIndex". You index the field, and MongoDB makes
// the index multikey BY ITSELF the moment it meets an array value.

db.students.createIndex({ subjects: 1 })

db.students.find({ subjects: "DS" })          // matches if the ARRAY CONTAINS it
db.students.find({ subjects: { $all: ["DS", "Python"] } })   // contains BOTH
db.students.find({ subjects: { $size: 3 } })  // exactly three -- NOT indexed
db.students.find({ "subjects.0": "DS" })      // DS is the FIRST element

// One index ENTRY per array element. A student with 3 subjects contributes 3
// entries pointing at the same document, which is why multikey indexes are
// larger than they look, and why an array of 1,000 elements is a bad idea.

// Step 3: Meet the restrictions
// 1. A compound index may contain AT MOST ONE array field.
db.students.createIndex({ subjects: 1, dept: 1 })      // OK -- one array
// db.students.createIndex({ subjects: 1, tags: 1 })   // ERROR if BOTH arrays
// 2. A multikey index cannot be a shard key.
// 3. $size is never served by an index -- it must scan. Store a length field
//    alongside the array if you need to query on it:
db.students.updateMany({}, [ { $set: { nSubjects: { $size: "$subjects" } } } ])
db.students.createIndex({ nSubjects: 1 })

// Step 4: Index an array of sub-documents, and fall into the trap
db.transcripts.drop()
db.transcripts.insertOne({ _id: 21, name: "Asha", enrollments: [
  { course: "DSC301", grade: "B" }, { course: "STA302", grade: "A" } ] })
db.transcripts.createIndex({ "enrollments.grade": 1 })    // also multikey

// The trap from experiment 9, restated: without $elemMatch the two conditions
// may be satisfied by DIFFERENT elements of the array.
db.transcripts.find({ "enrollments.course": "DSC301", "enrollments.grade": "A" })   // Asha -- wrongly
db.transcripts.find({ enrollments: { $elemMatch: { course: "DSC301", grade: "A" } } })   // nobody
// [Corrected: these queried db.students, whose documents have no enrollments,
// so both found nothing and the trap did not show. Asha's B in DSC301 and A in
// STA302 are two different elements, and only $elemMatch tells them apart.]

// =============================================================================
// Step 5: Create a text index
// PART B -- TEXT INDEXES
// =============================================================================
db.articles.drop()
db.articles.insertMany([
  { _id: 1, title: "Introduction to MongoDB",
    body: "MongoDB is a document database that stores data in BSON." },
  { _id: 2, title: "Aggregation pipelines explained",
    body: "The aggregation framework processes documents through stages." },
  { _id: 3, title: "Indexing strategy in MongoDB",
    body: "An index is a B-tree. Aggregation queries benefit from indexes too." },
  { _id: 4, title: "Relational databases",
    body: "SQL databases use tables, rows and joins." }
])

// Weights make a hit in the title count ten times a hit in the body.
db.articles.createIndex({ title: "text", body: "text" },
                        { weights: { title: 10, body: 1 },
                          name: "article_text",
                          default_language: "english" })

// Step 6: Search
db.articles.find({ $text: { $search: "mongodb" } })
db.articles.find({ $text: { $search: "mongodb aggregation" } })   // OR, not AND
db.articles.find({ $text: { $search: "\"aggregation framework\"" } })  // PHRASE
db.articles.find({ $text: { $search: "mongodb -relational" } })    // EXCLUDE

// Step 7: Rank by relevance
db.articles.find({ $text: { $search: "mongodb aggregation" } },
                 { score: { $meta: "textScore" }, title: 1 }).sort({ score: { $meta: "textScore" } })
// [Corrected: the .sort(...) began its own line. Typed into mongosh, a line that
// starts with a dot does not continue the one above -- the shell ran the
// find(), unsorted, without it, then rejected ".sort(...)" as an invalid command.]

// The sort is NOT optional. $text returns matches in no particular order; the
// score exists only if you project it, and only sorts if you sort by it.

// --- the rules, all examinable ----------------------------------------------
// 1. ONE text index per collection. It may span many fields -- even every
//    field, via { "$**": "text" } -- but you cannot have two.
db.articles.dropIndex("article_text")
db.articles.createIndex({ "$**": "text" })     // a WILDCARD text index
db.articles.dropIndex("$**_text")
db.articles.createIndex({ title: "text", body: "text" },
                        { weights: { title: 10, body: 1 }, name: "article_text" })
// 2. $text searches WORDS, not substrings. "mongo" does not match "MongoDB".
//    For substrings and prefixes you need a regex, or Atlas Search.
// 3. Search is case-insensitive and diacritic-insensitive by default.
// 4. Stemming and stop words follow default_language: searching "stores" also
//    matches "store" and "storing"; "the" and "is" are ignored entirely.
// 5. Only ONE $text expression per query, and it cannot appear inside $or with
//    a non-text clause.

db.articles.getIndexes()
