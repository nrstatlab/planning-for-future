#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove the UGC NET Paper I pages: the map says what the syllabus says, and the
model MCQs are well formed and, where a key can be computed, rightly keyed.

    python3 recheck_ugc_paper1.py [PATH_TO.pdf]   # default: docs/sources/ugc-net-paper-1-general.pdf

Written after the pages and independently of the generators (ugc_paper1_map.py,
ugc_paper1_mcqs.py, pdftext_ugc_paper1.py): it extracts the PDF itself and reads
the FINISHED HTML. Needs PyMuPDF for part A.

A. THE MAP (exams/ugc-net/paper-1/index.html), as recheck_ugc.py does for Paper II:
   1. every syllabus line printed appears verbatim in the document, in order;
   2. the page's words, unit by unit, are exactly the document's words;
   3. every link resolves to a file, every #anchor to an id; a "not here" row
      has no link, and every other row has one;
   4. the committed ugc_paper1_syllabus.txt is what the PDF extracts to;
   5. the page quotes the syllabus's objective and its note (i) verbatim.

B. THE MCQS (exams/ugc-net/paper-1/mcqs.html):
   1. each unit heading reads "Unit N — Title (k MCQs)", units in order, and
      unit N has a notes page;
   2. questions are numbered 1..k with k as stated, each with four options and
      an answer that starts with one key letter A-D and goes on to explain;
   3. no two stems in a unit are the same;
   4. a passage (div.comp) says how many questions it serves, and exactly that
      many follow it before the next passage or the end of the unit; in a unit
      with passages, no question comes before the first;
   5. a data-approved date, where present, is a real date;
   6. each entry of ugc_paper1_keys.py, worked out, equals the keyed option and
      no other.
