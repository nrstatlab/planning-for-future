#!/usr/bin/env python3
"""Generate the practice datasets under data/, as CSV.

Every course in this programme teaches methods that need data to practise on,
and until now the only data was embedded in the lab scripts. These files put a
dataset in front of the student for each method -- descriptive statistics,
regression, every hypothesis test, Apriori, decision trees, k-Means, DBSCAN,
ARIMA, VAR, drift detection, MapReduce, OLAP, SQL joins, document modelling
and the rest.

TWO RULES, and they are the whole point:

  1. Every dataset is GENERATED FROM A KNOWN TRUTH. The regression file was
     built from a slope of 6.0; the AR(2) series from phi = (0.6, -0.3); the
     three clusters from centres the generator chose. So the student is not
     merely running a method -- they can SCORE their answer against the number
     that produced the data.

  2. Every truth is asserted by tools/check_datasets.py, which reads the CSVs
     back off disk and recovers it. A practice dataset whose right answer
     nobody has checked is worse than no dataset, because a wrong answer then
     looks like a lesson.

Seeded throughout, so the files regenerate byte-identically. Regenerating and
finding a diff means something changed that should not have.

Usage:  python3 tools/make_datasets.py
"""
import csv
import math
import pathlib
import random
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
# An output directory can be passed as argv[1]. check_datasets.py uses that to
# regenerate into a temporary directory and compare -- if it regenerated over
# data/ instead, it would REPAIR any corruption before its own checks could
# see it, and every one of those checks would be unable to fail.
DATA = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 \
    else ROOT / "data"

# Every dataset's planted truth, keyed by path. check_datasets.py recovers each
# one from the file; data/README.md is generated from this same table, so the
# documentation cannot drift from what was actually planted.
TRUTHS = {}


def write(relpath, header, rows, truth, methods, note):
    """Write one CSV and record what it was built from."""
    path = DATA / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    TRUTHS[relpath] = {"truth": truth, "methods": methods, "note": note,
                       "rows": len(rows), "columns": header}
    return path


def rnd(x, n=4):
    return round(float(x), n)


# ---------------------------------------------------------------------------
# shared -- two datasets that several courses use, so the answers can be
# compared across the programme rather than each course inventing its own
# ---------------------------------------------------------------------------

UNIT_PRICE = {"Rice 5kg": 280, "Tea 500g": 210,
              "Shampoo 200ml": 140, "Notebook": 40}
SALES = [
    ("Rice 5kg",      "South", "2026-01-15", 10),
    ("Shampoo 200ml", "South", "2026-01-15",  5),
    ("Tea 500g",      "South", "2026-01-15",  8),
    ("Rice 5kg",      "South", "2026-02-10",  6),
    ("Notebook",      "North", "2026-02-10", 20),
    ("Tea 500g",      "South", "2026-04-05", 12),
    ("Rice 5kg",      "North", "2026-04-05",  4),
    ("Shampoo 200ml", "South", "2026-05-20",  7),
    ("Notebook",      "North", "2026-05-20", 15),
]


def shared_sales():
    rows = [(p, r, d, q, UNIT_PRICE[p], q * UNIT_PRICE[p])
            for p, r, d, q in SALES]
    write("shared/sales-transactions.csv",
          ["product", "region", "date", "quantity", "unit_price", "revenue"],
          rows,
          {"total_revenue": 12880, "south_revenue": 10360,
           "north_revenue": 2520, "best_product": "Rice 5kg",
           "best_product_revenue": 5600, "transactions": 9},
          ["pivot tables", "GROUP BY", "MapReduce", "DAX measures",
           "Hive and Spark aggregation", "OLAP roll-up"],
          "The same nine rows Courses 1, 8, 9, 11, 12 B and 15 B all analyse. "
          "Six different engines reach the same South total, which is only "
          "meaningful because they read the same rows.")


def shared_flowers():
    """Three species, four measurements. An iris-shaped problem, generated.

    Species A is linearly separable from the other two; B and C overlap. That
    is deliberate: a classifier that reports 100% on this file has a bug, and
    the confusion matrix should show the errors falling between B and C.
    """
    rng = np.random.default_rng(20260101)
    centres = {"alba":    (5.0, 3.4, 1.5, 0.2),
               "borealis": (6.0, 2.8, 4.4, 1.3),
               "carinata": (6.6, 3.0, 5.6, 2.0)}
    rows = []
    for species, mu in centres.items():
        pts = rng.normal(mu, (0.35, 0.30, 0.40, 0.22), size=(30, 4))
        # a flower cannot have a negative petal; the tail of the normal can
        pts = np.clip(pts, 0.1, None)
        for p in pts:
            rows.append([species] + [rnd(v, 2) for v in p])
    rng.shuffle(rows)
    write("shared/flowers.csv",
          ["species", "sepal_length", "sepal_width",
           "petal_length", "petal_width"],
          rows,
          {"rows": 90, "classes": 3, "per_class": 30,
           "separable_class": "alba",
           "overlapping_pair": ["borealis", "carinata"],
           "centres": {k: list(v) for k, v in centres.items()}},
          ["k-NN", "decision trees (ID3, C4.5, CART)", "Naive Bayes",
           "k-Means", "hierarchical clustering", "PCA", "train/test split"],
          "Built from three known centres. 'alba' separates cleanly; the "
          "other two overlap on purpose, so a perfect score means a leak.")


# ---------------------------------------------------------------------------
# Course 1 -- Office Automation: the spreadsheets the experiments build
# ---------------------------------------------------------------------------

def course_01_payroll():
    emp = [("Anitha Rao", "E101", "Analytics", 25000),
           ("Bharat Kumar", "E102", "Engineering", 32000),
           ("Chitra Devi", "E103", "Support", 18500),
           ("Daniel Joseph", "E104", "Engineering", 45000),
           ("Esha Nair", "E105", "Analytics", 28000),
           ("Faisal Ahmed", "E106", "Management", 52000)]
    write("course-1-office/payroll.csv",
          ["name", "emp_id", "department", "basic_pay"], emp,
          {"employees": 6, "total_basic": 200500,
           "da_rate": 0.30, "hra_rate": 0.15, "deduction_rate": 0.10,
           "gross_is": "1.45 x basic", "net_is": "1.32 x basic",
           "total_net": 264660},
          ["SUM, AVERAGE, absolute references", "VLOOKUP / XLOOKUP / "
           "INDEX+MATCH", "conditional formatting"],
          "Deduction is 10% of (Basic + DA), not of Basic -- which is why Net "
          "is 1.32 x Basic and not 1.35 x. Check one row and you have checked "
          "the sheet.")


def course_01_class_results():
    students = [
        (1, "Aarav", 92, 88, 95, 90, 96), (2, "Bhavna", 78, 82, 75, 80, 85),
        (3, "Chaitanya", 65, 70, 58, 72, 68), (4, "Divya", 45, 52, 38, 60, 55),
        (5, "Eshan", 88, 91, 85, 79, 93), (6, "Farhan", 55, 48, 62, 51, 58),
        (7, "Gayatri", 96, 94, 98, 92, 90), (8, "Harsha", 72, 68, 75, 70, 66),
        (9, "Ishita", 38, 42, 45, 40, 39), (10, "Jatin", 82, 78, 88, 75, 80),
        (11, "Kavya", 12, 20, 8, 15, 25), (12, "Lakshmi", 60, 65, 55, 68, 62),
        (13, "Manoj", 90, 85, 92, 88, 94), (14, "Nithya", 48, 55, 50, 45, 52),
        (15, "Omkar", 75, 80, 72, 78, 74), (16, "Pallavi", 68, 62, 70, 65, 60),
        (17, "Rahul", 35, 55, 60, 58, 62), (18, "Sneha", 98, 96, 99, 95, 97),
        (19, "Tarun", 58, 60, 52, 55, 57), (20, "Usha", 85, 88, 82, 90, 86)]
    write("course-1-office/class-results.csv",
          ["roll", "name", "maths", "physics", "chemistry", "english",
           "computers"], students,
          {"students": 20, "subjects": 5,
           "grades_on_average": {"A": 3, "B": 6, "C": 4, "D": 6, "F": 1},
           "failed_a_subject": ["Divya", "Ishita", "Kavya", "Rahul"],
           "hardest_paper": "maths", "maths_mean": 67.0,
           "grades_if_graded_on_total": {"A": 19, "B": 1}},
          ["IF / nested IF / IFS", "AND, OR, IFERROR", "MIN, MAX, COUNTIF",
           "descriptive statistics"],
          "Grade on the AVERAGE. Point the formula at the total and 19 of the "
          "20 get an A, including the student who failed all five papers.")


