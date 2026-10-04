# Practical Lab

**18 practicals**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.

Code lives in `labs/course-9-python-da/`.

> **Everything here runs.** This is one of the few courses whose prescribed
> tools install cleanly, so nothing is desk-checked and nothing says "not
> executed". All 18 practicals are executed and asserted by
> `tools/data-science/run_data_labs.py`, on the NumPy and Pandas versions in
> `output/VERSIONS.txt`, and their results are checked against the
> hand-computed values in the notes. Under **5. Execution and Results** is what each one printed;
> practical 18's charts are shown as it drew them.

```bash
pip install -r tools/data-science/requirements.txt
python3 tools/data-science/run_data_labs.py course9
```

| Practicals | Topic |
|---|---|
| 1–4 | NumPy |
| 5–8 | Pandas structures |
| 9–12 | I/O and cleaning |
| 13–14 | Strings and features |
| 15–18 | Wrangling and visualization |

Three practicals time something — 2's vectorisation and 12's `apply` against arithmetic, best
of three runs where it says so. A timing measures the machine at a moment, so those lines differ
from run to run, and `capture_lab_outputs.py --check` sets them aside; every other line must
repeat exactly.

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

## Practical 1 — Create and manipulate ndarrays; explore data types

### 1. Question

Create NumPy arrays and explore their attributes and data types.

### 2. Aim

Make arrays in the standard ways, read their attributes, and meet the dtype traps.

### 3. Steps

1. **Create arrays.**
2. **Read their attributes.**
3. **Meet the dtype traps.**
4. **See that np.empty is not zeros.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

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
</div>


### 4. Programme

{{programme: course-9-python-da/01_ndarray_basics.py}}

### 5. Execution and Results

