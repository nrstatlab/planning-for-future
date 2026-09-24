"""Practical 9 — Read and write data in CSV, TXT, JSON and Excel formats.

Every format is round-tripped through a temporary directory and asserted equal
to what went in, and the four traps that bite on real files are demonstrated.
"""
import io
import json
import tempfile
import pathlib
import numpy as np
import pandas as pd
from fixtures import students


def round_trips(tmp):
    df = students()

    csv = tmp / "students.csv"
    df.to_csv(csv, index=False)
    assert pd.read_csv(csv).equals(df), "CSV round trip"

    txt = tmp / "students.txt"
    df.to_csv(txt, sep="\t", index=False)
    assert pd.read_csv(txt, sep="\t").equals(df), "tab-separated round trip"

    js = tmp / "students.json"
    df.to_json(js, orient="records", indent=2)
    back = pd.read_json(js, orient="records")
    assert back[df.columns].equals(df), "JSON round trip"

    try:
        xl = tmp / "students.xlsx"
        df.to_excel(xl, index=False, sheet_name="Sem4")
        assert pd.read_excel(xl, sheet_name="Sem4").equals(df), "Excel round trip"
        excel = "yes"
    except ImportError:
        excel = "skipped (openpyxl not installed)"

    print(f"  round trips: CSV ok, TXT ok, JSON ok, Excel {excel}")


def index_false_matters(tmp):
    df = students()
    f = tmp / "with_index.csv"

    df.to_csv(f)                                  # no index=False
    assert "Unnamed: 0" in pd.read_csv(f).columns, "an unnamed column appears"

    df.to_csv(f, index=False)
    assert "Unnamed: 0" not in pd.read_csv(f).columns

    print("  index=False: without it every write adds an 'Unnamed: 0' column")


def the_four_traps(tmp):
    f = tmp / "messy.csv"
    f.write_text(
        "roll,name,marks,exam_date\n"
        "007,Asha,88,26-08-2026\n"
        "008,Ravi,-,27-08-2026\n"
        "009,Meena,94,28-08-2026\n")

    naive = pd.read_csv(f)

    # 1. Leading zeros are lost
    assert naive.roll.iloc[0] == 7, "'007' became the integer 7"
    fixed = pd.read_csv(f, dtype={"roll": str})
    assert fixed.roll.iloc[0] == "007", "dtype=str preserves them"

    # 2. Dates are strings. (Pandas 3 reads text as the new `str` dtype where
    # older versions used `object`; either way it is NOT a datetime.)
    assert not pd.api.types.is_datetime64_any_dtype(naive.exam_date)
    assert str(naive.exam_date.dtype) in ("object", "str")
    dated = pd.read_csv(f, parse_dates=["exam_date"], date_format="%d-%m-%Y")
    assert pd.api.types.is_datetime64_any_dtype(dated.exam_date)
    assert dated.exam_date.iloc[0].year == 2026 and dated.exam_date.iloc[0].month == 8

    # 3. A "-" makes a numeric column TEXT
    assert not pd.api.types.is_numeric_dtype(naive.marks), \
        "one '-' and the whole column is text, not numbers"
    clean = pd.read_csv(f, na_values=["-"])
    assert clean.marks.dtype == np.float64
    assert clean.marks.isna().sum() == 1

    # 4. Ambiguous date order -- without date_format, 03-04 could be either
    g = tmp / "ambig.csv"
    g.write_text("d\n03-04-2026\n")
    uk = pd.read_csv(g, parse_dates=["d"], date_format="%d-%m-%Y").d.iloc[0]
    us = pd.read_csv(g, parse_dates=["d"], date_format="%m-%d-%Y").d.iloc[0]
    assert uk.month == 4 and us.month == 3, "the same text, two different dates"

    print("  traps: '007' -> 7; dates -> strings; one '-' -> a TEXT column;")
    print("       03-04-2026 is 3 April or 4 March depending on date_format")


def json_normalize_flattens_nesting():
    """Course 7 Unit 5's nested college document -- and Course 10's shape."""
    raw = {
        "college": "NRI",
        "students": [
            {"roll": 21, "name": "Asha", "marks": {"maths": 88, "stats": 91}},
            {"roll": 22, "name": "Ravi", "marks": {"maths": 65, "stats": 58}},
        ],
    }

    flat = pd.json_normalize(raw["students"])
    assert list(flat.columns) == ["roll", "name", "marks.maths", "marks.stats"]
    assert flat["marks.maths"].tolist() == [88, 65]

    # read_json on the same structure leaves 'marks' as a column of DICTS,
    # which you cannot compute with.
    nested = pd.read_json(io.StringIO(json.dumps(raw["students"])))
    assert isinstance(nested.marks.iloc[0], dict)

    print("  json_normalize -> dotted columns ('marks.maths'); read_json leaves dicts")
    print("       this is the bridge from Course 7's JSON and Course 10's documents")


def main():
    print("Practical 9 -- Reading and writing data")
    with tempfile.TemporaryDirectory() as d:
        tmp = pathlib.Path(d)
        round_trips(tmp)
        index_false_matters(tmp)
        the_four_traps(tmp)
    json_normalize_flattens_nesting()


if __name__ == "__main__":
    main()