def course_01_budget():
    rows = [("Income", 45000), ("Rent", 15000), ("Food", 8000),
            ("Transport", 3500), ("Utilities", 2800),
            ("Entertainment", 2200), ("Miscellaneous", 1500)]
    write("course-1-office/budget.csv", ["category", "amount"], rows,
          {"income": 45000, "total_expenses": 33000, "savings": 12000,
           "savings_rate": 0.266667,
           "income_for_20000_savings": 53000,
           "income_for_30pct_rate": 47142.857142857},
          ["Goal Seek", "Scenario Manager", "one-variable data table"],
          "A savings RATE of 30% is not linear in income: the answer is "
          "33000/0.70, which is not a figure you can read off the sheet.")


# ---------------------------------------------------------------------------
# Course 3 -- Python: files, CSV, dictionaries
# ---------------------------------------------------------------------------

def course_03_students():
    rng = random.Random(3)
    names = ["Anil", "Bhavya", "Charan", "Deepa", "Eshwar", "Fatima",
             "Ganesh", "Harini", "Imran", "Jyothi", "Karthik", "Latha",
             "Mohan", "Nandini", "Om", "Priya", "Rakesh", "Sita",
             "Tarun", "Uma", "Varun", "Yamini", "Zoya", "Arjun", "Bina"]
    rows = []
    for i, n in enumerate(names, start=101):
        rows.append([i, n, rng.randint(35, 99), rng.randint(35, 99),
                     rng.randint(35, 99)])
    total = sum(r[2] + r[3] + r[4] for r in rows)
    write("course-3-python/students.csv",
          ["roll", "name", "python", "maths", "statistics"], rows,
          {"rows": 25, "grand_total": total,
           "mean_of_all_marks": rnd(total / (25 * 3), 6)},
          ["file handling", "the csv module", "dictionaries",
           "list comprehensions", "exception handling"],
          "Read it with csv.DictReader, total per student, and handle a "
          "missing file with try/except -- the three things practical 11 "
          "asks for.")

# ---------------------------------------------------------------------------
# Course 4 -- Statistics: one file per test, each built to a known answer
# ---------------------------------------------------------------------------

def course_04_heights():
    rng = np.random.default_rng(404)
    vals = rng.normal(165.0, 8.0, 60)
    rows = [[i, rnd(v, 1)] for i, v in enumerate(vals, start=1)]
    xs = [r[1] for r in rows]
    mean = sum(xs) / len(xs)
    var = sum((x - mean) ** 2 for x in xs) / (len(xs) - 1)
    write("course-4-stats/heights.csv", ["student_id", "height_cm"], rows,
          {"n": 60, "population_mean": 165.0, "population_sd": 8.0,
           "sample_mean": rnd(mean, 6), "sample_sd": rnd(math.sqrt(var), 6)},
          ["mean, median, mode", "variance and standard deviation",
           "skewness and kurtosis", "the normal distribution",
           "one-sample t-test against 165"],
          "Drawn from N(165, 8). The sample mean will not be exactly 165 -- "
          "the gap between it and the population value IS the sampling error "
          "the course is about.")


def course_04_regression():
    rng = np.random.default_rng(406)
    hours = rng.uniform(0, 10, 40)
    marks = 12.0 + 6.0 * hours + rng.normal(0, 4.0, 40)
    rows = [[rnd(h, 2), rnd(m, 2)] for h, m in zip(hours, marks)]
    write("course-4-stats/study-hours-marks.csv", ["hours", "marks"], rows,
          {"n": 40, "true_intercept": 12.0, "true_slope": 6.0,
           "noise_sd": 4.0, "expect_r_above": 0.9,
           "identity_to_check": "R-squared = r-squared, and t-squared = F"},
          ["scatter plot", "Karl Pearson's correlation coefficient",
           "least-squares regression", "the two regression lines",
           "coefficient of determination"],
          "Built from marks = 12 + 6 x hours + noise. Fit it and you should "
          "recover a slope near 6 -- and the two regression lines (y on x, x "
          "on y) will NOT coincide.")


def course_04_two_sample():
    rng = np.random.default_rng(407)
    a = rng.normal(70.0, 6.0, 25)
    b = rng.normal(75.0, 6.0, 25)
    rows = [["control", rnd(v, 2)] for v in a] + \
           [["treatment", rnd(v, 2)] for v in b]
    write("course-4-stats/treatment-groups.csv", ["group", "score"], rows,
          {"n_per_group": 25, "control_mean": 70.0, "treatment_mean": 75.0,
           "true_difference": 5.0, "common_sd": 6.0,
           "expect": "reject H0 at 5%"},
          ["independent two-sample t-test", "F-test for equal variances",
           "confidence interval for a difference of means",
           "Mann-Whitney U (non-parametric)"],
          "A real difference of 5 marks with sd 6 and n=25 per group. The "
          "test SHOULD reject -- if yours does not, check which tail you "
          "used.")


def course_04_paired():
    rng = np.random.default_rng(408)
    before = rng.normal(60.0, 9.0, 20)
    after = before + rng.normal(4.0, 2.5, 20)
    rows = [[i, rnd(x, 2), rnd(y, 2)]
            for i, (x, y) in enumerate(zip(before, after), start=1)]
    write("course-4-stats/before-after.csv",
          ["subject", "before", "after"], rows,
          {"n": 20, "true_mean_gain": 4.0, "gain_sd": 2.5,
           "expect": "paired t-test rejects; the unpaired test is weaker"},
          ["paired t-test", "one-sample t-test on the differences",
           "Wilcoxon signed-rank test"],
          "The pairing is the point: run an INDEPENDENT t-test on the same "
          "two columns and watch the evidence weaken, because the "
          "between-subject variation is no longer removed.")


def course_04_anova():
    rng = np.random.default_rng(409)
    means = {"A": 40.0, "B": 44.0, "C": 50.0}
    rows = []
    for name, mu in means.items():
        for v in rng.normal(mu, 4.0, 12):
            rows.append([name, rnd(v, 2)])
    write("course-4-stats/fertiliser-yield.csv", ["fertiliser", "yield"], rows,
          {"groups": 3, "n_per_group": 12, "true_means": means,
           "within_sd": 4.0, "expect": "one-way ANOVA rejects; C differs most"},
          ["one-way ANOVA", "the F distribution",
           "post-hoc comparison", "CRD in Design of Experiments"],
          "Three fertilisers, twelve plots each. A and B are close; C is "
          "clearly higher. ANOVA says 'not all equal' -- it does not say "
          "WHICH, which is why the post-hoc test exists.")


def course_04_chisquare():
    # a table built so the association is real and the expected counts are
    # all comfortably above 5, which is the condition the test needs
    rows = []
    counts = {("male", "tea"): 45, ("male", "coffee"): 25,
              ("female", "tea"): 20, ("female", "coffee"): 50}
    for (g, d), n in counts.items():
        rows.extend([[g, d]] * n)
    write("course-4-stats/preference-survey.csv",
          ["gender", "preference"], rows,
          {"respondents": 140, "table": {f"{g}/{d}": n
                                         for (g, d), n in counts.items()},
           "expect": "chi-square test of independence rejects",
           "degrees_of_freedom": 1},
          ["chi-square test of independence", "contingency tables",
           "expected frequencies", "Yates' correction"],
          "One row per respondent, so you must build the contingency table "
          "yourself first -- which is the half of the question students "
          "skip.")

# ---------------------------------------------------------------------------
# Course 5 -- DBMS: a small relational schema, plus one deliberately bad table
# ---------------------------------------------------------------------------

DEPTS = [("D1", "Analytics", "Vijayawada"), ("D2", "Engineering", "Hyderabad"),
         ("D3", "Support", "Guntur"), ("D4", "Management", "Hyderabad")]
EMPS = [("E101", "Anitha Rao", "D1", 25000, "2021-06-01", None),
        ("E102", "Bharat Kumar", "D2", 32000, "2020-01-15", "E106"),
        ("E103", "Chitra Devi", "D3", 18500, "2022-08-10", "E106"),
        ("E104", "Daniel Joseph", "D2", 45000, "2018-03-05", "E106"),
        ("E105", "Esha Nair", "D1", 28000, "2021-11-20", "E101"),
        ("E106", "Faisal Ahmed", "D4", 52000, "2016-07-01", None),
        ("E107", "Geetha Menon", "D2", 30000, "2023-02-14", "E104")]
PROJECTS = [("P1", "Sales Dashboard", "D1", 250000),
            ("P2", "Billing Rewrite", "D2", 800000),
            ("P3", "Helpdesk Portal", "D3", 120000),
            ("P4", "Data Lake", "D2", 640000)]
ASSIGN = [("E101", "P1", 30), ("E105", "P1", 25), ("E102", "P2", 40),
          ("E104", "P2", 35), ("E104", "P4", 10), ("E107", "P4", 38),
          ("E103", "P3", 20)]


