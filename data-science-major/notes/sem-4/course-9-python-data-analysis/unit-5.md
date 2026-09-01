# Unit 5 — Data Wrangling, Reshaping and Visualization

**Syllabus topics:** Merging and joining datasets, concatenating along an
axis, combining data with overlap, reshaping with pivot, stack and unstack,
basic hierarchical indexing, summary statistics by group or level.
Introduction to matplotlib — plots, customization, styling; Seaborn for
statistical data visualization; Plotly for interactive charts and dashboards.

> **This unit is overloaded.** It carries merging, concatenation, reshaping,
> hierarchical indexing, grouped statistics **and** three plotting libraries.
> Treat §§5.1–5.7 and §§5.8–5.11 as two separate topics with a week each.

---

## 5.1 Merging and joining

### 🎯 The big idea

`pd.merge` is **SQL's JOIN**. If you learned Course 5, you already know this;
only the syntax is new.

```python
students = pd.DataFrame({"roll": [21, 22, 23, 24],
                         "name": ["Asha", "Ravi", "Meena", "Kiran"]})
marks    = pd.DataFrame({"roll": [21, 22, 23, 25],
                         "marks": [88, 65, 94, 70]})

pd.merge(students, marks, on="roll")                    # INNER by default
pd.merge(students, marks, on="roll", how="left")
pd.merge(students, marks, on="roll", how="right")
pd.merge(students, marks, on="roll", how="outer")
pd.merge(students, marks, how="cross")                  # Cartesian product
```

### 🔢 The join types

| `how` | Keeps | SQL |
|---|---|---|
| `"inner"` (default) | Keys in **both** | `INNER JOIN` |
| `"left"` | **All** left rows | `LEFT OUTER JOIN` |
| `"right"` | **All** right rows | `RIGHT OUTER JOIN` |
| `"outer"` | The **union** of keys | `FULL OUTER JOIN` |
| `"cross"` | Every pair | `CROSS JOIN` |

With the data above:

```
inner  -> rolls 21, 22, 23              (3 rows — roll 24 and 25 dropped)
left   -> rolls 21, 22, 23, 24          (4 rows — Kiran's marks are NaN)
right  -> rolls 21, 22, 23, 25          (4 rows — roll 25 has no name)
outer  -> rolls 21, 22, 23, 24, 25      (5 rows)
```

**Note that `inner` silently discards rows.** That is the correct behaviour and
it is also how analyses quietly lose data. Always compare the row count before
and after.

### The parameters

```python
pd.merge(a, b, on="roll")
pd.merge(a, b, on=["roll", "year"])              # composite key
pd.merge(a, b, left_on="id", right_on="roll")    # differently named keys
pd.merge(a, b, left_index=True, right_index=True)
pd.merge(a, b, on="roll", suffixes=("_left", "_right"))
pd.merge(a, b, on="roll", indicator=True)        # adds a _merge column
pd.merge(a, b, on="roll", validate="one_to_one")
a.join(b)                                         # on the INDEX by default
```

### 💡 `indicator=True` and `validate=` are the two you should actually use

```python
m = pd.merge(students, marks, on="roll", how="outer", indicator=True)
m._merge.value_counts()
```
```
both          3
left_only     1        ← Kiran has no marks row
right_only    1        ← roll 25 has no student row
```

**`indicator=True` tells you what failed to match**, which is the question you
actually have when a merge produces the wrong row count.

**`validate=` catches the row explosion.** If both sides have duplicate keys,
the result is the **Cartesian product** of matching rows: 3 × 4 duplicates
become 12 rows. A merge that mysteriously multiplies your data is nearly always
this.

| `validate` | Asserts |
|---|---|
| `"one_to_one"` | Keys unique on **both** sides |
| `"one_to_many"` | Unique on the **left** |
| `"many_to_one"` | Unique on the **right** |
| `"many_to_many"` | No check |

**Use it every time.** It converts a silent data corruption into an immediate
error, which is exactly the trade you want.

### ⚠️ Three things that break merges

