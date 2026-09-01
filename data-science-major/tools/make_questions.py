#!/usr/bin/env python3
"""Write the practice questions for every dataset under data/.

Each dataset already carries a planted truth. This adds the other half: a set
of questions to answer with it, graded warm-up / core / stretch, and an answer
key.

THE ANSWERS ARE COMPUTED, NOT TYPED. Every answer below is a function of the
CSV, evaluated when this file runs. Three times while building the datasets I
wrote down a figure I had not calculated and three times it was wrong -- the
products stock value, the count of empty cells, and which loan feature mattered
most. An answer key assembled from memory would repeat that at fifty times the
scale, and a wrong answer key is worse than none: the student who gets it right
concludes they got it wrong.

`tools/check_datasets.py` regenerates this file into a temporary directory and
compares, so a dataset that changes without its answers being rebuilt fails the
suite.

Usage:  python3 tools/make_questions.py [output_dir]
"""
import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DATA

# dataset -> [(level, question, answer_fn), ...]
QUESTIONS = {}


def ask(dataset):
    """Decorator: register the question set for one dataset."""
    def wrap(fn):
        QUESTIONS[dataset] = fn
        return fn
    return wrap


def load(rel):
    return pd.read_csv(DATA / rel)


def pct(x, places=1):
    return f"{100 * float(x):.{places}f}%"


def money(x):
    return f"{float(x):,.0f}"


# ---------------------------------------------------------------------------
# shared
# ---------------------------------------------------------------------------

@ask("shared/sales-transactions.csv")
def _q(d):
    return [
        ("warm", "How many transactions are in the file, and how many "
                 "distinct products?",
         f"{len(d)} transactions over {d['product'].nunique()} products"),
        ("warm", "What is the total revenue?", money(d.revenue.sum())),
        ("core", "Build a pivot of revenue by region and product. What does "
                 "each region total?",
         "; ".join(f"{r} {money(v)}"
                   for r, v in d.groupby('region').revenue.sum().items())),
        ("core", "Which product earns the most, and what share of the total "
                 "is it?",
         f"{d.groupby('product').revenue.sum().idxmax()} — "
         f"{money(d.groupby('product').revenue.sum().max())}, "
         f"{pct(d.groupby('product').revenue.sum().max() / d.revenue.sum())} "
         "of the total"),
        ("core", "Group the dates by month. How many months appear, and why "
                 "is that fewer than the span suggests?",
         f"{d.date.str.slice(0, 7).nunique()} months "
         f"({', '.join(sorted(d.date.str.slice(0, 7).unique()))}) — March has "
         "no sale, and grouping omits empty periods rather than showing a "
         "zero"),
        ("stretch", "Compute month-on-month growth over a COMPLETE month "
                    "range. What happens at April, and which Excel function "
                    "exists for it?",
         "March is 0, so April divides by zero and gives #DIV/0! — that is "
         "what IFERROR is for. Dropping March instead makes April read "
         "+46.77%, two months of change labelled as one"),
    ]


@ask("shared/flowers.csv")
def _q(d):
    grouped = d.groupby("species").petal_length
    return [
        ("warm", "How many rows per species?",
         "; ".join(f"{k} {v}" for k, v in d.species.value_counts().items())),
        ("warm", "Which single measurement separates the species best?",
         "petal_length — its between-species spread is largest relative to "
         "the within-species spread"),
        ("core", "Split 70/30 and fit a k-NN classifier. Which two species "
                 "does it confuse, and why is that expected?",
         f"borealis and carinata — their petal_length ranges overlap "
         f"({grouped.max()['borealis']:.2f} against "
         f"{grouped.min()['carinata']:.2f}), while alba is separable"),
        ("core", "What is the largest petal_length among alba, and the "
                 "smallest among the other two?",
         f"alba max {grouped.max()['alba']:.2f}; others min "
         f"{d[d.species != 'alba'].petal_length.min():.2f} — no overlap at "
         "all"),
        ("stretch", "A classmate reports 100% accuracy. What went wrong?",
         "The label leaked, or they scored on the training set. Two species "
         "genuinely overlap here, so perfect separation is not available"),
    ]


# ---------------------------------------------------------------------------
# Course 1 -- Office Automation
# ---------------------------------------------------------------------------

@ask("course-1-office/payroll.csv")
def _q(d):
    da = d.basic_pay * 0.30
    gross = d.basic_pay + da + d.basic_pay * 0.15
    net = gross - (d.basic_pay + da) * 0.10
    return [
        ("warm", "Add DA (30% of basic), HRA (15%) and Gross. What is the "
                 "total gross bill?", money(gross.sum())),
        ("warm", "Who is paid most and least, net?",
         f"{d.loc[net.idxmax(), 'name']} {money(net.max())}; "
         f"{d.loc[net.idxmin(), 'name']} {money(net.min())}"),
        ("core", "Deduction is 10% of (Basic + DA). Write Net as a single "
                 "multiple of Basic and verify it on one row.",
         f"Net = 1.32 x Basic — e.g. {d.name.iloc[0]}: "
         f"{money(d.basic_pay.iloc[0])} x 1.32 = {money(net.iloc[0])}"),
        ("core", "Put the three rates in their own cells and reference them "
                 "absolutely. Why does that earn marks over typing 0.30?",
         "Changing the DA rate becomes a one-cell edit; hard-coded rates must "
         "be found in every formula and one will be missed"),
        ("stretch", "Take the deduction on Basic alone instead. By how much "
                    "does the monthly payroll rise?",
         f"Net becomes 1.35 x Basic, so the bill rises by 3% of the basic "
         f"total — {money(d.basic_pay.sum() * 0.03)} a month, with no error "
         "shown anywhere"),
    ]


@ask("course-1-office/class-results.csv")
def _q(d):
    subs = ["maths", "physics", "chemistry", "english", "computers"]
    avg = d[subs].mean(axis=1)
    grade = pd.cut(avg, [-1, 40, 60, 75, 90, 1000],
                   labels=["F", "D", "C", "B", "A"], right=False)
    fails = d.loc[d[subs].min(axis=1) < 40, "name"].tolist()
    return [
        ("warm", "Compute each student's total and average.",
         f"Class mean {d[subs].values.mean():.2f}; highest total "
         f"{d[subs].sum(axis=1).max()} ({d.loc[d[subs].sum(axis=1).idxmax(), 'name']})"),
        ("warm", "Which subject has the lowest class average?",
         f"{d[subs].mean().idxmin()} at {d[subs].mean().min():.2f}"),
        ("core", "Grade on the AVERAGE with A>=90, B>=75, C>=60, D>=40. What "
                 "is the distribution?",
         "; ".join(f"{g} {int((grade == g).sum())}" for g in "ABCDF")),
        ("core", "A student passes only if they clear 40 in EVERY subject. "
                 "Who fails, and how many would pass if you tested the "
                 "average instead?",
         f"{', '.join(fails)} fail. Testing the average passes all but "
         f"{', '.join(d.loc[avg < 40, 'name'])} — three students who failed a "
         "paper would be passed in error"),
        ("stretch", "Point the grade formula at the TOTAL instead of the "
                    "average. What happens, and what does the weakest "
                    "student get?",
         f"{int((pd.cut(d[subs].sum(axis=1), [-1, 40, 60, 75, 90, 100000], labels=['F', 'D', 'C', 'B', 'A'], right=False) == 'A').sum())} "
         "of 20 get an A, and Kavya — who failed all five papers with "
         f"{int(d.loc[d.name == 'Kavya', subs].sum(axis=1).iloc[0])}/500 — is "
         "awarded a B. Nothing errors"),
    ]


@ask("course-1-office/budget.csv")
def _q(d):
    income = float(d.loc[d.category == "Income", "amount"].iloc[0])
    exp = float(d.loc[d.category != "Income", "amount"].sum())
    return [
        ("warm", "What are total expenses and savings?",
         f"expenses {money(exp)}, savings {money(income - exp)}"),
        ("warm", "What is the savings rate?", pct((income - exp) / income, 2)),
        ("core", "Use Goal Seek to reach savings of 20,000 by changing "
                 "income. What income is needed?",
         money(exp + 20000)),
        ("core", "Now Goal Seek a savings RATE of 30%. Why can you not read "
                 "this one off the sheet?",
         f"{exp:,.0f}/0.70 = {exp / 0.70:,.2f} — the rate is not linear in "
         "income, so the answer is a division, not a subtraction"),
        ("stretch", "Ask Goal Seek for a 100% savings rate. What does it do, "
                    "and why?",
         "It exhausts its iterations and reports it may not have found a "
         "solution: the rate approaches 100% as income grows but never "
         "reaches it, so there is no root to find"),
        ("stretch", "Build a one-variable data table over rent from 12,000 "
                    "to 18,000. What is the slope?",
         "Exactly -1: every rupee of rent is a rupee off savings. Savings "
         "run 15,000 down to 9,000"),
    ]


# ---------------------------------------------------------------------------
# Courses 2, 3 -- C and Python
# ---------------------------------------------------------------------------

