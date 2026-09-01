// Experiment 1 -- Installing MongoDB, the Mongo shell and Compass.
//
// *** NOT EXECUTED ***
// This experiment needs a running server. mongod cannot be installed in the
// verification environment (the Debian repositories that host mongodb-org are
// blocked by the egress policy), so this file has never been run here, and it
// has NO .py half -- there is no query logic to execute, only server commands.
// See notes/sem-4/course-10-document-database/lab.md.

// --- 1. Connecting -----------------------------------------------------------
// From a terminal, NOT from inside mongosh:
//
//   mongosh                                          // localhost:27017
//   mongosh "mongodb://localhost:27017/collegeDB"    // straight into a db
//   mongosh "mongodb+srv://user:pass@cluster.mongodb.net/collegeDB"   // Atlas
//
// 27017 is the default port. Remember it -- it is asked in the viva.

// --- 2. Proving the install worked -------------------------------------------
db.version()                       // e.g. "7.0.14"
db.serverStatus().host             // hostname:port this shell is attached to
db.serverStatus().uptime           // seconds since mongod started
db.hostInfo()                      // OS, cores, memory the server can see

show dbs                           // the databases that have been WRITTEN to
show collections                   // collections in the CURRENT database
db                                 // which database am I in?
db.getMongo()                      // the connection string

// --- 3. mongosh is a JavaScript REPL, not a query box ------------------------
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

// --- 4. Administrative commands ----------------------------------------------
db.adminCommand({ listDatabases: 1 })
db.stats()                         // size, collection count, index count
db.students.stats()                // per-collection: storage and index sizes
db.getCollectionNames()

// --- 5. Housekeeping ---------------------------------------------------------
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