def course_05_schema():
    write("course-5-dbms/departments.csv",
          ["dept_id", "dept_name", "city"], DEPTS,
          {"rows": 4, "primary_key": "dept_id"},
          ["CREATE TABLE", "primary keys", "SELECT ... WHERE"],
          "The one-side of the one-to-many with employees.")
    write("course-5-dbms/employees.csv",
          ["emp_id", "name", "dept_id", "salary", "hired", "manager_id"],
          [[a, b, c, d, e, f if f else ""] for a, b, c, d, e, f in EMPS],
          {"rows": 7, "foreign_keys": ["dept_id -> departments",
                                       "manager_id -> employees"],
           "employees_with_no_manager": 2,
           "total_salary": sum(e[3] for e in EMPS),
           "inner_join_with_departments_rows": 7,
           "self_join_manager_rows": 5},
          ["INNER / LEFT / RIGHT / FULL JOIN", "self join", "GROUP BY "
           "with HAVING", "subqueries", "referential integrity"],
          "manager_id is a self-referencing foreign key and two rows are "
          "NULL. An INNER self-join loses those two; a LEFT join keeps them "
          "-- that difference is the exam question.")
    write("course-5-dbms/projects.csv",
          ["project_id", "project_name", "dept_id", "budget"], PROJECTS,
          {"rows": 4, "total_budget": sum(p[3] for p in PROJECTS)},
          ["aggregate functions", "ORDER BY", "correlated subqueries"],
          "Every project belongs to a department, so a three-table join runs "
          "employees -> departments -> projects.")
    write("course-5-dbms/assignments.csv",
          ["emp_id", "project_id", "hours_per_week"], ASSIGN,
          {"rows": 7, "composite_primary_key": ["emp_id", "project_id"],
           "employees_on_two_projects": ["E104"],
           "employees_on_no_project": ["E106"]},
          ["many-to-many resolution", "composite keys", "EXISTS / NOT EXISTS",
           "division queries"],
          "The junction table. 'Which employees work on NO project?' is the "
          "NOT EXISTS question, and E106 is the answer.")


def course_05_unnormalised():
    """One table in first-normal-form trouble, on purpose."""
    rows = [
        ("O1001", "2026-01-12", "Anitha Rao", "Vijayawada", "9876543210",
         "Rice 5kg; Tea 500g", "2; 3", "280; 210"),
        ("O1002", "2026-01-14", "Bharat Kumar", "Hyderabad", "9876500011",
         "Notebook", "10", "40"),
        ("O1003", "2026-02-02", "Anitha Rao", "Vijayawada", "9876543210",
         "Shampoo 200ml; Notebook; Tea 500g", "1; 4; 2", "140; 40; 210"),
        ("O1004", "2026-02-19", "Chitra Devi", "Guntur", "9876522233",
         "Rice 5kg", "5", "280"),
    ]
    write("course-5-dbms/unnormalised-orders.csv",
          ["order_id", "order_date", "customer_name", "customer_city",
           "customer_phone", "items", "quantities", "unit_prices"], rows,
          {"rows": 4, "violates": "1NF -- items, quantities and unit_prices "
                                  "are repeating groups in one cell",
           "then_violates": "2NF and 3NF -- customer city and phone depend on "
                            "the customer, not the order",
           "target": "orders, order_items, customers, products -- four tables",
           "repeated_customer": "Anitha Rao appears in O1001 and O1003"},
          ["1NF, 2NF, 3NF, BCNF", "functional dependencies",
           "decomposition", "update, insert and delete anomalies"],
          "Normalise it to 3NF and count the tables. Then change Anitha's "
          "phone number in the ORIGINAL file and see how many rows you have "
          "to touch -- that is the update anomaly, not a definition.")


# ---------------------------------------------------------------------------
# Course 6 -- R: a frame with factors, a numeric response and one NA column
# ---------------------------------------------------------------------------

def course_06_cars():
    rng = np.random.default_rng(606)
    n = 50
    weight = rng.uniform(0.9, 2.4, n)              # tonnes
    cyl = rng.choice([4, 6, 8], n, p=[0.5, 0.3, 0.2])
    # mpg falls with weight and with cylinders, both by a known amount
    mpg = 34.0 - 7.5 * weight - 0.8 * (cyl - 4) + rng.normal(0, 1.6, n)
    trans = rng.choice(["manual", "automatic"], n)
    rows = []
    for i in range(n):
        # three service records are genuinely missing, as real frames are
        service = "" if i in (7, 23, 41) else rnd(rng.uniform(1, 9), 1)
        rows.append([f"CAR{i + 1:03d}", rnd(mpg[i], 2), rnd(weight[i], 3),
                     int(cyl[i]), trans[i], service])
    write("course-6-r/car-mileage.csv",
          ["car_id", "mpg", "weight_t", "cylinders", "transmission",
           "service_months"], rows,
          {"rows": 50, "true_intercept": 34.0, "weight_coefficient": -7.5,
           "cylinder_coefficient": -0.8, "noise_sd": 1.6,
           "missing_service_months": 3,
           "cylinder_levels": [4, 6, 8]},
          ["data frames and factors", "read.csv and str()",
           "is.na / na.omit", "lm() multiple regression", "aggregate and "
           "tapply", "dplyr verbs", "ggplot2 scatter with a fitted line"],
          "Fit mpg ~ weight_t + cylinders and you should recover about -7.5 "
          "and -0.8. Three service_months are blank on purpose: read it "
          "without na.strings and R will make the whole column a factor.")


# ---------------------------------------------------------------------------
# Course 7 -- Web: a catalogue to render, validate and fetch
# ---------------------------------------------------------------------------

def course_07_products():
    rows = [
        ("P001", "Rice 5kg", "Grocery", 280, 42, 4.4, "in_stock"),
        ("P002", "Tea 500g", "Grocery", 210, 18, 4.1, "in_stock"),
        ("P003", "Shampoo 200ml", "Personal Care", 140, 0, 3.8, "out_of_stock"),
        ("P004", "Notebook", "Stationery", 40, 260, 4.6, "in_stock"),
        ("P005", "Pen (pack of 5)", "Stationery", 55, 130, 4.0, "in_stock"),
        ("P006", "Hand Wash 250ml", "Personal Care", 95, 7, 3.5, "low_stock"),
        ("P007", "Sugar 1kg", "Grocery", 48, 0, 4.2, "out_of_stock"),
        ("P008", "Stapler", "Stationery", 120, 15, 3.9, "in_stock"),
    ]
    write("course-7-web/products.csv",
          ["sku", "name", "category", "price", "stock", "rating", "status"],
          rows,
          {"rows": 8, "categories": 3, "out_of_stock": 2,
           "total_stock_value": sum(r[3] * r[4] for r in rows),
           "highest_rated": "Notebook",
           "cheapest_in_stock": "Notebook"},
          ["rendering a table from JSON", "the Fetch API",
           "array filter / map / reduce", "sorting a table by column",
           "form validation against a list"],
          "Convert it to JSON, render it as a table, then filter by category "
          "and sort by price -- experiments 14 and 16 in one file. Two rows "
          "are out of stock, so your filter has something to remove.")

# ---------------------------------------------------------------------------
# Course 8 -- Data Mining: association rules, clustering, OLAP
# ---------------------------------------------------------------------------

def course_08_basket():
    """Transactions with a planted rule: bread -> butter.

    Long form (one row per item) rather than one row per basket, because
    every tool -- mlxtend, WEKA, a GROUP BY -- wants it reshaped first, and
    reshaping it is half the exercise.
    """
    baskets = [
        ["bread", "butter", "milk"], ["bread", "butter"],
        ["bread", "butter", "jam"], ["milk", "eggs"],
        ["bread", "butter", "milk", "eggs"], ["bread", "jam"],
        ["butter", "milk"], ["bread", "butter", "eggs"],
        ["milk", "jam"], ["bread", "butter", "milk"],
        ["eggs", "jam"], ["bread", "butter"],
    ]
    rows = [[f"T{i:03d}", item]
            for i, b in enumerate(baskets, start=1) for item in b]
    n = len(baskets)
    bread = sum(1 for b in baskets if "bread" in b)
    butter = sum(1 for b in baskets if "butter" in b)
    both = sum(1 for b in baskets if {"bread", "butter"} <= set(b))
    write("course-8-datamining/market-basket.csv",
          ["transaction_id", "item"], rows,
          {"transactions": n, "distinct_items": 5,
           "support_bread": rnd(bread / n, 4),
           "support_butter": rnd(butter / n, 4),
           "support_bread_and_butter": rnd(both / n, 4),
           "confidence_bread_to_butter": rnd(both / bread, 4),
           "lift_bread_to_butter": rnd((both / n) / ((bread / n) * (butter / n)), 4),
           "planted_rule": "bread -> butter"},
          ["Apriori", "FP-Growth", "support, confidence and lift",
           "candidate generation and pruning", "Partition and DIC"],
          "Twelve baskets, one strong rule. Compute the support of every "
          "1-itemset by hand first -- Apriori's whole trick is that it never "
          "counts a 2-itemset whose halves failed.")


