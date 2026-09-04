#!/usr/bin/env python3
"""Give the Statistics half of the site the in-page navigation it never had.

Measured before this ran: 169 pages, 1,450 <h2> headings, **11** of them with
an id, and not one contents list -- while the Data Science half already emits a
collapsible "On this page" on 184 pages. 142 statistics pages have six or more
sections and no way to jump to any of them, and no heading anywhere in the
section can be linked to.

Doing this in JavaScript was the obvious shortcut and would have been the wrong
fix: an anchor that only exists once a script has run cannot be linked to from
another page, cannot be followed from a search result, is invisible to a search
engine, and disappears entirely if the script fails. The ids belong in the HTML.

Nothing here is new logic. add_anchors_and_toc() in build_site.py already does
exactly this for the other half of the site -- it takes rendered HTML, skips
headings that already carry an id, de-duplicates slugs, and falls back to h3
where the h2 headings are too few to be a map. This applies it to the pages
that were written by hand instead of generated.

Two smaller things ride along, because they touch the same files:

  * the CSS, ported verbatim from data-science-major so the two halves cannot
    drift apart, into all 21 copies of the statistics stylesheet (which are
    byte-identical -- see the root README);
  * MathJax made to match the page, in both directions. Removed from the 7
    statistics pages that carry no mathematics.
    Nearly a megabyte each, on a site whose whole appeal is loading fast on a
    phone. (An earlier count said 9. It was wrong: it searched for the word
    "mathjax" anywhere in the file, and two index pages merely say in prose
    that "all formulae are rendered with MathJax". Only a <script> whose src
    is MathJax costs the reader anything.) And *added* to 12 pages that were
    the other way round -- prose containing \(\chi^2\) and no MathJax to
    render it, so a reader saw the backslashes. That was not caused by this
    change; the check written to prove this change broke nothing found it.


Dry run by default; --apply writes.
"""
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECTION = ROOT / "statistics-major"
DS_CSS = ROOT / "data-science-major" / "css" / "styles.css"

_spec = importlib.util.spec_from_file_location(
    "_bs", ROOT / "data-science-major" / "tools" / "build_site.py")
_bs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bs)
add_anchors_and_toc = _bs.add_anchors_and_toc

# The body of a page starts after its banner (and after the "Topics Covered"
# chip row, where there is one -- that h2 labels furniture, not a section, and
# listing it in the contents would be the first and most useless entry).
AFTER_CHIPS = re.compile(r'(<div class="chips">.*?</div>\s*\n)', re.S)
AFTER_BANNER = re.compile(r'(<div class="banner">.*?</div>\s*\n)', re.S)

# ...and ends where the page stops being prose.
BODY_END = re.compile(r'(\n\s*<div class="page-nav">|\n\s*<footer|\n</div>\s*\n</body>)')

# Any script whose src is MathJax, not just the one spelling of the tag: two
# pages write it without the id, and matching only the id form would have left
# them alone while reporting success.
MATHJAX_TAG = re.compile(r'\s*<script[^>]+src="[^"]*mathjax[^"]*"[^>]*></script>', re.I)
MATHJAX_NEW = ('<script id="MathJax-script" async '
               'src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">'
               '</script>')
# What counts as mathematics here is exactly what MathJax will actually render,
# and that is narrower than it looks:
#
#   * its default delimiters are \\( inline and $$ or \\[ display -- a lone $ is
#     NOT one unless a page configures it, and only the 13 UGC NET pages do.
#     Treating "$...$" as math matched MongoDB's $and, jQuery's $(), R's
#     km$totss and Excel's $B$1 across 59 pages with no formula on them;
#   * it skips <pre> and <code>, so a regex like \\(\\d{3}\\) in a Python sample
#     and MongoDB's $$cid are not formulae either, however they are spelled.
_CODE = re.compile(r"<(code|pre)\b.*?</\1>", re.S)
_MATH_DELIM = re.compile(r"\$\$|\\\(|\\\[")


