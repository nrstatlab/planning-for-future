#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build exams/ugc-net/paper-1/index.html -- the UGC NET Paper I hub, which is its syllabus map.

    python3 ugc_paper1_map.py            # dry run, prints a summary
    python3 ugc_paper1_map.py --apply    # writes the page

The same three rules as the Statistics map (ugc_map.py), whose item splitter
and styles this reuses:

1. THE SYLLABUS TEXT IS NEVER RETYPED. Every printed line is a contiguous
   slice of ugc_paper1_syllabus.txt, which pdftext_ugc_paper1.py extracted
   from the UGC NET Bureau's PDF. The page's quotation of the document's
   objective and of its note on how the paper is set comes from the same file.
2. LINK LABELS ARE READ FROM THE DESTINATION: a Paper I section's own heading,
   a course page's own <title> (labels.py).
3. THE GRADE IS EARNED. A course is linked only if the row's evidence pattern
   is found in that page's text; a Paper I section only if its anchor exists.
   Either failure stops the build.

A unit whose notes are not written yet has rows with no section; its card on
this page says so rather than linking to a page that does not exist.
"""
import html
import os
import re
import sys

import labels
import mapkit
from ugc_map import STYLE, items
from ugc_paper1_map_data import UNITS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = os.path.join(ROOT, "exams", "ugc-net", "paper-1") + os.sep
OUT = BASE + "index.html"
SYLLABUS = os.path.join(HERE, "ugc_paper1_syllabus.txt")
labels.BASE = BASE


def source():
    """{"SYLLABUS": ..., "INTRO": ..., "NOTE": ...} from the extracted file."""
    out = {}
    for line in open(SYLLABUS, encoding="utf-8").read().splitlines():
        key, _, text = line.partition(": ")
        out[key] = text.strip()
    if set(out) != {"SYLLABUS", "INTRO", "NOTE"}:
        raise SystemExit("ugc_paper1_syllabus.txt: expected SYLLABUS, INTRO and NOTE lines, found %s" % sorted(out))
    return out


def syllabus_units():
    """[(roman, title, [item, ...])] in document order."""
    text = source()["SYLLABUS"]
    out = []
    for i, (roman, title, _) in enumerate(UNITS):
        head = "Unit %s: %s " % (roman, title)
        a = text.index(head) + len(head)
        b = text.index("Unit %s: %s " % UNITS[i + 1][:2]) if i + 1 < len(UNITS) else len(text)
        body = text[a:b].strip()
        its = items(body)
        assert "".join(its) == body, "item split lost text in Unit %s" % roman
        out.append((roman, title, its))
    return out


def unit_page(n):
    return BASE + "unit%d.html" % n


def page_text(path):
    t = open(os.path.normpath(BASE + path), encoding="utf-8").read()
    t = re.sub(r"<!-- site-(nav|foot|head).*?<!-- /site-\1 -->", "", t, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


_SECTIONS = {}


def section_heading(n, anchor):
    """The Paper I unit page's own heading for #anchor, number stripped."""
    key = (n, anchor)
    if key not in _SECTIONS:
        if not os.path.exists(unit_page(n)):
            raise SystemExit("Paper I unit%d.html does not exist, but a row links its #%s" % (n, anchor))
        page = open(unit_page(n), encoding="utf-8").read()
        m = re.search(r'<h2 id="%s"[^>]*>(.*?)</h2>' % re.escape(anchor), page, re.S)
        if not m:
            raise SystemExit("Paper I unit%d.html has no section #%s" % (n, anchor))
        h = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        _SECTIONS[key] = re.sub(r"^\d+\.\s*", "", h)
    return _SECTIONS[key]


def build_rows():
    doc = syllabus_units()
    units = []
    for n, ((roman, title, spec), (_, _, its)) in enumerate(zip(UNITS, doc), 1):
        expected, rows = 0, []
        for start, end, section, courses in spec:
            if start != expected:
                raise SystemExit("Unit %s: rows skip items %d..%d" % (roman, expected, start))
            expected = end
            line = "".join(its[start:end]).strip().rstrip(",;.:").strip()
            dests = []
            if section:
                dests.append(("unit%d.html#%s" % (n, section),
                              "Paper I Unit %s &mdash; %s" % (roman, html.escape(section_heading(n, section)))))
            deep = False
            for path, evidence in courses:
                full = os.path.normpath(BASE + path)
                if not os.path.exists(full):
                    raise SystemExit("Unit %s row %d-%d: %s does not exist" % (roman, start, end, path))
                if not re.search(evidence, page_text(path)):
                    raise SystemExit("Unit %s row %d-%d: %r not found in %s" % (roman, start, end, evidence, path))
                if path not in [d[0] for d in dests]:
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
        return '<span class="none">nothing on this site teaches it yet</span>'
    return "<br>".join('<a href="%s">%s</a>' % (esc(p), lab) for p, lab in dests)