def course_08_clusters():
    """Three separated blobs plus scattered noise -- k-Means against DBSCAN.

    The noise is what separates the two algorithms: k-Means must assign every
    noise point to some cluster, DBSCAN labels them -1. That contrast is the
    reason both are on the syllabus.
    """
    rng = np.random.default_rng(808)
    centres = [(2.0, 2.0), (8.0, 3.0), (5.0, 9.0)]
    rows = []
    for cid, (cx, cy) in enumerate(centres, start=1):
        for x, y in rng.normal((cx, cy), 0.55, size=(25, 2)):
            rows.append([rnd(x, 3), rnd(y, 3), cid])
    for x, y in rng.uniform((0, 0), (10, 11), size=(10, 2)):
        rows.append([rnd(x, 3), rnd(y, 3), -1])
    rng.shuffle(rows)
    write("course-8-datamining/cluster-points.csv",
          ["x", "y", "true_cluster"], rows,
          {"rows": 85, "true_k": 3, "points_per_cluster": 25,
           "noise_points": 10, "centres": centres,
           "expect": "k-Means finds 3 centres near those; DBSCAN with "
                     "eps~0.9 and min_samples~4 labels most noise -1"},
          ["k-Means and the elbow method", "k-Medoids", "DBSCAN",
           "hierarchical clustering and dendrograms",
           "silhouette score", "BIRCH"],
          "true_cluster is the answer key -- drop it before you cluster, "
          "then score against it. The ten rows labelled -1 are noise: "
          "k-Means cannot say so, DBSCAN can.")


def course_08_warehouse():
    """A fact table wide enough to roll up and drill down."""
    rng = np.random.default_rng(810)
    regions = {"South": ["Vijayawada", "Guntur"], "North": ["Hyderabad"]}
    products = {"Grocery": ["Rice 5kg", "Tea 500g"],
                "Personal": ["Shampoo 200ml"], "Stationery": ["Notebook"]}
    rows = []
    for month in range(1, 13):
        for region, cities in regions.items():
            for city in cities:
                for cat, items in products.items():
                    for item in items:
                        qty = int(rng.integers(2, 25))
                        rows.append([f"2026-{month:02d}", region, city, cat,
                                     item, qty, qty * UNIT_PRICE[item]])
    total = sum(r[6] for r in rows)
    south = sum(r[6] for r in rows if r[1] == "South")
    write("course-8-datamining/warehouse-facts.csv",
          ["month", "region", "city", "category", "product",
           "quantity", "revenue"], rows,
          {"rows": len(rows), "months": 12, "regions": 2, "cities": 3,
           "categories": 3, "products": 4, "total_revenue": total,
           "south_revenue": south,
           "grain": "one row per month per city per product"},
          ["star schema", "roll-up and drill-down", "slice and dice",
           "pivot", "OLAP cube operations", "measures against dimensions"],
          "State the grain before you aggregate anything. Roll up city -> "
          "region -> all and the totals must agree at every level; if they "
          "do not, you have double-counted a join.")


# ---------------------------------------------------------------------------
# Course 9 -- Pandas: one deliberately dirty file, one clean panel
# ---------------------------------------------------------------------------

def course_09_messy():
    """Every cleaning problem the syllabus names, planted and counted."""
    rows = [
        ["C001", " Anitha Rao ", "anitha@nri.ac.in", "Vijayawada", "28", "45000", "2024-01-15"],
        ["C002", "Bharat Kumar", "bharat@nri.ac.in", "hyderabad", "34", "62000", "2024-02-03"],
        ["C003", "Chitra Devi", "", "Guntur", "", "38000", "2024-02-19"],
        ["C004", "Daniel Joseph", "daniel@nri.ac.in", "HYDERABAD", "41", "", "2024-03-01"],
        ["C002", "Bharat Kumar", "bharat@nri.ac.in", "hyderabad", "34", "62000", "2024-02-03"],
        ["C005", "Esha Nair", "esha@nri.ac.in", "Vijayawada", "29", "51000", "2024-03-22"],
        ["C006", "Faisal Ahmed", "faisal@nri.ac.in", "Guntur", "150", "58000", "2024-04-10"],
        ["C007", "Geetha Menon", "geetha@nri.ac.in", " Hyderabad", "37", "1200000", "2024-04-28"],
        ["C008", "Harsha Reddy", "not-an-email", "Vijayawada", "26", "43000", "2024-05-05"],
        ["C009", "Indira Rao", "indira@nri.ac.in", "Guntur", "33", "47000", ""],
        ["C010", "Jyothi Varma", "jyothi@nri.ac.in", "Vijayawada", "31", "49000", "2024-06-14"],
        ["C011", "Kiran Babu", "kiran@nri.ac.in", "hyderabad", "", "", "2024-06-30"],
    ]
    write("course-9-python-da/messy-customers.csv",
          ["customer_id", "name", "email", "city", "age", "salary",
           "joined"], rows,
          {"rows": 12, "duplicate_rows": 1, "duplicate_id": "C002",
           "unique_customers": 11,
           "missing_email": 1, "missing_age": 2, "missing_salary": 2,
           "missing_joined": 1, "total_missing_cells": 6,
           "leading_or_trailing_space": ["C001 name", "C007 city"],
           "city_case_variants": ["Hyderabad", "hyderabad", "HYDERABAD"],
           "distinct_cities_after_cleaning": 3,
           "impossible_age": {"C006": 150},
           "salary_outlier": {"C007": 1200000},
           "invalid_email": "C008"},
          ["isnull and sum", "dropna against fillna", "drop_duplicates",
           "str.strip, str.lower, str.contains", "astype and to_datetime",
           "IQR and z-score outlier detection", "value_counts"],
          "Six empty cells, one duplicated row, three spellings of "
          "Hyderabad, an age of 150 and a salary twenty times the next. "
          "Clean it and your row count should fall from 12 to 11 and your "
          "city count from 5 to 3.")


def course_09_monthly():
    rng = np.random.default_rng(909)
    rows = []
    for year in (2024, 2025):
        for month in range(1, 13):
            for region in ("South", "North", "East"):
                base = {"South": 52000, "North": 38000, "East": 27000}[region]
                trend = 400 * ((year - 2024) * 12 + month)
                season = 6000 * math.sin(2 * math.pi * month / 12)
                v = base + trend + season + rng.normal(0, 1800)
                rows.append([f"{year}-{month:02d}", region, round(v)])
    write("course-9-python-da/monthly-sales.csv",
          ["month", "region", "revenue"], rows,
          {"rows": len(rows), "months": 24, "regions": 3,
           "trend_per_month": 400, "seasonal_amplitude": 6000,
           "region_base": {"South": 52000, "North": 38000, "East": 27000},
           "shape": "long -- 72 rows, not a 24x3 grid"},
          ["groupby and agg", "pivot_table", "melt and stack",
           "merge and join", "resample and rolling means",
           "matplotlib, Seaborn and Plotly"],
          "Long format on purpose. pivot_table it into a 24 x 3 grid, plot "
          "the three lines, then melt it back -- and check you get the same "
          "72 rows you started with.")

# ---------------------------------------------------------------------------
# Course 10 -- MongoDB: flat CSVs that map onto embedded and referenced models
# ---------------------------------------------------------------------------

def course_10_documents():
    students = [
        ("S101", "Anitha Rao", 19, "Vijayawada", "DSC301;STA302", "A;B"),
        ("S102", "Bharat Kumar", 20, "Hyderabad", "DSC301", "B"),
        ("S103", "Chitra Devi", 19, "Guntur", "STA302;CSC303;DSC301", "A;A;C"),
        ("S104", "Daniel Joseph", 21, "Hyderabad", "", ""),
        ("S105", "Esha Nair", 20, "Vijayawada", "CSC303;STA302", "B;A"),
        ("S106", "Faisal Ahmed", 22, "Guntur", "DSC301;CSC303", "C;B"),
    ]
    write("course-10-mongodb/students.csv",
          ["student_id", "name", "age", "city", "enrolled_courses",
           "grades"], students,
          {"rows": 6, "student_with_no_enrolment": "S104",
           "max_enrolments": 3, "distinct_cities": 3,
           "embedded_shape": "enrolments as an array of subdocuments",
           "array_field_note": "semicolon-separated, so you split before "
                               "you insert"},
          ["insertMany", "find with $eq, $gt, $in", "$elemMatch on arrays",
           "embedded against referenced models", "aggregation $unwind, "
           "$group, $lookup", "multikey indexes"],
          "Two semicolon-separated columns become ONE array of subdocuments. "
          "S104 has no enrolments -- so $unwind will drop that student "
          "unless you pass preserveNullAndEmptyArrays.")
    courses = [("DSC301", "Data Science with R", 4, "Dr. Rao", 60),
               ("STA302", "Statistical Foundations", 3, "Dr. Devi", 45),
               ("CSC303", "Web Technologies", 4, "Dr. Menon", 55)]
    write("course-10-mongodb/courses.csv",
          ["course_id", "title", "credits", "instructor", "capacity"], courses,
          {"rows": 3, "join_key": "course_id matches the ids inside "
                                  "students.enrolled_courses"},
          ["$lookup", "normalised against embedded modelling",
           "schema validation rules"],
          "The referenced half of the model. Embed it into each student and "
          "then change an instructor's name -- count how many documents you "
          "must touch. That count is the argument for referencing.")


