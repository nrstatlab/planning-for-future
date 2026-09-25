#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the solved APPSC Assistant Statistical Officer Paper-II pages, every
question solved:

    exams/appsc/solved-2025-paper-ii.html   the paper of 29 April 2025
    exams/appsc/solved-2022-paper-ii.html   the paper of 4 November 2022

    python3 appsc_paper.py            # dry run, prints a summary
    python3 appsc_paper.py --apply    # writes the pages

The same rules as the syllabus maps:

1. THE PAPER IS NEVER RETYPED HERE. For 2025, questions, options and the
   marked key come from appsc_paper_2025.json, which pdftext_appsc_paper.py
   read out of the Commission's PDF. The 2022 PDF prints its questions as
   pictures, so their words were transcribed once, into
   appsc_paper_2022_text.py (and are held to an OCR reading of the pictures
   by recheck_appsc_2022.py); its numbering and key come from
   appsc_paper_2022.json, which pdftext_appsc_2022.py read out of the PDF.
   Only the working, the topic and any flag are written in the _data files.
2. THE KEY SHOWN IS THE PAPER'S. Where the working finds the paper loose, a
   flag says so beside the Commission's answer; it never replaces it.
3. A "STUDY THIS" LINK IS EARNED. It is printed only if the page's own text
   contains the topic's evidence pattern, or the build stops. A topic this
   site does not teach says so, and is listed at the end.
