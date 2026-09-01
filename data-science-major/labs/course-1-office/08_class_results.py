"""Experiment 8 -- Class-wise and subject-wise results for twenty students.

Two mistakes make this experiment's sheet calculate perfectly and report
nonsense. Both are demonstrated here with the actual class, because a warning
in prose is easy to nod at and forget:

  1. Grading on the TOTAL instead of the average. The cut-offs (90/75/60/40)
     are percentages; a total out of 500 clears 90 almost automatically.
  2. Deciding pass/fail on the AVERAGE instead of every subject. A student can
     average well above 40 while failing a paper outright.

The corrected formulas, and the column layout every one of them depends on,
are in notes/sem-1/course-1-computer-fundamentals/lab.md.
"""
from collections import Counter

from fixtures import STUDENTS, SUBJECTS, PASS_MARK, GRADE_BANDS, FAIL_GRADE


def grade(score):
    """K2  =IF(I2>=90,"A",IF(I2>=75,"B",IF(I2>=60,"C",IF(I2>=40,"D","F"))))"""
    for cutoff, letter in GRADE_BANDS:
        if score >= cutoff:
            return letter
    return FAIL_GRADE


def rows():
    """Per student: total, average, result, grade -- columns H, I, J, K."""
    out = []
    for roll, name, *marks in STUDENTS:
        total = sum(marks)                              # H  =SUM(C2:G2)
        average = total / len(marks)                    # I  =AVERAGE(C2:G2)
        result = "Pass" if min(marks) >= PASS_MARK else "Fail"
        out.append((roll, name, marks, total, average, result, grade(average)))
    return out


def main():
    table = rows()

    print(f"  {'Roll':>4}  {'Name':<10}" +
          "".join(f"{s[:4]:>6}" for s in SUBJECTS) +
          f"{'Total':>7}{'Avg':>7}  {'Result':<7}{'Grade':>5}")
    print("  " + "-" * 74)
    for roll, name, marks, total, average, result, letter in table:
        print(f"  {roll:>4}  {name:<10}" + "".join(f"{m:>6}" for m in marks) +
              f"{total:>7}{average:>7.1f}  {result:<7}{letter:>5}")

    # --- the class summary the experiment asks for --------------------------
    dist = Counter(r[6] for r in table)
    assert dist == Counter({"B": 6, "D": 6, "C": 4, "A": 3, "F": 1}), dist
    fails = [r[1] for r in table if r[5] == "Fail"]
    assert fails == ["Divya", "Ishita", "Kavya", "Rahul"], fails
    print(f"\n  Grade distribution   " +
          "  ".join(f"{g}:{dist[g]}" for g in "ABCDF"))
    print(f"  Passed {len(table) - len(fails)} of {len(table)}; "
          f"failed: {', '.join(fails)}")

    # --- subject-wise: highest, lowest, average, pass count -----------------
    print(f"\n  {'Subject':<12}{'High':>6}{'Low':>6}{'Average':>9}{'Passed':>8}")
    print("  " + "-" * 41)
    for i, subject in enumerate(SUBJECTS):
        column = [r[2][i] for r in table]
        passed = sum(1 for m in column if m >= PASS_MARK)
        print(f"  {subject:<12}{max(column):>6}{min(column):>6}"
              f"{sum(column) / len(column):>9.2f}{passed:>8}")
        if subject == "Maths":
            assert (max(column), min(column), passed) == (98, 12, 17)
            assert sum(column) / len(column) == 67.0

    averages = {s: sum(r[2][i] for r in table) / len(table)
                for i, s in enumerate(SUBJECTS)}
    hardest = min(averages, key=averages.get)
    print(f"\n  Hardest paper by class average: {hardest} "
          f"({averages[hardest]:.2f})")

    # --- mistake 1: grading on the total ------------------------------------
    wrong = Counter(grade(r[3]) for r in table)
    assert wrong == Counter({"A": 19, "B": 1}), wrong
    kavya = next(r for r in table if r[1] == "Kavya")
    assert kavya[3] == 80 and kavya[6] == "F" and grade(kavya[3]) == "B"
    print(f"\n  If K2 referenced H2 (the total out of 500) instead of I2:")
    print(f"    grades become {dict(wrong)} -- 19 of 20 students get an A,")
    print(f"    and Kavya, who failed all five papers with {kavya[3]}/500,")
    print(f"    is awarded a {grade(kavya[3])}.")

    # --- mistake 2: pass/fail on the average --------------------------------
    lenient = [r[1] for r in table if r[4] < PASS_MARK]
    assert lenient == ["Kavya"], lenient
    wrongly_passed = sorted(set(fails) - set(lenient))
    assert wrongly_passed == ["Divya", "Ishita", "Rahul"], wrongly_passed
    print(f"\n  If J2 tested the average (>=40) instead of MIN(C2:G2):")
    for name in wrongly_passed:
        r = next(x for x in table if x[1] == name)
        low = min(r[2])
        subject = SUBJECTS[r[2].index(low)]
        print(f"    {name:<9} averages {r[4]:.1f} but scored "
              f"{low} in {subject} -- passed in error")


if __name__ == "__main__":
    main()
