# -*- coding: utf-8 -*-
"""The pieces every syllabus map on this site is built from.

Shared by iss_map.py and appsc_map.py so a fix to the table markup, the grade
pills or the gap list reaches both maps at once -- the same argument the maps
themselves make for linking into shared notes rather than copying them.
"""
import re

GRADE_TEXT = {"deep": "deep", "brief": "brief", "missing": "not here"}


def h2(text):
    """<h2> with an id.

    tools/add_statistics_navigation.py only walks statistics/, so nothing
    assigns ids under exams/ -- the generator does it, the way the
    csir-net map's ids are written by hand next door.
    """
    slug = re.sub(r"&[a-z]+;", " ", text)
    slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    return '  <h2 id="%s">%s</h2>\n' % (slug, text)


def dests(dest):
    """None, one path or several -- always a tuple."""
    if dest is None:
        return ()
    return (dest,) if isinstance(dest, str) else tuple(dest)


def counts(grades):
    c = {"deep": 0, "brief": 0, "missing": 0}
    for g in grades:
        c[g] += 1
    return c


def covered(c):
    n = sum(c.values())
    return 100.0 * (c["deep"] + c["brief"]) / n if n else 0.0


def tally_html(c, noun="syllabus lines"):
    return ('  <ul class="tally">\n'
            '    <li><b>%d</b>%s</li>\n'
            '    <li><b>%d</b>taught in depth</li>\n'
            '    <li><b>%d</b>covered at exam level</li>\n'
            '    <li><b>%d</b>not here yet</li>\n'
            '    <li><b>%.0f%%</b>covered</li>\n'
            '  </ul>\n' % (sum(c.values()), noun, c["deep"], c["brief"],
                           c["missing"], covered(c)))


def cell(dest, label, esc):
    ds = dests(dest)
    if not ds:
        return '<span class="none">nothing on this site teaches it</span>'
    return "<br>".join('<a href="%s">%s</a>' % (esc(d), label(d)) for d in ds)


def table_html(rows, label, esc, head="Syllabus line, as prescribed"):
    out = ['  <div class="scroll">\n    <table>\n',
           '      <tr><th>%s</th><th>Where it is taught here</th>'
           '<th>Depth</th></tr>\n' % head]
    for line, dest, grade in rows:
        out.append('      <tr><td>%s</td><td>%s</td>'
                   '<td><span class="g %s">%s</span></td></tr>\n'
                   % (line, cell(dest, label, esc), grade, GRADE_TEXT[grade]))
    out.append('    </table>\n  </div>\n')
    return "".join(out)


def gaps_html(lines, where, none_msg=None):
    """The red block. Every map states its own holes; that is the point of it."""
    if not lines:
        return ('  <div class="note">\n    <p><strong>No gaps in %s.</strong> %s</p>\n'
                '  </div>\n'
                % (where, none_msg or "Every line above points at a page on this site."))
    items = "".join("      <li>%s</li>\n" % m for m in lines)
    return ('  <div class="gaps">\n'
            '    <p><strong>Not covered yet &mdash; %d line%s in %s.</strong> '
            'Read these from a standard text; this site does not yet teach them.</p>\n'
            '    <ul>\n%s    </ul>\n  </div>\n'
            % (len(lines), "" if len(lines) == 1 else "s", where, items))


GRADE_KEY = h2("How to read the depth column") + """
  <p><span class="g deep">deep</span> a full unit page here, with the derivation
  worked out and problems solved step by step &mdash; enough to answer a descriptive
  paper, not just recognise the term.
  &nbsp;<span class="g brief">brief</span> covered, but at exam-summary level: the
  definition, the formula and a worked example, without the derivation.
  &nbsp;<span class="g missing">not here</span> nothing on this site teaches it.
  It is named rather than quietly skipped, because a map that hides its holes only
  tells you about them in the hall.</p>
"""
