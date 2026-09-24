"""Experiment 17 -- process HBase datasets using Spark integration with Hadoop.

THIS EXPERIMENT RUNS REAL SPARK. PySpark 4.2 installs from PyPI and Java 21 is
present, so a genuine SparkSession starts, real RDDs are built, and a real
shuffle happens inside reduceByKey. Nothing here is a simulation.

What is NOT real: HBase. The dataset comes from the experiment 15 model
instead of an HBase table, and `17_spark_hbase.scala` carries the connector
code, marked NOT EXECUTED. The Spark half is the half worth verifying, and it
is verified.

Run with:  /tmp/sparkenv/bin/python 17_spark.py
or let tools/run_bigdata_labs.py find the environment for you.
"""
import os
import sys

import fixtures as f


def spark_available():
    try:
        import pyspark  # noqa: F401
        return True
    except ImportError:
        return False


def main():
    print("  Experiment 17 -- Spark on the Hadoop stack")

    if not spark_available():
        print("""
    PySpark is not importable from this interpreter.
    Run tools/setup_spark.sh, then use /tmp/sparkenv/bin/python.
    SKIPPED -- and this line is what a skipped experiment looks like.""")
        return False

    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F

    spark = (SparkSession.builder
             .appName("course-12b-exp-17")
             .master("local[2]")
             .config("spark.ui.enabled", "false")
             .config("spark.sql.shuffle.partitions", "4")
             .getOrCreate())
    spark.sparkContext.setLogLevel("ERROR")
    print(f"\n    real SparkSession: version {spark.version}, "
          f"master {spark.sparkContext.master}")

    # ---- RDD: the word count from experiment 7, on a real engine ---------
    rdd = spark.sparkContext.parallelize(list(f.DOCS.values()), 3)
    counts = (rdd.flatMap(lambda line: line.split())
                 .map(lambda w: (w, 1))
                 .reduceByKey(lambda a, b: a + b))
    got = dict(counts.collect())
    print(f"\n    RDD word count: {len(got)} distinct words, "
          f"{sum(got.values())} total")
    assert sum(got.values()) == 48
    assert got["the"] == 5 and got["big"] == 4 and got["dog"] == 4
    print(f"      partitions: input {rdd.getNumPartitions()}, "
          f"after reduceByKey {counts.getNumPartitions()}")
    print("""         IDENTICAL to experiment 7's MapReduce answer, on a real
         distributed engine. reduceByKey is map -> COMBINE -> shuffle
         -> reduce; Spark applies the combiner automatically, which
         MapReduce makes you ask for""")

    # ---- the one comparison that matters --------------------------------
    print("\n    reduceByKey against groupByKey -- the same answer, not the same job:")
    grouped = (rdd.flatMap(lambda line: line.split())
                  .map(lambda w: (w, 1))
                  .groupByKey()
                  .mapValues(len))
    assert dict(grouped.collect()) == got
    # measure the map-side combine for THIS partitioning rather than quoting
    # experiment 7's number, which was per-document and not per-partition
    per_part = (rdd.flatMap(lambda line: line.split())
                   .map(lambda w: (w, 1))
                   .mapPartitions(lambda it: [len({k for k, _ in it})])
                   .collect())
    combined = sum(per_part)
    print(f"      groupByKey  : shuffles all 48 pairs, then counts")
    print(f"      reduceByKey : combines to {combined} map-side "
          f"({per_part} per partition), then shuffles")
    assert combined < 48
    print("""         same output, and groupByKey moves every record across
         the network while reduceByKey moves one per key per
         partition. On a real corpus groupByKey is how you produce an
         OutOfMemoryError on a single hot key. This is the most
         examined Spark question there is""")

    # ---- lazy evaluation and the DAG ------------------------------------
    lineage = (rdd.flatMap(lambda l: l.split())
                  .filter(lambda w: len(w) > 3)
                  .map(lambda w: (w[0], 1)))
    print(f"\n    lazy evaluation: three transformations queued, nothing ran")
    print(f"      the DAG has {len(lineage.toDebugString().decode().splitlines())} "
          f"stages of lineage recorded")
    result = lineage.reduceByKey(lambda a, b: a + b).collect()
    print(f"      .collect() is the ACTION -- it returned {len(result)} keys")
    assert len(result) > 0
    print("""         transformations build a DAG; only an ACTION submits it.
         That is why a typo in a map() surfaces at collect() and not
         where you wrote it -- and why Spark can fuse the whole chain
         into one pass over the data""")

    # ---- DataFrames over the shared star schema -------------------------
    sdf = spark.createDataFrame(f.SALES_DF)
    agg = (sdf.groupBy("region")
              .agg(F.sum("revenue").alias("revenue"),
                   F.sum("profit").alias("profit"))
              .orderBy(F.desc("revenue")))
    rows = {r["region"]: r["revenue"] for r in agg.collect()}
    print(f"\n    DataFrame aggregate over the SAME nine rows:")
    for r in agg.collect():
        print(f"      {r['region']:<8}{r['revenue']:>10,.0f}{r['profit']:>9,.0f}")
    assert rows["South"] == 10360.0 and rows["North"] == 2520.0
    assert sum(rows.values()) == f.total_revenue()
    print("""         10,360 and 2,520 again -- the third engine to produce
         them, after Course 11's DAX and experiment 10's SQL. Spark,
         DuckDB and Power BI agree, which is what reusing one dataset
         across three courses was for""")

    # ---- the logs, from experiment 12 ------------------------------------
    logs = spark.sparkContext.parallelize(f.access_logs(40), 2)
    by_status = (logs.map(lambda ln: (ln.rsplit(" ", 2)[-2], 1))
                     .reduceByKey(lambda a, b: a + b)
                     .collectAsMap())
    print(f"\n    the ingested access logs, aggregated in Spark:")
    for code in sorted(by_status):
        print(f"      HTTP {code}: {by_status[code]}")
    assert by_status["200"] == 24 and by_status["404"] == 8
    assert sum(by_status.values()) == 40
    print("""         the same 24 / 8 / 8 the Flume agent produced in
         experiment 12. Ingest with Flume, analyse with Spark, on
         bytes that were never transformed in between -- that is the
         end-to-end story the syllabus asks for""")

    # ---- why Spark replaced MapReduce -----------------------------------
    print("\n    Spark against MapReduce, on the parts that decided it:")
    print(f"      {'':<22}{'MapReduce':<26}{'Spark'}")
    for label, mr, sp in (
            ("between stages", "writes to HDFS", "keeps in MEMORY"),
            ("iterative jobs", "re-reads every pass", "cache() once"),
            ("API", "map and reduce only", "~80 operators"),
            ("interactive", "no", "yes -- the shell"),
            ("fault tolerance", "re-run the task", "recompute from LINEAGE"),
            ("streaming", "no", "structured streaming"),
            ("runs on YARN", "yes", "yes -- same cluster")):
        print(f"      {label:<22}{mr:<26}{sp}")
    print("""         the decisive row is the first. A ten-iteration machine
         learning job writes to HDFS nine times under MapReduce and
         zero times under Spark, which is where the '100x faster'
         headline comes from -- it is a claim about ITERATIVE jobs,
         and quoting it for a single-pass job is wrong""")

    # ---- caching, measured ----------------------------------------------
    base = spark.sparkContext.parallelize(range(200_000), 4).map(lambda x: x * 2)
    base.cache()
    first = base.sum()
    second = base.sum()
    assert first == second == sum(x * 2 for x in range(200_000))
    print(f"\n    cache(): two actions over the same RDD, sum = {first:,}")
    print(f"      storage level after cache(): {base.getStorageLevel()}")
    print("""         WITHOUT cache() the second sum recomputes the map from
         the source. With it, only the first action pays. Caching is
         the single highest-value Spark optimisation and the one
         students forget, because nothing FAILS without it -- the job
         is merely twice as slow""")
    base.unpersist()

    spark.stop()
    print("\n    SparkSession stopped cleanly.")
    return True


if __name__ == "__main__":
    main()
