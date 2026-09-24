"""Experiment 16 — $lookup, $unwind and $bucket.

Executed and asserted: $unwind (including the empty-array trap), $lookup in
both directions, $bucket, and $facet.

Not available in mongomock, and asserted as unavailable rather than described
as if tested: $bucketAuto, and $lookup's let/pipeline form.
"""
from pymongo.errors import OperationFailure

from fixtures import fresh_db


def by(rows, key="_id"):
    return {r[key]: r for r in rows}


# =============================================================================
# $unwind
# =============================================================================

def one_document_per_element():
    db = fresh_db()
    before = db.students.count_documents({})
    after = len(list(db.students.aggregate([{"$unwind": "$subjects"}])))

    assert before == 5
    assert after == 9 == 3 + 2 + 2 + 1 + 1, after

    print(f"  {before} students -> {after} documents (3+2+2+1+1 subjects)")


def counting_array_contents():
    """The whole reason $unwind exists. $group alone cannot do this."""
    db = fresh_db()
    rows = by(db.students.aggregate([
        {"$unwind": "$subjects"},
        {"$group": {"_id": "$subjects", "n": {"$sum": 1},
                    "who": {"$push": "$name"}}},
        {"$sort": {"n": -1, "_id": 1}}]))

    assert {k: v["n"] for k, v in rows.items()} == \
        {"DS": 3, "Stats": 3, "Python": 2, "R": 1}
    assert sorted(rows["DS"]["who"]) == ["Asha", "Kiran", "Ravi"]
    assert sorted(rows["Stats"]["who"]) == ["Asha", "Bhanu", "Meena"]
    assert rows["R"]["who"] == ["Meena"]
    assert sum(v["n"] for v in rows.values()) == 9, "every element counted once"

    print("  subject counts:")
    for s in ("DS", "Stats", "Python", "R"):
        print(f"    {s:7s} {rows[s]['n']}  {sorted(rows[s]['who'])}")


def unwind_silently_drops_empty_and_missing():
    """The one worth seeing fail. Two students vanish from a count."""
    db = fresh_db()
    db.students.insert_one({"_id": 26, "name": "Latha", "dept": "DS",
                            "subjects": []})
    db.students.insert_one({"_id": 27, "name": "Mohan", "dept": "DS"})

    assert db.students.count_documents({}) == 7

    dropped = list(db.students.aggregate([{"$unwind": "$subjects"}]))
    assert len(dropped) == 9, len(dropped)
    assert "Latha" not in {d["name"] for d in dropped}
    assert "Mohan" not in {d["name"] for d in dropped}

    kept = list(db.students.aggregate([
        {"$unwind": {"path": "$subjects",
                     "preserveNullAndEmptyArrays": True}}]))
    assert len(kept) == 11, len(kept)
    survivors = {d["name"] for d in kept}
    assert "Latha" in survivors and "Mohan" in survivors
    assert all("subjects" not in d for d in kept
               if d["name"] in ("Latha", "Mohan")), \
        "they come back with the field UNSET, not with an empty array"

    print("  7 students, two with no subjects (empty array / missing field):")
    print(f"    plain $unwind                        -> {len(dropped)} docs, both LOST")
    print(f"    preserveNullAndEmptyArrays: true     -> {len(kept)} docs, both kept")
    print("       'my count is short and I cannot see why' is nearly always this")


def includearrayindex_and_non_arrays():
    db = fresh_db()
    firsts = list(db.students.aggregate([
        {"$unwind": {"path": "$subjects", "includeArrayIndex": "pos"}},
        {"$match": {"pos": 0}},
        {"$project": {"_id": 0, "name": 1, "subjects": 1}}]))

    assert len(firsts) == 5, firsts
    assert {d["name"]: d["subjects"] for d in firsts} == \
        {"Asha": "DS", "Ravi": "DS", "Meena": "Stats",
         "Kiran": "DS", "Bhanu": "Stats"}

    # $unwind on a NON-array is not an error: it acts as a one-element array.
    scalar = list(db.students.aggregate([{"$unwind": "$name"}]))
    assert len(scalar) == 5, "unwinding a string yields the same 5 documents"

    # A typo'd path is therefore SILENT -- it just returns nothing.
    typo = list(db.students.aggregate([{"$unwind": "$subject"}]))
    assert typo == [], "no error, no rows -- the commonest silent failure"

    print("  includeArrayIndex 'pos', $match pos:0 -> each student's FIRST subject")
    print("  $unwind on a string   -> 5 documents (treated as one element)")
    print("  $unwind on '$subject' -> 0 documents (a TYPO, and it does not error)")


# =============================================================================
# $lookup
# =============================================================================

