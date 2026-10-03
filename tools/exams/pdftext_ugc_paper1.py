# -*- coding: utf-8 -*-
"""Extract the UGC NET Paper I syllabus into ugc_paper1_syllabus.txt.

    python3 pdftext_ugc_paper1.py [PDF]   # default: docs/sources/ugc-net-paper-1-general.pdf

The document is the UGC NET Bureau's "Syllabus, Subject: General Paper on
Teaching & Research Aptitude, Code No. : 00, Paper-I", four pages printed from
Word. Its text layer is clean: no equation objects, unlike the Statistics
syllabus (pdftext_ugc.py). Three things are done to it, and nothing else:

1. each page's printed page number (a lone 1, 2, 3, 4 at its top) is dropped;
2. the bullet glyph U+F0B7 (Symbol font, no text meaning) is dropped and the
   whitespace collapsed;
3. each unit heading, printed "Unit-IV" over "Communication", is written
   "Unit IV: Communication " -- the form the Statistics file uses, so
   ugc_map.syllabus_units() can split both the same way.

The file holds three lines, each with its label:

    SYLLABUS: Unit I: Teaching Aptitude ... Policies, Governance, and Administration.
    INTRO: The main objective is ... the quality of life.
    NOTE: (i) Five questions each carrying 2 marks ... for visually impaired candidates.

recheck_ugc_paper1.py extracts the PDF again, independently, and proves the
map page against it. Spellings are the document's own ("Anupalabddhi").

Needs PyMuPDF.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PDF = os.path.join(ROOT, "docs", "sources", "ugc-net-paper-1-general.pdf")
OUT = os.path.join(HERE, "ugc_paper1_syllabus.txt")

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
TITLES = ["Teaching Aptitude", "Research Aptitude", "Comprehension", "Communication",
          "Mathematical Reasoning and Aptitude", "Logical Reasoning", "Data Interpretation",
          "Information and Communication Technology (ICT)", "People, Development and Environment",
          "Higher Education System"]


def raw_text(pdf=PDF):
    import pymupdf
    pages = []
    for n, page in enumerate(pymupdf.open(pdf), 1):
        t = page.get_text()
        m = re.match(r"\s*%d\s" % n, t)
        if not m:
            raise SystemExit("page %d does not start with its page number" % n)
        pages.append(t[m.end():])
    text = " ".join(pages).replace("", " ")
    return re.sub(r"\s+", " ", text).strip()


def parts(pdf=PDF):
    text = raw_text(pdf)
    a = text.index("The main objective")
    b = text.index("The details of syllabi are as follows:")
    intro = text[a:b].strip()
    note_at = text.index("NOTE:")
    body, note = text[b + len("The details of syllabi are as follows:"):note_at].strip(), text[note_at + 5:].strip()
    for roman, title in zip(ROMAN, TITLES):
        head = "Unit-%s %s " % (roman, title)
        if body.count(head) != 1:
            raise SystemExit("expected one %r in the PDF text, found %d" % (head, body.count(head)))
        body = body.replace(head, "Unit %s: %s " % (roman, title))
    if not body.startswith("Unit I: Teaching Aptitude "):
        raise SystemExit("the syllabus does not start at Unit I")
    return body, intro, note


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else PDF
    body, intro, note = parts(pdf)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("SYLLABUS: %s\nINTRO: %s\nNOTE: %s\n" % (body, intro, note))
    print("wrote %s (%d characters of syllabus)" % (os.path.relpath(OUT, ROOT), len(body)))


if __name__ == "__main__":
    main()
