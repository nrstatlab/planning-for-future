# Unit 5 — Dynamic Memory, Structures, Unions and Files

**Syllabus topics:** Dynamic Memory Management — introduction, functions
`malloc`, `calloc`, `realloc`, `free`. Structures — basics, structure members,
accessing members, nested structures, array of structures, structures and
functions, structures and pointers. Unions — definition, difference between
structures and unions. Working with text files — modes, opening, reading,
writing and closing.

---

## 5.1 Dynamic memory management

### Why it exists

```c
int marks[100];        /* fixed at compile time */
```

What if you need 50? You waste half. What if you need 500? You crash. **Dynamic
allocation** lets you ask for exactly what you need, when you know how much
that is.

### The four functions — `<stdlib.h>`

| Function | Purpose | Initialises? |
|---|---|---|
| `malloc(size)` | Allocate `size` bytes | No — contains garbage |
| `calloc(n, size)` | Allocate `n × size` bytes | **Yes — all zeros** |
| `realloc(ptr, size)` | Resize an existing block | Preserves existing content |
| `free(ptr)` | Release the block | — |

### `malloc`

```c
int *p = (int *) malloc(5 * sizeof(int));   /* room for 5 ints */

if (p == NULL) {                            /* ALWAYS check */
    printf("Memory allocation failed\n");
    return 1;
}

for (int i = 0; i < 5; i++)
    p[i] = i * 10;                          /* use it like an array */

free(p);                                    /* release it */
p = NULL;                                   /* avoid a dangling pointer */
```

`malloc` returns `void *`, which any pointer type accepts. The cast `(int *)` is
required in C++ and optional in C; textbooks include it, so write it.

Use `sizeof(int)` rather than the literal `4` — it keeps the code correct on
machines with a different `int` size.

### `calloc`

```c
int *p = (int *) calloc(5, sizeof(int));    /* 5 ints, ALL SET TO ZERO */
```

| | `malloc` | `calloc` |
|---|---|---|
| Arguments | One (total bytes) | Two (count, size each) |
| Contents | Garbage | Zeros |
| Speed | Marginally faster | Slightly slower (it zeroes) |

`malloc(5 * sizeof(int))` and `calloc(5, sizeof(int))` allocate the same amount;
only the initialisation differs.

### `realloc`

```c
p = (int *) realloc(p, 10 * sizeof(int));   /* grow from 5 to 10 */
```

Existing contents are preserved; any new space is uninitialised. `realloc` may
move the block to a new address, which is why you must reassign `p`.

**A subtle bug:** if `realloc` fails it returns `NULL` *without* freeing the
original block. Writing `p = realloc(p, n)` then loses the only pointer to the
old memory. The safe idiom:

```c
int *temp = realloc(p, new_size);
if (temp != NULL)
    p = temp;
else
    /* p is still valid; handle the failure */;
```

### `free` and the three classic errors

```c
free(p);
```

1. **Memory leak** — allocating and never freeing. The program's memory use
   grows until it is killed. Every `malloc` needs a matching `free`.
2. **Dangling pointer** — using a pointer after freeing it. The memory may have
   been handed to something else. Set `p = NULL` after freeing.
3. **Double free** — calling `free(p)` twice on the same block. Undefined
   behaviour, often a crash. Setting `p = NULL` prevents this too, because
   `free(NULL)` is safely defined as doing nothing.

### Stack vs heap

| | Stack | Heap |
|---|---|---|
| Holds | Local variables, function parameters | Dynamically allocated memory |
| Managed by | The compiler, automatically | You, via `malloc`/`free` |
| Size | Small and fixed | Large |
| Speed | Fast | Slower |
| Lifetime | Until the function returns | Until you `free` it |
| Overflow | "Stack overflow" | `malloc` returns `NULL` |

## 5.2 Structures

A **structure** groups variables of **different types** under one name.

```c
struct Student {
    int   roll;
    char  name[50];
    float cgpa;
};                      /* the semicolon is REQUIRED */

struct Student s1 = {24001, "Ananya", 8.75};

printf("%d %s %.2f", s1.roll, s1.name, s1.cgpa);
```

