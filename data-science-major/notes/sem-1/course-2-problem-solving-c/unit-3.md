# Unit 3 — Derived Data Types: Arrays and Strings

**Syllabus topics:** Arrays — one-dimensional: declaration, initialization
and memory representation; two-dimensional: declaration, initialization and
memory representation. Strings — declaring and initializing string variables;
string handling functions; character handling functions.

---

## 3.1 One-dimensional arrays

An array is a collection of elements **of the same type**, stored in
**contiguous memory**, accessed by an index.

```c
int marks[5];                          /* declaration -- 5 ints, uninitialised */
int marks[5] = {85, 72, 90, 64, 78};   /* declaration with initialisation      */
int marks[]  = {85, 72, 90, 64, 78};   /* size inferred as 5                   */
int marks[5] = {85, 72};               /* rest filled with 0: {85,72,0,0,0}    */
int marks[5] = {0};                    /* all five set to 0                    */
```

**Indices start at 0.** An array of size 5 has valid indices 0 to 4. `marks[5]`
is out of bounds.

### Memory representation

For `int marks[5]` starting at address 1000, with a 4-byte `int`:

| Element | `marks[0]` | `marks[1]` | `marks[2]` | `marks[3]` | `marks[4]` |
|---|---|---|---|---|---|
| Address | 1000 | 1004 | 1008 | 1012 | 1016 |
| Value | 85 | 72 | 90 | 64 | 78 |

The address of element `i` is:

```
base_address + (i × sizeof(element_type))
```

So `marks[3]` sits at 1000 + 3 × 4 = 1012. Exam questions give you a base
address and a type and ask for a particular element's address — apply the
formula directly.

**Total memory** = number of elements × size of each = 5 × 4 = 20 bytes.

### C does not check bounds

```c
int a[5] = {1, 2, 3, 4, 5};
printf("%d", a[10]);     /* compiles, runs, prints garbage or crashes */
```

There is no error. C trusts you. Reading out of bounds gives whatever happens
to be in that memory; writing out of bounds corrupts it. This is the single
biggest source of bugs in C, and the reason languages like Python check every
index.

### Traversing

```c
int marks[5] = {85, 72, 90, 64, 78};
int i, sum = 0;

for (i = 0; i < 5; i++)          /* note: i < 5, not i <= 5 */
    sum += marks[i];

printf("Sum = %d, Average = %.2f\n", sum, sum / 5.0);
```

Writing `i <= 5` reads one element past the end. It is the most common array
bug there is.

## 3.2 Two-dimensional arrays

```c
int matrix[3][4];                    /* 3 rows, 4 columns */

int m[2][3] = { {1, 2, 3}, {4, 5, 6} };     /* clearest form */
int m[2][3] = {1, 2, 3, 4, 5, 6};           /* same thing, filled row by row */
int m[][3]  = { {1, 2, 3}, {4, 5, 6} };     /* rows inferred; columns REQUIRED */
```

The number of **columns can never be omitted** — the compiler needs it to
compute addresses.

### Memory representation — row-major order

C stores 2-D arrays **row by row** (row-major). For `int m[2][3]` at address
2000 with 4-byte ints:

| | col 0 | col 1 | col 2 |
|---|---|---|---|
| **row 0** | 2000 | 2004 | 2008 |
| **row 1** | 2012 | 2016 | 2020 |

The whole row 0 is laid down before row 1 begins. The address of `m[i][j]`:

```
base + ((i × number_of_columns) + j) × sizeof(type)
```

For `m[1][2]`: 2000 + ((1 × 3) + 2) × 4 = 2000 + 20 = 2020. ✓

**Why it matters:** looping row-first is faster than column-first, because
consecutive reads land in adjacent memory and the CPU cache fetches them
together. That is a real performance effect you will meet again in NumPy.

(FORTRAN uses column-major, which is why NumPy has an `order='F'` option. Not
examinable, but it explains the flag.)

### Matrix operations

```c
/* Addition -- element by element, same dimensions required */
for (i = 0; i < rows; i++)
    for (j = 0; j < cols; j++)
        sum[i][j] = a[i][j] + b[i][j];

/* Multiplication -- three nested loops */
for (i = 0; i < n; i++)
    for (j = 0; j < n; j++) {
        c[i][j] = 0;                    /* reset before accumulating */
        for (k = 0; k < n; k++)
            c[i][j] += a[i][k] * b[k][j];
    }

/* Transpose */
for (i = 0; i < rows; i++)
    for (j = 0; j < cols; j++)
        t[j][i] = a[i][j];
```

For multiplication, A(m×n) × B(n×p) = C(m×p): the **columns of A must equal the
rows of B**. Forgetting to reset `c[i][j] = 0` before the `k` loop leaves
garbage in the accumulator — a classic bug.

## 3.3 Strings

A string in C is a **character array terminated by the null character `'\0'`**.
There is no string type.

```c
char name[10] = "Ravi";
char name[10] = {'R', 'a', 'v', 'i', '\0'};   /* identical */
char name[]   = "Ravi";                        /* size 5: 4 letters + '\0' */
```

