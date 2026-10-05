"""The includes a lab.md may use, so that a lab page's code and output are never retyped.

    {{programme: course-3-python/02b_prime_check.py}}   the file, exactly, as a code block
    {{output: course-3-python/02b_prime_check.py}}      what it printed when run, from
                                                        labs/<course>/output/<file>.txt, and
                                                        any screenshots, <file>.N.png
    {{not-run: course-15a-nlp/12_bert_mlm.py}}          a box saying why it was not run: the
                                                        sentence after NOT EXECUTED in the file,
    {{not-run: course-5-dbms/04_plsql_oracle.sql | it needs Oracle}}   or the reason given

The outputs are written by tools/data-science/capture_lab_outputs.py, which runs every file a
lab page shows the output of; they are committed, so a build never runs a lab.

expand() also checks two things, and refuses the page if either fails:
  - in every section with a 3. Steps heading, the steps' bold headings ("1. **Read n.**")
    are, in order, the "Step i:" comments of the section's programme files;
  - an output is shown only for a file that was run: a file whose text carries
    "NOT EXECUTED" has no output file and is included with not-run.
"""
import html
import os
import pathlib
import re

INCLUDE = re.compile(r"^\{\{(programme|output|not-run): *([^}]+?) *\}\}[ \t]*$", re.M)
# "# Step 1: ...", "// Step 1: ...", "-- Step 1: ...", "% Step 1: ...", "<!-- Step 1: ... -->", "/* Step 1: ... */"
STEP = re.compile(r"^[ \t]*(?:#|//|--|%|<!--|/\*)[ \t]*Step (\d+): (.+?)[ \t]*(?:-->|\*/)?[ \t]*$", re.M)
STEP_ITEM = re.compile(r"^\d+\.\s+\*\*(.+?)\.\*\*", re.M)
LANG = {".py": "python", ".R": "r", ".c": "c", ".sql": "sql", ".js": "javascript", ".html": "html",
        ".css": "css", ".pl": "prolog", ".java": "java", ".sh": "bash", ".md": "markdown", ".json": "json",
        ".pig": "pig", ".hql": "sql", ".scala": "scala", ".rb": "ruby", ".conf": "properties"}
NOT_RUN = "NOT EXECUTED"


def output_path(labs, rel):
    f = labs / rel
    return f.parent / "output" / (f.name + ".txt")


def steps_of(text):
    """The Step i: comments of one file, checked to run 1, 2, 3, ..."""
    found = STEP.findall(text)
    return [int(i) for i, _ in found], [h for _, h in found]


def fence(text, lang=""):
    """A fenced block that cannot be closed early by the text it holds."""
    ticks = max([3] + [len(m) + 1 for m in re.findall(r"`{3,}", text)])
    return f"{'`' * ticks}{lang}\n{text.rstrip(chr(10))}\n{'`' * ticks}"


def not_run_reason(text):
    """The sentence after NOT EXECUTED in the file's header, for the not-run box."""
    i = text.find(NOT_RUN)
    line = text[i:].split("\n", 1)[0]
    rest = re.sub(r"^NOT EXECUTED\W*", "", line).strip(" -—#*/")
    return rest or "it needs a service these pages are not built against"


def expand(md, labs, where, page_dir=None):
    """Expand the includes in one lab.md; return (markdown, problems)."""
    problems = []

    def one(m):
        kind, (rel, _, reason) = m.group(1), m.group(2).partition("|")
        rel, reason = rel.strip(), reason.strip()
        if reason and kind != "not-run":
            problems.append(f"{where}: {kind} {rel}: only not-run takes a reason")
        f = labs / rel
        if not f.is_file():
            problems.append(f"{where}: {kind} {rel}: no such file under labs/")
            return m.group(0)
        text = f.read_text()
        if kind == "programme":
            return fence(text, LANG.get(f.suffix, ""))
        if kind == "not-run":
            if NOT_RUN not in text:
                problems.append(f"{where}: not-run {rel}, but the file does not say NOT EXECUTED")
            if output_path(labs, rel).exists():
                problems.append(f"{where}: not-run {rel} has an output file; a file not run has none")
            return ('<div class="warn" markdown="1">\n<span class="label">NOT RUN HERE</span>\n\n'
                    f"`{f.name}` was not run: {html.escape(reason or not_run_reason(text))}. "
                    "Nothing on this page claims an output it did not produce.\n</div>")
        # output
        if NOT_RUN in text:
            problems.append(f"{where}: output {rel}, but the file says NOT EXECUTED; use not-run")
            return m.group(0)
        out = output_path(labs, rel)
        if not out.exists():
            problems.append(f"{where}: output {rel}: not captured; run capture_lab_outputs.py")
            return m.group(0)
        # the input typed at a prompt is in the output, where the terminal echoed it
        parts = ['<span class="label">OUTPUT</span>', "", fence(out.read_text() or "(nothing printed)"), ""]
        shots = sorted(out.parent.glob(out.name.replace(".txt", ".*.png")), key=lambda p: int(p.name.split(".")[-2]))
        # A driver or a browser takes screenshots; an R script or a Python one without a
        # driver draws charts and saves them itself.
        drawn = f.suffix in (".R", ".py") and not (f.parent / f"_drive_{f.stem}.py").exists()
        what = "chart {i} of {n}, drawn by the program" if drawn else "screenshot {i} of {n}, taken while the program ran"
        for i, png in enumerate(shots, 1):
            src = os.path.relpath(png, page_dir) if page_dir else png.name
            parts += [f'<p><img src="{src}" alt="{html.escape(f.name)}: {what.format(i=i, n=len(shots))}" '
                      'style="max-width:100%;height:auto"></p>', ""]
        return '<div class="example" markdown="1">\n' + "\n".join(parts) + "</div>"

    # the steps check works on the source, before the includes are replaced
    for sec in re.split(r"^(?=## )", md, flags=re.M):
        if not re.search(r"^### 3\. Steps\s*$", sec, re.M):
            continue
        title = sec.split("\n", 1)[0].strip("# ").strip()
        want = []
        for kind, rel in INCLUDE.findall(sec):
            if kind != "programme" or not (labs / rel).is_file():
                continue
            nums, heads = steps_of((labs / rel).read_text())
            if nums != list(range(1, len(nums) + 1)):
                problems.append(f"{where}: {rel}: its Step comments are not numbered 1, 2, 3, ...")
            want += heads
        steps = re.search(r"^### 3\. Steps\s*$(.*?)^### 4\. Programme\s*$", sec, re.M | re.S)
        have = STEP_ITEM.findall(steps.group(1)) if steps else []
        if want and have != want:
            problems.append(f"{where}: \"{title}\": the Steps {have} are not the programme's Step "
                            f"comments {want}")
    return INCLUDE.sub(one, md), problems
