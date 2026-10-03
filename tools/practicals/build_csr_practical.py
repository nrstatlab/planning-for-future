#!/usr/bin/env python3
"""Write the practical course of Computational Statistics and R Programming (the earlier syllabus).

The seven experiments are in csr_data.py. Like build_csr2023_practical.py, whose R driver
and renderer this uses, it runs every step's R code (one R session per experiment) and puts
R's own output and plots on the page, in the programming structure: 1. Question, 2. Aim,
3. Steps, 4. Programme, 5. Execution and Results.

    statistics/computational-statistics-and-r-programming/practical.html
    statistics/computational-statistics-and-r-programming/img/e*.png

It needs R, so it is not part of tools/build_all.sh; its output is committed.

    python3 tools/practicals/build_csr_practical.py           # rewrite the page and images
    python3 tools/practicals/build_csr_practical.py --check   # rerun R; fail if the page differs
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_csr2023_practical as B  # noqa: E402
import csr_data as D  # noqa: E402

COURSE = B.ROOT / "statistics" / "computational-statistics-and-r-programming"
PAGE = COURSE / "practical.html"
IMG = COURSE / "img"
TITLE = "R Programming — Practical Course — 7 Experiments"
DESC = ("Seven R experiments, each set out as Question, Aim, Steps, Programme, and Execution and Results, "
        "with R's own output and plots.")


def render(outputs, version):
    toc, sections = [], []
    for e in D.E:
        hid, body = B.render_practical(e, outputs[e["n"]])
        toc.append((hid, f"Experiment {e['n']}: {e['title']}"))
        sections.append(body)
        if e["n"] == 4:
            sections.append(D.DECISION)
            toc.append(("choosing-the-right-test-experiments-3-5-6-7", "Choosing the Right Test (Experiments 3, 5, 6, 7)"))
    toc = [("list-of-practical-experiments-official-syllabus", "List of Practical Experiments (Official Syllabus)")] + toc
    toc.append(("lab-record-format-to-be-followed-for-every-experiment", "Lab Record Format (to be followed for every experiment)"))
    toc_html = "\n".join(f'    <li><a href="#{h}">{t}</a></li>' for h, t in toc)
    syl = "\n".join(f"    <li>{s}</li>" for s in D.SYLLABUS)
    return f"""<div class="wrapper">

  <div class="banner">
    <div class="crumbs"><a href="index.html">Home</a> &raquo; Practical</div>
<details class="toc">
  <summary>On this page</summary>
  <ol>
{toc_html}
  </ol>
</details>
    <h1>Practical Course — 7 Experiments</h1>
    <p>Each experiment is set out as it is written in the record: <strong>1. Question, 2. Aim, 3. Steps,
    4. Programme, 5. Execution and Results.</strong> Labs are done in the Computer Lab (≥ 4 hrs/month) using R.</p>
  </div>

  <div class="tip"><strong>How to use this manual:</strong> in the lab, copy the programme into an R script and run it
  line by line; the output you should see is under Execution and Results, step by step, with the result at the end.
  Every output and plot on this page was produced by running the programme shown, in R {version}. Use the built-in
  datasets (<code>iris</code>, <code>mtcars</code>, <code>airquality</code>, <code>sleep</code>) or a CSV from the UCI ML
  Repository.</div>

  <h2 id="list-of-practical-experiments-official-syllabus">List of Practical Experiments (Official Syllabus)</h2>
  <ol>
{syl}
  </ol>

{chr(10).join(sections)}
  <h2 id="lab-record-format-to-be-followed-for-every-experiment">Lab Record Format (to be followed for every experiment)</h2>
  <ol>
    <li><strong>1. Question</strong> &mdash; the dataset and the task.</li>
    <li><strong>2. Aim</strong> &mdash; the statistic, test or model the experiment produces.</li>
    <li><strong>3. Steps</strong> &mdash; the numbered steps, with the R commands and formulas they use.</li>
    <li><strong>4. Programme</strong> &mdash; the complete R script.</li>
    <li><strong>5. Execution and Results</strong> &mdash; the console output and plots, step by step, then the decision
    (from the p-value or \\(R^2\\)) and its plain-language interpretation.</li>
  </ol>

  <div class="tip">
    <strong>Note from syllabus:</strong> Practical problems must be done in the Computer Lab at least
    4 hours per month using R. Use real datasets (UCI ML Repository) or built-in datasets
    (<code>mtcars</code>, <code>airquality</code>, <code>iris</code>, etc.) for variety.
  </div>

  <div class="page-nav">
    <a href="unit5.html">← Previous: Unit 5</a>
    <a href="syllabus.html">Next: Syllabus →</a>
  </div>

  <footer>Practical Course — 7 Experiments • Computational Statistics &amp; R Programming</footer>
</div>
"""


def build(img_dir):
    if not shutil.which("Rscript"):
        sys.exit("Rscript was not found: this script needs R")
    version = subprocess.run(["Rscript", "-e", "cat(paste(R.version$major, R.version$minor, sep='.'))"],
                             capture_output=True, text=True, check=True).stdout.strip()
    img_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        outputs = {e["n"]: B.run_practical(e, img_dir, pathlib.Path(tmp)) for e in D.E}
    return render(outputs, version), version


def main():
    page = PAGE.read_text()
    if "--check" in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmp:
            body, version = build(pathlib.Path(tmp))
        bad = [] if B.BODY.search(page).group(0) == body else ["practical.html: the content differs from a fresh R run"]
        bad += [f"img/{n} is missing" for n in B.images(body) if not (IMG / n).exists()]
        if bad:
            print("FAIL\n  " + "\n  ".join(bad))
            return 1
        print(f"practical.html matches a fresh run in R {version}; {len(B.images(body))} images present")
        return 0
    body, version = build(IMG)
    B.TITLE, B.DESC = TITLE, DESC
    PAGE.write_text(B.splice(page, body))
    print(f"wrote {PAGE.relative_to(B.ROOT)} and {len(B.images(body))} images (R {version})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
