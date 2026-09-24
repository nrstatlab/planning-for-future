#!/usr/bin/env python3
"""Take the degree programme and the semester out of the Statistics pages' wording.

    python3 tools/retire_programme_labels.py            # dry run: count what would change
    python3 tools/retire_programme_labels.py --diff     # ... and print every change
    python3 tools/retire_programme_labels.py --apply    # write

One-shot, like retitle_and_describe.py. The second restructure
(restructure2.py) took the programme out of the URL and the menu; this takes
it out of what the pages SAY about themselves -- their titles, breadcrumbs,
banner lines, back-links, footers and descriptions, and the prose that calls
a course "this paper" or its predecessor "the undergraduate course".

WHAT IT DOES NOT TOUCH, deliberately:

  * syllabus.html pages. They transcribe the official document a course was
    written to, and its semesters, credits and paper numbers are part of what
    it says; each gets a one-line "source document" label instead.
  * paper codes in running prose ("Sampling Theory (STS-204)"): they name the
    document the course follows, which a reader checking coverage needs.
  * the teaching. Examples about students in "the previous semester", a
    question offering "Postgraduate" as an answer, CPM and PERT's
    "programme": those are content, and every rule below is scoped so that
    none of them can match.

The prose rules run only on the 13 advanced courses, which are the pages that
were written as papers of a programme.
"""
import argparse
import difflib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STAT = ROOT / "statistics"

ADVANCED = [
    "data-handling-using-r", "data-science-using-python",
    "design-and-analysis-of-experiments-advanced", "distribution-theory",
    "estimation-theory", "linear-algebra-and-linear-models", "mathematical-analysis",
    "multivariate-analysis", "probability-theory", "sampling-theory",
    "statistical-analysis-using-spss", "statistical-methods-using-python",
    "testing-of-hypotheses",
]
ALLIED = ["economics", "financial-accounting"]

SOURCE_NOTE = ('  <p class="source-note"><b>Source document.</b> This page reproduces the '
               'syllabus this course was written to, as published &mdash; its semesters, '
               'credits and paper numbers are that document&rsquo;s, not this site&rsquo;s. '
               'The course itself is studied on its own, in any order.</p>\n')
SOURCE_MARK = 'class="source-note"'

# ---- page furniture: every Statistics course -------------------------------
FURNITURE = [
    # The one course whose name is shared with a Foundation course keeps its
    # level in its title, so the two are never the same string in a tab or a
    # search result.
    (r"(<title>|<meta property=\"og:title\" content=\")Design and Analysis of Experiments \(STS-203\) — MSc Statistics, Semester II",
     r"\1Design and Analysis of Experiments (Advanced) — Complete Study Material"),
    # titles and og:title: "Sampling Theory (STS-204) — MSc Statistics, Semester II"
    (r"(<title>|<meta property=\"og:title\" content=\")([^<\"]+?) \(STS-\d+\) — MSc Statistics, Semester [IV]+",
     r"\1\2 — Complete Study Material"),
    (r"Testing of Hypotheses — Postgraduate Core, MSc Statistics", "Testing of Hypotheses — Complete Study Material"),
    # breadcrumbs
    (r'<div class="crumbs"><a href="\.\./index\.html">MSc Statistics</a> &raquo; (?:Semester [IV]+ &raquo; (?:Practical )?Paper [IVX]+|Postgraduate core &raquo; Testing of Hypotheses)</div>',
     "CRUMB"),
    (r'(<div class="crumbs">.*?)<a href="\.\./index\.html">Exam Subjects</a>', r'\1<a href="../index.html">Statistics</a>'),
    # back-links
    (r"&larr; MSc Statistics</a>", "&larr; All Statistics courses</a>"),
    (r">MSc Statistics &rarr;</a>", ">All Statistics courses &rarr;</a>"),
    (r"&larr; Exam Subjects</a>", "&larr; All Statistics courses</a>"),
    # footers
    (r"(<footer>[^<]*?) \(STS-\d+\)", r"\1"),
    (r"(<footer>[^<]*?) &middot; MSc Statistics</footer>", r"\1 &middot; Statistics</footer>"),
    (r"<footer>Testing of Hypotheses &middot; Postgraduate core</footer>", "<footer>Testing of Hypotheses &middot; Statistics</footer>"),
    # banner lines: "STS-204 · Semester II · 4 credits · theory, with Section B of the STS-206 practical"
    (r"<p>STS-\d+ &middot; Semester [IV]+ &middot; \d+ credits &middot; practical</p>",
     "<p>Advanced course &middot; practical</p>"),
    (r"<p>STS-\d+ &middot; Semester [IV]+ &middot; \d+ credits &middot; theory paper</p>",
     "<p>Advanced course &middot; theory</p>"),
    (r"<p>STS-\d+ &middot; Semester [IV]+ &middot; \d+ credits &middot; theory, with (?:Section [AB] of )?the STS-\d+ practical</p>",
     "<p>Advanced course &middot; theory, with its practical</p>"),
    (r"<p>Postgraduate core &middot; four units &middot; written to the topic, not to a paper code</p>",
     "<p>Advanced course &middot; four units &middot; written to the topic, not to a paper code</p>"),
    # descriptions (name, og and the JSON-LD copy are all the same string)
    (r"The Semester [IV]+ (R|Python|SPSS) practical", r"The \1 practical"),
    (r"Semester VI, Practical\. ", "Practical. "),
    (r"2 hrs/week, Credit 1\. ", ""),
]

