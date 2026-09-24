# Unit 4 — String Operations and Feature Engineering

**Syllabus topics:** String methods in Pandas, basic regular expressions,
vectorized string functions, creating dummy/indicator variables, permutation
and random sampling.

---

## 4.1 The `.str` accessor

### 🎯 The big idea

Python's string methods work on one string. Pandas' **`.str` accessor** applies
them to a whole column at once — and, crucially, **skips NaN instead of
crashing on it**.

```python
s = pd.Series(["  Asha Kumari ", "RAVI TEJA", "meena devi", None])

s.str.strip()                # whitespace off both ends
s.str.lower()                # asha kumari, ravi teja, meena devi, NaN
s.str.upper()
s.str.title()                # Asha Kumari
s.str.len()                  # 14.0, 9.0, 10.0, NaN   ← note float, because NaN
```

### ⚠️ Why not just use `apply`?

```python
s.apply(str.lower)      # AttributeError on the None
s.str.lower()           # NaN stays NaN — no crash
```

`.str` handles missing values for free. That alone is reason enough to prefer
it, and it is faster besides.

Note that `.str.len()` returns **float64** when the column contains NaN,
because there is no NaN in int64 — the same upcast as Unit 3 §3.3.

### The methods

| Method | Does |
|---|---|
| `strip`, `lstrip`, `rstrip` | Trim whitespace |
| `lower`, `upper`, `title`, `capitalize`, `swapcase` | Case |
| `len` | Length |
| `contains(pat)` | Boolean — **regex by default** |
| `startswith`, `endswith` | Boolean — **literal**, not regex |
| `replace(old, new)` | Substitute |
| `split(sep)`, `rsplit` | To a list, or `expand=True` for columns |
| `cat(sep=)` | Join a whole column into one string |
| `get(i)`, `slice(a, b)`, `[a:b]` | Substring |
| `pad`, `zfill`, `center` | Padding |
| `find`, `index` | Position |
| `count(pat)` | Occurrences |
| `extract(pat)`, `extractall` | Regex capture groups |
| `match`, `fullmatch` | Anchored regex test |
| `isdigit`, `isalpha`, `isnumeric`, `isspace` | Character-class tests |
| `normalize` | Unicode normalisation |

```python
names = pd.Series(["Asha Kumari", "Ravi Teja", "Meena Devi"])

names.str.split(" ")                    # lists: ['Asha', 'Kumari'], ...
names.str.split(" ", expand=True)       # TWO COLUMNS
names.str.split(" ").str[0]             # first names
names.str.split(" ", expand=True)[1]    # surnames
names.str.cat(sep=", ")                 # 'Asha Kumari, Ravi Teja, Meena Devi'
names.str[0]                            # first character: A, R, M
names.str[-4:]                          # last four characters
names.str.replace(" ", "_")
```

**`expand=True` is the one to remember**: it turns a split into real columns,
which is what you almost always want. Without it you get a column of Python
lists, which cannot be computed with.

## 4.2 Regular expressions in Pandas

Course 7 Unit 3 covered regex syntax; here is how Pandas uses it.

```python
s = pd.Series(["Asha 23 DS", "Ravi 24 Stats", "Meena 25 DS"])

s.str.contains(r"\d{2}")                 # regex — the DEFAULT
s.str.contains("DS", regex=False)        # literal — faster and safer
s.str.extract(r"(\w+) (\d+) (\w+)")      # 3 columns from 3 GROUPS
s.str.extract(r"(?P<name>\w+) (?P<roll>\d+)")   # NAMED groups -> column names
s.str.extractall(r"(\d)")                # EVERY match, a MultiIndex result
s.str.findall(r"\d+")                    # every match, as a list per row
s.str.replace(r"\d+", "N", regex=True)
s.str.count(r"[aeiou]")
s.str.match(r"^[A-Z]")                   # anchored at the START
s.str.fullmatch(r"[A-Za-z ]+")           # must match the WHOLE string
```

### 🔢 `extract` versus `findall` versus `extractall`

