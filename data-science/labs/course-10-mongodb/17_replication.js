// Experiment 17 -- Replication: setting up and observing a replica set.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server:
// _drive_17_replication.py starts three mongod processes, as section 0
// describes, and runs each part of this file on the member it names. What each
// line printed is on the lab page, and
// tools/data-science/capture_lab_outputs.py runs it again. There is no .py
// half: mongomock is a library, not a server, and nothing about replication
// could stand in for three of them. (Until October 2026 mongod could not be
// installed where these labs are checked, and this file was desk-checked only.)

// =============================================================================
// Step 1: Get three servers
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
// Step 2: Initiate the set, and read its status
// 1. Initiating the set -- run ONCE, on ONE member
// =============================================================================
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "localhost:27017" },
    { _id: 1, host: "localhost:27018" },
    { _id: 2, host: "localhost:27019" }
  ]
})
// With docker compose, the hosts are the service names: mongo1:27017,
// mongo2:27017 and mongo3:27017.
// [Changed: the hosts were mongo1, mongo2 and mongo3, which exist only on the
// docker compose network. These are the three processes of the route without
// Docker, which is how this file is run.]

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
// Step 3: Write on the primary, and read on a secondary
// 2. Watching data replicate
// =============================================================================
// On the PRIMARY:
use collegeDB
db.students.insertOne({ _id: 21, name: "Asha", dept: "DS" })

// On a SECONDARY -- a second terminal, connected to port 27018:
//   mongosh --port 27018
use collegeDB
db.students.find()                      // Asha is there: the write has replicated
db.getMongo().getReadPref()             // mode 'primary' -- and yet it read a secondary

// A shell connected to ONE member reads from that member, whatever the read
// preference says. Connected to the SET --
//   mongosh "mongodb://localhost:27017,localhost:27018/?replicaSet=rs0"
// -- it sends every read to the primary, unless you say otherwise:
db.getMongo().setReadPref("secondaryPreferred")
// A secondary may be behind the primary, so reading from one is something
// you choose, by read preference, when slightly stale data is acceptable.
// [Corrected: this said the first find() fails, "not primary and
// secondaryOk=false", until setReadPref() is called. That was the old mongo
// shell. In mongosh 2, connected straight to a secondary, it reads, as above.
// It also had no use collegeDB: a new shell starts in test, where there is no
// Asha to find.]

// =============================================================================
// Step 4: Look at the oplog
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
// Step 5: Step the primary down
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
// Step 6: Set the write concern and the read concern
// 5. Write concern and read concern -- the durability dial
// =============================================================================
// On the NEW primary: after the step-down, connect to whichever member
// rs.status() now shows as PRIMARY.
use collegeDB
// [Corrected: this use collegeDB was missing. After section 3's use local, the
// inserts below went into the local database, which is never replicated.]
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
// Step 7: Make a member hidden and delayed, and add an arbiter
// 6. Priority, hidden members and arbiters
// =============================================================================
cfg = rs.conf()
cfg.members[2].priority = 0            // never becomes primary
cfg.members[2].hidden = true           // and clients never see it
cfg.members[2].secondaryDelaySecs = 3600   // an HOUR behind -- a live undo button
// [Corrected: this was slaveDelay, which MongoDB 5.0 renamed. MongoDB 8 refuses
// the old name: "BSON field 'MemberConfig.slaveDelay' is an unknown field".]
rs.reconfig(cfg)

// A delayed hidden member is the answer to "someone ran deleteMany({})".
// It has the data as it was an hour ago.

db.adminCommand({ setDefaultRWConcern: 1, defaultWriteConcern: { w: "majority" } })
rs.addArb("localhost:27020")           // an ARBITER: votes, stores no data
// An arbiter changes what "majority" means without holding any data, so
// MongoDB 5 and later refuse to add one until the default write concern has
// been set explicitly -- the line before it.
// [Corrected: the setDefaultRWConcern line was missing, and without it
// rs.addArb() fails: "Reconfig attempted to install a config that would change
// the implicit default write concern".]

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
