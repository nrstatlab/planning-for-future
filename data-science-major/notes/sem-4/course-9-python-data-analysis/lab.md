# Course 9 — Practical Lab

**18 practicals**

Code lives in `labs/course-9-python-da/`.

> **Everything here runs.** This is the one Semester IV course whose prescribed
> tools install cleanly, so nothing is desk-checked and nothing says "not
> executed". All 18 practicals are executed and asserted by
> `tools/run_data_labs.py` on
> **NumPy 2.4.6 and Pandas 3.0.5**, and their results are checked against the
> hand-computed values in the notes.

```bash
pip install -r tools/requirements.txt
python3 tools/run_data_labs.py course9
```

## Working environment

The lab exam will give you either **Jupyter** or a plain editor.

```bash
jupyter lab          # or: jupyter notebook
python3 script.py
```

**In Jupyter, three things save you time:** `df.<TAB>` completes method names,
`pd.merge?` shows the docstring, and `%timeit expr` measures a line. Nobody
memorises the parameter lists — knowing how to look them up is the actual
skill, and examiners know it.

**One import block for everything:**

```python
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # no display on a server; saves files instead
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)
```

---

## Practicals 1–4 — NumPy

### 1. Create and manipulate ndarrays; explore data types

**File:** `01_ndarray_basics.py`

```python
a = np.array([1, 2, 3])
b = np.zeros((2, 3));  c = np.ones((2, 3));  d = np.full((2, 3), 7)
e = np.arange(0, 10, 2);  f = np.linspace(0, 1, 5)
g = np.eye(3);  h = np.random.default_rng(42).random((2, 3))

a.ndim, a.shape, a.size, a.dtype, a.itemsize, a.nbytes
a.astype(np.float64)
```

Asserted: `np.array([[1,2],[3,4]])` has `shape (2,2)`, `size 4`,
`itemsize 8`, `nbytes 32`; `arange(2,10,2)` is `[2,4,6,8]`;
`linspace(0,1,5)` is exactly `[0, .25, .5, .75, 1]`.

**The dtype traps, all asserted:** `int8` 127 + 1 wraps to **−128** with no
warning; assigning `3.7` into an int array **truncates to 3**; and
`np.array([1, 2, "3"])` makes **everything a string** (`<U21`).

**Say in the viva:** `np.empty` does not zero the memory — it hands you whatever
was there. Faster, and a bug if you forget to fill it.

### 2. Arithmetic and element-wise calculations

**File:** `02_arithmetic.py`

Asserted: `[1,2,3] + [4,5,6]` **concatenates** to six elements while the array
version **adds** to `[5,7,9]` — the first thing to get right coming from
Course 3.

Broadcasting, with the failure case:

```python
a - a.mean(axis=0)                    # centre each column  ✓
a - a.mean(axis=1)                    # ValueError -- shapes (2,3) and (2,)
a - a.mean(axis=1, keepdims=True)     # ✓
```

The `ValueError` is asserted, not just described, because *seeing* it is what
makes `keepdims` memorable.

**The speed measurement.** The script times a Python comprehension against the
vectorised form, best of three runs:

| Operation | Python | NumPy | Speed-up |
|---|---|---|---|
| `x * 2` | ~40 ms | ~0.8 ms | **~52×** |
| `sqrt(x)` | ~48 ms | ~1.1 ms | **~43×** |
| dot product | ~36 ms | ~0.08 ms | **~440×** |

on 1,000,000 elements. It asserts the speed-up exceeds 10× rather than a fixed
number, since timings vary by machine — an assertion that would fail on a
genuinely slow path but not on a fast machine.

### 3. Indexing, slicing, boolean and fancy indexing

**File:** `03_indexing.py`

The view/copy behaviour is the point, and it is asserted three ways:

```python
a[1:4]                   # VIEW  -- a[1:4].base is a
a[a > 2]                 # COPY
a[[0, 2]]                # COPY
```

Also asserted: `m[[0,1,2],[1,2,3]]` gives **three paired elements**, not a 3×3
block — `np.ix_` is what gives the submatrix; and that `and` in a mask raises
`ValueError` while `&` works.

### 4. Universal functions and statistics

**File:** `04_ufuncs_stats.py`

