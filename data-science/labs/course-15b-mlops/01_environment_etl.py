"""Experiments 1, 2, 3 and 6 -- the environment, the data lifecycle, a real
ETL job into a relational warehouse, and monolith against microservices.

Everything here runs. The database is real SQLite with real constraints, and
the ETL job is graded against a total that four other courses in this
programme independently compute.
"""
import json
import sqlite3
import sys
import tempfile
import time
import pathlib

import numpy as np
import pandas as pd

import fixtures as f


def experiment_1():
    print("\n    --- experiment 1: the data engineering environment")

    import sklearn
    import scipy
    print(f"\n      {'component':<16}{'version':<14}{'what it is for'}")
    rows = [
        ("Python", sys.version.split()[0], "the runtime"),
        ("pandas", pd.__version__, "in-memory transformation"),
        ("numpy", np.__version__, "the array layer under everything"),
        ("scikit-learn", sklearn.__version__, "the model"),
        ("scipy", scipy.__version__, "the statistical tests for drift"),
        ("sqlite3", sqlite3.sqlite_version, "the warehouse, with real "
         "constraints"),
    ]
    for name, ver, why in rows:
        print(f"      {name:<16}{ver:<14}{why}")

    for name, mod in [("mlflow", "mlflow"), ("dvc", "dvc"),
                      ("flask", "flask")]:
        try:
            m = __import__(mod)
            v = getattr(m, "__version__", "installed")
            print(f"      {name:<16}{str(v):<14}experiments 7, 9, 12")
        except Exception:                                   # noqa: BLE001
            print(f"      {name:<16}{'MISSING':<14}")

    print("""         PIN THESE VERSIONS. A data engineering environment that
         is not pinned is not reproducible, and 'it worked on my
         machine' is the failure this whole course exists to prevent.
         requirements.txt with == , not >= .
         The syllabus also names Jupyter and VSCode. Those are
         EDITORS -- useful, and not part of the reproducibility story.
         What must be pinned is the runtime and the libraries""")

    assert sys.version_info >= (3, 8)
    return rows


def experiment_2():
    print("\n    --- experiment 2: the data lifecycle on a real dataset")

    df = f.train_reference(4000)
    print(f"\n      {len(df):,} loan applications, {df.shape[1]} columns")

    print(f"\n      {'stage':<16}{'what happens':<42}{'evidence here'}")
    stages = [
        ("Generation", "the application form is submitted",
         f"{len(df):,} rows"),
        ("Storage", "written somewhere durable", "SQLite, experiment 3"),
        ("Ingestion", "moved into the analytics system", "the ETL job below"),
        ("Transformation", "cleaned, joined, aggregated", "type coercion, dedup"),
        ("Serving", "used by a model or a dashboard", "the API, experiment 12"),
    ]
    for a, b, c in stages:
        print(f"      {a:<16}{b:<42}{c}")

    print("""         THE DATA ENGINEERING LIFECYCLE IS NOT THE DATA SCIENCE
         LIFECYCLE, and the distinction is examined.
         The DATA lifecycle is about the data: it is created, stored,
         used, archived, destroyed.
         The DATA ENGINEERING lifecycle is about the PIPELINE that
         moves data between those states -- generation, storage,
         ingestion, transformation, serving -- with security,
         management, DataOps, architecture and orchestration
         underneath every stage as 'undercurrents'""")

    print(f"\n      profiling the data, which is where every project starts:")
    print(f"      {'column':<16}{'dtype':<10}{'nulls':>7}{'distinct':>10}"
          f"{'mean':>10}{'std':>8}")
    for c in df.columns:
        s = df[c]
        mean = f"{s.mean():.3f}" if pd.api.types.is_numeric_dtype(s) else "-"
        std = f"{s.std():.3f}" if pd.api.types.is_numeric_dtype(s) else "-"
        print(f"      {c:<16}{str(s.dtype):<10}{s.isna().sum():>7}"
              f"{s.nunique():>10}{mean:>10}{std:>8}")

    print(f"\n      the target: {df.approved.mean():.4f} approved")
    print("""         RECORD THE BASE RATE BEFORE YOU MODEL ANYTHING. It is
         the majority-class baseline, and it is what every accuracy
         figure in this course must be read against""")

    assert df.isna().sum().sum() == 0
    return df


