# -*- coding: utf-8 -*-
"""The working of every Paper I model MCQ whose key can be computed.

recheck_ugc_paper1.py evaluates each entry and requires the result to equal
the keyed option and no other option. The working is written here afresh, as
arithmetic, not copied from the explanation on the page, so a slip in either
shows up as a disagreement.

    (unit, question): (python expression, how to read the options, cues)

The cues are pieces of text the question's stem must contain, so that the
working here and the question on the page cannot drift apart unnoticed.

"number"  each option holds one number (with a unit or a sign around it, such as
          "₹1,026" or "45 km/h"); the result must lie strictly within half a unit of
          the last decimal place of the keyed option's number, and of no other's
"text"    the result, as a string, must equal the keyed option's text and no
          other's (letter series, codes, ratios)

SYLLOGISMS holds the "which conclusions follow" questions as their premises and
their two conclusions, each (kind, subject, predicate) with kind A, E, I or O;
recheck_ugc_paper1.py decides them on a Venn diagram, and finds each premise among
the stem's statements, and each conclusion after its numeral, in words.
"""
import math
from fractions import Fraction


def shift(word, k):
    return "".join(chr((ord(c) - 65 + k) % 26 + 65) for c in word)


def opposite(word):
    return "".join(chr(155 - ord(c)) for c in word)     # A (65) <-> Z (90)


