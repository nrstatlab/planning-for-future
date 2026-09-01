# Unit 1 — NumPy Essentials

**Syllabus topics:** NumPy ndarray — a multidimensional array object,
creating ndarrays, data types for ndarrays, arithmetic with arrays, basic
indexing and slicing, boolean indexing, fancy indexing, transposing arrays,
swapping axes, universal functions — element-wise operations, basic
mathematical and statistical functions, random number generation (basic use).

---

## 1.1 The ndarray

### 🎯 The big idea

A Python list holds **pointers to objects scattered across memory**, each with
its own type tag. A NumPy array holds **raw values in one contiguous block**,
all of the same type. That single difference buys everything else: speed,
element-wise arithmetic, and multidimensional indexing.

```
Python list [1, 2, 3]           NumPy array([1, 2, 3])
┌───┬───┬───┐                   ┌────┬────┬────┐
│ ● │ ● │ ● │  pointers          │  1 │  2 │  3 │  raw int64 values,
└─┬─┴─┬─┴─┬─┘                   └────┴────┴────┘  contiguous
  ▼   ▼   ▼
 int int int   ← each a full PyObject with a type tag and refcount
```

| | Python list | NumPy ndarray |
|---|---|---|
| Element types | **Mixed** | **One** (homogeneous) |
| Memory | Pointers, scattered | **Contiguous block** |
| Size | Growable | **Fixed at creation** |
| `a + b` | **Concatenates** | **Adds element-wise** |
| `a * 2` | **Repeats** | **Doubles every element** |
| Speed on 1M elements | ~100 ms | ~1 ms |
| Multidimensional | Nested lists, awkward | **Native** |

### ⚠️ `+` and `*` mean different things

```python
[1, 2, 3] + [4, 5, 6]              # [1, 2, 3, 4, 5, 6]     — concatenation
np.array([1,2,3]) + np.array([4,5,6])   # array([5, 7, 9])  — addition

[1, 2, 3] * 2                      # [1, 2, 3, 1, 2, 3]     — repetition
np.array([1, 2, 3]) * 2            # array([2, 4, 6])       — scaling
```

This is the first thing to get right and the most common source of confusion
for anyone arriving from Course 3.

### The attributes

```python
import numpy as np
a = np.array([[1, 2, 3], [4, 5, 6]])

a.ndim        # 2         — number of dimensions (the "rank")
a.shape       # (2, 3)    — rows, columns
a.size        # 6         — total elements = product of shape
a.dtype       # dtype('int64')
a.itemsize    # 8         — bytes per element
a.nbytes      # 48        — size * itemsize
a.T           # transposed
```

**`shape` is a tuple, always.** A 1-D array of 3 elements has shape `(3,)` —
note the trailing comma — not `(3, 1)` and not `3`. Confusing `(3,)` with
`(3, 1)` causes broadcasting surprises, so learn to read it.

## 1.2 Creating ndarrays

```python
np.array([1, 2, 3])                    # from a list
np.array([[1, 2], [3, 4]])             # 2-D from nested lists
np.array([1, 2, 3], dtype=np.float64)  # with an explicit dtype

np.zeros(5)                            # [0. 0. 0. 0. 0.]
np.zeros((2, 3))                       # a 2x3 block of zeros
np.ones((2, 3))
np.full((2, 3), 7)                     # filled with 7
np.empty((2, 3))                       # UNINITIALISED — garbage values
np.eye(3)                              # 3x3 identity
np.diag([1, 2, 3])                     # diagonal matrix

np.arange(10)                          # 0..9
np.arange(2, 10, 2)                    # [2 4 6 8]      — like range()
np.linspace(0, 1, 5)                   # [0. 0.25 0.5 0.75 1.]  — 5 points

np.zeros_like(a)                       # same shape and dtype as a
np.ones_like(a)

rng = np.random.default_rng(42)        # the MODERN random API
rng.random((2, 3))                     # uniform [0, 1)
```

### ⚠️ `arange` versus `linspace`

| | `arange(start, stop, step)` | `linspace(start, stop, num)` |
|---|---|---|
| Third argument | The **step size** | The **number of points** |
| Endpoint | **Excluded** | **Included** (by default) |
| Float behaviour | **Unreliable** | Exact count guaranteed |