**1. Type mismatch.** `roll` as `int64` on one side and text on the other.
Older Pandas matched **nothing** and returned an empty DataFrame **with no
error** — a notorious silent failure. **Pandas 3 raises a `ValueError`
instead** ("You are trying to merge on int64 and str columns"), which is a real
improvement, but you still have to fix the dtypes. Check `df.dtypes` on both
sides first.

**2. Whitespace and case.** `"DS"` and `"DS "` are different keys. Clean the
key columns before joining:
`df["key"] = df.key.str.strip().str.upper()`

**3. Missing keys — and Pandas does NOT behave like SQL here.** In SQL,
`NULL = NULL` is never true, so null-keyed rows never join. **Pandas joins NaN
to NaN.** On identical data (`[1, NaN, NaN]` joined to `[1, NaN]`), Pandas
returns **3 rows** and SQLite returns **1** — the lab asserts both.

So a null key silently *multiplies* rows in Pandas where it would silently
*drop* them in SQL. Course 5's mental model does not transfer; drop or fill
null keys before merging.

## 5.2 Concatenating along an axis

`concat` **stacks**; `merge` **matches**. That is the whole distinction.

```python
pd.concat([df1, df2])                        # stack ROWS (axis=0)
pd.concat([df1, df2], axis=1)                # stack COLUMNS
pd.concat([df1, df2], ignore_index=True)     # renumber 0..n-1
pd.concat([df1, df2], keys=["sem3", "sem4"]) # a MultiIndex marking the source
pd.concat([df1, df2], join="inner")          # keep only shared columns
pd.concat([df1, df2], verify_integrity=True) # raise on duplicate index labels
```

| | `concat` | `merge` |
|---|---|---|
| Combines by | **Stacking** | **Matching keys** |
| Direction | Rows or columns | Columns, by key |
| Needs a key? | No | Yes |
| Analogy | SQL `UNION ALL` | SQL `JOIN` |

### ⚠️ `concat` aligns on labels too

```python
a = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
b = pd.DataFrame({"y": [5, 6], "z": [7, 8]})
pd.concat([a, b])
```

```
     x  y    z
0  1.0  3  NaN
1  2.0  4  NaN
0  NaN  5  7.0
1  NaN  6  8.0
```

Non-matching **columns** become NaN, and the **index repeats** — note the two
0s and two 1s. Note also that `y` stays **int64** while `x` and `z` become
float: only the columns that actually gained a NaN are upcast. That duplicated index causes exactly the problems of Unit 2 §2.9.

**`ignore_index=True` is almost always what you want** when stacking rows, and
forgetting it is the most common concat mistake.

## 5.3 Combining data with overlap

When two datasets partly overlap and you want to **patch** one with the other
rather than join them:

```python
a = pd.Series([1, np.nan, 3, np.nan])
b = pd.Series([10, 20, 30, 40])

a.combine_first(b)          # [1.0, 20.0, 3.0, 40.0] — b fills a's gaps
df1.combine_first(df2)      # the same, column by column
df1.update(df2)             # IN PLACE: df2's non-null values overwrite df1's
np.where(a.isna(), b, a)    # the explicit version
a.combine(b, max)           # element-wise with any function
```

### ⚠️ `combine_first` versus `update`

| | `combine_first` | `update` |
|---|---|---|
| Returns | A **new** object | **None** — modifies in place |
| Fills | Only where the caller is **NaN** | **Overwrites** wherever the other is non-null |
| Index/columns | **Union** of both | Only the caller's — extras ignored |

`combine_first` is "fill my gaps from you". `update` is "take your values over
mine". They are not interchangeable, and `update`'s in-place, returns-None
behaviour surprises people who write `df = df1.update(df2)` and get `None`.

## 5.4 Hierarchical indexing

A **MultiIndex** gives an axis more than one level, letting a 2-D DataFrame
represent higher-dimensional data.