def lookup_returns_an_array_and_is_a_left_outer_join():
    db = fresh_db()
    db.enrollments.insert_one({"student_id": 21, "course_id": "GONE404",
                               "grade": "F"})

    joined = list(db.enrollments.aggregate([
        {"$lookup": {"from": "courses", "localField": "course_id",
                     "foreignField": "_id", "as": "course"}}]))

    assert len(joined) == 6, "every enrolment survives -- LEFT outer"
    sizes = {d["course_id"]: len(d["course"]) for d in joined}
    assert sizes["GONE404"] == 0, "no match -> EMPTY ARRAY, not a missing row"
    assert all(v == 1 for k, v in sizes.items() if k != "GONE404"), sizes
    assert all(isinstance(d["course"], list) for d in joined), \
        "as: is ALWAYS an array, even one-to-one -- that is why $unwind follows"

    # And now the consequence: the $unwind after it deletes the orphan.
    unwound = list(db.enrollments.aggregate([
        {"$lookup": {"from": "courses", "localField": "course_id",
                     "foreignField": "_id", "as": "course"}},
        {"$unwind": "$course"}]))
    assert len(unwound) == 5, "the orphan's empty array was dropped by $unwind"

    print("  6 enrolments, one pointing at a course that does not exist:")
    print("    after $lookup           -> 6 rows, the orphan has course: []")
    print("    after $lookup + $unwind -> 5 rows, the orphan is GONE")
    print("       $lookup is a LEFT outer join; the $unwind after it turns it")
    print("       into an inner one. Nothing warns you")


def joining_both_directions():
    db = fresh_db()

    # enrolments -> the student and the course behind each one
    rows = list(db.enrollments.aggregate([
        {"$lookup": {"from": "students", "localField": "student_id",
                     "foreignField": "_id", "as": "student"}},
        {"$lookup": {"from": "courses", "localField": "course_id",
                     "foreignField": "_id", "as": "course"}},
        {"$unwind": "$student"},
        {"$unwind": "$course"},
        {"$project": {"_id": 0, "name": "$student.name",
                      "title": "$course.title", "grade": 1}},
        {"$sort": {"name": 1, "title": 1}}]))

    assert len(rows) == 5
    assert rows[0] == {"name": "Asha", "title": "Data Science with R",
                       "grade": "A"}, rows[0]
    assert {r["name"] for r in rows} == {"Asha", "Ravi", "Meena", "Kiran"}

    # courses -> how many enrolled. $size beats $unwind when you want a count.
    counts = list(db.courses.aggregate([
        {"$lookup": {"from": "enrollments", "localField": "_id",
                     "foreignField": "course_id", "as": "enrolled"}},
        {"$project": {"_id": 0, "title": 1, "n": {"$size": "$enrolled"}}},
        {"$sort": {"n": -1, "title": 1}}]))

    assert counts == [{"title": "Data Science with R", "n": 2},
                      {"title": "Statistical Foundations", "n": 2},
                      {"title": "Web Technologies", "n": 1}], counts

    print("  enrolments -> student + course:")
    for r in rows:
        print(f"    {r['name']:6s} {r['title']:24s} {r['grade']}")
    print("  courses -> enrolment counts, via $size on the joined array:")
    for c in counts:
        print(f"    {c['title']:24s} {c['n']}")
    print("       $size needs no $unwind and no $group -- one stage, one pass")


def the_let_pipeline_form_is_not_implemented_here():
    """Asserted, so this file cannot start claiming to test what it describes."""
    db = fresh_db()
    try:
        list(db.courses.aggregate([{"$lookup": {
            "from": "enrollments",
            "let": {"cid": "$_id"},
            "pipeline": [{"$match": {"$expr": {"$and": [
                {"$eq": ["$course_id", "$$cid"]},
                {"$eq": ["$grade", "A"]}]}}}],
            "as": "aGrades"}}]))
        raise SystemExit("mongomock now implements let/pipeline -- assert it")
    except NotImplementedError as exc:
        assert "let" in str(exc), exc

    # The runnable equivalent: join everything, then filter. Same answer,
    # more work -- which is exactly the point the let form makes.
    rows = list(db.courses.aggregate([
        {"$lookup": {"from": "enrollments", "localField": "_id",
                     "foreignField": "course_id", "as": "e"}},
        {"$unwind": "$e"},
        {"$match": {"e.grade": "A"}},
        {"$group": {"_id": "$title", "n": {"$sum": 1}}},
        {"$sort": {"_id": 1}}]))
    assert rows == [{"_id": "Data Science with R", "n": 1},
                    {"_id": "Statistical Foundations", "n": 1}], rows

    print("  $lookup with let/pipeline: NotImplementedError in mongomock")
    print("  the join-then-filter equivalent DOES run, and gives:")
    for r in rows:
        print(f"    {r['_id']:24s} {r['n']} grade-A enrolment(s)")
    print("       same answer, and on real data far more expensive: it drags")
    print("       every enrolment in and then throws most of them away.")
    print("       $$cid is the OUTER let variable, $course_id the inner field")


# =============================================================================
# $bucket
# =============================================================================

