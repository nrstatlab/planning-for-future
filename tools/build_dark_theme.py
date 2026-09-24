#!/usr/bin/env python3
"""Derive a dark theme for the whole site from the stylesheets it already has.

    python3 tools/build_dark_theme.py          # dry run: what it would map
    python3 tools/build_dark_theme.py --apply  # write assets/site-dark.css

WHY GENERATED. The site paints its surfaces in five stylesheets and a dozen
inline <style> blocks -- about 150 background declarations and 200 distinct
colours. A hand-written dark theme would be a sixth copy of all of them, and
would silently fall behind the first time any section sheet changed. This
reads every rule that sets a colour and writes the same selector back, inside
`@media (prefers-color-scheme: dark)`, with the colour moved to the dark side:

  * a LIGHT background or border becomes a dark one of the same hue;
  * a DARK text colour becomes a light one of the same hue;
  * everything already right for a dark page -- white text on the blue
    banners, a dark badge behind white text -- is left exactly as it is.

Same selector, linked later, so each override wins by order and nothing
needs !important. var(--token) references are resolved against the sheet's
own :root before deciding, so `color: var(--ink)` is mapped as the dark ink it
is, while the tokens themselves are left alone (a token like the brand blue is
a text colour in one rule and a badge background in the next).

Whether the result is READABLE is not decided here. tools/check_contrast.js
loads pages in a dark-scheme browser and measures every text element against
the background actually painted behind it; this generator is only trusted
because that check passes.
"""
import argparse
import colorsys
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from stubs import is_stub  # noqa: E402

OUT = ROOT / "assets" / "site-dark.css"

# One representative of each distinct sheet (the subject sheet has 22 identical
# copies; their md5 is asserted equal elsewhere), plus site-base.css itself.
SHEETS = [
    "assets/nrstatlab.css",
    "statistics/bsc/descriptive-statistics/css/styles.css",
    "data-science/css/styles.css",
    "exams/ugc-net/styles.css",
    "data-science/machine-learning/self-study-notes/css/styles.css",
    "statistics/msc/css/styles.css",
    "assets/site-base.css",
]

COLOR_PROPS = {"color", "background", "background-color", "border", "border-color",
               "border-top", "border-bottom", "border-left", "border-right",
               "border-top-color", "border-bottom-color", "border-left-color",
               "border-right-color", "outline-color", "text-decoration-color",
               "fill", "stroke", "caret-color"}
TEXT_PROPS = {"color", "fill", "caret-color", "text-decoration-color"}

NAMED = {"white": "#ffffff", "black": "#000000", "#fff": "#ffffff", "#000": "#000000"}
COLOUR = re.compile(r"#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|"
                    r"rgba?\([^)]*\)|\bwhite\b|\bblack\b")
VAR = re.compile(r"var\((--[\w-]+)(?:,\s*([^)]+))?\)")


# ---------------------------------------------------------------- colour maths
def parse(c):
    """(r, g, b, a) in 0..1 for a CSS colour literal, or None."""
    c = NAMED.get(c.lower(), c)
    if c.startswith("#"):
        h = c[1:]
        if len(h) == 3:
            h = "".join(x * 2 for x in h)
        a = 1.0
        if len(h) == 8:
            a = int(h[6:8], 16) / 255
            h = h[:6]
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)
    m = re.match(r"rgba?\(([^)]*)\)", c)
    if m:
        parts = [p.strip() for p in re.split(r"[,\s/]+", m.group(1)) if p.strip()]
        try:
            rgb = [float(p.rstrip("%")) / (100 if p.endswith("%") else 255) for p in parts[:3]]
            a = float(parts[3].rstrip("%")) / (100 if parts[3].endswith("%") else 1) \
                if len(parts) > 3 else 1.0
        except (ValueError, IndexError):
            return None
        return tuple(rgb) + (a,)
    return None


def lum(rgb):
    def ch(x):
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def fmt(r, g, b, a):
    r, g, b = (max(0, min(255, round(x * 255))) for x in (r, g, b))
    if a >= 0.999:
        return f"#{r:02x}{g:02x}{b:02x}"
    return f"rgba({r}, {g}, {b}, {round(a, 3)})"


