#!/usr/bin/env python3
"""Give the UGC NET pages the "Topics Covered" chips the rest of the site has.

    python3 tools/add_ugcnet_chips.py            # dry run: what would be kept and dropped
    python3 tools/add_ugcnet_chips.py --apply    # write the chip blocks

WHY THIS EXISTS. ugc-net-statistics/ is the only section of six with no chips
anywhere, which has three consequences a reader feels: its 13 pages carry an
empty "k" field in assets/search-index.json, so site search can only match them
on their titles; topics.html therefore links into three sections and not this
one; and the 500-question MCQ bank -- probably the most useful single artefact
on this site -- cannot be found by searching for anything it actually drills.
Nothing here writes new content. It wires existing content into the site's own
index.

The chips are DERIVED, never hand-written. Same rule as the syllabus maps'
link labels: a wrong chip should be visibly wrong rather than plausibly wrong.

Idempotent: a second --apply run reports 0 changed, the way
add_statistics_navigation.py does.
"""
import argparse
import html as html_mod
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SECTION = os.path.join(ROOT, "exams", "ugc-net")

sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools", "data-science"))
# The chip rules live in the module that defines them. Importing rather than
# restating means a change to MAX_TOPIC_CHARS or FURTHER furniture reaches this
# generator too, instead of the two drifting apart.
import build_topic_index as bti                      # noqa: E402

MAX_CHIPS = 12          # house median is 8; the raw headings run to 47 on unit10

# Headings that pass is_topic() but should not become index entries.
#
# "Topic Overview — What & Why" is on 10 of the 13 pages: as an A-Z row it is
# one entry pointing at ten pages, which tells a reader nothing. The rest are
# real headings that are meaningless once separated from their page -- an index
# row reading "Variance" filed against a sampling page is worse than no row.
# This list came out of the dry run, not out of guessing.
SKIP = {
    "topic overview — what & why", "topic overview - what & why",
    "where the derivations are", "about these mcqs",
    "properties", "variance", "limits", "continuity", "tests", "functions",
    "composition", "efficiency", "interpretation", "key results",
    "key concepts", "common cases", "two wings", "summary", "notes",
    # pyq2026.html's only headings are the paper's own structure, not topics
    # anyone searches for. With these skipped it gets no chip block, which is
    # the honest outcome for a page whose headings name sections rather than
    # subjects -- the questions inside it are already reachable through the
    # unit pages' chips.
    "jump to", "paper i — general paper", "paper i - general paper",
    "paper i — topic distribution", "paper i - topic distribution",
    "paper ii — statistics (code 107)", "paper ii - statistics (code 107)",
    "paper ii — topic distribution", "paper ii - topic distribution",
}

# mcqs.html has no <h3> at all -- only <h2> like
#   "Unit 3 — Sampling Methods & Design of Experiments (50 MCQs)"
# of which five exceed MAX_TOPIC_CHARS and would be silently dropped. Stripping
# the unit number and the count turns all ten into clean topic names that pass.
UNIT_PREFIX = re.compile(r"^Unit\s+\d+\s*[—–-]\s*")
MCQ_SUFFIX = re.compile(r"\s*\(\d+\s*MCQs?\)\s*$")

# detex() renders backslash-TeX as characters, but it does NOT remove the $
# delimiters -- and ugc-net-statistics is the one section that writes maths as
# $...$. Without this, a heading like "Adjusted $R^2$" becomes a chip with the
# dollars intact, and topics.html, index.html and the search dropdown load no
# MathJax at all, so a reader sees the dollar signs printed literally.
#
# Note on what this is NOT for: check_no_raw_tex.py matches \command and $$
# only, so a single-dollar chip would pass it. The backslash forms it does
# catch are already gone by here, because bti.plain() runs detex() first --
# "$t$-test for individual $\beta_j$" arrives as "t-test for individual βⱼ".
# This step is about what the page shows a reader, not about the checker.
DOLLARS = re.compile(r"\$([^$]*)\$")

INSERT_AFTER = re.compile(r'(<main class="container">\s*\n(?:<section[^>]*>\s*\n)?)')
EXISTING = re.compile(r"[ \t]*<h2>Topics Covered</h2>\s*\n"
                      r"[ \t]*<div class=\"chips\">.*?</div>\s*\n",
                      re.S)


def text_of(fragment):
    return " ".join(
        html_mod.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def clean(heading):
    """One heading -> a chip, or None if it should not become one."""
    h = DOLLARS.sub(r"\1", heading)          # $R^2$ -> R^2, before detex
    h = bti.plain(h)                         # detex + whitespace, the shared rule
    h = UNIT_PREFIX.sub("", MCQ_SUFFIX.sub("", h)).strip()
    if not h or h.lower() in SKIP:
        return None
    return h if bti.is_topic(h) else None


def chips_for(page_text):
    """Chips for one page, in the order the page teaches them."""
    heads = re.findall(r"<h3[^>]*>(.*?)</h3>", page_text, re.S)
    if not heads:                            # mcqs.html
        heads = re.findall(r"<h2[^>]*>(.*?)</h2>", page_text, re.S)
    kept, dropped, seen = [], [], set()
    for raw in heads:
        t = text_of(raw)
        if not t:
            continue
        c = clean(t)
        if c is None:
            dropped.append(t)
            continue
        if c.lower() in seen:
            continue
        seen.add(c.lower())
        kept.append(c)
    return kept[:MAX_CHIPS], dropped


def block(chips):
    rows = "".join('    <span class="chip">%s</span>\n'
                   % html_mod.escape(c, quote=False) for c in chips)
    return "  <h2>Topics Covered</h2>\n  <div class=\"chips\">\n%s  </div>\n\n" % rows


def main(apply_changes):
    pages = sorted(f for f in os.listdir(SECTION) if f.endswith(".html"))
    changed = total_chips = 0
    for name in pages:
        path = os.path.join(SECTION, name)
        text = open(path, encoding="utf-8").read()
        stripped = EXISTING.sub("", text)           # so re-runs are idempotent
        chips, dropped = chips_for(stripped)
        print("%-16s %2d chips, %2d dropped" % (name, len(chips), len(dropped)))
        if chips:
            print("      keep: " + " | ".join(chips))
        if dropped:
            print("      drop: " + " | ".join(dropped[:6])
                  + (" ..." if len(dropped) > 6 else ""))
        if not chips:
            # No block at all rather than an empty or invented one.
            if stripped != text and apply_changes:
                open(path, "w", encoding="utf-8").write(stripped)
                changed += 1
            continue
        m = INSERT_AFTER.search(stripped)
        if not m:
            print("      SKIPPED: no <main class=\"container\"> to insert after")
            continue
        out = stripped[:m.end()] + block(chips) + stripped[m.end():]
        total_chips += len(chips)
        if out != text:
            changed += 1
            if apply_changes:
                open(path, "w", encoding="utf-8").write(out)
    print("\n%d pages, %d changed, %d chips total" % (len(pages), changed, total_chips))
    if not apply_changes:
        print("dry run -- pass --apply to write")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    main(ap.parse_args().apply)
