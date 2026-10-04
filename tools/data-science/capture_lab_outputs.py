#!/usr/bin/env python3
"""Run every lab program whose output a lab page shows, and keep what it printed.

    python3 tools/data-science/capture_lab_outputs.py                 # all courses
    python3 tools/data-science/capture_lab_outputs.py course-3-python # one course folder
    python3 tools/data-science/capture_lab_outputs.py --check [...]   # rerun; fail on any difference

The files run are the ones named by {{output: ...}} in the lab.md pages (lab_includes.py).
Each runs as a student would run it, in a fresh copy of its course folder (so a program that
writes files changes nothing here; the other courses are linked beside it, for the few that import from one), with the input its header gives after "Sample input:":

  .py  Python, with input() echoing what was typed after its prompt, as a terminal shows it;
       stdin is the sample input's words, one per line. Run with the Python running this script.
  .c   gcc -Wall -Wextra, a warning counting as a failure; run on a pseudo-terminal, each line of
       the sample input typed only when the program is waiting to read, so the terminal echoes it
       where a student would see it (the kernel's /proc/<pid>/syscall says when it is waiting).
  .R   Rscript --vanilla, with the clock fixed at CLOCK by faketime (Sys.Date() and Sys.time()
       would otherwise print something new every run), and R_DEFAULT_DEVICE=png, so each plot
       a script draws is a file, Rplot001.png, Rplot002.png, ..., kept as output/<file>.N.png.
  .html opened in Chromium by web_lab.py, served over http with the clock fixed: it lists the
       page's headings and elements, and screenshots the whole page.
  .sql the sqlite3 shell (-bail, box mode) on a fresh database, the script piped in with a
       .print of each question ("-- Q7. ...") before it, so the output says which question each
       result answers. The clock is fixed at CLOCK by faketime, as queries on 'now' would
       otherwise print something different every day. Then each statement run_sql_labs.py
       expects a constraint to reject is run against the database the script left, and must fail;
       the statement and the shell's error are printed.
  GUI  a program with a driver beside it (_drive_<name>.py, for <name>.py or <name>.R) is run through the driver instead:
       for tkinter, under a virtual display (xvfb-run) with a Python that has tkinter; for a page
       in a browser (a Shiny app, a plotly chart, a web page), with this Python and Playwright's
       Chromium. The driver uses the program as a student would, asserts what it shows, prints
       what it did, and saves screenshots as screens/N.png, kept as output/<file>.N.png.

stdout and stderr are kept together, in order. What was printed goes to
labs/<course>/output/<file>.txt, and the versions used to output/VERSIONS.txt beside it. Where a file's header also gives "Sample output:", every
line of it must appear in what the program printed (spacing apart).

Not part of tools/build_all.sh: it needs the lab packages. Its outputs are committed.
"""
import argparse
import difflib
import importlib.metadata
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lab_includes as L  # noqa: E402
import run_sql_labs  # noqa: E402

REPO = HERE.parent.parent
LABS = REPO / "data-science" / "labs"
NOTES = REPO / "data-science" / "notes"
TIMEOUT = 1800
CLOCK = "2026-10-04 12:00:00"
PACKAGES = ["numpy", "pandas", "scipy", "scikit-learn", "mlxtend", "matplotlib", "seaborn", "plotly",
            "openpyxl", "mongomock", "pyarrow", "fastavro", "duckdb", "pytholog", "torch", "keras",
            "statsmodels", "nltk", "spacy", "mlflow", "dvc", "flask"]

KEY = re.compile(r"[ \t]*(?:Sample (?:input|output)|Expected output|Syllabus|Note)\b[^:]*:")

ECHO = r'''
import builtins, runpy, sys
def _input(prompt=""):
    sys.stdout.write(str(prompt)); sys.stdout.flush()
    line = sys.stdin.readline()
    if not line:
        raise EOFError("no more sample input")
    sys.stdout.write(line if line.endswith("\n") else line + "\n"); sys.stdout.flush()
    return line.rstrip("\n")
builtins.input = _input
path = sys.argv[1]
sys.argv = [path]
sys.path.insert(0, ".")
runpy.run_path(path, run_name="__main__")
'''


