"""Experiments 8, 9 and 12 -- cloud databases, a batch ETL pipeline, and
loading a cloud data warehouse.

AWS RDS, BigQuery and Cosmos DB need an account, so `08_cloud_db.md` and
`12_etl_to_warehouse.md` carry the console and CLI steps, marked NOT
EXECUTED.

What runs is the pipeline itself: extract from a real relational source
(SQLite, standing in for RDS), transform, and load into a real columnar
warehouse (DuckDB, standing in for Redshift/BigQuery). The transformations,
the row counts and the money all reconcile -- and they reconcile against
Course 11 and Course 12 B, which used the same nine facts.

The pricing arithmetic at the end is the part of "cloud data warehouse" that
is genuinely different from Course 5's DBMS, and it is what gets examined.
"""
import os
import sqlite3
import tempfile

import duckdb

import fixtures as f

SRC_COLUMNS = ["order_id", "date_key", "store", "region", "product",
               "category", "qty", "list_price", "unit_cost"]


def money(x):
    return f"${x:,.2f}"


def extract(db_path):
    """E -- read from the operational database. Never transform here."""
    con = sqlite3.connect(db_path)
    con.execute("""CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY, date_key TEXT, store TEXT, region TEXT,
        product TEXT, category TEXT, qty INTEGER,
        list_price REAL, unit_cost REAL)""")
    rows = []
    for i, (_, r) in enumerate(f.SALES_DF.iterrows()):
        rows.append((i + 1, r["date_key"], r["store"], r["region"],
                     r["product"], r["category"], int(r["qty"]),
                     float(r["list_price"]), float(r["unit_cost"])))
    # deliberately dirty: one duplicate and one null region
    rows.append((10, rows[0][1], rows[0][2], rows[0][3], rows[0][4],
                 rows[0][5], rows[0][6], rows[0][7], rows[0][8]))
    rows.append((11, "D4", "Guntur", None, "Tea 500g", "Grocery",
                 3, 210.0, 150.0))
    con.executemany(
        "INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?)", rows)
    con.commit()
    out = con.execute(
        f"SELECT {', '.join(SRC_COLUMNS)} FROM orders").fetchall()
    con.close()
    return out


def transform(rows, log):
    """T -- and every step records what it dropped, or it is not auditable."""
    log["extracted"] = len(rows)

    seen, deduped = set(), []
    for r in rows:
        fingerprint = r[1:]                 # everything but the surrogate id
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        deduped.append(r)
    log["after_dedup"] = len(deduped)

    clean = [r for r in deduped if r[3] is not None]
    log["dropped_null_region"] = len(deduped) - len(clean)

    enriched = []
    for r in clean:
        d = dict(zip(SRC_COLUMNS, r))
        d["revenue"] = d["qty"] * d["list_price"]
        d["cost"] = d["qty"] * d["unit_cost"]
        d["profit"] = d["revenue"] - d["cost"]
        d["quarter"] = "Q1" if d["date_key"] in ("D1", "D2") else "Q2"
        enriched.append(d)
    log["loaded"] = len(enriched)
    return enriched


