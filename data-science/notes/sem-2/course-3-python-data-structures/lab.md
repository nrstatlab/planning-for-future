# Lab — Python Programming and Data Structures

**18 experiments**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.

All programs are in
`labs/course-3-python/`. All eighteen were run under Python 3.11 for this page, and what each
printed is shown under **5. Execution and Results**. The two Tkinter programs need a display:
they were run under a virtual one, by a driver beside each (`_drive_17_tkinter_input.py`,
`_drive_18_tkinter_calculator.py`) that types into the window, presses its buttons and checks
what it shows, and the window is shown as it looked.

```bash
bash tools/data-science/run_python_labs.sh        # re-run everything
python3 labs/course-3-python/05_list_operations.py
```

---

## The experiments

| # | Experiment | File | Unit |
|:---:|---|---|:---:|
| 1a | Basic details and literal types | `01a_basic_details.py` | 1 |
| 1b | All operator categories | `01b_operators.py` | 1 |
| 2a | Largest of three (`if-elif-else`) | `02a_largest_of_three.py` | 2 |
| 2b | Prime check using loops | `02b_prime_check.py` | 2 |
| 2c | `break`, `continue`, `pass` | `02c_loop_control.py` | 2 |
| 3a | Factorial by recursion | `03a_factorial_recursion.py` | 2 |
| 3b | Function argument types | `03b_function_arguments.py` | 2 |
| 4 | String slicing and methods | `04_string_operations.py` | 3 |
| 5 | List operations and comprehension | `05_list_operations.py` | 3 |
| 6 | Tuple packing and immutability | `06_tuple_operations.py` | 3 |
| 7 | Set operations | `07_set_operations.py` | 3 |
| 8 | Dictionary operations | `08_dictionary_operations.py` | 3 |
| 9 | Count vowels, consonants, digits, spaces | `09_count_file_characters.py` | 4 |
| 10 | Copy one file to another | `10_copy_file.py` | 4 |
| 11 | Process marks from a CSV | `11_csv_marks.py` | 4 |
| 12 | `try-except-finally` | `12_exception_handling.py` | 4 |
| 13 | Student class | `13_student_class.py` | 4 |
| 14 | Single and multilevel inheritance | `14_inheritance.py` | 4 |
| 15 | Stack and queue, list and linked | `15_stack_queue.py` | 5 |
| 16 | Singly linked list | `16_linked_list.py` | 5 |
| 17 | Tkinter — Label, Entry, Button | `17_tkinter_input.py` | 5 |
| 18 | Tkinter — calculator | `18_tkinter_calculator.py` | 5 |

---

## Experiment 1a — Basic details and literal types

### 1. Question

Unit 1. Display basic details using `print()` and demonstrate the different literal types: int, float, string, boolean, complex.

### 2. Aim

Print a student's details, and name the type of each kind of literal.

### 3. Steps

1. **Assign one literal of each type.**
2. **Print the details.**
3. **Name the type of each value.** `type(value).__name__` gives the type's name.
4. **The two parts of a complex number.**

### 4. Programme

{{programme: course-3-python/01a_basic_details.py}}

### 5. Execution and Results

