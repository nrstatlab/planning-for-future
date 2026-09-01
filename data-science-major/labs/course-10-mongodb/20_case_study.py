"""Experiment 20 — Case study: a library management system.

The schema is the one designed in practice.md Section C question 1, and this
runs the whole workflow against it: seed, issue, return, the five reports, and
the integrity check.

The integrity check is the point of the experiment. availableCopies is the
COMPUTED pattern -- it makes the availability lookup constant-time and
introduces a number that can drift out of step with the loans. So it is
asserted after every single write, not once at the end. When the last section
deliberately breaks it, the same check catches it.
"""
import datetime as dt

import mongomock

# This experiment does NOT use fixtures.py. The other nineteen share the
# collegeDB sample data; this one designs its own schema from scratch, which
# is the exercise.

DAY = dt.timedelta(days=1)
LOAN_DAYS = 14
FINE_PER_DAY = 2

BOOKS = [
    {"_id": "978-1491954461", "title": "MongoDB: The Definitive Guide",
     "authors": ["Shannon Bradshaw", "Kristina Chodorow"],
     "publisher": {"name": "O'Reilly", "year": 2019},
     "subjects": ["databases", "nosql"], "totalCopies": 5, "availableCopies": 5},
    {"_id": "978-0134685991", "title": "Effective Java",
     "authors": ["Joshua Bloch"],
     "publisher": {"name": "Addison-Wesley", "year": 2018},
     "subjects": ["programming", "java"], "totalCopies": 2, "availableCopies": 2},
    {"_id": "978-1449355739", "title": "Learning Python",
     "authors": ["Mark Lutz"], "publisher": {"name": "O'Reilly", "year": 2013},
     "subjects": ["programming", "python"], "totalCopies": 3, "availableCopies": 3},
]

MEMBERS = [
    {"_id": "M2026001", "name": "Asha Kumari", "email": "asha@nri.ac.in",
     "phones": ["9876543210"],
     "address": {"city": "Vijayawada", "state": "AP", "pin": "520010"},
     "joined": dt.datetime(2026, 7, 1), "active": True, "currentLoanCount": 0},
    {"_id": "M2026002", "name": "Ravi Teja", "email": "ravi@nri.ac.in",
     "phones": ["9876500000"],
     "address": {"city": "Guntur", "state": "AP", "pin": "522002"},
     "joined": dt.datetime(2026, 7, 5), "active": True, "currentLoanCount": 0},
]

# A fixed "today", so the overdue report is reproducible instead of drifting.
TODAY = dt.datetime(2026, 8, 26)


def seed():
    db = mongomock.MongoClient().libraryDB
    db.books.insert_many([dict(b) for b in BOOKS])
    db.members.insert_many([dict(m) for m in MEMBERS])
    db.books.create_index("subjects")
    db.loans.create_index([("member_id", 1), ("returned", 1)])
    db.loans.create_index([("returned", 1), ("due", 1)])
    db.loans.create_index([("isbn", 1), ("issued", -1)])
    db.members.create_index("email", unique=True)
    return db


# =============================================================================
# The two operations
# =============================================================================

def issue(db, member_id, isbn, on=TODAY):
    """Insert a loan and decrement the stored count -- CONDITIONALLY."""
    book = db.books.find_one({"_id": isbn})
    member = db.members.find_one({"_id": member_id})
    if book is None or member is None:
        return {"ok": False, "why": "unknown book or member"}

    # The guard lives IN THE FILTER. Reading availableCopies, testing it, then
    # decrementing is two operations: two concurrent borrowers both pass the
    # test and both decrement, and the count goes negative. One operation
    # cannot -- only one of them matches.
    dec = db.books.update_one({"_id": isbn, "availableCopies": {"$gt": 0}},
                              {"$inc": {"availableCopies": -1}})
    if dec.modified_count == 0:
        return {"ok": False, "why": "no copies available"}

    db.loans.insert_one({
        "member_id": member_id, "isbn": isbn,
        "book_title": book["title"],        # extended reference
        "member_name": member["name"],      # extended reference
        "issued": on, "due": on + LOAN_DAYS * DAY,
        "returned": None, "fine": 0})
    db.members.update_one({"_id": member_id},
                          {"$inc": {"currentLoanCount": 1}})
    return {"ok": True}


def return_book(db, member_id, isbn, on=TODAY):
    loan = db.loans.find_one({"member_id": member_id, "isbn": isbn,
                              "returned": None})
    if loan is None:
        return {"ok": False, "why": "no open loan"}

    days_late = max(0, (on - loan["due"]).days)
    fine = days_late * FINE_PER_DAY

    db.loans.update_one({"_id": loan["_id"]},
                        {"$set": {"returned": on, "fine": fine}})
    db.books.update_one({"_id": isbn}, {"$inc": {"availableCopies": 1}})
    db.members.update_one({"_id": member_id},
                          {"$inc": {"currentLoanCount": -1}})
    return {"ok": True, "daysLate": days_late, "fine": fine}


