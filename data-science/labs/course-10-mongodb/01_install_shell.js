// Experiment 1 -- Installing MongoDB, the Mongo shell and Compass.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. There is no .py half: these are server commands, with no query logic
// to run. (Until October 2026 mongod could not be installed where these labs
// are checked, and this file was desk-checked only.)

// Step 1: Connect
// From a terminal, NOT from inside mongosh:
//
//   mongosh                                          // localhost:27017
//   mongosh "mongodb://localhost:27017/collegeDB"    // straight into a db
//   mongosh "mongodb+srv://user:pass@cluster.mongodb.net/collegeDB"   // Atlas
//
// 27017 is the default port. Remember it -- it is asked in the viva.

// Step 2: Prove the install worked
db.version()                       // e.g. "7.0.14"
db.serverStatus().host             // hostname:port this shell is attached to
Math.floor(db.serverStatus().uptime / 60)   // whole minutes since mongod started
// [Changed: this was db.serverStatus().uptime, in seconds, which on a server
// started a moment ago reads 1 or 2 depending on the moment. In minutes it is 0.]
db.hostInfo().os                   // the OS the server is running on
db.hostInfo().system.numCores      // the cores it can see
// [Changed: this was db.hostInfo(), which prints some 350 lines, most of them
// disk counters that change by the second. These are the two lines that matter.]

show dbs                           // the databases that have been WRITTEN to
show collections                   // collections in the CURRENT database
db                                 // which database am I in?
db.getMongo()                      // the connection string

// Step 3: Use the shell as a JavaScript REPL
use collegeDB
load("00_sample_data.js")          // the five students, to have something to count
// This is the fact students most often miss, and it is worth demonstrating.
const depts = ["DS", "Stats", "CS"]
for (const d of depts) {
  print(`${d}: ${db.students.countDocuments({ dept: d })}`)
}

// Variables persist across statements; functions can be defined and reused.
function topper(dept) {
  return db.students.find({ dept }).sort({ "marks.maths": -1 }).limit(1).toArray()[0]
}
topper("DS")

// Load a script file from disk -- how you would run the rest of these labs:
//   load("02_create_insert.js")

// Step 4: Run the administrative commands
db.adminCommand({ listDatabases: 1 })
const s = db.stats()               // size, collection count, index count
({ collections: s.collections, objects: s.objects, indexes: s.indexes, dataSize: s.dataSize })
const c = db.students.stats()      // per-collection: documents, size, indexes
({ count: c.count, size: c.size, avgObjSize: c.avgObjSize, nindexes: c.nindexes })
// [Changed: these were db.stats() and db.students.stats() in full, which print
// the disk's free space and some 400 lines of storage-engine counters, both of
// which change from one run to the next. These are the figures the comments
// are about.]
db.getCollectionNames().sort()   // sorted: the server lists them in no fixed order

// Step 5: Clean up
use collegeDB                      // switches even if collegeDB does not exist
db.dropDatabase()                  // no confirmation, no undo

// --- MongoDB Compass ---------------------------------------------------------
// The official GUI (a separate download from the server).
//
//   * browse collections and documents without writing find()
//   * the Schema tab INFERS a schema from a sample -- the fastest way to see
//     what shape the documents in an inherited collection actually are
//   * the Explain Plan tab draws explain() output as a diagram instead of JSON,
//     which is worth the install on its own
//   * the Aggregations tab builds a pipeline stage by stage, showing the
//     intermediate documents after EACH stage -- exactly what you need when a
//     pipeline returns nothing and you cannot see which stage emptied it
//
// --- Know for the viva -------------------------------------------------------
//   * default port 27017
//   * mongosh is a full JavaScript REPL -- loops, variables, functions
//   * `show dbs` does NOT list a database until something has been written to
//     it: `use newdb` alone creates nothing
//   * the data directory defaults to /var/lib/mongodb (Linux); mongod refuses
//     to start if it does not exist or is not writable, which is the single
//     commonest install failure
