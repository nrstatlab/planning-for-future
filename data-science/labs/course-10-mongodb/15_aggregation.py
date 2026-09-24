"""Experiment 15 — $match, $group, $project, $sort.

Every figure printed here is computed by mongomock and asserted against the
hand-worked arithmetic in unit-4.md, so the notes and the pipeline check each
other. The one exception is $stdDevPop, which mongomock raises
NotImplementedError on; that is asserted as a limitation and the value is
computed in Python instead, clearly labelled.
"""
import statistics

import mongomock
from fixtures import fresh_db


def by(rows, key="_id"):
    """A pipeline result keyed for assertion. Aggregation order is not a promise."""
    return {r[key]: r for r in rows}


def where_and_having_are_the_same_stage():
    """The whole pipeline, and the sentence that earns the marks."""
    db = fresh_db()
    rows = list(db.students.aggregate([
        {"$match":   {"active": True}},
        {"$group":   {"_id": "$dept", "avg": {"$avg": "$marks.maths"},
                      "n": {"$sum": 1}}},
        {"$match":   {"n": {"$gt": 1}}},
        {"$sort":    {"avg": -1}},
        # $round would go here on a real server; mongomock does not have it,
        # and unsupported_operators() below asserts that. Both averages are
        # exact anyway, so nothing is hidden by leaving it out.
        {"$project": {"_id": 0, "dept": "$_id", "avg": 1, "n": 1}},
    ]))

    # active: true drops Kiran (DS, 71), so DS is Asha and Ravi only.
    assert rows == [{"dept": "DS", "avg": 76.5, "n": 2},
                    {"dept": "Stats", "avg": 73.0, "n": 2}], rows
    assert (88 + 65) / 2 == 76.5
    assert (94 + 52) / 2 == 73.0

    # $sort was honoured: descending by avg.
    assert [r["avg"] for r in rows] == sorted((r["avg"] for r in rows), reverse=True)

    print("  WHERE active=true, GROUP BY dept, HAVING n>1, ORDER BY avg DESC")
    print("    DS    (88+65)/2 = 76.5  n=2")
    print("    Stats (94+52)/2 = 73.0  n=2")
    print("       Kiran is DS with 71 but active:false, so the $match BEFORE")
    print("       $group excludes him and the DS average RISES from 74.67")


def the_filter_changes_the_answer():
    """Same grouping, no $match: unit-4.md Problem 1(a)'s figures."""
    db = fresh_db()
    rows = by(db.students.aggregate([
        {"$group": {"_id": "$dept", "avg": {"$avg": "$marks.maths"},
                    "n": {"$sum": 1}}}]))

    assert rows["DS"]["n"] == 3 and rows["Stats"]["n"] == 2
    assert round(rows["DS"]["avg"], 3) == 74.667, rows["DS"]["avg"]
    assert (88 + 65 + 71) / 3 == rows["DS"]["avg"]
    assert rows["Stats"]["avg"] == 73.0

    print("  without the $match: DS (88+65+71)/3 = 74.667 over 3, Stats 73 over 2")
    print("       these are unit-4.md Problem 1(a)'s numbers, and the pair of")
    print("       results above is why 'which $match, and where' is the question")


def group_id_is_the_key_and_null_is_the_grand_total():
    db = fresh_db()
    total = list(db.students.aggregate([
        {"$group": {"_id": None, "avg": {"$avg": "$marks.maths"},
                    "n": {"$sum": 1}}}]))
    assert total == [{"_id": None, "avg": 74.0, "n": 5}], total
    assert (88 + 65 + 94 + 71 + 52) / 5 == 74.0

    # _id is not optional -- omitting it is an error, not a grand total.
    # (A real server says "a group specification must include an _id";
    #  mongomock reaches for the key and raises KeyError. Either way: rejected.)
    try:
        list(db.students.aggregate([{"$group": {"n": {"$sum": 1}}}]))
        raise SystemExit("$group without _id should not be accepted")
    except KeyError as exc:
        assert str(exc) == "'_id'", exc

    print("  _id: null -> one bucket: avg 74.0 over 5 (the grand total)")
    print("  _id omitted -> ERROR. It is the grouping KEY, not an option")


def the_accumulators():
    db = fresh_db()
    rows = by(db.students.aggregate([{"$group": {
        "_id":      "$dept",
        "n":        {"$sum": 1},
        "totMaths": {"$sum": "$marks.maths"},
        "avgMaths": {"$avg": "$marks.maths"},
        "best":     {"$max": "$marks.maths"},
        "worst":    {"$min": "$marks.maths"},
        "everyone": {"$push": "$name"},
        "distinct": {"$addToSet": "$dept"},
    }}]))

    ds = rows["DS"]
    assert ds["n"] == 3
    assert ds["totMaths"] == 224 == 88 + 65 + 71
    assert round(ds["avgMaths"], 3) == 74.667
    assert (ds["best"], ds["worst"]) == (88, 65)
    assert sorted(ds["everyone"]) == ["Asha", "Kiran", "Ravi"]
    assert ds["distinct"] == ["DS"], "addToSet de-duplicates; push does not"

    st = rows["Stats"]
    assert (st["n"], st["totMaths"], st["avgMaths"]) == (2, 146, 73.0)
    assert (st["best"], st["worst"]) == (94, 52)

    print("  dept   n  sum  avg      max  min  $push")
    for d in ("DS", "Stats"):
        r = rows[d]
        print(f"  {d:6s} {r['n']}  {r['totMaths']:3d}  {r['avgMaths']:7.3f}  "
              f"{r['best']:3d}  {r['worst']:3d}  {r['everyone']}")
    print("       $push and $addToSet have NO SQL equivalent -- they are why")
    print("       MongoDB never needed GROUP_CONCAT")


