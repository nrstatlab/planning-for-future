# Unit 1 — Basics of Python Programming

**Syllabus topics:** Introduction to Python, features of Python, programming
modes (interactive and script), identifiers, naming conventions, keywords,
built-in data types, literals (integer, float, complex, boolean, string),
variables, operators, expressions, assignment statements, input/output
statements, Python syntax (lines, comments, indentation), operators and
operands, classification of operators (arithmetic, relational, logical,
bitwise, assignment, augmented assignment, identity), expressions and
precedence rules.

---

## 1.1 Introduction and features

Python was created by **Guido van Rossum** and released in **1991**. The name
comes from *Monty Python's Flying Circus*, not the snake.

**Features — a standard five-mark question:**

1. **Simple and readable** — the syntax is close to English
2. **Interpreted** — no separate compilation step
3. **Dynamically typed** — a variable's type is fixed by its value, not declared
4. **Platform independent** — the same code runs on Windows, Linux and macOS
5. **Free and open source**
6. **Object oriented** — everything is an object
7. **Extensive standard library** — "batteries included"
8. **Extensible and embeddable** — integrates with C, C++ and Java
9. **Supports multiple paradigms** — procedural, object oriented, functional
10. **Automatic memory management** — garbage collection; no `malloc`/`free`

### Python vs C — a comparison worth knowing

| | C | Python |
|---|---|---|
| Type system | Static — declare every type | Dynamic — inferred from the value |
| Execution | Compiled | Interpreted |
| Memory | Manual (`malloc`/`free`) | Automatic (garbage collected) |
| Block structure | Braces `{}` | **Indentation** |
| Statement end | Semicolon required | Newline |
| Speed | Fast | Slower |
| Lines to do the same job | More | Fewer |

## 1.2 Programming modes

**Interactive mode** — the `>>>` prompt. Type a statement, see the result
immediately. Ideal for experimenting; nothing is saved.

```
>>> 2 + 3
5
>>> print("Hello")
Hello
```

**Script mode** — write a `.py` file and run it with `python3 program.py`.
Reusable, and how real programs are written.

One difference that catches people out: in interactive mode an expression's
value is displayed automatically; in script mode you must `print()` it.

## 1.3 Identifiers and naming conventions

**Rules** (enforced by the interpreter):

- Start with a letter or underscore — **never a digit**
- Then letters, digits and underscores only
- No spaces, no special characters
- **Case sensitive**: `total`, `Total` and `TOTAL` are three names
- **Keywords cannot be used**
- No length limit

**Conventions** (PEP 8 — not enforced, but expected):

| Kind | Convention | Example |
|---|---|---|
| Variable, function | `lower_snake_case` | `total_marks`, `find_average()` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_SIZE`, `PI` |
| Class | `PascalCase` | `Student`, `BankAccount` |
| Private (by convention) | leading underscore | `_internal` |
| Name-mangled | two leading underscores | `__private` |
| Dunder (special) | double underscore both ends | `__init__`, `__str__` |

### Keywords

Python 3 has **35** keywords:

```
False   None    True    and     as      assert  async   await
break   class   continue def    del     elif    else    except
finally for     from    global  if      import  in      is
lambda  nonlocal not     or      pass    raise   return  try
while   with    yield
```

Check at any time with `import keyword; print(keyword.kwlist)`.

## 1.4 Data types and literals

| Category | Types |
|---|---|
| Numeric | `int`, `float`, `complex` |
| Boolean | `bool` |
| Sequence | `str`, `list`, `tuple`, `range` |
| Set | `set`, `frozenset` |
| Mapping | `dict` |
| Binary | `bytes`, `bytearray`, `memoryview` |
| None | `NoneType` |

```python
count   = 42                 # int     -- unlimited size in Python 3
price   = 99.75              # float
z       = 3 + 4j             # complex -- z.real is 3.0, z.imag is 4.0
flag    = True               # bool
name    = "Ananya"           # str
nothing = None               # NoneType
```

**Integers have no size limit in Python 3.** `2 ** 1000` is computed exactly —
no overflow, unlike C. This is a genuinely notable difference and a good exam
point.

**`bool` is a subclass of `int`**: `True == 1` and `False == 0` are both true,
and `True + True` is `2`. Odd, but occasionally useful:
`sum(x > 50 for x in marks)` counts how many exceed 50.

### Number bases

```python
0b1010    # binary      -> 10
0o17      # octal       -> 15
0xFF      # hexadecimal -> 255
1_000_000 # underscores for readability -> 1000000
```

### Checking types

```python
type(42)              # <class 'int'>
isinstance(42, int)   # True -- preferred, because it honours inheritance
```

## 1.5 Variables

Python variables are **references to objects**, not boxes holding values.

```python
x = 10        # the name x now refers to an int object with value 10
x = "hello"   # x now refers to a str object -- perfectly legal
```

No declaration and no fixed type. This is **dynamic typing**.

### Multiple assignment

```python
a, b, c = 1, 2, 3        # unpacking
x = y = z = 0            # chained -- all three refer to the same object
a, b = b, a              # swap, with no temporary variable
```

That last one is worth remembering: Python swaps in one line where C needs
three.

### Mutable and immutable — the idea that explains everything

| Immutable (cannot be changed in place) | Mutable (can be) |
|---|---|
| `int`, `float`, `complex`, `bool` | `list` |
| `str` | `dict` |
| `tuple` | `set` |
| `frozenset` | `bytearray` |

```python
s = "hello"
s[0] = "H"              # TypeError -- strings are immutable
s = "H" + s[1:]         # build a new string instead