```python
df = pd.DataFrame({
    "dept":    ["DS", "DS", "Stats", "Stats", "DS", "Stats"],
    "year":    [1, 2, 1, 2, 1, 2],
    "student": ["Asha", "Ravi", "Meena", "Kiran", "Bhanu", "Devi"],
    "marks":   [88, 65, 94, 71, 52, 79],
})

h = df.set_index(["dept", "year"]).sort_index()
```

```
            student  marks
dept  year
DS    1        Asha     88
      1       Bhanu     52
      2        Ravi     65
Stats 1       Meena     94
      2       Kiran     71
      2        Devi     79
```

### Selecting

```python
h.loc["DS"]                    # everything under DS
h.loc[("DS", 1)]               # a specific pair — note the TUPLE
h.loc[("DS", 1), "marks"]
h.loc["DS":"Stats"]            # a slice of the outer level
h.xs(1, level="year")          # cross-section: year 1, ALL departments
h.loc[(slice(None), 1), :]     # the same, with slice(None)
h.loc[pd.IndexSlice[:, 1], :]  # the same, more readably

h.index.names                  # FrozenList(['dept', 'year'])
h.index.levels                 # the distinct values per level
h.reset_index()                # back to flat columns
h.swaplevel()                  # exchange the levels
h.sort_index(level="year")
```

### ⚠️ Sort a MultiIndex before slicing it

```python
h = df.set_index(["dept", "year"])       # NOT sorted
h.loc["DS":"Stats"]
# UnsortedIndexError: 'Key length (1) was greater than MultiIndex lexsort depth (0)'
h.sort_index().loc["DS":"Stats"]         # fine
```

Slicing a MultiIndex requires it to be **lexically sorted**, because the slice
is resolved by binary search. `.sort_index()` immediately after `set_index` is
the habit to form — and it makes lookups faster besides.

### Statistics by level

```python
h.groupby(level="dept").marks.mean()
h.groupby(level=["dept", "year"]).marks.sum()
h.marks.mean(level="dept")               # removed in Pandas 2 — use groupby
```

## 5.5 Reshaping: pivot, stack, unstack

### 🎯 Long versus wide

The single most useful idea in this section.

```
LONG (tidy)                      WIDE
name  subject  marks             name   maths  stats
Asha  maths    88                Asha      88     91
Asha  stats    91         <->    Ravi      65     58
Ravi  maths    65
Ravi  stats    58
```

**Long is better for computing** — one row per observation, easy to filter,
group and plot. **Wide is better for reading** — it is what a person wants in a
report. You will convert between them constantly.

### 🔢 The four functions

| Function | Direction | Handles duplicates? |
|---|---|---|
| **`pivot`** | Long → wide | **No** — raises |
| **`pivot_table`** | Long → wide | **Yes** — aggregates |
| **`melt`** | Wide → long | — |
| **`stack` / `unstack`** | Between columns and index levels | — |

```python
long = pd.DataFrame({
    "name":    ["Asha", "Asha", "Ravi", "Ravi"],
    "subject": ["maths", "stats", "maths", "stats"],
    "marks":   [88, 91, 65, 58],
})

wide = long.pivot(index="name", columns="subject", values="marks")
```
```
subject  maths  stats
name
Asha        88     91
Ravi        65     58
```

```python
back = wide.reset_index().melt(id_vars="name",
                               var_name="subject", value_name="marks")
```

### ⚠️ `pivot` versus `pivot_table`

```python
long.pivot(index="name", columns="subject", values="marks")
# ValueError: Index contains duplicate entries, cannot reshape
#   -- if any (name, subject) pair appears twice

long.pivot_table(index="name", columns="subject", values="marks",
                 aggfunc="mean")      # averages the duplicates instead
```

**`pivot` is a pure reshape and requires the index/column pairs to be unique.
`pivot_table` aggregates, so duplicates are fine — and it silently averages
them, which you must actually want.**

```python
pd.pivot_table(df, index="dept", columns="year", values="marks",
               aggfunc=["mean", "count"], margins=True, fill_value=0)
```

`margins=True` adds row and column totals — a "grand total" row labelled `All`,
which is what a report usually needs.

### stack and unstack

