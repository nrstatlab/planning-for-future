# -*- coding: utf-8 -*-
"""Read the structure and the key of the APPSC 2022 Paper-II into appsc_paper_2022.json.

    python3 pdftext_appsc_2022.py [PDF]      # default: docs/sources/appsc-aso-2022-paper-ii.pdf
    python3 pdftext_appsc_2022.py --render   # also write a PNG of every question

The document is the Commission's "Question Paper Preview" of "ECOSTATS 0411S2"
(created 4 November 2022): 150 MCQs. Unlike the 2025 preview, every question
and every option here is a PICTURE -- the English and the Telugu stacked in one
image -- and the text layer carries only the headers and each option's ID
number. So this script reads what the text layer does hold:

  * each question's number and ID, and where its stem image(s) and its four
    option images sit;
  * the key, read twice and independently: the correct option's ID is printed
    green (the others red), and a tick icon (the others a cross) sits beside
    it. The icons are separate images here, not one shared one, so the tick
    is recognised by its pixels. The two reads must agree.

Two questions (51 and 81) carry the Commission's blue note that a discrepancy
was found and the question "is ignored for all candidates"; those, and only
those, may have no key. The words of the questions are transcribed by hand from
the renders into appsc_paper_2022_text.py; recheck_appsc_2022.py holds that
transcription to an OCR reading of the same images.
"""
import collections
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PDF = os.path.join(ROOT, "docs", "sources", "appsc-aso-2022-paper-ii.pdf")
OUT = os.path.join(HERE, "appsc_paper_2022.json")

GREEN, RED, BLUE = 0x008000, 0xFF0000, 0x0000FF
QHEAD = re.compile(r"Question Number : (\d+) Question Id : (\d+)")
OPTION_ID = re.compile(r"^\s*(\d{9,})\.\s*$")
IGNORED = "ignored for all candidates"
HEADER = ("Question Paper Name", "Creation Date", "Duration", "Total Marks")


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def icon_kinds(doc):
    """{pixel digest: 'tick' | 'cross'} for the small icons: the commoner
    pattern is the cross (three per question), the rarer the tick."""
    import fitz
    seen = collections.Counter()
    for p in doc:
        for i in p.get_image_info(xrefs=True):
            r = fitz.Rect(i["bbox"])
            if r.width < 12 and r.height < 12:
                seen[hashlib.md5(fitz.Pixmap(doc, i["xref"]).samples).hexdigest()] += 1
    if len(seen) != 2:
        raise SystemExit("expected two icon patterns, found %d" % len(seen))
    (a, na), (b, nb) = seen.most_common(2)
    return {a: "cross", b: "tick"}