"""
import datetime
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PDF = os.path.join(ROOT, "docs", "sources", "ugc-net-paper-1-general.pdf")
BASE = os.path.join(ROOT, "exams", "ugc-net", "paper-1")
PAGE = os.path.join(BASE, "index.html")
MCQS = os.path.join(BASE, "mcqs.html")
SYLLABUS = os.path.join(HERE, "ugc_paper1_syllabus.txt")
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

checks = 0
fails = []


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
    return cond


def norm(s):
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def strip_tags(s):
    return norm(re.sub(r"<[^>]+>", " ", s))


def words(s):
    return re.findall(r"[^\s,;.:]+", s)


# ------------------------------------------------------------------ A. the map

def pdf_parts(pdf):
    """(syllabus with unit headings removed, intro, note), from the PDF, from scratch."""
    import pymupdf
    pages = []
    for n, page in enumerate(pymupdf.open(pdf), 1):
        t = page.get_text()
        t = re.sub(r"^\s*%d\s" % n, " ", t, count=1)       # the page number at the top
        pages.append(t)
    text = norm(" ".join(pages).replace("", " "))
    intro = text[text.index("The main objective"):text.index("The details of syllabi")].strip()
    body = text[text.index("The details of syllabi are as follows:") + 38:text.index("NOTE:")].strip()
    note = text[text.index("NOTE:") + 5:].strip()
    return body, intro, note


def table_rows(chunk):
    out = []
    for tr in re.findall(r"<tr>(.*?)</tr>", chunk, re.S):
        tds = re.findall(r"<td>(.*?)</td>", tr, re.S)
        if len(tds) != 3:
            continue
        g = re.search(r'class="g (\w+)"', tds[2])
        out.append((strip_tags(tds[0]), re.findall(r'href="([^"]+)"', tds[1]), g.group(1) if g else "?"))
    return out


def check_map(pdf):
    body, intro, note = pdf_parts(pdf)
    page = open(PAGE, encoding="utf-8").read()
    rows = table_rows(page)
    ok(len(rows) > 0, "map: no table rows")
    print("map: %d rows" % len(rows))

    # 1 -- the document with its "Unit-IV Communication" headings, line by line in order
    doc = body
    cursor = 0
    for line, _, _ in rows:
        at = doc.find(line, cursor)
        if ok(at >= 0, ("map: OUT OF ORDER: " if doc.find(line) >= 0 else "map: NOT IN DOCUMENT: ") + line[:90]):
            cursor = at + len(line)

    # 2 -- words: the document's, against the page's unit titles and lines
    doc_words = words(re.sub(r"Unit-(?:%s)\b" % "|".join(ROMAN), " ", doc))
    page_words = []
    for chunk in re.split(r'<h2 id="unit-', page)[1:]:
        title = html.unescape(re.search(r"&mdash; (.*?)</h2>", chunk).group(1))
        page_words += words(title)
        for line, _, _ in table_rows(chunk):
            page_words += words(line)
    first = next((i for i, (a, b) in enumerate(zip(page_words, doc_words)) if a != b),
                 min(len(page_words), len(doc_words)))
    ok(page_words == doc_words, "map: the page's words are not the document's (first difference at word %d: %r vs %r)"
       % (first, page_words[first:first + 3], doc_words[first:first + 3]))

    # 3 -- links and anchors
    for line, hrefs, grade in rows:
        if grade == "missing":
            ok(not hrefs, "map: a 'not here' row carries a link: %s" % line[:60])
        else:
            ok(bool(hrefs), "map: a %s row has no link: %s" % (grade, line[:60]))
        for h in hrefs:
            path, _, anchor = h.partition("#")
            full = os.path.normpath(os.path.join(BASE, path))
            if not ok(os.path.exists(full), "map: link to a missing file: %s" % h):
                continue
            if anchor:
                ok('id="%s"' % anchor in open(full, encoding="utf-8").read(), "map: link to a missing anchor: %s" % h)

    # 4 -- the committed extraction
    committed = {}
    for ln in open(SYLLABUS, encoding="utf-8").read().splitlines():
        k, _, v = ln.partition(": ")
        committed[k] = v
    doc_headed = body
    for r in ROMAN:
        doc_headed = re.sub(r"Unit-%s (\S)" % r, r"Unit %s: \1" % r, doc_headed, count=1)
    ok(norm(committed.get("SYLLABUS", "")) == doc_headed, "map: ugc_paper1_syllabus.txt SYLLABUS differs from the PDF")
    ok(norm(committed.get("INTRO", "")) == intro, "map: ugc_paper1_syllabus.txt INTRO differs from the PDF")
    ok(norm(committed.get("NOTE", "")) == note, "map: ugc_paper1_syllabus.txt NOTE differs from the PDF")

    # 5 -- the quotations on the page
    text = strip_tags(page)
    ok(intro in text, "map: the page does not quote the syllabus's objective verbatim")
    clause = re.match(r"\(i\)\s*(.*?)\s*\(ii\)", note)
    ok(bool(clause) and clause.group(1) in text, "map: the page does not quote note (i) verbatim")


# ------------------------------------------------------------------ B. the MCQs

UNIT_H2 = re.compile(r'<h2( data-approved="([^"]*)")?>Unit (\d+) — (.*?) \((\d+) MCQs\)</h2>')
ITEM = re.compile(r'<div class="comp" data-questions="(\d+)">|<div class="mcq">(.*?)</details></div>', re.S)


def parse_mcq(block):
    q = re.search(r'<div class="q">(.*?)</div>', block, re.S)
    opts = re.findall(r"<li>(.*?)</li>", re.search(r'<ol class="options">(.*?)</ol>', block, re.S).group(1), re.S)
    ans = re.search(r"<details><summary>Show Answer</summary><p>(.*?)</p>", block + "</details>", re.S)
    return (q.group(1) if q else ""), opts, (ans.group(1) if ans else "")


def number_of(text):
    t = strip_tags(text).replace(",", "")
    m = re.fullmatch(r"-?\d+(?:\.\d+)?", t)
    return (float(t), len(t.split(".")[1]) if "." in t else 0) if m else None


def check_mcqs():
    sys.path.insert(0, HERE)
    import ugc_paper1_keys as K
    page = open(MCQS, encoding="utf-8").read()
    heads = list(UNIT_H2.finditer(page))
    ok(len(heads) > 0, "mcqs: no unit headings")
    found = {}
    for i, h in enumerate(heads):
        _, approved, unit, title, stated = h.groups()
        unit, stated = int(unit), int(stated)
        ok(unit == i + 1, "mcqs: unit %d is heading %d" % (unit, i + 1))
        ok(os.path.exists(os.path.join(BASE, "unit%d.html" % unit)), "mcqs: Unit %d has no notes page" % unit)
        if approved is not None:
            try:
                datetime.date.fromisoformat(approved)
                ok(True, "")
            except ValueError:
                ok(False, "mcqs: Unit %d data-approved %r is not a date" % (unit, approved))
        end = heads[i + 1].start() if i + 1 < len(heads) else len(page)
        chunk = page[h.end():end]
        n, stems = 0, set()
        passage = None                  # [declared, questions seen since it] for the current passage
        has_passage = 'class="comp"' in chunk

        def close(p):
            if p:
                ok(p[1] == p[0], "mcqs: Unit %d: a passage says it serves %d questions, %d follow it" % (unit, p[0], p[1]))
        for m in ITEM.finditer(chunk):
            if m.group(1):
                close(passage)
                passage = [int(m.group(1)), 0]
                continue
            ok(not has_passage or passage is not None,
               "mcqs: Unit %d has passages, but a question comes before the first" % unit)
            if passage:
                passage[1] += 1
            n += 1
            stem, opts, ans = parse_mcq(m.group(2))
            num = re.match(r"\s*(\d+)\.\s*", stem)
            ok(bool(num) and int(num.group(1)) == n, "mcqs: Unit %d: question %d is numbered %s" % (unit, n, num and num.group(1)))
            body = re.sub(r"^\s*\d+\.\s*", "", stem)
            ok(norm(body) not in stems, "mcqs: Unit %d Q%d repeats an earlier stem" % (unit, n))
            stems.add(norm(body))
            ok(len(opts) == 4, "mcqs: Unit %d Q%d has %d options" % (unit, n, len(opts)))
            ok(len({norm(o) for o in opts}) == len(opts), "mcqs: Unit %d Q%d has two identical options" % (unit, n))
            km = re.match(r"([A-D])\. (\S.*)", ans, re.S)
            if not ok(bool(km) and len(strip_tags(km.group(2))) >= 20,
                      "mcqs: Unit %d Q%d: the answer is not a key letter followed by an explanation" % (unit, n)):
                continue
            found[(unit, n)] = (km.group(1), opts)
        close(passage)
        ok(n == stated, "mcqs: Unit %d heading says %d MCQs, found %d" % (unit, stated, n))
    print("mcqs: %d units, %d questions" % (len(heads), len(found)))

    # 6 -- computed keys
    for (unit, n), (expr, kind) in sorted(K.COMPUTED.items()):
        if not ok((unit, n) in found, "keys: Unit %d Q%d is in ugc_paper1_keys.py but not on the page" % (unit, n)):
            continue
        key, opts = found[(unit, n)]
        value = eval(expr, {k: getattr(K, k) for k in dir(K) if not k.startswith("_")})
        if kind == "number":
            hits = []
            for label, o in zip("ABCD", opts):
                parsed = number_of(o)
                ok(parsed is not None, "keys: Unit %d Q%d option %s is not a number: %r" % (unit, n, label, o))
                if parsed and abs(round(value, parsed[1]) - parsed[0]) < 1e-9:
                    hits.append(label)
            ok(hits == [key], "keys: Unit %d Q%d works out to %r, matching options %s; the key is %s"
               % (unit, n, value, hits or "none", key))
    print("keys: %d computed" % len(K.COMPUTED))


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else PDF
    check_map(pdf)
    check_mcqs()
    print("%d checks, %d failures" % (checks, len(fails)))
    for f in fails[:30]:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