```python
np.sqrt, np.exp, np.log, np.abs, np.round, np.sin
np.maximum(a, b)      # ELEMENT-WISE pairing
np.max(a)             # the largest ONE value
a.sum(axis=0)  a.mean(axis=1)  a.std(ddof=1)  a.argmax()  a.cumsum()
```

**The `ddof` assertion is the important one.** For `[2,4,4,4,5,5,7,9]`,
`np.std` gives **2.0** (population) and `pd.Series.std` gives **2.1381**
(sample). The script asserts both, and asserts they differ — because that
silent discrepancy between two libraries is exactly the sort of thing that
ruins an analysis.

`np.nan` propagation is asserted too: `np.array([1, np.nan, 3]).sum()` is
`nan`, and `np.nansum` is 4.

---

## Practicals 5–8 — Pandas structures

### 5. Create and manipulate Series and DataFrames

**File:** `05_series_dataframe.py`

```python
pd.Series([72,45,91], index=["Asha","Ravi","Meena"], name="marks")
pd.Series({"a": 1, "b": 2})            # from a dict
pd.DataFrame({"a":[1,2], "b":[3,4]})   # dict -> COLUMNS
pd.DataFrame([[1,3],[2,4]], columns=["a","b"])   # list -> ROWS
```

**A dict gives columns; a list of lists gives rows.** Getting these the wrong
way round transposes your table, and the script asserts both shapes.

### 6. Indexing, selection, filtering and boolean indexing

**File:** `06_selection.py`

Asserted: `df.loc[0:2]` gives **three** rows and `df.iloc[0:2]` gives **two** —
labels inclusive, positions exclusive.

Also asserted: `df.query("maths > 70 and dept == 'DS'")` gives the same rows as
the `&` form, so you can use whichever reads better.

**The `SettingWithCopy` demonstration**, and it is worth reading carefully:

```python
sub = df[df.dept == "DS"]
sub["maths"] = 100            # Pandas 3: NO warning, and df is UNCHANGED
```

The script asserts both facts. Pandas 3's copy-on-write removed the warning, so
the old chained-assignment bug now fails **silently and completely**. The two
correct forms — one `.loc`, or an explicit `.copy()` — are asserted alongside.

### 7. Arithmetic and data alignment

**File:** `07_alignment.py`

```python
a = pd.Series([10,20,30], index=["x","y","z"])
b = pd.Series([1,2,3,4],  index=["w","x","y","z"])
a + b        # w NaN, x 12, y 23, z 34
```

Asserted exactly, including that the result is **float64** because NaN is a
float, and that `a.add(b, fill_value=0)` gives `w = 1`.

**The point the script makes explicit:** `x` sits at position 0 in `a` and
position 1 in `b`, yet the answer is right — Pandas aligned by **label**.
NumPy would have added mismatched pairs and produced a plausible wrong answer.

### 8. Sorting, ranking, dropping and duplicate indexes

**File:** `08_sort_rank.py`

All five tie-breaking methods asserted on `[70, 85, 70, 92, 60]`:

| method | The two 70s |
|---|---|
| `average` | 2.5 |
| `min` | 2 |
| `max` | 3 |
| `first` | 2 and 3 |
| `dense` | 2 |

**`min` versus `dense`** is the distinction: `min` leaves a gap after ties
(1, 2, 2, 4), `dense` does not (1, 2, 2, 3).

Also asserted: with a duplicate index, `s["a"]` returns a **Series** while
`s["b"]` returns a **scalar** — the return type depends on the data, which is
why code breaks the day a duplicate appears.

---

## Practicals 9–12 — I/O and cleaning

### 9. Read and write CSV, TXT, JSON and Excel

**File:** `09_io.py`

Every format is round-tripped through a temporary directory and asserted equal
to what went in.

**The four real-world traps, each asserted:**

```python
pd.read_csv(f)                            # roll "007" becomes the integer 7
pd.read_csv(f, dtype={"roll": str})       # stays "007"

pd.read_csv(f)                            # "2026-08-26" is an object string
pd.read_csv(f, parse_dates=["date"])      # a real datetime64

pd.read_csv(f)                            # "-" makes the column object dtype
pd.read_csv(f, na_values=["-"])           # NaN, and the column stays numeric

df.to_csv(f)                              # adds an unnamed index column
df.to_csv(f, index=False)                 # clean
```