# One line per unit card, saying what OUR notes cover -- not what the exam sets.
UNIT_NOTES = [
    "Levels of teaching, learners, factors, methods, SWAYAM and MOOCs, support systems, evaluation and CBCS.",
    "Types of research, positivism, methods, steps, thesis writing and referencing, ICT, ethics.",
    "How to read a passage and answer each kind of question, with worked passages.",
    "Types of communication, verbal and non-verbal, inter-cultural and classroom, barriers, mass media.",
    "Types of reasoning, number and letter series, codes, and the arithmetic the paper sets.",
    "Arguments, categorical propositions, the square of opposition, fallacies, Venn diagrams, Indian logic.",
    "Sources and kinds of data, charts and tables, reading them, and data in governance.",
    "ICT terms, the internet, intranet, e-mail, conferencing, digital initiatives, e-governance.",
    "MDGs and SDGs, pollution and waste, climate change, energy, disasters, laws and agreements.",
    "Ancient centres of learning, higher education since Independence, programmes, policy and governance.",
]


def unit_list():
    out = [mapkit.h2("The ten units"), '  <div class="units">\n']
    for n, ((roman, title, _), note) in enumerate(zip(UNITS, UNIT_NOTES), 1):
        if os.path.exists(unit_page(n)):
            out.append('    <a class="unit-link" href="unit%d.html"><span class="num">Unit %s</span>'
                       '<b>%s</b><span class="what">%s</span></a>\n' % (n, roman, esc(title), esc(note)))
        else:
            out.append('    <div class="unit-link soon"><span class="num">Unit %s</span>'
                       '<b>%s</b><span class="what">Notes in preparation.</span></div>\n' % (roman, esc(title)))
    out.append('  </div>\n\n')
    return "".join(out)


def start_path():
    a = ['  <ol class="start-path" aria-label="Start here">\n',
         '    <li><a href="unit1.html"><b>Read the units in order</b></a> &mdash; Unit I, Teaching Aptitude, '
         'first.</li>\n']
    if os.path.exists(BASE + "mcqs.html"):
        a.append('    <li><a href="mcqs.html"><b>Test yourself on the model MCQs</b></a> &mdash; every '
                 'answer explained rather than just marked.</li>\n')
    a.append('    <li><a href="../solved-2026.html#paper1"><b>Work through Paper I of June 2026</b></a>, '
             'all 50 questions solved.</li>\n'
             '    <li><a href="#unit-i-teaching-aptitude"><b>Check the syllabus, line by line</b></a> '
             '&mdash; below, each line with the section that teaches it.</li>\n  </ol>\n\n')
    return "".join(a)


EXTRA_STYLE = """<style>
  .unit-link.soon { background:#f8fafc; color:#5b6474; border-style:dashed; }
  .quote { border-left:4px solid #0f4c81; background:#fff; padding:12px 16px; margin:14px 0; border-radius:0 10px 10px 0; }
  .quote p { margin:0; }
</style>
"""


