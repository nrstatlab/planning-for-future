# Unit 2 — Pandas Basics and Data Structures

**Syllabus topics:** Series, DataFrame, Index objects, indexing and
selection, filtering and boolean indexing, arithmetic and data alignment,
sorting and ranking, dropping entries, handling duplicate indexes.

---

## 2.1 Series

### 🎯 The big idea

A **Series** is a one-dimensional array **with labels**. It is a NumPy array
and a dictionary at the same time: positional like the array, keyed like the
dictionary.

```python
import pandas as pd
import numpy as np

s = pd.Series([72, 45, 91, 66],
              index=["Asha", "Ravi", "Meena", "Kiran"],
              name="marks")
```

```
Asha     72
Ravi     45
Meena    91
Kiran    66
Name: marks, dtype: int64
```

| Attribute | Meaning |
|---|---|
| `s.values` | The underlying NumPy array |
| `s.index` | The labels |
| `s.dtype` | Element type |
| `s.name` | The Series' own name |
| `s.size`, `len(s)` | Number of elements |
| `s.shape` | `(4,)` |

### Creating

```python
pd.Series([1, 2, 3])                       # default RangeIndex 0,1,2
pd.Series([1, 2, 3], index=["a", "b", "c"])
pd.Series({"a": 1, "b": 2})                # from a dict — keys become the index
pd.Series(5, index=["a", "b", "c"])        # a scalar is BROADCAST
pd.Series(np.arange(5))
```

### Access

```python
s["Asha"]              # 72   — by label
s.iloc[0]              # 72   — by POSITION
s[["Asha", "Meena"]]   # a sub-Series
s[s > 60]              # boolean masking, as in NumPy
"Asha" in s            # True — checks the INDEX, like a dict
s.to_dict()
```

### ⚠️ Do not index a Series with `[]` and a bare integer

```python
t = pd.Series([10, 20, 30], index=[2, 0, 1])
t[0]     # AMBIGUOUS: label 0 or position 0?
```

Pandas resolves it as the **label**, giving 20 rather than 10 — and in Pandas
2+ positional `[]` on an integer index is deprecated outright. **Always say
which you mean:** `t.loc[0]` for the label, `t.iloc[0]` for the position.

## 2.2 DataFrame

A **DataFrame** is a two-dimensional table: an ordered collection of Series
that **share one index**. Think of a spreadsheet, or a SQL table with named
columns — with the crucial addition that the *rows* are labelled too.

```python
df = pd.DataFrame({
    "name":  ["Asha", "Ravi", "Meena", "Kiran", "Bhanu"],
    "dept":  ["DS", "DS", "Stats", "DS", "Stats"],
    "maths": [88, 65, 94, 71, 52],
    "stats": [91, 58, 89, 66, 47],
})
```

```
    name   dept  maths  stats
0   Asha     DS     88     91
1   Ravi     DS     65     58
2  Meena  Stats     94     89
3  Kiran     DS     71     66
4  Bhanu  Stats     52     47
```

| Attribute | Meaning |
|---|---|
| `df.shape` | `(5, 4)` — rows, columns |
| `df.columns` | The column labels (an Index) |
| `df.index` | The row labels |
| `df.dtypes` | Type **per column** |
| `df.values` / `df.to_numpy()` | As a NumPy array |
| `df.size` | 20 |
| `df.T` | Transposed |

### Creating

```python
pd.DataFrame({"a": [1, 2], "b": [3, 4]})          # dict of columns
pd.DataFrame([[1, 3], [2, 4]], columns=["a", "b"])  # list of ROWS
pd.DataFrame([{"a": 1, "b": 3}, {"a": 2, "b": 4}])  # list of dicts
pd.DataFrame(np.arange(6).reshape(2, 3), columns=list("xyz"))
```

**A dict gives columns; a list of lists gives rows.** Getting these the wrong
way round produces a transposed table, and it is the commonest construction
error.

### First look at any dataset

```python
df.head()          df.tail(3)        df.sample(5)
df.info()          # dtypes, non-null counts, memory — ALWAYS run this first
df.describe()      # count, mean, std, min, quartiles, max — numeric columns
df.describe(include="all")           # categorical columns too
df["dept"].value_counts()
df.nunique()       df.isna().sum()
```

**`df.info()` is the first thing to run on any new data**, because it shows the
dtypes and the non-null counts together — which reveals both "this numeric
column loaded as `object`" and "this column is 40% missing" in one glance.

## 2.3 Index objects