def extract(pdf=PDF):
    import fitz
    doc = fitz.open(pdf)
    kinds = icon_kinds(doc)
    head, questions, cur = [], [], None
    for pi, page in enumerate(doc):
        texts, pics = [], []
        for b in page.get_text("dict")["blocks"]:
            if b["type"] == 1:
                continue
            for l in b["lines"]:
                t = "".join(s["text"] for s in l["spans"])
                cols = {s["color"] for s in l["spans"] if s["text"].strip()}
                texts.append((l["bbox"], t, cols))
        for i in page.get_image_info(xrefs=True):
            r = fitz.Rect(i["bbox"])
            if r.width < 12 and r.height < 12:
                kind = kinds.get(hashlib.md5(fitz.Pixmap(doc, i["xref"]).samples).hexdigest())
                pics.append(("icon", kind, r))
            else:
                pics.append(("img", "%d:%d,%d" % (pi + 1, round(r.x0), round(r.y0)), r))
        # An option's ID, its icon and its picture share one row, but the
        # picture (two lines, English over Telugu) starts well above the ID.
        # So each is matched to the option ID whose bottom edge it shares;
        # anything left is part of a question's stem, placed by its top edge.
        labels = [(bb, t) for bb, t, _ in texts if OPTION_ID.match(t)]
        owned = {}
        for kind, val, r in pics:
            near = [(abs(bb[3] - r.y1), k) for k, (bb, _) in enumerate(labels)]
            if near and min(near)[0] <= 5 and r.x0 >= labels[min(near)[1]][0][0] - 2:
                owned.setdefault(min(near)[1], []).append((r.x0, kind, val))
                continue
            # a full-width option picture is set on the line below its ID,
            # starting where the ID's line ends (Q14, Q20, Q41, Q69)
            below = [(abs(bb[3] - r.y0), k) for k, (bb, _) in enumerate(labels)]
            if kind == "img" and below and min(below)[0] <= 2:
                owned.setdefault(min(below)[1], []).append((r.x0 + 1000, kind, val))
        events = [(bb[1], 0, "text", (t, cols, bb)) for bb, t, cols in texts]
        for kind, val, r in pics:
            if not any(val == v[2] and kind == v[1] for vs in owned.values() for v in vs):
                events.append((r.y0, 1, kind, val))
        events.sort(key=lambda e: (e[0], e[1]))
        for _, _, kind, val in events:
            if kind == "text":
                t_raw, cols, bb = val
                m = QHEAD.search(t_raw)
                if m:
                    cur = {"n": int(m.group(1)), "qid": m.group(2), "page": pi + 1,
                           "stem": [], "options": [], "state": "head"}
                    questions.append(cur)
                    continue
                if cur is None:
                    head.append(norm(t_raw))
                    continue
                t = norm(t_raw)
                if cols == {BLUE}:
                    cur["note"] = norm(cur.get("note", "") + " " + t)
                elif t.startswith("Correct Marks"):
                    cur["marks"] = t
                    cur["state"] = "stem"
                elif t == "Options :":
                    cur["state"] = "options"
                elif OPTION_ID.match(t_raw) and cur["state"] == "options":
                    o = {"no": len(cur["options"]) + 1, "id": OPTION_ID.match(t_raw).group(1),
                         "colour": "green" if cols == {GREEN} else "red" if cols == {RED} else sorted(cols),
                         "icon": None, "img": None}
                    k = next(k for k, (lb, _) in enumerate(labels) if lb is bb)
                    for _, pk, pv in sorted(owned.get(k, [])):
                        if pk == "icon":
                            o["icon"] = pv
                        elif o["img"] is None:
                            o["img"] = pv
                        else:
                            o.setdefault("more", []).append(pv)
                    cur["options"].append(o)
            elif cur is not None and kind == "img" and cur["state"] == "stem":
                cur["stem"].append(val)
            elif cur is not None and kind == "img" and cur["options"] and cur["options"][-1]["img"] is None:
                # the ID is at the foot of one page and its picture at the
                # head of the next (Q41, option 3)
                cur["options"][-1]["img"] = val
            elif cur is not None and kind == "img":
                cur.setdefault("stray", []).append(val)

    problems = []
    if [q["n"] for q in questions] != list(range(1, 151)):
        problems.append("questions are not 1..150 in order")
    for q in questions:
        q.pop("state")
        withdrawn = IGNORED in q.get("note", "")
        greens = [o["no"] for o in q["options"] if o["colour"] == "green"]
        ticks = [o["no"] for o in q["options"] if o["icon"] == "tick"]
        if len(q["options"]) != 4:
            problems.append("Q%d has %d options" % (q["n"], len(q["options"])))
        for o in q["options"]:
            if o["img"] is None:
                problems.append("Q%d option %d has no picture" % (q["n"], o["no"]))
        if not q["stem"]:
            problems.append("Q%d has no stem picture" % q["n"])
        if q.get("stray"):
            problems.append("Q%d has pictures after Options that belong to no option: %s"
                            % (q["n"], q["stray"]))
        if withdrawn:
            q["key"] = None
            q["withdrawn"] = True
            if greens:
                problems.append("Q%d is withdrawn but an option is green" % q["n"])
        else:
            if len(greens) != 1 or greens != ticks:
                problems.append("Q%d: green %s, ticks %s" % (q["n"], greens, ticks))
            q["key"] = greens[0] if greens else None
    header = {}
    for k in HEADER:
        if k + " :" in head:
            header[k] = head[head.index(k + " :") + 1]
        else:
            problems.append("header field %r not found" % k)
    marks = {q["marks"] for q in questions}
    header["Marks per question"] = sorted(marks)
    return header, questions, problems


def render(pdf, questions, outdir):
    """One PNG per question, from its header to the next question's."""
    import fitz
    doc = fitz.open(pdf)
    os.makedirs(outdir, exist_ok=True)
    heads = []
    for pi, page in enumerate(doc):
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                m = QHEAD.search("".join(s["text"] for s in l["spans"]))
                if m:
                    heads.append((int(m.group(1)), pi, l["bbox"][1]))
    for k, (n, pi, y) in enumerate(heads):
        end = heads[k + 1] if k + 1 < len(heads) else (None, doc.page_count - 1, doc[-1].rect.height)
        parts = []
        for pj in range(pi, end[1] + 1):
            page = doc[pj]
            y0 = y if pj == pi else 0
            y1 = end[2] if pj == end[1] else page.rect.height
            if y1 - y0 > 4:
                parts.append(page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2),
                                             clip=fitz.Rect(35, y0, 560, y1)))
        for j, pix in enumerate(parts):
            pix.save(os.path.join(outdir, "q%03d%s.png" % (n, "" if j == 0 else chr(97 + j))))
    return len(heads)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pdf = args[0] if args else PDF
    header, questions, problems = extract(pdf)
    for p in problems:
        print("PROBLEM", p)
    if problems:
        raise SystemExit(1)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"header": header, "questions": questions}, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("wrote %s: %d questions, %d keys (colour and icon agree), withdrawn: %s"
          % (os.path.relpath(OUT, ROOT), len(questions), sum(1 for q in questions if q["key"]),
             [q["n"] for q in questions if q.get("withdrawn")]))
    if "--render" in sys.argv:
        out = os.path.join(os.environ.get("RENDER_DIR", "/tmp"), "appsc2022")
        print("rendered %d questions to %s" % (render(pdf, questions, out), out))


if __name__ == "__main__":
    main()
