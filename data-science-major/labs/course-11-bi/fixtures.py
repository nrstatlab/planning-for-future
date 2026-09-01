"""Shared sample data for the Course 11 practicals.

One definition, used by every script, so the labs cannot drift from each other
or from the worked examples in the notes. Deliberately tiny: every figure in
notes/sem-5/course-11-business-intelligence/ can be checked by hand against
these tables, which is the only way a student can tell whether they have
understood a measure or merely copied it.

The shape is a textbook STAR: one fact table, four dimensions.

    dim_product ──┐
    dim_store ────┼── fact_sales
    dim_date ─────┘
    dim_supplier ── dim_product      (this one edge makes it a SNOWFLAKE)
"""
import pandas as pd

# --- dimensions -------------------------------------------------------------

DIM_PRODUCT = pd.DataFrame([
    #  key      name          category      supplier  unit_cost list_price
    ("P1", "Rice 5kg",      "Grocery",   "S1", 220.0, 280.0),
    ("P2", "Tea 500g",      "Grocery",   "S1", 150.0, 210.0),
    ("P3", "Shampoo 200ml", "Personal",  "S2",  90.0, 140.0),
    ("P4", "Notebook",      "Stationery","S3",  25.0,  40.0),
], columns=["product_key", "product", "category", "supplier_key",
            "unit_cost", "list_price"])

DIM_STORE = pd.DataFrame([
    ("T1", "Vijayawada", "South", 2019),
    ("T2", "Guntur",     "South", 2021),
    ("T3", "Hyderabad",  "North", 2020),
], columns=["store_key", "store", "region", "opened"])

DIM_SUPPLIER = pd.DataFrame([
    ("S1", "Annapurna Foods",  "Vijayawada"),
    ("S2", "CleanCo",          "Chennai"),
    ("S3", "Paper Mills Ltd",  "Guntur"),
], columns=["supplier_key", "supplier", "supplier_city"])

DIM_DATE = pd.DataFrame([
    ("D1", "2026-01-15", 2026, 1, "Q1"),
    ("D2", "2026-02-10", 2026, 2, "Q1"),
    ("D3", "2026-04-05", 2026, 4, "Q2"),
    ("D4", "2026-05-20", 2026, 5, "Q2"),
], columns=["date_key", "date", "year", "month", "quarter"])

# --- the fact table ---------------------------------------------------------
# Grain: ONE ROW PER PRODUCT PER STORE PER DAY. Stating the grain is the first
# thing you do when designing a fact table, and the first thing an examiner
# asks. Every measure below is only meaningful because the grain is fixed.

FACT_SALES = pd.DataFrame([
    #  date store product qty
    ("D1", "T1", "P1",  10),
    ("D1", "T1", "P3",   5),
    ("D1", "T2", "P2",   8),
    ("D2", "T1", "P1",   6),
    ("D2", "T3", "P4",  20),
    ("D3", "T2", "P2",  12),
    ("D3", "T3", "P1",   4),
    ("D4", "T1", "P3",   7),
    ("D4", "T3", "P4",  15),
], columns=["date_key", "store_key", "product_key", "qty"])


def star():
    """The fact table joined to every dimension -- one flat analysis table.

    This is what a BI tool builds internally when you drag fields from several
    tables onto one visual. Doing it explicitly once makes the rest obvious.
    """
    df = (FACT_SALES
          .merge(DIM_PRODUCT, on="product_key", how="left")
          .merge(DIM_STORE, on="store_key", how="left")
          .merge(DIM_DATE, on="date_key", how="left"))
    df["revenue"] = df["qty"] * df["list_price"]
    df["cost"] = df["qty"] * df["unit_cost"]
    df["profit"] = df["revenue"] - df["cost"]
    return df


def snowflake():
    """The star, plus the supplier dimension hanging off product.

    Product -> Supplier is what makes this a snowflake rather than a star:
    a dimension normalized into a second level instead of being flattened.
    """
    return star().merge(DIM_SUPPLIER, on="supplier_key", how="left")
