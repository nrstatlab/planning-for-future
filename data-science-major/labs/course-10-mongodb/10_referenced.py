"""Experiment 10 — A normalized model using document references."""
from fixtures import fresh_db


def two_reads_or_one_lookup():
    db = fresh_db()

    # Application-side: two reads.
    student = db.students.find_one({"_id": 21})
    enrolments = list(db.enrollments.find({"student_id": 21}))
    assert student["name"] == "Asha"
    assert len(enrolments) == 2

    # Or one $lookup.
    joined = list(db.enrollments.aggregate([
        {"$match": {"student_id": 21}},
        {"$lookup": {"from": "courses", "localField": "course_id",
                     "foreignField": "_id", "as": "course"}},
        {"$unwind": "$course"},
        {"$project": {"_id": 0, "course": "$course.title", "grade": 1}}]))

    assert sorted(j["course"] for j in joined) == \
        ["Data Science with R", "Statistical Foundations"], joined

    print(f"  two reads, or one $lookup -> {[j['course'] for j in joined]}")


def lookup_always_produces_an_array():
    """Which is why $unwind almost always follows it."""
    db = fresh_db()

    raw = list(db.enrollments.aggregate([
        {"$match": {"student_id": 21, "course_id": "DSC301"}},
        {"$lookup": {"from": "courses", "localField": "course_id",
                     "foreignField": "_id", "as": "course"}}]))

    assert isinstance(raw[0]["course"], list), "an ARRAY even for a 1-to-1 match"
    assert len(raw[0]["course"]) == 1

    unwound = list(db.enrollments.aggregate([
        {"$match": {"student_id": 21, "course_id": "DSC301"}},
        {"$lookup": {"from": "courses", "localField": "course_id",
                     "foreignField": "_id", "as": "course"}},
        {"$unwind": "$course"}]))
    assert isinstance(unwound[0]["course"], dict), "$unwind makes it a sub-document"
    assert unwound[0]["course"]["title"] == "Data Science with R"

    print("  $lookup gave course: [ {...} ]; $unwind made it course: { ... }")
    print("       without $unwind, '$course.title' would be an ARRAY of titles")


def lookup_is_a_left_outer_join():
    db = fresh_db()
    db.enrollments.insert_one({"student_id": 21, "course_id": "GONE", "grade": "F"})

    rows = list(db.enrollments.aggregate([
        {"$lookup": {"from": "courses", "localField": "course_id",
                     "foreignField": "_id", "as": "course"}}]))

    orphan = [r for r in rows if r["course_id"] == "GONE"][0]
    assert orphan["course"] == [], "an unmatched document gets an EMPTY ARRAY"
    assert len(rows) == 6, "the orphan is KEPT -- left outer join"

    # $unwind would then DROP it, unless you preserve empties.
    dropped = list(db.enrollments.aggregate([
        {"$lookup": {"from": "courses", "localField": "course_id",
                     "foreignField": "_id", "as": "course"}},
        {"$unwind": "$course"}]))
    assert len(dropped) == 5, "$unwind silently dropped the orphan"

    kept = list(db.enrollments.aggregate([
        {"$lookup": {"from": "courses", "localField": "course_id",
                     "foreignField": "_id", "as": "course"}},
        {"$unwind": {"path": "$course", "preserveNullAndEmptyArrays": True}}]))
    assert len(kept) == 6

    print("  $lookup kept the orphan with course: []; $unwind then DROPPED it")
    print("       preserveNullAndEmptyArrays: true keeps it -- 6 rows, not 5")


def references_are_not_enforced():
    """The row that matters most in the RDBMS comparison."""
    db = fresh_db()
    assert db.enrollments.count_documents({"course_id": "DSC301"}) == 2

    db.courses.delete_one({"_id": "DSC301"})
    assert db.courses.find_one({"_id": "DSC301"}) is None
    assert db.enrollments.count_documents({"course_id": "DSC301"}) == 2, \
        "the enrolments STILL reference a course that no longer exists"

    # An integrity check the application must run for itself.
    valid = set(db.courses.distinct("_id"))
    orphans = [e for e in db.enrollments.find()
               if e["course_id"] not in valid]
    assert len(orphans) == 2

    print("  deleting the course left 2 DANGLING references, with no error")
    print("       Course 5's foreign key would have refused; here the")
    print(f"       application must check -- {len(orphans)} orphans found")


def index_the_foreign_field():
    db = fresh_db()
    db.enrollments.create_index("course_id")
    db.enrollments.create_index("student_id")

    names = {i["name"] for i in db.enrollments.list_indexes()}
    assert "course_id_1" in names and "student_id_1" in names

    print("  indexed both foreignFields -- without them, $lookup scans the")
    print("       whole other collection ONCE PER INPUT DOCUMENT")


def main():
    print("Experiment 10 -- A normalized model with references")
    two_reads_or_one_lookup()
    lookup_always_produces_an_array()
    lookup_is_a_left_outer_join()
    references_are_not_enforced()
    index_the_foreign_field()


if __name__ == "__main__":
    main()
