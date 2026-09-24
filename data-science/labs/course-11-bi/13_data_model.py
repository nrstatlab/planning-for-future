"""Experiment 13 — Designing data models in Power BI (star and snowflake).

unit-4.md §4.3 claims a star costs 92 cells where one flat table costs 144, and
that the ratio converges on 4x as the fact table grows. Both are computed here.

The storage number is the LEAST important of the four arguments against a flat
table, and the script asserts the other three too -- particularly the decisive
one: a flat table CANNOT REPORT WHAT DID NOT HAPPEN.
"""
import pandas as pd

from fixtures import (DIM_DATE, DIM_PRODUCT, DIM_STORE, DIM_SUPPLIER,
                      FACT_SALES, snowflake, star)

FLAT_COLS = ["date_key", "store_key", "product_key", "qty",
             "product", "category", "supplier_key", "unit_cost", "list_price",
             "store", "region", "opened",
             "date", "year", "month", "quarter"]


def the_shape_of_a_star():
    """One fact, three dimensions, each one join away."""
    assert FACT_SALES.shape == (9, 4)
    assert DIM_PRODUCT.shape == (4, 6)
    assert DIM_STORE.shape == (3, 4)
    assert DIM_DATE.shape == (4, 5)

    # Every fact key resolves -- referential integrity, which nothing enforces.
    assert set(FACT_SALES["product_key"]) <= set(DIM_PRODUCT["product_key"])
    assert set(FACT_SALES["store_key"]) <= set(DIM_STORE["store_key"])
    assert set(FACT_SALES["date_key"]) <= set(DIM_DATE["date_key"])

    # The "one" side of every 1:* relationship must be unique.
    for name, dim, key in (("dim_product", DIM_PRODUCT, "product_key"),
                           ("dim_store", DIM_STORE, "store_key"),
                           ("dim_date", DIM_DATE, "date_key")):
        assert dim[key].is_unique, f"{name}.{key} must be unique for 1:*"

    print("  table          rows  cols   role")
    for name, d, role in (("fact_sales", FACT_SALES, "FACT   grain: product x store x day"),
                          ("dim_product", DIM_PRODUCT, "dimension"),
                          ("dim_store", DIM_STORE, "dimension"),
                          ("dim_date", DIM_DATE, "dimension")):
        print(f"    {name:12s} {d.shape[0]:4d}  {d.shape[1]:4d}   {role}")
    print("       every dimension key is unique, so every relationship is 1:*.")
    print("       Power BI REFUSES a 1:* whose 'one' side repeats -- and that")
    print("       refusal usually means the grain is wrong, not the tool")


def the_snowflake_edge():
    """dim_product -> dim_supplier is what makes this a snowflake."""
    assert "supplier_key" in DIM_PRODUCT.columns
    assert set(DIM_PRODUCT["supplier_key"]) <= set(DIM_SUPPLIER["supplier_key"])
    assert DIM_SUPPLIER["supplier_key"].is_unique

    st, sn = star(), snowflake()
    assert st.shape == (9, 19), st.shape
    assert sn.shape == (9, 21), sn.shape
    assert sn.shape[1] - st.shape[1] == 2, "supplier name and city"

    # Star: fact -> product is ONE hop. Snowflake: fact -> product -> supplier.
    hops_star = 1
    hops_snowflake = 2
    assert hops_snowflake > hops_star

    print(f"  star flattened      : {st.shape[0]} x {st.shape[1]}")
    print(f"  snowflake flattened : {sn.shape[0]} x {sn.shape[1]}")
    print(f"  reaching a supplier attribute: {hops_star} hop in a star, "
          f"{hops_snowflake} in a snowflake")
    print("       dim_supplier is kept separate because supplier attributes are")
    print("       SHARED across products and change independently. That is the")
    print("       one condition under which a snowflake earns its keep")


def storage_star_versus_flat():
    """unit-4.md's 92 vs 144, and the 4x convergence."""
    star_cells = (FACT_SALES.size + DIM_PRODUCT.size
                  + DIM_STORE.size + DIM_DATE.size)
    flat_cells = star()[FLAT_COLS].size

    assert FACT_SALES.size == 36 and DIM_PRODUCT.size == 24
    assert DIM_STORE.size == 12 and DIM_DATE.size == 20
    assert star_cells == 92, star_cells
    assert flat_cells == 144, flat_cells
    assert len(FLAT_COLS) == 16

    dim_cells = DIM_PRODUCT.size + DIM_STORE.size + DIM_DATE.size
    assert dim_cells == 56

    projections = []
    for n in (9, 1_000, 1_000_000):
        s = n * 4 + dim_cells          # dimensions do NOT grow
        f = n * len(FLAT_COLS)
        projections.append((n, s, f, f / s))

    assert projections[0][1] == 92 and projections[0][2] == 144
    assert round(projections[1][3], 2) == 3.94, projections[1][3]
    assert round(projections[2][3], 2) == 4.00, projections[2][3]

    print(f"  star  = fact {FACT_SALES.size} + dims {dim_cells} = {star_cells} cells")
    print(f"  flat  = {len(star())} rows x {len(FLAT_COLS)} cols  = {flat_cells} cells")
    print(f"  {'fact rows':>12s} {'star':>14s} {'flat':>14s}  ratio")
    for n, s, f, ratio in projections:
        print(f"  {n:>12,} {s:>14,} {f:>14,}  {ratio:.2f}x")
    print("       the ratio converges on 16/4 = 4x, because the dimensions stop")
    print("       mattering as the fact table grows. Storage is the WEAKEST of")
    print("       the four arguments, though -- the next function has the best one")


