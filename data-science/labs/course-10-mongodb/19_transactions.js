// Experiment 19 -- Multi-document ACID transactions.
//
// *** NOT EXECUTED ***
// Transactions require a REPLICA SET -- they depend on the oplog and majority
// commit -- and mongomock is a library, not a server, so it has none of that.
// mongod cannot be installed in the verification environment (the Debian
// repositories that host mongodb-org are blocked by the egress policy). This
// file has never been run here and has NO .py half.
// See notes/sem-4/course-10-document-database/lab.md.

// =============================================================================
// THE PREREQUISITE, which is itself a five-mark answer
// =============================================================================
// A standalone mongod REFUSES to start a transaction:
//
//   MongoServerError: Transaction numbers are only allowed on a replica set
//   member or mongos
//
// WHY: a transaction's commit must be durable and visible atomically, and
// MongoDB implements that on the oplog with a majority write concern. A
// standalone has no oplog to write to and no majority to reach. So: set up
// experiment 17 first, or use Atlas, whose free tier is a replica set.
//
// Single-DOCUMENT operations have always been atomic, replica set or not.
// That is the point most students miss, and it is why most well-modelled
// MongoDB applications never need this feature at all.

// =============================================================================
// 1. Setting up something worth a transaction
// =============================================================================
use bankDB
db.accounts.drop()
db.accounts.insertMany([
  { _id: "A", holder: "Asha", balance: 5000 },
  { _id: "B", holder: "Ravi", balance: 3000 }
])
// A transfer touches TWO documents. Nothing about the document model makes
// that atomic, and here the two balances genuinely belong to two owners --
// so this is the case where embedding is not the answer.

// =============================================================================
// 2. The core API -- a transfer that COMMITS
// =============================================================================
const session = db.getMongo().startSession()
const accounts = session.getDatabase("bankDB").accounts

session.startTransaction({
  readConcern:  { level: "snapshot" },
  writeConcern: { w: "majority" }
})

try {
  accounts.updateOne({ _id: "A" }, { $inc: { balance: -500 } })
  accounts.updateOne({ _id: "B" }, { $inc: { balance:  500 } })
  session.commitTransaction()
  print("committed: A 4500, B 3500")
} catch (e) {
  session.abortTransaction()
  print("aborted: " + e)
  throw e
} finally {
  session.endSession()
}

// IMPORTANT: reads and writes must go through session.getDatabase(...).
// db.accounts.updateOne(...) inside the block is NOT in the transaction --
// it commits immediately, and nothing warns you. That is the single commonest
// mistake with this API.

// =============================================================================
// 3. The demonstration that matters: an ABORT leaves BOTH unchanged
// =============================================================================
// Show the balances before, run this, show them after. Nothing moved.
const s2 = db.getMongo().startSession()
const acc2 = s2.getDatabase("bankDB").accounts
s2.startTransaction()
try {
  acc2.updateOne({ _id: "A" }, { $inc: { balance: -9999 } })   // overdraws
  const a = acc2.findOne({ _id: "A" })
  if (a.balance < 0) throw new Error("insufficient funds")
  acc2.updateOne({ _id: "B" }, { $inc: { balance: 9999 } })
  s2.commitTransaction()
} catch (e) {
  s2.abortTransaction()          // A's -9999 is UNDONE
  print("aborted, both balances unchanged: " + e.message)
} finally { s2.endSession() }

// Read A from ANOTHER shell while the transaction is open: you see the OLD
// balance. Uncommitted writes are invisible outside the session -- snapshot
// isolation, and the visible proof that this is a real transaction.

// =============================================================================
// 4. Retrying -- required, not optional
// =============================================================================
// A transaction can fail with a TRANSIENT error (a write conflict, a failover
// mid-commit). The error carries a label, and the caller is expected to retry:
//
//   e.hasErrorLabel("TransientTransactionError")   -> retry the WHOLE thing
//   e.hasErrorLabel("UnknownTransactionCommitResult") -> retry the COMMIT only
//
// Drivers wrap this: session.withTransaction(fn) retries for you and is what
// you should actually use.
//
//   session.withTransaction(() => {
//     accounts.updateOne({ _id: "A" }, { $inc: { balance: -500 } })
//     accounts.updateOne({ _id: "B" }, { $inc: { balance:  500 } })
//   })
//
// The callback must be IDEMPOTENT, because it may run more than once.

// =============================================================================
// 5. The limits
// =============================================================================
//   * default 60-second time limit (transactionLifetimeLimitSeconds); a
//     transaction that exceeds it is aborted
//   * 16 MB of oplog entries per transaction
//   * they hold locks, so long transactions block other writers
//   * a sharded transaction is slower again -- it coordinates across shards
//   * DDL inside a transaction is restricted: no createIndex, no dropDatabase;
//     collection creation is allowed only from MongoDB 4.4 onward

// =============================================================================
// THE POINT, from Unit 5 §5.9
// =============================================================================
// Transactions arrived in MongoDB 4.0 and are genuinely ACID. But:
//
//   IF YOUR COMMON OPERATIONS NEED THEM, YOUR SCHEMA IS PROBABLY WRONG.
//
// A student and their address, an order and its lines, a post and its
// comments -- embed those and every update is a single-document write, atomic
// with no transaction at all. Transactions are for the genuine cross-entity
// case: a bank transfer, where the two balances belong to different people and
// no amount of remodelling puts them in one document.
//
// Compare with Course 5: in SQL, transactions are how you do ordinary work.
// Here they are the escape hatch for the case the document model does not
// cover -- and reaching for it often is the signal to reconsider the model,
// or to ask whether the data was relational all along.