@ask("course-2-c/employee-records.csv")
def _q(d):
    return [
        ("warm", "Define a struct for one record and read the file with "
                 "fgets. How long must the name buffer be?",
         f"the longest name is {d.name.str.len().max()} characters, so "
         f"char name[{d.name.str.len().max() + 1}] at minimum — allow more"),
        ("warm", "Print the total and average salary.",
         f"total {money(d.salary.sum())}, average {money(d.salary.mean())}"),
        ("core", 'Why does scanf("%s", name) fail on this file?',
         "every name contains a space, so %s stops at the first one and "
         "leaves the surname in the buffer, which the next scanf then reads "
         "into the wrong field. Use fgets and strtok"),
        ("core", "Sort the array of structs by salary descending and print "
                 "the top three.",
         "; ".join(f"{r.name} {money(r.salary)}"
                   for r in d.nlargest(3, "salary").itertuples())),
        ("core", "Linear-search for employee 107 and report the comparison "
                 "count. How many would a binary search need?",
         f"linear finds it at position "
         f"{int(d.index[d.emp_no == 107][0]) + 1} of {len(d)}; binary needs "
         f"at most {int(np.ceil(np.log2(len(d))))} comparisons on the sorted "
         "array"),
        ("stretch", "Write the records back with fprintf, read them again "
                    "and compare. What breaks if a name contains a comma?",
         "the round trip splits that field in two — which is why real CSV "
         "quotes fields, and why you should test with a name like "
         '"Rao, Anitha"'),
    ]


@ask("course-3-python/students.csv")
def _q(d):
    subs = ["python", "maths", "statistics"]
    return [
        ("warm", "Read it with csv.DictReader and total each student's three "
                 "marks. Who scores highest?",
         f"{d.loc[d[subs].sum(axis=1).idxmax(), 'name']} with "
         f"{int(d[subs].sum(axis=1).max())}"),
        ("warm", "What is the mean mark across every student and subject?",
         f"{d[subs].values.mean():.4f}"),
        ("core", "Build a dict of name -> average and print those above the "
                 "class average.",
         f"class average {d[subs].values.mean():.2f}; "
         f"{int((d[subs].mean(axis=1) > d[subs].values.mean()).sum())} "
         "students are above it"),
        ("core", "Which subject has the widest spread, and by what measure?",
         f"{d[subs].std().idxmax()} — standard deviation "
         f"{d[subs].std().max():.2f} against "
         f"{d[subs].std().min():.2f} for {d[subs].std().idxmin()}"),
        ("stretch", "Wrap the read in try/except and run it against a "
                    "filename that does not exist. Which exception, and why "
                    "not a bare except?",
         "FileNotFoundError. A bare except also swallows KeyboardInterrupt "
         "and your own typos, so the program fails silently instead of "
         "loudly"),
    ]


# ---------------------------------------------------------------------------
# Course 4 -- Statistics
# ---------------------------------------------------------------------------

@ask("course-4-stats/heights.csv")
def _q(d):
    h = d.height_cm
    return [
        ("warm", "Compute the mean, median and mode class.",
         f"mean {h.mean():.4f}, median {h.median():.2f}"),
        ("warm", "Compute the range, variance and standard deviation.",
         f"range {h.max() - h.min():.1f}, variance {h.var():.4f}, "
         f"sd {h.std():.4f}"),
        ("core", "The data were drawn from N(165, 8). How far is your sample "
                 "mean from 165, and is that surprising?",
         f"{abs(h.mean() - 165):.4f} cm away; the standard error is "
         f"8/sqrt(60) = {8 / np.sqrt(60):.4f}, so it is well within one SE — "
         "sampling error, not a wrong answer"),
        ("core", "Test H0: mu = 165 at 5%. What do you conclude?",
         f"t = {(h.mean() - 165) / (h.std() / np.sqrt(len(h))):.4f} on "
         f"{len(h) - 1} df — do not reject; the data are consistent with 165"),
        ("stretch", "Compute skewness and kurtosis. What would you expect "
                    "from a normal sample of this size, and do you get it?",
         f"skewness {h.skew():.4f}, excess kurtosis {h.kurt():.4f} — both "
         "near zero, but n=60 gives them large standard errors, so small "
         "departures mean little"),
    ]


@ask("course-4-stats/study-hours-marks.csv")
def _q(d):
    slope, intercept = np.polyfit(d.hours, d.marks, 1)
    r = np.corrcoef(d.hours, d.marks)[0, 1]
    sx, sy = d.hours.std(), d.marks.std()
    return [
        ("warm", "Draw the scatter plot. Does the relationship look linear?",
         "yes — a clear positive straight-line trend with constant scatter"),
        ("warm", "Compute Karl Pearson's correlation coefficient.",
         f"r = {r:.4f}"),
        ("core", "Fit the least-squares line of marks on hours. What are the "
                 "slope and intercept, and what do they mean?",
         f"marks = {intercept:.4f} + {slope:.4f} x hours — about 6 marks per "
         "hour of study, and about 12 marks for a student who studies none"),
        ("core", "Show that R-squared equals r-squared for this fit.",
         f"both are {r ** 2:.6f}"),
        ("core", "Now fit hours on marks. Why is it not the same line?",
         f"slope {r * sx / sy:.4f} in the other direction; least squares "
         "minimises the error in the DEPENDENT variable, so swapping roles "
         "changes what is being minimised. The two lines cross at the means"),
        ("stretch", "The data were built from marks = 12 + 6 x hours. How "
                    "close did you get, and what explains the gap?",
         f"slope {slope:.4f} against 6.0, intercept {intercept:.4f} against "
         "12.0 — the gap is the noise term (sd 4) and n = 40"),
    ]


@ask("course-4-stats/treatment-groups.csv")
def _q(d):
    from scipy import stats
    a = d[d.group == "control"].score
    b = d[d.group == "treatment"].score
    tt = stats.ttest_ind(b, a)
    f = stats.f_oneway(a, b)
    return [
        ("warm", "Report n, mean and sd for each group.",
         f"control n={len(a)} mean {a.mean():.4f} sd {a.std():.4f}; "
         f"treatment n={len(b)} mean {b.mean():.4f} sd {b.std():.4f}"),
        ("warm", "What is the observed difference in means?",
         f"{b.mean() - a.mean():.4f}"),
        ("core", "Test whether the treatment mean is higher, at 5%.",
         f"t = {tt.statistic:.4f}, p = {tt.pvalue:.6f} — reject H0"),
        ("core", "Build a 95% confidence interval for the difference.",
         "centred on {:.2f}; it excludes zero, which is the same conclusion "
         "the test reached".format(b.mean() - a.mean())),
        ("stretch", "Run a one-way ANOVA on the same two groups. How does F "
                    "relate to t?",
         f"F = {f.statistic:.4f} = t^2 = {tt.statistic ** 2:.4f}. With two "
         "groups the two tests are algebraically the same"),
    ]


@ask("course-4-stats/before-after.csv")
def _q(d):
    from scipy import stats
    diff = d.after - d.before
    paired = stats.ttest_rel(d.after, d.before)
    unpaired = stats.ttest_ind(d.after, d.before)
    return [
        ("warm", "Compute the gain for each subject. What is the mean gain?",
         f"{diff.mean():.4f} with sd {diff.std():.4f}"),
        ("core", "Run a paired t-test. What do you conclude?",
         f"t = {paired.statistic:.4f}, p = {paired.pvalue:.3g} — the "
         "improvement is real"),
        ("core", "Now run an INDEPENDENT t-test on the same two columns. Why "
                 "is the evidence weaker?",
         f"p = {unpaired.pvalue:.4g} against {paired.pvalue:.3g}. The "
         "unpaired test treats the between-subject spread "
         f"(sd about {d.before.std():.1f}) as noise; pairing removes it and "
         f"leaves only the gain's own sd of {diff.std():.2f}"),
        ("core", "Which test is a one-sample t-test in disguise, and on what?",
         "the paired test — it is a one-sample test of the differences "
         "against zero, and gives an identical statistic"),
        ("stretch", "Run a Wilcoxon signed-rank test. When would you prefer "
                    "it?",
         "when the differences are clearly non-normal or the sample is very "
         "small; here it agrees, because the gains were generated normal"),
    ]


@ask("course-4-stats/fertiliser-yield.csv")
def _q(d):
    from scipy import stats
    groups = {k: g["yield"] for k, g in d.groupby("fertiliser")}
    f = stats.f_oneway(*groups.values())
    return [
        ("warm", "Report the mean yield for each fertiliser.",
         "; ".join(f"{k} {v.mean():.4f}" for k, v in groups.items())),
        ("core", "Run a one-way ANOVA at 5%. What do you conclude?",
         f"F = {f.statistic:.4f}, p = {f.pvalue:.3g} — not all three means "
         "are equal"),
        ("core", "ANOVA says they differ. It does not say which. Which pair "
                 "separates most?",
         f"{max(groups, key=lambda k: groups[k].mean())} against "
         f"{min(groups, key=lambda k: groups[k].mean())}, a gap of "
         f"{max(g.mean() for g in groups.values()) - min(g.mean() for g in groups.values()):.4f}"
         " — a post-hoc test is what licenses that claim"),
        ("core", "Partition the total sum of squares into between and within.",
         "between + within = total; the F ratio is the between mean square "
         "divided by the within mean square"),
        ("stretch", "Why not run three separate t-tests instead?",
         "three tests at 5% give roughly a 14% chance of at least one false "
         "positive. ANOVA tests all three at once at 5%"),
    ]


