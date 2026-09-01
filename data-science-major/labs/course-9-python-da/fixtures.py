"""Shared fixture data for the Course 9 practicals.

One definition, used by every script, so the labs cannot drift from each other
or from the worked examples in the notes.
"""
import numpy as np
import pandas as pd

STUDENTS = pd.DataFrame({
    "roll":  [21, 22, 23, 24, 25],
    "name":  ["Asha", "Ravi", "Meena", "Kiran", "Bhanu"],
    "dept":  ["DS", "DS", "Stats", "DS", "Stats"],
    "maths": [88, 65, 94, 71, 52],
    "stats": [91, 58, 89, 66, 47],
})

# The Course 4 example, reused so the two courses check each other.
COURSE4_SAMPLE = pd.Series([2, 4, 4, 4, 5, 5, 7, 9])

# Course 3 section 3.7's masking demonstration.
MASKING = pd.Series([10, 12, 11, 13, 12, 11, 250, 260])

MARKS_LONG = pd.DataFrame({
    "roll":    [21, 21, 22, 22, 23, 23, 24, 24, 25, 25],
    "subject": ["maths", "stats"] * 5,
    "marks":   [88, 91, 65, 58, 94, 89, 71, 66, 52, 47],
})


def students():
    return STUDENTS.copy()


def marks_long():
    return MARKS_LONG.copy()
