# Course 3 Lab — Python Programming and Data Structures

**18 experiments**

All programs are in
`labs/course-3-python/`. Sixteen were run
under Python 3.11; the two Tkinter programs were syntax-checked only, because
`tkinter` is not installed in the verification environment and a GUI needs a
display.

```bash
bash tools/run_python_labs.sh        # re-run everything
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

## Notes on the harder ones

### Experiment 2b — Prime check

Test divisors only up to √n. If n had a factor larger than its square root, the
matching co-factor would be smaller than the square root and you would have
found it already. Write the loop as `while divisor * divisor <= n` rather than
computing a square root — it avoids floating-point comparison entirely.

Remember that 0, 1 and negative numbers are **not** prime, and 2 is the only
even prime.

### Experiment 3b — Function arguments

Demonstrate all five: required, default, keyword, `*args` and `**kwargs`. Show
that `*args` arrives as a **tuple** and `**kwargs` as a **dict** — printing
`type()` for each makes the point clearly.

### Experiment 11 — CSV processing

Use `csv.DictReader`, which keys each row by the header. Two things to
remember: pass `newline=""` when opening, and convert every value — CSV data is
always strings.

### Experiment 13 — Student class

Include the constructor `__init__`, at least one private attribute with a
getter, `__str__`, and `__del__`. That covers the whole of the syllabus's
"classes, objects, attributes, methods, constructor and destructors" in one
program.

### Experiment 15 — Stack and queue

The syllabus asks for **both** the list and the linked-list implementations.
The linked-list versions are the more instructive: a linked stack pushes and
pops at the head, both O(1); a linked queue keeps both a front and a rear
pointer so that both operations are O(1), where the list version's
`pop(0)` is O(n).

Add the balanced-bracket checker as an application — it appears in exams
regularly.

### Experiment 16 — Singly linked list

The two operations that carry the marks are **deleting the head** (you must
move `self.head`, not `previous.next`) and **reversing the list** (save
`current.next` before overwriting it, or the rest of the chain is lost).

### Experiments 17–18 — Tkinter

Both need a display, so they cannot run over SSH or in a container without X
forwarding. On Debian/Ubuntu install `python3-tk` first.

For the calculator, note the security comment in the file: `eval()` is used on
a validated character set with empty builtins. `eval()` on unfiltered user
input is a genuine vulnerability — say so if asked, because it demonstrates
judgement beyond the syllabus.

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