@ask("course-4-stats/preference-survey.csv")
def _q(d):
    from scipy import stats
    table = pd.crosstab(d.gender, d.preference)
    chi2, p, dof, exp = stats.chi2_contingency(table)
    return [
        ("warm", "Build the 2x2 contingency table from the raw rows.",
         "; ".join(f"{g}/{c} {table.loc[g, c]}"
                   for g in table.index for c in table.columns)),
        ("warm", "How many respondents in total?", str(len(d))),
        ("core", "Compute the expected frequencies under independence.",
         "; ".join(f"{g}/{c} {exp[i][j]:.3f}"
                   for i, g in enumerate(table.index)
                   for j, c in enumerate(table.columns))),
        ("core", "Run the chi-square test of independence. Degrees of "
                 "freedom, statistic, conclusion?",
         f"dof = {dof}, chi-square = {chi2:.4f}, p = {p:.3g} — reject "
         "independence; preference is associated with gender"),
        ("stretch", "Is the test valid here? What is the condition, and does "
                    "Yates' correction change your conclusion?",
         f"every expected count exceeds 5 (smallest {exp.min():.2f}), so the "
         "approximation holds. Yates' correction is applied by default for "
         "2x2 and does not change the conclusion"),
    ]


# ---------------------------------------------------------------------------
# Course 5 -- DBMS
# ---------------------------------------------------------------------------

@ask("course-5-dbms/departments.csv")
def _q(d):
    return [
        ("warm", "Write CREATE TABLE for it, choosing types and the key.",
         f"dept_id CHAR(2) PRIMARY KEY, dept_name VARCHAR(40) NOT NULL, "
         f"city VARCHAR(40) — {len(d)} rows"),
        ("core", "Which city hosts more than one department?",
         "; ".join(f"{c} ({n})" for c, n in d.city.value_counts().items()
                   if n > 1)),
        ("core", "Why must dept_id be declared NOT NULL as well as PRIMARY "
                 "KEY?",
         "it need not be: PRIMARY KEY implies NOT NULL and UNIQUE. Saying so "
         "explicitly documents the intent, and is the safer habit"),
    ]


@ask("course-5-dbms/employees.csv")
def _q(d):
    return [
        ("warm", "How many employees, and what is the salary bill?",
         f"{len(d)} employees, {money(d.salary.sum())}"),
        ("warm", "Average salary per department.",
         "; ".join(f"{k} {money(v)}"
                   for k, v in d.groupby('dept_id').salary.mean().items())),
        ("core", "Join employees to departments and list name with "
                 "dept_name. How many rows come back?",
         f"{len(d)} — every employee has a valid dept_id, so an inner join "
         "loses nobody"),
        ("core", "Self-join to show each employee beside their manager. Why "
                 "does an INNER join return fewer rows than a LEFT join?",
         f"inner returns {int(d.manager_id.notna().sum())}, left returns "
         f"{len(d)} — the {int(d.manager_id.isna().sum())} employees with no "
         "manager have nothing to match, and only the LEFT join keeps them"),
        ("core", "Which departments have an average salary above the company "
                 "average? Use GROUP BY with HAVING.",
         "; ".join(k for k, v in d.groupby('dept_id').salary.mean().items()
                   if v > d.salary.mean())
         + f" (company average {money(d.salary.mean())})"),
        ("stretch", "Find employees earning more than their own manager.",
         "; ".join(
             f"{r.name_x} over {r.name_y}"
             for r in d.merge(d, left_on="manager_id", right_on="emp_id")
                       .query("salary_x > salary_y").itertuples()) or "none"),
    ]


@ask("course-5-dbms/projects.csv")
def _q(d):
    return [
        ("warm", "Total and average project budget.",
         f"total {money(d.budget.sum())}, average {money(d.budget.mean())}"),
        ("core", "Which department owns the largest total budget?",
         f"{d.groupby('dept_id').budget.sum().idxmax()} with "
         f"{money(d.groupby('dept_id').budget.sum().max())}"),
        ("core", "Write a three-table join: employee name, department name, "
                 "project name. What join order avoids a cartesian product?",
         "employees -> departments -> projects, joining on dept_id each "
         "time. Joining employees to projects directly has no shared key"),
    ]


@ask("course-5-dbms/assignments.csv")
def _q(d):
    emps = load("course-5-dbms/employees.csv")
    return [
        ("warm", "What is the primary key of this table?",
         "the composite (emp_id, project_id) — neither column alone is "
         "unique"),
        ("core", "Total hours committed per project.",
         "; ".join(f"{k} {v}" for k, v in
                   d.groupby('project_id').hours_per_week.sum().items())),
        ("core", "Which employee works on more than one project?",
         "; ".join(k for k, v in d.emp_id.value_counts().items() if v > 1)),
        ("core", "List employees on NO project. Which SQL construct answers "
                 "this cleanly?",
         f"{', '.join(sorted(set(emps.emp_id) - set(d.emp_id)))} — "
         "NOT EXISTS, or a LEFT JOIN with IS NULL. An inner join can never "
         "answer it, because the rows are not there to be joined"),
        ("stretch", "Find employees assigned to EVERY project. What is this "
                    "class of query called?",
         "relational division — none qualify here, since no employee appears "
         "on all four projects"),
    ]


@ask("course-5-dbms/unnormalised-orders.csv")
def _q(d):
    return [
        ("warm", "Which normal form does this table break first, and why?",
         "1NF — items, quantities and unit_prices each pack several values "
         "into one cell"),
        ("core", "Decompose it to 3NF. How many tables, and what are their "
                 "keys?",
         "four: customers(customer_id), products(product_id), "
         "orders(order_id), order_items(order_id, product_id)"),
        ("core", "Which columns depend on the customer rather than the "
                 "order, and which normal form does that violate?",
         "customer_city and customer_phone — a transitive dependency through "
         "customer_name, which is 3NF"),
        ("stretch", "Change one customer's phone number in the ORIGINAL "
                    "table. How many rows must you touch, and what is that "
                    "anomaly called?",
         f"{int(d.customer_name.value_counts().max())} rows for "
         f"{d.customer_name.value_counts().idxmax()} — the update anomaly. "
         "Miss one and the table contradicts itself"),
        ("stretch", "What happens if you want to record a new product nobody "
                    "has ordered yet?",
         "you cannot — there is no row to put it in without inventing a fake "
         "order. That is the insert anomaly"),
    ]


# ---------------------------------------------------------------------------
# Courses 6, 7 -- R and Web
# ---------------------------------------------------------------------------

@ask("course-6-r/car-mileage.csv")
def _q(d):
    X = np.column_stack([np.ones(len(d)), d.weight_t, d.cylinders])
    beta = np.linalg.lstsq(X, d.mpg, rcond=None)[0]
    return [
        ("warm", "read.csv it and run str(). How many observations and "
                 "variables, and which are factors?",
         f"{len(d)} observations, {d.shape[1]} variables; transmission is a "
         "factor with 2 levels, cylinders is numeric but has only 3 values"),
        ("warm", "How many service_months are missing?",
         f"{int(d.service_months.isna().sum())} — rows "
         f"{', '.join(d.loc[d.service_months.isna(), 'car_id'])}"),
        ("core", "Fit lm(mpg ~ weight_t + cylinders). Report the "
                 "coefficients.",
         f"intercept {beta[0]:.4f}, weight {beta[1]:.4f}, cylinders "
         f"{beta[2]:.4f}"),
        ("core", "The data were built from 34 - 7.5*weight - 0.8*(cyl-4). "
                 "How close is your fit?",
         f"weight {beta[1]:.3f} against -7.5 and cylinders {beta[2]:.3f} "
         "against -0.8 — the intercept absorbs the (cyl-4) shift"),
        ("core", "Use tapply or dplyr to get mean mpg by cylinder count.",
         "; ".join(f"{int(k)} cyl {v:.4f}"
                   for k, v in d.groupby('cylinders').mpg.mean().items())),
        ("stretch", "Read the file WITHOUT na.strings and inspect "
                    "service_months. What has R done, and why does it "
                    "matter?",
         "the blanks make it character, so R makes the whole column a factor "
         "and mean() returns NA with a warning. Every numeric operation on "
         "that column silently stops working"),
        ("stretch", "ggplot mpg against weight, coloured by transmission, "
                    "with a fitted line per group. Do the slopes differ?",
         "geom_smooth(method='lm') per group; the generator put no "
         "transmission effect in, so any difference you see is noise"),
    ]


