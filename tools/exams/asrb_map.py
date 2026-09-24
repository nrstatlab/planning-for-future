#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build exams/asrb-net/index.html from the syllabus and the map data.

    python3 asrb_map.py            # dry run, prints a summary
    python3 asrb_map.py --apply    # writes the page

Two rules this generator exists to enforce:

1. THE SYLLABUS TEXT IS NEVER RETYPED. Every line printed on the page is a
   contiguous slice of asrb_syllabus.txt, which came out of the PDF. A row can
   choose which items to group; it cannot choose their wording.

2. LINK LABELS ARE READ FROM THE DESTINATION'S OWN <title>. Hand-written
   labels are how a map ends up pointing confidently at the wrong page -- that
   happened twice while the ISS map was being built, and both times the label
   was right and the href was not. Here a wrong href produces a visibly wrong
   label instead of a plausible one.
"""
import html
import os
import re
import sys

import mapkit
from asrb_map_data import UNITS

HERE = os.path.dirname(os.path.abspath(__file__))
# tools/exams/ -> repository root is two levels up; pages live in exams/.
ROOT = os.path.dirname(os.path.dirname(HERE))
PAPERS = os.path.join(ROOT, "exams")
OUT = os.path.join(PAPERS, "asrb-net", "index.html")
SYLLABUS = os.path.join(HERE, "asrb_syllabus.txt")

SOURCE_NOTE = (
    "a syllabus document supplied to this site, headed "
    "<strong>&ldquo;49. AGRICULTURAL STATISTICS&rdquo;</strong> and running from "
    "page 104 to page 106 of a larger combined syllabus"
)


def syllabus_units():
    """{unit number: [item, ...]} straight out of the extracted text."""
    text = open(SYLLABUS, encoding="utf-8").read()
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(Unit \d+: )", text)
    out = {}
    for i in range(1, len(parts), 2):
        num = int(re.search(r"Unit (\d+)", parts[i]).group(1))
        out[num] = [s.strip() for s in parts[i + 1].split(";") if s.strip()]
    return out


def strip_unit_title(item, title):
    """Item 0 of each unit carries the unit title glued to its front."""
    return item[len(title):].strip() if item.startswith(title) else item


def page_title(path):
    """The destination's own <title>, minus the site-wide suffix."""
    full = os.path.normpath(os.path.join(PAPERS, "asrb-net", path))
    if not os.path.exists(full):
        raise SystemExit("destination does not exist: %s" % path)
    m = re.search(r"<title>(.*?)</title>",
                  open(full, encoding="utf-8").read(), re.S)
    if not m:
        raise SystemExit("destination has no <title>: %s" % path)
    return re.sub(r"\s+", " ", m.group(1)).strip()


def label(path):
    t = page_title(path)
    # "Topic — Subject (Unit N)"  ->  "Subject (Unit N)"; else the whole title.
    m = re.search(r"&mdash;\s*(.+)$|—\s*(.+)$", t)
    return m.group(1) or m.group(2) if m else t


def esc(s):
    return html.escape(s, quote=True)


def build_rows():
    items = syllabus_units()
    units = []
    for num, title, spec in UNITS:
        raw = items[num]
        raw = [strip_unit_title(raw[0], title)] + raw[1:]
        expected = 0
        rows = []
        for start, end, dest, grade in spec:
            if start != expected:
                raise SystemExit(
                    "unit %d: rows skip items %d..%d" % (num, expected, start))
            expected = end
            line = "; ".join(raw[start:end])
            line = line.rstrip(".")
            rows.append((line, dest, grade))
        if expected != len(raw):
            raise SystemExit("unit %d: %d items covered, %d in the document"
                             % (num, expected, len(raw)))
        units.append((num, title, rows))
    return units


