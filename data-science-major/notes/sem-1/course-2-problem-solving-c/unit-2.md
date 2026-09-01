# Unit 2 — Control Statements

**Syllabus topics:** Decision-making statements — `if`, `if-else`, `else-if`
ladder, `switch`. Loop control statements — `while`, `for`, `do-while`. Jump
control statements — `break`, `continue`, `goto`.

---

This is the shortest unit and the easiest to score on. Almost every question is
either "write a program to…" or "what is the output of…". Both reward practice
rather than memorisation.

## 2.1 Decision making

### `if`

```c
if (marks >= 40)
    printf("Pass\n");
```

### `if-else`

```c
if (marks >= 40)
    printf("Pass\n");
else
    printf("Fail\n");
```

### `else-if` ladder

Conditions are tested top to bottom; the **first** true one runs and the rest
are skipped.

```c
if (marks >= 90)       grade = 'A';
else if (marks >= 75)  grade = 'B';
else if (marks >= 60)  grade = 'C';
else if (marks >= 40)  grade = 'D';
else                   grade = 'F';
```

Order matters. Reverse this ladder — testing `>= 40` first — and every passing
student gets a D, because the first condition is true for all of them.

### Nested `if`

```c
if (age >= 18) {
    if (has_id)
        printf("Allowed\n");
    else
        printf("ID required\n");
}
```

**The dangling else.** An `else` binds to the *nearest unmatched* `if`, not to
the one your indentation suggests:

```c
if (a > 0)
    if (b > 0)
        printf("both positive\n");
else                             /* binds to the INNER if, despite indentation */
    printf("a is not positive\n");   /* ... so this is wrong */
```

Always use braces on nested `if`s. This is a favourite "find the error"
question.

### `switch`

```c
switch (choice) {
case 1:
    printf("Addition\n");
    break;
case 2:
    printf("Subtraction\n");
    break;
default:
    printf("Invalid choice\n");
}
```

**Rules — all examinable:**

- The controlling expression must be an **integer or character** type. `float`
  and `string` will not compile.
- Each `case` label must be a **constant**, not a variable or a range.
- **`break` is essential.** Without it, control *falls through* into the next
  case and keeps going.
- `default` is optional and may appear anywhere, though convention puts it last.
- Duplicate case labels are a compile error.

**Deliberate fall-through** is occasionally useful:

```c
switch (grade) {
case 'A':
case 'B':
case 'C':
    printf("Pass\n");   /* all three land here */
    break;
case 'F':
    printf("Fail\n");
}
```

### `if-else` ladder vs `switch`

| | `if-else` ladder | `switch` |
|---|---|---|
| Condition | Any expression, including ranges | Equality against constants only |
| Data types | Any, including `float` and strings | Integer and character only |
| Speed | Tests each in turn | Can use a jump table — often faster |
| Readability | Cluttered with many branches | Cleaner for many discrete values |

Use `switch` for a menu; use a ladder for `marks >= 90`-style ranges.

## 2.2 Loops

### `while` — entry-controlled

```c
int i = 1;              /* initialise */
while (i <= 5) {        /* test BEFORE the body */
    printf("%d ", i);
    i++;                /* update -- forget this and the loop never ends */
}
```

If the condition is false at the start, the body runs **zero** times.

### `for` — entry-controlled, all three parts in one line

```c
for (int i = 1; i <= 5; i++)
    printf("%d ", i);
```

`for (initialise; condition; update)`. Any part may be left empty;
`for (;;)` is an infinite loop.

### `do-while` — exit-controlled

```c
int i = 1;
do {
    printf("%d ", i);
    i++;
} while (i <= 5);       /* the semicolon here is REQUIRED */
```

The body runs **at least once**, because the test comes after it. That is the
whole difference, and it is asked constantly.

```c
int i = 10;
while (i < 5)   { printf("while\n");    i++; }   /* prints nothing   */
do              { printf("do-while\n"); i++; } while (i < 5);  /* prints once */
```

### Comparison

