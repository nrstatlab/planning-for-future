# Unit 2 — Control Flow, Functions and Modules

**Syllabus topics:** Control flow — `if`, `if-else`, `if-elif-else`.
Iterative statements — `while`, `for`, nested loops. Loop control statements —
`break`, `continue`, `pass`; `else` with loops. Need for functions, defining and
invoking user-defined functions, `return`, function input/output cases, scope of
variables (local, global, nested functions), function arguments (required,
positional, default, variable-length), `main()` function, documentation strings,
recursive functions, anonymous functions (lambda), library functions. Modules —
`import`, `from..import`, creating and using modules, namespaces.

---

## 2.1 Conditional statements

```python
if condition:
    ...
elif another_condition:
    ...
else:
    ...
```

Note: **`elif`**, not `else if`. The colon is mandatory. There is no `switch`
statement in Python before 3.10 (which added `match`, outside this syllabus) —
use a dictionary or an `if-elif` ladder instead.

### The conditional expression (ternary)

```python
status = "Pass" if marks >= 40 else "Fail"
```

Equivalent to C's `marks >= 40 ? "Pass" : "Fail"`, but ordered
value-first.

### Dictionary dispatch — the Pythonic replacement for `switch`

```python
operations = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
}
result = operations["add"](5, 3)          # 8
result = operations.get(op, lambda a, b: None)(5, 3)   # safe default
```

## 2.2 Loops

### `for` — iterates over a sequence

Python's `for` is a **for-each** loop. It does not count; it walks a collection.

```python
for item in [10, 20, 30]:
    print(item)

for ch in "hello":
    print(ch)

for i in range(5):            # 0 1 2 3 4
    print(i)

for i in range(1, 6):         # 1 2 3 4 5
    print(i)

for i in range(10, 0, -2):    # 10 8 6 4 2
    print(i)
```

`range(start, stop, step)` — **`stop` is excluded**. `range(1, 5)` gives
1, 2, 3, 4.

### Useful iteration helpers

```python
for index, value in enumerate(["a", "b", "c"]):
    print(index, value)       # 0 a / 1 b / 2 c

for name, mark in zip(names, marks):
    print(name, mark)         # pairs them up; stops at the shorter list

for key, value in student.items():
    print(key, value)
```

`enumerate` is the right answer when you need both the index and the value.
Writing `for i in range(len(lst))` and then `lst[i]` works but is un-Pythonic
and examiners notice.

### `while`

```python
count = 0
while count < 5:
    print(count)
    count += 1                # forget this and it never ends
```

### `else` with a loop — unique to Python

The `else` block runs **only if the loop finished without hitting `break`**.

```python
for n in range(2, number):
    if number % n == 0:
        print(f"{number} is not prime")
        break
else:
    print(f"{number} is prime")      # runs only when no divisor was found
```

Read `for...else` as "for...**nothing found**". It removes the need for a
`found = False` flag, and it is examined precisely because it surprises people.

### `break`, `continue`, `pass`

| Statement | Effect |
|---|---|
| `break` | Leave the innermost loop immediately |
| `continue` | Skip to the next iteration |
| `pass` | Do nothing — a placeholder where a statement is syntactically required |

```python
def not_written_yet():
    pass                     # valid; an empty body would be a SyntaxError
```

`pass` is *not* a loop control statement in the way the other two are — it is a
null statement. The syllabus groups them together, so know all three.

### Nested loops

A loop inside another loop. The **inner loop runs completely for every single
iteration of the outer loop**, so the body executes *outer × inner* times.

```python
for i in range(1, 4):            # outer: 3 iterations
    for j in range(1, 4):        # inner: 3 iterations, restarted each time
        print(i * j, end=" ")
    print()                      # after the inner loop finishes
```
```
1 2 3
2 4 6
3 6 9
```

The classic exam question is a pattern:

```python
n = 5
for i in range(1, n + 1):
    print("*" * i)               # 1 star, then 2, then 3...
```
```
*
**
***
****
*****
```

And the multiplication table, which uses the inner loop's variable in the
formatting:

```python
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i * j:4}", end="")
    print()
```

### ⚠️ `break` leaves only the *innermost* loop

```python
for i in range(3):
    for j in range(3):
        if j == 1:
            break                # leaves the j loop ONLY
        print(i, j)
```

This prints `0 0`, `1 0`, `2 0` — the outer loop keeps going. There is no
`break 2` in Python. To leave both, use a flag, a `for…else`, or put the
loops in a function and `return`:

```python
def find(grid, target):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == target:
                return r, c      # returns out of BOTH loops at once
    return None
```

Returning from a function is the cleanest of the three, and it is what
experienced Python programmers reach for.

### 💡 Nested loops and complexity

Two nested loops over *n* items each do *n²* work. At n = 1,000 that is a
million operations — fine. At n = 100,000 it is ten billion, and your program
appears to hang. Course 3 Unit 5 returns to this; for now, notice when you
have written a nested loop over a large collection, because a `set` or a
`dict` often replaces the inner one with a single lookup:

```python
# O(n²) — for every a, scan all of b
common = [x for x in a if x in b]           # b is a list: slow

# O(n) — membership in a set is one hash lookup
b_set = set(b)
common = [x for x in a if x in b_set]
```

## 2.3 Functions

```python
def greet(name):
    """Return a greeting for name."""     # docstring
    return f"Hello, {name}!"

message = greet("Ananya")
```

A function with no `return` returns **`None`**.

### The four argument types

```python
def student(name, course, year=1, *subjects, **details):
    ...
```