```python
np.arange(0, 1, 0.1).size      # 10 — usually
np.arange(0, 0.3, 0.1)         # array([0. , 0.1, 0.2]) — but the count can
                               #   surprise you with other steps
np.linspace(0, 1, 11)          # exactly 11 points, 0 to 1 inclusive
```

**Never use `arange` with a float step** where the count matters. Floating-point
accumulation means the number of elements is not always what the arithmetic
suggests. `linspace` asks for a count and delivers it.

`np.empty` does **not** zero the memory — it hands you whatever was there. It
is faster, and it is a bug waiting to happen if you forget to fill it.

## 1.3 Data types

| dtype | Meaning |
|---|---|
| `int8`, `int16`, `int32`, `int64` | Signed integers |
| `uint8` … `uint64` | Unsigned |
| `float16`, `float32`, `float64` | Floating point (`float64` is the default) |
| `complex64`, `complex128` | Complex |
| `bool_` | Boolean |
| `object` | Python objects — **loses every NumPy advantage** |
| `<U10` | Unicode string, ≤ 10 characters |

```python
a = np.array([1, 2, 3])
a.dtype                        # int64
b = a.astype(np.float64)       # returns a NEW array — astype always COPIES
np.array([1, 2, 3.5])          # float64 — UPCAST to hold them all
np.array([1, 2, "3"])          # dtype '<U21' — everything became a STRING
```

### ⚠️ Two dtype traps

**Integer overflow wraps silently.**

```python
np.array([127], dtype=np.int8) + 1      # array([-128])  — no warning
```

**Integer division truncates in place.**

```python
a = np.array([1, 2, 3])
a[0] = 3.7            # a becomes [3, 2, 3] — the .7 is DISCARDED
a / 2                 # array([1.5, 1. , 1.5]) — true division gives float64
a // 2                # array([1, 1, 1])       — floor division stays int
```

Assigning a float into an int array truncates without complaint. If a column
should hold fractions, make it `float64` at creation.

## 1.4 Arithmetic and broadcasting

### 🎯 Vectorisation

Every arithmetic operator works **element-wise**, with no loop:

```python
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

a + b       # [11 22 33 44]
a * b       # [10 40 90 160]
b / a       # [10. 10. 10. 10.]
a ** 2      # [ 1  4  9 16]
a > 2       # [False False  True  True]   — a boolean array
-a          # [-1 -2 -3 -4]
```

### 🔢 Broadcasting

When shapes differ, NumPy **stretches** the smaller one — without copying —
according to two rules, applied from the **trailing** dimension backwards:

1. Dimensions are compatible if they are **equal**, or if **one of them is 1**.
2. A missing dimension is treated as 1.

```
(3, 4) + (4,)     ->  (4,) becomes (1, 4) -> stretched to (3, 4)   ✓
(3, 4) + (3, 1)   ->  the 1 stretches to 4                          ✓
(3, 4) + (3,)     ->  trailing 4 vs 3 — INCOMPATIBLE                ✗
```

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])            # (2, 3)

a + 10                               # scalar broadcasts to everything
a + np.array([10, 20, 30])           # (3,) -> each ROW
a + np.array([[10], [20]])           # (2, 1) -> each COLUMN
```

**Worked example.** Centre each column on its own mean:

```python
a - a.mean(axis=0)      # a.mean(axis=0) has shape (3,) -> broadcasts per column
```

Centre each **row** instead, and the naive version fails:

```python
a - a.mean(axis=1)               # ValueError: (2,3) and (2,) are incompatible
a - a.mean(axis=1, keepdims=True)  # (2,1) broadcasts correctly
a - a.mean(axis=1)[:, np.newaxis]  # the same thing, written differently
```

**`keepdims=True` is the fix**, and it is worth remembering because this exact
error appears constantly.

### ⚠️ `axis` is the axis that DISAPPEARS

This is the single most confusing thing in NumPy, and stating it this way makes
it stick:

```python
a.shape            # (2, 3)
a.sum(axis=0).shape   # (3,)  — axis 0 collapsed: a COLUMN total
a.sum(axis=1).shape   # (2,)  — axis 1 collapsed: a ROW total
a.sum()               # a scalar — everything collapsed
```

`axis=0` runs **down** the rows and gives one value **per column**. Students
read "axis=0 means rows" and then expect a row total. It means "collapse the
row axis", which produces column results.

## 1.5 Why vectorise

```python
import time
n = 1_000_000
lst = list(range(n))
arr = np.arange(n)

