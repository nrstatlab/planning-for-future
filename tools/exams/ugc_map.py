#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build exams/ugc-net/index.html -- the UGC NET hub, which is its syllabus map.

    python3 ugc_map.py            # dry run, prints a summary
    python3 ugc_map.py --apply    # writes the page

The same three rules as the other maps (asrb_map.py):

1. THE SYLLABUS TEXT IS NEVER RETYPED. Every printed line is a contiguous
   slice of ugc_syllabus.txt, which pdftext_ugc.py extracted from the UGC NET
   Bureau's PDF. A row chooses which items to group, never their wording.
2. LINK LABELS ARE READ FROM THE DESTINATION: a UGC NET section's own heading,
   a course page's own <title> (labels.py).
3. THE GRADE IS EARNED. A course is linked only if the row's evidence pattern
   is found in that page's text; a UGC NET section only if its anchor exists.
   Either failure stops the build. "deep" = a full course unit teaches it,
   "brief" = the UGC NET section alone, "not here" = nothing does.

The map IS the hub, as it is for ISS, CSIR, ASRB and APPSC: the menu, the
cards and the breadcrumbs all open index.html, so that is where the map has
to be. It lived at syllabus-map.html for one release; that path is now a
redirect stub, and nothing may be written there again.
"""
import html
import os
import re
import sys

import labels
import mapkit
from ugc_map_data import UNITS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = os.path.join(ROOT, "exams", "ugc-net") + os.sep
OUT = BASE + "index.html"
SYLLABUS = os.path.join(HERE, "ugc_syllabus.txt")
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
labels.BASE = BASE


def items(body):
    """The document's pieces: split after , ; . : at top level (outside
    parentheses), each keeping its separator, so "".join(items) == body."""
    out, cur, depth = [], "", 0
    for i, c in enumerate(body):
        cur += c
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif depth == 0 and c in ",;.:" and (i + 1 == len(body) or body[i + 1] == " "):
            out.append(cur)
            cur = ""
    if cur.strip():
        out.append(cur)
    return out


def syllabus_units():
    """[(roman, title, [item, ...])] in document order."""
    text = open(SYLLABUS, encoding="utf-8").read().strip()
    out = []
    for i, (roman, title, _) in enumerate(UNITS):
        head = "Unit %s: %s " % (roman, title)
        a = text.index(head) + len(head)
        if i + 1 < len(UNITS):
            b = text.index("Unit %s: %s " % (UNITS[i + 1][0], UNITS[i + 1][1]))
        else:
            b = len(text)
        body = text[a:b].strip()
        its = items(body)
        assert "".join(its) == body, "item split lost text in Unit %s" % roman
        out.append((roman, title, its))
    return out


def page_text(path):
    t = open(os.path.normpath(BASE + path), encoding="utf-8").read()
    t = re.sub(r"<!-- site-(nav|foot|head).*?<!-- /site-\1 -->", "", t, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


_SECTIONS = {}


def section_heading(unit_no, anchor):
    """The UGC NET unit page's own heading for #anchor, number stripped."""
    key = (unit_no, anchor)
    if key not in _SECTIONS:
        page = open(BASE + "unit%d.html" % unit_no, encoding="utf-8").read()
        m = re.search(r'<h2 id="%s"[^>]*>(.*?)</h2>' % re.escape(anchor), page, re.S)
        if not m:
            raise SystemExit("UGC NET unit%d.html has no section #%s" % (unit_no, anchor))
        h = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        h = re.sub(r"^\d+\.\s*", "", h)
        # Headings write maths as $2^2$ for the page's MathJax; the map has none.
        h = re.sub(r"\$([^$]+)\$", lambda mm: mm.group(1).replace("^2", "²").replace("^3", "³")
                   .replace("^", ""), h)
        _SECTIONS[key] = h
    return _SECTIONS[key]


