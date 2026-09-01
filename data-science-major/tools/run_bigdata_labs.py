#!/usr/bin/env python3
"""Run and assert the Course 12 B practicals, and audit the ones that cannot run.

Course 12 B is the most environment-constrained course in the programme.
Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper are all uninstallable
here, so this runner does two jobs:

  1. EXECUTE the eleven Python halves, which assert every figure the notes
     quote -- HDFS block arithmetic, YARN scheduling, MapReduce with a real
     shuffle, Hive-style SQL through DuckDB, a real SQLite-to-Parquet import,
     Flume channel semantics, REAL Avro and REAL Parquet, the HBase data
     model and ZooKeeper's coordination recipes.

  2. AUDIT the fifteen files that cannot run, asserting that every one still
     carries '*** NOT EXECUTED ***'. If someone strips that marker without
     making the file runnable, this suite fails.

Experiment 17 needs PySpark, which lives in its own virtual environment
(tools/setup_spark.sh). If that environment is absent the experiment is
SKIPPED LOUDLY and the suite still passes -- the same graceful-skip pattern
the jsdom check uses in Course 7.
"""
import os
import pathlib
import subprocess
import sys
import traceback

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB = ROOT / "labs" / "course-12b-bigdata"
MARKER = "*** NOT EXECUTED ***"
SPARK_VENV = pathlib.Path(os.environ.get("SPARK_VENV", "/tmp/sparkenv"))

# The experiments that run in the ordinary interpreter.
PY_LABS = [
    ("04_blocks_replication", "4"),
    ("05_fault_tolerance", "5"),
    ("06_yarn_scheduling", "6"),
    ("07_wordcount", "7"),
    ("08_inverted_index", "8"),
    ("09_pig_equivalent", "9"),
    ("10_hive_duckdb", "10"),
    ("11_sqoop_equivalent", "11"),
    ("12_flume_equivalent", "12"),
    ("13_avro_parquet", "13"),
    ("14_pipeline", "14"),
    ("15_hbase_model", "15"),
    ("16_zookeeper_model", "16"),
]

# The files that document a tool this environment cannot install.
NOT_EXECUTED = {
    "01_install_hadoop.sh":  "Hadoop itself -- apt is blocked by the egress policy",
    "02_hdfs_commands.sh":   "needs a running NameNode",
    "03_architecture.sh":    "needs the five daemons and their logs",
    "04_hdfs_store.sh":      "needs HDFS",
    "05_fault_tolerance.sh": "needs DataNodes to kill",
    "06_yarn.sh":            "needs a ResourceManager",
    "09_analysis.pig":       "Pig is not installable",
    "10_hive.hql":           "Hive is not installable",
    "11_sqoop.sh":           "Sqoop needs an RDBMS and a cluster",
    "12_flume.conf":         "Flume is not installable",
    "15_hbase.rb":           "HBase is not installable",
    "16_zookeeper.sh":       "needs a 3-server ensemble",
    "17_spark_hbase.scala":  "needs the HBase connector; the PySpark half DOES run",
    "WordCount.java":        "needs the Hadoop jars to compile",
    "InvertedIndex.java":    "needs the Hadoop jars to compile",
}


def banner(text):
    print("\n" + "=" * 62)
    print(text)
    print("=" * 62)


def main():
    banner("Course 12 B -- Big Data Technologies")
    sys.path.insert(0, str(LAB))

    passed, failed = 0, 0
    for module, exp in PY_LABS:
        print(f"\n  --- {module}.py")
        try:
            mod = __import__(module)
            mod.main()
            passed += 1
        except Exception:
            traceback.print_exc()
            print(f"  FAILED: experiment {exp}")
            failed += 1

    # ---- experiment 17, in its own environment ---------------------------
    banner("Experiment 17 -- REAL Apache Spark")
    spark_python = SPARK_VENV / "bin" / "python"
    if not spark_python.exists():
        print(f"""
  SKIPPED. No PySpark environment at {SPARK_VENV}.
  Build it with:   bash tools/setup_spark.sh
  Then re-run.     The other 16 experiments are unaffected.

  This is a SKIP, not a pass. Nothing in the notes claims a Spark
  figure that this run did not produce.""")
        spark_ok = None
    else:
        proc = subprocess.run(
            [str(spark_python), str(LAB / "17_spark.py")],
            capture_output=True, text=True, cwd=str(LAB))
        noise = ("WARN", "SLF4J", "log4j", "FutureWarning", "require_minimum",
                 "Setting default log level", "To adjust logging",
                 "Using Spark's default", "Picked up JAVA_TOOL_OPTIONS")
        for line in proc.stdout.splitlines():
            if not any(n in line for n in noise):
                print(line)
        if proc.returncode != 0:
            print(proc.stderr[-2000:])
            print("  FAILED: experiment 17")
            failed += 1
            spark_ok = False
        else:
            passed += 1
            spark_ok = True

    # ---- audit the files that cannot run ---------------------------------
    banner("Course 12 B -- auditing the files that cannot run")
    missing = []
    for name, why in sorted(NOT_EXECUTED.items()):
        path = LAB / name
        if not path.exists():
            missing.append(f"{name}: FILE MISSING")
        elif MARKER not in path.read_text(encoding="utf-8"):
            missing.append(f"{name}: marker {MARKER!r} is GONE")
    if missing:
        for m in missing:
            print(f"  {m}")
        failed += len(missing)
    else:
        print(f"  {len(NOT_EXECUTED)} files, all carrying '{MARKER}'")
        print("  each one names the tool it needs and the runnable half that")
        print("  verifies its logic:")
        for name, why in sorted(NOT_EXECUTED.items()):
            print(f"    {name:<24}{why}")

    banner(f"{passed} lab programs executed and asserted, {failed} failed")
    print("covering all 17 prescribed experiments")
    if spark_ok:
        print("""Experiment 17 ran on a REAL SparkSession -- real RDDs, a real
shuffle inside reduceByKey, and a real DataFrame aggregate that
reproduces Course 11's 10,360 / 2,520 for the third time.""")
    elif spark_ok is None:
        print("""Experiment 17 was SKIPPED -- no PySpark environment. Every other
experiment ran. Nothing is claimed that was not executed.""")
    print("""Avro and Parquet are written by fastavro and pyarrow, so those files
are the real formats. Hadoop, Hive, Pig, Sqoop, Flume, HBase and
ZooKeeper cannot be installed here; their files say NOT EXECUTED and
this script asserts that they still do.""")
    print("=" * 62)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