# Python loop
t = time.perf_counter()
out = [x * 2 for x in lst]
loop = time.perf_counter() - t

# NumPy
t = time.perf_counter()
out = arr * 2
vec = time.perf_counter() - t
```

Typical result: the NumPy version is **30 to 100 times faster**. (The lab
measures it on your machine and asserts the speed-up is real.)

**Three reasons:**

1. The loop runs in the C layer, not the Python interpreter.
2. No per-element `PyObject` boxing, type checks or reference counting.
3. Contiguous memory means the CPU cache and SIMD instructions work.

**The practical rule: if you are writing `for i in range(len(arr))`, there is
almost certainly an array operation that replaces it.**

## 1.6 Indexing and slicing

```python
a = np.arange(10)             # [0 1 2 3 4 5 6 7 8 9]

a[0]        # 0
a[-1]       # 9
a[2:5]      # [2 3 4]
a[:3]       # [0 1 2]
a[::2]      # [0 2 4 6 8]
a[::-1]     # reversed
```

Two dimensions use a **comma**, not chained brackets:

```python
m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

m[1, 2]        # 6           — row 1, column 2   ← preferred
m[1][2]        # 6           — works, but creates a temporary row first
m[1]           # [4 5 6]     — a whole row
m[:, 1]        # [2 5 8]     — a whole column
m[0:2, 1:3]    # [[2 3], [5 6]]
m[::2, ::2]    # [[1 3], [7 9]]
```

### ⚠️ Slices are VIEWS, not copies

**This is the most important difference from Python lists and it causes real
bugs.**

```python
lst = [1, 2, 3, 4, 5]
s = lst[1:4]
s[0] = 99
lst              # [1, 2, 3, 4, 5]  — unchanged; list slicing COPIES

a = np.array([1, 2, 3, 4, 5])
v = a[1:4]
v[0] = 99
a                # array([ 1, 99,  3,  4,  5])  — CHANGED!
```

A NumPy slice is a **window onto the same memory**. Writing through it writes
to the original.

```python
v.base is a            # True — a view knows its parent
a[1:4].copy()          # an explicit copy, when you need one
```

**Why views?** Because a slice of a gigabyte array would otherwise cost a
gigabyte. Views make slicing free. The cost is that you must know when you have
one — and `.copy()` is how you say you do not want one.

## 1.7 Boolean indexing

Select by **condition** rather than position.

```python
marks = np.array([72, 45, 91, 66, 38, 88])

marks > 50                  # array([True, False, True, True, False, True])
marks[marks > 50]           # array([72, 91, 66, 88])  — only the passes
marks[marks > 50].mean()    # 79.25

marks[(marks > 50) & (marks < 90)]     # 72, 66, 88
marks[(marks < 40) | (marks > 90)]     # 38, 91
marks[~(marks > 50)]                   # 45, 38

marks[marks < 50] = 50                 # assignment through a mask
np.where(marks >= 50, "Pass", "Fail")  # element-wise ternary
```

### ⚠️ Use `&`, `|`, `~` — never `and`, `or`, `not`

```python
marks[(marks > 50) and (marks < 90)]
# ValueError: The truth value of an array with more than one element is ambiguous
```

Python's `and` tries to reduce each operand to a **single** True or False, and
an array of six booleans has no single truth value. The bitwise operators
`&`, `|` and `~` work element-wise, which is what you want.

**And the parentheses are mandatory:** `&` binds *tighter* than `>`, so
`marks > 50 & marks < 90` parses as `marks > (50 & marks) < 90` and fails.

### Boolean helpers

```python
(marks > 50).sum()         # 4      — True counts as 1
(marks > 50).any()         # True
(marks > 50).all()         # False
(marks > 50).mean()        # 0.667  — the PROPORTION passing
np.count_nonzero(marks > 50)   # 4
np.where(marks > 50)       # (array([0, 2, 3, 5]),) — the INDICES
```

`(condition).sum()` for a count and `(condition).mean()` for a proportion are
idioms worth memorising.

## 1.8 Fancy indexing

Index with an **array of indices**.

```python
a = np.array([10, 20, 30, 40, 50])

a[[0, 2, 4]]             # array([10, 30, 50])
a[[4, 4, 0]]             # array([50, 50, 10]) — repeats allowed, any order
a[np.array([True, False, True, False, True])]   # boolean, not fancy