def build_rows():
    doc = syllabus_units()
    units = []
    for k, ((roman, title, spec), (_, _, its)) in enumerate(zip(UNITS, doc)):
        n = k + 1
        expected, rows = 0, []
        for start, end, section, courses in spec:
            if start != expected:
                raise SystemExit("Unit %s: rows skip items %d..%d" % (roman, expected, start))
            expected = end
            line = "".join(its[start:end]).strip().rstrip(",;.:").strip()
            dests = []
            if section:
                dests.append(("unit%d.html#%s" % (n, section),
                              "UGC NET Unit %s &mdash; %s" % (roman, html.escape(section_heading(n, section)))))
            deep = False
            for path, evidence in courses:
                full = os.path.normpath(BASE + path)
                if not os.path.exists(full):
                    raise SystemExit("Unit %s row %d-%d: %s does not exist" % (roman, start, end, path))
                if not re.search(evidence, page_text(path)):
                    raise SystemExit("Unit %s row %d-%d: %r not found in %s"
                                     % (roman, start, end, evidence, path))
                dests.append((path, labels.label(path)))
                deep = True
            grade = "deep" if deep else ("brief" if section else "missing")
            rows.append((line, dests, grade))
        if expected != len(its):
            raise SystemExit("Unit %s: %d items covered, %d in the document" % (roman, expected, len(its)))
        units.append((roman, title, rows))
    return units


def esc(s):
    return html.escape(s, quote=True)


def cell(dests):
    if not dests:
        return '<span class="none">nothing on this site teaches it</span>'
    return "<br>".join('<a href="%s">%s</a>' % (esc(p), lab) for p, lab in dests)


def render(units):
    grades = [g for _, _, rows in units for _, _, g in rows]
    c = mapkit.counts(grades)
    a = []
    url = "https://nrstatlab.github.io/planning-for-future/exams/ugc-net/index.html"
    desc = ("UGC NET Statistics (code 107): ten units of study notes, model MCQs and a solved "
            "paper, with every line of the official syllabus mapped onto the unit notes and the "
            "full courses on this site.")
    a.append('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
             '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
             '<title>UGC NET Statistics Study Material</title>\n'
             '<meta property="og:title" content="UGC NET Statistics Study Material">\n'
             '<meta name="description" content="%s">\n<meta property="og:description" content="%s">\n'
             '<meta property="og:type" content="article">\n<meta property="og:site_name" content="NRSTATLAB">\n'
             '<meta name="twitter:card" content="summary">\n<meta property="og:url" content="%s">\n'
             '<link rel="stylesheet" href="../../statistics/css/styles.css">\n' % (desc, desc, url))
    a.append(STYLE)
    a.append('</head>\n<body>\n\n<div class="wrapper">\n\n'
             '  <div class="banner">\n    <h1>UGC NET Statistics Study Material</h1>\n'
             '    <p>Subject code 107 &middot; the official syllabus, line by line, and the page that teaches each line</p>\n'
             '  </div>\n\n')
    a.append('  <p class="lede">Ten units of study notes written for the <strong>UGC NET Bureau&rsquo;s '
             '&ldquo;NET Syllabus, Subject: Statistics, Code 107&rdquo;</strong>, with that syllabus '
             'reproduced below in the document&rsquo;s own words. Each line points at the section of '
             'the unit notes that teaches it and, where one exists, the full course on this site '
             'that takes it further.</p>\n\n')
    a.append(START_PATH)
    a.append(unit_list())
    a.append('  <div class="note">\n    <p><strong>What this page does not say.</strong> The '
             'syllabus lists topics and nothing else, so this page says nothing about marks, '
             'duration, the number of questions or eligibility. Read those in the current '
             'notification for the session you are sitting.</p>\n'
             '    <p style="margin-bottom:0">Five symbols in the PDF are equation objects that do '
             'not survive as text &mdash; L&prime; in L&prime;Hospital, 2&sup2; and 2&sup3;, R&sup2;, '
             'T&sup2; and the word Latex. They were read off the printed page and are shown as '
             'printed.</p>\n  </div>\n\n')
    a.append(mapkit.tally_html(c))
    a.append('\n')
    a.append(mapkit.h2("How to read the depth column") + GRADE_TEXT)
    for n, (roman, title, rows) in enumerate(units, 1):
        a.append(mapkit.h2("Unit %s &mdash; %s" % (roman, esc(title))))
        uc = mapkit.counts([g for _, _, g in rows])
        a.append('  <p class="unit-tally">%d lines &middot; %d deep &middot; %d brief &middot; %d not here'
                 ' &middot; <a href="unit%d.html">Read the Unit %s notes &rarr;</a></p>\n'
                 % (len(rows), uc["deep"], uc["brief"], uc["missing"], n, roman))
        a.append('  <div class="scroll">\n    <table>\n      <tr><th>Syllabus line, as prescribed</th>'
                 '<th>Where it is taught here</th><th>Depth</th></tr>\n')
        for line, dests, grade in rows:
            a.append('      <tr><td>%s</td><td>%s</td><td><span class="g %s">%s</span></td></tr>\n'
                     % (esc(line), cell(dests), grade, mapkit.GRADE_TEXT[grade]))
        a.append('    </table>\n  </div>\n\n')
    brief = [(r, l) for r, _, rows in units for l, _, g in rows if g == "brief"]
    missing = [(r, l) for r, _, rows in units for l, _, g in rows if g == "missing"]
    a.append(mapkit.h2("Where this site is thinnest"))
    a.append(mapkit.gaps_html(["<b>Unit %s</b> &mdash; %s" % (r, esc(l)) for r, l in missing],
                              "this syllabus",
                              "Every line above points at a page on this site."))
    a.append('  <p>%d lines are taught only in the UGC NET unit notes, at exam level, with no full '
             'course behind them yet. They are marked <span class="g brief">brief</span> above; '
             'Unit IX, Stochastic Processes, is the largest block of them, because no course here '
             'teaches Markov chains or queues.</p>\n\n' % len(brief))
    a.append('</div>\n\n</body>\n</html>\n')
    return "".join(a), c


