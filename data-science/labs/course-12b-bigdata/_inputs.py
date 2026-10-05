"""The input files the Course 12 B tool scripts read, written from fixtures.py.

    python3 _inputs.py DIR

The scripts name files a cluster would already hold -- sales.csv, a store dimension, product
tags, documents, an access log. These are those files, made from the same nine sales rows and
six documents the Python halves use, so a Hive query and its DuckDB twin read the same data:

  sales.csv           the nine fact rows, with a header (Hive skips it; see 09 and 10)
  stores.csv          store, city, region -- each store is named after its city
  tags.tsv            product <TAB> tags separated by ';' (Pig's default delimiter is a tab)
  docs/doc1.txt ...   the six documents, for word count and the inverted index
  access.log          the 40 access-log lines, for Flume
  syslog              a few log lines, for experiment 3's word count
"""
import pathlib
import sys

import fixtures as f

COLUMNS = ["date_key", "store", "region", "product", "category", "qty", "list_price"]
TAGS = {"Rice 5kg": "staple;grain;bulk", "Tea 500g": "beverage;daily",
        "Shampoo 200ml": "personal;care", "Notebook": "paper;school"}


def write(d):
    d = pathlib.Path(d)
    (d / "docs").mkdir(parents=True, exist_ok=True)
    rows = f.SALES_DF[COLUMNS]
    lines = [",".join(COLUMNS)] + [",".join(str(v) for v in r) for r in rows.itertuples(index=False)]
    (d / "sales.csv").write_text("\n".join(lines) + "\n")
    stores = f.c11.DIM_STORE
    (d / "stores.csv").write_text("".join(f"{s},{s},{r}\n" for s, r in zip(stores.store, stores.region)))
    (d / "tags.tsv").write_text("".join(f"{p}\t{t}\n" for p, t in TAGS.items()))
    for name, text in f.DOCS.items():
        (d / "docs" / name).write_text(text + "\n")
    (d / "access.log").write_text("\n".join(f.access_logs()) + "\n")
    (d / "syslog").write_text("".join(f"Aug 12 09:{i:02d}:00 lab {text}\n"
                                      for i, text in enumerate(f.DOCS.values())))


if __name__ == "__main__":
    write(sys.argv[1])
