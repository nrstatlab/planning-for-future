#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print the content of a page as plain text for reading, formulas kept as TeX.

    python3 tools/audit/extract.py statistics/econometrics/unit1.html [start [length]]

Headings are marked with #, ## and ### and their ids, so a finding can be
tied to its section. The site chrome, scripts and styles are left out.
"""
import html
import re
import sys


def text(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    t = re.sub(r"<!-- site-nav.*?<!-- /site-nav -->", "", t, flags=re.S)
    t = re.sub(r"<!-- site-foot.*?<!-- /site-foot -->", "", t, flags=re.S)
    b = t.find("<body")
    t = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", "", t[b:], flags=re.S)
    t = re.sub(r'<h([1-4])(?: id="([^"]*)")?[^>]*>', lambda m: "\n\n%s [%s] " % ("#" * int(m.group(1)), m.group(2) or ""), t)
    t = re.sub(r"</(p|li|tr|h[1-6]|div|pre|table|summary|dt|dd)>", "\n", t)
    t = re.sub(r"</t[dh]>", " | ", t)
    t = re.sub(r"<br ?/?>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()


if __name__ == "__main__":
    s = text(sys.argv[1])
    a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    n = int(sys.argv[3]) if len(sys.argv) > 3 else len(s)
    print("[%d characters]" % len(s))
    print(s[a:a + n])
