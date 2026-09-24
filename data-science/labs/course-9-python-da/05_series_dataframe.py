"""Practical 5 — Create and manipulate Pandas Series and DataFrames."""
import numpy as np
import pandas as pd
from fixtures import students


def series_creation():
    s = pd.Series([72, 45, 91, 66],
                  index=["Asha", "Ravi", "Meena", "Kiran"], name="marks")
    assert s.shape == (4,)
    assert s.name == "marks"
    assert s.index.tolist() == ["Asha", "Ravi", "Meena", "Kiran"]
    assert s["Asha"] == 72, "by LABEL"
    assert s.iloc[0] == 72, "by POSITION"
    assert "Asha" in s, "`in` checks the INDEX, like a dict"
    assert s[s > 60].tolist() == [72, 91, 66]

    assert pd.Series([1, 2, 3]).index.tolist() == [0, 1, 2], "default RangeIndex"
    assert pd.Series({"a": 1, "b": 2}).index.tolist() == ["a", "b"], "dict keys"
    assert pd.Series(5, index=["a", "b", "c"]).tolist() == [5, 5, 5], "scalar broadcasts"

    print(f"  Series: {s.shape[0]} labelled values, array-like and dict-like at once")


def dataframe_creation():
    """A dict gives COLUMNS; a list of lists gives ROWS."""
    by_cols = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    by_rows = pd.DataFrame([[1, 3], [2, 4]], columns=["a", "b"])
    by_dicts = pd.DataFrame([{"a": 1, "b": 3}, {"a": 2, "b": 4}])

    assert by_cols.equals(by_rows), "the same table, built two ways"
    assert by_cols.equals(by_dicts)
    assert by_cols.shape == (2, 2)

    # Getting it the wrong way round transposes the table.
    wrong = pd.DataFrame([[1, 2], [3, 4]], columns=["a", "b"])
    assert wrong.a.tolist() == [1, 3], "rows, not columns"
    assert not wrong.equals(by_cols) or True

    print("  DataFrame: dict -> columns, list of lists -> rows, list of dicts -> rows")


def attributes_and_inspection():
    df = students()
    assert df.shape == (5, 5), "5 students, 5 columns"
    assert df.size == 25
    assert list(df.columns) == ["roll", "name", "dept", "maths", "stats"]
    assert df.index.tolist() == [0, 1, 2, 3, 4]

    assert len(df.head(2)) == 2
    assert len(df.tail(3)) == 3
    assert df.dept.value_counts().to_dict() == {"DS": 3, "Stats": 2}
    assert df.nunique().dept == 2
    assert df.isna().sum().sum() == 0

    d = df.describe()
    assert "mean" in d.index and "50%" in d.index
    assert round(float(d.loc["mean", "maths"]), 2) == 74.00

    print(f"  shape {df.shape}, dtypes {df.dtypes.nunique()} distinct, "
          f"dept counts {df.dept.value_counts().to_dict()}")
    print(f"       df.info() is the FIRST thing to run: dtypes and non-null "
          f"counts together")


def index_objects():
    df = students()
    d2 = df.set_index("name")
    assert d2.index.name == "name"
    assert d2.loc["Asha", "maths"] == 88
    # reset_index puts the label back as the FIRST column
    assert list(d2.reset_index().columns)[0] == "name"

    # The Index is IMMUTABLE
    try:
        df.index[0] = "x"
        raise AssertionError("expected a TypeError")
    except TypeError:
        pass

    # ...but replacing the whole index is fine
    d3 = df.copy()
    d3.index = list("abcde")
    assert d3.index.tolist() == list("abcde")

    assert "mathematics" in df.rename(columns={"maths": "mathematics"}).columns

    print("  Index is immutable (set_index/reset_index/rename replace it wholesale)")


def new_columns():
    df = students()
    df["total"] = df.maths + df.stats
    assert df.total.tolist() == [179, 123, 183, 137, 99]

    df["avg"] = df[["maths", "stats"]].mean(axis=1)
    assert df.avg.iloc[0] == 89.5

    # Attribute assignment does NOT create a column.
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df.newcol = 0
    assert "newcol" not in df.columns, "df.newcol = 0 sets an ATTRIBUTE, not a column"
    df["newcol"] = 0
    assert "newcol" in df.columns

    print(f"  totals {df.total.tolist()}; df['x'] = ... creates a column, df.x = ... does not")


def main():
    print("Practical 5 -- Series and DataFrame")
    series_creation()
    dataframe_creation()
    attributes_and_inspection()
    index_objects()
    new_columns()


if __name__ == "__main__":
    main()
