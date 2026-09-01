"""Experiment 4 — Logical operators."""
from fixtures import fresh_db, names


def implicit_and_explicit():
    db = fresh_db()

    implicit = names(db.students.find({"dept": "DS", "age": {"$lt": 22}}))
    explicit = names(db.students.find(
        {"$and": [{"dept": "DS"}, {"age": {"$lt": 22}}]}))
    assert implicit == explicit == ["Asha", "Ravi"], implicit

    # $and is REQUIRED for two conditions on the same field expressed
    # as separate clauses.
    both = names(db.students.find(
        {"$and": [{"age": {"$gte": 20}}, {"age": {"$lte": 21}}]}))
    assert both == ["Asha", "Bhanu", "Meena", "Ravi"], both

    print("  implicit AND == explicit $and; $and needed for same-field clauses")


def or_operator():
    db = fresh_db()
    got = names(db.students.find(
        {"$or": [{"dept": "Stats"}, {"marks.maths": {"$gt": 85}}]}))
    assert got == ["Asha", "Bhanu", "Meena"], got
    print(f"  $or (Stats OR maths>85) -> {got}")


def nor_is_de_morgan():
    db = fresh_db()

    nor = names(db.students.find({"$nor": [{"dept": "DS"}, {"age": 20}]}))
    assert nor == ["Bhanu"], nor

    # NOT(A OR B) == (NOT A) AND (NOT B) -- Course 1's De Morgan
    de_morgan = names(db.students.find(
        {"$and": [{"dept": {"$ne": "DS"}}, {"age": {"$ne": 20}}]}))
    assert nor == de_morgan, f"{nor} != {de_morgan}"

    print(f"  $nor [dept=DS, age=20] -> {nor}, identical to (NOT A) AND (NOT B)")


def not_needs_an_operator_expression():
    db = fresh_db()

    ok = names(db.students.find({"age": {"$not": {"$gt": 21}}}))
    assert ok == ["Asha", "Bhanu", "Meena", "Ravi"], ok

    # $not cannot take a plain value.
    try:
        list(db.students.find({"age": {"$not": 21}}))
        raise AssertionError("expected an error from $not with a plain value")
    except Exception as e:
        assert not isinstance(e, AssertionError), "should be a query error"

    print("  $not inverts an OPERATOR EXPRESSION; a plain value is an error")


def combining():
    db = fresh_db()

    got = names(db.students.find({
        "dept": "DS",
        "$or": [{"marks.maths": {"$gt": 80}}, {"marks.stats": {"$gt": 80}}]}))
    assert got == ["Asha"], got

    nested = names(db.students.find({
        "$and": [
            {"$or": [{"dept": "DS"}, {"dept": "Stats"}]},
            {"$or": [{"age": 20}, {"marks.maths": {"$gt": 70}}]},
        ]}))
    assert nested == ["Asha", "Kiran", "Meena"], nested

    print(f"  nested $and/$or -> {nested}")


def main():
    print("Experiment 4 -- Logical operators")
    implicit_and_explicit()
    or_operator()
    nor_is_de_morgan()
    not_needs_an_operator_expression()
    combining()


if __name__ == "__main__":
    main()