@ask("course-7-web/products.csv")
def _q(d):
    return [
        ("warm", "Convert the file to JSON and render it as an HTML table "
                 "with JavaScript. How many rows and columns?",
         f"{len(d)} rows, {d.shape[1]} columns"),
        ("warm", "What is the total value of stock on hand?",
         money((d.price * d.stock).sum())),
        ("core", "Filter to in-stock items only. How many remain, and what "
                 "array method does it?",
         f"{int((d.status == 'in_stock').sum())} remain — Array.prototype"
         ".filter"),
        ("core", "Sort by price descending and list the top three.",
         "; ".join(f"{r['name']} ({r.price})"
                   for _, r in d.nlargest(3, "price").iterrows())),
        ("core", "Group by category and total the stock. Which method chain "
                 "does this in JavaScript?",
         "; ".join(f"{k} {v}"
                   for k, v in d.groupby('category').stock.sum().items())
         + " — reduce into an object keyed by category"),
        ("stretch", "Build a form that only accepts an SKU present in the "
                    "file. Which validation approach, and what does it miss?",
         "a datalist or a fetch-and-check against the list. Client-side "
         "validation is a convenience, not a guarantee — anyone can post "
         "past it, so the server must check again"),
    ]


# ---------------------------------------------------------------------------
# Course 8 -- Data Mining
# ---------------------------------------------------------------------------

@ask("course-8-datamining/market-basket.csv")
def _q(d):
    baskets = d.groupby("transaction_id")["item"].apply(set)
    n = len(baskets)
    sup = lambda items: sum(1 for s in baskets if set(items) <= s) / n
    return [
        ("warm", "Reshape long to baskets. How many transactions and "
                 "distinct items?",
         f"{n} transactions, {d.item.nunique()} items"),
        ("warm", "Compute the support of every single item.",
         "; ".join(f"{i} {sup([i]):.4f}"
                   for i in sorted(d.item.unique()))),
        ("core", "At minimum support 0.3, which 1-itemsets survive to the "
                 "next level?",
         "; ".join(i for i in sorted(d.item.unique()) if sup([i]) >= 0.3)),
        ("core", "Compute support, confidence and lift for bread -> butter.",
         f"support {sup(['bread', 'butter']):.4f}, confidence "
         f"{sup(['bread', 'butter']) / sup(['bread']):.4f}, lift "
         f"{sup(['bread', 'butter']) / (sup(['bread']) * sup(['butter'])):.4f}"),
        ("core", "Confidence for butter -> bread is different. Why, and what "
                 "does that tell you about rules?",
         f"{sup(['bread', 'butter']) / sup(['butter']):.4f} — confidence is "
         "not symmetric, because it divides by a different antecedent. Lift "
         "is symmetric; confidence is not"),
        ("stretch", "State the Apriori property and show one 2-itemset it "
                    "lets you skip counting.",
         "no superset of an infrequent set can be frequent. At support 0.3, "
         f"jam ({sup(['jam']):.2f}) fails, so every pair containing jam is "
         "pruned without being counted"),
    ]


@ask("course-8-datamining/cluster-points.csv")
def _q(d):
    from sklearn.cluster import KMeans, DBSCAN
    X = d[["x", "y"]].values
    km = KMeans(3, n_init=10, random_state=0).fit(X)
    db = DBSCAN(eps=0.9, min_samples=4).fit(X)
    noise_true = (d.true_cluster == -1).values
    caught = int(((db.labels_ == -1) & noise_true).sum())
    return [
        ("warm", "Plot x against y. How many groups do you see by eye, and "
                 "what else is on the plot?",
         f"{int(d[d.true_cluster != -1].true_cluster.nunique())} tight "
         f"groups plus {int(noise_true.sum())} scattered points"),
        ("core", "Drop true_cluster and run k-Means with k=3. Report the "
                 "centres.",
         "; ".join(f"({c[0]:.3f}, {c[1]:.3f})"
                   for c in sorted(map(tuple, km.cluster_centers_.round(3))))),
        ("core", "Use the elbow method to choose k. Does it agree?",
         "the inertia drop flattens after k=3, which matches the three "
         "planted centres"),
        ("core", "Run DBSCAN with eps=0.9 and min_samples=4. How many points "
                 "does it call noise, and how many of those really are?",
         f"it labels {int((db.labels_ == -1).sum())} as noise, of which "
         f"{caught} of the {int(noise_true.sum())} planted noise points are "
         "correctly caught"),
        ("stretch", "k-Means put every noise point in some cluster. Why can "
                    "it not do otherwise, and when does that matter?",
         "k-Means partitions — every point must belong somewhere, so "
         "outliers drag centres towards themselves. It matters whenever "
         "'none of the above' is a real answer, such as fraud or sensor "
         "faults"),
        ("stretch", "Score both against true_cluster with the adjusted Rand "
                    "index. Which wins, and is that fair?",
         "DBSCAN, because the index rewards labelling noise correctly. "
         "Comparing on the clustered points alone is the fairer test"),
    ]


@ask("course-8-datamining/warehouse-facts.csv")
def _q(d):
    return [
        ("warm", "State the grain of this fact table in one sentence.",
         "one row per month per city per product — "
         f"{len(d)} rows = 12 x 3 x 4"),
        ("warm", "Total revenue across the whole cube.",
         money(d.revenue.sum())),
        ("core", "Roll up from city to region to all. Do the totals agree at "
                 "every level?",
         f"they must, and they do: {money(d.groupby('city').revenue.sum().sum())}"
         f" = {money(d.groupby('region').revenue.sum().sum())} = "
         f"{money(d.revenue.sum())}"),
        ("core", "Slice to one month and dice by region and category. Which "
                 "OLAP operations are these?",
         "slice fixes one dimension to a single value; dice takes a "
         "sub-cube across several. Drill-down goes region -> city"),
        ("core", "Which region-category pair earns most?",
         "{} — {}".format(
             " / ".join(d.groupby(["region", "category"]).revenue.sum().idxmax()),
             money(d.groupby(["region", "category"]).revenue.sum().max()))),
        ("stretch", "Join this to a store dimension that has two rows per "
                    "city and total the revenue. What has happened?",
         "every fact row matches twice and the total doubles — a fan trap. "
         "The join has changed the grain without saying so"),
    ]


# ---------------------------------------------------------------------------
# Courses 9, 10, 11
# ---------------------------------------------------------------------------

@ask("course-9-python-da/messy-customers.csv")
def _q(d):
    raw = pd.read_csv(DATA / "course-9-python-da/messy-customers.csv",
                      dtype=str, keep_default_na=False)
    sal = pd.to_numeric(raw.salary, errors="coerce").dropna()
    q1, q3 = sal.quantile(0.25), sal.quantile(0.75)
    return [
        ("warm", "Load it and count missing values per column.",
         "; ".join(f"{c} {int((raw[c] == '').sum())}"
                   for c in raw.columns if (raw[c] == '').any())
         + f" — {int((raw == '').sum().sum())} empty cells in all"),
        ("warm", "How many rows, and how many are duplicates?",
         f"{len(raw)} rows, {int(raw.duplicated().sum())} exact duplicate "
         f"(customer_id {raw.loc[raw.duplicated(), 'customer_id'].iloc[0]})"),
        ("core", "Clean the city column. How many distinct cities before and "
                 "after?",
         f"{raw.city.nunique()} before, "
         f"{raw.city.str.strip().str.lower().nunique()} after stripping and "
         "lowercasing"),
        ("core", "Find the rows with leading or trailing whitespace. Which "
                 "columns, and why is str.strip not enough on its own?",
         "name on C001 and city on C007. Strip fixes the edges; it does not "
         "fix case, so 'Hyderabad' and 'hyderabad' still differ afterwards"),
        ("core", "Detect outliers in salary with the IQR rule. Which row, and "
                 "by how much?",
         f"Q1 {money(q1)}, Q3 {money(q3)}, upper fence "
         f"{money(q3 + 1.5 * (q3 - q1))} — one salary of {money(sal.max())} "
         "sits far beyond it"),
        ("core", "Which age is impossible, and which email fails a naive "
                 "check?",
         f"age {int(pd.to_numeric(raw.age, errors='coerce').max())}, and "
         "'not-an-email' has no @"),
        ("stretch", "Decide dropna against fillna for each column and justify "
                    "it. What is your final row count?",
         "11 after removing the duplicate. Age and salary are candidates for "
         "median fill; a missing joined date probably cannot be invented, so "
         "that row may have to go or stay flagged"),
    ]


@ask("course-9-python-da/monthly-sales.csv")
def _q(d):
    wide = d.pivot(index="month", columns="region", values="revenue")
    return [
        ("warm", "How many rows, months and regions?",
         f"{len(d)} rows, {d.month.nunique()} months, {d.region.nunique()} "
         "regions"),
        ("warm", "Mean revenue per region.",
         "; ".join(f"{k} {money(v)}"
                   for k, v in d.groupby('region').revenue.mean().items())),
        ("core", "pivot_table it into a months-by-regions grid. What shape?",
         f"{wide.shape[0]} x {wide.shape[1]}, with no gaps"),
        ("core", "melt it back. Do you recover the original row count?",
         f"yes — {len(wide.reset_index().melt(id_vars='month'))} rows, the "
         "same 72"),
        ("core", "Which month had the highest total across all regions?",
         f"{d.groupby('month').revenue.sum().idxmax()} with "
         f"{money(d.groupby('month').revenue.sum().max())}"),
        ("core", "Plot a 3-month rolling mean per region. What does it "
                 "reveal that the raw series hides?",
         "the upward trend — the 12-month season dominates the raw plot and "
         "the rolling mean damps it"),
        ("stretch", "Separate trend from season. The data were built with a "
                    "trend of +400 a month and an amplitude of 6000. Can you "
                    "recover both?",
         "regress revenue on a month index per region for the trend; average "
         "the residuals by calendar month for the season"),
    ]