"""
import html
import json
import os
import re
import sys

import labels
import appsc_paper_data
import appsc_paper_2022_data
from appsc_paper_data import GROUPS, ITEMS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = os.path.join(ROOT, "exams", "appsc") + os.sep
MAP = "assistant-statistical-officer.html"
SITE = "https://nrstatlab.github.io/planning-for-future/exams/appsc/"
labels.BASE = BASE


def load_2025():
    data = json.load(open(os.path.join(HERE, "appsc_paper_2025.json"), encoding="utf-8"))
    return data["header"], data["questions"], data["images"]


def load_2022():
    """The 2022 paper in the 2025 paper's shape: numbering, option IDs and key
    from the JSON the PDF was read into, the words from the transcription."""
    from appsc_paper_2022_text import TEXT
    data = json.load(open(os.path.join(HERE, "appsc_paper_2022.json"), encoding="utf-8"))
    header = dict(data["header"])
    marks = header.pop("Marks per question")
    if len(marks) != 1:
        raise SystemExit("2022: questions carry different marks: %s" % marks)
    m = re.match(r"Correct Marks : (\S+) Wrong Marks : (\S+)$", marks[0])
    header["Number of Questions"] = str(len(data["questions"]))
    header["Section Negative Marks"] = m.group(2)
    qs = []
    for q in data["questions"]:
        t = TEXT[q["n"]]
        if len(t["options"]) != len(q["options"]):
            raise SystemExit("2022 Q%d: %d options transcribed, %d in the PDF"
                             % (q["n"], len(t["options"]), len(q["options"])))
        qs.append({"n": q["n"], "stem": t["stem"], "key": q["key"],
                   "options": [dict(o, no=k + 1) for k, o in enumerate(t["options"])]})
    return header, qs, {}


PAPERS = [
    {"year": "2025", "out": "solved-2025-paper-ii.html", "load": load_2025, "data": appsc_paper_data,
     "source": "docs/sources/appsc-aso-2025-paper-ii.pdf", "maths": False,
     "date": "29 April 2025", "held": "Held 29 April 2025",
     "lede": "The previous Assistant Statistical Officer examination&rsquo;s subject paper",
     "set_against": "The paper was set against the same ten-item syllabus as the current notification",
     "marked": "which marks the correct option of every question with a tick",
     "words": "The English version of each question is reproduced; the paper also prints it in Telugu."},
    {"year": "2022", "out": "solved-2022-paper-ii.html", "load": load_2022, "data": appsc_paper_2022_data,
     "source": "docs/sources/appsc-aso-2022-paper-ii.pdf", "maths": True,
     "date": "4 November 2022", "held": "Question paper of 4 November 2022",
     "lede": "An earlier Assistant Statistical Officer subject paper",
     "set_against": "Its questions fall under the same ten items of the Paper-II syllabus",
     "marked": "which marks the correct option of every question in green, with a tick",
     "words": "In this PDF every question and option is printed as a picture, English above Telugu, "
              "with no text behind it; the English is transcribed here from those pictures. The "
              "numbering and the answer marked are read from the PDF itself."},
]
TOKEN = re.compile(r"\[\[([^\]]+)\]\]")
# What the paper prints as a picture, read off the page: marked, so that
# recheck_appsc_paper.py can hold every OTHER word to the PDF.
IMG = '<span class="pdfimg" data-img="%s">%s</span>'


def page_text(rel):
    t = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    t = re.sub(r"<!-- site-(nav|foot|head).*?<!-- /site-\1 -->", "", t, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def study_links(topics):
    """topic -> (href from this page, label), or None; the build stops on a
    link whose page does not contain its evidence."""
    out = {}
    for topic, (item, path, evidence) in topics.items():
        if path is None:
            out[topic] = None
            continue
        if not os.path.exists(os.path.join(ROOT, path)):
            raise SystemExit("topic %s: %s does not exist" % (topic, path))
        if not re.search(evidence, page_text(path)):
            raise SystemExit("topic %s: %r not found in %s" % (topic, evidence, path))
        href = os.path.relpath(os.path.join(ROOT, path), BASE).replace(os.sep, "/")
        out[topic] = (href, labels.label(href))
    return out


MATH = re.compile(r"(\$[^$]+\$)")


def text(s, images, maths=False):
    """Paper text as HTML: escaped, and each image token replaced by what the
    image prints (already in $...$). Text read out of a PDF keeps a bare $
    away from MathJax; a transcription (maths=True) writes its mathematics
    in $...$ and has no other $."""
    parts = TOKEN.split(s)
    out = []
    for i, part in enumerate(parts):
        if i % 2:
            out.append(IMG % (part, images[part]))
        elif maths:
            if part.count("$") % 2:
                raise SystemExit("unbalanced $ in %r" % s)
            out.append(html.escape(part, quote=False))
        else:
            out.append(html.escape(part, quote=False).replace("$", '<span class="usd">$</span>'))
    return "".join(out)


def table_html(rows, images, maths):
    """The first row is a heading. A heading row with a gap in it (a cell
    spanning the columns after it) has a row of sub-headings under it, which
    holds no figure. In a heading row, a cell followed by empty ones spans them."""
    heads = 1
    while (heads < len(rows) and not all(rows[heads - 1])
           and not any(re.search(r"\d", c) for c in rows[heads])):
        heads += 1
    body = []
    for r, row in enumerate(rows):
        tag = "th" if r < heads else "td"
        cells, k = [], 0
        while k < len(row):
            span = 1
            if tag == "th" and row[k]:
                while k + span < len(row) and not row[k + span]:
                    span += 1
            cells.append("<%s%s>%s</%s>" % (tag, ' colspan="%d"' % span if span > 1 else "",
                                              text(row[k], images, maths), tag))
            k += span
        body.append("<tr>%s</tr>" % "".join(cells))
    return '<div class="scroll"><table>%s</table></div>' % "".join(body)


def stem_html(q, images, maths=False):
    out = []
    for p in q["stem"]:
        if "p" in p:
            out.append("<p>%s</p>" % text(p["p"], images, maths))
        elif "img" in p:
            out.append("<p>%s</p>" % (IMG % (p["img"], images[p["img"]])))
        elif "list" in p:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % text(t, images, maths) for t in p["list"]))
        else:
            out.append(table_html(p["table"], images, maths))
    return "".join(out)


def option_html(o, images, maths):
    """An option read from the PDF has "text"; a transcribed one has its
    printed "lines", or is a "table"."""
    if "text" in o:
        return text(o["text"], images, maths)
    if "table" in o:
        return table_html(o["table"], images, maths)
    return "<br>".join(text(t, images, maths) for t in o["lines"])


def build(paper):
    header, qs, images = paper["load"]()
    solutions, topics = paper["data"].SOLUTIONS, paper["data"].TOPICS
    links = study_links(topics)
    missing = [q["n"] for q in qs if q["n"] not in solutions]
    if missing:
        raise SystemExit("%s: no solution written for Q%s" % (paper["year"], ", Q".join(map(str, missing))))
    rows = []
    for q in qs:
        topic, working, flag = solutions[q["n"]]
        if topic not in topics:
            raise SystemExit("%s Q%d: unknown topic %r" % (paper["year"], q["n"], topic))
        rows.append((q, topics[topic][0], topic, working, flag))
    return header, images, links, rows


def mcq(q, item, topic, working, flag, images, links, maths=False):
    n = q["n"]
    opts = "".join('<li value="%d"%s>%s</li>' % (o["no"], ' class="key"' if o["no"] == q["key"] else "",
                                                option_html(o, images, maths)) for o in q["options"])
    if q["key"]:
        o = q["options"][q["key"] - 1]
        if "table" in o:
            answer = "<strong>Answer: (%d)</strong>, the table marked (%d)" % (q["key"], q["key"])
        else:
            answer = "<strong>Answer: (%d) %s</strong>" % (q["key"], option_html(o, images, maths))
    else:
        answer = "<strong>No answer: the Commission withdrew this question.</strong>"
    link = links[topic]
    study = ('<p class="study">Study this: <a href="%s">%s</a></p>' % (html.escape(link[0]), link[1])
             if link else '<p class="study none">Not taught on this site yet &mdash; see '
                          '<a href="#where-this-site-is-thinnest">where this site is thinnest</a>.</p>')
    note = '<p class="flag">&#9888; %s</p>' % flag if flag else ""
    return ('<div class="mcq" id="q%d"><div class="q"><span class="qn">Q%d.</span> %s</div>\n'
            '<ol class="options">%s</ol>\n'
            '<details><summary>Show answer</summary><p>%s</p><p>%s</p>%s%s</details></div>\n'
            % (n, n, stem_html(q, images, maths), opts, answer, working, study, note))


def qlist(ns):
    return " and ".join(", ".join("Q%d" % n for n in ns).rsplit(", ", 1))


def render(paper, header, images, links, rows):
    by_item = {}
    for q, item, *_ in rows:
        by_item.setdefault(item, []).append(q["n"])
    withdrawn = [q["n"] for q, *_ in rows if not q["key"]]
    flagged = [q["n"] for q, _, _, _, flag in rows if flag]
    gaps = [(q["n"], topic) for q, _, topic, _, _ in rows if links[topic] is None]
    maths = paper["maths"]
    others = [p for p in PAPERS if p is not paper]

    a = []
    desc = ("The APPSC Assistant Statistical Officer Paper-II of %s, all %d questions "
            "with the answer the Commission marked, the working, and the page on this site that "
            "teaches each one." % (paper["date"], len(rows)))
    title = "APPSC Assistant Statistical Officer &mdash; Paper-II, %s, Solved" % paper["date"]
    a.append('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
             '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
             '<title>%s</title>\n<meta property="og:title" content="%s">\n'
             '<meta name="description" content="%s">\n<meta property="og:description" content="%s">\n'
             '<meta property="og:type" content="article">\n<meta property="og:site_name" content="NRSTATLAB">\n'
             '<meta name="twitter:card" content="summary">\n<meta property="og:url" content="%s">\n'
             '<link rel="stylesheet" href="../../statistics/css/styles.css">\n'
             % (title, title, desc, desc, SITE + paper["out"]))
    a.append(MATHJAX)
    a.append(STYLE)
    a.append('</head>\n<body>\n\n<div class="wrapper">\n\n'
             '  <div class="banner">\n    <h1>APPSC Assistant Statistical Officer &mdash; Paper-II, Solved</h1>\n'
             '    <p>%s &middot; every question with the Commission&rsquo;s marked answer, '
             'the working, and where it is taught</p>\n  </div>\n\n' % paper["held"])
    a.append('  <p class="lede">%s, all %d questions in the paper&rsquo;s own words. Under each, '
             '<em>Show answer</em> gives the option the Commission marked correct, the working that '
             'gets there, and the page on this site that teaches the topic. %s &mdash; see the '
             '<a href="%s">syllabus map</a>. %s</p>\n\n'
             % (paper["lede"], len(rows), paper["set_against"], MAP,
                " ".join('Also solved: the <a href="%s">paper of %s</a>.' % (p["out"], p["date"])
                         for p in others)))
    a.append('  <div class="note">\n'
             '    <p><strong>Source.</strong> The Commission&rsquo;s question paper preview '
             '&ldquo;%s&rdquo;, created %s (<a href="../../%s">the PDF</a>), %s. It states: %s '
             'questions, duration %s minutes, total marks %s, negative marks %s per wrong answer. %s</p>\n'
             '    <p style="margin-bottom:0"><strong>How to read it.</strong> The answer shown is '
             'always the one the paper marks. Where the working finds the paper loose &mdash; a '
             'misprint, or a key that rests on one reading of the question &mdash; a &#9888; note '
             'says so beside it (%d questions). %s by the Commission and %s no answer.</p>\n  </div>\n\n'
             % (html.escape(header["Question Paper Name"]), header["Creation Date"].split()[0],
                paper["source"], paper["marked"], header["Number of Questions"], header["Duration"],
                header["Total Marks"], header["Section Negative Marks"], paper["words"], len(flagged),
                qlist(withdrawn) + (" were withdrawn" if len(withdrawn) > 1 else " was withdrawn"),
                "have" if len(withdrawn) > 1 else "has"))

    # where the questions fall, by syllabus item
    top = max(len(v) for v in by_item.values())
    bars = "".join('<div class="chart-row"><span class="chart-label"><a href="%s#%s">%d. %s</a></span>'
                   '<span class="chart-track"><span class="chart-bar" style="width:%.1f%%">%d</span></span></div>'
                   % (MAP, ITEMS[i][1], i, ITEMS[i][0], 100.0 * len(by_item.get(i, [])) / top,
                      len(by_item.get(i, [])))
                   for i in sorted(ITEMS))
    a.append('  <div class="pyq-chart"><h3>Where the %d questions fall</h3><p class="chart-note">By '
             'item of the Paper-II syllabus. Each question is placed in the item it tests; the '
             'reasoning-style questions sit with the subject they reason about.</p>%s</div>\n\n'
             % (len(rows), bars))

    a.append('  <ul class="jump">%s<li><a href="#where-this-site-is-thinnest">Where this site is '
             'thinnest</a></li></ul>\n\n'
             % "".join('<li><a href="#%s">%s</a></li>' % (gid, name) for gid, name, _ in GROUPS))
    for gid, name, items in GROUPS:
        qs = [r for r in rows if r[1] in items]
        span = "Q%d&ndash;Q%d" % (min(r[0]["n"] for r in qs), max(r[0]["n"] for r in qs))
        a.append('  <h2 id="%s">%s <small>%d questions &middot; %s</small></h2>\n' % (gid, name, len(qs), span))
        for q, item, topic, working, flag in qs:
            a.append(mcq(q, item, topic, working, flag, images, links, maths))
        a.append("\n")

    a.append('  <h2 id="where-this-site-is-thinnest">Where this site is thinnest</h2>\n')
    by_topic = {}
    for n, topic in gaps:
        by_topic.setdefault(topic, []).append(n)
    a.append('  <p>%d questions test something no page on this site teaches yet. The working above '
             'is all there is for them for now:</p>\n  <ul class="gaps">%s</ul>\n'
             % (len(gaps), "".join('<li>%s &mdash; %s</li>' % (GAP_NAMES[t], ", ".join(
                 '<a href="#q%d">Q%d</a>' % (n, n) for n in ns)) for t, ns in by_topic.items())))
    a.append('\n</div>\n\n</body>\n</html>\n')
    return "".join(a), by_item, withdrawn, flagged, gaps

GAP_NAMES = {
    "value": "The labour theory of value",
    "consumption": "The consumption function: MPC, APC and APS",
    "parallel": "The parallel economy",
    "natural-u": "The natural rate of unemployment",
    "occupation": "Occupational structure and population density",
    "welfare": "The PDS, the minimum support price and the PQLI",
    "company": "The Companies Act, 2013 on books of account",
    "gates": "Logic gates",
    "dma": "Direct memory access",
    "excel-use": "Everyday Excel operations (AutoFit, F2, deleting rows, leading zeros)",
}
GAP_NAMES.update(appsc_paper_2022_data.GAP_NAMES)

MATHJAX = r"""<script>
window.MathJax = {
  tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']], processEscapes: true },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
"""

STYLE = """<style>
  .mcq { background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:14px 18px; margin:12px 0; }
  .mcq .q { font-weight:600; color:#16233a; }
  .mcq .q p { margin:.2rem 0 .45rem; }
  .mcq .qn { color:#0f4c81; font-weight:700; margin-right:.2rem; }
  .mcq .q table { margin:.3rem 0 .6rem; font-weight:400; font-size:.92rem; }
  .mcq ol.options { margin:.2rem 0 .5rem 1.6rem; padding:0; }
  .mcq ol.options li { margin:.12rem 0; }
  .mcq details { background:#ecfdf5; border-left:3px solid #047857; border-radius:0 8px 8px 0; padding:.45rem .8rem; margin-top:.3rem; }
  .mcq details summary { cursor:pointer; font-weight:600; color:#065f46; }
  .mcq details p { margin:.4rem 0; }
  .mcq .study { font-size:.9rem; }
  .mcq .study.none { color:#5b6474; font-style:italic; }
  .mcq .flag { color:#92400e; font-size:.9rem; }
  .jump { list-style:none; display:flex; flex-wrap:wrap; gap:8px; padding:0; margin:10px 0 18px; }
  .jump a { display:inline-block; padding:6px 12px; border:1px solid #e2e8f0; border-radius:999px; background:#fff; text-decoration:none; font-weight:600; font-size:.9rem; }
  h2 small { font-size:.62em; font-weight:600; color:#5b6474; margin-left:.4rem; }
  .pyq-chart { background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:16px 18px; margin:14px 0 20px; }
  .pyq-chart h3 { margin:0 0 .2rem; color:#0f4c81; }
  .pyq-chart .chart-note { margin:0 0 .9rem; color:#5b6474; font-size:.88rem; }
  .chart-row { display:grid; grid-template-columns:minmax(9rem,17rem) 1fr; align-items:center; gap:.6rem; margin:.3rem 0; }
  .chart-label { font-size:.86rem; text-align:right; line-height:1.2; }
  .chart-label a { color:#16233a; text-decoration:none; border-bottom:1px dotted #94a3b8; }
  .chart-track { display:block; background:#eef2f7; border-radius:5px; overflow:hidden; }
  .chart-bar { display:block; background:#0f4c81; color:#fff; font-size:.8rem; font-weight:700; padding:.25rem .5rem; border-radius:5px; min-width:1.8rem; box-sizing:border-box; text-align:right; }
  .gaps li { margin:.25rem 0; }
  .scroll { overflow-x:auto; }
  .mcq mjx-container[display="true"], .mcq p > mjx-container { max-width:100%; overflow-x:auto; overflow-y:hidden; }
  .mcq mjx-container:not([display="true"]) { display:inline-block; max-width:100%; overflow-x:auto; overflow-y:hidden; vertical-align:middle; }
  @media (max-width:560px){ .chart-row{ grid-template-columns:1fr; gap:.15rem; } .chart-label{ text-align:left; } }
</style>
"""


def main():
    for paper in PAPERS:
        header, images, links, rows = build(paper)
        page, by_item, withdrawn, flagged, gaps = render(paper, header, images, links, rows)
        print("%s: %d questions  %d flagged  %d withdrawn  %d not taught here yet"
              % (paper["year"], len(rows), len(flagged), len(withdrawn), len(gaps)))
        for i in sorted(ITEMS):
            print("  item %2d  %-45s %3d" % (i, ITEMS[i][0], len(by_item.get(i, []))))
        if "--apply" in sys.argv:
            out = BASE + paper["out"]
            open(out, "w", encoding="utf-8").write(page)
            print("wrote %s (%d bytes)" % (os.path.relpath(out, ROOT), len(page)))
    if "--apply" not in sys.argv:
        print("dry run -- pass --apply to write")


if __name__ == "__main__":
    main()