def has_math(html_text):
    """True when MathJax would find something on this page to typeset."""
    return bool(_MATH_DELIM.search(_CODE.sub(" ", html_text)))

# The whole block, so the two halves of the site cannot style the same element
# differently. Taken from the source file rather than retyped.
CSS_FROM, CSS_TO = "details {", "@media print { details.toc { display: none; } }"

MARKER = "/* ---- in-page navigation, ported from data-science-major ---- */"


def body_span(text):
    """(start, end) of the prose region, or None if the page has no shape."""
    m = AFTER_CHIPS.search(text) or AFTER_BANNER.search(text)
    if not m:
        return None
    start = m.end()
    e = BODY_END.search(text, start)
    return (start, e.start() if e else len(text))


def rewrite_page(path):
    """Returns (new_text, note) -- new_text is None when nothing changed."""
    text = path.read_text(encoding="utf-8")
    notes = []
    out = text

    span = body_span(out)
    if span:
        start, end = span
        body = out[start:end]
        fixed = add_anchors_and_toc(body)
        if fixed != body:
            out = out[:start] + fixed + out[end:]
            notes.append(f"+{len(re.findall(r'<h[23][^>]* id=', fixed))} anchors")
            if 'class="toc"' in fixed:
                notes.append("contents")

    # The tag should match the page, both ways round. The test runs on the
    # whole file minus the head, so a formula in a figure caption or a table
    # still counts.
    math = has_math(out.split("</head>", 1)[-1])
    loads = bool(MATHJAX_TAG.search(out))
    if loads and not math:
        out = MATHJAX_TAG.sub("", out, count=1)
        notes.append("-mathjax")
    elif math and not loads:
        out = out.replace("</head>", MATHJAX_NEW + "\n</head>", 1)
        notes.append("+mathjax")

    return (out if out != text else None), ", ".join(notes)


def css_block():
    src = DS_CSS.read_text(encoding="utf-8")
    a = src.index(CSS_FROM)
    b = src.index(CSS_TO) + len(CSS_TO)
    return src[a:b]


def main(apply=False):
    pages = sorted(p for p in SECTION.rglob("*.html"))
    changed, anchors_added, toc_added = [], 0, 0
    mj_removed = mj_added = 0

    for p in pages:
        new, note = rewrite_page(p)
        if new is None:
            continue
        changed.append((p, note))
        m = re.search(r"\+(\d+) anchors", note)
        anchors_added += int(m.group(1)) if m else 0
        toc_added += "contents" in note
        mj_removed += "-mathjax" in note
        mj_added += "+mathjax" in note
        if apply:
            p.write_text(new, encoding="utf-8")

    print(f"{len(pages)} pages, {len(changed)} changed")
    print(f"   {toc_added} gained a contents list")
    print(f"   {anchors_added} headings now carry an id")
    print(f"   {mj_removed} stopped loading MathJax they had no use for")
    print(f"   {mj_added} started loading the MathJax their formulae needed")

    sheets = sorted(SECTION.rglob("css/styles.css"))
    block = css_block()
    # Replace any block already ported rather than skipping the file, so a
    # change to the source stylesheet reaches all 21 copies on the next run.
    want = f"{MARKER}\n{block}\n"
    todo = []
    for sheet in sheets:
        cur = sheet.read_text(encoding="utf-8")
        head = cur.split(MARKER)[0].rstrip("\n")
        new_text = f"{head}\n\n{want}"
        if new_text != cur:
            todo.append((sheet, new_text))
    print(f"   {len(todo)} of {len(sheets)} stylesheets need the rules "
          f"({len(block)} bytes each)")
    if apply:
        for sheet, new_text in todo:
            sheet.write_text(new_text, encoding="utf-8")

    if not apply:
        print("\ndry run -- pass --apply to write. Sample:")
        for p, note in changed[:6]:
            print(f"   {note:34} {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(apply="--apply" in sys.argv))
