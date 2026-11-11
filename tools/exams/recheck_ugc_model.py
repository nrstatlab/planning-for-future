#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check the finished UGC NET model-question pages, independently of
ugc_model.py: reads only the HTML.

    python3 recheck_ugc_model.py

Every unit page: fifty questions numbered Q1..Q50, four different options, an
answer (A)-(D) that repeats the option it names, an explanation, a notes link
whose target exists, no letter keyed more than 16 times, balanced $ signs, no
bare '<' in text, and no stem already used on another model page, in the short
MCQs or in the solved paper. The index links exactly the unit pages there are.
"""
import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIRS = ["exams/ugc-net/model", "exams/ugc-net/paper-1/model"]
OLD = ["exams/ugc-net/mcqs.html", "exams/ugc-net/solved-2026.html", "exams/ugc-net/paper-1/mcqs.html"]
bad = []


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", re.sub(r"<[^>]+>", " ", s).lower()).strip()


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


seen = {}
for rel in OLD:
    for stem in re.findall(r'<div class="q">(.*?)</div>\s*<ol', read(rel), re.S):
        s = norm(re.sub(r"^\s*(<span[^>]*>.*?</span>|\d+\.)", "", stem))
        if len(s) > 40:
            seen[s] = rel
total = 0
for d in DIRS:
    if not os.path.isdir(os.path.join(ROOT, d)):
        continue
    units = sorted((f for f in os.listdir(os.path.join(ROOT, d)) if re.fullmatch(r"unit\d+\.html", f)),
                   key=lambda f: int(f[4:-5]))
    linked = re.findall(r'href="(unit\d+\.html)"', read(d + "/index.html"))
    if sorted(set(linked)) != sorted(units):
        bad.append("%s/index.html links %s, pages are %s" % (d, linked, units))
    for u in units:
        rel = d + "/" + u
        t = read(rel)
        body = t[t.index("<main"):t.index("</main>")]
        blocks = re.findall(r'<div class="mcq" id="q(\d+)">(.*?)</details></div>', body, re.S)
        if [int(n) for n, _ in blocks] != list(range(1, 51)):
            bad.append("%s: questions are not Q1..Q50 (%d found)" % (rel, len(blocks)))
        keys = collections.Counter()
        for n, b in blocks:
            where = "%s Q%s" % (rel, n)
            stem = re.search(r'<div class="q"><span class="qn">Q%s\.</span>(.*?)</div>\s*<ol class="options">' % n, b, re.S)
            opts = re.findall(r"<li>(.*?)</li>", b[b.index('<ol class="options">'):b.index("</ol>")], re.S)
            ans = re.search(r"<strong>Answer: \(([A-D])\) (.*?)</strong></p>\s*<p>(.*?)</p>\s*<p class=\"notes\">.*?<a href=\"([^\"#]+)#([^\"]+)\">", b, re.S)
            if not stem or len(opts) != 4 or len(set(map(norm, opts))) != 4 and len(set(opts)) != 4:
                bad.append(where + ": stem or the four options")
                continue
            if not ans:
                bad.append(where + ": answer, explanation or notes link")
                continue
            keys[ans.group(1)] += 1
            if not ans.group(2).rstrip(".").startswith(opts["ABCD".index(ans.group(1))].rstrip(".")):
                bad.append(where + ": the answer does not repeat option " + ans.group(1))
            if len(norm(ans.group(3))) < 60:
                bad.append(where + ": explanation too short")
            target = os.path.normpath(os.path.join(ROOT, d, ans.group(4)))
            if not os.path.exists(target) or 'id="%s"' % ans.group(5) not in open(target, encoding="utf-8").read():
                bad.append(where + ": notes link %s#%s" % (ans.group(4), ans.group(5)))
            for part in (stem.group(1), ans.group(3)) + tuple(opts):
                if part.replace("\\$", "").count("$") % 2:
                    bad.append(where + ": unbalanced $")
                if re.search(r"<(?![a-zA-Z/!])", part):
                    bad.append(where + ": bare <")
            s = norm(stem.group(1))
            if len(s) > 40:
                if s in seen:
                    bad.append(where + ": stem already used in " + seen[s])
                seen[s] = where
        total += len(blocks)
        if keys and max(keys.values()) > 16:
            bad.append("%s: keys are lopsided %s" % (rel, dict(keys)))
        print("%s: %d questions, keys %s" % (rel, len(blocks), dict(sorted(keys.items()))))
for b in bad:
    print("FAIL " + b)
print("%d model questions checked, %d problems" % (total, len(bad)))
sys.exit(1 if bad else 0)
