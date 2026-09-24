"""Experiment 7 — Creating basic visualizations in Power BI.

A chart cannot be asserted, but the DATA BEHIND IT can, and that is where
visuals go wrong. Every function here computes exactly what one visual would
show and checks it -- so if the figure on your card disagrees with this, the
visual is wrong, not the note.

The chart images are rendered to PNG too, so the shapes can be looked at.
"""
import pathlib

import matplotlib
matplotlib.use("Agg")                     # no display in this environment
import matplotlib.pyplot as plt

from fixtures import star

DF = star()
OUT = pathlib.Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)


def card_values():
    """Cards: one number each. The unit-5.md rule is 3-5 of them."""
    cards = {
        "Total Revenue": DF["revenue"].sum(),
        "Total Profit": DF["profit"].sum(),
        "Units Sold": DF["qty"].sum(),
        "Margin %": DF["profit"].sum() / DF["revenue"].sum() * 100,
    }
    assert cards["Total Revenue"] == 12880.0
    assert cards["Total Profit"] == 3525.0
    assert cards["Units Sold"] == 87
    assert round(cards["Margin %"], 4) == 27.3680
    assert len(cards) == 4, "3-5 cards; four is right"

    print("  cards:")
    for name, value in cards.items():
        shown = f"{value:,.2f}%" if name.endswith("%") else f"{value:,.0f}"
        print(f"    {name:15s} {shown:>12s}")
    print("       every one of these needs a comparison beside it -- vs target,")
    print("       vs last period, or vs a peer. A bare number is not information")


def bar_chart_data():
    """A ranked bar chart: revenue by category, sorted descending."""
    data = DF.groupby("category")["revenue"].sum().sort_values(ascending=False)

    assert list(data.index) == ["Grocery", "Personal", "Stationery"], list(data.index)
    assert list(data.values) == [9800.0, 1680.0, 1400.0], list(data.values)
    assert data.sum() == 12880.0
    assert list(data.values) == sorted(data.values, reverse=True), "SORT the bars"

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(data.index, data.values, color="#0f4c81")
    ax.set_ylim(0, None)                  # zero baseline -- unit-5.md's rule
    ax.set_ylabel("Revenue")
    ax.set_title("Revenue by category")
    fig.tight_layout()
    fig.savefig(OUT / "07_bar_category.png", dpi=110)
    plt.close(fig)

    print("  bar (revenue by category, ranked):")
    for cat, val in data.items():
        print(f"    {cat:11s} {val:>9,.0f}  {'#' * int(val / 400)}")
    print("       sorted descending, y-axis starting at ZERO. Both are rules,")
    print("       not preferences -- bar LENGTH is the message")


def line_chart_needs_ordered_time():
    """A line chart over quarters. Order by time, never by value."""
    data = DF.groupby("quarter")["revenue"].sum().sort_index()

    assert list(data.index) == ["Q1", "Q2"]
    assert list(data.values) == [7660.0, 5220.0], list(data.values)
    assert data.sum() == 12880.0

    change = (data["Q2"] - data["Q1"]) / data["Q1"] * 100
    assert round(change, 4) == -31.8538, round(change, 4)

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(data.index, data.values, marker="o", color="#0f4c81")
    ax.set_ylim(0, None)
    ax.set_ylabel("Revenue")
    ax.set_title("Revenue by quarter")
    fig.tight_layout()
    fig.savefig(OUT / "07_line_quarter.png", dpi=110)
    plt.close(fig)

    print(f"  line (revenue by quarter): Q1 {data['Q1']:,.0f} -> "
          f"Q2 {data['Q2']:,.0f}  ({change:+.2f}%)")
    print("       a line chart implies ORDER. Sorting it by value would make")
    print("       the line meaningless while still looking like a chart")


def matrix_is_a_pivot_table():
    """Region x category, with margins -- Course 1's pivot table, again."""
    pivot = DF.pivot_table(index="region", columns="category",
                           values="revenue", aggfunc="sum", fill_value=0,
                           margins=True, margins_name="Total")

    assert pivot.loc["Total", "Total"] == 12880.0
    assert pivot.loc["South", "Grocery"] == 8680.0, pivot.loc["South", "Grocery"]
    assert pivot.loc["North", "Grocery"] == 1120.0
    assert pivot.loc["North", "Personal"] == 0, "North sold no Personal items"
    assert pivot.loc["South", "Total"] == 10360.0
    assert pivot.loc["North", "Total"] == 2520.0

    print("  matrix (region x category):")
    print(pivot.to_string().replace("\n", "\n    ").rjust(4))
    print("       this is Course 1's pivot table with a different name.")
    print("       fill_value=0 matters: an empty cell reads as 'unknown',")
    print("       a zero reads as 'none sold'. They are different claims")


def pie_chart_is_usually_wrong():
    """Five slices or fewer, parts of one whole -- and a bar is usually better."""
    data = DF.groupby("category")["revenue"].sum().sort_values(ascending=False)
    exact = data / data.sum() * 100
    shares = exact.round(4)

    assert len(data) == 3, "three slices is within the limit"
    # Check the EXACT shares sum to 100; the rounded ones total 100.0001,
    # which is itself the reason a pie's printed labels rarely add up.
    assert round(exact.sum(), 9) == 100.0, "parts of ONE whole -- required"
    assert round(shares.sum(), 4) == 100.0001, shares.sum()
    assert round(shares["Grocery"], 4) == 76.087, shares["Grocery"]
    assert round(shares["Personal"], 4) == 13.0435
    assert round(shares["Stationery"], 4) == 10.8696

    # The reason a bar is better: the two small slices are hard to rank by eye.
    gap = abs(shares["Personal"] - shares["Stationery"])
    assert round(gap, 4) == 2.1739, gap

    print("  pie (category share):")
    for cat, pct in shares.items():
        print(f"    {cat:11s} {pct:>7.2f}%")
    print(f"    {'(sum)':11s} {shares.sum():>7.4f}%  <- rounded labels overshoot 100")
    print(f"       Personal and Stationery differ by {gap:.2f} points. As angles")
    print("       that is nearly indistinguishable; as bar lengths it is obvious.")
    print("       Pie: parts of ONE whole, 5 slices max, and only when 'about")
    print("       half' is the message rather than a ranking")


def main():
    print("Experiment 7 -- Basic visualizations")
    card_values()
    bar_chart_data()
    line_chart_needs_ordered_time()
    matrix_is_a_pivot_table()
    pie_chart_is_usually_wrong()
    print(f"  charts written to {OUT.name}/")


if __name__ == "__main__":
    main()
