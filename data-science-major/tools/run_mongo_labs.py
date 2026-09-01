#!/usr/bin/env python3
"""Execute and verify the Course 10 (MongoDB) lab programs.

`mongod` cannot be installed in this environment -- the Debian repositories
that host `mongodb-org` are blocked by the egress policy -- so every experiment
comes in two halves:

  NN_name.js   the mongosh script for the lab exam. NEVER RUN HERE, and its
               first lines say so.
  NN_name.py   the same query logic through mongomock, asserted.

This runner executes the .py halves, and then AUDITS the .js halves: every one
must carry the NOT EXECUTED marker, and every .js must either have a .py
partner or be one of the three experiments that genuinely cannot have one
(replication, GridFS and transactions all need a server, and mongomock is a
library). That audit is the part that keeps this honest -- without it a .js
file could quietly lose its marker and start looking like a test result.

Usage:  python3 tools/run_mongo_labs.py
"""
import io
import pathlib
import runpy
import sys
import traceback
import warnings

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABS = ROOT / "labs" / "course-10-mongodb"

MARKER = "*** NOT EXECUTED ***"

# The experiments with no runnable half, and why. Anything else missing a .py
# partner is an omission, and this runner fails on it.
NO_PYTHON_HALF = {
    "01_install_shell":  "server commands only -- there is no query logic to run",
    "17_replication":    "needs three mongod processes; mongomock is not a server",
    "18_gridfs":         "mongomock does not implement GridFS",
    "19_transactions":   "transactions require a replica set",
}


def run_one(path):
    """Run a lab script in its own namespace, capturing its output."""
    buf = io.StringIO()
    stdout = sys.stdout
    sys.path.insert(0, str(path.parent))
    try:
        sys.stdout = buf
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            runpy.run_path(str(path), run_name="__main__")
        return True, buf.getvalue()
    except Exception:
        return False, buf.getvalue() + "\n" + traceback.format_exc()
    finally:
        sys.stdout = stdout
        sys.path.remove(str(path.parent))


def audit_the_mongosh_scripts():
    """Every .js must be marked NOT EXECUTED, and paired or explained."""
    print(f"\n{'=' * 62}\nCourse 10 -- auditing the mongosh scripts\n{'=' * 62}")
    problems = []
    scripts = sorted(p for p in LABS.glob("*.js") if p.stem[0].isdigit())

    for js in scripts:
        head = "".join(js.read_text().splitlines(keepends=True)[:12])
        if MARKER not in head:
            problems.append(f"{js.name}: missing the '{MARKER}' marker")

        partner = js.with_suffix(".py")
        if partner.exists():
            if js.stem in NO_PYTHON_HALF:
                problems.append(
                    f"{js.name}: listed as having no runnable half, but "
                    f"{partner.name} exists -- update NO_PYTHON_HALF")
        elif js.stem not in NO_PYTHON_HALF:
            problems.append(f"{js.name}: no {partner.name}, and no reason given")

    print(f"  {len(scripts)} mongosh scripts, all carrying '{MARKER}'"
          if not problems else "  PROBLEMS:")
    for p in problems:
        print(f"    *** {p}")

    print(f"  {len(NO_PYTHON_HALF)} experiments have no runnable half:")
    for stem, why in sorted(NO_PYTHON_HALF.items()):
        print(f"    {stem:18s} {why}")

    return problems


def main():
    if not LABS.exists():
        print(f"directory not present: {LABS.relative_to(ROOT)}")
        return 2

    print(f"\n{'=' * 62}\nCourse 10 -- Document Oriented Database\n{'=' * 62}")

    scripts = sorted(p for p in LABS.glob("*.py") if p.stem[0].isdigit())
    passed = failed = 0
    for script in scripts:
        ok, output = run_one(script)
        if ok:
            passed += 1
            print(f"\n  --- {script.name}")
        else:
            failed += 1
            print(f"\n  --- {script.name}   *** FAILED ***")
        for line in output.rstrip().splitlines():
            print(f"  {line}")

    problems = audit_the_mongosh_scripts()

    expected = 20 - len(NO_PYTHON_HALF)
    print(f"\n{'=' * 62}")
    print(f"{passed} of the {expected} runnable experiments executed and "
          f"asserted, {failed} failed")
    if len(scripts) != expected:
        print(f"*** expected {expected} runnable experiments, found {len(scripts)}")
    if problems:
        print(f"*** {len(problems)} problem(s) with the mongosh scripts")
    if not failed and not problems and len(scripts) == expected:
        print("Every query in the notes was executed through mongomock, and")
        print("every script that was NOT run says so in its own first lines.")
    print(f"{'=' * 62}")
    return 1 if (failed or problems or len(scripts) != expected) else 0


if __name__ == "__main__":
    sys.exit(main())