def experiment_3():
    print("\n    --- experiment 3: ETL from CSV and JSON into a warehouse")

    tmp = pathlib.Path(tempfile.mkdtemp())
    csv_path, json_path = f.write_sources(tmp / "raw")
    db = tmp / "warehouse.db"

    print(f"\n      sources: {csv_path.name} and {json_path.name}")
    print("      the CSV is deliberately messy -- and this is the experiment:")
    print("        * 'south' in lowercase where the rest say 'South'")
    print("        * a price written 'Rs 140' with a currency prefix")
    print("        * order 6 appears TWICE")
    print("        * order 10 has a NULL units field")

    # ---- EXTRACT ---------------------------------------------------------
    raw_csv = pd.read_csv(csv_path, dtype=str)
    raw_json = pd.DataFrame(json.loads(json_path.read_text())).astype(str)
    raw = pd.concat([raw_csv, raw_json], ignore_index=True)
    print(f"\n      EXTRACT: {len(raw_csv)} rows from CSV + "
          f"{len(raw_json)} from JSON = {len(raw)}")
    print("""         EXTRACT EVERYTHING AS TEXT FIRST. Letting the reader
         infer types silently turns "Rs 140" into a null or leaves
         the column as strings, and you find out three joins later""")

    # ---- the naive total, for comparison --------------------------------
    naive = pd.to_numeric(raw.units, errors="coerce").fillna(0) * \
        pd.to_numeric(raw.unit_price, errors="coerce").fillna(0)
    naive_south = int(naive[raw.region == "South"].sum())
    print(f"\n      the NAIVE total for South, with no cleaning: "
          f"Rs {naive_south:,}")

    # ---- TRANSFORM -------------------------------------------------------
    df = raw.copy()
    before = len(df)
    df["region"] = df.region.str.strip().str.title()
    df["unit_price"] = pd.to_numeric(
        df.unit_price.str.replace(r"[^0-9.]", "", regex=True), errors="coerce")
    df["units"] = pd.to_numeric(df.units, errors="coerce")
    df["order_id"] = pd.to_numeric(df.order_id, errors="coerce")

    n_null = int(df.units.isna().sum())
    df = df.dropna(subset=["units", "unit_price", "order_id"])
    n_dup = int(df.duplicated(subset=["order_id"]).sum())
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    df["units"] = df.units.astype(int)
    df["unit_price"] = df.unit_price.astype(int)
    df["order_id"] = df.order_id.astype(int)
    df["revenue"] = df.units * df.unit_price

    print(f"\n      TRANSFORM: {before} rows in, {len(df)} out")
    print(f"        title-cased the region        -> "
          f"{sorted(df.region.unique())}")
    print(f"        stripped currency prefixes    -> unit_price is "
          f"{df.unit_price.dtype}")
    print(f"        dropped {n_null} row(s) with a null units field")
    print(f"        dropped {n_dup} duplicate order id(s)")

    # ---- LOAD ------------------------------------------------------------
    con = f.warehouse(db)
    for i, r in enumerate(sorted(df.region.unique()), start=1):
        con.execute("INSERT INTO dim_region VALUES (?,?)", (i, r))
    for i, p in enumerate(sorted(df["product"].unique()), start=1):
        con.execute("INSERT INTO dim_product VALUES (?,?)", (i, p))
    rid = dict(con.execute("SELECT region, region_id FROM dim_region"))
    pid = dict(con.execute("SELECT product, product_id FROM dim_product"))
    for _, r in df.iterrows():
        con.execute("INSERT INTO fact_sales VALUES (?,?,?,?,?,?)",
                    (int(r.order_id), rid[r.region], pid[r["product"]],
                     int(r.units), int(r.unit_price), int(r.revenue)))
    con.commit()
    print(f"\n      LOAD: {len(df)} rows into a star schema "
          f"(1 fact + 2 dimensions)")

    q = """SELECT d.region, SUM(fs.revenue) AS revenue
           FROM fact_sales fs JOIN dim_region d USING (region_id)
           GROUP BY d.region ORDER BY revenue DESC"""
    out = pd.read_sql(q, con)
    print(f"\n      {'region':<10}{'revenue':>12}")
    for _, r in out.iterrows():
        print(f"      {r.region:<10}{r.revenue:>12,}")

    south = int(out.loc[out.region == "South", "revenue"].iloc[0])
    print(f"\n      South = Rs {south:,}")
    print(f"      the naive figure was Rs {naive_south:,} -- "
          f"a difference of Rs {south - naive_south:,}")
    print(f"""         THE NAIVE FIGURE IS WRONG BY Rs {abs(south - naive_south):,},
         and NOTHING RAISED AN ERROR. Three separate defects, none
         of which throws: the lowercase 'south' row did not match the
         filter, the price written 'Rs 140' would not parse as a
         number, and order 6 was counted twice.
         AND NOW LOOK AT THE SIZE OF THE ERROR. Three defects worth
         Rs -1,680, Rs -700 and Rs +2,520 nearly cancelled, leaving a
         total off by only Rs 140 -- about one percent.
         THAT IS THE DANGEROUS CASE. A figure that is wildly wrong
         gets noticed; a figure that is 1% wrong gets reported to the
         board. The errors did not cancel because anything corrected
         them, they cancelled by luck, and next month they will not.
         THAT IS WHY CLEANING IS THE JOB, and why the only reliable
         check is an independently computed figure to compare
         against -- which is what the five-engine cross-check below
         is for""")

    print(f"""         CROSS-COURSE CHECK: Rs {south:,} is the same South total
         that Course 11 computes in DAX, Course 12 B in Hive and in
         Spark, and Course 13 B in its warehouse. FIVE independent
         engines now agree, which is worth more than any one of them
         being carefully written""")

    # ---- the constraints earn their place -------------------------------
    print("\n      and the constraints are not decoration:")
    for label, sql in [
        ("units = 0",
         "INSERT INTO fact_sales VALUES (99,1,1,0,300,0)"),
        ("unknown region_id",
         "INSERT INTO fact_sales VALUES (98,77,1,1,300,300)"),
        ("duplicate order_id",
         "INSERT INTO fact_sales VALUES (1,1,1,1,300,300)"),
    ]:
        try:
            con.execute("PRAGMA foreign_keys=ON")
            con.execute(sql)
            con.commit()
            print(f"        {label:<22}ACCEPTED -- the constraint is missing")
        except sqlite3.Error as exc:
            print(f"        {label:<22}rejected: {type(exc).__name__}")

    print("""         PUT THE CONSTRAINTS IN THE DATABASE, not only in the
         pipeline. A pipeline is one program; the database is the last
         line of defence against every OTHER program that will ever
         write to it -- including the one written in a hurry, by
         somebody else, at the end of a quarter""")

    assert south == f.SOUTH_TOTAL, (
        f"South is Rs {south:,}, but Courses 11, 12 B and 13 B all get "
        f"Rs {f.SOUTH_TOTAL:,}")
    assert naive_south != south, "the messy data should have broken the naive sum"
    con.close()
    return south, naive_south


