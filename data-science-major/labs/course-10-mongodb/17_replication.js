// Experiment 17 -- Replication: setting up and observing a replica set.
//
// *** NOT EXECUTED ***
// A replica set needs THREE mongod processes. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here, and
// it has NO .py half: mongomock is a library, not a server, and there is
// nothing about replication it could stand in for. Nothing in this file is a
// test result. See notes/sem-4/course-10-document-database/lab.md.

// =============================================================================
// 0. Getting three servers
// =============================================================================
// EASIEST -- MongoDB Atlas. The free tier IS a three-member replica set, which
// a local install is not. Connect with mongodb+srv:// and rs.status() works.
//
// LOCAL -- docker compose, three services on one network:
//
//   services:
//     mongo1: { image: mongo, command: --replSet rs0 --bind_ip_all, ports: ["27017:27017"] }
//     mongo2: { image: mongo, command: --replSet rs0 --bind_ip_all, ports: ["27018:27017"] }
//     mongo3: { image: mongo, command: --replSet rs0 --bind_ip_all, ports: ["27019:27017"] }
//
//   docker compose up -d
//   docker compose exec mongo1 mongosh
//
// WITHOUT DOCKER -- three mongod processes, three data directories, three ports:
//
//   mkdir -p /data/rs0-{1,2,3}
//   mongod --replSet rs0 --port 27017 --dbpath /data/rs0-1 --bind_ip localhost &
//   mongod --replSet rs0 --port 27018 --dbpath /data/rs0-2 --bind_ip localhost &
//   mongod --replSet rs0 --port 27019 --dbpath /data/rs0-3 --bind_ip localhost &

// =============================================================================
// 1. Initiating the set -- run ONCE, on ONE member
// =============================================================================
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})

// The shell prompt changes: rs0 [direct: other] > ... then rs0 [primary] >
// Election takes a second or two. Until it finishes there is no primary and
// no writes are accepted.

rs.status()          // members[], each with stateStr, health, optimeDate
rs.conf()            // the configuration, with each member's votes and priority
rs.isMaster()        // or db.hello() -- who is primary right now?

// WHAT TO SHOW THE EXAMINER in rs.status():
//   * exactly ONE member with stateStr "PRIMARY"
//   * two with "SECONDARY"
//   * health: 1 on all three
//   * optimeDate close together -- that closeness IS replication lag

// =============================================================================
// 2. Watching data replicate
// =============================================================================
// On the PRIMARY:
use collegeDB
db.students.insertOne({ _id: 21, name: "Asha", dept: "DS" })

// On a SECONDARY (connect to port 27018):
db.students.find()                      // ERROR: not primary and secondaryOk=false
db.getMongo().setReadPref("secondaryPreferred")
db.students.find()                      // now it works, and Asha is there

// SECONDARIES REJECT READS BY DEFAULT, and that is a deliberate choice, not a
// bug: a secondary may be behind, so MongoDB makes you say you accept that.

// =============================================================================
// 3. The oplog -- how replication actually works
// =============================================================================
use local
db.oplog.rs.find().sort({ $natural: -1 }).limit(5)
db.oplog.rs.stats().maxSize                  // the CAP, in bytes
rs.printReplicationInfo()                    // oplog size and its time window

// The oplog is a CAPPED collection of idempotent operations. Secondaries tail
// it and replay it. Two consequences worth stating in the viva:
//   * idempotent, so replaying an entry twice is safe -- which is what makes
//     recovery after a crash possible at all
//   * capped, so if a secondary falls further behind than the oplog's time
//     window, it can no longer catch up and needs a FULL resync

// =============================================================================
// 4. Failover -- the demonstration that earns the marks
// =============================================================================
rs.printSecondaryReplicationInfo()      // lag per secondary, in seconds

rs.stepDown(60)                         // primary steps down for 60 seconds
// Watch: an election starts, a secondary becomes PRIMARY, and for roughly
// 10-30 seconds there is NO primary and every write fails. Show that gap.

// Or pull the plug, which is more convincing:
//   docker compose stop mongo1
//   rs.status()      // mongo1 health 0, stateStr "(not reachable/healthy)"
//   docker compose start mongo1     // it rejoins as a SECONDARY, not primary

// =============================================================================
// 5. Write concern and read concern -- the durability dial
// =============================================================================
db.students.insertOne({ _id: 22, name: "Ravi" },
                      { writeConcern: { w: 1 } })
// Acknowledged by the PRIMARY only. Fast. Lost if the primary dies before the
// secondaries have it -- a "rollback".

db.students.insertOne({ _id: 23, name: "Meena" },
                      { writeConcern: { w: "majority", j: true, wtimeout: 5000 } })
// Acknowledged by a MAJORITY, and on disk (j: true). Slower, and survives the
// loss of any one member. ALWAYS set wtimeout, or a stalled member hangs you.

db.students.find().readConcern("majority")   // only data a majority holds
db.students.find().readConcern("local")      // the default: may be rolled back

// | w        | acknowledged by     | survives primary loss? |
// |----------|---------------------|------------------------|
// | 0        | nobody (fire and forget) | no                |
// | 1        | the primary         | NO                     |
// | majority | 2 of 3              | yes                    |

// =============================================================================
// 6. Priority, hidden members and arbiters
// =============================================================================
cfg = rs.conf()
cfg.members[2].priority = 0            // never becomes primary
cfg.members[2].hidden = true           // and clients never see it
cfg.members[2].slaveDelay = 3600       // an HOUR behind -- a live undo button
rs.reconfig(cfg)

// A delayed hidden member is the answer to "someone ran deleteMany({})".
// It has the data as it was an hour ago.

rs.addArb("mongo4:27017")              // an ARBITER: votes, stores no data

// =============================================================================
// WHY AN ODD NUMBER OF MEMBERS? -- asked every year
// =============================================================================
// A primary must be elected by a STRICT MAJORITY of votes.
//
//   3 members: majority 2, tolerates 1 failure
//   4 members: majority 3, tolerates 1 failure   <-- no better than 3
//   5 members: majority 3, tolerates 2 failures
//
// The fourth member buys NO extra fault tolerance and adds a machine, network
// traffic and a chance of a tie. So: odd numbers.
//
// The majority rule also prevents SPLIT BRAIN. If the network partitions 3-2,
// only the side of 3 can elect a primary; the side of 2 has no majority and
// steps down to secondary. Two primaries accepting conflicting writes is
// impossible by construction, not by convention.
//
// This is Unit 5 §5.7, and it is CAP in practice: MongoDB chooses CONSISTENCY
// over availability, so the minority side refuses writes rather than diverge.
