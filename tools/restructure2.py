#!/usr/bin/env python3
"""One Statistics: take the programme and the semester out of every URL.

    python3 tools/restructure2.py            # dry run: print the old -> new map
    python3 tools/restructure2.py --apply    # move, rewrite links, write stubs

WHY. The site is for exam preparation now, and a visitor studies it course by
course, not as a degree. The URL still said which degree a course came from:

    /statistics/bsc/sampling-techniques/     becomes  /statistics/sampling-techniques/
    /statistics/msc/sampling-theory/         becomes  /statistics/sampling-theory/
    /subjects/economics/                     becomes  /statistics/economics/

One folder name is shared by both programmes -- design-and-analysis-of-
experiments -- and the postgraduate one becomes ...-advanced, the level tag
the catalogue gives it (tools/course_catalogue.py).

The two programme hubs that no longer have anything to list,
statistics/msc/index.html and subjects/index.html, become stubs to the one
Statistics hub. The postgraduate and allied stylesheets were one file twice
over (byte-identical), so both become statistics/css/styles.css.

THE MACHINERY IS tools/restructure.py's, imported rather than copied: links
resolved against the file's old directory and made relative to its new one,
HTML-only href pass, <code>/<pre> left alone, newline-guarded patterns. What is
new here is the stub layer. The first restructure left 690 stubs, and each of
them points at a page this one moves; they are re-pointed straight at the
final page, so no old URL ever takes two hops.

Python generator data (tools/exams/*) is rewritten at the literal level, as
the first restructure did -- see rewrite_python().
"""
import argparse
import os
import posixpath
import re
import subprocess
import sys
from urllib.parse import quote, unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import restructure as r1          # noqa: E402
from stubs import is_stub         # noqa: E402

ROOT = r1.ROOT

# Folder names that exist in both programmes; the postgraduate one is renamed.
CLASH = {"design-and-analysis-of-experiments": "design-and-analysis-of-experiments-advanced"}

# Hubs with nothing left to list: stub to the one Statistics hub.
RETIRED = {
    "statistics/msc/index.html": "statistics/index.html",
    "subjects/index.html": "statistics/index.html",
}

SHEET = "statistics/css/styles.css"


def new_path(old):
    parts = old.split("/")
    if old in RETIRED:
        return None                       # handled separately: not a move
    if old in ("statistics/msc/css/styles.css", "subjects/css/styles.css"):
        return SHEET
    if len(parts) >= 3 and parts[0] == "statistics" and parts[1] == "bsc":
        return "statistics/" + "/".join(parts[2:])
    if len(parts) >= 3 and parts[0] == "statistics" and parts[1] == "msc":
        course = CLASH.get(parts[2], parts[2])
        return "statistics/" + "/".join([course] + parts[3:])
    if len(parts) >= 3 and parts[0] == "subjects":
        return "statistics/" + "/".join(parts[1:])
    return None


def build_map(files):
    moves = {}
    for old in files:
        new = new_path(old)
        if new and new != old:
            moves[old] = new
    # The link map also sends the retired hubs to the one hub, so every link
    # to them is rewritten, although the files themselves are not moved.
    links = dict(moves)
    links.update(RETIRED)
    return moves, links


# ---- Python generator data --------------------------------------------------
# Order matters: the one renamed course first, then the generic prefixes.
PY_RULES = [
    ("statistics/msc/design-and-analysis-of-experiments/",
     "statistics/design-and-analysis-of-experiments-advanced/"),
    ("statistics/msc/css/styles.css", SHEET),
    ("statistics/bsc/", "statistics/"),
    ("statistics/msc/", "statistics/"),
    ("subjects/economics/", "statistics/economics/"),
    ("subjects/financial-accounting/", "statistics/financial-accounting/"),
    ('"../../subjects/"', '"../../statistics/"'),
]
PY_FILES = ["tools/exams/iss_map_data.py", "tools/exams/appsc_map_data.py",
            "tools/exams/asrb_map_data.py", "tools/exams/asrb_map.py",
            "tools/exams/appsc_map.py", "tools/exams/csirmap.py"]


