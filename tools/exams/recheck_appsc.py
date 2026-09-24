# -*- coding: utf-8 -*-
"""Check the APPSC pages against the notifications they claim to reproduce.

Written after the pages, deliberately not importing appsc_map_data: it walks
the finished HTML, pulls every syllabus line out of the first column of every
graded table, and looks for that line's wording in the text extracted afresh
from the PDF the page names as its source.  A line that cannot be found in its
own source is a fabrication, and fails.

Matching is on content words, not on punctuation: the notifications break words
across lines and pad them with the double spaces that justified PDF text leaves
behind, and the pages tidy that up, so comparing raw strings would fail on
whitespace while missing real invention.  Every content word of the printed
line must appear in the source, in order.
"""
import html as _html
import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pdftext_appsc as pdftext

# tools/exams/ -> repository root is two levels up; the pages live in exams/.
PAGES = os.path.join(os.path.dirname(os.path.dirname(HERE)), "exams", "appsc") + os.sep

# The two APPSC notifications are third-party PDFs and are not in this
# repository, so their location is given on the command line:
#
#     python3 recheck_appsc.py AD.pdf ASO.pdf
#
# Without them the page-against-page checks still run and the
# page-against-source checks are skipped, and the script says which.
PDFS = {}
if len(sys.argv) == 3:
    PDFS = {"AD": sys.argv[1], "ASO": sys.argv[2]}

# a line printed on a page may legitimately reword the notification's
# punctuation and connectives; these are the words we do not insist on
SKIP = set("""a an and or the of to in on for with by as at is are be its their
into from that this these those only basic all any each such other others
""".split())

# Two words are misspelt in both notifications.  The pages print the correct
# spelling -- a study page that reproduced them would look like its own typo,
# and "Bowl's" would send a reader searching for the wrong statistician -- so
# the corrections are declared here instead of being made silently, and this
# recheck prints them on every run.
SOURCE_TYPOS = {
    "variation": "veriation",   # "Coefficient of Veriation", item 8
    "bowley's": "bowl's",       # "Karl Pearson and Bowl's measures of skewness"
}


def words(s):
    s = _html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("—", " ").replace("–", " ").replace("−", " ")
    s = re.sub(r"[^A-Za-z0-9']+", " ", s).lower()
    return [SOURCE_TYPOS.get(w, w) for w in s.split()
            if w not in SKIP and len(w) > 1]


def source_words(path):
    return words(" ".join(pdftext.pages(path)))


def first_column(page_html):
    """Every <td> that opens a row of a graded table."""
    out = []
    for tr in re.findall(r"<tr>(.*?)</tr>", page_html, re.S):
        tds = re.findall(r"<td>(.*?)</td>", tr, re.S)
        if len(tds) == 3 and ('class="g ' in tr):
            out.append(tds[0])
    return out


def contains_in_order(hay, needle):
    """Is every word of needle present in hay, in order?"""
    i = 0
    for w in needle:
        try:
            i = hay.index(w, i) + 1
        except ValueError:
            return False
    return True


def main():
    src = {k: source_words(p) for k, p in PDFS.items()}
    if src:
        print("source words:", {k: len(v) for k, v in src.items()})
    else:
        print("no notification PDFs given -- the page-against-source checks "
              "are SKIPPED. Pass the two PDF paths to run them:")
        print("    python3 recheck_appsc.py AD.pdf ASO.pdf")
    for good, bad in sorted(SOURCE_TYPOS.items()):
        print("  declared source misspelling: the notifications print %r; "
              "the pages print %r" % (bad, good))

    checked = fail = skipped = 0
    for name, key in (("assistant-director.html", "AD"),
                      ("assistant-statistical-officer.html", "ASO"),
                      ("index.html", None)):
        page = open(PAGES + name, encoding="utf-8").read()
        lines = first_column(page)
        # the index's comparison table is not a syllabus table
        if name == "index.html":
            lines = [l for l in lines if not re.match(r"^\d+\. ", _html.unescape(l).strip())]
        for raw in lines:
            w = words(raw)
            if not w:
                continue
            if not src:
                skipped += 1        # counted as skipped, never as checked
                continue
            checked += 1
            keys = [key] if key else list(src)
            if not any(contains_in_order(src[k], w) for k in keys):
                fail += 1
                print("  NOT IN SOURCE (%s): %s" % (name, _html.unescape(raw)[:110]))
        print("%-38s %3d line(s) checked" % (name, len(lines)))

    # the quoted passages must also be present verbatim in their own source
    QUOTES = [
        ("assistant-director.html", "AD",
         "for each wrong answer will be penalized with 1/3rd of the marks prescribed"),
        ("assistant-statistical-officer.html", "ASO",
         "for each wrong answer will be penalized with 1/3rd of the marks prescribed"),
        ("assistant-director.html", "AD",
         "Must possess Post Graduate Degree in one of the Subjects of Mathematics"),
        ("assistant-statistical-officer.html", "ASO",
         "Bachelor's Degree with Statistics as one of the main subjects"),
        ("index.html", None,
         "subject to variation upon confirmation being received from the concerned Department"),
    ]
    for name, key, q in QUOTES:
        page = open(PAGES + name, encoding="utf-8").read()
        pw = words(q)
        if not src:
            skipped += 1
            continue
        checked += 1
        on_page = contains_in_order(words(page), pw)
        keys = [k for k in ([key] if key else list(src)) if k in src]
        in_src = any(contains_in_order(src[k], pw) for k in keys)
        if not (on_page and in_src):
            fail += 1
            print("  QUOTE FAILED (%s, on page %s, in source %s): %s"
                  % (name, on_page, in_src, q[:70]))

    # the scheme figures the pages print must be the ones the notifications give
    NUMS = [("assistant-director.html", ["150", "450"]),
            ("assistant-statistical-officer.html", ["150", "300"])]
    for name, ns in NUMS:
        page = open(PAGES + name, encoding="utf-8").read()
        for n in ns:
            checked += 1
            if n not in page:
                fail += 1
                print("  MISSING FIGURE %s on %s" % (n, name))

    tail = ("" if not skipped else
            "  [%d source comparison(s) SKIPPED -- no notification PDFs given]"
            % skipped)
    print("\n%d check(s), %d failure(s)%s" % (checked, fail, tail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
