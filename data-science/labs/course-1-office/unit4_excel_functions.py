"""Unit 4 -- the text, counting and logical functions, with their results.

Unit 4 lists each function beside the answer it produces. Those answers are
claims, so they are checked here: every Result column in the notes' text
function table is recomputed, and so are the two comparisons the notes make a
point of -- COUNT against COUNTA against COUNTBLANK, and nested IF against
IFS.

Excel semantics are reproduced, including the ones that surprise people:
positions are 1-based, FIND is case-sensitive and errors when it fails, and
an empty cell is not the same thing as a zero.

Run by tools/run_office_labs.py.
"""

VALUE_ERROR = "#VALUE!"
EMPTY = None          # an empty cell, as distinct from the empty string


# --- text functions ---------------------------------------------------------
# Positions in Excel start at 1, not 0. Every off-by-one in this experiment
# comes from forgetting that.

def left(text, n):
    return text[:n]


def right(text, n):
    return text[-n:] if n else ""


def mid(text, start, n):
    return text[start - 1:start - 1 + n]


def trim(text):
    """Leading and trailing spaces removed, internal runs collapsed to one."""
    return " ".join(text.split())


def proper(text):
    return text.title()


def find(sub, text):
    """Case-sensitive. Returns #VALUE! when the substring is absent."""
    position = text.find(sub)
    return VALUE_ERROR if position < 0 else position + 1


def search(sub, text):
    """Case-insensitive. Same #VALUE! on failure."""
    position = text.lower().find(sub.lower())
    return VALUE_ERROR if position < 0 else position + 1


def textjoin(separator, ignore_empty, values):
    if ignore_empty:
        values = [v for v in values if v not in (EMPTY, "")]
    return separator.join(values)


TEXT_CASES = [
    ('=LEFT("DataScience",4)',          left("DataScience", 4),      "Data"),
    ('=RIGHT("DataScience",7)',         right("DataScience", 7),     "Science"),
    ('=MID("DataScience",5,7)',         mid("DataScience", 5, 7),    "Science"),
    ('=LEN("Data")',                    len("Data"),                 4),
    ('=TRIM("  a  b  ")',               trim("  a  b  "),            "a b"),
    ('=CONCAT("Data","Science")',       "Data" + "Science",          "DataScience"),
    ('=TEXTJOIN(", ",TRUE,A1:A3)',      textjoin(", ", True, ["a", "b", "c"]),
     "a, b, c"),
    ('=PROPER("john doe")',             proper("john doe"),          "John Doe"),
    ('=UPPER("john doe")',              "john doe".upper(),          "JOHN DOE"),
    ('=FIND("S","DataScience")',        find("S", "DataScience"),    5),
    ('=SEARCH("s","DataScience")',      search("s", "DataScience"),  5),
    ('=SUBSTITUTE("a-b","-","+")',      "a-b".replace("-", "+"),     "a+b"),
    ('=TEXT(0.85,"0%")',                f"{0.85:.0%}",               "85%"),
]


# --- counting ---------------------------------------------------------------

def count(cells):
    """COUNT -- numeric cells only."""
    return sum(1 for c in cells if isinstance(c, (int, float)))


def counta(cells):
    """COUNTA -- every cell that is not empty, text included."""
    return sum(1 for c in cells if c is not EMPTY)


def countblank(cells):
    """COUNTBLANK -- the empty ones."""
    return sum(1 for c in cells if c is EMPTY)


# --- logical ----------------------------------------------------------------

def nested_if(score):
    """=IF(B2>=90,"A",IF(B2>=75,"B",IF(B2>=60,"C",IF(B2>=40,"D","F"))))"""
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"


def ifs(score):
    """=IFS(B2>=90,"A", B2>=75,"B", B2>=60,"C", B2>=40,"D", TRUE,"F")

    The final TRUE is the else branch. Leave it out and a score below 40 gives
    #N/A rather than "F" -- IFS has no default.
    """
    for condition, result in [(score >= 90, "A"), (score >= 75, "B"),
                              (score >= 60, "C"), (score >= 40, "D"),
                              (True, "F")]:
        if condition:
            return result


def main():
    print(f"  {'Formula':<34}{'Result':<14}")
    print("  " + "-" * 50)
    for formula, computed, expected in TEXT_CASES:
        assert computed == expected, (formula, computed, expected)
        print(f"  {formula:<34}{str(computed):<14}ok")

    # FIND is case-sensitive and SEARCH is not. That is the distinction the
    # notes call a standard two-mark question, so it gets an assertion.
    assert find("s", "DataScience") == VALUE_ERROR
    assert search("s", "DataScience") == 5
    assert find("S", "DataScience") == search("S", "DataScience") == 5
    print(f"\n  =FIND(\"s\",\"DataScience\")   {VALUE_ERROR}   "
          "(case-sensitive, and it errors rather than returning 0)")
    print(f"  =SEARCH(\"s\",\"DataScience\") 5         (case-insensitive)")

    # Splitting a full name, the routine exam task. practice.md Q15 quotes
    # the intermediate values for "Ananya Sharma" -- 7, 13 and 6 -- so those
    # are asserted rather than just the answer.
    print()
    for full, expected in [("John Doe", ("John", "Doe")),
                           ("Ananya Sharma", ("Ananya", "Sharma"))]:
        space = find(" ", full)
        first = left(full, space - 1)
        last = right(full, len(full) - space)
        assert (first, last) == expected, (full, first, last)
        print(f"  Splitting {full!r}:  first = {first!r}, last = {last!r}  "
              f"(space at {space}, LEN {len(full)})")
    assert find(" ", "Ananya Sharma") == 7
    assert len("Ananya Sharma") == 13
    assert len("Ananya Sharma") - find(" ", "Ananya Sharma") == 6

    # A name with no space: FIND errors, which is why Q15 says wrap it.
    assert find(" ", "Prince") == VALUE_ERROR
    print(f"  Splitting 'Prince':      FIND(\" \",A2) is {VALUE_ERROR} -- "
          "wrap the pair in IFERROR")

    # --- COUNT vs COUNTA vs COUNTBLANK --------------------------------------
    # One range, three answers. Note that 0 is a number and "" is text.
    cells = [45, EMPTY, "absent", 0, 78, EMPTY, "N/A", 91]
    shown = ["(empty)" if c is EMPTY else repr(c) for c in cells]
    assert (count(cells), counta(cells), countblank(cells)) == (4, 6, 2)
    assert counta(cells) + countblank(cells) == len(cells)
    print(f"\n  A range of {len(cells)}: {', '.join(shown)}")
    print(f"    COUNT       {count(cells)}   numeric cells only "
          "(0 counts; text does not)")
    print(f"    COUNTA      {counta(cells)}   every non-empty cell, "
          "text included")
    print(f"    COUNTBLANK  {countblank(cells)}   the empty ones")
    print("    COUNTA + COUNTBLANK always equals the size of the range; "
          "COUNT does not.")

    # --- nested IF against IFS ----------------------------------------------
    for score in range(0, 101):
        assert nested_if(score) == ifs(score), score
    boundaries = [(90, "A"), (89, "B"), (75, "B"), (74, "C"),
                  (60, "C"), (59, "D"), (40, "D"), (39, "F")]
    for score, expected in boundaries:
        assert nested_if(score) == expected, (score, nested_if(score))
    print("\n  Nested IF and IFS agree on all 101 whole scores from 0 to 100.")
    print("  The cut-offs are inclusive: " + ", ".join(
        f"{s}->{g}" for s, g in boundaries))


if __name__ == "__main__":
    main()
