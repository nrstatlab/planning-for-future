# -*- coding: utf-8 -*-
"""Extract the UGC NET Statistics (code 107) syllabus into ugc_syllabus.txt.

    python3 pdftext_ugc.py [PDF]      # default: docs/sources/ugc-net-statistics-code-107.pdf

The document is the UGC NET Bureau's "NET Syllabus, Subject: Statistics,
Code 107", five pages printed from Word. Its text layer is clean except in
five places, where the author used Word's equation editor: those glyphs are
Cambria Math with no text mapping, so any extractor reads them as blanks.
They were read off the rendered page instead (PyMuPDF, 4-5x, in this
repository's history) and are filled in here, each by the exact blank it
replaces, so a change to the document fails loudly rather than drifting:

    Unit II    "L′ Hospital’s rule"            the prime is an equation object
    Unit III   "Factorial experiments- 2², 2³"  two superscripts
    Unit VI    "R², adjusted R²"               two superscripts
    Unit VIII  "generalized T² statistic"      Hotelling's T-squared
    Unit X     "Latex and other word processing software"   set in math italic

recheck_ugc.py names the same five, independently, and proves every other
character of every printed line against the PDF.

Needs PyMuPDF (import fitz), which this container has; tools/exams/pdftext.py
is the fallback for PDFs it cannot open.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PDF = os.path.join(ROOT, "docs", "sources", "ugc-net-statistics-code-107.pdf")
OUT = os.path.join(HERE, "ugc_syllabus.txt")

# (the text as extracted, the text as printed) -- each must occur exactly once.
EQUATIONS = [
    ("Taylor’s theorem, L Hospital’s rule", "Taylor’s theorem, L′ Hospital’s rule"),
    ("Factorial experiments- , confounding", "Factorial experiments- 2², 2³, confounding"),
    ("Analysis of variance for linear model, , adjusted , tests",
     "Analysis of variance for linear model, R², adjusted R², tests"),
    ("generalized statistic,", "generalized T² statistic,"),
    ("scripts and functions. and other word", "scripts and functions. Latex and other word"),
]


def raw_text(pdf=PDF):
    """The document's text, whitespace collapsed, from Unit I to the end."""
    import fitz                                  # PyMuPDF
    doc = fitz.open(pdf)
    text = " ".join(page.get_text() for page in doc)
    text = re.sub(r"\s+", " ", text).strip()
    # Page 1 lists the unit titles; the syllabus proper starts on page 2.
    start = text.index("Unit I: Probability and Distributions Basic")
    return text[start:]


def syllabus_text(pdf=PDF):
    text = raw_text(pdf)
    for extracted, printed in EQUATIONS:
        n = text.count(extracted)
        if n != 1:
            raise SystemExit("expected one %r in the PDF text, found %d" % (extracted, n))
        text = text.replace(extracted, printed)
    return text


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else PDF
    text = syllabus_text(pdf)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print("wrote %s (%d characters)" % (os.path.relpath(OUT, ROOT), len(text)))


if __name__ == "__main__":
    main()
