#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove the solved APPSC 2022 Paper-II page says what the Commission's paper says.

    python3 recheck_appsc_2022.py [PATH_TO.pdf]          # default: docs/sources/appsc-aso-2022-paper-ii.pdf
    python3 recheck_appsc_2022.py --ocr [PATH_TO.pdf]    # also hold the words to an OCR reading

Written after the page, from the document rather than from the generator: it
reads the PDF with its own code and the FINISHED HTML, so a bug in
pdftext_appsc_2022.py or appsc_paper.py cannot hide behind the same bug
here. It asserts:

1.  The page has the paper's 150 questions, each number once, in the
    paper's order within each part of the page, each with the PDF's four
    options.
2.  The option the page marks, and the answer it gives, is the one the PDF
    marks -- read here twice, independently of the extractor: the option ID
    printed in green, and the icon beside it drawn in green (a tick) rather
    than red (a cross). The two reads must agree.
3.  The questions the PDF withdraws (its blue note, "ignored for all
    candidates") show no answer and say so, and no other question lacks one.
4.  The words on the page are exactly the transcribed words of
    appsc_paper_2022_text.py, question by question: nothing dropped or added
    between the transcription and the page.
5.  With --ocr, the transcription is held to the pictures it was typed from:
    RapidOCR reads each stem and option picture, and every transcribed
    word of each must be found in what the OCR reads there -- bar the two
    declared in OCR_EXCEPTIONS, which were checked by eye. Words are matched
    loosely (the OCR runs them together) and numbers strictly (see
    ocr_missing). One limit: the OCR makes stray digits of the Telugu, so a
    slip of a single digit can go unseen; a changed word, a longer number,
    a decimal or a table figure does not. (The
    pictures also carry the Telugu, which the OCR reads as noise and which is
    simply not asked for.) This needs rapidocr_onnxruntime, so it is run
    locally, not in CI; the OCR reading is cached in $TMPDIR.
6.  The duration, marks and negative marking the page quotes are the ones the
    PDF states.
7.  Every link resolves to a file that exists, and every #anchor to an id.
"""
import collections
import html
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PDF = os.path.join(ROOT, "docs", "sources", "appsc-aso-2022-paper-ii.pdf")
PAGE = os.path.join(ROOT, "exams", "appsc", "solved-2022-paper-ii.html")
GREEN, BLUE = 0x008000, 0x0000FF
OCR_SHARE = 1.0
# What the OCR cannot read, checked by eye against the PDF instead.
# The check fails if one of these ever reads, so the list cannot go stale.
OCR_EXCEPTIONS = {
    (121, "stem"): "the subscript of $P_{90}$, which the OCR drops",
    (123, "option 1"): "the single word \"Trend\" above its Telugu; the OCR returns \"808\"",
}

checks = 0
fails = []


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def words(s):
    return re.findall(r"\S+", html.unescape(s).replace("\xa0", " "))


def icon(r):
    """The tick and cross icons are small in both directions; a picture of a
    single digit is as narrow, but tall."""
    return r.width < 12 and r.height < 12


def pdf_questions(pdf):
    """{n: {"ids": [option IDs], "green": [nos], "ticks": [nos], "withdrawn": bool,
    "stem": [picture boxes], "options": [picture box or None]}}, and the header lines."""
    import fitz                                        # PyMuPDF
    doc = fitz.open(pdf)
    out, head, cur = {}, [], None
    for pi, page in enumerate(doc):
        lines, icons, pics = [], [], []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(s["text"] for s in l["spans"])
                cols = {s["color"] for s in l["spans"] if s["text"].strip()}
                lines.append((fitz.Rect(l["bbox"]), t, cols))
        for i in page.get_image_info(xrefs=True):
            r = fitz.Rect(i["bbox"])
            if icon(r):
                pix = fitz.Pixmap(doc, i["xref"])
                s, k = pix.samples, pix.n
                red, green = sum(s[0::k]), sum(s[1::k])
                icons.append((r, "tick" if green > red else "cross"))
            else:
                pics.append((pi, r))
        events = sorted([(r.y0, 0, ("line", r, t, cols)) for r, t, cols in lines] +
                        [(r.y0, 1, ("pic", p, r)) for p, r in pics], key=lambda e: (e[0], e[1]))
        for _, _, ev in events:
            if ev[0] == "line":
                _, r, t, cols = ev
                m = re.search(r"Question Number : (\d+) Question Id", t)
                if m:
                    cur = out[int(m.group(1))] = {"ids": [], "green": [], "ticks": [], "withdrawn": False,
                                                  "stem": [], "phase": "head", "labels": []}
                    continue
                if cur is None:
                    head.append(t.strip())
                    continue
                if cols == {BLUE}:
                    cur["withdrawn"] = cur["withdrawn"] or "ignored for all candidates" in t
                elif t.startswith("Correct Marks"):
                    cur["phase"] = "stem"
                    cur["marks"] = t.strip()
                elif t.strip() == "Options :":
                    cur["phase"] = "options"
                elif cur["phase"] == "options" and re.match(r"^\s*\d{9,}\.\s*$", t):
                    no = len(cur["ids"]) + 1
                    cur["ids"].append(t.strip().rstrip("."))
                    if cols == {GREEN}:
                        cur["green"].append(no)
                    cur["labels"].append((pi, r, no))
                    # the tick or cross is drawn just right of the ID, on its line
                    for ir, kind in icons:
                        if abs(ir.x0 - r.x1) < 3 and abs(ir.y1 - r.y1) < 4 and kind == "tick":
                            cur["ticks"].append(no)
            elif cur is not None and cur["phase"] == "stem":
                cur["stem"].append(ev[1:])
    for q in out.values():
        q.pop("phase")
    return out, head


def page_questions(page):
    out = collections.OrderedDict()
    for m in re.finditer(r'<div class="mcq" id="q(\d+)">(.*?)</details></div>', page, re.S):
        n, body = int(m.group(1)), m.group(2)
        q, _, answer = body.partition("<details>")
        q = re.sub(r'<span class="qn">Q\d+\.</span>', " ", q)
        key = re.search(r'<li value="(\d)" class="key">', q)
        ans = re.search(r"<strong>Answer: \((\d)\)", answer)
        opts = re.findall(r'<li value="(\d)"', q)
        out[n] = {"words": words(re.sub(r"<[^>]+>", " ", q)), "options": [int(o) for o in opts],
                  "key": int(key.group(1)) if key else None,
                  "answer": int(ans.group(1)) if ans else None,
                  "noanswer": "the Commission withdrew this question" in answer}
    return out


def transcribed_words(t):
    out = []
    for b in t["stem"]:
        if "p" in b:
            out += words(b["p"])
        elif "list" in b:
            for s in b["list"]:
                out += words(s)
        else:
            for row in b["table"]:
                for c in row:
                    out += words(c)
    for o in t["options"]:
        for s in o.get("lines", []):
            out += words(s)
        for row in o.get("table", []):
            for c in row:
                out += words(c)
    return out


ROMAN = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii"}


def ocr_fold(s):
    """Letters and digits only, lower case, with the pairs an OCR confuses
    (o and 0, l and 1) folded together."""
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("o", "0").replace("l", "1"))


NUMBER = re.compile(r"[0-9]+(?:[.,][0-9]+)*")


def ocr_tokens(s):
    """What an OCR reading can be held to: the words and numbers, with TeX
    commands dropped (\\frac{5}{32} -> 5 32) and the list numerals (i), (ii),
    (iii) left out, since the OCR reads (iii) as (ii) as often as not. A number
    keeps its decimal point and commas until it is matched."""
    s = re.sub(r"\\[A-Za-z]+", " ", s)
    return [t for t in re.findall(r"[a-z0-9]+(?:[.,][0-9]+)*", s.lower()) if t not in ROMAN]


def ocr_missing(need, lines):
    """The transcribed tokens not found in the OCR's lines. The OCR runs words
    together ("aretrue"), so a word counts as read if it is anywhere in the run
    of letters and digits it produced. A number must be one of the numbers the
    OCR read, as often as it is transcribed (so 0.05 is not "found" in 0.5, nor
    a third 10 in a table that has two); failing that, part of one, since a
    superscript is read into its base (2^10 as 210) -- but only a plain run of
    digits, since the OCR also runs a list of numbers together ("60,63"), and
    each of those counts as a number of its own. The OCR's numbers are taken
    only from runs holding a real digit, with o and l read as 0 and 1 there,
    so that "following" is not the number 0110."""
    run = "".join(ocr_fold(line) for line in lines)
    numbers, plain = collections.Counter(), set()
    for line in lines:
        for chunk in re.findall(r"[a-z0-9.,]+", line.lower()):
            if re.search(r"[0-9]", chunk):
                for n in NUMBER.findall(chunk.replace("o", "0").replace("l", "1")):
                    numbers[re.sub(r"[.,]", "", n)] += 1
                    pieces = n.split(",")
                    if len(pieces) > 1:
                        numbers.update(p.replace(".", "") for p in pieces)
                    else:
                        plain.add(n)
    out = []
    for t in need:
        if NUMBER.fullmatch(t):
            n = re.sub(r"[.,]", "", t)
            if numbers[n] > 0:
                numbers[n] -= 1
            elif not any(n in m for m in plain):
                out.append(t)
        elif ocr_fold(t) not in run:
            out.append(t)
    return out


def unit_texts(t):
    """[(label, text)]: the stem as one unit, then each option."""
    stem = []
    for b in t["stem"]:
        stem += [b["p"]] if "p" in b else b.get("list", []) + [c for r in b.get("table", []) for c in r]
    units = [("stem", " ".join(stem))]
    for k, o in enumerate(t["options"]):
        units.append(("option %d" % (k + 1), " ".join(o.get("lines", []) +
                                                     [c for r in o.get("table", []) for c in r])))
    return units


def ocr_check(pdf, doc_qs, text):
    import fitz
    from rapidocr_onnxruntime import RapidOCR
    cache_path = os.path.join(tempfile.gettempdir(), "appsc2022-ocr.json")
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    engine, doc = None, fitz.open(pdf)

    def read(pi, r, pad=False):
        """The OCR's lines for one picture. With pad, the picture is set in a
        white margin first: the OCR's detector passes over a lone digit or a
        short word drawn right up to the edge of its picture."""
        key = "%d:%d,%d,%d,%d%s" % (pi + 1, round(r.x0), round(r.y0), round(r.x1), round(r.y1),
                                    ":pad" if pad else "")
        if key not in cache:
            import cv2
            import numpy
            nonlocal engine
            engine = engine or RapidOCR()
            pix = doc[pi].get_pixmap(matrix=fitz.Matrix(3, 3), clip=r, alpha=False)
            img = numpy.frombuffer(pix.samples, dtype=numpy.uint8).reshape(pix.height, pix.width, pix.n)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            if pad:
                img = cv2.copyMakeBorder(img, 40, 40, 40, 40, cv2.BORDER_CONSTANT, value=(255, 255, 255))
            res, _ = engine(img)
            cache[key] = [t for _, t, _ in (res or [])]
        return cache[key]

    low = []
    for n, d in doc_qs.items():
        # the stem pictures; each option's picture is the one whose foot shares the
        # option ID's line (or, set full width, starts on the line below it)
        pics = {"stem": d["stem"]}
        for pi, lr, no in d["labels"]:
            boxes = [fitz.Rect(i["bbox"]) for i in doc[pi].get_image_info()]
            mine = [(pi, r) for r in boxes if not icon(r) and
                    ((abs(r.y1 - lr.y1) <= 5 and r.x0 >= lr.x0 - 2) or abs(r.y0 - lr.y1) <= 2)]
            if not mine and pi + 1 < doc.page_count:
                # an ID at the foot of a page, its picture at the head of the next
                nxt = sorted((fitz.Rect(i["bbox"]) for i in doc[pi + 1].get_image_info()
                              if not icon(fitz.Rect(i["bbox"]))), key=lambda r: r.y0)
                mine = [(pi + 1, nxt[0])] if nxt else []
            pics["option %d" % no] = mine
        for label, want in unit_texts(text[n]):
            need = ocr_tokens(want)
            if not need:
                continue
            lines = [line for pi, r in pics[label] for line in read(pi, r)]
            missing = ocr_missing(need, lines)
            if missing:
                lines += [line for pi, r in pics[label] for line in read(pi, r, True)]
                missing = ocr_missing(need, lines)
            share = 1 - len(missing) / len(need)
            if share < OCR_SHARE:
                low.append((n, label, share, missing))
    json.dump(cache, open(cache_path, "w"))
    return low


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pdf = args[0] if args else PDF
    sys.path.insert(0, HERE)
    from appsc_paper_2022_text import TEXT
    doc_qs, head = pdf_questions(pdf)
    page = open(PAGE, encoding="utf-8").read()
    pq = page_questions(page)

    # 1
    # the page groups the questions by subject, so it holds each number once
    # and keeps the paper's order within each part
    ok(sorted(pq) == list(range(1, 151)) and page.count('<div class="mcq" id="q') == 150,
       "the page does not hold questions 1..150 once each: %s" % sorted(pq)[:10])
    for part in re.split(r"<h2 id=", page)[1:]:
        ns = [int(n) for n in re.findall(r'<div class="mcq" id="q(\d+)">', part)]
        ok(ns == sorted(ns), "a part of the page is out of the paper's order: %s" % ns[:10])
    ok(sorted(doc_qs) == list(range(1, 151)), "the PDF's questions are not 1..150")
    print("questions: %d in the PDF, %d on the page" % (len(doc_qs), len(pq)))
    withdrawn = []
    for n, d in doc_qs.items():
        p = pq.get(n)
        if p is None:
            ok(False, "Q%d missing from the page" % n)
            continue
        ok(len(d["ids"]) == 4 and p["options"] == [1, 2, 3, 4],
           "Q%d: the PDF has %d options, the page %s" % (n, len(d["ids"]), p["options"]))
        # 2 and 3
        if d["withdrawn"]:
            withdrawn.append(n)
            ok(not d["green"] and not d["ticks"], "Q%d is withdrawn in the PDF but an option is marked" % n)
            ok(p["key"] is None and p["answer"] is None and p["noanswer"],
               "Q%d is withdrawn in the PDF but the page shows an answer" % n)
        else:
            ok(len(d["green"]) == 1 and d["green"] == d["ticks"],
               "Q%d: in the PDF the green ID is %s but the tick is at %s" % (n, d["green"], d["ticks"]))
            mark = d["green"][0] if d["green"] else None
            ok(p["key"] == mark, "Q%d: page marks option %s, the PDF %s" % (n, p["key"], mark))
            ok(p["answer"] == mark, "Q%d: page answers %s, the PDF marks %s" % (n, p["answer"], mark))
        # 4
        a, b = collections.Counter(transcribed_words(TEXT[n])), collections.Counter(p["words"])
        ok(a == b, "Q%d words differ: transcription-only %s, page-only %s"
           % (n, list((a - b).elements())[:6], list((b - a).elements())[:6]))
    ok(withdrawn == [51, 81], "the PDF withdraws %s, expected Q51 and Q81" % withdrawn)
    print("withdrawn in the PDF: %s" % withdrawn)

    # 5
    if "--ocr" in sys.argv:
        low = ocr_check(pdf, doc_qs, TEXT)
        for n, label, share, missing in low:
            ok((n, label) in OCR_EXCEPTIONS,
               "Q%d %s: only %.0f%% of the transcribed words are in the OCR reading; not found: %s"
               % (n, label, 100 * share, missing[:8]))
        for n, label in OCR_EXCEPTIONS:
            ok(any((n, label) == (m, l) for m, l, _, _ in low),
               "Q%d %s is declared unreadable but the OCR now reads it; drop the exception" % (n, label))
        print("OCR: %d stems and options with a word the OCR did not find, %d of them declared "
              "(checked by eye)" % (len(low), len(OCR_EXCEPTIONS)))

    # 6
    def field(k):
        return head[head.index(k + " :") + 1]
    note = re.sub(r"\s+", " ", re.search(r"<strong>Source\.</strong>(.*?)</p>", page, re.S).group(1))
    marks = {d["marks"] for d in doc_qs.values()}
    ok(len(marks) == 1, "the questions carry different marks: %s" % marks)
    wrong = re.search(r"Wrong Marks : (\S+)", marks.pop()).group(1)
    for phrase in ("duration %s minutes" % field("Duration"), "total marks %s" % field("Total Marks"),
                   "negative marks %s" % wrong, "%d questions" % len(doc_qs),
                   "&ldquo;%s&rdquo;" % field("Question Paper Name")):
        ok(phrase in note, "the source note does not say %r" % phrase)

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
    for f in fails[:40]:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
