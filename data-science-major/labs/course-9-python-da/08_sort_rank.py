"""Practical 8 — Sorting, ranking, dropping entries and duplicate indexes."""
import numpy as np
import pandas as pd
from fixtures import students


def sorting():
    df = students()
    assert df.sort_values("maths").name.tolist() == \
        ["Bhanu", "Ravi", "Kiran", "Asha", "Meena"]
    assert df.sort_values("maths", ascending=False).name.iloc[0] == "Meena"

    multi = df.sort_values(["dept", "maths"], ascending=[True, False])
    assert multi.name.tolist() == ["Asha", "Kiran", "Ravi", "Meena", "Bhanu"]

    assert df.nlargest(3, "maths").name.tolist() == ["Meena", "Asha", "Kiran"]
    assert df.nsmallest(2, "maths").name.tolist() == ["Bhanu", "Ravi"]

    # NaN placement
    d = df.copy()
    d.loc[0, "maths"] = np.nan
    assert pd.isna(d.sort_values("maths").maths.iloc[-1]), "NaN sorts LAST by default"
    assert pd.isna(d.sort_values("maths", na_position="first").maths.iloc[0])

    print("  sort_values, multi-key with per-key direction, nlargest, NaN placement")


def ranking():
    """The tie-breaking methods -- the whole examinable point."""
    s = pd.Series([70, 85, 70, 92, 60])

    expected = {
        "average": [2.5, 4.0, 2.5, 5.0, 1.0],
        "min":     [2.0, 4.0, 2.0, 5.0, 1.0],
        "max":     [3.0, 4.0, 3.0, 5.0, 1.0],
        "first":   [2.0, 4.0, 3.0, 5.0, 1.0],
        "dense":   [2.0, 3.0, 2.0, 4.0, 1.0],
    }
    for method, want in expected.items():
        got = s.rank(method=method).tolist()
        assert got == want, f"{method}: {got} != {want}"

    assert s.rank().tolist() == expected["average"], "average is the DEFAULT"
    assert s.rank(ascending=False).tolist() == [3.5, 2.0, 3.5, 1.0, 5.0]
    assert s.rank(pct=True).max() == 1.0

    # min leaves a GAP after ties; dense does not.
    assert 3.0 not in expected["min"], "min: 1, 2, 2, 4 -- a gap at 3"
    assert 3.0 in expected["dense"], "dense: 1, 2, 2, 3 -- no gap"

    print("  ranking [70,85,70,92,60], the two 70s get:")
    for method, want in expected.items():
        print(f"    {method:8s} {want}")


def dropping():
    df = students()

    assert len(df.drop(0)) == 4
    assert len(df.drop([0, 2])) == 3
    assert "maths" not in df.drop(columns="maths").columns
    assert "maths" not in df.drop("maths", axis=1).columns

    # drop returns a COPY -- df itself is unchanged
    df.drop(columns="maths")
    assert "maths" in df.columns, "drop does NOT modify in place"

    d = df.copy()
    d.loc[0, "maths"] = np.nan
    d.loc[1, ["maths", "stats"]] = np.nan
    assert len(d.dropna()) == 3, "any NaN in the row removes it"
    assert len(d.dropna(subset=["stats"])) == 4
    # Row 0 has 4 non-null values and row 1 has 3; the rest have all 5.
    assert d.notna().sum(axis=1).tolist() == [4, 3, 5, 5, 5]
    assert len(d.dropna(thresh=4)) == 4, "keep rows with >= 4 non-null values"
    assert len(d.dropna(thresh=5)) == 3, "keep only complete rows"

    print("  drop returns a COPY; dropna(subset=) and thresh= narrow the criterion")


def duplicate_indexes():
    """The return TYPE depends on the data, which is why code breaks later."""
    s = pd.Series([1, 2, 3, 4], index=["a", "a", "b", "c"])

    assert s.index.is_unique is False
    assert isinstance(s["a"], pd.Series) and len(s["a"]) == 2
    assert np.isscalar(s["b"]) or isinstance(s["b"], (int, np.integer))

    assert s.index.duplicated().tolist() == [False, True, False, False]
    assert len(s[~s.index.duplicated(keep="first")]) == 3

    print("  duplicate index: s['a'] -> a SERIES, s['b'] -> a SCALAR")
    print("       code written against a unique index breaks when one appears")


def duplicate_rows():
    df = pd.DataFrame({
        "roll": [21, 22, 21, 23, 22],
        "name": ["Asha", "Ravi", "Asha", "Meena", "Ravi Teja"],
        "marks": [88, 65, 88, 94, 65],
    })

    assert df.duplicated().sum() == 1, "only row 2 is a FULL duplicate"
    assert df.duplicated(subset=["roll"]).sum() == 2, "two rolls repeat"
    assert df.duplicated(subset=["roll"], keep=False).sum() == 4, \
        "keep=False marks ALL members of every duplicate group"

    assert len(df.drop_duplicates()) == 4
    assert len(df.drop_duplicates(subset=["roll"])) == 3, "one row per student"
    assert df.drop_duplicates(subset=["roll"], keep="last").name.tolist() == \
        ["Asha", "Meena", "Ravi Teja"]

    print("  duplicated(): 1 full duplicate, but 2 duplicated ROLLS --")
    print("       'Ravi' and 'Ravi Teja' are the same student with a typo, and")
    print("       a bare drop_duplicates() would miss it. Specify the subset.")


def main():
    print("Practical 8 -- Sorting, ranking, dropping, duplicates")
    sorting()
    ranking()
    dropping()
    duplicate_indexes()
    duplicate_rows()


if __name__ == "__main__":
    main()