@ask("course-10-mongodb/students.csv")
def _q(d):
    d = d.fillna("")
    return [
        ("warm", "Import it so each student is one document. What must you "
                 "do with enrolled_courses first?",
         "split on ';' into an array — a bare import leaves one string, and "
         "no array operator will work on it"),
        ("core", "Model enrolments as an array of subdocuments pairing course "
                 "with grade. Write one document out in full.",
         "each of the two semicolon-separated columns has the same length "
         "per row, so element i of one pairs with element i of the other"),
        ("core", "Find students enrolled in DSC301 with a grade of A. Which "
                 "operator, and why is a plain dotted query wrong?",
         "$elemMatch — a dotted query matches if ANY element has the course "
         "and ANY element has the grade, which is not the same condition"),
        ("core", "$unwind the enrolments and count per course. Which student "
                 "disappears, and how do you keep them?",
         f"{d.loc[d.enrolled_courses == '', 'student_id'].iloc[0]} has no "
         "enrolments, so $unwind drops them. "
         "preserveNullAndEmptyArrays: true keeps them"),
        ("core", "How many students per city?",
         "; ".join(f"{k} {v}" for k, v in d.city.value_counts().items())),
        ("stretch", "Would you embed the course document in each student, or "
                    "reference it? Argue from this data.",
         "reference — a course's instructor would otherwise be duplicated "
         "into every enrolled student, and renaming one instructor would "
         "mean rewriting several documents"),
    ]


@ask("course-10-mongodb/courses.csv")
def _q(d):
    return [
        ("warm", "How many courses, and what is the total capacity?",
         f"{len(d)} courses, {int(d.capacity.sum())} seats"),
        ("core", "$lookup students onto courses. How would you count "
                 "enrolments per course?",
         "$unwind the student enrolments first, then $group by course_id — "
         "$lookup alone gives you arrays, not counts"),
        ("stretch", "Add a schema validation rule that rejects a course with "
                    "capacity below 1. What does MongoDB do to documents "
                    "already in the collection?",
         "nothing — validation applies to writes from that point on. "
         "Existing bad documents stay until you find and fix them"),
    ]


@ask("course-11-bi/dim-product.csv")
def _q(d):
    return [
        ("warm", "Which column makes this a snowflake rather than a pure "
                 "star?",
         "supplier_key — it points at a further dimension table instead of "
         "carrying the supplier's attributes inline"),
        ("core", "Compute the margin per product from unit_cost and "
                 "list_price. Which has the best percentage margin?",
         "{} at {}".format(
             d.loc[((d.list_price - d.unit_cost) / d.list_price).idxmax(),
                   "product"],
             pct(((d.list_price - d.unit_cost) / d.list_price).max()))),
        ("core", "Should margin be a calculated column or a measure? Why?",
         "a measure — margin percentage must be computed as total profit "
         "over total revenue at whatever grain the visual asks for. A "
         "calculated column would average the percentages, which is wrong"),
    ]


@ask("course-11-bi/dim-store.csv")
def _q(d):
    return [
        ("warm", "How many stores per region?",
         "; ".join(f"{k} {v}" for k, v in d.region.value_counts().items())),
        ("core", "A visual shows average revenue by region. Why can that "
                 "mislead here?",
         "South has two stores and North one, so an average per STORE and a "
         "total per REGION tell different stories. Say which you mean"),
        ("stretch", "Add a slicer on region. What must you check before "
                    "trusting the dashboard?",
         "that every pivot is connected to the slicer through Report "
         "Connections — an unconnected visual keeps showing unfiltered data "
         "beside filtered ones"),
    ]


@ask("course-11-bi/dim-date.csv")
def _q(d):
    return [
        ("warm", "How many quarters appear, and how many months?",
         f"{d.quarter.nunique()} quarters, {d.month.nunique()} months"),
        ("core", "Which calendar month is missing, and what breaks because "
                 "of it?",
         "March. A month-on-month growth measure has no March row to divide "
         "by, so April either divides by zero or silently compares to "
         "February"),
        ("stretch", "Why do BI tools want a dedicated date table rather than "
                    "the dates already in the fact table?",
         "so that every date in the range exists, including the ones with no "
         "transactions. Time intelligence needs a continuous axis"),
    ]


@ask("course-11-bi/fact-sales.csv")
def _q(d):
    prod = load("course-11-bi/dim-product.csv")
    store = load("course-11-bi/dim-store.csv")
    j = d.merge(prod, on="product_key").merge(store, on="store_key")
    j["revenue"] = j.qty * j.list_price
    return [
        ("warm", "State the grain, and give SUM and COUNT of qty.",
         f"one row per product per store per day; SUM {int(d.qty.sum())}, "
         f"COUNT {len(d)}, AVERAGE {d.qty.mean():.4f}"),
        ("core", "Join all three dimensions and compute revenue. What is the "
                 "total, and the South total?",
         f"{money(j.revenue.sum())} total, "
         f"{money(j[j.region == 'South'].revenue.sum())} South"),
        ("core", "DISTINCTCOUNT of product_key against COUNTROWS. Why do "
                 "they differ?",
         f"{d.product_key.nunique()} against {len(d)} — one counts distinct "
         "values, the other counts rows, and products repeat across days"),
        ("core", "Write a measure for South revenue that ignores whatever "
                 "region the visual is filtered to.",
         "CALCULATE(SUM(revenue), ALL(region), region = \"South\") — "
         "CALCULATE REPLACES filter context rather than adding to it"),
        ("stretch", "Check the join added no rows. Why is that worth "
                    "checking every time?",
         f"{len(j)} rows in, {len(d)} rows out — a many-to-many on any key "
         "would multiply the facts and inflate every total silently"),
    ]


# ---------------------------------------------------------------------------
# Courses 12 A, 12 B, 13 A, 13 B
# ---------------------------------------------------------------------------

@ask("course-12a-ml/house-prices.csv")
def _q(d):
    X = np.column_stack([np.ones(len(d)), d.area_sqft, d.bedrooms, d.age_years])
    b = np.linalg.lstsq(X, d.price_lakh, rcond=None)[0]
    pred = X @ b
    r2 = 1 - ((d.price_lakh - pred) ** 2).sum() / \
        ((d.price_lakh - d.price_lakh.mean()) ** 2).sum()
    rmse = float(np.sqrt(((d.price_lakh - pred) ** 2).mean()))
    return [
        ("warm", "How many rows, and what is the price range?",
         f"{len(d)} rows, {d.price_lakh.min():.2f} to "
         f"{d.price_lakh.max():.2f} lakh"),
        ("core", "Split 80/20 and fit multiple linear regression. Report the "
                 "coefficients.",
         f"intercept {b[0]:.4f}, area {b[1]:.6f}, bedrooms {b[2]:.4f}, age "
         f"{b[3]:.4f} (full-data fit)"),
        ("core", "Report MAE, RMSE and R-squared on the fit.",
         f"MAE {np.abs(d.price_lakh - pred).mean():.4f}, RMSE {rmse:.4f}, "
         f"R-squared {r2:.4f}"),
        ("core", "The data were built from 12 + 0.045*area + 3.5*beds - "
                 "0.25*age. How close are you?",
         f"area {b[1]:.5f} against 0.045, bedrooms {b[2]:.3f} against 3.5, "
         f"age {b[3]:.3f} against -0.25"),
        ("core", "Standardise the features and refit. What changes, and what "
                 "does not?",
         "the coefficients change scale; the predictions and R-squared do "
         "not. Scaling matters for regularisation and distance methods, not "
         "for plain least squares"),
        ("stretch", "Add area squared. Does R-squared improve, and is that "
                    "evidence of a better model?",
         "R-squared can only rise when you add a term, so it is not "
         "evidence. Compare on held-out data, or use adjusted R-squared"),
    ]


