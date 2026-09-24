"""Experiment 11 — Creating visualizations in Tableau (Marks card, shelves, views).

Experiment 7 covered the chart types Power BI and Tableau share. This one
covers what is specific to Tableau's model: a view's granularity is decided by
the dimensions on the shelves and on the Marks card, and getting that wrong
produces the single most common beginner result -- a scatter plot with one dot.
"""
import pandas as pd

from fixtures import star

DF = star()


def granularity_is_set_by_the_dimensions_in_the_view():
    """The rule that explains every 'why is my chart wrong?' question."""
    cases = [
        ([], 1),                                 # no dimension -> ONE mark
        (["region"], 2),
        (["store"], 3),
        (["category"], 3),
        (["store", "category"], 5),          # NOT 9 -- see below
    ]
    for dims, expected in cases:
        marks = 1 if not dims else len(DF.groupby(dims, observed=True))
        assert marks == expected, (dims, marks, expected)

    # 3 stores x 3 categories is 9 combinations, but only 5 occur in the data.
    cross_product = DF["store"].nunique() * DF["category"].nunique()
    actual = len(DF.groupby(["store", "category"], observed=True))
    assert cross_product == 9 and actual == 5

    print("  dimensions in the view -> number of marks drawn:")
    for dims, expected in cases:
        label = ", ".join(dims) if dims else "(none)"
        print(f"    {label:22s} -> {expected} mark(s)")
    print(f"       store x category could be {cross_product} combinations but only")
    print(f"       {actual} occur, and Tableau draws a mark ONLY where data exists.")
    print("       That is why an absent combination looks identical to a zero --")
    print("       and why unit-4.md insists on a star, where the dimension row")
    print("       exists even when the fact row does not")


def the_scatter_with_one_dot():
    """Two measures and no dimension aggregates everything to a single mark."""
    # What a beginner drags: SUM(revenue) and SUM(profit), nothing else.
    one_mark = (DF["revenue"].sum(), DF["profit"].sum())
    assert one_mark == (12880.0, 3525.0)

    # The fix: a dimension on DETAIL gives one mark per thing.
    per_product = DF.groupby("product").agg(
        revenue=("revenue", "sum"), profit=("profit", "sum"))
    assert len(per_product) == 4, len(per_product)
    assert per_product.loc["Rice 5kg", "revenue"] == 5600.0
    assert per_product["revenue"].sum() == 12880.0

    # And the correlation only exists once there is more than one point.
    corr = per_product["revenue"].corr(per_product["profit"])
    assert round(corr, 4) == 0.9591, round(corr, 4)

    print(f"  SUM(revenue) vs SUM(profit), no dimension -> 1 mark at "
          f"{one_mark[0]:,.0f}, {one_mark[1]:,.0f}")
    print(f"  product on Detail                         -> "
          f"{len(per_product)} marks:")
    for name, r in per_product.iterrows():
        print(f"      {name:14s} revenue {r['revenue']:>8,.0f}  "
              f"profit {r['profit']:>7,.0f}")
    print(f"  correlation across the {len(per_product)} points = {corr:.4f}")
    print("       'my scatter plot has one dot' is ALWAYS the missing Detail")
    print("       dimension. A correlation needs points to be computed from")


def marks_card_encodings():
    """Colour, Size, Label, Detail -- and which of them changes granularity."""
    encodings = [
        ("Colour", "a dimension",  True,  "one mark per value, coloured"),
        ("Colour", "a measure",    False, "a continuous colour ramp"),
        ("Size",   "a measure",    False, "mark area scales"),
        ("Label",  "anything",     False, "text on the mark"),
        ("Detail", "a dimension",  True,  "SPLITS marks without any visual change"),
        ("Tooltip", "anything",    False, "hover text only"),
    ]
    splits = [e for e in encodings if e[2]]
    assert len(splits) == 2
    assert {e[0] for e in splits} == {"Colour", "Detail"}

    print("  Marks card:")
    print(f"    {'shelf':9s} {'holds':13s} {'splits marks?':14s} effect")
    for shelf, holds, splits_marks, effect in encodings:
        print(f"    {shelf:9s} {holds:13s} {str(splits_marks):14s} {effect}")
    print("       DETAIL is the one to know: it changes granularity and changes")
    print("       nothing visible, so it silently alters every aggregate")


def dual_axis_needs_synchronised_scales():
    """Two measures on one chart. Unsynchronised axes mislead."""
    by_quarter = DF.groupby("quarter").agg(
        revenue=("revenue", "sum"), profit=("profit", "sum"))

    assert list(by_quarter["revenue"]) == [7660.0, 5220.0]
    assert list(by_quarter["profit"]) == [1990.0, 1535.0], list(by_quarter["profit"])
    assert by_quarter["revenue"].sum() == 12880.0
    assert by_quarter["profit"].sum() == 3525.0

    rev_change = (by_quarter["revenue"]["Q2"] / by_quarter["revenue"]["Q1"] - 1) * 100
    prof_change = (by_quarter["profit"]["Q2"] / by_quarter["profit"]["Q1"] - 1) * 100
    assert round(rev_change, 4) == -31.8538, round(rev_change, 4)
    assert round(prof_change, 4) == -22.8643, round(prof_change, 4)

    # Profit fell LESS than revenue, so the margin actually improved.
    m1 = by_quarter["profit"]["Q1"] / by_quarter["revenue"]["Q1"] * 100
    m2 = by_quarter["profit"]["Q2"] / by_quarter["revenue"]["Q2"] * 100
    assert round(m1, 4) == 25.9791, round(m1, 4)
    assert round(m2, 4) == 29.4061, round(m2, 4)
    assert m2 > m1, "the margin ROSE while both totals fell"

    print("  quarter   revenue    profit   margin")
    for q, r in by_quarter.iterrows():
        print(f"    {q}      {r['revenue']:>8,.0f}  {r['profit']:>8,.0f}   "
              f"{r['profit'] / r['revenue'] * 100:5.2f}%")
    print(f"    change   {rev_change:>7.2f}%  {prof_change:>7.2f}%   "
          f"{m2 - m1:+5.2f}pp")
    print("       revenue fell 31.85% but profit only 22.86%, so the MARGIN")
    print("       rose 3.43 points. Two falling lines, and the real story is")
    print("       the gap between them. An unsynchronised dual axis rescales")
    print("       each series to fill the plot and hides exactly that")


def geographic_roles():
    """Not runnable -- Tableau geocodes place names. Stated, not tested."""
    places = {"Vijayawada": "City", "Guntur": "City", "Hyderabad": "City",
              "South": "not geographic", "North": "not geographic"}
    cities = [p for p, role in places.items() if role == "City"]
    assert len(cities) == 3
    assert set(cities) == set(DF["store"].unique())

    print(f"  {len(cities)} store names carry the City geographic role: {cities}")
    print("       Tableau assigns Country/State/City/Postcode roles and then")
    print("       generates latitude and longitude itself. When places do not")
    print("       plot it is an unset role or an ambiguous name -- Edit Locations")
    print("       fixes it. 'South' and 'North' are NOT geographic, so a map of")
    print("       region needs a custom territory or a shapefile")


def main():
    print("Experiment 11 -- Tableau visualizations: shelves and the Marks card")
    granularity_is_set_by_the_dimensions_in_the_view()
    the_scatter_with_one_dot()
    marks_card_encodings()
    dual_axis_needs_synchronised_scales()
    geographic_roles()


if __name__ == "__main__":
    main()
