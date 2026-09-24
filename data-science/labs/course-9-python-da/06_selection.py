"""Practical 6 — Indexing, selection, filtering and boolean indexing."""
import warnings
import numpy as np
import pandas as pd
from fixtures import students


def three_accessors():
    df = students()

    assert isinstance(df["maths"], pd.Series), "one column -> Series"
    assert isinstance(df[["maths", "stats"]], pd.DataFrame), "a list -> DataFrame"

    assert df.loc[0, "maths"] == 88
    assert df.iloc[0, 3] == 88
    assert df.at[0, "maths"] == 88
    assert df.iat[0, 3] == 88
    assert df.iloc[-1]["name"] == "Bhanu"

    print("  [] selects columns; .loc by label; .iloc by position; .at/.iat one cell")


def loc_is_inclusive_iloc_is_not():
    """The asymmetry that looks like a bug and is deliberate."""
    df = students()
    assert len(df.loc[0:2]) == 3, "labels INCLUSIVE"
    assert len(df.iloc[0:2]) == 2, "positions EXCLUSIVE"

    # With labels you often do not know what follows, so an exclusive endpoint
    # would make a column slice unusable.
    cols = df.loc[:, "name":"maths"].columns.tolist()
    assert cols == ["name", "dept", "maths"], "'maths' is INCLUDED"

    print("  .loc[0:2] -> 3 rows; .iloc[0:2] -> 2 rows; labels inclusive, positions not")


def filtering():
    df = students()

    assert df[df.maths > 70].name.tolist() == ["Asha", "Meena", "Kiran"]
    assert df[(df.maths > 70) & (df.dept == "DS")].name.tolist() == ["Asha", "Kiran"]
    assert df[df.dept.isin(["Stats"])].name.tolist() == ["Meena", "Bhanu"]
    assert df[~df.dept.isin(["Stats"])].shape[0] == 3
    assert df[df.maths.between(60, 90)].name.tolist() == ["Asha", "Ravi", "Kiran"]
    assert df[df.name.str.startswith("A")].name.tolist() == ["Asha"]

    # query() gives the same answer, more readably
    a = df[(df.maths > 70) & (df.dept == "DS")]
    b = df.query("maths > 70 and dept == 'DS'")
    assert a.equals(b)

    threshold = 70
    assert df.query("maths > @threshold").shape[0] == 3, "@ refers to a Python variable"

    print("  filters agree between & and query(); between() is inclusive both ends")


def and_raises():
    df = students()
    try:
        df[(df.maths > 70) and (df.dept == "DS")]
        raise AssertionError("expected ValueError")
    except ValueError as e:
        assert "ambiguous" in str(e)
    print("  `and` raises 'truth value is ambiguous' -- use & with parentheses")


def setting_with_copy():
    """Pandas 3 changed this. Know exactly how."""
    df = students()
    before = df.loc[df.dept == "DS", "maths"].tolist()
    assert before == [88, 65, 71]

    sub = df[df.dept == "DS"]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        sub["maths"] = 100
    warned = [w for w in caught if "SettingWithCopy" in w.category.__name__]

    # Pandas 3: copy-on-write means NO warning AND the original is untouched.
    assert df.loc[df.dept == "DS", "maths"].tolist() == before, \
        "the original must be unchanged under copy-on-write"
    assert warned == [], "Pandas 3 no longer warns -- the bug is now SILENT"

    # Correct form 1: modify the original, in ONE .loc
    d1 = students()
    d1.loc[d1.dept == "DS", "maths"] = 100
    assert d1.loc[d1.dept == "DS", "maths"].tolist() == [100, 100, 100]

    # Correct form 2: work separately, and say so
    d2 = students()
    part = d2[d2.dept == "DS"].copy()
    part["maths"] = 100
    assert d2.loc[d2.dept == "DS", "maths"].tolist() == before, "d2 untouched, intentionally"

    print("  Pandas 3: chained assignment leaves the original UNCHANGED and")
    print("       raises NO warning -- it now fails silently and completely")
    print("       fix 1: df.loc[mask, 'col'] = x    fix 2: .copy() first")


def main():
    print("Practical 6 -- Selection and filtering")
    three_accessors()
    loc_is_inclusive_iloc_is_not()
    filtering()
    and_raises()
    setting_with_copy()


if __name__ == "__main__":
    main()
