# Lab — Problem Solving Using C

**15 experiments**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.

Every program is in `labs/course-2-c/` as a
compilable `.c` file. All fifteen compile under `gcc -Wall -Wextra` with no
warnings and were run against the sample inputs below. Each was run on a terminal, with its
sample input typed at its prompts, so the output under **5. Execution and Results** is what you
would see, the typed values included.

Re-run the whole set:

```bash
bash tools/data-science/run_c_labs.sh
```

Compile and run one:

```bash
gcc -Wall -Wextra -o armstrong labs/course-2-c/01_armstrong.c
./armstrong
```

---

## The experiments

| # | Experiment | File | Sample input | Key idea |
|:---:|---|---|---|---|
| 1 | Armstrong number | `01_armstrong.c` | `153` | digit extraction with `% 10` and `/ 10` |
| 2 | Sum of digits | `02_sum_of_digits.c` | `12345` | same peeling loop |
| 3 | Fibonacci series | `03_fibonacci.c` | `10` | iterative, three variables |
| 4 | Largest and smallest | `04_largest_smallest.c` | `5` then `23 7 91 4 56` | seed with `a[0]`, not 0 |
| 5 | Swap by value and address | `05_swap_value_address.c` | `10 20` | **the** parameter-passing demo |
| 6 | String operations | `06_string_operations.c` | `Hello` `World` | library and hand-written versions |
| 7 | Linear search | `07_linear_search.c` | `5`, list, `30` | return index, −1 for absent |
| 8 | Matrix addition | `08_matrix_addition.c` | `2 2` then both matrices | 2-D arrays passed to functions |
| 9 | Factorial by recursion | `09_factorial_recursive.c` | `5` | base case and recursive case |
| 10 | Matrix multiplication | `10_matrix_multiplication.c` | `2` then both matrices | three nested loops |
| 11 | Sort ascending | `11_sort_ascending.c` | `6` then the list | bubble sort with early exit |
| 12 | Employee salary | `12_employee_salary.c` | `2` then two records | structures and formatted output |
| 13 | File read/write | `13_file_read_write.c` | none | `fopen`, `fprintf`, `fgets`, `fclose` |
| 14 | Reverse a file | `14_reverse_file.c` | none | `fseek` from `SEEK_END` |
| 15 | Book database | `15_book_file_crud.c` | menu choices | full CRUD on a binary file |

---

## Experiment 1 — Armstrong number

### 1. Question

Check whether a number is an Armstrong number (here 153).

### 2. Aim

Decide whether a number equals the sum of its digits each raised to the number of digits.

### 3. Steps

1. **Count the digits.**
2. **Raise a digit to a power.**
3. **Read the number.**
4. **Add each digit raised to the number of digits.** `% 10` takes the last digit and `/ 10` drops it.
5. **Compare the sum with the number.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

An n-digit number equals the sum of its digits each raised to the power n.
153 = 1³ + 5³ + 3³. You must **count the digits first** to know the exponent —
that step is what most students miss. 1634 is a four-digit Armstrong number:
1⁴ + 6⁴ + 3⁴ + 4⁴ = 1 + 1296 + 81 + 256 = 1634.
</div>


### 4. Programme

{{programme: course-2-c/01_armstrong.c}}

### 5. Execution and Results

