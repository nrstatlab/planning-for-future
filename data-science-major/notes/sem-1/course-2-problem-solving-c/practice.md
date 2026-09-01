# Course 2 — Practice Questions with Solutions

Work each one before reading the solution. Copying answers teaches nothing;
getting them wrong and finding out why is the whole point.

---

## Section A — Trace the output

### Q1

```c
int i = 5;
printf("%d %d %d", i++, ++i, i++);
```

**Answer: undefined behaviour.** Modifying `i` more than once between sequence
points has no defined result — different compilers print different things, and
so does the same compiler at different optimisation levels.

If an exam asks this expecting a specific answer, the expected answer is
usually `5 7 7` (arguments evaluated right to left, as many compilers do). Give
that, then add one line: *"this is undefined behaviour; the standard does not
specify the order of evaluation."* That sentence is what distinguishes a strong
answer.

### Q2

```c
int a[5] = {1, 2, 3, 4, 5};
int *p = a;
printf("%d %d %d", *p, *(p + 2), *p + 2);
```

**Answer: `1 3 3`**

- `*p` → the value at `a[0]` → `1`
- `*(p + 2)` → the value at `a[2]` → `3`
- `*p + 2` → `(*p) + 2` → `1 + 2` → `3`

The last two look alike and mean different things: brackets change what is
dereferenced. Dereferencing binds tighter than addition.

### Q3

```c
void counter(void) {
    static int c = 0;
    int d = 0;
    c++; d++;
    printf("%d %d | ", c, d);
}
/* called three times */
```

**Answer: `1 1 | 2 1 | 3 1 |`**

`c` is `static`, so it is initialised once and survives between calls. `d` is a
plain local, recreated and reset to 0 every time.

### Q4

```c
int x = 10;
if (x = 5)
    printf("Five");
else
    printf("Not five");
```

**Answer: `Five`**

`x = 5` is an *assignment*, not a comparison. It stores 5 in `x` and the
expression evaluates to 5, which is non-zero and therefore true. `if (x == 5)`
was intended. Compiling with `-Wall` warns about this.

### Q5

```c
char s[] = "Hello";
printf("%d %d", strlen(s), sizeof(s));
```

**Answer: `5 6`**

`strlen` counts characters up to but not including `'\0'` → 5. `sizeof` counts
allocated bytes, which includes the terminator → 6.

### Q6

```c
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) break;
        printf("%d%d ", i, j);
    }
}
```

**Answer: `00 10 20`**

The inner loop breaks as soon as `j == 1`, so only `j == 0` ever prints. `break`
leaves only the inner loop; the outer one continues.

---

## Section B — Find and fix the error

### Q7

```c
int main() {
    int n;
    printf("Enter n: ");
    scanf("%d", n);
    printf("%d", n);
}
```

**Error:** `scanf` is missing `&`. It needs the *address* to write into.

**Fix:** `scanf("%d", &n);`

### Q8

```c
int *p;
*p = 10;
printf("%d", *p);
```

**Error:** `p` was never initialised, so it holds garbage. Writing through it
corrupts whatever memory that address names.

**Fix:**

```c
int x;
int *p = &x;
*p = 10;
```

or allocate: `int *p = malloc(sizeof(int)); if (p) *p = 10; ... free(p);`

### Q9

```c
struct Student {
    int roll;
    char name[50];
}
int main() { ... }
```

**Error:** missing semicolon after the closing brace of the structure
definition. The error message points at `int main`, which is confusing — when
the compiler complains about a line that looks fine, check the line above.

**Fix:** `};`

### Q10

```c
char str1[10] = "Hello", str2[10] = "Hello";
if (str1 == str2)
    printf("Equal");
```

**Error:** `==` compares the two *addresses*, which are different. It never
prints "Equal".

**Fix:** `if (strcmp(str1, str2) == 0)`

### Q11

```c
int *p = malloc(5 * sizeof(int));
p[0] = 10;
free(p);
printf("%d", p[0]);
```

**Error:** using `p` after `free` — a dangling pointer. It may print 10, may
print garbage, may crash.

**Fix:** print before freeing, and set `p = NULL;` after `free(p);`

---

## Section C — Write the program

### Q12 — Check whether a string is a palindrome

```c
#include <stdio.h>
#include <string.h>

int is_palindrome(const char *s)
{
    int i = 0, j = strlen(s) - 1;
    while (i < j) {
        if (s[i] != s[j])
            return 0;
        i++;
        j--;
    }
    return 1;
}

int main(void)
{
    char s[100];
    printf("Enter a string: ");
    scanf("%99s", s);
    printf("%s is %sa palindrome\n", s, is_palindrome(s) ? "" : "not ");
    return 0;
}
```

Two pointers walking inwards from both ends. O(n) time, O(1) extra space — say
so if the question asks for complexity.

### Q13 — Reverse an array in place

