"""Experiment 10 -- Hive queries for structured data analysis: tables,
partitions and the queries that go with them.

Hive is not installed here. `10_hive.hql` carries the HiveQL you submit, marked
NOT EXECUTED. What runs here is DuckDB, which speaks close enough to ANSI SQL
that the SAME query text answers the same question -- so the RESULTS in the
notes are verified even though Hive itself never ran.

The data is Course 11's star schema, imported rather than copied, so a Hive
aggregate here and a DAX measure there are computed from the same nine rows.
"""
import duckdb

import fixtures as f


def q(con, sql):
    return con.execute(sql).fetchall()


def main():
    print("  Experiment 10 -- Hive-style SQL over the star schema")

    con = duckdb.connect()
    con.register("sales", f.SALES_DF)

    print(f"\n    {len(f.SALES_DF)} fact rows, "
          f"total revenue {f.total_revenue():,.0f}")

    # ---- a plain aggregate ----------------------------------------------
    rows = q(con, """
        SELECT region, SUM(revenue) AS revenue, SUM(profit) AS profit
        FROM sales GROUP BY region ORDER BY revenue DESC
    """)
    print(f"\n    {'region':<10}{'revenue':>12}{'profit':>10}{'margin':>9}")
    for region, rev, prof in rows:
        print(f"    {region:<10}{rev:>12,.0f}{prof:>10,.0f}{100 * prof / rev:>8.2f}%")
    got = dict((r[0], r[1]) for r in rows)
    assert got["South"] == 10360.0, "must match Course 11's CALCULATE figure"
    assert got["North"] == 2520.0
    assert sum(got.values()) == f.total_revenue()
    print("""         South = 10,360 is the SAME number Course 11's DAX
         CALCULATE measure produced. Two engines, two languages, one
         dataset -- if they ever disagree the suite fails, which is
         what makes the cross-check worth having""")

    # ---- partitioning ----------------------------------------------------
    print("\n    partitioning by quarter -- what Hive actually does:")
    parts = q(con, """
        SELECT quarter, COUNT(*) AS rows, SUM(revenue) AS revenue
        FROM sales GROUP BY quarter ORDER BY quarter
    """)
    total_rows = sum(p[1] for p in parts)
    print(f"      {'partition':<14}{'rows':>6}{'revenue':>12}{'scanned for Q2':>16}")
    for quarter, n, rev in parts:
        print(f"      quarter={quarter:<7}{n:>6}{rev:>12,.0f}"
              f"{(n if quarter == 'Q2' else 0):>16}")
    q2_rows = next(n for quarter, n, _ in parts if quarter == "Q2")
    print(f"      {'TOTAL':<14}{total_rows:>6}{'':>12}{q2_rows:>16}")
    assert total_rows == 9 and q2_rows == 4
    print(f"""         a partitioned table stores each quarter in its own HDFS
         DIRECTORY, so 'WHERE quarter = ''Q2''' reads {q2_rows} rows instead
         of {total_rows} -- partition PRUNING, decided before a single byte is
         read. The partition column is a directory name, not a column
         in the data files, which is why it costs no storage""")

    print("""
      the trap: partition on something with FEW distinct values.
      Partitioning by date_key here would make 4 directories for 9
      rows -- the small-files problem from experiment 4, created on
      purpose. Partition by quarter or month; BUCKET by customer_id""")

    # ---- bucketing -------------------------------------------------------
    print("\n    bucketing (CLUSTERED BY store INTO 3 BUCKETS):")
    buckets = {}
    for store in sorted(f.SALES_DF["store"].unique()):
        h = sum(ord(c) for c in store) % 3
        buckets.setdefault(h, []).append(store)
    for b in range(3):
        print(f"      bucket {b}: {buckets.get(b, []) or '(empty)'}")
    assert 1 not in buckets, "bucket 1 draws nothing from three store names"
    print("""         BUCKET 1 IS EMPTY, with three stores over three buckets.
         Hashing does not distribute small key sets evenly, and an
         empty bucket is still a file the job opens.
         Buckets are FILES inside a partition, assigned by a hash
         of the column. Two tables bucketed the same way on the same
         column can be joined bucket-to-bucket with no shuffle at all
         -- a sort-merge bucket join, and the reason bucketing exists""")

    # ---- managed vs external --------------------------------------------
    print("\n    managed against external tables:")
    print(f"      {'':<12}{'data lives':<26}{'DROP TABLE deletes'}")
    print(f"      {'MANAGED':<12}{'/user/hive/warehouse':<26}{'the DATA too'}")
    print(f"      {'EXTERNAL':<12}{'wherever you point it':<26}{'only the metadata'}")
    print("""         use EXTERNAL for data you did not produce and cannot
         recreate. A DROP TABLE on a managed table over the company's
         only copy of a dataset is the classic Hive accident""")

    # ---- a join, and why Hive cares --------------------------------------
    rows = q(con, """
        SELECT category, product, SUM(qty) AS units, SUM(revenue) AS revenue
        FROM sales GROUP BY category, product
        HAVING SUM(revenue) > 1000
        ORDER BY revenue DESC
    """)
    print(f"\n    products above 1,000 revenue:")
    print(f"      {'category':<12}{'product':<16}{'units':>6}{'revenue':>10}")
    for cat, prod, units, rev in rows:
        print(f"      {cat:<12}{prod:<16}{units:>6.0f}{rev:>10,.0f}")
    assert len(rows) == 4, "four products clear 1,000 -- Notebook only just"
    grocery = sum(r[3] for r in rows if r[0] == "Grocery")
    assert grocery == 9800.0
    print("""         HAVING filters GROUPS, WHERE filters ROWS -- and in Hive
         that distinction is a job-plan difference, not a syntax
         nicety: a WHERE on a partition column prunes directories
         before the job starts, a HAVING cannot""")

    # ---- Hive is not a database -----------------------------------------
    print("\n    what Hive is NOT:")
    print(f"      {'expectation':<30}{'reality'}")
    for exp, real in (
            ("row-level UPDATE/DELETE", "only with ACID tables + ORC + buckets"),
            ("sub-second queries", "seconds to minutes -- it plans a JOB"),
            ("indexes", "removed in Hive 3; use partitions and ORC/Parquet"),
            ("a running server holding data", "metadata only; data is files in HDFS"),
            ("enforced constraints", "declarative only; NOT enforced")):
        print(f"      {exp:<30}{real}")
    print("""         Hive is a COMPILER: HiveQL in, a MapReduce/Tez/Spark job
         out. Everything surprising about it follows from that one
         sentence, and it is the right answer to 'compare Hive with an
         RDBMS'""")

    con.close()


if __name__ == "__main__":
    main()
