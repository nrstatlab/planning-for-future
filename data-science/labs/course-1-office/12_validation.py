"""Experiment 12 -- Data entry form with drop-downs and input rules.

Data Validation is a set of predicates Excel evaluates before it lets a value
into a cell. Writing them out as functions and then testing them against bad
input is exactly what the experiment asks you to demonstrate, and it turns up
the thing the syllabus's own email rule gets wrong.

Every rule below is tested with values that SHOULD pass and values that
SHOULD be rejected. A rule you have not tried to break is a rule you have not
tested.
"""
from datetime import date

COURSES = ["B.Sc. Data Science", "B.Sc. Statistics", "B.Com", "B.A."]
ROLL_MIN, ROLL_MAX = 1, 200
DOB_MIN, DOB_MAX = date(1990, 1, 1), date(2012, 12, 31)


def course_rule(value):
    """Allow -> List, Source: the four courses. A dropdown IS the rule."""
    return value in COURSES


def roll_rule(value):
    """Allow -> Whole number, between 1 and 200."""
    return isinstance(value, int) and ROLL_MIN <= value <= ROLL_MAX


def dob_rule(value):
    """Allow -> Date, between 1990-01-01 and 2012-12-31."""
    return isinstance(value, date) and DOB_MIN <= value <= DOB_MAX


def phone_rule(value):
    """Allow -> Text length, equal to 10."""
    return isinstance(value, str) and len(value) == 10


def email_rule_syllabus(value):
    """Allow -> Custom, formula  =ISNUMBER(SEARCH("@",E2))

    This is the rule the experiment names. It asks one question: does an @
    appear anywhere? SEARCH is case-insensitive and accepts wildcards, and
    ISNUMBER turns "found at position n" into TRUE.
    """
    return isinstance(value, str) and "@" in value


def email_rule_better(value):
    """=AND(ISNUMBER(SEARCH("@",E2)), ISNUMBER(SEARCH(".",E2)),
            LEN(E2)>=6, ISERROR(SEARCH(" ",E2)))

    Still not a real address check -- nothing short of a regular expression
    is -- but it rejects the cases the plain rule lets through.
    """
    return (isinstance(value, str) and "@" in value and "." in value
            and len(value) >= 6 and " " not in value)


CHECKS = [
    ("Course",  course_rule,  "List",         [("B.Sc. Data Science", True),
                                               ("B.Sc. Physics", False),
                                               ("", False)]),
    ("Roll no", roll_rule,    "Whole number", [(1, True), (200, True),
                                               (201, False), (0, False),
                                               (45.5, False)]),
    ("DOB",     dob_rule,     "Date",         [(date(2006, 7, 14), True),
                                               (date(1989, 12, 31), False),
                                               (date(2013, 1, 1), False)]),
    ("Phone",   phone_rule,   "Text length",  [("9876543210", True),
                                               ("98765432", False),
                                               ("98765432101", False)]),
]


def main():
    for field, rule, kind, cases in CHECKS:
        print(f"\n  {field}  --  Allow: {kind}")
        for value, expected in cases:
            got = rule(value)
            assert got == expected, (field, value, got)
            mark = "accepted" if got else "REJECTED"
            shown = ("(empty)" if value == "" else
                     value.isoformat() if isinstance(value, date) else
                     repr(value))
            print(f"    {shown:<24}{mark}")

    # --- the email rule, and what it lets through ---------------------------
    print("\n  Email  --  Allow: Custom,  =ISNUMBER(SEARCH(\"@\",E2))")
    email_cases = [
        "asha@nri.ac.in",
        "ASHA@NRI.AC.IN",
        "@",
        "not an email @ all",
        "asha.nri.ac.in",
    ]
    print(f"    {'value':<24}{'syllabus rule':<16}stricter rule")
    for value in email_cases:
        a = "accepted" if email_rule_syllabus(value) else "REJECTED"
        b = "accepted" if email_rule_better(value) else "REJECTED"
        print(f"    {value:<24}{a:<16}{b}")

    # A single @ character satisfies the rule the syllabus specifies. So does
    # a sentence containing one. Neither is an email address, and Excel will
    # accept both without a murmur.
    assert email_rule_syllabus("@") is True
    assert email_rule_syllabus("not an email @ all") is True
    assert email_rule_better("@") is False
    assert email_rule_better("not an email @ all") is False

    # And what it correctly keeps out.
    assert email_rule_syllabus("asha.nri.ac.in") is False

    print("\n  Both rules accept a real address and reject one with no @.")
    print("  The difference is '@' on its own, and a sentence with an @ in")
    print("  it: the syllabus rule takes both. Say so in the viva -- knowing")
    print("  the limits of your own validation is the point of the exercise.")

    # --- the two tabs students forget --------------------------------------
    print("\n  Every rule needs all three tabs filled in:")
    for tab, purpose in [
            ("Settings",      "the rule itself"),
            ("Input Message", "the hint shown when the cell is selected"),
            ("Error Alert",   "Stop / Warning / Information, and your text")]:
        print(f"    {tab:<16}{purpose}")
    print("\n  Stop refuses the value. Warning and Information both ALLOW it")
    print("  after a confirmation -- so a form that must not accept bad data")
    print("  has to use Stop.")


if __name__ == "__main__":
    main()
