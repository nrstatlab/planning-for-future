# -*- coding: utf-8 -*-
"""Render exams/iss/ from iss_map_data.py.

Nothing here is hand-typed twice: the syllabus lines come from iss_map_data,
the link text comes from each destination page's own <title> via labels.py,
and every count on every page is computed from the same rows that build the
tables, so a page cannot disagree with itself.
"""
import os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import iss_map_data as D
import labels
import shell_iss
from mapkit import GRADE_KEY, GRADE_TEXT, cell, counts, dests, gaps_html, h2, table_html, tally_html

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "exams", "iss") + os.sep
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV"}

SOURCE = ("Examination Notice No.&nbsp;07/2026-IES/ISS, dated 11.02.2026 &mdash; "
          "Appendix-I, Scheme of Examination, and Section-II, Standard and Syllabi")
SRC_SHORT = "Examination Notice No.&nbsp;07/2026-IES/ISS"

# ----------------------------------------------------------------- helpers
def rows_of(paper):
    for rn, sn, rows in D.PAPERS[paper]["sections"]:
        for r in rows:
            yield rn, sn, r


# ------------------------------------------------------------- paper pages
def paper_page(p):
    info = D.PAPERS[p]
    rows = list(rows_of(p))
    plain = [r for _, _, r in rows]
    c = counts(g for _, _, (_, _, g) in rows)
    rn = ROMAN[p]

    body = ['  <p class="lede">Paper %s of the Indian Statistical Service written '
            'examination is <strong>%s</strong>, and this page takes its syllabus '
            'one line at a time. Each line is reproduced as it is prescribed, then '
            'pointed at the page on this site that teaches it, with the depth stated '
            'rather than implied.</p>\n' % (rn, info["code"].title().replace("Statistics-", "Statistics-"))]

    body.append('  <div class="quote">\n    <p>%s (%s) &mdash; %d marks, %s.</p>\n'
                '    <cite>%s</cite>\n  </div>\n'
                % (info["code"].replace("STATISTICS", "Statistics"), info["type"],
                   info["marks"], info["time"], SOURCE))

    if p == 4:
        body.append('  <div class="note">\n    <p><strong>You answer two of the seven '
                    'sections.</strong> The notification states: &ldquo;In Statistics-IV, '
                    'there will be SEVEN Sections in the paper. Candidates have to choose '
                    'any TWO Sections out of them. All Sections will carry equal '
                    'marks.&rdquo; So the tally below counts the whole paper; in the hall '
                    'you need two sections, and the sensible choice is the pair whose rows '
                    'are greenest for you.</p>\n  </div>\n')

    body.append(tally_html(c))

    for rnum, sname, srows in info["sections"]:
        sub = [r for r in rows if r[0] == rnum]
        sc = counts(g for _, _, (_, _, g) in sub)
        body.append(h2("Section (%s) &mdash; %s" % (rnum, sname)))
        body.append('  <p>%d syllabus lines: %d taught in depth, %d at exam level, '
                    '%d not here yet.</p>\n' % (sum(sc.values()), sc["deep"],
                                                sc["brief"], sc["missing"]))
        body.append(table_html(srows, labels.label, labels.esc))

    body.append(h2("What this paper still needs"))
    body.append(gaps_html([l for _, _, (l, _, g) in rows if g == "missing"],
                          "Paper %s" % rn))

    nav = []
    if p > 1:
        nav.append('<a href="paper%d.html">&larr; Paper %s</a>' % (p - 1, ROMAN[p - 1]))
    nav.append('<a href="index.html">All four papers</a>')
    if p < 4:
        nav.append('<a href="paper%d.html">Paper %s &rarr;</a>' % (p + 1, ROMAN[p + 1]))
    body.append('  <p>%s</p>\n' % ' &nbsp;&middot;&nbsp; '.join(nav))

    shell_iss.page(
        OUT + "paper%d.html" % p,
        title="Paper %s: %s &mdash; ISS Syllabus Map" % (rn, info["code"].title()),
        desc=("Every line of the %s syllabus mapped to the page that teaches it, "
              "with the depth graded and the gaps named."
              % info["code"].replace("STATISTICS", "Statistics")),
        crumb="ISS Paper %s" % rn,
        h1="Statistics-%s &mdash; the syllabus, line by line" % rn,
        sub="%s &middot; %d marks &middot; %s &middot; %d syllabus lines, %d%% covered here"
            % (info["type"], info["marks"], info["time"], sum(c.values()),
               round(100.0 * (c["deep"] + c["brief"]) / sum(c.values()))),
        body="".join(body),
        back="index.html", backlabel="Back to the ISS syllabus map",
        footer="Syllabus text from %s" % SRC_SHORT)
    return c


