#!/usr/bin/env python3
"""Execute and verify the Course 13 A (Artificial Intelligence) lab programs.

Each experiment has two halves, and both run:

  NN_name.pl   the SWI-Prolog program for the lab exam. SWI-Prolog 9 installs from
               the Ubuntu archive (tools/data-science/setup_prolog.sh), and each file
               is consulted and its "% ?-" queries asked by prolog_lab.py.
  NN_name.py   the same logic, executed and asserted in Python.

FIVE EXPERIMENTS ALSO RUN PROLOG-STYLE RESOLUTION IN PYTHON. The pytholog
package implements SLD resolution over Horn clauses, so in the Python half the
family tree, the graph, the logic encodings, forward chaining and the expert
system are RUN as logic programs rather than simulated.

Its limits are asserted rather than glossed over -- pytholog has no list
terms, no arithmetic evaluation, no cut and no DCG notation, and each lab
script that hits one of those proves it before falling back to Python.

This runner also RUNS the .pl files: each must load without a warning, raise
no error but the one it demonstrates, give the answers below -- the same
figures the Python halves assert -- and carry no NOT EXECUTED marker, since it
is executed. (Until October 2026 SWI-Prolog could not be installed here, and
every .pl carried the marker.)

Usage:  python3 tools/data-science/run_ai_labs.py
"""
import io
import pathlib
import runpy
import sys
import traceback
import warnings

# tools/data-science/ -> the SECTION root, which is where everything this
# script reads and writes lives. Three levels up is the repository.
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent / "data-science"
LABS = ROOT / "labs" / "course-13a-ai"
# The one spelling of the honesty marker. It was "*** NOT EXECUTED ***"
# until the asterisks turned out to be Markdown that never fired, so the
# heading rendered them literally. build_site.py reads this same string to
# decide whether a lab page may claim "Executed, with assertions", and
# audit_content.py asserts every runner here spells it identically -- a
# runner that disagreed would pass while labelling an unrun lab as run.
MARKER = "NOT EXECUTED"
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


# What SWI-Prolog must answer: the same figures the Python halves assert.
ANSWERS = {
    "01_family_tree.pl": ["L = [asha, ravi, kiran, meena, bhanu].", "L = [ravi].", "?- father(X, kiran).\nfalse."],
    "02_lists.pl": ["X = [a, b, c, d].", "X = [c, b, a].", "N = 3.", "X = [a, b, c],\nY = []."],
    "03_maximum.pl": ["M = 9."],
    "04_flatten.pl": ["X = [1, 2, 3, 4, 5, 6, 7]."],
    "05_factorial_fib.pl": ["F = 120.", "F = 55.", "F = 832040."],
    "06_gcd.pl": ["G = 6.", "G = 1."],
    "07_cut_fail.pl": ["?- fly(tweety).\ntrue.", "?- fly(pingu).\nfalse."],
    "08_graph_search.pl": ["DFS: [a,b,d,e,g] (5 nodes)\nBFS: [a,c,g] (3 nodes)\ntrue."],
    "12_astar.pl": ["P = [arad, sibiu, rimnicu, pitesti, bucharest],\nC = 418 ;"],
    "13_map_colouring.pl": ["SA = blue,", "% the first of 18 answers"],
    "14_n_queens.pl": ["Qs = [1, 5, 8, 6, 3, 7, 2, 4].", "N = 92."],
    "15_logic.pl": ["?- wet_ground.\ntrue.", "L = [asha, meena]."],
    "16_chaining.pl": ["KB = [a, b, c, d, e]."],
    "17_expert_system.pl": ["      fever(patient)  -- a fact in working memory",
                            "?- assertz(rash(patient)), bacterial(patient).\ntrue."],
    "18_dcg.pl": ["?- sentence([cat, the, chases], []).\nfalse.",
                  "Tree = s(np(det(the), adj(big), n(cat)), vp(v(chases), np(det(a), n(mouse))))."],
    "19_naive_bayes.pl": ["P = 0.005291005291005291.", "P = 0.02057142857142857.", "C = no.", "P = 0.125."],
}
# The one error a query is there to show: SWI-Prolog raises it for a goal nothing defines.
EXPECTED_ERRORS = {"16_chaining.pl": ["ERROR: Unknown procedure: z/1"]}


def audit_prolog_files():
    """Every .pl runs in SWI-Prolog, cleanly, and gives its answers."""
    print(f"\n{'=' * 62}\nCourse 13 A -- running the Prolog files in SWI-Prolog\n{'=' * 62}")
    import shutil
    if not shutil.which("swipl"):
        return ["swipl not found: run tools/data-science/setup_prolog.sh"]
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import prolog_lab
    problems = []
    programs = sorted(p for p in LABS.glob("*.pl") if p.stem[0].isdigit())
    for pl in programs:
        text = pl.read_text()
        if MARKER in text:
            problems.append(f"{pl.name}: says '{MARKER}', but it is run")
        code, out = prolog_lab.run(pl)
        errors = [ln for ln in out.split("\n") if ln.startswith(("ERROR", "Warning"))]
        unexpected = [e for e in errors if e not in EXPECTED_ERRORS.get(pl.name, [])]
        missing = [a for a in ANSWERS.get(pl.name, []) if a not in out]
        if code or unexpected or missing or pl.name not in ANSWERS:
            problems.append(f"{pl.name}: exit {code}; unexpected {unexpected[:2]}; missing {missing[:2]}")
        n = len(prolog_lab.queries(text))
        print(f"  {pl.name:24s} {n:2d} quer{'y' if n == 1 else 'ies'}"
              + ("" if not problems or not problems[-1].startswith(pl.name) else "   *** FAILED ***"))

    covered = {int(pl.stem.split("_")[0]) for pl in programs}
    print(f"  {len(programs)} Prolog programs run" if not problems else "  PROBLEMS:")
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
        print("Every .pl ran in SWI-Prolog and gave the answers the Python halves")
        print("assert. In Python, five experiments ran as logic programs through")
        print("pytholog's SLD resolution; where its limits bite -- no lists, no")
        print("arithmetic, no cut, no DCG -- the script PROVES the limit first.")
    print(f"{'=' * 62}")
    return 1 if (failed or problems) else 0


if __name__ == "__main__":
    sys.exit(main())