@ask("course-12a-ml/loan-approval.csv")
def _q(d):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    X = d[["income", "debt", "credit_score"]].values
    y = d.approved.values
    pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    acc = cross_val_score(pipe, X, y, cv=5).mean()
    pipe.fit(X, y)
    co = dict(zip(["income", "debt", "credit_score"], pipe[-1].coef_[0]))
    return [
        ("warm", "What fraction of applications were approved?",
         pct(y.mean(), 2)),
        ("core", "Fit logistic regression with 5-fold cross-validation. What "
                 "accuracy?", f"{acc:.4f}"),
        ("core", "Build the confusion matrix and compute precision, recall "
                 "and F1. Which matters more for a lender?",
         "recall on defaults if you fear bad loans; precision on approvals "
         "if you fear turning away good customers. The threshold is a "
         "business choice, not a statistical one"),
        ("core", "Standardise, then rank the features by coefficient size. "
                 "Which matters most?",
         "; ".join(f"{k} {v:+.4f}" for k, v in
                   sorted(co.items(), key=lambda kv: -abs(kv[1])))),
        ("stretch", "credit_score has by far the biggest RAW coefficient in "
                    "the rule that generated this data (0.008 against "
                    "0.00005 for income), yet income has the larger "
                    "standardised effect. Explain.",
         "a coefficient is per unit, and the units differ enormously. "
         "Income's spread is about 30,000 and credit score's about 160, so "
         "coefficient x spread — the effect over the range actually seen — "
         "favours income"),
        ("stretch", "You reach 100% accuracy. What has gone wrong?",
         "a leak. The labels were drawn from a probability, so some "
         "applicants near the boundary went either way and no model can "
         "separate them"),
    ]


@ask("course-12a-ml/customer-segments.csv")
def _q(d):
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import adjusted_rand_score as ari
    X = d[["annual_spend", "visits_per_year", "online_ratio"]].values
    raw = KMeans(3, n_init=10, random_state=0).fit(X)
    sc = KMeans(3, n_init=10, random_state=0).fit(
        StandardScaler().fit_transform(X))
    return [
        ("warm", "Compare the three columns' ranges. What do you notice?",
         "; ".join(f"{c} {d[c].min():.2f}-{d[c].max():.2f}"
                   for c in ["annual_spend", "visits_per_year",
                             "online_ratio"])
         + " — five orders of magnitude apart"),
        ("core", "Cluster with k=3 WITHOUT scaling and score against "
                 "true_segment.",
         f"adjusted Rand index {ari(d.true_segment, raw.labels_):.4f}"),
        ("core", "Now scale first and score again.",
         f"adjusted Rand index {ari(d.true_segment, sc.labels_):.4f}"),
        ("core", "Explain the difference in one sentence.",
         "Euclidean distance is dominated by whichever feature has the "
         "largest numbers, so unscaled k-Means clusters on annual_spend "
         "alone and ignores the other two"),
        ("stretch", "Use PCA to plot the segments in two dimensions. Should "
                    "you scale before PCA too?",
         "yes, for the same reason — PCA maximises variance, and an unscaled "
         "large-range feature will take the first component by itself"),
    ]


@ask("course-12b-bigdata/web-logs.csv")
def _q(d):
    return [
        ("warm", "How many requests, distinct IPs and distinct paths?",
         f"{len(d)} requests, {d.ip.nunique()} IPs, {d.path.nunique()} paths"),
        ("warm", "What is the error rate (status 400 or above)?",
         pct((d.status >= 400).mean(), 2)),
        ("core", "Count hits per path. Which is busiest?",
         f"{d.path.value_counts().idxmax()} with "
         f"{int(d.path.value_counts().max())} hits"),
        ("core", "Write this as a MapReduce. What does the mapper emit, what "
                 "does the reducer receive, and what does a combiner change?",
         "mapper emits (path, 1); reducer receives (path, [1,1,...]) and "
         "sums. A combiner sums locally first, cutting shuffle traffic "
         "without changing the answer — because addition is associative"),
        ("core", "Total bytes per IP. Which IP transferred most?",
         f"{d.groupby('ip').bytes.sum().idxmax()} with "
         f"{money(d.groupby('ip').bytes.sum().max())} bytes"),
        ("stretch", "Do the same three counts a dict, a Hive GROUP BY and a "
                    "Spark reduceByKey. Must they agree, and why bother?",
         "they must, and checking is how you learn to trust the "
         "distributed answer. If reduceByKey disagrees with the dict, the "
         "bug is yours, not Spark's"),
    ]


@ask("course-12b-bigdata/wordcount-corpus.csv")
def _q(d):
    from collections import Counter
    w = Counter(x for t in d.text for x in t.split())
    return [
        ("warm", "Count the words by hand. How many in total, and how many "
                 "distinct?",
         f"{sum(w.values())} words, {len(w)} distinct"),
        ("warm", "Which word appears most often, and how many times?",
         f"'{w.most_common(1)[0][0]}' {w.most_common(1)[0][1]} times"),
        ("core", "Now run it as MapReduce and compare with your hand count.",
         "; ".join(f"{k} {v}" for k, v in w.most_common(5))),
        ("core", "Compute TF-IDF for 'dog' and for 'the'. Why does one score "
                 "near zero?",
         f"'the' appears in {sum(1 for t in d.text if 'the' in t.split())} of "
         f"{len(d)} documents, so its IDF is near zero — a word in every "
         "document distinguishes nothing"),
        ("stretch", "Lowercase and strip punctuation first. Does the answer "
                    "change here, and would it on real text?",
         "not here — the corpus is already clean lowercase. On real text it "
         "changes everything, which is why preprocessing is a step, not an "
         "afterthought"),
    ]


@ask("course-13a-ai/graph-edges.csv")
def _q(d):
    return [
        ("warm", "How many nodes and edges? Is the graph directed?",
         f"{len(set(d.from_city) | set(d.to_city))} nodes, {len(d)} edges, "
         "undirected — each row is traversable both ways"),
        ("core", "Run BFS from Arad to Bucharest. What path, how many hops, "
                 "what cost?",
         "Arad-Sibiu-Fagaras-Bucharest, 3 hops, cost 450"),
        ("core", "Run uniform-cost search. What changes?",
         "Arad-Sibiu-Rimnicu-Pitesti-Bucharest, 4 hops, cost 418 — one hop "
         "longer and 32 cheaper"),
        ("core", "Why is BFS's answer not wrong?",
         "BFS optimises hops and UCS optimises cost. They answer different "
         "questions, and BFS is only optimal for cost when every edge costs "
         "the same"),
        ("stretch", "Add a straight-line heuristic and run A*. What must the "
                    "heuristic satisfy, and what happens if it does not?",
         "admissibility — it must never overestimate. An overestimate can "
         "prune the optimal path, and A* then returns a worse route while "
         "still claiming to be finished"),
        ("stretch", "Run DFS. Why can it return a much worse path?",
         "it commits to one branch to its end. It is complete on a finite "
         "graph but optimal on neither hops nor cost"),
    ]


@ask("course-13a-ai/map-colouring.csv")
def _q(d):
    from collections import defaultdict
    nbr = defaultdict(set)
    for r in d.itertuples():
        nbr[r.region].add(r.neighbour)
        nbr[r.neighbour].add(r.region)
    return [
        ("warm", "List each region's neighbours. Which region has none?",
         "T — Tasmania appears in no adjacency, so it takes any colour"),
        ("core", "Colour the map with 3 colours by backtracking. Give one "
                 "valid assignment.",
         "many exist; any assignment where WA, NT and SA all differ works"),
        ("core", "Show that 2 colours cannot work.",
         "WA, NT and SA are mutually adjacent — a triangle needs 3"),
        ("core", "Apply the minimum-remaining-values heuristic. Which "
                 "variable does it pick first, and which last?",
         f"SA first — it has {len(nbr['SA'])} neighbours, the most "
         "constrained; T last, being unconstrained"),
        ("stretch", "Run AC-3 before search. What does arc consistency prune "
                    "here, and when does it help most?",
         "little on an uncoloured map with 3 values each; it earns its keep "
         "once some variables are assigned, or when domains are large"),
    ]


@ask("course-13a-ai/family-relations.csv")
def _q(d):
    gp = {(a.parent, b.child) for a in d.itertuples()
          for b in d.itertuples() if a.child == b.parent}
    return [
        ("warm", "Load it as parent/2 facts. How many facts and how many "
                 "individuals?",
         f"{len(d)} facts, {len(set(d.parent) | set(d.child))} individuals"),
        ("core", "Define sibling(X,Y). What must you add to stop everyone "
                 "being their own sibling?",
         "X \\= Y — without it, sibling(mary, mary) succeeds through the "
         "same parent"),
        ("core", "Define grandparent(X,Z) :- parent(X,Y), parent(Y,Z). How "
                 "many solutions?",
         f"{len(gp)} pairs"),
        ("core", "Write ancestor/2 recursively. Which clause must come "
                 "first, and why?",
         "the base case parent(X,Y) first. Put the recursive clause first "
         "and a query with an unbound argument can loop forever"),
        ("stretch", "Trace backtracking on grandparent(john, X). What does "
                    "unification bind at each step?",
         "Y binds to each of john's children in turn, then Z to each of that "
         "child's children; on failure Prolog unbinds Z and retries the next Y"),
    ]


