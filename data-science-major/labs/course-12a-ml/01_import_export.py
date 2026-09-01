"""Experiment 1 — Import and export data with pandas.

The first practical, and the one that decides whether the rest of the course is
frustrating. Every format has a way of silently changing your data on the round
trip, and this script demonstrates each one failing and then fixing it.
"""
import io
import json
import pathlib
import tempfile

import pandas as pd

from fixtures import STUDY, churn

TMP = pathlib.Path(tempfile.mkdtemp(prefix="ml_lab1_"))


def csv_round_trip():
    path = TMP / "study.csv"
    STUDY.to_csv(path, index=False)
    back = pd.read_csv(path)

    assert back.shape == STUDY.shape == (10, 2)
    assert list(back.columns) == ["hours", "score"]
    assert back["score"].sum() == STUDY["score"].sum() == 710
    assert back.equals(STUDY)

    print(f"  CSV round trip: {back.shape}, score total {back['score'].sum()} -- identical")


def index_false_matters():
    """to_csv(index=True) adds a phantom column that read_csv turns into data."""
    with_index = TMP / "with_index.csv"
    STUDY.to_csv(with_index)                      # index=True is the DEFAULT
    back = pd.read_csv(with_index)

    assert back.shape == (10, 3), back.shape
    assert back.columns[0] == "Unnamed: 0", list(back.columns)

    fixed = pd.read_csv(with_index, index_col=0)
    assert fixed.shape == (10, 2)
    assert fixed.equals(STUDY)

    print(f"  to_csv() with the default index -> read back as {back.shape}, "
          f"first column '{back.columns[0]}'")
    print("       'Unnamed: 0' is the commonest junk column in data science.")
    print("       Write with index=False, or read with index_col=0")


def dtypes_are_not_preserved_by_csv():
    """CSV is text. Types are GUESSED on the way back in."""
    df = pd.DataFrame({"id": ["001", "002", "010"],
                       "flag": [True, False, True],
                       "when": pd.to_datetime(["2026-01-15", "2026-02-10", "2026-04-05"])})
    path = TMP / "types.csv"
    df.to_csv(path, index=False)
    back = pd.read_csv(path)

    # The zero-padded id became an integer and lost its padding.
    assert str(df["id"].dtype) == "str" or df["id"].dtype == object
    assert back["id"].tolist() == [1, 2, 10], back["id"].tolist()
    assert back["id"].tolist() != df["id"].tolist()

    # The date became a plain string. (In pandas 3 the string dtype prints as
    # "str" rather than the old "object" -- assert the property, not the name.)
    assert not pd.api.types.is_datetime64_any_dtype(back["when"])
    assert isinstance(back["when"].iloc[0], str), back["when"].iloc[0]

    fixed = pd.read_csv(path, dtype={"id": str}, parse_dates=["when"])
    assert fixed["id"].tolist() == ["001", "002", "010"]
    assert pd.api.types.is_datetime64_any_dtype(fixed["when"])

    print(f"  zero-padded id '001','002','010' -> read back as {back['id'].tolist()}")
    print(f"  dates -> dtype {back['when'].dtype} (text, not a date)")
    print("  with dtype={'id': str}, parse_dates=['when'] -> both correct")
    print("       CSV stores TEXT. Every type is re-guessed on read, and a")
    print("       pin code, phone number or account id loses its leading zeros")


def excel_and_multiple_sheets():
    path = TMP / "data.xlsx"
    with pd.ExcelWriter(path) as xl:
        STUDY.to_excel(xl, sheet_name="study", index=False)
        churn().head(20).to_excel(xl, sheet_name="churn", index=False)

    sheets = pd.read_excel(path, sheet_name=None)     # None -> a dict of ALL
    assert set(sheets) == {"study", "churn"}
    assert sheets["study"].shape == (10, 2)
    assert sheets["churn"].shape == (20, 4)

    one = pd.read_excel(path, sheet_name="study")
    assert one.equals(STUDY)

    print(f"  Excel: {len(sheets)} sheets -> {[f'{k} {v.shape}' for k, v in sheets.items()]}")
    print("       sheet_name=None returns a DICT of every sheet. Unlike CSV,")
    print("       Excel preserves dtypes, which is its one real advantage")