lst = [1, 2, 3]
lst[0] = 99             # fine -- lists are mutable
```

This distinction governs function argument behaviour, dictionary keys, default
arguments and copying. It is examined constantly. Learn it now.

## 1.6 Operators

### Arithmetic

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | Addition | `7 + 3` | `10` |
| `-` | Subtraction | `7 - 3` | `4` |
| `*` | Multiplication | `7 * 3` | `21` |
| `/` | **True division** | `7 / 3` | `2.3333` |
| `//` | **Floor division** | `7 // 3` | `2` |
| `%` | Modulus | `7 % 3` | `1` |
| `**` | Exponent | `7 ** 3` | `343` |

**`/` always returns a float**, even when it divides evenly: `6 / 3` is `2.0`,
not `2`. This differs from C, where `7/3` is `2`. In Python you must write
`7 // 3` for that.

Floor division rounds **towards negative infinity**, not towards zero:
`-7 // 2` is `-4`, not `-3`. Similarly `-7 % 2` is `1`, because Python's
modulus takes the sign of the divisor. C would give `-1`.

### Relational

`==`, `!=`, `<`, `>`, `<=`, `>=` — all return `True` or `False`.

**Chained comparison** is a Python feature C lacks:

```python
if 0 < x < 100:          # reads naturally, and means 0 < x and x < 100
```

### Logical

`and`, `or`, `not` — words, not `&&`, `||`, `!`.

They **short-circuit**: `and` stops at the first falsy operand, `or` at the
first truthy one. So `if x != 0 and 10 / x > 2` is safe — the division is never
attempted when `x` is 0.

They also return an **operand**, not necessarily a boolean:

```python
"a" and "b"      # 'b'  -- both truthy, so the last is returned
"" or "default"  # 'default'
```

**Falsy values:** `False`, `None`, `0`, `0.0`, `""`, `[]`, `()`, `{}`,
`set()`. Everything else is truthy.

### Bitwise

`&` AND · `|` OR · `^` XOR · `~` NOT · `<<` left shift · `>>` right shift

```python
12 & 5     # 1100 & 0101 = 0100 = 4
12 | 5     # 1101 = 13
12 ^ 5     # 1001 = 9
12 << 1    # 24  -- shifting left by 1 doubles
12 >> 1    # 6   -- shifting right by 1 halves
```

### Assignment and augmented assignment

`=` `+=` `-=` `*=` `/=` `//=` `%=` `**=` `&=` `|=` `^=` `>>=` `<<=`

`x += 5` is shorthand for `x = x + 5` — though for mutable objects the two are
not identical (`+=` on a list modifies in place; `= x +` builds a new one).

### Identity vs equality — a heavily examined distinction

| | Operator | Question it answers |
|---|---|---|
| Equality | `==` | Do these have the same **value**? |
| Identity | `is` | Are these the **same object** in memory? |

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

