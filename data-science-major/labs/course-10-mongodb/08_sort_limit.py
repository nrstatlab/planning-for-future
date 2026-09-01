"""Experiment 8 — Sorting, limiting and skipping."""
from fixtures import fresh_db


def sorting():
    db = fresh_db()

    desc = [d["name"] for d in db.students.find().sort("marks.maths", -1)]
    assert desc == ["Meena", "Asha", "Kiran", "Ravi", "Bhanu"], desc

    asc = [d["name"] for d in db.students.find().sort("marks.maths", 1)]
    assert asc == list(reversed(desc))

    multi = [(d["dept"], d["marks"]["maths"])
             for d in db.students.find().sort([("dept", 1), ("marks.maths", -1)])]
    assert multi == [("DS", 88), ("DS", 71), ("DS", 65),
                     ("Stats", 94), ("Stats", 52)], multi

    print(f"  sort by maths desc -> {desc}")
    print(f"  multi-key sort (dept asc, maths desc) groups then orders within")


def limit_and_skip():
    db = fresh_db()

    top3 = [d["name"] for d in db.students.find().sort("marks.maths", -1).limit(3)]
    assert top3 == ["Meena", "Asha", "Kiran"]

    page2 = [d["name"] for d in db.students.find().sort("_id", 1).skip(2).limit(2)]
    assert page2 == ["Meena", "Kiran"], page2

    print(f"  top 3 by maths: {top3}; page 2 by _id: {page2}")


def order_is_fixed():
    """sort, then skip, then limit -- whatever order you chain them."""
    db = fresh_db()

    a = [d["name"] for d in db.students.find().sort("marks.maths", -1).limit(3)]
    b = [d["name"] for d in db.students.find().limit(3).sort("marks.maths", -1)]
    assert a == b == ["Meena", "Asha", "Kiran"], (a, b)

    print("  .limit(3).sort(...) == .sort(...).limit(3) -- the server decides")
    print("       it sorts EVERYTHING and then takes three, not the reverse")


def range_pagination_beats_skip():
    db = fresh_db()

    # skip-based
    p1 = list(db.students.find().sort("_id", 1).limit(2))
    p2 = list(db.students.find().sort("_id", 1).skip(2).limit(2))
    p3 = list(db.students.find().sort("_id", 1).skip(4).limit(2))

    # range-based: remember the last _id seen
    r1 = list(db.students.find().sort("_id", 1).limit(2))
    r2 = list(db.students.find({"_id": {"$gt": r1[-1]["_id"]}})
                         .sort("_id", 1).limit(2))
    r3 = list(db.students.find({"_id": {"$gt": r2[-1]["_id"]}})
                         .sort("_id", 1).limit(2))

    for skip_page, range_page in [(p1, r1), (p2, r2), (p3, r3)]:
        assert [d["_id"] for d in skip_page] == [d["_id"] for d in range_page]

    print("  range pagination gives IDENTICAL pages, and every page costs the")
    print("       same -- skip(100000) would walk and discard 100,000 documents")


def cursor_versus_document():
    db = fresh_db()

    cursor = db.students.find({"_id": 21})
    assert not hasattr(cursor, "get"), "find() gives a CURSOR"
    assert list(cursor)[0]["name"] == "Asha"

    doc = db.students.find_one({"_id": 21})
    assert doc["name"] == "Asha", "findOne gives the DOCUMENT"

    print("  find() -> a cursor (iterate it); findOne() -> a document or None")


def main():
    print("Experiment 8 -- Sorting, limiting, skipping")
    sorting()
    limit_and_skip()
    order_is_fixed()
    range_pagination_beats_skip()
    cursor_versus_document()


if __name__ == "__main__":
    main()