The **Index** is what makes Pandas more than NumPy: it carries the labels and
drives alignment.

```python
idx = df.index                     # RangeIndex(start=0, stop=5, step=1)
df.columns                         # Index(['name','dept','maths','stats'], ...)

df2 = df.set_index("name")         # promote a column to the index
df2.reset_index()                  # push it back to a column
df2.index.name                     # 'name'
df.rename(columns={"maths": "mathematics"})
```

| Index type | For |
|---|---|
| `RangeIndex` | Default integers, memory-efficient |
| `Index` | Generic (strings, mixed) |
| `DatetimeIndex` | Timestamps — enables `df["2026-01"]` slicing |
| `MultiIndex` | Hierarchical (Unit 5) |
| `CategoricalIndex` | A fixed set of labels |

### ⚠️ The Index is immutable

```python
df.index[0] = "x"      # TypeError: Index does not support mutable operations
df.index = ["a", "b", "c", "d", "e"]     # replacing the WHOLE index is fine
```

Immutability is what allows an index to be shared safely between objects
without defensive copying.

**Indexes need not be unique** — see §2.9, where that becomes a problem.

## 2.4 Indexing and selection

### 🔢 The three accessors

| Accessor | Selects by | Endpoint |
|---|---|---|
| `df[...]` | **Columns** (or a boolean mask / row slice) | — |
| `df.loc[rows, cols]` | **Labels** | **Inclusive** |
| `df.iloc[rows, cols]` | **Positions** | **Exclusive** |

```python
df["maths"]                  # one column -> a SERIES
df[["maths", "stats"]]       # several -> a DATAFRAME
df.maths                     # attribute access — convenient, limited

df.loc[0]                    # row with LABEL 0
df.loc[0, "maths"]           # one cell
df.loc[0:2, "name":"maths"]  # INCLUSIVE of row 2 and column 'maths'
df.loc[:, "maths"]           # every row, one column
df.loc[df.maths > 70, ["name", "maths"]]   # mask + column list

df.iloc[0]                   # first row by POSITION
df.iloc[0, 2]                # row 0, column 2
df.iloc[0:2, 0:3]            # EXCLUSIVE of row 2 and column 3
df.iloc[-1]                  # last row
df.iloc[[0, 2, 4], [0, 2]]   # fancy indexing

df.at[0, "maths"]            # a single cell, fast
df.iat[0, 2]                 # a single cell by position, fast
```

### ⚠️ `.loc` is inclusive, `.iloc` is exclusive

```python
df.loc[0:2]     # THREE rows — 0, 1 and 2
df.iloc[0:2]    # TWO rows — 0 and 1
```

This asymmetry looks like a bug and is deliberate. With **labels**, you often
do not know what comes after `"maths"`, so an exclusive endpoint would be
unusable — `df.loc[:, "name":"maths"]` has to include `maths` to be meaningful.
With **positions**, exclusivity matches Python slicing everywhere else.

**Learn the rule as: labels inclusive, positions exclusive.** It is a
guaranteed two-mark question.

### ⚠️ `df.maths` versus `df["maths"]`

Attribute access fails silently or confusingly when the column name

- contains a space or punctuation — `df.total marks` is a syntax error;
- collides with a method — `df.count` gives the **method**, not the column;
- is not a string.

**And you cannot create a column with it:** `df.newcol = 0` sets an *attribute*
on the DataFrame, not a column, and Pandas warns you. **Always use
`df["newcol"] = 0`.**

## 2.5 Filtering and boolean indexing

```python
df[df.maths > 70]
df[(df.maths > 70) & (df.dept == "DS")]        # & | ~, with parentheses
df[df.dept.isin(["DS", "Stats"])]
df[~df.dept.isin(["Stats"])]
df[df.maths.between(60, 90)]                   # INCLUSIVE both ends
df[df.name.str.startswith("A")]
df[df.maths.isna()]
df.query("maths > 70 and dept == 'DS'")        # a readable alternative
df.query("maths > @threshold")                 # @ refers to a Python variable
```

As in NumPy, use `&`, `|`, `~` — not `and`, `or`, `not` — and parenthesise
each comparison.

`df.query()` is worth knowing: it takes a string, so `and`/`or` work normally
and long conditions read better. It is slightly slower and cannot handle
column names with spaces without backticks.

### Selecting rows and columns together

```python
df.loc[df.maths > 70, "name"]                  # a Series of names
df.loc[df.maths > 70, ["name", "maths"]]       # a DataFrame
df.loc[df.dept == "DS", "maths"] = 0           # assignment through .loc
```