m = np.arange(12).reshape(3, 4)
m[[0, 2]]                # rows 0 and 2
m[[0, 1, 2], [1, 2, 3]]  # elements (0,1), (1,2), (2,3) -> array([1, 6, 11])
m[[0, 2]][:, [1, 3]]     # rows 0,2 then columns 1,3
m[np.ix_([0, 2], [1, 3])]  # the same submatrix, in one step
```

### ⚠️ Fancy indexing always COPIES

```python
a = np.array([1, 2, 3, 4, 5])
f = a[[0, 2]]
f[0] = 99
a            # unchanged — fancy indexing returns a COPY

s = a[0:2]
s[0] = 99
a            # CHANGED — basic slicing returns a VIEW
```

| Indexing | Returns |
|---|---|
| Basic slice `a[1:4]` | **View** |
| Boolean mask `a[a > 2]` | **Copy** |
| Fancy `a[[0, 2]]` | **Copy** |
| Single element `a[0]` | A scalar |

This table is a guaranteed exam question and a genuine source of bugs.

Note `m[[0,1,2], [1,2,3]]` gives **three elements**, not a 3×3 submatrix — the
two index arrays are paired position by position. Use `np.ix_` for the
submatrix.

## 1.9 Reshaping, transposing and swapping axes

```python
a = np.arange(12)

a.reshape(3, 4)          # 3 rows, 4 columns
a.reshape(3, -1)         # -1 means "work it out": also (3, 4)
a.reshape(-1, 1)         # a column vector, (12, 1)
a.ravel()                # flatten — a VIEW where possible
a.flatten()              # flatten — always a COPY

m = np.arange(6).reshape(2, 3)
m.T                      # transpose, (3, 2) — a VIEW
m.transpose()            # the same
np.swapaxes(m, 0, 1)     # the same for 2-D

t = np.arange(24).reshape(2, 3, 4)
t.transpose(1, 0, 2).shape    # (3, 2, 4) — reorder the axes explicitly
np.swapaxes(t, 0, 2).shape    # (4, 3, 2)
```

`reshape` requires the total size to match: 12 elements can become (3,4),
(4,3), (2,6), (2,2,3) — but never (5,3).

**`.T` is a view.** Transposing a large matrix costs nothing; NumPy just
changes how it walks the memory.

```python
np.concatenate([a, b])                  # along an existing axis
np.vstack([a, b])   /  np.hstack([a, b])
np.stack([a, b])                        # creates a NEW axis
np.split(a, 3)  /  np.hsplit(m, 2)
```

**`stack` versus `concatenate`** is a two-mark distinction: `concatenate` joins
along an existing axis and the result has the same `ndim`; `stack` adds a
dimension.

## 1.10 Universal functions

A **ufunc** applies element-wise to a whole array, in compiled code.

### Unary

```python
np.sqrt(a)   np.exp(a)   np.log(a)   np.log2(a)   np.log10(a)
np.abs(a)    np.sign(a)  np.square(a)
np.floor(a)  np.ceil(a)  np.round(a, 2)  np.trunc(a)
np.sin(a)    np.cos(a)   np.tan(a)       # RADIANS
np.isnan(a)  np.isinf(a) np.isfinite(a)
```

### Binary

```python
np.add(a, b)       np.subtract(a, b)   np.multiply(a, b)   np.divide(a, b)
np.power(a, b)     np.mod(a, b)
np.maximum(a, b)   np.minimum(a, b)    # ELEMENT-WISE pairwise
np.greater(a, b)   np.equal(a, b)
```

### ⚠️ `np.maximum` versus `np.max`

```python
np.maximum([1, 5, 3], [4, 2, 6])   # array([4, 5, 6]) — element-wise PAIRING
np.max([1, 5, 3])                  # 5               — the largest ONE value
```

`maximum` is a binary ufunc; `max` is a reduction. Confusing them is common.

`np.nan` propagates through everything: `np.array([1, np.nan, 3]).sum()` is
`nan`. Use `np.nansum`, `np.nanmean`, `np.nanmax` to skip them — or Pandas,
which skips them by default.

## 1.11 Mathematical and statistical functions

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

a.sum()          # 21
a.sum(axis=0)    # [5 7 9]     — per column
a.sum(axis=1)    # [6 15]      — per row
a.mean()         # 3.5
a.min()  a.max() # 1, 6
a.argmin()       # 0    — the INDEX of the minimum
a.argmax()       # 5
a.std()          # 1.7078  — POPULATION sd, ddof=0
a.var()          # 2.9167
a.cumsum()       # [ 1  3  6 10 15 21]
a.cumprod()
np.median(a)     # 3.5
np.percentile(a, [25, 50, 75])
np.corrcoef(x, y)
np.cov(x, y)
np.unique(a)     # sorted unique values
np.sort(a)       # returns a sorted COPY
a.sort()         # sorts IN PLACE
np.argsort(a)    # the indices that would sort it
```

