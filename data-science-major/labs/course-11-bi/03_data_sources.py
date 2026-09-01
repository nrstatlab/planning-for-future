"""Experiment 3 — Connecting to different data sources.

The Power BI half is a click-path (Get Data -> Excel / Text-CSV / Web) and is
written out in lab.md. What runs here is the part that actually matters and
that students get wrong: every format has a failure mode, and the failure is
silent. Each one below is DEMONSTRATED failing and then fixed.
"""
import io
import json
import pathlib
import tempfile

import pandas as pd

from fixtures import DIM_STORE, FACT_SALES

TMP = pathlib.Path(tempfile.mkdtemp(prefix="bi_lab3_"))


def csv_round_trip():
    """The baseline: write a CSV, read it back, prove nothing changed."""
    path = TMP / "sales.csv"
    FACT_SALES.to_csv(path, index=False)
    back = pd.read_csv(path)

    assert back.shape == FACT_SALES.shape, (back.shape, FACT_SALES.shape)
    assert list(back.columns) == list(FACT_SALES.columns)
    assert back["qty"].sum() == FACT_SALES["qty"].sum() == 87

    print(f"  CSV      {back.shape[0]} rows x {back.shape[1]} cols, qty total "
          f"{back['qty'].sum()} -- unchanged")


def the_delimiter_trap():
    """A semicolon CSV read as comma-separated: ONE column, no error."""
    text = "store_key;store;region\nT1;Vijayawada;South\nT2;Guntur;South\n"

    wrong = pd.read_csv(io.StringIO(text))
    assert wrong.shape[1] == 1, wrong.shape
    assert wrong.columns[0] == "store_key;store;region"

    right = pd.read_csv(io.StringIO(text), sep=";")
    assert right.shape == (2, 3), right.shape
    assert list(right.columns) == ["store_key", "store", "region"]

    print(f"  semicolon CSV read as comma -> {wrong.shape[1]} column, NO ERROR")
    print(f"  the same file with sep=';'   -> {right.shape[1]} columns")
    print("       Power BI shows this in the preview pane. LOOK at the preview")
    print("       before pressing Load -- it is the whole point of that screen")


def the_encoding_trap():
    """UTF-8 written, Latin-1 read: names silently mangled, no exception."""
    names = pd.DataFrame({"store": ["Vijayawāda", "Guntūr"]})
    path = TMP / "names.csv"
    names.to_csv(path, index=False, encoding="utf-8")

    right = pd.read_csv(path, encoding="utf-8")
    wrong = pd.read_csv(path, encoding="latin-1")

    assert list(right["store"]) == ["Vijayawāda", "Guntūr"]
    assert list(wrong["store"]) != list(right["store"])
    assert "Ä" in wrong["store"][0] or "Å" in wrong["store"][0], wrong["store"][0]

    print(f"  utf-8 file read as utf-8    -> {right['store'][0]}")
    print(f"  the SAME file read as latin-1 -> {wrong['store'][0]}")
    print("       no exception, no warning. This is why the encoding dropdown")
    print("       exists, and why you check a name with an accent in it")


def excel_sheet_versus_table():
    """A sheet brings the title row and the blank line. A named table does not."""
    path = TMP / "report.xlsx"
    with pd.ExcelWriter(path) as xl:
        # A sheet as a human would lay it out: title, blank row, then data.
        messy = pd.DataFrame(
            [["Monthly Sales Report", None, None],
             [None, None, None],
             ["store_key", "store", "region"],
             ["T1", "Vijayawada", "South"],
             ["T2", "Guntur", "South"]])
        messy.to_excel(xl, sheet_name="Report", index=False, header=False)
        DIM_STORE.to_excel(xl, sheet_name="Clean", index=False)

    raw = pd.read_excel(path, sheet_name="Report")
    assert raw.columns[0] == "Monthly Sales Report", list(raw.columns)
    assert raw.shape[0] == 4, raw.shape

    fixed = pd.read_excel(path, sheet_name="Report", skiprows=2)
    assert list(fixed.columns) == ["store_key", "store", "region"], list(fixed.columns)
    assert fixed.shape[0] == 2

    clean = pd.read_excel(path, sheet_name="Clean")
    assert list(clean.columns) == list(DIM_STORE.columns)
    assert clean.shape == DIM_STORE.shape

    print(f"  sheet as-is      -> header is '{raw.columns[0]}', {raw.shape[0]} junk rows")
    print(f"  skiprows=2       -> {list(fixed.columns)}")
    print(f"  a proper table   -> {clean.shape[0]} rows, correct headers immediately")
    print("       in Power BI: pick the TABLE in the navigator, not the sheet.")
    print("       If there is no table, 'Use First Row as Headers' + Remove Top Rows")


def web_api_json_is_nested():
    """A Web API returns nested JSON. Expanding it is the whole task."""
    payload = {
        "meta": {"generated": "2026-08-27", "count": 2},
        "results": [
            {"store": {"key": "T1", "name": "Vijayawada"},
             "sales": [{"product": "P1", "qty": 10}, {"product": "P3", "qty": 5}]},
            {"store": {"key": "T2", "name": "Guntur"},
             "sales": [{"product": "P2", "qty": 8}]},
        ],
    }
    path = TMP / "api.json"
    path.write_text(json.dumps(payload))
    doc = json.loads(path.read_text())

    # Reading it naively gives one row per result with objects inside cells.
    naive = pd.DataFrame(doc["results"])
    assert isinstance(naive["store"][0], dict), "the cell holds a DICT, not a value"
    assert isinstance(naive["sales"][0], list), "and this one holds a LIST"

    # json_normalize with record_path is the fix -- Course 9 Unit 3's function.
    flat = pd.json_normalize(doc["results"], record_path="sales",
                             meta=[["store", "key"], ["store", "name"]])
    assert flat.shape == (3, 4), flat.shape
    assert list(flat.columns) == ["product", "qty", "store.key", "store.name"]
    assert flat["qty"].sum() == 23
    assert list(flat["store.key"]) == ["T1", "T1", "T2"]

    print(f"  naive read      -> {naive.shape[0]} rows, cells contain dicts and lists")
    print(f"  json_normalize  -> {flat.shape[0]} rows x {flat.shape[1]} cols, qty {flat['qty'].sum()}")
    print("       Power BI does this with the EXPAND arrows on record and list")
    print("       columns. It is the same operation, clicked instead of typed")


def import_versus_directquery():
    """Not runnable -- a table, because the choice is the examinable part."""
    rows = [
        ("Where the data sits", "Copied into the .pbix", "Stays in the source"),
        ("Speed", "Fast (in-memory columnar)", "The source's speed"),
        ("Freshness", "As of last refresh", "Live"),
        ("Size limit", "1 GB model on Pro", "None -- no copy"),
        ("DAX available", "All of it", "A restricted subset"),
        ("Load on source", "Only at refresh", "Every interaction"),
    ]
    assert len(rows) == 6
    print("  Import vs DirectQuery:")
    print(f"    {'':22s} {'IMPORT':28s} DIRECTQUERY")
    for label, imp, dq in rows:
        print(f"    {label:22s} {imp:28s} {dq}")
    print("       Import is the default and the right answer unless the data is")
    print("       too large to copy or must be to-the-second")


def main():
    print("Experiment 3 -- Connecting to different data sources")
    csv_round_trip()
    the_delimiter_trap()
    the_encoding_trap()
    excel_sheet_versus_table()
    web_api_json_is_nested()
    import_versus_directquery()


if __name__ == "__main__":
    main()
