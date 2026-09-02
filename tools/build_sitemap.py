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

_spec = importlib.util.spec_from_file_location(
    "_bs", ROOT / "data-science-major" / "tools" / "build_site.py")
_bs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bs)
SITE_BASE = _bs.SITE_BASE          # the one place the domain is written down

# 404.html is served for missing URLs, so listing it would invite a crawler to
# index the error page itself. The archive is a kept record, not study material.
SKIP_NAMES = {"404.html"}
SKIP_DIRS = {"archive"}


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
              "Disallow: /data-science-major/labs/course-7-web/\n\n"
              f"Sitemap: {SITE_BASE}/sitemap.xml\n")

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