BRAND_HUE = colorsys.rgb_to_hls(0x0f / 255, 0x4c / 255, 0x81 / 255)[0]


def to_dark_surface(c, border=False):
    """A light background (or border) -> a dark one of the same hue."""
    r, g, b, a = c
    if lum(c) < 0.35:
        return None                        # already dark enough to sit behind light text
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if border:
        nl = 0.22 + (1 - l) * 0.5
    else:
        nl = 0.13 + (1 - l) * 0.5          # white -> 13%, a pale tint -> ~14-16%
    ns = min(s, 0.42)
    if s < 0.08:
        # White and the near-greys: give them the brand's hue, faintly, so a
        # card reads as part of the same dark page rather than a grey hole.
        h, ns = BRAND_HUE, 0.28
    return fmt(*colorsys.hls_to_rgb(h, nl, ns), a)


def to_light_text(c):
    """A dark text colour -> a light one of the same hue."""
    r, g, b, a = c
    if lum(c) >= 0.3:
        return None                        # already light: white on a banner, say
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    nl = 0.90 - l * 0.30                   # black -> 90%, the brand blue -> ~82%
    ns = min(s, 0.65)
    return fmt(*colorsys.hls_to_rgb(h, nl, ns), a)


# ----------------------------------------------------------------- CSS reading
COMMENT = re.compile(r"/\*.*?\*/", re.S)


def blocks(css):
    """Yield (media or None, selector, body) for every plain rule, one level of
    @media deep. @keyframes, @font-face and print styles are skipped."""
    css = COMMENT.sub("", css)
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        head = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        body = css[j + 1:k - 1]
        if head.startswith("@media"):
            if "print" not in head:
                for _, sel, b in blocks(body):
                    yield head, sel, b
        elif not head.startswith("@"):
            yield None, head, body
        i = k


def decls(body):
    for d in body.split(";"):
        if ":" in d:
            p, v = d.split(":", 1)
            yield p.strip().lower(), v.strip()


def tokens_of(css):
    toks = {}
    for media, sel, body in blocks(css):
        if media is None and sel.strip() == ":root":
            for p, v in decls(body):
                if p.startswith("--"):
                    toks[p] = v
    return toks


def resolve(value, toks):
    for _ in range(4):
        new = VAR.sub(lambda m: toks.get(m.group(1), m.group(2) or m.group(0)), value)
        if new == value:
            break
        value = new
    return value


# Rules that are already dark by design, or that the chrome's own sheet owns.
SKIP_SEL = re.compile(r"\.sitenav|\.sitefoot|\.nav-skip|::selection|:root")


def map_decl(prop, value, toks):
    """The dark-mode value for one declaration, or None to leave it alone."""
    if prop not in COLOR_PROPS:
        return None
    value = resolve(value, toks)
    changed = False

    def sub(m):
        nonlocal changed
        c = parse(m.group(0))
        if c is None or c[3] == 0:
            return m.group(0)
        if prop in TEXT_PROPS:
            new = to_light_text(c)
        else:
            new = to_dark_surface(c, border=prop.startswith("border") or prop == "outline-color")
        if new is None:
            return m.group(0)
        changed = True
        return new
    out = COLOUR.sub(sub, value)
    if "var(" in out:
        return None                        # an unresolved token: cannot judge it
    return out if changed else None


def inline_styles():
    """Every distinct <style> block on a real page (the hubs and the maps)."""
    seen = {}
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts or "archive" in p.parts or is_stub(p):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("data-science/labs/"):
            continue
        for m in re.finditer(r"<style[^>]*>(.*?)</style>", p.read_text(errors="replace"), re.S):
            css = m.group(1).replace("{{", "{").replace("}}", "}")
            seen.setdefault(css, rel)
    return [(src, css) for css, src in seen.items()]


