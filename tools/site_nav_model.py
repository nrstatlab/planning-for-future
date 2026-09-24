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

SEMESTER = {"sem-1": "Semester I", "sem-2": "Semester II", "sem-3": "Semester III",
            "sem-4": "Semester IV", "sem-5": "Semester V", "sem-6": "Semester VI"}


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


def _hubs(section):
    """(folder, label, href) for every subfolder of `section` that has an index."""
    out = []
    for d in sorted((ROOT / section).iterdir()):
        ix = d / "index.html"
        if d.is_dir() and ix.exists():
            out.append((d.name, label_of(ix, drop_artefact=section == "exams"),
                        f"{section}/{d.name}/index.html"))
    return out


def _disambiguate(rows):
    """Two folders may carry the same <title>; say which is which from the path.

    statistics/bsc/computational-statistics-and-r-programming and
    ...-2023 are two syllabus revisions of one subject and their titles are
    identical. Silently showing the reader the same label twice would be worse
    than either fixing the titles or saying so, and this is not the place to
    edit content -- so the folder's own distinguishing tail is appended.
    """
    seen = {}
    for name, lab, href in rows:
        seen.setdefault(lab, []).append(name)
    out = []
    for name, lab, href in rows:
        clash = seen[lab]
        if len(clash) > 1:
            year = re.search(r"-(\d{4})$", name)
            dated = [n for n in clash if re.search(r"-\d{4}$", n)]
            if year:
                lab = f"{lab} ({year.group(1)} syllabus)"
            elif len(dated) != len(clash) - 1:
                # Nothing in the folder names says which is which, so the whole
                # name goes in rather than a guess.
                lab = f"{lab} ({name})"
            # else: this is the one undated member of the group -- the others
            # carry their year, so it is already distinguished by their labels.
        out.append((name, lab, href))
    return out


def courses_by_semester():
    """The 19 Data Science courses, in syllabus order, grouped by semester."""
    spec = importlib.util.spec_from_file_location(
        "_bs", ROOT / "tools" / "data-science" / "build_site.py")
    bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)
    groups = {}
    for c in bs.COURSES:
        sem = SEMESTER[pathlib.PurePosixPath(c["src"]).parts[1]]
        ix = ROOT / "data-science" / c["slug"] / "index.html"
        if ix.exists():
            groups.setdefault(sem, []).append(
                (label_of(ix), f"data-science/{c['slug']}/index.html"))
    return [(SEMESTER[k], groups[SEMESTER[k]])
            for k in sorted(SEMESTER) if SEMESTER[k] in groups]


def ugc_net_pages():
    """UGC NET's own 13 pages, which is why its sticky 13-link row can go."""
    d = ROOT / "exams" / "ugc-net"
    rows = []
    for name in sorted(p.name for p in d.glob("unit*.html")):
        n = int(re.search(r"\d+", name).group())
        rows.append((n, name))
    out = [(f"Unit {n}", f"exams/ugc-net/{name}") for n, name in sorted(rows)]
    for name, lab in (("mcqs.html", "Model MCQs"),
                      ("solved-2026.html", "Solved 2026 paper")):
        if (d / name).exists():
            out.append((lab, f"exams/ugc-net/{name}"))
    return out


def menu():
    """[(label, href or None, [(group label or None, [(label, href)])])]"""
    bsc = _disambiguate(_hubs("statistics/bsc"))
    msc = _disambiguate(_hubs("statistics/msc"))
    exams = _disambiguate(_hubs("exams"))
    subj = _disambiguate(_hubs("subjects"))
    return [
        ("Statistics", "statistics/index.html", [
            ("BSc", [(l, h) for _, l, h in bsc]),
            ("MSc", [(l, h) for _, l, h in msc]),
        ]),
        ("Data Science", "data-science/index.html",
         [(sem, rows) for sem, rows in courses_by_semester()]),
        ("Examinations", "exams/index.html", [
            (None, [(l, h) for _, l, h in exams]),
            ("UGC NET, page by page", ugc_net_pages()),
        ]),
        # The hub exists; the first version of this menu forgot it, so
        # Subjects was the one menu with no "All of" row.
        ("Subjects", "subjects/index.html", [
            (None, [(l, h) for _, l, h in subj]),
        ]),
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
