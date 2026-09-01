# Course 3 — Practice Questions with Solutions

Predict each answer before reading on.

---

## Section A — Predict the output

### Q1
```python
print(10 / 3, 10 // 3, 10 % 3, 10 ** 3)
```
**Answer: `3.3333333333333335 3 1 1000`**

`/` always gives a float. `//` floors. Note the floating-point representation —
`10/3` is not exactly 3.3333.

### Q2
```python
print(-7 // 2, -7 % 2)
```
**Answer: `-4 1`**

Floor division rounds **towards negative infinity**, so −3.5 becomes −4 (not
−3). The modulus takes the sign of the *divisor*, giving +1. C would give −3
and −1. A favourite exam trap.

### Q3
```python
print(2 ** 3 ** 2, -2 ** 2)
```
**Answer: `512 -4`**

`**` is right-associative, so `2 ** (3 ** 2)` = `2 ** 9` = 512. And `**` binds
tighter than unary minus, so `-2 ** 2` is `-(2 ** 2)` = −4.

### Q4
```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```
**Answer: `[1, 2, 3, 4]`**

`b = a` does not copy — both names refer to the same list object. Use
`b = a.copy()` for an independent list.

### Q5
```python
def add(item, lst=[]):
    lst.append(item)
    return lst

print(add(1))
print(add(2))
```
**Answer: `[1]` then `[1, 2]`**

The mutable default is created **once**, at definition time, and persists
between calls. Fix it with `lst=None` and `if lst is None: lst = []`.

### Q6
```python
print(sorted([3, 1, 2]), [3, 1, 2].sort())
```
**Answer: `[1, 2, 3] None`**

`sorted()` returns a new list; `.sort()` sorts in place and returns `None`.

### Q7
```python
for i in range(3):
    if i == 1:
        break
else:
    print("completed")
print("done")
```
**Answer: `done`**

The `else` of a loop runs only when the loop finished **without** `break`. It
did break, so `completed` never prints.

### Q8
```python
print({1, 2, 3} == {3, 2, 1})
print([1, 2, 3] == [3, 2, 1])
```
**Answer: `True` then `False`**

Sets are unordered, so order is irrelevant to equality. Lists are ordered, so
it matters.

### Q9
```python
s = "hello"
print(s[::-1], s[1:3], s[-2:])
```
**Answer: `olleh el lo`**

### Q10
```python
x = 10
def f():
    x = 20
f()
print(x)
```
**Answer: `10`**

The assignment inside `f` creates a *local* `x`. The global is untouched.
Adding `global x` would make it print 20.

---

## Section B — Find and fix

### Q11
```python
age = input("Enter age: ")
if age > 18:
    print("Adult")
```
**Error:** `input()` returns a string; comparing `str` to `int` raises
`TypeError`.
**Fix:** `age = int(input("Enter age: "))`

### Q12
```python
class Student:
    def __init__(name, roll):
        self.name = name
```
**Errors:** `self` is missing from the parameter list, and `roll` is never
stored.
**Fix:**
```python
def __init__(self, name, roll):
    self.name = name
    self.roll = roll
```

### Q13
```python
try:
    x = 1 / 0
except:
    pass
```
**Errors:** a bare `except:` catches `KeyboardInterrupt` and `SystemExit`,
making the program unstoppable; and `pass` silently swallows the problem.
**Fix:**
```python
try:
    x = 1 / 0
except ZeroDivisionError as exc:
    print(f"Error: {exc}")
```

### Q14
```python
numbers = [1, 2, 3, 4, 5, 6]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)
```
**Error:** modifying a list while iterating over it. The iterator's index keeps
advancing while the list shrinks, so elements are skipped. This prints
`[1, 3, 5]` only by luck on some inputs; on `[2, 4]` it leaves `[4]`.
**Fix:** `numbers = [n for n in numbers if n % 2 != 0]`

### Q15
```python
with open("data.txt", "w") as fh:
    content = fh.read()
```
**Errors:** `"w"` truncates the file — its contents are already gone — and a
file opened for writing cannot be read.
**Fix:** open with `"r"`.

---

## Section C — Write the program

### Q16 — Count word frequency in a sentence

```python
def word_frequency(sentence):
    frequency = {}
    for word in sentence.lower().split():
        word = word.strip(".,!?;:")
        if word:
            frequency[word] = frequency.get(word, 0) + 1
    return frequency

text = "the quick brown fox jumps over the lazy dog. The dog barks."
for word, count in sorted(word_frequency(text).items(),
                          key=lambda pair: -pair[1]):
    print(f"{word:<10} {count}")
```

