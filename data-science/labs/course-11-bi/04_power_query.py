"""Experiment 4 — Data cleaning and transformation with Power Query.

Power Query is a recorded, ordered list of steps replayed at every refresh.
That ordering is not decoration -- the SAME steps in a different order give a
different answer, and this script proves it.

Each function is one ribbon button, with the pandas call that does the same
thing, so the pair is learnable together.
"""
import pandas as pd

# A deliberately dirty extract: the shapes real spreadsheets arrive in.
DIRTY = pd.DataFrame({
    "store":  ["  Vijayawada ", "GUNTUR", "Vijayawada", "Hyderabad",
               "Vijayawada", "guntur", None],
    "region": ["South", None,   None,     "North",  None,  None,  "North"],
    "sales":  ["2,800", "1680", "700",    "800",    "700", "1680", "n/a"],
    "date":   ["2026-01-15", "2026-01-15", "2026-01-15", "2026-02-10",
               "2026-01-15", "2026-01-15", "2026-02-10"],
})


def trim_and_clean():
    """Transform -> Format -> Trim, and Clean (removes control characters)."""
    df = DIRTY.copy()
    assert df["store"][0] == "  Vijayawada ", "leading and trailing spaces"

    df["store"] = df["store"].str.strip()
    assert df["store"][0] == "Vijayawada"

    # "Vijayawada" and "  Vijayawada " are DIFFERENT values until trimmed --
    # which is why an untrimmed column produces two slicer entries that look
    # identical on screen.
    raw_distinct = DIRTY["store"].nunique(dropna=True)
    trimmed_distinct = df["store"].nunique(dropna=True)
    assert raw_distinct == 5 and trimmed_distinct == 4, (raw_distinct, trimmed_distinct)

    print(f"  Trim: {raw_distinct} distinct stores -> {trimmed_distinct}")
    print("       an untrimmed column gives two slicer entries that look the same")


def case_folding_is_not_trim():
    """'GUNTUR', 'Guntur' and 'guntur' are three stores until you fix case."""
    df = DIRTY.copy()
    df["store"] = df["store"].str.strip()
    assert df["store"].nunique(dropna=True) == 4

    df["store"] = df["store"].str.title()
    assert df["store"].nunique(dropna=True) == 3, sorted(df["store"].dropna().unique())
    assert sorted(df["store"].dropna().unique()) == ["Guntur", "Hyderabad", "Vijayawada"]

    print("  Transform -> Format -> Capitalize Each Word: 4 -> 3 distinct stores")
    print("       GUNTUR / guntur were separate rows in every chart")


def fill_down():
    """Transform -> Fill -> Down. The classic merged-cell repair."""
    df = DIRTY.copy()
    assert df["region"].isna().sum() == 4

    df["region"] = df["region"].ffill()
    assert df["region"].isna().sum() == 0
    assert list(df["region"]) == ["South"] * 3 + ["North"] * 4, list(df["region"])

    print("  Fill Down: 4 nulls -> 0")
    print("       merged cells in Excel export as a value then blanks. Fill Down")
    print("       is the repair -- but ONLY if the rows are still in source order")


def replace_values_and_types():
    """Replace Values, then Change Type. Order matters -- see below."""
    df = DIRTY.copy()

    # "n/a" and thousands separators both defeat a numeric conversion.
    cleaned = (df["sales"].str.replace(",", "", regex=False)
                          .replace("n/a", None))
    numeric = pd.to_numeric(cleaned, errors="raise")
    assert numeric.isna().sum() == 1, "n/a became null, not zero"
    assert numeric.sum() == 8360.0, numeric.sum()

    # The alternative -- replacing n/a with 0 -- changes every average.
    as_zero = pd.to_numeric(cleaned.fillna(0))
    assert as_zero.sum() == 8360.0, "the SUM is the same"
    assert round(numeric.mean(), 4) == 1393.3333, round(numeric.mean(), 4)
    assert round(as_zero.mean(), 4) == 1194.2857, round(as_zero.mean(), 4)

    print(f"  Replace ',' then to-number: sum {numeric.sum():.0f}, "
          f"mean {numeric.mean():.4f} (n/a -> null, excluded)")
    print(f"  n/a replaced with 0 instead: sum {as_zero.sum():.0f}, "
          f"mean {as_zero.mean():.4f}")
    print("       the SUM is identical and the MEAN is not. Null excludes the")
    print("       row; zero counts it as a real zero. State which you chose")


def remove_duplicates_depends_on_the_columns():
    """Remove Duplicates removes rows identical in the SELECTED columns."""
    df = DIRTY.copy()
    df["store"] = df["store"].str.strip().str.title()

    all_cols = df.drop_duplicates()
    on_store = df.drop_duplicates(subset=["store"])
    on_store_date = df.drop_duplicates(subset=["store", "date"])

    assert len(df) == 7
    # Rows 4 and 5 are exact copies of rows 2 and 1, so two go.
    assert len(all_cols) == 5, len(all_cols)
    assert len(on_store) == 4, len(on_store)
    assert len(on_store_date) == 4, len(on_store_date)

    print(f"  Remove Duplicates on: all columns -> {len(all_cols)} rows")
    print(f"                        [store]     -> {len(on_store)} rows")
    print(f"                        [store,date]-> {len(on_store_date)} rows")
    print("       select the wrong columns and you delete real data. It keeps")
    print("       the FIRST occurrence, so sort before de-duplicating")