# -------------------------------------------------------------- index page
def index_page(percounts):
    total = {"deep": 0, "brief": 0, "missing": 0}
    for c in percounts.values():
        for k in total:
            total[k] += c[k]
    n = sum(total.values())

    b = []
    b.append('  <p class="lede">The Indian Statistical Service syllabus is the widest '
             'statistics syllabus in the country that is also <em>fixed</em>. Every state '
             'degree board writes its own; every university writes its own MSc; every '
             'commission writes its own paper. The ISS list sits above all of them, and '
             'almost every topic any of them asks for appears somewhere on it. So this '
             'site maps itself against the ISS syllabus once, and any other syllabus can '
             'be read through that map.</p>\n')

    b.append('  <p>All four Statistics papers are mapped below, %d syllabus lines in '
             'total. Each line is reproduced as prescribed, pointed at the page here that '
             'teaches it, and graded for depth. Where nothing here teaches it, the line '
             'says so.</p>\n' % n)

    b.append(tally_html(total))

    b.append(h2("The four papers") + '  <div class="cards">\n')
    for p in (1, 2, 3, 4):
        info = D.PAPERS[p]
        c = percounts[p]
        nn = sum(c.values())
        secs = ", ".join(s[1] for s in info["sections"])
        b.append('    <a class="card" href="paper%d.html">\n'
                 '      <h3>Paper %s &mdash; %s</h3>\n'
                 '      <p>%s.<br>%d lines &middot; %d deep &middot; %d brief &middot; '
                 '%d not here &middot; <strong>%d%% covered</strong></p>\n'
                 '    </a>\n'
                 % (p, ROMAN[p], info["code"].title(), secs, nn, c["deep"],
                    c["brief"], c["missing"],
                    round(100.0 * (c["deep"] + c["brief"]) / nn)))
    b.append('  </div>\n')

    b.append(h2("The written examination, as the notification sets it out"))
    b.append('  <div class="scroll">\n    <table>\n'
             '      <tr><th>Subject</th><th>Maximum marks</th><th>Time allowed</th></tr>\n'
             '      <tr><td>General English</td><td>100</td><td>3 hrs.</td></tr>\n'
             '      <tr><td>General Studies</td><td>100</td><td>3 hrs.</td></tr>\n'
             '      <tr><td>Statistics-I (Objective)</td><td>200</td><td>2 hrs.</td></tr>\n'
             '      <tr><td>Statistics-II (Objective)</td><td>200</td><td>2 hrs.</td></tr>\n'
             '      <tr><td>Statistics-III (Descriptive)</td><td>200</td><td>3 hrs.</td></tr>\n'
             '      <tr><td>Statistics-IV (Descriptive)</td><td>200</td><td>3 hrs.</td></tr>\n'
             '    </table>\n  </div>\n')
    b.append('  <div class="quote">\n'
             '    <p>&ldquo;Statistics I &amp; II will be of Objective Type Questions '
             '(80 questions with maximum marks of 200 in each paper) to be attempted in '
             '120 minutes.&rdquo;</p>\n'
             '    <p>&ldquo;Statistics III and IV will be of Descriptive Type having Short '
             'Answer/ Small Problems Questions (50%%) and Long Answer and Comprehension '
             'problem questions (50%%). At least one Short Answer and One Long Answer '
             'Question from each section is compulsory. In Statistics-IV, there will be '
             'SEVEN Sections in the paper. Candidates have to choose any TWO Sections out '
             'of them. All Sections will carry equal marks.&rdquo;</p>\n'
             '    <cite>%s</cite>\n  </div>\n' % SOURCE)

    b.append('  <div class="note">\n    <p><strong>That table is quoted, not remembered.</strong> '
             'It is reproduced from the notification named under it, and from nowhere else. '
             'Marks, timings and the number of sections change between notifications, so '
             'read the current official notice for the year you are sitting and treat this '
             'page as being about the statistics.</p>\n  </div>\n')

    b.append(h2("Why the descriptive papers change what it means to be covered"))
    b.append('  <div class="quote">\n    <p>&ldquo;The candidates will be expected to '
             'illustrate theory by facts, and to analyse problems with the help of theory. '
             'They will be expected to be particularly conversant with Indian problems in '
             'the field(s) of Economics/Statistics.&rdquo;</p>\n'
             '    <cite>%s</cite>\n  </div>\n' % SOURCE)
    b.append('  <p>Papers III and IV are written by hand, and that sentence is why a '
             '<span class="g brief">brief</span> grade is not good enough for them. '
             'Recognising Horvitz&ndash;Thompson in a list of four options is an objective-paper '
             'skill; deriving its variance and then saying what the estimate means for the '
             'survey in front of you is a descriptive-paper skill. Where a line below is '
             'graded brief and sits in Paper III or IV, treat it as work still to do.</p>\n')

    b.append(GRADE_KEY)

    b.append(h2("The work queue"))
    b.append('  <p>%d of the %d lines have nothing behind them. They are listed here '
             'together, paper by paper, because this list is what gets built next &mdash; '
             'in that order, roughly, by how many other syllabuses also ask for '
             'them.</p>\n' % (total["missing"], n))
    for p in (1, 2, 3, 4):
        miss = [(sn, line) for _, sn, (line, _, g) in rows_of(p) if g == "missing"]
        if not miss:
            continue
        items = "".join("      <li><em>%s</em> &mdash; %s</li>\n" % (sn, line)
                        for sn, line in miss)
        b.append('  <div class="gaps">\n    <p><strong>Paper %s &mdash; %d line%s.</strong></p>\n'
                 '    <ul>\n%s    </ul>\n  </div>\n'
                 % (ROMAN[p], len(miss), "" if len(miss) == 1 else "s", items))

    b.append(h2("Using this map for a syllabus that is not the ISS one"))
    b.append('  <p>Take your own syllabus a line at a time and find the nearest ISS line '
             'above. The destination is the same page either way, because the statistics '
             'is the same &mdash; a state degree board asking for stratified sampling and the '
             'ISS asking for stratified sampling want the same derivation, at different '
             'depths. What differs is how far down the page you need to read, and the depth '
             'column tells you that. The two places this breaks down are worth knowing: '
             'ISS Paper I asks for numerical analysis, which most statistics degrees do not, '
             'and ISS Paper II asks for official statistics at a level no degree syllabus '
             'reaches. Both are in the work queue above.</p>\n')
    b.append('  <p>The other maps on this site &mdash; '
             '<a href="../csir-net/index.html">CSIR NET</a> and the '
             '<a href="../ugc-net/index.html">UGC NET units</a> &mdash; '
             'point at the same pages, so a correction to a proof reaches every map at '
             'once.</p>\n')

    shell_iss.page(
        OUT + "index.html",
        title="ISS Syllabus Map &mdash; Indian Statistical Service Statistics Papers",
        desc=("All four Indian Statistical Service statistics papers mapped line by line "
              "onto the notes on this site, with the depth graded and the gaps named."),
        crumb="Indian Statistical Service",
        h1="Indian Statistical Service &mdash; the syllabus, mapped",
        sub="Four statistics papers &middot; %d syllabus lines &middot; %d%% covered here "
            "&middot; %d gaps named" % (n, round(100.0 * (total["deep"] + total["brief"]) / n),
                                        total["missing"]),
        body="".join(b),
        back="../index.html", backlabel="Back to Statistics for Examinations",
        footer="Syllabus and scheme text from %s" % SRC_SHORT)
    return total


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    per = {p: paper_page(p) for p in (1, 2, 3, 4)}
    tot = index_page(per)
    print("wrote index.html + paper1-4.html to", OUT)
    print("totals:", tot, "=", sum(tot.values()))
