"""Experiment 11 -- import data from an RDBMS into Hadoop using Sqoop.

Sqoop is not installed. `11_sqoop.sh` carries the real commands, marked NOT
EXECUTED. What runs here is the same import, honestly: a REAL relational
database (SQLite), a REAL split-by query, REAL parallel range reads, and a
REAL Parquet file at the other end. Only the cluster is missing.

Sqoop's entire trick is one line of SQL you never see:
    SELECT MIN(id), MAX(id) FROM table
and then one range query per mapper. Everything students find confusing about
Sqoop -- why --split-by matters, why a text primary key breaks it, why 4
mappers can produce wildly unequal files -- follows from that.
"""
import os
import sqlite3
import tempfile

import pyarrow as pa
import pyarrow.parquet as pq

import fixtures as f

FIELDS = ["order_id", "store", "region", "product", "category", "qty", "revenue"]


def build_rdbms(path, rows):
    con = sqlite3.connect(path)
    con.execute("""CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY, store TEXT, region TEXT,
        product TEXT, category TEXT, qty INTEGER, revenue REAL)""")
    con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", rows)
    con.commit()
    return con


def boundaries(con, table, col, mappers):
    """Exactly what Sqoop runs before it launches a single mapper."""
    lo, hi = con.execute(f"SELECT MIN({col}), MAX({col}) FROM {table}").fetchone()
    step = (hi - lo + 1) / mappers
    out = []
    for m in range(mappers):
        a = lo + int(m * step)
        b = lo + int((m + 1) * step) - 1 if m < mappers - 1 else hi
        out.append((a, b))
    return lo, hi, out


def main():
    print("  Experiment 11 -- Sqoop import, with a real database at one end")

    tmp = tempfile.mkdtemp(prefix="bigdata11_")
    db = os.path.join(tmp, "retail.db")

    # 90 orders, built from the nine shared rows so the totals stay checkable
    base = f.SALES_DF
    rows = []
    for i in range(90):
        r = base.iloc[i % 9]
        rows.append((i + 1, r["store"], r["region"], r["product"],
                     r["category"], int(r["qty"]), float(r["revenue"])))
    con = build_rdbms(db, rows)
    n = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    total = con.execute("SELECT SUM(revenue) FROM orders").fetchone()[0]
    print(f"\n    source: SQLite table 'orders', {n} rows, "
          f"revenue {total:,.0f}")
    assert n == 90 and abs(total - f.total_revenue() * 10) < 1e-6
    print(f"""         the 90 rows are ten copies of Course 11's nine, so the
         source total is exactly 10 x {f.total_revenue():,.0f}. If the imported
         Parquet does not carry that number, the import lost data --
         and that is the only import test that matters""")

    # ---- what Sqoop does first -------------------------------------------
    lo, hi, ranges = boundaries(con, "orders", "order_id", 4)
    print(f"\n    step 1: SELECT MIN(order_id), MAX(order_id) -> {lo}, {hi}")
    print(f"    step 2: split into 4 ranges, one per mapper")
    print(f"      {'mapper':<8}{'WHERE clause':<44}{'rows':>6}")
    imported = []
    for m, (a, b) in enumerate(ranges):
        where = f"order_id >= {a} AND order_id <= {b}"
        part = con.execute(
            f"SELECT {', '.join(FIELDS)} FROM orders WHERE {where}").fetchall()
        imported.extend(part)
        print(f"      {m:<8}{where:<44}{len(part):>6}")
    counts = [len(con.execute(
        f"SELECT 1 FROM orders WHERE order_id >= {a} AND order_id <= {b}"
    ).fetchall()) for a, b in ranges]
    assert sum(counts) == n
    assert max(counts) - min(counts) <= 1, "an integer key splits near-evenly"
    print(f"""         four mappers, {min(counts)} or {max(counts)} rows each ({n} does not
         divide by 4), four TCP connections to
         the database. Sqoop's parallelism is DATABASE parallelism --
         raise -m to 20 on a production OLTP box and you have written
         a denial of service against your own company""")

    # ---- the skew trap ---------------------------------------------------
    print("\n    now split by a column that is NOT uniform -- 'qty':")
    lo2, hi2, ranges2 = boundaries(con, "orders", "qty", 4)
    print(f"      MIN(qty), MAX(qty) = {lo2}, {hi2}")
    print(f"      {'mapper':<8}{'range':<20}{'rows':>6}")
    skew = []
    for m, (a, b) in enumerate(ranges2):
        c = con.execute(
            f"SELECT COUNT(*) FROM orders WHERE qty >= {a} AND qty <= {b}"
        ).fetchone()[0]
        skew.append(c)
        print(f"      {m:<8}{f'{a}..{b}':<20}{c:>6}")
    assert sum(skew) == n
    assert max(skew) > 3 * min(skew) if min(skew) else True
    print(f"""         {max(skew)} rows for one mapper and {min(skew)} for another.
         Sqoop assumes the split column is UNIFORMLY DISTRIBUTED
         between its min and max, and qty is not. The job's wall
         clock is the slowest mapper, so a bad --split-by wastes
         three quarters of your parallelism.
         Split on the PRIMARY KEY unless you have measured otherwise""")

    print("\n    --split-by on a TEXT column:")
    print("      Sqoop needs an ORDERED, NUMERIC column to compute ranges.")
    print("      On text it must either refuse, or use")
    print("      -Dorg.apache.sqoop.splitter.allow_text_splitter=true")
    print("      which splits on string ordering and skews horribly.")
    print("""         a table with a UUID or composite primary key has no
         natural split column, and the honest answer is -m 1 --
         one mapper, no parallelism, correct results""")

    # ---- the target ------------------------------------------------------
    table = pa.Table.from_pylist(
        [dict(zip(FIELDS, r)) for r in sorted(imported)])
    out = os.path.join(tmp, "orders.parquet")
    pq.write_table(table, out, compression="snappy")
    back = pq.read_table(out)
    imported_total = sum(back.column("revenue").to_pylist())
    print(f"\n    landed: {out.split(os.sep)[-1]}, {back.num_rows} rows, "
          f"revenue {imported_total:,.0f}")
    assert back.num_rows == n
    assert abs(imported_total - total) < 1e-6, "the import must not lose money"
    print("""         row count AND the sum of a money column, both checked.
         Counting rows alone would not catch a truncated numeric
         type, which is the classic Sqoop bug: an Oracle NUMBER(38)
         silently becoming a Java double""")

    # ---- incremental -----------------------------------------------------
    print("\n    incremental import, the two modes:")
    print(f"      {'mode':<15}{'--check-column':<18}{'catches'}")
    print(f"      {'append':<15}{'an increasing id':<18}"
          f"{'new rows only'}")
    print(f"      {'lastmodified':<15}{'a timestamp':<18}"
          f"{'new AND updated rows'}")
    last = con.execute("SELECT MAX(order_id) FROM orders").fetchone()[0]
    con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?)",
                    [(91, "Guntur", "South", "Tea 500g", "Grocery", 3, 630.0)])
    con.commit()
    new = con.execute(
        f"SELECT COUNT(*) FROM orders WHERE order_id > {last}").fetchone()[0]
    assert new == 1
    print(f"\n      --last-value {last} now selects {new} row")
    print("""         NEITHER MODE CATCHES A DELETE. Sqoop has no way to see a
         row that is gone, so an incrementally imported table drifts
         away from its source over time. The fix is a periodic full
         re-import, and knowing that is the difference between having
         used Sqoop and having read about it""")

    con.close()
    os.remove(out)
    os.remove(db)
    os.rmdir(tmp)


if __name__ == "__main__":
    main()
