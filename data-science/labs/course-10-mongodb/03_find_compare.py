"""Experiment 3 — find() and the comparison operators."""
from fixtures import fresh_db, names


def equality_and_findone():
    db = fresh_db()
    assert names(db.students.find({"dept": "DS"})) == ["Asha", "Kiran", "Ravi"]
    assert names(db.students.find({"dept": "DS", "age": 20})) == ["Asha"]

    one = db.students.find_one({"_id": 21})
    assert one["name"] == "Asha"
    assert db.students.find_one({"_id": 999}) is None, "findOne returns null"

    print("  equality, implicit AND, findOne -> a document or None")


def comparison_operators():
    db = fresh_db()
    cases = {
        "$gt 20":  ({"age": {"$gt": 20}},  ["Bhanu", "Kiran", "Ravi"]),
        "$gte 21": ({"age": {"$gte": 21}}, ["Bhanu", "Kiran", "Ravi"]),
        "$lt 21":  ({"age": {"$lt": 21}},  ["Asha", "Meena"]),
        "$lte 20": ({"age": {"$lte": 20}}, ["Asha", "Meena"]),
        "$ne 20":  ({"age": {"$ne": 20}},  ["Bhanu", "Kiran", "Ravi"]),
        "$in":     ({"dept": {"$in": ["DS", "CS"]}}, ["Asha", "Kiran", "Ravi"]),
        "$nin":    ({"dept": {"$nin": ["Stats"]}},   ["Asha", "Kiran", "Ravi"]),
    }
    for label, (q, want) in cases.items():
        got = names(db.students.find(q))
        assert got == want, f"{label}: {got} != {want}"

    print(f"  all seven comparison operators verified")


def a_range_is_one_object():
    """Written as two keys, the first is silently discarded."""
    db = fresh_db()

    correct = names(db.students.find({"age": {"$gte": 20, "$lte": 21}}))
    assert correct == ["Asha", "Bhanu", "Meena", "Ravi"], correct

    # In Python a dict literal with a duplicate key keeps the LAST -- the same
    # silent overwrite JavaScript performs. Only $lte survives.
    wrong = names(db.students.find({"age": {"$gte": 20}, "age": {"$lte": 21}}))
    assert wrong == ["Asha", "Bhanu", "Meena", "Ravi"] or "Kiran" not in wrong
    assert names(db.students.find({"age": {"$lte": 21}})) == wrong, \
        "only the LAST condition survived -- the $gte vanished"

    print("  a range must be ONE object; two keys silently drops one condition")


def dot_notation():
    db = fresh_db()
    assert names(db.students.find({"marks.maths": {"$gte": 90}})) == ["Meena"]
    assert names(db.students.find({"marks.maths": {"$gt": 60, "$lt": 90}})) == \
        ["Asha", "Kiran", "Ravi"]
    print("  dot notation reaches into sub-documents")


def ne_matches_missing_fields():
    """The trap: 'not equal to DS' is true of a field that does not exist."""
    db = fresh_db()
    db.students.insert_one({"_id": 26, "name": "NoDept"})

    loose = names(db.students.find({"dept": {"$ne": "DS"}}))
    assert "NoDept" in loose, "$ne ALSO matched the document with no dept"
    assert loose == ["Bhanu", "Meena", "NoDept"], loose

    tight = names(db.students.find({"dept": {"$ne": "DS", "$exists": True}}))
    assert tight == ["Bhanu", "Meena"], tight

    print("  $ne matched the document with NO dept field at all --")
    print("       combine with $exists: true when that matters")


def counting_and_distinct():
    db = fresh_db()
    assert db.students.count_documents({}) == 5
    assert db.students.count_documents({"dept": "DS"}) == 3
    assert sorted(db.students.distinct("dept")) == ["DS", "Stats"]
    assert sorted(db.students.distinct("subjects")) == ["DS", "Python", "R", "Stats"], \
        "distinct flattens ARRAY values"
    print("  distinct on an array field flattens it: DS, Python, R, Stats")


def main():
    print("Experiment 3 -- find() and comparison operators")
    equality_and_findone()
    comparison_operators()
    a_range_is_one_object()
    dot_notation()
    ne_matches_missing_fields()
    counting_and_distinct()


if __name__ == "__main__":
    main()