`json_normalize` is asserted on Course 7's nested college document: nested keys
become dotted columns (`marks.maths`), which is what makes API data usable.
Course 10's MongoDB documents have the same shape.

### 10. Detect, drop, fill and replace missing values

**File:** `10_missing.py`

Asserted: `np.nan == np.nan` is `False`, so `df[df.x == np.nan]` is **always
empty**; one NaN upcasts an int64 column to float64, while `Int64` keeps it.

**The variance-shrinkage measurement**, which is the experiment worth doing:
with 30% of a column replaced by its mean, the mean is preserved exactly and
the standard deviation falls by about **16%** — close to the
1 − √0.7 = 16.3% you would predict. The script asserts the mean is unchanged
and the spread is not.

**The leakage demonstration:** fitting the imputer on train + test gives a fill
value of 258 where fitting on train alone gives 11 — the test set's outlier has
leaked into the training features.

### 11. Rename axes, remove duplicates, filter outliers

**File:** `11_outliers.py`

The masking demonstration, asserted:

```python
s = pd.Series([10, 12, 11, 13, 12, 11, 250, 260])
(z.abs() > 3).sum()                    # 0  -- neither outlier flagged
((s < lo) | (s > hi)).sum()            # 2  -- IQR catches both
```

mean 72.375, sd 112.7538, so ±3σ is a band of ±338 that contains both. **The
outliers concealed themselves by corrupting the statistics used to find them.**

The column-cleanup line is asserted too:
`df.columns.str.strip().str.lower().str.replace(" ", "_")` turns
`" Total  Marks "` into `total__marks`.

### 12. Transform data with mapping functions and string operations

**File:** `12_transform.py`

Asserted: `map` with an incomplete dict silently produces **NaN**, while
`replace` leaves unmatched values alone — the difference that catches people.

`cut` versus `qcut` on a skewed series: `cut(4)` gives counts `[8, 0, 0, 1]`
and `qcut(4)` gives `[3, 2, 2, 2]`. Equal-**width** against
equal-**frequency**, exactly Course 8 §2.9.

**The performance measurement:** `df.a + df.b` against
`df.apply(lambda r: r.a + r.b, axis=1)` on 200,000 rows — roughly **2,900×**.
The script asserts the speed-up exceeds 50×.

---

## Practicals 13–14 — Strings and features

### 13. String operations and regular expressions

**File:** `13_strings.py`

```python
rolls.str.extract(r"(?P<year>\d{2})(?P<branch>[A-Z]{3})(?P<number>\d{4})")
```

Named groups become column names directly, and `0145` **keeps its leading
zero** because `extract` returns strings — right for an identifier, and the
script asserts it.

**The dtype-dependent `contains` behaviour**, verified on Pandas 3.0.5 and
worth knowing precisely:

| Column dtype | `str.contains` returns | Masking with it |
|---|---|---|
| `str` (Pandas 3 default) | `bool`, NaN → False | **Works** |
| `object` | `object`, NaN → None | **Raises ValueError** |

So `na=False` is no longer always required — and you should pass it anyway,
because you will not always know which dtype a column arrived with.

### 14. Dummy variables, permutation and random sampling

**File:** `14_dummies_sampling.py`

Asserted: *k* dummy columns **sum to 1 in every row** — the collinearity
itself, demonstrated rather than asserted in prose — and `drop_first=True`
gives *k − 1* with the dropped level as the all-zeros reference.

**The bootstrap measurement:** drawing *n* indices with replacement from *n*
leaves about **36.8%** unselected, matching 1/e = 0.3679. That is the `.632`
in Course 8's .632 bootstrap, and the mechanism behind bagging.

**Stratification, asserted:** on an 8-DS/2-Stats frame, an unstratified 50%
sample can miss Stats entirely; the stratified version always gives 4 and 1.

**A Pandas 3 note the script demonstrates:** `groupby().apply()` now
**excludes the grouping column** from each group, so a naive stratified sample
loses `dept`. Select the columns explicitly, or use
`train_test_split(..., stratify=...)`.

---