START_PATH = """  <ol class="start-path" aria-label="Start here">
    <li><a href="unit1.html"><b>Read the ten units in order</b></a> &mdash; Unit I,
    Probability and Distributions, first; the later units build on it.</li>
    <li><a href="mcqs.html"><b>Test yourself on the model MCQs</b></a> &mdash; every unit,
    each answer explained rather than just marked.</li>
    <li><a href="solved-2026.html"><b>Work through the solved June 2026 paper</b></a>.</li>
    <li><a href="#unit-i-probability-and-distributions"><b>Check the syllabus, line by line</b></a>
    &mdash; below, each line with the unit section and the full course that teach it.</li>
  </ol>

"""

# One line on each unit page, saying what OUR notes cover -- not what the exam
# sets, which only the syllabus below says.
UNIT_NOTES = [
    "Probability axioms, Bayes' theorem, random variables, MGF, standard distributions, convergence, CLT, LLN.",
    "Sequences, series, continuity, differentiation, integration, vector spaces, eigenvalues, quadratic forms.",
    "SRS, stratified, cluster, systematic, ratio and regression estimation, ANOVA, CRD, RBD, LSD, BIBD.",
    "Unbiasedness, MLE, MoM, UMVUE, Cram\u00e9r\u2013Rao, sufficiency, Rao\u2013Blackwell, Lehmann\u2013Scheff\u00e9, CIs.",
    "Neyman\u2013Pearson, UMP tests, LRT, SPRT, chi-square, sign, Wilcoxon, Mann\u2013Whitney, Kruskal\u2013Wallis.",
    "Gauss\u2013Markov, OLS, GLS, dummy variables, multicollinearity, heteroscedasticity, autocorrelation, 2SLS.",
    "ACF, PACF, stationarity, AR, MA, ARMA, ARIMA, Yule\u2013Walker, forecasting, spectral density.",
    "Multivariate normal, Wishart, Hotelling's T\u00b2, discriminant, principal components, canonical correlation.",
    "Markov chains, Chapman\u2013Kolmogorov, gambler's ruin, Poisson process, birth\u2013death, M/M/1 queues.",
    "MoSPI, NSO, NSC, Indian statisticians, R programming, LaTeX basics.",
]