def bucket_boundaries_are_closed_below_and_open_above():
    db = fresh_db()
    rows = by(db.students.aggregate([{"$bucket": {
        "groupBy": "$marks.maths",
        "boundaries": [0, 40, 60, 75, 101],
        "default": "Other",
        "output": {"count": {"$sum": 1}, "names": {"$push": "$name"}}}}]))

    assert {k: v["count"] for k, v in rows.items()} == {40: 1, 60: 2, 75: 2}
    assert rows[40]["names"] == ["Bhanu"]                       # 52
    assert sorted(rows[60]["names"]) == ["Kiran", "Ravi"]        # 71, 65
    assert sorted(rows[75]["names"]) == ["Asha", "Meena"]        # 88, 94
    assert 0 not in rows, "the 0-40 bucket is EMPTY and is simply not emitted"

    print("  bucket   count  names")
    for lo, hi in ((0, 40), (40, 60), (60, 75), (75, 101)):
        r = rows.get(lo)
        label = f"[{lo:3d},{hi:4d})"
        if r:
            print(f"  {label}  {r['count']:5d}  {sorted(r['names'])}")
        else:
            print(f"  {label}  {'--':>5s}  (empty buckets are NOT emitted)")


def why_the_top_boundary_is_101():
    """A perfect score is the test case, and 100 as the boundary loses it."""
    db = fresh_db()
    db.students.insert_one({"_id": 28, "name": "Perfect", "dept": "DS",
                            "marks": {"maths": 100, "stats": 100},
                            "subjects": ["DS"], "age": 20, "active": True})

    with_101 = by(db.students.aggregate([{"$bucket": {
        "groupBy": "$marks.maths", "boundaries": [0, 40, 60, 75, 101],
        "default": "Other", "output": {"names": {"$push": "$name"}}}}]))
    assert "Perfect" in with_101[75]["names"], with_101

    with_100 = by(db.students.aggregate([{"$bucket": {
        "groupBy": "$marks.maths", "boundaries": [0, 40, 60, 75, 100],
        "default": "Other", "output": {"names": {"$push": "$name"}}}}]))
    assert with_100["Other"]["names"] == ["Perfect"], with_100
    assert "Perfect" not in with_100[75]["names"]

    # And without a default, an out-of-range value is an ERROR.
    try:
        list(db.students.aggregate([{"$bucket": {
            "groupBy": "$marks.maths", "boundaries": [0, 40, 60, 75, 100],
            "output": {"n": {"$sum": 1}}}}]))
        raise SystemExit("$bucket should reject an out-of-range value with no default")
    except OperationFailure as exc:
        assert "no default was specified" in str(exc), exc

    print("  a student who scored exactly 100:")
    print("    boundaries [..., 75, 101] -> lands in [75,101)   CORRECT")
    print("    boundaries [..., 75, 100] -> lands in 'Other'    WRONG")
    print("    boundaries [..., 75, 100], no default -> ERROR")
    print("       buckets are [lower, upper): closed below, OPEN above. The top")
    print("       boundary must exceed the maximum, so it is max+1, not max")


def bucketauto_is_not_implemented_here():
    db = fresh_db()
    try:
        list(db.students.aggregate([
            {"$bucketAuto": {"groupBy": "$marks.maths", "buckets": 3}}]))
        raise SystemExit("mongomock now implements $bucketAuto -- assert it")
    except NotImplementedError as exc:
        assert "$bucketAuto" in str(exc), exc

    print("  $bucketAuto: NotImplementedError in mongomock")
    print("       it picks boundaries to even out the COUNTS, so you never")
    print("       state them. Good for a first look at unfamiliar data; wrong")
    print("       for a report, because the boundaries MOVE when the data does")
    print("       and last month's chart is no longer comparable with this one")


def facet_runs_several_pipelines_in_one_pass():
    db = fresh_db()
    out = list(db.students.aggregate([{"$facet": {
        "byDept":   [{"$group": {"_id": "$dept", "n": {"$sum": 1}}},
                     {"$sort": {"_id": 1}}],
        "topThree": [{"$sort": {"marks.maths": -1}}, {"$limit": 3},
                     {"$project": {"_id": 0, "name": 1}}],
    }}]))

    assert len(out) == 1, "$facet emits exactly ONE document"
    result = out[0]
    assert result["byDept"] == [{"_id": "DS", "n": 3},
                                {"_id": "Stats", "n": 2}], result["byDept"]
    assert [d["name"] for d in result["topThree"]] == ["Meena", "Asha", "Kiran"]

    print("  $facet -> ONE document holding both results:")
    print(f"    byDept   {result['byDept']}")
    print(f"    topThree {[d['name'] for d in result['topThree']]}")
    print("       one pass over the collection instead of two queries, which")
    print("       is how a dashboard gets all its panels in a single round trip")


def main():
    print("Experiment 16 -- $lookup, $unwind, $bucket")
    one_document_per_element()
    counting_array_contents()
    unwind_silently_drops_empty_and_missing()
    includearrayindex_and_non_arrays()
    lookup_returns_an_array_and_is_a_left_outer_join()
    joining_both_directions()
    the_let_pipeline_form_is_not_implemented_here()
    bucket_boundaries_are_closed_below_and_open_above()
    why_the_top_boundary_is_101()
    bucketauto_is_not_implemented_here()
    facet_runs_several_pipelines_in_one_pass()


if __name__ == "__main__":
    main()
