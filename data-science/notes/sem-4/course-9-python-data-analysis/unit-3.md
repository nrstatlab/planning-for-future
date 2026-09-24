# Unit 3 — Data Input, Output and Cleaning

**Syllabus topics:** Reading and writing data in text format (CSV, TXT),
working with JSON, reading Microsoft Excel files, handling missing data,
dropping and filling missing values, replacing values, renaming axis indexes,
removing duplicates, filtering outliers, transforming data using mapping or
functions.

---

## 3.1 Reading and writing text data

### The readers

```python
pd.read_csv("marks.csv")
pd.read_csv("data.txt", sep="\t")            # or read_table
pd.read_csv("data.txt", sep=r"\s+")          # any run of whitespace
pd.read_excel("book.xlsx", sheet_name="Sem4")
pd.read_json("students.json")
pd.read_sql("SELECT * FROM students", conn)   # Course 5's SQL, straight in
pd.read_html("https://example.com/table")     # every <table> on a page
pd.read_parquet("big.parquet")
pd.read_clipboard()
```

### The parameters that matter

```python
pd.read_csv(
    "marks.csv",
    sep=",",                    # delimiter
    header=0,                   # which row holds the names; None if there is none
    names=["roll", "name", "maths"],   # supply your own
    index_col="roll",           # promote a column to the index
    usecols=["roll", "maths"],  # read only these — saves time and memory
    dtype={"roll": str},        # force a type; str preserves leading zeros
    na_values=["NA", "-", "?", "missing"],   # extra strings meaning missing
    keep_default_na=True,
    parse_dates=["dob"],        # parse as datetime, not string
    skiprows=2,                 # skip junk at the top
    nrows=1000,                 # read only the first n
    encoding="utf-8",
    thousands=",",              # "1,234" -> 1234
    comment="#",
)
```

### ⚠️ Four things that go wrong on real files

**1. Leading zeros disappear.** A roll number `007` is read as the integer 7.
`dtype={"roll": str}` prevents it. Once lost, the zeros cannot be recovered
without knowing the intended width.

**2. Encoding errors.** A `UnicodeDecodeError` means the file is not UTF-8 —
Indian government data is often `latin-1` or `cp1252`. Try
`encoding="latin-1"`, which never fails (though it may mangle characters), then
check the result.

**3. Dates become strings.** Without `parse_dates`, a date column is `object`
dtype and you cannot subtract, sort chronologically, or resample. Always check
`df.dtypes` after loading.

**4. Missing values written as text.** `"NA"`, `"-"`, `"N/A"`, `"null"`, `"?"`,
`"NULL"` and an empty cell are all common. Pandas recognises many by default;
anything unusual needs `na_values`. **If a numeric column loads as text, this is
usually why** — Pandas 3 shows that as dtype `str`, older versions as `object`.

```python
df.dtypes                     # ALWAYS check after reading
df.info()
```

### Writing

```python
df.to_csv("out.csv", index=False)        # index=False almost always
df.to_csv("out.csv", sep="\t", na_rep="NA", float_format="%.2f")
df.to_excel("out.xlsx", sheet_name="Results", index=False)
df.to_json("out.json", orient="records", indent=2)
df.to_parquet("out.parquet")             # typed, compressed, fast
df.to_markdown()                         # for a report
```

**`index=False` matters.** Without it, every write adds an unnamed column, and
a file round-tripped three times acquires `Unnamed: 0`, `Unnamed: 0.1`,
`Unnamed: 0.2`. If you see those, someone forgot.

### 💡 CSV is a bad format, and you will use it anyway

CSV carries no types (everything is text), no schema, no compression, and no
agreed way to quote or escape. **Parquet** fixes all four — it is typed,
columnar, compressed and far faster — and every Pandas installation can read
it. Use CSV for interchange with humans and spreadsheets; use Parquet for
anything you will read back yourself.

## 3.2 Working with JSON

