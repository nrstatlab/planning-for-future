"""Experiment 11 -- Sales report with pivot tables and charts.

A pivot table is a group-by with a layout. Building one by hand once makes
the dialog obvious afterwards: Rows are the group keys down the side, Columns
are the group keys across the top, Values is the aggregation, and the Grand
Total row is the same aggregation with no grouping at all.

The nine rows here are the ones Course 11 loads into Power BI and Tableau, so
the region totals this pivot produces can be compared straight across the
programme -- ₹10,360 for South, computed here with a dictionary and there
with DAX.
"""
from collections import defaultdict

from fixtures import sales_rows

ROWS = sales_rows()   # product, region, date, qty, revenue


def pivot(rows, row_key, col_key, value, aggregate=sum):
    """Rows = row_key, Columns = col_key, Values = aggregate of `value`."""
    buckets = defaultdict(list)
    for row in rows:
        buckets[(row_key(row), col_key(row))].append(value(row))
    return {cell: aggregate(values) for cell, values in buckets.items()}


def render(cells, title, money=True):
    row_labels = sorted({r for r, _c in cells})
    col_labels = sorted({c for _r, c in cells})
    width = max(len(str(x)) for x in list(row_labels) + ["Grand Total"]) + 2

    print(f"\n  {title}")
    print(f"  {'':<{width}}" + "".join(f"{c:>15}" for c in col_labels) +
          f"{'Total':>15}")
    grand = 0
    col_totals = defaultdict(int)
    for r in row_labels:
        total = 0
        line = f"  {r:<{width}}"
        for c in col_labels:
            v = cells.get((r, c), 0)
            total += v
            col_totals[c] += v
            line += f"{v:>15,}" if v else f"{'-':>15}"
        grand += total
        print(line + f"{total:>15,}")
    print(f"  {'Grand Total':<{width}}" +
          "".join(f"{col_totals[c]:>15,}" for c in col_labels) +
          f"{grand:>15,}")
    return grand


def main():
    print(f"  {len(ROWS)} transactions: Product, Region, Date, "
          "Quantity, Revenue\n")
    for product, region, date, qty, revenue in ROWS:
        print(f"    {product:<15}{region:<7}{date}  {qty:>3}  {revenue:>7,}")

    # --- pivot 1: Rows = Region, Columns = Product, Values = Sum of Revenue -
    by_region_product = pivot(ROWS, lambda r: r[1], lambda r: r[0],
                              lambda r: r[4])
    grand = render(by_region_product,
                   "Rows = Region   Columns = Product   Values = Sum of Revenue")

    region_totals = defaultdict(int)
    for (region, _product), value in by_region_product.items():
        region_totals[region] += value
    assert region_totals == {"South": 10360, "North": 2520}, dict(region_totals)
    assert grand == 12880

    # --- pivot 2: Rows = Date grouped by month -----------------------------
    # Right-click a date in the pivot -> Group -> Months. That is all the
    # grouping is: take the first seven characters of the ISO date.
    by_month = pivot(ROWS, lambda r: r[2][:7], lambda r: "Revenue",
                     lambda r: r[4])
    render(by_month, "Rows = Date (grouped by month)   Values = Sum of Revenue")

    months = {m: v for (m, _c), v in by_month.items()}
    assert months == {"2026-01": 5180, "2026-02": 2480,
                      "2026-04": 3640, "2026-05": 1580}, months
    assert sum(months.values()) == 12880

    # There is no March. Excel's date grouping only shows months that OCCUR,
    # so the pivot lists four rows and a line chart drawn from it joins
    # February straight to April -- a two-month gap rendered as one step.
    # Experiment 14 shows what that does to a growth column.
    assert "2026-03" not in months
    print("\n  Note the pivot has four month rows, not five: no sale fell in")
    print("  March, and pivot grouping omits empty periods rather than")
    print("  showing them as zero. Experiment 14 deals with the consequences.")

    # --- Sum vs Count vs Average, the three the examiner asks you to switch -
    qty_sum = sum(r[3] for r in ROWS)
    assert qty_sum == 87
    print(f"\n  Value Field Settings on the same field:")
    print(f"    Sum of Quantity      {qty_sum}")
    print(f"    Count of Quantity    {len(ROWS)}")
    print(f"    Average of Quantity  {qty_sum / len(ROWS):.2f}")
    assert round(qty_sum / len(ROWS), 2) == 9.67

    # --- what a slicer does -------------------------------------------------
    # A slicer is a filter applied before the group-by, nothing more.
    south_only = [r for r in ROWS if r[1] == "South"]
    sliced = pivot(south_only, lambda r: r[1], lambda r: r[0], lambda r: r[4])
    assert sum(sliced.values()) == 10360
    print(f"\n  Slicer set to South: the same pivot now totals "
          f"{sum(sliced.values()):,} -- a filter applied before grouping.")


if __name__ == "__main__":
    main()