| Method | Returns | Matches |
|---|---|---|
| `extract` | A **DataFrame**, one column per group | **First** match only |
| `findall` | A Series of **lists** | All matches |
| `extractall` | A DataFrame with a **MultiIndex** | All matches, as rows |

`extract` is the one you want most of the time, because a DataFrame of columns
is immediately usable while a column of lists is not.

**Worked example.** Parse `23DSC0145` into year, branch and number:

```python
rolls = pd.Series(["23DSC0145", "24STA0067", "23DSC0198"])

parts = rolls.str.extract(r"(?P<year>\d{2})(?P<branch>[A-Z]{3})(?P<number>\d{4})")
```

```
  year branch number
0   23    DSC   0145
1   24    STA   0067
2   23    DSC   0198
```

Named groups become column names directly. Note the values are **strings** —
`0145` keeps its leading zero, which is right for a roll number and wrong for
arithmetic. Convert explicitly with `.astype(int)` when you need a number.

### ⚠️ Three regex traps in Pandas

**`contains` may return NaN for missing values rather than False — and
whether it does depends on the column's dtype.**

```python
# Pandas 3's new default str dtype: NaN becomes False, masking works
s = pd.Series(["abc", None])            # dtype: str
s.str.contains("a")                     # [True, False], dtype bool
s[s.str.contains("a")]                  # fine

# object dtype -- still common with mixed or older data
o = pd.Series(["abc", None], dtype="object")
o.str.contains("a")                     # [True, None], dtype OBJECT
o[o.str.contains("a")]                  # ValueError: cannot mask with NA
o[o.str.contains("a", na=False)]        # correct
```

Verified on Pandas 3.0.5. **Pass `na=False` anyway**: it costs nothing, it is
correct under both dtypes, and you will not always know which dtype a column
arrived with.

**`replace` needs `regex=` stated.** In current Pandas the default is
`regex=False` — a literal replacement — so a pattern silently fails to match.
Say which you mean.

**Special characters must be escaped.** `s.str.replace(".", "")` with
`regex=True` deletes *every character*, because `.` matches anything. Use
`regex=False`, or `re.escape`.

## 4.3 Feature engineering

### 🎯 What it is

**Creating new columns that make the underlying pattern easier for a model to
see.** It is usually worth more than the choice of algorithm — Course 8's
material is largely about which model to pick, and in practice a well-chosen
feature beats a better model on the same features.

### From dates

```python
df["dob"] = pd.to_datetime(df.dob)

df["year"]      = df.dob.dt.year
df["month"]     = df.dob.dt.month
df["day"]       = df.dob.dt.day
df["dayofweek"] = df.dob.dt.dayofweek       # Monday = 0
df["dayname"]   = df.dob.dt.day_name()
df["quarter"]   = df.dob.dt.quarter
df["is_weekend"] = df.dob.dt.dayofweek >= 5
df["days_since"] = (pd.Timestamp("2026-08-26") - df.dob).dt.days
df["age"] = ((pd.Timestamp("2026-08-26") - df.dob).dt.days / 365.25).astype(int)
```

**A raw date is nearly useless to a model**; the *year*, the *day of week*, the
*age it implies* are what carry signal. This is the clearest example of why
feature engineering matters.

### From numbers

```python
df["total"]   = df.maths + df.stats
df["average"] = df[["maths", "stats"]].mean(axis=1)
df["diff"]    = df.maths - df.stats
df["ratio"]   = df.maths / df.stats.replace(0, np.nan)   # guard the zero
df["log_income"] = np.log1p(df.income)                   # log(1+x): safe at 0
df["marks_z"] = (df.marks - df.marks.mean()) / df.marks.std()
df["marks_pct"] = df.marks.rank(pct=True)
df["grade"] = pd.cut(df.marks, [0, 40, 60, 75, 100],
                     labels=["Fail", "Pass", "First", "Distinction"])
```

`np.log1p(x)` computes log(1 + x), which is defined at 0 — the standard way to
log-transform a count or an income that can legitimately be zero.

### From categories

```python
df["dept_size"] = df.groupby("dept").dept.transform("size")
df["dept_mean"] = df.groupby("dept").marks.transform("mean")
df["above_dept_mean"] = df.marks > df.dept_mean
df["is_topper"] = df.marks == df.groupby("dept").marks.transform("max")
```

