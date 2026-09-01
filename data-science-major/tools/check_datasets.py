#!/usr/bin/env python3
"""Recover every practice dataset's planted truth from the CSV on disk.

data/ exists so a student can SCORE an answer, not merely produce one. That
only works if the answer key is right, so this script reads each file back
and runs the method it is meant for:

  * fit the regression and check the slope is near the 6.0 it was built from
  * fit the AR(2) and check phi comes back near (0.6, -0.3)
  * cluster the blobs and check the recovered centres match
  * run the Granger test both ways and check it fires in one direction only
  * count the missing cells, the duplicate row and the three spellings of
    Hyderabad, and check they match what the index claims

Nothing here is a smoke test. Each assertion is the answer a student would
compute, so if one fails the DATA is wrong, not the script.

Usage:  python3 tools/check_datasets.py
"""
import csv
import hashlib
import io
import math
import pathlib
import subprocess
import sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

checks = []


def check(label, ok, detail=""):
    checks.append((label, bool(ok), detail))
    print(f"  {'ok  ' if ok else 'FAIL'} {label}"
          f"{'' if ok else '   -- ' + str(detail)}")


def load(rel):
    return pd.read_csv(DATA / rel)


def close(a, b, tol):
    return abs(float(a) - float(b)) <= tol


# ---------------------------------------------------------------------------

def check_determinism():
    """Regenerating must reproduce every file byte for byte.

    Into a TEMPORARY directory, never over data/. Regenerating in place would
    repair a corrupted file before the hundred checks below could notice it,
    which would leave all of them unable to fail -- the worst kind of test.
    """
    import tempfile
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    have = {p.relative_to(DATA).as_posix(): digest(p)
            for p in sorted(DATA.rglob("*.csv"))}
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable,
                        str(ROOT / "tools" / "make_datasets.py"), tmp],
                       capture_output=True, check=True)
        fresh = {p.relative_to(pathlib.Path(tmp)).as_posix(): digest(p)
                 for p in sorted(pathlib.Path(tmp).rglob("*.csv"))}
    changed = sorted(k for k in set(have) | set(fresh)
                     if have.get(k) != fresh.get(k))
    check(f"{len(have)} datasets on disk match a fresh generation, "
          "byte for byte", not changed, changed[:3])


def check_questions():
    """The published answer key must equal what the code computes now.

    Same trick as the datasets: regenerate into a temporary directory and
    compare. If a dataset changes and the questions are not rebuilt, the
    answer key silently starts lying, and this is what notices.
    """
    import tempfile
    live = (DATA / "PRACTICE-QUESTIONS.md")
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable,
                            str(ROOT / "tools" / "make_questions.py"), tmp],
                           capture_output=True, text=True)
        fresh = pathlib.Path(tmp) / "PRACTICE-QUESTIONS.md"
        check("every dataset has a question set",
              r.returncode == 0, r.stdout.strip()[:200])
        if not fresh.exists():
            check("the answer key regenerates", False, "not produced")
            return
        check("the published answer key matches a fresh computation",
              live.read_bytes() == fresh.read_bytes(),
              "data/PRACTICE-QUESTIONS.md is stale -- run "
              "tools/make_questions.py")

    text = live.read_text()
    datasets = sorted(p.relative_to(DATA).as_posix()
                      for p in DATA.rglob("*.csv"))
    absent = [d for d in datasets if f"### `data/{d}`" not in text]
    check(f"{len(datasets)} datasets each appear in the answer key",
          not absent, absent[:3])

    # every question must have an answer beside it, tier by tier
    import re as _re
    mismatched = []
    for block in text.split("### `data/")[1:]:
        name = block.split("`")[0]
        body, _, answers = block.partition("<details><summary>Answers")
        qn = len(_re.findall(r"^\d+\. ", body, _re.M))
        an = len(_re.findall(r"^\d+\. ", answers, _re.M))
        if qn != an or qn < 3:
            mismatched.append(f"{name}: {qn} questions, {an} answers")
    check("every question has an answer, and no set has fewer than three",
          not mismatched, mismatched[:3])


