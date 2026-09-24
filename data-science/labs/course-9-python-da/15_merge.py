"""Practical 15 — Merge, join and concatenate datasets."""
import numpy as np
import pandas as pd

STUDENTS = pd.DataFrame({"roll": [21, 22, 23, 24],
                         "name": ["Asha", "Ravi", "Meena", "Kiran"]})
MARKS = pd.DataFrame({"roll": [21, 22, 23, 25],
                      "marks": [88, 65, 94, 70]})


def the_four_join_types():
    expected = {"inner": (3, [21, 22, 23]),
                "left":  (4, [21, 22, 23, 24]),
                "right": (4, [21, 22, 23, 25]),
                "outer": (5, [21, 22, 23, 24, 25])}

    for how, (n, keys) in expected.items():
        m = pd.merge(STUDENTS, MARKS, on="roll", how=how)
        assert len(m) == n, f"{how}: {len(m)} != {n}"
        assert sorted(m.roll.tolist()) == keys

    left = pd.merge(STUDENTS, MARKS, on="roll", how="left")
    assert pd.isna(left.loc[left.roll == 24, "marks"].iloc[0]), "Kiran has no marks"

    right = pd.merge(STUDENTS, MARKS, on="roll", how="right")
    assert pd.isna(right.loc[right.roll == 25, "name"].iloc[0]), "roll 25 has no name"

    cross = pd.merge(STUDENTS, MARKS, how="cross")
    assert len(cross) == 16, "4 x 4 -- every pair"

    print("  inner 3, left 4, right 4, outer 5, cross 16 rows")
    print("       inner SILENTLY drops rows -- compare the count before and after")


def indicator_tells_you_what_failed():
    m = pd.merge(STUDENTS, MARKS, on="roll", how="outer", indicator=True)
    counts = m._merge.value_counts().to_dict()
    assert counts["both"] == 3
    assert counts["left_only"] == 1
    assert counts["right_only"] == 1

    assert m[m._merge == "left_only"].name.iloc[0] == "Kiran"
    assert m[m._merge == "right_only"].roll.iloc[0] == 25

    print(f"  indicator=True -> {counts}")
    print(f"       left_only is Kiran (a student with no marks), right_only is")
    print(f"       roll 25 (marks with no student) -- the question you ACTUALLY have")


def three_things_that_break_merges():
    # 1. dtype mismatch. Older Pandas returned an EMPTY frame with no error --
    # a notorious silent failure. Pandas 3 RAISES instead, which is a real
    # improvement: verified on 3.0.5.
    a = STUDENTS.copy()
    b = MARKS.copy()
    b["roll"] = b.roll.astype(str)
    try:
        pd.merge(a, b, on="roll", how="inner")
        raise AssertionError("Pandas 3 should raise on an int64/str merge")
    except ValueError as e:
        assert "int64" in str(e) and "str" in str(e)

    b["roll"] = b.roll.astype(int)
    assert len(pd.merge(a, b, on="roll")) == 3, "fixed once the dtypes agree"

    # 2. whitespace in the key
    left = pd.DataFrame({"dept": ["DS", "Stats"], "head": ["Rao", "Devi"]})
    right = pd.DataFrame({"dept": ["DS ", " Stats"], "n": [3, 2]})
    assert len(pd.merge(left, right, on="dept")) == 0, "'DS' != 'DS '"
    right["dept"] = right.dept.str.strip()
    assert len(pd.merge(left, right, on="dept")) == 2

    # 3. NaN keys. Pandas JOINS NaN to NaN -- unlike SQL, where NULL = NULL is
    # never true and null-keyed rows simply do not join. Verified below against
    # sqlite3 on identical data.
    l2 = pd.DataFrame({"k": [1, np.nan, np.nan], "v": ["a", "b", "c"]})
    r2 = pd.DataFrame({"k": [1, np.nan], "w": ["x", "y"]})
    m2 = pd.merge(l2, r2, on="k", how="inner")
    assert len(m2) == 3, "pandas matched BOTH NaN rows -- 1 real + 2 NaN"
    assert m2.k.isna().sum() == 2

    import sqlite3
    con = sqlite3.connect(":memory:")
    con.execute("create table l(k real, v text)")
    con.execute("create table r(k real, w text)")
    con.executemany("insert into l values (?,?)", [(1, "a"), (None, "b"), (None, "c")])
    con.executemany("insert into r values (?,?)", [(1, "x"), (None, "y")])
    sql_rows = con.execute("select l.k, v, w from l join r on l.k = r.k").fetchall()
    assert len(sql_rows) == 1, "SQL joins only the 1 -- NULL never equals NULL"
    con.close()

    print("  dtype mismatch -> Pandas 3 RAISES (older versions returned 0 rows")
    print("       silently); whitespace in the key -> 0 rows")
    print("  NaN keys: pandas gave 3 rows, the SAME join in SQL gave 1 --")
    print("       pandas JOINS NaN to NaN, SQL never joins NULL to NULL.")
    print("       Course 5's mental model does NOT transfer here.")


