"""Experiment 9 — An embedded data model."""
import mongomock

DOCS = [
    {"_id": 21, "name": "Asha Kumari", "dept": "DS",
     "address": {"city": "Vijayawada", "state": "AP", "pin": "520010"},
     "enrollments": [
         {"course": "DSC301", "title": "Data Science with R", "grade": "A", "credits": 4},
         {"course": "STA302", "title": "Statistical Foundations", "grade": "B", "credits": 3}]},
    {"_id": 22, "name": "Ravi Teja", "dept": "DS",
     "address": {"city": "Guntur", "state": "AP", "pin": "522002"},
     "enrollments": [
         {"course": "DSC301", "title": "Data Science with R", "grade": "C", "credits": 4}]},
]


def db():
    d = mongomock.MongoClient().collegeDB
    d.embedded.insert_many([dict(x) for x in DOCS])
    return d


def one_read_gets_everything():
    d = db()
    doc = d.embedded.find_one({"_id": 21})
    assert doc["name"] == "Asha Kumari"
    assert doc["address"]["city"] == "Vijayawada"
    assert len(doc["enrollments"]) == 2
    assert doc["enrollments"][0]["title"] == "Data Science with R"

    print("  ONE read returned the student, the address and both enrolments")
    print("       -- no join anywhere, which is the point of embedding")


def querying_nested_and_arrays():
    d = db()
    assert [x["name"] for x in d.embedded.find({"address.city": "Vijayawada"})] \
        == ["Asha Kumari"]
    assert sorted(x["name"] for x in d.embedded.find({"enrollments.grade": "A"})) \
        == ["Asha Kumari"]
    assert sorted(x["name"] for x in d.embedded.find({"enrollments.course": "DSC301"})) \
        == ["Asha Kumari", "Ravi Teja"], "ANY element matches"
    print("  dot notation queries the embedded address and the enrolment array")


def elemmatch_is_required():
    """Two conditions on an array of sub-documents: different elements can
    satisfy different conditions unless you use $elemMatch."""
    d = db()
    # Ravi took DSC301 (grade C) and nothing with grade A -- so he should NOT
    # match "DSC301 with grade A".
    wrong = sorted(x["name"] for x in d.embedded.find(
        {"enrollments.course": "DSC301", "enrollments.grade": "A"}))
    right = sorted(x["name"] for x in d.embedded.find(
        {"enrollments": {"$elemMatch": {"course": "DSC301", "grade": "A"}}}))

    assert right == ["Asha Kumari"], right
    assert wrong == ["Asha Kumari"], wrong   # Ravi has no grade A at all

    # Now make the trap visible: give Ravi an A in a DIFFERENT course.
    d.embedded.update_one({"_id": 22}, {"$push": {"enrollments": {
        "course": "WEB303", "title": "Web Technologies", "grade": "A", "credits": 3}}})

    wrong2 = sorted(x["name"] for x in d.embedded.find(
        {"enrollments.course": "DSC301", "enrollments.grade": "A"}))
    right2 = sorted(x["name"] for x in d.embedded.find(
        {"enrollments": {"$elemMatch": {"course": "DSC301", "grade": "A"}}}))

    assert wrong2 == ["Asha Kumari", "Ravi Teja"], \
        "WRONG: Ravi matched using DSC301 from one element and grade A from another"
    assert right2 == ["Asha Kumari"], "RIGHT: one element must satisfy both"

    print("  after giving Ravi an A in a DIFFERENT course:")
    print(f"       without $elemMatch -> {wrong2}   (Ravi is a FALSE match)")
    print(f"       with    $elemMatch -> {right2}")


def positional_update():
    d = db()
    d.embedded.update_one({"_id": 21, "enrollments.course": "STA302"},
                          {"$set": {"enrollments.$.grade": "A"}})
    doc = d.embedded.find_one({"_id": 21})
    grades = {e["course"]: e["grade"] for e in doc["enrollments"]}
    assert grades == {"DSC301": "A", "STA302": "A"}, grades
    print("  the positional $ updated the element the QUERY matched")


def pushing_and_aggregating():
    d = db()
    d.embedded.update_one({"_id": 22}, {"$push": {"enrollments": {
        "course": "WEB303", "title": "Web Technologies", "grade": "B", "credits": 3}}})
    assert len(d.embedded.find_one({"_id": 22})["enrollments"]) == 2

    credits = {r["_id"]: r["credits"] for r in d.embedded.aggregate([
        {"$unwind": "$enrollments"},
        {"$group": {"_id": "$name", "credits": {"$sum": "$enrollments.credits"}}}])}
    assert credits == {"Asha Kumari": 7, "Ravi Teja": 7}, credits

    print(f"  total credits per student (needs $unwind): {credits}")


def the_limitation():
    """Embedding is right here because enrolments are BOUNDED. State the case
    where it would be wrong."""
    d = db()
    doc = d.embedded.find_one({"_id": 21})
    assert len(doc["enrollments"]) <= 10, "a degree has a bounded number of courses"

    print("  embedding is right here because a student's enrolments are BOUNDED")
    print("       -- attendance records or log entries would NOT be, and would")
    print("       eventually breach the 16 MB document limit")


def main():
    print("Experiment 9 -- An embedded data model")
    one_read_gets_everything()
    querying_nested_and_arrays()
    elemmatch_is_required()
    positional_update()
    pushing_and_aggregating()
    the_limitation()


if __name__ == "__main__":
    main()
