#!/usr/bin/env python3
"""Extract page-referenced text from the Data Science Major syllabus PDF.

Written because neither pdftotext nor pypdf is available in this environment.
Uses only the standard library (re + zlib).

Important: two pages of this PDF (16 and 25) reference their content as an
*indirect array* of streams -- /Contents 118 0 R where object 118 is
"[71 0 R 119 0 R]" -- rather than pointing at a stream directly. A naive
extractor returns those pages blank and silently drops DBMS Units 2-5 and the
Python textbook list. resolve_contents() below handles both forms.

Usage: python3 tools/extract_syllabus.py <input.pdf> > docs/syllabus-extracted.md
"""
import re
import sys
import zlib

OBJ_RE = re.compile(rb"(\d+)\s+0\s+obj\r?\n?(.*?)endobj", re.S)
STREAM_RE = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.S)
REF_RE = re.compile(rb"(\d+)\s+0\s+R")
TEXT_OP_RE = re.compile(rb"\[(.*?)\]\s*TJ|\((.*?)\)\s*Tj|T\*", re.S)
LITERAL_RE = re.compile(rb"\((.*?)(?<!\\)\)", re.S)

ESCAPES = {b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b",
           b"f": b"\f", b"(": b"(", b")": b")", b"\\": b"\\"}


def load_objects(data):
    return {int(m.group(1)): m.group(2) for m in OBJ_RE.finditer(data)}


def stream_of(objs, num):
    """Decompressed stream bytes of object `num`, or b'' if it has none."""
    body = objs.get(num, b"")
    m = STREAM_RE.search(body)
    if not m:
        return b""
    raw = m.group(1)
    if b"FlateDecode" not in body:
        return raw
    try:
        return zlib.decompress(raw)
    except zlib.error:
        try:
            return zlib.decompressobj().decompress(raw)
        except zlib.error:
            return b""


def resolve_contents(objs, page_body):
    """Concatenated content streams for a page.

    Handles /Contents N 0 R pointing at a stream, /Contents [A 0 R B 0 R]
    inline, and /Contents N 0 R where N is itself an array of stream refs.
    """
    inline = re.search(rb"/Contents\s*\[(.*?)\]", page_body, re.S)
    if inline:
        refs = [int(n) for n in REF_RE.findall(inline.group(1))]
    else:
        single = re.search(rb"/Contents\s+(\d+)\s+0\s+R", page_body)
        if not single:
            return b""
        num = int(single.group(1))
        body = objs.get(num, b"")
        # An indirect array of streams rather than a stream itself.
        if STREAM_RE.search(body) is None and b"[" in body:
            refs = [int(n) for n in REF_RE.findall(body)]
        else:
            refs = [num]
    return b"".join(stream_of(objs, n) for n in refs)


def unescape(s):
    out = bytearray()
    i = 0
    while i < len(s):
        if s[i:i + 1] != b"\\":
            out += s[i:i + 1]
            i += 1
            continue
        nxt = s[i + 1:i + 2]
        if nxt in ESCAPES:
            out += ESCAPES[nxt]
            i += 2
        elif nxt.isdigit():
            try:
                out.append(int(s[i + 1:i + 4], 8))
                i += 4
            except ValueError:
                i += 2
        else:
            i += 2
    return bytes(out)


def extract_text(content):
    parts = []
    for m in TEXT_OP_RE.finditer(content):
        if m.group(1) is not None:
            parts.append(b"".join(unescape(p) for p in LITERAL_RE.findall(m.group(1))))
        elif m.group(2) is not None:
            parts.append(unescape(m.group(2)))
        else:
            parts.append(b"\n")
    text = b"".join(parts).decode("latin-1")
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]{2,}", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def page_order(data):
    kids = re.search(rb"/Count\s*\d+\s*/Kids\s*\[(.*?)\]", data, re.S)
    return [int(n) for n in REF_RE.findall(kids.group(1))] if kids else []


def main():
    path = sys.argv[1]
    with open(path, "rb") as fh:
        data = fh.read()
    objs = load_objects(data)
    pages = page_order(data)

    print("# B.Sc. (Data Science) Major — extracted syllabus text\n")
    print(f"Source: `{path}` — {len(pages)} pages.")
    print("Extracted verbatim so every claim in the notes is traceable to a page.")
    print("Regenerate with `python3 tools/extract_syllabus.py <pdf>`.\n")
    blank = []
    for i, num in enumerate(pages, 1):
        text = extract_text(resolve_contents(objs, objs.get(num, b"")))
        if not text:
            blank.append(i)
        print(f"\n## Page {i}\n")
        print(text if text else "_(no extractable text on this page)_")
    if blank:
        print(f"\n<!-- pages with no extractable text: {blank} -->", file=sys.stderr)


if __name__ == "__main__":
    main()