def unsupported_operators():
    """Two operators this pipeline would use on a real server, and cannot here.

    Asserted rather than commented, so the day mongomock gains them this file
    fails and gets rewritten to test them instead of describing them.
    """
    db = fresh_db()

    try:
        list(db.students.aggregate([
            {"$group": {"_id": "$dept", "sd": {"$stdDevPop": "$marks.maths"}}}]))
        raise SystemExit("mongomock now implements $stdDevPop -- assert it here")
    except NotImplementedError as exc:
        assert "$stdDevPop" in str(exc), exc

    try:
        list(db.students.aggregate([
            {"$project": {"m": {"$round": ["$marks.maths", 1]}}}]))
        raise SystemExit("mongomock now implements $round -- use it above")
    except Exception as exc:
        assert "$round" in str(exc), exc

    print("  not available in mongomock (both work on a real server):")
    print("    $round      OperationFailure: Unrecognized expression '$round'")
    print("    $stdDevPop  NotImplementedError")
    print("  so $stdDevPop is computed in Python here instead:")
    for dept in ("DS", "Stats"):
        vals = [d["marks"]["maths"] for d in db.students.find({"dept": dept})]
        pop = statistics.pstdev(vals)
        samp = statistics.stdev(vals)
        print(f"    {dept:6s} {vals}  $stdDevPop {pop:7.4f}   $stdDevSamp {samp:7.4f}")
    print("       Course 4's distinction, unchanged: $stdDevPop divides by n,")
    print("       $stdDevSamp by n-1. MongoDB makes you choose, as R does")


def project_computes_and_renames():
    db = fresh_db()
    rows = by(db.students.aggregate([{"$project": {
        "_id": 0, "name": 1,
        "total": {"$add": ["$marks.maths", "$marks.stats"]},
        "band": {"$switch": {"branches": [
            {"case": {"$gte": ["$marks.maths", 75]}, "then": "Distinction"},
            {"case": {"$gte": ["$marks.maths", 60]}, "then": "First"},
            {"case": {"$gte": ["$marks.maths", 40]}, "then": "Pass"}],
            "default": "Fail"}},
    }}], ), key="name")

    assert rows["Asha"] == {"name": "Asha", "total": 179, "band": "Distinction"}
    assert rows["Meena"]["total"] == 183 and rows["Meena"]["band"] == "Distinction"
    assert rows["Ravi"]["band"] == "First" and rows["Kiran"]["band"] == "First"
    assert rows["Bhanu"]["band"] == "Pass"
    assert all("dept" not in r for r in rows.values()), \
        "$project is EXCLUSIVE: naming any field drops the rest"

    print("  name   total  band")
    for n in ("Meena", "Asha", "Kiran", "Ravi", "Bhanu"):
        print(f"  {n:6s} {rows[n]['total']:5d}  {rows[n]['band']}")
    print("       dept is GONE -- $project keeps only what you name. Use")
    print("       $addFields when you meant 'everything, plus this'")


def addfields_keeps_everything():
    db = fresh_db()
    rows = list(db.students.aggregate([
        {"$addFields": {"total": {"$add": ["$marks.maths", "$marks.stats"]}}},
        {"$sort": {"total": -1}},
        {"$limit": 3},
    ]))

    assert [(r["name"], r["total"]) for r in rows] == \
        [("Meena", 183), ("Asha", 179), ("Kiran", 137)], rows
    assert all("dept" in r and "subjects" in r for r in rows), \
        "$addFields adds; it never removes"

    print("  top 3 by total, via $addFields: Meena 183, Asha 179, Kiran 137")
    print("       dept and subjects survived -- that is the difference")


def match_first_or_pay_for_it():
    """The optimiser helps, but only when it can. State the rule, not the hope."""
    db = fresh_db()

    late = list(db.students.aggregate([
        {"$group": {"_id": "$dept", "n": {"$sum": 1}}},
        {"$match": {"_id": "DS"}}]))
    early = list(db.students.aggregate([
        {"$match": {"dept": "DS"}},
        {"$group": {"_id": "$dept", "n": {"$sum": 1}}}]))

    assert late == early == [{"_id": "DS", "n": 3}], (late, early)

    print("  both orders return [{_id: 'DS', n: 3}] -- SAME ANSWER, different cost")
    print("       $match first can use an index on dept and groups 3 documents;")
    print("       $match last groups all 5 and then filters GROUPS, which no")
    print("       index describes, because they are new documents")
    print("       On 5 documents this is invisible. On 5,000,000 it is the")
    print("       whole query -- and that is what explain() shows you")


def main():
    print("Experiment 15 -- $match, $group, $project, $sort")
    where_and_having_are_the_same_stage()
    the_filter_changes_the_answer()
    group_id_is_the_key_and_null_is_the_grand_total()
    the_accumulators()
    unsupported_operators()
    project_computes_and_renames()
    addfields_keeps_everything()
    match_first_or_pay_for_it()


if __name__ == "__main__":
    main()
