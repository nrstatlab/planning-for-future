#!/usr/bin/env python3
"""Fail unless every practical on every practical page has its paper's structure.

The site sets out its practicals in one of two ways, the way a practical record is written:

  statistical paper   1. Problem   2. Aim  3. Formula  4. Calculation  5. Result
  programming paper   1. Question  2. Aim  3. Steps    4. Programme    5. Execution and Results

A practical is an <h2> section that has any of these headings as an <h3>. Each one must
have exactly the five <h3> headings of its paper's structure, numbered and in order, and
no other <h3>: anything more (a check in R, a working table, a note) goes in a box inside
one of the five. Every live page must be in TEMPLATE, so a new course has to choose; each
must have at least one practical; and "Procedure", the old third heading, must be gone,
from the headings and from the page's own account of its structure.

The Data Science lab pages (data-science/<course>/lab.html) are all programming papers. Those
not yet moved to the structure are in DS_PENDING: skipped, and reported, until they are.

    python3 tools/check_practicals.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

STRUCTURE = {
    "statistical": ["Problem", "Aim", "Formula", "Calculation", "Result"],
    "programming": ["Question", "Aim", "Steps", "Programme", "Execution and Results"],
}

S, P = "statistical", "programming"
TEMPLATE = {
    "actuarial-statistics": S,
    "advanced-actuarial-statistics": S,
    "applied-statistics": S,
    "applied-statistics-ii": S,
    "computational-statistics-and-r-programming": P,
    "computational-statistics-and-r-programming-2023": P,
    "data-handling-using-r": P,
    "data-science-using-python": P,
    "descriptive-statistics": S,
    "design-and-analysis-of-experiments": S,
    "design-and-analysis-of-experiments-advanced": S,
    "distribution-theory": S,
    "econometrics": S,
    "estimation-theory": S,
    "inferential-statistics": S,
    "linear-algebra-and-linear-models": S,
    "multivariate-analysis": S,
    "operations-research": S,
    "optimization-techniques": S,
    "sampling-techniques": S,
    "sampling-theory": S,
    "statistical-analysis-of-clinical-trials": S,
    "statistical-analysis-using-spss": P,
    "statistical-data-analysis-using-ms-excel": S,
    "statistical-methods": S,
    "statistical-methods-using-python": P,
    "statistical-quality-control": S,
    "statistical-techniques-for-research-methodology": S,
    "theoretical-continuous-distributions": S,
    "theoretical-discrete-distributions": S,
    "theory-of-probability": S,
}

DS_PENDING = {
    "artificial-intelligence", "big-data", "business-intelligence", "cloud-computing",
    "data-mining", "deep-learning",
    "document-database", "machine-learning", "mlops", "nlp",
    "python-data-analysis", "time-series",
    "web-technologies",
}

NAMES = {n for names in STRUCTURE.values() for n in names} - {"Aim"}
H2 = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.S)
H3 = re.compile(r"<h3\b[^>]*>(.*?)</h3>", re.S)
TAG = re.compile(r"<[^>]+>")
NUMBERED = re.compile(r"^(\d+)\.\s+(.*)$")


def text(fragment):
    return re.sub(r"\s+", " ", TAG.sub("", fragment)).strip()


def content(page):
    """The page's own column, without the site chrome, scripts and comments."""
    s = page[page.find('<div class="wrapper">'):]
    s = s.split("<!-- site-foot", 1)[0]
    return re.sub(r"<script\b.*?</script>|<!--.*?-->", "", s, flags=re.S)


def check_page(name, page, kind):
    bad = []
    body = content(page)
    want = STRUCTURE[kind]
    parts = H2.split(body)
    practicals = 0
    for title, section in zip(parts[1::2], parts[2::2]):
        heads = [text(h) for h in H3.findall(section)]
        bare = [NUMBERED.sub(r"\2", h) for h in heads]
        if not (set(bare) & NAMES or "Procedure" in bare):
            continue
        practicals += 1
        expect = [f"{i}. {h}" for i, h in enumerate(want, 1)]
        if heads != expect:
            bad.append(f"{name}: \"{text(title)[:60]}\" has {heads}; a {kind} practical has {expect}")
    if practicals == 0:
        bad.append(f"{name}: no practical with the {kind} structure was found")
    if re.search(r"<h3\b[^>]*>\s*\d+\.\s*Procedure\s*</h3>", body):
        bad.append(f"{name}: a \"Procedure\" heading is left; it is now \"3. {want[2]}\"")
    # The page's own account of its structure (the intro, the record list, the description)
    # must name the same sections: "Procedure" is no longer one of them.
    head = page[:page.find("</head>")]
    told = re.findall(r'<meta name="description" content="[^"]*"', head) + [body]
    if any(re.search(r"\b3\.\s+Procedure\b|<strong>(?:3\.\s+)?Procedure</strong>", t) for t in told):
        bad.append(f"{name}: the page still describes a \"Procedure\" section; the third is \"{want[2]}\"")
    return practicals, bad


def main():
    bad, checked, total = [], [], 0
    pages = {}
    for p in sorted((ROOT / "statistics").glob("*/practical.html")):
        page = p.read_text()
        if 'http-equiv="refresh"' in page:
            continue
        pages[p.parent.name] = page
    for name in sorted(set(pages) - set(TEMPLATE)):
        bad.append(f"{name}: not in TEMPLATE; choose \"statistical\" or \"programming\" for it")
    for name in sorted(set(TEMPLATE) - set(pages)):
        bad.append(f"{name}: in TEMPLATE, but statistics/{name}/practical.html is not a live page")
    for name in sorted(set(pages) & set(TEMPLATE)):
        n, b = check_page(name, pages[name], TEMPLATE[name])
        total += n
        checked.append(name)
        bad += b
    labs = sorted(p.parent.name for p in (ROOT / "data-science").glob("*/lab.html"))
    for name in sorted(set(DS_PENDING) - set(labs)):
        bad.append(f"data-science/{name}: in DS_PENDING, but data-science/{name}/lab.html does not exist")
    ds = 0
    for name in labs:
        if name in DS_PENDING:
            continue
        n, b = check_page(f"data-science/{name}", (ROOT / "data-science" / name / "lab.html").read_text(), P)
        total += n
        ds += 1
        bad += b
    waiting = len(set(labs) & DS_PENDING)
    print(f"{len(checked)} practical pages and {ds} lab pages checked, {total} practicals in their paper's "
          "structure" + (f"; {waiting} lab pages not yet moved to it" if waiting else ""))
    if bad:
        print(f"FAIL: {len(bad)} problem(s)")
        for b in bad[:30]:
            print("   ", b)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