# ---- prose: the 13 advanced courses only ------------------------------------
PROSE = [
    (r"How This Paper Connects to the Rest of the Programme", "How This Course Connects to the Others"),
    (r"Units in this Paper", "Units in this Course"),
    (r"The Three Python Papers Together", "The Three Python Courses Together"),
    (r"The postgraduate ([a-z ]+?) paper in four units", r"The advanced \1 course in four units"),
    (r"The postgraduate theory of testing", "The advanced theory of testing"),
    (r"new at postgraduate level", "new at this level"),
    # Sentences wrap in the source, so these two allow any whitespace.
    (r",\s+the\s+first\s+theory\s+paper\s+of\s+Semester\s+I\s+and\s+the\s+only\s+one\s+in\s+the\s+programme\s+that\s+is\s+pure\s+mathematics",
     ", the only course in the catalogue that is pure mathematics"),
    (r",\s+the\s+third\s+theory\s+paper\s+of\s+Semester\s+I\.", "."),
    (r"the\s+rest\s+of\s+the\s+programme\s+assumes", "the courses that follow assume"),
    (r"the\s+rest\s+of\s+the\s+programme\s+needs", "the courses that follow need"),
    (r"\b\d-credit (conventional )?practical", r"\1practical"),
    (r"Everything the BSc paper ", "Everything the Foundation course "),
    (r"the undergraduate word", "the Foundation course&rsquo;s word"),
    (r"\bUndergraduate\b", "Foundation"),
    (r"\bundergraduate\b", "Foundation"),
    (r"the rest of the programme", "the courses that follow"),
    (r"later in the programme", "later in the catalogue"),
    (r"it is why this unit sits in the programme", "it is why this unit is here"),
    (r"a range the programme runs", "a range the catalogue runs"),
    (r"\bthis Paper\b", "this Course"),
    (r"\b([Tt])his paper\b", r"\1his course"),
    (r"\b([Tt])hat paper\b", r"\1hat course"),
    (r"\b([Tt])he whole paper\b", r"\1he whole course"),
    (r"\b([Tt])he paper\b", r"\1he course"),
    (r"\bno practical paper\b", "no practical"),
    (r"\btheory paper\b", "theory course"),
]
# Obsolete: every advanced course is written now, so none is shown in italics.
ITALICS_NOTE = re.compile(r'\s*<p style="font-size:\.92rem;color:#4b5563"><em>Papers shown in italics '
                          r'.*?</em></p>', re.S)

# Nothing inside these is page wording.
PROTECT = re.compile(r"<!-- (site-nav|site-head|site-foot|course-catalogue|useful-for|next-course)"
                     r".*?<!-- /\1 -->|<pre\b.*?</pre>|<code\b.*?</code>", re.S)


def course_label(folder):
    t = (STAT / folder / "index.html").read_text()
    m = re.search(r"<h1>(.*?)</h1>", t, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip()


def rewrite(text, rules, crumb):
    kept = []

    def hold(m):
        kept.append(m.group(0))
        return "\x00%d\x00" % (len(kept) - 1)

    out = PROTECT.sub(hold, text)
    for pat, rep in rules:
        if rep == "CRUMB":
            out = re.sub(pat, '<div class="crumbs"><a href="../index.html">Statistics</a> &raquo; %s</div>' % crumb, out)
        else:
            out = re.sub(pat, rep, out)
    return re.sub(r"\x00(\d+)\x00", lambda m: kept[int(m.group(1))], out)


def pages():
    for d in sorted(STAT.iterdir()):
        if not d.is_dir() or not (d / "index.html").exists():
            continue
        for p in sorted(d.glob("*.html")):
            head = p.read_text(errors="replace")[:2048]
            if 'http-equiv="refresh"' in head:
                continue
            yield d.name, p


def main(apply_changes, show):
    changed = 0
    for folder, p in pages():
        text = p.read_text()
        if p.name == "syllabus.html":
            out = text
            if SOURCE_MARK not in out:
                i = out.index('<div class="banner">')
                h = out.index("</h1>", i)
                e = out.index("</div>", h) + len("</div>\n")
                out = out[:e] + SOURCE_NOTE + out[e:]
        else:
            crumb = course_label(folder)
            out = rewrite(text, FURNITURE, crumb)
            if folder in ADVANCED:
                out = rewrite(out, PROSE, crumb)
                out = ITALICS_NOTE.sub("", out)
        if out != text:
            changed += 1
            if show:
                sys.stdout.writelines(difflib.unified_diff(
                    text.splitlines(True), out.splitlines(True),
                    str(p.relative_to(ROOT)), str(p.relative_to(ROOT)), n=0))
            if apply_changes:
                p.write_text(out)
    print("%d page(s) %s" % (changed, "written" if apply_changes else "would change"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--diff", action="store_true")
    a = ap.parse_args()
    main(a.apply, a.diff)
