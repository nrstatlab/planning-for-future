# -*- coding: utf-8 -*-
"""Render exams/appsc/ from appsc_map_data.py.

Two posts, one syllabus body.  Both per-post pages are built from the same
SUBJECT rows, so a correction reaches both; what differs between them is the
scheme, the standard, the eligibility, and which paper each item sits in.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

import appsc_map_data as A
import labels
import shell_iss
from mapkit import GRADE_KEY, counts, covered, dests, gaps_html, h2, table_html, tally_html

# tools/exams/ -> repository root is two levels up; pages live in exams/.
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "exams", "appsc") + os.sep
labels.BASE = OUT

STAT_ITEMS = (6, 7, 8, 9, 10)          # the five statistics items
NOTE_SRC = ("Both notifications were supplied in full; every figure and every syllabus "
            "line on these pages is reproduced from them and from nothing else.")


def lbl(d):
    return labels.label(d)


def tbl(rows):
    return table_html(rows, lbl, labels.esc)


def all_rows(post):
    """Every graded row for a post, in the order that post's papers run."""
    out = []
    out += [("General Studies and Mental Ability", r) for r in A.GS_GRADED]
    for num, title, pap, rows in A.SUBJECT:
        for r in rows:
            out.append(("%d. %s" % (num, title), r))
    for pid, title, rows in A.CPT:
        for r in rows:
            out.append(("Computer Proficiency Test, " + title, r))
    return out


def grades(rows):
    return counts(g for _, (_, _, g) in rows)


# ------------------------------------------------------------- per-post page
# The earlier examinations' subject papers, solved question by question
# (appsc_paper.py). Linked from both maps and the hub.
SOLVED_NOTE = ('  <div class="note">\n    <p><strong>Practise on past papers.</strong> Two of the '
               'Commission&rsquo;s Assistant Statistical Officer Paper-II question papers are solved '
               'here, all 150 questions of each, with the answer the Commission marked, the working, '
               'and the page that teaches it: the <a href="solved-2025-paper-ii.html">paper of 29 '
               'April 2025</a> and the <a href="solved-2022-paper-ii.html">paper of 4 November '
               '2022</a>.%s</p>\n'
               '  </div>\n')


