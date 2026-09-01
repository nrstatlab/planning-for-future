"""Experiment 6 — Deleting documents."""
from fixtures import fresh_db, names, STUDENTS


def delete_one_and_many():
    db = fresh_db()
    assert db.students.count_documents({}) == 5

    r = db.students.delete_one({"_id": 25})
    assert r.deleted_count == 1 and db.students.count_documents({}) == 4

    r = db.students.delete_one({"dept": "DS"})
    assert r.deleted_count == 1, "ONE, even though three match"
    assert db.students.count_documents({"dept": "DS"}) == 2

    r = db.students.delete_many({"dept": "DS"})
    assert r.deleted_count == 2 and db.students.count_documents({"dept": "DS"}) == 0

    print("  deleteOne removes ONE of three matches; deleteMany removes all")


def find_one_and_delete():
    db = fresh_db()
    doc = db.students.find_one_and_delete({"_id": 21})
    assert doc["name"] == "Asha", "it RETURNS the deleted document"
    assert db.students.find_one({"_id": 21}) is None
    print("  findOneAndDelete returns the document it removed")


def delete_all_versus_drop():
    """deleteMany({}) empties the collection; drop() removes it entirely."""
    db = fresh_db()
    db.students.create_index("dept")
    before_indexes = len(list(db.students.list_indexes()))
    assert before_indexes >= 2, "_id plus the one we made"

    db.students.delete_many({})
    assert db.students.count_documents({}) == 0
    assert "students" in db.list_collection_names(), "the COLLECTION remains"
    assert len(list(db.students.list_indexes())) == before_indexes, \
        "and so do its INDEXES"

    db2 = fresh_db()
    db2.students.create_index("dept")
    db2.students.drop()
    assert "students" not in db2.list_collection_names(), "gone entirely"

    print(f"  deleteMany({{}}): 0 documents, collection and {before_indexes} indexes kept")
    print(f"  drop(): the collection, its documents and its indexes all removed")


def no_confirmation_no_undo():
    """A deliberate demonstration of how easy the mistake is."""
    db = fresh_db()
    intended = {"dept": "Physics"}          # matches nothing
    typo = {}                               # what a slip produces

    r_safe = db.students.delete_many(intended)
    assert r_safe.deleted_count == 0 and db.students.count_documents({}) == 5

    r_oops = db.students.delete_many(typo)
    assert r_oops.deleted_count == 5, "an empty filter matched EVERYTHING"
    assert db.students.count_documents({}) == 0

    print("  an empty filter deleted all 5 documents, reported success, and")
    print("       there is no transaction to roll back -- unlike Course 5")


def main():
    print("Experiment 6 -- Deleting documents")
    delete_one_and_many()
    find_one_and_delete()
    delete_all_versus_drop()
    no_confirmation_no_undo()


if __name__ == "__main__":
    main()