def style_attributes():
    """Distinct colour declarations written in style="..." attributes.

    66 uses of 22 declarations, on hand-written pages -- a caution box painted
    `background:#fffbe6` in the markup, say. An inline style beats any rule in
    a stylesheet, so these are matched by attribute and overridden with
    !important, the one place this file needs it. SVG is left out: diagrams
    keep their light panel (see dark_theme_extra.css).
    """
    found = set()
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts or "archive" in p.parts or is_stub(p):
            continue
        if p.relative_to(ROOT).as_posix().startswith("data-science/labs/"):
            continue
        text = re.sub(r"<svg\b.*?</svg>", "", p.read_text(errors="replace"), flags=re.S)
        for st in re.findall(r'<(?!svg)[a-z][a-z0-9]*[^>]*\sstyle="([^"]*)"', text):
            for d in st.split(";"):
                d = d.strip()
                if ":" in d and (COLOUR.search(d) or "var(--" in d):
                    found.add(d)
    return sorted(found)


def build():
    sources = [(s, (ROOT / s).read_text()) for s in SHEETS if (ROOT / s).exists()]
    sources += [(f"<style> on {src}", css) for src, css in inline_styles()]
    base_toks = tokens_of((ROOT / "assets" / "site-base.css").read_text())
    # An inline <style> block on a UGC NET page writes var(--text), a token
    # only the UGC NET sheet defines -- so blocks resolve against every sheet's
    # tokens, not just their own.
    all_toks = {}
    for src_name in SHEETS:
        f = ROOT / src_name
        if f.exists():
            all_toks.update(tokens_of(f.read_text()))
    all_toks.update(base_toks)
    out, count = [], 0
    for src, css in sources:
        # Resolve tokens the way the browser will: the sheet's own, then any
        # site-base.css redefines on top (it is linked later, so it wins --
        # UGC NET's --accent is #f59e0b in its sheet and #b45309 on the page).
        toks = dict(all_toks) if src.startswith("<style>") else {}
        toks.update(tokens_of(css))
        toks.update(base_toks)
        rules = []
        for media, sel, body in blocks(css):
            if SKIP_SEL.search(sel):
                continue
            mapped = []
            for p, v in decls(body):
                nv = map_decl(p, v, toks)
                if nv is not None:
                    mapped.append(f"{p}: {nv}")
            if mapped:
                rule = f"  {sel} {{ {'; '.join(mapped)}; }}"
                if media:
                    rule = f"  {media} {{ {sel} {{ {'; '.join(mapped)}; }} }}"
                rules.append(rule)
        if rules:
            count += len(rules)
            out.append(f"  /* from {src} */")
            out.extend(rules)
    attrs = []
    for d in style_attributes():
        prop, val = (x.strip() for x in d.split(":", 1))
        nv = map_decl(prop.lower(), val, all_toks)
        if nv is not None:
            sel = '[style*="%s"]' % d.replace('"', '\\"')
            attrs.append(f"  {sel} {{ {prop}: {nv} !important; }}")
    if attrs:
        out.append("  /* from style=\"...\" attributes on hand-written pages */")
        out.extend(attrs)
        count += len(attrs)
    return out, count, len(sources)


HEADER = """/* GENERATED by tools/build_dark_theme.py -- do not edit; edit the sheets it
   reads, then re-run it. It maps every colour rule on the site to the dark
   side, same selector, so each override wins by being linked later. Whether
   the result is readable is checked, not assumed: tools/check_contrast.js. */
@media (prefers-color-scheme: dark) {
  :root { color-scheme: dark; }
"""


def main(apply):
    rules, count, nsrc = build()
    css = HEADER + "\n".join(rules) + "\n" + (ROOT / "tools" / "dark_theme_extra.css").read_text() + "}\n"
    print(f"{nsrc} stylesheets and <style> blocks read, {count} rules mapped, "
          f"{len(css):,} bytes")
    if apply:
        OUT.write_text(css)
        print("wrote", OUT.relative_to(ROOT))
    else:
        print("dry run -- pass --apply to write")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    main(ap.parse_args().apply)