a == b     # True  -- same contents
a is b     # False -- two separate list objects
a is c     # True  -- c is another name for the same object
```

**Use `is` only with `None`, `True` and `False`.** `if x is None` is correct
style; `if x is 5` may work by accident (small integers are cached) and fail
for larger values.

### Membership

`in` and `not in`:

```python
"a" in "cat"           # True
3 in [1, 2, 3]         # True
"key" in {"key": 1}    # True -- checks KEYS, not values
```

### Precedence — highest to lowest

```
**
~  +x  -x                    (unary)
*  /  //  %
+  -
<<  >>
&
^
|
==  !=  >  >=  <  <=  is  is not  in  not in
not
and
or
```

Two consequences worth remembering: `**` binds tighter than unary minus, so
`-2 ** 2` is `-4`; and `**` is **right associative**, so `2 ** 3 ** 2` is
`2 ** 9` = `512`, not `64`.

## 1.7 Input and output

```python
name = input("Enter your name: ")          # ALWAYS returns a string
age  = int(input("Enter your age: "))      # convert explicitly
cgpa = float(input("Enter your CGPA: "))
```

**`input()` always returns a string.** Forgetting to convert is the single most
common beginner error: `input() + 1` raises `TypeError`, and
`if input() == 5` is never true because `"5" != 5`.

### Output formatting

```python
name, marks = "Ananya", 87.5

print(f"{name} scored {marks}")               # f-string -- modern, preferred
print("{} scored {}".format(name, marks))     # .format()
print("%s scored %.2f" % (name, marks))       # %-formatting -- C style

print(f"{marks:.2f}")     # 87.50    -- two decimals
print(f"{name:>10}")      # right-aligned in 10 columns
print(f"{name:<10}")      # left-aligned
print(f"{name:^10}")      # centred
```

`print()` parameters:

```python
print("a", "b", sep="-")      # a-b        -- separator between items
print("a", end="")            # no newline at the end
```

## 1.8 Syntax: lines, comments and indentation

### Indentation defines blocks

This is Python's most distinctive feature. Where C uses `{}`, Python uses
**indentation**, and it is not optional:

```python
if x > 0:
    print("positive")        # 4 spaces -- part of the if block
    print("still inside")
print("always runs")         # unindented -- outside the block
```

**Use 4 spaces per level.** Never mix tabs and spaces — Python 3 rejects it
with a `TabError`. Configure your editor to insert spaces when Tab is pressed.

### Comments

```python
# a single-line comment

"""
A triple-quoted string. Used as a docstring when it is the first statement
in a module, function or class; otherwise it is just an unused string that
happens to serve as a multi-line comment.
"""

def area(r):
    """Return the area of a circle of radius r."""   # a real docstring
    return 3.14159 * r ** 2

print(area.__doc__)      # docstrings are retrievable at runtime
```

### Statements and line continuation

One statement per line, no semicolon needed. To break a long line:

```python
total = (first_value +
         second_value +
         third_value)          # implicit continuation inside brackets

total = first_value + \
        second_value           # explicit continuation -- avoid if you can
```

Brackets are preferred; a stray space after a backslash breaks it silently.

---

## Exam questions from this unit

**Two marks**

1. List any five features of Python.
2. What is the difference between `/` and `//`?
3. Distinguish `==` and `is`.
4. What does `input()` return, and why does it matter?
5. Name any five Python keywords.

**Five marks**

1. Explain the classification of operators in Python with examples.
2. Explain mutable and immutable types with examples.
3. Explain the built-in data types of Python.
4. Explain operator precedence with examples, including `2 ** 3 ** 2`.

**Ten marks**

1. Explain the features of Python and compare it with C.
2. Explain all operator categories in Python with examples and a precedence table.

## Mistakes that cost marks

- Forgetting `int()` around `input()`
- Expecting `/` to return an integer
- Mixing tabs and spaces for indentation
- Using `&&`, `||`, `!` instead of `and`, `or`, `not`
- Using `is` to compare values instead of `==`
- Forgetting the colon `:` after `if`, `for`, `while`, `def`, `class`
- Thinking `-2 ** 2` is `4` (it is `-4`)
