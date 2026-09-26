#!/usr/bin/env python3
"""Write sitemap.xml and robots.txt.

406 pages is more than a search engine will find by crawling links alone,
especially where a page is reached only from one deep index. The sitemap lists
them all, with each page's last commit date so a re-crawl knows what changed.
"""
import importlib.util
import pathlib
import subprocess
import sys
from datetime import date
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
# A redirect stub is an .html file like any other: without this every one
# of the 690 the restructure left behind would be listed, indexed and
# asserted on as though a reader could land on it.
from stubs import is_stub  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "_bs", ROOT / "tools" / "data-science" / "build_site.py")
_bs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bs)
SITE_BASE = _bs.SITE_BASE          # the one place the domain is written down

# 404.html is served for missing URLs, so listing it would invite a crawler to
# index the error page itself. The archive is a kept record, not study material.
SKIP_NAMES = {"404.html"}
SKIP_DIRS = {"archive"}

# robots.txt's Disallow lines, written down once. A URL both disallowed and
# listed in the sitemap sends a crawler two opposite instructions, so the
# sitemap skips every path here and main() refuses to write one that does not.
LAB_DEMOS = ("/data-science/labs/course-7-web/",)
# The old section roots hold nothing but the redirect stubs the 2026
# restructure left behind. Each carries robots noindex of its own, so this
# is belt and braces -- but it also stops a crawler spending its budget on
# 690 files that only forward it somewhere else.
MOVED = ("/statistics-major/", "/data-science-major/", "/statistics-papers/",
         "/exam-subjects/", "/ugc-net-statistics/", "/which-statistical-test.html")
DISALLOWED = LAB_DEMOS + MOVED


def disallowed(rel):
    """True if robots.txt tells a crawler to keep out of this site path."""
    return any(("/" + rel).startswith(d) for d in DISALLOWED)


def last_modified(path):
    """The file's last commit date, or today's if git does not know it."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, timeout=15).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return date.today().isoformat()


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts or SKIP_DIRS & set(p.parts) or p.name in SKIP_NAMES:
            continue
        if is_stub(p):
            continue
        if disallowed(p.relative_to(ROOT).as_posix()):
            continue
        yield p


def priority(rel):
    """The home page first, then section and topic indexes, then everything else."""
    if rel == "index.html":
        return "1.0"
    if rel in ("topics.html",) or rel.count("/") == 1 and rel.endswith("index.html"):
        return "0.8"
    return "0.6"


def main(apply=False):
    entries = []
    for p in pages():
        rel = p.relative_to(ROOT).as_posix()
        # a directory index is reachable at its folder URL, which is the tidier form
        loc = rel[:-len("index.html")] if rel.endswith("/index.html") else rel
        entries.append((loc, last_modified(p), priority(rel)))

    body = "\n".join(
        f"  <url>\n"
        f"    <loc>{escape(f'{SITE_BASE}/{loc}')}</loc>\n"
        f"    <lastmod>{mod}</lastmod>\n"
        f"    <priority>{pri}</priority>\n"
        f"  </url>"
        for loc, mod, pri in entries)

    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{body}\n</urlset>\n")

    robots = ("User-agent: *\n"
              "Allow: /\n\n"
              "# The lab source pages are teaching artefacts rather than study pages.\n"
              + "".join("Disallow: %s\n" % m for m in LAB_DEMOS)
              + "\n# Moved in the 2026 restructure. These paths hold redirect stubs only;\n"
              "# every page they point at is in the sitemap under its new URL.\n"
              + "".join("Disallow: %s\n" % m for m in MOVED)
              + f"\nSitemap: {SITE_BASE}/sitemap.xml\n")

    clash = [loc for loc, _, _ in entries if disallowed(loc)]
    if clash:
        sys.exit(f"FAIL: {len(clash)} sitemap url(s) are disallowed in robots.txt, "
                 f"e.g. {clash[0]}")

    print(f"{len(entries)} urls")
    if apply:
        (ROOT / "sitemap.xml").write_text(sitemap)
        (ROOT / "robots.txt").write_text(robots)
        print("wrote sitemap.xml and robots.txt")
    else:
        print("dry run -- pass --apply to write")
        for e in entries[:3]:
            print("   ", e)


if __name__ == "__main__":
    main(apply="--apply" in sys.argv)