### ⚠️ NumPy's `std` defaults to the POPULATION formula

This matters, and it connects directly to Course 4.

```python
x = np.array([2, 4, 4, 4, 5, 5, 7, 9])

x.std()            # 2.0    — divides by n      (ddof=0, POPULATION)
x.std(ddof=1)      # 2.1381 — divides by n − 1  (SAMPLE)
```

Course 4 taught that the **sample** standard deviation divides by *n − 1* to be
unbiased. **NumPy defaults to `ddof=0`, and Pandas defaults to `ddof=1`.** The
same data gives different answers depending on which library you used, which
is exactly the sort of silent discrepancy that ruins an analysis.

```python
np.std(x)                  # 2.0000   — population
pd.Series(x).std()         # 2.1381   — sample
```

**Always pass `ddof` explicitly** when it matters, and say which you mean.

## 1.12 Random number generation

```python
rng = np.random.default_rng(42)        # the modern Generator API

rng.random(5)                          # uniform [0, 1)
rng.integers(1, 7, size=10)            # dice: 1..6, high EXCLUSIVE
rng.normal(loc=50, scale=10, size=5)   # normal, mean 50, sd 10
rng.uniform(2, 8, size=5)
rng.binomial(n=10, p=0.5, size=5)
rng.poisson(lam=3, size=5)
rng.choice([1, 2, 3], size=5, replace=True)
rng.choice(arr, size=3, replace=False)     # a sample without replacement
rng.permutation(arr)                       # a shuffled COPY
rng.shuffle(arr)                           # shuffles IN PLACE
```

### 💡 Always seed, and use the modern API

```python
np.random.seed(42);  np.random.rand(3)     # LEGACY — global state
rng = np.random.default_rng(42); rng.random(3)   # MODERN — an object
```

The legacy functions share one hidden global generator, so any library that
draws a random number can change your results. `default_rng` gives you your own
generator, which is reproducible and thread-safe. Both appear in textbooks;
prefer the second.

**Seeding is not optional in analysis work.** An unseeded train/test split
cannot be reproduced, and a result nobody can reproduce is not a result.

**Worked example.** Simulate 10,000 rolls of two dice and estimate P(sum = 7).

```python
rng = np.random.default_rng(0)
rolls = rng.integers(1, 7, size=(10_000, 2))
totals = rolls.sum(axis=1)
p7 = (totals == 7).mean()          # ≈ 0.1667
```

The exact answer is 6/36 = 0.1667, and with 10,000 trials the simulation lands
within about 0.01 of it — a direct check of Course 4 Unit 1's classical
probability against the empirical definition.

---

## Practice problems

### Problem 1

Given `a = np.arange(1, 13).reshape(3, 4)`:

(a) `a.shape`, `a.ndim`, `a.size`
(b) `a[1, 2]`, `a[:, 1]`, `a[1:, 2:]`
(c) `a.sum(axis=0)` and `a.sum(axis=1)`
(d) All elements greater than 6
(e) The mean of each row, as a column vector

**Solution.**

```python
a = np.arange(1, 13).reshape(3, 4)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]]
```

| Expression | Result |
|---|---|
| `a.shape` | `(3, 4)` |
| `a.ndim` | `2` |
| `a.size` | `12` |
| `a[1, 2]` | `7` |
| `a[:, 1]` | `array([ 2, 6, 10])` |
| `a[1:, 2:]` | `array([[ 7, 8], [11, 12]])` |
| `a.sum(axis=0)` | `array([15, 18, 21, 24])` — per **column** |
| `a.sum(axis=1)` | `array([10, 26, 42])` — per **row** |
| `a[a > 6]` | `array([ 7, 8, 9, 10, 11, 12])` |
| `a.mean(axis=1, keepdims=True)` | `array([[2.5], [6.5], [10.5]])` |