**Always leave room for the terminator.** `char name[4] = "Ravi";` has no space
for `'\0'`, so every string function will read past the end looking for one.

```
 R    a    v    i   '\0'
[0]  [1]  [2]  [3]  [4]     <- length 4, but 5 bytes of storage
```

### Reading strings

```c
char name[50];

scanf("%s", name);              /* stops at the first whitespace: "Ravi Kumar"
                                   gives just "Ravi". No & -- an array name is
                                   already an address. */

scanf("%49s", name);            /* better: limits the length */

fgets(name, sizeof(name), stdin);   /* reads the whole line INCLUDING '\n' */

gets(name);                     /* NEVER. Removed from the C standard. */
```

`gets()` cannot know the size of its buffer, so any long input overwrites
memory past the array. Use `fgets`.

### String handling functions — `<string.h>`

| Function | Purpose | Example |
|---|---|---|
| `strlen(s)` | Length, **excluding** `'\0'` | `strlen("Ravi")` → 4 |
| `strcpy(dest, src)` | Copy src into dest | `strcpy(a, "Hello")` |
| `strncpy(dest, src, n)` | Copy at most n characters | safer |
| `strcat(dest, src)` | Append src to dest | `"Hello" + "World"` |
| `strncat(dest, src, n)` | Append at most n | safer |
| `strcmp(s1, s2)` | Compare | 0 if equal, <0 if s1<s2, >0 if s1>s2 |
| `strncmp(s1, s2, n)` | Compare first n characters | |
| `strrev(s)` | Reverse — **not standard**, Turbo C only | |
| `strlwr(s)` / `strupr(s)` | Case conversion — also non-standard | |
| `strstr(s1, s2)` | Find s2 inside s1 | returns a pointer or NULL |
| `strchr(s, c)` | Find character c in s | returns a pointer or NULL |
| `strtok(s, delim)` | Split into tokens | |

**`strcmp` returns 0 when the strings are EQUAL.** That inverted logic catches
everyone:

```c
if (strcmp(a, b) == 0)      /* correct: the strings match */
if (strcmp(a, b))           /* true when they DIFFER */
if (a == b)                 /* WRONG: compares addresses, not contents */
```

**`strlen` vs `sizeof`:**

```c
char s[50] = "Ravi";
strlen(s)     /* 4  -- characters up to '\0'      */
sizeof(s)     /* 50 -- bytes allocated to the array */
```

### Character handling functions — `<ctype.h>`

| Function | Returns true when |
|---|---|
| `isalpha(c)` | c is a letter |
| `isdigit(c)` | c is a digit |
| `isalnum(c)` | c is a letter or digit |
| `isspace(c)` | c is a space, tab or newline |
| `isupper(c)` / `islower(c)` | c is upper/lower case |
| `ispunct(c)` | c is punctuation |
| `toupper(c)` / `tolower(c)` | *converts* and returns the character |

`toupper` and `tolower` return the converted character — they do not modify in
place:

```c
c = toupper(c);       /* correct  */
toupper(c);           /* does nothing useful */
```

### Implementing them yourself

Exams frequently ask you to write `strlen` or `strcpy` without the library.

```c
int my_strlen(const char *s)
{
    int len = 0;
    while (s[len] != '\0')     /* walk until the terminator */
        len++;
    return len;
}

void my_strcpy(char *dest, const char *src)
{
    int i = 0;
    while (src[i] != '\0') {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';            /* do not forget the terminator */
}

int my_strcmp(const char *a, const char *b)
{
    int i = 0;
    while (a[i] != '\0' && a[i] == b[i])
        i++;
    return a[i] - b[i];        /* 0 when both hit '\0' together */
}
```

Working versions of all of these are in
`labs/course-2-c/06_string_operations.c`.

---

## Exam questions from this unit

**Two marks**

1. How is a string terminated in C?
2. Difference between `strlen()` and `sizeof()` for a character array.
3. What does `strcmp()` return?
4. Why must the column size be specified in a 2-D array declaration?

**Five marks**

1. Explain the memory representation of a one-dimensional array with an example.
2. Explain row-major order and calculate the address of `a[2][3]` given a base
   address of 1000 for `int a[4][5]`.
3. Explain any five string handling functions with examples.
4. Write a program to find the largest and smallest elements of an array.

**Ten marks**

1. Explain 1-D and 2-D arrays with declaration, initialization and memory
   representation.
2. Write a program to multiply two matrices and explain the logic.

## Mistakes that cost marks

- Looping `i <= n` instead of `i < n` — reads one element past the end
- Forgetting `'\0'` when building a string by hand
- Using `==` to compare strings instead of `strcmp`
- Declaring `char name[4]` for `"Ravi"` — no room for the terminator
- Omitting the column size in a 2-D array declaration
- Forgetting to zero `c[i][j]` before accumulating in matrix multiplication
- Using `strrev`, `strlwr` or `strupr` and finding they do not exist in GCC —
  they are Turbo C extensions, not standard C
