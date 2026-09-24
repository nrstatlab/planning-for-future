"""Experiment 5 — Cleaning a higher-education student performance dataset.

The education case study from unit-1.md §1.4 and unit-2.md §2.7.

The examinable decision is what to do with "AB" (absent). It is not a cleaning
detail -- it changes the pass rate, and two departments that choose differently
will report different figures from the same file. Both choices are computed
here so the difference is a number rather than an opinion.
"""
import pandas as pd

# As received: wide (a column per subject), marks as text, absences as "AB".
RAW = pd.DataFrame({
    "student_id": ["S1", "S2", "S3", "S4", "S5", "S5"],
    "programme":  ["BSc-DS", "BSc-DS", "BSc-DS", "BSc-STAT", "BSc-STAT", "BSc-STAT"],
    "semester":   [5, 5, 5, 5, 5, 5],
    "Maths":      [" 88", "65", "94", "AB", "52", "52"],
    "Stats":      ["91", "58", "89", "66", "AB", "AB"],
    "Python":     ["76", "AB", "81", "70", "45", "45"],
})


def clean_and_reshape():
    """The Power Query pipeline, in order. The order is not arbitrary."""
    df = RAW.copy()

    # 1. Remove Duplicates -- S5 was uploaded twice, identically.
    df = df.drop_duplicates()
    assert len(df) == 5, len(df)

    # 2. Unpivot the subject columns (Tableau: Pivot; pandas: melt).
    long = df.melt(id_vars=["student_id", "programme", "semester"],
                   var_name="subject", value_name="marks_raw")
    assert long.shape == (15, 5), long.shape
    assert set(long["subject"]) == {"Maths", "Stats", "Python"}

    # 3. Trim, then convert. "AB" cannot become a number, so it must be
    #    decided on FIRST -- see the two functions below.
    long["marks_raw"] = long["marks_raw"].str.strip()
    # Three absences survive: S4 Maths, S5 Stats, S2 Python. The fourth "AB"
    # was in S5's duplicate row, which step 1 already removed -- which is
    # itself the reason to de-duplicate BEFORE counting anything.
    assert (long["marks_raw"] == "AB").sum() == 3, "three absences"

    print(f"  {len(RAW)} raw rows -> {len(df)} after Remove Duplicates")
    print(f"  unpivot 3 subject columns -> {long.shape[0]} rows "
          f"({len(df)} students x 3 subjects)")
    print(f"  absences marked 'AB': {(long['marks_raw'] == 'AB').sum()}")
    return long


def ab_as_null_versus_zero(long):
    """The decision that changes the answer. Both computed, neither hidden."""
    as_null = pd.to_numeric(long["marks_raw"], errors="coerce")
    as_zero = as_null.fillna(0)

    assert as_null.isna().sum() == 3
    assert len(as_null) == 15 and as_null.notna().sum() == 12
    assert as_null.sum() == 875.0

    stats = {
        "AB -> null (excluded)": (as_null.mean(), as_null.notna().sum(),
                                  (as_null >= 40).sum() / as_null.notna().sum()),
        "AB -> 0 (counted)":     (as_zero.mean(), len(as_zero),
                                  (as_zero >= 40).sum() / len(as_zero)),
    }

    null_mean, null_n, null_pass = stats["AB -> null (excluded)"]
    zero_mean, zero_n, zero_pass = stats["AB -> 0 (counted)"]

    # 875/12 = 72.9167 excluding absences; 875/15 = 58.3333 counting them as 0.
    assert round(null_mean, 4) == 72.9167, round(null_mean, 4)
    assert round(zero_mean, 4) == 58.3333, round(zero_mean, 4)
    assert round(null_pass * 100, 4) == 100.0, round(null_pass * 100, 4)
    assert round(zero_pass * 100, 4) == 80.0, round(zero_pass * 100, 4)

    print("  the 'AB' decision, both ways:")
    print(f"    {'':24s} {'mean':>8s} {'n':>4s} {'pass rate':>10s}")
    for label, (m, n, p) in stats.items():
        print(f"    {label:24s} {m:8.4f} {n:>4d} {p * 100:9.2f}%")
    print(f"       the mean moves {null_mean - zero_mean:.2f} marks and the pass")
    print(f"       rate {(null_pass - zero_pass) * 100:.2f} points. NEITHER IS WRONG --")
    print("       but the dashboard must say which it did, or two departments")
    print("       will report different pass rates from one file")
    return as_null


