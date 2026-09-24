#!/usr/bin/env python3
"""Tell a redirect stub from a page, for every tool that walks the tree.

GitHub Pages has no redirect mechanism: the only way to keep an old URL alive
is to leave a file at it, so the 2026 restructure left 689 of them behind (see
tools/restructure.py). They are HTML files in the tree like any other, and
without this every one of them would be listed in the sitemap, indexed by the
search box, mined for chips by the A-Z index and asserted on by the canonical
checker -- four tools reporting on pages no reader should ever land on.

The test is what the stub actually is, not where it sits: a meta refresh plus
robots noindex. Written that way on purpose, so it also catches the two stubs
that predate the restructure and were written by hand.
"""
import re

REFRESH = re.compile(r'<meta\s+http-equiv="refresh"', re.I)
NOINDEX = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.I)

# A stub is tiny; reading the head is enough and keeps a 690-file walk cheap.
HEAD_BYTES = 2048


def is_stub(path):
    """True when this .html file exists only to forward a reader somewhere else."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            head = fh.read(HEAD_BYTES)
    except OSError:
        return False
    return bool(REFRESH.search(head) and NOINDEX.search(head))