def post_page(key, other):
    doc = A.DOCS[key]
    rows = all_rows(key)
    c = grades(rows)
    stat_rows = [r for num, t, p, rs in A.SUBJECT if num in STAT_ITEMS for r in rs]
    stat_c = counts(g for _, _, g in stat_rows)

    b = []
    b.append('  <p class="lede">The written examination for %s in the %s, mapped one '
             'syllabus line at a time. Each line is reproduced as the notification '
             'prescribes it, pointed at the page here that teaches it, and graded for '
             'depth &mdash; and where nothing here teaches it, the line says so.</p>\n'
             % (doc["post"], doc["service"]))

    b.append(SOLVED_NOTE % ("" if key == "ASO" else
                            " They were set for the Assistant Statistical Officer, but their ten "
                            "subject items are the ones this notification splits across Papers 2 "
                            "and 3."))

    rowsh = "".join('      <tr><td>%s</td><td>%s</td><td>%d</td><td>%d</td><td>%d</td></tr>\n'
                    % p for p in doc["papers"])
    b.append('  <div class="scroll">\n    <table>\n'
             '      <tr><th>Paper</th><th>Subject</th><th>No. of questions</th>'
             '<th>Duration, minutes</th><th>Maximum marks</th></tr>\n'
             '%s      <tr><td colspan="4"><strong>Total</strong></td>'
             '<td><strong>%d</strong></td></tr>\n    </table>\n  </div>\n'
             % (rowsh, doc["total"]))
    b.append('  <div class="quote">\n    <p>Scheme of examination as set out in %s.</p>\n'
             '    <p><strong>Negative marks.</strong> &ldquo;%s&rdquo;</p>\n'
             '    <cite>%s</cite>\n  </div>\n'
             % (doc["scheme_src"], A.NEGATIVE, doc["notice"]))

    b.append('  <div class="quote">\n    <p><strong>Educational qualification.</strong> '
             '%s</p>\n    <cite>%s</cite>\n  </div>\n'
             % (doc["eligibility"], doc["notice"]))

    b.append(tally_html(c))

    if key == "AD":
        b.append('  <div class="note">\n    <p><strong>&ldquo;P. G. Standard&rdquo; does not '
                 'mean postgraduate statistics here.</strong> The notification labels Papers 2 '
                 'and 3 P. G. standard, but the statistics Paper-3 lists is undergraduate: '
                 'collection of data, central tendency, dispersion and skewness, correlation, '
                 'time series and index numbers. There is no estimation, no testing of '
                 'hypotheses, no inference of any kind. Every one of its %d lines is answered '
                 'by the Foundation courses on this site, and none of the '
                 '<a href="../../statistics/">Advanced courses</a> is needed for it. '
                 'Read that as good news about where to spend the months.</p>\n  </div>\n'
                 % sum(stat_c.values()))
    else:
        b.append('  <div class="note">\n    <p><strong>One paper, ten items, and the statistics '
                 'is the back half of it.</strong> Items 1 to 5 of Paper-II are economics, '
                 'accounting and computing; items 6 to 10 are the statistics, and all %d of '
                 'their lines are answered by the Foundation courses here. The same ten '
                 'items appear in the Assistant Director notification, split across two papers '
                 '&mdash; see <a href="%s.html">that map</a>.</p>\n  </div>\n'
                 % (sum(stat_c.values()), A.DOCS[other]["slug"]))

    # ---- General Studies
    b.append(h2("General Studies and Mental Ability"))
    b.append('  <p>Nine of the ten items in this paper are general knowledge &mdash; current '
             'events, science, history, geography, polity, the economy, environment, disaster '
             'management and reasoning. This site does not teach them and is not going to; '
             'they are named here so the map is not read as covering them:</p>\n')
    b.append('  <ul>\n%s  </ul>\n' % "".join("    <li>%s</li>\n" % t for t in A.GS_TITLES))
    b.append('  <p>The tenth item is statistics, and it is taught here:</p>\n')
    b.append(tbl(A.GS_GRADED))

    # ---- the ten subject items
    for num, title, pap, rows in A.SUBJECT:
        where = pap if key == "AD" else "PAPER-II"
        sc = counts(g for _, _, g in rows)
        b.append(h2("%d. %s" % (num, title)))
        b.append('  <p><strong>%s</strong> &middot; %d line%s: %d taught in depth, %d at exam '
                 'level, %d not here yet.</p>\n'
                 % (where, sum(sc.values()), "" if sum(sc.values()) == 1 else "s",
                    sc["deep"], sc["brief"], sc["missing"]))
        b.append(tbl(rows))
        if num in A.ITEM_NOTES:
            b.append('  <div class="note">\n    <p>%s</p>\n  </div>\n' % A.ITEM_NOTES[num])

    # ---- CPT
    b.append(h2("Computer Proficiency Test"))
    b.append('  <div class="quote">\n    <p>%s.</p>\n    <cite>Scheme prescribed by %s, '
             'reproduced in %s</cite>\n  </div>\n' % (A.CPT_SCHEME, A.CPT_SRC, doc["notice"]))
    b.append('  <p>A qualifying practical test, and the best-covered paper of the three: the '
             'data-science section of this site teaches almost all of it.</p>\n')
    for pid, title, rows in A.CPT:
        sc = counts(g for _, _, g in rows)
        b.append('  <h3>%s</h3>\n' % title)
        b.append('  <p>%d lines: %d deep, %d brief, %d not here.</p>\n'
                 % (sum(sc.values()), sc["deep"], sc["brief"], sc["missing"]))
        b.append(tbl(rows))

    b.append(h2("What this paper still needs"))
    b.append(gaps_html([line for _, (line, _, _) in rows_missing(all_rows(key))],
                       doc["post"]))

    b.append('  <p><a href="%s.html">%s &rarr;</a> &nbsp;&middot;&nbsp; '
             '<a href="index.html">Both posts</a> &nbsp;&middot;&nbsp; '
             '<a href="../iss/index.html">The ISS map</a></p>\n'
             % (A.DOCS[other]["slug"], A.DOCS[other]["post"]))

    shell_iss.page(
        OUT + doc["slug"] + ".html",
        title="%s &mdash; APPSC Syllabus Map" % doc["post"],
        desc=("Every line of the %s syllabus mapped to the page that teaches it, with the "
              "depth graded and the gaps named." % doc["post"]),
        crumb="APPSC %s" % doc["post"],
        h1="%s &mdash; the syllabus, line by line" % doc["post"],
        sub="%s &middot; %s &middot; %d graded lines, %d%% covered here"
            % (doc["service"], doc["standard"], sum(c.values()), round(covered(c))),
        body="".join(b),
        back="index.html", backlabel="Back to the APPSC map",
        footer="Syllabus and scheme text from %s" % doc["notice"])
    return c


