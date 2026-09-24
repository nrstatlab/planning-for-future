# Unit 3 — Sequences, Sets and Mapping Types

**Syllabus topics:** Strings — representation, indexing, slicing,
immutability, operators, traversal, accumulation, formatting and methods.
Lists — overview, indexing, slicing, methods, mutability, operations (add,
update, delete, search, copy, traverse), comprehension. Tuples — operations,
immutability, tuple assignment, arrays and operations. Sets — overview,
methods, mathematical operations, frozenset, comprehension. Dictionaries —
overview, methods, operations, traversal, comparison.

---

This unit is the heart of practical Python. Nearly everything you do in later
courses is manipulating these four types.

## 3.0 The four at a glance

| | List | Tuple | Set | Dictionary |
|---|---|---|---|---|
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` | `{1, 2, 3}` | `{"a": 1}` |
| Ordered | Yes | Yes | **No** | Yes (3.7+) |
| Mutable | **Yes** | No | Yes | Yes |
| Duplicates | Yes | Yes | **No** | Keys no, values yes |
| Indexed | Yes | Yes | **No** | By key |
| Lookup speed | O(n) | O(n) | **O(1)** | **O(1)** |

**Choosing between them** — the question examiners actually want answered:

- **List** — an ordered collection you will change
- **Tuple** — an ordered collection that must not change (and can be a dict key)
- **Set** — membership testing and removing duplicates
- **Dictionary** — looking values up by a key

## 3.1 Strings

Strings are **immutable sequences of characters**.

### Indexing and slicing

```python
s = "DataScience"
#    0123456789...
#   -11 ... -1  (negative indices count from the end)

s[0]        # 'D'
s[-1]       # 'e'
s[0:4]      # 'Data'      -- start included, stop EXCLUDED
s[4:]       # 'Science'
s[:4]       # 'Data'
s[::2]      # 'Dtsine'    -- every second character
s[::-1]     # 'ecneicSataD' -- reversed; the idiomatic way to reverse a string
```

`s[start:stop:step]`. Out-of-range slices do **not** raise — `s[0:999]` simply
returns the whole string. Out-of-range *indexing* does: `s[999]` raises
`IndexError`.

### Immutability

```python
s = "hello"
s[0] = "H"          # TypeError: 'str' object does not support item assignment
s = "H" + s[1:]     # correct: build a new string
```

Every "modification" creates a new string. Building a long string by repeated
`+=` in a loop is therefore O(n²); use `"".join(list_of_pieces)` instead.

### Operators

```python
"Data" + "Science"     # concatenation -> 'DataScience'
"ab" * 3               # repetition    -> 'ababab'
"a" in "cat"           # membership    -> True
len("hello")           # 5
```

### Common methods

| Method | Purpose |
|---|---|
| `upper()`, `lower()`, `title()`, `capitalize()`, `swapcase()` | case |
| `strip()`, `lstrip()`, `rstrip()` | remove whitespace |
| `split(sep)` | string → list |
| `join(iterable)` | list → string |
| `replace(old, new)` | substitution |
| `find(sub)` / `index(sub)` | position — `find` gives −1, `index` raises |
| `count(sub)` | occurrences |
| `startswith()` / `endswith()` | prefix/suffix test |
| `isalpha()`, `isdigit()`, `isalnum()`, `isspace()` | classification |

**All string methods return a new string.** `s.upper()` does not change `s`;
you must write `s = s.upper()`.

```python
"a,b,c".split(",")        # ['a', 'b', 'c']
"-".join(["a", "b"])      # 'a-b'   -- note: separator.join(list)
```

### Formatting

```python
name, marks = "Ananya", 87.5
f"{name} scored {marks:.1f}"     # f-string, preferred
"{} scored {}".format(name, marks)
"%s scored %.1f" % (name, marks)
```

## 3.2 Lists

The workhorse: ordered, mutable, allows duplicates, holds mixed types.

```python
marks = [85, 72, 90, 64]
mixed = [1, "two", 3.0, [4, 5]]        # nesting is fine
```

### Methods

| Method | Effect | Returns |
|---|---|---|
| `append(x)` | Add x at the end | `None` |
| `insert(i, x)` | Insert x at index i | `None` |
| `extend(iterable)` | Add all items | `None` |
| `remove(x)` | Delete the **first** x | `None` — `ValueError` if absent |
| `pop([i])` | Remove and **return** item at i (default last) | the item |
| `clear()` | Empty the list | `None` |
| `index(x)` | Position of the first x | int — `ValueError` if absent |
| `count(x)` | How many x | int |
| `sort()` | Sort **in place** | `None` |
| `reverse()` | Reverse **in place** | `None` |
| `copy()` | Shallow copy | a new list |

**In-place methods return `None`.** This bites everyone once:

```python
marks = marks.sort()        # WRONG -- marks is now None
marks.sort()                # right -- sorts in place
marks = sorted(marks)       # right -- sorted() returns a new list
```

The rule: `list.sort()` and `list.reverse()` mutate and return `None`;
`sorted()` and `reversed()` leave the original alone and return something new.

### `append` vs `extend`

```python
a = [1, 2]
a.append([3, 4])      # [1, 2, [3, 4]]   -- one new element, a list
b = [1, 2]
b.extend([3, 4])      # [1, 2, 3, 4]     -- each item added separately
```

### Copying — shallow vs deep

```python
a = [1, 2, 3]
b = a                 # NOT a copy -- b is another name for the same list
b[0] = 99             # a is now [99, 2, 3] too

