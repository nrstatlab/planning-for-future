# -*- coding: utf-8 -*-
import os, pathlib, posixpath, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csirmap import UNIT1, UNIT4, check

bad = check()
assert not bad, bad

BADGE = {"deep":  '<span class="g deep">deep</span>',
         "brief": '<span class="g brief">brief</span>',
         "missing": '<span class="g missing">not here</span>'}

PAGE_DIR = "exams/csir-net"


def rel(path):
    """csirmap holds destinations from the repository root; the page needs them
    relative to itself. Written this way round so csirmap can keep checking
    that every destination exists, which it can only do from the root."""
    return posixpath.relpath(path, PAGE_DIR)


def rows(data):
    out = []
    for text, dests, grade in data:
        if dests:
            links = "<br>".join(f'<a href="{rel(p)}">{lab}</a>' for p, lab in dests)
        else:
            links = '<span class="none">nothing on this site teaches it</span>'
        out.append(f"      <tr><td>{text}</td><td>{links}</td><td>{BADGE[grade]}</td></tr>")
    return "\n".join(out)

def count(data, g): return sum(1 for _, _, x in data if x == g)

missing = [t for t, d, g in UNIT4 if g == "missing"] + [t for t, d, g in UNIT1 if g == "missing"]
missing_li = "\n".join(f"      <li>{m}</li>" for m in missing)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CSIR NET Mathematical Sciences &mdash; Syllabus Map for Statistics Candidates</title>
<meta name="description" content="Every line of CSIR NET Units 1 and 4 mapped onto the notes on this site, graded deep, brief or missing. Units 2 and 3 are for mathematics candidates.">
<meta property="og:title" content="CSIR NET Mathematical Sciences &mdash; Syllabus Map for Statistics Candidates">
<meta property="og:description" content="Every line of CSIR NET Units 1 and 4 mapped onto the notes on this site, graded deep, brief or missing. Units 2 and 3 are for mathematics candidates.">
<meta property="og:type" content="article">
<meta property="og:site_name" content="NRSTATLAB">
<meta name="twitter:card" content="summary">
<meta property="og:url" content="https://nrstatlab.github.io/planning-for-future/exams/csir-net/index.html">
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif; margin:0;
         background:#f5f7fb; color:#1f2937; line-height:1.6; }}
  .wrapper {{ max-width:1100px; margin:0 auto; padding:28px 22px 80px; }}
  .banner {{ background:linear-gradient(135deg,#0f4c81 0%,#1e7fbf 100%); color:#fff;
            padding:34px 24px; border-radius:14px;
            box-shadow:0 6px 20px rgba(15,76,129,.18); margin-bottom:30px; }}
  .banner h1 {{ margin:0 0 6px; font-size:1.85rem; }}
  .banner p {{ margin:0; opacity:.95; }}
  h2 {{ color:#0f4c81; border-bottom:3px solid #1e7fbf; padding-bottom:6px; margin-top:42px; }}
  h3 {{ color:#0f4c81; margin-top:28px; }}
  .lede {{ font-size:1.02rem; }}
  .quote {{ background:#fff; border-left:5px solid #0f4c81; border-radius:10px;
           padding:16px 22px; margin:18px 0; box-shadow:0 2px 10px rgba(0,0,0,.06); }}
  .quote p {{ margin:0 0 8px; }}
  .quote p:last-child {{ margin:0; }}
  .quote cite {{ font-size:.85rem; color:#6b7280; font-style:normal; }}
  .note {{ background:#fffbeb; border:1px solid #fde68a; border-left:5px solid #f59e0b;
          border-radius:10px; padding:16px 20px; margin:20px 0; }}
  .note strong {{ color:#92400e; }}
  .gaps {{ background:#fef2f2; border:1px solid #fecaca; border-left:5px solid #dc2626;
          border-radius:10px; padding:4px 22px 16px; margin:20px 0; }}
  .gaps strong {{ color:#991b1b; }}
  .scroll {{ overflow-x:auto; border-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,.06);
            margin:16px 0; background:#fff; }}
  table {{ border-collapse:collapse; width:100%; min-width:620px; }}
  th, td {{ text-align:left; padding:10px 14px; border-bottom:1px solid #e2e8f0;
           font-size:.92rem; vertical-align:top; }}
  th {{ background:#eef4fa; color:#0f4c81; position:sticky; top:0; }}
  tr:last-child td {{ border-bottom:none; }}
  td:first-child {{ width:46%; }}
  .g {{ display:inline-block; font-size:.72rem; font-weight:700; letter-spacing:.04em;
       padding:2px 9px; border-radius:10px; white-space:nowrap; }}
  .g.deep {{ background:#d1fae5; color:#065f46; }}
  .g.brief {{ background:#fef3c7; color:#92400e; }}
  .g.missing {{ background:#fee2e2; color:#991b1b; }}
  .none {{ color:#991b1b; font-size:.88rem; }}
  .tally {{ display:flex; gap:10px; flex-wrap:wrap; margin:14px 0 0; padding:0; list-style:none; }}
  .tally li {{ background:#fff; border:1px solid #e2e8f0; border-radius:10px;
              padding:10px 16px; font-size:.9rem; }}
  .tally b {{ display:block; font-size:1.3rem; color:#0f4c81; }}
  a {{ color:#0f4c81; }}
  footer {{ text-align:center; margin-top:46px; font-size:.85rem; color:#6b7280; }}
  @media (max-width:760px) {{ .banner h1 {{ font-size:1.4rem; }} td:first-child {{ width:auto; }} }}
</style>
<link rel="canonical" href="https://nrstatlab.github.io/planning-for-future/exams/csir-net/index.html">
</head>
<body>
<div class="wrapper">

  <div class="banner">
    <h1>CSIR NET Mathematical Sciences</h1>
    <p>The syllabus, line by line, against what this site actually teaches</p>
  </div>

  <p class="lede">This is a map, not a set of notes. Every line of the official syllabus is
  listed below and pointed at the page here that teaches it &mdash; or marked as not here, where
  nothing does. The statistics itself lives in the study sections and is linked to rather than
  copied, so correcting a proof once corrects it for every exam that points at it.</p>

  <h2 id="which-units-you-sit">Which units you sit</h2>

  <p>The syllabus answers this itself, in its closing paragraph:</p>

  <div class="quote">
    <p>&ldquo;All students are expected to answer questions from Unit I. Students in mathematics
    are expected to answer additional question from Unit II and III. Students with in statistics
    are expected to answer additional question from Unit IV.&rdquo;</p>
    <cite>&mdash; CSIR-UGC NET common syllabus for Part B and C, Mathematical Sciences
    (quoted verbatim, including its own grammar)</cite>
  </div>

  <p>So a <strong>statistics</strong> candidate reads <strong>Unit 1 and Unit 4</strong>. Units 2
  and 3 are for mathematics candidates; they are listed at the foot of this page so you can see
  what is being left out, and why.</p>

  <ul class="tally">
    <li><b>{len(UNIT1) + len(UNIT4)}</b>syllabus lines mapped</li>
    <li><b>{count(UNIT1,'deep') + count(UNIT4,'deep')}</b>taught in depth here</li>
    <li><b>{count(UNIT1,'brief') + count(UNIT4,'brief')}</b>covered briefly</li>
    <li><b>{count(UNIT1,'missing') + count(UNIT4,'missing')}</b>not here at all</li>
  </ul>

  <div class="note">
    <p><strong>No exam pattern appears on this page.</strong> Marks, duration, negative marking,
    the number of papers and eligibility are not in the syllabus document this page was built
    from, and they change between notifications. Read the current official notification for those.
    Use this page for the statistics, not for the rules.</p>
  </div>

  <h2 id="how-to-read-the-grades">How to read the grades</h2>
  <p><span class="g deep">deep</span> a full unit page here, with derivations and worked problems
  &mdash; usually more than the exam needs.
  &nbsp;<span class="g brief">brief</span> covered, at exam level, on one page.
  &nbsp;<span class="g missing">not here</span> nothing on this site teaches it; you will need
  another source.</p>

  <h2 id="unit-1-analysis-and-linear-algebra">Unit 1 &mdash; Analysis and Linear Algebra</h2>
  <p>Every candidate answers this unit. Most of it is covered by the existing
  <a href="../ugc-net/unit2.html">Real Analysis &amp; Matrix Algebra</a> page
  written for UGC NET, which is why so many rows point at one destination. The measure-theoretic
  and abstract-algebraic parts are the real holes.</p>

  <div class="scroll">
    <table>
      <tr><th>Syllabus line</th><th>Where it is taught here</th><th>Depth</th></tr>
{rows(UNIT1)}
    </table>
  </div>

  <h2 id="unit-4-statistics">Unit 4 &mdash; Statistics</h2>
  <p>This is the statistics candidate's second unit, and where this site is strongest. Several
  of these rows point at pages rewritten from textbook sources, with every step shown and every
  worked answer recomputed &mdash; more than a question paper will ask for.</p>

  <div class="scroll">
    <table>
      <tr><th>Syllabus line</th><th>Where it is taught here</th><th>Depth</th></tr>
{rows(UNIT4)}
    </table>
  </div>

  <div class="gaps">
    <h3 id="what-is-not-here">What is not here</h3>
    <p>Naming these is the point of the map. Across both units, <strong>{len(missing)} lines</strong>
    have nothing on this site behind them:</p>
    <ul>
{missing_li}
    </ul>
    <p>The Unit 1 gaps are pure mathematics &mdash; measure theory, metric-space topology and
    abstract linear algebra &mdash; which is a long way from the rest of this site. The three
    Unit 4 gaps are closer to home and are the more likely additions.</p>
  </div>

  <h2 id="units-2-and-3-not-covered">Units 2 and 3 &mdash; not covered, and not planned</h2>

  <p>These are the mathematics candidate's units. This site does not teach them and is not
  planning to. They are listed so that a candidate can tell in one glance whether this is the
  wrong place to be.</p>

  <div class="scroll">
    <table>
      <tr><th>Unit</th><th>Topics, as the syllabus lists them</th></tr>
      <tr><td><strong>Unit 2</strong></td><td>Complex analysis &mdash; algebra of complex numbers,
      analytic functions, Cauchy&rsquo;s theorem and integral formula, Liouville, maximum modulus,
      Taylor and Laurent series, residues, conformal and M&ouml;bius mappings. Algebra &mdash;
      permutations and combinations, congruences, Chinese remainder theorem, groups, Sylow
      theorems, rings and ideals, unique factorization and Euclidean domains, polynomial rings,
      fields and Galois theory. Topology &mdash; basis, dense sets, product topology, separation
      axioms, connectedness and compactness.</td></tr>
      <tr><td><strong>Unit 3</strong></td><td>Ordinary differential equations, partial
      differential equations, numerical analysis, calculus of variations, linear integral
      equations and classical mechanics.</td></tr>
    </table>
  </div>

  <h2 id="source">Source</h2>
  <p>Built from the official CSIR-UGC NET common syllabus for Part B and C, Mathematical
  Sciences, as supplied. Syllabus lines are quoted from that document; the wording is the
  syllabus&rsquo;s own, not a paraphrase. Nothing on this page comes from any other source, and
  nothing that was not in the document &mdash; marks, dates, eligibility &mdash; appears at all.</p>

  <p><a href="../">&larr; Back to Statistics for Examinations</a></p>

  <footer>
    <p>CSIR NET Mathematical Sciences &middot; syllabus map &middot;
    <a href="../../">NRSTATLAB</a></p>
  </footer>
</div>
</body>
</html>
"""

# tools/exams/ -> repository root is two levels up; the page lives in exams/.
out = (pathlib.Path(__file__).resolve().parent.parent.parent
       / "exams" / "csir-net" / "index.html")
out.write_text(HTML)
print("wrote", out, len(HTML), "bytes")
print("Unit 1:", len(UNIT1), "rows   Unit 4:", len(UNIT4), "rows   missing:", len(missing))