def unit_list():
    """The ten unit pages, as cards, titled from the syllabus's own unit titles."""
    out = [mapkit.h2("The ten units"), '  <div class="units">\n']
    for n, ((roman, title, _), note) in enumerate(zip(UNITS, UNIT_NOTES), 1):
        out.append('    <a class="unit-link" href="unit%d.html"><span class="num">Unit %s</span>'
                   '<b>%s</b><span class="what">%s</span></a>\n' % (n, roman, esc(title), esc(note)))
    out.append('  </div>\n\n')
    return "".join(out)


GRADE_TEXT = """  <p><span class="g deep">deep</span> a full course unit on this site teaches it, with the
  derivation worked out &mdash; the link after the UGC NET section.
  &nbsp;<span class="g brief">brief</span> the UGC NET unit notes cover it at exam level:
  the definition, the result and two worked examples, without the full derivation.
  &nbsp;<span class="g missing">not here</span> nothing on this site teaches it. Every
  course link was checked against that page&rsquo;s own text when this map was built.</p>
"""

STYLE = """<style>
  .tally { list-style:none; display:flex; flex-wrap:wrap; gap:10px; padding:0; margin:22px 0 6px; }
  .tally li { background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:10px 14px;
              font-size:.86rem; color:#4b5563; display:flex; flex-direction:column; gap:2px; min-width:104px; }
  .tally b { font-size:1.35rem; color:#0f4c81; }
  .unit-tally { font-size:.85rem; color:#5b6474; margin:.2rem 0 .6rem; }
  .g { display:inline-block; padding:2px 9px; border-radius:999px; font-size:.76rem; font-weight:600; white-space:nowrap; }
  .g.deep { background:#d1fae5; color:#065f46; }
  .g.brief { background:#fef3c7; color:#92400e; }
  .g.missing { background:#fee2e2; color:#991b1b; }
  .none { color:#991b1b; font-style:italic; font-size:.88rem; }
  .scroll { overflow-x:auto; }
  .scroll table { min-width:640px; }
  .scroll td:first-child { text-align:left; }
  .scroll td:nth-child(2) { text-align:left; font-size:.9rem; }
  .gaps { background:#fef2f2; border:1px solid #fecaca; border-left:5px solid #ef4444;
          border-radius:10px; padding:16px 20px; margin:18px 0 28px; }
  .gaps ul { margin:.4rem 0 0; padding-left:1.1rem; }
  .units { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:10px; margin:10px 0 26px; }
  .unit-link { display:flex; flex-direction:column; gap:3px; background:#fff; border:1px solid #e2e8f0;
               border-radius:10px; padding:12px 14px; text-decoration:none; color:#1f2937; }
  .unit-link:hover, .unit-link:focus-visible { border-color:#0f4c81; }
  .unit-link .num { font-size:.76rem; font-weight:700; letter-spacing:.04em; text-transform:uppercase; color:#0f4c81; }
  .unit-link b { font-size:.98rem; }
  .unit-link .what { font-size:.84rem; color:#4b5563; }
</style>
"""


def main():
    units = build_rows()
    page, c = render(units)
    print("%d rows  %d deep  %d brief  %d not here  %.0f%% covered"
          % (sum(c.values()), c["deep"], c["brief"], c["missing"], mapkit.covered(c)))
    for roman, title, rows in units:
        uc = mapkit.counts([g for _, _, g in rows])
        print("  Unit %-5s %-55s %2d rows  %2d/%2d/%2d"
              % (roman, title[:55], len(rows), uc["deep"], uc["brief"], uc["missing"]))
    if "--apply" in sys.argv:
        open(OUT, "w", encoding="utf-8").write(page)
        print("wrote %s (%d bytes)" % (os.path.relpath(OUT, ROOT), len(page)))
    else:
        print("dry run -- pass --apply to write")


if __name__ == "__main__":
    main()