| Type | Syntax | Notes |
|---|---|---|
| **Required (positional)** | `name` | Matched by position; must be supplied |
| **Default** | `year=1` | Used when the caller omits it |
| **Keyword** | `student(course="DS", name="A")` | Matched by name; order stops mattering |
| **Variable-length positional** | `*subjects` | Collected into a **tuple** |
| **Variable-length keyword** | `**details` | Collected into a **dict** |

The order is fixed: **required, default, `*args`, `**kwargs`**. Any other order
is a `SyntaxError`.

```python
def total(*numbers):
    return sum(numbers)          # numbers is a tuple

total(1, 2, 3)                   # 6

def profile(**details):
    return details               # a dict

profile(name="A", roll=1)        # {'name': 'A', 'roll': 1}
```

### The mutable default argument trap

```python
def add_item(item, basket=[]):       # DANGEROUS
    basket.append(item)
    return basket

add_item("apple")     # ['apple']
add_item("banana")    # ['apple', 'banana']  <- the SAME list persists!
```

The default is evaluated **once**, when the function is defined, not on each
call. The fix:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

A favourite interview and exam question.

### Scope — the LEGB rule

Python looks names up in this order:

1. **L**ocal — inside the current function
2. **E**nclosing — inside any enclosing function
3. **G**lobal — at module level
4. **B**uilt-in — `print`, `len`, `range`, …

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)         # local
    inner()
    print(x)             # enclosing

outer()
print(x)                 # global
```

### `global` and `nonlocal`

```python
count = 0

def increment():
    global count         # without this, count += 1 raises UnboundLocalError
    count += 1

def outer():
    x = 10
    def inner():
        nonlocal x       # rebinds the ENCLOSING x, not a global one
        x = 20
    inner()
    return x             # 20
```

**Why `UnboundLocalError`?** Assigning to a name anywhere in a function makes
that name local for the whole function — including *before* the assignment. So
`count += 1` tries to read a local `count` that does not yet exist. `global`
says "no, I mean the module-level one".

### Recursion

```python
def factorial(n):
    if n in (0, 1):              # base case
        return 1
    return n * factorial(n - 1)  # recursive case
```

Python's default recursion limit is **1000** — `sys.setrecursionlimit()` can
raise it, but deep recursion is a sign that a loop would be better. Python has
no tail-call optimisation.

### Lambda — anonymous functions

```python
square = lambda x: x ** 2            # equivalent to def square(x): return x**2

sorted(students, key=lambda s: s["marks"])
list(filter(lambda x: x % 2 == 0, numbers))
list(map(lambda x: x * 2, numbers))
```

**Restrictions:** a lambda holds a **single expression** — no statements, no
assignments, no loops, no `return` keyword (the expression's value is returned
implicitly). Use it for short throwaway functions, mainly as a `key=` argument.

### `main()` and `__name__`

```python
def main():
    print("Running the program")

if __name__ == "__main__":
    main()
```

When a file is run directly, `__name__` is `"__main__"`. When it is *imported*,
`__name__` is the module's name. The guard therefore means: **run this only if
the file is executed directly, not when it is imported**. Without it, importing
your module would execute its test code.

## 2.4 Modules

A module is simply a `.py` file.

```python
import math                    # whole module
math.sqrt(16)

import math as m               # with an alias
m.sqrt(16)

from math import sqrt, pi      # specific names
sqrt(16)

from math import *             # everything -- AVOID: pollutes the namespace
```

`from module import *` is discouraged because it can silently overwrite names
you already have.

### Creating your own module

```python
# mymath.py
PI = 3.14159

def area(r):
    return PI * r ** 2
```

```python
# main.py
import mymath
print(mymath.area(5))
```

### Namespaces

A namespace maps names to objects. Three levels:

- **Built-in** — created when the interpreter starts, holds `print`, `len`, …
- **Global** — one per module
- **Local** — one per function call

`dir(module)` lists a module's names; `globals()` and `locals()` return the
current namespaces as dictionaries.

### Standard library modules worth knowing

| Module | For |
|---|---|
| `math` | `sqrt`, `pow`, `ceil`, `floor`, `pi`, `factorial` |
| `random` | `random()`, `randint()`, `choice()`, `shuffle()`, `seed()` |
| `datetime` | dates and times |
| `os`, `sys` | operating system and interpreter |
| `statistics` | `mean`, `median`, `mode`, `stdev`, `variance` |
| `csv`, `json` | file formats |

`statistics` is genuinely useful for Course 4 — see
`labs/course-4-stats/python/`, where it
is used to cross-check hand-computed answers.

---

## Exam questions from this unit

**Two marks**

1. What is the difference between `break` and `continue`?
2. What does `pass` do?
3. When does a loop's `else` block execute?
4. What is a lambda function? State two restrictions.
5. What is the purpose of `if __name__ == "__main__":`?

**Five marks**

1. Explain the four types of function arguments with examples.
2. Explain the LEGB rule with an example.
3. Explain `global` and `nonlocal` with examples.
4. Explain `for...else` with a prime-checking example.

**Ten marks**

1. Explain functions in Python — definition, calling, arguments, return values,
   scope and recursion — with examples.
2. Explain modules — creating, importing, the different import forms, and
   namespaces.

## Mistakes that cost marks

- Forgetting the colon after `if`, `for`, `while`, `def`
- Using `else if` instead of `elif`
- Expecting `range(1, 5)` to include 5
- Using a mutable default argument
- Forgetting `global` and hitting `UnboundLocalError`
- Putting `*args` before a required parameter
- Trying to write a statement inside a lambda
