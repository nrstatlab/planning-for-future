"""Experiment 14 — Joins and blending in Tableau.

The fan trap, measured. unit-3.md §3.6 and unit-4.md quote these figures:
revenue 12,880 -> 25,760 and target 20,800 -> 66,700. Both are produced here.

The fan trap matters more than any other single item in this course because it
is SILENT. No error, no warning, no null -- the totals simply become wrong, and
they stay wrong until somebody notices the revenue does not match finance.
"""
import pandas as pd

from fixtures import star

SALES = star()

# One row per store per quarter: two rows for every store.
TARGETS = pd.DataFrame([
    ("T1", "Q1", 5000.0), ("T1", "Q2", 5500.0),
    ("T2", "Q1", 3000.0), ("T2", "Q2", 3200.0),
    ("T3", "Q1", 2000.0), ("T3", "Q2", 2100.0),
], columns=["store_key", "quarter", "target"])


def the_correct_totals():
    """Establish the truth before breaking it."""
    revenue = SALES["revenue"].sum()
    target = TARGETS["target"].sum()

    assert len(SALES) == 9 and len(TARGETS) == 6
    assert revenue == 12880.0
    assert target == 20800.0

    rows_per_store = SALES["store_key"].value_counts().sort_index().to_dict()
    assert rows_per_store == {"T1": 4, "T2": 2, "T3": 3}, rows_per_store

    print(f"  sales   : {len(SALES)} rows, revenue {revenue:>10,.0f}")
    print(f"  targets : {len(TARGETS)} rows, target  {target:>10,.0f}")
    print(f"  sales rows per store: {rows_per_store}  (this is what inflates the target)")
    return revenue, target


def the_fan_trap(revenue, target):
    """Join on store alone. Both sides inflate, by different factors."""
    bad = SALES.merge(TARGETS, on="store_key", how="left",
                      suffixes=("", "_t"))

    assert len(bad) == 18, len(bad)
    bad_revenue = bad["revenue"].sum()
    bad_target = bad["target"].sum()

    assert bad_revenue == 25760.0, bad_revenue
    assert bad_target == 66700.0, bad_target
    assert bad_revenue == revenue * 2, "each sales row met 2 target rows"

    # The target inflation is uneven, because stores have different row counts.
    # T1: (5000+5500)*4 = 42000, T2: (3000+3200)*2 = 12400, T3: (2000+2100)*3 = 12300
    per_store = bad.groupby("store_key")["target"].sum().to_dict()
    assert per_store == {"T1": 42000.0, "T2": 12400.0, "T3": 12300.0}, per_store
    assert sum(per_store.values()) == 66700.0

    print(f"  join on store_key ALONE -> {len(bad)} rows (9 x 2)")
    print(f"    revenue {revenue:>10,.0f} -> {bad_revenue:>10,.0f}   "
          f"x{bad_revenue / revenue:.1f}  (uniform: 2 targets per store)")
    print(f"    target  {target:>10,.0f} -> {bad_target:>10,.0f}   "
          f"x{bad_target / target:.2f}  (UNEVEN)")
    print("    target inflation per store:")
    for store, n in (("T1", 4), ("T2", 2), ("T3", 3)):
        base = TARGETS[TARGETS.store_key == store]["target"].sum()
        print(f"      {store}: {base:>7,.0f} x {n} sales rows = {per_store[store]:>8,.0f}")
    print("       NO ERROR WAS RAISED. Both numbers are simply wrong now")
    return bad


def fix_one_join_on_the_full_grain():
    """Join on every column that defines the match: store AND quarter."""
    good = SALES.merge(TARGETS, on=["store_key", "quarter"], how="left")

    assert len(good) == 9, len(good)
    assert good["revenue"].sum() == 12880.0
    assert good["target"].notna().all(), "every sales row found its target"

    # The target must be de-duplicated before summing -- it repeats per row.
    deduped = good.drop_duplicates(["store_key", "quarter"])["target"].sum()
    assert deduped == 20800.0, deduped
    # Still inflated: T1Q1's 5000 meets 3 sales rows, T3Q2's 2100 meets 2.
    # 5000*3 + 5500 + 3000 + 3200 + 2000 + 2100*2 = 32,900.
    assert good["target"].sum() == 32900.0, good["target"].sum()

    print(f"  join on store_key AND quarter -> {len(good)} rows")
    print(f"    revenue                     = {good['revenue'].sum():>10,.0f}  CORRECT")
    print(f"    target, summed naively      = {good['target'].sum():>10,.0f}  still wrong")
    print(f"    target, de-duplicated first = {deduped:>10,.0f}  CORRECT")
    print("       fixing the grain fixed REVENUE but not the target, because a")
    print("       target row still repeats once per sales row at that grain.")
    print("       A measure from the 'one' side always needs de-duplication")


