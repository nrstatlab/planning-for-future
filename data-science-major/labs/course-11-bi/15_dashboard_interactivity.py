"""Experiment 15 — A dashboard with drill-downs, filters and slicers.

The four interactive features from unit-5.md §5.4, with the distinction that
carries the marks made numeric: a FILTER changes which rows are shown, a
PARAMETER changes what is calculated. Same visual, different mechanism.

Drilldown is modelled as walking a hierarchy defined once in the model --
Region -> City -> Store -- which is unit-4.md §4.6's point about defining
hierarchies centrally rather than per visual.
"""
from fixtures import star

DF = star()
HIERARCHY = ["region", "store", "product"]      # Region -> Store -> Product


def drilldown_walks_a_hierarchy():
    """Each level adds a dimension; the grand total never changes."""
    levels = []
    for depth in range(1, len(HIERARCHY) + 1):
        dims = HIERARCHY[:depth]
        g = DF.groupby(dims, observed=True)["revenue"].sum()
        levels.append((dims, len(g), g.sum()))

    # 2 regions -> 3 stores -> 5 distinct (store, product) pairs. Not 9: the
    # fact table has 9 rows, but several are the same product and store on
    # different DATES, and date is not in this hierarchy.
    assert [n for _, n, _ in levels] == [2, 3, 5], [n for _, n, _ in levels]
    assert all(total == 12880.0 for _, _, total in levels), \
        "drilling down NEVER changes the total -- it only redistributes it"

    print("  drill down Region -> Store -> Product:")
    for dims, n, total in levels:
        print(f"    {' > '.join(dims):28s} {n:2d} rows, total {total:>9,.0f}")
    print("       the total is identical at every level. If it changes when you")
    print("       drill, the model is wrong -- usually a fan trap (experiment 14)")


def drill_down_one_item_versus_expand_all():
    """Drilling ONE item is not the same as expanding the whole level."""
    # Expand all: every region gets its stores.
    expand_all = DF.groupby(["region", "store"], observed=True)["revenue"].sum()
    assert len(expand_all) == 3, len(expand_all)

    # Drill into South only: only South's stores appear.
    south_only = (DF[DF["region"] == "South"]
                  .groupby(["region", "store"], observed=True)["revenue"].sum())
    assert len(south_only) == 2, len(south_only)
    assert south_only.sum() == 10360.0
    assert expand_all.sum() == 12880.0
    assert south_only.sum() != expand_all.sum()

    print(f"  Expand all      -> {len(expand_all)} rows, total {expand_all.sum():,.0f}")
    print(f"  Drill into South-> {len(south_only)} rows, total {south_only.sum():,.0f}")
    print("       'expand all' keeps every region and adds a level; 'drill down'")
    print("       on one item FILTERS to it. The totals differ, and users read")
    print("       both as 'the number' unless the title says which")


def a_filter_changes_which_rows():
    """Slicer / filter: fewer rows, the same measure definition."""
    unfiltered = DF["revenue"].sum()
    filtered = DF[DF["region"] == "South"]["revenue"].sum()

    assert unfiltered == 12880.0
    assert filtered == 10360.0
    assert filtered < unfiltered
    assert len(DF[DF["region"] == "South"]) == 6 and len(DF) == 9

    # Two filters intersect.
    both = DF[(DF["region"] == "South") & (DF["category"] == "Grocery")]
    assert both["revenue"].sum() == 8680.0, both["revenue"].sum()
    assert len(both) == 4

    print(f"  no filter                  9 rows, {unfiltered:>9,.0f}")
    print(f"  region = South             {len(DF[DF.region == 'South'])} rows, {filtered:>9,.0f}")
    print(f"  + category = Grocery       {len(both)} rows, {both['revenue'].sum():>9,.0f}")
    print("       filters INTERSECT. Each one can only reduce the row set,")
    print("       which is why a dashboard with six slicers usually shows zero")