### Accessing members

| Through | Operator | Example |
|---|---|---|
| A structure variable | `.` (dot) | `s1.roll` |
| A pointer to a structure | `->` (arrow) | `ptr->roll` |

```c
struct Student *ptr = &s1;
printf("%d", ptr->roll);        /* preferred */
printf("%d", (*ptr).roll);      /* identical, but clumsy */
```

The brackets in `(*ptr).roll` are essential — `.` binds tighter than `*`, so
`*ptr.roll` would be parsed as `*(ptr.roll)` and fail to compile. `->` exists
precisely to avoid this.

### Array of structures

```c
struct Student class[50];

class[0].roll = 24001;
strcpy(class[0].name, "Ananya");

for (int i = 0; i < n; i++)
    printf("%d %s\n", class[i].roll, class[i].name);
```

This is the standard shape of a record-keeping program, and of lab experiments
12 and 15.

### Nested structures

```c
struct Date {
    int day, month, year;
};

struct Employee {
    int  id;
    char name[50];
    struct Date joining;      /* a structure inside a structure */
};

struct Employee e;
e.joining.day = 15;           /* chain the dots */
```

The inner structure must be defined **before** it is used.

### Structures and functions

```c
/* By value -- the whole structure is copied */
void display(struct Student s) { printf("%d", s.roll); }

/* By address -- only a pointer is passed; changes reach the caller */
void update(struct Student *s) { s->cgpa = 9.0; }

/* Returning a structure */
struct Student create(int roll, const char *name)
{
    struct Student s;
    s.roll = roll;
    strcpy(s.name, name);
    return s;
}
```

Passing a large structure by value copies every byte. Pass a pointer instead —
faster, and it lets the function modify the original. Use `const struct Student *`
when it should read but not write.

### Assignment works; comparison does not

```c
struct Student a = {1, "X", 8.0}, b;
b = a;                  /* legal -- copies every member */
if (a == b)             /* ILLEGAL -- will not compile */
```

To compare, test the members individually. (`memcmp` may disagree with your
intent because of padding bytes between members.)

### `typedef`

```c
typedef struct {
    int roll;
    char name[50];
} Student;              /* now "Student" alone is the type */

Student s1;             /* instead of struct Student s1; */
```

## 5.3 Unions

A **union** looks like a structure but all members **share the same memory**.
Its size is that of its largest member, and only one member holds a valid value
at a time.

```c
union Data {
    int   i;
    float f;
    char  str[20];
};

union Data d;
d.i = 10;
printf("%d", d.i);      /* 10 -- fine */
d.f = 22.5;             /* this OVERWRITES the memory holding i */
printf("%d", d.i);      /* garbage -- i is no longer meaningful */
```

### Structure vs union — the guaranteed exam question

| | Structure | Union |
|---|---|---|
| Memory | Sum of all members (plus padding) | Size of the **largest** member |
| Members valid | **All** simultaneously | **One** at a time |
| Changing one member | Others unaffected | Overwrites the others |
| Keyword | `struct` | `union` |
| Use for | Grouping related data | Saving memory when only one value applies |

```c
struct S { int i; float f; char c; };   /* about 12 bytes with padding */
union  U { int i; float f; char c; };   /* 4 bytes -- the largest member */
```

**When a union is the right tool:** a value that could be one of several types,
paired with a tag saying which — a shape that is either a circle (radius) or a
rectangle (width and height), never both.

## 5.4 File handling

Variables vanish when the program ends. Files persist.

### Opening and closing

```c
FILE *fp;
fp = fopen("data.txt", "r");

if (fp == NULL) {                    /* ALWAYS check */
    printf("Cannot open file\n");
    return 1;
}

/* ... work with the file ... */

fclose(fp);                          /* ALWAYS close */
```

`FILE` is a structure defined in `stdio.h`; you always use a `FILE *`.

Failing to `fclose` risks losing buffered output — data sits in memory waiting
to be written and is discarded if the program ends without flushing.

### File modes