def academic_metrics(long, marks):
    """The visuals: subject-wise averages, pass rate, distinction count."""
    df = long.assign(marks=marks).dropna(subset=["marks"])

    by_subject = (df.groupby("subject")
                    .agg(avg=("marks", "mean"), n=("marks", "size"))
                    .round(4).sort_index())
    # One absence per subject, so every subject has 4 of a possible 5 marks.
    assert list(by_subject["n"]) == [4, 4, 4], list(by_subject["n"])
    assert round(by_subject.loc["Maths", "avg"], 4) == 74.75
    assert round(by_subject.loc["Stats", "avg"], 4) == 76.0
    assert round(by_subject.loc["Python", "avg"], 4) == 68.0

    by_prog = (df.groupby("programme")
                 .agg(avg=("marks", "mean"), n=("marks", "size")).round(4))
    assert by_prog.loc["BSc-DS", "n"] == 8
    assert by_prog.loc["BSc-STAT", "n"] == 4
    assert round(by_prog.loc["BSc-DS", "avg"], 4) == 80.25
    assert round(by_prog.loc["BSc-STAT", "avg"], 4) == 58.25

    distinctions = int((df["marks"] >= 75).sum())
    assert distinctions == 6, distinctions

    print("  subject      avg      n")
    for subj, row in by_subject.iterrows():
        print(f"    {subj:9s} {row['avg']:7.2f}  {int(row['n'])}")
    print("  programme    avg      n")
    for prog, row in by_prog.iterrows():
        print(f"    {prog:9s} {row['avg']:7.2f}  {int(row['n'])}")
    print(f"  distinctions (>=75): {distinctions}")
    print("       note the n column: 4, not 5, in every subject -- one student")
    print("       was absent from each. ALWAYS show n beside an average computed")
    print("       after excluding nulls, or it looks more solid than it is.")
    print("       BSc-STAT's 58.25 rests on FOUR marks from two students")


def the_pass_rate_measure_shape(long, marks):
    """CALCULATE in the numerator, plain COUNTROWS in the denominator."""
    df = long.assign(marks=marks).dropna(subset=["marks"])

    numerator = int((df["marks"] >= 40).sum())     # CALCULATE(COUNTROWS, marks>=40)
    denominator = len(df)                          # COUNTROWS(marks)
    pass_rate = numerator / denominator

    assert (numerator, denominator) == (12, 12)
    assert pass_rate == 1.0

    # Raise the bar, to prove the shape works and not just that all 12 passed.
    strict_num = int((df["marks"] >= 75).sum())
    assert strict_num == 6
    assert round(strict_num / denominator * 100, 4) == 50.0

    print(f"  Pass Rate  = CALCULATE(COUNTROWS, marks>=40) / COUNTROWS")
    print(f"             = {numerator}/{denominator} = {pass_rate * 100:.2f}%")
    print(f"  Distinction Rate (>=75) = {strict_num}/{denominator} = "
          f"{strict_num / denominator * 100:.2f}%")
    print("       CALCULATE on top, plain count underneath. That shape is EVERY")
    print("       rate measure in BI -- memorise it once and reuse it")


def main():
    print("Experiment 5 -- Student performance: clean, reshape, measure")
    long = clean_and_reshape()
    marks = ab_as_null_versus_zero(long)
    academic_metrics(long, marks)
    the_pass_rate_measure_shape(long, marks)


if __name__ == "__main__":
    main()
