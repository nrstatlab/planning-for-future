# Course 9 — Practice Questions with Solutions

Every code block here has been executed on **NumPy 2.4.6 and Pandas 3.0.5**
and its output asserted by
`tools/run_data_labs.py`.

---

## Section A — Two-mark questions

### 1. Distinguish a Python list from a NumPy ndarray.

A list holds **pointers to objects scattered in memory**, each with its own type
tag; an ndarray holds **raw values of one type in a contiguous block**. That
gives the array element-wise arithmetic (`a + b` adds rather than
concatenating), native multidimensional indexing, fixed size, and roughly
50× the speed on a million elements.

### 2. What does `axis=0` mean?

**The axis that disappears.** `a.sum(axis=0)` collapses the row axis, so a
`(2, 3)` array gives a `(3,)` result — one value **per column**. Reading it as
"operate on rows" and expecting a row total is the standard error.

### 3. Distinguish a view from a copy.

A **view** shares memory with the original, so writing through it changes the
original. A **copy** does not.

| Indexing | Returns |
|---|---|
| Basic slice `a[1:4]` | **View** |
| Boolean mask `a[a > 2]` | **Copy** |
| Fancy `a[[0, 2]]` | **Copy** |

Views exist so that slicing a gigabyte array costs nothing. `.copy()` is how
you opt out.

### 4. Why must you write `&` rather than `and` in a mask?

`and` tries to reduce each operand to a **single** True or False, and an array
of booleans has no single truth value — it raises `ValueError: The truth value
of an array with more than one element is ambiguous`. `&` works element-wise.
The parentheses are also mandatory, because `&` binds tighter than `>`.

### 5. What does `ddof` control, and what are the defaults?

The **delta degrees of freedom** — the divisor is *n − ddof*. `ddof=0` is the
**population** formula, `ddof=1` the **sample** formula.

**NumPy defaults to `ddof=0` and Pandas to `ddof=1`.** For
`[2, 4, 4, 4, 5, 5, 7, 9]`, `np.std` gives **2.0** and `pd.Series.std` gives
**2.1381** — the same data, two libraries, two answers. Course 4 taught the
sample formula, so Pandas agrees and NumPy does not.

### 6. Distinguish `.loc` from `.iloc`.

`.loc` selects by **label** and is **inclusive** of its endpoint; `.iloc`
selects by **position** and is **exclusive**. `df.loc[0:2]` gives three rows,
`df.iloc[0:2]` gives two.

Labels are inclusive because you often do not know what follows `"maths"`, so
`df.loc[:, "name":"maths"]` has to include `maths` to be usable.

### 7. What is data alignment?

Pandas **matches on the index before computing**. `a + b` pairs label with
label, not position with position, and labels present in only one operand
become NaN. NumPy would add mismatched pairs and give a plausible wrong answer;
alignment turns that silent bug into a visible NaN.

### 8. What does `SettingWithCopyWarning` mean?

That Pandas cannot tell whether the object you are assigning to is a view or a
copy of the original, so it cannot tell whether the assignment will reach it.

**Under Pandas 3 the warning is gone** — copy-on-write makes the answer
consistent: the original is **never** modified, and nothing is printed. The
unpredictability is gone; the bug is not, and it now fails silently. Use
`df.loc[mask, "col"] = x` to modify, or `.copy()` to work separately.

### 9. Why does `df[df.x == np.nan]` never return anything?

IEEE 754 defines NaN to compare unequal to everything, itself included, so
`np.nan == np.nan` is `False`. Use `.isna()`.

### 10. Why does one NaN turn an integer column into float?

There is no NaN value in the int64 type, so the whole column is upcast to
float64 to hold it. **Nullable dtypes** — capital-I `Int64` — keep the integer
type and use `pd.NA`.

### 11. Distinguish `cut` from `qcut`.

`cut` makes **equal-width** bins (or bins at boundaries you supply); `qcut`
makes **equal-frequency** bins (quantiles). Exactly Course 8 Unit 2 §2.9's
distinction. `cut`'s intervals are **right-closed by default**, so a mark of
exactly 40 falls in `(0, 40]`.

### 12. Distinguish `merge` from `concat`.

`concat` **stacks** — rows or columns, no key needed, like SQL's `UNION ALL`.
`merge` **matches on a key**, like SQL's `JOIN`.

### 13. Name the four join types.

| `how` | Keeps | SQL |
|---|---|---|
| `inner` (default) | Keys in both | `INNER JOIN` |
| `left` | All left rows | `LEFT OUTER JOIN` |
| `right` | All right rows | `RIGHT OUTER JOIN` |
| `outer` | The union of keys | `FULL OUTER JOIN` |