**`transform` is the key tool** here: it returns one value per *original row*
rather than one per group, so the group statistic can be attached as a column
and compared against each row.

### ⚠️ Leakage, again

The rule from Course 8 §2.8 applies with full force:

- **Never build a feature from the target.** A `passed` column derived from
  `marks` makes predicting `marks` trivial and useless.
- **Never build a feature from information unavailable at prediction time.**
  "Total spend over the customer's lifetime" is not known on the day they sign
  up.
- **Fit any statistic on the training split only.** A z-score computed over the
  whole dataset encodes the test set's mean into the training features.

## 4.4 Dummy and indicator variables

### 🔢 One-hot encoding

```python
pd.get_dummies(df.dept)
pd.get_dummies(df, columns=["dept", "gender"])
pd.get_dummies(df.dept, prefix="dept")
pd.get_dummies(df.dept, drop_first=True)         # k − 1 columns
pd.get_dummies(df.dept, dummy_na=True)           # a column for NaN
pd.get_dummies(df.dept, dtype=int)               # 0/1 instead of True/False
```

```
   dept          dept_DS  dept_Stats
0    DS            True       False
1  Stats          False        True
2    DS            True       False
```

### ⚠️ The dummy variable trap

With *k* categories, *k* dummy columns are **perfectly collinear** — they sum
to 1 in every row, so any one is a linear function of the others. That makes
the design matrix singular, and a linear or logistic regression cannot solve
it (or solves it with wildly unstable coefficients).

**`drop_first=True` is the fix**, giving *k − 1* columns with one category
absorbed into the intercept as the reference level.

**Tree models do not care** and are usually better off with all *k*, since
dropping one hides that category from every split. So:

| Model | Use |
|---|---|
| Linear / logistic regression | `drop_first=True` |
| Decision tree, random forest, boosting | Keep all *k* |

### Other encodings

```python
# Ordinal — when the order is REAL
df["size_code"] = df["size"].map({"S": 1, "M": 2, "L": 3, "XL": 4})

# Binary from a condition
df["is_ds"] = (df.dept == "DS").astype(int)

# Multi-label: one row, several tags
df.skills.str.get_dummies(sep=",")

# Frequency encoding — replace a category by how often it occurs
df["dept_freq"] = df.dept.map(df.dept.value_counts(normalize=True))
```

**`str.get_dummies(sep=",")` is worth knowing**: it turns `"python,sql,r"` into
three indicator columns in one call, which is otherwise fiddly.

**Do not integer-encode an unordered category** — Course 8 §2.9's warning. It
tells every distance-based model that `M` is the average of `S` and `L`.

### 💡 High-cardinality categories

One-hot encoding a column with 5,000 distinct values produces 5,000 columns,
most of them almost entirely zero. Alternatives: keep the top *n* and bucket
the rest as `"Other"`; frequency-encode; or target-encode (replace each
category by the mean target for that category) — with the strong caveat that
target encoding **leaks** unless it is fitted inside a cross-validation fold.

## 4.5 Permutation and random sampling

```python
rng = np.random.default_rng(42)

df.sample(n=3, random_state=42)               # 3 random rows
df.sample(frac=0.2, random_state=42)          # 20% of the rows
df.sample(frac=1, random_state=42)            # SHUFFLE — all rows, new order
df.sample(n=5, replace=True, random_state=42) # bootstrap — with replacement
df.sample(n=3, weights="marks", random_state=42)   # probability by weight
df.sample(n=2, axis=1)                        # random COLUMNS

# Permutation of the index
order = rng.permutation(len(df))
df.iloc[order]
df.take(order)

# Shuffle and reset the index
shuffled = df.sample(frac=1, random_state=0).reset_index(drop=True)
```

### 🔢 Stratified sampling

Plain random sampling can miss a small class entirely. **Stratified** sampling
preserves the class proportions:

