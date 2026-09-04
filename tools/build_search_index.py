#!/usr/bin/env python3
"""Write assets/search-index.json -- the whole site, searchable from the browser.

594 pages and no way to search them. A reader who knows the word but not which
unit it sits in had only the A-Z index and Ctrl+F on one page at a time. On a
static host, searching is one of the few jobs that genuinely cannot be done
without JavaScript, which is why this exists at all.

What goes in a record is chosen to be what a reader actually types: the page
title, the topics the page itself claims to teach (its "Topics Covered" chips),
its section headings, and its one-line description. Not the body text -- full
text would multiply the index by twenty for matches that are mostly incidental
mentions, and the chips already say what a page is *about* rather than what it
happens to contain.

The chip rules are not restated here. They live in build_topic_index.py, which
already knows that "An EBS volume is in ONE availability zone" is a sentence and
not a topic; this imports them so the two indexes can never disagree.

Run after anything that adds, removes or retitles a page.
"""
import html as html_mod
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "search-index.json"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# The chip vocabulary and its filters, from the module that defines them.
_ti = _load(ROOT / "tools" / "build_topic_index.py", "_ti")
plain, is_topic, CHIP_RE, TITLE_RE = _ti.plain, _ti.is_topic, _ti.CHIP_RE, _ti.TITLE_RE

H2_RE = re.compile(r"<h2[^>]*>(.*?)</h2>", re.S)
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')

# Same rule as the sitemap: the error page is not study material, and the
# archive is a kept record rather than something to send a reader to.
SKIP_NAMES = {"404.html"}
SKIP_DIRS = {"archive"}

# A page's section, for the label shown beside a result.
SECTIONS = {
    "statistics-major": "Statistics",
    "data-science-major": "Data Science",
    "ugc-net-statistics": "UGC NET",
}

# Headings past this many are sub-sub-sections nobody searches by name, and
# chips past this many are a syllabus dump rather than what the page is about.
MAX_HEADINGS = 25
MAX_TOPICS = 30

# Chips that repeat the page's own title add nothing to a match and cost bytes.
def _useful(topic, title):
    return topic.lower() not in title.lower()


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts or SKIP_DIRS & set(p.parts) or p.name in SKIP_NAMES:
            continue
        yield p


def record(path):
    text = path.read_text(errors="replace")
    m = TITLE_RE.search(text)
    title = plain(m.group(1)) if m else path.stem
    # The site's titles all end in the same few suffixes; carrying them in every
    # record would mean every query matched every page a little.
    title = re.sub(r"\s*[—-]\s*NRSTATLAB\s*$", "", title).strip()

    heads = []
    for h in H2_RE.findall(text):
        t = plain(h)
        if t and t.lower() not in ("topics covered", "contents", "on this page"):
            heads.append(t)

    topics = []
    for c in CHIP_RE.findall(text):
        t = plain(c)
        if is_topic(t) and _useful(t, title) and t not in topics:
            topics.append(t)

    d = DESC_RE.search(text)
    rel = path.relative_to(ROOT).as_posix()
    return {
        "u": rel,
        "t": title,
        "s": SECTIONS.get(path.relative_to(ROOT).parts[0], "NRSTATLAB"),
        "h": heads[:MAX_HEADINGS],
        "k": topics[:MAX_TOPICS],
        "d": html_mod.unescape(d.group(1))[:180] if d else "",
    }


def main(apply=False):
    recs = [record(p) for p in pages()]

    # A page that is in the sitemap but not the index is a page a reader can be
    # sent to and can never find. Assert the two agree rather than hoping.
    want = {p.relative_to(ROOT).as_posix() for p in pages()}
    got = {r["u"] for r in recs}
    assert want == got, f"not indexed: {sorted(want - got)[:5]}"
    for r in recs:
        assert r["t"], f"{r['u']} has no title to search by"

    blob = json.dumps(recs, separators=(",", ":"), ensure_ascii=False)
    heads = sum(len(r["h"]) for r in recs)
    topics = sum(len(r["k"]) for r in recs)
    print(f"{len(recs)} pages, {heads} headings, {topics} topics")
    print(f"{len(blob.encode()) / 1024:.0f} KB raw "
          f"(the reader downloads it gzipped, about a fifth of that)")

    thin = [r["u"] for r in recs if not r["h"] and not r["k"] and not r["d"]]
    if thin:
        print(f"{len(thin)} pages have only a title to match on, e.g. {thin[:3]}")

    if apply:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(blob, encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)}")
    else:
        print("dry run -- pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main(apply="--apply" in sys.argv))
