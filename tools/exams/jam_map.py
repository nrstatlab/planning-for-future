#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build exams/iit-jam/index.html from the JAM Mathematical Statistics syllabus and the map data.

    python3 jam_map.py            # dry run, prints a summary
    python3 jam_map.py --apply    # writes the page

The rules are the ones asrb_map.py states:

1. THE SYLLABUS TEXT IS NEVER RETYPED. Every line printed on the page is a
   contiguous slice of jam_ms_syllabus.txt, which came out of the PDF.

2. LINK LABELS ARE READ FROM THE DESTINATION. The course and unit come from the
   destination's <title>, the section from the heading that carries the #id, so
   a wrong href produces a visibly wrong label. A missing page or section stops
   the build.
"""
import html
import os
import re
import sys
from urllib.parse import quote

import mapkit
from jam_map_data import SECTIONS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE_DIR = os.path.join(ROOT, "exams", "iit-jam")
OUT = os.path.join(PAGE_DIR, "index.html")
SYLLABUS = os.path.join(HERE, "jam_ms_syllabus.txt")
URL = "https://statstricks360.com/exams/iit-jam/index.html"


def syllabus_sections():
    """{section number: (title, [line, ...])} straight out of the syllabus file."""
    out, cur = {}, None
    for line in open(SYLLABUS, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("# "):
            continue
        m = re.match(r"## (\d+) \| (.+)$", line)
        if m:
            cur = int(m.group(1))
            out[cur] = (m.group(2), [])
        else:
            out[cur][1].append(line)
    return out


def esc(s):
    return html.escape(s, quote=True)


def plain(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"\\\(|\\\)", "", s)
    s = s.replace("\\mathbb{R}^{2}", "R²").replace("^{2}", "²").replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


_cache = {}


def page_text(path):
    full = os.path.normpath(os.path.join(PAGE_DIR, path))
    if full not in _cache:
        if not os.path.exists(full):
            raise SystemExit("destination does not exist: %s" % path)
        _cache[full] = open(full, encoding="utf-8").read()
    return _cache[full]


def label(dest):
    path, _, anchor = dest.partition("#")
    text = page_text(path)
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    if not m:
        raise SystemExit("destination has no <title>: %s" % path)
    title = re.sub(r"\s+", " ", html.unescape(m.group(1))).strip()
    if "/ugc-net/unit" in path:
        where = "UGC NET " + title.split(":")[0]
    elif path.endswith("index.html"):
        where = title.split(" — ")[0]
    else:
        where = title.split(" — ")[-1]
    if not anchor:
        return esc(where)
    h = re.search(r'<(h[1-4]) id="%s"[^>]*>(.*?)</\1>' % re.escape(anchor), text, re.S)
    if not h:
        raise SystemExit("no section #%s in %s" % (anchor, path))
    head = re.sub(r"^\d+(\.\d+)?\.?\s+", "", plain(h.group(2)))
    return "%s &mdash; %s" % (esc(where), esc(head))


def href(dest):
    path, _, anchor = dest.partition("#")
    return path + ("#" + quote(anchor, safe="-_") if anchor else "")


def build_rows():
    items = syllabus_sections()
    out = []
    for num, title, spec in SECTIONS:
        doc_title, raw = items[num]
        if doc_title != title:
            raise SystemExit("section %d title differs from the syllabus file" % num)
        expected, rows = 0, []
        for start, end, dest, grade in spec:
            if start != expected:
                raise SystemExit("section %d: rows skip lines %d..%d" % (num, expected, start))
            expected = end
            rows.append((" ".join(raw[start:end]), dest, grade))
        if expected != len(raw):
            raise SystemExit("section %d: %d lines covered, %d in the document" % (num, expected, len(raw)))
        out.append((num, title, rows))
    return out


STYLE = """<style>
  .tally { list-style:none; display:flex; flex-wrap:wrap; gap:10px;
           padding:0; margin:22px 0 6px; }
  .tally li { background:#fff; border:1px solid #e2e8f0; border-radius:10px;
              padding:10px 14px; font-size:.86rem; color:#4b5563;
              display:flex; flex-direction:column; gap:2px; min-width:104px; }
  .tally b { font-size:1.35rem; color:#0f4c81; }
  .unit-tally { font-size:.85rem; color:#6b7280; margin:.2rem 0 .6rem; }
  .g { display:inline-block; padding:2px 9px; border-radius:999px;
       font-size:.76rem; font-weight:600; white-space:nowrap; }
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
  .gaps li { margin:.3rem 0; font-size:.92rem; }
</style>
"""


def render(sections):
    grades = [g for _, _, rows in sections for _, _, g in rows]
    c = mapkit.counts(grades)
    title = "IIT JAM Mathematical Statistics (MS) &mdash; Syllabus Map"
    desc = ("Every line of the IIT JAM 2026 Mathematical Statistics (MS) syllabus, all twelve sections, "
            "pointed at the course unit on this site that teaches it, with the depth stated.")
    out = []
    a = out.append
    a('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n')
    a('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    a('<title>%s</title>\n' % title)
    a('<meta property="og:title" content="%s">\n' % title)
    a('<meta name="description" content="%s">\n' % desc)
    a('<meta property="og:description" content="%s">\n' % desc)
    a('<meta property="og:type" content="article">\n')
    a('<meta property="og:site_name" content="StatsTricks360">\n')
    a('<meta name="twitter:card" content="summary">\n')
    a('<meta property="og:url" content="%s">\n' % URL)
    a('<link rel="stylesheet" href="../../statistics/css/styles.css">\n')
    a('<link rel="canonical" href="%s">\n' % URL)
    a(STYLE)
    a('</head>\n<body>\n\n<div class="wrapper">\n\n')
    a('  <div class="banner">\n'
      '    <h1>IIT JAM &mdash; Mathematical Statistics (MS)</h1>\n'
      '    <p>A PG entrance examination: the syllabus, one line at a time, pointed at the page that teaches it</p>\n'
      '  </div>\n\n')
    a('  <p class="lede">JAM, the Joint Admission Test for Masters, is the entrance examination for '
      'M.Sc. and related programmes at the IITs and other institutes; <strong>Mathematical Statistics '
      '(MS)</strong> is its statistics paper. The paper has twelve sections: three of mathematics '
      '(sequences and series, calculus, matrices) and nine of statistics. This page maps the '
      '<strong>JAM 2026</strong> MS syllabus document. Each line is reproduced as the document words '
      'it, then pointed at the course unit here that teaches it, with the depth stated.</p>\n\n')
    a('  <div class="note">\n'
      '    <p><strong>No exam pattern is stated here.</strong> The syllabus document gives topics only. '
      'Marks, question types, duration, negative marking and eligibility are in the official JAM '
      'information brochure for the year you sit; read that for the rules, and this page for the '
      'statistics.</p>\n'
      '  </div>\n\n')
    a(mapkit.tally_html(c))
    a('\n')
    a(mapkit.GRADE_KEY)
    a('\n')
    for num, sec_title, rows in sections:
        a(mapkit.h2("Section %d &mdash; %s" % (num, esc(sec_title))))
        uc = mapkit.counts([g for _, _, g in rows])
        n = sum(uc.values())
        a('  <p class="unit-tally">%d line%s &middot; %d deep &middot; %d brief &middot; %d not here</p>\n'
          % (n, "" if n == 1 else "s", uc["deep"], uc["brief"], uc["missing"]))
        a(table(rows))
        a('\n')
    missing = ["Section %d &mdash; %s" % (num, esc(line)) for num, _, rows in sections
               for line, _, g in rows if g == "missing"]
    a(mapkit.h2("What is not here"))
    a(mapkit.gaps_html(missing, "the JAM MS syllabus",
                       "Every line above points at a page on this site. Lines marked brief are covered "
                       "at exam-summary level in UGC NET Unit II; the course units linked beside them "
                       "carry the full treatment of the neighbouring lines."))
    a('\n</div>\n\n</body>\n</html>\n')
    return "".join(out), c


def table(rows):
    out = ['  <div class="scroll">\n    <table>\n',
           '      <tr><th>Syllabus line, as prescribed</th><th>Where it is taught here</th>'
           '<th>Depth</th></tr>\n']
    for line, dest, grade in rows:
        ds = mapkit.dests(dest)
        cell = ("<br>".join('<a href="%s">%s</a>' % (esc(href(d)), label(d)) for d in ds)
                if ds else '<span class="none">nothing on this site teaches it</span>')
        out.append('      <tr><td>%s</td><td>%s</td><td><span class="g %s">%s</span></td></tr>\n'
                   % (esc(line), cell, grade, mapkit.GRADE_TEXT[grade]))
    out.append('    </table>\n  </div>\n')
    return "".join(out)


def main():
    sections = build_rows()
    page, c = render(sections)
    print("%d rows  %d deep  %d brief  %d not here  %.0f%% covered"
          % (sum(c.values()), c["deep"], c["brief"], c["missing"], mapkit.covered(c)))
    if "--apply" in sys.argv:
        os.makedirs(PAGE_DIR, exist_ok=True)
        open(OUT, "w", encoding="utf-8").write(page)
        print("wrote %s (%d bytes)" % (OUT, len(page)))
    else:
        print("dry run -- pass --apply to write")


if __name__ == "__main__":
    main()
