# -*- coding: utf-8 -*-
"""Pull the text out of a PDF, without poppler.

This container has no pdftotext, no working pypdf (its _cffi_backend is
missing) and no OCR, so the maps that are built from official PDFs need their
own extractor. It handles the one case those documents actually use: a Word
file printed to PDF, whose fonts are subset TrueType with CID-keyed glyph
codes rather than ASCII.

Two decoding paths, in order:

1. The font's own /ToUnicode CMap, when it has one. That is authoritative.
2. Microsoft's subset glyph ordering, when it does not -- glyph 3 is a space
   and the printable ASCII range follows it in order. Wrong for a font that
   was subset differently, which is why path 1 is tried first and why anything
   built from this output is checked back against it by a recheck script.

Used by asrb_map_data.py, and by recheck_asrb.py to prove that every syllabus
line printed on the finished page really is in the document it claims.

    python3 pdftext.py FILE.pdf          # text, one block per page
"""
import re
import sys
import zlib

# Microsoft subset ordering: glyph 3 is space, printable ASCII follows.
STD_ORDER = (" !\"#$%&'()*+,-./0123456789:;<=>?@"
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"
             "abcdefghijklmnopqrstuvwxyz{|}~")
FIRST_GLYPH = 3


def _objects(data):
    """Every `N 0 obj ... endobj` in the file, by number."""
    return {int(m.group(1)): m.group(2)
            for m in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", data, re.S)}


def _stream(objs, num):
    """The decompressed stream of one object, or b'' if it has none."""
    body = objs.get(num, b"")
    m = re.search(rb"stream\r?\n(.*?)endstream", body, re.S)
    if not m:
        return b""
    raw = m.group(1)
    if b"/FlateDecode" in body:
        try:
            return zlib.decompress(raw)
        except zlib.error:
            return b""
    return raw


def _tounicode(objs):
    """Every /ToUnicode CMap in the file, merged into one code -> text map.

    Merging rather than tracking which font is current: these documents set
    one text font and the glyph codes do not collide in practice. A collision
    would show up as garbled words, which the recheck would catch.
    """
    out = {}
    for num in objs:
        cmap = _stream(objs, num)
        if b"beginbfchar" not in cmap and b"beginbfrange" not in cmap:
            continue
        text = cmap.decode("latin-1")
        for block in re.findall(r"beginbfchar(.*?)endbfchar", text, re.S):
            for src, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block):
                out[int(src, 16)] = "".join(
                    chr(int(dst[i:i + 4], 16)) for i in range(0, len(dst), 4))
        for block in re.findall(r"beginbfrange(.*?)endbfrange", text, re.S):
            for lo, hi, dst in re.findall(
                    r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block):
                lo, hi, base = int(lo, 16), int(hi, 16), int(dst, 16)
                for i in range(hi - lo + 1):
                    out[lo + i] = chr(base + i)
    return out


def _glyph(code, unimap):
    if code in unimap:
        return unimap[code]
    i = code - FIRST_GLYPH
    return STD_ORDER[i] if 0 <= i < len(STD_ORDER) else ""


def _content_ids(page_body):
    """/Contents, whether it is one reference or an array of them."""
    m = re.search(rb"/Contents\s*(?:\[([^\]]*)\]|(\d+)\s+0\s+R)", page_body)
    if not m:
        return []
    if m.group(1):
        return [int(x) for x in re.findall(rb"(\d+)\s+0\s+R", m.group(1))]
    return [int(m.group(2))]


def page_texts(path):
    """The text of each page, in document order."""
    data = open(path, "rb").read()
    objs = _objects(data)
    unimap = _tounicode(objs)
    pages = sorted(n for n, b in objs.items()
                   if re.search(rb"/Type\s*/Page[^s]", b))
    out = []
    for num in pages:
        body = b"".join(_stream(objs, c) for c in _content_ids(objs[num]))
        text = body.decode("latin-1")
        chars = []
        for m in re.finditer(r"\[(.*?)\]\s*TJ|<([0-9A-Fa-f]+)>\s*Tj|(T\*|Td|TD)",
                             text, re.S):
            if m.group(3):                      # a line or position move
                chars.append("\n")
                continue
            if m.group(1) is not None:
                codes = re.findall(r"<([0-9A-Fa-f]+)>", m.group(1))
            else:
                codes = [m.group(2)]
            for hexstr in codes:
                for i in range(0, len(hexstr), 4):
                    chars.append(_glyph(int(hexstr[i:i + 4], 16), unimap))
        out.append(re.sub(r"\n{2,}", "\n", "".join(chars)))
    return out


def flat_text(path):
    """Every page joined and whitespace collapsed -- what a recheck greps."""
    joined = " ".join(page_texts(path))
    return re.sub(r"\s+", " ", joined).strip()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: pdftext.py FILE.pdf")
    for i, page in enumerate(page_texts(sys.argv[1]), 1):
        print("=============== PAGE %d ===============" % i)
        print(page)