def header_block(text, key):
    """The lines after "<key>:" in a file's opening comment or docstring, until the next key."""
    m = re.search(rf"^[ \t*#/]*{key}(?: \([^)]*\))?:[ \t]*(.*)$", text, re.M)
    if not m:
        return None
    lines = [m.group(1).rstrip()]
    for ln in text[m.end():].split("\n")[1:]:
        body = re.sub(r"^[ \t]*(?:\*|#|//)?", "", ln)
        if not body.strip() or KEY.match(body) or ln.strip().startswith(('"""', "*/")):
            break
        if not body.startswith((" ", "\t")):          # a continuation is indented under the value
            break
        lines.append(body.strip())
    return [x for x in lines if x]


def sample_input(f, text):
    block = header_block(text, "Sample input")
    if block is None:
        return ""
    if f.suffix == ".py":                              # input() reads one line per call
        return "".join(w + "\n" for ln in block for w in ln.split())
    return "".join(ln + "\n" for ln in block)


def shown_outputs():
    """Every file a lab page shows the output of: (course folder, path under it)."""
    found = []
    for md in sorted(NOTES.glob("sem-*/course-*/lab.md")):
        for kind, rel in L.INCLUDE.findall(md.read_text()):
            if kind == "output":
                found.append(rel)
    return found


def waiting_to_read(pid):
    """True if the process is blocked in read() on its standard input."""
    try:
        call = pathlib.Path(f"/proc/{pid}/syscall").read_text().split()
    except OSError:
        return False
    return len(call) > 1 and call[0] == "0" and int(call[1], 16) == 0


def run_on_tty(cmd, cwd, env, typed, timeout):
    """Run cmd on a pseudo-terminal, typing each line of `typed` when it waits to read."""
    import pty
    import select
    import time
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(cwd)
        os.execvpe(cmd[0], cmd, env)
    out, lines, end = b"", typed.splitlines(), time.time() + timeout
    while True:
        ready, _, _ = select.select([fd], [], [], 0.05)
        if ready:
            try:
                data = os.read(fd, 65536)
            except OSError:
                data = b""
            if not data:
                break
            out += data
            continue
        if lines and waiting_to_read(pid):
            os.write(fd, lines.pop(0).encode() + b"\n")
        if time.time() > end:
            os.kill(pid, 9)
            sys.exit(f"{cmd[0]}: still running after {timeout} s")
    _, status = os.waitpid(pid, 0)
    os.close(fd)
    if lines:
        sys.exit(f"{cmd[0]}: finished with sample input left unread: {lines}")
    return os.waitstatus_to_exitcode(status), out.decode(errors="replace").replace("\r\n", "\n")


def tk_python():
    """A Python that can import tkinter: this one if it can, else a system one."""
    for py in [sys.executable] + [shutil.which(n) for n in ("python3.13", "python3.12", "python3")]:
        if py and subprocess.run([py, "-c", "import tkinter"], capture_output=True).returncode == 0:
            return py
    sys.exit("no Python with tkinter here: install python3-tk")


SQL_QUESTION = re.compile(r"^-- ((?:Q\d+\.|BONUS:).*)$")
SQL_MORE = re.compile(r"^--\s{2,}(\S.*)$")


def sql_script(text):
    """The script with a .print of each question, its continuation lines included, before it."""
    lines, out = text.split("\n"), [".mode box"]
    for i, ln in enumerate(lines):
        m = SQL_QUESTION.match(ln)
        if m:
            q = m.group(1).rstrip()
            for more in lines[i + 1:i + 5]:
                if q.endswith((".", "?", ":")) or not SQL_MORE.match(more):
                    break
                q += " " + SQL_MORE.match(more).group(1).rstrip()
            out.append('.print ""')
            out += ['.print "' + part.replace('"', '\\"') + '"'
                    for part in textwrap.wrap(q, 92, subsequent_indent="    ")]
        out.append(ln)
    return "\n".join(out) + "\n"


