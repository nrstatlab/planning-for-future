#!/usr/bin/env python3
"""Move the whole site onto one URL scheme, and leave redirects behind.

    python3 tools/restructure.py            # dry run: print the old -> new map
    python3 tools/restructure.py --apply    # move, rewrite links, write stubs

WHY. The repository's shape recorded its history rather than a decision: 20 of
21 BSc subject folders contained spaces (so 160 sitemap <loc> entries were
invalid and every one of those pages was a %20 URL), two naming conventions sat
inside one section, 323 filenames repeated their own folder name, and the
section names were inconsistent (-major on two of five).

THE SCHEME. The URL is the design and the folders follow it:

    /statistics/bsc/<subject>/unit1.html   was statistics-major/<subject with
                                           spaces>/unit1_<subject>.html
    /statistics/msc/<subject>/unit1.html   was statistics-major/msc/...
    /data-science/<course>/unit1.html      was data-science-major/<course>/
                                           unit1_<course>.html
    /subjects/<subject>/unit1.html         was exam-subjects/...
    /exams/<exam>/                         was statistics-papers/<exam>/ and
                                           ugc-net-statistics/
    /guides/which-test.html                was which-statistical-test.html
    /tools/{,data-science/,exams/}         was three separate tools directories

LINKS ARE RESOLVED, NOT PATTERN-MATCHED. Every href and src is resolved against
the file's OLD directory to an absolute repository path, mapped, then made
relative to the file's NEW directory. Depth changes therefore fix themselves,
which a regex over "../" could not do.

STUBS. GitHub Pages cannot redirect: the only mechanism it offers is a file at
the old path. Every moved page leaves one behind carrying a meta refresh and
robots noindex -- but NO rel=canonical, because it is meaningless on a noindex
page and would break check_canonical.py's assertion that nothing outside the
sitemap carries one.
"""
import argparse
import os
import posixpath
import re
import subprocess
from urllib.parse import quote, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def slug(name):
    """'applied statistics ii' -> 'applied-statistics-ii'."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def strip_suffix(stem, folder):
    """'unit1_descriptive statistics' -> 'unit1'; leaves a clean stem alone."""
    for sep in ("_", " "):
        tail = sep + folder
        if stem.endswith(tail):
            return stem[: -len(tail)]
    return stem


def tracked():
    out = subprocess.run(["git", "-C", ROOT, "ls-files"],
                         capture_output=True, text=True, check=True).stdout
    return [p for p in out.splitlines() if p]


def new_path(old):
    """The new repository path for one tracked file, or None to leave it."""
    parts = old.split("/")
    top = parts[0]

    if top == "statistics-major":
        if len(parts) == 2:                               # index.html, README.md
            return "statistics/" + parts[1]
        if parts[1] == "msc":
            return "statistics/msc/" + "/".join(parts[2:])
        subject = slug(parts[1])
        rest = parts[2:]
        if rest[0] == "css":
            return f"statistics/bsc/{subject}/" + "/".join(rest)
        stem, ext = os.path.splitext(rest[-1])
        return f"statistics/bsc/{subject}/{strip_suffix(stem, parts[1])}{ext}"

    if top == "data-science-major":
        if parts[1] == "tools":
            return "tools/data-science/" + "/".join(parts[2:])
        if len(parts) == 2:
            return "data-science/" + parts[1]
        rest = parts[1:]
        folder = rest[0]
        # machine-learning is a course folder like any other, so its own pages
        # get the suffix stripped; its self-study-notes/ subtree is three parts
        # deep and never reaches this branch.
        if len(rest) == 2 and folder not in ("notes", "labs", "data", "docs", "css"):
            stem, ext = os.path.splitext(rest[-1])
            return f"data-science/{folder}/{strip_suffix(stem, folder)}{ext}"
        return "data-science/" + "/".join(rest)

    if top == "ugc-net-statistics":
        name = parts[-1]
        if name == "pyq2026.html":
            name = "solved-2026.html"
        return "exams/ugc-net/" + "/".join(parts[1:-1] + [name])

    if top == "statistics-papers":
        if parts[1] == "tools":
            return "tools/exams/" + "/".join(parts[2:])
        return "exams/" + "/".join(parts[1:])

    if top == "exam-subjects":
        return "subjects/" + "/".join(parts[1:])

    if old == "which-statistical-test.html":
        return "guides/which-test.html"

    return None


def build_map():
    return {old: new_path(old) for old in tracked()
            if new_path(old) and new_path(old) != old}


# [^"\n] and not [^"]: without the newline guard this matched from an href="
# in one line's code example to the next quotation mark 35 lines further down
# and percent-encoded everything between, which is what it did to README.md,
# docs/GO-LIVE-REPORT.md and sitemap.xml on the first run.
ATTR = re.compile(r'((?:href|src)=")([^"\n]+)(")')
# A root-absolute href ("/" on 404.html, which JavaScript rewrites at runtime
# to the project root) is not relative to anything here and must be left alone.
SKIP = re.compile(r"^(#|/|mailto:|https?:|//|data:|javascript:)")
CODE = re.compile(r"<(code|pre)\b.*?</\1>", re.S)


def remap_links(text, old_file, new_file, moves):
    old_dir = posixpath.dirname(old_file)
    new_dir = posixpath.dirname(new_file)

    def one(m):
        pre, url, post = m.group(1), m.group(2), m.group(3)
        if SKIP.match(url):
            return m.group(0)
        frag = ""
        if "#" in url:
            url, frag = url.split("#", 1)
            frag = "#" + frag
        if not url:
            return pre + frag + post
        trailing = url.endswith("/")
        target = posixpath.normpath(posixpath.join(old_dir, unquote(url)))
        # The map holds files, not directories, so a link to a folder ("exams/"
        # or "asrb-net/") misses it. Resolve those through their index.html and
        # take that file's new folder -- without this, every directory link
        # still points at the pre-move tree.
        if target in moves:
            moved = moves[target]
        elif target + "/index.html" in moves:
            moved = posixpath.dirname(moves[target + "/index.html"])
        else:
            moved = target
        rel = posixpath.relpath(moved, new_dir or ".")
        if trailing and not rel.endswith("/"):
            rel += "/"
        return pre + quote(rel, safe="/._-~()!*'") + frag + post

    # A <code> or <pre> block is a lesson, not a link. web-technologies/unit2
    # shows the reader <link rel="stylesheet" href="styles.css">, and without
    # this that example came out as href="../../data-science-major/web-
    # technologies/styles.css" -- correct as a path, wrong as teaching.
    out, last = [], 0
    for m in CODE.finditer(text):
        out.append(ATTR.sub(one, text[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(ATTR.sub(one, text[last:]))
    return "".join(out)


# Bounded by a quote, an angle bracket or a newline. The first run used
# [^"]* , which in a Markdown file ran from the URL in one line past every
# newline to the next quotation mark 35 lines later and percent-encoded the
# lot -- that is what happened to README.md, docs/GO-LIVE-REPORT.md and,
# worst, sitemap.xml, where a single match swallowed the whole file.
CANON = re.compile(r'(https://nrstatlab\.github\.io/planning-for-future/)([^"\n<>]*)')


def remap_absolute(text, moves):
    """rel=canonical and og:url carry the full URL; move those too."""
    def one(m):
        base, path = m.group(1), m.group(2)
        plain = unquote(path)
        if plain in moves:
            moved = moves[plain]
        elif plain.rstrip("/") + "/index.html" in moves:
            # A canonical URL may name a directory, and the map holds files --
            # the same gap remap_links() closes. One stub page's canonical was
            # left on the old section name without this.
            moved = posixpath.dirname(moves[plain.rstrip("/") + "/index.html"]) + "/"
        else:
            moved = plain
        return base + quote(moved, safe="/._-~()!*'")
    return CANON.sub(one, text)


STUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={rel}">
<title>Moved</title>
</head>
<body>
<p>This page has moved to <a href="{rel}">{new}</a>.</p>
</body>
</html>
"""

