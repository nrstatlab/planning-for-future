#!/usr/bin/env python3
"""Fail on a bare "<" in page text, or on equation tags that would repeat an id.

In HTML a "<" that cannot begin a tag -- "0 < x", "k<1", "<\\Lambda" -- is
still read as text by a browser, so nothing looks wrong. But it is invalid
markup, and it is one keystroke away from the version that is not harmless:
"x<y" opens a tag called "y" and swallows the rest of the formula. The 2026
audit found 98 of them across 20 pages, the largest single class of the
validator's errors. The rule is the validator's own: outside <script>,
<style> and comments, "<" must be followed by a letter, "/", "!" or "?",
or be written &lt;.

This is a cheap stand-in for running the full validator on every page; the
validator itself remains the release check (docs/ARCHITECTURE.md).

It also catches one error the validator cannot see, because MathJax creates
it after the page loads: a page that repeats an equation tag. When each proof
numbers its equations from (1), MathJax gives every "\tag{1}" the id
"mjx-eqn:1", and the page ends up with duplicate ids. Such a page must set
MathJax's tagformat option so that each tag gets its own id.

    python3 tools/check_markup.py
"""
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {"archive", ".git"}
PROTECT = re.compile(r"<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->", re.S | re.I)
BARE_LT = re.compile(r"<(?=[^A-Za-z/!?])")
TAG = re.compile(r"\\tag\{([^{}]*)\}")


def main():
    bad, pages = [], 0
    for p in sorted(ROOT.rglob("*.html")):
        if SKIP & set(p.relative_to(ROOT).parts):
            continue
        pages += 1
        text = PROTECT.sub(lambda m: " " * len(m.group(0)), p.read_text(errors="replace"))
        for m in BARE_LT.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            bad.append(f"{p.relative_to(ROOT)}:{line}: {text[m.start():m.start() + 30]!r}")
        tags = collections.Counter(TAG.findall(text))
        repeated = sorted(t for t, n in tags.items() if n > 1)
        if repeated and "tagformat" not in p.read_text(errors="replace"):
            bad.append(f"{p.relative_to(ROOT)}: \\tag{{{repeated[0]}}} is used more than once "
                       f"and the page does not set MathJax tagformat, so the ids repeat")
    print(f"{pages} pages checked for a bare '<' and for repeated equation tags")
    if bad:
        print(f"FAIL: {len(bad)} problem(s) -- write a bare '<' as &lt;; give repeated tags "
              f"their own ids with tagformat")
        for b in bad[:20]:
            print("   ", b)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