def a_flat_table_cannot_report_what_did_not_happen():
    """The decisive argument, and the one that convinces people."""
    st = star()

    # Which products sold nothing? From a flat table you cannot ask.
    sold = set(st["product_key"])
    all_products = set(DIM_PRODUCT["product_key"])
    unsold = all_products - sold
    assert unsold == set(), "in the sample every product sold at least once"

    # Remove P4's sales, as a slow month would.
    reduced = st[st["product_key"] != "P4"]
    sold_now = set(reduced["product_key"])
    unsold_now = all_products - sold_now
    assert unsold_now == {"P4"}, unsold_now

    # FROM THE FLAT TABLE: P4 simply is not there. It cannot be counted.
    assert "P4" not in reduced["product_key"].values
    assert len(reduced["product"].unique()) == 3

    # FROM THE STAR: a LEFT join from the dimension shows it, as a blank.
    report = DIM_PRODUCT[["product_key", "product"]].merge(
        reduced.groupby("product_key", as_index=False)["qty"].sum(),
        on="product_key", how="left")
    assert len(report) == 4, "all four products appear"
    assert report.loc[report["product_key"] == "P4", "qty"].isna().all()
    assert int(report["qty"].sum()) == int(reduced["qty"].sum()) == 52

    print("  P4 sold nothing this period.")
    print(f"    flat table  -> {len(reduced['product'].unique())} products visible. "
          f"P4 is INVISIBLE")
    print(f"    star model  -> {len(report)} products, P4 shown with a blank:")
    for _, r in report.iterrows():
        qty = "(blank)" if pd.isna(r["qty"]) else f"{int(r['qty'])}"
        print(f"      {r['product_key']}  {r['product']:14s} {qty:>7s}")
    print("       'which products sold nothing?' is unanswerable from a flat")
    print("       table and trivial from a star. THIS is the argument to give")


def redundancy_invites_inconsistency():
    """The second argument: one misspelling creates a second store."""
    st = star()
    assert st["store"].nunique() == 3

    typo = st.copy()
    typo.loc[typo.index[0], "store"] = "Vijaywada"      # one character dropped
    assert typo["store"].nunique() == 4, "a fourth store now exists"

    # In a star the name is stored ONCE, so the same typo is impossible there.
    assert len(DIM_STORE) == 3
    assert DIM_STORE["store"].nunique() == 3
    repeats = st["store"].value_counts().to_dict()
    assert repeats == {"Vijayawada": 4, "Hyderabad": 3, "Guntur": 2}, repeats

    print(f"  'Vijayawada' is stored {repeats['Vijayawada']} times in a flat table")
    print(f"  mistype ONE of them -> {typo['store'].nunique()} stores in every chart")
    print(f"  in the star it is stored {int((DIM_STORE['store'] == 'Vijayawada').sum())} "
          f"time, so the typo cannot happen")
    print("       renaming a category in a flat table rewrites a million rows;")
    print("       in a star it is one cell")


def measures_by_additivity():
    """unit-4.md §4.2: which measures may be summed over which dimensions."""
    st = star()

    # Additive: qty and revenue sum over every dimension and agree.
    by_region = st.groupby("region")["revenue"].sum().sum()
    by_category = st.groupby("category")["revenue"].sum().sum()
    by_quarter = st.groupby("quarter")["revenue"].sum().sum()
    assert by_region == by_category == by_quarter == 12880.0, \
        "an ADDITIVE measure gives the same total however you slice it"

    # Non-additive: margin % does not, and the gap is the proof.
    margin_overall = st["profit"].sum() / st["revenue"].sum() * 100
    margin_summed = (st.groupby("region")
                       .apply(lambda g: g["profit"].sum() / g["revenue"].sum() * 100,
                              include_groups=False).sum())
    assert round(margin_overall, 4) == 27.3680
    assert round(margin_summed, 4) != round(margin_overall, 4)

    # Semi-additive: a stock balance summed over time is meaningless.
    stock = pd.DataFrame({"day": ["Mon", "Tue", "Wed"], "on_hand": [50, 48, 55]})
    assert stock["on_hand"].sum() == 153, "153 units never existed"
    assert stock["on_hand"].iloc[-1] == 55, "the closing balance is the answer"

    print(f"  ADDITIVE      revenue by region / category / quarter all total "
          f"{by_region:,.0f}")
    print(f"  NON-ADDITIVE  margin overall {margin_overall:.4f}%, "
          f"but summing the two regional margins gives {margin_summed:.4f}%")
    print(f"  SEMI-ADDITIVE stock 50, 48, 55 -> SUM = {stock['on_hand'].sum()} "
          f"units that never existed; the answer is the closing "
          f"{stock['on_hand'].iloc[-1]}")
    print("       a semi-additive measure needs its own SNAPSHOT fact table.")
    print("       Two facts sharing dimensions = a FACT CONSTELLATION")


def main():
    print("Experiment 13 -- Star and snowflake data models")
    the_shape_of_a_star()
    the_snowflake_edge()
    storage_star_versus_flat()
    a_flat_table_cannot_report_what_did_not_happen()
    redundancy_invites_inconsistency()
    measures_by_additivity()


if __name__ == "__main__":
    main()