def a_parameter_changes_what_is_calculated():
    """The distinction that earns the marks: same rows, different numbers."""
    base_revenue = DF["revenue"].sum()
    base_rows = len(DF)

    scenarios = {}
    for pct in (0, 5, 10, -5):
        # Round to paise: 12880 * 1.10 is 14168.000000000002 in binary
        # floating point, and a currency measure should never show that.
        projected = round(base_revenue * (1 + pct / 100), 2)
        scenarios[pct] = (base_rows, projected)

    assert scenarios[0] == (9, 12880.0)
    assert scenarios[5] == (9, 13524.0), scenarios[5]
    assert scenarios[10] == (9, 14168.0), scenarios[10]
    assert scenarios[-5] == (9, 12236.0), scenarios[-5]
    assert all(rows == base_rows for rows, _ in scenarios.values()), \
        "the ROW COUNT never changes -- that is what makes it a parameter"

    print("  what-if parameter 'price change %':")
    print(f"    {'change':>8s} {'rows':>6s} {'projected revenue':>19s}")
    for pct, (rows, projected) in scenarios.items():
        print(f"    {pct:+7d}% {rows:>6d} {projected:>19,.0f}")
    print("       NINE ROWS in every scenario. A filter would have changed that")
    print("       number; a parameter changes only the calculation. This is the")
    print("       model component of a DSS (unit-1.md 1.6) inside a BI tool")


def drill_through_versus_drill_down():
    """Drill-through jumps to a filtered detail page."""
    # The dashboard shows revenue by category.
    summary = DF.groupby("category")["revenue"].sum()
    assert len(summary) == 3

    # Right-click Grocery -> drill through -> a page filtered to Grocery.
    detail = DF[DF["category"] == "Grocery"][
        ["date", "store", "product", "qty", "revenue"]]
    assert len(detail) == 5, len(detail)
    assert detail["revenue"].sum() == summary["Grocery"] == 9800.0

    print(f"  summary page: {len(summary)} categories")
    print(f"  drill through on 'Grocery' -> a detail page of {len(detail)} rows")
    for _, r in detail.iterrows():
        print(f"      {r['date']}  {r['store']:11s} {r['product']:14s} "
              f"{int(r['qty']):>3d}  {r['revenue']:>8,.0f}")
    print(f"    detail sums to {detail['revenue'].sum():,.0f}, matching the summary")
    print("       drill-through is the right answer to 'users want the rows'.")
    print("       Keep the dashboard clean; put the table on another page")


def the_four_features():
    features = [
        ("Filter",     "which rows are shown", "pane, may be hidden"),
        ("Slicer",     "which rows are shown", "ON CANVAS, visible and clickable"),
        ("Parameter",  "WHAT IS CALCULATED",   "on canvas, feeds a measure"),
        ("Drilldown",  "the level of detail",  "in place, along a hierarchy"),
        ("Drill-through", "the PAGE",          "jumps, carrying the filter"),
    ]
    changes_rows = [f for f in features if f[1] == "which rows are shown"]
    assert len(changes_rows) == 2
    assert {f[0] for f in changes_rows} == {"Filter", "Slicer"}

    print("  the interactive features:")
    print(f"    {'feature':14s} {'changes':22s} where")
    for name, changes, where in features:
        print(f"    {name:14s} {changes:22s} {where}")
    print("       a SLICER IS A FILTER THE USER CAN SEE. The real distinction")
    print("       in this table is the third row: only a parameter changes the")
    print("       calculation rather than the row set")


def main():
    print("Experiment 15 -- Drill-downs, filters, slicers and parameters")
    drilldown_walks_a_hierarchy()
    drill_down_one_item_versus_expand_all()
    a_filter_changes_which_rows()
    a_parameter_changes_what_is_calculated()
    drill_through_versus_drill_down()
    the_four_features()


if __name__ == "__main__":
    main()