### ⚠️ `SettingWithCopyWarning`

```python
subset = df[df.dept == "DS"]
subset["maths"] = 100          # SettingWithCopyWarning
```

The warning means: **Pandas cannot tell whether `subset` is a view or a copy**,
so it cannot tell you whether the assignment reached `df`. Chained indexing —
`df[mask]["col"] = x` — has the same problem, and silently does nothing at all
when the intermediate is a copy.

**The two correct forms:**

```python
df.loc[df.dept == "DS", "maths"] = 100    # to modify the ORIGINAL: one .loc
subset = df[df.dept == "DS"].copy()       # to work separately: be explicit
subset["maths"] = 100
```

**Never chain.** Under Pandas 3 the chained form reliably does nothing rather
than sometimes working — and, since Pandas 3 also dropped the warning, it does
nothing *silently*. Verified on Pandas 3.0.5: the assignment above leaves `df`
untouched and prints no warning.

## 2.6 Arithmetic and data alignment

### 🎯 The big idea

**Pandas aligns on the index before computing.** This is the feature that most
distinguishes it from NumPy, and it prevents a whole class of silent errors.

```python
a = pd.Series([1, 2, 3], index=["x", "y", "z"])
b = pd.Series([10, 20, 30], index=["z", "y", "w"])

a + b
```

```
w     NaN        ← in b only
x     NaN        ← in a only
y    22.0        ← 2 + 20
z    13.0        ← 3 + 10   — note it aligned z with z, NOT position with position
```

Two things happened. Labels present in only one operand became **NaN** (the
union of indexes is used). And `z` was matched with `z` even though they sat
at different positions.

**With NumPy this would have added position by position and given a plausible,
wrong answer.** Alignment turns a silent bug into a visible NaN.

### Filling instead of NaN

```python
a.add(b, fill_value=0)      # treat missing labels as 0
a.sub(b, fill_value=0)
a.mul(b, fill_value=1)
a.div(b, fill_value=1)
```

| Operator | Method |
|---|---|
| `+` | `add` |
| `-` | `sub` |
| `*` | `mul` |
| `/` | `div` |
| `//` | `floordiv` |
| `%` | `mod` |
| `**` | `pow` |

The methods exist precisely so you can pass `fill_value` and `axis`.

### DataFrame and Series arithmetic

```python
df[["maths", "stats"]] * 2                     # element-wise
df["total"] = df.maths + df.stats              # a new column
df["avg"] = df[["maths", "stats"]].mean(axis=1)

nums = df[["maths", "stats"]]
nums - nums.mean()                             # broadcasts down the COLUMNS
nums.sub(nums.mean(axis=1), axis=0)            # ...and across the ROWS
```

**By default a DataFrame–Series operation matches the Series' index against the
DataFrame's *columns*** and broadcasts down the rows. To match against the
*index* instead, pass `axis=0` (or `axis="index"`).

## 2.7 Sorting and ranking

```python
df.sort_values("maths")                          # ascending
df.sort_values("maths", ascending=False)
df.sort_values(["dept", "maths"], ascending=[True, False])
df.sort_values("maths", na_position="first")     # default is 'last'
df.sort_index()                                  # by row label
df.sort_index(axis=1)                            # by COLUMN name

df.nlargest(3, "maths")                          # faster than sort + head
df.nsmallest(3, "maths")
```

### 🔢 Ranking

```python
s = pd.Series([70, 85, 70, 92, 60])
s.rank()                                # 2.5, 4.0, 2.5, 5.0, 1.0
s.rank(method="min")                    # 2, 4, 2, 5, 1
s.rank(method="max")                    # 3, 4, 3, 5, 1
s.rank(method="first")                  # 2, 4, 3, 5, 1
s.rank(method="dense")                  # 2, 3, 2, 4, 1
s.rank(ascending=False)                 # rank 1 = highest
s.rank(pct=True)                        # as a percentile
```

**Ties are the whole question.** The two 70s occupy ranks 2 and 3, and the
method decides what to report:

| method | The two 70s get | Note |
|---|---|---|
| `average` (default) | **2.5** each | (2+3)/2 |
| `min` | 2 each | Competition ranking — next is 4 |
| `max` | 3 each | |
| `first` | 2 and 3 | By order of appearance |
| `dense` | 2 each | Next is **3**, no gap |

