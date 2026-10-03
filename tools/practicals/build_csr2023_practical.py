#!/usr/bin/env python3
"""Write the practical course of Computational Statistics and R Programming (2023 syllabus).

The ten practicals are in csr2023_data.py. This script runs every step's R code, one R
session per practical, and puts R's own output (and its plots, as PNG images) on the page:

    statistics/computational-statistics-and-r-programming-2023/practical.html
    statistics/computational-statistics-and-r-programming-2023/img/p*.png

It replaces only the page's content (from <div class="wrapper"> to the site footer) and its
title and description; the site chrome around it belongs to tools/add_site_nav.py.

It needs R with ggplot2 and caTools (rpart comes with R), so it is not part of
tools/build_all.sh: its output is committed. Run it again after editing the data:

    python3 tools/practicals/build_csr2023_practical.py           # rewrite the page and images
    python3 tools/practicals/build_csr2023_practical.py --check   # rerun R; fail if the page differs
"""
import html
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import csr2023_data as D  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
COURSE = ROOT / "statistics" / "computational-statistics-and-r-programming-2023"
PAGE = COURSE / "practical.html"
IMG = COURSE / "img"

TITLE = "Computational Statistics &amp; R Programming (2023 syllabus) — Practical Course"
DESC = ("Ten R practicals, each set out as Question, Aim, Steps, Programme, and Execution and "
        "Results, with R's own output and plots.")

# Each chunk is evaluated as the Console would: visible values are printed, and a
# command's warnings are printed after its result. A chunk that stops with an error
# stops the build.
DRIVER = r'''
options(width = 70)
IMG <- commandArgs(trailingOnly = TRUE)[1]
.run <- function(id, file, plot = "", w = 770, h = 460) {
  cat("\n@@BEGIN ", id, "\n", sep = "")
  if (nzchar(plot)) png(file.path(IMG, plot), width = w, height = h, res = 110, type = "cairo")
  exprs <- parse(file = file, keep.source = FALSE)
  for (e in exprs) {
    ws <- character(0)
    withCallingHandlers({
        r <- withVisible(eval(e, envir = globalenv()))
        if (r$visible) print(r$value)
      },
      warning = function(w) {
        call <- conditionCall(w)
        ws <<- c(ws, paste0(if (!is.null(call)) paste0("In ", deparse(call)[1], " :\n  "), conditionMessage(w)))
        invokeRestart("muffleWarning")
      },
      message = function(m) { cat(conditionMessage(m)); invokeRestart("muffleMessage") })
    # As at the Console: the warnings of a command come after its result.
    if (length(ws) == 1) cat("Warning message:\n", ws, "\n", sep = "")
    if (length(ws) > 1) cat("Warning messages:\n", paste0(seq_along(ws), ": ", ws, collapse = "\n"), "\n", sep = "")
  }
  if (nzchar(plot)) invisible(dev.off())
  cat("@@END ", id, "\n", sep = "")
}
'''

MARK = re.compile(r"\n@@BEGIN (\S+)\n(.*?)@@END \1\n", re.S)


def slug(text):
    s = re.sub(r"<[^>]+>", "", html.unescape(text)).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def run_practical(p, img_dir, work):
    """Run one practical's steps in a single R session; return {step index: output}."""
    calls = []
    if p.get("prelude"):                       # shared set-up, run first and not shown as a step
        f = work / f"p{p['n']}_s0.R"
        f.write_text(p["prelude"] + "\n")
        calls.append(f'.run("s0", "{f.as_posix()}", "")')
    for i, (_, _, code, opt) in enumerate(p["steps"], 1):
        if code is None or opt.get("run", True) is False:
            continue
        f = work / f"p{p['n']}_s{i}.R"
        f.write_text(code + "\n")
        w, h = opt.get("size", (770, 460))
        calls.append(f'.run("s{i}", "{f.as_posix()}", "{opt.get("plot", "")}", {w}, {h})')
    if not calls:
        return {}
    script = work / f"p{p['n']}.R"
    script.write_text(DRIVER + "\n".join(calls) + "\n")
    res = subprocess.run(["Rscript", "--vanilla", str(script), str(pathlib.Path(img_dir).resolve())],
                         capture_output=True, text=True, cwd=work)   # files a programme writes stay out of the tree
    if res.returncode != 0:
        sys.exit(f"Practical {p['n']}: R stopped\n{res.stdout[-2000:]}\n{res.stderr[-2000:]}")
    out = {int(m.group(1)[1:]): m.group(2).rstrip("\n") for m in MARK.finditer(res.stdout)}
    if len(out) != len(calls):
        sys.exit(f"Practical {p['n']}: {len(calls)} chunks run, {len(out)} outputs read")
    if out.pop(0, ""):
        sys.exit(f"Practical {p['n']}: the prelude printed something; it must only set up")
    return out


