// Experiment 20 -- Case study: a library management system.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 20_case_study.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)
//
// The schema is the one designed in practice.md Section C question 1. Read
// that answer first: it justifies every embed and every reference, and this
// script only implements it.

use libraryDB
db.books.drop(); db.members.drop(); db.loans.drop()

// =============================================================================
// Step 1: Seed the books and members
// 1. SEED
// =============================================================================
db.books.insertMany([
  { _id: "978-1491954461", title: "MongoDB: The Definitive Guide",
    authors: ["Shannon Bradshaw", "Kristina Chodorow"],
    publisher: { name: "O'Reilly", year: 2019 },
    subjects: ["databases", "nosql"], totalCopies: 5, availableCopies: 5 },
  { _id: "978-0134685991", title: "Effective Java",
    authors: ["Joshua Bloch"], publisher: { name: "Addison-Wesley", year: 2018 },
    subjects: ["programming", "java"], totalCopies: 2, availableCopies: 2 },
  { _id: "978-1449355739", title: "Learning Python",
    authors: ["Mark Lutz"], publisher: { name: "O'Reilly", year: 2013 },
    subjects: ["programming", "python"], totalCopies: 3, availableCopies: 3 }
])

db.members.insertMany([
  { _id: "M2026001", name: "Asha Kumari", email: "asha@nri.ac.in",
    phones: ["9876543210"],
    address: { city: "Vijayawada", state: "AP", pin: "520010" },
    joined: ISODate("2026-07-01"), active: true, currentLoanCount: 0 },
  { _id: "M2026002", name: "Ravi Teja", email: "ravi@nri.ac.in",
    phones: ["9876500000"],
    address: { city: "Guntur", state: "AP", pin: "522002" },
    joined: ISODate("2026-07-05"), active: true, currentLoanCount: 0 }
])

// =============================================================================
// Step 2: Create the indexes
// 2. INDEXES -- practice.md Step 4
// =============================================================================
db.books.createIndex({ title: "text", authors: "text" })
db.books.createIndex({ subjects: 1 })                 // multikey
db.loans.createIndex({ member_id: 1, returned: 1 })   // query 2
db.loans.createIndex({ returned: 1, due: 1 })         // query 4, ESR
db.loans.createIndex({ isbn: 1, issued: -1 })         // query 5
db.members.createIndex({ email: 1 }, { unique: true })

// =============================================================================
// Step 3: Issue books, with a conditional decrement
// 3. ISSUE -- two writes, and a CONDITIONAL decrement
// =============================================================================
// A fixed "today", as in 20_case_study.py, so that a loan can be late.
const TODAY = ISODate("2026-08-26")
const DAY = 24 * 60 * 60 * 1000
// [Changed: TODAY was added, and issue() takes the day. Every loan was issued
// at new Date(), the moment the script ran, so no return could ever be late and
// the overdue report could never find anything.]

function issue(memberId, isbn, on = TODAY) {
  const book   = db.books.findOne({ _id: isbn })
  const member = db.members.findOne({ _id: memberId })

  // The guard is IN THE FILTER, not in an if. Checking availableCopies > 0 and
  // then decrementing is two operations, and two concurrent borrowers both
  // pass the check. This is one operation, so only one of them can match.
  const dec = db.books.updateOne({ _id: isbn, availableCopies: { $gt: 0 } },
                                 { $inc: { availableCopies: -1 } })
  if (dec.modifiedCount === 0) return { ok: false, why: "no copies available" }

  const issued = on
  const due    = new Date(issued.getTime() + 14 * 24 * 60 * 60 * 1000)
  db.loans.insertOne({
    member_id: memberId, isbn,
    book_title:  book.title,      // EXTENDED REFERENCE -- practice.md Step 3
    member_name: member.name,
    issued, due, returned: null, fine: 0 })
  db.members.updateOne({ _id: memberId }, { $inc: { currentLoanCount: 1 } })
  return { ok: true }
}