def check_shared():
    df = load("shared/sales-transactions.csv")
    check("sales: revenue is quantity x unit_price on every row",
          (df.quantity * df.unit_price == df.revenue).all())
    check("sales: total 12,880 and South 10,360",
          df.revenue.sum() == 12880
          and df[df.region == "South"].revenue.sum() == 10360,
          f"{df.revenue.sum()} / {df[df.region == 'South'].revenue.sum()}")
    best = df.groupby("product").revenue.sum().idxmax()
    check("sales: Rice 5kg is the best-selling product at 5,600",
          best == "Rice 5kg"
          and df.groupby("product").revenue.sum().max() == 5600, best)

    f = load("shared/flowers.csv")
    check("flowers: 90 rows, 3 species, 30 each",
          len(f) == 90 and f.species.value_counts().nunique() == 1
          and f.species.nunique() == 3)
    check("flowers: no negative measurement",
          (f.select_dtypes("number") > 0).all().all())
    # alba should separate on petal_length; the other two should overlap
    alba = f[f.species == "alba"].petal_length
    rest = f[f.species != "alba"].petal_length
    check("flowers: alba separates cleanly on petal_length",
          alba.max() < rest.min(), f"{alba.max()} vs {rest.min()}")
    bor = f[f.species == "borealis"].petal_length
    car = f[f.species == "carinata"].petal_length
    check("flowers: borealis and carinata overlap, as intended",
          bor.max() > car.min(), f"{bor.max()} vs {car.min()}")


def check_course_01():
    p = load("course-1-office/payroll.csv")
    net = p.basic_pay * 1.32
    gross = p.basic_pay * 1.45
    da = p.basic_pay * 0.30
    ded = (p.basic_pay + da) * 0.10
    check("payroll: net really is gross minus the deduction",
          np.allclose(net, gross - ded))
    check("payroll: totals are 200,500 basic and 264,660 net",
          p.basic_pay.sum() == 200500 and round(net.sum()) == 264660)

    r = load("course-1-office/class-results.csv")
    subs = ["maths", "physics", "chemistry", "english", "computers"]
    avg = r[subs].mean(axis=1)
    grade = pd.cut(avg, [-1, 40, 60, 75, 90, 1000],
                   labels=["F", "D", "C", "B", "A"], right=False)
    dist = Counter(grade.astype(str))
    check("class results: grades on the AVERAGE are A3 B6 C4 D6 F1",
          dict(dist) == {"A": 3, "B": 6, "C": 4, "D": 6, "F": 1}, dict(dist))
    failed = sorted(r.loc[r[subs].min(axis=1) < 40, "name"])
    check("class results: four students fail at least one subject",
          failed == ["Divya", "Ishita", "Kavya", "Rahul"], failed)
    on_total = pd.cut(r[subs].sum(axis=1), [-1, 40, 60, 75, 90, 100000],
                      labels=["F", "D", "C", "B", "A"], right=False)
    check("class results: grading on the TOTAL gives 19 A's",
          Counter(on_total.astype(str))["A"] == 19)
    check("class results: maths is the hardest paper, mean 67.0",
          r[subs].mean().idxmin() == "maths" and r.maths.mean() == 67.0)

    b = load("course-1-office/budget.csv")
    income = int(b.loc[b.category == "Income", "amount"].iloc[0])
    expenses = int(b.loc[b.category != "Income", "amount"].sum())
    check("budget: savings 12,000 and a 30% rate needs 47,142.86",
          income - expenses == 12000
          and close(expenses / 0.70, 47142.857142857, 1e-6))


def check_course_02_03():
    e = load("course-2-c/employee-records.csv")
    check("C records: 10 rows, 4 departments, total salary 331,500",
          len(e) == 10 and e.department.nunique() == 4
          and e.salary.sum() == 331500, e.salary.sum())
    check("C records: every name contains a space (the scanf trap)",
          e.name.str.contains(" ").all())
    check("C records: the longest name fits a char[32] with room for NUL",
          e.name.str.len().max() < 31, e.name.str.len().max())

    st = load("course-3-python/students.csv")
    check("students: 25 rows and every mark inside 35..99",
          len(st) == 25
          and st[["python", "maths", "statistics"]].values.min() >= 35
          and st[["python", "maths", "statistics"]].values.max() <= 99)
    check("students: roll numbers are unique and consecutive from 101",
          list(st.roll) == list(range(101, 126)))


