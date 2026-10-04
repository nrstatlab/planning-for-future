#!/usr/bin/env python3
"""Verify the Course 6 lab material.

  1. Executes every Python equivalent in labs/course-6-r/python/. Those carry
     the assertions, so a wrong number fails the build.
  2. Runs every R script with Rscript, in a temporary copy of the folder (they
     write files), and fails if one stops with an error. 18_shiny_app.R is a
     web server, so it is not run here: capture_lab_outputs.py runs it, through
     _drive_18_shiny_app.py, in a browser. Where Rscript is not installed, the
     R scripts are only checked for structure, and the runner says so.
  3. Structurally checks each .R file -- balanced braces, brackets and quotes.

Until October 2026 R could not be installed where these labs are checked, and
this runner could do no more than step 3.

Usage: python3 tools/data-science/run_r_equivalents.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

# tools/data-science/ -> the SECTION root, which is where everything this
# script reads and writes lives. Three levels up is the repository.
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent / "data-science"
R_DIR = ROOT / "labs" / "course-6-r"
PY_DIR = R_DIR / "python"


def check_r_syntax(path):
    """Balanced delimiters outside strings and comments, plus the header."""
    text = path.read_text()
    problems = []

    if "NOT EXECUTED" in text:
        problems.append("says NOT EXECUTED, but R scripts are run")

    depth = {"(": 0, "[": 0, "{": 0}
    closer = {")": "(", "]": "[", "}": "{"}
    for raw in text.splitlines():
        line, in_str, quote = [], False, ""
        for ch in raw:
            if in_str:
                if ch == quote:
                    in_str = False
                continue
            if ch in "\"'":
                in_str, quote = True, ch
                continue
            if ch == "#":
                break
            line.append(ch)
        for ch in line:
            if ch in depth:
                depth[ch] += 1
            elif ch in closer:
                depth[closer[ch]] -= 1
        if in_str:
            problems.append("unterminated string")

    for sym, n in depth.items():
        if n != 0:
            problems.append(f"unbalanced '{sym}' (net {n:+d})")
    return problems


def main():
    failures = 0

    print("Python equivalents (executed -- these carry the assertions)")
    scripts = sorted(p for p in PY_DIR.glob("*.py") if not p.name.startswith("_"))
    for script in scripts:
        print(f"  {script.name:<36} ", end="")
        result = subprocess.run([sys.executable, script.name],
                                cwd=PY_DIR, capture_output=True, text=True)
        if result.returncode == 0:
            print("ok")
        else:
            print("FAILED")
            tail = (result.stderr or result.stdout).strip().splitlines()[-4:]
            for line in tail:
                print(f"      {line}")
            failures += 1

    r_files = sorted(R_DIR.glob("*.R"))
    rscript = shutil.which("Rscript")
    print("\nR scripts" + ("" if rscript else " (Rscript is not installed: structure only)"))
    ran = 0
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp) / "course-6-r"
        shutil.copytree(R_DIR, work, ignore=shutil.ignore_patterns("output"))
        for path in r_files:
            problems = check_r_syntax(path)
            print(f"  {path.name:<36} ", end="")
            verdict = "structure ok"
            if rscript and not problems and path.name != "18_shiny_app.R":
                result = subprocess.run([rscript, "--vanilla", path.name], cwd=work,
                                        capture_output=True, text=True, timeout=600)
                if result.returncode == 0:
                    verdict, ran = "ran, structure ok", ran + 1
                else:
                    problems.append("Rscript failed: "
                                    + " / ".join(result.stderr.strip().splitlines()[-3:]))
            elif path.name == "18_shiny_app.R":
                verdict = "structure ok (a server: capture_lab_outputs.py runs it in a browser)"
            if problems:
                print("PROBLEMS")
                for p in problems:
                    print(f"      {p}")
                failures += 1
            else:
                print(verdict)

    print()
    print(f"{len(scripts)} Python equivalents executed, {ran} of {len(r_files)} R scripts run, "
          f"all {len(r_files)} structurally checked")
    if failures:
        print(f"FAILURES: {failures}")
        return 1
    print("Course 6 labs verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
