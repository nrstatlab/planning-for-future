# -*- coding: utf-8 -*-
"""Turn a destination path into the link text the map shows.

The label is read from the destination page's own <title>, never hand-written,
so a page that is retitled cannot end up with a stale label on the map.
"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
BASE = ROOT + "statistics-papers/iss/"

ROMAN = {1:"I",2:"II",3:"III",4:"IV",5:"V",6:"VI",7:"VII",8:"VIII",9:"IX",10:"X"}


def title_of(dest):
    p = os.path.normpath(BASE + dest)
    s = open(p, encoding="utf-8").read()
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip()


def label(dest):
    return amp(_label(dest))


def _label(dest):
    """Programme prefix + subject + unit, built from the page's own title."""
    t = title_of(dest)
    rel = os.path.normpath(dest).replace("\\", "/")
    # strip the leading ../../
    rel = rel.split("../")[-1] if rel.startswith("../") else rel
    rel = re.sub(r"^(\.\./)+", "", os.path.normpath(dest))

    if rel.startswith("ugc-net-statistics/"):
        m = re.match(r"Unit ([IVX]+): (.*?) —", t)
        if m:
            return "UGC NET Unit %s &mdash; %s" % (m.group(1), m.group(2))
        return "UGC NET " + t

    if rel.startswith("statistics-major/msc/"):
        prefix = "MSc"
    elif rel.startswith("statistics-major/"):
        prefix = "BSc"
    elif rel.startswith("data-science-major/"):
        prefix = "Data Science"
    else:
        prefix = ""

    # "Subject — Practical Course — 10 Experiments"
    m = re.match(r"(.*?) \u2014 Practical Course", t)
    if m:
        return "%s %s &mdash; Practical" % (prefix, m.group(1))
    # "Topic — Subject (Unit 3)"
    m = re.match(r"(.*?) — (.*?) \(Unit (\d+)\)$", t)
    if m:
        return "%s %s Unit %s &mdash; %s" % (prefix, m.group(2), m.group(3), m.group(1))
    # "Practical — Subject (STS-108)"  /  "Topic — Subject (STS-108)"
    m = re.match(r"(.*?) — (.*?) \(STS-\d+\)$", t)
    if m:
        return "%s %s &mdash; %s" % (prefix, m.group(2), m.group(1))
    # "Subject — Complete Study Material" / "Subject — something"
    m = re.match(r"(.*?) — (.*)$", t)
    if m:
        return "%s %s" % (prefix, m.group(1))
    return ("%s %s" % (prefix, t)).strip()


def amp(s):
    """Escape a bare & that a page title carries unescaped."""
    return re.sub(r"&(?!(?:[A-Za-z][A-Za-z0-9]{1,8}|#[0-9]{1,5}|#x[0-9A-Fa-f]{1,5});)", "&amp;", s)


def esc(dest):
    """href for the map page: the path with spaces percent-encoded."""
    return dest.replace(" ", "%20")