### 14. Why use `validate=` on a merge?

Because duplicate keys on both sides produce the **Cartesian product** of
matching rows — 3 × 4 duplicates become 12 rows — silently. `validate="one_to_one"`
turns that data corruption into an immediate error.

### 15. Distinguish `pivot` from `pivot_table`.

`pivot` is a **pure reshape** and raises if any index/column pair is duplicated.
`pivot_table` **aggregates**, so duplicates are fine — and it silently averages
them unless you choose `aggfunc`, which you must actually want.

### 16. Distinguish `agg` from `transform`.

`agg` returns **one row per group**; `transform` returns **one value per
original row**. Use `transform` to attach a group statistic back as a column —
`agg` gives a length mismatch.

### 17. Distinguish `size` from `count` in a groupby.

`size()` counts **all rows** per group; `count()` counts **non-null values**.
They differ by exactly the number of missing values.

### 18. Distinguish a histogram from a bar chart.

A **histogram** shows the distribution of **one continuous variable** — the
bars are bins and touch, because the axis is continuous. A **bar chart**
compares **categories** — the bars have gaps, because there is nothing between
"DS" and "Stats".

### 19. What is the dummy variable trap?

With *k* categories, *k* one-hot columns sum to 1 in every row, so they are
**perfectly collinear** and `XᵀX` is singular — a linear or logistic regression
cannot solve it uniquely. `drop_first=True` gives *k − 1* columns with one
category absorbed into the intercept. **Tree models do not care** and are
better off with all *k*.

### 20. Why must `random_state` be set?

Because an unseeded split cannot be reproduced, so neither can any accuracy
measured on it — and a result nobody can reproduce is not a result.

---

## Section B — Five-mark questions

### 1. Explain broadcasting with the rules and examples.

When shapes differ, NumPy **stretches** the smaller operand without copying,
comparing dimensions from the **trailing** end backwards:

1. Dimensions are compatible if they are **equal** or if **one is 1**.
2. A missing dimension is treated as 1.

```
(3, 4) + (4,)     ->  (4,) becomes (1,4) -> stretched to (3,4)   ✓
(3, 4) + (3, 1)   ->  the 1 stretches to 4                        ✓
(3, 4) + (3,)     ->  trailing 4 vs 3 — INCOMPATIBLE              ✗
```

```python
a = np.array([[1, 2, 3], [4, 5, 6]])       # (2, 3)
a + 10                                      # scalar to everything
a + np.array([10, 20, 30])                  # (3,) -> each ROW
a - a.mean(axis=0)                          # centre each COLUMN
a - a.mean(axis=1, keepdims=True)           # centre each ROW
```

**`keepdims=True` is the point of the last line.** `a.mean(axis=1)` has shape
`(2,)`, whose trailing dimension 2 does not match 3, so it raises. `keepdims`
gives `(2, 1)`, which broadcasts correctly. This exact error is extremely
common.

### 2. Explain indexing in NumPy — basic, boolean and fancy.

```python
a = np.arange(10)
a[2:5]          # basic slice -> a VIEW
a[a > 5]        # boolean mask -> a COPY
a[[0, 2, 4]]    # fancy -> a COPY

m = np.arange(12).reshape(3, 4)
m[1, 2]         # comma, not m[1][2]
m[:, 1]         # a whole column
m[[0,1,2], [1,2,3]]   # PAIRED -> three elements, not a 3x3 block
m[np.ix_([0,2],[1,3])] # the submatrix
```

The view/copy behaviour is the examinable part: a slice can always be expressed
as a start/stop/stride over the same memory, so it is a view; an arbitrary list
of indices cannot, so NumPy must copy.

Boolean masking needs `&`, `|`, `~` with parentheses, and
`(cond).sum()` / `(cond).mean()` give a count and a proportion.

### 3. Explain the methods of handling missing data.

| Method | When | Danger |
|---|---|---|
| `dropna()` | Few rows, missing at random | Aggressive — one NaN removes the whole row |
| Mean | Numeric, symmetric | **Shrinks the variance** |
| Median | Numeric, **skewed** | Same, but robust |
| Mode | Categorical | — |
| `ffill` / `interpolate` | **Ordered** data only | Meaningless on unordered rows |
| Model-based (`KNNImputer`) | Accuracy matters | Costly; can invent structure |

