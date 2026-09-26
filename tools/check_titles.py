#!/usr/bin/env python3
"""Fail if two indexed pages share a <title>.

The title is what a search result and a browser tab show. When two pages
carry the same one, a reader cannot tell which result is which. The 2026
audit found three such pairs: the Data Mining and the Machine Learning
"K-Means clustering in Python" labs, and the index and syllabus pages of
the two editions of Computational Statistics & R Programming.

The set of indexed pages is the sitemap's, taken from build_sitemap.py, so
the lab demos and redirect stubs that search engines are told to skip are
not held to this.

    python3 tools/check_titles.py
"""
import collections
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TITLE = re.compile(r"<title>(.*?)</title>", re.S)

sys.path.insert(0, str(ROOT / "tools"))
_spec = importlib.util.spec_from_file_location("_sm", ROOT / "tools" / "build_sitemap.py")
_sm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sm)


def main():
    seen = collections.defaultdict(list)
    for p in _sm.pages():
        m = TITLE.search(p.read_text(errors="replace"))
        if m:
            seen[re.sub(r"\s+", " ", m.group(1)).strip()].append(p.relative_to(ROOT).as_posix())
    dups = {t: ps for t, ps in seen.items() if len(ps) > 1}
    print(f"{sum(map(len, seen.values()))} indexed pages; {len(seen)} distinct titles")
    if dups:
        print(f"FAIL: {len(dups)} title(s) used by more than one page:")
        for t, ps in sorted(dups.items()):
            print(f"    {t!r}: {', '.join(ps)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
