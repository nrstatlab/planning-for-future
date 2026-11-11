# -*- coding: utf-8 -*-
"""Exam-standard model questions for UGC NET, fifty a unit (owner, 11 November
2026): p2_unitNN.py for Statistics (Code 107), p1_unitNN.py for Paper I.

Each module gives TITLE, BLURB and QUESTIONS; a question is
Q(stem, [A, B, C, D], key, explanation, anchor) in HTML, where anchor is the id
of the section of the unit notes that teaches it. ("PASSAGE", label, html)
precedes the questions set on a passage or a data set. ugc_model.py writes the
pages, recheck_ugc_model.py checks them and ugc_model_verify.py recomputes the
numerical answers.
"""
ROMAN = ["I", "II", "III", "IV", "V"]


def Q(stem, opts, key, expl, anchor):
    return {"q": stem, "o": opts, "k": key, "e": expl, "a": anchor}


def st(*items):
    """Numbered statements under a stem."""
    return '<span class="stmts">' + "".join(
        "<span>(%s) %s</span>" % (ROMAN[i], s) for i, s in enumerate(items)) + "</span>"


def match(left, right, h1="List I", h2="List II"):
    """A match-the-lists table: left items (a), (b) ...; right items (i), (ii) ..."""
    rn = ["i", "ii", "iii", "iv", "v"]
    rows = "".join("<tr><td>(%s) %s</td><td>(%s) %s</td></tr>" % ("abcde"[i], l, rn[i], r)
                   for i, (l, r) in enumerate(zip(left, right)))
    return '<table class="lists"><tr><th>%s</th><th>%s</th></tr>%s</table>' % (h1, h2, rows)


AR = ["Both (A) and (R) are true and (R) is the correct explanation of (A)",
      "Both (A) and (R) are true but (R) is not the correct explanation of (A)",
      "(A) is true but (R) is false",
      "(A) is false but (R) is true"]


def ar(a, r):
    return ('Given below are two statements, one labelled Assertion (A) and the other Reason (R).'
            '<span class="stmts"><span><b>Assertion (A):</b> %s</span><span><b>Reason (R):</b> %s</span></span>'
            'Choose the correct answer.' % (a, r))
