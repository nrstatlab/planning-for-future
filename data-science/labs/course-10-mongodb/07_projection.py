"""Experiment 7 — Projection."""
from fixtures import fresh_db


def inclusion_and_exclusion():
    db = fresh_db()

    d = db.students.find_one({"_id": 21}, {"name": 1, "dept": 1})
    assert set(d) == {"_id", "name", "dept"}, "_id is included BY DEFAULT"

    d = db.students.find_one({"_id": 21}, {"name": 1, "_id": 0})
    assert set(d) == {"name"}

    d = db.students.find_one({"_id": 21}, {"marks": 0, "subjects": 0})
    assert "marks" not in d and "subjects" not in d
    assert {"name", "dept", "age", "active", "_id"} <= set(d)

    print("  inclusion adds _id automatically; exclusion keeps everything else")


def cannot_mix():
    db = fresh_db()
    try:
        list(db.students.find({}, {"name": 1, "dept": 0}))
        raise AssertionError("expected an error from mixing inclusion/exclusion")
    except Exception as e:
        assert not isinstance(e, AssertionError)

    # _id is the ONE exception.
    d = db.students.find_one({"_id": 21}, {"name": 1, "_id": 0})
    assert set(d) == {"name"}

    print("  mixing inclusion and exclusion raises; _id is the one exception")


def nested_projection():
    db = fresh_db()
    d = db.students.find_one({"_id": 21}, {"marks.maths": 1, "_id": 0})
    assert d == {"marks": {"maths": 88}}, d
    print("  'marks.maths': 1 keeps the sub-document with only that field")


def array_projection():
    db = fresh_db()

    d = db.students.find_one({"_id": 21}, {"subjects": {"$slice": 2}, "_id": 0,
                                           "name": 1})
    assert d["subjects"] == ["DS", "Stats"], "the first 2"

    d = db.students.find_one({"_id": 21}, {"subjects": {"$slice": -1}, "_id": 0,
                                           "name": 1})
    assert d["subjects"] == ["Python"], "a negative slice takes from the END"

    print("  $slice: 2 -> first two; $slice: -1 -> the last one")


def projection_reduces_work():
    """Not just cosmetic -- fewer bytes read and sent."""
    db = fresh_db()
    full = db.students.find_one({"_id": 21})
    thin = db.students.find_one({"_id": 21}, {"name": 1, "_id": 0})

    assert len(str(full)) > 3 * len(str(thin)), \
        "the projected document is a fraction of the size"

    print(f"  full document {len(str(full))} chars vs projected {len(str(thin))}")
    print(f"       and a projection fully covered by an index needs no document read")


def main():
    print("Experiment 7 -- Projection")
    inclusion_and_exclusion()
    cannot_mix()
    nested_projection()
    array_projection()
    projection_reduces_work()


if __name__ == "__main__":
    main()