`dict.get(word, 0)` avoids a `KeyError` on the first sighting of each word.
`collections.Counter(text.split())` does the same job in one line — mention it
as the idiomatic alternative.

### Q17 — Second largest element without sorting

```python
def second_largest(numbers):
    if len(numbers) < 2:
        raise ValueError("need at least two elements")
    largest = second = float("-inf")
    for n in numbers:
        if n > largest:
            second = largest
            largest = n
        elif n > second and n != largest:
            second = n
    if second == float("-inf"):
        raise ValueError("all elements are equal")
    return second
```

One pass, O(n). `sorted(set(numbers))[-2]` also works but is O(n log n).

### Q18 — Check whether two strings are anagrams

```python
def are_anagrams(a, b):
    a = "".join(sorted(a.lower().replace(" ", "")))
    b = "".join(sorted(b.lower().replace(" ", "")))
    return a == b

print(are_anagrams("Listen", "Silent"))     # True
```

The counting version using a dictionary is O(n) rather than O(n log n) — give
the sorted version for brevity and mention the faster one.

### Q19 — A Student class with marks and grade

```python
class Student:
    def __init__(self, roll, name, marks):
        self.roll = roll
        self.name = name
        self.marks = marks          # a dict of subject -> mark

    def total(self):
        return sum(self.marks.values())

    def average(self):
        return self.total() / len(self.marks)

    def grade(self):
        avg = self.average()
        if avg >= 85: return "A"
        if avg >= 70: return "B"
        if avg >= 50: return "C"
        return "F"

    def __str__(self):
        return (f"{self.roll} {self.name}: total {self.total()}, "
                f"average {self.average():.2f}, grade {self.grade()}")


s = Student(24001, "Ananya", {"maths": 85, "python": 92, "stats": 78})
print(s)
```

### Q20 — Reverse a singly linked list

```python
def reverse(self):
    previous, current = None, self.head
    while current:
        following = current.next     # save it before overwriting
        current.next = previous      # flip the pointer
        previous = current           # advance both markers
        current = following
    self.head = previous             # the old tail is the new head
```

Saving `current.next` **before** overwriting it is the whole trick. Skip that
line and you lose the rest of the list irrecoverably.

Draw it out for a three-node list — examiners award marks for the diagram.

---

## Section D — Long answers

### Q21 — Compare lists, tuples, sets and dictionaries

Give the property table (ordered, mutable, duplicates, indexed, syntax), then
a short example of each, then **when to use each**. That last part is what
separates a full-mark answer:

- List — an ordered collection you will modify
- Tuple — a fixed record; also usable as a dictionary key
- Set — membership tests and de-duplication, both O(1)
- Dictionary — lookup by key

### Q22 — Explain the types of inheritance

Cover single, multilevel, multiple, hierarchical and hybrid, with a short
program for each and a diagram. Then explain `super()` and the MRO, and finish
with method overriding.

Full treatment in [unit-4.md Part C](unit-4.md); runnable code in
`14_inheritance.py`.

### Q23 — Explain exception handling with all clauses

`try`, `except` (specific before general), `else`, `finally`, `raise`, custom
exception classes, and `assert`. Give a single worked program that uses all of
them, and state clearly when each block runs.

---

## Quick self-test

1. What does `input()` return?
2. Why is `{}` not an empty set?
3. What does `list.sort()` return?
4. When does a loop's `else` clause run?
5. What is the difference between `is` and `==`?
6. Does Python support method overloading?
7. Why must `super().__init__()` be called in a child constructor?
8. What is the time complexity of `pop(0)` on a list?
9. What does `with open(...)` guarantee?
10. Why is `__private` not truly private?

**Answers:** 1. Always a string. · 2. `{}` creates an empty *dict*; use `set()`.
· 3. `None` — it sorts in place. · 4. Only when the loop ended without `break`.
· 5. `==` compares values, `is` compares object identity. · 6. No — a later
definition replaces the earlier one; simulate with default arguments or
`*args`. · 7. Otherwise the parent's attributes are never initialised. ·
8. O(n) — every later element shifts down. · 9. The file is closed even if an
exception is raised. · 10. It is name-mangled to `_ClassName__private`, which
prevents accidents but is still reachable.