Three points carry the marks. **Why** a value is missing matters — MNAR data
(high earners declining to state income) biases the result when dropped, and
nothing in the data reveals it. **Mean imputation shrinks the standard
deviation** — the lab measures a 16% loss at 30% missingness — weakening every
correlation. And **impute after splitting**, never before, or the training set
encodes the test set's mean.

### 4. Explain `map`, `apply`, `applymap` and `transform`.

| Tool | Input | Returns |
|---|---|---|
| `Series.map` | Series | Same length; substitutes from a dict or function |
| `Series.apply` | Series | Same length or a scalar |
| `DataFrame.apply` | Column (or row with `axis=1`) | Aggregated or same-shape |
| `DataFrame.map` (was `applymap`) | Each cell | Same shape |
| `transform` | Series or group | **Same shape as the input** |

```python
df.dept.map({"DS": "Data Science"})            # unmapped keys become NaN
df.dept.replace({"DS": "Data Science"})        # unmatched values are LEFT ALONE
df.groupby("dept").marks.transform("mean")     # the group mean, per ROW
```

**`map` with an incomplete dictionary silently produces NaN**; `replace` does
not. And all four call a Python function per element or row, so
`df.maths + df.stats` is around **2,900×** faster than the equivalent
`apply(axis=1)` on 200,000 rows — measured in the lab.

### 5. Explain outlier detection by z-score and IQR, and compare them.

```python
# z-score
z = (s - s.mean()) / s.std();  outliers = s[z.abs() > 3]

# IQR
q1, q3 = s.quantile([0.25, 0.75]);  iqr = q3 - q1
outliers = s[(s < q1 - 1.5*iqr) | (s > q3 + 1.5*iqr)]
```

On `[10, 12, 11, 13, 12, 11, 250, 260]`:

| Rule | Found |
|---|---|
| z-score, \|z\| > 3 | **0** |
| IQR, 1.5× | **2** |

**The z-score rule fails because of masking.** The two large values pull the
mean to 72.4 and inflate the standard deviation to 112.8, so three standard
deviations is a band of ±338 that comfortably contains both. The outliers have
concealed themselves by corrupting the very statistics used to find them.

**The IQR rule is immune** because quartiles depend on the *rank* of values,
not their magnitude: Q1 and Q3 sit at 11.0 and 72.25 whether the largest value
is 250 or 250,000.

**Use robust statistics to detect outliers**, and always investigate before
deleting — the outlier may be the fraud you were hired to find.

### 6. Explain merging, with all four join types.

Given `students` (rolls 21–24) and `marks` (rolls 21, 22, 23, 25):

| `how` | Rows | Keys |
|---|:---:|---|
| `inner` | 3 | 21, 22, 23 |
| `left` | 4 | 21–24; Kiran's marks NaN |
| `right` | 4 | 21, 22, 23, 25; roll 25's name NaN |
| `outer` | 5 | 21–25 |

```python
m = pd.merge(students, marks, on="roll", how="outer", indicator=True)
m._merge.value_counts()      # both 3, left_only 1, right_only 1
```

**`indicator=True` answers the question you actually have** — "why did I get
three rows instead of four?" — and `validate="one_to_one"` catches the
Cartesian-product explosion from duplicate keys.

Three things break merges in practice: **dtype mismatch** (int64 versus object
matches nothing and returns an empty frame with no error), **whitespace and
case** in the key, and **NaN keys**, which never match anything.

### 7. Explain split–apply–combine.

```
SPLIT by key -> APPLY a function per group -> COMBINE into one result
```

```python
df.groupby("dept").marks.mean()
df.groupby("dept").agg(avg=("marks","mean"), n=("marks","size"))   # named agg
df.groupby(["dept","year"]).marks.mean()
df.groupby("dept").filter(lambda g: len(g) >= 3)   # whole groups kept or dropped
df["dept_mean"] = df.groupby("dept").marks.transform("mean")
```

The four methods differ in what they return: `agg` one row per group,
`transform` one value per original row, `filter` a subset of rows, `apply`
anything. **`transform` is what attaches a group statistic back as a column.**

Check a share calculation by asserting it sums to 100 within each group — that
catches a mis-grouped denominator immediately.

### 8. Compare matplotlib, Seaborn and Plotly.

| | matplotlib | Seaborn | Plotly |
|---|---|---|---|
| Output | Static image | Static image | **Interactive HTML** |
| Input | Arrays | **DataFrames** | **DataFrames** |
| Grouping | Manual loop | `hue=`, `col=` | `color=` |
| Statistics | You compute them | **Computed** — CI, KDE, regression | Some |
| Control | **Total** | Less | Less |
| Works in print | Yes | Yes | **No** |

