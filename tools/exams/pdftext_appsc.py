# -*- coding: utf-8 -*-
"""The PDF text extractor the APPSC recheck was written against.

TWO EXTRACTORS LIVE HERE ON PURPOSE. pdftext.py is a later, better-documented
rewrite used by the ASRB map. It is NOT a drop-in replacement for this one:
the two disagree about whitespace between text runs, so where this module
yields "SERVICE (General Recruitment) 1. Application", pdftext.py yields
"SERVICE(General Recruitment)1.Application". recheck_appsc.py compares word
sequences, so swapping them silently changes what its 155 checks mean.

Unifying them is real work with a real risk of weakening that recheck, and it
is not what tracking these generators was for. Until someone does it properly
-- and re-proves the 155 checks against the notifications -- both stay.
"""
import re, sys, zlib


def _load(path):
    d = open(path, "rb").read()
    pos = {}
    for m in re.finditer(rb"(?:^|[^0-9])(\d+)\s+(\d+)\s+obj\b", d):
        pos[int(m.group(1))] = m.end()
    return d, pos


def _body(d, pos, n):
    if n not in pos:
        return b""
    s = pos[n]
    e = d.find(b"endobj", s)
    return d[s:e if e > 0 else s + 4000]


def _stream(d, pos, n):
    b = _body(d, pos, n)
    i = b.find(b"stream")
    if i < 0:
        return None
    j = b.find(b"\n", i) + 1
    for end in (len(b), b.find(b"endstream", j)):
        try:
            return zlib.decompress(b[j:end])
        except Exception:
            pass
    return None


def _cmap(raw):
    mp = {}
    if not raw:
        return mp
    for blk in re.findall(rb"beginbfchar(.*?)endbfchar", raw, re.S):
        for a, bb in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            mp[int(a, 16)] = "".join(chr(int(bb[i:i + 4], 16))
                                     for i in range(0, len(bb), 4))
    for blk in re.findall(rb"beginbfrange(.*?)endbfrange", raw, re.S):
        for a, bb, c in re.findall(
                rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            lo, hi, st = int(a, 16), int(bb, 16), int(c, 16)
            for i in range(hi - lo + 1):
                mp[lo + i] = chr(st + i)
    return mp


def pages(path):
    """One string per page, in document order."""
    d, pos = _load(path)
    page_objs = [n for n in sorted(pos)
                 if re.search(rb"/Type\s*/Page[^s]", _body(d, pos, n))]
    out = []
    for pn in page_objs:
        pb = _body(d, pos, pn)
        fonts = {}
        fm = re.search(rb"/Font\s*<<(.*?)>>", pb, re.S)
        if fm:
            for name, num in re.findall(rb"/(\w+)\s+(\d+)\s+0\s+R", fm.group(1)):
                fb = _body(d, pos, int(num))
                tu = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", fb)
                fonts[name.decode()] = _cmap(_stream(d, pos, int(tu.group(1)))) if tu else {}
        cm = re.search(rb"/Contents\s+(\d+)\s+0\s+R", pb)
        if not cm:
            out.append("")
            continue
        raw = _stream(d, pos, int(cm.group(1)))
        if not raw:
            out.append("")
            continue
        cur, buf = {}, []
        for t in re.finditer(
                rb"/(\w+)\s+[\d.]+\s+Tf"
                rb"|\[((?:[^\[\]]|\\.)*)\]\s*TJ"
                rb"|<([0-9A-Fa-f]+)>\s*Tj"
                rb"|\(((?:[^()\\]|\\.)*)\)\s*Tj"
                rb"|(T\*|Td|TD)", raw):
            if t.group(1):
                cur = fonts.get(t.group(1).decode(), {})
            elif t.group(2) is not None:
                seg = ""
                for piece in re.finditer(
                        rb"<([0-9A-Fa-f]+)>|\(((?:[^()\\]|\\.)*)\)|(-?\d+)", t.group(2)):
                    if piece.group(1):
                        h = piece.group(1)
                        seg += "".join(cur.get(int(h[i:i + 4], 16), "")
                                       for i in range(0, len(h), 4))
                    elif piece.group(2) is not None:
                        seg += piece.group(2).decode("latin-1")
                    elif int(piece.group(3)) < -180:
                        seg += " "
                buf.append(seg)
            elif t.group(3):
                h = t.group(3)
                buf.append("".join(cur.get(int(h[i:i + 4], 16), "")
                                   for i in range(0, len(h), 4)))
            elif t.group(4) is not None:
                buf.append(t.group(4).decode("latin-1"))
            else:
                buf.append("\n")
        out.append("".join(buf))
    return out


if __name__ == "__main__":
    for i, p in enumerate(pages(sys.argv[1]), 1):
        print("\n=============== PAGE %d ===============" % i)
        print(re.sub(r"\n{2,}", "\n", p))
