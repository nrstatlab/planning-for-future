#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove the solved APPSC 2025 Paper-II page says what the Commission's paper says.

    python3 recheck_appsc_paper.py [PATH_TO.pdf]   # default: docs/sources/appsc-aso-2025-paper-ii.pdf

Written after the page, from the document rather than from the generator: it
reads the PDF with its own code and the FINISHED HTML, so a bug in
pdftext_appsc_paper.py or appsc_paper.py cannot hide behind the same bug
here. It asserts:

1.  The page has the paper's 150 questions, numbered 1 to 150, in order.
2.  Each question's words -- stem, table cells and options -- are exactly the
    words of that question's English block in the PDF: none dropped, none
    added, none "corrected". Words are compared as a multiset per question,
    because a table's cells reach the PDF's text layer in an order of their
    own; the order of the questions is item 1.
3.  The answer the page shows, and the option it marks, is the option the
    PDF ticks -- read here from the tick icon's own position, independently
    of the text colours the extractor used.
4.  The one question the PDF withdraws ("ignored for all candidates") shows
    no answer, and no other question lacks one.
5.  Every image in a question's English block appears on the page exactly
    once, in that question, marked as read from the picture; nothing else
    is so marked. These are the only words item 2 does not hold to the PDF.
6.  The duration, marks and negative marking the page quotes are the ones the
    PDF's header states.
