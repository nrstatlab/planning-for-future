"""Experiment 9 -- data analysis with Pig Latin scripts.

Pig is not installed. `09_analysis.pig` carries the real Pig Latin, marked NOT
EXECUTED. What runs here is the same dataflow, one operator at a time, so the
INTERMEDIATE relations in the notes are real -- and stepping through them is
exactly how you debug a Pig script anyway (that is what ILLUSTRATE does).

Pig's value over Hive is that it is a DATAFLOW language: you name every
intermediate relation, so a 12-step transformation reads top to bottom instead
of nesting twelve sub-queries.
"""
import fixtures as f

SALES = f.SALES_DF


def show(name, rel, cols, limit=4):
    print(f"\n    {name} -- {len(rel)} rows")
    head = rel[cols].head(limit)
    widths = [max(len(str(c)), int(rel[c].astype(str).str.len().max())) + 3
              for c in cols]
    print("      " + "".join(f"{c:>{w}}" for c, w in zip(cols, widths)))
    for _, r in head.iterrows():
        print("      " + "".join(
            f"{r[c]:>{w},.0f}" if isinstance(r[c], float) else f"{str(r[c]):>{w}}"
            for c, w in zip(cols, widths)))
    if len(rel) > limit:
        print(f"      ... {len(rel) - limit} more")


def main():
    print("  Experiment 9 -- the Pig Latin dataflow, one operator at a time")

    # A = LOAD
    A = SALES.copy()
    show("A = LOAD 'sales'", A, ["store", "product", "qty", "revenue"])

    # B = FILTER
    B = A[A["qty"] >= 6]
    show("B = FILTER A BY qty >= 6", B, ["store", "product", "qty", "revenue"])
    assert len(B) == 7, 'seven of nine orders are 6 units or more'

    # C = GROUP
    C = B.groupby("category")
    print(f"\n    C = GROUP B BY category -- {C.ngroups} groups")
    for name, grp in C:
        print(f"      ({name}, {{{len(grp)} tuples}})")
    print("""         GROUP in Pig produces a BAG per key, not an aggregate.
         The bag is the value, and FOREACH ... GENERATE is what turns
         it into numbers. Hive fuses the two; Pig keeps them apart,
         which is why Pig can do things to a group that SQL cannot
         express without a window function""")

    # D = FOREACH ... GENERATE
    D = (C.agg(units=("qty", "sum"), revenue=("revenue", "sum"),
               orders=("order_id", "count") if "order_id" in B else ("qty", "size"))
         .reset_index())
    print(f"\n    D = FOREACH C GENERATE group, SUM(B.qty), SUM(B.revenue)")
    print(f"      {'category':<12}{'units':>8}{'revenue':>12}{'orders':>8}")
    for _, r in D.iterrows():
        print(f"      {r['category']:<12}{r['units']:>8.0f}"
              f"{r['revenue']:>12,.0f}{r['orders']:>8.0f}")
    assert D["revenue"].sum() == B["revenue"].sum()

    # E = ORDER
    E = D.sort_values("revenue", ascending=False)
    print(f"\n    E = ORDER D BY revenue DESC")
    print(f"      top category: {E.iloc[0]['category']} "
          f"at {E.iloc[0]['revenue']:,.0f}")
    assert E.iloc[0]["category"] == "Grocery"

    # F = JOIN
    print("\n    F = JOIN A BY store_key, stores BY store_key")
    joined = A.groupby(["region", "store"], as_index=False)["revenue"].sum()
    print(f"      {'region':<8}{'store':<14}{'revenue':>12}")
    for _, r in joined.sort_values("revenue", ascending=False).iterrows():
        print(f"      {r['region']:<8}{r['store']:<14}{r['revenue']:>12,.0f}")
    assert joined["revenue"].sum() == f.total_revenue()

    # ---- what makes Pig Pig ---------------------------------------------
    print("\n    the operators, and their SQL equivalents:")
    print(f"      {'Pig Latin':<26}{'SQL'}")
    for pig, sql in (
            ("LOAD / STORE", "no equivalent -- SQL assumes a table exists"),
            ("FILTER", "WHERE"),
            ("FOREACH .. GENERATE", "SELECT"),
            ("GROUP", "GROUP BY, but the bag is kept"),
            ("JOIN", "JOIN"),
            ("ORDER", "ORDER BY"),
            ("DISTINCT", "DISTINCT"),
            ("FLATTEN", "UNNEST / LATERAL VIEW explode"),
            ("ILLUSTRATE", "no equivalent -- sample data through the plan")):
        print(f"      {pig:<26}{sql}")

    print("""
         two operators have no SQL equivalent, and they are the
         reason to reach for Pig: LOAD, which lets a script read a
         semi-structured file with no schema declared in advance,
         and ILLUSTRATE, which pushes a few representative rows
         through every step of the plan so you can see where a
         12-stage pipeline went wrong""")

    print("\n    lazy evaluation, which surprises everyone:")
    print("      nothing runs until STORE or DUMP.")
    print("      A = LOAD ...;   B = FILTER ...;   C = GROUP ...;")
    print("      -- no job has been submitted yet")
    print("      STORE C INTO 'out';  -- NOW Pig compiles and runs it")
    print("""         because Pig sees the whole dataflow before executing, it
         can merge the FILTER into the LOAD and fuse consecutive
         FOREACHes into one MapReduce job. Writing the steps
         separately costs nothing -- which is the entire argument
         against nesting sub-queries to avoid 'extra passes'""")


if __name__ == "__main__":
    main()