# ---------------------------------------------------------------------------
# Course 11 -- Business Intelligence: the star schema, one file per table
# ---------------------------------------------------------------------------

def course_11_star():
    write("course-11-bi/dim-product.csv",
          ["product_key", "product", "category", "supplier_key",
           "unit_cost", "list_price"],
          [("P1", "Rice 5kg", "Grocery", "S1", 220.0, 280.0),
           ("P2", "Tea 500g", "Grocery", "S1", 150.0, 210.0),
           ("P3", "Shampoo 200ml", "Personal", "S2", 90.0, 140.0),
           ("P4", "Notebook", "Stationery", "S3", 25.0, 40.0)],
          {"rows": 4, "role": "dimension",
           "snowflake_edge": "supplier_key points at a further table, which "
                             "is what makes this a snowflake rather than a "
                             "pure star"},
          ["dimensional modelling", "star against snowflake",
           "relationships and cardinality", "Power Query"],
          "Four products. The supplier column is the one edge that turns the "
          "star into a snowflake.")
    write("course-11-bi/dim-store.csv",
          ["store_key", "store", "region", "opened"],
          [("T1", "Vijayawada", "South", 2019), ("T2", "Guntur", "South", 2021),
           ("T3", "Hyderabad", "North", 2020)],
          {"rows": 3, "regions": {"South": 2, "North": 1}},
          ["slicers and cross-filtering", "row-level security"],
          "Two southern stores against one northern one -- so a naive "
          "average by region is not the same as a total by region.")
    write("course-11-bi/dim-date.csv",
          ["date_key", "date", "year", "month", "quarter"],
          [("D1", "2026-01-15", 2026, 1, "Q1"), ("D2", "2026-02-10", 2026, 2, "Q1"),
           ("D3", "2026-04-05", 2026, 4, "Q2"), ("D4", "2026-05-20", 2026, 5, "Q2")],
          {"rows": 4, "missing_month": "March -- there is no D-key for it",
           "quarters": {"Q1": 2, "Q2": 2}},
          ["time intelligence", "date hierarchies", "grouping by month"],
          "There is no March. Group by month and you get four rows, not "
          "five -- which is what breaks a month-on-month growth column.")
    write("course-11-bi/fact-sales.csv",
          ["date_key", "store_key", "product_key", "qty"],
          [("D1", "T1", "P1", 10), ("D1", "T1", "P3", 5), ("D1", "T2", "P2", 8),
           ("D2", "T1", "P1", 6), ("D2", "T3", "P4", 20), ("D3", "T2", "P2", 12),
           ("D3", "T3", "P1", 4), ("D4", "T1", "P3", 7), ("D4", "T3", "P4", 15)],
          {"rows": 9, "total_qty": 87, "total_revenue": 12880,
           "south_revenue": 10360, "north_revenue": 2520,
           "grain": "one row per product per store per day"},
          ["SUM, COUNT, DISTINCTCOUNT", "CALCULATE and filter context",
           "measure against calculated column", "fan and chasm traps"],
          "Join it to all three dimensions and you have the flat table a BI "
          "tool builds internally. Revenue is qty x list_price: 12,880 in "
          "total, 10,360 of it South.")


# ---------------------------------------------------------------------------
# Course 12 A -- Machine Learning: regression, classification, clustering
# ---------------------------------------------------------------------------

def course_12a_houses():
    rng = np.random.default_rng(1201)
    n = 200
    area = rng.uniform(600, 2600, n)
    beds = rng.integers(1, 5, n)
    age = rng.uniform(0, 40, n)
    price = (12.0 + 0.045 * area + 3.5 * beds - 0.25 * age
             + rng.normal(0, 8.0, n))
    rows = [[rnd(a, 1), int(b), rnd(g, 1), rnd(p, 2)]
            for a, b, g, p in zip(area, beds, age, price)]
    write("course-12a-ml/house-prices.csv",
          ["area_sqft", "bedrooms", "age_years", "price_lakh"], rows,
          {"rows": 200, "intercept": 12.0, "area_coefficient": 0.045,
           "bedroom_coefficient": 3.5, "age_coefficient": -0.25,
           "noise_sd": 8.0, "expect_r2_above": 0.85},
          ["simple and multiple linear regression", "train/test split",
           "MAE, MSE, RMSE, R-squared", "feature scaling",
           "polynomial regression", "regularisation"],
          "Fit it and compare your coefficients with the four above. Then "
          "scale the features and refit: the coefficients change, the "
          "predictions do not, and knowing why is the point.")


def course_12a_loans():
    rng = np.random.default_rng(1202)
    n = 300
    income = rng.uniform(15000, 120000, n)
    debt = rng.uniform(0, 60000, n)
    score = rng.integers(300, 850, n)
    # a known logistic rule, so the Bayes-optimal boundary is knowable
    z = -6.0 + 0.00005 * income - 0.00006 * debt + 0.008 * score
    prob = 1 / (1 + np.exp(-z))
    approved = (rng.uniform(0, 1, n) < prob).astype(int)
    rows = [[round(i), round(d), int(s), int(a)]
            for i, d, s, a in zip(income, debt, score, approved)]
    write("course-12a-ml/loan-approval.csv",
          ["income", "debt", "credit_score", "approved"], rows,
          {"rows": 300, "positive_rate": rnd(float(approved.mean()), 4),
           "true_rule": "sigmoid(-6 + 0.00005*income - 0.00006*debt "
                        "+ 0.008*credit_score)",
           "largest_raw_coefficient": "credit_score (0.008, which is 160x "
                                     "the coefficient on income)",
           "largest_standardised_effect": "income -- because its spread is "
                                          "far wider, coefficient x SD comes "
                                          "out around 1.5 against 1.3 for "
                                          "credit_score",
           "expect_accuracy_above": 0.75},
          ["logistic regression", "k-NN", "decision tree", "Naive Bayes",
           "SVM", "confusion matrix, precision, recall, F1", "ROC and AUC",
           "cross-validation"],
          "Generated from a logistic rule, so there IS an irreducible error "
          "rate -- a model reporting 100% has leaked the label. Compare your "
          "coefficients with the true ones, and note which feature matters "
          "most: credit_score has by far the biggest RAW coefficient, but "
          "income has the biggest effect, because a coefficient means "
          "nothing until you multiply it by the spread of its variable.")


def course_12a_segments():
    rng = np.random.default_rng(1203)
    profiles = [(2200, 4, 0.15), (7800, 12, 0.35), (15500, 26, 0.62)]
    rows = []
    for cid, (spend, visits, ratio) in enumerate(profiles, start=1):
        for _ in range(40):
            rows.append([round(rng.normal(spend, spend * 0.12)),
                         int(max(1, rng.normal(visits, visits * 0.2))),
                         rnd(min(0.99, max(0.01, rng.normal(ratio, 0.06))), 3),
                         cid])
    rng.shuffle(rows)
    write("course-12a-ml/customer-segments.csv",
          ["annual_spend", "visits_per_year", "online_ratio",
           "true_segment"], rows,
          {"rows": 120, "true_k": 3, "per_segment": 40,
           "profiles": {"1": "low spend, rare visits, mostly in store",
                        "2": "mid spend, monthly, mixed",
                        "3": "high spend, fortnightly, mostly online"},
           "note": "the three features are on wildly different scales"},
          ["k-Means", "the elbow method", "silhouette score",
           "feature scaling before distance-based methods",
           "hierarchical clustering", "PCA for visualisation"],
          "Cluster it WITHOUT scaling first. annual_spend runs to five "
          "figures and online_ratio is under 1, so unscaled k-Means clusters "
          "on spend alone. Then scale and watch the answer change.")

# ---------------------------------------------------------------------------
# Course 12 B -- Big Data: things you count in parallel
# ---------------------------------------------------------------------------

