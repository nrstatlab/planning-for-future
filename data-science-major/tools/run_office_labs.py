#!/usr/bin/env python3
"""Execute and verify the Course 1 (Office Automation) lab programs.

Course 1's lab is Word, PowerPoint and Excel. None of the three can be
installed here, and for six of the fourteen experiments there is nothing to
install anyway -- assembling a computer, drawing a topology, writing a resume
and a letter, building a presentation and laying out a timetable produce
documents, not numbers.

The other eight are arithmetic, and arithmetic can be checked. Each has:

  the click-path   the menus, dialogs and formulas, written out in
                   notes/sem-1/course-1-computer-fundamentals/lab.md. That is
                   what the lab examiner asks you to demonstrate.

  NN_name.py       the same computation, executed and asserted, run by this
                   script.

The Python halves are NOT a substitute for the spreadsheet and the notes never
claim they are. They exist so that every FIGURE in the notes is produced by
running code -- when lab.md says grading on the total awards 19 of 20 students
an A, experiment 8 proves it on the actual class.

Course 1 was the last course in this repository with no executed verification
at all, which is exactly why an error survived in its class-results formulas:
nothing could catch it. These scripts import nothing but the standard library,
so they run wherever Python does.

Usage:  python3 tools/run_office_labs.py
"""
import io
import pathlib
import runpy
import sys
import traceback

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABS = ROOT / "labs" / "course-1-office"

# Experiment number -> why it has no runnable half.
DOCUMENT_ONLY = {
    1: "assembling and disassembling hardware",
    2: "observing and drawing a network topology",
    3: "a resume -- a Word document",
    4: "a leave letter -- a Word document",
    5: "a presentation with audio and video",
    6: "a timetable -- layout and formatting, no computation",
}
TOTAL_EXPERIMENTS = 14

# Not an experiment: Unit 1 and practice.md are largely number-system
# conversions, and practice.md tells the reader every answer in it was
# verified computationally. This is the file that makes that true.
EXTRA_SCRIPTS = ["unit1_number_systems.py", "unit4_excel_functions.py"]


def run_one(script):
    """Run one lab program, capturing everything it prints."""
    buffer = io.StringIO()
    stdout, sys.stdout = sys.stdout, buffer
    cwd = sys.path[:]
    sys.path.insert(0, str(LABS))
    try:
        runpy.run_path(str(script), run_name="__main__")
        return True, buffer.getvalue()
    except Exception:
        return False, buffer.getvalue() + "\n" + traceback.format_exc()
    finally:
        sys.stdout = stdout
        sys.path[:] = cwd


def audit():
    """Check the experiment list against what is actually on disk."""
    problems = []
    scripts = sorted(p for p in LABS.glob("*.py") if p.stem[0].isdigit())
    numbered = {int(p.stem.split("_")[0]) for p in scripts}
    expected = set(range(1, TOTAL_EXPERIMENTS + 1)) - set(DOCUMENT_ONLY)

    for name in EXTRA_SCRIPTS:
        if not (LABS / name).exists():
            problems.append(f"missing: {name}")

    missing = sorted(expected - numbered)
    if missing:
        problems.append(f"experiments with no script: {missing}")
    extra = sorted(numbered - expected)
    if extra:
        problems.append(f"scripts for document-only experiments: {extra}")

    print(f"\n  {len(numbered)} of {TOTAL_EXPERIMENTS} experiments compute "
          "something; the other "
          f"{len(DOCUMENT_ONLY)} produce documents:")
    for number, why in sorted(DOCUMENT_ONLY.items()):
        print(f"    {number:>2}  {why}")
    return problems


def cross_check_course_11():
    """The sales rows must still match the ones Course 11 analyses.

    Course 1 pivots them in a dictionary; Course 11 measures them with DAX;
    Course 12 B with Hive and Spark; Course 13 B with a warehouse query;
    Course 15 B with an ETL job. All six report ₹10,360 for the South region.
    That only means anything if the underlying rows are the same rows, so
    this asserts it rather than trusting it.
    """
    sys.path.insert(0, str(LABS))
    sys.path.insert(0, str(ROOT / "labs" / "course-11-bi"))
    try:
        import fixtures as course_1
        import importlib
        course_11 = importlib.import_module("fixtures")
        if course_11 is course_1:                       # name collision
            del sys.modules["fixtures"]
            sys.path.remove(str(LABS))
            course_11 = importlib.import_module("fixtures")

        star = course_11.star()
        theirs = sorted((row.product, row.region, row.date, int(row.qty),
                         int(row.revenue)) for row in star.itertuples())
        ours = sorted(course_1.sales_rows())
    except ImportError as exc:                          # pandas missing
        print(f"\n  Cross-course check SKIPPED: {exc}")
        return []
    finally:
        sys.modules.pop("fixtures", None)
        for path in (str(LABS), str(ROOT / "labs" / "course-11-bi")):
            while path in sys.path:
                sys.path.remove(path)

    south = sum(r[4] for r in ours if r[1] == "South")
    if ours != theirs:
        return [f"Course 1 and Course 11 sales rows have drifted apart:\n"
                f"    Course 1  {ours}\n    Course 11 {theirs}"]
    if south != 10360:
        return [f"South total is {south}, not 10360"]

    print(f"\n  Cross-course check: the {len(ours)} sales rows match Course "
          "11's exactly,")
    print(f"  and both put the South region at {south:,} -- the same figure "
          "Courses")
    print("  12 B, 13 B and 15 B reach with Hive, Spark, SQL and an ETL job.")
    return []


def main():
    print(f"\n{'=' * 62}\nCourse 1 -- Computer Fundamentals and Office "
          f"Automation\n{'=' * 62}")

    scripts = sorted(p for p in LABS.glob("*.py") if p.stem[0].isdigit())
    scripts += [LABS / name for name in EXTRA_SCRIPTS]
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

    problems = audit() + cross_check_course_11()
    for problem in problems:
        print(f"\n  PROBLEM: {problem}")

    print(f"\n{'=' * 62}")
    print(f"{passed} lab programs executed and asserted, {failed} failed")
    if not failed and not problems:
        print("Every figure quoted in the Course 1 notes was produced by")
        print("running code. The spreadsheet click-paths are in lab.md,")
        print("marked NOT EXECUTED -- nothing here implies a test that did")
        print("not run.")
    print(f"{'=' * 62}")
    return 1 if (failed or problems) else 0


if __name__ == "__main__":
    sys.exit(main())