def run_sql(f, env):
    """Run the script on a new database, then the constraint tests against what it left."""
    for tool in ("sqlite3", "faketime", "stdbuf"):
        if not shutil.which(tool):
            sys.exit(f"{f.name}: needs {tool}, which is not installed")
    db = f.with_suffix(".db")
    res = subprocess.run(["faketime", CLOCK, "stdbuf", "-o0", "sqlite3", "-bail", str(db)],
                         cwd=f.parent, input=sql_script(f.read_text()), stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, env=env, timeout=TIMEOUT)
    printed, tests = res.stdout, run_sql_labs.CONSTRAINT_TESTS.get(f.name, [])
    if res.returncode or not tests:
        return res.returncode, printed
    printed += ("\nConstraint tests: each statement below must be rejected "
                "(tools/data-science/run_sql_labs.py runs the same ones).\n")
    for label, stmt in tests:
        t = subprocess.run(["sqlite3", "-cmd", "PRAGMA foreign_keys = ON", str(db), stmt], cwd=f.parent,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
        if t.returncode == 0:
            sys.exit(f"{f.name}: constraint not enforced: {label}")
        printed += f"\n-- {label}\n{stmt};\n{t.stdout}"
    return 0, printed


def run_one(rel, work):
    f = work / rel
    text = f.read_text()
    driver = f.with_name("_drive_" + f.stem + ".py")
    stdin = sample_input(f, text)
    env = dict(os.environ, PYTHONHASHSEED="0", MPLBACKEND="Agg", TZ="UTC", LC_ALL="C.UTF-8",
               KERAS_BACKEND="torch", PYTHONDONTWRITEBYTECODE="1")
    if driver.exists():
        (f.parent / "screens").mkdir(exist_ok=True)
        if "playwright" in driver.read_text() or "web_lab" in driver.read_text():   # a browser
            cmd = [sys.executable, driver.name]
            env["PYTHONPATH"] = str(HERE)                 # for web_lab
        else:
            if not shutil.which("xvfb-run"):
                sys.exit(f"{rel}: has a GUI driver, and xvfb-run is not installed")
            cmd = ["xvfb-run", "-a", "-s", "-screen 0 480x400x24", tk_python(), driver.name]
    elif f.suffix == ".py":
        cmd = [sys.executable, "-c", ECHO, f.name]
    elif f.suffix == ".c":
        exe = f.with_suffix("")
        cc = subprocess.run(["gcc", "-Wall", "-Wextra", "-o", str(exe), f.name, "-lm"], cwd=f.parent,
                            capture_output=True, text=True)
        if cc.returncode or cc.stderr:
            sys.exit(f"{rel}: gcc\n{cc.stderr}")
        cmd = [str(exe)]
    elif f.suffix == ".R":
        for tool in ("Rscript", "faketime"):
            if not shutil.which(tool):
                sys.exit(f"{rel}: needs {tool}, which is not installed")
        cmd = ["faketime", CLOCK, "Rscript", "--vanilla", f.name]
        env["R_DEFAULT_DEVICE"] = "png"
    elif f.suffix == ".sql":
        cmd = None
    elif f.suffix == ".html":
        cmd = [sys.executable, str(HERE / "web_lab.py"), f.name]
    else:
        sys.exit(f"{rel}: no runner for {f.suffix} files")
    if f.suffix == ".c":
        code, printed = run_on_tty(cmd, f.parent, env, stdin, TIMEOUT)
    elif f.suffix == ".sql":
        code, printed = run_sql(f, env)
    else:
        res = subprocess.run(cmd, cwd=f.parent, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, env=env, timeout=TIMEOUT)
        code, printed = res.returncode, res.stdout
    out = "\n".join(ln.rstrip() for ln in printed.rstrip("\n").split("\n"))
    if code != 0:
        sys.exit(f"{rel}: exit status {code}\n{out[-3000:]}")
    if str(work) in out:
        sys.exit(f"{rel}: its output names the temporary folder it ran in, so it would differ on every run")
    stated = header_block(text, "Sample output")
    flat = "\n".join(" ".join(ln.split()) for ln in out.split("\n"))     # the header's spacing is loose
    missing = [ln for ln in (stated or []) if " ".join(ln.split()) not in flat]
    if missing:
        sys.exit(f"{rel}: the header's Sample output is not what it printed; missing {missing}")
    if driver.exists() or f.suffix == ".html":
        shots = sorted((f.parent / "screens").glob("*.png"), key=lambda p: int(p.stem))
    elif f.suffix == ".R":
        shots = sorted(f.parent.glob("Rplot*.png"))
    else:
        shots = []
    return out + "\n", shots


IMPORT_NAME = {"scikit-learn": "sklearn"}


def versions(rels):
    """The languages and compilers used, and the version of each package these files load."""
    texts = "\n".join((LABS / r).read_text() for r in rels)
    drivers = [LABS / r for r in rels
               if (LABS / r).with_name("_drive_" + pathlib.Path(r).stem + ".py").exists()]
    drivers = [d.with_name("_drive_" + d.stem + ".py").read_text() for d in drivers]
    lines = []
    if any(r.endswith(".py") for r in rels) or drivers or any(r.endswith(".html") for r in rels):
        lines.append(f"Python {platform.python_version()}")
    for name in PACKAGES:
        mod = IMPORT_NAME.get(name, name)
        if not re.search(rf"^\s*(?:import|from)\s+{re.escape(mod)}\b", texts, re.M):
            continue
        try:
            lines.append(f"{name} {importlib.metadata.version(name)}")
        except importlib.metadata.PackageNotFoundError:
            pass
    for tool, flag, ext in (("gcc", "--version", ".c"), ("Rscript", "--version", ".R"),
                            ("sqlite3", "--version", ".sql")):
        if shutil.which(tool) and any(r.endswith(ext) for r in rels):
            r = subprocess.run([tool, flag], capture_output=True, text=True)
            line = (r.stdout or r.stderr).strip().split("\n")[0]
            lines.append("SQLite " + " ".join(line.split()[:2]) if tool == "sqlite3" else line)
    r_code = "\n".join(ln.split("#")[0] for r in rels if r.endswith(".R")
                       for ln in (LABS / r).read_text().split("\n"))      # comments dropped
    r_pkgs = sorted({a or b for a, b in re.findall(r"\blibrary\((\w+)\)|\b(\w+)::", r_code)})
    if r_pkgs and shutil.which("Rscript"):
        r = subprocess.run(["Rscript", "-e", "for (p in commandArgs(TRUE)) cat(p, format(packageVersion(p)), '\\n')",
                            *r_pkgs], capture_output=True, text=True)
        lines += ["R package " + ln.strip() for ln in r.stdout.strip().split("\n") if ln.strip()]
    if any("playwright" in d or "web_lab" in d for d in drivers) or any(r.endswith(".html") for r in rels):
        lines.append(f"playwright {importlib.metadata.version('playwright')} (its Chromium opens the pages)")
    if any(r.endswith(".html") and "code.jquery.com" in (LABS / r).read_text() for r in rels):
        lines.append("jQuery 3.7.1, from npm, in place of code.jquery.com")
    if any("tkinter" in d for d in drivers):
        lines.append("tkinter, under Xvfb (for the drivers)")
    return "\n".join(lines) + "\n"


def stage(course, work):
    """A fresh copy of the course folder, with the other courses beside it, linked, for the few
    programs that import from a sibling course (course 6's Python uses course 4's statlib)."""
    shutil.copytree(LABS / course, work / course, ignore=shutil.ignore_patterns("output"))
    for other in LABS.iterdir():
        if other.is_dir() and other.name != course:
            (work / other.name).symlink_to(other)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("courses", nargs="*", help="course folders under data-science/labs (default: all)")
    ap.add_argument("--check", action="store_true", help="rerun and compare; write nothing")
    a = ap.parse_args()
    todo = [r for r in shown_outputs() if not a.courses or r.split("/")[0] in a.courses]
    bad, done = [], {}
    by_course = {}
    for rel in todo:
        by_course.setdefault(rel.split("/")[0], []).append(rel)
    for course, rels in sorted(by_course.items()):
        with tempfile.TemporaryDirectory() as tmp:
            for rel in rels:
                work = pathlib.Path(tmp) / rel.replace("/", "_")
                stage(course, work)
                out, screens = run_one(rel, work)
                target = L.output_path(LABS, rel)
                if a.check:
                    old = target.read_text() if target.exists() else ""
                    if old != out:
                        bad.append(rel + "\n" + "".join(difflib.unified_diff(
                            old.splitlines(True), out.splitlines(True), "committed", "now")))
                else:
                    target.parent.mkdir(exist_ok=True)
                    target.write_text(out)
                    for old in target.parent.glob(target.name.replace(".txt", ".*.png")):
                        old.unlink()
                    for i, png in enumerate(screens, 1):
                        shutil.copy(png, target.parent / target.name.replace(".txt", f".{i}.png"))
                done[rel] = len(out.splitlines())
        if not a.check:
            for d in {L.output_path(LABS, r).parent for r in rels}:
                (d / "VERSIONS.txt").write_text(versions([r for r in rels if L.output_path(LABS, r).parent == d]))
    if bad:
        print("FAIL: the output differs from the committed one\n" + "\n".join(bad))
        return 1
    print(f"{'checked' if a.check else 'captured'} {len(done)} program(s) in {len(by_course)} course(s)"
          + ("; every output is as committed" if a.check else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
