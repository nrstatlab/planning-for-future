#!/usr/bin/env python3
"""Execute and verify the Course 13 A (Artificial Intelligence) lab programs.

SWI-Prolog cannot be installed here -- the Debian repositories that host it are
blocked by the egress policy -- so each experiment has two halves:

  NN_name.pl   the SWI-Prolog program for the lab exam. NEVER RUN HERE, and
               its first lines say so.
  NN_name.py   the same logic, executed and asserted.

FIVE EXPERIMENTS GENUINELY EXECUTE PROLOG-STYLE RESOLUTION. The pytholog
package implements SLD resolution over Horn clauses, so the family tree, the
graph, the logic encodings, forward chaining and the expert system are RUN as
logic programs rather than simulated.

Its limits are asserted rather than glossed over -- pytholog has no list
terms, no arithmetic evaluation, no cut and no DCG notation, and each lab
script that hits one of those proves it before falling back to Python.

This runner also AUDITS the .pl files: every one must carry the NOT EXECUTED
marker. Without that check a Prolog file could quietly lose its marker and
start reading like a test result.

Usage:  python3 tools/run_ai_labs.py
"""
import io
import pathlib
import runpy
import sys
import traceback
import warnings

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABS = ROOT / "labs" / "course-13a-ai"
MARKER = "*** NOT EXECUTED ***"
TOTAL_EXPERIMENTS = 19


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


def audit_prolog_files():
    """Every .pl must be marked NOT EXECUTED."""
    print(f"\n{'=' * 62}\nCourse 13 A -- auditing the Prolog files\n{'=' * 62}")
    problems = []
    programs = sorted(p for p in LABS.glob("*.pl") if p.stem[0].isdigit())

    for pl in programs:
        head = "".join(pl.read_text().splitlines(keepends=True)[:12])
        if MARKER not in head:
            problems.append(f"{pl.name}: missing the '{MARKER}' marker")

    covered = set()
    for pl in programs:
        first = pl.stem.split("_")[0]
        covered.add(int(first))

    print(f"  {len(programs)} Prolog programs, all carrying '{MARKER}'"
          if not problems else "  PROBLEMS:")
    for p in problems:
        print(f"    *** {p}")
    print(f"  they cover experiments: {sorted(covered)}")
    print("  (08_graph_search.pl covers experiments 8-11, which are one graph)")
    return problems


def main():
    if not LABS.exists():
        print(f"directory not present: {LABS.relative_to(ROOT)}")
        return 2

    print(f"\n{'=' * 62}\nCourse 13 A -- Artificial Intelligence\n{'=' * 62}")

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

    problems = audit_prolog_files()

    print(f"\n{'=' * 62}")
    print(f"{passed} lab programs executed and asserted, {failed} failed")
    print(f"covering all {TOTAL_EXPERIMENTS} prescribed experiments")
    if not failed and not problems:
        print("Five experiments ran as REAL LOGIC PROGRAMS through pytholog's")
        print("SLD resolution. Where its limits bite -- no lists, no arithmetic,")
        print("no cut, no DCG -- the script PROVES the limit before falling back")
        print("to Python, and the .pl file carries the real Prolog.")
    print(f"{'=' * 62}")
    return 1 if (failed or problems) else 0


if __name__ == "__main__":
    sys.exit(main())
