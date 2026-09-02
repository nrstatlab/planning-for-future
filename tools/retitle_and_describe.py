#!/usr/bin/env python3
"""Put the topic first in every hand-written page's title, and give it a description.

The generated Data Science pages get this from build_site.py. The Statistics,
UGC NET and self-study pages are hand-written HTML, so they get it here -- from
the SAME rules, imported rather than restated, so the two halves of the site
cannot drift apart.

Run with --apply to write; without it, this only reports.
"""
import html as html_mod
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Reuse the generator's own title rules -- audit_content.py loads build_site.py
# the same way, so this is the established pattern in this repository.
_spec = importlib.util.spec_from_file_location(
    "_bs", ROOT / "data-science-major" / "tools" / "build_site.py")
_bs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bs)
topic_first, add_acronyms, SITE_BASE = _bs.topic_first, _bs.add_acronyms, _bs.SITE_BASE

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
BANNER_RE = re.compile(
    r'<div class="banner">.*?<h1[^>]*>(.*?)</h1>\s*(?:<p>(.*?)</p>)?', re.S)
FIRST_P_RE = re.compile(r"<p>(.*?)</p>", re.S)


def plain(text):
    """Tag-free, entity-free, whitespace-collapsed."""
    return " ".join(html_mod.unescape(re.sub(r"<[^>]+>", " ", text)).split())


def shorten(text, limit=160):
    """Cut at a clause boundary near the length a search result displays."""
    text = plain(text)
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for sep in ("; ", ", ", " "):
        if sep in cut:
            cut = cut.rsplit(sep, 1)[0]
            break
    return cut.rstrip(" ,;—-") + "…"


def new_title(old):
    """Apply the topic-first rule to a '<left> | <subject>' title."""
    old = plain(old)
    if "|" not in old:
        return add_acronyms(old)
    left, _, subject = old.partition("|")
    return topic_first(left, subject)


def describe(text):
    """The banner sub-line if there is one, else the first real paragraph."""
    m = BANNER_RE.search(text)
    if m and m.group(2) and plain(m.group(2)):
        return shorten(m.group(2))
    body = text.split("</div>", 1)[-1]
    for p in FIRST_P_RE.finditer(body):
        candidate = plain(p.group(1))
        if len(candidate) > 40:
            return shorten(candidate)
    return ""


def meta_block(title, desc, url_path):
    d = html_mod.escape(desc, quote=True)
    t = html_mod.escape(title, quote=True)
    return (f'<meta name="description" content="{d}">\n'
            f'<meta property="og:title" content="{t}">\n'
            f'<meta property="og:description" content="{d}">\n'
            f'<meta property="og:type" content="article">\n'
            f'<meta property="og:site_name" content="NRSTATLAB">\n'
            f'<meta name="twitter:card" content="summary">\n'
            f'<meta property="og:url" content="{SITE_BASE}/{url_path}">\n')


def generated_pages():
    """Exactly what build_site.py writes -- asked of it, not guessed by glob."""
    ds = ROOT / "data-science-major"
    out = {(ds / f"{slug}.html").resolve() for _, slug, _, _ in _bs.TOP_PAGES}
    for course in _bs.COURSES:
        slug = course["slug"]
        out.add((ds / slug / f"index_{slug}.html").resolve())
        for i in range(1, len(course["units"]) + 1):
            out.add((ds / slug / f"unit{i}_{slug}.html").resolve())
        for _, (out_slug, _, _) in _bs.EXTRA_PAGES.items():
            out.add((ds / slug / f"{out_slug}_{slug}.html").resolve())
        for _, name, _ in _bs.lab_sources(course):
            out.add((ds / slug / name).resolve())
    return out


def targets():
    """Hand-written pages only -- never the generated ones."""
    generated = generated_pages()
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts or "archive" in p.parts:
            continue
        if p.resolve() in generated:
            continue
        if p.name == "404.html" or "course-7-web" in p.parts:
            continue          # the 404 has no banner; the web labs are taught artefacts
        yield p


def main(apply=False):
    changed = titled = described = 0
    for p in targets():
        text = original = p.read_text(errors="replace")
        m = TITLE_RE.search(text)
        if not m:
            continue
        old_t = plain(m.group(1))
        new_t = new_title(m.group(1))
        if new_t != old_t:
            text = text.replace(m.group(0), f"<title>{html_mod.escape(new_t)}</title>", 1)
            titled += 1
            if not apply:
                print(f"  {old_t}\n    -> {new_t}")

        # A page may already carry a description and still have no share card,
        # so the two are decided separately.
        has_desc = re.search(r'<meta name="description" content="([^"]*)"', text)
        desc = html_mod.unescape(has_desc.group(1)) if has_desc else describe(original)
        if desc and 'property="og:' not in text:
            url_path = p.relative_to(ROOT).as_posix()
            block = meta_block(new_t, desc, url_path)
            if has_desc:
                block = "\n".join(l for l in block.split("\n")
                                  if not l.startswith('<meta name="description"'))
            tag = f"<title>{html_mod.escape(new_t)}</title>\n"
            if tag in text:
                text = text.replace(tag, tag + block, 1)
                described += 1

        if text != original:
            changed += 1
            if apply:
                p.write_text(text)
    verb = "updated" if apply else "would update"
    print(f"\n{verb} {changed} pages: {titled} retitled, {described} described")


if __name__ == "__main__":
    main(apply="--apply" in sys.argv)
