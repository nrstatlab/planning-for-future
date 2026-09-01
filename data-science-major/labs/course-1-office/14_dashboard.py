"""Experiment 14 -- Dashboard with combo charts, sparklines and slicers.

The capstone, and the one where a sheet that looks finished is most often
wrong. Everything a dashboard shows is derived, so a dashboard multiplies
whatever mistake is underneath it by the number of tiles on the page.

Two derived values are computed here and both need care:

  * the growth column, which divides by the previous period -- and the
    previous period can be zero, which is where IFERROR from experiment 9
    earns its place;
  * the sparkline series, whose shape depends on whether a missing month is
    drawn as a gap or as a zero.

Same nine transactions as experiment 11.
"""
from collections import defaultdict

from fixtures import sales_rows

ROWS = sales_rows()
MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"]
DIV0 = "#DIV/0!"


def monthly_revenue(rows, months=MONTHS):
    """Revenue per month, with every month in the range present.

    The pivot in experiment 11 lists only the four months that HAVE sales.
    Laying the series out against a complete month range instead is what
    makes a trend line honest -- and it is what puts a zero into the
    denominator of the growth column.
    """
    totals = defaultdict(int)
    for _product, _region, date, _qty, revenue in rows:
        totals[date[:7]] += revenue
    return [totals[m] for m in months]


def growth(series):
    """=IFERROR((B3-B2)/B2, "n/a")  filled down the column."""
    out = [None]
    for previous, current in zip(series, series[1:]):
        out.append(DIV0 if previous == 0 else (current - previous) / previous)
    return out


def main():
    series = monthly_revenue(ROWS)
    assert series == [5180, 2480, 0, 3640, 1580], series
    assert sum(series) == 12880

    # --- KPI cells ----------------------------------------------------------
    total = sum(r[4] for r in ROWS)
    by_product = defaultdict(int)
    for product, _region, _date, _qty, revenue in ROWS:
        by_product[product] += revenue
    best = max(by_product, key=by_product.get)
    average = total / len(ROWS)

    print("  KPI cells")
    print(f"    Total revenue              {total:>12,}")
    print(f"    Best product               {best:>12}  "
          f"({by_product[best]:,})")
    print(f"    Average per transaction    {average:>12,.2f}")
    print(f"    Transactions               {len(ROWS):>12,}")

    assert total == 12880
    assert best == "Rice 5kg" and by_product[best] == 5600
    assert round(average, 2) == 1431.11
    assert sum(by_product.values()) == total

    # --- the combo chart's two series ---------------------------------------
    # Columns = revenue (rupees, thousands). Line = growth (a percentage).
    # They share nothing but a category axis, which is precisely why the line
    # needs a SECONDARY axis: on one axis a 30% growth figure plots as 0.3 of
    # a rupee and vanishes into the baseline.
    rates = growth(series)
    print("\n  Combo chart series (columns = revenue, line = growth)")
    print(f"    {'Month':<10}{'Revenue':>10}{'Growth':>12}")
    for month, revenue, rate in zip(MONTHS, series, rates):
        if rate is None:
            shown = "-"
        elif rate == DIV0:
            shown = DIV0
        else:
            shown = f"{rate:.2%}"
        print(f"    {month:<10}{revenue:>10,}{shown:>12}")

    assert rates[0] is None
    assert round(rates[1], 4) == round((2480 - 5180) / 5180, 4)
    assert rates[2] == -1.0                     # a month with no sales at all
    assert rates[3] == DIV0                     # ...and then dividing by it
    assert round(rates[4], 4) == round((1580 - 3640) / 3640, 4)

    print(f"\n    March has no sales, so April's growth divides by zero.")
    print(f"    That is the {DIV0} the =IFERROR(...) wrapper from experiment")
    print("    9 exists for. Without it the chart's line series breaks at")
    print("    April and the tile shows an error where a number should be.")

    # The alternative most students reach for -- drop the empty month -- does
    # not fix anything, it hides it. February to April then reads as one
    # step of +46.77% growth when it is two months of change, and nothing on
    # the chart says so.
    present = [v for v in series if v]
    misleading = growth(present)[2]
    assert round(misleading, 4) == round((3640 - 2480) / 2480, 4)
    print(f"\n    Dropping March instead gives April a growth of "
          f"{misleading:.2%},")
    print("    which is two months of change labelled as one. Neither the")
    print("    chart nor the number admits it. Keep the empty month.")

    # --- sparklines ---------------------------------------------------------
    # One tiny line per product row, drawn from that row's monthly series.
    print("\n  Sparkline series, one row per product")
    print(f"    {'Product':<15}" + "".join(f"{m[-2:]:>8}" for m in MONTHS) +
          f"{'Total':>9}")
    for product in sorted(by_product, key=by_product.get, reverse=True):
        product_rows = [r for r in ROWS if r[0] == product]
        product_series = monthly_revenue(product_rows)
        assert sum(product_series) == by_product[product]
        print(f"    {product:<15}" +
              "".join(f"{v:>8,}" for v in product_series) +
              f"{sum(product_series):>9,}")

    # --- what to check before you submit ------------------------------------
    print("\n  Before submitting, verify each of these on the sheet itself:")
    for item in [
            "every pivot is connected to the slicer (Report Connections)",
            "the growth line is on the SECONDARY axis, not the primary",
            "the growth column is wrapped in IFERROR",
            "empty periods are shown, not silently dropped",
            "gridlines hidden, working sheets hidden, dashboard protected"]:
        print(f"    [ ] {item}")


if __name__ == "__main__":
    main()
