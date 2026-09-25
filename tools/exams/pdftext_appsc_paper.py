# -*- coding: utf-8 -*-
"""Extract the APPSC 2025 Paper-II question paper into appsc_paper_2025.json.

    python3 pdftext_appsc_paper.py [PDF]     # default: docs/sources/appsc-aso-2025-paper-ii.pdf
    python3 pdftext_appsc_paper.py --render  # also write 4x PNGs of every image-printed item

The document is the Commission's "Question Paper Preview" of "Paper II
Subject", created 29 April 2025: 150 MCQs, each printed in English and then
in Telugu. Only the English block of each question is kept (the owner's
choice). The preview marks the answer it counts correct in two independent
ways, and both are read:

  * a tick icon beside the correct option (image xref TICK) and a cross
    beside each other one (xref CROSS);
  * the correct option's text in green (#008000), the others in red.

The key is taken from the tick. Where an option has text, its colour must
agree with its icon, and exactly one option per question must carry the
tick -- otherwise the build stops, because a key read wrongly would be
worse than none.

A few formulas and tables are printed as pictures, with no text behind them.
They were read off 4x renders of the page and are written out in IMAGES
below, each by the image's page and position, so a changed document fails
loudly rather than drifting. recheck_appsc_paper.py names the same images
independently and proves every other word against the PDF.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PDF = os.path.join(ROOT, "docs", "sources", "appsc-aso-2025-paper-ii.pdf")
OUT = os.path.join(HERE, "appsc_paper_2025.json")

# What the page may quote about the paper -- only what the paper says itself.
HEADER = ("Question Paper Name", "Creation Date", "Duration", "Total Marks",
          "Number of Questions", "Section Negative Marks")
GREEN, RED, BLACK, BLUE = 0x008000, 0xFF0000, 0x000000, 0x0000FF
QHEAD = re.compile(r"Question Number : (\d+) Question Id : (\d+)")
LABEL = re.compile(r"^\s*([1-4])\.\s*$")
# An option the Commission withdrew is printed without icons, number and
# text on one line.
INLINE = re.compile(r"^\s*([1-4])\.\s+(\S.*)$")
# The Commission's own notes are printed in blue. The one this paper carries
# withdraws a question; that, and only that, lets a question have no key.
IGNORED = "question is ignored for all candidates"
# A line that begins one of these starts a new line of the question; any
# other line is the paper's own line wrap and joins the one before it.
BREAK = re.compile(r"^\s*(?:[A-H][.)]\s|[IVX]+[.)]\s?|\(?[ivx]+[.)]|\(?[a-h]\)|\d+[.)]\s|•|"
                   r"Statement|Assertion|Reason|Conclusion|Column|List|LIST|Choose|Select|"
                   r"Options|Codes|Year|Class|Frequency|Match)")

# Images that carry question content, keyed "page:x0,y0" (page from 1).
# Each was read off a 4x render and is written as printed, words as words
# and mathematics in $...$ for MathJax. Nothing is corrected here: where the
# paper prints something odd (Q112's options say r(U,V)), it stays odd, and
# the solution says so.
IMAGES = {
    # Q33, option 2
    "13:111,297": r"$\dfrac{(\text{Price level in current period} - \text{price level in previous period})}"
                  r"{\text{price level in previous period}}$",
    # Q106, the four options
    "40:63,390": r"$\frac{1}{216}$",
    "40:63,413": r"$\frac{1}{36}$",
    "40:63,436": r"$\frac{1}{64}$",
    "40:63,459": r"$\frac{1}{108}$",
    # Q108, the two statements
    "41:45,150": r"Statement I: If two variables X and Y are independent then $r_{XY} = 0$",
    "41:43,161": r"Statement II: If $r_{XY} = 0$, then two variables X and Y are independent.",
    # Q109, the four options
    "41:63,475": r"$\frac{1}{5}$",
    "41:63,498": r"$\frac{2}{5}$",
    "41:63,522": r"$\frac{3}{5}$",
    "41:63,545": r"$\frac{4}{5}$",
    # Q111, the question
    "42:43,241": r"If $\mathrm{COV}(X,Y) = -16.5$, $\mathrm{Var}(X) = 2.89$ and $\mathrm{var}(Y) = 100$, "
                 r"then $r_{XY}$ is:",
    # Q112, the question
    "42:43,485": r"Let $r_{XY}$ be the coefficient of correlation between X and Y. If variable $U = 3X$ "
                 r"and variable $V = Y + 2$, then coefficient of correlation between U and V is:",
    # Q118, Column B item II
    "45:311,29": r"$\dfrac{\sum p_1 q_1}{\sum p_1 q_0}$ *100",
    # Q121, the question and option 1
    "46:43,126": r"For any two events A and B, $P(A \cup B)$ is equal to",
    "46:63,156": r"$P(A) + P(B)$",
    # Q126, the trend line and the four options
    "48:43,185": r"$Y_c = 30 + 3.6X$",
    "48:63,213": r"$Y_c = 2.5 + 0.025X$",
    "48:63,229": r"$Y_c = 25 + 0.25X$",
    "48:63,247": r"$Y_c = 0.25 + 0.25X$",
    "48:63,263": r"$Y_c = 30 + 0.025X$",
    # Q133, the question
    "50:43,690": r"If $X \sim N(0,1)$ and $Y = X^2$ then $r_{XY}$ is:",
    # Q135, the question and the four options
    "51:43,506": r"Given that X, Y and $Z = (X + 2Y)$ are variables such that $\mathrm{Var}(X) = 4$, "
                 r"$\mathrm{Var}(Y) = 3$ and $\mathrm{Var}(Z) = 4$, then $r_{XY}$ is:",
    "51:63,532": r"$\frac{2}{3}$",
    "51:63,556": r"$\frac{1}{3}$",
    "51:63,579": r"$-\frac{\sqrt{3}}{2}$",
    "51:63,605": r"$\frac{2}{\sqrt{3}}$",
}


def icon_xrefs(doc):
    """The two 16x16 icons used hundreds of times: the most and the second
    most repeated images. The tick is the rarer of the two (one per
    question), the cross the commoner (three per question)."""
    count = {}
    for p in doc:
        for i in p.get_image_info(xrefs=True):
            count[i["xref"]] = count.get(i["xref"], 0) + 1
    two = sorted(count, key=lambda x: -count[x])[:2]
    tick, cross = sorted(two, key=lambda x: count[x])
    return tick, cross


def stream(doc):
    """Every line and image, page by page, in the order the page holds them."""
    for pi, page in enumerate(doc):
        xref_at = {tuple(round(v) for v in i["bbox"]): i["xref"]
                   for i in page.get_image_info(xrefs=True)}
        for b in page.get_text("dict")["blocks"]:
            if b["type"] == 1:
                bb = tuple(round(v) for v in b["bbox"])
                yield {"kind": "img", "page": pi + 1, "bbox": bb, "xref": xref_at.get(bb)}
                continue
            for l in b["lines"]:
                text = "".join(s["text"] for s in l["spans"])
                colours = {s["color"] for s in l["spans"] if s["text"].strip()}
                yield {"kind": "text", "page": pi + 1, "text": text, "spans": l["spans"],
                       "bbox": tuple(round(v) for v in l["bbox"]), "colours": colours}


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def image_key(item):
    return "%d:%d,%d" % (item["page"], item["bbox"][0], item["bbox"][1])


# Where a table cell starts, and a run of spaces the paper uses as a tab.
GAP = 30
TAB = re.compile(r"(?:[ \xa0]{4,})")
MARK = re.compile(r"^\s*(?:[A-H]\s?[-.)]|[IVX]+[.)\s]|\(?[ivx]+[.)]|\(?[a-h]\)|\d+[.)]\s|Column|List|LIST)")
END = re.compile(r"^\s*(?:Choose|Select|Match the|The |Options|Codes)")


def segments(item):
    """A line as cells: [(x, text)], split where the paper leaves a gap."""
    if item["kind"] == "img":
        return [(item["bbox"][0], "[[%s]]" % image_key(item))]
    out = []
    for sp in item["spans"]:
        x = round(sp["bbox"][0])
        parts = TAB.split(sp["text"])
        for i, part in enumerate(parts):
            if out and i == 0 and x - out[-1][2] < GAP:
                out[-1] = (out[-1][0], out[-1][1] + part, round(sp["bbox"][2]))
            else:
                # a cell split out of the middle of one span has no x of its
                # own; it is the column after the one before it
                out.append((x if i == 0 else None, part, round(sp["bbox"][2])))
    return [(x, norm(t)) for x, t, _ in out if norm(t)]


def stem_parts(items):
    """The question's lines as parts: {"p": text}, {"table": rows}, {"img": key}.

    Lines sharing a baseline form one visual row. Two or more cells in a row
    start a table; after that each cell goes to the column nearest its x, a
    cell that opens with a row marker (A., (i), 1., ...) starts a new row when
    its column is already filled, and any other cell continues the one above
    it. A lone left-hand line that is not a marker ends the table."""
    rows = []
    for it in items:
        segs = segments(it)
        if not segs:
            continue
        y = it["bbox"][1]
        # text never joins a picture's row: Q108 prints its "." level with
        # the statement image, and merging dropped it
        if rows and rows[-1][0] == it["page"] and abs(rows[-1][1] - y) <= 2 and it["kind"] == "text" \
                and rows[-1][3] == "text":
            rows[-1][2].extend(segs)
        else:
            rows.append([it["page"], y, list(segs), it["kind"]])
    parts, cols, cur = [], None, None
    for page, y, segs, kind in rows:
        if kind == "img" and cols is None:
            parts.append({"img": segs[0][1][2:-2]})
            continue
        segs = sorted(segs, key=lambda s: -1 if s[0] is None else s[0]) if all(s[0] is not None for s in segs) else segs
        if cols is None:
            if len(segs) > 1:
                cols = [s[0] for s in segs]
                cur = [s[1] for s in segs]
                parts.append({"table": [cur]})
                continue
            t = segs[0][1]
            if parts and "p" in parts[-1] and not BREAK.match(t):
                parts[-1]["p"] += " " + t
            else:
                parts.append({"p": t})
            continue
        # in a table
        if len(segs) == 1 and segs[0][0] is not None and cols[0] is not None \
                and abs(segs[0][0] - cols[0]) < GAP and cur[0] and not MARK.match(segs[0][1]) \
                or END.match(segs[0][1]):
            cols = None
            parts.append({"p": segs[0][1]})
            continue
        placed = []
        for i, (x, t) in enumerate(segs):
            if x is None:
                c = min(len(cols) - 1, (placed[-1] if placed else 0) + 1)
            else:
                known = [(abs(x - cx), k) for k, cx in enumerate(cols) if cx is not None]
                c = min(known)[1] if known else i
                if known and min(known)[0] > GAP:
                    for k, cx in enumerate(cols):          # a column first seen here
                        if cx is None:
                            cols[k] = x
                            c = k
                            break
            placed.append(c)
        # a marker in a filled column starts a row; so does a full row of
        # cells arriving when every cell of the current one is filled (a
        # horizontal table: "Year 1941 1942 ..." then "Production 80 90 ...")
        if any(MARK.match(t) and cur[c] for (x, t), c in zip(segs, placed)) or \
                len(segs) == len(cols) and all(cur):
            cur = [""] * len(cols)
            parts[-1]["table"].append(cur)
        for (x, t), c in zip(segs, placed):
            cur[c] = (cur[c] + " " + t).strip()
    return parts


def extract(pdf=PDF):
    import fitz                                  # PyMuPDF
    doc = fitz.open(pdf)
    tick, cross = icon_xrefs(doc)
    questions, seen = [], set()
    cur = None
    head_lines = []
    for it in stream(doc):
        if not questions and it["kind"] == "text":
            head_lines.append(norm(it["text"]))
        if it["kind"] == "text":
            m = QHEAD.search(it["text"])
            if m:
                n = int(m.group(1))
                cur = None
                if n not in seen:          # the first block is English, the second Telugu
                    seen.add(n)
                    cur = {"n": n, "qid": m.group(2), "page": it["page"],
                           "stem": [], "options": [], "state": "head"}
                    questions.append(cur)
                continue
        if cur is None:
            continue
        if it["kind"] == "text":
            t = it["text"]
            if cur["state"] == "head":
                if t.startswith("Correct Marks"):
                    cur["marks"] = norm(t)
                    cur["state"] = "stem"
                continue
            if it["colours"] == {BLUE}:
                cur["note"] = norm(cur.get("note", "") + " " + t)
                continue
            if cur["state"] == "stem" and norm(t) == "Options :":
                cur["state"] = "options"
                continue
            if cur["state"] == "options":
                m = LABEL.match(t)
                if m:
                    cur["options"].append({"no": int(m.group(1)), "text": "", "icon": None,
                                           "colours": set(it["colours"]), "img": []})
                    continue
                m = INLINE.match(t)
                if m and not cur["options"] or m and cur["options"][-1]["no"] == int(m.group(1)) - 1 \
                        and cur["options"][-1]["icon"] is None and cur["options"][-1]["text"]:
                    cur["options"].append({"no": int(m.group(1)), "text": norm(m.group(2)), "icon": None,
                                           "colours": set(it["colours"]), "img": []})
                    continue
                if cur["options"] and norm(t):
                    o = cur["options"][-1]
                    o["text"] = norm(o["text"] + " " + t)
                    o["colours"] |= it["colours"]
                continue
            cur.setdefault("raw", []).append(it)
        else:
            if cur["state"] == "options" and cur["options"]:
                o = cur["options"][-1]
                if it["xref"] in (tick, cross) and o["icon"] is None:
                    o["icon"] = "tick" if it["xref"] == tick else "cross"
                else:
                    # kept where it sits: Q33's fraction is between
                    # "Inflation rate =" and "*100"
                    o["img"].append(image_key(it))
                    o["text"] = (o["text"] + " [[%s]]" % image_key(it)).strip()
            elif cur["state"] == "stem":
                cur.setdefault("raw", []).append(it)

    problems = []
    for q in questions:
        q["stem"] = stem_parts(q.pop("raw", []))
        q.pop("state")
        ticks = [o["no"] for o in q["options"] if o["icon"] == "tick"]
        if len(q["options"]) != 4:
            problems.append("Q%d has %d options" % (q["n"], len(q["options"])))
        withdrawn = IGNORED in q.get("note", "").replace("So,this", "So, this")
        if withdrawn:
            if ticks:
                problems.append("Q%d is withdrawn but has a ticked option" % q["n"])
        elif len(ticks) != 1:
            problems.append("Q%d has %d ticked options" % (q["n"], len(ticks)))
        q["key"] = ticks[0] if ticks else None
        for o in q["options"]:
            col = o.pop("colours") - {BLACK}
            if o["text"].strip() and not withdrawn:
                want = GREEN if o["icon"] == "tick" else RED
                if col != {want}:
                    problems.append("Q%d option %d: icon %s but text colour %s"
                                    % (q["n"], o["no"], o["icon"], sorted(hex(c) for c in col)))
            if not o["img"]:
                o.pop("img")
    if len(questions) != 150:
        problems.append("%d questions, not 150" % len(questions))
    # The paper's own header: "Duration :" on one line, "150" on the next.
    header = {}
    for k in HEADER:
        i = head_lines.index(k + " :") if k + " :" in head_lines else -1
        if i < 0 or i + 1 >= len(head_lines):
            problems.append("header field %r not found" % k)
        else:
            header[k] = head_lines[i + 1]
    return header, questions, problems


def render(pdf, questions, outdir):
    import fitz
    doc = fitz.open(pdf)
    os.makedirs(outdir, exist_ok=True)
    keys = set()
    for q in questions:
        for p in q["stem"]:
            if "img" in p:
                keys.add(p["img"])
        for o in q["options"]:
            keys.update(o.get("img", []))
    for k in sorted(keys):
        page, xy = k.split(":")
        page = doc[int(page) - 1]
        for i in page.get_image_info(xrefs=True):
            bb = [round(v) for v in i["bbox"]]
            if "%d,%d" % (bb[0], bb[1]) == xy:
                r = fitz.Rect(i["bbox"]) + (-3, -3, 3, 3)
                pix = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=r)
                pix.save(os.path.join(outdir, k.replace(":", "_").replace(",", "_") + ".png"))
    return sorted(keys)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pdf = args[0] if args else PDF
    header, questions, problems = extract(pdf)
    if problems:
        for p in problems:
            print("PROBLEM", p)
        raise SystemExit(1)
    unread = []
    for q in questions:
        for part in q["stem"]:
            for row in part.get("table", []):
                for cell in row:
                    for k in re.findall(r"\[\[([^\]]+)\]\]", cell):
                        if IMAGES.get(k) is None:
                            unread.append((q["n"], k))
        for part in q["stem"]:
            if "img" in part:
                part["as"] = IMAGES.get(part["img"])
                if part["as"] is None:
                    unread.append((q["n"], part["img"]))
        for o in q["options"]:
            for k in o.pop("img", []):
                if IMAGES.get(k) is None:
                    unread.append((q["n"], k))
    if "--render" in sys.argv:
        out = os.path.join(os.environ.get("RENDER_DIR", "/tmp"), "appsc_images")
        print("rendered %d images to %s" % (len(render(pdf, questions, out)), out))
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"header": header, "images": IMAGES, "questions": questions},
                  fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("wrote %s: %d questions, key read for %d, %d image items unread"
          % (os.path.relpath(OUT, ROOT), len(questions),
             sum(1 for q in questions if q["key"]), len(unread)))
    for n, k in unread:
        print("   unread image  Q%d  %s" % (n, k))


if __name__ == "__main__":
    main()
