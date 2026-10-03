#!/usr/bin/env python3
"""Move the statistical practical pages from "3. Procedure" to "3. Formula".

The statistical structure is 1. Problem, 2. Aim, 3. Formula, 4. Calculation, 5. Result.
The pages were written with a third section, "3. Procedure", that held three things in
turn: the steps (an <ol>), the formula box(es), and a blank working table. This puts each
where the structure wants it, and changes no other text:

  3. Formula       the formula box(es) first, then the steps, under "Applying it:"
  4. Calculation   the blank working table first, then the working as before

Each section is taken apart into its top-level blocks; any block of another kind stops
the script, so nothing is moved that has not been looked at. Run once (it was, in
October 2026); kept for the record and for a page written the old way.

    python3 tools/practicals/retemplate_statistical.py PAGE...         # report
    python3 tools/practicals/retemplate_statistical.py --apply PAGE... # rewrite
"""
import re
import sys

PROC = re.compile(r'<h3 id="3-procedure(-\d+)?">\s*3\. Procedure\s*</h3>((?:(?!<h[23]\b).)*?)'
                  r'(<h3 id="4-calculation(?:-\d+)?">\s*4\. Calculation\s*</h3>)', re.S)
TAGS = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>")
VOID = {"br", "img", "hr", "input", "meta", "link", "col", "wbr", "span"}


def blocks(body):
    """The top-level elements of a fragment, as (tag, html); text between them must be blank."""
    out, depth, start, pos, top = [], 0, None, 0, None
    for m in TAGS.finditer(body):
        close, tag, selfclose = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or selfclose:
            continue
        if not close:
            if depth == 0:
                if body[pos:m.start()].strip():
                    raise ValueError(f"text outside a block: {body[pos:m.start()].strip()[:60]!r}")
                start, top = m.start(), tag
                cls = re.search(r'class="([^"]+)"', m.group(0))
                top = tag + ("." + cls.group(1) if cls else "")
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append((top, body[start:m.end()]))
                pos = m.end()
    if depth != 0 or body[pos:].strip():
        raise ValueError("unbalanced section")
    return out


def rewrite(page, name):
    count = 0

    def one(m):
        nonlocal count
        suffix, body, calc = m.group(1) or "", m.group(2), m.group(3)
        steps, formulas, blank = [], [], []
        parts = blocks(body)
        for i, (tag, html) in enumerate(parts):
            if tag == "ol":
                steps.append(html)
            elif tag == "div.formula":
                formulas.append(html)
            elif tag == "p" and re.match(r"<p><strong>Blank\b", html):
                blank.append(html)
            elif tag.startswith("table") and blank and parts[i - 1][0] == "p":
                blank.append(html)
            else:
                raise ValueError(f"{name} 3-procedure{suffix}: a {tag} block -- move it by hand")
        if len(steps) != 1 or not formulas:
            raise ValueError(f"{name} 3-procedure{suffix}: {len(steps)} step lists, "
                             f"{len(formulas)} formula boxes -- do it by hand")
        count += 1
        new = [f'<h3 id="3-formula{suffix}">3. Formula</h3>', *formulas,
               "<p><strong>Applying it:</strong></p>", *steps]
        moved = "\n  ".join(new) + "\n\n  " + calc
        if blank:
            moved += "\n  " + "\n  ".join(blank)
        return moved

    return PROC.sub(one, page), count


def main():
    apply = "--apply" in sys.argv[1:]
    for path in [a for a in sys.argv[1:] if not a.startswith("--")]:
        page = open(path).read()
        new, n = rewrite(page, path)
        left = len(re.findall(r">\s*3\. Procedure\s*</h3>", new))
        print(f"{path}: {n} sections moved" + (f"; {left} left for hand work" if left else ""))
        if apply and new != page:
            open(path, "w").write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
