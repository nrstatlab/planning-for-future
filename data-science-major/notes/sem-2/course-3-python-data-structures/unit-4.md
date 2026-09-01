# Unit 4 — File Handling, Exception Handling and Object-Oriented Programming

**Syllabus topics:** File handling — types, paths, basic operations
(open/close, read/write), CSV files, `os`/`pathlib`. Error and exception
handling — syntax errors, built-in exceptions, catching and handling exceptions
(`try-except`, `raise`), user-defined exceptions, assertions. OOP concepts —
classes, objects, attributes, methods, constructors and destructors.
Encapsulation — private and public members. Inheritance — single, multilevel,
multiple, method overriding.

---

> **This unit is overloaded.** It contains what would normally be three units:
> file handling, exception handling, and the whole of object-oriented
> programming. Compare Unit 1, which covers only literals and operators. See
> [`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D6**.
>
> **Plan for four weeks on this unit, not two.** The three parts below are
> effectively independent — study them in order, and do not start OOP until
> files and exceptions are solid.

---

# Part A — File Handling

## A.1 Opening and closing

```python
fh = open("data.txt", "r")
content = fh.read()
fh.close()                      # easy to forget, and skipped entirely if an
                                # exception is raised in between
```

**Always prefer the `with` statement:**

```python
with open("data.txt", "r") as fh:
    content = fh.read()
# the file is closed automatically here, even if an exception was raised
```

`with` is a context manager. It is the correct answer to any exam question
about safe file handling.

## A.2 File modes

| Mode | Meaning | If missing | If present |
|---|---|---|---|
| `"r"` | Read (default) | `FileNotFoundError` | Opens at the start |
| `"w"` | Write | Creates it | **Truncates it to empty** |
| `"a"` | Append | Creates it | Writes at the end |
| `"x"` | Exclusive create | Creates it | `FileExistsError` |
| `"r+"` | Read and write | Error | Opens at the start |
| `"w+"` | Read and write | Creates it | **Truncates** |
| `"a+"` | Read and append | Creates it | Writes at the end |

Add `"b"` for binary (`"rb"`, `"wb"`) or `"t"` for text (the default).

**`"w"` destroys the file's contents the moment you open it** — before you have
written anything. Use `"a"` when you mean to add to a file.

## A.3 Reading and writing

```python
with open("data.txt") as fh:
    everything = fh.read()          # the whole file as one string
    one_line  = fh.readline()       # a single line, including '\n'
    all_lines = fh.readlines()      # a list of lines

with open("data.txt") as fh:        # the memory-efficient idiom
    for line in fh:                 # reads one line at a time
        print(line.strip())         # strip() removes the trailing newline

with open("out.txt", "w") as fh:
    fh.write("first line\n")        # write() does NOT add a newline
    fh.writelines(["a\n", "b\n"])   # nor does writelines()
```

`read()` loads the entire file into memory. For a large file, iterate over the
file object instead — it reads lazily.

## A.4 File positions

```python
fh.tell()            # current byte position
fh.seek(0)           # back to the start
fh.seek(10)          # 10 bytes in
```

## A.5 CSV files

```python
import csv

# Writing
with open("marks.csv", "w", newline="") as fh:
    writer = csv.writer(fh)
    writer.writerow(["roll", "name", "marks"])
    writer.writerows([[24001, "Ananya", 85], [24002, "Bhavana", 72]])

# Reading as lists
with open("marks.csv", newline="") as fh:
    for row in csv.reader(fh):
        print(row)                      # ['24001', 'Ananya', '85'] -- all strings

# Reading as dictionaries, keyed by the header row
with open("marks.csv", newline="") as fh:
    for row in csv.DictReader(fh):
        print(row["name"], int(row["marks"]))
```

Two points that cost marks: pass **`newline=""`** when opening a CSV (without
it, Windows writes blank lines between rows), and remember that **every value
read from a CSV is a string** — convert numbers explicitly.

Worked example: `11_csv_marks.py`.

## A.6 `os` and `pathlib`

```python
import os

os.getcwd()                       # current directory
os.listdir(".")                   # names in a directory
os.path.exists("data.txt")        # does it exist?
os.path.join("folder", "f.txt")   # correct separator for the platform
os.remove("data.txt")
os.mkdir("newdir")
os.rename("old.txt", "new.txt")
```

```python
from pathlib import Path          # the modern, object-oriented alternative

p = Path("data") / "marks.csv"    # / joins paths -- readable and portable
p.exists()
p.read_text()
p.suffix                          # '.csv'
p.stem                            # 'marks'
```

Use `os.path.join` or `pathlib` rather than writing `"data/" + filename`, so
your code works on Windows too.

---

# Part B — Exception Handling

## B.1 Syntax errors vs exceptions

A **syntax error** is caught before the program runs — the code is not valid
Python and nothing executes:

```python
if x > 5          # SyntaxError: missing colon
```

An **exception** occurs *during* execution, in code that is syntactically fine:

```python
10 / 0            # ZeroDivisionError
```

Only exceptions can be caught and handled.

## B.2 Common built-in exceptions

| Exception | Raised when |
|---|---|
| `ZeroDivisionError` | Dividing by zero |
| `ValueError` | Right type, wrong value — `int("abc")` |
| `TypeError` | Wrong type — `"1" + 1` |
| `IndexError` | Sequence index out of range |
| `KeyError` | Dictionary key not found |
| `FileNotFoundError` | Opening a file that does not exist |
| `AttributeError` | Object has no such attribute |
| `NameError` | Using an undefined name |
| `ImportError` / `ModuleNotFoundError` | Import failed |
| `IndentationError` | Bad indentation |
| `OverflowError` | Result too large for a float |
| `StopIteration` | An iterator is exhausted |

## B.3 `try` / `except` / `else` / `finally`

```python
try:
    number = int(input("Enter a number: "))
    result = 100 / number
except ValueError:
    print("That was not a number")
except ZeroDivisionError:
    print("Cannot divide by zero")
except (TypeError, AttributeError) as exc:      # several in one clause
    print(f"Type problem: {exc}")
except Exception as exc:                        # catch-all -- put it LAST
    print(f"Unexpected: {exc}")
else:
    print(f"Result is {result}")                # runs only if NO exception
finally:
    print("This always runs")                   # cleanup, error or not
```

**Order matters.** Python tries each `except` in turn and uses the first that
matches. A bare `except Exception` placed first would swallow everything, so
the specific handlers must come before the general one.

| Block | Runs when |
|---|---|
| `try` | Always — it is the code being guarded |
| `except` | Only if a matching exception occurred |
| `else` | Only if **no** exception occurred |
| `finally` | **Always**, whether or not there was an exception |

**Never write a bare `except:`.** It catches `KeyboardInterrupt` and
`SystemExit` too, so your program cannot be stopped with Ctrl-C. Use
`except Exception:` if you really need a catch-all.

## B.4 `raise`

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age

try:
    set_age(-5)
except ValueError as exc:
    print(exc)                  # Age cannot be negative
```

Re-raising after logging:

```python
try:
    risky()
except Exception:
    log_it()
    raise               # a bare raise re-raises the current exception
```

## B.5 User-defined exceptions

```python
class InsufficientBalanceError(Exception):
    """Raised when a withdrawal exceeds the available balance."""

    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Cannot withdraw {amount}; balance is only {balance}")


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError(balance, amount)
    return balance - amount
```

Custom exceptions inherit from `Exception` (not from `BaseException`). Naming
them `...Error` is the convention.

## B.6 Assertions

```python
assert len(scores) > 0, "scores must not be empty"
```

Raises `AssertionError` with the message when the condition is false.

**Assertions are for detecting programmer errors, not for validating user
input**, because Python's `-O` flag removes them entirely. Never rely on an
assertion for anything security- or correctness-critical at runtime.

Worked examples:
`12_exception_handling.py`.

---

# Part C — Object-Oriented Programming

## C.1 Classes and objects

A **class** is a blueprint; an **object** is an instance built from it. One
`Student` class, many student objects.

```python
class Student:
    college = "Adikavi Nannaya University"      # CLASS attribute -- shared

    def __init__(self, roll, name, marks):      # CONSTRUCTOR
        self.roll = roll                        # INSTANCE attributes
        self.name = name
        self.marks = marks

    def average(self):                          # METHOD
        return sum(self.marks) / len(self.marks)

    def display(self):
        print(f"{self.roll} {self.name} {self.average():.2f}")


s1 = Student(24001, "Ananya", [85, 78, 92])     # creating an object
s1.display()
```

### `self`

`self` refers to the object the method was called on. It is **the first
parameter of every instance method**, supplied automatically by Python:
`s1.display()` really means `Student.display(s1)`.

The name `self` is a convention, not a keyword — but never rename it.

**Forgetting `self` is the most common OOP error in exams.** Both in the
parameter list and when accessing attributes: `self.name`, not `name`.

### Class vs instance attributes

```python
class Student:
    count = 0                          # class attribute -- one, shared

    def __init__(self, name):
        self.name = name               # instance attribute -- one per object
        Student.count += 1             # update via the CLASS, not self
```

Changing a class attribute through the class affects every object. Assigning to
it through an instance (`s1.count = 5`) quietly creates a *new instance
attribute* that shadows the class one — a classic trap.

## C.2 Constructor and destructor

```python
class Student:
    def __init__(self, name):          # CONSTRUCTOR -- runs on creation
        self.name = name
        print(f"{name} created")

    def __del__(self):                 # DESTRUCTOR -- runs on deletion
        print(f"{self.name} destroyed")
```

`__del__` runs when the object is garbage collected, which is **not
necessarily** when you call `del`. Python uses reference counting: the object
is destroyed when the last reference to it disappears. Do not rely on `__del__`
for important cleanup — use `with` and context managers.

### Other dunder methods worth knowing

```python
def __str__(self):                     # what print() shows -- for humans
    return f"Student({self.name})"

def __repr__(self):                    # what the shell shows -- for developers
    return f"Student(roll={self.roll!r})"

def __len__(self):                     # enables len(obj)
    return len(self.marks)

def __eq__(self, other):               # enables obj1 == obj2
    return self.roll == other.roll
```

## C.3 Encapsulation

Bundling data with the methods that operate on it, and controlling access to
that data.

| Convention | Syntax | Meaning |
|---|---|---|
| Public | `self.name` | Use freely |
| Protected | `self._name` | "Internal — please do not touch" (convention only) |
| Private | `self.__name` | Name-mangled to `_ClassName__name` |

```python
class Account:
    def __init__(self, balance):
        self.__balance = balance       # private

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.__balance += amount

    def get_balance(self):             # a getter
        return self.__balance


a = Account(1000)
a.deposit(500)
a.get_balance()          # 1500
a.__balance              # AttributeError
a._Account__balance      # 1500 -- name mangling, not true privacy
```

**Python has no real access control.** The double underscore triggers *name
mangling*, which prevents accidental collisions in subclasses and signals
intent — but a determined caller can still reach the attribute. State this in
an exam: "Python enforces encapsulation by convention, not by the compiler."

The point of the getter/setter pair is not secrecy but **validation**: the
`deposit` method can reject a negative amount, where direct attribute
assignment could not.

## C.4 Inheritance

A child class acquires the attributes and methods of a parent.

### Single inheritance

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print(f"Name: {self.name}, Age: {self.age}")


class Student(Person):                       # Student inherits from Person
    def __init__(self, name, age, roll):
        super().__init__(name, age)          # call the parent's constructor
        self.roll = roll

    def display(self):                       # METHOD OVERRIDING
        super().display()                    # reuse the parent's version
        print(f"Roll: {self.roll}")
```

`super()` gives access to the parent class. Calling `super().__init__()` is
essential — without it the parent's attributes are never set.

### Multilevel inheritance — a chain

```python
class Person: ...
class Student(Person): ...
class ResearchScholar(Student): ...      # Person -> Student -> ResearchScholar
```

### Multiple inheritance — two parents

```python
class Student: ...
class Teacher: ...
class TeachingAssistant(Student, Teacher): ...
```

Python resolves conflicts using the **Method Resolution Order (MRO)**,
computed by the C3 linearisation algorithm:

```python
TeachingAssistant.__mro__
# (TeachingAssistant, Student, Teacher, object)
```

Methods are looked up left to right along that order. C++ has the "diamond
problem" here; Python's MRO is its answer to it.

### Types of inheritance — all five

| Type | Shape |
|---|---|
| Single | One parent, one child |
| Multilevel | A → B → C |
| Multiple | Two or more parents, one child |
| Hierarchical | One parent, several children |
| Hybrid | A combination of the above |

The syllabus names the first three; know all five.

### Method overriding vs overloading

**Overriding** — a child redefines a method it inherited. Fully supported.

**Overloading** — several methods with the same name and different signatures.
**Python does not support this.** A later definition simply replaces the
earlier one. Simulate it with default arguments or `*args`:

```python
def add(self, a, b=0, c=0):        # handles 1, 2 or 3 arguments
    return a + b + c
```

This is a favourite exam question: *"Does Python support method overloading?"*
The answer is no, followed by the workaround.

### Polymorphism

The same call, different behaviour depending on the object's class:

```python
for obj in (Person("A", 40), Student("B", 19, 24001)):
    obj.display()          # calls whichever version belongs to that class
```

Python uses **duck typing**: if an object has a `display()` method it can be
used here, regardless of what it inherits from. "If it walks like a duck and
quacks like a duck, treat it as a duck."

Worked examples:
`13_student_class.py` and
`14_inheritance.py`.

---

## Exam questions from this unit

**Two marks**

1. What is the difference between `"w"` and `"a"` file modes?
2. Why is the `with` statement preferred for file handling?
3. Difference between a syntax error and an exception.
4. When does the `finally` block execute?
5. What is `self`?
6. Does Python support method overloading?

**Five marks**

1. Explain file modes with a table and examples.
2. Explain `try-except-else-finally` with a complete example.
3. Explain how to define a user-defined exception, with an example.
4. Explain encapsulation in Python and why it is by convention.
5. Explain method overriding with an example.

**Ten marks**

1. Explain exception handling in Python fully — built-in exceptions, `try`,
   `except`, `else`, `finally`, `raise`, user-defined exceptions and assertions.
2. Explain the types of inheritance with programs for each, and explain the MRO.
3. Explain classes, objects, constructors, destructors and encapsulation with a
   complete program.

## Mistakes that cost marks

- Forgetting `self` in a method definition or when accessing an attribute
- Forgetting to call `super().__init__()` in a child's constructor
- Placing `except Exception` before the specific handlers
- Using a bare `except:`
- Opening a valuable file with `"w"` and losing it
- Forgetting `newline=""` when writing a CSV
- Treating CSV values as numbers without converting them
- Claiming Python supports method overloading
- Believing `__private` is genuinely inaccessible