```python
import json

df = pd.read_json("students.json")
df = pd.read_json(text, orient="records")
df.to_json("out.json", orient="records", indent=2)

with open("nested.json") as f:
    raw = json.load(f)
flat = pd.json_normalize(raw)                       # flatten nested objects
flat = pd.json_normalize(raw, record_path="marks",
                         meta=["roll", "name"])     # explode a nested list
```

| `orient` | Shape |
|---|---|
| `records` | `[{col: val}, …]` — **the usual API shape** |
| `columns` | `{col: {index: val}}` — the default for `to_json` |
| `index` | `{index: {col: val}}` |
| `split` | `{"index": …, "columns": …, "data": …}` |
| `values` | Just the array |

### 🔢 `json_normalize` is the useful one

Course 7 Unit 5's nested college document, flattened:

```python
raw = {"college": "NRI",
       "students": [
           {"roll": 21, "name": "Asha",  "marks": {"maths": 88, "stats": 91}},
           {"roll": 22, "name": "Ravi",  "marks": {"maths": 65, "stats": 58}},
       ]}

pd.json_normalize(raw["students"])
```

```
   roll  name  marks.maths  marks.stats
0    21  Asha           88           91
1    22  Ravi           65           58
```

Nested keys become dotted column names. `pd.read_json` on the same structure
would leave `marks` as a column of dicts, which you cannot compute with —
**`json_normalize` is what makes nested API data usable.**

Course 10's MongoDB documents have exactly this shape, so this function is the
bridge from that course to this one.

## 3.3 Handling missing data

### 🔢 What counts as missing

| Marker | For |
|---|---|
| `np.nan` | Missing float — the classic |
| `None` | Missing object |
| `pd.NA` | The newer, dtype-agnostic marker |
| `pd.NaT` | Missing datetime |

```python
df.isna()             df.notna()
df.isna().sum()                    # missing count PER COLUMN
df.isna().sum().sum()              # total
df.isna().mean()                   # PROPORTION missing per column
df.isna().any(axis=1).sum()        # rows with any missing value
```

`df.isna().mean()` is the one to remember: it turns counts into proportions, so
you can see at a glance that a column is 3% missing versus 70% missing — a
difference that changes what you should do about it.

### ⚠️ `NaN != NaN`

```python
np.nan == np.nan          # False
df[df.maths == np.nan]    # ALWAYS EMPTY — never do this
df[df.maths.isna()]       # correct
```

NaN is defined by IEEE 754 to compare unequal to everything, itself included.
Every language behaves this way, and `isna()` exists precisely because `==`
cannot work.

### ⚠️ NaN forces a column to float

```python
pd.Series([1, 2, 3]).dtype              # int64
pd.Series([1, 2, np.nan]).dtype         # float64  — the ints were upcast
pd.Series([1, 2, pd.NA], dtype="Int64").dtype    # Int64 — a NULLABLE integer
```

There is no NaN in the int64 type, so one missing value converts the whole
column to float. **Nullable dtypes** — capital-I `Int64`, `Float64`,
`boolean`, `string` — keep the type and use `pd.NA`. Use them when a column is
conceptually an integer.

### Dropping

```python
df.dropna()                          # any missing value in the row
df.dropna(how="all")                 # only entirely empty rows
df.dropna(subset=["maths", "stats"]) # only these columns matter
df.dropna(axis=1)                    # drop COLUMNS instead
df.dropna(thresh=3)                  # keep rows with >= 3 non-null values
```

**`dropna()` with no arguments is aggressive**: one missing value anywhere in a
row removes the whole row. On a wide table with scattered gaps it can delete
most of the data. Check `len(df.dropna())` against `len(df)` before committing.

### Filling