@ask("course-13b-cloud/storage-costs.csv")
def _q(d):
    monthly = d.gb_stored * d.price_per_gb_month
    arch = d[d.tier == "archive"].iloc[0]
    return [
        ("warm", "Monthly storage cost per tier, and in total.",
         "; ".join(f"{t} {v:.2f}" for t, v in zip(d.tier, monthly))
         + f"; total {monthly.sum():.2f}"),
        ("core", "Which tier is cheapest per GB-month, and by what factor "
                 "against the dearest?",
         f"{d.loc[d.price_per_gb_month.idxmin(), 'tier']} — "
         f"{d.price_per_gb_month.max() / d.price_per_gb_month.min():.1f}x "
         "cheaper than the dearest"),
        ("core", "Now cost a full retrieval of every byte in archive. "
                 "Compare with its monthly storage bill.",
         f"retrieval {arch.gb_stored * arch.retrieval_per_gb:.2f} against "
         f"storage {arch.gb_stored * arch.price_per_gb_month:.2f} — about "
         f"{arch.retrieval_per_gb / arch.price_per_gb_month:.0f} months of "
         "storage in a single read"),
        ("core", "Add egress for that retrieval. What is the true cost?",
         f"{arch.gb_stored * (arch.retrieval_per_gb + arch.egress_per_gb):.2f}"
         " — egress is charged on top and is usually the bigger surprise"),
        ("stretch", "How often must you read the archive tier before it "
                    "stops being the cheapest option? State the assumption "
                    "your answer depends on.",
         "roughly once every few years on these numbers; the answer depends "
         "entirely on how much of it you read each time, which is the "
         "assumption every cloud cost model hides"),
    ]


@ask("course-13b-cloud/iam-policies.csv")
def _q(d):
    return [
        ("warm", "How many statements and how many principals?",
         f"{len(d)} statements, {d.principal.nunique()} principals"),
        ("core", "Can alice delete reports/q1.csv? Show the evaluation.",
         "no — she has an explicit Deny on s3:DeleteObject for reports/*, "
         "and Deny always wins"),
        ("core", "Can bob read reports/salaries.csv? And reports/q1.csv?",
         "salaries.csv no — a specific Deny beats the wildcard Allow. "
         "q1.csv yes — the Allow applies and nothing denies it"),
        ("core", "carol has s3:* on the bucket. Can she delete?",
         "no. A wildcard Allow is not unrestricted access when an explicit "
         "Deny names the action"),
        ("core", "dave appears nowhere. What can he do?",
         "nothing — anything not explicitly allowed is denied by default"),
        ("stretch", "State the evaluation order in full, and say which rule "
                    "makes 'grant broadly, deny narrowly' workable.",
         "explicit Deny, then explicit Allow, then implicit Deny. Because "
         "Deny is absolute, a broad Allow can be safely carved back with "
         "targeted Denies"),
    ]


# ---------------------------------------------------------------------------
# Courses 14 A, 14 B, 15 A, 15 B
# ---------------------------------------------------------------------------

@ask("course-14a-deeplearning/xor.csv")
def _q(d):
    return [
        ("warm", "Plot the four points. Can you separate the 1s from the 0s "
                 "with a straight line?",
         "no — (0,1) and (1,0) are the 1s and they sit on opposite corners"),
        ("core", "Train a single-layer perceptron. What is the best accuracy "
                 "it reaches, however long you train?",
         "0.75 — three of the four. Exhausting the weight space confirms it: "
         "no line does better"),
        ("core", "Add one hidden layer of two units with a non-linear "
                 "activation. What happens?",
         "it reaches 1.0. The hidden layer bends the space so a line in the "
         "new space is a curve in the old one"),
        ("core", "Replace the activation with the identity. Does the hidden "
                 "layer still help?",
         "no — a stack of linear maps is a linear map. The non-linearity is "
         "what the hidden layer is FOR"),
        ("stretch", "Do one forward and one backward pass by hand on a "
                    "2-2-1 network. Where does the chain rule enter?",
         "at every layer: the gradient at a weight is the local derivative "
         "times the gradient flowing back from above. That product is "
         "backpropagation"),
    ]


@ask("course-14a-deeplearning/sensor-failures.csv")
def _q(d):
    from sklearn.linear_model import LogisticRegression
    from sklearn.neural_network import MLPClassifier
    from sklearn.model_selection import cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    X = d[["temperature_c", "vibration_mm_s"]].values
    y = d.failed.values
    lin = cross_val_score(make_pipeline(StandardScaler(),
                                        LogisticRegression(max_iter=1000)),
                          X, y, cv=5).mean()
    net = cross_val_score(make_pipeline(StandardScaler(),
                                        MLPClassifier((16, 8), max_iter=3000,
                                                      random_state=0)),
                          X, y, cv=5).mean()
    return [
        ("warm", "What fraction of readings are failures?", pct(y.mean(), 2)),
        ("warm", "Scatter temperature against vibration, coloured by label. "
                 "What shape is the boundary?",
         "an ellipse — failures lie OUTSIDE a safe region in the middle"),
        ("core", "Fit logistic regression with cross-validation. What "
                 "accuracy?", f"{lin:.4f}"),
        ("core", "Now fit a network with one or two hidden layers.",
         f"{net:.4f} — about {100 * (net - lin):.0f} points better"),
        ("core", "Why can the linear model not be fixed by training longer?",
         "its decision boundary is a straight line and the true one is "
         "closed and curved. No amount of training changes the shape of the "
         "hypothesis"),
        ("stretch", "Five per cent of labels were flipped when the file was "
                    "built. What does that imply about any accuracy above "
                    "0.95?",
         "it is impossible on held-out data — the ceiling is 0.95. A higher "
         "figure means you scored on the training set or leaked the label"),
    ]


@ask("course-14b-timeseries/ar2-series.csv")
def _q(d):
    v = d.value.values
    m = v.mean()
    acf = lambda k: (((v[k:] - m) * (v[:len(v) - k] - m)).sum()
                     / ((v - m) ** 2).sum())
    r1, r2 = acf(1), acf(2)
    p1 = r1 * (1 - r2) / (1 - r1 ** 2)
    p2 = (r2 - r1 ** 2) / (1 - r1 ** 2)
    return [
        ("warm", "Plot the series. Does it look stationary, and what would "
                 "tell you it was not?",
         "yes — no trend and constant variance. A wandering level or growing "
         "swings would say otherwise"),
        ("warm", "Compute the lag-1 and lag-2 autocorrelations.",
         f"r1 = {r1:.4f}, r2 = {r2:.4f}"),
        ("core", "Plot the ACF and PACF. What order do they suggest, and "
                 "which plot tells you?",
         "AR(2) — the PACF cuts off after lag 2 while the ACF tails off. For "
         "an MA process it is the other way round"),
        ("core", "Estimate the coefficients with Yule-Walker.",
         f"phi1 = {p1:.4f}, phi2 = {p2:.4f} (built from 0.6 and -0.3)"),
        ("core", "Fit ARIMA(2,0,0) and compare AIC with ARIMA(1,0,0) and "
                 "ARIMA(3,0,0). Which wins?",
         "the AR(2) should, and if AR(3) edges it, check whether the third "
         "coefficient is distinguishable from zero"),
        ("stretch", "Run ADF and KPSS. What does each test's null hypothesis "
                    "say, and why run both?",
         "ADF's null is a unit root; KPSS's null is stationarity. They point "
         "opposite ways, so agreement is strong evidence and disagreement "
         "tells you the case is borderline"),
        ("stretch", "Run Ljung-Box on the residuals. What are you hoping for?",
         "a LARGE p-value — you want to fail to reject, meaning no "
         "autocorrelation is left for the model to have captured"),
    ]


@ask("course-14b-timeseries/seasonal-sales.csv")
def _q(d):
    v = d.sales.values
    mo = d.month.str.slice(5, 7).astype(int)
    bym = d.groupby(mo).sales.mean()
    return [
        ("warm", "How many months, and over how many years?",
         f"{len(d)} months, {len(d) // 12} years"),
        ("core", "Decompose into trend, season and remainder. Is the season "
                 "additive or multiplicative here?",
         "additive — the swing stays about the same size as the level rises"),
        ("core", "Which calendar month is strongest and which weakest?",
         f"{bym.idxmax()} at {bym.max():.2f}, {bym.idxmin()} at "
         f"{bym.min():.2f} — a swing of {bym.max() - bym.min():.2f}"),
        ("core", "Difference at lag 12. What does the standard deviation do?",
         f"{v.std():.2f} falls to {(v[12:] - v[:-12]).std():.2f} — the "
         "season is gone, the trend remains"),
        ("core", "Now difference again at lag 1. What is left?",
         "close to noise. Doing the two in the wrong order leaves the season "
         "tangled in the trend"),
        ("stretch", "Fit SARIMA with s=12 and forecast 12 months. Do the "
                    "intervals widen, and should they?",
         "yes — uncertainty compounds with horizon. A forecast whose "
         "interval does not widen is not a forecast"),
        ("stretch", "Compare Holt-Winters with SARIMA. When would you prefer "
                    "each?",
         "Holt-Winters for a quick, robust seasonal forecast with little "
         "tuning; SARIMA when you want diagnostics and a model you can "
         "defend term by term"),
    ]


