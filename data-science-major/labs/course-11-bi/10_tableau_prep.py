"""Experiment 10 — Data cleaning, pivoting and filtering in Tableau.

Two things Tableau does differently from Power Query, and both are examinable:

  * Tableau's PIVOT is Power Query's UNPIVOT. Opposite names, same operation.
  * Filters apply in a fixed ORDER, and a Top-N filter computed before a
    dimension filter gives the top N overall rather than within the selection.

The second is demonstrated numerically, because it is the exam question and
because the wrong answer looks entirely plausible.
"""
import pandas as pd

from fixtures import star

DF = star()

# As a spreadsheet arrives: a column per quarter.
WIDE = pd.DataFrame([
    ("T1", "Vijayawada", "South", 3500, 2660),
    ("T2", "Guntur",     "South", 1680, 2520),
    ("T3", "Hyderabad",  "North", 1920,  600),
], columns=["store_key", "store", "region", "Q1", "Q2"])


def tableau_pivot_is_power_query_unpivot():
    long = WIDE.melt(id_vars=["store_key", "store", "region"],
                     var_name="quarter", value_name="revenue")

    assert WIDE.shape == (3, 5)
    assert long.shape == (6, 5), long.shape
    assert set(long["quarter"]) == {"Q1", "Q2"}
    assert long["revenue"].sum() == WIDE[["Q1", "Q2"]].to_numpy().sum() == 12880

    print(f"  wide {WIDE.shape} -> long {long.shape}, total {long['revenue'].sum():,}")
    print("    Tableau   : select the columns -> Pivot")
    print("    Power BI  : select the columns -> Unpivot Columns")
    print("    pandas    : melt")
    print("       three names, one operation. Say the right one per tool")
    return long


def filter_order_changes_the_answer(long):
    """Top-N before a dimension filter gives the top N OVERALL. The trap."""
    # WRONG: rank across everything, then filter to South.
    top2_overall = long.nlargest(2, "revenue")
    wrong = top2_overall[top2_overall["region"] == "South"]

    # RIGHT: filter to South first (a CONTEXT filter), then rank.
    south = long[long["region"] == "South"]
    right = south.nlargest(2, "revenue")

    assert list(top2_overall["revenue"]) == [3500, 2660], list(top2_overall["revenue"])
    assert len(wrong) == 2, "both happen to be South here"

    assert len(right) == 2
    assert list(right["revenue"]) == [3500, 2660], list(right["revenue"])

    # Make the divergence unmistakable by asking for the top 2 in NORTH.
    top2_north_wrong = top2_overall[top2_overall["region"] == "North"]
    top2_north_right = long[long["region"] == "North"].nlargest(2, "revenue")
    assert len(top2_north_wrong) == 0, "the overall top 2 contains no North row"
    assert len(top2_north_right) == 2, "North does have a top 2"
    assert list(top2_north_right["revenue"]) == [1920, 600]

    print("  'top 2 stores in North':")
    print(f"    rank first, then filter -> {len(top2_north_wrong)} rows  WRONG "
          f"(the overall top 2 is all South)")
    print(f"    filter first, then rank -> {len(top2_north_right)} rows  RIGHT "
          f"{list(top2_north_right['revenue'])}")
    print("       in Tableau, promote the region filter to a CONTEXT filter so")
    print("       it runs BEFORE the Top-N. That is what context filters are for")


def the_order_of_operations():
    """The list itself, asserted so it cannot be reordered by accident."""
    order = [
        "Extract filters",
        "Data source filters",
        "Context filters",
        "Dimension filters",
        "Measure filters",
        "Table calculation filters",
    ]
    assert len(order) == 6
    assert order.index("Context filters") < order.index("Dimension filters")
    assert order[-1] == "Table calculation filters"

    print("  Tableau filter order of operations:")
    for i, step in enumerate(order, 1):
        print(f"    {i}. {step}")
    print("       context BEFORE dimension is the pair that matters, and")
    print("       table calculation filters run LAST -- they hide rows without")
    print("       recomputing, which is why a running total keeps its old values")


def cleaning_in_tableau():
    """Aliases, splits and Data Interpreter -- the Data Source tab's tools."""
    messy = pd.DataFrame({
        "store_code": ["T1-Vijayawada", "T2-Guntur", "T3-Hyderabad"],
        "region_raw": ["S", "S", "N"],
    })

    # Split on a delimiter: Tableau's Custom Split.
    split = messy["store_code"].str.split("-", n=1, expand=True)
    split.columns = ["store_key", "store"]
    assert list(split["store_key"]) == ["T1", "T2", "T3"]
    assert list(split["store"]) == ["Vijayawada", "Guntur", "Hyderabad"]

    # Aliases change what is DISPLAYED, not the underlying value.
    alias = {"S": "South", "N": "North"}
    displayed = messy["region_raw"].map(alias)
    assert list(displayed) == ["South", "South", "North"]
    assert list(messy["region_raw"]) == ["S", "S", "N"], \
        "the stored value is UNCHANGED -- that is what an alias means"

    print(f"  Custom Split on '-': {list(split['store_key'])} + "
          f"{list(split['store'])}")
    print(f"  Alias S/N -> {list(displayed)}")
    print(f"    underlying values still {list(messy['region_raw'])}")
    print("       an alias is a display label. It does not change the data, so")
    print("       it does not fix a join key -- that needs a real calculation")


def main():
    print("Experiment 10 -- Tableau cleaning, pivoting and filtering")
    long = tableau_pivot_is_power_query_unpivot()
    filter_order_changes_the_answer(long)
    the_order_of_operations()
    cleaning_in_tableau()


if __name__ == "__main__":
    main()