```python
df.fillna(0)
df.fillna({"maths": 0, "name": "Unknown"})        # per column
df.fillna(df.mean(numeric_only=True))             # column means
df.fillna(df.median(numeric_only=True))           # more robust — Course 8, §2.5
df["dept"] = df.dept.fillna(df.dept.mode()[0])    # mode for categorical

df.ffill()                     # carry the last valid value FORWARD
df.bfill()                     # carry the next valid value BACKWARD
df.ffill(limit=2)              # at most 2 consecutive
df.interpolate()               # linear between neighbours
df.interpolate(method="time")  # for a DatetimeIndex
```

**`ffill` is for ordered data** — a time series, a sensor reading — where "the
last known value still applies" is a real assumption. Applying it to unordered
rows is meaningless, because "the previous row" has no meaning.

**Interpolation is for numeric series with a genuine ordering.** It invents
values that look plausible, which is either exactly right (a temperature
between two readings) or dangerously misleading (an income between two
unrelated customers).

### 💡 Which method to choose

Course 8 Unit 2 §2.5 covers this properly. The short version:

| Situation | Method |
|---|---|
| Few rows affected, missing at random | **Drop** |
| Numeric, roughly symmetric | Mean |
| Numeric, **skewed or with outliers** | **Median** |
| Categorical | Mode, or an explicit `"Unknown"` category |
| Ordered time series | `ffill` or `interpolate` |
| Accuracy matters most | Model-based (`KNNImputer`, `IterativeImputer`) |

And the two warnings that carry marks: **mean imputation shrinks the variance**,
and **imputation must be fitted after the train/test split**, never before.

## 3.4 Replacing values

```python
df.replace(-999, np.nan)                        # a sentinel for missing
df.replace([-999, -1000], np.nan)
df.replace({-999: np.nan, "N/A": np.nan})
df.replace({"dept": {"DS": "Data Science"}})    # per column
df["name"].replace(r"^\s*$", np.nan, regex=True)  # blank strings -> NaN
df["phone"].replace(r"\D", "", regex=True)        # strip non-digits
```

**Sentinel values are why `replace` exists.** Legacy systems store "missing" as
`-999`, `0`, `9999` or `1900-01-01`. Loaded naively they are *numbers*, so
`mean()` silently includes them and your average age becomes negative.
**Convert sentinels to NaN as the first cleaning step**, before computing
anything.

## 3.5 Renaming axis indexes

```python
df.rename(columns={"maths": "mathematics", "stats": "statistics"})
df.rename(index={0: "first"})
df.rename(columns=str.lower)                     # a function
df.rename(columns=lambda c: c.strip().lower().replace(" ", "_"))

df.columns = ["a", "b", "c", "d"]                # replace them all
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.index.name = "roll"
df.rename_axis("roll")
df.add_prefix("q1_")   /   df.add_suffix("_2026")
```

That `str.strip().str.lower().str.replace(" ", "_")` chain is worth memorising
as the standard column-cleanup line. Real spreadsheets arrive with
`" Total  Marks "` — leading spaces, inconsistent case, embedded spaces — and
every one of those breaks `df.Total_Marks` and confuses `merge`.

## 3.6 Removing duplicates

```python
df.duplicated()                             # fully duplicated rows
df.duplicated(subset=["roll"])              # duplicated on the key
df.duplicated(keep=False)                   # mark EVERY copy
df.duplicated().sum()

df.drop_duplicates()
df.drop_duplicates(subset=["roll"], keep="last")
df.drop_duplicates(subset=["name"], ignore_index=True)
```

| `keep` | Marks as duplicate |
|---|---|
| `"first"` (default) | Every copy **after** the first |
| `"last"` | Every copy **before** the last |
| `False` | **All** members of every duplicate group |

**Use `keep=False` when investigating.** `df[df.duplicated(subset=["roll"], keep=False)]`
shows you *both* rows of each clash so you can see which to keep; the default
shows only one of them, which is useless for deciding.

### ⚠️ "Duplicate" usually means duplicate on a key

Two records for the same student, differing in one typo'd field, are **not**
fully duplicated rows — so `drop_duplicates()` will not touch them. Specify the
`subset` that defines identity:

