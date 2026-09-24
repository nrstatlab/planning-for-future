#!/usr/bin/env python3
"""What goes in the site navigation, read from the tree rather than written out.

Kept apart from add_site_nav.py so the menu can be inspected on its own:

    python3 tools/site_nav_model.py        # print the whole menu, with its targets

Every label is taken from the destination page's own <title>, the same rule the
syllabus maps use for their link text: a page that is retitled cannot end up
with a stale label in the menu, and a wrong label is visibly wrong rather than
plausibly wrong.
"""
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TITLE = re.compile(r"<title>(.*?)</title>", re.S)
# Titles are written "Subject — what it is"; the menu wants the subject. Both
# the character and the entity appear, because one half of the site is
# hand-written and the other is generated.
TAIL = re.compile(r"\s*(?:—|&mdash;|&ndash;|–)\s")
# "ISS Syllabus Map" and "UGC NET Statistics Study Material" name the artefact
# rather than the exam; in a menu of exams that is noise on every row.
DROP = re.compile(r"\s*(?:Syllabus Map|Study Material|Complete Study Material)\s*$")


def amp(s):
    """Escape a bare & that a page title carries unescaped, as labels.py does."""
    return re.sub(r"&(?!(?:[A-Za-z][A-Za-z0-9]{1,8}|#[0-9]{1,5}|#x[0-9A-Fa-f]{1,5});)",
                  "&amp;", s)


def label_of(index_path, drop_artefact=False):
    """The menu label for one hub page, from its own <title>."""
    m = TITLE.search(index_path.read_text(errors="replace"))
    if not m:
        return index_path.parent.name
    t = re.sub(r"\s+", " ", m.group(1)).strip()
    t = TAIL.split(t)[0].strip()
    if drop_artefact:
        t = DROP.sub("", t).strip()
    return amp(t)


# The paper codes the postgraduate courses carry, "(STS-203)", belong to the
# scheme they were written for; a visitor choosing a course has no use for them.
CODE = re.compile(r"\s*\(STS-\d+\)")

# The two exam groups. The NET exams are the three national eligibility
# tests; ISS and APPSC are recruitment examinations and are listed apart.
NET = ["ugc-net", "csir-net", "asrb-net"]
OTHER = ["iss", "appsc"]


def statistics_rows():
    """[(group, [(label, href)])] for the Statistics menu, in catalogue order."""
    cat = _catalogue()
    rows = []
    for folder, level, group in cat.statistics_courses():
        ix = ROOT / "statistics" / folder / "index.html"
        rows.append((folder, CODE.sub("", label_of(ix)), level, group,
                     f"statistics/{folder}/index.html"))
    # Two courses may carry one name: the Foundation and Advanced courses of
    # one topic, or two revisions of one course (whose folder carries a year).
    names = {}
    for folder, lab, level, group, href in rows:
        names.setdefault(lab, []).append((folder, level))
    out = {}
    for folder, lab, level, group, href in rows:
        clash = names[lab]
        if len(clash) > 1:
            year = re.search(r"-(\d{4})$", folder)
            if year:
                lab = f"{lab} ({year.group(1)} syllabus)"
            elif len({lvl for _, lvl in clash}) == len(clash):
                lab = f"{lab} ({level})"
        out.setdefault(group, []).append((lab, href))
    return [(g, out[g]) for g, _ in cat.STATISTICS if g in out]


def data_science_rows():
    """[(group, [(label, href)])] for the Data Science menu, in catalogue order."""
    cat = _catalogue()
    out = {}
    for slug, group in cat.data_science_courses():
        ix = ROOT / "data-science" / slug / "index.html"
        out.setdefault(group, []).append((label_of(ix), f"data-science/{slug}/index.html"))
    return [(g, out[g]) for g, _ in cat.DATA_SCIENCE if g in out]


def exam_rows(names):
    rows = []
    for name in names:
        ix = ROOT / "exams" / name / "index.html"
        if ix.exists():
            rows.append((label_of(ix, drop_artefact=True), f"exams/{name}/index.html"))
    return rows


def _catalogue():
    spec = importlib.util.spec_from_file_location(
        "_cat", ROOT / "tools" / "course_catalogue.py")
    cat = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cat)
    return cat


def menu():
    """[(label, href or None, [(group label or None, [(label, href)])])]

    Examinations first: the site is for exam preparation, and the courses
    are what a visitor studies for an exam."""
    return [
        ("Examinations", "exams/index.html", [
            ("NET exams", exam_rows(NET)),
            ("Other exams", exam_rows(OTHER)),
            # No per-unit rows for UGC NET: its hub lists the ten units and
            # each unit page links the next, as every other exam's pages do.
        ]),
        ("Statistics", "statistics/index.html", statistics_rows()),
        ("Data Science", "data-science/index.html", data_science_rows()),
    ]


PLAIN = [("Topics A&ndash;Z", "topics.html"),
         ("Which test?", "guides/which-test.html")]


def main():
    n = 0
    for top, hub, groups in menu():
        print("%s%s" % (top, "   -> " + hub if hub else ""))
        n += bool(hub)
        for g, rows in groups:
            if g:
                print("   [%s]" % g)
            for lab, href in rows:
                print("      %-52s %s" % (lab, href))
                n += 1
    for lab, href in PLAIN:
        print("%s   -> %s" % (lab, href))
        n += 1
    print("\n%d link(s) in the menu" % n)
    missing = [h for _, hub, gs in menu() for h in
               ([hub] if hub else []) + [x[1] for _, rows in gs for x in rows]]
    missing += [h for _, h in PLAIN]
    gone = [h for h in missing if not (ROOT / h).exists()]
    print("%d target(s) do not exist" % len(gone))
    for g in gone:
        print("   ", g)
    return 1 if gone else 0


if __name__ == "__main__":
    sys.exit(main())