def pre(text):
    return f"<pre><code>{html.escape(text, quote=False)}</code></pre>"


def alt_for(p, heading):
    word = p.get("word", "Practical")
    return html.escape(f"{word} {p['n']}: {re.sub(r'<[^>]+>', '', heading)}, as drawn by the R code above")


def sid(name, n):
    """The h3 ids of the site's practical pages: 1-question, 1-question-2, ..."""
    return name if n == 1 else f"{name}-{n}"


def img(p, heading, name, size=(770, 460)):
    return (f'<p><img src="img/{name}" width="{size[0]}" height="{size[1]}" alt="{alt_for(p, heading)}" '
            f'style="max-width:100%;height:auto;border-radius:4px"></p>')


def render_practical(p, outputs):
    """One practical in the programming structure: Question, Aim, Steps, Programme,
    Execution and Results."""
    n = p["n"]
    word = p.get("word", "Practical")          # the course's own name for one: Practical, Experiment
    hid = f"{word.lower()}-{n}-{slug(p['title'])}"
    o = [f"  <!-- {n} -->",
         f'  <h2 id="{hid}">{word} {n}: {p["title"]}</h2>',
         f'  <h3 id="{sid("1-question", n)}">1. Question</h3>', p["question"].strip(),
         f'  <h3 id="{sid("2-aim", n)}">2. Aim</h3>', f"  <p>{p['aim']}</p>",
         f'  <h3 id="{sid("3-steps", n)}">3. Steps</h3>', "  <ol>"]
    for heading, expl, _, _ in p["steps"]:
        o.append(f"    <li><strong>{heading}.</strong>" + (f"\n    {expl.strip()}" if expl else "") + "</li>")
    o += ["  </ol>",
          '  <div class="formula">', '    <span class="label">R COMMANDS AND FORMULAS USED</span>',
          '    <table class="left">', "      <tr><th>Command or formula</th><th>What it does</th></tr>"]
    o += [f"      <tr><td>{t}</td><td>{m}</td></tr>" for t, m in p["commands"]]
    o += ["    </table>", "  </div>"]

    # The programme: every step's code, in order, as one script.
    lines = [f"# {word} {n}: {html.unescape(re.sub(r'<[^>]+>', '', p['title']))}"]
    if p.get("prelude"):
        lines += ["", "# " + p.get("prelude_title", "The data set"), p["prelude"]]
    for i, (heading, _, code, opt) in enumerate(p["steps"], 1):
        if code is None:
            continue
        head = f"# Step {i}: {html.unescape(re.sub(r'<[^>]+>', '', heading))}"
        if opt.get("run", True) is False:
            head += "  (run on your own computer)"
        lines += ["", head, code]
    o += [f'  <h3 id="{sid("4-programme", n)}">4. Programme</h3>',
          '  <div class="example">', f'    <span class="label">{word.upper()} {n} &mdash; THE R PROGRAMME</span>',
          "    " + pre("\n".join(lines)), "  </div>"]

    o.append(f'  <h3 id="{sid("5-execution-and-results", n)}">5. Execution and Results</h3>')
    for i, (heading, _, code, opt) in enumerate(p["steps"], 1):
        if code is None:
            continue
        ran = opt.get("run", True)
        shown = outputs.get(i, "") if ran else opt.get("shown", "")
        o += [f"  <h4>Step {i}: {heading}</h4>", '  <div class="example">']
        if shown:
            label = "OUTPUT" if ran else "OUTPUT (typical; not run here)"
            o += [f'    <span class="label">{label}</span>', "    " + pre(shown)]
        elif not opt.get("plot"):
            o.append("    <p>" + opt.get("quiet", "Nothing is printed: this step only creates objects or loads packages.") + "</p>")
        if opt.get("plot"):
            o += ['    <span class="label">PLOT</span>', "    " + img(p, heading, opt["plot"], opt.get("size", (770, 460)))]
        if opt.get("note"):
            o.append(f"    <p>{opt['note']}</p>")
        o.append("  </div>")
    for note in p["notes"]:
        o += ['  <div class="tip">', f"    <strong>Note.</strong> {note}", "  </div>"]
    o += ['  <div class="concept">', '    <span class="label">RESULT</span>', p["conclusion"].strip(), "  </div>", ""]
    return hid, "\n".join(o)


