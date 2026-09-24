"""Experiment 8 (Python equivalent) -- read/write CSV, JSON, XML.

R version: ../08_file_io.R  (read.csv, jsonlite, XML, readxl)
Excel is omitted here: writing .xlsx needs a third-party library, and the point
of the experiment -- that each format round-trips -- is made by the other three.
"""
import csv, json, tempfile, pathlib
import xml.etree.ElementTree as ET
from _shared import STUDENTS

COLS = ["name", "section", "gender", "hours", "marks", "attendance"]
ROWS = [dict(zip(COLS, r)) for r in STUDENTS]


def csv_roundtrip(d):
    p = d / "students.csv"
    with open(p, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(ROWS)
    with open(p, newline="") as fh:
        back = list(csv.DictReader(fh))
    # everything read from CSV is a string -- the same trap as in Course 3
    return back, all(isinstance(v, str) for v in back[0].values())


def json_roundtrip(d):
    p = d / "students.json"
    p.write_text(json.dumps(ROWS, indent=2))
    back = json.loads(p.read_text())
    return back, isinstance(back[0]["marks"], int)      # JSON preserves types


def xml_roundtrip(d):
    p = d / "students.xml"
    root = ET.Element("students")
    for r in ROWS:
        el = ET.SubElement(root, "student")
        for k, v in r.items():
            ET.SubElement(el, k).text = str(v)
    ET.ElementTree(root).write(p, encoding="utf-8", xml_declaration=True)
    back = [{c.tag: c.text for c in el} for el in ET.parse(p).getroot()]
    return back, all(isinstance(v, str) for v in back[0].values())


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td)
        for name, fn in (("CSV", csv_roundtrip), ("JSON", json_roundtrip),
                         ("XML", xml_roundtrip)):
            back, typed = fn(d)
            same = len(back) == len(ROWS) and back[0]["name"] == ROWS[0]["name"]
            print(f"{name:<6} wrote {len(ROWS)} rows, read {len(back)} back  "
                  f"-> {'round-trips ✓' if same else 'MISMATCH'}")
            if name == "JSON":
                print(f"       numeric types preserved: {typed}")
            else:
                print(f"       all values come back as strings: {typed}")

    print("\n  KEY POINT: CSV and XML are untyped -- everything returns as text,")
    print("  so numbers must be converted explicitly. JSON preserves numbers and")
    print("  booleans. In R this is why read.csv() has colClasses= and why")
    print("  jsonlite::fromJSON() gives you a usable data frame directly.")