def render(units):
    all_grades = [g for _, _, rows in units for _, _, g in rows]
    c = mapkit.counts(all_grades)
    out = []
    a = out.append

    a('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n')
    a('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    desc = ("Every line of the ASRB NET Agricultural Statistics syllabus mapped onto "
            "the notes on this site, graded deep, brief or missing. Statistical "
            "Genetics is named as a gap rather than hidden.")
    a('<title>ASRB NET Agricultural Statistics &mdash; Syllabus Map</title>\n')
    a('<meta property="og:title" content="ASRB NET Agricultural Statistics &mdash; Syllabus Map">\n')
    a('<meta name="description" content="%s">\n' % desc)
    a('<meta property="og:description" content="%s">\n' % desc)
    a('<meta property="og:type" content="article">\n')
    a('<meta property="og:site_name" content="NRSTATLAB">\n')
    a('<meta name="twitter:card" content="summary">\n')
    a('<meta property="og:url" content="https://nrstatlab.github.io/planning-for-future/exams/asrb-net/index.html">\n')
    a('<link rel="stylesheet" href="../../statistics/msc/css/styles.css">\n')
    a('<link rel="canonical" href="https://nrstatlab.github.io/planning-for-future/exams/asrb-net/index.html">\n')
    a(STYLE)
    a(BAR_STYLE)
    a('</head>\n<body>\n')
    a(BAR)
    a('\n')
    a('<div class="wrapper">\n\n')
    a('  <div class="banner">\n'
      '    <h1>ASRB NET &mdash; Agricultural Statistics</h1>\n'
      '    <p>The syllabus, one line at a time, pointed at the page that teaches it</p>\n'
      '  </div>\n\n')

    a('  <p class="lede">This page maps %s. Each line is reproduced as the '
      'document words it, then pointed at the page on this site that teaches it, '
      'with the depth stated rather than implied.</p>\n\n' % SOURCE_NOTE)

    a('  <div class="note">\n'
      '    <p><strong>What this document is, exactly.</strong> It carries no '
      'letterhead, no notification number, no date and no issuing authority &mdash; '
      'it is a Word file printed to PDF, and its own page numbers show it is an '
      'extract of subject 49 from a larger syllabus. So this page maps its '
      '<em>topics</em> and says nothing about marks, duration, paper count, '
      'negative marking or eligibility, none of which appear in it. If you have the '
      'official notification, those things are in there and not here.</p>\n'
      '  </div>\n\n')

    a(mapkit.tally_html(c))
    a('\n')
    a(mapkit.GRADE_KEY)
    a('\n')

    for num, title, rows in units:
        head = "Unit %d &mdash; %s" % (num, esc(title))
        a(mapkit.h2(head))
        uc = mapkit.counts([g for _, _, g in rows])
        a('  <p class="unit-tally">%d line%s &middot; %d deep &middot; %d brief '
          '&middot; %d not here</p>\n'
          % (sum(uc.values()), "" if sum(uc.values()) == 1 else "s",
             uc["deep"], uc["brief"], uc["missing"]))
        table_rows = [(esc(line), dest, grade) for line, dest, grade in rows]
        a(mapkit.table_html(table_rows, label, esc))
        a('\n')

    gaps = ["Unit %d &mdash; %s" % (num, esc(line[:110] + ("&hellip;" if len(line) > 110 else "")))
            for num, _, rows in units for line, _, g in rows if g == "missing"]
    a(mapkit.h2("What is not here"))
    a(gaps_block(units))

    a('</div>\n\n</body>\n</html>\n')
    return "".join(out), c