**Seaborn for exploring, matplotlib for the final static figure, Plotly when
someone needs to interact.** Seaborn returns matplotlib axes, so you can start
in one and finish in the other — which is what most people do.

Use matplotlib's **object-oriented** interface (`fig, ax = plt.subplots()`),
not `pyplot`'s stateful one, which breaks as soon as you have two plots or a
function. On a server, set `matplotlib.use("Agg")` before importing pyplot.

---

## Section C — Ten-mark questions

### 1. A complete cleaning pipeline for a messy CSV

**Question.** The file has roll numbers with leading zeros, dates as
`DD-MM-YYYY`, missing values as `"-"` and `"NA"`, `-999` for absent students,
column names with trailing spaces, and some duplicated students.

**Solution.**

```python
import pandas as pd, numpy as np

# 1. LOAD with the right options -- fixing these later is harder
df = pd.read_csv(
    "marks.csv",
    dtype={"roll": str},                  # preserve leading zeros
    na_values=["-", "NA", "N/A", "?", ""],
    parse_dates=["exam_date"],
    date_format="%d-%m-%Y",               # DD-MM-YYYY, not the US order
)

# 2. COLUMN NAMES first -- everything below depends on them
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# 3. SENTINELS to NaN, BEFORE any statistic is computed
df["marks"] = df.marks.replace(-999, np.nan)

# 4. INSPECT -- never impute blind
print(df.dtypes)
print(df.isna().sum())
print(f"worst column is {df.isna().mean().max():.1%} missing")

# 5. RECORD the missingness, then impute
df["marks_was_missing"] = df.marks.isna().astype(int)
df["marks"] = df.marks.fillna(df.marks.median())   # median: marks are skewed

# 6. DOMAIN rules before statistical ones
df = df[df.marks.between(0, 100)]

# 7. DEDUPLICATE on the key that defines identity
df = df.drop_duplicates(subset=["roll"], keep="last")

# 8. DERIVE features
df["grade"] = pd.cut(df.marks, [0, 40, 60, 75, 100],
                     labels=["Fail", "Pass", "First", "Distinction"])
df["year"] = df.exam_date.dt.year
```

**The order is the examinable part.**

**Column names first**, or every later reference breaks. **Sentinels before
statistics**, or the median you impute with is itself corrupted by the −999s —
this is the single most consequential ordering decision in the pipeline.
**Domain rules before outlier rules**, because a mark of 150 is invalid
whatever the quartiles say. **Deduplicate on the key**, not on whole rows: two
records for the same student differing by one typo are not fully duplicated, so
a bare `drop_duplicates()` misses them.

`date_format` is not optional: without it, `03-04-2026` is ambiguous and may be
read as 4 March.

Step 5's indicator column matters — Course 8 §2.5's point that **the fact of
missingness is itself information**, and often predictive.

### 2. Merge, reshape, aggregate and visualise

**Question.** Given a students table and a long marks table, produce a
department × subject table of means, add each student's rank in their
department, and plot the distribution.

**Solution.**

```python
students = pd.DataFrame({"roll": [21, 22, 23, 24, 25],
                         "name": ["Asha","Ravi","Meena","Kiran","Bhanu"],
                         "dept": ["DS","DS","Stats","DS","Stats"]})
long = pd.DataFrame({
    "roll":    [21,21,22,22,23,23,24,24,25,25],
    "subject": ["maths","stats"]*5,
    "marks":   [88,91,65,58,94,89,71,66,52,47]})

# 1. MERGE -- validate, so a duplicate key cannot silently multiply rows
df = pd.merge(students, long, on="roll", how="inner", validate="one_to_many")
assert len(df) == 10

# 2. RESHAPE long -> wide
wide = df.pivot(index="name", columns="subject", values="marks")
wide["total"] = wide.maths + wide.stats

# 3. AGGREGATE: department x subject means, with totals
table = pd.pivot_table(df, index="dept", columns="subject", values="marks",
                       aggfunc="mean", margins=True, margins_name="All")

# 4. RANK within department -- method="min" so a tie still yields a rank 1
flat = df.pivot_table(index=["dept","name"], columns="subject",
                      values="marks").reset_index()
flat["total"] = flat.maths + flat.stats
flat["dept_rank"] = flat.groupby("dept").total.rank(ascending=False,
                                                    method="min")
flat["dept_mean"] = flat.groupby("dept").total.transform("mean")
flat["above_mean"] = flat.total > flat.dept_mean

# 5. VISUALISE
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].hist(df.marks, bins=8, color="#2b4c7e", edgecolor="white")
axes[0].set_title("Distribution of marks")
axes[0].set_xlabel("Marks"); axes[0].set_ylabel("Frequency")

df.boxplot(column="marks", by="dept", ax=axes[1])
axes[1].set_title("Marks by department"); axes[1].set_xlabel("Department")

axes[2].scatter(wide.maths, wide.stats, s=60, color="#2b8a3e")
axes[2].set_xlabel("Maths"); axes[2].set_ylabel("Statistics")
axes[2].set_title("Maths vs Statistics")

fig.suptitle(""); fig.tight_layout()
fig.savefig("overview.png", dpi=150, bbox_inches="tight")
plt.close(fig)
```

