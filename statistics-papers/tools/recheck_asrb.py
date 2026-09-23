#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove the ASRB map says what the source document says.

    python3 recheck_asrb.py [PATH_TO.pdf]

Written after the page, from the document rather than from the generator, and
it reads the FINISHED HTML rather than the data file -- so a bug in asrb_map.py
cannot hide behind the same bug here. Three things are asserted:

1.  Every syllabus line printed in the tables appears verbatim in the extracted
    text, and the lines appear in the same order as the document.
2.  Every row's destination link resolves to a file that exists, and every
    "not here" row has no link at all.
3.  The committed asrb_syllabus.txt still matches what the PDF extracts to,
    when the PDF is given. Without it, that one check is skipped and says so.

A recheck that has never failed proves nothing, so this one was mutation
tested: reorder two rows, silently correct "dispersion matrx" to "matrix", and
drop a clause from a line -- each must be caught. See the commit message.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAPERS = os.path.dirname(HERE)
PAGE = os.path.join(PAPERS, "asrb-net", "index.html")
SYLLABUS = os.path.join(HERE, "asrb_syllabus.txt")

checks = 0
fails = []


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


# THE ONE NORMALISATION THIS FILE ALLOWS, DECLARED BY NAME.
#
# The document contains two places where a semicolon is preceded by a space:
#
#     ...Null distribution of Hotelling's T 2 ; Multivariate analysis...
#     ...based upon LDF and Mahalanobis' D 2 ; Canonical correlations...
#
# Both follow a superscript 2, and the space is where the superscript sat --
# a typesetting artifact of the extraction, not something the syllabus says.
# The page joins its items with "; ", so it cannot reproduce that space.
#
# Collapsing it on BOTH sides is therefore comparing like with like. It is
# written here, narrowly and by name, rather than folded into norm() as a
# general "be lenient about punctuation" rule -- every other difference
# between the page and the document still fails this file.
_SPACE_BEFORE_SEMICOLON = re.compile(r"\s+;")


def norm(s):
    """Whitespace-insensitive, entity-decoded, for comparing prose."""
    s = re.sub(r"\s+", " ", html.unescape(s)).strip()
    return _SPACE_BEFORE_SEMICOLON.sub(";", s)


def table_rows(page):
    """(line, hrefs, grade) for every row of every table on the page."""
    out = []
    for tr in re.findall(r"<tr>(.*?)</tr>", page, re.S):
        tds = re.findall(r"<td>(.*?)</td>", tr, re.S)
        if len(tds) != 3:
            continue                                  # the header row
        line = norm(re.sub(r"<[^>]+>", "", tds[0]))
        hrefs = re.findall(r'href="([^"]+)"', tds[1])
        gm = re.search(r'class="g (\w+)"', tds[2])
        out.append((line, hrefs, gm.group(1) if gm else "?"))
    return out


def main():
    page = open(PAGE, encoding="utf-8").read()
    source = norm(open(SYLLABUS, encoding="utf-8").read())
    rows = table_rows(page)

    ok(rows, "no table rows found on the page")
    print("rows on the page: %d" % len(rows))

    # 1. every line verbatim, and in document order
    cursor = 0
    for line, _, _ in rows:
        at = source.find(line, cursor)
        if at < 0:
            anywhere = source.find(line)
            if anywhere < 0:
                ok(False, "NOT IN SOURCE: %s" % line[:90])
            else:
                ok(False, "OUT OF ORDER (found at %d, cursor %d): %s"
                   % (anywhere, cursor, line[:90]))
            continue
        ok(True, "")
        cursor = at + len(line)

    # 1b. THE LINES MUST ACCOUNT FOR THE WHOLE DOCUMENT.
    #
    # Check 1 proves every printed line is real. It does NOT prove the lines
    # are complete: drop a clause from the middle of a row and what is left is
    # still a verbatim contiguous substring, so check 1 passes. Mutation
    # testing found exactly that hole -- removing "Bernoulli weak law of large
    # numbers; " from a line went undetected until this check was added.
    #
    # So: split both sides into semicolon items and compare the sequences.
    # Nothing can be dropped, reordered or invented without failing here.
    page_items = [i.strip().rstrip(".") for line, _, _ in rows
                  for i in line.split(";") if i.strip()]
    doc_items = []
    for chunk in re.split(r"Unit \d+: ", source)[1:]:
        doc_items += [i.strip().rstrip(".") for i in chunk.split(";") if i.strip()]
    # Each unit's first item carries the unit title glued to its front, because
    # the document runs the heading straight into the prose. The titles are
    # taken from the page's own <h2>s rather than from asrb_map_data.py, so
    # this file still owes nothing to the generator -- and a wrong heading
    # fails here too.
    heads = [norm(h) for h in re.findall(r"<h2 id=\"unit-[^\"]*\">(.*?)</h2>", page)]
    titles = [h.split("—", 1)[1].strip() for h in heads if "—" in h]
    ok(len(titles) == 8, "expected 8 unit headings, found %d" % len(titles))
    for t in titles:
        for k, it in enumerate(doc_items):
            if it.startswith(t):
                doc_items[k] = it[len(t):].strip()
                break
        else:
            ok(False, "no syllabus item starts with the unit heading %r" % t)
    ok(len(page_items) == len(doc_items),
       "the page prints %d syllabus items; the document has %d"
       % (len(page_items), len(doc_items)))
    for k, (p, s) in enumerate(zip(page_items, doc_items)):
        ok(p == s, "item %d differs\n         page: %s\n         doc : %s"
           % (k, p[:80], s[:80]))
    print("syllabus items: %d on the page, %d in the document"
          % (len(page_items), len(doc_items)))

    # 2. destinations resolve; "not here" rows link nowhere
    for line, hrefs, grade in rows:
        if grade == "missing":
            ok(not hrefs, "a 'not here' row still links somewhere: %s" % line[:70])
            continue
        ok(bool(hrefs), "a graded row links nowhere: %s" % line[:70])
        for h in hrefs:
            full = os.path.normpath(os.path.join(PAPERS, "asrb-net", h))
            ok(os.path.exists(full), "dead link %s on row: %s" % (h, line[:60]))

    # 3. the committed text still matches the PDF
    if len(sys.argv) > 1:
        sys.path.insert(0, HERE)
        import pdftext
        fresh = re.sub(r"pg\.\s*\d+\s*", "", pdftext.flat_text(sys.argv[1]))
        ok(norm(fresh) == source,
           "asrb_syllabus.txt no longer matches what the PDF extracts to")
        print("re-extracted from the PDF and compared: %d chars" % len(norm(fresh)))
    else:
        print("no PDF given -- skipped the source-text comparison "
              "(pass the pdf path to run it)")

    grades = [g for _, _, g in rows]
    print("grades: %d deep, %d brief, %d not here"
          % (grades.count("deep"), grades.count("brief"), grades.count("missing")))
    print("%d checks, %d failures" % (checks, len(fails)))
    for f in fails:
        print("  FAIL " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
