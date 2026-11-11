#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write the exam-standard model questions of UGC NET from ugc_model_data/.

    python3 ugc_model.py            # dry run: counts and the spread of keys
    python3 ugc_model.py --apply    # writes the pages

Statistics (Code 107): exams/ugc-net/model/index.html and unitN.html.
Paper I: exams/ugc-net/paper-1/model/index.html and unitN.html.
Fifty questions a unit (owner, 11 November 2026). A unit has a page once its
data module exists; the index lists only those units. The markup of a question
is the solved paper's: div.mcq, span.qn, ol.options, details with the answer.

recheck_ugc_model.py checks the finished pages independently of this file.
"""
import collections
import html
import importlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
L = "ABCD"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

PAPERS = {
    "p2": dict(dir=os.path.join("exams", "ugc-net", "model"), name="UGC NET Statistics",
               long="UGC NET Statistics (Code 107)", num=lambda n: ROMAN[n - 1],
               home="UGC NET Statistics", solved="../solved-2026.html#paper2",
               solved_label="Paper II of June 2026", mcqs_label="the 500 short model MCQs"),
    "p1": dict(dir=os.path.join("exams", "ugc-net", "paper-1", "model"), name="UGC NET Paper I",
               long="UGC NET Paper I (General Paper)", num=str,
               home="UGC NET Paper I", solved="../../solved-2026.html#paper1",
               solved_label="Paper I of June 2026", mcqs_label="the short model MCQs"),
}

MATHJAX = """<script>
window.MathJax = {
  tex: {
    inlineMath: [['$','$'], ['\\\\(','\\\\)']],
    displayMath: [['$$','$$'], ['\\\\[','\\\\]']],
    processEscapes: true,
    processEnvironments: true,
    packages: {'[+]': ['ams', 'noerrors', 'noundefined']}
  },
  loader: { load: ['[tex]/noerrors'] },
  options: {
    skipHtmlTags: ['script','noscript','style','textarea','pre','code','annotation','annotation-xml']
  },
  svg: { fontCache: 'global' }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
"""

STYLE = """<style>
.mcq { background:#fff; border:1px solid var(--border); border-radius:8px; padding:0.9rem 1.1rem; margin:0.7rem 0; box-shadow:0 1px 2px rgba(0,0,0,0.04); }
.mcq .q { font-weight:600; margin-bottom:0.4rem; color:var(--text); }
.mcq .q .qn { color:var(--primary); margin-right:0.25rem; }
.mcq .q .stmts { display:block; font-weight:400; margin:0.45rem 0 0.45rem 0.4rem; }
.mcq .q .stmts > span { display:block; margin:0.2rem 0; }
.mcq .q table.lists { font-weight:400; margin:0.6rem 0; border-collapse:collapse; width:100%; }
.mcq .q table.lists th, .mcq .q table.lists td { border:1px solid var(--border); padding:0.35rem 0.6rem; text-align:left; vertical-align:top; }
.mcq ol.options { list-style:upper-alpha; margin-left:1.5rem; margin-bottom:0.5rem; }
.mcq ol.options li { margin-bottom:0.3rem; }
.mcq details { background:#ecfdf5; border-left:3px solid var(--success); padding:0.4rem 0.7rem; border-radius:0 6px 6px 0; margin-top:0.3rem; }
.mcq details summary { cursor:pointer; font-weight:600; color:#065f46; }
.mcq details p { margin-top:0.3rem; }
.mcq details p.notes { font-size:0.92rem; }
.comp { background:#fffbe6; border:1px solid var(--border); border-left:5px solid var(--accent); border-radius:0 8px 8px 0; padding:0.8rem 1.1rem; margin:1.4rem 0 0.4rem; }
.comp .clabel { font-weight:700; color:#92400e; display:block; margin-bottom:0.3rem; }
.model-units { list-style:none; margin:1rem 0; padding:0; }
.model-units li { border:1px solid var(--border); border-radius:8px; padding:0.7rem 1rem; margin:0.5rem 0; background:#fff; }
.model-units li small { display:block; color:var(--muted, #555); }
</style>
"""


def load(paper):
    units = []
    for n in range(1, 11):
        try:
            m = importlib.import_module("ugc_model_data.%s_unit%02d" % (paper, n))
        except ModuleNotFoundError:
            continue
        units.append((n, m.TITLE, m.BLURB, m.QUESTIONS))
    return units


def anchors(path):
    """{id: heading text} of the h2 sections of a notes page."""
    with open(path, encoding="utf-8") as fh:
        t = fh.read()
    out = {}
    for i, h in re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', t, re.S):
        out[i] = re.sub(r"^\d+\.\s*", "", re.sub(r"<[^>]+>", "", h)).strip()
    return out


def head(title, desc, url, math):
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="StatsTricks360">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:url" content="https://statstricks360.com/{url}">
<link rel="stylesheet" href="{'../' * (url.count('/') - 2)}styles.css">
{MATHJAX if math else ''}{STYLE}</head>
<body>
"""


def unit_page(paper, P, units, i):
    n, title, blurb, qs = units[i]
    num = P["num"](n)
    notes = os.path.join(ROOT, os.path.dirname(P["dir"]), "unit%d.html" % n)
    anc = anchors(notes)
    nq = sum(1 for q in qs if not isinstance(q, tuple))
    url = P["dir"].replace(os.sep, "/") + "/unit%d.html" % n
    page_title = f"Model Questions, Unit {num}: {title} — {P['name']}"
    desc = (f"{nq} model questions of examination standard on Unit {num}, {title}, of {P['long']}: "
            "each with its answer and a full worked explanation.")
    out = [head(page_title, desc, url, True), f"""
<header class="site-header">
  <h1>Model Questions — Unit {num}: {title}</h1>
  <p>{P['long']} &middot; {nq} questions &middot; Click "Show Answer" for the worked solution</p>
</header>

<main class="container">

<section class="unit-content">
<h2 id="about">About this set</h2>
<p>{blurb}</p>
<p>These are model questions written for practice at the standard of the paper; they are not questions from a past paper. Try each one before opening the answer. Every answer gives the working and a link to the section of the <a href="../unit{n}.html">Unit {num} notes</a> that teaches it.</p>
</section>

<h2 id="questions">The questions</h2>
"""]
    keys, k = collections.Counter(), 0
    for q in qs:
        if isinstance(q, tuple):
            out.append(f'\n<div class="comp" data-questions="{q[3] if len(q) > 3 else 5}"><span class="clabel">{q[1]}</span>\n{q[2]}\n</div>\n')
            continue
        assert len(q["o"]) == 4 and q["k"] in L, q["q"][:60]
        assert q["a"] in anc, "%s unit %d: no section #%s in the notes" % (paper, n, q["a"])
        k += 1
        keys[q["k"]] += 1
        ans = q["o"][L.index(q["k"])]
        lis = "".join(f"<li>{o}</li>" for o in q["o"])
        out.append(f'\n<div class="mcq" id="q{k}"><div class="q"><span class="qn">Q{k}.</span> {q["q"]}</div>\n'
                   f'<ol class="options">{lis}</ol>\n'
                   f'<details><summary>Show Answer</summary><p><strong>Answer: ({q["k"]}) {ans}{"" if ans.rstrip().endswith((".", "$$")) else "."}</strong></p>\n'
                   f'<p>{q["e"]}</p>\n'
                   f'<p class="notes">Read this in the notes: <a href="../unit{n}.html#{q["a"]}">Unit {num}, {anc[q["a"]]}</a></p></details></div>\n')
    prev = (f'unit{units[i - 1][0]}.html', f'&larr; Unit {P["num"](units[i - 1][0])}') if i else ("index.html", "&larr; All units")
    nxt = (f'unit{units[i + 1][0]}.html', f'Unit {P["num"](units[i + 1][0])} &rarr;') if i + 1 < len(units) else ("index.html", "All units &rarr;")
    out.append(f"""
<div class="pagination">
  <a href="{prev[0]}">{prev[1]}</a>
  <a class="next" href="{nxt[0]}">{nxt[1]}</a>
</div>
</main>

<footer class="site-footer">
  <p>{P['name']} Model Questions &middot; <a href="index.html">All units</a> &middot; <a href="../index.html">Back to {P['home']}</a></p>
</footer>

</body>
</html>
""")
    return "unit%d.html" % n, "".join(out), nq, keys


def index_page(paper, P, units, counts):
    total = sum(counts.values())
    url = P["dir"].replace(os.sep, "/") + "/index.html"
    title = f"Model Questions — {P['long']}"
    desc = (f"Model questions of examination standard for {P['long']}, fifty on each unit, "
            "each with its answer and a full worked explanation.")
    items = "".join(
        f'<li><a href="unit{n}.html"><b>Unit {P["num"](n)} &mdash; {t}</b></a><small>{counts[n]} questions &middot; {b}</small></li>\n'
        for n, t, b, _ in units)
    more = "" if len(units) == 10 else "<p>The remaining units are added as they are written and checked.</p>\n"
    return "index.html", head(title, desc, url, False) + f"""
<header class="site-header">
  <h1>Model Questions — {P['name']}</h1>
  <p>{P['long']} &middot; {total} questions &middot; fifty on each unit, every answer worked out</p>
</header>

<main class="container">

<section class="unit-content">
<h2 id="about">About these questions</h2>
<p>Model questions written at the standard of the paper, unit by unit: problems that take several steps, &ldquo;which of the statements are correct&rdquo;, match List I with List II, and assertion and reason, as well as direct questions. Each one has four options and one right answer, and <em>Show Answer</em> gives the full working, often with the reason the tempting wrong option is wrong, and a link to the notes.</p>
<p>They are written for practice and are not questions from a past paper. For shorter recall questions use <a href="../mcqs.html">{P['mcqs_label']}</a>; for the real thing, work through <a href="{P['solved']}">{P['solved_label']}</a>.</p>

<h2 id="units">Units</h2>
<ul class="model-units">
{items}</ul>
{more}</section>

<div class="pagination">
  <a href="../mcqs.html">&larr; Model MCQs</a>
  <a class="next" href="../index.html">{P['home']} &rarr;</a>
</div>
</main>

<footer class="site-footer">
  <p>{P['name']} Model Questions &middot; <a href="../index.html">Back to {P['home']}</a></p>
</footer>

</body>
</html>
"""


def main():
    apply = "--apply" in sys.argv
    for paper, P in PAPERS.items():
        units = load(paper)
        if not units:
            continue
        pages, counts = [], {}
        for i in range(len(units)):
            name, text, nq, keys = unit_page(paper, P, units, i)
            counts[units[i][0]] = nq
            pages.append((name, text))
            print("%s unit %d: %d questions; keys %s" % (paper, units[i][0], nq, dict(sorted(keys.items()))))
        pages.append(index_page(paper, P, units, counts))
        if apply:
            os.makedirs(os.path.join(ROOT, P["dir"]), exist_ok=True)
            for name, text in pages:
                with open(os.path.join(ROOT, P["dir"], name), "w", encoding="utf-8") as fh:
                    fh.write(text)
            print("wrote %d pages in %s" % (len(pages), P["dir"]))
    if not apply:
        print("dry run -- pass --apply to write")


if __name__ == "__main__":
    main()