## Practicals 15–18 — Wrangling and visualization

### 15. Merge, join and concatenate

**File:** `15_merge.py`

All four join types asserted on the rolls 21–24 / 21,22,23,25 pair: **3, 4, 4,
5** rows. `indicator=True` gives `both 3, left_only 1, right_only 1`.

**Three failure modes, each asserted:**

```python
# 1. dtype mismatch -> EMPTY result, no error
pd.merge(a, b.astype({"roll": str}), on="roll")     # 0 rows

# 2. whitespace in the key -> no match
pd.merge(a, b_with_trailing_spaces, on="dept")      # 0 rows

# 3. duplicate keys on both sides -> CARTESIAN PRODUCT
pd.merge(dup_a, dup_b, on="k")                       # 3 x 4 = 12 rows
pd.merge(dup_a, dup_b, on="k", validate="one_to_one")# raises MergeError
```

That third one is why `validate=` is worth using every time.

### 16. Reshape with pivot, stack, unstack; hierarchical indexing

**File:** `16_reshape.py`

Long → wide → long asserted as a round trip. `pivot` on a duplicated
`(name, subject)` pair **raises ValueError**; `pivot_table` succeeds and
**silently averages** to 91.5 unless you choose `aggfunc="max"` for 95 —
both asserted, because which is right is a question about your data.

The MultiIndex sort requirement is asserted as a raised
`UnsortedIndexError`, then fixed with `.sort_index()`.

### 17. Summary statistics grouped by level or category

**File:** `17_groupby.py`

`agg` gives 2 rows, `transform` gives 5 — asserted, because that is the
distinction students get wrong. `size()` includes NaN and `count()` does not.

**The share check:** percentages computed with `transform("sum")` as the
denominator sum to exactly 100 within each group. The script asserts it, which
is the habit worth forming — it catches a mis-grouped denominator immediately.

### 18. Basic visualizations with matplotlib

**File:** `18_plots.py`

Runs under the **Agg** backend, so it opens no window and writes PNG files to a
temporary directory. Asserted: each file exists and is non-empty; each axes
object has a non-empty title and both axis labels.

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0,0].hist(marks, bins=10)              # DISTRIBUTION of one variable
axes[0,1].bar(depts, means)                 # comparing CATEGORIES
axes[1,0].scatter(maths, stats)             # relationship
axes[1,1].boxplot([ds, st], tick_labels=["DS","Stats"])
fig.tight_layout()
fig.savefig(path, dpi=150, bbox_inches="tight")
plt.close(fig)                              # or you leak memory in a loop
```

Seaborn and Plotly are imported **conditionally** — if either is absent the
script says so and skips that section rather than failing, so the suite stays
green on a minimal install. Read the output: it tells you which ran.

---

## Lab examination

An hour, a dataset, and one practical number.

**What costs marks:**

- Writing a Python loop where a vectorised expression exists
- `and` / `or` instead of `&` / `|`, or missing parentheses
- Expecting `.loc[0:2]` to give two rows
- Chained assignment `df[mask]["col"] = x` — which in Pandas 3 does nothing at
  all, silently
- Forgetting `index=False` when writing CSV
- Not checking `df.dtypes` after loading
- Using `agg` where `transform` was needed
- Forgetting `ignore_index=True` when concatenating rows
- Plotting categorical counts as a histogram
- Leaving axes unlabelled

**What earns them:**

- **Run `df.info()` first, every time**, and say what it tells you: dtypes and
  non-null counts together reveal both "this loaded as object" and "this is 40%
  missing" in one glance.
- **State the shape before and after every merge or filter.** "3 rows became 2,
  because the inner join dropped roll 24" is the kind of sentence that
  distinguishes someone who is reading their output from someone who is
  running cells.
- **Use `validate=` and `indicator=True`** on merges and explain why.
- **Check your own arithmetic**: a share must sum to 100 within its group; a
  round trip must return the original. Write the assertion.
- **Know the two defaults that differ** — `np.std` is the population formula
  and `pd.Series.std` is the sample one. Being able to say that, and pass
  `ddof` explicitly, is a two-mark answer that many candidates miss.
- **Label both axes with units.** It takes two lines and it is the difference
  between a chart and a picture.