# =============================================================================
# The integrity check -- run after EVERY write
# =============================================================================

def drifted(db):
    """Books whose stored availableCopies disagrees with their open loans.

    Empty is the only acceptable answer. This is the whole reason the computed
    pattern is safe to use: it is cheap to verify, so verify it.
    """
    bad = []
    for b in db.books.find():
        out = db.loans.count_documents({"isbn": b["_id"], "returned": None})
        expected = b["totalCopies"] - out
        if b["availableCopies"] != expected:
            bad.append({"isbn": b["_id"], "title": b["title"],
                        "stored": b["availableCopies"], "expected": expected,
                        "openLoans": out})
    return bad


def members_drifted(db):
    """The same check for currentLoanCount -- a second computed field."""
    bad = []
    for m in db.members.find():
        out = db.loans.count_documents({"member_id": m["_id"], "returned": None})
        if m["currentLoanCount"] != out:
            bad.append({"member": m["_id"], "stored": m["currentLoanCount"],
                        "expected": out})
    return bad


def consistent(db, step):
    assert drifted(db) == [], (step, drifted(db))
    assert members_drifted(db) == [], (step, members_drifted(db))


# =============================================================================
# The workflow
# =============================================================================

def the_happy_path(db):
    consistent(db, "after seeding")

    assert issue(db, "M2026001", "978-1491954461")["ok"]
    consistent(db, "after issue 1")
    assert issue(db, "M2026001", "978-0134685991")["ok"]
    consistent(db, "after issue 2")
    assert issue(db, "M2026002", "978-0134685991")["ok"]
    consistent(db, "after issue 3")
    assert issue(db, "M2026002", "978-1449355739")["ok"]
    consistent(db, "after issue 4")

    assert db.books.find_one({"_id": "978-0134685991"})["availableCopies"] == 0
    assert db.members.find_one({"_id": "M2026001"})["currentLoanCount"] == 2
    assert db.loans.count_documents({"returned": None}) == 4

    print("  4 issues, and availableCopies / currentLoanCount agree with the")
    print("  loans collection after every single one:")
    for b in db.books.find().sort("_id", 1):
        print(f"    {b['title']:34s} {b['availableCopies']}/{b['totalCopies']} available")


def the_sixth_copy_of_a_five_copy_book(db):
    """The conditional decrement, and why it is not an if statement."""
    # Effective Java has 2 copies and both are out.
    before = db.books.find_one({"_id": "978-0134685991"})["availableCopies"]
    assert before == 0
    result = issue(db, "M2026001", "978-0134685991")

    assert result == {"ok": False, "why": "no copies available"}, result
    assert db.books.find_one({"_id": "978-0134685991"})["availableCopies"] == 0, \
        "the count must not go NEGATIVE"
    assert db.loans.count_documents({"isbn": "978-0134685991"}) == 2, \
        "and no loan row was written for the refused issue"
    consistent(db, "after a refused issue")

    print("  a third issue of a 2-copy book -> refused, count stayed at 0,")
    print("  no loan row written")
    print("       the guard is { _id: isbn, availableCopies: { $gt: 0 } } in the")
    print("       FILTER. As an if-then-decrement it is two operations, and two")
    print("       concurrent borrowers both pass the test. As one update, they")
    print("       cannot: the second one matches nothing")


def returning_on_time_and_late(db):
    # On time: issued TODAY, due TODAY+14, returned TODAY+10.
    on_time = return_book(db, "M2026002", "978-1449355739", TODAY + 10 * DAY)
    assert on_time == {"ok": True, "daysLate": 0, "fine": 0}, on_time
    consistent(db, "after an on-time return")
    assert db.books.find_one({"_id": "978-1449355739"})["availableCopies"] == 3

    # Late: returned TODAY+20, six days past the due date.
    late = return_book(db, "M2026002", "978-0134685991", TODAY + 20 * DAY)
    assert late == {"ok": True, "daysLate": 6, "fine": 12}, late
    assert 6 * FINE_PER_DAY == 12
    consistent(db, "after a late return")
    assert db.books.find_one({"_id": "978-0134685991"})["availableCopies"] == 1

    # Returning something not on loan changes nothing.
    again = return_book(db, "M2026002", "978-0134685991", TODAY + 21 * DAY)
    assert again == {"ok": False, "why": "no open loan"}, again
    consistent(db, "after a duplicate return")

    print("  returned day 10 of a 14-day loan -> 0 days late, fine 0")
    print("  returned day 20 of a 14-day loan -> 6 days late, fine Rs 12")
    print("  returning it a second time       -> refused, nothing changed")
    print("       that last one matters: without the returned: null in the")
    print("       filter, a double return increments availableCopies twice and")
    print("       the library thinks it owns a copy it does not have")