| Mode | Meaning | If the file does not exist | If it does |
|---|---|---|---|
| `"r"` | Read | Returns `NULL` | Opens at the start |
| `"w"` | Write | Creates it | **Erases all contents** |
| `"a"` | Append | Creates it | Writes at the end |
| `"r+"` | Read and write | Returns `NULL` | Opens at the start |
| `"w+"` | Read and write | Creates it | **Erases all contents** |
| `"a+"` | Read and append | Creates it | Reads anywhere, writes at the end |

Add `b` for binary — `"rb"`, `"wb"` — which matters on Windows, where text mode
translates line endings.

**`"w"` destroys the file's contents the instant you open it.** Opening a
valuable file with `"w"` by mistake loses the data before you have written
anything. Use `"a"` when you mean to add.

### Reading and writing

| Purpose | Character | String | Formatted | Block |
|---|---|---|---|---|
| Write | `fputc(ch, fp)` | `fputs(s, fp)` | `fprintf(fp, "...", ...)` | `fwrite(&data, size, n, fp)` |
| Read | `fgetc(fp)` | `fgets(s, n, fp)` | `fscanf(fp, "...", ...)` | `fread(&data, size, n, fp)` |

```c
/* Write */
FILE *fp = fopen("out.txt", "w");
fprintf(fp, "Roll: %d, Name: %s\n", 24001, "Ananya");
fputs("A second line\n", fp);
fclose(fp);

/* Read line by line -- the standard idiom */
char line[256];
fp = fopen("out.txt", "r");
while (fgets(line, sizeof(line), fp) != NULL)
    printf("%s", line);
fclose(fp);

/* Read character by character */
int ch;                            /* int, NOT char -- EOF needs the extra range */
while ((ch = fgetc(fp)) != EOF)
    putchar(ch);
```

**`fgetc` returns `int`, not `char`.** `EOF` is `-1`, and if you store the
result in a `char` you cannot reliably tell `EOF` from the byte `0xFF`. Declare
the variable `int`.

### Random access

```c
fseek(fp, 0, SEEK_END);        /* jump to the end */
long size = ftell(fp);         /* current position = file size in bytes */
rewind(fp);                    /* back to the start */

fseek(fp, 10, SEEK_SET);       /* 10 bytes from the beginning */
fseek(fp, -5, SEEK_CUR);       /* 5 bytes back from here      */
```

Origins: `SEEK_SET` (start), `SEEK_CUR` (current), `SEEK_END` (end).

Used in `14_reverse_file.c` to walk
a file backwards, and in
`15_book_file_crud.c` to
overwrite a record in place.

### Deleting a record from a file

You cannot remove bytes from the middle of a file. The standard technique:

1. Open the original for reading and a temporary file for writing
2. Copy every record **except** the one being deleted
3. Close both, `remove()` the original, `rename()` the temporary

Implemented in
`15_book_file_crud.c`.

---

## Exam questions from this unit

**Two marks**

1. Differentiate `malloc()` and `calloc()`.
2. What is a dangling pointer? How do you avoid one?
3. What is the size of a union with an `int`, a `float` and a `char[20]`?
4. Name the file opening modes and their meanings.
5. Why must `fgetc()`'s result be stored in an `int`?

**Five marks**

1. Explain the dynamic memory allocation functions with syntax and examples.
2. Explain nested structures and arrays of structures with examples.
3. Distinguish between a structure and a union with a program illustrating
   the memory difference.
4. Explain file opening modes with a table.

**Ten marks**

1. Explain structures in detail — declaration, initialization, member access,
   nesting, arrays of structures, and passing to functions.
2. Explain text file handling in C with all the read/write functions and a
   complete program.
3. Write a menu-driven program to store book details in a file with add,
   search, update and delete operations.

## Mistakes that cost marks

- Omitting the semicolon after a structure definition
- Using `.` on a pointer instead of `->`
- Forgetting to check `malloc` for `NULL`
- Leaking memory — no `free` to match the `malloc`
- Using a pointer after freeing it
- Opening an existing file with `"w"` and destroying its contents
- Not checking `fopen` for `NULL`
- Forgetting `fclose`, losing buffered output
- Storing `fgetc()`'s return value in a `char`
- Trying to compare two structures with `==`
- Expecting all union members to hold valid values at once
