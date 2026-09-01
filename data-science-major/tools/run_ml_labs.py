#!/usr/bin/env python3
"""Execute and verify the Course 12 A (Machine Learning) lab programs.

EVERYTHING IN THIS COURSE RUNS. scikit-learn, NumPy, pandas, SciPy and
matplotlib are all installed, so all 12 practicals execute and every figure
quoted in the notes is asserted here. There is no "NOT EXECUTED" file anywhere
in Course 12 A -- unlike Courses 6, 8, 10, 11 and 13 B, nothing it needs is
blocked by this environment's egress policy.

Two cross-course checks run as part of the suite:

  * experiment 6 asserts that scikit-learn reproduces COURSE 4's hand-computed
    regression -- slope 4.3030, intercept 43.0303, R^2 0.9958. If the two
    courses ever disagree, one of them is wrong and this fails.
  * experiments 8 and 9 reproduce COURSE 8's entropy (0.2467 information gain)
    and Naive Bayes posteriors (0.005291 and 0.020571) exactly.

Every script fixes its random seed, so the figures in the notes are
reproducible on any machine.

Usage:  python3 tools/run_ml_labs.py
"""
import io
import pathlib
import runpy
import sys
import traceback
import warnings

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABS = ROOT / "labs" / "course-12a-ml"
TOTAL_EXPERIMENTS = 12


def run_one(path):
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


def main():
    if not LABS.exists():
        print(f"directory not present: {LABS.relative_to(ROOT)}")
        return 2

    print(f"\n{'=' * 62}\nCourse 12 A -- Machine Learning\n{'=' * 62}")

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

    missing = TOTAL_EXPERIMENTS - len(scripts)
    print(f"\n{'=' * 62}")
    print(f"{passed} of {TOTAL_EXPERIMENTS} lab programs executed and asserted, "
          f"{failed} failed")
    if missing:
        print(f"*** {missing} experiment(s) not present")
    if not failed and not missing:
        print("Every practical in this course RUNS. No file here is marked")
        print("NOT EXECUTED, because nothing this course needs is blocked.")
        print("Course 4's regression and Course 8's entropy and Naive Bayes")
        print("figures are reproduced exactly, so the courses check each other.")
    print(f"{'=' * 62}")
    return 1 if (failed or missing) else 0


if __name__ == "__main__":
    sys.exit(main())