```python
df.drop_duplicates(subset=["roll"])          # one row per student
```

## 3.7 Filtering outliers

```python
# 1. Domain rules first, always
df = df[(df.age >= 0) & (df.age <= 120)]
df = df[df.marks.between(0, 100)]

# 2. The z-score rule (assumes roughly normal)
z = (df.marks - df.marks.mean()) / df.marks.std()
outliers = df[z.abs() > 3]

# 3. The IQR rule (distribution-free, robust)
q1, q3 = df.marks.quantile([0.25, 0.75])
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = df[(df.marks < lo) | (df.marks > hi)]

# 4. Capping (winsorising) instead of deleting
df["marks"] = df.marks.clip(lower=lo, upper=hi)
```

### ⚠️ The z-score rule is broken by the outliers it looks for

**This is the point of the section.** The mean and standard deviation are both
computed *from data containing the outliers*, so a large outlier inflates the
standard deviation, which widens the ±3σ band, which can hide the outlier —
and can hide smaller ones next to it. This is called **masking**.

```python
s = pd.Series([10, 12, 11, 13, 12, 11, 250, 260])

z = (s - s.mean()) / s.std()
(z.abs() > 3).sum()          # 0 — NEITHER 250 nor 260 is flagged!

q1, q3 = s.quantile([0.25, 0.75])
iqr = q3 - q1
((s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)).sum()    # 2 — both caught
```

With two large values the standard deviation becomes enormous, no point exceeds
three of them, and the z-score rule reports a clean dataset. **The IQR rule uses
quartiles**, which are unaffected by how extreme the extremes are, so it catches
both. (The lab asserts this exact result.)

**And the most important rule of all: investigate before deleting.** An outlier
may be a data-entry error (delete it), a genuine extreme (keep it), or the
fraud you were hired to find (definitely keep it). Course 8 Unit 2 §2.6 makes
the same point: noise and outliers are not the same thing.

## 3.8 Transforming with mapping and functions

### The four tools

| Tool | Works on | Typical use |
|---|---|---|
| **`map`** | A Series | Substitute values from a dict or function |
| **`apply`** | A Series or DataFrame | An arbitrary function, per element/row/column |
| **`applymap`** | A DataFrame (now `map`) | Element-wise across every cell |
| **`transform`** | A Series or group | Return the **same shape** as the input |

```python
df["dept_full"] = df.dept.map({"DS": "Data Science", "Stats": "Statistics"})
df["grade"] = df.marks.map(lambda m: "Pass" if m >= 40 else "Fail")

df["total"] = df[["maths", "stats"]].apply(sum, axis=1)      # per ROW
df[["maths", "stats"]].apply(np.mean)                        # per COLUMN
df.apply(lambda r: r.maths * 0.6 + r.stats * 0.4, axis=1)

df[["maths", "stats"]].map(lambda x: x + 5)   # element-wise (was applymap)
```

### ⚠️ `map` on a Series versus `apply` on a DataFrame

```python
df.dept.map({"DS": "Data Science"})     # 'Stats' becomes NaN — UNMAPPED KEYS
                                        #   are silently dropped
df.dept.map({"DS": "Data Science"}).fillna(df.dept)   # keep the originals
df.dept.replace({"DS": "Data Science"})               # leaves others alone
```

**`map` with an incomplete dictionary silently produces NaN.** That is
occasionally what you want and usually a bug. `replace` leaves unmatched values
alone, which is the safer default.

### 💡 `apply(axis=1)` is slow — usually avoidably

```python
df.apply(lambda r: r.maths + r.stats, axis=1)     # a Python call PER ROW
df.maths + df.stats                                # vectorised, ~100x faster
```

`apply(axis=1)` calls a Python function once per row, which is the loop that
Unit 1 §1.5 told you to avoid. **Before writing it, ask whether the operation
can be expressed on whole columns** — it usually can. Reach for `apply` only
when the logic genuinely cannot be vectorised.

