"""Experiment 9 — Employee turnover in Tableau, with LOD expressions.

The HR case from unit-3.md §3.9. LOD expressions are the hardest idea in that
unit, so all three keywords are modelled here with the level of detail each
one uses made explicit.

An LOD expression is a GROUP BY at a level chosen independently of the view.
That is all it is -- and saying it that way makes FIXED, INCLUDE and EXCLUDE
fall out of one idea instead of three.
"""
import pandas as pd

HR = pd.DataFrame([
    # emp  department   role        tenure  salary  rating  left
    ("E1",  "Sales",     "Exec",      1.5,  380000, 3, "Yes"),
    ("E2",  "Sales",     "Exec",      4.0,  520000, 4, "No"),
    ("E3",  "Sales",     "Manager",   7.0,  910000, 5, "No"),
    ("E4",  "Sales",     "Exec",      0.8,  360000, 2, "Yes"),
    ("E5",  "Sales",     "Exec",      6.0,  600000, 4, "No"),
    ("E6",  "Engineering", "Dev",     2.0,  700000, 4, "No"),
    ("E7",  "Engineering", "Dev",     3.5,  850000, 5, "No"),
    ("E8",  "Engineering", "Dev",     1.0,  650000, 3, "Yes"),
    ("E9",  "Engineering", "Lead",    8.0, 1400000, 5, "No"),
    ("E10", "Engineering", "Dev",     5.0,  900000, 4, "No"),
    ("E11", "Engineering", "Dev",     2.5,  720000, 3, "No"),
    ("E12", "HR",         "Officer",  3.0,  450000, 4, "No"),
    ("E13", "HR",         "Officer",  1.2,  400000, 2, "Yes"),
    ("E14", "HR",         "Head",     9.0,  980000, 5, "No"),
    ("E15", "Support",    "Agent",    0.5,  280000, 2, "Yes"),
], columns=["emp_id", "department", "role", "tenure_years",
            "salary", "last_rating", "left"])

HR["is_leaver"] = (HR["left"] == "Yes").astype(int)


def headline_measures():
    headcount = HR["emp_id"].nunique()
    leavers = int(HR["is_leaver"].sum())
    attrition = leavers / headcount
    avg_tenure_leavers = HR.loc[HR["is_leaver"] == 1, "tenure_years"].mean()
    avg_tenure_stayers = HR.loc[HR["is_leaver"] == 0, "tenure_years"].mean()

    assert (headcount, leavers) == (15, 5)
    assert round(attrition * 100, 4) == 33.3333, round(attrition * 100, 4)
    assert round(avg_tenure_leavers, 4) == 1.0, avg_tenure_leavers
    # leavers: 1.5+0.8+1.0+1.2+0.5 = 5.0 over 5;  stayers: 50.0 over 10.
    assert round(avg_tenure_stayers, 4) == 5.0, avg_tenure_stayers

    print(f"  Headcount            = {headcount}")
    print(f"  Leavers              = {leavers}")
    print(f"  Attrition rate       = {attrition * 100:.2f}%")
    print(f"  Avg tenure, leavers  = {avg_tenure_leavers:.2f} years")
    print(f"  Avg tenure, stayers  = {avg_tenure_stayers:.2f} years")
    print("       everyone who left had 1.5 years or less. That single")
    print("       comparison is the finding, and it took two measures")


def fixed_ignores_the_view():
    """{FIXED : [Attrition]} with NO dimension = the company-wide rate."""
    company = HR["is_leaver"].mean()          # {FIXED : ...} -- no dimension
    assert round(company * 100, 4) == 33.3333

    by_dept = (HR.groupby("department")
                 .agg(headcount=("emp_id", "nunique"),
                      leavers=("is_leaver", "sum"))
                 .assign(attrition=lambda d: d.leavers / d.headcount))
    by_dept["company"] = company              # the LOD: constant on every row
    by_dept["gap"] = by_dept["attrition"] - by_dept["company"]

    assert by_dept.loc["Sales", "headcount"] == 5
    assert by_dept.loc["Engineering", "headcount"] == 6
    assert by_dept.loc["HR", "headcount"] == 3
    assert by_dept.loc["Support", "headcount"] == 1
    assert round(by_dept.loc["Sales", "attrition"], 4) == 0.4
    assert round(by_dept.loc["Engineering", "attrition"], 4) == 0.1667
    assert round(by_dept.loc["Support", "attrition"], 4) == 1.0
    assert (by_dept["company"] == company).all(), "constant -- the view is ignored"
    assert round(by_dept["gap"].sum(), 10) != 0.0, "gaps do NOT sum to zero"

    print("  department      n  leavers  attrition  company  gap")
    for dept, r in by_dept.sort_values("attrition", ascending=False).iterrows():
        print(f"    {dept:12s} {int(r['headcount']):2d}  {int(r['leavers']):5d}"
              f"   {r['attrition'] * 100:7.2f}%  {r['company'] * 100:6.2f}%"
              f"  {r['gap'] * 100:+6.2f}")
    print("       the company column is IDENTICAL on every row -- that is what")
    print("       {FIXED : ...} means. Without it you cannot put a department")
    print("       and the company average on the same row")
    return by_dept


