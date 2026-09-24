"""Practical 17 — Summary statistics grouped by level or category.

Also recomputes Course 4's worked examples in Pandas, which is where finding
D8's Excel/Python gap finally closes.
"""
import numpy as np
import pandas as pd
from fixtures import students, COURSE4_SAMPLE


def split_apply_combine():
    df = students()

    means = df.groupby("dept").maths.mean()
    assert means.index.tolist() == ["DS", "Stats"]
    assert round(float(means["DS"]), 4) == round((88 + 65 + 71) / 3, 4)

    agg = df.groupby("dept").maths.agg(["mean", "median", "std", "count",
                                        "min", "max"])
    assert list(agg.columns) == ["mean", "median", "std", "count", "min", "max"]
    assert agg.loc["DS", "count"] == 3

    named = df.groupby("dept").agg(avg=("maths", "mean"),
                                   top=("maths", "max"),
                                   n=("maths", "size"))
    assert list(named.columns) == ["avg", "top", "n"], "named aggregation is clearest"
    assert named.loc["Stats", "top"] == 94

    flat = df.groupby("dept", as_index=False).maths.mean()
    assert "dept" in flat.columns, "as_index=False keeps it a column"

    print(f"  groupby means {means.round(2).to_dict()}; named agg -> {list(named.columns)}")


def size_versus_count():
    df = students()
    df.loc[0, "maths"] = np.nan

    assert df.groupby("dept").size().to_dict() == {"DS": 3, "Stats": 2}, "ALL rows"
    assert df.groupby("dept").maths.count().to_dict() == {"DS": 2, "Stats": 2}, \
        "NON-NULL values"

    print("  size() {'DS': 3} vs count() {'DS': 2} -- they differ by the NaN")


def agg_transform_filter():
    df = students()

    a = df.groupby("dept").maths.agg("mean")
    assert len(a) == 2, "one row per GROUP"

    t = df.groupby("dept").maths.transform("mean")
    assert len(t) == len(df) == 5, "one value per ORIGINAL ROW"

    # This is why transform exists: agg cannot be assigned back.
    df["dept_mean"] = t
    assert df.loc[df.dept == "DS", "dept_mean"].nunique() == 1, \
        "every DS row carries the SAME departmental mean"
    assert round(float(df.loc[df.dept == "DS", "dept_mean"].iloc[0]), 4) == \
        round((88 + 65 + 71) / 3, 4)

    try:
        df["bad"] = a
        # If this does not raise it will align on the INDEX and give NaN,
        # which is just as wrong, only quieter.
        assert df.bad.isna().all(), "aligning a 2-row agg onto 5 rows gives NaN"
    except Exception:
        pass

    f = df.groupby("dept").filter(lambda g: len(g) >= 3)
    assert len(f) == 3 and set(f.dept) == {"DS"}, "whole GROUPS kept or dropped"

    print("  agg -> 2 rows, transform -> 5, filter -> 3 (only the group of 3+)")


def group_shares_must_sum_to_100():
    """The check worth writing every time you compute a share."""
    df = students()
    df["pct_of_dept"] = df.maths / df.groupby("dept").maths.transform("sum") * 100

    sums = df.groupby("dept").pct_of_dept.sum()
    assert np.allclose(sums.to_numpy(), 100.0), sums.to_dict()

    # The WRONG denominator: the grand total instead of the group total.
    df["wrong"] = df.maths / df.maths.sum() * 100
    wrong_sums = df.groupby("dept").wrong.sum()
    assert not np.allclose(wrong_sums.to_numpy(), 100.0), \
        "the assertion CATCHES a mis-grouped denominator"

    print(f"  shares sum to {sums.round(6).to_dict()} -- with the grand total as")
    print(f"       the denominator they sum to {wrong_sums.round(2).to_dict()},")
    print(f"       which is exactly what the assertion is for")


