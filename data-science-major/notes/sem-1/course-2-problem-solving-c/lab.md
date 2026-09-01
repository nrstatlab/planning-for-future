# Course 2 Lab — Problem Solving Using C

**15 experiments**

Every program is in `labs/course-2-c/` as a
compilable `.c` file. All fifteen compile under `gcc -Wall -Wextra` with no
warnings and were run against the sample inputs below.

Re-run the whole set:

```bash
bash tools/run_c_labs.sh
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

## Notes on the harder ones

### Experiment 1 — Armstrong number

An n-digit number equals the sum of its digits each raised to the power n.
153 = 1³ + 5³ + 3³. You must **count the digits first** to know the exponent —
that step is what most students miss. 1634 is a four-digit Armstrong number:
1⁴ + 6⁴ + 3⁴ + 4⁴ = 1 + 1296 + 81 + 256 = 1634.

### Experiment 5 — Swap by value and address

The most examined program in the course. Make sure your output shows all three
states — before, inside the function, after — for **both** methods. The point
is visible only in the contrast: call by value prints `10 20` after the call,
call by address prints `20 10`.

### Experiment 10 — Matrix multiplication

Three nested loops, and `c[i][j]` must be reset to 0 before the innermost loop
accumulates into it. Verify by hand on 2×2 matrices before trusting your code:

```
[1 2] × [5 6] = [1×5+2×7  1×6+2×8] = [19 22]
[3 4]   [7 8]   [3×5+4×7  3×6+4×8]   [43 50]
```

### Experiment 12 — Employee salary

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

### Experiment 14 — Reverse a file

`fseek(fp, -i, SEEK_END)` for i = 1, 2, 3… walks backwards from the end one
byte at a time. Open in binary mode (`"rb"`) so no line-ending translation
interferes.

### Experiment 15 — Book database

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
