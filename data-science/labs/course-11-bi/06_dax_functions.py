"""Experiment 6 — Implementing DAX functions.

DAX cannot be executed outside Power BI, so this script implements its
SEMANTICS in pandas and asserts the figures quoted in unit-2.md. The point is
not to reimplement DAX; it is that every number the notes claim -- 87, 9,
9.667, 12880, 3525, 29.7619%, 27.3680%, 80.43% -- is produced by running code.

The three ideas being modelled:
  * filter context      -- what a measure can see when a visual renders
  * CALCULATE           -- REPLACING a filter rather than adding to it
  * measure vs column   -- aggregate-then-divide, not divide-then-average
"""
import pandas as pd

from fixtures import star

DF = star()


# --- the model: a filter context is just a boolean mask ---------------------

def in_context(**filters):
    """The rows a visual would be showing, given its filters."""
    df = DF
    for col, val in filters.items():
        df = df[df[col] == val]
    return df


# --- the aggregation functions the syllabus names ---------------------------

def sum_count_average():
    """SUM, COUNT, COUNTROWS, AVERAGE, DISTINCTCOUNT -- unit-2.md's table."""
    total_qty = DF["qty"].sum()
    count_qty = DF["qty"].notna().sum()          # COUNT ignores blanks
    countrows = len(DF)                          # COUNTROWS does not
    avg_qty = DF["qty"].mean()
    distinct_products = DF["product_key"].nunique()

    assert total_qty == 87, total_qty
    assert count_qty == 9 and countrows == 9
    assert round(avg_qty, 3) == 9.667, avg_qty
    assert avg_qty == total_qty / countrows
    assert distinct_products == 4

    print(f"  SUM(qty)                = {total_qty}")
    print(f"  COUNT(qty)              = {count_qty}")
    print(f"  COUNTROWS(fact_sales)   = {countrows}")
    print(f"  AVERAGE(qty)            = {avg_qty:.3f}   ({total_qty}/{countrows})")
    print(f"  DISTINCTCOUNT(product)  = {distinct_products}")


def count_and_countrows_disagree_on_blanks():
    """The examinable difference, shown rather than asserted in prose."""
    with_blank = DF.copy()
    with_blank.loc[with_blank.index[0], "qty"] = None

    count_qty = with_blank["qty"].notna().sum()
    countrows = len(with_blank)

    assert countrows == 9
    assert count_qty == 8, count_qty
    assert count_qty != countrows, "this is the whole point"

    print(f"  blank ONE qty value:  COUNT(qty) = {count_qty}, "
          f"COUNTROWS = {countrows}")
    print("       COUNT ignores blanks; COUNTROWS does not. On a complete")
    print("       column they agree, which is why the difference surprises people")


def sumx_is_row_by_row():
    """Total Revenue = SUMX(fact, qty * price). An iterator, not an aggregator."""
    revenue = (DF["qty"] * DF["list_price"]).sum()
    profit = revenue - (DF["qty"] * DF["unit_cost"]).sum()

    assert revenue == 12880.0, revenue
    assert profit == 3525.0, profit

    # SUM(qty) * SUM(price) is the WRONG answer, and it is a real mistake.
    # SUM(qty)=87, SUM(list_price) over the nine rows = 1620, 87*1620 = 140940.
    wrong = DF["qty"].sum() * DF["list_price"].sum()
    assert DF["list_price"].sum() == 1620.0
    assert wrong == 140940.0, wrong
    assert wrong > revenue * 10

    print(f"  SUMX(fact, qty * price)  = {revenue:,.0f}   CORRECT")
    print(f"  SUM(qty) * SUM(price)    = {wrong:,.0f}   WRONG")
    print("       SUMX evaluates the expression ROW BY ROW and then adds.")
    print("       Multiplying two totals multiplies unrelated things")


# --- CALCULATE ---------------------------------------------------------------

def calculate_replaces_the_filter():
    """The unit-2.md table, reproduced. This is the exam question."""
    south_revenue = in_context(region="South")["revenue"].sum()
    assert south_revenue == 10360.0, south_revenue

    rows = []
    for region in ("North", "South"):
        total_in_context = in_context(region=region)["revenue"].sum()
        # CALCULATE([Total Revenue], region = "South") -- the argument REPLACES
        # the row's own region filter, so it is the same on every row.
        calculated = south_revenue
        rows.append((region, total_in_context, calculated))

    assert rows[0] == ("North", 2520.0, 10360.0), rows[0]
    assert rows[1] == ("South", 10360.0, 10360.0), rows[1]
    assert rows[0][2] == rows[1][2], "identical on both rows -- the filter was REPLACED"
    assert DF["revenue"].sum() == 12880.0

    print("  region   [Total Revenue]   [South Revenue]")
    for region, ctx, calc in rows:
        print(f"  {region:7s} {ctx:>14,.0f} {calc:>17,.0f}")
    print(f"  {'Total':7s} {DF['revenue'].sum():>14,.0f} {south_revenue:>17,.0f}")
    print("       read the NORTH row: [South Revenue] shows South's figure.")
    print("       CALCULATE REPLACED the region filter rather than adding to it")


def keepfilters_intersects_instead():
    """The modifier that makes CALCULATE add rather than replace."""
    south = DF[DF["region"] == "South"]["revenue"].sum()

    results = {}
    for region in ("North", "South"):
        ctx = DF[DF["region"] == region]
        # KEEPFILTERS: intersect the outer filter with the inner one.
        kept = ctx[ctx["region"] == "South"]["revenue"].sum()
        results[region] = kept

    assert results["South"] == 10360.0
    assert results["North"] == 0.0, "North AND South is empty -- correctly"
    assert south == 10360.0

    print(f"  with KEEPFILTERS:  North -> {results['North']:,.0f}   "
          f"South -> {results['South']:,.0f}")
    print("       North INTERSECT South is empty, so it is 0 rather than 10,360.")
    print("       That is the difference between replacing and intersecting")


