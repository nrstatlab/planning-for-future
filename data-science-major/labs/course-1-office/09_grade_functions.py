"""Experiment 9 -- Grade evaluation with IF, AND, OR and IFERROR.

The syllabus names all four functions, so all four appear. What this script
adds is the part the examiner actually tests: what each formula does when the
cell is EMPTY, or holds text, or holds a number outside 0-100.

Excel's own quirks are reproduced faithfully rather than tidied up, because
the quirks are the lesson:

  * an empty cell compares as 0, so a blank silently grades "F", not "no data"
  * ISNUMBER is what separates "absent" from "scored nothing"
  * IFERROR only catches ERRORS -- a blank is not an error, so IFERROR does
    not catch it, and the formula the notes give needs ISBLANK as well
"""
from fixtures import GRADE_BANDS, FAIL_GRADE, PASS_MARK

BLANK = ""          # an empty cell
ERROR = "#VALUE!"   # what Excel puts in a cell whose formula failed


def excel_number(cell):
    """How a comparison like B2>=90 sees a cell.

    Excel coerces an empty cell to 0 in a numeric comparison. Text does not
    coerce -- and in a comparison, text sorts ABOVE every number, so
    "absent">=90 is TRUE. That is not a joke; it is why the guarded formula
    below exists.
    """
    if cell is BLANK or cell == BLANK:
        return 0
    if isinstance(cell, str):
        return float("inf")          # text > any number, in Excel's ordering
    return cell


def naive_grade(cell):
    """=IF(B2>=90,"A",IF(B2>=75,"B",IF(B2>=60,"C",IF(B2>=40,"D","F"))))"""
    value = excel_number(cell)
    for cutoff, letter in GRADE_BANDS:
        if value >= cutoff:
            return letter
    return FAIL_GRADE


def guarded_grade(cell):
    """The formula lab.md gives, with the blank and text cases handled:

        =IF(ISBLANK(B2),"Absent",
           IFERROR(IF(NOT(ISNUMBER(B2)),NA(),
             IF(B2>=90,"A",IF(B2>=75,"B",IF(B2>=60,"C",IF(B2>=40,"D","F"))))),
           "No data"))
    """
    if cell is BLANK or cell == BLANK:
        return "Absent"
    if not isinstance(cell, (int, float)):
        return "No data"            # IFERROR catches the NA() we raised
    return naive_grade(cell)


def both_cleared(a, b):
    """=IF(AND(B2>=40, C2>=40), "Pass", "Fail")"""
    return "Pass" if (excel_number(a) >= PASS_MARK and
                      excel_number(b) >= PASS_MARK) else "Fail"


def any_distinction(a, b):
    """=IF(OR(B2>=90, C2>=90), "Distinction", "-")"""
    return "Distinction" if (excel_number(a) >= 90 or
                             excel_number(b) >= 90) else "-"


CASES = [
    #  cell        what it is
    (95,          "a clear A"),
    (75,          "exactly on the B cut-off"),
    (74.9,        "a whisker below it"),
    (39,          "below the pass mark"),
    (0,           "scored nothing"),
    (BLANK,       "an empty cell -- the student was absent"),
    ("AB",        "text typed into the marks column"),
    (ERROR,       "a cell already holding an error"),
]


def main():
    print(f"  {'Cell':<10}{'Naive IF':<12}{'Guarded':<12}What it is")
    print("  " + "-" * 66)
    for cell, description in CASES:
        shown = "(empty)" if cell == BLANK else repr(cell)
        print(f"  {shown:<10}{naive_grade(cell):<12}"
              f"{guarded_grade(cell):<12}{description}")

    # The cut-offs are inclusive: >= means 75 is a B, not a C.
    assert naive_grade(75) == "B" and naive_grade(74.9) == "C"
    assert naive_grade(90) == "A" and naive_grade(89.9) == "B"

    # An empty cell grades F under the naive formula. This is the single
    # result worth remembering from this experiment: the sheet reports a
    # failure for a student who was never examined.
    assert naive_grade(BLANK) == "F"
    assert guarded_grade(BLANK) == "Absent"

    # Text does not error either -- it grades A, because in Excel's ordering
    # text is greater than every number.
    assert naive_grade("AB") == "A"
    assert guarded_grade("AB") == "No data"

    print("\n  AND / OR, on two subjects")
    print(f"  {'B2':>8}{'C2':>8}  {'AND -> Pass?':<14}OR -> Distinction?")
    print("  " + "-" * 50)
    for a, b in [(85, 90), (45, 38), (95, 60), (40, 40), (BLANK, 95)]:
        sa = "(empty)" if a == BLANK else a
        sb = "(empty)" if b == BLANK else b
        print(f"  {str(sa):>8}{str(sb):>8}  {both_cleared(a, b):<14}"
              f"{any_distinction(a, b)}")

    assert both_cleared(45, 38) == "Fail"       # AND needs both
    assert both_cleared(40, 40) == "Pass"       # the boundary passes
    assert any_distinction(95, 60) == "Distinction"
    assert both_cleared(BLANK, 95) == "Fail"    # blank is 0, so AND fails
    assert any_distinction(BLANK, 95) == "Distinction"

    print("\n  IFERROR catches errors, not blanks. Test your sheet with an")
    print("  empty cell as well as with text -- the examiner will.")


if __name__ == "__main__":
    main()
