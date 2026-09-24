"""Experiment 13 -- Budget planning with Goal Seek and Scenario Manager.

Goal Seek is a numerical root finder wearing a dialog box. It changes one
cell, watches another, and stops when the watched cell reaches your target.
Implementing it -- properly, with bisection, not by rearranging the algebra --
is the only way to see why it sometimes fails to converge, which is the
question the examiner asks.

The syllabus asks for three things and students routinely stop at the first:
Goal Seek, Scenario Manager, and a one-variable Data Table. All three are
here.
"""
from fixtures import INCOME, EXPENSES

TOTAL_EXPENSES = sum(EXPENSES.values())


def savings(income=INCOME, expenses=None):
    """B10  =B2-SUM(B4:B9)"""
    return income - (TOTAL_EXPENSES if expenses is None else expenses)


def savings_rate(income):
    """B11  =B10/B2   -- savings as a fraction of income."""
    return savings(income) / income


def goal_seek(formula, target, lo, hi, tolerance=1e-9, max_iterations=100):
    """What Tools -> Goal Seek does: change one cell until another hits a
    target. Bisection needs the answer bracketed and the formula monotonic
    over the bracket -- exactly the two conditions under which Excel's own
    Goal Seek reports 'may not have found a solution'.
    """
    f_lo, f_hi = formula(lo) - target, formula(hi) - target
    if f_lo * f_hi > 0:
        raise ValueError("target is not bracketed -- Goal Seek would fail")
    for iterations in range(1, max_iterations + 1):
        mid = (lo + hi) / 2
        f_mid = formula(mid) - target
        if abs(f_mid) < tolerance or (hi - lo) / 2 < tolerance:
            return mid, iterations
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    raise RuntimeError("did not converge")


def main():
    print(f"  Monthly income          {INCOME:>10,}")
    for name, amount in EXPENSES.items():
        print(f"    {name:<20}{amount:>10,}")
    print(f"  Total expenses          {TOTAL_EXPENSES:>10,}")
    print(f"  Savings                 {savings():>10,}")
    print(f"  Savings rate            {savings_rate(INCOME):>10.2%}")

    assert TOTAL_EXPENSES == 33000
    assert savings() == 12000
    assert round(savings_rate(INCOME), 6) == round(12000 / 45000, 6)

    # --- Goal Seek 1: a savings amount --------------------------------------
    # Set cell B10 To value 20000 By changing cell B2. Linear, so the answer
    # is obvious -- which makes it the right one to check the machinery on.
    income, iterations = goal_seek(savings, 20000, 0, 500000)
    print(f"\n  Goal Seek: savings of 20,000 by changing income")
    print(f"    income required  {income:>12,.2f}   ({iterations} iterations)")
    assert abs(income - 53000) < 1e-6, income

    # --- Goal Seek 2: a savings RATE ----------------------------------------
    # This is the one worth doing. The rate is NOT linear in income, so you
    # cannot read the answer off the sheet, and 'save 30% of what I earn'
    # needs a bigger rise than most people guess.
    income30, iterations = goal_seek(savings_rate, 0.30, 1, 500000)
    print(f"\n  Goal Seek: a savings RATE of 30% by changing income")
    print(f"    income required  {income30:>12,.2f}   ({iterations} iterations)")
    print(f"    check            {savings_rate(income30):>12.4%}")
    assert abs(income30 - 33000 / 0.70) < 1e-4, income30
    assert abs(income30 - 47142.857142857) < 1e-4
    print(f"    a rise of {income30 - INCOME:,.2f}, to move the rate from "
          f"{savings_rate(INCOME):.2%} to 30%")

    # --- when Goal Seek fails ----------------------------------------------
    # A savings rate of 100% needs infinite income: the target is approached
    # but never reached. Excel would grind through its iteration limit and
    # report that it may not have found a solution.
    try:
        goal_seek(savings_rate, 1.00, 1, 10 ** 9)
        raise AssertionError("a 100% savings rate should not be reachable")
    except ValueError as exc:
        print(f"\n  Goal Seek: a savings rate of 100%  ->  {exc}")

    # --- Scenario Manager ---------------------------------------------------
    scenarios = {
        "Best case":  (52000, 31000),
        "Realistic":  (45000, 33000),
        "Worst case": (41000, 35500),
    }
    print("\n  Scenario Summary")
    print(f"    {'':<14}{'Income':>10}{'Expenses':>11}{'Savings':>10}{'Rate':>9}")
    for name, (inc, exp) in scenarios.items():
        s = inc - exp
        print(f"    {name:<14}{inc:>10,}{exp:>11,}{s:>10,}{s / inc:>9.1%}")

    assert [inc - exp for inc, exp in scenarios.values()] == [21000, 12000, 5500]
    # The realistic column must reproduce the live sheet, or the scenario has
    # drifted from the model it is supposed to describe.
    assert scenarios["Realistic"] == (INCOME, TOTAL_EXPENSES)

    # --- one-variable data table -------------------------------------------
    # Rent down the left column, savings recalculated for each. Data ->
    # What-If Analysis -> Data Table, Column input cell = the rent cell.
    print("\n  One-variable Data Table: savings against rent")
    print(f"    {'Rent':>8}{'Savings':>10}{'Rate':>9}")
    other_expenses = TOTAL_EXPENSES - EXPENSES["Rent"]
    table = []
    for rent in range(12000, 18001, 1000):
        s = savings(expenses=other_expenses + rent)
        table.append((rent, s))
        print(f"    {rent:>8,}{s:>10,}{s / INCOME:>9.1%}")

    assert other_expenses == 18000
    assert table == [(12000, 15000), (13000, 14000), (14000, 13000),
                     (15000, 12000), (16000, 11000), (17000, 10000),
                     (18000, 9000)], table
    # Every extra rupee of rent is a rupee off savings -- the slope is -1, and
    # the table exists to make that visible rather than argued.
    slopes = {(b[1] - a[1]) / (b[0] - a[0]) for a, b in zip(table, table[1:])}
    assert slopes == {-1.0}, slopes
    print(f"\n    Slope: {slopes.pop():.0f} -- one rupee of rent, one rupee "
          "of savings.")


if __name__ == "__main__":
    main()
