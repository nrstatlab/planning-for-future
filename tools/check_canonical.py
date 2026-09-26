#!/usr/bin/env python3
"""Give every indexed page a canonical URL, and assert that it stays true.

A canonical tag tells a search engine which address is the original. It matters
here for one reason: a static site can be mirrored by anyone with `wget`, and
without this tag a copy can outrank the original. It cannot stop the copying --
nothing can, the pages are HTML -- but it keeps the credit.

Two rules, and both directions are checked (plus og:url, below):

  * every page in the sitemap carries a canonical, and it is that page's own
    sitemap URL, absolute;
  * no page outside the sitemap carries one -- 404.html and archive/ must not,
    or a search engine is told the error page is the original of something.

og:url is the address a shared link previews as, and it has to be the same
address: every indexed page carries one equal to its canonical. 94 pages (the
MSc courses, ISS and APPSC maps, the practical-only courses) had none; --apply
writes it beside the canonical, like the canonical itself.

The set of indexed pages is not restated here. It comes from build_sitemap.py,
which defines it, so the sitemap and the canonicals cannot drift apart.

The generated pages get their tag from their own generator (build_site.py and
build_topic_index.py); a tag written into one of those by hand would be
destroyed on the next build. This writes the tag for the HAND-WRITTEN pages
only, and then verifies all of them.

    python3 tools/check_canonical.py            # report
    python3 tools/check_canonical.py --apply    # write the missing ones
"""
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
# A redirect stub is an .html file like any other: without this every one
# of the 690 the restructure left behind would be listed, indexed and
# asserted on as though a reader could land on it.
from stubs import is_stub  # noqa: E402


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# The definition of "indexed", and the one place the domain is written down.
_sm = _load(ROOT / "tools" / "build_sitemap.py", "_sm")
SITE_BASE = _sm.SITE_BASE

CANON_RE = re.compile(r'<link rel="canonical" href="([^"]*)"\s*/?>')
OGURL_RE = re.compile(r'<meta property="og:url" content="([^"]*)"\s*/?>')
HEAD_END = "</head>"

# One page points its canonical somewhere else on purpose: it is a single-file
# dump of notes whose real home is the folder index, so it declares itself a
# duplicate of that. Named here so the check treats it as intended rather than
# quietly skipping anything that disagrees.
DELIBERATE = {
    "data-science/machine-learning/self-study-notes/ml_self_study_notes.html":
        f"{SITE_BASE}/data-science/machine-learning/self-study-notes/",
}


def indexed():
    """path -> the absolute URL the sitemap publishes for it."""
    return {p: f"{SITE_BASE}/{p.relative_to(ROOT).as_posix()}" for p in _sm.pages()}


def expected(path, url):
    rel = path.relative_to(ROOT).as_posix()
    return DELIBERATE.get(rel, url)


def main(apply=False):
    want = indexed()
    wrote = ok = wrong = 0
    problems = []

    og_ok = og_wrote = 0
    for path, url in sorted(want.items()):
        text = path.read_text(errors="replace")
        target = expected(path, url)
        og = OGURL_RE.search(text)
        if og and og.group(1) == target:
            og_ok += 1
        elif apply:
            tag = f'<meta property="og:url" content="{target}">'
            text = OGURL_RE.sub(tag, text, count=1) if og else \
                text.replace(HEAD_END, f"{tag}\n{HEAD_END}", 1)
            path.write_text(text)
            og_wrote += 1
        else:
            problems.append(f"{path.relative_to(ROOT)}: "
                            + (f"og:url {og.group(1)}, should be {target}" if og else "no og:url"))
            wrong += 1
        found = CANON_RE.search(text)

        if found and found.group(1) == target:
            ok += 1
            continue
        if found:
            # present but pointing elsewhere -- rewrite it to the right address
            if apply:
                path.write_text(CANON_RE.sub(
                    f'<link rel="canonical" href="{target}">', text, count=1))
                wrote += 1
            else:
                problems.append(f"{path.relative_to(ROOT)}: points at "
                                f"{found.group(1)}, should be {target}")
                wrong += 1
            continue
        if apply:
            assert HEAD_END in text, f"{path} has no </head> to write into"
            path.write_text(text.replace(
                HEAD_END, f'<link rel="canonical" href="{target}">\n{HEAD_END}', 1))
            wrote += 1
        else:
            problems.append(f"{path.relative_to(ROOT)}: no canonical")
            wrong += 1

    # nothing outside the sitemap may claim to be canonical for anything
    stray = []
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts or p in want:
            continue
        # A stub carries no canonical by design -- it is noindex, so one would
        # be meaningless -- but it must not be asserted on as a page either.
        if is_stub(p):
            continue
        if CANON_RE.search(p.read_text(errors="replace")):
            stray.append(str(p.relative_to(ROOT)))

    print(f"{len(want)} indexed pages; {ok} already correct, "
          f"{wrote} written, {wrong} wrong")
    print(f"og:url: {og_ok} already correct, {og_wrote} written")
    print(f"{len(DELIBERATE)} deliberate exception(s), asserted by name")
    for pr in problems[:12]:
        print("   ", pr)
    if stray:
        print(f"\n{len(stray)} page(s) outside the sitemap carry a canonical "
              f"and should not:")
        for s in stray:
            print("   ", s)

    if apply:
        print("\nre-run without --apply to verify")
        return 0
    return 1 if (wrong or stray) else 0


if __name__ == "__main__":
    sys.exit(main(apply="--apply" in sys.argv))