def course_12b_logs():
    rng = np.random.default_rng(1204)
    ips = [f"10.0.{rng.integers(0, 4)}.{i}" for i in range(1, 26)]
    paths = ["/", "/index.html", "/products", "/products/rice",
             "/cart", "/checkout", "/api/search", "/static/app.js"]
    codes = [200, 200, 200, 200, 301, 404, 500]
    rows = []
    for i in range(1200):
        rows.append([f"2026-03-{rng.integers(1, 8):02d}T"
                     f"{rng.integers(0, 24):02d}:{rng.integers(0, 60):02d}:00Z",
                     ips[int(rng.integers(0, len(ips)))],
                     paths[int(rng.integers(0, len(paths)))],
                     int(codes[int(rng.integers(0, len(codes)))]),
                     int(rng.integers(120, 9000))])
    from collections import Counter
    status = Counter(r[3] for r in rows)
    write("course-12b-bigdata/web-logs.csv",
          ["timestamp", "ip", "path", "status", "bytes"], rows,
          {"rows": 1200, "distinct_ips": len(set(r[1] for r in rows)),
           "distinct_paths": 8,
           "status_counts": {str(k): v for k, v in sorted(status.items())},
           "total_bytes": sum(r[4] for r in rows),
           "error_rate": rnd(sum(v for k, v in status.items() if k >= 400)
                             / len(rows), 4)},
          ["MapReduce word count and its shape", "the shuffle and sort phase",
           "combiners", "Hive GROUP BY", "Pig FOREACH GENERATE",
           "Spark RDD reduceByKey and DataFrame agg"],
          "Big enough that counting by hand is out and a map-reduce is in. "
          "Count hits per path, bytes per IP and the error rate three ways "
          "-- a dict, a GROUP BY and reduceByKey -- and the answers must "
          "agree.")


def course_12b_corpus():
    docs = [
        ("D1", "the quick brown fox jumps over the lazy dog"),
        ("D2", "the lazy dog sleeps in the warm sun"),
        ("D3", "a quick brown dog outpaces a quick fox"),
        ("D4", "data flows through the cluster and the cluster counts words"),
        ("D5", "counting words is the hello world of distributed computing"),
    ]
    from collections import Counter
    words = Counter(w for _, t in docs for w in t.split())
    write("course-12b-bigdata/wordcount-corpus.csv",
          ["doc_id", "text"], docs,
          {"documents": 5, "total_words": sum(words.values()),
           "distinct_words": len(words),
           "top_word": words.most_common(1)[0][0],
           "top_word_count": words.most_common(1)[0][1],
           "count_of_dog": words["dog"], "count_of_quick": words["quick"]},
          ["the canonical MapReduce word count", "mapper, combiner, reducer",
           "TF-IDF (Course 15 A uses the same file)"],
          "Small enough to count by hand, which is the point: work out the "
          "answer on paper, then make MapReduce agree with you.")


# ---------------------------------------------------------------------------
# Course 13 A -- AI: search, constraints and logic, as relations
# ---------------------------------------------------------------------------

def course_13a_graph():
    edges = [("Arad", "Zerind", 75), ("Arad", "Sibiu", 140),
             ("Arad", "Timisoara", 118), ("Zerind", "Oradea", 71),
             ("Oradea", "Sibiu", 151), ("Timisoara", "Lugoj", 111),
             ("Lugoj", "Mehadia", 70), ("Mehadia", "Drobeta", 75),
             ("Drobeta", "Craiova", 120), ("Sibiu", "Fagaras", 99),
             ("Sibiu", "Rimnicu", 80), ("Rimnicu", "Pitesti", 97),
             ("Rimnicu", "Craiova", 146), ("Craiova", "Pitesti", 138),
             ("Pitesti", "Bucharest", 101), ("Fagaras", "Bucharest", 211)]
    write("course-13a-ai/graph-edges.csv",
          ["from_city", "to_city", "cost"], edges,
          {"edges": 16, "nodes": 13, "undirected": True,
           "shortest_path_arad_to_bucharest":
               ["Arad", "Sibiu", "Rimnicu", "Pitesti", "Bucharest"],
           "shortest_cost": 418,
           "bfs_path_is_shorter_in_hops_but_costlier":
               ["Arad", "Sibiu", "Fagaras", "Bucharest"],
           "bfs_path_cost": 450},
          ["BFS, DFS, uniform-cost search", "depth-limited and iterative "
           "deepening", "greedy best-first and A*", "admissible heuristics"],
          "The classic map. BFS finds a three-hop route costing 450; "
          "uniform-cost finds a four-hop route costing 418. Fewest steps and "
          "cheapest are different questions, and this file proves it.")


def course_13a_csp():
    adj = [("WA", "NT"), ("WA", "SA"), ("NT", "SA"), ("NT", "Q"),
           ("SA", "Q"), ("SA", "NSW"), ("SA", "V"), ("Q", "NSW"),
           ("NSW", "V")]
    write("course-13a-ai/map-colouring.csv",
          ["region", "neighbour"], adj,
          {"regions": 7, "adjacencies": 9, "isolated_region": "T",
           "chromatic_number": 3,
           "expect": "3 colours suffice; 2 do not, because WA-NT-SA is a "
                     "triangle"},
          ["constraint satisfaction", "backtracking search",
           "forward checking and arc consistency (AC-3)",
           "minimum-remaining-values heuristic"],
          "Tasmania touches nothing, so it takes any colour -- a free "
          "variable that MRV should pick last. WA, NT and SA form a "
          "triangle, which is why two colours cannot work.")


def course_13a_family():
    rows = [("john", "mary"), ("john", "peter"), ("susan", "mary"),
            ("susan", "peter"), ("mary", "alice"), ("mary", "bob"),
            ("david", "alice"), ("david", "bob"), ("peter", "carol")]
    write("course-13a-ai/family-relations.csv", ["parent", "child"], rows,
          {"facts": 9, "individuals": 8,
           "siblings": [["mary", "peter"], ["alice", "bob"]],
           "grandparent_pairs": 6,
           "expect": "grandparent(X,Z) :- parent(X,Y), parent(Y,Z) yields 6"},
          ["Prolog facts and rules", "unification and backtracking",
           "recursive rules (ancestor)", "first-order logic",
           "forward and backward chaining"],
          "Load it as parent/2 facts and define sibling, grandparent and a "
          "recursive ancestor. Six grandparent pairs -- count them by hand "
          "before you run it.")


# ---------------------------------------------------------------------------
# Course 13 B -- Cloud: the two things you can compute without an account
# ---------------------------------------------------------------------------

def course_13b_costs():
    rows = [("standard", "hot", 500, 0.023, 0.0, 0.09),
            ("infrequent", "cool", 2000, 0.0125, 0.01, 0.09),
            ("archive", "cold", 8000, 0.00099, 0.02, 0.09)]
    monthly = [gb * price for _, _, gb, price, _, _ in rows]
    write("course-13b-cloud/storage-costs.csv",
          ["tier", "temperature", "gb_stored", "price_per_gb_month",
           "retrieval_per_gb", "egress_per_gb"], rows,
          {"tiers": 3,
           "monthly_storage_cost": {r[0]: rnd(m, 4)
                                    for r, m in zip(rows, monthly)},
           "total_monthly_storage": rnd(sum(monthly), 4),
           "archive_is_cheaper_to_store_but":
               "retrieving all 8000 GB costs 160.00, which is twenty times "
               "its monthly storage bill",
           "break_even_note": "archive only wins if you read it rarely"},
          ["storage tiers and lifecycle policies", "total cost of ownership",
           "egress charges", "capex against opex"],
          "Work out the monthly bill, then the bill if you had to read every "
          "byte back once. The cheapest tier to STORE is the most expensive "
          "to READ, and that reversal is the exam answer.")


def course_13b_iam():
    rows = [("alice", "s3:GetObject", "reports/*", "Allow"),
            ("alice", "s3:PutObject", "reports/*", "Allow"),
            ("alice", "s3:DeleteObject", "reports/*", "Deny"),
            ("bob", "s3:GetObject", "reports/*", "Allow"),
            ("bob", "s3:GetObject", "reports/salaries.csv", "Deny"),
            ("carol", "s3:*", "reports/*", "Allow"),
            ("carol", "s3:DeleteObject", "reports/*", "Deny")]
    write("course-13b-cloud/iam-policies.csv",
          ["principal", "action", "resource", "effect"], rows,
          {"statements": 7, "principals": 3,
           "rule": "an explicit Deny always beats an Allow, and anything not "
                   "allowed is denied by default",
           "alice_can_delete": False,
           "bob_can_read_salaries": False,
           "bob_can_read_other_reports": True,
           "carol_can_delete": False,
           "dave_can_read": False},
          ["IAM policy evaluation", "explicit deny against implicit deny",
           "least privilege", "wildcards in resource ARNs"],
          "Carol has s3:* on the bucket AND an explicit Deny on delete. "
          "Explicit Deny wins -- so a wildcard Allow is not the same as "
          "unrestricted access, and dave, who appears nowhere, is denied by "
          "default.")

