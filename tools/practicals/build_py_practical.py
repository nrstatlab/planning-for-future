#!/usr/bin/env python3
"""Write a practical page in the programming structure from a data module, running its Python.

    python3 tools/practicals/build_py_practical.py smp_data           # rewrite the page
    python3 tools/practicals/build_py_practical.py smp_data --check   # rerun; fail if the page differs

The data module gives PAGE (path from the repository root), TITLE, DESC, HEAD (the HTML from
<div class="wrapper"> up to the first practical; "{toc}" is replaced by the contents list and
"{version}" by the Python version), SRC (the folder of programme files, relative to this
script), PRACTICALS and TAIL (the HTML after the last practical, up to and including the
wrapper's closing </div>).

Each practical is a dict: n, title, file (a programme in SRC), question, aim, steps (one
explanation for each "# Step i: heading" comment in the file, in order), optional method (HTML
for a box under the steps: the formulae and tables), commands ([(function, what it does)]),
optional reading (HTML after the output), notes and conclusion. Optional too: hid and heading
(the h2's id and text, where the page keeps its own), and extra, a list of further listings
({file, label, intro, run}): each is shown under 4. Programme after the main one, and those with
run=True are run and their output shown under 5. Execution and Results. A module may also give
LIBS, the packages whose versions replace "{libs}" in HEAD.

Every programme is run, in a copy of SRC so that one may import another (tails.py), by the
Python that runs this script. What it prints is the output shown: 1. Question, 2. Aim,
3. Steps, 4. Programme, 5. Execution and Results.
"""
import html
import importlib
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_csr2023_practical as B  # noqa: E402
from build_r_practical import toc_of  # noqa: E402

STEP = re.compile(r"^# Step (\d+): (.+)$", re.M)


def run(D, p, work):
    res = subprocess.run([sys.executable, p["file"]], capture_output=True, text=True, cwd=work)
    if res.returncode != 0 or res.stderr:
        sys.exit(f"Practical {p['n']}: {p['file']} stopped or warned\n{res.stderr[-2000:]}")
    return res.stdout.rstrip("\n")


def render(p, code, output, k, extras):
    n = p["n"]
    hid = p.get("hid", f"practical-{n}-{B.slug(p['title'])}")
    heading = p.get("heading") or f"Practical {n}: {p['title']}"
    heads = STEP.findall(code)
    if [int(i) for i, _ in heads] != list(range(1, len(heads) + 1)):
        sys.exit(f"Practical {n}: the # Step comments in {p['file']} are not numbered 1, 2, 3, ...")
    if len(heads) != len(p["steps"]):
        sys.exit(f"Practical {n}: {len(heads)} # Step comments in {p['file']}, {len(p['steps'])} explanations")
    o = [f"  <!-- {n} -->",
         f'  <h2 id="{hid}">{heading}</h2>',
         f'  <h3 id="{B.sid("1-question", k)}">1. Question</h3>', p["question"].strip(),
         f'  <h3 id="{B.sid("2-aim", k)}">2. Aim</h3>', f"  <p>{p['aim']}</p>",
         f'  <h3 id="{B.sid("3-steps", k)}">3. Steps</h3>', "  <ol>"]
    for (_, head), expl in zip(heads, p["steps"]):
        o.append(f"    <li><strong>{html.escape(head, quote=False)}.</strong>\n    {expl.strip()}</li>")
    o.append("  </ol>")
    if p.get("method"):
        o += ['  <div class="formula">', '    <span class="label">THE METHOD</span>', p["method"].strip(), "  </div>"]
    o += ['  <div class="formula">', '    <span class="label">PYTHON USED</span>',
          '    <table class="left">', "      <tr><th>Function or statement</th><th>What it does</th></tr>"]
    o += [f"      <tr><td>{t}</td><td>{m}</td></tr>" for t, m in p["commands"]]
    o += ["    </table>", "  </div>",
          f'  <h3 id="{B.sid("4-programme", k)}">4. Programme</h3>',
          '  <div class="example">',
          f'    <span class="label">PRACTICAL {n} &mdash; {p["file"]}</span>',
          "    " + B.pre(code.rstrip("\n")), "  </div>"]
    for x, xcode, _ in extras:
        if x.get("intro"):
            o.append(f"  <p>{x['intro']}</p>")
        o += ['  <div class="example">', f'    <span class="label">{x["label"]} &mdash; {x["file"]}</span>',
              "    " + B.pre(xcode.rstrip("\n")), "  </div>"]
    o += [f'  <h3 id="{B.sid("5-execution-and-results", k)}">5. Execution and Results</h3>',
          f"  <p>Saved as <code>{p['file']}</code> and run with <code>python3 {p['file']}</code>, it printed:</p>",
          '  <div class="example">', '    <span class="label">OUTPUT</span>', "    " + B.pre(output), "  </div>"]
    for x, _, xout in extras:
        if x.get("run"):
            o += [f"  <p>And <code>{x['file']}</code> printed:</p>",
                  '  <div class="example">', '    <span class="label">OUTPUT</span>', "    " + B.pre(xout), "  </div>"]
    if p.get("reading"):
        o.append(p["reading"].strip())
    for note in p.get("notes", []):
        o += ['  <div class="tip">', f"    {note}", "  </div>"]
    o += ['  <div class="concept">', '    <span class="label">RESULT</span>', p["conclusion"].strip(), "  </div>", ""]
    return "\n".join(o)


def build(D):
    src = HERE / D.SRC
    parts = []
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp)
        for f in src.glob("*.py"):
            shutil.copy(f, work / f.name)
        for k, p in enumerate(D.PRACTICALS, 1):
            code = (src / p["file"]).read_text()
            extras = [(x, (src / x["file"]).read_text(), run(D, x | {"n": p["n"]}, work) if x.get("run") else "")
                      for x in p.get("extra", [])]
            parts.append(render(p, code, run(D, p, work), k, extras))
    rest = "\n".join(parts) + "\n" + D.TAIL
    head = D.HEAD.replace("{version}", platform.python_version())
    if getattr(D, "LIBS", None):
        vs = [f"{name} {importlib.import_module(mod).__version__}" for mod, name in D.LIBS]
        head = head.replace("{libs}", ", ".join(vs[:-1]) + " and " + vs[-1] if len(vs) > 1 else vs[0])
    return head.replace("{toc}", toc_of(head + rest)) + rest


def main():
    D = importlib.import_module(sys.argv[1])
    page_path = B.ROOT / D.PAGE
    page = page_path.read_text()
    body = build(D)
    if "--check" in sys.argv[2:]:
        if B.BODY.search(page).group(0) != body:
            print(f"FAIL\n  {D.PAGE}: the content differs from a fresh run")
            return 1
        print(f"{D.PAGE} matches a fresh run in Python {platform.python_version()}")
        return 0
    B.TITLE, B.DESC = D.TITLE, html.unescape(D.DESC)
    page_path.write_text(B.splice(page, body))
    print(f"wrote {D.PAGE} (Python {platform.python_version()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