def fix_two_blend():
    """Blending: aggregate FIRST, then match. Nothing can duplicate."""
    # Primary source, aggregated to the linking field.
    sales_agg = SALES.groupby("store_key", as_index=False)["revenue"].sum()
    # Secondary source, aggregated to the SAME field.
    target_agg = TARGETS.groupby("store_key", as_index=False)["target"].sum()

    blended = sales_agg.merge(target_agg, on="store_key", how="left")

    assert len(blended) == 3, "one row per store -- the linking field's grain"
    assert blended["revenue"].sum() == 12880.0
    assert blended["target"].sum() == 20800.0

    blended["attainment"] = blended["revenue"] / blended["target"]
    expected = {"T1": 6160.0 / 10500, "T2": 4200.0 / 6200, "T3": 2520.0 / 4100}
    for _, r in blended.iterrows():
        assert abs(r["attainment"] - expected[r["store_key"]]) < 1e-12

    print(f"  blend (aggregate, THEN match) -> {len(blended)} rows")
    print(f"    revenue {blended['revenue'].sum():>10,.0f}   "
          f"target {blended['target'].sum():>10,.0f}   BOTH CORRECT")
    print("    store   revenue    target  attainment")
    for _, r in blended.iterrows():
        print(f"      {r['store_key']}  {r['revenue']:>8,.0f}  {r['target']:>8,.0f}"
              f"     {r['attainment'] * 100:6.1f}%")
    print("       blending is a LEFT JOIN PERFORMED AFTER AGGREGATION. That one")
    print("       sentence explains both why it cannot duplicate and why it")
    print("       cannot give you row-level detail from the secondary source")


def fix_three_lod():
    """{FIXED [Store] : SUM([Target])} de-duplicates the target side."""
    bad = SALES.merge(TARGETS, on="store_key", how="left", suffixes=("", "_t"))
    assert len(bad) == 18

    # The LOD: compute the target ONCE per store, independent of the row count.
    fixed_target = TARGETS.groupby("store_key")["target"].sum()
    bad["lod_target"] = bad["store_key"].map(fixed_target)

    per_store = bad.groupby("store_key")["lod_target"].first().to_dict()
    assert per_store == {"T1": 10500.0, "T2": 6200.0, "T3": 4100.0}, per_store
    assert sum(per_store.values()) == 20800.0

    print("  {FIXED [Store] : SUM([Target])} on the 18-row join:")
    for store in ("T1", "T2", "T3"):
        print(f"    {store}: {per_store[store]:>8,.0f}  (constant on all "
              f"{(bad.store_key == store).sum()} rows)")
    print(f"    sum of the per-store values = {sum(per_store.values()):>8,.0f}  CORRECT")
    print("       the LOD recovers the right target even from the broken join.")
    print("       Revenue is still doubled though -- an LOD patches a measure,")
    print("       it does not repair the model. Prefer fix one or fix two")


def join_types():
    """Inner, left, right and full outer, on data with a deliberate orphan."""
    stores = pd.DataFrame([("T1", "Vijayawada"), ("T2", "Guntur"),
                           ("T3", "Hyderabad"), ("T4", "Vizag")],
                          columns=["store_key", "store"])
    sales_by_store = SALES.groupby("store_key", as_index=False)["revenue"].sum()
    sales_by_store = pd.concat([sales_by_store, pd.DataFrame(
        [{"store_key": "T9", "revenue": 500.0}])], ignore_index=True)

    counts = {}
    for how in ("inner", "left", "right", "outer"):
        counts[how] = len(stores.merge(sales_by_store, on="store_key", how=how))

    assert counts == {"inner": 3, "left": 4, "right": 4, "outer": 5}, counts

    print("  4 stores (T1-T4), sales for T1-T3 and an orphan T9:")
    for how, label in (("inner", "INNER"), ("left", "LEFT"),
                       ("right", "RIGHT"), ("outer", "FULL OUTER")):
        print(f"    {label:11s} -> {counts[how]} rows")
    print("       T4 has no sales and T9 has no store. INNER loses both;")
    print("       FULL OUTER keeps both and is how you FIND them.")
    print("       'Which stores sold nothing?' = LEFT join, then filter to null")


def main():
    print("Experiment 14 -- Joins, blending and the fan trap")
    revenue, target = the_correct_totals()
    the_fan_trap(revenue, target)
    fix_one_join_on_the_full_grain()
    fix_two_blend()
    fix_three_lod()
    join_types()


if __name__ == "__main__":
    main()
