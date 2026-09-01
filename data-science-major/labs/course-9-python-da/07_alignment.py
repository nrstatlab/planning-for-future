"""Practical 7 — Arithmetic and data alignment between Series and DataFrames.

Alignment is the feature that most distinguishes Pandas from NumPy, and the
one that turns a whole class of silent bugs into visible NaNs.
"""
import numpy as np
import pandas as pd
from fixtures import students


def alignment_is_by_label():
    a = pd.Series([10, 20, 30], index=["x", "y", "z"])
    b = pd.Series([1, 2, 3, 4], index=["w", "x", "y", "z"])

    r = a + b
    assert r.index.tolist() == ["w", "x", "y", "z"], "the UNION of both indexes"
    assert np.isnan(r["w"]), "w is in b only"
    assert r["x"] == 12 and r["y"] == 23 and r["z"] == 34
    assert r.dtype == np.float64, "NaN is a float, so the result is float64"

    # The decisive point: x sits at position 0 in a and position 1 in b, yet
    # the answer is right, because Pandas matched LABEL to LABEL.
    assert a.index.get_loc("x") == 0
    assert b.index.get_loc("x") == 1

    # NumPy, with no labels, would have added mismatched pairs -- and produced
    # a plausible, wrong answer with no warning at all.
    common = ["x", "y", "z"]
    positional = a.to_numpy() + b.to_numpy()[:3]
    assert positional.tolist() == [11, 22, 33], "wrong, and silently so"
    assert a.add(b)[common].tolist() == [12.0, 23.0, 34.0], "right"

    print(f"  a + b -> {dict(zip(r.index, [None if pd.isna(v) else v for v in r]))}")
    print(f"       positional would give {positional.tolist()} -- plausible and WRONG")


def fill_value():
    a = pd.Series([10, 20, 30], index=["x", "y", "z"])
    b = pd.Series([1, 2, 3, 4], index=["w", "x", "y", "z"])

    r = a.add(b, fill_value=0)
    assert r["w"] == 1, "0 + 1"
    assert r["x"] == 12 and r["y"] == 23 and r["z"] == 34
    assert not r.isna().any()

    assert a.sub(b, fill_value=0)["w"] == -1
    assert a.mul(b, fill_value=1)["w"] == 1

    print(f"  fill_value=0 -> w = {r['w']}, and no NaN remains")


def dataframe_series_arithmetic():
    df = students().set_index("name")[["maths", "stats"]]

    doubled = df * 2
    assert doubled.loc["Asha", "maths"] == 176

    # By DEFAULT a DataFrame-Series operation matches the Series' index against
    # the DataFrame's COLUMNS and broadcasts down the rows.
    centred_cols = df - df.mean()
    assert centred_cols.shape == df.shape
    assert abs(centred_cols.maths.mean()) < 1e-12, "each column now has mean 0"

    # To match against the INDEX instead, pass axis=0.
    centred_rows = df.sub(df.mean(axis=1), axis=0)
    assert centred_rows.shape == df.shape
    assert abs(centred_rows.loc["Asha"].mean()) < 1e-12, "each ROW now has mean 0"

    print("  df - df.mean() centres COLUMNS; df.sub(df.mean(axis=1), axis=0) centres ROWS")


def alignment_across_dataframes():
    a = pd.DataFrame({"x": [1, 2], "y": [3, 4]}, index=["p", "q"])
    b = pd.DataFrame({"y": [10, 20], "z": [30, 40]}, index=["q", "r"])

    r = a + b
    assert sorted(r.columns) == ["x", "y", "z"], "union of COLUMNS"
    assert sorted(r.index) == ["p", "q", "r"], "union of INDEX"
    assert r.loc["q", "y"] == 14, "the only cell present in both"
    assert r.isna().sum().sum() == 8, "every other cell is NaN"

    print(f"  DataFrame + DataFrame aligns on BOTH axes: only ('q','y') overlaps")


def main():
    print("Practical 7 -- Arithmetic and data alignment")
    alignment_is_by_label()
    fill_value()
    dataframe_series_arithmetic()
    alignment_across_dataframes()


if __name__ == "__main__":
    main()
