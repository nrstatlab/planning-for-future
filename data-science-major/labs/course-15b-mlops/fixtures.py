"""Shared data for the Course 15 B practicals.

THE DATASET IS GENERATED FROM KNOWN COEFFICIENTS, and that is the whole
design of this course's labs. MLOps is about detecting when a model has gone
wrong, and you cannot verify a drift detector on data whose drift you do not
know. Here the drift is INJECTED at a known magnitude on a known feature at a
known time, so a detector can be scored rather than merely run.

The business scenario is a loan-approval model, chosen because it makes the
Unit 5 governance material concrete: it has a protected attribute, a real
cost asymmetry between the two error types, and a plausible reason for the
input distribution to shift.

CROSS-COURSE: the South-region revenue total of Rs 10,360 that Courses 11,
12 B and 13 B all compute appears here too, in the ETL experiment, so the
warehouse this course loads can be checked against the three that came
before it.
"""
import json
import math
import pathlib
import sqlite3

import numpy as np
import pandas as pd

SEED = 42

# ---------------------------------------------------------------- the model
#
# The true coefficients. Every experiment that fits a model can be checked
# against these rather than against its own output.

TRUE_COEF = {
    "income": 0.9,
    "loan_amount": -0.7,
    "credit_years": 0.5,
    "age": 0.1,
}
TRUE_INTERCEPT = -0.2

FEATURES = list(TRUE_COEF)
PROTECTED = "region"          # not a model input; used for the fairness audit
REGIONS = ["North", "South", "East", "West"]


def applicants(n=4000, seed=SEED, drift=0.0, drift_feature="income"):
    """Loan applications, with an OPTIONAL known shift on one feature.

    `drift` is measured in standard deviations of that feature. drift=0.0 is
    the reference distribution the model was trained on; drift=1.5 is a large,
    unambiguous shift. Because the magnitude is known, a detector's output can
    be scored against it.
    """
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "income": rng.normal(0, 1, n),
        "loan_amount": rng.normal(0, 1, n),
        "credit_years": rng.normal(0, 1, n),
        "age": rng.normal(0, 1, n),
        "region": rng.choice(REGIONS, n),
    })
    if drift:
        df[drift_feature] = df[drift_feature] + drift

    z = TRUE_INTERCEPT + sum(TRUE_COEF[f] * df[f] for f in FEATURES)
    p = 1 / (1 + np.exp(-z))
    df["approved"] = (rng.random(n) < p).astype(int)
    return df


def train_reference(n=4000, seed=SEED):
    """The training set the production model was fitted on."""
    return applicants(n=n, seed=seed, drift=0.0)


def production_batches(n_per_batch=500, n_batches=10, drift_starts=5,
                       max_drift=1.5, seed=SEED + 1):
    """Ten daily batches. Batches 0-4 are clean; drift ramps in from batch 5.

    Returns (list_of_frames, list_of_true_drift_magnitudes) so a detector can
    be scored against the truth, batch by batch.
    """
    frames, truth = [], []
    for b in range(n_batches):
        if b < drift_starts:
            d = 0.0
        else:
            step = (b - drift_starts + 1) / (n_batches - drift_starts)
            d = max_drift * step
        frames.append(applicants(n=n_per_batch, seed=seed + b, drift=d))
        truth.append(d)
    return frames, truth


# ----------------------------------------------------------- the ETL source
#
# The same sales figures Courses 11, 12 B and 13 B use. South must total
# 10,360 -- four engines now agree on that number, and this makes five.

# These are the SAME rows Course 11's star schema holds, flattened to one
# line per sale. Reusing them is the point: this course's ETL job must
# reproduce the South total that Course 11 computes in DAX, Course 12 B in
# Hive and in Spark, and Course 13 B in its warehouse. Five engines, one
# number, and any of them drifting is caught by the others.
#
#   store T1 Vijayawada South | T2 Guntur South | T3 Hyderabad North
#   P1 Rice 5kg 280 | P2 Tea 500g 210 | P3 Shampoo 200ml 140 | P4 Notebook 40

SALES_ROWS = [
    # (order_id, region, product, units, unit_price)
    (1, "South", "Rice 5kg", 10, 280),
    (2, "South", "Shampoo 200ml", 5, 140),
    (3, "South", "Tea 500g", 8, 210),
    (4, "South", "Rice 5kg", 6, 280),
    (5, "North", "Notebook", 20, 40),
    (6, "South", "Tea 500g", 12, 210),
    (7, "North", "Rice 5kg", 4, 280),
    (8, "South", "Shampoo 200ml", 7, 140),
    (9, "North", "Notebook", 15, 40),
]


def write_sources(tmpdir):
    """Write the CSV and JSON an ETL job will read. Deliberately messy.

    The messiness is the experiment: a region spelled two ways, a price
    arriving with a currency prefix, a null, and a duplicate order id.
    An ETL job that does not handle these produces a wrong total silently --
    and because the right answer is known, the lab can prove it.
    """
    tmpdir = pathlib.Path(tmpdir)
    tmpdir.mkdir(parents=True, exist_ok=True)

    csv_path = tmpdir / "orders.csv"
    lines = ["order_id,region,product,units,unit_price"]
    for oid, region, product, units, price in SALES_ROWS[:6]:
        r = region.lower() if oid == 3 else region     # 'south', lowercase
        p = f"Rs {price}" if oid == 2 else str(price)  # a currency prefix
        lines.append(f"{oid},{r},{product},{units},{p}")
    lines.append("6,South,Tea 500g,12,210")            # a DUPLICATE of order 6
    lines.append("10,North,Notebook,,40")              # a NULL units field
    csv_path.write_text("\n".join(lines) + "\n")

    json_path = tmpdir / "orders.json"
    json_path.write_text(json.dumps([
        {"order_id": oid, "region": region, "product": product,
         "units": units, "unit_price": price}
        for oid, region, product, units, price in SALES_ROWS[6:]
    ], indent=2))

    return csv_path, json_path


SOUTH_TOTAL = 10360     # what Courses 11, 12 B and 13 B all compute


def warehouse(path):
    """An empty star-schema warehouse, ready for the ETL job to load."""
    con = sqlite3.connect(path)
    con.executescript("""
        DROP TABLE IF EXISTS fact_sales;
        DROP TABLE IF EXISTS dim_region;
        DROP TABLE IF EXISTS dim_product;

        CREATE TABLE dim_region (
            region_id INTEGER PRIMARY KEY,
            region    TEXT UNIQUE NOT NULL
        );
        CREATE TABLE dim_product (
            product_id INTEGER PRIMARY KEY,
            product    TEXT UNIQUE NOT NULL
        );
        CREATE TABLE fact_sales (
            order_id   INTEGER PRIMARY KEY,
            region_id  INTEGER NOT NULL REFERENCES dim_region(region_id),
            product_id INTEGER NOT NULL REFERENCES dim_product(product_id),
            units      INTEGER NOT NULL CHECK (units > 0),
            unit_price INTEGER NOT NULL CHECK (unit_price > 0),
            revenue    INTEGER NOT NULL
        );
    """)
    con.commit()
    return con
