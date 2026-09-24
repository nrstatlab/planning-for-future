"""Experiment 13 — Single-field and compound indexes.

mongomock records indexes but does not report IXSCAN, so this script asserts
that indexes are CREATED and ENFORCED correctly, and demonstrates the prefix
rule and ESR as tables. Run explain("executionStats") on a real server to see
the plan.
"""
import mongomock
from pymongo.errors import DuplicateKeyError
from fixtures import fresh_db


def creating_and_listing():
    db = fresh_db()
    db.students.create_index("dept")
    db.students.create_index([("dept", 1), ("marks.maths", -1)])
    db.students.create_index("age", name="age_idx")

    names = {i["name"] for i in db.students.list_indexes()}
    assert "_id_" in names, "_id is indexed AUTOMATICALLY"
    assert "dept_1" in names
    assert "age_idx" in names, "a custom name"
    assert any("marks.maths" in n for n in names), names

    db.students.drop_index("dept_1")
    assert "dept_1" not in {i["name"] for i in db.students.list_indexes()}

    print(f"  created and listed {len(names)} indexes, including the automatic _id")


def unique_is_enforced():
    db = fresh_db()
    db.students.create_index("name", unique=True)

    try:
        db.students.insert_one({"_id": 99, "name": "Asha"})
        raise AssertionError("expected a DuplicateKeyError")
    except DuplicateKeyError:
        pass

    db.students.insert_one({"_id": 99, "name": "Unique Name"})
    assert db.students.count_documents({}) == 6

    print("  a unique index rejected a duplicate name and accepted a new one")


def unique_and_missing_fields():
    """A missing field indexes as null, and two nulls collide."""
    db = mongomock.MongoClient().collegeDB
    db.people.create_index("email", unique=True)

    db.people.insert_one({"_id": 1, "name": "A"})          # no email -> null
    try:
        db.people.insert_one({"_id": 2, "name": "B"})      # also null
        raise AssertionError("expected a DuplicateKeyError from two nulls")
    except DuplicateKeyError:
        pass

    print("  a unique index allowed ONE document with no email, then rejected")
    print("       the next -- a missing field indexes as null, and nulls collide")
    print("       fix: partialFilterExpression: { email: { $exists: true } }")


def the_prefix_rule():
    """An index on {a,b,c} serves left-hand PREFIXES only."""
    index = ["dept", "year", "cgpa"]
    cases = [
        (["dept"],                 True,  "a prefix"),
        (["dept", "year"],         True,  "a prefix"),
        (["dept", "year", "cgpa"], True,  "the whole index"),
        (["year"],                 False, "not a prefix -- COLLSCAN"),
        (["cgpa"],                 False, "not a prefix -- COLLSCAN"),
        (["year", "cgpa"],         False, "not a prefix -- COLLSCAN"),
    ]

    def is_prefix(fields):
        return index[:len(fields)] == fields

    print(f"  index {{{', '.join(index)}}}:")
    for fields, expected, why in cases:
        assert is_prefix(fields) == expected, (fields, expected)
        mark = "uses it " if expected else "does NOT"
        print(f"    query on {str(fields):28s} {mark}  ({why})")

    print("       the phone book, sorted by (surname, forename): finding every")
    print("       Kumari is fast; finding every Asha means reading the whole book")


def the_esr_rule():
    """Equality, Sort, Range."""
    query = {"equality": "dept", "sort": "age", "range": "marks.maths"}
    correct = ["dept", "age", "marks.maths"]
    wrong = ["dept", "marks.maths", "age"]

    assert correct.index("age") < correct.index("marks.maths"), \
        "the SORT field must come before the RANGE field"
    assert wrong.index("marks.maths") < wrong.index("age"), \
        "this ordering puts the range first, and the sort cannot use the index"

    print(f"  ESR: query is dept = 'DS', maths > 70, sorted by age")
    print(f"    correct: {{{', '.join(correct)}}}   E, S, R")
    print(f"    wrong:   {{{', '.join(wrong)}}}   the range leaves everything")
    print(f"             after it unordered, so the sort falls back to memory")


def covered_query_fields():
    """Every field in the filter AND the projection must be in the index."""
    index = {"dept", "name"}
    filt = {"dept"}
    proj_bad = {"dept", "name", "_id"}      # _id is returned BY DEFAULT
    proj_good = {"dept", "name"}            # with _id: 0

    assert not (filt | proj_bad) <= index, "_id is not in the index -- NOT covered"
    assert (filt | proj_good) <= index, "with _id: 0 it IS covered"

    print("  covered query needs filter + projection inside the index")
    print("       find({dept}, {dept:1, name:1})        NOT covered -- _id sneaks in")
    print("       find({dept}, {dept:1, name:1, _id:0}) COVERED, totalDocsExamined 0")


def what_indexes_cost():
    db = fresh_db()
    for field in ["dept", "age", "active", "name"]:
        db.students.create_index(field)
    n = len(list(db.students.list_indexes()))
    assert n == 5, f"4 plus _id, got {n}"

    print(f"  {n} indexes means every insert, update and delete maintains {n}")
    print(f"       B-trees. Index what you QUERY, not everything -- the limit")
    print(f"       is 64 per collection, and reaching it means something is wrong")


def main():
    print("Experiment 13 -- Indexes")
    creating_and_listing()
    unique_is_enforced()
    unique_and_missing_fields()
    the_prefix_rule()
    the_esr_rule()
    covered_query_fields()
    what_indexes_cost()


if __name__ == "__main__":
    main()