def duplicate_keys_explode():
    """The row explosion that validate= exists to catch."""
    left = pd.DataFrame({"k": ["a", "a", "a"], "l": [1, 2, 3]})
    right = pd.DataFrame({"k": ["a", "a", "a", "a"], "r": [10, 20, 30, 40]})

    m = pd.merge(left, right, on="k")
    assert len(m) == 12, "3 x 4 = the CARTESIAN PRODUCT"

    try:
        pd.merge(left, right, on="k", validate="one_to_one")
        raise AssertionError("expected a MergeError")
    except pd.errors.MergeError:
        pass

    # And it passes when the relationship really holds.
    ok = pd.merge(STUDENTS, MARKS, on="roll", validate="one_to_one")
    assert len(ok) == 3

    print("  3 duplicate keys x 4 -> 12 rows; validate='one_to_one' raises MergeError")
    print("       use it EVERY time: silent corruption becomes an immediate error")


def concat_stacks():
    a = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    b = pd.DataFrame({"y": [5, 6], "z": [7, 8]})

    c = pd.concat([a, b])
    assert sorted(c.columns) == ["x", "y", "z"], "the UNION of columns"
    assert c.index.tolist() == [0, 1, 0, 1], "the index REPEATS"
    assert c.y.dtype == np.int64, "y gained no NaN, so it stays int64"
    assert c.x.isna().sum() == 2 and c.z.isna().sum() == 2

    ri = pd.concat([a, b], ignore_index=True)
    assert ri.index.tolist() == [0, 1, 2, 3], "ignore_index renumbers"

    inner = pd.concat([a, b], join="inner")
    assert list(inner.columns) == ["y"], "only the shared column"

    keyed = pd.concat([a, b], keys=["first", "second"])
    assert keyed.index.nlevels == 2, "keys give a MultiIndex marking the source"

    side = pd.concat([a, b], axis=1)
    assert side.shape == (2, 4), "axis=1 stacks COLUMNS"

    print("  concat stacks (union of columns, index REPEATS); merge matches on a key")
    print("       ignore_index=True is almost always what you want for rows")


def join_on_the_index():
    a = STUDENTS.set_index("roll")
    b = MARKS.set_index("roll")
    j = a.join(b)
    assert len(j) == 4, "join defaults to a LEFT join on the index"
    assert j.marks.isna().sum() == 1
    assert len(a.join(b, how="inner")) == 3
    print("  .join() works on the INDEX and defaults to how='left'")


def main():
    print("Practical 15 -- Merging and concatenation")
    the_four_join_types()
    indicator_tells_you_what_failed()
    three_things_that_break_merges()
    duplicate_keys_explode()
    concat_stacks()
    join_on_the_index()


if __name__ == "__main__":
    main()