```python
wide.stack()          # columns -> an INNER index level   (wide -> long)
h.unstack()           # the innermost index level -> columns (long -> wide)
h.unstack(level=0)    # a specific level
h.unstack(level="year")
wide.stack().unstack()   # a round trip, back to where you started
```

**Mnemonic: `stack` makes it *taller*, `unstack` makes it *wider*.**

### ⚠️ `unstack` refuses duplicates, exactly as `pivot` does

The `h` above has **two** DS/year-1 students (Asha and Bhanu) and two
Stats/year-2 students (Kiran and Devi), so:

```python
h.unstack("year")
# ValueError: Index contains duplicate entries, cannot reshape
```

That is the same rule as §5.5: a reshape cannot put two values in one cell.
**Aggregate to unique pairs first**, and then it works:

```python
h.groupby(level=["dept", "year"]).marks.mean().unstack("year")
```
```
year      1     2
dept
DS     70.0  65.0        ← (88 + 52) / 2 = 70
Stats  94.0  75.0        ← (71 + 79) / 2 = 75
```

On a subset where each (dept, year) pair *is* unique, the shape comes out as
you would expect:

```python
h[h.student.isin(["Asha", "Ravi", "Meena", "Kiran"])].unstack("year")
```
```
      student        marks
year        1      2     1   2
dept
DS       Asha   Ravi    88  65
Stats   Meena  Kiran    94  71
```

Note the result has a **MultiIndex on the columns** — unstacking pushed a row
level up into the columns.

## 5.6 Summary statistics by group

### 🎯 Split–apply–combine

```
   SPLIT              APPLY              COMBINE
df ------> groups ------> a value ------> one result per group
   by key         per group
```

```python
df.groupby("dept").marks.mean()
df.groupby("dept").marks.agg(["mean", "median", "std", "count", "min", "max"])
df.groupby(["dept", "year"]).marks.mean()
df.groupby("dept").agg(avg=("marks", "mean"),
                       top=("marks", "max"),
                       n=("marks", "size"))          # NAMED aggregation
df.groupby("dept").size()                            # rows per group
df.groupby("dept").marks.describe()
df.groupby("dept", as_index=False).marks.mean()      # keep 'dept' as a column
df.groupby("dept", dropna=False)                     # include the NaN group
df.groupby(pd.Grouper(key="date", freq="ME")).marks.mean()   # by month
```

### ⚠️ `size` versus `count`

```python
df.groupby("dept").size()          # rows per group — INCLUDES NaN
df.groupby("dept").marks.count()   # NON-NULL values per group
```

They differ exactly by the number of missing values, and the difference is
often the interesting thing.

### `agg` versus `transform` versus `filter` versus `apply`

| Method | Returns |
|---|---|
| `agg` | **One row per group** |
| `transform` | **One value per original row** |
| `filter` | A **subset of rows**, whole groups kept or dropped |
| `apply` | Anything |

```python
df.groupby("dept").marks.agg("mean")             # 2 rows
df.groupby("dept").marks.transform("mean")       # 6 values, one per row
df.groupby("dept").filter(lambda g: len(g) >= 3) # only groups of 3+
```

**`transform` is what you use to add a group statistic back as a column**, and
it is the one students most often reach for `agg` instead — producing a length
mismatch.

```python
df["dept_mean"] = df.groupby("dept").marks.transform("mean")
df["above_avg"] = df.marks > df.dept_mean
df["pct_of_dept_total"] = df.marks / df.groupby("dept").marks.transform("sum")
```

### 🔢 Cross-tabulation

```python
pd.crosstab(df.dept, df.year)                            # counts
pd.crosstab(df.dept, df.year, normalize="index")         # row proportions
pd.crosstab(df.dept, df.year, values=df.marks, aggfunc="mean")
pd.crosstab(df.dept, df.year, margins=True)              # with totals
```

`crosstab` is `pivot_table` specialised to counting, and it is the fastest way
to produce the contingency tables of Course 4 Unit 5's chi-square test.

## 5.7 Recomputing Course 4 in Pandas