def rewrite_python():
    """Literal rewrite of the path strings the exam generators carry.

    iss_map_data.py builds MSc paths as M + "folder/unitN.html" with
    M = "../../statistics/msc/". Once M is "../../statistics/", M + "design-
    and-analysis-of-experiments/" would silently name the BSc course, so those
    concatenations are rewritten to the renamed folder first."""
    changed = []
    for rel in PY_FILES:
        p = os.path.join(ROOT, rel)
        text = open(p, encoding="utf-8").read()
        out = re.sub(r'\bM \+ "design-and-analysis-of-experiments/',
                     'M + "design-and-analysis-of-experiments-advanced/', text)
        for a, b in PY_RULES:
            out = out.replace(a, b)
        if out != text:
            open(p, "w", encoding="utf-8").write(out)
            changed.append(rel)
    return changed


# ---- stubs -----------------------------------------------------------------
REFRESH_URL = re.compile(r'(<meta http-equiv="refresh" content="\d+;\s*url=)([^"]+)(")', re.I)


def repoint_stub(path_rel, links):
    """Point an existing stub at the page its target has moved to."""
    p = os.path.join(ROOT, path_rel)
    text = open(p, encoding="utf-8", errors="replace").read()
    m = REFRESH_URL.search(text)
    if not m:
        return False
    url = m.group(2)
    frag = ""
    if "#" in url:
        url, frag = url.split("#", 1)
        frag = "#" + frag
    here = posixpath.dirname(path_rel)
    target = posixpath.normpath(posixpath.join(here, unquote(url)))
    if target in links:
        moved = links[target]
    elif target + "/index.html" in links:
        moved = posixpath.dirname(links[target + "/index.html"])
    else:
        return False
    new_rel = quote(posixpath.relpath(moved, here or "."), safe="/._-~()!*'")
    old_rel = m.group(2).split("#", 1)[0]
    out = text.replace(old_rel + frag, new_rel + frag) if frag else text.replace(old_rel, new_rel)
    # The visible text of the machine-written stubs names the destination path.
    out = out.replace(">" + target + "<", ">" + moved + "<")
    if out != text:
        open(p, "w", encoding="utf-8").write(out)
        return True
    return False


def main(apply_changes):
    before = r1.tracked()
    moves, links = build_map(before)
    pages = {o: n for o, n in moves.items() if o.endswith(".html")}
    print("%d files move, of which %d are pages; %d hubs retire"
          % (len(moves), len(pages), len(RETIRED)))
    seen = {}
    for o, n in moves.items():
        seen.setdefault(n, []).append(o)
    clashes = {n: os for n, os in seen.items() if len(os) > 1 and n != SHEET}
    if clashes:
        for n, os_ in clashes.items():
            print("CLASH", n, os_)
        sys.exit(1)
    for o in sorted(moves)[:6]:
        print("   %s\n      -> %s" % (o, moves[o]))
    if not apply_changes:
        print("\ndry run -- pass --apply to move")
        return

    stubs_before = [f for f in before if f.endswith(".html")
                    and f not in moves and is_stub(os.path.join(ROOT, f))]

    for old, new in sorted(moves.items()):
        dest = os.path.join(ROOT, new)
        if os.path.exists(dest):
            # The second copy of the identical stylesheet.
            subprocess.run(["git", "-C", ROOT, "rm", "-q", old], check=True)
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        subprocess.run(["git", "-C", ROOT, "mv", old, new], check=True)
    print("moved %d files" % len(moves))

    rewritten = 0
    for old in before:
        new = moves.get(old, old)
        if not new.endswith(r1.REWRITE_EXT):
            continue
        path = os.path.join(ROOT, new)
        if not os.path.exists(path) or (old in moves and old.endswith(".css")):
            continue
        text = open(path, encoding="utf-8", errors="replace").read()
        out = r1.remap_links(text, old, new, links) if new.endswith(r1.LINK_EXT) else text
        out = r1.remap_absolute(out, links)
        if out != text:
            open(path, "w", encoding="utf-8").write(out)
            rewritten += 1
    print("rewrote links in %d files" % rewritten)

    n = sum(repoint_stub(s, links) for s in stubs_before)
    print("re-pointed %d existing stubs" % n)

    for old, new in sorted(list(pages.items()) + list(RETIRED.items())):
        dest = os.path.join(ROOT, old)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        rel = posixpath.relpath(new, posixpath.dirname(old) or ".")
        open(dest, "w", encoding="utf-8").write(
            r1.STUB.format(rel=quote(rel, safe="/._-~()!*'"), new=new))
    print("wrote %d redirect stubs" % (len(pages) + len(RETIRED)))

    print("rewrote generator data in", ", ".join(rewrite_python()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    main(ap.parse_args().apply)
