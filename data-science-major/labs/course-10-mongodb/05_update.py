"""Experiment 5 — Update operators."""
from fixtures import fresh_db, names


def set_unset_inc_rename():
    db = fresh_db()

    db.students.update_one({"_id": 21}, {"$set": {"age": 21}})
    assert db.students.find_one({"_id": 21})["age"] == 21

    db.students.update_one({"_id": 21}, {"$set": {"marks.python": 85}})
    assert db.students.find_one({"_id": 21})["marks"]["python"] == 85, \
        "$set creates a nested field"

    r = db.students.update_many({"dept": "DS"}, {"$inc": {"marks.maths": 5}})
    assert r.modified_count == 3
    assert db.students.find_one({"_id": 21})["marks"]["maths"] == 93

    db.students.update_one({"_id": 21}, {"$inc": {"age": -1}})
    assert db.students.find_one({"_id": 21})["age"] == 20, "a negative $inc subtracts"

    db.students.update_one({"_id": 21}, {"$unset": {"active": ""}})
    assert "active" not in db.students.find_one({"_id": 21}), \
        "$unset REMOVES the field; its value is ignored"

    db.students.update_many({}, {"$rename": {"dept": "department"}})
    doc = db.students.find_one({"_id": 22})
    assert "department" in doc and "dept" not in doc

    print("  $set (incl. nested), $inc (incl. negative), $unset, $rename")


def several_operators_at_once():
    db = fresh_db()
    db.students.update_one({"_id": 22}, {
        "$set":   {"grade": "B"},
        "$inc":   {"age": 1},
        "$unset": {"active": ""}})
    d = db.students.find_one({"_id": 22})
    assert d["grade"] == "B" and d["age"] == 22 and "active" not in d
    print("  several operators combine in one update document")


def update_one_changes_exactly_one():
    """The commonest CRUD mistake: silent, and it reports success."""
    db = fresh_db()
    assert db.students.count_documents({"dept": "DS"}) == 3

    r = db.students.update_one({"dept": "DS"}, {"$set": {"flag": True}})
    assert r.modified_count == 1, "ONE, even though three matched"
    assert db.students.count_documents({"flag": True}) == 1

    db2 = fresh_db()
    r2 = db2.students.update_many({"dept": "DS"}, {"$set": {"flag": True}})
    assert r2.modified_count == 3
    assert db2.students.count_documents({"flag": True}) == 3

    print("  updateOne -> modifiedCount 1 of 3 matches; updateMany -> 3")
    print("       the command SUCCEEDS either way -- nothing warns you")


def replace_one_destroys_everything():
    db = fresh_db()
    before = db.students.find_one({"_id": 21})
    assert set(before) >= {"name", "dept", "marks", "subjects", "age", "active"}

    db.students.replace_one({"_id": 21}, {"name": "Asha K"})
    after = db.students.find_one({"_id": 21})

    assert set(after) == {"_id", "name"}, f"only _id and name survive: {set(after)}"
    assert after["name"] == "Asha K"

    # updateOne with $set preserves the rest.
    db2 = fresh_db()
    db2.students.update_one({"_id": 21}, {"$set": {"name": "Asha K"}})
    kept = db2.students.find_one({"_id": 21})
    assert "marks" in kept and "subjects" in kept and kept["name"] == "Asha K"

    print("  replaceOne left only {_id, name}; updateOne+$set kept everything")


def upsert_is_atomic():
    db = fresh_db()

    # First call: inserts.
    r = db.counters.update_one({"_id": "visits"},
                               {"$inc": {"count": 1},
                                "$setOnInsert": {"created": "2026-08-26"}},
                               upsert=True)
    assert r.upserted_id == "visits"
    assert db.counters.find_one({"_id": "visits"})["count"] == 1

    # Later calls: update, and $setOnInsert does NOT re-apply.
    for _ in range(4):
        db.counters.update_one({"_id": "visits"},
                               {"$inc": {"count": 1},
                                "$setOnInsert": {"created": "LATER"}},
                               upsert=True)
    doc = db.counters.find_one({"_id": "visits"})
    assert doc["count"] == 5
    assert doc["created"] == "2026-08-26", "$setOnInsert applies ONLY on insert"

    print("  upsert: inserted then incremented to 5; $setOnInsert applied once")


def find_one_and_update():
    db = fresh_db()
    from pymongo import ReturnDocument

    after = db.students.find_one_and_update(
        {"_id": 21}, {"$set": {"age": 22}},
        return_document=ReturnDocument.AFTER)
    assert after["age"] == 22, "returnDocument: 'after' gives the NEW document"

    db2 = fresh_db()
    before = db2.students.find_one_and_update({"_id": 21}, {"$set": {"age": 22}})
    assert before["age"] == 20, "the default returns the document BEFORE the update"

    print("  findOneAndUpdate returns the OLD document by default, or the new one")


def main():
    print("Experiment 5 -- Updating documents")
    set_unset_inc_rename()
    several_operators_at_once()
    update_one_changes_exactly_one()
    replace_one_destroys_everything()
    upsert_is_atomic()
    find_one_and_update()


if __name__ == "__main__":
    main()
