#!/usr/bin/env python3
"""Fail if an image is published that nothing on the site uses.

The site is served straight from the repository (.nojekyll), so every tracked
file is public. The 2026 audit found eighteen review screenshots (r2-*.png,
r6-*.png, 3.5 MB) committed to the web root: nothing linked them, but anyone
could fetch them. This keeps that from happening again: every tracked image
must be named by at least one tracked page, stylesheet, script, note or
generator. A picture that is referenced nowhere is either a leftover to delete
or a link that is missing -- both worth knowing.

    python3 tools/check_published.py
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMAGES = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico")
TEXT = (".html", ".css", ".js", ".md", ".py", ".json", ".xml", ".txt", ".sh", ".yml")


def tracked():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return [f for f in out.split("\0") if f]


def main():
    files = tracked()
    images = [f for f in files if f.lower().endswith(IMAGES)]
    corpus = []
    for f in files:
        if f.lower().endswith(TEXT) and (ROOT / f).is_file():
            corpus.append((f, (ROOT / f).read_text(errors="replace")))

    unused = []
    for img in images:
        name = pathlib.PurePosixPath(img).name
        if not any(name in text for f, text in corpus if f != img):
            unused.append(img)

    print(f"{len(images)} tracked images; {len(images) - len(unused)} referenced")
    if unused:
        print(f"FAIL: {len(unused)} published image(s) that nothing references:")
        for u in unused:
            print("   ", u)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