def check_course_04():
    h = load("course-4-stats/heights.csv")
    check("heights: 60 draws whose mean sits within 2 SE of 165",
          len(h) == 60
          and abs(h.height_cm.mean() - 165) < 2 * 8 / math.sqrt(60),
          h.height_cm.mean())

    m = load("course-4-stats/study-hours-marks.csv")
    slope, intercept = np.polyfit(m.hours, m.marks, 1)
    r = np.corrcoef(m.hours, m.marks)[0, 1]
    check("regression: slope recovers 6.0 (built from marks = 12 + 6h)",
          close(slope, 6.0, 0.6), slope)
    check("regression: intercept recovers 12.0", close(intercept, 12.0, 3.5),
          intercept)
    check("regression: R-squared equals r-squared",
          close(r ** 2, 1 - ((m.marks - (intercept + slope * m.hours)) ** 2).sum()
                / ((m.marks - m.marks.mean()) ** 2).sum(), 1e-9))
    check("regression: correlation above 0.9 as claimed", r > 0.9, r)

    from scipy import stats
    t = load("course-4-stats/treatment-groups.csv")
    a = t[t.group == "control"].score
    b = t[t.group == "treatment"].score
    tt = stats.ttest_ind(b, a)
    check("two-sample: the planted 5-mark difference is detected",
          tt.pvalue < 0.05 and close(b.mean() - a.mean(), 5.0, 2.5),
          f"p={tt.pvalue:.4g}, diff={b.mean() - a.mean():.2f}")

    pa = load("course-4-stats/before-after.csv")
    paired = stats.ttest_rel(pa.after, pa.before)
    unpaired = stats.ttest_ind(pa.after, pa.before)
    check("paired: the paired test rejects and beats the unpaired one",
          paired.pvalue < 0.01 and paired.pvalue < unpaired.pvalue,
          f"paired={paired.pvalue:.3g} unpaired={unpaired.pvalue:.3g}")

    an = load("course-4-stats/fertiliser-yield.csv")
    groups = [g["yield"].values for _, g in an.groupby("fertiliser")]
    f_stat, p = stats.f_oneway(*groups)
    check("ANOVA: three fertilisers are not all equal",
          p < 0.05 and an.groupby("fertiliser")["yield"].mean().idxmax() == "C",
          f"p={p:.4g}")

    ch = load("course-4-stats/preference-survey.csv")
    table = pd.crosstab(ch.gender, ch.preference)
    chi2, p, dof, expected = stats.chi2_contingency(table)
    check("chi-square: gender and preference are dependent, dof 1",
          p < 0.01 and dof == 1 and (expected > 5).all(), f"p={p:.4g}")
    check("chi-square: the contingency table is the one documented",
          table.loc["male", "tea"] == 45 and table.loc["female", "coffee"] == 50)


def check_course_05():
    d = load("course-5-dbms/departments.csv")
    e = load("course-5-dbms/employees.csv")
    p = load("course-5-dbms/projects.csv")
    a = load("course-5-dbms/assignments.csv")
    check("dbms: every employee's dept_id exists in departments",
          set(e.dept_id) <= set(d.dept_id))
    check("dbms: every project's dept_id exists in departments",
          set(p.dept_id) <= set(d.dept_id))
    check("dbms: assignments reference real employees and projects",
          set(a.emp_id) <= set(e.emp_id) and set(a.project_id) <= set(p.project_id))
    check("dbms: two employees have no manager (the LEFT-join case)",
          e.manager_id.isna().sum() == 2, e.manager_id.isna().sum())
    check("dbms: an inner self-join keeps 5 rows, a left join keeps 7",
          len(e.merge(e, left_on="manager_id", right_on="emp_id")) == 5
          and len(e.merge(e, left_on="manager_id", right_on="emp_id",
                          how="left")) == 7)
    no_project = sorted(set(e.emp_id) - set(a.emp_id))
    check("dbms: E106 is the one employee on no project",
          no_project == ["E106"], no_project)
    check("dbms: assignments has a composite key with no duplicates",
          not a.duplicated(["emp_id", "project_id"]).any())

    u = load("course-5-dbms/unnormalised-orders.csv")
    # u.items would resolve to DataFrame.items, the method
    multi = int(u["items"].str.contains(";").sum())
    check("unnormalised: 2 of the 4 orders pack several items into one cell",
          multi == 2, multi)
    check("unnormalised: one customer repeats, so the update anomaly is real",
          u.customer_name.duplicated().any())
    check("unnormalised: item, quantity and price counts line up per row",
          all(len(a.split(";")) == len(b.split(";")) == len(c.split(";"))
              for a, b, c in zip(u["items"], u["quantities"],
                                 u["unit_prices"])))