def ratio(*parts):
    g = 0
    for p in parts:
        g = math.gcd(g, p)
    return " : ".join(str(p // g) for p in parts)


def chain(ab, bc):
    """A : B and B : C combined into A : B : C."""
    (a, b1), (b2, c) = ab, bc
    return ratio(a * b2, b1 * b2, c * b1)


def largest(fracs):
    return max(fracs, key=Fraction)


def h_index(citations):
    c = sorted(citations, reverse=True)
    return sum(1 for i, x in enumerate(c, 1) if x >= i)


COMPUTED = {
    # Unit I Q20: SGPA, credit-weighted
    (1, 20): ("(4*8 + 3*6 + 3*10) / (4 + 3 + 3)", "number", ["grade points 8, 6 and 10", "4, 3 and 3 credits"]),
    # Unit II Q16: h-index of six papers
    (2, 16): ("h_index([12, 10, 7, 5, 3, 1])", "number", ["12, 10, 7, 5, 3 and 1"]),
    # Unit V
    (5, 1): ("95 * 2 + 1", "number", ["5, 11, 23, 47, 95"]),
    (5, 4): ("chr(ord('L') + 3)", "text", ["C, F, I, L"]),
    (5, 5): ("chr(ord('T') - 2)", "text", ["Z, X, V, T"]),
    (5, 6): ("shift('APPLE', 1)", "text", ["MANGO", "NBOHP", "APPLE"]),
    (5, 7): ("opposite('DOG')", "text", ["CAT", "XZG", "DOG"]),
    (5, 8): ("math.hypot(6, 8)", "number", ["6 km south", "8 km"]),
    (5, 10): ("largest(['3/4', '5/7', '7/9', '2/3'])", "text", ["largest"]),
    (5, 11): ("2 * 30 * 60 / (30 + 60)", "number", ["30 km/h", "60 km/h"]),
    (5, 12): ("90 * 1000 / 3600", "number", ["90 km/h"]),
    (5, 13): ("(200 + 300) / (72 * 1000 / 3600)", "number", ["200 m", "72 km/h", "300 m"]),
    (5, 14): ("100 * 1.10 * 0.90", "number", ["raised by 10%", "lowered by 10%"]),
    (5, 15): ("chain((3, 4), (6, 7))", "text", ["A : B = 3 : 4", "B : C = 6 : 7"]),
    (5, 16): ("(1500 - 1250) / 1250 * 100", "number", ["₹1,250", "₹1,500"]),
    (5, 17): ("1200 * (1 - 0.10) * (1 - 0.05)", "number", ["₹1,200", "10% and 5%"]),
    (5, 18): ("5000 * (1 + 0.08) ** 2 - 5000 - 5000 * 0.08 * 2", "number", ["₹5,000", "2 years", "8%"]),
    (5, 19): ("13310 / 1.1 ** 3", "number", ["₹13,310", "3 years", "10%"]),
    (5, 20): ("(40 * 50 + 60 * 60) / (40 + 60)", "number", ["40 students average 50", "60 students average 60"]),
    # Unit VII, data set 1 (sales in thousands: A, B, C over 2021-2024)
    (7, 1): ("SALES['A'][2] + SALES['B'][2] + SALES['C'][2]", "number", ["2023"]),
    (7, 2): ("(SALES['A'][3] - SALES['A'][2]) / SALES['A'][2] * 100", "number", ["2023 to 2024"]),
    (7, 3): ("SALES['B'][1] / sum(v[1] for v in SALES.values()) * 100", "number", ["2022"]),
    (7, 4): ("sum(SALES['C']) / 4", "number", ["four years"]),
    (7, 5): ("str(next(2021 + i for i in range(1, 4) if SALES['B'][i] < SALES['B'][i - 1]))", "text", ["B's sales fall"]),
    # Unit VII, data set 2 (a budget of 50 lakh, shares in percent)
    (7, 6): ("50 * SHARE['Laboratories'] / 100", "number", ["laboratories"]),
    (7, 7): ("SHARE['Library'] * 360 / 100", "number", ["Library"]),
    (7, 8): ("50 * (SHARE['Salaries'] - SHARE['Laboratories'] - SHARE['Scholarships']) / 100", "number", ["salaries", "laboratories and scholarships"]),
    (7, 9): ("ratio(SHARE['Maintenance'], SHARE['Scholarships'])", "text", ["maintenance", "scholarships"]),
    (7, 10): ("50 * 1.2 * SHARE['Library'] / 100", "number", ["20% larger", "library"]),
    # Unit VIII
    (8, 1): ("8", "number", ["byte", "bits"]),
    (8, 2): ("2 * 1024 * 8", "number", ["1,024 bytes", "2 KB"]),
    (8, 3): ("int('1011', 2)", "number", ["1011"]),
    (8, 4): ("int('11001', 2)", "number", ["11001"]),
}

# Dated facts and counts: the keyed option's number must be this one (and no other
# option's), and the unit's notes page must state it in the words given, so the
# question and the notes cannot disagree.
FACTS = {
    (8, 19): (2015, "launched on 1 July 2015"),
    (9, 1): (17, "17 goals and 169 targets"),
    (9, 2): (169, "17 goals and 169 targets"),
    (9, 12): (1986, "The Environment (Protection) Act, 1986"),
    (9, 13): (8, "It has eight national missions"),
    (9, 16): (1997, "Kyoto Protocol 1997 (in force 2005)"),
    (10, 6): (1956, "made a statutory body by the UGC Act, 1956"),
    (10, 8): (1994, "1994 National Assessment and Accreditation Council (NAAC)"),
    (10, 9): (1985, "the national open university, in 1985"),
    (10, 19): (1992, "revised in 1992 with a Programme of Action"),
}

SALES = {"A": [30, 36, 45, 54], "B": [40, 38, 42, 48], "C": [25, 30, 33, 36]}
SHARE = {"Salaries": 45, "Library": 10, "Laboratories": 15, "Maintenance": 12, "Scholarships": 8, "Others": 10}
assert sum(SHARE.values()) == 100
# The data sets these figures come from: the passage whose label starts with the key
# must hold exactly this table (row label -> its numbers, in order).
TABLES = {(7, "Data set 1"): SALES, (7, "Data set 2"): {k: [v] for k, v in SHARE.items()}}

SYLLOGISMS = {
    (6, 1): ([("A", "doctor", "graduate"), ("I", "graduate", "teacher")],
             ("I", "doctor", "teacher"), ("I", "teacher", "graduate")),
    (6, 2): ([("E", "apple", "mango"), ("A", "mango", "fruit")],
             ("O", "fruit", "apple"), ("E", "fruit", "apple")),
    (6, 3): ([("A", "pen", "pencil"), ("A", "pencil", "eraser")],
             ("A", "pen", "eraser"), ("I", "eraser", "pen")),
    (6, 4): ([("I", "cat", "dog"), ("I", "dog", "rat")],
             ("I", "cat", "rat"), ("E", "cat", "rat")),
    (6, 5): ([("E", "book", "pen"), ("I", "pen", "box")],
             ("O", "box", "book"), ("I", "book", "box")),
}