### Binning

```python
pd.cut(df.marks, bins=[0, 40, 60, 75, 100],
       labels=["Fail", "Pass", "First", "Distinction"])
pd.cut(df.marks, bins=4)                    # 4 EQUAL-WIDTH bins
pd.qcut(df.marks, q=4, labels=["Q1", "Q2", "Q3", "Q4"])   # equal-FREQUENCY
```

**`cut` is equal-width; `qcut` is equal-frequency** — exactly Course 8 Unit 2
§2.9's distinction, and the same two-mark question. `cut` with explicit `bins`
is how you apply a grading scheme; `qcut` is how you make quartiles.

Note that `cut`'s intervals are **right-closed by default**: a mark of exactly
40 falls in `(0, 40]`, which is "Fail". Pass `right=False` to change it — and
check which convention your grading scheme actually uses, because the boundary
students are the ones who complain.

---

## Practice problems

### Problem 1

A CSV has: roll numbers with leading zeros, dates as `DD-MM-YYYY`, missing
values written as `"-"` and `"NA"`, a marks column containing `-999` for
absent students, and column names with trailing spaces.

Write the loading and cleaning code.

**Solution.**

```python
df = pd.read_csv(
    "marks.csv",
    dtype={"roll": str},                 # preserve leading zeros
    na_values=["-", "NA", "N/A", ""],    # extra missing markers
    parse_dates=["exam_date"],
    date_format="%d-%m-%Y",              # DD-MM-YYYY, not the US order
)

# 1. Clean the column names FIRST -- everything else depends on them
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# 2. Sentinels become NaN, before any arithmetic
df["marks"] = df.marks.replace(-999, np.nan)

# 3. Check what we have
print(df.dtypes)
print(df.isna().sum())
print(f"{df.isna().mean().max():.1%} missing in the worst column")

# 4. Impute -- median, because marks are skewed by the failures
df["marks"] = df.marks.fillna(df.marks.median())

# 5. Domain rules
df = df[df.marks.between(0, 100)]

# 6. One row per student
df = df.drop_duplicates(subset=["roll"], keep="last")
```

**The order matters and is the examinable part.** Clean the column names first,
or every later reference breaks. Convert sentinels **before** computing any
statistic, or the median you impute with is itself corrupted by the −999s.
Apply domain rules before outlier rules, because a mark of 150 is invalid
regardless of what the quartiles say.

`date_format="%d-%m-%Y"` is not optional: without it, `03-04-2026` is ambiguous
and Pandas may read it as 4 March.

### Problem 2

`s = pd.Series([10, 12, 11, 13, 12, 11, 250, 260])`. Apply the z-score and IQR
rules. Explain the difference.

**Solution.**

```python
s = pd.Series([10, 12, 11, 13, 12, 11, 250, 260])

mu, sd = s.mean(), s.std()          # 72.375, 112.7538
z = (s - mu) / sd
z.abs().max()                       # 1.664  -- nothing exceeds 3

q1, q3 = s.quantile([0.25, 0.75])   # 11.0, 72.25
iqr = q3 - q1                       # 61.25
lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr # -80.875, 164.125
s[(s < lo) | (s > hi)]              # 250 and 260 -- BOTH caught
```

| Rule | Outliers found |
|---|---|
| z-score, \|z\| > 3 | **0** |
| IQR, 1.5× | **2** — the 250 and the 260 |

**The z-score rule fails because of masking.** The two large values pull the
mean up to 72.4 and inflate the standard deviation to 112.8. Three standard
deviations is then a band of ±338, which comfortably contains both — the
outliers have concealed themselves by corrupting the very statistics used to
find them.

**The IQR rule is immune** because quartiles depend only on the *rank* of
values, not their magnitude. Q1 and Q3 sit at 11.0 and 72.25 regardless of
whether the largest value is 250 or 250,000.

**The general lesson:** use robust statistics — median, IQR, MAD — to detect
outliers, and reserve mean-based rules for data you already believe is clean.

