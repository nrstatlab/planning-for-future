"""Shared sample data for the Course 1 spreadsheet experiments.

Course 1's lab is Word, PowerPoint and Excel, so most of it produces documents
rather than code. But eight of the fourteen experiments are ARITHMETIC, and
arithmetic can be checked. These tables are the data the notes work through,
defined once so that the notes, the experiments and each other cannot drift.

Deliberately small enough to check by hand -- six employees, twenty students,
nine sales rows. If you cannot reproduce a figure with a calculator, the
experiment has not taught you anything.

The sales table is the SAME nine rows Course 11 loads into Power BI and
Tableau. `tools/run_office_labs.py` asserts that they still match, so the
₹10,360 South total this course computes with a pivot table is the identical
figure Course 11 computes with DAX, Course 12 B with Hive and Spark, Course
13 B with a warehouse query and Course 15 B with an ETL job.
"""

# --- Experiments 7 and 10: the payroll sheet --------------------------------
# One sheet serves both. Experiment 7 computes the salary columns from Basic
# Pay; experiment 10 looks employees up in it four different ways.
#
# Columns, in this order, because every formula depends on the order:
#     A Name    B EmpID    C Department    D Basic Pay
EMPLOYEES = [
    ("Anitha Rao",    "E101", "Analytics",   25000),
    ("Bharat Kumar",  "E102", "Engineering", 32000),
    ("Chitra Devi",   "E103", "Support",     18500),
    ("Daniel Joseph", "E104", "Engineering", 45000),
    ("Esha Nair",     "E105", "Analytics",   28000),
    ("Faisal Ahmed",  "E106", "Management",  52000),
]
EMP_COLUMNS = ["Name", "EmpID", "Department", "Basic"]

# The allowance structure the syllabus specifies. Kept in named constants for
# the same reason the notes tell you to keep them in their own cells: changing
# the DA rate must be a one-place edit.
DA_RATE = 0.30          # of Basic
HRA_RATE = 0.15         # of Basic
DEDUCTION_RATE = 0.10   # of (Basic + DA)  <-- note: NOT of Basic alone


# --- Experiments 8 and 9: the class results sheet ---------------------------
# Twenty students, five subjects, marks out of 100.
#
#     A Roll   B Name   C..G the five subjects   H Total  I Average
#     J Result  K Grade
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computers"]
STUDENTS = [
    (1,  "Aarav",     92, 88, 95, 90, 96),
    (2,  "Bhavna",    78, 82, 75, 80, 85),
    (3,  "Chaitanya", 65, 70, 58, 72, 68),
    (4,  "Divya",     45, 52, 38, 60, 55),   # averages 50 but fails Chemistry
    (5,  "Eshan",     88, 91, 85, 79, 93),
    (6,  "Farhan",    55, 48, 62, 51, 58),
    (7,  "Gayatri",   96, 94, 98, 92, 90),
    (8,  "Harsha",    72, 68, 75, 70, 66),
    (9,  "Ishita",    38, 42, 45, 40, 39),   # averages 40.8 but fails two
    (10, "Jatin",     82, 78, 88, 75, 80),
    (11, "Kavya",     12, 20,  8, 15, 25),   # the only student failing all five
    (12, "Lakshmi",   60, 65, 55, 68, 62),
    (13, "Manoj",     90, 85, 92, 88, 94),   # 89.8 -- misses an A by 0.2
    (14, "Nithya",    48, 55, 50, 45, 52),
    (15, "Omkar",     75, 80, 72, 78, 74),
    (16, "Pallavi",   68, 62, 70, 65, 60),
    (17, "Rahul",     35, 55, 60, 58, 62),   # averages 54 but fails Maths
    (18, "Sneha",     98, 96, 99, 95, 97),
    (19, "Tarun",     58, 60, 52, 55, 57),
    (20, "Usha",      85, 88, 82, 90, 86),
]

PASS_MARK = 40
# Grade cut-offs, applied to the AVERAGE. Read as: score >= cut-off gets that
# letter, first match wins.
GRADE_BANDS = [(90, "A"), (75, "B"), (60, "C"), (40, "D")]
FAIL_GRADE = "F"


# --- Experiments 11 and 14: the sales table ---------------------------------
# Product, Region, Date, Quantity, Revenue -- exactly the five columns
# experiment 11 names. Revenue is Quantity x unit price, and the unit prices
# are Course 11's list prices.
UNIT_PRICE = {
    "Rice 5kg": 280,
    "Tea 500g": 210,
    "Shampoo 200ml": 140,
    "Notebook": 40,
}
SALES = [
    #  product          region   date          qty
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


def sales_rows():
    """The sales table with the Revenue column filled in."""
    return [(product, region, date, qty, qty * UNIT_PRICE[product])
            for product, region, date, qty in SALES]


# --- Experiment 13: the monthly budget --------------------------------------
INCOME = 45000
EXPENSES = {
    "Rent": 15000,
    "Food": 8000,
    "Transport": 3500,
    "Utilities": 2800,
    "Entertainment": 2200,
    "Miscellaneous": 1500,
}