**This section closes finding [D8](../../../SYLLABUS-REVIEW.md).** Course 4
taught these statistics by hand; here they are as one-line method calls, on
the same numbers.

```python
x = pd.Series([2, 4, 4, 4, 5, 5, 7, 9])

x.mean()                 # 5.0
x.median()               # 4.5
x.mode()[0]              # 4
x.var()                  # 4.5714  — SAMPLE, ddof=1
x.var(ddof=0)            # 4.0     — POPULATION
x.std()                  # 2.1381  — SAMPLE
x.std(ddof=0)            # 2.0     — POPULATION
x.quantile([0.25, 0.5, 0.75])
x.skew()  x.kurt()
x.describe()
```

### ⚠️ Pandas and NumPy disagree by default

```python
np.std(x)            # 2.0     — ddof=0, POPULATION
pd.Series(x).std()   # 2.1381  — ddof=1, SAMPLE
```

**NumPy defaults to the population formula and Pandas to the sample formula.**
The same data, two libraries, two answers. Course 4 Unit 2 taught that the
sample standard deviation divides by *n − 1*; Pandas agrees, NumPy does not.
**State which you mean, and pass `ddof` explicitly** when it matters.

### Correlation and regression

```python
df[["maths", "stats"]].corr()                 # Pearson matrix
df.maths.corr(df.stats)                       # one number
df.maths.corr(df.stats, method="spearman")    # rank correlation
df[["maths", "stats"]].cov()

from scipy import stats
slope, intercept, r, p, se = stats.linregress(df.maths, df.stats)
```

Course 4's worked regression, its correlation coefficient and its t-test all
reappear here as single calls — and the Course 9 lab **asserts that the Pandas
answers match the hand-computed values in Course 4's notes**, so the two courses
cannot drift apart.

## 5.8 matplotlib

```python
import matplotlib
matplotlib.use("Agg")          # a NON-INTERACTIVE backend: saves files,
                               # opens no window -- required on a server
import matplotlib.pyplot as plt
```

### The two interfaces

```python
# pyplot (stateful) -- fine for a quick look
plt.plot(x, y)
plt.title("Marks")
plt.show()

# object-oriented -- USE THIS for anything real
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, label="maths")
ax.set_title("Marks by student")
ax.set_xlabel("Student")
ax.set_ylabel("Marks")
ax.legend()
fig.savefig("marks.png", dpi=150, bbox_inches="tight")
plt.close(fig)
```

**The object-oriented interface is the one to learn.** `pyplot` keeps a hidden
"current figure", which breaks the moment you have two plots, a loop or a
function. Explicit `fig, ax` never does.

### The plot types

| Plot | Call | For |
|---|---|---|
| Line | `ax.plot(x, y)` | Trends over an ordered axis |
| Bar | `ax.bar(x, h)` / `ax.barh` | Comparing categories |
| Histogram | `ax.hist(v, bins=20)` | **One variable's distribution** |
| Scatter | `ax.scatter(x, y)` | Two variables' relationship |
| Box | `ax.boxplot(data)` | Distribution and outliers |
| Pie | `ax.pie(v, labels=…)` | Parts of a whole — use sparingly |
| Heatmap | `ax.imshow(m)` | A matrix |

### ⚠️ Histogram versus bar chart

A **histogram** shows the distribution of **one continuous variable**: the bars
are *bins* and touch each other, because the axis is continuous. A **bar chart**
compares **categories**: the bars have gaps, because there is nothing between
"DS" and "Stats".

Drawing categorical counts as a histogram, or a distribution as a bar chart, is
a guaranteed lost mark.

### Customisation and subplots

```python
ax.plot(x, y, color="#2b4c7e", linewidth=2, linestyle="--",
        marker="o", markersize=6, alpha=0.8, label="maths")
ax.set_xlim(0, 100);  ax.set_ylim(0, 100)
ax.set_xticks(range(0, 101, 20))
ax.tick_params(axis="x", rotation=45)
ax.grid(True, alpha=0.3)
ax.annotate("topper", xy=(3, 94), xytext=(4, 80),
            arrowprops=dict(arrowstyle="->"))
ax.axhline(df.marks.mean(), color="red", linestyle=":", label="mean")

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].hist(df.marks)
axes[0, 1].scatter(df.maths, df.stats)
fig.suptitle("Overview")
fig.tight_layout()

plt.style.use("seaborn-v0_8-whitegrid")
```