**Four decisions earn the marks.**

`validate="one_to_many"` — `students` has unique rolls, `long` has two rows
each. Stating that relationship makes the merge self-checking.

`pivot` rather than `pivot_table` in step 2 — each `(name, subject)` pair is
unique, so a pure reshape is correct and will **raise** if that assumption ever
breaks, rather than silently averaging.

`method="min"` for the rank — with `"average"`, two students tied at the top
both get 1.5 and `dept_rank == 1` finds no topper at all.

`transform("mean")` rather than `agg` in step 4 — `agg` returns one row per
department, which cannot be compared against a five-row frame.

And the **object-oriented** matplotlib interface with **labelled axes**: an
unlabelled axis makes a chart unreadable, and `plt.close(fig)` prevents a
memory leak when this runs in a loop.

### 3. Feature engineering and encoding

**Question.** From `dob`, `income`, `dept` and `skills` (a comma-separated
string), build features suitable for (a) a logistic regression and (b) a random
forest. Explain every difference.

**Solution.**

```python
df["dob"] = pd.to_datetime(df.dob)
TODAY = pd.Timestamp("2026-08-26")

# --- from dates: the raw date is nearly useless; what it IMPLIES is not
df["age"]        = ((TODAY - df.dob).dt.days / 365.25).astype(int)
df["birth_year"] = df.dob.dt.year
df["birth_month"]= df.dob.dt.month

# --- from numbers
df["log_income"] = np.log1p(df.income)          # log(1+x): defined at 0
df["income_band"] = pd.qcut(df.income, 4, labels=["Q1","Q2","Q3","Q4"])

# --- from categories, using group statistics
df["dept_size"] = df.groupby("dept").dept.transform("size")

# --- multi-label: "python,sql" -> two indicator columns, in one call
skills = df.skills.str.get_dummies(sep=",")
```

**(a) For a logistic regression:**

```python
X_lr = pd.concat([
    df[["age", "log_income", "dept_size"]],
    pd.get_dummies(df.dept, prefix="dept", drop_first=True, dtype=int),
    skills,
], axis=1)

from sklearn.preprocessing import StandardScaler
X_lr[["age","log_income","dept_size"]] = StandardScaler().fit_transform(
    X_lr[["age","log_income","dept_size"]])
```

**(b) For a random forest:**

```python
X_rf = pd.concat([
    df[["age", "income", "dept_size"]],          # raw income is fine
    pd.get_dummies(df.dept, prefix="dept", dtype=int),   # ALL k columns
    skills,
], axis=1)
```

**The three differences, and why:**

| | Logistic regression | Random forest |
|---|---|---|
| `drop_first` | **True** | **False** |
| Scaling | **Required** | **Not needed** |
| Log transform | Helps — it linearises | Irrelevant |

**`drop_first`** — *k* dummy columns sum to 1 in every row, so they are
perfectly collinear and `XᵀX` is singular; the regression has no unique
solution. A tree inverts no matrix, and dropping a level would **hide that
category from every split**, so it wants all *k*.

**Scaling** — logistic regression's coefficients and its regularisation
penalty are scale-dependent, so an unscaled income in rupees dominates an age
in years. A tree splits on the **order** of values, which scaling does not
change, so it is exactly invariant to it.

**The log transform** — regression assumes a roughly linear relationship, and
income is right-skewed; `log1p` makes it closer to linear. A tree can place a
split anywhere, so a monotone transform changes nothing at all.

**And the rule that overrides all three: no leakage.** Every one of these
features must be computable at prediction time, none may be derived from the
target, and every fitted statistic — the scaler, the `qcut` boundaries, the
group sizes — must be **fitted on the training split only** and then applied to
the test set. Fitting the scaler on all the data encodes the test set's mean
into the training features, and the accuracy you then report is not real.