def multi_key_and_level():
    h = pd.DataFrame({
        "dept": ["DS", "DS", "Stats", "Stats", "DS", "Stats"],
        "year": [1, 2, 1, 2, 1, 2],
        "marks": [88, 65, 94, 71, 52, 79]})

    two = h.groupby(["dept", "year"]).marks.mean()
    assert two.index.nlevels == 2
    assert two[("DS", 1)] == 70.0, "(88 + 52) / 2"

    idx = h.set_index(["dept", "year"])
    assert idx.groupby(level="dept").marks.mean().to_dict() == \
        h.groupby("dept").marks.mean().to_dict(), "grouping by LEVEL"

    print(f"  groupby(['dept','year']) -> a MultiIndex; ('DS', 1) = {two[('DS',1)]}")


def crosstab():
    h = pd.DataFrame({"dept": ["DS", "DS", "Stats", "Stats", "DS", "Stats"],
                      "year": [1, 2, 1, 2, 1, 2],
                      "marks": [88, 65, 94, 71, 52, 79]})

    c = pd.crosstab(h.dept, h.year)
    assert c.loc["DS", 1] == 2, "COUNTS by default"

    n = pd.crosstab(h.dept, h.year, normalize="index")
    assert np.allclose(n.sum(axis=1).to_numpy(), 1.0), "row proportions"

    v = pd.crosstab(h.dept, h.year, values=h.marks, aggfunc="mean")
    assert v.loc["DS", 1] == 70.0

    m = pd.crosstab(h.dept, h.year, margins=True)
    assert m.loc["All", "All"] == 6

    print("  crosstab: counts, normalize='index', values+aggfunc, margins")
    print("       the fastest route to Course 4's contingency tables")


def course4_recomputed():
    """Finding D8: Course 4's hand statistics, as one-line method calls."""
    x = COURSE4_SAMPLE
    assert x.tolist() == [2, 4, 4, 4, 5, 5, 7, 9]

    assert x.mean() == 5.0
    assert x.median() == 4.5
    assert x.mode()[0] == 4
    assert round(float(x.var()), 4) == 4.5714, "SAMPLE, ddof=1"
    assert x.var(ddof=0) == 4.0, "POPULATION"
    assert round(float(x.std()), 4) == 2.1381
    assert x.std(ddof=0) == 2.0

    # The library disagreement, asserted.
    assert float(np.std(x.to_numpy())) == 2.0, "numpy defaults to POPULATION"
    assert round(float(x.std()), 4) == 2.1381, "pandas defaults to SAMPLE"

    q = x.quantile([0.25, 0.5, 0.75])
    assert q[0.5] == 4.5

    d = x.describe()
    assert d["count"] == 8 and d["mean"] == 5.0
    assert round(float(d["std"]), 4) == 2.1381, "describe uses the SAMPLE sd"

    print(f"  Course 4 recomputed: mean {x.mean()}, median {x.median()}, "
          f"mode {x.mode()[0]}")
    print(f"       sample sd {x.std():.4f} (pandas) vs population "
          f"{np.std(x.to_numpy()):.1f} (numpy)")
    print(f"       describe() reports the SAMPLE sd -- which is Course 4's")


def correlation():
    df = students()
    c = df[["maths", "stats"]].corr()
    assert c.loc["maths", "stats"] == c.loc["stats", "maths"], "symmetric"
    assert np.allclose(np.diag(c.to_numpy()), 1.0)

    r = float(df.maths.corr(df.stats))
    assert 0.9 < r < 1.0, f"strongly positive here: {r:.4f}"

    sp = float(df.maths.corr(df.stats, method="spearman"))
    assert -1 <= sp <= 1

    print(f"  Pearson r = {r:.4f}, Spearman = {sp:.4f} -- Course 4 Unit 4, one call")


def main():
    print("Practical 17 -- Grouped summary statistics")
    split_apply_combine()
    size_versus_count()
    agg_transform_filter()
    group_shares_must_sum_to_100()
    multi_key_and_level()
    crosstab()
    course4_recomputed()
    correlation()


if __name__ == "__main__":
    main()
