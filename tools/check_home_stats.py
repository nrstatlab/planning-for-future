#!/usr/bin/env python3
"""Check the home page's headline figures against the tree.

Those five tiles are hand-written, and the site keeps growing underneath them:
"Pages" said 405 when there were 593, because 187 pages were added after the
number was last touched. A figure on the front page that is quietly wrong is
worse than no figure, so this asserts each one.

Run it after anything that adds or removes pages. --fix rewrites the stale
numbers in place.
"""
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"

# 404.html is an error page, not study material, so it is not counted -- the
# same rule the sitemap uses.
NOT_A_PAGE = {"404.html"}


def _courses():
    spec = importlib.util.spec_from_file_location(
        "_bs", ROOT / "data-science-major" / "tools" / "build_site.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return len(m.COURSES)


def expected():
    pages = [p for p in ROOT.rglob("*.html")
             if ".git" not in p.parts and p.name not in NOT_A_PAGE]
    labs = [p for p in ROOT.rglob("*")
            if "labs" in p.parts and p.suffix in
            {".py", ".R", ".c", ".sql", ".js", ".sh"}]
    # the question set states its own size; taking it from there rather than
    # counting headings, which count datasets, not questions
    qsrc = (ROOT / "data-science-major" / "data" / "PRACTICE-QUESTIONS.md").read_text()
    qm = re.search(r"(\d+)\s+questions\s+over\s+\d+\s+datasets", qsrc)
    return {
        "Statistics subjects":  len([d for d in (ROOT / "statistics-major").iterdir()
                                     if d.is_dir() and d.name != "css"]),
        "Data Science courses": _courses(),
        "Pages":                len(pages),
        "Lab programs":         len(labs),
        "Practice questions":   int(qm.group(1)) if qm else None,
    }


TILE = re.compile(
    r'(<div class="stat"><b>)([\d,]+)(</b><span>)([^<]+)(</span></div>)')

# The "Start here" chips carry figures too, and they drift for the same reason
# the tiles do -- the A-Z index gained 11 topics the moment a page was added.
CHIP = re.compile(r'(<small>)([\d,]+)( (?:topics)</small>)')


def chip_expected():
    """Figures quoted in the chip row, taken from the artefact each describes."""
    idx = (ROOT / "topics.html")
    return {"topics": idx.read_text().count("<dt>") if idx.exists() else None}


def main(fix=False):
    want = expected()
    text = HOME.read_text()
    problems, out = [], text
    for m in TILE.finditer(text):
        label = m.group(4).strip()
        claimed = int(m.group(2).replace(",", ""))
        target = want.get(label)
        if target is None:
            continue
        if claimed != target:
            problems.append(f"{label}: page says {claimed:,}, tree has {target:,}")
            if fix:
                out = out.replace(m.group(0),
                                  f"{m.group(1)}{target:,}{m.group(3)}"
                                  f"{m.group(4)}{m.group(5)}")
    chips = chip_expected()
    for m in CHIP.finditer(text):
        what = m.group(3).strip().removesuffix("</small>")
        claimed = int(m.group(2).replace(",", ""))
        target = chips.get(what)
        if target is None or claimed == target:
            continue
        problems.append(f"{what} chip: page says {claimed:,}, "
                        f"the index has {target:,}")
        if fix:
            out = out.replace(m.group(0),
                              f"{m.group(1)}{target:,}{m.group(3)}")

    if fix and out != text:
        HOME.write_text(out)
        print(f"fixed {len(problems)} stale figure(s):")
    for p in problems:
        print("  ", p)
    if not problems:
        print(f"home page figures agree with the tree "
              f"({want['Pages']:,} pages, {want['Lab programs']} lab programs)")
        return 0
    return 0 if fix else 1


if __name__ == "__main__":
    sys.exit(main(fix="--fix" in sys.argv))