def render(outputs):
    sections, toc, ids = [], [], {}
    for p in D.P:
        hid, body = render_practical(p, outputs[p["n"]])
        sections.append(body)
        toc.append((hid, f"Practical {p['n']}: {p['title']}"))
        ids[p["n"]] = hid
    by_ex = {}
    for p in D.P:
        for ex in p["syllabus"]:
            by_ex.setdefault(ex, []).append(p)
    map_id = "the-syllabus-exercises-and-the-practicals"
    rows = []
    for ex, text in D.SYLLABUS:
        links = ", ".join(f'<a href="#{ids[q["n"]]}">Practical {q["n"]}</a>' for q in by_ex[ex])
        rows.append(f"      <tr><td>{ex}</td><td>{text}</td><td>{links}</td></tr>")
    toc_html = "\n".join(f'    <li><a href="#{h}">{t}</a></li>' for h, t in [(map_id, "The syllabus exercises and the practicals")] + toc)
    return f"""<div class="wrapper">

  <div class="banner">
    <div class="crumbs"><a href="index.html">Home</a> &raquo; Practical</div>
<details class="toc">
  <summary>On this page</summary>
  <ol>
{toc_html}
  </ol>
</details>
    <h1>Practical Course — 10 Practicals</h1>
    <p>{DESC}</p>
  </div>

  <div class="tip">
    <strong>How to use:</strong> each practical is set out as it is written in the record: 1. Question,
    2. Aim, 3. Steps, 4. Programme, 5. Execution and Results. Open RStudio, copy the programme into a new
    script, run it line by line with <em>Ctrl + Enter</em>, and check that you get the output shown under
    Execution and Results. Every output and plot on this page was produced by running the code
    shown, in R {R_VERSION}.
  </div>

  <h2 id="{map_id}">The syllabus exercises and the practicals</h2>
  <p>The syllabus lists eleven exercises; they are done here in ten practicals. Exercise 2, the working
  directory, is the last step of Practical 1, and the plots of Exercise 11 begin in Practical 9 and fill
  Practical 10.</p>
  <table class="left">
      <tr><th>Exercise</th><th>In the syllabus</th><th>Done in</th></tr>
{chr(10).join(rows)}
  </table>

{chr(10).join(sections)}
  <div class="page-nav">
    <a href="unit5.html">&#8592; Previous: Unit 5</a>
    <a href="syllabus.html">Next: Syllabus &#8594;</a>
  </div>

  <footer>Practical Course — Computational Statistics &amp; R Programming</footer>
</div>
"""


R_VERSION = ""
BODY = re.compile(r'<div class="wrapper">.*?</div>\n(?=\n<!-- site-foot|\n?</body>)', re.S)


def build(img_dir):
    global R_VERSION
    if not shutil.which("Rscript"):
        sys.exit("Rscript was not found: this script needs R, with ggplot2 and caTools")
    R_VERSION = subprocess.run(["Rscript", "-e", "cat(paste(R.version$major, R.version$minor, sep='.'))"],
                               capture_output=True, text=True, check=True).stdout.strip()
    img_dir.mkdir(parents=True, exist_ok=True)
    outputs = {}
    with tempfile.TemporaryDirectory() as tmp:
        for p in D.P:
            outputs[p["n"]] = run_practical(p, img_dir, pathlib.Path(tmp))
    return render(outputs)


def splice(page, body):
    if not BODY.search(page):
        sys.exit("practical.html: the content block <div class=\"wrapper\"> ... </div> was not found")
    page = BODY.sub(lambda m: body, page, count=1)
    page = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", page, count=1)
    for attr in ('name="description"', 'property="og:description"'):
        page = re.sub(rf'<meta {attr} content="[^"]*">', f'<meta {attr} content="{html.escape(DESC)}">', page, count=1)
    return page


def images(body):
    return sorted(set(re.findall(r'src="img/([^"]+)"', body)))


def main():
    check = "--check" in sys.argv[1:]
    page = PAGE.read_text()
    if check:
        with tempfile.TemporaryDirectory() as tmp:
            body = build(pathlib.Path(tmp))
            now = BODY.search(page).group(0)
            bad = [] if now == body else ["practical.html: the content differs from a fresh R run"]
            for name in images(body):
                if not (IMG / name).exists():
                    bad.append(f"img/{name} is missing")
            if bad:
                print("FAIL\n  " + "\n  ".join(bad))
                return 1
            print(f"practical.html matches a fresh run in R {R_VERSION}; {len(images(body))} images present")
            return 0
    body = build(IMG)
    PAGE.write_text(splice(page, body))
    stale = sorted(set(x.name for x in IMG.glob("*.png")) - set(images(body)))
    for name in stale:
        (IMG / name).unlink()
    print(f"wrote {PAGE.relative_to(ROOT)} and {len(images(body))} images (R {R_VERSION})"
          + (f"; removed {len(stale)} unused" if stale else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
