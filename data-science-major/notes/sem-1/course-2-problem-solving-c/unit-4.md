# Unit 4 — Pointers, Functions and Storage Classes

**Syllabus topics:** Unit 4 is titled **"Functions"**, but the printed topic
list opens with pointers:

> Pointers: Pointer data type, pointer declaration, initialization, accessing
> values using pointers. Pointer arithmetic, pointers and arrays. Function
> prototype, definition and calling. Return statement. Nesting of functions.
> Categories of functions. Recursion (basic concept only). Parameter passing by
> address & by value. Local and global variables. Storage classes: automatic,
> external, static and register.

The title does not match the content — see
[`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D5**. If you
revise "functions" from the unit title alone you will be unprepared for the
pointer questions, which carry the heavier marks.

**This is the hardest unit in the course.** Budget extra time.

---

## 4.1 Pointers

Every variable lives at an **address** in memory. A **pointer** is a variable
whose value is such an address.

```c
int x = 10;
int *p;        /* p is a pointer to int -- it can hold the address of an int */
p = &x;        /* & is the "address of" operator */

printf("%d",  x);    /* 10        -- the value                */
printf("%p", (void *) &x);   /* 0x7ffd... -- the address      */
printf("%p", (void *) p);    /* the same address              */
printf("%d", *p);    /* 10        -- * dereferences: "value at" */
```

Two operators, and keeping them straight is most of the battle:

| Operator | Name | Meaning |
|---|---|---|
| `&` | address-of | "where does this variable live?" |
| `*` | dereference / indirection | "what value is at this address?" |

They are inverses: `*(&x)` is `x`.

### A diagram is worth more than the syntax

```
   x                        p
+------+                +----------+
|  10  |  <-----------  |   1000   |
+------+                +----------+
addr 1000                addr 2000

  *p  reads the value at address 1000  ->  10
  &x  is the address 1000
   p  holds 1000
  &p  is 2000
```

**Draw this for every pointer question.** Pointer bugs are obvious in a diagram
and invisible in code.

### Modifying through a pointer

```c
int x = 10;
int *p = &x;
*p = 25;              /* writes THROUGH the pointer */
printf("%d", x);      /* 25 -- x itself changed */
```

This is why pointers matter: they let a function reach out and change something
the caller owns.

### The null pointer

```c
int *p = NULL;        /* points to nothing, deliberately */
if (p != NULL)        /* always check before dereferencing */
    printf("%d", *p);
```

Dereferencing `NULL` crashes the program (a segmentation fault). Dereferencing
an **uninitialised** pointer is worse — it may not crash, and instead silently
corrupts whatever memory it happens to address.

```c
int *p;               /* DANGER: p holds garbage */
*p = 10;              /* writes 10 somewhere random */
```

Always initialise a pointer, to a real address or to `NULL`.

### Pointer arithmetic

Pointer arithmetic is scaled by the size of the pointed-to type.

```c
int a[5] = {10, 20, 30, 40, 50};
int *p = a;           /* an array name is the address of its first element */

printf("%d", *p);        /* 10 */
printf("%d", *(p + 1));  /* 20 -- p+1 advances by sizeof(int), not 1 byte */
printf("%d", *(p + 3));  /* 40 */
p++;                     /* now points at a[1] */
```

If `p` holds address 1000 and `int` is 4 bytes, `p + 1` is **1004**, not 1001.

| Operation | Allowed? | Result |
|---|---|---|
| `p + n`, `p - n` | Yes | address ± n × sizeof(type) |
| `p++`, `p--` | Yes | move one element |
| `p1 - p2` | Yes | number of *elements* between them |
| `p1 + p2` | **No** | adding two addresses is meaningless |
| `p * 2`, `p / 2` | **No** | |
| `p1 == p2`, `p1 < p2` | Yes | comparison is fine |

### Pointers and arrays

The array/pointer relationship is the source of most exam questions here.

```c
int a[5] = {10, 20, 30, 40, 50};

a          /* equivalent to &a[0] */
a[i]       /* equivalent to *(a + i) */
&a[i]      /* equivalent to (a + i) */
```

All four of these print the same thing:

```c
printf("%d", a[2]);
printf("%d", *(a + 2));
printf("%d", p[2]);       /* where p = a */
printf("%d", *(p + 2));
```

**But an array is not a pointer.** The differences are examinable:

| | Array | Pointer |
|---|---|---|
| Memory | The elements themselves | One address |
| `sizeof` | Total bytes of all elements | Size of one address (8 bytes) |
| Reassignment | `a = something;` is illegal | `p = something;` is fine |
| Allocation | At declaration | Points wherever you aim it |

```c
int a[5];
int *p = a;
sizeof(a)    /* 20 -- 5 ints */
sizeof(p)    /* 8  -- one address on a 64-bit machine */
```

That `sizeof` difference is why passing an array to a function loses its size —
the parameter is a pointer, and the function must be told the length separately.

## 4.2 Functions

### Prototype, definition, call

```c
int add(int a, int b);        /* 1. PROTOTYPE -- declares the signature */

int main(void)
{
    int result = add(5, 3);   /* 3. CALL */
    printf("%d\n", result);
    return 0;
}

int add(int a, int b)         /* 2. DEFINITION -- the body */
{
    return a + b;
}
```

The prototype tells the compiler the return type and parameter types before it
meets the call. Without it, the compiler assumes `int` and cannot check your
arguments.

**Terminology that gets asked:** the names in the *definition* are **formal
parameters**; the values in the *call* are **actual arguments**.

### The `return` statement

- Sends a value back and **exits the function immediately**
- A function may have several `return`s; the first one reached wins
- `void` functions use a bare `return;` or none at all
- Only **one value** can be returned. To return several, use a structure or
  pass pointers to output variables.

### Categories of functions

Four combinations, and exams ask you to name and illustrate all of them:

| Category | Example |
|---|---|
| No arguments, no return value | `void greet(void)` |
| No arguments, with return value | `int getChoice(void)` |
| With arguments, no return value | `void display(int n)` |
| With arguments, with return value | `int add(int a, int b)` |

### Nesting of functions

C allows a function to **call** another function (which the syllabus calls
nesting):

```c
void inner(void) { printf("inner\n"); }
void outer(void) { inner(); }
```

C does **not** allow a function to be **defined inside** another function.
Unlike Python, `main()` cannot contain a nested definition. (GCC offers this as
a non-standard extension — do not rely on it.)

### Recursion

A function that calls itself. Every recursive function needs:

1. A **base case** that returns without recursing — otherwise it never stops
2. A **recursive case** that moves towards the base case

```c
unsigned long long factorial(int n)
{
    if (n == 0 || n == 1)             /* BASE CASE */
        return 1;
    return n * factorial(n - 1);      /* RECURSIVE CASE */
}
```

**Trace `factorial(4)`** — exams ask for exactly this:

```
factorial(4) = 4 * factorial(3)
                   factorial(3) = 3 * factorial(2)
                                      factorial(2) = 2 * factorial(1)
                                                          factorial(1) = 1   <- base
                                      factorial(2) = 2 * 1 = 2
                   factorial(3) = 3 * 2 = 6
factorial(4) = 4 * 6 = 24
```

Each call gets its own copy of `n` on the **stack**. Too many nested calls
exhausts the stack — a **stack overflow**. `factorial(-1)` recurses forever,
because the base case is never reached.

| | Recursion | Iteration |
|---|---|---|
| Readability | Closer to the mathematical definition | More verbose |
| Memory | A stack frame per call | Constant |
| Speed | Slower — call overhead | Faster |
| Risk | Stack overflow | Infinite loop |

## 4.3 Parameter passing — the exam's favourite topic

### Call by value

A **copy** of the argument is passed. The function cannot touch the original.

```c
void swap(int a, int b)
{
    int t = a; a = b; b = t;
}

int x = 10, y = 20;
swap(x, y);
printf("%d %d", x, y);    /* STILL 10 20 -- only the copies were swapped */
```

### Call by address (call by reference)

The **address** is passed, so the function reaches the original.

```c
void swap(int *a, int *b)
{
    int t = *a; *a = *b; *b = t;
}

int x = 10, y = 20;
swap(&x, &y);
printf("%d %d", x, y);    /* 20 10 -- genuinely swapped */
```

| | Call by value | Call by address |
|---|---|---|
| What is passed | A copy of the value | The address |
| Original affected? | No | Yes |
| Memory | Extra copy | Just an address |
| Syntax at the call | `swap(x, y)` | `swap(&x, &y)` |
| Syntax in the function | `int a` | `int *a` |

**Strictly, C has only call by value** — passing `&x` passes a *copy of the
address*. The effect is call by reference, which is what the syllabus and the
textbooks call it. Say "call by address" and you are safe either way.

**Arrays are always effectively passed by address.** The array name decays to a
pointer, so a function can modify the caller's array without any `&`:

```c
void doubleAll(int a[], int n)     /* identical to int *a */
{
    for (int i = 0; i < n; i++)
        a[i] *= 2;                 /* the CALLER's array changes */
}
```

Working demonstration:
`labs/course-2-c/05_swap_value_address.c`.

## 4.4 Local and global variables

```c
int count = 0;              /* GLOBAL -- visible to every function */

void increment(void)
{
    int temp = 5;           /* LOCAL -- exists only inside increment() */
    count++;                /* the global is reachable here */
}
```

| | Local | Global |
|---|---|---|
| Declared | Inside a function or block | Outside all functions |
| Scope | That function/block only | The whole file (and beyond, with `extern`) |
| Lifetime | Until the function returns | The whole program run |
| Default value | **Garbage** | **Zero** |
| Stored in | Stack | Data segment |

**Prefer locals.** A global can be changed from anywhere, which makes bugs
untraceable. Globals are shown here because they are examinable, not because
they are good practice.

When a local shares a name with a global, the **local wins** inside its scope:

```c
int x = 10;                  /* global */
void f(void) {
    int x = 20;              /* local shadows the global */
    printf("%d", x);         /* 20 */
}
```

## 4.5 Storage classes

A storage class fixes a variable's **scope**, **lifetime**, **default value**
and **storage location**. The four-row table below is a guaranteed exam
question — memorise it.

| Storage class | Keyword | Scope | Lifetime | Default | Stored in |
|---|---|---|---|---|---|
| Automatic | `auto` | Block | Until block exits | Garbage | Stack |
| External | `extern` | Global, across files | Whole program | Zero | Data segment |
| Static | `static` | Block (or file) | **Whole program** | Zero | Data segment |
| Register | `register` | Block | Until block exits | Garbage | CPU register (if available) |

### `auto`

The default for local variables. `auto int x;` and `int x;` are identical, so
the keyword is essentially never written.

### `static` — the one worth understanding

A `static` local keeps its value **between calls**, but stays invisible outside
its function:

```c
void counter(void)
{
    static int count = 0;     /* initialised ONCE, on the first call */
    count++;
    printf("%d ", count);
}

/* counter(); counter(); counter();  prints:  1 2 3 */
```

Compare with a plain local, which resets to 0 every call and prints `1 1 1`.

A `static` **global** restricts a variable or function to its own source file —
the C equivalent of "private".

### `extern`

Declares that a variable exists **in another file**, so this file may use it.

```c
/* file1.c */  int total = 100;
/* file2.c */  extern int total;    /* not a new variable -- the same one */
```

`extern` declares; it does not allocate. The definition lives in exactly one
file.

### `register`

Requests that the variable be kept in a CPU register for speed. It is only a
*hint* — the compiler may ignore it. **You cannot take the address of a
`register` variable** (`&x` is a compile error), because registers have no
memory address. Modern optimisers make far better decisions than the
programmer, so the keyword is obsolete in practice; it remains examinable.

---

## Exam questions from this unit

**Two marks**

1. What is a pointer? How is it declared and initialized?
2. Distinguish between `&` and `*`.
3. What is a null pointer? Why is dereferencing one dangerous?
4. State two differences between an array and a pointer.
5. What are the two essential parts of a recursive function?

**Five marks**

1. Explain call by value and call by address with a swap program for each.
2. Explain pointer arithmetic with examples. Which operations are not permitted?
3. Explain the storage classes in C with a comparison table.
4. Explain recursion with a factorial example and trace `factorial(4)`.
5. Explain the categories of functions with examples of each.

**Ten marks**

1. Explain pointers in detail — declaration, initialization, dereferencing,
   arithmetic, and the relationship with arrays.
2. Explain all four storage classes with scope, lifetime, default value,
   storage location and an example each.

## Mistakes that cost marks

- Dereferencing an uninitialised or null pointer
- Assuming `p + 1` adds one byte — it adds `sizeof(type)` bytes
- Writing `swap(x, y)` when the function expects addresses (needs `swap(&x, &y)`)
- Expecting a call-by-value swap to change the caller's variables
- Forgetting that a `static` local is initialised only once
- Trying `&x` on a `register` variable
- Assuming a local variable defaults to 0 — it holds garbage
- Trying to return an array from a function (return a pointer, or pass the
  destination in)