```python
# In Pandas 3 the grouping column is excluded from each group, so name the
# columns explicitly if you want 'dept' to survive into the result.
strat = (df.groupby("dept", group_keys=False)[df.columns.tolist()]
           .apply(lambda g: g.sample(frac=0.5, random_state=0)))

# or, with scikit-learn
from sklearn.model_selection import train_test_split
train, test = train_test_split(df, test_size=0.3, random_state=42,
                               stratify=df.dept)
```

**Use `stratify=` whenever the classes are imbalanced.** Without it, a 5%
minority class can be absent from a small test set entirely, and the accuracy
you measure means nothing.

### ⚠️ Always set `random_state`

```python
df.sample(n=3)                     # different every run
df.sample(n=3, random_state=42)    # reproducible
```

An unseeded split cannot be reproduced, so neither can your reported accuracy —
and a result nobody can reproduce is not a result. It is also how you get
"it worked yesterday": the split changed.

### 💡 Sampling and the bootstrap

`replace=True` is the bootstrap of Course 8 §4.9. Drawing *n* rows with
replacement from *n* rows leaves about **36.8%** of them unselected — the
(1 − 1/n)ⁿ → 1/e limit — and those become the out-of-bag test set. That is
where the `.632` in the .632 bootstrap comes from, and it is the mechanism
behind bagging and Random Forest.

---

## Practice problems

### Problem 1

A `students` DataFrame has a `full_name` column like `"  KUMARI, Asha  "` and a
`roll` column like `"23DSC0145"`. Produce clean `first`, `last`, `year`,
`branch` and `number` columns.

**Solution.**

```python
# Clean first -- strip, then fix the case
name = df.full_name.str.strip().str.title()

# "Kumari, Asha" -> surname, first name
parts = name.str.split(",", expand=True)
df["last"]  = parts[0].str.strip()
df["first"] = parts[1].str.strip()

# Parse the roll number with named capture groups
roll = df.roll.str.strip().str.upper().str.extract(
    r"(?P<year>\d{2})(?P<branch>[A-Z]{3})(?P<number>\d{4})")
df = df.join(roll)

# Only 'number' should become numeric, and only if you need arithmetic --
# as a string it keeps its leading zeros, which an identifier should.
df["number_int"] = df.number.astype(int)
df["admission_year"] = 2000 + df.year.astype(int)
```

**Three points earn the marks.** Strip **before** splitting, or the surname
carries leading spaces and every later match fails. Use **named groups** so the
columns arrive already labelled. And leave `year`, `branch` and `number` as
strings — an identifier is not a quantity, and converting `0145` to 145 loses
information you cannot recover.

Guard against rows that do not match: `extract` yields NaN for those, so
`df[roll.year.isna()]` shows you the malformed roll numbers rather than
silently dropping them.

### Problem 2

Explain the dummy variable trap and when `drop_first=True` should be used.

**Solution.**

```python
d = pd.get_dummies(pd.Series(["DS", "Stats", "Maths", "DS"]), dtype=int)
```
```
   DS  Maths  Stats
0   1      0      0
1   0      0      1
2   0      1      0
3   1      0      0
```

Every row sums to exactly 1, so `DS = 1 − Maths − Stats`. The three columns
are **perfectly collinear**: any one is an exact linear function of the others.

For a linear or logistic regression this makes the matrix **XᵀX singular**, so
it cannot be inverted. There is no unique solution — infinitely many coefficient
sets fit equally well — and in practice you get either an error or wildly
unstable coefficients that flip sign on tiny changes to the data.

```python
pd.get_dummies(s, drop_first=True, dtype=int)
```
```
   Maths  Stats
0      0      0        ← DS is now the REFERENCE level
1      0      1
2      1      0
3      0      0
```

With *k − 1* columns the reference category is absorbed into the intercept, and
each remaining coefficient reads as "the effect relative to DS" — which is both
solvable and interpretable.

**When to use it:**

| Model | drop_first | Why |
|---|---|---|
| Linear / logistic regression | **Yes** | Singularity |
| Regularised regression (ridge, lasso) | Optional | The penalty resolves the collinearity |
| Decision tree, forest, boosting | **No** | No matrix inversion, and dropping a level hides it from every split |
| k-NN, K-Means | **No** | Dropping distorts the distances |