# TWO PASSES, TWO DIFFERENT SETS OF FILES.
#
# The href/src pass runs on HTML and nothing else, because HTML is the only
# format here where href= and src= are links. Everywhere else they are code:
#
#   * .md -- all 20 of them sit in fenced blocks in the web-technologies notes
#     teaching HTML, and rewriting them turned a lesson that reads
#     <link rel="stylesheet" href="styles.css"> into one that reads
#     href="../../../../data-science-major/notes/sem-3/...";
#   * .js -- search.js builds a link by concatenation, '<a href="' + esc(...),
#     and run_web_labs.js asserts on `<img src="${img.getAttribute("src")}">`.
#     Both were percent-encoded into nonsense on the first run.
#
# The absolute-URL pass runs on the served formats. Markdown is left out of
# that one too: docs/GO-LIVE-REPORT.md quotes the old spaced URLs as the
# evidence for the finding this restructure answers, and rewriting them would
# erase the evidence. The Markdown that really does need new links --
# README.md's section table -- is rewritten as content, by hand.
LINK_EXT = (".html",)
REWRITE_EXT = (".html", ".css", ".js", ".xml", ".json")


def main(apply_changes):
    moves = build_map()
    pages = {o: n for o, n in moves.items() if o.endswith(".html")}
    print("%d files move, of which %d are pages" % (len(moves), len(pages)))
    for o in sorted(moves)[:8]:
        print("   %s\n      -> %s" % (o, moves[o]))
    print("   ... (%d more)" % max(0, len(moves) - 8))

    if not apply_changes:
        print("\ndry run -- pass --apply to move")
        return

    # Every tracked file BEFORE anything moves. This list has to be taken here:
    # calling git ls-files again afterwards returns the NEW paths, and then
    # every link is resolved against the directory the file has already moved
    # to rather than the one it was written in. That mistake produced 2,507
    # broken links the first time this script was run.
    before = tracked()

    for old, new in sorted(moves.items()):
        os.makedirs(os.path.dirname(os.path.join(ROOT, new)), exist_ok=True)
        subprocess.run(["git", "-C", ROOT, "mv", old, new], check=True)
    print("moved %d files" % len(moves))

    rewritten = 0
    for old in before:
        new = moves.get(old, old)
        if not new.endswith(REWRITE_EXT):
            continue
        path = os.path.join(ROOT, new)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8", errors="replace").read()
        out = remap_links(text, old, new, moves) if new.endswith(LINK_EXT) else text
        out = remap_absolute(out, moves)
        if out != text:
            open(path, "w", encoding="utf-8").write(out)
            rewritten += 1
    print("rewrote links in %d files" % rewritten)

    for old, new in sorted(pages.items()):
        dest = os.path.join(ROOT, old)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        rel = posixpath.relpath(new, posixpath.dirname(old) or ".")
        open(dest, "w", encoding="utf-8").write(
            STUB.format(rel=quote(rel, safe="/._-~()!*'"), new=new))
    print("wrote %d redirect stubs" % len(pages))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    main(ap.parse_args().apply)