# ---------------------------------------------------------------------------
# Course 14 A -- Deep Learning
# ---------------------------------------------------------------------------

def course_14a_xor():
    write("course-14a-deeplearning/xor.csv", ["x1", "x2", "y"],
          [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)],
          {"rows": 4, "linearly_separable": False,
           "single_layer_perceptron_best_accuracy": 0.75,
           "why": "no straight line puts (0,1) and (1,0) on one side and "
                  "(0,0) and (1,1) on the other",
           "solved_by": "one hidden layer of 2 units with a non-linear "
                        "activation"},
          ["the perceptron and its limit", "activation functions",
           "one hidden layer", "backpropagation by hand"],
          "Four rows that ended an AI winter. Train a single-layer "
          "perceptron until you are convinced it cannot exceed 3 of 4, then "
          "add one hidden layer.")


def course_14a_sensor():
    rng = np.random.default_rng(1401)
    n = 400
    t = rng.uniform(15, 45, n)         # temperature
    v = rng.uniform(0, 10, n)          # vibration
    # a circular decision boundary -- deliberately not linear
    fail = (((t - 30) / 9) ** 2 + ((v - 5) / 3) ** 2 > 1.0)
    flip = rng.uniform(0, 1, n) < 0.05
    label = (fail ^ flip).astype(int)
    rows = [[rnd(a, 2), rnd(b, 2), int(c)] for a, b, c in zip(t, v, label)]
    write("course-14a-deeplearning/sensor-failures.csv",
          ["temperature_c", "vibration_mm_s", "failed"], rows,
          {"rows": 400, "boundary": "elliptical: ((t-30)/9)^2 + "
                                    "((v-5)/3)^2 > 1",
           "label_noise": 0.05, "ceiling_accuracy": 0.95,
           "positive_rate": rnd(float(label.mean()), 4),
           "expect": "logistic regression plateaus near 0.65; one hidden "
                     "layer reaches the low 0.9s"},
          ["binary classification with a neural net", "why depth helps",
           "sigmoid output and binary cross-entropy",
           "overfitting, dropout, early stopping"],
          "The boundary is an ellipse, so a linear model cannot do well "
          "however long you train it. Five per cent of labels are flipped, "
          "so 0.95 is the ceiling -- anything above it is a leak.")


# ---------------------------------------------------------------------------
# Course 14 B -- Time Series
# ---------------------------------------------------------------------------

def course_14b_ar2():
    rng = np.random.default_rng(1402)
    n, burn = 300, 200
    phi1, phi2, sigma = 0.6, -0.3, 1.0
    x = np.zeros(n + burn)
    e = rng.normal(0, sigma, n + burn)
    for t in range(2, n + burn):
        x[t] = phi1 * x[t - 1] + phi2 * x[t - 2] + e[t]
    x = x[burn:]
    rows = [[t + 1, rnd(v, 5)] for t, v in enumerate(x)]
    write("course-14b-timeseries/ar2-series.csv", ["t", "value"], rows,
          {"n": 300, "model": "AR(2)", "phi1": 0.6, "phi2": -0.3,
           "sigma": 1.0, "stationary": True,
           "expect": "ACF tails off, PACF cuts off after lag 2; a fitted "
                     "AR(2) recovers roughly (0.6, -0.3)"},
          ["stationarity", "ACF and PACF read together", "AR, MA and ARMA",
           "Yule-Walker and MLE estimation", "AIC and BIC",
           "the Ljung-Box test", "ADF and KPSS"],
          "Built from phi = (0.6, -0.3) after a 200-point burn-in. The PACF "
          "cutting off at lag 2 is how you would have identified the order "
          "without being told.")


def course_14b_seasonal():
    rng = np.random.default_rng(1403)
    rows = []
    for i in range(72):                       # six years of months
        year, month = 2020 + i // 12, i % 12 + 1
        level = 1000 + 8.0 * i
        season = 220 * math.sin(2 * math.pi * month / 12) \
            + 90 * math.cos(2 * math.pi * month / 6)
        rows.append([f"{year}-{month:02d}",
                     round(level + season + rng.normal(0, 35), 2)])
    write("course-14b-timeseries/seasonal-sales.csv", ["month", "sales"], rows,
          {"n": 72, "years": 6, "period": 12, "trend_per_month": 8.0,
           "base_level": 1000, "seasonal_amplitude": 220, "noise_sd": 35,
           "expect": "differencing at lag 12 removes the season; SARIMA "
                     "with s=12 fits; Holt-Winters recovers the trend"},
          ["decomposition, additive against multiplicative", "STL",
           "seasonal differencing", "SARIMA", "Holt-Winters",
           "forecast intervals"],
          "A linear trend of +8 a month under a 12-month season. Difference "
          "once at lag 12 and the season goes; difference again at lag 1 and "
          "the trend goes. Doing it in the wrong order is the classic error.")


def course_14b_var():
    rng = np.random.default_rng(1404)
    n, burn = 250, 100
    a = np.zeros(n + burn); b = np.zeros(n + burn); c = np.zeros(n + burn)
    for t in range(2, n + burn):
        a[t] = 0.5 * a[t - 1] + rng.normal(0, 1)
        # b depends on a's PAST -- so a Granger-causes b, and not the reverse
        b[t] = 0.3 * b[t - 1] + 0.6 * a[t - 1] + rng.normal(0, 1)
        c[t] = 0.4 * c[t - 1] + rng.normal(0, 1)
    rows = [[t + 1, rnd(a[burn + t], 5), rnd(b[burn + t], 5),
             rnd(c[burn + t], 5)] for t in range(n)]
    write("course-14b-timeseries/macro-indicators.csv",
          ["t", "rates", "inflation", "unrelated"], rows,
          {"n": 250,
           "rates_granger_causes_inflation": True,
           "inflation_granger_causes_rates": False,
           "unrelated_causes_nothing": True,
           "coefficients": {"rates_ar1": 0.5, "inflation_ar1": 0.3,
                            "rates_to_inflation": 0.6, "unrelated_ar1": 0.4}},
          ["VAR models", "Granger causality", "impulse response",
           "state-space form and the Kalman filter",
           "cointegration"],
          "Causality is planted in ONE direction: rates move inflation, "
          "inflation does not move rates. Test both ways -- a Granger test "
          "that fires in both directions has found correlation, not cause. "
          "The third column is a control that should fire in neither.")


# ---------------------------------------------------------------------------
# Course 15 A -- NLP
# ---------------------------------------------------------------------------

def course_15a_sentiment():
    rows = [
        ("The delivery was quick and the product works perfectly", 1),
        ("Excellent quality for the price, very happy", 1),
        ("Arrived broken and the seller ignored my messages", 0),
        ("Terrible experience, I want a refund", 0),
        ("Battery life is outstanding and it charges fast", 1),
        ("Stopped working after two days, complete waste", 0),
        ("Packaging was neat and delivery was on time", 1),
        ("The screen is dim and the buttons stick", 0),
        ("Good value, would buy again", 1),
        ("Not as described, the colour is wrong", 0),
        ("Setup was simple and the manual is clear", 1),
        ("Overpriced for what it does", 0),
        ("Sound quality is rich and the fit is comfortable", 1),
        ("It broke within a week of light use", 0),
        ("Fast shipping, well packed, exactly as pictured", 1),
        ("Customer service never replied to three emails", 0),
        ("Works well but the cable is too short", 1),
        ("Cheap plastic, feels like it will snap", 0),
        ("Better than the branded one I replaced", 1),
        ("Does not hold a charge at all", 0),
    ]
    write("course-15a-nlp/sentiment-reviews.csv", ["text", "label"], rows,
          {"rows": 20, "positive": 10, "negative": 10, "balanced": True,
           "labelled_by": "hand",
           "note": "'Works well but the cable is too short' is positive but "
                   "contains a negative clause -- bag-of-words will find it "
                   "hard, and that is the lesson"},
          ["tokenization", "stopword removal", "stemming and lemmatization",
           "bag of words and TF-IDF", "Naive Bayes and logistic regression "
           "for sentiment", "train/test split on text"],
          "Twenty reviews, balanced, labelled by hand so the accuracy you "
          "compute means something. One review is deliberately mixed.")