def experiment_6():
    print("\n    --- experiment 6: monolith against microservices, measured")

    print("""
      the mock business problem: a loan application must be scored,
      logged, and a decision letter generated. Three units of work.""")

    def unit(ms):
        time.sleep(ms / 1000.0)

    SCORE, LOG, LETTER = 4, 1, 3        # milliseconds of work each

    def monolith(n):
        t0 = time.perf_counter()
        for _ in range(n):
            unit(SCORE); unit(LOG); unit(LETTER)
        return time.perf_counter() - t0

    def microservices(n, hop_ms=2):
        """Same work, but each step is a network call away."""
        t0 = time.perf_counter()
        for _ in range(n):
            unit(hop_ms); unit(SCORE)
            unit(hop_ms); unit(LOG)
            unit(hop_ms); unit(LETTER)
        return time.perf_counter() - t0

    n = 40
    m_t = monolith(n)
    s_t = microservices(n)
    print(f"\n      {n} applications, same work in both:")
    print(f"        monolith       {m_t * 1000:>8.1f} ms   "
          f"({m_t / n * 1000:.2f} ms each)")
    print(f"        microservices  {s_t * 1000:>8.1f} ms   "
          f"({s_t / n * 1000:.2f} ms each)")
    print(f"        the network cost {(s_t - m_t) / m_t * 100:.0f}% more time")

    print("""         MICROSERVICES ARE SLOWER FOR THE SAME WORK, and any
         honest comparison starts there. Every boundary you draw is a
         serialisation, a network hop and a new failure mode.
         So what do you get for it? NOT speed. You get INDEPENDENT
         DEPLOYMENT and INDEPENDENT SCALING, and those only pay when
         the parts genuinely differ""")

    print(f"\n      where it pays -- scoring is 4x the cost of logging:")
    print(f"      {'strategy':<34}{'instances':>10}{'wasted capacity'}")
    print(f"      {'monolith, scaled 4x':<34}{4:>10}"
          f"   4x of EVERY component")
    print(f"      {'microservices, scale scorer 4x':<34}{'4 + 1 + 1':>10}"
          f"   none")
    print("""         THAT is the argument, and it is an argument about COST
         at scale rather than about elegance.
         THE RULE THE INDUSTRY LEARNED THE HARD WAY: start with a
         well-structured monolith. Split a service out when you can
         name the specific scaling or deployment problem it solves.
         A team of four does not need eleven services, and 'we use
         microservices' is not an architecture""")

    print(f"\n      {'':<22}{'monolith':<26}{'microservices'}")
    for label, a, b in [
        ("deploy", "all or nothing", "per service"),
        ("scale", "the whole thing", "the hot part only"),
        ("failure", "one crash, all down", "degraded, if you designed for it"),
        ("debugging", "one stack trace", "distributed tracing, or nothing"),
        ("data", "one database, joins work", "one per service, joins do NOT"),
        ("team", "coordination on release", "independent teams"),
    ]:
        print(f"      {label:<22}{a:<26}{b}")

    print("""         'ONE DATABASE PER SERVICE' IS THE ROW THAT SURPRISES
         PEOPLE. If two services share a database they are not
         independent -- a schema change breaks both -- so the pattern
         requires splitting the data too, and then a join you used to
         write in SQL becomes an API call and an in-memory merge.
         That is the real cost, and it is why the ETL in experiment 3
         puts everything in ONE warehouse: analytics wants joins""")

    assert s_t > m_t, "network hops should cost time"
    return m_t, s_t


def main():
    print("  Experiments 1, 2, 3 and 6 -- environment, lifecycle, ETL, "
          "architecture")
    experiment_1()
    experiment_2()
    experiment_3()
    experiment_6()
    print("\n    all assertions passed")


if __name__ == "__main__":
    main()