{{output: course-9-python-da/01_ndarray_basics.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Every array is created and described as asserted; int8 wraps, floats truncate into ints, and one string makes the whole array strings.
</div>


## Practical 2 — Arithmetic and element-wise calculations

### 1. Question

Perform arithmetic and element-wise calculations on arrays.

### 2. Aim

Compute on whole arrays at once, broadcast shapes together, and measure what that saves.

### 3. Steps

1. **Compare a list with an array.**
2. **Compute element-wise.**
3. **Broadcast shapes together.**
4. **Reduce along an axis.**
5. **Time a loop against a vectorised sum.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

Asserted: `[1,2,3] + [4,5,6]` **concatenates** to six elements while the array
version **adds** to `[5,7,9]` — the first thing to get right coming from
Python Programming and Data Structures.

Broadcasting, with the failure case:

```python
a - a.mean(axis=0)                    # centre each column  ✓
a - a.mean(axis=1)                    # ValueError -- shapes (2,3) and (2,)
a - a.mean(axis=1, keepdims=True)     # ✓
```

The `ValueError` is asserted, not just described, because *seeing* it is what
makes `keepdims` memorable.
</div>


### 4. Programme

{{programme: course-9-python-da/02_arithmetic.py}}

### 5. Execution and Results

{{output: course-9-python-da/02_arithmetic.py}}

**The speed measurement.** The script times a Python comprehension against the
vectorised form, best of three runs, on 1,000,000 elements; the figures above are this run's.
It asserts only that NumPy is faster — the program's own comments say why: a fixed floor (it
was 10×) failed on a loaded machine at 7.1× for the dot product, a false alarm, because a wall
clock measures the machine, not the code.

**Corrected:** this page said the script asserts a speed-up of more than 10×, and gave a table
of approximate timings (~52×, ~43×, ~440×). The assertion was relaxed to "faster" when the floor
proved flaky, and timings vary from run to run; the run's own are above.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Lists concatenate and arrays add; broadcasting needs keepdims; and NumPy was many times faster, by the figures this run measured, above.
</div>


## Practical 3 — Indexing, slicing, boolean and fancy indexing

### 1. Question

Select elements of arrays by indexing, slicing, boolean masks and lists of indices.

### 2. Aim

Select from arrays every way NumPy allows, and know which ways copy.

### 3. Steps

1. **Slice.**
2. **Tell a view from a copy.**
3. **Select with a boolean mask.**
4. **See why `and` raises.**
5. **Select with lists of indices.**
6. **Reshape.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

The view/copy behaviour is the point, and it is asserted three ways:

```python
a[1:4]                   # VIEW  -- a[1:4].base is a
a[a > 2]                 # COPY
a[[0, 2]]                # COPY
```

Also asserted: `m[[0,1,2],[1,2,3]]` gives **three paired elements**, not a 3×3
block — `np.ix_` is what gives the submatrix; and that `and` in a mask raises
`ValueError` while `&` works.
</div>


### 4. Programme

{{programme: course-9-python-da/03_indexing.py}}

### 5. Execution and Results

{{output: course-9-python-da/03_indexing.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A slice is a view; a boolean mask and a fancy index are copies; `and` raises where `&` works.
</div>


## Practical 4 — Universal functions and statistics

### 1. Question

Apply universal functions and mathematical and statistical functions to arrays.

### 2. Aim

Use NumPy's ufuncs and statistics, and know where its defaults differ from Pandas.

### 3. Steps

1. **Apply the unary ufuncs.**
2. **Tell np.maximum from np.max.**
3. **See NaN propagate.**
4. **Compute the statistics.**
5. **Set ddof, NumPy's against Pandas's.**
6. **Generate random numbers.**

<div class="formula" markdown="1">
<span class="label">THE ddof ASSERTION</span>

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
</div>


### 4. Programme

{{programme: course-9-python-da/04_ufuncs_stats.py}}

### 5. Execution and Results

{{output: course-9-python-da/04_ufuncs_stats.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

np.std gives 2.0 and Pandas 2.1381 for the same data: population against sample.
</div>


## Practical 5 — Create and manipulate Series and DataFrames

### 1. Question

Create and manipulate Pandas Series and DataFrames.

### 2. Aim

Build Series and DataFrames from dicts and lists, and inspect and extend them.

### 3. Steps

1. **Create a Series.**
2. **Create a DataFrame.**
3. **Inspect it.**
4. **Work with Index objects.**
5. **Add columns.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

```python
pd.Series([72,45,91], index=["Asha","Ravi","Meena"], name="marks")
pd.Series({"a": 1, "b": 2})            # from a dict
pd.DataFrame({"a":[1,2], "b":[3,4]})   # dict -> COLUMNS
pd.DataFrame([[1,3],[2,4]], columns=["a","b"])   # list -> ROWS
```

**A dict gives columns; a list of lists gives rows.** Getting these the wrong
way round transposes your table, and the script asserts both shapes.
</div>


### 4. Programme

{{programme: course-9-python-da/05_series_dataframe.py}}

### 5. Execution and Results

{{output: course-9-python-da/05_series_dataframe.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A dict gives columns and a list of lists rows; both shapes are asserted.
</div>


## Practical 6 — Indexing, selection, filtering and boolean indexing

### 1. Question

Select, filter and index the rows and columns of a DataFrame.

### 2. Aim

Select with [], loc and iloc, filter with masks and query, and set values safely in Pandas 3.

### 3. Steps

1. **Select with [], loc and iloc.**
2. **See loc include its end and iloc not.**
3. **Filter rows.**
4. **See why `and` raises.**
5. **Set values on a selection, under Pandas 3.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

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
</div>


### 4. Programme

{{programme: course-9-python-da/06_selection.py}}

### 5. Execution and Results

{{output: course-9-python-da/06_selection.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

loc includes its end label and iloc excludes its end position; chained assignment does nothing in Pandas 3, silently.
</div>


## Practical 7 — Arithmetic and data alignment

### 1. Question

Perform arithmetic between Series and DataFrames, and see how Pandas aligns them.

### 2. Aim

Add and subtract labelled data, and see alignment by label at work.

### 3. Steps

1. **Align arithmetic by label.**
2. **Fill the gaps with fill_value.**
3. **Combine a DataFrame and a Series.**
4. **Align two DataFrames.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

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
</div>


### 4. Programme

{{programme: course-9-python-da/07_alignment.py}}

### 5. Execution and Results

{{output: course-9-python-da/07_alignment.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Pandas adds by label, not position: `x` meets `x` though it sits at different positions, and a missing label gives NaN unless fill_value is set.
</div>


## Practical 8 — Sorting, ranking, dropping and duplicate indexes

### 1. Question

Sort and rank data, drop entries, and handle duplicate index labels.

### 2. Aim

Sort and rank, with each way of breaking ties, and see what duplicate labels do.

### 3. Steps

1. **Sort.**
2. **Rank, and break ties.**
3. **Drop rows and columns.**
4. **Handle duplicate index labels.**
5. **Find duplicate rows.**

<div class="formula" markdown="1">
<span class="label">RANKING TIES</span>

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
</div>


### 4. Programme

{{programme: course-9-python-da/08_sort_rank.py}}

### 5. Execution and Results

{{output: course-9-python-da/08_sort_rank.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The two 70s rank 2.5 by average, 2 by min and dense, 3 by max, and 2 and 3 by first; a duplicate label returns a Series where a unique one returns a scalar.
</div>


## Practical 9 — Read and write CSV, TXT, JSON and Excel

### 1. Question

Read and write data in CSV, TXT, JSON and Excel formats.

### 2. Aim

Round-trip data through each format, and avoid the four traps of reading it back.

### 3. Steps

1. **Write and read each format, in a temporary folder.**
2. **Flatten nested JSON.**

<div class="formula" markdown="1">
<span class="label">THE FOUR TRAPS</span>

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

`json_normalize` is asserted on Web Technologies' nested college document: nested keys
become dotted columns (`marks.maths`), which is what makes API data usable.
Document Oriented Database's MongoDB documents have the same shape.
</div>


### 4. Programme

{{programme: course-9-python-da/09_io.py}}

### 5. Execution and Results

{{output: course-9-python-da/09_io.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Every format round-trips; dtype=, parse_dates=, na_values= and index=False each fix a trap.
</div>


## Practical 10 — Detect, drop, fill and replace missing values

### 1. Question

Detect, drop, fill and replace the missing values in a dataset.

### 2. Aim

Find missing values, and handle them without distorting the data or leaking the test set.

### 3. Steps

1. **Detect the missing values.**
2. **See NaN never equal NaN.**
3. **See NaN turn integers to floats.**
4. **Drop them, and see how much goes.**
5. **See mean imputation shrink the spread.**
6. **Impute skewed data by the median.**
7. **Replace sentinel values first.**
8. **Impute after splitting.**
9. **Keep a flag of what was missing.**
10. **Fill forward, in order.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

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
</div>


### 4. Programme

{{programme: course-9-python-da/10_missing.py}}

### 5. Execution and Results

{{output: course-9-python-da/10_missing.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Mean imputation of 30% cut the spread by 16.3%, as 1 − √0.7 predicts; fitting on everything gave a fill value of 258.25 against 11.00 from the training rows.
</div>


## Practical 11 — Rename axes, remove duplicates, filter outliers

### 1. Question

Rename axes, remove duplicates, and filter outliers.

### 2. Aim

Clean names and duplicates, and find outliers by a rule the outliers cannot hide from.

### 3. Steps

1. **Clean the column names.**
2. **Rename the axes.**
3. **Remove duplicates.**
4. **Find outliers: the z-score's masking against the IQR.**
5. **Cap outliers instead of deleting them.**
6. **Apply domain rules first.**

<div class="formula" markdown="1">
<span class="label">MASKING</span>

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
</div>


### 4. Programme

{{programme: course-9-python-da/11_outliers.py}}

### 5. Execution and Results

{{output: course-9-python-da/11_outliers.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The z-score flags neither 250 nor 260, which inflate the SD to 112.75; the IQR rule flags both.
</div>


## Practical 12 — Transform data with mapping functions and string operations

### 1. Question

Transform data with mapping functions and string operations.

### 2. Aim

Recode values with map and replace, bin numbers, and vectorise rather than apply.

### 3. Steps

1. **Tell map from replace.**
2. **Use map, apply, applymap and replace.**
3. **Vectorise instead of apply.**
4. **Bin numbers into categories.**
5. **Transform strings.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

Asserted: `map` with an incomplete dict silently produces **NaN**, while
`replace` leaves unmatched values alone — the difference that catches people.

`cut` versus `qcut` on a skewed series: `cut(4)` gives counts `[8, 0, 0, 1]`
and `qcut(4)` gives `[3, 2, 2, 2]`. Equal-**width** against
equal-**frequency**, exactly Data Mining §2.9.
</div>


### 4. Programme

{{programme: course-9-python-da/12_transform.py}}

### 5. Execution and Results

{{output: course-9-python-da/12_transform.py}}

**The performance measurement:** `df.a + df.b` against
`df.apply(lambda r: r.a + r.b, axis=1)` on 200,000 rows; the run's figure is above, and the
script asserts the speed-up exceeds 50×. **Corrected:** this page said "roughly 2,900×", one
run's figure, as though it were fixed; the timing varies from run to run.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

map with an incomplete dict makes NaN where replace leaves values alone; cut gave [8,0,0,1] and qcut [3,2,2,2]; a + b was far faster than apply, by the figure above.
</div>


## Practical 13 — String operations and regular expressions

### 1. Question

Apply string operations and regular expressions to DataFrame columns.

### 2. Aim

Split, extract and validate text with the .str accessor and regular expressions.

### 3. Steps

1. **Use .str, which handles NaN.**
2. **Split strings.**
3. **Extract a roll number.**
4. **Compare extract, findall and extractall.**
5. **Pass na= to contains.**
6. **State regex= in replace.**
7. **Validate with patterns.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

```python
rolls.str.extract(r"(?P<year>\d{2})(?P<branch>[A-Z]{3})(?P<number>\d{4})")
```

Named groups become column names directly, and `0145` **keeps its leading
zero** because `extract` returns strings — right for an identifier, and the
script asserts it.

**The dtype-dependent `contains` behaviour**, verified on Pandas 3 and
worth knowing precisely:

| Column dtype | `str.contains` returns | Masking with it |
|---|---|---|
| `str` (Pandas 3 default) | `bool`, NaN → False | **Works** |
| `object` | `object`, NaN → None | **Raises ValueError** |

So `na=False` is no longer always required — and you should pass it anyway,
because you will not always know which dtype a column arrived with.
</div>


### 4. Programme

{{programme: course-9-python-da/13_strings.py}}

### 5. Execution and Results

{{output: course-9-python-da/13_strings.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

extract with named groups gives named columns and keeps leading zeros; str.contains needs na=False on an object column.
</div>


## Practical 14 — Dummy variables, permutation and random sampling

### 1. Question

Create dummy variables, and draw permutations and random samples.

### 2. Aim

Encode categories as dummies, and sample reproducibly, with and without stratification.

### 3. Steps

1. **One-hot encode, and avoid the dummy trap.**
2. **Encode multiple labels.**
3. **Tell ordinal from nominal.**
4. **Sample, reproducibly.**
5. **Bootstrap, and count the out-of-bag rows.**
6. **Stratify.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

Asserted: *k* dummy columns **sum to 1 in every row** — the collinearity
itself, demonstrated rather than asserted in prose — and `drop_first=True`
gives *k − 1* with the dropped level as the all-zeros reference.

**The bootstrap measurement:** drawing *n* indices with replacement from *n*
leaves about **36.8%** unselected, matching 1/e = 0.3679. That is the `.632`
in Data Mining's .632 bootstrap, and the mechanism behind bagging.

**Stratification, asserted:** on an 8-DS/2-Stats frame, an unstratified 50%
sample can miss Stats entirely; the stratified version always gives 4 and 1.

**A Pandas 3 note the script demonstrates:** `groupby().apply()` now
**excludes the grouping column** from each group, so a naive stratified sample
loses `dept`. Select the columns explicitly, or use
`train_test_split(..., stratify=...)`.
</div>


### 4. Programme

{{programme: course-9-python-da/14_dummies_sampling.py}}

### 5. Execution and Results

{{output: course-9-python-da/14_dummies_sampling.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

k dummies sum to 1 in every row; a bootstrap leaves 36.8% unchosen; unstratified samples lost the Stats students on 5 of 30 seeds, and stratified ones never.
</div>


## Practical 15 — Merge, join and concatenate

### 1. Question

Merge, join and concatenate datasets.

### 2. Aim

Combine tables every way Pandas offers, and catch the merges that fail silently.

### 3. Steps

1. **Merge four ways.**
2. **Use indicator= to see what failed.**
3. **Meet three things that break merges.**
4. **See duplicate keys explode the rows.**
5. **Concatenate.**
6. **Join on the index.**

<div class="formula" markdown="1">
<span class="label">THE FAILURE MODES</span>

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
</div>


### 4. Programme

{{programme: course-9-python-da/15_merge.py}}

### 5. Execution and Results

{{output: course-9-python-da/15_merge.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The four joins give 3, 4, 4 and 5 rows; a type mismatch gives none; duplicate keys give 12, and validate= refuses them.
</div>


## Practical 16 — Reshape with pivot, stack, unstack; hierarchical indexing

### 1. Question

Reshape data with pivot, stack and unstack, and use hierarchical indexing.

### 2. Aim

Move between long and wide forms, and index by several levels.

### 3. Steps

1. **Go from long to wide and back.**
2. **See pivot refuse duplicates.**
3. **Add margins to a pivot table.**
4. **Index hierarchically.**
5. **Stack and unstack.**
6. **Combine data that overlaps.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

Long → wide → long asserted as a round trip. `pivot` on a duplicated
`(name, subject)` pair **raises ValueError**; `pivot_table` succeeds and
**silently averages** to 91.5 unless you choose `aggfunc="max"` for 95 —
both asserted, because which is right is a question about your data.

The MultiIndex sort requirement is asserted as a raised
`UnsortedIndexError`, then fixed with `.sort_index()`.
</div>


### 4. Programme

{{programme: course-9-python-da/16_reshape.py}}

### 5. Execution and Results

{{output: course-9-python-da/16_reshape.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

pivot refuses a duplicate pair; pivot_table averages it to 91.5, or takes 95 with aggfunc="max".
</div>


## Practical 17 — Summary statistics grouped by level or category

### 1. Question

Compute summary statistics grouped by level or category.

### 2. Aim

Group, aggregate, transform and filter, and check that shares add up.

### 3. Steps

1. **Split, apply, combine.**
2. **Tell size from count.**
3. **Use agg, transform and filter.**
4. **Check that the shares sum to 100.**
5. **Group by several keys, and by level.**
6. **Cross-tabulate.**
7. **Recompute Course 4's statistics.**
8. **Find the correlations.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

`agg` gives 2 rows, `transform` gives 5 — asserted, because that is the
distinction students get wrong. `size()` includes NaN and `count()` does not.

**The share check:** percentages computed with `transform("sum")` as the
denominator sum to exactly 100 within each group. The script asserts it, which
is the habit worth forming — it catches a mis-grouped denominator immediately.
</div>


### 4. Programme

{{programme: course-9-python-da/17_groupby.py}}

### 5. Execution and Results

{{output: course-9-python-da/17_groupby.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

agg gives one row per group and transform one per row; shares computed with transform sum to 100 in every group.
</div>


## Practical 18 — Basic visualizations with matplotlib

### 1. Question

Draw basic visualisations with matplotlib, and with Seaborn and Plotly.

### 2. Aim

Draw the four basic chart types, label them, and draw them honestly.

### 3. Steps

1. **Draw the plots, into plots/.**
2. **Draw honest charts.**

<div class="formula" markdown="1">
<span class="label">THE POINT</span>

Runs under the **Agg** backend, so it opens no window and writes PNG files to
`plots/`, beside the program. Asserted: each file exists and is non-empty; each axes
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
</div>


### 4. Programme

{{programme: course-9-python-da/18_plots.py}}

### 5. Execution and Results

{{output: course-9-python-da/18_plots.py}}

The images are the PNG files the program wrote, in name order: two charts from the
object-oriented interface, the four-panel overview, the pandas chart and the Seaborn one. Plotly's
chart is an HTML page, `interactive.html`, and is not shown.

**Changed:** the program wrote its charts to a temporary directory, deleted when it finished,
so no one could see them. It now writes them to `plots/`.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The charts are drawn and labelled, shown above; a bar axis that starts at 90 makes a 5.3% difference look twofold.
</div>


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
