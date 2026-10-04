#!/usr/bin/env python3
"""Run every lab program whose output a lab page shows, and keep what it printed.

    python3 tools/data-science/capture_lab_outputs.py                 # all courses
    python3 tools/data-science/capture_lab_outputs.py course-3-python # one course folder
    python3 tools/data-science/capture_lab_outputs.py --check [...]   # rerun; fail on any difference

The files run are the ones named by {{output: ...}} in the lab.md pages (lab_includes.py).
Each runs as a student would run it, in a fresh copy of its course folder (so a program that
writes files changes nothing here), with the input its header gives after "Sample input:":

  .py  Python, with input() echoing what was typed after its prompt, as a terminal shows it;
       stdin is the sample input's words, one per line. Run with the Python running this script.
  .c   gcc -Wall -Wextra, a warning counting as a failure; run on a pseudo-terminal, each line of
       the sample input typed only when the program is waiting to read, so the terminal echoes it
       where a student would see it (the kernel's /proc/<pid>/syscall says when it is waiting).
  .R   Rscript --vanilla.
  GUI  a program with a driver beside it (_drive_<file>.py) is run through the driver instead,
       under a virtual display (xvfb-run) with a Python that has tkinter: the driver fills in
       the window, presses its buttons, asserts what it shows, prints what it did, and saves
       screenshots as screens/N.png, which are kept as output/<file>.N.png.

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

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lab_includes as L  # noqa: E402

REPO = HERE.parent.parent
LABS = REPO / "data-science" / "labs"
NOTES = REPO / "data-science" / "notes"
TIMEOUT = 1800
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


def run_one(rel, work):
    f = work / rel
    text = f.read_text()
    driver = f.with_name("_drive_" + f.name)
    stdin = sample_input(f, text)
    env = dict(os.environ, PYTHONHASHSEED="0", MPLBACKEND="Agg", TZ="UTC", LC_ALL="C.UTF-8",
               KERAS_BACKEND="torch", PYTHONDONTWRITEBYTECODE="1")
    if driver.exists():
        if not shutil.which("xvfb-run"):
            sys.exit(f"{rel}: has a GUI driver, and xvfb-run is not installed")
        (f.parent / "screens").mkdir(exist_ok=True)
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
        cmd = ["Rscript", "--vanilla", f.name]
    else:
        sys.exit(f"{rel}: no runner for {f.suffix} files")
    if f.suffix == ".c":
        code, printed = run_on_tty(cmd, f.parent, env, stdin, TIMEOUT)
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
    shots = sorted((f.parent / "screens").glob("*.png"), key=lambda p: int(p.stem)) if driver.exists() else []
    return out + "\n", shots


IMPORT_NAME = {"scikit-learn": "sklearn"}


def versions(rels):
    """Python, the compilers, and the version of each package these files import."""
    texts = "\n".join((LABS / r).read_text() for r in rels)
    lines = [f"Python {platform.python_version()}"]
    for name in PACKAGES:
        mod = IMPORT_NAME.get(name, name)
        if not re.search(rf"^\s*(?:import|from)\s+{re.escape(mod)}\b", texts, re.M):
            continue
        try:
            lines.append(f"{name} {importlib.metadata.version(name)}")
        except importlib.metadata.PackageNotFoundError:
            pass
    for tool, flag, ext in (("gcc", "--version", ".c"), ("Rscript", "--version", ".R")):
        if shutil.which(tool) and any(r.endswith(ext) for r in rels):
            r = subprocess.run([tool, flag], capture_output=True, text=True)
            lines.append((r.stdout or r.stderr).strip().split("\n")[0])
    return "\n".join(lines) + "\n"


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
                shutil.copytree(LABS / course, work / course, ignore=shutil.ignore_patterns("output"))
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
