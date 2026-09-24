#!/usr/bin/env python3
"""Check that the site is one course catalogue, with no programme or semester showing.

    python3 tools/check_catalogue.py      # exit 1 on any failure

Four assertions, each written against the finished pages rather than the
tools that wrote them, so a bug in a generator cannot hide behind the same
bug in its check:

  1. every course folder is in tools/course_catalogue.py exactly once;
  2. the Statistics and Data Science menus, as rendered on the home page, list
     the courses in catalogue order;
  3. no "Semester", "BSc" or "MSc" in the navigation, in any course page's
     <title> or breadcrumb, or in a hub's headings. Pages that reproduce an
     official syllabus are exempt, and are identified by the source note they
     carry, not by name;
  4. every course an exam's "Courses for this exam" block lists is linked from
     that exam's own pages outside the block, and every "Useful for" line on a
     course names exactly the exams whose blocks list it.
"""
import importlib.util
import pathlib
import posixpath
import re
import sys
from urllib.parse import unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("_cat", ROOT / "tools" / "course_catalogue.py")
cat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cat)

EXAMS = ["ugc-net", "csir-net", "asrb-net", "iss", "appsc"]
WORD = re.compile(r"\b(Semesters?|BSc|MSc|B\.Sc\.|M\.Sc\.)\b")
NAV = re.compile(r"<!-- site-nav.*?<!-- /site-nav -->", re.S)
HREF = re.compile(r'href="([^"#]+)')
fails = []


def fail(msg):
    fails.append(msg)


def is_stub(text):
    return 'http-equiv="refresh"' in text[:2048]


def pages(*dirs):
    for d in dirs:
        for p in sorted((ROOT / d).rglob("*.html")):
            t = p.read_text(errors="replace")
            if not is_stub(t):
                yield p, t


def resolve(page, url):
    here = page.parent.relative_to(ROOT).as_posix()
    return posixpath.normpath(posixpath.join(here, unquote(url)))


def course_key(target):
    parts = target.split("/")
    if len(parts) >= 3 and parts[0] in ("statistics", "data-science"):
        return parts[0] + "/" + parts[1]
    return None


# 1 -------------------------------------------------------------------------
for problem in cat.problems():
    fail("catalogue: " + problem)

# 2 -------------------------------------------------------------------------
home = (ROOT / "index.html").read_text()
nav = NAV.search(home)
if not nav:
    fail("menu: no navigation block on index.html")
else:
    shown = [h for h in HREF.findall(nav.group(0))]
    for section, want in (
            ("statistics", ["statistics/%s/index.html" % f for f, _, _ in cat.statistics_courses()]),
            ("data-science", ["data-science/%s/index.html" % s for s, _ in cat.data_science_courses()])):
        got = [h for h in shown if h.startswith(section + "/") and h.count("/") == 2
               and not h.startswith(section + "/index")]
        if got != want:
            first = next((i for i, (a, b) in enumerate(zip(got, want)) if a != b), min(len(got), len(want)))
            fail("menu: %s order differs from the catalogue at position %d (%s vs %s)"
                 % (section, first + 1, got[first] if first < len(got) else "-",
                    want[first] if first < len(want) else "-"))

# 3 -------------------------------------------------------------------------
m = WORD.search(nav.group(0)) if nav else None
if m:
    fail("wording: the navigation says %r" % m.group(0))
course_dirs = {"statistics/%s" % f for f, _, _ in cat.statistics_courses()} | \
              {"data-science/%s" % s for s, _ in cat.data_science_courses()}
for p, t in pages("statistics", "data-science"):
    rel = p.relative_to(ROOT).as_posix()
    if "/".join(rel.split("/")[:2]) not in course_dirs or 'class="source-note"' in t:
        continue
    title = re.search(r"<title>(.*?)</title>", t, re.S)
    crumb = re.search(r'<div class="crumbs">(.*?)</div>', t, re.S)
    for where, text in (("title", title.group(1) if title else ""),
                        ("breadcrumb", crumb.group(1) if crumb else "")):
        w = WORD.search(text)
        if w:
            fail("wording: %s %s says %r" % (rel, where, w.group(0)))
for hub in ("index.html", "statistics/index.html", "data-science/index.html", "exams/index.html"):
    t = NAV.sub("", (ROOT / hub).read_text())
    for h in re.findall(r"<h[1-4][^>]*>(.*?)</h[1-4]>", t, re.S):
        w = WORD.search(h)
        if w:
            fail("wording: %s heading %r says %r" % (hub, re.sub(r"\s+", " ", h)[:60], w.group(0)))

# 4 -------------------------------------------------------------------------
BLOCK = re.compile(r"<!-- exam-courses:.*?<!-- /exam-courses -->", re.S)
OWN = re.compile(r"<!-- (site-nav|site-foot|exam-courses|useful-for|next-course).*?<!-- /\1 -->", re.S)
listed = {}
for exam in EXAMS:
    hub = ROOT / "exams" / exam / "index.html"
    t = hub.read_text()
    b = BLOCK.search(t)
    if not b:
        fail("exams: %s has no Courses for this exam block" % exam)
        continue
    listed[exam] = {course_key(resolve(hub, u)) for u in HREF.findall(b.group(0))} - {None}
    evidence = set()
    for p, text in pages("exams/" + exam):
        for u in HREF.findall(OWN.sub("", text)):
            if not re.match(r"^(mailto:|https?:|//|/)", u):
                k = course_key(resolve(p, u))
                if k:
                    evidence.add(k)
    for k in sorted(listed[exam] - evidence):
        fail("exams: %s lists %s, but none of its pages links to it" % (exam, k))
    for k in sorted((evidence & course_dirs) - listed[exam]):
        fail("exams: %s links to %s but does not list it" % (exam, k))
USEFUL = re.compile(r"<!-- useful-for:.*?<!-- /useful-for -->", re.S)
for k in sorted(course_dirs):
    ix = ROOT / k / "index.html"
    u = USEFUL.search(ix.read_text())
    says = set(re.findall(r"exams/([a-z-]+)/index\.html", u.group(0))) if u else set()
    want = {e for e, ks in listed.items() if k in ks}
    if says != want:
        fail("useful-for: %s says %s, the exam lists say %s" % (k, sorted(says), sorted(want)))

n = len(cat.statistics_courses()) + len(cat.data_science_courses())
if fails:
    for f in fails:
        print("FAIL", f)
    print("%d failure(s)" % len(fails))
    sys.exit(1)
print("catalogue, menu, wording and exam links agree (%d courses, %d exams)" % (n, len(EXAMS)))
