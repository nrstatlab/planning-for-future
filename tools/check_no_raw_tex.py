#!/usr/bin/env python3
"""Fail if TeX reaches a string that is never typeset.

MathJax renders the body of a page. It does not render:

  * the <title>, which is the browser tab and the blue line in a Google result;
  * <meta name="description">, which is the grey line underneath it;
  * the "Topics Covered" chips once they are collected into topics.html;
  * the headings and descriptions copied into assets/search-index.json.

A reader who searched for "X-bar chart" was shown "\\bar{X} and R Charts" in the
dropdown, and Google was being offered "Construction of \\(\\bar{X}\\) and R
charts" as a page summary. detex() in build_site.py exists to prevent this; the
point of this file is that a symbol detex() has never met is REPORTED rather
than shipped, because a silent partial conversion is worse than a loud stop.

So the rule is deliberately blunt: no backslash command, and no "$$", in any of
those places. A lone "$" is allowed -- MongoDB's $lookup is not mathematics, and
treating it as such once cost two pages their description.

    python3 tools/check_no_raw_tex.py
"""
import html as html_mod
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "assets" / "search-index.json"

# A backslash followed by letters is a command; "$$" is a display delimiter.
TEX = re.compile(r"\\[A-Za-z]+|\$\$")

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')
OG_DESC_RE = re.compile(r'<meta property="og:description" content="([^"]*)"')
CHIP_RE = re.compile(r'<span class="chip">(.*?)</span>', re.S)

DT_RE = re.compile(r"<dt>(.*?)</dt>", re.S)
MATHJAX_RE = re.compile(r'<script[^>]+src="[^"]*mathjax[^"]*"', re.I)

SKIP_DIRS = {"archive", ".git"}
# Always checked: these four are never typeset, wherever they appear.
PAGE_FIELDS = (("title", TITLE_RE), ("description", DESC_RE),
               ("og:description", OG_DESC_RE), ("A-Z entry", DT_RE))


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        if SKIP_DIRS & set(p.parts):
            continue
        yield p


def main():
    bad = []

    for p in pages():
        text = p.read_text(errors="replace")
        fields = list(PAGE_FIELDS)
        # A chip is different: on a unit page it sits in the body, and if that
        # page loads MathJax the reader sees a typeset symbol, not a backslash.
        # What must be clean is the chip once it has been COLLECTED into
        # topics.html or the search index, and both of those are checked.
        if not MATHJAX_RE.search(text):
            fields.append(("chip", CHIP_RE))
        for label, rx in fields:
            for m in rx.finditer(text):
                value = html_mod.unescape(m.group(1))
                if TEX.search(value):
                    bad.append((f"{p.relative_to(ROOT)} [{label}]", value))

    if INDEX.exists():
        for rec in json.loads(INDEX.read_text()):
            for key in ("t", "h", "k", "d"):
                for value in (rec[key] if isinstance(rec[key], list)
                              else [rec[key]]):
                    if TEX.search(value):
                        bad.append((f"search-index [{key}] {rec['u']}", value))

    print(f"{len(list(pages()))} pages and the search index checked")
    if not bad:
        print("no raw TeX in any title, description, chip or search field")
        return 0

    print(f"\n{len(bad)} string(s) carry TeX that will never be typeset:")
    for where, value in bad[:25]:
        print(f"   {where}\n      {value[:140]}")
    if len(bad) > 25:
        print(f"   ... and {len(bad) - 25} more")
    print("\nAdd the symbol to detex() in data-science-major/tools/build_site.py,")
    print("then re-run the topic index, the search index and retitle_and_describe.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
