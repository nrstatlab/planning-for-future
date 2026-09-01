#!/usr/bin/env python3
"""Verify the Course 6 lab material.

R cannot be installed in this environment (the Debian package repositories are
blocked by the network policy), so the R scripts are desk-checked only. What
this runner does:

  1. Executes every Python equivalent in labs/course-6-r/python/. Those carry
     the assertions, so a wrong number fails the build.
  2. Structurally checks each .R file -- balanced braces, brackets and quotes,
     and the presence of the "NOT EXECUTED" header, so no R file can silently
     start claiming to have been tested.

Usage: python3 tools/run_r_equivalents.py
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
R_DIR = ROOT / "labs" / "course-6-r"
PY_DIR = R_DIR / "python"


def check_r_syntax(path):
    """Balanced delimiters outside strings and comments, plus the header."""
    text = path.read_text()
    problems = []

    if "NOT EXECUTED IN VERIFICATION" not in text:
        problems.append("missing the 'NOT EXECUTED' header")

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

    print(f"\nR scripts (desk-checked -- structure only, R is not installable)")
    r_files = sorted(R_DIR.glob("*.R"))
    for path in r_files:
        problems = check_r_syntax(path)
        print(f"  {path.name:<36} ", end="")
        if problems:
            print("PROBLEMS")
            for p in problems:
                print(f"      {p}")
            failures += 1
        else:
            print("structure ok, header present")

    print()
    print(f"{len(scripts)} Python equivalents executed, "
          f"{len(r_files)} R scripts structurally checked")
    if failures:
        print(f"FAILURES: {failures}")
        return 1
    print("Course 6 labs verified "
          "(R syntax itself is unverified -- run it in RStudio)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
