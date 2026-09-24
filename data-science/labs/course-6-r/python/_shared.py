"""Shared sample data for the Course 6 lab equivalents.

Keeping one dataset across experiments means the numbers in one experiment can
be cross-checked against another, which is how several errors were caught while
writing these.
"""

MARKS = [45, 67, 78, 52, 89, 91, 73, 64, 58, 82,
         76, 69, 71, 85, 60, 55, 93, 48, 79, 66]

# Hours studied against exam score -- the same pair used in Course 4 Unit 4,
# so the regression output here must match the notes there.
HOURS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
SCORES = [52, 55, 61, 64, 70, 72, 78, 82, 85, 91]

STUDENTS = [
    # name,      section, gender, hours, marks, attendance
    ("Ananya",   "A", "F",  9, 85, 92),
    ("Bhavana",  "A", "F",  5, 62, 78),
    ("Charan",   "B", "M", 11, 91, 95),
    ("Divya",    "B", "F",  4, 55, 70),
    ("Eshwar",   "A", "M",  7, 74, 85),
    ("Fiona",    "C", "F",  8, 79, 88),
    ("Gopal",    "C", "M",  3, 48, 65),
    ("Harika",   "B", "F", 10, 88, 90),
    ("Ismail",   "A", "M",  6, 68, 80),
    ("Jyothi",   "C", "F",  2, 41, 60),
]