`min` versus `dense` is the distinction to remember: `min` leaves a gap after
ties (1, 2, 2, 4), `dense` does not (1, 2, 2, 3).

## 2.8 Dropping entries

```python
df.drop(0)                          # drop the row with label 0
df.drop([0, 2])
df.drop("maths", axis=1)            # drop a column
df.drop(columns=["maths", "stats"])  # clearer — prefer this
df.drop(index=[0, 1], columns=["dept"])

s.drop("Ravi")
df.dropna()                         # rows with ANY missing value
df.dropna(how="all")                # only rows entirely missing
df.dropna(subset=["maths"])         # only where maths is missing
df.dropna(axis=1)                   # drop COLUMNS with missing values
df.dropna(thresh=3)                 # keep rows with >= 3 non-null values
```

### ⚠️ `drop` returns a copy; it does not modify in place

```python
df.drop("maths", axis=1)      # returns a new DataFrame — df is UNCHANGED
df = df.drop("maths", axis=1) # correct: reassign
```

**`inplace=True` is being deprecated across Pandas** — it never actually saved
memory, it broke method chaining, and it made code harder to reason about.
Reassign instead.

## 2.9 Duplicate indexes

An index is **not required to be unique**, and duplicates change behaviour in
ways that surprise people.

```python
s = pd.Series([1, 2, 3, 4], index=["a", "a", "b", "c"])

s.index.is_unique      # False
s["a"]                 # returns a SERIES of two values
s["b"]                 # returns the SCALAR 3
```

**The return type depends on the data**, which means code written against a
unique index breaks the day a duplicate appears — and the failure is a
`TypeError` somewhere downstream, not at the point of the problem.

```python
df.index.duplicated()             # boolean array, first occurrence False
df[df.index.duplicated()]         # the duplicate rows
df[~df.index.duplicated(keep="first")]   # keep the first of each
df.reset_index(drop=True)         # abandon the labels entirely
df.loc[df.index.drop_duplicates()]
```

### Duplicate ROWS, which is a different question

```python
df.duplicated()                          # fully duplicated rows
df.duplicated(subset=["name", "dept"])   # duplicated on those columns only
df.duplicated(keep=False)                # mark ALL copies, not just the later ones
df.drop_duplicates()
df.drop_duplicates(subset=["name"], keep="last")
```

`keep="first"` (the default) marks later copies; `keep="last"` marks earlier
ones; **`keep=False` marks every member of every duplicate group**, which is
what you want when you are investigating rather than cleaning.

### ⚠️ Duplicates break joins

If both sides of a merge have duplicate keys, the result is the **Cartesian
product** of the matching rows: 3 × 4 duplicates become 12 rows. A join that
mysteriously multiplies your row count is almost always this.

```python
pd.merge(left, right, on="id", validate="one_to_one")   # raises if violated
```

**`validate=` is the defence**, and it is worth using every time — it turns a
silent row explosion into an immediate error.

---

## Practice problems

### Problem 1

```python
a = pd.Series([10, 20, 30], index=["x", "y", "z"])
b = pd.Series([1, 2, 3, 4], index=["w", "x", "y", "z"])
```

Give the output of `a + b` and of `a.add(b, fill_value=0)`, and explain.

**Solution.**

```python
a + b
```
```
w     NaN
x    12.0
y    23.0
z    34.0
dtype: float64
```

```python
a.add(b, fill_value=0)
```
```
w     1.0
x    12.0
y    23.0
z    34.0
dtype: float64
```

**Explanation.** Pandas takes the **union** of the two indexes — w, x, y, z —
and aligns by label before adding: x is 10 + 2, y is 20 + 3, z is 30 + 4.
Label `w` exists only in `b`, so the plain `+` gives NaN. `fill_value=0`
substitutes 0 for the missing operand, giving 0 + 1 = 1.

Two further points. The dtype becomes **float64** even though both inputs were
int64, because NaN is a float. And note that `a` and `b` are in *different
positions* — `x` is position 0 in `a` and position 1 in `b` — yet the answer is
right, because alignment is by **label, not position**. NumPy would have added
mismatched pairs and produced a wrong answer with no warning.

### Problem 2

Given the student DataFrame of §2.2, write expressions for:

(a) students in DS with maths above 70
(b) name and total marks, sorted by total descending
(c) the top 2 by maths in each department
(d) the rank of each student by total, with tied ranks averaged
(e) drop the `stats` column and any student scoring below 50 in maths

**Solution.**