### Pandas' own plotting

```python
df.plot(kind="line")
df.marks.plot(kind="hist", bins=20)
df.plot(kind="scatter", x="maths", y="stats")
df.groupby("dept").marks.mean().plot(kind="bar")
df.plot(kind="box")
```

A thin matplotlib wrapper, and the quickest way to look at a DataFrame. It
returns an `Axes`, so you can customise it exactly as above.

## 5.9 Seaborn

**Seaborn is matplotlib for statistical graphics**: it knows about DataFrames,
handles grouping by colour, and computes the statistics for you.

```python
import seaborn as sns

sns.histplot(data=df, x="marks", hue="dept", kde=True)
sns.boxplot(data=df, x="dept", y="marks")
sns.violinplot(data=df, x="dept", y="marks")     # box + density
sns.scatterplot(data=df, x="maths", y="stats", hue="dept", size="total")
sns.regplot(data=df, x="maths", y="stats")       # scatter + FITTED LINE + CI
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", center=0)
sns.pairplot(df, hue="dept")                     # every pair, at once
sns.barplot(data=df, x="dept", y="marks")        # mean + CONFIDENCE INTERVAL
sns.countplot(data=df, x="dept")                 # counts
sns.lineplot(data=df, x="year", y="marks", hue="dept")
sns.set_theme(style="whitegrid", palette="deep")
```

| | matplotlib | Seaborn |
|---|---|---|
| Input | Arrays | **DataFrames**, with column names |
| Grouping | Manual loop | `hue=`, `col=`, `row=` |
| Statistics | You compute them | **Computed for you** — CIs, KDE, regression |
| Defaults | Plain | Attractive |
| Control | **Total** | Less, but it returns matplotlib axes |

**`sns.pairplot(df, hue="dept")` in one line** produces the scatter-plot matrix
that Course 8's Experiment 5 built by hand in WEKA. **`sns.heatmap(df.corr())`**
is the fastest way to spot redundant features.

Note that `sns.barplot` shows the **mean with a confidence interval**, not a
raw count — `countplot` is the one for counts. Confusing them is common.

## 5.10 Plotly

**Plotly makes interactive charts** — hover tooltips, zoom, pan, click-to-hide
— that render as HTML.

```python
import plotly.express as px

fig = px.scatter(df, x="maths", y="stats", color="dept",
                 size="total", hover_data=["name"],
                 title="Maths vs Statistics")
fig.write_html("scatter.html")          # standalone, opens in any browser
fig.write_image("scatter.png")          # static, needs the kaleido package

px.bar(df, x="dept", y="marks", color="year", barmode="group")
px.line(ts, x="date", y="value", color="series")
px.box(df, x="dept", y="marks")
px.histogram(df, x="marks", nbins=20, color="dept")
px.imshow(df.corr(numeric_only=True), text_auto=True)
```

`plotly.express` is the high-level interface — one call per chart. The
lower-level `plotly.graph_objects` gives full control when you need it.

### 🔢 Which library, when

| | matplotlib | Seaborn | Plotly |
|---|---|---|---|
| Output | Static image | Static image | **Interactive HTML** |
| Best for | Publication figures, full control | **Statistical exploration** | Dashboards, web, presentation |
| Learning curve | Steepest | Gentle | Gentle |
| DataFrame-aware | No | **Yes** | **Yes** |
| File size | Small PNG | Small PNG | Large HTML (bundles JS) |
| Works in a report/print | **Yes** | **Yes** | No — it needs a browser |

**The practical answer: Seaborn for exploring, matplotlib for the final static
figure, Plotly when someone needs to interact with it.** Seaborn returns
matplotlib axes, so you can start in Seaborn and finish in matplotlib —
which is what most people actually do.