def all_removes_filters_for_pct_of_total():
    """Pct of Total = DIVIDE([Rev], CALCULATE([Rev], ALL(dim_store)))."""
    grand = DF["revenue"].sum()
    pcts = {}
    for region in ("South", "North"):
        rev = DF[DF["region"] == region]["revenue"].sum()
        pcts[region] = round(rev / grand * 100, 4)

    assert pcts == {"South": 80.4348, "North": 19.5652}, pcts
    assert round(sum(pcts.values()), 4) == 100.0, "the check that it is right"

    print(f"  grand total (ALL removed the region filter) = {grand:,.0f}")
    for region, pct in pcts.items():
        print(f"    {region:6s} {DF[DF.region == region].revenue.sum():>9,.0f}  {pct:>7.2f}%")
    print(f"    {'':6s} {'':>9s}  {sum(pcts.values()):>7.2f}%  <- sums to 100, so it is right")


def divide_handles_zero_and_slash_does_not():
    """DIVIDE gives you a defined result on a zero denominator; / does not."""
    import math

    empty = DF[DF["region"] == "West"]          # a region with no rows
    numerator = empty["profit"].sum()
    denominator = empty["revenue"].sum()
    assert (numerator, denominator) == (0.0, 0.0)

    # DIVIDE(a, b) -> BLANK when b is 0 (or the third argument, if supplied).
    divide_result = None if denominator == 0 else numerator / denominator
    assert divide_result is None

    # Plain division: Python raises, and numpy/pandas returns nan silently.
    # DAX returns Infinity or NaN. All three are results you did not choose.
    try:
        float(numerator) / float(denominator)
        raise SystemExit("expected ZeroDivisionError from Python floats")
    except ZeroDivisionError:
        pass

    import numpy as np
    with np.errstate(invalid="ignore", divide="ignore"):
        numpy_result = np.float64(numerator) / np.float64(denominator)
    assert math.isnan(numpy_result), numpy_result

    print("  region 'West' has no rows, so revenue sums to 0:")
    print("    DIVIDE(profit, revenue)  -> BLANK, by definition")
    print("    Python float division    -> ZeroDivisionError")
    print("    numpy / pandas division  -> nan, SILENTLY")
    print("    DAX plain '/'            -> Infinity or NaN")
    print("       three engines, three different wrong answers. DIVIDE is the")
    print("       only one where YOU chose what a zero denominator means")


# --- measure vs calculated column -------------------------------------------

def the_average_of_averages_trap():
    """unit-2.md's headline numbers: 29.7619% wrong, 27.3680% right."""
    per_row = DF["profit"] / DF["revenue"] * 100

    as_column = per_row.mean()                                   # WRONG
    as_measure = DF["profit"].sum() / DF["revenue"].sum() * 100   # RIGHT

    assert round(as_column, 4) == 29.7619, round(as_column, 4)
    assert round(as_measure, 4) == 27.3680, round(as_measure, 4)
    assert as_column > as_measure

    # And the reason, stated as an assertion: the measure is revenue-weighted.
    weighted = (per_row * DF["revenue"]).sum() / DF["revenue"].sum()
    assert round(weighted, 4) == round(as_measure, 4), \
        "the correct answer IS the revenue-weighted average of the row margins"

    print(f"  per-row margins: {[round(m, 2) for m in per_row]}")
    print(f"  AVERAGE of the column     = {as_column:.4f}%   WRONG")
    print(f"  SUM(profit)/SUM(revenue)  = {as_measure:.4f}%   RIGHT")
    print(f"  revenue-weighted average  = {weighted:.4f}%   (identical to RIGHT)")
    print(f"  the error is {as_column - as_measure:.4f} percentage points")
    print("       the column treats a Rs 600 line and a Rs 2,800 line as equal.")
    print("       AGGREGATE, THEN DIVIDE -- never divide, then average")


def if_and_switch():
    total_qty = DF["qty"].sum()
    assert total_qty == 87

    def band(q):
        if q > 15:
            return "Large"
        if q > 8:
            return "Medium"
        return "Small"

    # qty values are 10, 5, 8, 6, 20, 12, 4, 7, 15.
    #   Large  (>15): 20                  -> 1
    #   Medium (>8) : 10, 12, 15          -> 3   (15 is NOT > 15)
    #   Small       : 5, 8, 6, 4, 7       -> 5
    bands = DF["qty"].map(band).value_counts().to_dict()
    assert bands == {"Small": 5, "Medium": 3, "Large": 1}, bands
    assert sum(bands.values()) == 9

    print(f"  SWITCH(TRUE(), qty>15 'Large', qty>8 'Medium', 'Small'):")
    for name in ("Large", "Medium", "Small"):
        print(f"    {name:7s} {bands[name]} rows")
    print("       SWITCH(TRUE(), ...) is the DAX idiom for a nested IF.")
    print("       Use it beyond two branches")


def main():
    print("Experiment 6 -- DAX functions")
    sum_count_average()
    count_and_countrows_disagree_on_blanks()
    sumx_is_row_by_row()
    calculate_replaces_the_filter()
    keepfilters_intersects_instead()
    all_removes_filters_for_pct_of_total()
    divide_handles_zero_and_slash_does_not()
    the_average_of_averages_trap()
    if_and_switch()


if __name__ == "__main__":
    main()