def course_15a_ner():
    rows = [
        ("Anitha Rao joined NRI Institute in Vijayawada last August",
         "Anitha Rao|PERSON; NRI Institute|ORG; Vijayawada|GPE; August|DATE"),
        ("Infosys opened an office in Hyderabad on 12 March 2025",
         "Infosys|ORG; Hyderabad|GPE; 12 March 2025|DATE"),
        ("The Krishna river flows past Vijayawada into Andhra Pradesh",
         "Krishna|LOC; Vijayawada|GPE; Andhra Pradesh|GPE"),
        ("Dr Menon will present at the Guntur conference in December",
         "Dr Menon|PERSON; Guntur|GPE; December|DATE"),
        ("Wipro reported revenue of 22000 crore for the quarter",
         "Wipro|ORG; 22000 crore|MONEY"),
    ]
    write("course-15a-nlp/ner-sentences.csv",
          ["sentence", "expected_entities"], rows,
          {"sentences": 5, "entity_types": ["PERSON", "ORG", "GPE", "LOC",
                                            "DATE", "MONEY"],
           "total_entities": 15,
           "known_difficulty": "off-the-shelf English models mislabel Indian "
                               "state and river names more often than city "
                               "names"},
          ["named entity recognition", "POS tagging", "chunking",
           "evaluating NER against gold labels",
           "precision and recall for extraction"],
          "The gold labels are in the second column, so you can SCORE the "
          "tagger rather than eyeball it. Expect the model to get the cities "
          "right and to struggle with 'Andhra Pradesh' and 'Krishna'.")


# ---------------------------------------------------------------------------
# Course 15 B -- MLOps: a reference batch and a drifted one
# ---------------------------------------------------------------------------

def course_15b_drift():
    rng = np.random.default_rng(1501)

    def batch(n, income_mu, score_mu, seed_tag):
        income = rng.normal(income_mu, 18000, n).clip(8000, None)
        score = rng.normal(score_mu, 90, n).clip(300, 850)
        debt = rng.uniform(0, 50000, n)
        z = -6.0 + 0.00005 * income - 0.00006 * debt + 0.008 * score
        y = (rng.uniform(0, 1, n) < 1 / (1 + np.exp(-z))).astype(int)
        return [[seed_tag, round(i), round(d), int(s), int(t)]
                for i, d, s, t in zip(income, debt, score, y)]

    ref = batch(400, 55000, 640, "reference")
    drift = batch(400, 55000 * 1.0, 585, "current")   # score shifts, income does not
    write("course-15b-mlops/loan-reference.csv",
          ["batch", "income", "debt", "credit_score", "approved"], ref,
          {"rows": 400, "credit_score_mean": 640, "income_mean": 55000,
           "role": "the distribution the model was trained on"},
          ["training a baseline", "MLflow experiment tracking",
           "model registry", "DVC data versioning"],
          "Train on this one and register it. It is the reference every "
          "later batch is compared against.")
    write("course-15b-mlops/loan-current.csv",
          ["batch", "income", "debt", "credit_score", "approved"], drift,
          {"rows": 400, "credit_score_mean": 585, "income_mean": 55000,
           "drifted_feature": "credit_score -- the mean falls by 55 points",
           "undrifted_features": ["income", "debt"],
           "expect": "PSI and a KS test flag credit_score and NOT income; "
                     "the relationship between features and label is "
                     "unchanged, so retraining gains very little"},
          ["population stability index", "the Kolmogorov-Smirnov test",
           "data drift against concept drift",
           "retraining triggers and the metric gate", "monitoring"],
          "ONE feature moved. Detect which, and resist retraining on "
          "reflex: the inputs shifted but the input-to-label relationship "
          "did not, so a retrain buys almost nothing. Knowing that is the "
          "Unit 5 answer.")

def course_02_records():
    """Fixed-width-friendly records for the C file-handling practicals."""
    rows = [(101, "Anitha Rao", 25000, 3, "Analytics"),
            (102, "Bharat Kumar", 32000, 5, "Engineering"),
            (103, "Chitra Devi", 18500, 1, "Support"),
            (104, "Daniel Joseph", 45000, 8, "Engineering"),
            (105, "Esha Nair", 28000, 4, "Analytics"),
            (106, "Faisal Ahmed", 52000, 10, "Management"),
            (107, "Geetha Menon", 30000, 2, "Engineering"),
            (108, "Harsha Reddy", 22000, 1, "Support"),
            (109, "Indira Rao", 38000, 6, "Analytics"),
            (110, "Jyothi Varma", 41000, 7, "Engineering")]
    write("course-2-c/employee-records.csv",
          ["emp_no", "name", "salary", "years", "department"], rows,
          {"rows": 10, "total_salary": sum(r[2] for r in rows),
           "highest_paid": "Faisal Ahmed",
           "longest_name_length": max(len(r[1]) for r in rows),
           "departments": 4,
           "note_for_c": "names contain a space, so scanf(\"%s\") stops "
                         "at the first one -- use fgets and strtok"},
          ["struct and array of structs", "fgets, sscanf, strtok",
           "fopen / fscanf / fprintf", "string functions (strlen, strcpy, "
           "strcmp)", "sorting an array of structs", "linear and binary "
           "search"],
          "Ten records for the file-handling and structure practicals. The "
          "names contain spaces on purpose: scanf(\"%s\") reads 'Anitha' "
          "and leaves 'Rao' in the buffer, which is the bug every student "
          "writes once.")


COURSE_NAMES = {
    "shared": "Used by several courses",
    "course-1-office": "Course 1 — Office Automation",
    "course-2-c": "Course 2 — Problem Solving Using C",
    "course-3-python": "Course 3 — Python Programming",
    "course-4-stats": "Course 4 — Statistical Foundations",
    "course-5-dbms": "Course 5 — Database Management Systems",
    "course-6-r": "Course 6 — Data Science with R",
    "course-7-web": "Course 7 — Web Technologies",
    "course-8-datamining": "Course 8 — Data Mining",
    "course-9-python-da": "Course 9 — Python for Data Analysis",
    "course-10-mongodb": "Course 10 — Document Oriented Database",
    "course-11-bi": "Course 11 — Business Intelligence Tools",
    "course-12a-ml": "Course 12 A — Machine Learning",
    "course-12b-bigdata": "Course 12 B — Big Data Technologies",
    "course-13a-ai": "Course 13 A — Artificial Intelligence",
    "course-13b-cloud": "Course 13 B — Cloud Computing",
    "course-14a-deeplearning": "Course 14 A — Deep Learning",
    "course-14b-timeseries": "Course 14 B — Time Series",
    "course-15a-nlp": "Course 15 A — Natural Language Processing",
    "course-15b-mlops": "Course 15 B — Data Engineering and MLOps",
}
ORDER = list(COURSE_NAMES)


def write_index():
    """data/README.md, generated from the same table the checker asserts.

    Written rather than maintained by hand, so the index cannot claim a
    dataset has a property that was never planted in it.
    """
    out = ["# Practice datasets",
           "",
           "One CSV per method, or close to it. Every file was **generated "
           "from a known truth** — the regression file from a slope of 6.0, "
           "the AR(2) series from phi = (0.6, −0.3), the three clusters from "
           "centres the generator chose — so you can **score your answer**, "
           "not merely produce one.",
           "",
           "`tools/check_datasets.py` reads every file back off disk and "
           "recovers its planted truth. A dataset whose right answer nobody "
           "has checked is worse than no dataset, because a wrong answer "
           "then looks like a lesson.",
           "",
           "```bash",
           "python3 tools/make_datasets.py    # regenerate (deterministic)",
           "python3 tools/check_datasets.py   # prove each truth is recoverable",
           "```",
           "",
           f"**{len(TRUTHS)} datasets.** Seeded, so regenerating gives "
           "byte-identical files; a diff after regenerating means something "
           "changed that should not have.",
           ""]
    for folder in ORDER:
        files = sorted(k for k in TRUTHS if k.split("/")[0] == folder)
        if not files:
            continue
        out += ["---", "", f"## {COURSE_NAMES[folder]}", ""]
        for rel in files:
            t = TRUTHS[rel]
            out += [f"### `data/{rel}`", "",
                    f"{t['rows']} rows · "
                    + " · ".join(f"`{c}`" for c in t["columns"]), "",
                    "**Practise:** " + "; ".join(t["methods"]) + ".", "",
                    t["note"], "",
                    "<details><summary>What it was built from</summary>", ""]
            for k, v in t["truth"].items():
                out.append(f"- `{k}` — {v}")
            out += ["", "</details>", ""]
    (DATA / "README.md").write_text("\n".join(out) + "\n")

def main():
    DATA.mkdir(exist_ok=True)
    made = [fn for name, fn in sorted(globals().items())
            if name.startswith(("shared_", "course_")) and callable(fn)]
    for fn in made:
        fn()
    write_index()
    print(f"\n  {len(TRUTHS)} datasets written under data/")
    for rel in sorted(TRUTHS):
        t = TRUTHS[rel]
        print(f"    {rel:<48} {t['rows']:>4} rows")


if __name__ == "__main__":
    main()