### Problem 3

Explain `map`, `apply`, `applymap` and `transform`, with an example of each and
a note on performance.

**Solution.**

```python
df = pd.DataFrame({"dept": ["DS", "Stats", "DS"],
                   "maths": [88, 94, 65],
                   "stats": [91, 89, 58]})

# map -- Series only; substitute values from a dict or a function
df["dept_full"] = df.dept.map({"DS": "Data Science", "Stats": "Statistics"})

# apply on a Series -- an arbitrary function per element
df["grade"] = df.maths.apply(lambda m: "A" if m >= 90 else "B")

# apply on a DataFrame -- per column by default, per row with axis=1
df[["maths", "stats"]].apply(np.mean)             # one value per COLUMN
df.apply(lambda r: r.maths * 0.6 + r.stats * 0.4, axis=1)   # per ROW

# map on a DataFrame (formerly applymap) -- every cell
df[["maths", "stats"]].map(lambda x: x + 5)

# transform -- must return the SAME SHAPE as its input
df.groupby("dept").maths.transform("mean")        # the group mean, per ROW
```

| Tool | Input | Returns |
|---|---|---|
| `Series.map` | Series | Series, same length |
| `Series.apply` | Series | Series or scalar |
| `DataFrame.apply` | Column or row | Aggregated or same-shape |
| `DataFrame.map` | Each cell | DataFrame, same shape |
| `transform` | Series or group | **Same shape as the input** |

**`transform` versus `agg` is the useful distinction:** `groupby().agg("mean")`
gives one row per group, while `groupby().transform("mean")` gives one value
per **original row**, which is what you need to add a group statistic back as a
column.

**On performance:** all four call a Python function per element or per row, so
all four are slow relative to a vectorised expression. `df.maths + df.stats` is
**thousands** of times faster than the equivalent `apply(axis=1)` — the lab
measures roughly 2,900× on 200,000 rows. Use these tools when the logic
genuinely cannot be expressed on whole columns, not as a first resort.

---

## Exam questions from this unit

**Two marks**

1. Name three parameters of `read_csv` and what they do.
2. Why pass `dtype={"roll": str}`?
3. Why does `df[df.x == np.nan]` never return anything?
4. Why does one NaN turn an integer column into float?
5. Distinguish `dropna()` from `dropna(how="all")`.
6. Distinguish `ffill` from `interpolate`.
7. What does `keep=False` do in `duplicated`?
8. Distinguish `cut` from `qcut`.
9. Distinguish `map` from `replace` for substituting values.
10. Why is `apply(axis=1)` slow?

**Five marks**

1. Explain `read_csv` with its important parameters.
2. Explain reading and writing JSON, including `json_normalize`.
3. Explain the methods of handling missing data.
4. Explain removing duplicates with `keep` and `subset`.
5. Explain outlier detection by z-score and IQR, and compare them.
6. Explain `map`, `apply` and `transform` with examples.
7. Explain renaming and cleaning column names.

**Ten marks**

1. Write a complete data-cleaning pipeline for a messy CSV, explaining each
   step and its order.
2. Explain missing-data handling exhaustively — detection, dropping, filling
   and imputation — with the trade-offs of each.
3. Explain data transformation with mapping, functions and binning.

## Mistakes that cost marks

- Comparing to `np.nan` with `==`
- Forgetting `index=False` when writing CSV
- Losing leading zeros by not forcing a string dtype
- Not checking `df.dtypes` after loading
- Leaving sentinel values like −999 in a numeric column
- Computing a statistic before converting sentinels to NaN
- Using `dropna()` with no arguments on a wide table
- Using the mean to impute a skewed column
- Trusting the z-score rule on data with extreme outliers
- Deleting outliers without investigating them
- Cleaning column names after writing code that uses them
- Using `map` with an incomplete dict and silently producing NaN
- Reaching for `apply(axis=1)` where a column expression exists