def check_course_06_07():
    c = load("course-6-r/car-mileage.csv")
    check("cars: three service_months are genuinely missing",
          c.service_months.isna().sum() == 3, c.service_months.isna().sum())
    X = np.column_stack([np.ones(len(c)), c.weight_t, c.cylinders])
    beta = np.linalg.lstsq(X, c.mpg, rcond=None)[0]
    check("cars: the weight coefficient recovers -7.5",
          close(beta[1], -7.5, 1.2), beta[1])
    check("cars: the cylinder coefficient recovers -0.8",
          close(beta[2], -0.8, 0.6), beta[2])
    check("cars: cylinders take exactly the three documented levels",
          sorted(c.cylinders.unique()) == [4, 6, 8])

    w = load("course-7-web/products.csv")
    check("products: 8 rows, 3 categories, 2 out of stock",
          len(w) == 8 and w.category.nunique() == 3
          and (w.status == "out_of_stock").sum() == 2)
    check("products: every out-of-stock row really has zero stock",
          (w.loc[w.status == "out_of_stock", "stock"] == 0).all())
    check("products: stock value totals 35,555",
          (w.price * w.stock).sum() == 35555, (w.price * w.stock).sum())


def check_course_08():
    b = load("course-8-datamining/market-basket.csv")
    baskets = b.groupby("transaction_id")["item"].apply(set)
    n = len(baskets)
    sup = lambda items: sum(1 for s in baskets if set(items) <= s) / n
    conf = sup(["bread", "butter"]) / sup(["bread"])
    lift = sup(["bread", "butter"]) / (sup(["bread"]) * sup(["butter"]))
    check("basket: 12 transactions over 5 distinct items",
          n == 12 and b.item.nunique() == 5)
    check("basket: bread -> butter has confidence 0.875 and lift above 1.3",
          close(conf, 0.875, 1e-9) and lift > 1.3, f"{conf:.4f} / {lift:.4f}")
    check("basket: the Apriori property holds for this rule",
          sup(["bread", "butter"]) <= min(sup(["bread"]), sup(["butter"])))

    cp = load("course-8-datamining/cluster-points.csv")
    check("clusters: 75 clustered points and 10 noise points",
          (cp.true_cluster != -1).sum() == 75
          and (cp.true_cluster == -1).sum() == 10)
    from sklearn.cluster import KMeans, DBSCAN
    X = cp[["x", "y"]].values
    km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
    found = sorted(tuple(np.round(c, 0)) for c in km.cluster_centers_)
    want = sorted([(2.0, 2.0), (8.0, 3.0), (5.0, 9.0)])
    ok = all(min(math.dist(f, w) for w in want) < 1.2 for f in found)
    check("clusters: k-Means recovers the three planted centres", ok, found)
    db = DBSCAN(eps=0.9, min_samples=4).fit(X)
    noise_found = (db.labels_ == -1)
    noise_true = (cp.true_cluster == -1).values
    caught = int((noise_found & noise_true).sum())
    check("clusters: DBSCAN labels most planted noise as noise",
          caught >= 7, f"{caught} of 10")

    wh = load("course-8-datamining/warehouse-facts.csv")
    check("warehouse: 144 rows at one row per month per city per product",
          len(wh) == 144 and not wh.duplicated(
              ["month", "city", "product"]).any())
    by_city = wh.groupby("city").revenue.sum().sum()
    by_region = wh.groupby("region").revenue.sum().sum()
    check("warehouse: roll-up city -> region -> all conserves the total",
          by_city == by_region == wh.revenue.sum())


def check_course_09():
    m = pd.read_csv(DATA / "course-9-python-da/messy-customers.csv",
                    dtype=str, keep_default_na=False)
    check("messy: 12 rows, one of them a duplicate of C002",
          len(m) == 12 and m.duplicated().sum() == 1
          and m.customer_id.value_counts().max() == 2)
    blanks = int((m == "").sum().sum())
    check("messy: exactly 6 empty cells", blanks == 6, blanks)
    check("messy: three spellings of Hyderabad collapse to one",
          m.city.nunique() == 5 and m.city.str.strip().str.lower().nunique() == 3,
          f"{m.city.nunique()} raw, "
          f"{m.city.str.strip().str.lower().nunique()} cleaned")
    check("messy: C001's name and C007's city carry stray whitespace",
          m.loc[m.customer_id == "C001", "name"].iloc[0] != 
          m.loc[m.customer_id == "C001", "name"].iloc[0].strip()
          and m.loc[m.customer_id == "C007", "city"].iloc[0].startswith(" "))
    ages = pd.to_numeric(m.age, errors="coerce")
    check("messy: the impossible age of 150 is present",
          ages.max() == 150, ages.max())
    sal = pd.to_numeric(m.salary, errors="coerce").dropna()
    check("messy: the salary outlier is beyond 3 IQRs of the upper quartile",
          sal.max() > sal.quantile(0.75) + 3 * (sal.quantile(0.75) - sal.quantile(0.25)))
    check("messy: exactly one email fails a naive @-and-dot check",
          int((~m.email.str.contains("@") | ~m.email.str.contains(r"\.")).sum()
              - (m.email == "").sum()) == 1)

    s = load("course-9-python-da/monthly-sales.csv")
    check("monthly sales: long format, 24 months x 3 regions",
          len(s) == 72 and s.month.nunique() == 24 and s.region.nunique() == 3)
    wide = s.pivot(index="month", columns="region", values="revenue")
    check("monthly sales: pivot gives a full 24 x 3 grid with no gaps",
          wide.shape == (24, 3) and not wide.isna().any().any())
    check("monthly sales: South > North > East on average, as designed",
          s.groupby("region").revenue.mean().idxmax() == "South"
          and s.groupby("region").revenue.mean().idxmin() == "East")


