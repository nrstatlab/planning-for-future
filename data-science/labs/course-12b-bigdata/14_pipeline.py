"""Experiment 14 -- an end-to-end ingestion workflow combining batch (Sqoop)
and streaming (Flume).

This is the experiment that ties the course together, and the one where the
interesting problem is not any single tool but the JOIN BETWEEN THEM: batch
data arrives hourly and complete, streaming data arrives continuously and
incomplete, and a query that spans both has to decide what it means by "now".

Runs end to end: SQLite -> Parquet (the batch side), log events -> Parquet
(the streaming side), then a real DuckDB query across the two.
"""
import os
import sqlite3
import tempfile
from collections import Counter

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

import fixtures as f


def batch_leg(tmp):
    """Sqoop's half: a full-fidelity import of a slow-changing table."""
    db = os.path.join(tmp, "orders.db")
    con = sqlite3.connect(db)
    con.execute("""CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY, host TEXT, region TEXT, revenue REAL)""")
    rows = []
    hosts = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]
    for i, (_, r) in enumerate(f.SALES_DF.iterrows()):
        rows.append((i + 1, hosts[i % 4], r["region"], float(r["revenue"])))
    con.executemany("INSERT INTO orders VALUES (?,?,?,?)", rows)
    con.commit()
    data = con.execute("SELECT order_id, host, region, revenue FROM orders").fetchall()
    con.close()
    path = os.path.join(tmp, "batch.parquet")
    pq.write_table(pa.Table.from_pylist(
        [dict(zip(("order_id", "host", "region", "revenue"), r)) for r in data]),
        path)
    return path, len(data), sum(r[3] for r in data)


def stream_leg(tmp, n):
    """Flume's half: events, parsed, with headers, landed as Parquet."""
    events = []
    for line in f.access_logs(n):
        host = line.split(" ", 1)[0]
        status = line.rsplit(" ", 2)[-2]
        size = int(line.rsplit(" ", 1)[-1])
        events.append({"host": host, "status": status, "bytes": size})
    path = os.path.join(tmp, "stream.parquet")
    pq.write_table(pa.Table.from_pylist(events), path)
    return path, len(events)


