# -*- coding: utf-8 -*-
"""Which page on this site teaches each line of the UGC NET Paper I syllabus.

The source is the UGC NET Bureau's "Syllabus, Subject: General Paper on
Teaching & Research Aptitude, Code No. : 00, Paper-I"
(docs/sources/ugc-net-paper-1-general.pdf), extracted to
ugc_paper1_syllabus.txt by pdftext_ugc_paper1.py. As in ugc_map_data.py, THE
SYLLABUS TEXT IS NOT STORED HERE: each row names a half-open range of that
unit's items (ugc_map.items()), and ugc_paper1_map.py joins the slice to print
the line in the document's own words.

EACH ROW: (start, end, section, courses)

  section  the anchor on the Paper I unit page (exams/ugc-net/paper-1/unitN.html)
           that teaches the line, or None while that unit's notes are not
           written yet
  courses  [(course page, evidence)] -- a full course unit that teaches the
           line, with a regular expression that must match that page's text

THE GRADE IS DERIVED, as for the Statistics map: "deep" when a full course
unit also teaches the line, "brief" when only the Paper I notes do, "not here"
when nothing does. Paper I is mostly not statistics, so most lines are brief
by nature; the deep links are the few places where a course on this site goes
further (research methods, data presentation, the internet).

Paths are relative to exams/ugc-net/paper-1/.
"""

S = "../../../statistics/"
D = "../../../data-science/"
RM = S + "statistical-techniques-for-research-methodology/"
DS = S + "descriptive-statistics/"
CF = D + "computer-fundamentals/"

UNITS = [
    ("I", "Teaching Aptitude", [
        (0, 3, "concept", []),
        (3, 4, "levels", []),
        (4, 5, "characteristics", []),
        (5, 7, "learners", []),
        (7, 8, "differences", []),
        (8, 14, "factors", []),
        (14, 17, "methods", []),
        (17, 19, "online", []),
        (19, 22, "support", []),
        (22, 24, "evaluation", []),
        (24, 25, "cbcs", []),
        (25, 27, "cbt", []),
    ]),
    ("II", "Research Aptitude", [
        (0, 4, "meaning", [(RM + "unit1.html", r"Types of Research")]),
        (4, 5, "positivism", []),
        (5, 9, "methods", []),
        (9, 10, "qualquant", [(RM + "unit1.html", r"Based on Approach")]),
        (10, 11, "steps", []),
        (11, 13, "writing", [(RM + "unit5.html", r"Reference Section")]),
        (13, 14, "ict", []),
        (14, 15, "ethics", []),
    ]),
    ("III", "Comprehension", [
        (0, 2, "approach", []),
    ]),
    ("IV", "Communication", [
        (0, 3, "meaning", []),
        (3, 5, "verbal", []),
        (5, 6, "intercultural", []),
        (6, 7, "classroom", []),
        (7, 8, "barriers", []),
        (8, 9, "massmedia", []),
    ]),
    ("V", "Mathematical Reasoning and Aptitude", [
        (0, 1, "reasoning", []),
        (1, 3, "series", []),
        (3, 4, "codes", []),
        (4, 5, "aptitude", []),
    ]),
    ("VI", "Logical Reasoning", [
        (0, 2, "arguments", []),
        (2, 4, "categorical", []),
        (4, 5, "fallacies", []),
        (5, 7, "language", []),
        (7, 8, "square", []),
        (8, 9, "deduction", []),
        (9, 10, "analogies", []),
        (10, 12, "venn", []),
        (12, 14, "indian-logic", []),
        (14, 20, "pramanas", []),
        (20, 23, "anumana", []),
    ]),
    ("VII", "Data Interpretation", [
        (0, 2, "data", [(DS + "unit1.html", r"Collection of Data"), (DS + "unit1.html", r"Classification of Data")]),
        (2, 3, "types", [(DS + "unit1.html", r"[Qq]ualitative")]),
        (3, 4, "graphs", [(DS + "unit2.html", r"Diagrammatic Representation")]),
        (4, 5, "interpretation", []),
        (5, 6, "governance", []),
    ]),
    ("VIII", "Information and Communication Technology (ICT)", [
        (0, 2, None, []),
        (2, 3, None, [(CF + "unit2.html", r"What the Internet is")]),
        (3, 4, None, []),
        (4, 5, None, [(CF + "unit2.html", r"\bEmail\b")]),
        (5, 6, None, []),
        (6, 7, None, []),
        (7, 8, None, []),
    ]),
    ("IX", "People, Development and Environment", [
        (0, 2, None, []),
        (2, 4, None, []),
        (4, 7, None, []),
        (7, 12, None, []),
        (12, 13, None, []),
        (13, 14, None, []),
        (14, 22, None, []),
        (22, 24, None, []),
        (24, 25, None, []),
        (25, 26, None, []),
        (26, 32, None, []),
    ]),
    ("X", "Higher Education System", [
        (0, 1, None, []),
        (1, 2, None, []),
        (2, 4, None, []),
        (4, 6, None, []),
        (6, 7, None, []),
        (7, 10, None, []),
    ]),
]
