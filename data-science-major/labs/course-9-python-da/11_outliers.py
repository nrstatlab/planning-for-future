"""Practical 11 — Rename axes, remove duplicates, filter outliers."""
import numpy as np
import pandas as pd
from fixtures import students, MASKING


def cleaning_column_names():
    df = pd.DataFrame({" Roll No ": [21, 22], "Total  Marks": [88, 65],
                       "DEPT": ["DS", "Stats"]})

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    assert list(df.columns) == ["roll_no", "total__marks", "dept"]

    # A double space becomes a double underscore -- collapse runs with a regex.
    df.columns = df.columns.str.replace(r"_+", "_", regex=True)
    assert list(df.columns) == ["roll_no", "total_marks", "dept"]

    other = pd.DataFrame({"a": [1]}).rename(columns=str.upper)
    assert list(other.columns) == ["A"], "rename also takes a FUNCTION"

    print("  ' Roll No ' -> roll_no; collapse '_+' or you get total__marks")


def renaming_axes():
    df = students()
    r = df.rename(columns={"maths": "mathematics"})
    assert "mathematics" in r.columns and "maths" not in r.columns
    assert "maths" in df.columns, "rename returns a COPY"

    idx = df.set_index("name").rename(index={"Asha": "Asha K"})
    assert "Asha K" in idx.index

    p = df.add_prefix("q1_")
    assert list(p.columns)[0] == "q1_roll"

    print("  rename(columns=), rename(index=), add_prefix -- all return copies")


def deduplication():
    df = pd.DataFrame({
        "roll": [21, 22, 21, 23, 22],
        "name": ["Asha", "Ravi", "Asha", "Meena", "Ravi Teja"],
        "marks": [88, 65, 88, 94, 65]})

    assert df.duplicated().sum() == 1
    assert df.duplicated(subset=["roll"]).sum() == 2
    assert df.duplicated(subset=["roll"], keep=False).sum() == 4

    investigate = df[df.duplicated(subset=["roll"], keep=False)]
    assert len(investigate) == 4, "keep=False shows BOTH sides of every clash"

    assert len(df.drop_duplicates()) == 4
    assert len(df.drop_duplicates(subset=["roll"])) == 3

    print("  keep=False shows both sides of each clash -- what you need to DECIDE")


def masking_z_score_versus_iqr():
    """The demonstration that matters: the z-score rule hides its own outliers."""
    s = MASKING
    assert s.tolist() == [10, 12, 11, 13, 12, 11, 250, 260]

    mu, sd = float(s.mean()), float(s.std())
    assert round(mu, 3) == 72.375
    assert round(sd, 4) == 112.7538

    z = (s - mu) / sd
    assert round(float(z.abs().max()), 4) == 1.664
    assert (z.abs() > 3).sum() == 0, "the z-score rule finds NOTHING"

    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    assert (float(q1), float(q3), float(iqr)) == (11.0, 72.25, 61.25)
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    assert round(float(lo), 3) == -80.875 and round(float(hi), 3) == 164.125

    found = s[(s < lo) | (s > hi)]
    assert found.tolist() == [250, 260], "IQR catches BOTH"

    print(f"  mean {mu:.3f}, sd {sd:.4f} -> 3sd is a band of +/-{3*sd:.1f}")
    print(f"  z-score |z|>3 finds {(z.abs() > 3).sum()}; IQR finds {len(found)}: {found.tolist()}")
    print(f"       the outliers CONCEALED themselves by inflating the sd used")
    print(f"       to find them -- quartiles depend on RANK, so IQR is immune")


def capping_instead_of_deleting():
    s = MASKING
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr

    capped = s.clip(lower=lo, upper=hi)
    assert capped.max() == hi, "winsorised, not deleted"
    assert len(capped) == len(s), "no rows lost"
    assert capped.tolist()[:6] == s.tolist()[:6], "the sensible values are untouched"

    print(f"  clip() caps at {hi:.3f} instead of deleting -- no rows lost")


def domain_rules_come_first():
    df = pd.DataFrame({"age": [25, -3, 40, 215, 33],
                       "marks": [88, 65, 150, 71, 52]})

    valid = df[(df.age.between(0, 120)) & (df.marks.between(0, 100))]
    # Three rows fail: age -3, age 215, and marks 150. Only rows 0 and 4 pass
    # BOTH rules -- note that row 2 has a perfectly good age and an impossible
    # mark, so a per-column check would have kept it.
    assert len(valid) == 2, valid
    assert valid.age.tolist() == [25, 33]
    assert valid.marks.tolist() == [88, 52]
    assert -3 not in valid.age.tolist() and 215 not in valid.age.tolist()
    assert 150 not in valid.marks.tolist()

    print("  domain rules first: age -3 and 215, marks 150 are invalid whatever")
    print("       the quartiles say -- statistics cannot tell you a mark of 150")
    print("       is impossible, but the syllabus can")


def main():
    print("Practical 11 -- Renaming, duplicates, outliers")
    cleaning_column_names()
    renaming_axes()
    deduplication()
    masking_z_score_versus_iqr()
    capping_instead_of_deleting()
    domain_rules_come_first()


if __name__ == "__main__":
    main()
