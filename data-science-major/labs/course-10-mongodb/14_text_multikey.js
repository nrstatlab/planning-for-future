// Experiment 14 -- Text search and multikey indexes.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB

// =============================================================================
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

// --- the restrictions, all examinable ----------------------------------------
// 1. A compound index may contain AT MOST ONE array field.
db.students.createIndex({ subjects: 1, dept: 1 })      // OK -- one array
// db.students.createIndex({ subjects: 1, tags: 1 })   // ERROR if BOTH arrays
// 2. A multikey index cannot be a shard key.
// 3. $size is never served by an index -- it must scan. Store a length field
//    alongside the array if you need to query on it:
db.students.updateMany({}, [ { $set: { nSubjects: { $size: "$subjects" } } } ])
db.students.createIndex({ nSubjects: 1 })

// --- arrays of SUB-DOCUMENTS -------------------------------------------------
db.students.createIndex({ "enrollments.grade": 1 })    // also multikey

// The trap from experiment 9, restated: without $elemMatch the two conditions
// may be satisfied by DIFFERENT elements of the array.
db.students.find({ "enrollments.course": "DSC301", "enrollments.grade": "A" })
db.students.find({ enrollments: { $elemMatch: { course: "DSC301", grade: "A" } } })

// =============================================================================
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

// --- searching ---------------------------------------------------------------
db.articles.find({ $text: { $search: "mongodb" } })
db.articles.find({ $text: { $search: "mongodb aggregation" } })   // OR, not AND
db.articles.find({ $text: { $search: "\"aggregation framework\"" } })  // PHRASE
db.articles.find({ $text: { $search: "mongodb -relational" } })    // EXCLUDE

// --- ranking by relevance ----------------------------------------------------
db.articles.find({ $text: { $search: "mongodb aggregation" } },
                 { score: { $meta: "textScore" }, title: 1 })
          .sort({ score: { $meta: "textScore" } })

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
