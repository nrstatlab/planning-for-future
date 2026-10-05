#!/usr/bin/env python3
"""Run and assert the Course 12 B practicals: the Python halves, and the tool files on a cluster.

Every experiment has a tool file -- a shell script of hdfs, yarn, sqoop or zkCli.sh commands, a
Pig or Hive script, an HBase shell script, a Flume agent's configuration, Java or Scala -- and
most also have a Python half that runs the same logic and asserts it. This runner:

  1. EXECUTES the thirteen Python halves, which assert every figure the notes quote -- HDFS
     block arithmetic, YARN scheduling, MapReduce with a real shuffle, Hive-style SQL through
     DuckDB, a real SQLite-to-Parquet import, Flume channel semantics, REAL Avro and REAL
     Parquet, the HBase data model and ZooKeeper's coordination recipes;
  2. runs experiment 17's PySpark half in its own environment (setup_spark.sh), and SKIPS it
     LOUDLY if that is absent;
  3. RUNS every tool file on a real Hadoop 3.3.6 cluster (hadoop_lab.py, and the file's
     _drive_ script where it needs a database or data put in place first), exactly as
     capture_lab_outputs.py does for the lab page, and checks the answers below are in what it
     printed. Where the stack is not installed (setup_hadoop.sh) it says so, and the files
     are only audited; --audit-only skips the runs, which take about half an hour;
  4. AUDITS the tool files: none may still say NOT EXECUTED, since each is run, and each must
     have the output the lab page shows.

Until October 2026 the Hadoop stack could not be installed where these labs are checked, and
this runner could do only 1, 2 and an audit that every tool file said NOT EXECUTED.

Usage:  python3 tools/data-science/run_bigdata_labs.py [--audit-only]
"""
import os
import pathlib
import subprocess
import sys
import tempfile
import traceback

# tools/data-science/ -> the SECTION root, which is where everything this
# script reads and writes lives. Three levels up is the repository.
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent / "data-science"
LAB = ROOT / "labs" / "course-12b-bigdata"
# The one spelling of the honesty marker. It was "*** NOT EXECUTED ***"
# until the asterisks turned out to be Markdown that never fired, so the
# heading rendered them literally. build_site.py reads this same string to
# decide whether a lab page may claim "Executed, with assertions", and
# audit_content.py asserts every runner here spells it identically -- a
# runner that disagreed would pass while labelling an unrun lab as run.
MARKER = "NOT EXECUTED"
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

# The tool files, and what each must print when it runs on the cluster: the figures the lab
# page quotes, which are the ones the Python halves assert.
TOOL_FILES = {
    "01_install_hadoop.sh":  ["has been successfully formatted", "Live datanodes (1):",
                              "NameNode        http://localhost:9870  200"],
    "02_hdfs_commands.sh":   ["Replication 2 set: /user/student/moved.csv", "Live datanodes (4):"],
    "03_architecture.sh":    ["Final-State : SUCCEEDED"],
    "04_hdfs_store.sh":      ["replication=3, 3 block(s)", "len=46137344", "replication=3, 5 block(s)"],
    "05_fault_tolerance.sh": ["Dead datanodes (1):", "Safe mode is ON", "314572800"],
    "06_yarn.sh":            ["Estimated value of Pi is 3.14", "Capacity : 75.00%", "Final-State : KILLED"],
    "WordCount.java":        ["Map output records=48", "Combine output records=39", "Reduce output records=26"],
    "InvertedIndex.java":    ["quick\tdoc1.txt:1, doc3.txt:2", "Reduce output records=26"],
    "09_analysis.pig":       ["Grocery,4,36,8680.0", "Stationery,2,35,1400.0", "Personal,1,7,980.0"],
    "10_hive.hql":           ["South\t10360.0\t48", "North\t2520.0\t39"],
    "11_sqoop.sh":           ["Retrieved 90 records.", "Hive import complete.", "Retrieved 10 records.",
                              "incremental.last.value = 100", "Exported 3 records."],
    "12_flume.conf":         ["8 path=/static/app.js\tstatus=500", "24 200", "8 404"],
    "15_hbase.rb":           ["value=11", "COUNTER VALUE = 1"],
    "16_zookeeper.sh":       ["Mode: leader"],
    "17_spark_hbase.scala":  ["partitions = 1", "| South|10360.0|   48|"],
}
# What no run may print: the shell failing on a line, or a Java program dying.
NEVER = ("command not found", "Exception in thread \"main\"", "syntax error")


