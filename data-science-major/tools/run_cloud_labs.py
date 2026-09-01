#!/usr/bin/env python3
"""Run and assert the Course 13 B practicals, and audit the ones that cannot run.

THERE IS NO CLOUD ACCOUNT FOR THIS REPOSITORY AND NONE WILL BE CREATED.
Signing up requires a payment card and accepts a billing relationship, which
is not something a study repository should do on anyone's behalf. So the
console click-paths and CLI commands live in 14 Markdown files, each marked
'*** NOT EXECUTED ***', each naming the runnable half that verifies its logic.

What DOES run is more than it sounds, because most of what this course
teaches is not proprietary:

  * IAM's policy evaluation algorithm, implemented and exercised -- explicit
    deny, allow, implicit deny, and the demonstration that adding admin
    access does not defeat a deny.
  * Object-store key semantics: prefixes, the absence of directories, the
    copy-plus-delete that stands in for a rename, versioning and delete
    markers.
  * The pricing arithmetic for storage classes, egress, block against file
    against object, BigQuery per-TB and Redshift per-node-hour.
  * Hypervisor overcommit, and the point at which it fails.
  * A REAL web server, serving a REAL page over TCP (experiment 2).
  * A REAL ETL pipeline into a REAL columnar warehouse (experiments 8-12).
  * An autoscaling control loop, measured honestly.
  * A REAL scikit-learn model and a REAL AutoML search.
  * A REAL HTTP endpoint serving that model, called over the network
    (experiment 15).
"""
import pathlib
import sys
import traceback

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB = ROOT / "labs" / "course-13b-cloud"
MARKER = "*** NOT EXECUTED ***"

PY_LABS = [
    ("01_vm_and_hosting", "1, 2, 7"),
    ("03_iam_and_account", "3, 10"),
    ("04_storage", "4, 5, 6"),
    ("09_etl_warehouse", "8, 9, 12"),
    ("11_train_and_automl", "11, 14"),
    ("13_monitoring_autoscale", "13"),
    ("15_deploy_endpoint", "15"),
]

NOT_EXECUTED = {
    "01_create_vm.md":          "VMware Workstation is not installed",
    "02_web_server.md":         "Apache/XAMPP on a VM; the page IS served locally",
    "03_account_setup.md":      "needs a cloud account -- none exists",
    "04_buckets.md":            "needs S3",
    "05_ebs.md":                "needs EC2 and EBS",
    "06_efs.md":                "needs EFS and two instances",
    "07_notebook.md":           "needs a cloud VM or SageMaker",
    "08_cloud_db.md":           "needs RDS / BigQuery / Cosmos DB",
    "10_sagemaker_notebook.md": "needs SageMaker and IAM",
    "11_sagemaker_train.md":    "needs a SageMaker training job",
    "12_etl_to_warehouse.md":   "needs Glue and Redshift/BigQuery",
    "13_monitoring.md":         "needs CloudWatch",
    "14_automl.md":             "needs Autopilot / Vertex / Azure AutoML",
    "15_deploy.md":             "needs a SageMaker endpoint",
}


def banner(text):
    print("\n" + "=" * 62)
    print(text)
    print("=" * 62)


def main():
    banner("Course 13 B -- Cloud Computing for Data Science")
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

    banner("Course 13 B -- auditing the files that cannot run")
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
        print("  each names the service it needs and the runnable half that")
        print("  verifies its logic:")
        for name, why in sorted(NOT_EXECUTED.items()):
            print(f"    {name:<26}{why}")

    banner(f"{passed} lab programs executed and asserted, {failed} failed")
    print("covering all 15 prescribed experiments")
    print("""No cloud account exists and none was created. Every claim about a
provider's behaviour is documented, not demonstrated -- but the
algorithms behind them are implemented and run: IAM evaluation,
object-store prefixes, the pricing arithmetic, hypervisor overcommit,
an autoscaling control loop, and a REAL model served over a REAL
HTTP endpoint that this script calls and shuts down.""")
    print("=" * 62)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
