#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove the UGC NET map says what the UGC NET Bureau's syllabus says.

    python3 recheck_ugc.py [PATH_TO.pdf]     # default: docs/sources/ugc-net-statistics-code-107.pdf

Written after the page, from the document rather than from the generator: it
extracts the PDF itself and reads the FINISHED HTML, so a bug in ugc_map.py
or pdftext_ugc.py cannot hide behind the same bug here. It asserts:

1.  Every syllabus line printed on the page appears verbatim in the document,
    in document order.
2.  The lines account for the WHOLE document: the page's words, unit by unit,
    are exactly the document's words, so no clause can be dropped, reordered
    or invented without failing (a verbatim line can still be a line with a
    clause cut out of its middle -- check 1 alone would pass that).
3.  Every link resolves to a file that exists, every #anchor to an id on that
    page, and a "not here" row has no link at all.
4.  The committed ugc_syllabus.txt is still exactly what the PDF extracts to.

THE FIVE DECLARED EXCEPTIONS. Five glyphs in the PDF are Word equation
objects (Cambria Math, no text mapping) and extract as blanks. They were read
off the rendered page and are restated here, by name and independently of
pdftext_ugc.py, as the only difference allowed between PDF and page.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PDF = os.path.join(ROOT, "docs", "sources", "ugc-net-statistics-code-107.pdf")
PAGE = os.path.join(ROOT, "exams", "ugc-net", "index.html")
SYLLABUS = os.path.join(HERE, "ugc_syllabus.txt")

EQUATIONS = {
    "Taylor’s theorem, L Hospital’s rule": "Taylor’s theorem, L′ Hospital’s rule",
    "Factorial experiments- , confounding": "Factorial experiments- 2², 2³, confounding",
    "Analysis of variance for linear model, , adjusted , tests":
        "Analysis of variance for linear model, R², adjusted R², tests",
    "generalized statistic,": "generalized T² statistic,",
    "scripts and functions. and other word": "scripts and functions. Latex and other word",
}
UNIT_HEAD = re.compile(r"Unit (?:I|II|III|IV|V|VI|VII|VIII|IX|X): ")

checks = 0
fails = []


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def norm(s):
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def pdf_text(pdf):
    import fitz                                   # PyMuPDF
    text = norm(" ".join(p.get_text() for p in fitz.open(pdf)))
    text = text[text.index("Unit I: Probability and Distributions Basic"):]
    for blank, printed in EQUATIONS.items():
        ok(text.count(blank) == 1, "equation blank not found exactly once: %r" % blank)
        text = text.replace(blank, printed)
    return text


def table_rows(page):
    out = []
    for tr in re.findall(r"<tr>(.*?)</tr>", page, re.S):
        tds = re.findall(r"<td>(.*?)</td>", tr, re.S)
        if len(tds) != 3:
            continue
        line = norm(re.sub(r"<[^>]+>", "", tds[0]))
        hrefs = re.findall(r'href="([^"]+)"', tds[1])
        g = re.search(r'class="g (\w+)"', tds[2])
        out.append((line, hrefs, g.group(1) if g else "?"))
    return out


def words(s):
    return re.findall(r"[^\s,;.:]+", s)


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else PDF
    source = pdf_text(pdf)
    page = open(PAGE, encoding="utf-8").read()
    rows = table_rows(page)
    ok(len(rows) > 0, "no table rows on the page")
    print("rows on the page: %d" % len(rows))

    # 1
    cursor = 0
    for line, _, _ in rows:
        at = source.find(line, cursor)
        if at < 0:
            ok(False, ("OUT OF ORDER: " if source.find(line) >= 0 else "NOT IN DOCUMENT: ") + line[:90])
            continue
        ok(True, "")
        cursor = at + len(line)

    # 2 -- the document's words, unit headings removed, against the page's
    doc_words = words(UNIT_HEAD.sub(" ", source))
    heads = re.findall(r"<h2 id=\"unit-[^\"]*\">Unit [IVX]+ &mdash; (.*?)</h2>", page)
    doc_words = [w for w in doc_words]
    page_words = []
    # The unit titles are printed as headings, not as table lines, so they are
    # put back where the document has them before comparing.
    tables = re.split(r"<h2 id=\"unit-", page)[1:]
    for chunk in tables:
        title = html.unescape(re.search(r"&mdash; (.*?)</h2>", chunk).group(1))
        page_words += words(title)
        for line, _, _ in table_rows(chunk):
            page_words += words(line)
    ok(page_words == doc_words,
       "the page's words are not the document's words (first difference at word %s)"
       % next((i for i, (a, b) in enumerate(zip(page_words, doc_words)) if a != b),
              min(len(page_words), len(doc_words))))

    # 3
    base = os.path.dirname(PAGE)
    for line, hrefs, grade in rows:
        if grade == "missing":
            ok(not hrefs, "a 'not here' row carries a link: %s" % line[:60])
        else:
            ok(bool(hrefs), "a %s row has no link: %s" % (grade, line[:60]))
        for h in hrefs:
            path, _, anchor = h.partition("#")
            full = os.path.normpath(os.path.join(base, path))
            if not os.path.exists(full):
                ok(False, "link to a missing file: %s" % h)
                continue
            if anchor:
                ok('id="%s"' % anchor in open(full, encoding="utf-8").read(),
                   "link to a missing anchor: %s" % h)
            else:
                ok(True, "")

    # 4
    committed = norm(open(SYLLABUS, encoding="utf-8").read())
    ok(committed == source, "ugc_syllabus.txt differs from what the PDF extracts to")

    print("%d checks, %d failures" % (checks, len(fails)))
    for f in fails[:20]:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