def main():
    print("  Experiments 8, 9 and 12 -- cloud DB, batch ETL, warehouse load")

    tmp = tempfile.mkdtemp(prefix="cloud09_")
    db = os.path.join(tmp, "orders.db")

    # ---- E ---------------------------------------------------------------
    raw = extract(db)
    print(f"\n    EXTRACT from the operational database (SQLite as RDS):")
    print(f"      {len(raw)} rows, including one duplicate and one null region")
    assert len(raw) == 11

    # ---- T ---------------------------------------------------------------
    log = {}
    clean = transform(raw, log)
    print(f"\n    TRANSFORM, with an audit trail at every step:")
    print(f"      {'step':<26}{'rows':>6}")
    for step in ("extracted", "after_dedup", "dropped_null_region", "loaded"):
        print(f"      {step:<26}{log[step]:>6}")
    assert log == {"extracted": 11, "after_dedup": 10,
                   "dropped_null_region": 1, "loaded": 9}
    print("""         11 in, 9 out, and the pipeline can SAY WHERE THE OTHER TWO
         WENT. A transformation that silently drops rows is worse than
         one that fails: the numbers still look plausible.
         Every ETL job should emit these counts, and a monitoring rule
         should alarm when the drop rate moves""")

    # ---- L ---------------------------------------------------------------
    con = duckdb.connect()
    con.execute("""CREATE TABLE fact_sales (
        order_id INTEGER, date_key VARCHAR, store VARCHAR, region VARCHAR,
        product VARCHAR, category VARCHAR, qty INTEGER,
        list_price DOUBLE, unit_cost DOUBLE,
        revenue DOUBLE, cost DOUBLE, profit DOUBLE, quarter VARCHAR)""")
    con.executemany(
        "INSERT INTO fact_sales VALUES (" + ",".join(["?"] * 13) + ")",
        [[r[c] for c in ("order_id", "date_key", "store", "region", "product",
                         "category", "qty", "list_price", "unit_cost",
                         "revenue", "cost", "profit", "quarter")]
         for r in clean])

    n, rev = con.execute(
        "SELECT COUNT(*), SUM(revenue) FROM fact_sales").fetchone()
    print(f"\n    LOAD into the warehouse (DuckDB as Redshift/BigQuery):")
    print(f"      {n} rows, revenue {money(rev)}")
    assert n == 9 and rev == f.total_revenue()
    print(f"""         {money(rev)} is Course 11's total, Course 12 B's Hive total and
         Course 12 B's Spark total. FOUR engines now agree on the same
         nine facts, and the suite fails if any of them drifts""")

    rows = con.execute("""
        SELECT region, SUM(revenue) rev, SUM(profit) prof
        FROM fact_sales GROUP BY region ORDER BY rev DESC""").fetchall()
    print(f"\n      {'region':<10}{'revenue':>12}{'profit':>10}")
    for region, r, p in rows:
        print(f"      {region:<10}{money(r):>12}{money(p):>10}")
    assert dict((r[0], r[1]) for r in rows)["South"] == 10360.0

    # ---- ETL against ELT -------------------------------------------------
    print("\n    ETL against ELT, which is the modern distinction:")
    print(f"      {'':<16}{'ETL':<34}{'ELT'}")
    for label, etl, elt in (
            ("transform runs", "on a separate compute box", "IN the warehouse"),
            ("lands in the DW", "clean data only", "RAW data, then transformed"),
            ("re-run a change", "re-extract from source", "re-run SQL on raw"),
            ("needs", "an ETL server or Glue", "a warehouse that scales"),
            ("source load", "one read", "one read"),
            ("suits", "limited warehouse capacity", "cheap elastic compute")):
        print(f"      {label:<16}{etl:<34}{elt}")
    print("""         ELT WON BECAUSE WAREHOUSE COMPUTE GOT CHEAP AND ELASTIC.
         Landing raw data means a transformation bug is fixed by
         re-running SQL rather than re-extracting from a production
         database that may no longer hold the old rows -- which is
         exactly the DELETE problem Course 12 B found in Sqoop""")

    # ---- what makes a cloud warehouse different --------------------------
    print("\n    what makes a cloud DW different from Course 5's RDBMS:")
    print(f"      {'':<22}{'RDBMS (Course 5)':<28}{'cloud DW'}")
    for label, rdbms, dw in (
            ("storage layout", "ROW", "COLUMNAR"),
            ("workload", "many small transactions", "few huge scans"),
            ("indexes", "central to performance", "usually none"),
            ("scaling", "a bigger box", "add nodes / serverless"),
            ("compute & storage", "coupled", "SEPARATED"),
            ("billed on", "the box, hourly", "BYTES SCANNED or node-hours"),
            ("a bad query costs", "time", "TIME AND MONEY")):
        print(f"      {label:<22}{rdbms:<28}{dw}")

    # ---- the pricing arithmetic -----------------------------------------
    print("\n    BigQuery on-demand, at "
          f"${f.BIGQUERY_PER_TB_SCANNED:.2f} per TB SCANNED:")
    print(f"      {'query':<44}{'TB scanned':>12}{'cost':>10}")
    scenarios = [
        ("SELECT * FROM events                      ", 10.0),
        ("SELECT user_id FROM events                ", 0.4),
        ("SELECT user_id ... WHERE dt = '2026-08-01'", 0.02),
    ]
    costs = {}
    for label, tb in scenarios:
        c = tb * f.BIGQUERY_PER_TB_SCANNED
        costs[label.strip()] = c
        print(f"      {label:<44}{tb:>12.2f}{money(c):>10}")
    full = costs["SELECT * FROM events"]
    pruned = costs["SELECT user_id ... WHERE dt = '2026-08-01'"]
    assert full / pruned == 500
    print(f"""         THE SAME QUESTION, {full / pruned:.0f}x THE PRICE. Selecting one
         column instead of all reads a fraction of the bytes
         (Course 12 B's column projection), and a partition filter
         removes almost all of the rest (Course 12 B's partition
         pruning).
         In Course 12 B those techniques saved TIME. Here they save
         MONEY, on the same mechanism -- which is why 'SELECT *' is a
         billing incident on a serverless warehouse and merely rude on
         a server you already own""")

    print(f"\n    Redshift, at ${f.REDSHIFT_RA3_XLPLUS_HOUR:.3f} per node-hour:")
    for nodes in (2, 4, 8):
        m = nodes * f.REDSHIFT_RA3_XLPLUS_HOUR * f.HOURS_PER_MONTH
        print(f"      {nodes} nodes: {money(m):>12}/month, "
              f"{'queries are free at the margin'}")
    two = 2 * f.REDSHIFT_RA3_XLPLUS_HOUR * f.HOURS_PER_MONTH
    breakeven_tb = two / f.BIGQUERY_PER_TB_SCANNED
    print(f"""
      break-even: {breakeven_tb:,.0f} TB scanned per month
         BELOW that, on-demand BigQuery is cheaper and you pay nothing
         when idle. ABOVE it, a provisioned cluster is cheaper and an
         extra query costs nothing at the margin.
         That is the whole provisioned-against-serverless decision,
         and it is a calculation rather than a preference""")
    assert 250 < breakeven_tb < 260

    con.close()
    os.remove(db)
    os.rmdir(tmp)


if __name__ == "__main__":
    main()