issue("M2026001", "978-1491954461")
issue("M2026001", "978-0134685991")
issue("M2026002", "978-0134685991")
issue("M2026002", "978-1449355739")

// The third copy of a two-copy book:
issue("M2026001", "978-0134685991")     // -> { ok: false, why: "no copies available" }

// =============================================================================
// Step 4: Return them, and charge the fines
// 4. RETURN -- set returned, compute the fine, put the copy back
// =============================================================================
function returnBook(memberId, isbn, on) {
  const loan = db.loans.findOne({ member_id: memberId, isbn, returned: null })
  if (!loan) return { ok: false, why: "no open loan" }

  const daysLate = Math.max(0, Math.ceil((on - loan.due) / (24 * 60 * 60 * 1000)))
  const fine = daysLate * 2                      // Rs 2 per day

  db.loans.updateOne({ _id: loan._id }, { $set: { returned: on, fine } })
  db.books.updateOne({ _id: isbn }, { $inc: { availableCopies: 1 } })
  db.members.updateOne({ _id: memberId }, { $inc: { currentLoanCount: -1 } })
  return { ok: true, daysLate, fine }
}

returnBook("M2026002", "978-1449355739", new Date(TODAY.getTime() + 10 * DAY))   // day 10 of 14
returnBook("M2026002", "978-0134685991", new Date(TODAY.getTime() + 20 * DAY))   // day 20: 6 late
returnBook("M2026002", "978-0134685991", new Date(TODAY.getTime() + 21 * DAY))   // again: refused
// [Changed: the return was at new Date(); the late return and the second
// return, which 20_case_study.py asserts, were added.]

// =============================================================================
// Step 5: Run the five reports
// 5. THE FIVE QUERIES -- practice.md Step 5
// =============================================================================
// 1. availability
db.books.findOne({ _id: "978-1491954461" }, { title: 1, availableCopies: 1 })

// 2. a member's current loans
db.loans.find({ member_id: "M2026001", returned: null })

// 4. overdue -- the extended reference pays for itself here: no $lookup
const asAt = new Date(TODAY.getTime() + 20 * DAY)     // overdue as at day 20
db.loans.find({ returned: null, due: { $lt: asAt } }).sort({ due: 1 })
// [Corrected: the .sort(...) began its own line. Typed into mongosh, a line that
// starts with a dot does not continue the one above -- the shell ran the
// find(), unsorted, without it, then rejected ".sort(...)" as an invalid command.]

// 5. most borrowed -- $match FIRST
db.loans.aggregate([
  { $match:  { issued: { $gte: ISODate("2026-01-01") } } },
  { $group:  { _id: "$isbn", title: { $first: "$book_title" },
               times: { $sum: 1 } } },
  { $sort:   { times: -1, _id: 1 } },
  { $limit:  10 }
])

// subject report -- multikey + $unwind
db.books.aggregate([
  { $unwind: "$subjects" },
  { $group:  { _id: "$subjects", titles: { $push: "$title" },
               n: { $sum: 1 } } },
  { $sort:   { n: -1, _id: 1 } }
])

// =============================================================================
// Step 6: Check the stock counts against the loans
// 6. THE INTEGRITY CHECK -- the point of the whole experiment
// =============================================================================
// availableCopies is the COMPUTED pattern: it makes query 1 constant-time and
// introduces a number that can DRIFT. The only defence is to check it.
db.books.aggregate([
  { $lookup: {
      from: "loans", localField: "_id", foreignField: "isbn", as: "loans" } },
  { $project: {
      title: 1, totalCopies: 1, availableCopies: 1,
      out: { $size: { $filter: { input: "$loans", as: "l",
                                 cond: { $eq: ["$$l.returned", null] } } } } } },
  { $addFields: { expected: { $subtract: ["$totalCopies", "$out"] } } },
  { $match: { $expr: { $ne: ["$availableCopies", "$expected"] } } }
])
// This should return NOTHING. Anything it returns is a book whose stored count
// disagrees with its open loans -- run it nightly, and alert on any row.