c = a.copy()          # shallow copy: a new list, same element objects
c = a[:]              # same thing
c = list(a)           # same thing

import copy
d = copy.deepcopy(a)  # deep copy: nested objects copied too
```

The difference shows only with nesting:

```python
a = [[1, 2], [3, 4]]
shallow = a.copy()
shallow[0][0] = 99       # a is ALSO changed -- the inner lists are shared
deep = copy.deepcopy(a)
deep[0][0] = 99          # a is unaffected
```

### List comprehension

```python
squares  = [x ** 2 for x in range(10)]
evens    = [x for x in range(20) if x % 2 == 0]
labels   = ["even" if x % 2 == 0 else "odd" for x in range(5)]
matrix   = [[r * c for c in range(3)] for r in range(3)]     # nested
flattened = [item for row in matrix for item in row]         # order matters
```

The general form: `[expression for item in iterable if condition]`. With
`if-else`, the conditional expression comes **before** the `for`; with a plain
filter, the `if` comes **after**. Getting that backwards is a `SyntaxError`.

Comprehensions are faster than the equivalent `for` loop with `append`, and
examiners expect you to know them.

## 3.3 Tuples

Ordered, **immutable**, allows duplicates.

```python
point = (3, 4)
single = (5,)          # the TRAILING COMMA is what makes it a tuple
not_tuple = (5)        # this is just the int 5
packed = 1, 2, 3       # brackets are optional
```

### Packing and unpacking

```python
student = "Ananya", 24001, 8.75      # packing
name, roll, cgpa = student            # unpacking
first, *rest = (1, 2, 3, 4)           # first=1, rest=[2,3,4]
a, b = b, a                           # swap
```

### Methods

Only two — `count()` and `index()`. Everything that would modify a list is
absent, because tuples cannot be modified.

### Why use a tuple?

1. **Immutability as a guarantee** — the data cannot be changed by accident
2. **Hashable, so usable as a dictionary key** — a list cannot be
3. **Slightly faster and smaller** than a list
4. **Signals intent** — a fixed record, not a growable collection

```python
locations = {(17.68, 83.21): "Visakhapatnam"}    # tuple key: fine
locations = {[17.68, 83.21]: "Visakhapatnam"}    # TypeError: unhashable
```

**A subtlety:** a tuple is immutable, but if it *contains* a mutable object,
that object can still change:

```python
t = ([1, 2], 3)
t[0].append(9)      # allowed -- the tuple still holds the same list object
t[0] = [9]          # TypeError -- reassigning the element is not
```

## 3.4 Sets

Unordered, mutable, **no duplicates**.

```python
s = {1, 2, 3}
s = set([1, 1, 2, 2, 3])       # {1, 2, 3} -- duplicates dropped
empty = set()                  # {} would be an empty DICTIONARY
```

### Mathematical operations

| Operation | Operator | Method |
|---|---|---|
| Union | `A \| B` | `A.union(B)` |
| Intersection | `A & B` | `A.intersection(B)` |
| Difference | `A - B` | `A.difference(B)` |
| Symmetric difference | `A ^ B` | `A.symmetric_difference(B)` |
| Subset | `A <= B` | `A.issubset(B)` |
| Superset | `A >= B` | `A.issuperset(B)` |
| Disjoint | — | `A.isdisjoint(B)` |

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
A | B      # {1, 2, 3, 4, 5, 6}
A & B      # {3, 4}
A - B      # {1, 2}
A ^ B      # {1, 2, 5, 6}
```