{{output: course-2-c/01_armstrong.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

153 = 1³ + 5³ + 3³, so 153 is an Armstrong number.
</div>


## Experiment 2 — Sum of digits

### 1. Question

Find the sum of the digits of a number (here 12345).

### 2. Aim

Add the digits of a number by peeling them off one at a time.

### 3. Steps

1. **Read the number.**
2. **Peel off each digit and add it.**
3. **Print the sum.**

### 4. Programme

{{programme: course-2-c/02_sum_of_digits.c}}

### 5. Execution and Results

{{output: course-2-c/02_sum_of_digits.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The digits of 12345 add to 15.
</div>


## Experiment 3 — Fibonacci series

### 1. Question

Print the first n terms of the Fibonacci series (here 10).

### 2. Aim

Generate the series iteratively, with three variables.

### 3. Steps

1. **Read the number of terms.**
2. **Print each term and move the pair on.** `long long` holds more terms before it overflows.

### 4. Programme

{{programme: course-2-c/03_fibonacci.c}}

### 5. Execution and Results

{{output: course-2-c/03_fibonacci.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The first ten terms are 0 1 1 2 3 5 8 13 21 34.
</div>


## Experiment 4 — Largest and smallest

### 1. Question

Find both the largest and the smallest number in a list (here 23, 7, 91, 4, 56).

### 2. Aim

Find the extremes of a list in one pass.

### 3. Steps

1. **Read the numbers.**
2. **Seed both with the first element.** Not 0, which breaks on a list of negative numbers.
3. **Compare every other element.**
4. **Print the two.**

### 4. Programme

{{programme: course-2-c/04_largest_smallest.c}}

### 5. Execution and Results

{{output: course-2-c/04_largest_smallest.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The largest is 91 and the smallest 4.
</div>


## Experiment 5 — Swap by value and address

### 1. Question

Swap two numbers using call by value and call by address (here 10 and 20).

### 2. Aim

Show that only call by address changes the caller's variables.

### 3. Steps

1. **Swap by value: the function gets copies.**
2. **Swap by address: the function gets pointers.**
3. **Read two integers.**
4. **Call by value: before, inside, after.**
5. **Call by address: before, inside, after.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

The most examined program in the course. Make sure your output shows all three
states — before, inside the function, after — for **both** methods. The point
is visible only in the contrast: call by value prints `10 20` after the call,
call by address prints `20 10`.
</div>


### 4. Programme

{{programme: course-2-c/05_swap_value_address.c}}

### 5. Execution and Results

{{output: course-2-c/05_swap_value_address.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Both functions swap their own copies, but only call by address changes `x` and `y`: after it they are 20 and 10, while after call by value they are still 10 and 20.
</div>


## Experiment 6 — String operations

### 1. Question

Perform the string operations — length, compare, copy, concatenate, reverse — with the library functions and with functions of your own (here on Hello and World).

### 2. Aim

Use the string library, and write its functions by hand.

### 3. Steps

1. **Hand-written strlen and strcpy.**
2. **Hand-written strcmp and reverse.**
3. **Read two strings.**
4. **The library functions.**
5. **The hand-written versions.**

### 4. Programme

{{programme: course-2-c/06_string_operations.c}}

### 5. Execution and Results

{{output: course-2-c/06_string_operations.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Both versions agree: the length of Hello is 5, and Hello compares below World (−15, the difference of H and W). The copy is Hello, reversed olleH, and the two joined HelloWorld.
</div>


## Experiment 7 — Linear search

### 1. Question

Search a list for an element by linear search (here 30 in 10, 20, 30, 40, 50).

### 2. Aim

Find an element's position, or report that it is absent.

### 3. Steps

1. **Search, returning the index or -1.**
2. **Read the list and the key.**
3. **Search, and report the position.**

### 4. Programme

{{programme: course-2-c/07_linear_search.c}}

### 5. Execution and Results

{{output: course-2-c/07_linear_search.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

30 is at position 3 (index 2).
</div>


## Experiment 8 — Matrix addition

### 1. Question

Use functions to add two matrices (here two 2 × 2 matrices).

### 2. Aim

Pass 2-D arrays to functions to read, add and print them.

### 3. Steps

1. **Read a matrix.**
2. **Add two matrices.**
3. **Print a matrix.**
4. **Read the order and both matrices.**
5. **Add them, and print the sum.**

### 4. Programme

{{programme: course-2-c/08_matrix_addition.c}}

### 5. Execution and Results

{{output: course-2-c/08_matrix_addition.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A + B = [6 8; 10 12].
</div>


## Experiment 9 — Factorial by recursion

### 1. Question

Find the factorial of a number using recursion (here 5).

### 2. Aim

Compute n! recursively, refusing the inputs it cannot handle.

### 3. Steps

1. **The recursive function: a base case and a recursive case.**
2. **Read n, refusing a negative or an overflow.** 21! does not fit in 64 bits.
3. **Print n!.**

### 4. Programme

{{programme: course-2-c/09_factorial_recursive.c}}

### 5. Execution and Results

{{output: course-2-c/09_factorial_recursive.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

5! = 120.
</div>


## Experiment 10 — Matrix multiplication

### 1. Question

Multiply two square matrices (here two 2 × 2 matrices).

### 2. Aim

Multiply matrices with three nested loops.

### 3. Steps

1. **Multiply: reset each cell, then accumulate.**
2. **Read the order and both matrices.**
3. **Multiply them, and print the product.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

Three nested loops, and `c[i][j]` must be reset to 0 before the innermost loop
accumulates into it. Verify by hand on 2×2 matrices before trusting your code:

```
[1 2] × [5 6] = [1×5+2×7  1×6+2×8] = [19 22]
[3 4]   [7 8]   [3×5+4×7  3×6+4×8]   [43 50]
```
</div>


### 4. Programme

{{programme: course-2-c/10_matrix_multiplication.c}}

### 5. Execution and Results

{{output: course-2-c/10_matrix_multiplication.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A × B = [19 22; 43 50], as worked by hand.
</div>


## Experiment 11 — Sort ascending

### 1. Question

Sort a list in ascending order (here 64, 34, 25, 12, 22, 11).

### 2. Aim

Sort by bubble sort, stopping as soon as a pass makes no swap.

### 3. Steps

1. **Bubble sort, with an early exit.**
2. **Read the list.**
3. **Sort it, and print it.**

### 4. Programme

{{programme: course-2-c/11_sort_ascending.c}}

### 5. Execution and Results

{{output: course-2-c/11_sort_ascending.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The sorted list is 11 12 22 25 34 64.
</div>


## Experiment 12 — Employee salary

### 1. Question

Using a structure, compute the gross and net salary of employees from their basic pay.

### 2. Aim

Hold each employee's record in a structure, and compute the pay by the syllabus rules.

### 3. Steps

1. **The employee structure.**
2. **The salary rules, in order.**
3. **Read each employee and compute the pay.**
4. **Print the table.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

The rules from the syllabus, in order — each depends on the one before:

```
DA        = 30% of Basic Pay
HRA       = 15% of Basic Pay
Deduction = 10% of (Basic Pay + DA)      <- includes DA, not just basic
Gross     = Basic Pay + DA + HRA
Net       = Gross − Deduction
```

For a basic pay of 50,000: DA = 15,000, HRA = 7,500,
Deduction = 10% of 65,000 = 6,500, Gross = 72,500, Net = 66,000.
</div>


### 4. Programme

{{programme: course-2-c/12_employee_salary.c}}

### 5. Execution and Results

{{output: course-2-c/12_employee_salary.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Alice's basic pay of 50,000 gives a gross of 72,500 and a net of 66,000; Bob's 20,000 gives 29,000 and 26,400.
</div>


## Experiment 13 — File read/write

### 1. Question

Write text to a file and read it back.

### 2. Aim

Open, write, close, reopen and read a text file.

### 3. Steps

1. **Write three lines.**
2. **Read them back.**

### 4. Programme

{{programme: course-2-c/13_file_read_write.c}}

### 5. Execution and Results

{{output: course-2-c/13_file_read_write.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The three lines written to `sample.txt` are read back unchanged.
</div>


## Experiment 14 — Reverse a file

### 1. Question

Copy the contents of a file into another in reverse order.

### 2. Aim

Read a file backwards with `fseek`, and write what it reads.

### 3. Steps

1. **Create the input file.**
2. **Copy it backwards, one byte at a time from the end.**
3. **Show both files.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

`fseek(fp, -i, SEEK_END)` for i = 1, 2, 3… walks backwards from the end one
byte at a time. Open in binary mode (`"rb"`) so no line-ending translation
interferes.
</div>


### 4. Programme

{{programme: course-2-c/14_reverse_file.c}}

### 5. Execution and Results

{{output: course-2-c/14_reverse_file.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

ABCDEFG is written out as GFEDCBA.
</div>


## Experiment 15 — Book database

### 1. Question

Create a Book structure (ISBN, Title, Author, Price, Pages, Publisher), store book details in a file, and add, search, update and delete books by ISBN.

### 2. Aim

Keep records in a binary file, and carry out all four operations on it.

### 3. Steps

1. **The book record.**
2. **Print a book.**
3. **Add: append a record.**
4. **Search by ISBN.**
5. **Update: overwrite the record in place.**
6. **Delete: copy the rest to a temporary file.**
7. **Display all.**
8. **The menu.**

<div class="formula" markdown="1">
<span class="label">THE METHOD</span>

The largest program in the list. Four operations on a binary file of `struct
Book` records:

- **Add** — `fopen` in `"ab"` (append binary), then `fwrite`
- **Search** — `fread` in a loop until the ISBN matches
- **Update** — `fopen` in `"rb+"`, `fread` until found, then
  `fseek(fp, -sizeof(b), SEEK_CUR)` to step back over the record just read, and
  `fwrite` over it
- **Delete** — copy every record except the target into a temporary file, then
  `remove()` the original and `rename()` the temporary

That last technique is the one to remember: **you cannot delete bytes from the
middle of a file.** Rewriting to a temporary file is the standard answer.
</div>


### 4. Programme

{{programme: course-2-c/15_book_file_crud.c}}

### 5. Execution and Results

{{output: course-2-c/15_book_file_crud.c}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Two books are added, book 111 is found and its price updated to 600.00, book 222 is deleted, and the file then holds one book.
</div>


---

## Lab exam tips

1. **Write the program on paper first.** Terminals are scarce and time is short.
2. **Compile early and often.** One error at a time is manageable; twenty is not.
3. **Read the error message.** "Expected `;` before `int`" means the missing
   semicolon is on the line *above* the one named.
4. **Test edge cases** before the examiner does: n = 0, an empty array, a
   negative number, a file that does not exist.
5. **Print prompts.** `printf("Enter n: ")` before every `scanf`. Marks are given
   for a usable interface.
6. **Comment the logic**, not the syntax. `/* peel off the last digit */` is
   useful; `/* increment i */` is not.
7. **Expect a viva.** Be ready for "why did you use a `while` here?" and "what
   happens if I enter 0?"

## What the practical record should contain

For each experiment, the five parts set out above: **1. Question**, the task as set; **2. Aim**, in
one line; **3. Steps**, the method in numbered steps; **4. Programme**, the program, each step
marked by a comment; **5. Execution and Results**, what it printed for the sample input, and the
result in words.