### Problem 3

Given a `marks` DataFrame with `dept`, add: each student's rank within their
department, the departmental mean, whether they beat it, and a stratified 50%
sample.

**Solution.**

```python
# 1. Rank within department -- 1 = highest
df["dept_rank"] = df.groupby("dept").marks.rank(ascending=False, method="min")

# 2. Departmental mean, attached to EVERY row -- this is what transform is for
df["dept_mean"] = df.groupby("dept").marks.transform("mean")

# 3. Comparison
df["above_dept_mean"] = df.marks > df.dept_mean

# 4. Departmental topper
df["is_topper"] = df.dept_rank == 1

# 5. Stratified 50% sample.
# NOTE: in Pandas 3, groupby().apply() EXCLUDES the grouping column from each
# group, so select the columns explicitly to keep 'dept' in the result.
sample = (df.groupby("dept", group_keys=False)[df.columns.tolist()]
            .apply(lambda g: g.sample(frac=0.5, random_state=42)))

# scikit-learn is clearer for a train/test split:
from sklearn.model_selection import train_test_split
train, test = train_test_split(df, test_size=0.5, random_state=42,
                               stratify=df.dept)
```

**Why `transform` and not `agg`.** `df.groupby("dept").marks.mean()` returns
one row per department — two values — which cannot be assigned to a
five-row DataFrame. `transform("mean")` returns one value **per original row**,
broadcasting the group's mean back to each of its members, so it aligns for
assignment and comparison.

**Why `method="min"` for the rank.** It gives competition ranking: two students
tied at the top both get rank 1, and the next gets 3. `method="average"` would
give them 1.5 each, so `dept_rank == 1` would find no topper at all — a silent
bug in step 4.

**Why stratify.** A plain `df.sample(frac=0.5)` could draw entirely from one
department, leaving the other unrepresented. Grouping first guarantees half of
each. `group_keys=False` keeps the original index rather than adding the
department as an outer level, and the explicit column list is needed because
**Pandas 3 excludes the grouping column from the groups it passes to `apply`** —
without it, `dept` is missing from the result.

---

## Exam questions from this unit

**Two marks**

1. Why use `.str.lower()` rather than `.apply(str.lower)`?
2. What does `expand=True` do in `str.split`?
3. Distinguish `str.extract` from `str.findall`.
4. Why pass `na=False` to `str.contains`?
5. What is one-hot encoding?
6. What is the dummy variable trap?
7. When should `drop_first=True` be used, and when not?
8. Why must `random_state` be set?
9. What is stratified sampling, and when is it needed?
10. Distinguish `transform` from `agg` in a groupby.

**Five marks**

1. Explain the vectorized string methods with examples.
2. Explain regular expressions in Pandas with `extract`, `contains` and
   `replace`.
3. Explain feature engineering with examples from dates, numbers and
   categories.
4. Explain dummy variables and the dummy variable trap.
5. Explain permutation and random sampling, including stratification.
6. Explain data leakage in feature engineering.

**Ten marks**

1. Given a messy name and identifier column, write and explain a complete
   parsing pipeline using string methods and regular expressions.
2. Explain feature engineering exhaustively, with the encodings appropriate to
   each model type.
3. Explain sampling — simple, stratified, weighted and bootstrap — and why
   reproducibility matters.

## Mistakes that cost marks

- Using `.apply(str.lower)` and crashing on NaN
- Forgetting `expand=True` and getting a column of lists
- Using `str.contains` as a filter without `na=False`
- Forgetting `regex=True` on `str.replace`, so the pattern never matches
- Not escaping `.` in a regex and deleting every character
- Converting an identifier to an integer and losing its leading zeros
- Integer-encoding an unordered category
- One-hot encoding for a regression without `drop_first`
- Dropping a level for a tree model, hiding that category from every split
- Building a feature from the target — leakage
- Computing a z-score over the whole dataset before splitting
- Sampling without `random_state`
- Using an unstratified split on imbalanced classes
- Using `agg` where `transform` was needed, and getting a length mismatch
