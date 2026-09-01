#!/usr/bin/env python3
"""Execute and verify the Course 8 (Data Mining) and Course 9 (Python for Data
Analysis) lab programs.

Every script here RUNS. Each one asserts its results against the hand-computed
values written out in the notes, so the notes and the code check each other:
if either drifts, this fails.

The WEKA halves of the Course 8 experiments cannot run in this environment --
WEKA needs a host the egress policy blocks -- so they are documented as
click-paths in notes/sem-4/course-8-data-mining/lab.md and are clearly marked
NOT EXECUTED there. Nothing in this runner implies otherwise.

Usage:  python3 tools/run_data_labs.py [course8|course9]
"""
import io
import pathlib
import runpy
import sys
import traceback
import warnings

ROOT = pathlib.Path(__file__).resolve().parent.parent

SUITES = {
    "course8": (ROOT / "labs" / "course-8-datamining", "Course 8 -- Data Mining"),
    "course9": (ROOT / "labs" / "course-9-python-da", "Course 9 -- Python for Data Analysis"),
}


def run_one(path):
    """Run a lab script in its own namespace, capturing its output.

    Returns (ok, output). An AssertionError means a claim in the notes no
    longer matches what the code computes -- that is the whole point.
    """
    buf = io.StringIO()
    stdout, cwd = sys.stdout, pathlib.Path.cwd()
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


def run_suite(key):
    directory, title = SUITES[key]
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62}")

    if not directory.exists():
        print(f"  directory not present: {directory.relative_to(ROOT)}")
        return 0, 0

    scripts = sorted(p for p in directory.glob("*.py")
                     if p.stem[0].isdigit())
    if not scripts:
        print(f"  no lab scripts in {directory.relative_to(ROOT)} yet")
        return 0, 0

    passed = failed = 0
    for script in scripts:
        ok, output = run_one(script)
        if ok:
            passed += 1
            print(f"\n  --- {script.name}")
            for line in output.rstrip().splitlines():
                print(f"  {line}")
        else:
            failed += 1
            print(f"\n  --- {script.name}   *** FAILED ***")
            for line in output.rstrip().splitlines():
                print(f"  {line}")
    return passed, failed


def main():
    wanted = sys.argv[1:] or list(SUITES)
    unknown = [w for w in wanted if w not in SUITES]
    if unknown:
        print(f"unknown suite(s): {unknown}; choose from {list(SUITES)}")
        return 2

    total_passed = total_failed = 0
    for key in wanted:
        p, f = run_suite(key)
        total_passed += p
        total_failed += f

    print(f"\n{'=' * 62}")
    print(f"{total_passed} lab programs executed and asserted, {total_failed} failed")
    if total_failed == 0 and total_passed:
        print("Every hand-computed value in the notes was reproduced by running code.")
    print(f"{'=' * 62}")
    return 1 if total_failed else 0


if __name__ == "__main__":
    sys.exit(main())