def main():
    print("  Experiment 14 -- batch and streaming, joined")

    tmp = tempfile.mkdtemp(prefix="bigdata14_")
    batch, n_batch, batch_rev = batch_leg(tmp)
    stream, n_stream = stream_leg(tmp, 40)

    print(f"\n    batch  leg (Sqoop) : {n_batch} orders, "
          f"revenue {batch_rev:,.0f}")
    print(f"    stream leg (Flume) : {n_stream} events")
    assert abs(batch_rev - f.total_revenue()) < 1e-6

    con = duckdb.connect()
    con.execute(f"CREATE VIEW batch AS SELECT * FROM '{batch}'")
    con.execute(f"CREATE VIEW stream AS SELECT * FROM '{stream}'")

    # ---- the join --------------------------------------------------------
    rows = con.execute("""
        SELECT b.host,
               COUNT(DISTINCT b.order_id) AS orders,
               SUM(DISTINCT b.revenue)    AS revenue,
               COUNT(s.host)              AS events,
               SUM(CASE WHEN s.status = '500' THEN 1 ELSE 0 END) AS errors
        FROM batch b LEFT JOIN stream s ON b.host = s.host
        GROUP BY b.host ORDER BY b.host
    """).fetchall()
    print(f"\n    joined on host:")
    print(f"      {'host':<12}{'orders':>8}{'events':>8}{'errors':>8}")
    for host, orders, rev, events, errors in rows:
        print(f"      {host:<12}{orders:>8}{events:>8}{errors:>8}")
    total_events = sum(r[3] for r in rows)
    assert total_events != n_stream, "the join FANS OUT -- see below"
    print(f"""
      events counted through the join: {total_events}
      events actually ingested       : {n_stream}""")
    print("""         THE JOIN INFLATED THE EVENT COUNT. Each host appears in
         several orders, so every event is counted once per matching
         order -- a FAN TRAP, and the same defect Course 11 found in
         a Power BI model. It is not a Spark problem, a Hive problem
         or a SQL problem; it is a GRAIN problem, and it appears
         wherever two fact tables are joined directly""")

    # ---- the fix ---------------------------------------------------------
    fixed = con.execute("""
        WITH ev AS (
            SELECT host, COUNT(*) AS events,
                   SUM(CASE WHEN status = '500' THEN 1 ELSE 0 END) AS errors
            FROM stream GROUP BY host),
             ord AS (
            SELECT host, COUNT(*) AS orders, SUM(revenue) AS revenue
            FROM batch GROUP BY host)
        SELECT o.host, o.orders, o.revenue, e.events, e.errors
        FROM ord o JOIN ev e ON o.host = e.host ORDER BY o.host
    """).fetchall()
    print(f"\n    the fix -- aggregate EACH SIDE to a common grain FIRST:")
    print(f"      {'host':<12}{'orders':>8}{'revenue':>10}{'events':>8}{'errors':>8}")
    for host, orders, rev, events, errors in fixed:
        print(f"      {host:<12}{orders:>8}{rev:>10,.0f}{events:>8}{errors:>8}")
    assert sum(r[3] for r in fixed) == n_stream
    assert abs(sum(r[2] for r in fixed) - batch_rev) < 1e-6
    print(f"""         {sum(r[3] for r in fixed)} events and {sum(r[2] for r in fixed):,.0f} revenue -- both totals now
         reconcile with the sources. Aggregate to a shared grain, THEN
         join. That single rule prevents most wrong numbers in a data
         warehouse, and it is worth stating in exactly those words""")

    # ---- what actually differs between the two legs ---------------------
    print("\n    the two legs are not interchangeable:")
    print(f"      {'':<20}{'batch (Sqoop)':<26}{'streaming (Flume)'}")
    for label, b, s in (
            ("arrives", "on a schedule", "continuously"),
            ("completeness", "a whole table, consistent", "whatever has landed"),
            ("late data", "impossible", "NORMAL -- and must be handled"),
            ("re-runnable", "yes, idempotent", "no -- events are consumed"),
            ("catches DELETEs", "on a full re-import", "never"),
            ("file sizes", "large, controllable", "small unless you roll"),
            ("failure means", "re-run the import", "gap in the data")):
        print(f"      {label:<20}{b:<26}{s}")
    print("""         'late data is normal' is the row that changes the design.
         A streaming aggregate for 09:00 is not final at 10:00, so
         either you accept eventual correctness or you keep a
         watermark and re-emit. The batch leg has no such problem,
         which is why the LAMBDA ARCHITECTURE keeps both""")

    # ---- lambda vs kappa -------------------------------------------------
    print("\n    the two architectures this experiment is really about:")
    print(f"      {'':<10}{'layers':<34}{'cost'}")
    print(f"      {'Lambda':<10}{'batch + speed + serving':<34}"
          f"{'the logic is written TWICE'}")
    print(f"      {'Kappa':<10}{'one streaming path, replayable':<34}"
          f"{'needs a log like Kafka'}")
    print("""         Lambda's real cost is not machines, it is that the same
         business rule exists in two codebases and they drift. Kappa
         removes the batch layer by making the stream replayable --
         which is why Kafka replaced Flume in most of these pipelines
         after about 2016. Say that and you have placed the whole
         syllabus in time""")

    # ---- the reconciliation check ---------------------------------------
    status_counts = Counter(
        r[0] for r in con.execute("SELECT status FROM stream").fetchall())
    print(f"\n    reconciliation: {dict(sorted(status_counts.items()))}")
    assert status_counts["200"] == 24
    assert sum(status_counts.values()) == 40
    print("""         the same 24 / 8 / 8 as experiments 12 and 17. Three
         experiments, three code paths, one set of numbers -- and if
         a change ever breaks one of them the suite fails on all
         three, which is the only reason to build the check""")

    con.close()
    for path in (batch, stream, os.path.join(tmp, "orders.db")):
        os.remove(path)
    os.rmdir(tmp)


if __name__ == "__main__":
    main()