def rows_missing(rows):
    return [(sec, r) for sec, r in rows if r[2] == "missing"]


# -------------------------------------------------------------- index page
def index_page(per):
    any_rows = all_rows("AD")
    total = grades(any_rows)
    stat_rows = [r for num, t, p, rs in A.SUBJECT if num in STAT_ITEMS for r in rs]
    stat_c = counts(g for _, _, g in stat_rows)

    b = []
    b.append('  <p class="lede">Two posts, two notifications, and &mdash; the thing worth '
             'knowing before you plan anything &mdash; <strong>one syllabus between '
             'them</strong>. The Assistant Director notification splits ten subject items '
             'across Paper-2 and Paper-3; the Assistant Statistical Officer notification takes '
             'the same ten items, in the same words, as a single Paper-II. So this map is built '
             'once and serves both.</p>\n')

    b.append('  <div class="cards">\n')
    for key in ("AD", "ASO"):
        doc, c = A.DOCS[key], per[key]
        b.append('    <a class="card" href="%s.html">\n      <h3>%s</h3>\n'
                 '      <p>%s<br>%s<br><strong>%d papers, %d marks</strong> &middot; %s</p>\n'
                 '    </a>\n'
                 % (doc["slug"], doc["post"], doc["service"], doc["notice"],
                    len(doc["papers"]), doc["total"], doc["standard"]))
    b.append('  </div>\n')
    b.append('  <p>The two cards carry different schemes and the same syllabus. Both maps grade '
             'the identical %d lines &mdash; %d taught in depth here, %d at exam level, %d not '
             'here at all &mdash; because the ten subject items, the General Studies paper and '
             'the Computer Proficiency Test are word for word the same in both notifications. '
             'Only the split and the standard differ.</p>\n'
             % (sum(total.values()), total["deep"], total["brief"], total["missing"]))

    b.append(tally_html(stat_c, noun="statistics lines, items 6 to 10"))
    other_rows = [r for num, t, p, rs in A.SUBJECT if num not in STAT_ITEMS for r in rs]
    oc = counts(g for _, _, g in other_rows)
    b.append('  <div class="note">\n    <p><strong>Every line of the ten subject items has a page '
             'behind it.</strong> All %d lines of the five statistics items resolve to a page here, '
             'nearly all of them with the working shown. The %d economics, accounting and '
             'computing lines are taught by the Economics, Financial Accounting and computer '
             'fundamentals courses: %d in depth, %d at exam level, %d not yet.</p>\n  </div>\n'
             % (sum(stat_c.values()), sum(oc.values()), oc["deep"], oc["brief"], oc["missing"]))
    b.append(SOLVED_NOTE % "")

    # ---- the shared body, side by side
    b.append(h2("One syllabus, split two ways"))
    b.append('  <div class="scroll">\n    <table>\n'
             '      <tr><th>Subject item, as both notifications word it</th>'
             '<th>Assistant Director</th><th>Assistant Statistical Officer</th>'
             '<th>Covered here</th></tr>\n')
    for num, title, pap, rows in A.SUBJECT:
        sc = counts(g for _, _, g in rows)
        n = sum(sc.values())
        pill = "deep" if sc["missing"] == 0 else ("missing" if sc["deep"] + sc["brief"] == 0 else "brief")
        txt = ("all %d lines" % n if sc["missing"] == 0
               else ("none of %d" % n if sc["deep"] + sc["brief"] == 0
                     else "%d of %d" % (sc["deep"] + sc["brief"], n)))
        b.append('      <tr><td>%d. %s</td><td>%s</td><td>PAPER-II</td>'
                 '<td><span class="g %s">%s</span></td></tr>\n'
                 % (num, title, pap, pill, txt))
    b.append('    </table>\n  </div>\n')
    b.append('  <p>Read that table downwards and the shape of both examinations is the same '
             'shape: a block of economics and accounting, a block of computing, and a block of '
             'statistics, each with a course here behind it. What differs '
             'is the packaging &mdash; and the marks, since the Assistant Director carries the '
             'economics and the statistics in separate 150-mark papers while the Assistant '
             'Statistical Officer carries both in one.</p>\n')

    # ---- scheme
    b.append(h2("The two schemes, as the notifications set them out"))
    b.append('  <div class="scroll">\n    <table>\n'
             '      <tr><th>&nbsp;</th><th>Assistant Director</th>'
             '<th>Assistant Statistical Officer</th></tr>\n'
             '      <tr><td>Notification</td><td>%s</td><td>%s</td></tr>\n'
             '      <tr><td>Service</td><td>%s</td><td>%s</td></tr>\n'
             '      <tr><td>Standard</td><td>%s</td><td>%s</td></tr>\n'
             '      <tr><td>Papers</td><td>%d</td><td>%d</td></tr>\n'
             '      <tr><td>Total marks</td><td>%d</td><td>%d</td></tr>\n'
             '      <tr><td>Scheme prescribed by</td><td>%s</td><td>%s</td></tr>\n'
             '    </table>\n  </div>\n'
             % (A.DOCS["AD"]["notice"], A.DOCS["ASO"]["notice"],
                A.DOCS["AD"]["service"], A.DOCS["ASO"]["service"],
                A.DOCS["AD"]["standard"], A.DOCS["ASO"]["standard"],
                len(A.DOCS["AD"]["papers"]), len(A.DOCS["ASO"]["papers"]),
                A.DOCS["AD"]["total"], A.DOCS["ASO"]["total"],
                A.DOCS["AD"]["scheme_src"], A.DOCS["ASO"]["scheme_src"]))
    b.append('  <p>Every paper in both schemes is 150 questions in 150 minutes for 150 marks, '
             'objective type, with the same negative marking: &ldquo;%s&rdquo;</p>\n' % A.NEGATIVE)

    b.append('  <div class="note">\n    <p><strong>No vacancy count and no pay scale appears on '
             'these pages, deliberately.</strong> Both notifications state that the number of '
             'vacancies is &ldquo;subject to variation upon confirmation being received from the '
             'concerned Department&rdquo; &mdash; a figure already provisional in its own source '
             'has no business being repeated in a study guide, where it would go stale quietly. '
             'The same goes for dates. %s Read the current official notification for the '
             'recruitment you are sitting; use these pages for the statistics.</p>\n  </div>\n'
             % NOTE_SRC)

    b.append(GRADE_KEY)

    b.append(h2("Where this sits against the other maps"))
    b.append('  <p>Every statistics line in these papers is also a line of the '
             '<a href="../iss/index.html">Indian Statistical Service syllabus</a>, which asks '
             'for the same topics and then keeps going &mdash; estimation, testing, sampling '
             'theory, multivariate analysis, none of which APPSC asks for at all. So reading '
             'for the ISS covers APPSC statistics on the way past, but not the reverse. If you '
             'are sitting both, read the ISS map and treat this one as the subset that is '
             'examined first.</p>\n')

    b.append(h2("The work queue"))
    miss = rows_missing(any_rows)
    b.append('  <p>%d of the %d graded lines have nothing behind them. They are listed rather '
             'than dropped, because a map that hides its holes only tells you about them in the '
             'hall.</p>\n' % (total["missing"], sum(total.values())))
    b.append(gaps_html([line for _, (line, _, _) in miss], "these two syllabuses"))

    shell_iss.page(
        OUT + "index.html",
        title="APPSC Syllabus Map &mdash; Assistant Director and Assistant Statistical Officer",
        desc=("Both APPSC statistics recruitments mapped line by line onto the notes on this "
              "site, with the depth graded and the gaps named."),
        crumb="APPSC",
        h1="APPSC &mdash; two posts, one syllabus, mapped",
        sub="Assistant Director &middot; Assistant Statistical Officer &middot; %d graded lines "
            "&middot; every subject line with a page behind it" % sum(total.values()),
        body="".join(b),
        back="../index.html", backlabel="Back to Statistics for Examinations",
        footer="Syllabus and scheme text from %s and %s"
               % (A.DOCS["AD"]["notice"], A.DOCS["ASO"]["notice"]))
    return total


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    per = {"AD": post_page("AD", "ASO"), "ASO": post_page("ASO", "AD")}
    tot = index_page(per)
    print("wrote index + 2 post pages to", OUT)
    print("totals:", tot, "=", sum(tot.values()), "covered %.1f%%" % covered(tot))
