"""Experiment 2 — Databases, collections, inserting documents.

Runs the same logic as 02_create_insert.js through mongomock and asserts it.
"""
import mongomock
from pymongo.errors import BulkWriteError, DuplicateKeyError
from fixtures import STUDENTS


def lazy_creation():
    """A database and a collection spring into existence on the first write."""
    client = mongomock.MongoClient()
    assert "collegeDB" not in client.list_database_names(), \
        "referencing a database does not create it"

    db = client.collegeDB
    assert "collegeDB" not in client.list_database_names(), \
        "nor does referencing it through the client"

    db.students.insert_one({"_id": 1, "name": "X"})
    assert "collegeDB" in client.list_database_names(), "NOW it exists"
    assert "students" in db.list_collection_names()

    print("  lazy creation: a database appears only after the first write")


def insert_one_and_many():
    db = mongomock.MongoClient().collegeDB

    r = db.students.insert_one(dict(STUDENTS[0]))
    assert r.inserted_id == 21
    assert db.students.count_documents({}) == 1

    r = db.students.insert_many([dict(d) for d in STUDENTS[1:]])
    assert r.inserted_ids == [22, 23, 24, 25]
    assert db.students.count_documents({}) == 5

    print(f"  insertOne -> insertedId 21; insertMany -> {r.inserted_ids}")


def ordered_stops_unordered_continues():
    """The examinable behaviour: ordered:true (the default) stops at the
    first error, so later documents are NEVER ATTEMPTED."""
    db = mongomock.MongoClient().collegeDB
    db.students.insert_many([dict(d) for d in STUDENTS])

    batch = [{"_id": 30, "name": "X"},
             {"_id": 21, "name": "DUPLICATE"},     # already exists
             {"_id": 31, "name": "Y"}]

    try:
        db.students.insert_many([dict(d) for d in batch])      # ordered=True
        raise AssertionError("expected a BulkWriteError")
    except BulkWriteError:
        pass

    assert db.students.count_documents({"_id": 30}) == 1, "inserted BEFORE the error"
    assert db.students.count_documents({"_id": 31}) == 0, \
        "NEVER ATTEMPTED -- ordered stops at the first failure"

    db2 = mongomock.MongoClient().collegeDB
    db2.students.insert_many([dict(d) for d in STUDENTS])
    try:
        db2.students.insert_many([dict(d) for d in batch], ordered=False)
        raise AssertionError("expected a BulkWriteError")
    except BulkWriteError:
        pass

    assert db2.students.count_documents({"_id": 30}) == 1
    assert db2.students.count_documents({"_id": 31}) == 1, \
        "unordered CONTINUES past the error"

    print("  ordered=True: 30 in, 21 fails, 31 never attempted")
    print("  ordered=False: 30 AND 31 in, only 21 fails")


def generated_object_id():
    db = mongomock.MongoClient().collegeDB
    r = db.students.insert_one({"name": "Devi", "dept": "Stats"})

    from bson import ObjectId
    assert isinstance(r.inserted_id, ObjectId)
    assert len(r.inserted_id.binary) == 12, "12 bytes"
    assert r.inserted_id.generation_time is not None, "it embeds its creation time"

    print(f"  omitting _id generates a 12-byte ObjectId carrying a timestamp")


def collection_management():
    db = mongomock.MongoClient().collegeDB
    db.students.insert_many([dict(d) for d in STUDENTS])

    assert db.students.count_documents({}) == 5
    assert db.students.count_documents({"dept": "DS"}) == 3
    assert sorted(db.students.distinct("dept")) == ["DS", "Stats"]

    db.students.drop()
    assert "students" not in db.list_collection_names()

    print("  countDocuments, distinct, drop -- all as documented")


def main():
    print("Experiment 2 -- Databases, collections, inserting")
    lazy_creation()
    insert_one_and_many()
    ordered_stops_unordered_continues()
    generated_object_id()
    collection_management()


if __name__ == "__main__":
    main()