```python
# (a)
df[(df.dept == "DS") & (df.maths > 70)]
# or:  df.query("dept == 'DS' and maths > 70")

# (b)
df["total"] = df.maths + df.stats
df[["name", "total"]].sort_values("total", ascending=False)

# (c)
df.sort_values("maths", ascending=False).groupby("dept").head(2)
# or:  df.groupby("dept", group_keys=False).apply(lambda g: g.nlargest(2, "maths"))

# (d)
df["rank"] = df.total.rank(ascending=False, method="average")

# (e)
cleaned = df.drop(columns="stats")
cleaned = cleaned[cleaned.maths >= 50]
```

With the fixture data, (b) gives Meena 183, Asha 179, Kiran 137, Ravi 123,
Bhanu 99; and (d) gives Meena rank 1 and Bhanu rank 5.

Three points that earn marks. In (a), `&` with parentheses — `and` raises a
ValueError. In (c), `sort_values` then `groupby().head(2)` is both faster and
clearer than an `apply`. In (e), `drop` returns a copy, so the reassignment is
essential — and using `df.drop(columns=...)` rather than `axis=1` states the
intent.

### Problem 3

Explain what `SettingWithCopyWarning` means and give two correct fixes.

```python
ds = df[df.dept == "DS"]
ds["maths"] = ds["maths"] + 5
```

**Solution.**

`df[df.dept == "DS"]` may return a **view** into `df` or a **copy** of it — and
Pandas cannot always tell which. So it cannot tell whether the assignment will
reach the original `df`. Rather than guess, it warns.

The consequences were genuinely ambiguous in older Pandas: sometimes `df` was
modified, sometimes not, depending on memory layout.

**Under Pandas 3 the behaviour changed, and you must know how.** Copy-on-write
is now the default, so `df[df.dept == "DS"]` always returns a copy, the
original is **never** modified — and **no warning is raised at all**. The
unpredictability is gone; the bug is not. Code that intended to update `df`
now fails silently and completely, with nothing on the console to tell you.

That makes the correct forms *more* important than they were, not less.

**Fix 1 — to modify the original**, do it in a single `.loc` so there is no
intermediate object at all:

```python
df.loc[df.dept == "DS", "maths"] += 5
```

**Fix 2 — to work on a separate table**, say so explicitly:

```python
ds = df[df.dept == "DS"].copy()
ds["maths"] += 5              # df is untouched, and that is intended
```

The general rule: **never chain an index onto an index when assigning.**
`df[mask]["col"] = x` is always wrong; `df.loc[mask, "col"] = x` is always
right.

---

## Exam questions from this unit

**Two marks**

1. Distinguish a Series from a DataFrame.
2. Distinguish `.loc` from `.iloc`.
3. Why is `.loc` inclusive of its endpoint?
4. What is data alignment?
5. Why does `a + b` produce NaN for a label in only one Series?
6. Distinguish `df.maths` from `df["maths"]`.
7. What does `SettingWithCopyWarning` mean?
8. Distinguish `rank(method='min')` from `rank(method='dense')`.
9. Why must an index be checked for uniqueness before a merge?
10. Does `drop` modify the DataFrame in place?

**Five marks**

1. Explain the Series with creation, access and attributes.
2. Explain the DataFrame with creation and inspection methods.
3. Explain Index objects and their types.
4. Explain `[]`, `.loc` and `.iloc` with examples.
5. Explain boolean filtering with examples.
6. Explain data alignment with an example, and `fill_value`.
7. Explain sorting and ranking, with all the tie-breaking methods.
8. Explain handling duplicate indexes and duplicate rows.

**Ten marks**

1. Explain Pandas indexing and selection exhaustively, with examples of each
   accessor and the view/copy issue.
2. Write a program that loads student data and performs filtering, sorting,
   ranking and aggregation, explaining every step.
3. Explain data alignment and arithmetic between Series and DataFrames.

## Mistakes that cost marks

- Using `and` / `or` instead of `&` / `|` in a filter
- Omitting the parentheses in a compound condition
- Expecting `.loc[0:2]` to give two rows
- Using `df.maths = ...` to create a column
- Chained assignment: `df[mask]["col"] = x`
- Forgetting that `drop` returns a copy
- Expecting NumPy-style positional arithmetic instead of label alignment
- Being surprised that `a + b` produces NaN and float64
- Assuming an index is unique when it is not
- Merging on duplicated keys and getting a Cartesian product
- Confusing `rank(method='min')` with `rank(method='dense')`
- Relying on `inplace=True`, which is being deprecated
