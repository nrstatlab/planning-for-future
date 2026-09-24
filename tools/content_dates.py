#!/usr/bin/env python3
"""When each page's CONTENT last changed, for the footer's "Last updated".

    python3 tools/content_dates.py statistics/sampling-techniques/unit2.html

The obvious answer -- `git log -1 -- <file>` -- is wrong in two ways here:

  * it stops at the 2026 restructure. That commit left a redirect stub at every
    old path, so git does not see a rename; it sees the old file rewritten and
    a new file added. With -C it sees the truth, a COPY, and history can be
    followed back through it;
  * it counts commits that touched every page without touching what any page
    says: the restructure rewrote 8,000 links, the navigation added a bar, the
    footer adds this line. Dating a unit on probability "24 September" because
    a menu was added that day would be a small lie on 691 pages.

So history is walked once, newest first, following copies and renames, and a
commit is skipped for dating (but still followed through) when it is one of
the site-wide mechanical changes. Those are named below by hash, and any later
commit can opt out the same way by carrying the trailer

    Site-chrome: yes

in its message. A page whose only commits are mechanical is dated by its
oldest commit, i.e. when it was written.

A later restructure -- one that, like the first, moves pages and leaves a
stub at every old path -- carries

    Site-restructure: yes

so its copies are followed as the first one's are, and it is mechanical too.
A commit that is mechanical for most pages but really did change a few can
name those, one trailer line each,

    Content: statistics/index.html

and only those pages are dated by it.

One `git log` over the whole history (about 3 seconds), not one per page.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

RESTRUCTURE = "828b0d86c8e43ac6f25cb63ee91dba5f99a48ab0"
# Site-wide changes that altered no page's teaching content.
MECHANICAL = {
    "828b0d86c8e43ac6f25cb63ee91dba5f99a48ab0",   # the restructure: moves and links
    "18cc014aa7dcfded4cb338fd2ac387807686a839",   # the navigation bar
}
TRAILER = "Site-chrome: yes"
MOVE_TRAILER = "Site-restructure: yes"
CONTENT = "Content: "
SEP = "\x1e"


def _log():
    out = subprocess.run(
        ["git", "-c", "diff.renameLimit=20000", "log", "--no-merges", "-C",
         "--name-status", f"--format={SEP}%H %cs%n%B{SEP}"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    commits = []
    parts = out.split(SEP)
    # parts: '', 'H date\nbody', '\nname-status...', 'H date\nbody', ...
    i = 1
    while i < len(parts) - 1:
        head, files = parts[i], parts[i + 1]
        sha, date = head.split("\n", 1)[0].split()
        body = head.split("\n", 1)[1] if "\n" in head else ""
        entries = [ln.split("\t") for ln in files.strip().splitlines() if "\t" in ln]
        moved = sha == RESTRUCTURE or MOVE_TRAILER in body
        changed = {ln[len(CONTENT):].strip() for ln in body.splitlines()
                   if ln.startswith(CONTENT)}
        mechanical = TRAILER in body or sha in MECHANICAL or MOVE_TRAILER in body
        commits.append((sha, date, mechanical, moved, changed, entries))
        i += 2
    return commits


def content_dates(paths):
    """{path: 'YYYY-MM-DD'} for every repository-relative path given."""
    want = set(paths)
    tracking = {p: p for p in want}     # name in history -> page it became
    dated, oldest = {}, {}
    for sha, date, mechanical, moved, changed, entries in _log():
        for e in entries:
            status = e[0][0]
            # A copy is followed only inside the restructure commit. The
            # restructure is where pages really were copied (a stub was left
            # at the old path), with similarity as low as 57% because every
            # link changed -- so no score threshold separates it. Anywhere
            # else -- including later chrome commits -- "C" means a new file
            # that merely resembles an old one:
            # about.html came out as a 55% copy of 404.html and was dated
            # 2 September, three weeks before it was written.
            if status == "C" and not moved and len(e) == 3:
                e = ["A", e[2]]
                status = "A"
            if status in "RC" and len(e) == 3:
                old, new = e[1], e[2]
                if new in tracking:
                    page = tracking.pop(new)
                    oldest[page] = date
                    if (not mechanical or page in changed) and page not in dated:
                        dated[page] = date
                    tracking[old] = page    # keep following it further back
            elif len(e) >= 2 and e[1] in tracking:
                page = tracking[e[1]]
                oldest[page] = date
                if (not mechanical or page in changed) and page not in dated:
                    dated[page] = date
                if status == "A":           # born here; nothing older to find
                    del tracking[e[1]]
    return {p: dated.get(p) or oldest.get(p) for p in want}


if __name__ == "__main__":
    for p, d in sorted(content_dates(sys.argv[1:]).items()):
        print(d, p)