Plotly's output embeds a JavaScript library, so a "simple" chart can be a
3 MB HTML file. That is fine on a web page (Course 7) and wrong in an email.

## 5.11 Making a chart honest

Worth a mark, and worth more than a mark outside the exam:

- **Label both axes, with units.** An unlabelled axis makes a chart unreadable.
- **Start a bar chart's y-axis at zero.** Truncating it exaggerates differences
  — the classic misleading chart. A *line* chart of a trend may legitimately
  start elsewhere; a bar chart may not, because the bar's *length* is the
  encoding.
- **Do not use a pie chart for more than about five categories**, and never for
  values that are not parts of one whole.
- **Choose a colourmap that survives colour-blindness and greyscale** —
  `viridis`, not `jet`. Roughly 8% of men have some form of colour vision
  deficiency.
- **Use a diverging colourmap only around a meaningful midpoint** — a
  correlation heatmap centred at 0, not at the data's mean.
- **Do not plot a mean without a measure of spread.** Two groups with the same
  mean and very different variance are not the same, and a bare bar chart
  cannot show that. Seaborn's `barplot` adds a confidence interval for exactly
  this reason.

---

## Practice problems

### Problem 1

```python
students = pd.DataFrame({"roll": [21, 22, 23, 24],
                         "name": ["Asha", "Ravi", "Meena", "Kiran"]})
marks    = pd.DataFrame({"roll": [21, 22, 23, 25],
                         "marks": [88, 65, 94, 70]})
```

Give the row count and contents for each `how`, and say how to find the
non-matching rows.

**Solution.**

| `how` | Rows | Keys | Notes |
|---|:---:|---|---|
| `inner` | **3** | 21, 22, 23 | Kiran and roll 25 dropped |
| `left` | **4** | 21, 22, 23, 24 | Kiran's `marks` is NaN |
| `right` | **4** | 21, 22, 23, 25 | Roll 25's `name` is NaN |
| `outer` | **5** | 21–25 | Both NaNs present |

```python
m = pd.merge(students, marks, on="roll", how="outer", indicator=True)
m._merge.value_counts()
```
```
both          3
left_only     1        ← roll 24, Kiran: a student with no marks record
right_only    1        ← roll 25: a marks record with no student
```

```python
m[m._merge == "left_only"]     # students missing marks
m[m._merge == "right_only"]    # orphaned marks
```

**`indicator=True` is the answer to the last part**, and it is the right habit:
it turns "why did I get 3 rows instead of 4?" into a table you can read.

Note also `validate="one_to_one"` here — both `roll` columns are unique, so it
passes, and it would raise immediately if a duplicate ever appeared.

### Problem 2

Convert this long table to wide, then back, and explain when `pivot` fails.

```python
long = pd.DataFrame({
    "name":    ["Asha", "Asha", "Ravi", "Ravi", "Meena", "Meena"],
    "subject": ["maths", "stats", "maths", "stats", "maths", "stats"],
    "marks":   [88, 91, 65, 58, 94, 89],
})
```

**Solution.**

```python
wide = long.pivot(index="name", columns="subject", values="marks")
```
```
subject  maths  stats
name
Asha        88     91
Meena       94     89
Ravi        65     58
```

```python
back = (wide.reset_index()
            .melt(id_vars="name", var_name="subject", value_name="marks"))
```

Six rows again — though **sorted differently**, because `pivot` sorts the index
alphabetically. Compare with `sort_values` before asserting equality.

**When `pivot` fails.** Add a second maths mark for Asha — a re-sit:

```python
long2 = pd.concat([long, pd.DataFrame({"name": ["Asha"], "subject": ["maths"],
                                       "marks": [95]})])
long2.pivot(index="name", columns="subject", values="marks")
# ValueError: Index contains duplicate entries, cannot reshape
```

The pair `(Asha, maths)` now appears twice, and `pivot` cannot put two values
in one cell. It is a **pure reshape** and refuses to guess.