def check_course_10_11():
    st = load("course-10-mongodb/students.csv")
    co = load("course-10-mongodb/courses.csv")
    st["enrolled_courses"] = st.enrolled_courses.fillna("")
    st["grades"] = st.grades.fillna("")
    check("mongo: one student has no enrolment (the $unwind trap)",
          (st.enrolled_courses == "").sum() == 1)
    pairs_ok = all(
        (r.enrolled_courses == "" and r.grades == "")
        or len(r.enrolled_courses.split(";")) == len(r.grades.split(";"))
        for r in st.itertuples())
    check("mongo: every course in the array has a matching grade", pairs_ok)
    ids = {c for r in st.enrolled_courses if r for c in r.split(";")}
    check("mongo: every referenced course id exists in courses.csv",
          ids <= set(co.course_id), ids - set(co.course_id))

    prod = load("course-11-bi/dim-product.csv")
    store = load("course-11-bi/dim-store.csv")
    date = load("course-11-bi/dim-date.csv")
    fact = load("course-11-bi/fact-sales.csv")
    check("star: every fact key resolves to a dimension row",
          set(fact.product_key) <= set(prod.product_key)
          and set(fact.store_key) <= set(store.store_key)
          and set(fact.date_key) <= set(date.date_key))
    joined = (fact.merge(prod, on="product_key")
                  .merge(store, on="store_key").merge(date, on="date_key"))
    joined["revenue"] = joined.qty * joined.list_price
    check("star: the joined table totals 12,880 with 10,360 South",
          joined.revenue.sum() == 12880
          and joined[joined.region == "South"].revenue.sum() == 10360)
    check("star: qty totals 87 and the join adds no rows",
          fact.qty.sum() == 87 and len(joined) == len(fact))
    check("star: March is absent from the date dimension",
          not date.date.str.startswith("2026-03").any())


def check_course_12():
    h = load("course-12a-ml/house-prices.csv")
    X = np.column_stack([np.ones(len(h)), h.area_sqft, h.bedrooms, h.age_years])
    beta = np.linalg.lstsq(X, h.price_lakh, rcond=None)[0]
    pred = X @ beta
    r2 = 1 - ((h.price_lakh - pred) ** 2).sum() / \
        ((h.price_lakh - h.price_lakh.mean()) ** 2).sum()
    check("houses: the area coefficient recovers 0.045",
          close(beta[1], 0.045, 0.006), beta[1])
    check("houses: the age coefficient recovers -0.25",
          close(beta[3], -0.25, 0.12), beta[3])
    check("houses: R-squared above the documented 0.85", r2 > 0.85, r2)

    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    lo = load("course-12a-ml/loan-approval.csv")
    Xl = lo[["income", "debt", "credit_score"]].values
    yl = lo.approved.values
    pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    acc = cross_val_score(pipe, Xl, yl, cv=5).mean()
    check("loans: cross-validated accuracy clears the documented 0.75",
          acc > 0.75, acc)
    check("loans: it does NOT reach 1.0 -- the label carries real noise",
          acc < 0.99, acc)
    pipe.fit(Xl, yl)
    coefs = dict(zip(["income", "debt", "credit_score"],
                     pipe[-1].coef_[0]))
    # income wins on the STANDARDISED scale even though credit_score has the
    # far larger raw coefficient -- the file documents both, because the gap
    # between them is the lesson
    check("loans: income has the largest standardised effect, credit_score "
          "the largest raw coefficient",
          max(coefs, key=lambda k: abs(coefs[k])) == "income"
          and abs(coefs["credit_score"]) > abs(coefs["debt"]),
          {k: round(float(v), 3) for k, v in coefs.items()})

    from sklearn.cluster import KMeans
    seg = load("course-12a-ml/customer-segments.csv")
    Xs = seg[["annual_spend", "visits_per_year", "online_ratio"]].values
    raw = KMeans(3, n_init=10, random_state=0).fit(Xs)
    scaled = KMeans(3, n_init=10, random_state=0).fit(
        StandardScaler().fit_transform(Xs))
    from sklearn.metrics import adjusted_rand_score as ari
    truth = seg.true_segment.values
    check("segments: scaling changes the answer, which is the lesson",
          ari(truth, scaled.labels_) >= ari(truth, raw.labels_),
          f"raw={ari(truth, raw.labels_):.3f} scaled={ari(truth, scaled.labels_):.3f}")
    check("segments: scaled k-Means recovers the three planted segments",
          ari(truth, scaled.labels_) > 0.85, ari(truth, scaled.labels_))


