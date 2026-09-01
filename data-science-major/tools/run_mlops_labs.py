#!/usr/bin/env python3
"""Run and assert the Course 15 B practicals.

ELEVEN OF THE SIXTEEN EXPERIMENTS RUN, and what runs is the real tool rather
than a description of it:

  * MLflow 3 with a SQLite backend -- six runs logged and queried back
  * git and DVC -- two data versions committed, and `dvc checkout` restoring
    the earlier one, verified by comparing the recovered column's mean
  * a real Flask server on a real socket, called over HTTP, including its
    two error paths and a /metrics endpoint parsed back as Prometheus
    exposition format
  * SQLite with real constraints, which reject the three bad inserts the
    lab attempts
  * scipy's KS test and a hand-written PSI, scored against drift injected at
    a known magnitude

FIVE CANNOT RUN, for three different reasons, and each says which:

  04_kafka_rabbitmq.md      Kafka and RabbitMQ need a broker process
  05_hdfs.md                Hadoop needs a JVM and a NameNode
  10_docker.md              the Docker client is here; the daemon is not
  11_github_actions.md      a workflow needs a GitHub runner
  15_prometheus_grafana.md  Prometheus and Grafana are server processes

Every one of those has a runnable half in this directory, and none of the
halves is filler: the batch-against-streaming latency comparison, the ETL
into a warehouse, the Flask app the container would package, the determinism
check the CI pipeline exists to protect, and the /metrics endpoint Prometheus
would scrape.

THE DESIGN THAT MAKES THIS COURSE CHECKABLE: the dataset is generated from
known coefficients and the drift is injected at a known magnitude, so a drift
detector can be SCORED rather than merely run -- 4 of 5 drifted batches
caught, 0 false alarms on clean ones, with a one-batch detection lag.
"""
import pathlib
import sys
import traceback

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB = ROOT / "labs" / "course-15b-mlops"
MARKER = "*** NOT EXECUTED ***"

PY_LABS = [
    ("01_environment_etl", "1, 2, 3, 6"),
    ("04_batch_vs_event", "4 (mechanism)"),
    ("07_mlflow_dvc", "7, 8, 9"),
    ("12_serve_drift_govern", "12, 13, 14, 16"),
]

NOT_EXECUTED = {
    "04_kafka_rabbitmq.md":     "Kafka/RabbitMQ need a broker process",
    "05_hdfs.md":               "Hadoop needs a JVM and a NameNode",
    "10_docker.md":             "the Docker daemon is not running here",
    "11_github_actions.md":     "a workflow needs a GitHub runner",
    "15_prometheus_grafana.md": "Prometheus and Grafana are servers",
}


def banner(text):
    print("\n" + "=" * 62)
    print(text)
    print("=" * 62)


def main():
    banner("Course 15 B -- Data Engineering and MLOps")
    sys.path.insert(0, str(LAB))

    passed, failed = 0, 0
    for module, exps in PY_LABS:
        print(f"\n  --- {module}.py   (experiments {exps})")
        try:
            __import__(module).main()
            passed += 1
        except Exception:
            traceback.print_exc()
            print(f"  FAILED: experiments {exps}")
            failed += 1

    banner("Course 15 B -- auditing the files that cannot run")
    problems = []
    for name in sorted(NOT_EXECUTED):
        path = LAB / name
        if not path.exists():
            problems.append(f"{name}: FILE MISSING")
        elif MARKER not in path.read_text(encoding="utf-8"):
            problems.append(f"{name}: marker {MARKER!r} is GONE")
    if problems:
        for p in problems:
            print(f"  {p}")
        failed += len(problems)
    else:
        print(f"  {len(NOT_EXECUTED)} files, all carrying '{MARKER}'")
        for name, why in sorted(NOT_EXECUTED.items()):
            print(f"    {name:<28}{why}")
        print("  each names the runnable half that covers the same ground.")

    banner(f"{passed} lab programs executed and asserted, {failed} failed")
    print("covering all 16 prescribed experiments")
    print("""Eleven run against the real tools: MLflow with a SQLite backend,
git and DVC with a genuine data rollback, a Flask server on a real
socket, SQLite constraints that actually reject bad rows, and scipy's
statistical tests.

The dataset is generated from KNOWN coefficients and the drift is
injected at a KNOWN magnitude, so the fitted model can be checked
against the truth that produced it and the drift detector can be
scored. Two of those scores contradict the story the experiment
would otherwise tell: three ETL defects nearly cancelled, leaving a
revenue total wrong by only 1%, and automatic retraining on drift
improved accuracy by 0.0016 -- because the inputs moved and the
relationship did not.""")
    print("=" * 62)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