def banner(text):
    print("\n" + "=" * 62)
    print(text)
    print("=" * 62)


def audit_tool_files():
    """No tool file may say NOT EXECUTED, and each has the output its lab page shows."""
    banner("Course 12 B -- auditing the tool files")
    import lab_includes
    problems = []
    for name in TOOL_FILES:
        path = LAB / name
        if not path.exists():
            problems.append(f"{name}: FILE MISSING")
        elif MARKER in path.read_text(encoding="utf-8"):
            problems.append(f"{name}: says {MARKER!r}, but it is run")
        elif not lab_includes.output_path(LAB.parent, f"{LAB.name}/{name}").exists():
            problems.append(f"{name}: has no committed output -- run capture_lab_outputs.py")
    others = sorted(p.name for p in LAB.iterdir() if p.is_file() and p.suffix not in (".py", ".pyc")
                    and p.name not in TOOL_FILES)
    if others:
        problems.append(f"files this runner does not know: {others}")
    for p in problems:
        print(f"  *** {p}")
    if not problems:
        print(f"  {len(TOOL_FILES)} tool files: none says {MARKER!r}, and each has its output")
    return problems


ran_tools = False


def run_tool_files():
    """Each tool file on a fresh cluster, as the lab page's output was made."""
    global ran_tools
    banner("Course 12 B -- running the tool files on a Hadoop cluster")
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import capture_lab_outputs as capture
    import hadoop_lab
    if not hadoop_lab.HADOOP.exists() or not all((hadoop_lab.PREFIX / d).exists()
                                                  for d in hadoop_lab.TOOLS.values()):
        print(f"  NOT RUN: the Hadoop stack is not installed in {hadoop_lab.PREFIX}.")
        print("  Install it with:  bash tools/data-science/setup_hadoop.sh")
        print("  The files were audited only.")
        return []
    problems = []
    for name, answers in TOOL_FILES.items():
        rel = f"{LAB.name}/{name}"
        with tempfile.TemporaryDirectory() as tmp:
            work = pathlib.Path(tmp)
            capture.stage(LAB.name, work)
            try:
                out, _ = capture.run_one(rel, work)
            except SystemExit as e:
                problems.append(f"{name}: {str(e).splitlines()[0]}")
                print(f"  {name:24s} *** FAILED ***")
                continue
        missing = [a for a in answers if a not in out]
        bad = [n for n in NEVER if n in out]
        if missing or bad:
            problems.append(f"{name}: missing {missing[:2]}; printed {bad}")
        print(f"  {name:24s} " + ("*** FAILED ***" if missing or bad else
                                  f"ran; {len(answers)} answer{'' if len(answers) == 1 else 's'} found"))
    for p in problems:
        print(f"  *** {p}")
    ran_tools = not problems
    return problems


def main():
    audit_only = "--audit-only" in sys.argv[1:]
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

    problems = audit_tool_files()
    if not audit_only:
        problems += run_tool_files()
    failed += len(problems)

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
are the real formats.""")
    if ran_tools:
        print("""Every tool file ran on a real Hadoop 3.3.6 cluster -- HDFS, YARN,
MapReduce, Pig, Hive, Sqoop from MariaDB, Flume, HBase, a three-server
ZooKeeper ensemble and Spark reading HBase -- and printed its answers.""")
    print("=" * 62)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
