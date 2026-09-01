#!/usr/bin/env python3
"""Execute and verify the Course 11 (Business Intelligence Tools) lab programs.

Power BI Desktop is Windows-only and Tableau Desktop is proprietary; neither
can be installed here. So every experiment has two halves:

  the click-path   the exact menus, panes and dialogs you follow in the tool.
                   Written out in notes/sem-5/course-11-business-intelligence/
                   lab.md and marked NOT EXECUTED. That is what the lab
                   examiner asks you to demonstrate.

  NN_name.py       the same transformation, measure or join, executed and
                   asserted. Run by this script.

The Python halves are NOT a substitute for the tools and the notes never claim
they are. They exist so that every FIGURE in the notes is produced by running
code -- when unit-3.md says a fan trap turns 12,880 into 25,760, experiment 14
proves it.

Four experiments have no runnable half -- 1, 2, 8 and 12 are tool operation
with no computation to check. This script asserts that list against what is on
disk rather than leaving it implicit, so an experiment cannot go missing
unnoticed.

Usage:  python3 tools/run_bi_labs.py
"""
import io
import pathlib
import runpy
import sys
import traceback
import warnings

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABS = ROOT / "labs" / "course-11-bi"

# Experiment number -> why it has no runnable half.
CLICK_PATH_ONLY = {
    1:  "comparing the two tools -- a table, not a computation",
    2:  "building the same dashboard in both tools",
    8:  "connecting Tableau Public to a data source",
    12: "assembling a Tableau story from worksheets",
}
TOTAL_EXPERIMENTS = 15


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


def audit():
    """Every experiment is either runnable or listed with a reason."""
    print(f"\n{'=' * 62}\nCourse 11 -- auditing experiment coverage\n{'=' * 62}")

    runnable = sorted(int(p.stem.split("_")[0])
                      for p in LABS.glob("*.py") if p.stem[0].isdigit())
    accounted = set(runnable) | set(CLICK_PATH_ONLY)
    missing = sorted(set(range(1, TOTAL_EXPERIMENTS + 1)) - accounted)
    overlap = sorted(set(runnable) & set(CLICK_PATH_ONLY))

    problems = []
    if missing:
        problems.append(f"experiments neither runnable nor explained: {missing}")
    if overlap:
        problems.append(f"listed as click-path only but a .py exists: {overlap}")

    print(f"  {len(runnable)} runnable: {runnable}")
    print(f"  {len(CLICK_PATH_ONLY)} click-path only:")
    for n, why in sorted(CLICK_PATH_ONLY.items()):
        print(f"    {n:2d}  {why}")
    for p in problems:
        print(f"    *** {p}")
    return problems


def main():
    if not LABS.exists():
        print(f"directory not present: {LABS.relative_to(ROOT)}")
        return 2

    print(f"\n{'=' * 62}\nCourse 11 -- Business Intelligence Tools\n{'=' * 62}")

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

    problems = audit()

    print(f"\n{'=' * 62}")
    print(f"{passed} lab programs executed and asserted, {failed} failed")
    if not failed and not problems:
        print("Every figure quoted in the Course 11 notes was produced by")
        print("running code. The tool click-paths are in lab.md, marked")
        print("NOT EXECUTED -- nothing here implies a test that did not run.")
    print(f"{'=' * 62}")
    return 1 if (failed or problems) else 0


if __name__ == "__main__":
    sys.exit(main())