### Methods

`add(x)`, `update(iterable)`, `remove(x)` (raises `KeyError` if absent),
`discard(x)` (silent if absent), `pop()` (removes an arbitrary element),
`clear()`.

**`remove` vs `discard`** is a two-mark question: `remove` raises on a missing
element, `discard` does not.

### `frozenset`

The immutable set. Being hashable, it can be a dictionary key or an element of
another set.

```python
fs = frozenset([1, 2, 3])
fs.add(4)          # AttributeError -- no such method
```

### Why sets are fast

Membership testing is **O(1)** for a set and **O(n)** for a list, because sets
are hash tables. For 10,000 lookups in a large collection that difference is
the whole runtime.

```python
if item in big_list:     # slow  -- scans every element
if item in big_set:      # fast  -- one hash computation
```

## 3.5 Dictionaries

**Key–value pairs.** Keys must be unique and **hashable** (so immutable);
values can be anything.

```python
student = {"name": "Ananya", "roll": 24001, "cgpa": 8.75}
```

Since Python 3.7 dictionaries preserve **insertion order** — worth stating in
an exam, since older textbooks say they are unordered.

### Access

```python
student["name"]              # 'Ananya'
student["email"]             # KeyError

student.get("email")         # None -- no exception
student.get("email", "n/a")  # 'n/a' -- with a default
```

Prefer `.get()` when a key may be missing.

### Methods

| Method | Returns |
|---|---|
| `keys()` | a view of the keys |
| `values()` | a view of the values |
| `items()` | a view of (key, value) pairs |
| `get(k, default)` | the value, or the default |
| `pop(k)` | the value, removing the pair |
| `popitem()` | the last (key, value) pair, removing it |
| `update(other)` | merges another dict in |
| `setdefault(k, v)` | the value; inserts it first if absent |
| `clear()` | `None` |
| `copy()` | a shallow copy |

### Traversal

```python
for key in student:                     # iterating gives KEYS
    print(key, student[key])

for key, value in student.items():      # preferred
    print(key, value)

for value in student.values():
    print(value)
```

### Dictionary comprehension

```python
squares = {x: x ** 2 for x in range(5)}
passed  = {k: v for k, v in marks.items() if v >= 40}
inverted = {v: k for k, v in original.items()}
```

### Nested dictionaries

```python
students = {
    24001: {"name": "Ananya", "marks": {"maths": 85, "python": 92}},
    24002: {"name": "Bhavana", "marks": {"maths": 72, "python": 65}},
}
students[24001]["marks"]["maths"]        # 85
```

This is the shape of JSON, which you will meet in Sem IV's Document Oriented
Database course.

---

## Exam questions from this unit

**Two marks**

1. Difference between a list and a tuple.
2. How do you create an empty set, and why not `{}`?
3. What does `remove()` do that `discard()` does not?
4. Why can a tuple be a dictionary key but a list cannot?
5. What does `list.sort()` return?

**Five marks**

1. Explain string slicing with examples, including negative indices.
2. Explain any five list methods with examples.
3. Explain the set operations with a Venn-diagram style example.
4. Explain shallow copy and deep copy with an example that distinguishes them.
5. Explain list, set and dictionary comprehensions with examples.

**Ten marks**

1. Compare lists, tuples, sets and dictionaries in detail, with syntax,
   properties, methods and when to use each.
2. Explain dictionaries fully — creation, access, methods, traversal, nesting
   and comprehension.

## Mistakes that cost marks

- Writing `marks = marks.sort()` and getting `None`
- Forgetting the trailing comma in a one-element tuple
- Using `{}` for an empty set (it is an empty dict)
- Trying to index a set — sets are unordered and have no indices
- Modifying a list while iterating over it (skips elements)
- Assuming `b = a` copies a list
- Using a list as a dictionary key
- Confusing `append` with `extend`