def step_order_changes_the_answer():
    """The demonstration that justifies the whole Applied Steps pane."""
    df = DIRTY.copy()
    df["sales_n"] = pd.to_numeric(
        df["sales"].str.replace(",", "", regex=False).replace("n/a", None))

    # Order A: de-duplicate FIRST, then trim/case-fold.
    a = df.drop_duplicates(subset=["store", "date"]).copy()
    a["store"] = a["store"].str.strip().str.title()
    a_total = a["sales_n"].sum()

    # Order B: trim/case-fold FIRST, then de-duplicate.
    b = df.copy()
    b["store"] = b["store"].str.strip().str.title()
    b = b.drop_duplicates(subset=["store", "date"])
    b_total = b["sales_n"].sum()

    assert len(a) == 6 and len(b) == 4, (len(a), len(b))
    # A keeps 2800+1680+700+800+1680; B keeps 2800+1680+800.
    assert a_total == 7660.0 and b_total == 5280.0, (a_total, b_total)
    assert a_total - b_total == 2380.0

    print("  SAME two steps, two orders:")
    print(f"    de-duplicate then clean -> {len(a)} rows, total {a_total:.0f}")
    print(f"    clean then de-duplicate -> {len(b)} rows, total {b_total:.0f}")
    print(f"    the two orders differ by {a_total - b_total:.0f}")
    print("       '  Vijayawada ' and 'Vijayawada' are not duplicates until")
    print("       they have been trimmed, so de-duplicating first MISSES them.")
    print("       CLEAN BEFORE YOU DE-DUPLICATE -- and this is why Applied")
    print("       Steps is an ordered list and not a set")


def unpivot_is_the_examinable_one():
    """Transform -> Unpivot Columns. pandas calls it melt; Tableau calls it Pivot."""
    wide = pd.DataFrame({"store": ["T1", "T2"],
                         "Jan": [5000, 3000], "Feb": [5200, 3100]})
    long = wide.melt(id_vars="store", var_name="month", value_name="sales")

    assert wide.shape == (2, 3)
    assert long.shape == (4, 3), long.shape
    assert list(long.columns) == ["store", "month", "sales"]
    assert long["sales"].sum() == wide[["Jan", "Feb"]].to_numpy().sum() == 16300

    # The reason: a March column breaks the wide chart and not the long one.
    wide_mar = wide.assign(Mar=[5400, 3200])
    long_mar = wide_mar.melt(id_vars="store", var_name="month", value_name="sales")
    assert long_mar.shape == (6, 3), "same three columns, more rows"
    assert list(long_mar.columns) == list(long.columns), \
        "the SCHEMA did not change -- that is the whole point"

    print(f"  Unpivot: {wide.shape} wide -> {long.shape} long, total {long['sales'].sum()}")
    print(f"  add a March column: {wide_mar.shape} wide -> {long_mar.shape} long")
    print("       the long table's COLUMNS did not change, so no chart broke.")
    print("       Power Query: Unpivot. Tableau: Pivot. pandas: melt")


def group_by_and_merge():
    """Group By, and Merge Queries -- the last two ribbon buttons that matter."""
    df = DIRTY.copy()
    df["store"] = df["store"].str.strip().str.title()
    df["sales_n"] = pd.to_numeric(
        df["sales"].str.replace(",", "", regex=False).replace("n/a", None))
    df = df.dropna(subset=["store"])

    grouped = (df.groupby("store", as_index=False)
                 .agg(total=("sales_n", "sum"), lines=("sales_n", "size")))
    assert len(grouped) == 3
    assert grouped.set_index("store")["total"].to_dict() == \
        {"Guntur": 3360.0, "Hyderabad": 800.0, "Vijayawada": 4200.0}

    lookup = pd.DataFrame({"store": ["Vijayawada", "Guntur", "Hyderabad"],
                           "manager": ["Asha", "Ravi", "Meena"]})
    merged = grouped.merge(lookup, on="store", how="left")
    assert merged["manager"].isna().sum() == 0
    assert len(merged) == len(grouped), "a LEFT join to a unique key cannot add rows"

    print("  Group By store:")
    for _, r in grouped.iterrows():
        print(f"    {r['store']:12s} total {r['total']:7.0f}  ({r['lines']} lines)")
    print("  Merge Queries (left join to a unique key) added manager, no row growth")
    print("       if a merge ADDS rows, the right-hand key is not unique --")
    print("       that is the fan trap, and experiment 14 measures it")


def main():
    print("Experiment 4 -- Power Query cleaning and transformation")
    trim_and_clean()
    case_folding_is_not_trim()
    fill_down()
    replace_values_and_types()
    remove_duplicates_depends_on_the_columns()
    step_order_changes_the_answer()
    unpivot_is_the_examinable_one()
    group_by_and_merge()


if __name__ == "__main__":
    main()