{{output: course-3-python/01a_basic_details.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The details print as labelled lines, and the five literals are an `int`, a `float`, a `str`, a `bool` and a `complex`, whose real and imaginary parts are 3.0 and 4.0.
</div>


## Experiment 1b — All operator categories

### 1. Question

Unit 1. Perform arithmetic, relational, logical, bitwise and assignment operations on two integers given as input (here 12 and 5).

### 2. Aim

Show what each operator gives on the same two numbers.

### 3. Steps

1. **Read two integers.** `input()` returns text, so each is converted with `int()`.
2. **Arithmetic.**
3. **Relational.**
4. **Logical.**
5. **Bitwise.**
6. **Augmented assignment.**
7. **Identity and membership.**

### 4. Programme

{{programme: course-3-python/01b_operators.py}}

### 5. Execution and Results

{{output: course-3-python/01b_operators.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

On 12 and 5: `/` gives 2.4, always a float, while `//` gives 2 and `%` 2; `12 & 5` is 4, `12 | 5` 13 and `~12` −13; `a is b` is False and `a in [a, b]` True.
</div>


## Experiment 2a — Largest of three (if-elif-else)

### 1. Question

Unit 2. Find the largest of three numbers using `if-elif-else` (here 45, 78 and 23).

### 2. Aim

Choose the largest of three numbers by comparison.

### 3. Steps

1. **Read three numbers.**
2. **Compare them with if-elif-else.**
3. **Print the largest, and check it with max().** The built-in `max()` is the cross-check — correct, but the exam wants the `if-elif-else` version.

### 4. Programme

{{programme: course-3-python/02a_largest_of_three.py}}

### 5. Execution and Results

{{output: course-3-python/02a_largest_of_three.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The largest of 45, 78 and 23 is 78, and `max()` agrees.
</div>


## Experiment 2b — Prime check

### 1. Question

Unit 2. Check whether a number is prime using loops (here 29).

### 2. Aim

Decide whether n is prime, testing as few divisors as possible.

### 3. Steps

1. **Read n.**
2. **A number below 2 is not prime.**
3. **Try each divisor up to the square root.** `break` leaves the loop at the first divisor found.
4. **Report the result.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

Test divisors only up to √n. If n had a factor larger than its square root, the
matching co-factor would be smaller than the square root and you would have
found it already. Write the loop as `while divisor * divisor <= n` rather than
computing a square root — it avoids floating-point comparison entirely.

Remember that 0, 1 and negative numbers are **not** prime, and 2 is the only
even prime.
</div>


### 4. Programme

{{programme: course-3-python/02b_prime_check.py}}

### 5. Execution and Results

{{output: course-3-python/02b_prime_check.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

29 has no divisor from 2 to 5, so it is prime.
</div>


## Experiment 2c — break, continue, pass

### 1. Question

Unit 2. Illustrate the loop control statements `break`, `continue` and `pass`.

### 2. Aim

Show what each of the three statements does to the same loop.

### 3. Steps

1. **break.**
2. **continue.**
3. **pass.**
4. **else on a loop.** A loop's `else` runs only when the loop was not broken out of.

### 4. Programme

{{programme: course-3-python/02c_loop_control.py}}

### 5. Execution and Results

{{output: course-3-python/02c_loop_control.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

`break` stops the count at 4; `continue` skips the even numbers; `pass` does nothing, so the multiples of 3 are simply not printed; and the loop's `else` runs because nothing broke out of it.
</div>


## Experiment 3a — Factorial by recursion

### 1. Question

Unit 2. Calculate the factorial of a number using recursion (here 6).

### 2. Aim

Compute n! recursively, and trace the calls.

### 3. Steps

1. **The recursive function: a base case and a recursive case.** Without the base case the recursion never stops.
2. **The same function, printing each call.**
3. **Read n, and print n! and the call trace.**

### 4. Programme

{{programme: course-3-python/03a_factorial_recursion.py}}

### 5. Execution and Results

{{output: course-3-python/03a_factorial_recursion.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

6! = 720. The trace shows six calls going down to the base case and six returns coming back up.
</div>


## Experiment 3b — Function arguments

### 1. Question

Unit 2. Demonstrate the different types of function arguments: default, positional, keyword and variable-length.

### 2. Aim

Call functions with every kind of argument, and see what each receives.

### 3. Steps

1. **Required and default parameters.**
2. **Variable-length *args and **kwargs.**
3. **All four kinds in their required order.**
4. **Call with positional, keyword and default arguments.**
5. **Call with variable-length arguments.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

Demonstrate all five: required, default, keyword, `*args` and `**kwargs`. Show
that `*args` arrives as a **tuple** and `**kwargs` as a **dict** — printing
`type()` for each makes the point clearly.
</div>


### 4. Programme

{{programme: course-3-python/03b_function_arguments.py}}

### 5. Execution and Results

{{output: course-3-python/03b_function_arguments.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Positional arguments match by position and keyword ones by name; `year` falls back to 1; `*args` arrives as the tuple `(1, 2, 3, 4, 5)` and `**kwargs` as a dict.
</div>


## Experiment 4 — String slicing and methods

### 1. Question

Unit 3. Illustrate string slicing, concatenation, repetition and the built-in string methods.

### 2. Aim

Take a string apart by index and slice, and transform it with its methods.

### 3. Steps

1. **The string.**
2. **Indexing.**
3. **Slicing.** `text[start:stop:step]`; the stop is excluded.
4. **Concatenation and repetition.**
5. **The string methods.**
6. **Immutability.**
7. **Traversal.**

### 4. Programme

{{programme: course-3-python/04_string_operations.py}}

### 5. Execution and Results

{{output: course-3-python/04_string_operations.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

`text[5:12]` is `'Science'` and `text[::-1]` the string reversed; the methods return new strings, and assigning to `text[0]` raises a `TypeError`, because strings are immutable.
</div>


## Experiment 5 — List operations and comprehension

### 1. Question

Unit 3. Create a list of numbers and perform insertion, deletion, searching, sorting and list comprehension.

### 2. Aim

Change a list in each of the ways a list can be changed.

### 3. Steps

1. **The list.**
2. **Insertion.**
3. **Deletion.**
4. **Searching.**
5. **Sorting.** `sorted()` returns a new list; `.sort()` sorts in place.
6. **List comprehension.**
7. **Mutability: an alias and a copy.**

### 4. Programme

{{programme: course-3-python/05_list_operations.py}}

### 5. Execution and Results

{{output: course-3-python/05_list_operations.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Every operation changes the list in place; `sorted()` leaves it alone. After `numbers[0] = 999` the alias has changed too, because it is the same list, and the copy has not.
</div>


## Experiment 6 — Tuple packing and immutability

### 1. Question

Unit 3. Demonstrate tuple packing, unpacking and immutability.

### 2. Aim

Show what tuples are for, and that they cannot be changed.

### 3. Steps

1. **Packing.**
2. **Unpacking.**
3. **Extended unpacking.**
4. **Swapping by tuple assignment.**
5. **Operations.**
6. **Immutability.**
7. **The single-element tuple.**
8. **Tuples as dictionary keys.**

### 4. Programme

{{programme: course-3-python/06_tuple_operations.py}}

### 5. Execution and Results

{{output: course-3-python/06_tuple_operations.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

`a, b = b, a` swaps without a temporary variable; `t[0] = 99` raises a `TypeError`; `(5)` is an `int` and `(5,)` a tuple; and a tuple of coordinates can be a dictionary key.
</div>


## Experiment 7 — Set operations

### 1. Question

Unit 3. Implement the set operations: union, intersection, difference, subset and superset.

### 2. Aim

Combine and compare two sets.

### 3. Steps

1. **Two sets.**
2. **Union, intersection and difference.**
3. **Subset and superset.**
4. **Modifying a set.**
5. **Duplicates are dropped.**
6. **Frozenset.**
7. **Set comprehension.**

### 4. Programme

{{programme: course-3-python/07_set_operations.py}}

### 5. Execution and Results

{{output: course-3-python/07_set_operations.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A ∪ B is {1, …, 8}, A ∩ B is {4, 5}, and A − B is {1, 2, 3}; {1, 2, 3} is a subset of A; `discard()` ignores a missing value where `remove()` raises a `KeyError`; and a frozenset has no `add()`.
</div>


## Experiment 8 — Dictionary operations

### 1. Question

Unit 3. Create a dictionary of student roll numbers and marks, then add, update, delete and traverse it.

### 2. Aim

Keep a set of marks in a dictionary and work with them.

### 3. Steps

1. **The dictionary.**
2. **Add.**
3. **Update.**
4. **Delete.**
5. **Access.** `get()` returns None (or a default) for a missing key; `[]` raises a `KeyError`.
6. **Traversal.**
7. **Aggregates.**
8. **Dictionary comprehension.**

### 4. Programme

{{programme: course-3-python/08_dictionary_operations.py}}

### 5. Execution and Results

{{output: course-3-python/08_dictionary_operations.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

After the changes four students remain, with total 337 and average 84.25; roll 24003 has the highest mark (91) and 24005 the lowest (78).
</div>


## Experiment 9 — Count vowels, consonants, digits and spaces

### 1. Question

Unit 4. Read a text file and display the count of vowels, consonants, digits and spaces.

### 2. Aim

Classify every character of a file.

### 3. Steps

1. **Write the sample file.**
2. **Read it back.**
3. **Classify each character.**
4. **Print the counts.**

### 4. Programme

{{programme: course-3-python/09_count_file_characters.py}}

### 5. Execution and Results

{{output: course-3-python/09_count_file_characters.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The two lines hold 24 vowels, 34 consonants, 4 digits and 9 spaces: 71 characters, not counting the newlines.
</div>


## Experiment 10 — Copy one file to another

### 1. Question

Unit 4. Copy the contents of one file into another file.

### 2. Aim

Copy a file line by line, and check the copy.

### 3. Steps

1. **Write the source file.**
2. **Copy it line by line.**
3. **Print the copy.**
4. **Check that the two files match.**

### 4. Programme

{{programme: course-3-python/10_copy_file.py}}

### 5. Execution and Results

{{output: course-3-python/10_copy_file.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Three lines are copied, and the two files are identical.
</div>


## Experiment 11 — CSV processing

### 1. Question

Unit 4. Read and process student marks from a CSV file, calculating the average, highest and lowest.

### 2. Aim

Read a CSV file into records and summarise them.

### 3. Steps

1. **Write the CSV file.**
2. **Read it with DictReader, converting the marks.**
3. **Print each student.**
4. **The class summary.**
5. **Subject by subject.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

Use `csv.DictReader`, which keys each row by the header. Two things to
remember: pass `newline=""` when opening, and convert every value — CSV data is
always strings.
</div>


### 4. Programme

{{programme: course-3-python/11_csv_marks.py}}

### 5. Execution and Results

{{output: course-3-python/11_csv_marks.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The class average is 79.00; Charan has the highest total (275) and Divya the lowest (209).
</div>


## Experiment 12 — try-except-finally

### 1. Question

Unit 4. Demonstrate exception handling using `try-except-finally`.

### 2. Aim

Catch each common exception, and raise one of your own.

### 3. Steps

1. **A user-defined exception.**
2. **try, except, else and finally.** `else` runs only when no exception was raised; `finally` always runs.
3. **ZeroDivisionError.**
4. **ValueError.**
5. **Several exception types.**
6. **FileNotFoundError.**
7. **raise.**
8. **assert.**

### 4. Programme

{{programme: course-3-python/12_exception_handling.py}}

### 5. Execution and Results

{{output: course-3-python/12_exception_handling.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Each error is caught and reported instead of stopping the program; `finally` runs both times; and the user-defined `InvalidMarkError` rejects a mark of 150.
</div>


## Experiment 13 — Student class

### 1. Question

Unit 4. Create a class `Student` with attributes and methods to display its details.

### 2. Aim

Define a class with a constructor, methods, a private attribute and a destructor, and use it.

### 3. Steps

1. **The class, its attributes and its constructor.**
2. **The methods.**
3. **A private attribute, reached through methods.**
4. **display, __str__ and the destructor.**
5. **Create two objects and display them.**
6. **__str__ at work.**
7. **Encapsulation at work.**
8. **Class and instance attributes.**
9. **The destructor at work.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

Include the constructor `__init__`, at least one private attribute with a
getter, `__str__`, and `__del__`. That covers the whole of the syllabus's
"classes, objects, attributes, methods, constructor and destructors" in one
program.
</div>


### 4. Programme

{{programme: course-3-python/13_student_class.py}}

### 5. Execution and Results

{{output: course-3-python/13_student_class.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Ananya averages 85.00 (grade A) and Bhavana 63.67 (grade C). The private fee attribute changes only through `pay_fees()`; changing the class attribute changes every object; and the destructor runs for each object.
</div>


## Experiment 14 — Single and multilevel inheritance

### 1. Question

Unit 4. Demonstrate single and multilevel inheritance. The syllabus (Unit 4) also lists multiple inheritance and method overriding, so both are included.

### 2. Aim

Build classes on classes, and see which method each object uses.

### 3. Steps

1. **Single inheritance, with overriding.**
2. **Multilevel inheritance.**
3. **Multiple inheritance.**
4. **Polymorphism.**

### 4. Programme

{{programme: course-3-python/14_inheritance.py}}

### 5. Execution and Results

{{output: course-3-python/14_inheritance.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Each subclass overrides `display()` and `role()` and reuses its parent's through `super()`; the method resolution order of `ResearchScholar` is ResearchScholar → Student → Person → object; and the same `role()` call gives a different answer for each class.
</div>


## Experiment 15 — Stack and queue

### 1. Question

Unit 5. Implement a stack (LIFO) and a queue (FIFO) using both lists and linked lists.

### 2. Aim

Build a stack and a queue two ways each, and use a stack for a real check.

### 3. Steps

1. **A stack on a list.**
2. **A queue on a list.**
3. **A stack on a linked list.**
4. **A queue on a linked list.**
5. **A priority queue.**
6. **Use each of them.**
7. **Underflow.**
8. **Balanced brackets, with a stack.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

The syllabus asks for **both** the list and the linked-list implementations.
The linked-list versions are the more instructive: a linked stack pushes and
pops at the head, both O(1); a linked queue keeps both a front and a rear
pointer so that both operations are O(1), where the list version's
`pop(0)` is O(n).

Add the balanced-bracket checker as an application — it appears in exams
regularly.
</div>


### 4. Programme

{{programme: course-3-python/15_stack_queue.py}}

### 5. Execution and Results

{{output: course-3-python/15_stack_queue.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The stacks give back 30 then 20, last in first out; the queues give back A then B, first in first out; the priority queue serves the heart attack first; and `{[()]}` is balanced where `{[(])}` and `(((` are not.
</div>


## Experiment 16 — Singly linked list

### 1. Question

Unit 5. Implement a singly linked list: node creation, insertion, deletion and traversal. The syllabus (Unit 5) names singly, doubly and circular linked lists but says "Single Linked list implementation only".

### 2. Aim

Build a linked list and carry out every operation on it.

### 3. Steps

1. **A node: a value and a link.**
2. **Insertion.**
3. **Deletion.**
4. **Search, length, reverse and display.**
5. **Build a list and use each operation.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

The two operations that carry the marks are **deleting the head** (you must
move `self.head`, not `previous.next`) and **reversing the list** (save
`current.next` before overwriting it, or the rest of the chain is lost).
</div>


### 4. Programme

{{programme: course-3-python/16_linked_list.py}}

### 5. Execution and Results

{{output: course-3-python/16_linked_list.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The list grows to 10 → 20 → 25 → 30, finds 25 at index 2, deletes 25 and then the head, and reverses 20 → 30 → 40 to 40 → 30 → 20.
</div>


## Experiment 17 — Tkinter — Label, Entry, Button

### 1. Question

Unit 5. A Tkinter program with Label, Entry and Button widgets that takes user input and displays it.

### 2. Aim

Build a small form whose buttons respond to events.

### 3. Steps

1. **Labels and Entry widgets.**
2. **Buttons, bound to their handlers.**
3. **The output label.**
4. **The Submit handler.**
5. **The Clear handler.**
6. **Start the event loop.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

Both Tkinter programs need a display, so they cannot run over SSH or in a container without X
forwarding. On Debian/Ubuntu install `python3-tk` first. For this page each was run under a
virtual display by its driver, which types into the window, presses the buttons and checks what
appears.
</div>


### 4. Programme

{{programme: course-3-python/17_tkinter_input.py}}

### 5. Execution and Results

{{output: course-3-python/17_tkinter_input.py}}

The window after Submit, and after Clear.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Submit shows the three entries in the output label; Clear empties the form; and Submit with the name missing raises the warning and shows nothing.
</div>


## Experiment 18 — Tkinter — calculator

### 1. Question

Unit 5. A simple calculator application in Tkinter.

### 2. Aim

Build a calculator whose buttons all share one handler, and keep its `eval()` safe.

### 3. Steps

1. **The display and the buttons.**
2. **One handler for every button.**
3. **Evaluate, safely.**
4. **Start the event loop.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

For the calculator, note the security comment in the file: `eval()` is used on
a validated character set with empty builtins. `eval()` on unfiltered user
input is a genuine vulnerability — say so if asked, because it demonstrates
judgement beyond the syllabus.
</div>


### 4. Programme

{{programme: course-3-python/18_tkinter_calculator.py}}

### 5. Execution and Results

{{output: course-3-python/18_tkinter_calculator.py}}

The window after 12+7*3=, and after 8/0=.

Note that `**` is two `*` keys, so the character check lets powers through: `2**3` gives 8. The
check limits *which characters* can reach `eval()`, not which expressions — which is why the
empty builtins are needed as well.

**The window is cut off on the right and at the bottom.** The program fixes it at 300 × 380 and
makes it not resizable, but with the fonts of the Linux machine it ran on, the buttons ask for
336 × 428, so the last column and the bottom row (0, ., <, =) are clipped; they still work, and
the driver pressed them. Fonts differ between systems, and Windows' narrower Arial may fit.
Leaving out `geometry()` and `resizable()`, so that Tk sizes the window to its widgets, makes it
fit everywhere.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

12+7×3 gives 33 and (12+7)×3 gives 57, so precedence and brackets work; 7/2 gives 3.5; 8/0 shows "Cannot divide by zero"; and an expression with letters in it is refused before `eval()` sees it.
</div>


---

## Lab exam tips

1. **Watch your indentation.** It is the most common cause of a program that
   will not run at all. Four spaces, never tabs.
2. **Convert `input()`.** `int(input(...))` or `float(input(...))`.
3. **Print prompts** before every input.
4. **Test the edge cases**: an empty list, n = 0, a negative number, a missing
   file, a division by zero.
5. **Use meaningful names.** `student_marks`, not `sm`.
6. **Add a docstring** to every function you define — the syllabus lists
   documentation strings explicitly, and it is free marks.
7. **Expect a viva.** "Why a dictionary here rather than a list?" and "what
   happens if the file does not exist?" are the standard questions.

## What the practical record should contain

For each experiment, the five parts set out above: **1. Question**, the task as set; **2. Aim**, in
one line; **3. Steps**, the method in numbered steps; **4. Programme**, the program, each step
marked by a comment; **5. Execution and Results**, what it printed when it was run, and the result
in words.