```python
long2.pivot_table(index="name", columns="subject", values="marks",
                  aggfunc="mean")     # Asha's maths becomes 91.5
long2.pivot_table(index="name", columns="subject", values="marks",
                  aggfunc="max")      # or 95, if the re-sit supersedes
```

**`pivot_table` aggregates**, so it succeeds — but notice that it *silently
averages* unless you choose `aggfunc`. Whether 91.5 or 95 is right is a
question about your data, not about Pandas, and the default will quietly answer
it for you if you let it.

### Problem 3

Given a DataFrame with `dept`, `year` and `marks`, compute: the mean by
department, mean and count by department and year, each student's marks as a
percentage of their department's total, and a department × year table of means
with totals.

**Solution.**

```python
# 1. Mean by department
df.groupby("dept").marks.mean()

# 2. Mean and count by department and year -- named aggregation is clearest
df.groupby(["dept", "year"]).agg(
    mean_marks=("marks", "mean"),
    n=("marks", "size"),
).reset_index()

# 3. Each student's share of their department's total -- TRANSFORM, not agg
df["pct_of_dept"] = (df.marks / df.groupby("dept").marks.transform("sum") * 100)

# 4. A department x year table with totals
pd.pivot_table(df, index="dept", columns="year", values="marks",
               aggfunc="mean", margins=True, margins_name="All")
```

**Why `transform` in step 3.** `df.groupby("dept").marks.sum()` returns one row
per department — two values for a six-row DataFrame — so dividing by it raises
a length mismatch, or worse, aligns on the wrong axis. `transform("sum")`
returns the department total **repeated for every row of that department**, so
the division is element-wise and correct.

**Check your work:** the percentages must sum to 100 within each department.

```python
df.groupby("dept").pct_of_dept.sum()      # 100.0 for every department
```

That check is worth writing every time you compute a share — it catches a
mis-grouped denominator immediately.

---

## Exam questions from this unit

**Two marks**

1. Distinguish `merge` from `concat`.
2. Name the four join types and what each keeps.
3. What does `indicator=True` do?
4. Why use `validate=` on a merge?
5. Distinguish `combine_first` from `update`.
6. Why must a MultiIndex be sorted before slicing?
7. Distinguish `pivot` from `pivot_table`.
8. Distinguish `stack` from `unstack`.
9. Distinguish `agg` from `transform`.
10. Distinguish `size` from `count` in a groupby.
11. Distinguish a histogram from a bar chart.
12. Why do NumPy and Pandas give different standard deviations?

**Five marks**

1. Explain merging with all the join types and an example of each.
2. Explain concatenation, and how it differs from merging.
3. Explain hierarchical indexing with selection examples.
4. Explain reshaping with pivot, melt, stack and unstack.
5. Explain split–apply–combine with `agg`, `transform` and `filter`.
6. Explain matplotlib's two interfaces and the main plot types.
7. Compare matplotlib, Seaborn and Plotly.

**Ten marks**

1. Given two datasets, write and explain a complete pipeline: merge, clean,
   reshape, aggregate and visualise.
2. Explain reshaping exhaustively — long versus wide, and all four functions —
   with worked examples.
3. Explain the three visualization libraries with examples, and the principles
   of an honest chart.

## Mistakes that cost marks

- Using `merge` where `concat` was needed, or the reverse
- Forgetting that `inner` is the default and silently losing rows
- Merging on columns of different dtypes and getting an empty result
- Not cleaning whitespace from key columns before joining
- Merging on duplicated keys and getting a Cartesian product
- Forgetting `ignore_index=True` when stacking rows
- Slicing an unsorted MultiIndex
- Using `pivot` on data with duplicate index/column pairs
- Letting `pivot_table` silently average duplicates you did not know about
- Using `agg` where `transform` was needed
- Confusing `size` (all rows) with `count` (non-null)
- Drawing categorical counts as a histogram
- Truncating a bar chart's y-axis
- Quoting `np.std` as the sample standard deviation
- Using `pyplot`'s stateful interface inside a loop or a function