def the_five_reports(db):
    # 1. availability -- one document, no join
    b = db.books.find_one({"_id": "978-1491954461"},
                          {"title": 1, "availableCopies": 1})
    assert b == {"_id": "978-1491954461",
                 "title": "MongoDB: The Definitive Guide",
                 "availableCopies": 4}, b

    # 2. a member's open loans
    asha = list(db.loans.find({"member_id": "M2026001", "returned": None}))
    assert len(asha) == 2
    assert {l["isbn"] for l in asha} == {"978-1491954461", "978-0134685991"}

    # 4. overdue, as at TODAY + 20 days
    as_at = TODAY + 20 * DAY
    overdue = list(db.loans.find({"returned": None, "due": {"$lt": as_at}})
                   .sort("due", 1))
    assert len(overdue) == 2, overdue
    # The extended reference is what makes this report joinless.
    assert all("book_title" in l and "member_name" in l for l in overdue)
    assert {l["member_name"] for l in overdue} == {"Asha Kumari"}

    # 5. most borrowed
    top = list(db.loans.aggregate([
        {"$match": {"issued": {"$gte": dt.datetime(2026, 1, 1)}}},
        {"$group": {"_id": "$isbn", "title": {"$first": "$book_title"},
                    "times": {"$sum": 1}}},
        {"$sort": {"times": -1, "_id": 1}},
        {"$limit": 10}]))
    assert [(t["title"], t["times"]) for t in top] == [
        ("Effective Java", 2),
        ("Learning Python", 1),
        ("MongoDB: The Definitive Guide", 1)], top

    # subjects -- multikey plus $unwind
    subs = list(db.books.aggregate([
        {"$unwind": "$subjects"},
        {"$group": {"_id": "$subjects", "n": {"$sum": 1}}},
        {"$sort": {"n": -1, "_id": 1}}]))
    assert {s["_id"]: s["n"] for s in subs} == \
        {"programming": 2, "databases": 1, "java": 1, "nosql": 1, "python": 1}

    print(f"  1. availability   MongoDB Definitive Guide {b['availableCopies']}/5")
    print(f"  2. Asha's loans   {len(asha)} open")
    print(f"  4. overdue at {as_at.date()}  {len(overdue)}, both Asha's, no $lookup")
    print("  5. most borrowed  " +
          ", ".join(f"{t['title'].split(':')[0]} x{t['times']}" for t in top))
    print("       report 4 reads ONE collection because book_title and")
    print("       member_name were copied onto the loan -- the extended")
    print("       reference pattern paying for itself")


def when_it_drifts_the_check_catches_it(db):
    """Break it on purpose. A check that has never failed is not a check."""
    assert drifted(db) == []

    # Exactly the bug the transaction in practice.md Step 5 prevents: the loan
    # was written and the decrement was not.
    db.loans.insert_one({"member_id": "M2026002", "isbn": "978-1491954461",
                         "book_title": "MongoDB: The Definitive Guide",
                         "member_name": "Ravi Teja",
                         "issued": TODAY, "due": TODAY + LOAN_DAYS * DAY,
                         "returned": None, "fine": 0})

    bad = drifted(db)
    assert len(bad) == 1, bad
    assert bad[0]["isbn"] == "978-1491954461"
    assert bad[0]["stored"] == 4 and bad[0]["expected"] == 3, bad
    assert members_drifted(db) == [{"member": "M2026002",
                                    "stored": 0, "expected": 1}], \
        members_drifted(db)

    print("  a loan written with the decrement missing -- a half-done issue:")
    print(f"    {bad[0]['title']}: stored {bad[0]['stored']}, "
          f"expected {bad[0]['expected']} ({bad[0]['openLoans']} open loans)")
    print("    M2026002: currentLoanCount 0, expected 1")
    print("       nothing errored. The reports still ran. Only the check found")
    print("       it -- which is why it runs nightly, and why practice.md puts")
    print("       the two writes in a TRANSACTION in the first place")

    # Repair, and confirm.
    db.books.update_one({"_id": "978-1491954461"},
                        {"$inc": {"availableCopies": -1}})
    db.members.update_one({"_id": "M2026002"},
                          {"$inc": {"currentLoanCount": 1}})
    consistent(db, "after repair")
    print("  repaired, and both checks are clean again")


def main():
    print("Experiment 20 -- Library management case study")
    print("  schema: practice.md Section C question 1")
    # ONE database, carried through the whole workflow -- each stage builds on
    # the state the last one left, exactly as the real application would.
    db = seed()
    the_happy_path(db)
    the_sixth_copy_of_a_five_copy_book(db)
    returning_on_time_and_late(db)
    the_five_reports(db)
    when_it_drifts_the_check_catches_it(db)


if __name__ == "__main__":
    main()
