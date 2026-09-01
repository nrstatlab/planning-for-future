"""Practical 16 — Reshape with pivot, stack, unstack; hierarchical indexing."""
import numpy as np
import pandas as pd

LONG = pd.DataFrame({
    "name":    ["Asha", "Asha", "Ravi", "Ravi", "Meena", "Meena"],
    "subject": ["maths", "stats"] * 3,
    "marks":   [88, 91, 65, 58, 94, 89],
})

HIER = pd.DataFrame({
    "dept":    ["DS", "DS", "Stats", "Stats", "DS", "Stats"],
    "year":    [1, 2, 1, 2, 1, 2],
    "student": ["Asha", "Ravi", "Meena", "Kiran", "Bhanu", "Devi"],
    "marks":   [88, 65, 94, 71, 52, 79],
})


def long_to_wide_and_back():
    wide = LONG.pivot(index="name", columns="subject", values="marks")
    assert wide.shape == (3, 2)
    assert wide.index.tolist() == ["Asha", "Meena", "Ravi"], "pivot SORTS the index"
    assert wide.loc["Asha", "maths"] == 88

    back = wide.reset_index().melt(id_vars="name", var_name="subject",
                                   value_name="marks")
    assert len(back) == 6, "six rows again"

    # Same data, different ORDER -- compare after sorting, not directly.
    a = back.sort_values(["name", "subject"]).reset_index(drop=True)
    b = LONG.sort_values(["name", "subject"]).reset_index(drop=True)
    assert a.equals(b), "a genuine round trip"

    print("  long -> wide -> long round-trips (after sorting: pivot reorders)")


def pivot_refuses_duplicates():
    dup = pd.concat([LONG, pd.DataFrame({"name": ["Asha"], "subject": ["maths"],
                                         "marks": [95]})], ignore_index=True)
    try:
        dup.pivot(index="name", columns="subject", values="marks")
        raise AssertionError("expected ValueError on duplicates")
    except ValueError as e:
        assert "duplicate" in str(e).lower()

    avg = dup.pivot_table(index="name", columns="subject", values="marks",
                          aggfunc="mean")
    assert avg.loc["Asha", "maths"] == 91.5, "silently AVERAGED 88 and 95"

    mx = dup.pivot_table(index="name", columns="subject", values="marks",
                         aggfunc="max")
    assert mx.loc["Asha", "maths"] == 95, "or take the re-sit, if that is the rule"

    print("  pivot RAISES on a duplicated (name, subject); pivot_table gives")
    print("       91.5 with the default mean or 95 with max -- which is right is")
    print("       a question about your DATA, and the default answers it for you")


def pivot_table_margins():
    t = pd.pivot_table(HIER, index="dept", columns="year", values="marks",
                       aggfunc="mean", margins=True, margins_name="All")
    assert "All" in t.index and "All" in t.columns
    assert round(float(t.loc["All", "All"]), 4) == round(HIER.marks.mean(), 4)

    multi = pd.pivot_table(HIER, index="dept", values="marks",
                           aggfunc=["mean", "count"])
    assert multi.columns.nlevels == 2, "several aggfuncs -> a MultiIndex on columns"

    print(f"  margins=True adds the grand total: {t.loc['All','All']:.4f}")


def hierarchical_indexing():
    h = HIER.set_index(["dept", "year"])

    # Slicing a MultiIndex requires it to be LEXICALLY SORTED.
    try:
        h.loc["DS":"Stats"]
        raise AssertionError("expected UnsortedIndexError")
    except pd.errors.UnsortedIndexError:
        pass

    hs = h.sort_index()
    assert len(hs.loc["DS":"Stats"]) == 6
    assert len(hs.loc["DS"]) == 3
    assert len(hs.loc[("DS", 1)]) == 2, "a TUPLE selects both levels"

    assert hs.index.names == ["dept", "year"]
    assert hs.index.nlevels == 2

    xs = hs.xs(1, level="year")
    assert len(xs) == 3, "cross-section: year 1, all departments"
    assert len(hs.loc[(slice(None), 1), :]) == 3, "the same with slice(None)"
    assert len(hs.loc[pd.IndexSlice[:, 1], :]) == 3, "and with IndexSlice"

    assert hs.reset_index().shape == HIER.shape
    assert hs.swaplevel().index.names == ["year", "dept"]

    print("  slicing an UNSORTED MultiIndex raises UnsortedIndexError --")
    print("       .sort_index() right after .set_index() is the habit to form")


def stack_and_unstack():
    wide = LONG.pivot(index="name", columns="subject", values="marks")

    stacked = wide.stack()
    assert isinstance(stacked, pd.Series) and len(stacked) == 6
    assert stacked.index.nlevels == 2, "columns became an INNER index level"

    assert stacked.unstack().equals(wide), "a round trip"

    # unstack refuses duplicates for exactly the same reason pivot does:
    # HIER has two DS/year-1 students and two Stats/year-2 students.
    h = HIER.set_index(["dept", "year"]).sort_index()
    try:
        h.unstack("year")
        raise AssertionError("expected a duplicate-entries ValueError")
    except ValueError as e:
        assert "duplicate" in str(e).lower()

    # Aggregate to unique pairs first, and it works.
    agg = h.groupby(level=["dept", "year"]).marks.mean().unstack("year")
    assert agg.loc["DS", 1] == 70.0, "(88 + 52) / 2"
    assert agg.loc["Stats", 2] == 75.0, "(71 + 79) / 2"
    assert agg.index.tolist() == ["DS", "Stats"]

    # On a subset with unique pairs, the MultiIndex-on-columns shape appears.
    uniq = h[h.student.isin(["Asha", "Ravi", "Meena", "Kiran"])].unstack("year")
    assert uniq.columns.nlevels == 2, "a row level was pushed UP into the columns"
    assert uniq.index.tolist() == ["DS", "Stats"]
    assert uniq.loc["DS", ("student", 1)] == "Asha"

    u0 = h.groupby(level=["dept", "year"]).marks.mean().unstack(level=0)
    assert u0.index.name == "year"

    print("  stack makes it TALLER, unstack makes it WIDER -- and unstack")
    print("       REFUSES duplicates just as pivot does; aggregate first")


def combining_with_overlap():
    a = pd.Series([1, np.nan, 3, np.nan])
    b = pd.Series([10, 20, 30, 40])

    assert a.combine_first(b).tolist() == [1.0, 20.0, 3.0, 40.0], "fill MY gaps"

    d1 = pd.DataFrame({"x": [1, np.nan], "y": [3, 4]})
    d2 = pd.DataFrame({"x": [10, 20], "y": [30, 40]})

    cf = d1.combine_first(d2)
    assert cf.x.tolist() == [1.0, 20.0], "only the gap was filled"
    assert cf.y.tolist() == [3, 4], "y had no gaps, so d2 is ignored"

    up = d1.copy()
    result = up.update(d2)
    assert result is None, "update returns None -- it modifies IN PLACE"
    assert up.x.tolist() == [10.0, 20.0], "update OVERWRITES, it does not fill"
    assert up.y.tolist() == [30.0, 40.0]

    print("  combine_first fills MY gaps and returns a new object;")
    print("       update OVERWRITES in place and returns None")


def main():
    print("Practical 16 -- Reshaping and hierarchical indexing")
    long_to_wide_and_back()
    pivot_refuses_duplicates()
    pivot_table_margins()
    hierarchical_indexing()
    stack_and_unstack()
    combining_with_overlap()


if __name__ == "__main__":
    main()
