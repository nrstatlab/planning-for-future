#!/usr/bin/env python3
"""Execute and verify the Course 10 (MongoDB) lab programs.

Every experiment has a mongosh script, NN_name.js, the one for the lab exam, and sixteen
also have NN_name.py, the same query logic through mongomock, asserted. This runner:

  1. runs the .py halves, whose assertions fail the build on a wrong answer;
  2. runs every .js on a real MongoDB server, typed into mongosh as a student would, through
     mongo_lab.py, or its driver (_drive_17_replication.py starts a replica set of three,
     _drive_18_gridfs.py runs mongofiles), and fails if one does not run to its end. Where
     mongod or mongosh is not installed (setup_mongodb.sh, npm install), it says so, and
     the scripts are only audited;
  3. audits the .js files: none may still say NOT EXECUTED, and each must have a .py
     partner or a reason it has none;
  4. checks that 00_sample_data.js, which the scripts load, holds exactly fixtures.py's data.

Until October 2026 mongod could not be installed where these labs are checked, and this
runner could do only 1 and 3, with every .js marked NOT EXECUTED.

Usage:  python3 tools/data-science/run_mongo_labs.py
"""
import io
import json
import pathlib
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import traceback
import warnings

# tools/data-science/ -> the SECTION root, which is where everything this
# script reads and writes lives. Three levels up is the repository.
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent / "data-science"
LABS = ROOT / "labs" / "course-10-mongodb"

# The one spelling of the honesty marker. It was "*** NOT EXECUTED ***"
# until the asterisks turned out to be Markdown that never fired, so the
# heading rendered them literally. build_site.py reads this same string to
# decide whether a lab page may claim "Executed, with assertions", and
# audit_content.py asserts every runner here spells it identically -- a
# runner that disagreed would pass while labelling an unrun lab as run.
MARKER = "NOT EXECUTED"

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
    """No .js may still say NOT EXECUTED, and each must be paired or explained."""
    print(f"\n{'=' * 62}\nCourse 10 -- auditing the mongosh scripts\n{'=' * 62}")
    problems = []
    scripts = sorted(p for p in LABS.glob("*.js") if p.stem[0].isdigit() and p.stem != "00_sample_data")

    for js in scripts:
        if MARKER in js.read_text():
            problems.append(f"{js.name}: still says '{MARKER}', but the scripts are run")

        partner = js.with_suffix(".py")
        if partner.exists():
            if js.stem in NO_PYTHON_HALF:
                problems.append(
                    f"{js.name}: listed as having no runnable half, but "
                    f"{partner.name} exists -- update NO_PYTHON_HALF")
        elif js.stem not in NO_PYTHON_HALF:
            problems.append(f"{js.name}: no {partner.name}, and no reason given")

    print(f"  {len(scripts)} mongosh scripts, none marked '{MARKER}'"
          if not problems else "  PROBLEMS:")
    for p in problems:
        print(f"    *** {p}")

    print(f"  {len(NO_PYTHON_HALF)} experiments have no runnable half:")
    for stem, why in sorted(NO_PYTHON_HALF.items()):
        print(f"    {stem:18s} {why}")

    return problems


def check_the_sample_data():
    """00_sample_data.js must hold exactly the documents in fixtures.py."""
    sys.path.insert(0, str(LABS))
    import fixtures
    sys.path.remove(str(LABS))
    js = (LABS / "00_sample_data.js").read_text()
    problems = []
    for name in ("students", "courses", "enrollments"):
        m = re.search(rf"db\.{name}\.insertMany\((\[.*?\n\])\)", js, re.S)
        if not m or json.loads(m.group(1)) != getattr(fixtures, name.upper()):
            problems.append(f"00_sample_data.js: its {name} differ from fixtures.{name.upper()}")
    print(f"\n  00_sample_data.js holds fixtures.py's data exactly" if not problems else "")
    for p in problems:
        print(f"    *** {p}")
    return problems


def run_the_mongosh_scripts():
    """Each .js on a fresh server, through mongo_lab.py or its driver. Returns problems."""
    print(f"\n{'=' * 62}\nCourse 10 -- the mongosh scripts, on a real server\n{'=' * 62}")
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import mongo_lab
    missing = [str(t) for t in (mongo_lab.BIN / "mongod", mongo_lab.MONGOSH) if not t.exists()]
    if missing:
        print(f"  not installed: {', '.join(missing)} -- the scripts are only audited.\n"
              "  Run tools/data-science/setup_mongodb.sh and npm --prefix tools/data-science install.")
        return [], 0
    problems, ran = [], 0
    scripts = sorted(p for p in LABS.glob("*.js") if p.stem[0].isdigit() and p.stem != "00_sample_data")
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp) / LABS.name
        shutil.copytree(LABS, work, ignore=shutil.ignore_patterns("output", "__pycache__"))
        for js in scripts:
            driver = work / f"_drive_{js.stem}.py"
            cmd = [sys.executable, driver.name] if driver.exists() else \
                  [sys.executable, str(pathlib.Path(mongo_lab.__file__)), js.name]
            r = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=1800,
                               env={**__import__("os").environ, "PYTHONPATH": str(pathlib.Path(mongo_lab.__file__).parent)})
            if r.returncode == 0:
                ran += 1
                print(f"  {js.name:<24} ran, {len(r.stdout.splitlines())} lines")
            else:
                problems.append(f"{js.name}: " + (r.stderr or r.stdout).strip().splitlines()[-1])
                print(f"  {js.name:<24} FAILED")
    return problems, ran


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

    problems = audit_the_mongosh_scripts() + check_the_sample_data()
    shell_problems, ran = run_the_mongosh_scripts()
    problems += shell_problems

    expected = 20 - len(NO_PYTHON_HALF)
    print(f"\n{'=' * 62}")
    print(f"{passed} of the {expected} runnable experiments executed and "
          f"asserted, {failed} failed")
    if len(scripts) != expected:
        print(f"*** expected {expected} runnable experiments, found {len(scripts)}")
    if problems:
        print(f"*** {len(problems)} problem(s) with the mongosh scripts")
    print(f"{ran} of the 20 mongosh scripts run on a real server")
    if not failed and not problems and len(scripts) == expected:
        print("Every query in the notes was executed through mongomock"
              + (", and every mongosh script on MongoDB itself." if ran == 20 else "."))
    print(f"{'=' * 62}")
    return 1 if (failed or problems or len(scripts) != expected) else 0


if __name__ == "__main__":
    sys.exit(main())