```c
void reverse(int a[], int n)
{
    int i = 0, j = n - 1, temp;
    while (i < j) {
        temp = a[i];
        a[i] = a[j];
        a[j] = temp;
        i++;
        j--;
    }
}
```

Same two-pointer idea. Looping all the way to `n-1` instead of stopping at the
middle would reverse it and then reverse it back.

### Q14 — Count vowels, consonants, digits and spaces

```c
#include <stdio.h>
#include <ctype.h>

int main(void)
{
    char s[200];
    int v = 0, c = 0, d = 0, sp = 0;

    printf("Enter a line: ");
    fgets(s, sizeof(s), stdin);

    for (int i = 0; s[i] != '\0'; i++) {
        char ch = tolower(s[i]);
        if (isalpha(ch)) {
            if (ch=='a'||ch=='e'||ch=='i'||ch=='o'||ch=='u') v++;
            else c++;
        }
        else if (isdigit(ch)) d++;
        else if (ch == ' ') sp++;
    }

    printf("Vowels %d, Consonants %d, Digits %d, Spaces %d\n", v, c, d, sp);
    return 0;
}
```

`fgets` rather than `scanf("%s")`, because the input has spaces in it.

### Q15 — Sum of digits, recursively

```c
int sum_of_digits(int n)
{
    if (n == 0)                              /* base case */
        return 0;
    return (n % 10) + sum_of_digits(n / 10); /* last digit + the rest */
}
```

Trace `sum_of_digits(123)`:

```
= 3 + sum_of_digits(12)
= 3 + (2 + sum_of_digits(1))
= 3 + (2 + (1 + sum_of_digits(0)))
= 3 + (2 + (1 + 0)) = 6
```

### Q16 — Second largest element of an array

```c
int second_largest(const int a[], int n)
{
    int largest = a[0], second = -2147483647;

    for (int i = 1; i < n; i++) {
        if (a[i] > largest) {
            second = largest;      /* the old champion is demoted */
            largest = a[i];
        }
        else if (a[i] > second && a[i] != largest) {
            second = a[i];
        }
    }
    return second;
}
```

One pass, O(n). Sorting first would work but costs O(n log n) — mention the
difference if asked. The `a[i] != largest` guard handles duplicated maxima.

---

## Section D — Long answers

### Q17 — Compare call by value and call by address

Structure your answer as: definition of each → syntax → a swap program for each
→ the comparison table → a conclusion.

See [unit-4.md §4.3](unit-4.md) for the full treatment and
`05_swap_value_address.c`
for runnable code.

The mark scheme almost always wants: both programs written out, the *output* of
each shown, and an explicit statement that call by value cannot modify the
caller's variables.

### Q18 — Explain the four storage classes

Draw the four-row table (scope, lifetime, default value, storage location),
then give a short example of each. The `static` counter example is the one that
demonstrates understanding rather than memorisation:

```c
void f(void) { static int c = 0; printf("%d ", ++c); }
/* three calls print 1 2 3, not 1 1 1 */
```

### Q19 — Explain structures vs unions with a memory diagram

```c
struct S { int i; char c; float f; };   /* ~12 bytes, all members valid */
union  U { int i; char c; float f; };   /*  4 bytes, one member valid   */
```

```
struct S in memory:          union U in memory:
+------+---+---+------+      +------+
|  i   | c |pad|  f   |      | i/c/f|    all three share these 4 bytes
+------+---+---+------+      +------+
 4 B    1B  3B  4 B           4 B
```

Say explicitly: **writing to one union member destroys the others**. Then give
the memory-saving use case.

---

## Quick self-test

Ten minutes, no notes. If you cannot answer these, re-read the unit named.

1. What does `sizeof(int)` return, and why is the answer not fixed? *(Unit 1)*
2. Write the syntax of a `do-while` loop, including the semicolon. *(Unit 2)*
3. Give the address of `a[2][3]` for `int a[4][5]` based at 1000. *(Unit 3)*
4. What does `p + 1` mean when `p` is `int *` pointing at 2000? *(Unit 4)*
5. Which storage class keeps its value between function calls? *(Unit 4)*
6. What is the difference between `"w"` and `"a"` file modes? *(Unit 5)*
7. How large is `union U { int i; double d; char s[10]; };`? *(Unit 5)*
8. Why must every recursive function have a base case? *(Unit 4)*

**Answers:** 1. Typically 4 bytes; implementation-defined. · 2. `do { ... } while (cond);`
· 3. 1000 + ((2×5)+3)×4 = 1052. · 4. Address 2004 — it advances by `sizeof(int)`.
· 5. `static`. · 6. `"w"` truncates the file; `"a"` appends to it. · 7. 16 bytes
— the largest member is `double` (8) but alignment rounds `char[10]` up, so the
union is the size of its largest member rounded to its alignment; on most
systems, 16. · 8. Without one the recursion never terminates and the stack
overflows.
