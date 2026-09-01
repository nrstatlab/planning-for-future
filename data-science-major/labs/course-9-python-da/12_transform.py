"""Practical 12 — Transform data using mapping functions and string operations."""
import time
import numpy as np
import pandas as pd
from fixtures import students


def map_versus_replace():
    """map with an incomplete dict silently produces NaN; replace does not."""
    dept = pd.Series(["DS", "Stats", "DS"])

    mapped = dept.map({"DS": "Data Science"})
    assert mapped.isna().sum() == 1, "'Stats' was UNMAPPED -> NaN"

    replaced = dept.replace({"DS": "Data Science"})
    assert replaced.tolist() == ["Data Science", "Stats", "Data Science"], \
        "replace leaves unmatched values ALONE"

    rescued = dept.map({"DS": "Data Science"}).fillna(dept)
    assert rescued.tolist() == replaced.tolist()

    print("  map + incomplete dict -> NaN (silently); replace keeps the rest")


def the_four_tools():
    df = students()

    # map -- Series only
    df["dept_full"] = df.dept.map({"DS": "Data Science", "Stats": "Statistics"})
    assert df.dept_full.iloc[0] == "Data Science"

    # apply on a Series
    df["grade"] = df.maths.apply(lambda m: "A" if m >= 90 else "B")
    assert df.grade.tolist() == ["B", "B", "A", "B", "B"]

    # apply on a DataFrame -- per COLUMN by default
    col_means = df[["maths", "stats"]].apply(np.mean)
    assert col_means.index.tolist() == ["maths", "stats"]
    assert round(float(col_means.maths), 2) == 74.00

    # ...per ROW with axis=1
    weighted = df.apply(lambda r: r.maths * 0.6 + r.stats * 0.4, axis=1)
    assert len(weighted) == 5
    assert round(float(weighted.iloc[0]), 2) == 89.20

    # DataFrame.map -- every CELL (this was applymap)
    bumped = df[["maths", "stats"]].map(lambda x: x + 5)
    assert bumped.loc[0, "maths"] == 93

    # transform -- the SAME SHAPE as the input
    gm = df.groupby("dept").maths.transform("mean")
    assert len(gm) == len(df), "one value per ORIGINAL ROW"
    assert len(df.groupby("dept").maths.mean()) == 2, "agg gives one per GROUP"

    print("  map/apply/DataFrame.map/transform -- transform keeps the shape")


def vectorise_instead_of_apply():
    n = 200_000
    df = pd.DataFrame({"a": np.arange(n), "b": np.arange(n)})

    t = time.perf_counter()
    slow = df.apply(lambda r: r.a + r.b, axis=1)
    apply_time = time.perf_counter() - t

    t = time.perf_counter()
    fast = df.a + df.b
    vec_time = time.perf_counter() - t

    assert (slow.to_numpy() == fast.to_numpy()).all(), "same answer"
    speedup = apply_time / vec_time
    assert speedup > 50, f"only {speedup:.0f}x -- something is wrong"

    print(f"  on {n:,} rows: apply(axis=1) {apply_time*1000:.0f} ms vs "
          f"a + b {vec_time*1000:.2f} ms -> {speedup:.0f}x")
    print(f"       apply(axis=1) calls a Python function PER ROW -- the very")
    print(f"       loop Unit 1 told you to avoid")


def binning():
    marks = pd.Series([35, 45, 62, 78, 92, 40])

    graded = pd.cut(marks, bins=[0, 40, 60, 75, 100],
                    labels=["Fail", "Pass", "First", "Distinction"])
    assert graded.tolist() == ["Fail", "Pass", "First", "Distinction",
                               "Distinction", "Fail"]

    # cut is RIGHT-CLOSED by default: exactly 40 falls in (0, 40] = "Fail"
    assert str(pd.cut(pd.Series([40]), bins=[0, 40, 60, 75, 100],
                      labels=["Fail", "Pass", "First", "Distinction"]).iloc[0]) == "Fail"
    assert str(pd.cut(pd.Series([40]), bins=[0, 40, 60, 75, 100],
                      labels=["Fail", "Pass", "First", "Distinction"],
                      right=False).iloc[0]) == "Pass", "right=False flips it"

    # cut = equal WIDTH; qcut = equal FREQUENCY
    skewed = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 100])
    assert pd.cut(skewed, 4).value_counts().sort_index().tolist() == [8, 0, 0, 1]
    assert pd.qcut(skewed, 4).value_counts().sort_index().tolist() == [3, 2, 2, 2]

    print("  cut(4) on skewed data -> counts [8,0,0,1]; qcut(4) -> [3,2,2,2]")
    print("       and cut is RIGHT-closed: a mark of exactly 40 is a Fail")


def string_transforms():
    names = pd.Series(["  asha kumari ", "RAVI TEJA", None])

    assert names.str.strip().str.title().tolist()[:2] == ["Asha Kumari", "Ravi Teja"]
    assert names.str.lower().isna().sum() == 1, ".str skips NaN instead of crashing"

    try:
        names.apply(str.lower)
        raise AssertionError("expected a TypeError on the None")
    except TypeError:
        pass

    split = pd.Series(["Asha Kumari", "Ravi Teja"]).str.split(" ", expand=True)
    assert split.shape == (2, 2), "expand=True gives real COLUMNS"
    assert split[0].tolist() == ["Asha", "Ravi"]

    nolist = pd.Series(["Asha Kumari"]).str.split(" ")
    assert isinstance(nolist.iloc[0], list), "without expand you get LISTS"

    print("  .str skips NaN where .apply(str.lower) raises; expand=True -> columns")


def main():
    print("Practical 12 -- Transforming data")
    map_versus_replace()
    the_four_tools()
    vectorise_instead_of_apply()
    binning()
    string_transforms()


if __name__ == "__main__":
    main()