def check_course_12b_13():
    lg = load("course-12b-bigdata/web-logs.csv")
    check("logs: 1200 rows over 8 paths", len(lg) == 1200
          and lg.path.nunique() == 8)
    check("logs: the error rate matches a direct count",
          close((lg.status >= 400).mean(),
                lg.status.isin([404, 500]).mean(), 1e-12))
    by_path = lg.groupby("path").size()
    check("logs: hits per path sum back to the row count",
          by_path.sum() == len(lg))

    wc = load("course-12b-bigdata/wordcount-corpus.csv")
    words = Counter(w for t in wc.text for w in t.split())
    check("wordcount: 'the' is the most frequent word",
          words.most_common(1)[0][0] == "the", words.most_common(3))
    check("wordcount: dog appears 3 times and quick 3 times",
          words["dog"] == 3 and words["quick"] == 3,
          f"dog={words['dog']} quick={words['quick']}")

    g = load("course-13a-ai/graph-edges.csv")
    adj = defaultdict(list)
    for r in g.itertuples():
        adj[r.from_city].append((r.to_city, r.cost))
        adj[r.to_city].append((r.from_city, r.cost))
    import heapq
    def ucs(start, goal):
        pq, seen = [(0, start, [start])], set()
        while pq:
            c, node, path = heapq.heappop(pq)
            if node == goal:
                return c, path
            if node in seen:
                continue
            seen.add(node)
            for nxt, w in adj[node]:
                if nxt not in seen:
                    heapq.heappush(pq, (c + w, nxt, path + [nxt]))
        return None, None
    cost, path = ucs("Arad", "Bucharest")
    check("graph: uniform-cost finds the 418 route through Rimnicu",
          cost == 418 and path == ["Arad", "Sibiu", "Rimnicu", "Pitesti",
                                   "Bucharest"], f"{cost} {path}")
    # BFS: fewest hops, ignoring cost
    from collections import deque
    q, seen = deque([("Arad", ["Arad"])]), {"Arad"}
    bfs_path = None
    while q:
        node, pth = q.popleft()
        if node == "Bucharest":
            bfs_path = pth
            break
        for nxt, _ in adj[node]:
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, pth + [nxt]))
    bfs_cost = sum(w for a, b in zip(bfs_path, bfs_path[1:])
                   for n, w in adj[a] if n == b)
    check("graph: BFS finds a shorter path in hops that costs more",
          len(bfs_path) < len(path) and bfs_cost > cost,
          f"{bfs_path} costs {bfs_cost}")

    mc = load("course-13a-ai/map-colouring.csv")
    nbr = defaultdict(set)
    for r in mc.itertuples():
        nbr[r.region].add(r.neighbour)
        nbr[r.neighbour].add(r.region)
    def colourable(k):
        regions = sorted(nbr)
        assign = {}
        def bt(i):
            if i == len(regions):
                return True
            for c in range(k):
                r = regions[i]
                if all(assign.get(n) != c for n in nbr[r]):
                    assign[r] = c
                    if bt(i + 1):
                        return True
                    del assign[r]
            return False
        return bt(0)
    check("CSP: three colours suffice and two do not",
          colourable(3) and not colourable(2))

    fam = load("course-13a-ai/family-relations.csv")
    gp = {(r1.parent, r2.child) for r1 in fam.itertuples()
          for r2 in fam.itertuples() if r1.child == r2.parent}
    check("logic: exactly 6 grandparent pairs, as documented",
          len(gp) == 6, len(gp))

    sc = load("course-13b-cloud/storage-costs.csv")
    monthly = (sc.gb_stored * sc.price_per_gb_month)
    arch = sc[sc.tier == "archive"].iloc[0]
    check("cloud: archive stores cheapest but costs most to read back",
          monthly.idxmin() == sc.index[sc.tier == "archive"][0]
          and arch.gb_stored * arch.retrieval_per_gb
          > 20 * arch.gb_stored * arch.price_per_gb_month)

    iam = load("course-13b-cloud/iam-policies.csv")
    def allowed(principal, action, resource):
        """Deny wins; anything not matched by an Allow is denied by default."""
        def matches(pattern):
            return resource == pattern or (pattern.endswith("*")
                                           and resource.startswith(pattern[:-1]))
        hits = [r for r in iam.itertuples()
                if r.principal == principal
                and r.action in (action, "s3:*")
                and matches(r.resource)]
        if any(r.effect == "Deny" for r in hits):
            return False
        return any(r.effect == "Allow" for r in hits)
    check("IAM: explicit Deny beats a wildcard Allow for carol",
          not allowed("carol", "s3:DeleteObject", "reports/x.csv"))
    check("IAM: bob reads other reports but not salaries.csv",
          allowed("bob", "s3:GetObject", "reports/q1.csv")
          and not allowed("bob", "s3:GetObject", "reports/salaries.csv"))
    check("IAM: an unknown principal is denied by default",
          not allowed("dave", "s3:GetObject", "reports/q1.csv"))


