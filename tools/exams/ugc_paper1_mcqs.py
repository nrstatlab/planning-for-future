#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write exams/ugc-net/paper-1/mcqs.html from ugc_paper1_mcq_data.py.

    python3 ugc_paper1_mcqs.py            # dry run: counts and the spread of keys
    python3 ugc_paper1_mcqs.py --apply    # writes the page

The markup is the Statistics MCQ page's (exams/ugc-net/mcqs.html), which the web
application reads: a unit heading "Unit N — Title (k MCQs)", then div.mcq with
div.q "1. ...", ol.options and details p "B. explanation". Two additions: a
passage is a div.comp whose data-questions says how many questions follow it,
and an approved unit's heading carries data-approved with the owner's date.

recheck_ugc_paper1.py checks the finished page independently of this file.
"""
import collections
import os
import sys

from ugc_paper1_mcq_data import APPROVED, UNITS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "exams", "ugc-net", "paper-1", "mcqs.html")
units = UNITS
L = "ABCD"
n_total = sum(sum(1 for q in u[3] if q[0] != "PASSAGE") for u in units)
head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Model MCQs — UGC NET Paper I (General Paper)</title>
<meta name="description" content="Model MCQs for UGC NET Paper I, the General Paper on Teaching and Research Aptitude: twenty on each unit, every answer explained.">
<meta property="og:title" content="Model MCQs — UGC NET Paper I (General Paper)">
<meta property="og:description" content="Model MCQs for UGC NET Paper I, the General Paper on Teaching and Research Aptitude: twenty on each unit, every answer explained.">
<meta property="og:type" content="article">
<meta property="og:site_name" content="StatsTricks360">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:url" content="https://nrstatlab.github.io/planning-for-future/exams/ugc-net/paper-1/mcqs.html">
<link rel="stylesheet" href="../styles.css">
<style>
.mcq {{ background:#fff; border:1px solid var(--border); border-radius:8px; padding:0.9rem 1.1rem; margin:0.7rem 0; box-shadow:0 1px 2px rgba(0,0,0,0.04); }}
.mcq .q {{ font-weight:600; margin-bottom:0.4rem; color:var(--text); }}
.mcq ol.options {{ list-style:upper-alpha; margin-left:1.5rem; margin-bottom:0.5rem; }}
.mcq ol.options li {{ margin-bottom:0.15rem; }}
.mcq details {{ background:#ecfdf5; border-left:3px solid var(--success); padding:0.4rem 0.7rem; border-radius:0 6px 6px 0; margin-top:0.3rem; }}
.mcq details summary {{ cursor:pointer; font-weight:600; color:#065f46; }}
.mcq details p {{ margin-top:0.3rem; }}
.mcq-unit-head {{ background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%); color:#fff; padding:1rem 1.5rem; border-radius:8px; margin: 2.5rem 0 1rem; }}
.mcq-unit-head h2 {{ color:#fff; border:none; margin:0; padding:0; }}
.mcq-unit-head p {{ margin:0; opacity:0.92; font-size:0.95rem; }}
.comp {{ background:#fffbe6; border:1px solid var(--border); border-left:5px solid var(--accent); border-radius:0 8px 8px 0; padding:0.8rem 1.1rem; margin:1.4rem 0 0.4rem; }}
.comp .clabel {{ font-weight:700; color:#92400e; display:block; margin-bottom:0.3rem; }}
</style>
</head>
<body>

<header class="site-header">
  <h1>Model MCQs — UGC NET Paper I</h1>
  <p>{n_total} questions &middot; 20 per unit &middot; Click "Show Answer" to reveal</p>
</header>

<main class="container">

<section class="unit-content">
  <h2>Topics Covered</h2>
  <div class="chips">
""" + "".join(f'    <span class="chip">{t}</span>\n' for _, t, _, _ in units) + """  </div>

<h2>About these MCQs</h2>
<p>Model questions written for the official Paper I syllabus, twenty on each unit, at the level of the paper. Each has four options and one right answer; <em>Show Answer</em> gives the answer and why, and often why the tempting wrong option is wrong. Units are added as their notes are written. For the real thing, work through <a href="../solved-2026.html#paper1">Paper I of June 2026</a>.</p>
<div class="toc">
<h4>Jump to Unit:</h4>
<ul style="columns:2;">
""" + "".join(f'<li><a href="#unit{n}">Unit {n} — {t}</a></li>\n' for n, t, _, _ in units) + """</ul>
</div>
</section>
"""
body, keys = [], collections.Counter()
for n, title, blurb, qs in units:
    nq = sum(1 for q in qs if q[0] != "PASSAGE")
    attr = f' data-approved="{APPROVED[n]}"' if n in APPROVED else ""
    body.append(f'\n<!-- ============================ UNIT {n} ============================ -->\n'
                f'<div class="mcq-unit-head" id="unit{n}">\n<h2{attr}>Unit {n} — {title} ({nq} MCQs)</h2>\n<p>{blurb}</p>\n</div>\n')
    k = 0
    for q in qs:
        if q[0] == "PASSAGE":
            body.append(f'\n<div class="comp" data-questions="5"><span class="clabel">{q[1]}</span>\n{q[2]}\n</div>\n')
            continue
        stem, opts, key, expl = q
        assert len(opts) == 4 and key in L, stem
        k += 1
        keys[key] += 1
        lis = "".join(f"<li>{o}</li>" for o in opts)
        body.append(f'\n<div class="mcq"><div class="q">{k}. {stem}</div>\n<ol class="options">{lis}</ol>\n'
                    f'<details><summary>Show Answer</summary><p>{key}. {expl}</p></details></div>\n')
    assert k == nq
last = units[-1][0]
tail = f"""
<div class="pagination">
  <a href="unit{last}.html">&larr; Unit {last}</a>
  <a class="next" href="../solved-2026.html#paper1">Solved June 2026 Paper I &rarr;</a>
</div>
</main>

<footer class="site-footer">
  <p>UGC NET Paper I Model MCQs &middot; <a href="index.html">Back to Paper I</a></p>
</footer>

</body>
</html>
"""
print("%d questions in %d units; keys %s; approved units %s"
      % (n_total, len(units), dict(sorted(keys.items())), sorted(APPROVED) or "none"))
if "--apply" in sys.argv:
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(head + "".join(body) + tail)
    print("wrote %s" % os.path.relpath(OUT, ROOT))
else:
    print("dry run -- pass --apply to write")