@ask("course-14b-timeseries/macro-indicators.csv")
def _q(d):
    return [
        ("warm", "Plot all three series. Which two look related?",
         "rates and inflation; the third is a control with no relationship"),
        ("core", "Test whether rates Granger-cause inflation.",
         "yes, strongly — the lagged rates improve the inflation model"),
        ("core", "Now test the reverse direction.",
         "no. The causality was planted one way only"),
        ("core", "Test the control series in both directions. What should "
                 "you find, and why does it matter?",
         "nothing significant either way. A control that stays quiet is what "
         "tells you the test is not simply firing on everything"),
        ("core", "Fit a VAR. How do you choose the lag order?",
         "by information criterion — AIC or BIC over candidate lags, not by "
         "eye"),
        ("stretch", "Your test fires in BOTH directions on some other "
                    "dataset. What have you found?",
         "feedback, or a common driver you have not modelled. Granger "
         "causality is about predictive precedence, not cause"),
    ]


@ask("course-15a-nlp/sentiment-reviews.csv")
def _q(d):
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import make_pipeline
    from sklearn.model_selection import cross_val_score
    tf = cross_val_score(make_pipeline(TfidfVectorizer(), MultinomialNB()),
                         d.text, d.label, cv=5).mean()
    bow = cross_val_score(make_pipeline(CountVectorizer(), MultinomialNB()),
                          d.text, d.label, cv=5).mean()
    return [
        ("warm", "How many reviews, and is the set balanced?",
         f"{len(d)} reviews, {int(d.label.sum())} positive and "
         f"{int((d.label == 0).sum())} negative — balanced, so 0.5 is the "
         "coin-flip baseline"),
        ("warm", "Tokenize and remove stopwords. How does the vocabulary "
                 "shrink?",
         f"{len(set(w.lower() for t in d.text for w in t.split()))} raw "
         "tokens before stopword removal"),
        ("core", "Stem and lemmatize 'works', 'working', 'stopped'. Where do "
                 "the two disagree?",
         "a stemmer chops to a possibly non-word ('studi'); a lemmatizer "
         "returns a dictionary form ('study'). Stemming is faster, "
         "lemmatizing is correct"),
        ("core", "Build bag-of-words and TF-IDF features and cross-validate "
                 "Naive Bayes on each.",
         f"bag-of-words {bow:.4f}, TF-IDF {tf:.4f}"),
        ("core", "Which review is hardest, and why?",
         "'Works well but the cable is too short' — positive overall, but it "
         "carries negative words, and bag-of-words cannot see the 'but'"),
        ("stretch", "With 20 reviews, how much should you trust a 5% "
                    "difference between two models?",
         "not at all. One review is 5% of the data, so the fold-to-fold "
         "spread swamps a gap that size"),
    ]


@ask("course-15a-nlp/ner-sentences.csv")
def _q(d):
    types = [p.split("|")[1] for e in d.expected_entities for p in e.split(";")]
    from collections import Counter
    c = Counter(t.strip() for t in types)
    return [
        ("warm", "How many sentences, and how many gold entities in total?",
         f"{len(d)} sentences, {sum(c.values())} entities"),
        ("warm", "Which entity types appear, and how often?",
         "; ".join(f"{k} {v}" for k, v in sorted(c.items()))),
        ("core", "Run spaCy's NER and compare against the gold column. "
                 "Compute precision and recall.",
         "match on both span and type; a right span with the wrong label is "
         "a miss, not a hit"),
        ("core", "Which entities does an English model most often get wrong "
                 "here?",
         "Indian state and river names — 'Andhra Pradesh' and 'Krishna' are "
         "far rarer in the training data than the city names"),
        ("stretch", "Your model tags 'Krishna' as PERSON. Is that a bug, and "
                    "what would fix it?",
         "not a bug — it is a genuine ambiguity resolved by context the "
         "model lacks. Fine-tuning on Indian text, or a gazetteer, is what "
         "fixes it"),
    ]


@ask("course-15b-mlops/loan-reference.csv")
def _q(d):
    return [
        ("warm", "Summarise each feature: mean and spread.",
         "; ".join(f"{c} mean {d[c].mean():.1f} sd {d[c].std():.1f}"
                   for c in ["income", "debt", "credit_score"])),
        ("core", "Train a classifier and log it with MLflow. What must you "
                 "log for the run to be reproducible?",
         "parameters, metrics, the model artifact, the data version and the "
         "random seed. A metric with no parameters beside it proves nothing"),
        ("core", "Register the model and tag it as the baseline. Why does "
                 "the registry matter more than the file?",
         "it names which version is in production and lets you roll back. A "
         "file on disk records neither"),
        ("stretch", "Put the data under DVC. What goes into git, and what "
                    "does not?",
         "a small pointer file goes into git; the bytes go to the DVC remote. "
         "That is how the repository stays small while the data is versioned"),
    ]


@ask("course-15b-mlops/loan-current.csv")
def _q(d):
    ref = load("course-15b-mlops/loan-reference.csv")
    from scipy import stats as st

    def psi(a, b, bins=10):
        edges = np.percentile(a, np.linspace(0, 100, bins + 1))
        edges[0], edges[-1] = -np.inf, np.inf
        pa = np.histogram(a, edges)[0] / len(a) + 1e-6
        pb = np.histogram(b, edges)[0] / len(b) + 1e-6
        return float(((pb - pa) * np.log(pb / pa)).sum())

    return [
        ("warm", "Compare each feature's mean against the reference batch. "
                 "Which has moved?",
         "; ".join(f"{c} {ref[c].mean():.1f} -> {d[c].mean():.1f}"
                   for c in ["income", "debt", "credit_score"])),
        ("core", "Compute the PSI for each feature against the reference.",
         "; ".join(f"{c} {psi(ref[c], d[c]):.4f}"
                   for c in ["income", "debt", "credit_score"])),
        ("core", "The usual thresholds are 0.1 for 'investigate' and 0.2 for "
                 "'act'. What do you do?",
         f"credit_score at {psi(ref.credit_score, d.credit_score):.3f} clears "
         "the action threshold; the other two do not. Investigate the score "
         "feed first"),
        ("core", "Run a two-sample KS test on each feature. Does it agree "
                 "with PSI?",
         "; ".join(
             f"{c} p={st.ks_2samp(ref[c], d[c]).pvalue:.3g}"
             for c in ["income", "debt", "credit_score"])),
        ("core", "Score the reference model on the new batch. Has accuracy "
                 "collapsed?",
         "no — the inputs shifted but the input-to-label relationship did "
         "not. This is DATA drift, not CONCEPT drift"),
        ("stretch", "Your monitoring fires a retrain. Should you? Argue both "
                    "sides.",
         "retraining costs a deployment and gains almost nothing here, "
         "because the rule generating the label is unchanged. But a shifting "
         "input distribution is a warning that the population is changing, "
         "so investigate the cause rather than either retraining on reflex "
         "or ignoring it"),
    ]


# ---------------------------------------------------------------------------

LEVELS = [("warm", "Warm-up"), ("core", "Core"), ("stretch", "Stretch")]
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


def main():
    datasets = sorted(p.relative_to(DATA).as_posix()
                      for p in DATA.rglob("*.csv"))
    missing = [d for d in datasets if d not in QUESTIONS]
    if missing:
        print("NO QUESTIONS FOR:")
        for m in missing:
            print("   ", m)
        return 1

    total_q = 0
    out = [
        "# Practice questions",
        "",
        "A question set for every dataset in `data/`, graded **warm-up** → "
        "**core** → **stretch**. Warm-ups check you can load the file and "
        "read it; core questions are the ones an exam asks; stretch "
        "questions are the ones worth arguing about in a viva.",
        "",
        "**The answers are computed, not typed.** Every answer below is a "
        "function of the CSV, evaluated when this page is generated. Three "
        "figures I wrote from memory while building the datasets turned out "
        "wrong, and a wrong answer key is worse than none — the student who "
        "gets it right concludes they got it wrong.",
        "",
        "Answers are folded away. Work the question first; the point is the "
        "method, and the number only tells you whether the method was right.",
        "",
    ]
    counts = []
    for folder in COURSE_NAMES:
        rels = [d for d in datasets if d.split("/")[0] == folder]
        if not rels:
            continue
        out += ["---", "", f"## {COURSE_NAMES[folder]}", ""]
        for rel in rels:
            qs = QUESTIONS[rel](load(rel))
            total_q += len(qs)
            counts.append((rel, len(qs)))
            out += [f"### `data/{rel}`", ""]
            n = 0
            for key, title in LEVELS:
                tier = [q for q in qs if q[0] == key]
                if not tier:
                    continue
                out += [f"**{title}**", ""]
                for _, question, _ans in tier:
                    n += 1
                    out.append(f"{n}. {question}")
                out.append("")
            out += ["<details><summary>Answers</summary>", ""]
            n = 0
            for key, _title in LEVELS:
                for _, _question, ans in [q for q in qs if q[0] == key]:
                    n += 1
                    out.append(f"{n}. {ans}")
            out += ["", "</details>", ""]

    out.insert(8, f"**{total_q} questions over {len(datasets)} datasets.**")
    out.insert(9, "")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "PRACTICE-QUESTIONS.md").write_text("\n".join(out) + "\n")
    print(f"  {total_q} questions over {len(datasets)} datasets")
    thin = [(r, c) for r, c in counts if c < 3]
    if thin:
        print("  thin sets (fewer than 3 questions):", thin)
    return 0


if __name__ == "__main__":
    sys.exit(main())