7.  Every link resolves to a file that exists, and every #anchor to an id.
"""
import collections
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PDF = os.path.join(ROOT, "docs", "sources", "appsc-aso-2025-paper-ii.pdf")
PAGE = os.path.join(ROOT, "exams", "appsc", "solved-2025-paper-ii.html")

checks = 0
fails = []


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def words(s):
    s = html.unescape(s).replace("\xa0", " ")
    return re.findall(r"\S+", s)


def pdf_questions(pdf):
    """{n: {"words": [...], "tick": option no or None, "images": [keys], "withdrawn": bool}}
    from the first (English) block of each question number."""
    import fitz                                   # PyMuPDF
    doc = fitz.open(pdf)
    # The option icons are tiny squares, drawn hundreds of times. Of the two,
    # the tick is drawn once per question block, the cross three times.
    count = collections.Counter()
    for p in doc:
        for i in p.get_image_info(xrefs=True):
            r = fitz.Rect(i["bbox"])
            if r.width < 12 and r.height < 12:
                count[i["xref"]] += 1
    (a, na), (b, nb) = count.most_common(2)
    tick = a if na < nb else b
    icons = {a, b}

    out, head, cur = {}, [], None
    for pi, page in enumerate(doc):
        imgs = [(i["xref"], fitz.Rect(i["bbox"])) for i in page.get_image_info(xrefs=True)]
        lines = []
        for bl in page.get_text("dict")["blocks"]:
            for l in bl.get("lines", []):
                t = "".join(s["text"] for s in l["spans"])
                blue = all(s["color"] == 0x0000FF for s in l["spans"] if s["text"].strip())
                lines.append((fitz.Rect(l["bbox"]), t, blue and bool(t.strip())))
        events = [(r.y0, "line", (r, t, blue)) for r, t, blue in lines] + \
                 [(r.y0, "img", (x, r)) for x, r in imgs]
        # Lines in page order; an image sits between the lines around it.
        order = sorted(range(len(events)), key=lambda k: (events[k][0], 0 if events[k][1] == "line" else 1))
        labels = {}                 # option label line -> option number, this page
        ticks = []                  # (question, y): matched to labels once the page is read
        for k in order:
            y, kind, val = events[k]
            if kind == "line":
                r, t, blue = val
                m = re.search(r"Question Number : (\d+) ", t)
                if m:
                    n = int(m.group(1))
                    cur = None if n in out else {"n": n, "words": [], "tick": None, "images": [],
                                                 "withdrawn": False, "phase": "head"}
                    if cur:
                        out[n] = cur
                    continue
                if cur is None:
                    if not out:
                        head.append(t.strip())
                    continue
                if cur["phase"] == "head":
                    if t.startswith("Correct Marks"):
                        cur["phase"] = "body"
                    continue
                if blue:
                    cur["withdrawn"] = cur["withdrawn"] or "ignored for all candidates" in t
                    continue
                if t.strip() == "Options :":
                    cur["phase"] = "options"
                    continue
                lm = re.match(r"^\s*([1-4])\.\s*(.*)$", t)
                if lm and r.x0 < 50 and cur["phase"] == "options":
                    labels[(pi, round(r.y0))] = (cur, int(lm.group(1)))
                    cur["words"] += words(lm.group(2))
                    continue
                cur["words"] += words(t)
            else:
                x, r = val
                if cur is None or cur["phase"] == "head":
                    continue
                if x in icons:
                    if x == tick:
                        ticks.append((cur, r.y0))
                    continue
                cur["images"].append("%d:%d,%d" % (pi + 1, round(r.x0), round(r.y0)))
        # An icon is drawn a point above its "1." label, so it is matched to the
        # nearest label of its own question after the whole page is read.
        for q, ty in ticks:
            near = [(abs(ly - ty), no) for (lp, ly), (lq, no) in labels.items() if lq is q]
            if near and min(near)[0] < 4:
                ok(q["tick"] is None, "Q%d has two ticks" % q["n"])
                q["tick"] = min(near)[1]
            else:
                ok(False, "Q%d: a tick with no option label beside it" % q["n"])
    return out, head


def page_questions(page):
    out = collections.OrderedDict()
    for m in re.finditer(r'<div class="mcq" id="q(\d+)">(.*?)</details></div>', page, re.S):
        n, body = int(m.group(1)), m.group(2)
        answer_part = body
        body = body.split("<details>")[0]           # the question, not the answer's echo of it
        imgs = re.findall(r'<span class="pdfimg" data-img="([^"]+)">', body)
        shown = re.sub(r'<span class="pdfimg" data-img="[^"]+">.*?</span>(?=[^<]*(?:<|$))', " ", body, flags=re.S)
        shown = re.sub(r'<span class="pdfimg"[^>]*>(?:(?!</span>).)*</span>', " ", shown, flags=re.S)
        q = shown.split("<details>")[0]
        q = re.sub(r'<span class="qn">Q\d+\.</span>', " ", q)
        key = re.search(r'<li value="(\d)" class="key">', body)
        ans = re.search(r"<strong>Answer: \((\d)\)", answer_part)
        # the page keeps a bare $ out of MathJax's reach with a span; it is
        # part of the word, not a break in it
        q = re.sub(r'<span class="usd">\$</span>', "$", q)
        out[n] = {"words": words(re.sub(r"<[^>]+>", " ", q)), "images": imgs,
                  "key": int(key.group(1)) if key else None,
                  "answer": int(ans.group(1)) if ans else None,
                  "noanswer": "the Commission withdrew this question" in answer_part}
    return out


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else PDF
    doc_qs, head = pdf_questions(pdf)
    page = open(PAGE, encoding="utf-8").read()
    pq = page_questions(page)

    # 1
    ok(list(pq) == list(range(1, 151)), "the page's questions are not 1..150 in order: %s" % list(pq)[:10])
    ok(sorted(doc_qs) == list(range(1, 151)), "the PDF's questions are not 1..150")
    print("questions: %d in the PDF, %d on the page" % (len(doc_qs), len(pq)))

    for n, d in doc_qs.items():
        p = pq.get(n)
        if p is None:
            ok(False, "Q%d missing from the page" % n)
            continue
        # 2
        a, b = collections.Counter(d["words"]), collections.Counter(p["words"])
        ok(a == b, "Q%d words differ: PDF-only %s, page-only %s"
           % (n, list((a - b).elements())[:6], list((b - a).elements())[:6]))
        # 3 and 4
        if d["withdrawn"]:
            ok(d["tick"] is None and p["key"] is None and p["answer"] is None and p["noanswer"],
               "Q%d is withdrawn in the PDF but the page shows an answer" % n)
        else:
            ok(d["tick"] is not None, "Q%d: no tick found in the PDF" % n)
            ok(p["key"] == d["tick"], "Q%d: page marks option %s, the PDF ticks %s" % (n, p["key"], d["tick"]))
            ok(p["answer"] == d["tick"], "Q%d: page answers %s, the PDF ticks %s" % (n, p["answer"], d["tick"]))
        # 5
        ok(sorted(d["images"]) == sorted(p["images"]),
           "Q%d images: PDF %s, page %s" % (n, sorted(d["images"]), sorted(p["images"])))
    ok(sum(1 for d in doc_qs.values() if d["withdrawn"]) == 1, "expected exactly one withdrawn question")

    # 6
    def field(k):
        return head[head.index(k + " :") + 1]
    note = re.search(r"<strong>Source\.</strong>(.*?)</p>", page, re.S).group(1)
    for k, phrase in (("Duration", "duration %s minutes"), ("Total Marks", "total marks %s"),
                      ("Section Negative Marks", "negative marks %s"),
                      ("Number of Questions", "%s questions")):
        ok(phrase % field(k) in re.sub(r"\s+", " ", note), "the source note does not quote %s = %s" % (k, field(k)))

    # 7
    base = os.path.dirname(PAGE)
    ids = set(re.findall(r'id="([^"]+)"', page))
    for h in set(re.findall(r'href="([^"]+)"', page)):
        if re.match(r"^(https?:|mailto:|//)", h):
            continue
        path, _, anchor = h.partition("#")
        full = os.path.normpath(os.path.join(base, path)) if path else PAGE
        if not os.path.exists(full):
            ok(False, "link to a missing file: %s" % h)
            continue
        if anchor:
            text = page if not path else open(full, encoding="utf-8").read()
            ok('id="%s"' % anchor in text or (not path and anchor in ids), "link to a missing anchor: %s" % h)
        else:
            ok(True, "")

    print("%d checks, %d failures" % (checks, len(fails)))
    for f in fails[:25]:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
