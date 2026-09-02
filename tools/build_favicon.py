#!/usr/bin/env python3
"""Write favicon.ico and favicon.svg.

Every browser asks for /favicon.ico whether or not a page links one, so with no
icon in the repository every visit fired a 404 at the error page and every tab
showed a blank glyph. The .ico is what browsers fetch on their own, so it alone
fixes all 594 pages without editing any of them; the .svg is there for anything
that prefers it.

The mark is three ascending bars -- the histogram on the home page's own card --
in white on the site's blue.
"""
import pathlib
import struct
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLUE = (15, 76, 129)          # #0f4c81, the site's blue
WHITE = (255, 255, 255)
N = 32                        # the size browsers ask for


def pixels():
    """32x32 RGBA rows: three ascending bars on a solid ground."""
    bars = [(6, 12, 20), (13, 19, 15), (20, 26, 9)]    # x0, x1, top; all end at 27
    rows = []
    for y in range(N):
        row = bytearray()
        for x in range(N):
            rgb = BLUE
            for x0, x1, top in bars:
                if x0 <= x < x1 and top <= y < 27:
                    rgb = WHITE
            row += bytes(rgb) + b"\xff"
        rows.append(bytes(row))
    return rows


def png(rows):
    raw = b"".join(b"\x00" + r for r in rows)          # filter byte per scanline
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", N, N, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def ico(png_bytes):
    """An ICO whose single image is a PNG -- accepted by every current browser."""
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", N, N, 0, 0, 1, 32, len(png_bytes), 22)
    return header + entry + png_bytes


SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#0f4c81"/>
  <rect x="6"  y="20" width="6" height="7"  fill="#fff"/>
  <rect x="13" y="15" width="6" height="12" fill="#fff"/>
  <rect x="20" y="9"  width="6" height="18" fill="#fff"/>
</svg>
"""

def main():
    data = png(pixels())
    (ROOT / "favicon.ico").write_bytes(ico(data))
    (ROOT / "favicon.png").write_bytes(data)
    (ROOT / "favicon.svg").write_text(SVG)
    print(f"favicon.ico {len(ico(data))}B, favicon.png {len(data)}B, favicon.svg")


if __name__ == "__main__":
    main()