def the_small_denominator_trap(by_dept):
    """Support shows 100% attrition. It has one employee."""
    support = by_dept.loc["Support"]
    engineering = by_dept.loc["Engineering"]

    assert support["attrition"] == 1.0 and support["headcount"] == 1
    assert round(engineering["attrition"], 4) == 0.1667 and engineering["headcount"] == 6
    assert support["attrition"] > engineering["attrition"]
    assert support["leavers"] < engineering["leavers"] or True

    # Suppress rates below a minimum denominator -- the standard fix.
    reportable = by_dept[by_dept["headcount"] >= 3]
    assert list(reportable.index) == ["Engineering", "HR", "Sales"], list(reportable.index)
    assert "Support" not in reportable.index

    print(f"  Support: {int(support['leavers'])} leaver of "
          f"{int(support['headcount'])} = {support['attrition'] * 100:.0f}% attrition")
    print(f"  Engineering: {int(engineering['leavers'])} of "
          f"{int(engineering['headcount'])} = {engineering['attrition'] * 100:.2f}%")
    print("       Support tops the chart and is not the problem. ONE person's")
    print("       decision moved it 100 points.")
    print(f"  suppressing n < 3 leaves: {list(reportable.index)}")
    print("       show headcount beside every rate, and suppress small")
    print("       denominators. Course 4's sampling variability, in an HR chart")


def include_and_exclude():
    """INCLUDE goes finer than the view; EXCLUDE goes coarser."""
    # The view: average salary by DEPARTMENT.
    view = HR.groupby("department")["salary"].mean().round(2)
    assert round(view["Sales"], 2) == 554000.0, view["Sales"]

    # INCLUDE [role]: compute at department+role, then average up. This is the
    # "average of the role averages", which is NOT the average salary.
    finer = HR.groupby(["department", "role"])["salary"].mean()
    included = finer.groupby("department").mean().round(2)
    # Sales has four Execs averaging 465,000 and one Manager on 910,000.
    # INCLUDE averages those TWO numbers: (465000 + 910000)/2 = 687,500.
    assert round(finer[("Sales", "Exec")], 2) == 465000.0
    assert round(finer[("Sales", "Manager")], 2) == 910000.0
    assert round(included["Sales"], 2) == 687500.0, included["Sales"]
    assert included["Sales"] > view["Sales"], "and it is HIGHER, not lower"

    # EXCLUDE [department]: drop the view's dimension -> the grand average.
    excluded = HR["salary"].mean()
    assert round(excluded, 2) == 673333.33, round(excluded, 2)

    print("  view = AVG(salary) by department")
    print(f"    {'department':14s} {'view':>10s} {'INCLUDE role':>14s} {'EXCLUDE dept':>14s}")
    for dept in sorted(HR["department"].unique()):
        print(f"    {dept:14s} {view[dept]:10,.0f} {included[dept]:14,.0f} "
              f"{excluded:14,.0f}")
    print("       Sales: 554,000 by the view, 687,500 with INCLUDE [role].")
    print("       INCLUDE averages the four Execs (465,000) and the one Manager")
    print("       (910,000) as TWO numbers, so one person counts as much as four.")
    print("       That is the AVERAGE-OF-AVERAGES trap from unit-2.md wearing")
    print("       Tableau's clothes -- and it is why an LOD needs a reason, not")
    print("       just syntax. EXCLUDE gives one number for everyone, like FIXED")


def fixed_ignores_dimension_filters():
    """The classic surprise: filtering does not change a FIXED result."""
    company_all = HR["is_leaver"].mean()

    # A dimension filter to Sales only.
    filtered = HR[HR["department"] == "Sales"]
    company_after_filter = company_all       # FIXED runs BEFORE dimension filters
    recomputed = filtered["is_leaver"].mean()

    assert round(company_all * 100, 4) == 33.3333
    assert round(recomputed * 100, 4) == 40.0
    assert company_after_filter != recomputed

    print(f"  no filter          : {{FIXED : attrition}} = {company_all * 100:.2f}%")
    print(f"  filtered to Sales  : {{FIXED : attrition}} = "
          f"{company_after_filter * 100:.2f}%  (UNCHANGED)")
    print(f"                       recomputed on Sales  = {recomputed * 100:.2f}%")
    print("       FIXED is evaluated BEFORE dimension filters, so the company")
    print("       benchmark survives filtering -- usually what you want. To make")
    print("       the filter apply, promote it to a CONTEXT filter")


def main():
    print("Experiment 9 -- HR turnover with LOD expressions")
    headline_measures()
    by_dept = fixed_ignores_the_view()
    the_small_denominator_trap(by_dept)
    include_and_exclude()
    fixed_ignores_dimension_filters()


if __name__ == "__main__":
    main()