def gaps_block(units):
    gen = [rows for num, _, rows in units if num == 6][0]
    missing_lines = [(num, line) for num, _, rows in units
                     for line, _, g in rows if g == "missing"]
    gen_missing = sum(1 for num, _ in missing_lines if num == 6)
    others = [(num, line) for num, line in missing_lines if num != 6]
    out = ['  <div class="gaps">\n']
    out.append(
        '    <p><strong>Unit 6, Statistical Genetics, is not on this site at all.</strong> '
        '%d of its %d rows are red &mdash; every one except <em>Survival analysis</em>, '
        'which is covered elsewhere and is the only line in the unit that is. That is the '
        'single largest gap any map here reports. Population and quantitative genetics '
        '&mdash; Hardy&ndash;Weinberg equilibrium, gene and genotypic frequencies, '
        'heritability, breeding value, selection indices &mdash; is a subject this site '
        'does not teach, not a corner of one it teaches thinly. Read it from a standard '
        'text; nothing here will substitute.</p>\n' % (gen_missing, len(gen)))
    if others:
        items = "".join(
            "      <li><b>Unit %d</b> &mdash; %s</li>\n"
            % (num, esc(line[:150] + ("…" if len(line) > 150 else "")))
            for num, line in others)
        out.append(
            '    <p><strong>And %d line%s elsewhere.</strong> These are named one by '
            'one rather than rounded off, because a candidate needs to know which '
            'book to open:</p>\n    <ul>\n%s    </ul>\n'
            % (len(others), "" if len(others) == 1 else "s", items))
    out.append('  </div>\n\n')
    return "".join(out)


# The hub bar is copied verbatim from the ISS and APPSC map pages rather than
# reinvented. Its rules live in an inline <style> on every page that carries it,
# because the shared subject stylesheet this page links does not define them --
# the first draft of this generator used its own class names and the bar
# rendered as plain underlined links on white, which the screenshot caught.
BAR_STYLE = """<style>
.nrstatlab-bar{background:#0f4c81;color:#fff;font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif;font-size:.9rem;line-height:1.5;padding:10px 22px;margin:0}
.nrstatlab-bar .nrstatlab-inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.nrstatlab-bar a.nrstatlab-brand{color:#fff;font-weight:700;letter-spacing:.09em;text-decoration:none;border-bottom:2px solid rgba(255,255,255,.45);padding-bottom:1px}
.nrstatlab-bar a.nrstatlab-brand:hover{border-bottom-color:#fff}
.nrstatlab-bar .nrstatlab-sep{opacity:.55}
.nrstatlab-bar .nrstatlab-here{opacity:.95}
.nrstatlab-bar a.nrstatlab-topics{color:#fff;text-decoration:none;font-weight:600;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.32);border-radius:6px;padding:2px 10px;white-space:nowrap}
.nrstatlab-bar a.nrstatlab-topics:hover{background:rgba(255,255,255,.3)}
</style>
"""

BAR = ('<div class="nrstatlab-bar"><div class="nrstatlab-inner">'
       '<a class="nrstatlab-brand" href="../../">NRSTATLAB</a>'
       '<span class="nrstatlab-sep">&rsaquo;</span>'
       '<a href="../" style="color:#fff">Examinations</a>'
       '<span class="nrstatlab-sep">&rsaquo;</span>'
       '<span class="nrstatlab-here">ASRB NET</span>'
       '<a class="nrstatlab-topics" href="../../topics.html">Topics A&ndash;Z</a>'
       '</div></div>\n')

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
  .none { color:#9ca3af; font-style:italic; font-size:.88rem; }
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


def main():
    units = build_rows()
    page, c = render(units)
    total = sum(c.values())
    print("%d rows  %d deep  %d brief  %d not here  %.0f%% covered"
          % (total, c["deep"], c["brief"], c["missing"], mapkit.covered(c)))
    for num, title, rows in units:
        uc = mapkit.counts([g for _, _, g in rows])
        print("  Unit %d  %-58s %2d rows  %2d/%2d/%2d"
              % (num, title[:58], len(rows), uc["deep"], uc["brief"], uc["missing"]))
    if "--apply" in sys.argv:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        open(OUT, "w", encoding="utf-8").write(page)
        print("wrote %s (%d bytes)" % (OUT, len(page)))
    else:
        print("dry run -- pass --apply to write")


if __name__ == "__main__":
    main()