def render(units):
    src = source()
    grades = [g for _, _, rows in units for _, _, g in rows]
    c = mapkit.counts(grades)
    note = re.match(r"\(i\)\s*(.*?)\s*\(ii\)", src["NOTE"])
    if not note:
        raise SystemExit("the syllabus note has no clause (i)")
    title = "UGC NET Paper I Study Material"
    url = "https://nrstatlab.github.io/planning-for-future/exams/ugc-net/paper-1/index.html"
    desc = ("UGC NET Paper I, the General Paper on Teaching and Research Aptitude: study notes and "
            "model MCQs unit by unit, with every line of the official syllabus mapped onto them.")
    a = ['<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
         '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
         '<title>%s</title>\n<meta property="og:title" content="%s">\n'
         '<meta name="description" content="%s">\n<meta property="og:description" content="%s">\n'
         '<meta property="og:type" content="article">\n<meta property="og:site_name" content="StatsTricks360">\n'
         '<meta name="twitter:card" content="summary">\n<meta property="og:url" content="%s">\n'
         '<link rel="stylesheet" href="../../../statistics/css/styles.css">\n' % (title, title, desc, desc, url),
         STYLE, EXTRA_STYLE,
         '</head>\n<body>\n\n<div class="wrapper">\n\n'
         '  <div class="banner">\n    <h1>%s</h1>\n'
         '    <p>General Paper on Teaching &amp; Research Aptitude &middot; Code 00 &middot; the official '
         'syllabus, line by line, and the page that teaches each line</p>\n  </div>\n\n' % title,
         '  <p class="lede">Paper I is the paper every UGC NET candidate sits, whatever their subject. '
         'These notes are written for the <strong>UGC NET Bureau&rsquo;s syllabus, &ldquo;General Paper on '
         'Teaching &amp; Research Aptitude&rdquo;</strong>, reproduced below in the document&rsquo;s own '
         'words. For Paper II in Statistics, see <a href="../index.html">UGC NET Statistics (Code 107)</a>.</p>\n\n',
         '  <div class="quote">\n    <p><strong>What the syllabus says it tests.</strong> &ldquo;%s&rdquo;</p>\n'
         '  </div>\n\n' % esc(src["INTRO"]),
         '  <div class="note">\n    <p><strong>How the paper is set, in the syllabus&rsquo;s own words.</strong> '
         '&ldquo;%s&rdquo; With ten units, that is 50 questions and 100 marks. The syllabus says nothing '
         'about duration or eligibility; read those in the current notification for the session you are '
         'sitting.</p>\n  </div>\n\n' % esc(note.group(1)),
         start_path(), unit_list(), mapkit.tally_html(c), '\n',
         mapkit.h2("How to read the depth column"),
         '  <p><span class="g deep">deep</span> a full course unit on this site also teaches it, further '
         'than the exam needs &mdash; the link after the Paper I section.\n'
         '  &nbsp;<span class="g brief">brief</span> the Paper I notes cover it at exam level: what it '
         'means, the points examiners ask about, and worked examples.\n'
         '  &nbsp;<span class="g missing">not here</span> nothing on this site teaches it yet. Every '
         'course link was checked against that page&rsquo;s own text when this map was built.</p>\n']
    for n, (roman, title_u, rows) in enumerate(units, 1):
        a.append(mapkit.h2("Unit %s &mdash; %s" % (roman, esc(title_u))))
        uc = mapkit.counts([g for _, _, g in rows])
        tail = (' &middot; <a href="unit%d.html">Read the Unit %s notes &rarr;</a>' % (n, roman)
                if os.path.exists(unit_page(n)) else " &middot; notes in preparation")
        a.append('  <p class="unit-tally">%d lines &middot; %d deep &middot; %d brief &middot; %d not here%s</p>\n'
                 % (len(rows), uc["deep"], uc["brief"], uc["missing"], tail))
        a.append('  <div class="scroll">\n    <table>\n      <tr><th>Syllabus line, as prescribed</th>'
                 '<th>Where it is taught here</th><th>Depth</th></tr>\n')
        for line, dests, grade in rows:
            a.append('      <tr><td>%s</td><td>%s</td><td><span class="g %s">%s</span></td></tr>\n'
                     % (esc(line), cell(dests), grade, mapkit.GRADE_TEXT[grade]))
        a.append('    </table>\n  </div>\n\n')
    missing = [(r, l) for r, _, rows in units for l, _, g in rows if g == "missing"]
    a.append(mapkit.h2("Where this site is thinnest"))
    a.append(mapkit.gaps_html(["<b>Unit %s</b> &mdash; %s" % (r, esc(l)) for r, l in missing],
                              "this syllabus", "Every line above points at a page on this site."))
    a.append('</div>\n\n</body>\n</html>\n')
    return "".join(a), c


def main():
    units = build_rows()
    page, c = render(units)
    print("%d rows  %d deep  %d brief  %d not here  %.0f%% covered"
          % (sum(c.values()), c["deep"], c["brief"], c["missing"], mapkit.covered(c)))
    for roman, title, rows in units:
        uc = mapkit.counts([g for _, _, g in rows])
        print("  Unit %-5s %-50s %2d rows  %2d/%2d/%2d" % (roman, title[:50], len(rows), uc["deep"], uc["brief"], uc["missing"]))
    if "--apply" in sys.argv:
        os.makedirs(BASE, exist_ok=True)
        open(OUT, "w", encoding="utf-8").write(page)
        print("wrote %s (%d bytes)" % (os.path.relpath(OUT, ROOT), len(page)))
    else:
        print("dry run -- pass --apply to write")


if __name__ == "__main__":
    main()