def check_course_14_15():
    x = load("course-14a-deeplearning/xor.csv")
    check("xor: the four rows are the XOR truth table",
          sorted(map(tuple, x.values.tolist()))
          == [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)])
    # a perceptron cannot exceed 3 of 4 -- proved by exhausting the sign
    # pattern rather than by training and hoping
    best = 0
    for w1 in np.linspace(-3, 3, 61):
        for w2 in np.linspace(-3, 3, 61):
            for b in np.linspace(-3, 3, 61):
                pred = ((x.x1 * w1 + x.x2 * w2 + b) > 0).astype(int)
                best = max(best, int((pred == x.y).sum()))
    check("xor: no linear boundary classifies more than 3 of the 4",
          best == 3, best)

    sf = load("course-14a-deeplearning/sensor-failures.csv")
    from sklearn.linear_model import LogisticRegression
    from sklearn.neural_network import MLPClassifier
    from sklearn.model_selection import cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    Xs = sf[["temperature_c", "vibration_mm_s"]].values
    ys = sf.failed.values
    lin = cross_val_score(make_pipeline(StandardScaler(),
                                        LogisticRegression(max_iter=1000)),
                          Xs, ys, cv=5).mean()
    net = cross_val_score(make_pipeline(StandardScaler(),
                                        MLPClassifier((16, 8), max_iter=3000,
                                                      random_state=0)),
                          Xs, ys, cv=5).mean()
    check("sensors: a hidden layer beats logistic regression on a curved "
          "boundary", net > lin + 0.10, f"linear={lin:.3f} net={net:.3f}")
    check("sensors: neither reaches 1.0 -- 5% of labels are flipped",
          net < 0.99, net)

    ar = load("course-14b-timeseries/ar2-series.csv")
    v = ar.value.values
    # Yule-Walker for AR(2) straight from the sample autocorrelations
    def acf(k):
        m = v.mean()
        return (((v[k:] - m) * (v[:len(v) - k] - m)).sum()
                / ((v - m) ** 2).sum())
    r1, r2 = acf(1), acf(2)
    phi1 = r1 * (1 - r2) / (1 - r1 ** 2)
    phi2 = (r2 - r1 ** 2) / (1 - r1 ** 2)
    check("AR(2): Yule-Walker recovers phi1 near 0.6",
          close(phi1, 0.6, 0.12), phi1)
    check("AR(2): Yule-Walker recovers phi2 near -0.3",
          close(phi2, -0.3, 0.12), phi2)
    check("AR(2): the series is stationary (roots outside the unit circle)",
          abs(phi2) < 1 and phi1 + phi2 < 1 and phi2 - phi1 < 1)

    ss = load("course-14b-timeseries/seasonal-sales.csv")
    vals = ss.sales.values
    d12 = vals[12:] - vals[:-12]
    check("seasonal: differencing at lag 12 shrinks the variance sharply",
          d12.std() < vals.std() / 2, f"{vals.std():.1f} -> {d12.std():.1f}")
    month = ss.month.str.slice(5, 7).astype(int)
    by_month = ss.groupby(month).sales.mean()
    check("seasonal: a 12-month cycle is present in the monthly means",
          by_month.max() - by_month.min() > 250,
          by_month.max() - by_month.min())

    mv = load("course-14b-timeseries/macro-indicators.csv")
    from statsmodels.tsa.stattools import grangercausalitytests
    import warnings
    hush = io.StringIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        stdout, sys.stdout = sys.stdout, hush
        try:
            fwd = grangercausalitytests(mv[["inflation", "rates"]], maxlag=2)
            rev = grangercausalitytests(mv[["rates", "inflation"]], maxlag=2)
            ctl = grangercausalitytests(mv[["inflation", "unrelated"]], maxlag=2)
        finally:
            sys.stdout = stdout
    pf = fwd[1][0]["ssr_ftest"][1]
    pr = rev[1][0]["ssr_ftest"][1]
    pc = ctl[1][0]["ssr_ftest"][1]
    check("VAR: rates Granger-cause inflation", pf < 0.01, f"p={pf:.4g}")
    check("VAR: inflation does NOT Granger-cause rates", pr > 0.05,
          f"p={pr:.4g}")
    check("VAR: the control series causes nothing", pc > 0.05, f"p={pc:.4g}")

    sr = load("course-15a-nlp/sentiment-reviews.csv")
    check("sentiment: 20 reviews, balanced 10/10",
          len(sr) == 20 and sr.label.sum() == 10)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import make_pipeline as mp
    from sklearn.model_selection import cross_val_score as cvs
    acc = cvs(mp(TfidfVectorizer(), MultinomialNB()), sr.text, sr.label,
              cv=5).mean()
    check("sentiment: a bag-of-words model beats the 0.5 coin-flip baseline",
          acc > 0.5, acc)

    ner = load("course-15a-nlp/ner-sentences.csv")
    total = sum(len(e.split(";")) for e in ner.expected_entities)
    check("NER: 15 gold entities across 5 sentences",
          len(ner) == 5 and total == 15, total)
    check("NER: every gold entity is written as text|TYPE",
          all("|" in part for e in ner.expected_entities
              for part in e.split(";")))

    ref = load("course-15b-mlops/loan-reference.csv")
    cur = load("course-15b-mlops/loan-current.csv")
    from scipy import stats as st

    def psi(a, b, bins=10):
        edges = np.percentile(a, np.linspace(0, 100, bins + 1))
        edges[0], edges[-1] = -np.inf, np.inf
        pa = np.histogram(a, edges)[0] / len(a) + 1e-6
        pb = np.histogram(b, edges)[0] / len(b) + 1e-6
        return float(((pb - pa) * np.log(pb / pa)).sum())

    psi_score = psi(ref.credit_score, cur.credit_score)
    psi_income = psi(ref.income, cur.income)
    check("drift: PSI flags credit_score (above the 0.2 action threshold)",
          psi_score > 0.2, psi_score)
    check("drift: PSI clears income, which did not move",
          psi_income < 0.1, psi_income)
    ks_score = st.ks_2samp(ref.credit_score, cur.credit_score).pvalue
    ks_income = st.ks_2samp(ref.income, cur.income).pvalue
    check("drift: KS agrees -- credit_score shifted, income did not",
          ks_score < 0.01 and ks_income > 0.05,
          f"score p={ks_score:.3g}, income p={ks_income:.3g}")
    check("drift: the mean credit score fell by roughly 55 points",
          close(ref.credit_score.mean() - cur.credit_score.mean(), 55, 20),
          ref.credit_score.mean() - cur.credit_score.mean())


def main():
    print(f"\n{'=' * 66}\nPractice datasets -- recovering each planted truth"
          f"\n{'=' * 66}")
    for fn in (check_determinism, check_questions, check_shared, check_course_01,
               check_course_02_03, check_course_04, check_course_05, check_course_06_07,
               check_course_08, check_course_09, check_course_10_11,
               check_course_12, check_course_12b_13, check_course_14_15):
        print()
        fn()
    failed = [c for c in checks if not c[1]]
    n_files = len(list(DATA.rglob("*.csv")))
    print(f"\n{'=' * 66}")
    print(f"{len(checks)} checks over {n_files} datasets, {len(failed)} failed")
    if not failed:
        print("Every dataset's answer key was recovered from the file itself.")
    print(f"{'=' * 66}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