| | `while` | `for` | `do-while` |
|---|---|---|---|
| Condition tested | Before body | Before body | After body |
| Minimum iterations | 0 | 0 | **1** |
| Best for | Unknown iteration count | Known iteration count | Menus, input validation |
| Semicolon after | No | No | **Yes** |

### Nested loops

```c
for (int i = 1; i <= 4; i++) {
    for (int j = 1; j <= i; j++)
        printf("* ");
    printf("\n");
}
```

Output:

```
*
* *
* * *
* * * *
```

Pattern-printing questions appear in nearly every paper. The trick is always
the same: the outer loop controls **rows**, the inner loop controls **columns**,
and the inner loop's bound usually depends on the outer variable.

## 2.3 Jump statements

### `break`

Leaves the **innermost** loop or `switch` immediately.

```c
for (int i = 1; i <= 10; i++) {
    if (i == 5) break;
    printf("%d ", i);       /* 1 2 3 4 */
}
```

In nested loops, `break` escapes only one level.

### `continue`

Skips the rest of this iteration and jumps to the next one.

```c
for (int i = 1; i <= 10; i++) {
    if (i % 2 == 0) continue;
    printf("%d ", i);       /* 1 3 5 7 9 */
}
```

**Careful in a `while` loop:** if the update statement sits after the
`continue`, it gets skipped and the loop hangs forever.

```c
int i = 0;
while (i < 10) {
    if (i == 5) continue;   /* BUG: i never increments again */
    printf("%d ", i);
    i++;
}
```

### `goto`

```c
    if (error) goto cleanup;
    /* ... */
cleanup:
    printf("Cleaning up\n");
```

`goto` jumps to a label in the same function. **Avoid it.** It destroys the
readability that structured programming exists to provide, and every `goto` can
be rewritten with loops and flags. Exams ask you to define it and then explain
why it is discouraged — the accepted answer cites Dijkstra's 1968 letter *"Go
To Statement Considered Harmful"* and the resulting "spaghetti code".

The one defensible use is jumping to a single cleanup block from deep inside
nested error handling, which is common in the Linux kernel.

### `break` vs `continue`

| | `break` | `continue` |
|---|---|---|
| Effect | Exits the loop entirely | Skips to the next iteration |
| Works in `switch` | Yes | No |
| Remaining iterations | Abandoned | Still run |

---

## Worked example — trace the output

```c
int i, j;
for (i = 1; i <= 3; i++) {
    for (j = 1; j <= 3; j++) {
        if (j == 2) continue;
        if (i == 3) break;
        printf("%d%d ", i, j);
    }
}
```

Trace it row by row:

| i | j | `j == 2`? | `i == 3`? | Action |
|---|---|---|---|---|
| 1 | 1 | no | no | print `11` |
| 1 | 2 | **yes** | — | continue |
| 1 | 3 | no | no | print `13` |
| 2 | 1 | no | no | print `21` |
| 2 | 2 | **yes** | — | continue |
| 2 | 3 | no | no | print `23` |
| 3 | 1 | no | **yes** | break inner loop |

Output: `11 13 21 23`

The `continue` at `j == 2` fires before the `i == 3` test, which is why
row 3 checks `j == 1` first and only then breaks.

---

## Exam questions from this unit

**Two marks**

1. Differentiate `while` and `do-while`.
2. What is the purpose of `break` and `continue`?
3. Why is `goto` discouraged?
4. Can `switch` be used with a floating-point expression? Explain.

**Five marks**

1. Explain the `switch` statement with syntax and an example. What happens if
   `break` is omitted?
2. Compare entry-controlled and exit-controlled loops with examples.
3. Write a program to print the Floyd's triangle pattern.

**Ten marks**

1. Explain all decision-making statements in C with syntax, flowcharts and
   examples.
2. Explain loop control statements in C, comparing all three loops.

## Mistakes that cost marks

- A stray semicolon: `if (x > 0);` — the `if` body is now empty and the block
  below it always runs
- `=` instead of `==` in a condition: `if (x = 5)` assigns 5 and is always true
- Omitting `break` in a `switch` and not realising the cases fall through
- Forgetting the semicolon after `while` in a `do-while`
- Forgetting the update statement, producing an infinite loop
- Using `continue` in a `while` loop before the increment
