"""Experiment 11 — One-to-one, one-to-many and many-to-many."""
import mongomock
from fixtures import fresh_db


def one_to_one_embed():
    db = mongomock.MongoClient().collegeDB
    db.people.insert_one({"_id": 21, "name": "Asha Kumari",
                          "address": {"city": "Vijayawada", "state": "AP",
                                      "pin": "520010"}})

    doc = db.people.find_one({"_id": 21})
    assert doc["address"]["city"] == "Vijayawada", "one read, no join"
    assert [d["name"] for d in db.people.find({"address.pin": "520010"})] \
        == ["Asha Kumari"], "and it is still queryable"

    print("  1-to-1: EMBED. One read; the sub-document is still queryable by dot")


def one_to_few_embed_array():
    db = mongomock.MongoClient().collegeDB
    db.people.insert_one({"_id": 21, "name": "Asha",
                          "phones": ["9876543210", "9876543211"]})

    assert len(db.people.find_one({"_id": 21})["phones"]) == 2
    assert [d["_id"] for d in db.people.find({"phones": "9876543210"})] == [21], \
        "any element matches"

    print("  1-to-few: embed as an ARRAY -- bounded, so no 16 MB risk")


def one_to_many_reference_from_child():
    """The array must NOT live on the parent: it is unbounded."""
    db = fresh_db()

    # The CHILD holds the parent's id.
    for e in db.enrollments.find({"course_id": "DSC301"}):
        assert "course_id" in e

    got = sorted(e["student_id"] for e in db.enrollments.find({"course_id": "DSC301"}))
    assert got == [21, 22], got

    # Adding a thousand enrolments does not grow the course document at all.
    before = len(str(db.courses.find_one({"_id": "DSC301"})))
    db.enrollments.insert_many([{"course_id": "DSC301", "student_id": 1000 + i,
                                 "grade": "B"} for i in range(1000)])
    after = len(str(db.courses.find_one({"_id": "DSC301"})))
    assert before == after, "the COURSE document is unchanged -- that is the point"
    assert db.enrollments.count_documents({"course_id": "DSC301"}) == 1002

    print(f"  1-to-many: reference from the CHILD. 1000 more enrolments left the")
    print(f"       course document at {after} chars -- an embedded array would")
    print(f"       have grown it, and eventually breached 16 MB")


def many_to_many_both_ways():
    db = fresh_db()

    # Option A: an array of ids on the student
    db.students.update_one({"_id": 21},
                           {"$set": {"course_ids": ["DSC301", "STA302"]}})
    assert [d["name"] for d in db.students.find({"course_ids": "DSC301"})] == ["Asha"]

    # Option C: the junction collection -- queryable from BOTH directions
    hers = sorted(e["course_id"] for e in db.enrollments.find({"student_id": 21}))
    assert hers == ["DSC301", "STA302"], hers

    theirs = sorted(e["student_id"] for e in db.enrollments.find({"course_id": "DSC301"}))
    assert theirs == [21, 22], theirs

    print(f"  M-to-M: student 21 takes {hers}; DSC301 has students {theirs}")


def the_junction_carries_the_relationship_attributes():
    """Why option C wins when the relationship has its own data."""
    db = fresh_db()

    e = db.enrollments.find_one({"student_id": 21, "course_id": "DSC301"})
    assert e["grade"] == "A"

    # The grade belongs to NEITHER entity:
    assert "grade" not in db.students.find_one({"_id": 21})
    assert "grade" not in db.courses.find_one({"_id": "DSC301"})

    # An array of ids could not hold it.
    db.students.update_one({"_id": 21}, {"$set": {"course_ids": ["DSC301"]}})
    s = db.students.find_one({"_id": 21})
    assert s["course_ids"] == ["DSC301"], "just an id -- nowhere to put the grade"

    print("  the GRADE lives on the enrolment, not on the student or the course")
    print("       -- exactly the reasoning that produces a junction TABLE in")
    print("       Course 5, and it survives the translation unchanged")


def main():
    print("Experiment 11 -- Modelling relationships")
    one_to_one_embed()
    one_to_few_embed_array()
    one_to_many_reference_from_child()
    many_to_many_both_ways()
    the_junction_carries_the_relationship_attributes()


if __name__ == "__main__":
    main()
