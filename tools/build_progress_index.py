#!/usr/bin/env python3
"""Which pages count as units, for the reader's progress (assets/progress.js).

    python3 tools/build_progress_index.py            # dry run: print the counts
    python3 tools/build_progress_index.py --apply    # write assets/progress-index.json

Progress is kept in the reader's own browser and never leaves it. What the
browser needs from the site is only this: for each course, the pages a reader
can mark done, so a course home can say "3 of 5 done" and a hub card "3/5".
The list is counted from the folders, by the same rule the hub cards use for
"5 units + practical" (tools/build_course_hubs.py), and the course order is the
catalogue's (tools/course_catalogue.py) -- so the two can never disagree.

A page id is its path from the site root, e.g. statistics/sampling-theory/
unit2.html: stable, readable, and the obvious key if progress is ever synced to
an account.

role_of() is imported by tools/add_site_nav.py, which tells each page what
progress.js should do on it: "unit" pages get the mark-done toggle, "summary"
pages (hubs, course homes, exam hubs, home, About) show totals, and every other
page does nothing and fetches nothing.
"""
import argparse
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "progress-index.json"

spec = importlib.util.spec_from_file_location("_cat", ROOT / "tools" / "course_catalogue.py")
cat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cat)

# UGC NET is studied like a course: ten units, then the question bank and the
# solved paper.
UGC = ("exams/ugc-net", ["unit%d.html" % n for n in range(1, 11)] + ["mcqs.html", "solved-2026.html"])
UNIT = re.compile(r"unit\d+\.html")
EXTRA = ("practical.html", "lab.html")


def _is_page(p):
    return p.exists() and 'http-equiv="refresh"' not in p.read_text(errors="replace")[:2048]


def units_of(folder):
    """The markable pages of one course folder, units first, in unit order."""
    units = sorted((p.name for p in folder.glob("unit*.html")
                    if UNIT.fullmatch(p.name) and _is_page(p)),
                   key=lambda n: int(re.search(r"\d+", n).group()))
    return units + [n for n in EXTRA if _is_page(folder / n)]


def courses():
    """{course dir: [unit file names]} in catalogue order, UGC NET last."""
    out = {}
    for f, _, _ in cat.statistics_courses():
        out["statistics/" + f] = units_of(ROOT / "statistics" / f)
    for s, _ in cat.data_science_courses():
        out["data-science/" + s] = units_of(ROOT / "data-science" / s)
    ugc_dir, ugc_units = UGC
    out[ugc_dir] = [u for u in ugc_units if _is_page(ROOT / ugc_dir / u)]
    return out


_COURSES = None


def role_of(page_rel):
    """'unit', 'summary' or '' for a root-relative page path."""
    global _COURSES
    if _COURSES is None:
        _COURSES = courses()
    d, _, name = page_rel.rpartition("/")
    if name in _COURSES.get(d, ()):
        return "unit"
    if page_rel in ("index.html", "about.html", "statistics/index.html",
                    "data-science/index.html", "exams/index.html"):
        return "summary"
    if name == "index.html" and (d in _COURSES or d.startswith("exams/")):
        return "summary"
    return ""


def main(apply_changes):
    data = {"v": 1, "courses": courses()}
    total = sum(len(v) for v in data["courses"].values())
    empty = [k for k, v in data["courses"].items() if not v]
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=False) + "\n"
    print("%d courses, %d markable pages, %d bytes%s"
          % (len(data["courses"]), total, len(text.encode()),
             "; EMPTY: " + ", ".join(empty) if empty else ""))
    if empty:
        return 1
    if apply_changes and (not OUT.exists() or OUT.read_text() != text):
        OUT.write_text(text)
        print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    sys.exit(main(ap.parse_args().apply))