Note (c): `axis=0` collapses the row axis, leaving one value per column.
And (e) needs `keepdims=True` to get shape `(3, 1)` rather than `(3,)`.

### Problem 2

Explain, with output, why these differ:

```python
a = np.array([1, 2, 3, 4, 5])
x = a[1:4];      x[0] = 99;   print(a)
b = np.array([1, 2, 3, 4, 5])
y = b[[1, 2, 3]]; y[0] = 99;  print(b)
```

**Solution.**

```
[ 1 99  3  4  5]      ← a was modified
[1 2 3 4 5]           ← b was NOT
```

**Basic slicing returns a view**: `x` shares memory with `a`, so writing to
`x[0]` writes to `a[1]`. **Fancy indexing returns a copy**: `y` is new memory,
so writing to it leaves `b` alone.

You can confirm it:

```python
a[1:4].base is a          # True  — it is a view
b[[1,2,3]].base is b      # False — it is a copy
```

The reason for the asymmetry is that a *slice* can always be expressed as a
start/stop/stride over the same memory, whereas an arbitrary list of indices
cannot — so NumPy has no choice but to copy.

To avoid the surprise, write `a[1:4].copy()` when you intend to modify.

### Problem 3

An array of 30 exam marks. Write NumPy expressions for: the pass count
(≥ 40), the pass percentage, the top 5 marks, the marks within one standard
deviation of the mean, and the marks z-scored — then a boolean grade array.

**Solution.**

```python
rng = np.random.default_rng(7)
marks = rng.integers(20, 100, size=30)

# (a) pass count and percentage
passes = (marks >= 40).sum()
pct    = (marks >= 40).mean() * 100

# (b) top 5, descending
top5 = np.sort(marks)[-5:][::-1]
# or, without sorting the whole array:
top5 = marks[np.argsort(marks)[-5:][::-1]]

# (c) within one sample standard deviation of the mean
mu, sd = marks.mean(), marks.std(ddof=1)
within = marks[(marks >= mu - sd) & (marks <= mu + sd)]

# (d) z-scores
z = (marks - mu) / sd

# (e) grades
grades = np.select(
    [marks >= 75, marks >= 60, marks >= 40],
    ["Distinction", "First", "Pass"],
    default="Fail")
```

Three points that earn the marks. **`ddof=1`** because these 30 marks are a
*sample* — Course 4's distinction, and NumPy's default would give the
population value. **`&` with parentheses**, not `and`. And **`np.select`**
rather than nested `np.where` calls, which is both clearer and what a marker
is looking for.

---

## Exam questions from this unit

**Two marks**

1. Distinguish a Python list from a NumPy ndarray.
2. What does `a + b` do for lists, and for arrays?
3. Distinguish `arange` from `linspace`.
4. What does `axis=0` mean?
5. Distinguish a view from a copy.
6. Why must you write `&` rather than `and` in a boolean mask?
7. Distinguish `np.max` from `np.maximum`.
8. What does `ddof` control, and what is NumPy's default?
9. What does `reshape(3, -1)` mean?
10. Distinguish `concatenate` from `stack`.

**Five marks**

1. Explain the ndarray and its attributes with examples.
2. Explain the ways of creating ndarrays.
3. Explain broadcasting with the rules and examples.
4. Explain basic slicing, boolean indexing and fancy indexing, and say which
   return views.
5. Explain universal functions with examples.
6. Explain the statistical functions and the `axis` parameter.
7. Explain random number generation and why seeding matters.

**Ten marks**

1. Explain NumPy indexing exhaustively — basic, boolean and fancy — with
   examples and the view/copy behaviour of each.
2. Write a program to analyse a marks array using NumPy, and explain every
   operation.
3. Explain broadcasting, vectorisation and why NumPy is faster than Python
   loops.

## Mistakes that cost marks

- Expecting `+` to concatenate arrays
- Reading `axis=0` as "operate on rows" rather than "collapse the row axis"
- Using `and` / `or` in a boolean mask
- Omitting the parentheses around each comparison in a compound mask
- Modifying a slice and being surprised the original changed
- Expecting fancy indexing to return a view
- Using `arange` with a float step where the count matters
- Assigning a float into an integer array and losing the fraction
- Forgetting `keepdims=True` when broadcasting a row statistic back
- Quoting `std()` as the sample standard deviation — it is the population one
- Using `np.random.seed` with the legacy API instead of `default_rng`
- Writing a Python loop where a vectorised operation exists