def json_orientations():
    """The 'orient' argument changes the file completely."""
    small = STUDY.head(3)
    shapes = {}
    for orient in ("records", "columns", "index", "split", "values"):
        text = small.to_json(orient=orient)
        shapes[orient] = len(text)
        if orient in ("records", "columns", "index", "split"):
            back = pd.read_json(io.StringIO(text), orient=orient)
            assert back.shape == small.shape, (orient, back.shape)

    assert json.loads(small.to_json(orient="records"))[0] == {"hours": 2, "score": 52}
    assert list(json.loads(small.to_json(orient="columns"))) == ["hours", "score"]

    print("  the same 3 rows, five JSON orientations:")
    for orient, size in shapes.items():
        print(f"    orient='{orient}':{'':<{10 - len(orient)}} {size} chars")
    print("       'records' is the one APIs use -- a list of objects. You must")
    print("       pass the SAME orient to read_json, or the frame comes back")
    print("       transposed or empty")


def parquet_preserves_everything():
    """The format to use between Python programs."""
    df = pd.DataFrame({"id": ["001", "002"],
                       "when": pd.to_datetime(["2026-01-15", "2026-02-10"]),
                       "flag": [True, False],
                       "value": [1.5, 2.5]})
    path = TMP / "data.parquet"
    try:
        df.to_parquet(path, index=False)
    except (ImportError, ValueError) as exc:
        print(f"  parquet unavailable ({type(exc).__name__}) -- skipped")
        return

    back = pd.read_parquet(path)
    assert back["id"].tolist() == ["001", "002"], "leading zeros SURVIVE"
    assert pd.api.types.is_datetime64_any_dtype(back["when"]), "dates survive"
    assert back["flag"].dtype == bool
    assert back.equals(df)

    csv_size = len(df.to_csv(index=False).encode())
    parquet_size = path.stat().st_size
    print(f"  Parquet: every dtype preserved, frame identical on round trip")
    print(f"    csv {csv_size} bytes, parquet {parquet_size} bytes "
          f"(parquet wins only on LARGE data -- it has a header)")
    print("       columnar, typed, compressed. Use it between programs;")
    print("       use CSV only when a human or a foreign tool must read it")


def reading_a_subset_of_a_large_file():
    """usecols and nrows -- what you do when the file will not fit."""
    big = churn(n=400)
    path = TMP / "big.csv"
    big.to_csv(path, index=False)

    head = pd.read_csv(path, nrows=5)
    assert head.shape == (5, 4)

    two_cols = pd.read_csv(path, usecols=["tenure_months", "churned"])
    assert two_cols.shape == (400, 2), two_cols.shape

    chunks = list(pd.read_csv(path, chunksize=150))
    assert [len(c) for c in chunks] == [150, 150, 100]
    assert sum(len(c) for c in chunks) == 400

    print(f"  nrows=5              -> {head.shape}")
    print(f"  usecols=[2 columns]  -> {two_cols.shape}")
    print(f"  chunksize=150        -> {[len(c) for c in chunks]} rows per chunk")
    print("       read the head FIRST to see the columns, then usecols to load")
    print("       only what you need. chunksize when it will not fit in memory")


def main():
    print("Experiment 1 -- Importing and exporting data with pandas")
    csv_round_trip()
    index_false_matters()
    dtypes_are_not_preserved_by_csv()
    excel_and_multiple_sheets()
    json_orientations()
    parquet_preserves_everything()
    reading_a_subset_of_a_large_file()


if __name__ == "__main__":
    main()
