# Unit 2 — Basics of R Programming

**Syllabus topics:** Introduction to R and RStudio. Data types, variables,
operators. Control structures (`if`, loops, `apply`). Functions and packages.
Data input/output (CSV, Excel, XML, JSON).

---

You know Python from Course 3. This unit is mostly **translation** — the
concepts transfer, the syntax does not. The notes flag every place R behaves
differently, because those are exactly the places you will make mistakes.

## 2.1 R and RStudio

**R** is the language and the interpreter. **RStudio** is the IDE almost
everyone uses with it.

RStudio's four panes:

| Pane | Contains |
|---|---|
| **Source** (top-left) | Your `.R` script |
| **Console** (bottom-left) | The R prompt, where code executes |
| **Environment / History** (top-right) | Every object currently in memory |
| **Files / Plots / Packages / Help** (bottom-right) | Output and documentation |

**The Environment pane is R's most useful feature for a beginner.** It shows
every variable and its contents at all times, which makes debugging far more
visual than Python's.

Run the current line with **Ctrl+Enter**. Run the whole script with
**Ctrl+Shift+Enter**.

## 2.2 The assignment operator

```r
x <- 10          # the idiomatic R assignment
x = 10           # works, but not conventional
10 -> x          # legal, right-assignment; rarely used
x <<- 10         # global assignment, inside a function
```

**Use `<-`.** `=` works for assignment but is reserved by convention for
function arguments, and mixing them is how you write R that other people find
odd. Alt+− in RStudio types `<-` for you.

## 2.3 Data types

| Type | Example | Check |
|---|---|---|
| **numeric** (double) | `3.14`, `10` | `is.numeric()` |
| **integer** | `10L` | `is.integer()` |
| **character** | `"hello"` | `is.character()` |
| **logical** | `TRUE`, `FALSE`, `T`, `F` | `is.logical()` |
| **complex** | `3+4i` | `is.complex()` |
| **raw** | bytes | `is.raw()` |

`class(x)` and `typeof(x)` both report the type. `str(x)` gives the most useful
summary of any object.

> **In R, `10` is a double, not an integer.** Write `10L` for an integer.
> `class(10)` returns `"numeric"`, which surprises everyone once.

### The five data structures

| Structure | Dimensions | Contents |
|---|---|---|
| **Vector** | 1-D | All the **same** type |
| **Matrix** | 2-D | All the **same** type |
| **Array** | n-D | All the **same** type |
| **List** | 1-D | **Mixed** types |
| **Data frame** | 2-D | Columns may differ; rows are observations |

**The vector is R's fundamental unit.** There is no scalar type — `x <- 5`
creates a vector of length 1. `length(5)` returns 1, not an error.

```r
v <- c(1, 2, 3, 4, 5)          # c() = combine
v <- 1:5                        # the colon operator
v <- seq(1, 10, by = 2)         # 1 3 5 7 9
v <- rep(0, 5)                  # 0 0 0 0 0
```

### 💡 Vectorisation — the idea that makes R feel different

Operations apply to whole vectors at once, with no loop:

```r
v <- c(1, 2, 3, 4, 5)
v * 2                # 2 4 6 8 10
v + v                # 2 4 6 8 10
sqrt(v)              # applies elementwise
v[v > 3]             # 4 5   -- boolean filtering
```

Writing a `for` loop to double every element is not wrong, but it is slow and
marks you as someone thinking in C. **Think in whole vectors.**

**Recycling**: if two vectors differ in length, R repeats the shorter one.

```r
c(1, 2, 3, 4) + c(10, 20)      # 11 22 13 24  -- (10,20) recycled
c(1, 2, 3) + c(10, 20)         # warning: longer object length is not a
                               # multiple of shorter object length
```

Recycling is powerful and is also a silent bug factory. If you see that warning,
stop and check your lengths.

### Indexing from 1 — and negative indexing

```r
v <- c(10, 20, 30, 40, 50)
v[1]        # 10   -- R starts at 1, NOT 0
v[2:4]      # 20 30 40
v[-1]       # 20 30 40 50   -- negative means EXCLUDE, not "from the end"
v[c(TRUE, FALSE, TRUE, FALSE, TRUE)]   # 10 30 50
```

**Two traps for Python programmers**, both examinable:

1. **Indexing starts at 1.**
2. **`v[-1]` removes the first element.** In Python it returns the last one. In
   R there is no negative-from-the-end indexing; use `tail(v, 1)`.

### Matrices, lists and data frames

```r
m <- matrix(1:6, nrow = 2, ncol = 3)          # fills COLUMN-wise by default
m <- matrix(1:6, nrow = 2, byrow = TRUE)      # fill row-wise
m[1, 2]        # row 1, column 2
m[1, ]         # entire row 1
dim(m); t(m)   # dimensions; transpose

lst <- list(name = "Ravi", age = 20, marks = c(85, 90))
lst$name          # "Ravi"
lst[["age"]]      # 20
lst[1]            # a LIST of length 1
lst[[1]]          # the ELEMENT itself

df <- data.frame(roll = c(1, 2, 3),
                 name = c("A", "B", "C"),
                 marks = c(85, 72, 91))
df$marks              # a column
df[df$marks > 80, ]   # filter rows -- note the trailing comma
nrow(df); ncol(df); str(df); head(df); summary(df)
```

**`[` vs `[[` on a list** is a classic exam question: single brackets return a
*list*, double brackets return the *element*.

**Note `matrix()` fills column-wise by default** — the opposite of C's row-major
layout from Course 2. `byrow = TRUE` changes it.

### Missing values

| Value | Means |
|---|---|
| `NA` | Not Available — missing data |
| `NULL` | The empty object; absence of a value entirely |
| `NaN` | Not a Number — `0/0` |
| `Inf`, `-Inf` | Infinity — `1/0` |

```r
is.na(x)                       # test -- NEVER x == NA
mean(v, na.rm = TRUE)          # remove NAs before computing
sum(is.na(df$col))             # count missing
```

> **`x == NA` always returns `NA`, never `TRUE`.** Comparing to an unknown value
> yields an unknown result. Use `is.na(x)`. This is the same trap as SQL's
> `= NULL` from Course 5 — and for exactly the same reason.

### Factors — categorical data

```r
grades <- factor(c("A", "B", "A", "C"))
levels(grades)                   # "A" "B" "C"
table(grades)                    # frequency count

sizes <- factor(c("small", "large", "medium"),
                levels = c("small", "medium", "large"),
                ordered = TRUE)  # an ORDERED factor
```

A factor stores categories as integers with labels. R uses them throughout
modelling — `lm()` automatically creates dummy variables from a factor.

**The classic bug:** `as.numeric(factor)` returns the internal *codes*, not the
values. `as.numeric(as.character(f))` is the correct conversion.

## 2.4 Operators

| Category | Operators |
|---|---|
| Arithmetic | `+ - * / ^ %% %/%` |
| Relational | `< > <= >= == !=` |
| Logical (vectorised) | `& \| !` |
| Logical (single value) | `&& \|\|` |
| Assignment | `<- <<- = ->` |
| Special | `%in%`, `%>%` (pipe), `:` |

**`&` vs `&&`** is examinable: `&` compares element by element across a vector;
`&&` evaluates only the first element and is for a single `if` condition. Modern
R errors if you give `&&` a vector longer than one — which is a good thing.

```r
c(TRUE, FALSE) & c(TRUE, TRUE)     # TRUE FALSE  -- elementwise
5 %in% c(1, 5, 9)                  # TRUE
7 %% 3                             # 1  -- modulus
7 %/% 3                            # 2  -- integer division
2 ^ 3                              # 8  -- R uses ^, not **
```

## 2.5 Control structures

```r
if (marks >= 40) {
  print("Pass")
} else if (marks >= 30) {
  print("Supplementary")
} else {
  print("Fail")
}

ifelse(v > 3, "big", "small")      # VECTORISED -- returns a vector

for (i in 1:5) print(i)
for (name in c("A", "B")) print(name)

i <- 1
while (i <= 5) { print(i); i <- i + 1 }

repeat { i <- i + 1; if (i > 10) break }
```

**`if` vs `ifelse`** — a reliable two-mark question. `if` takes a **single**
condition and controls flow. `ifelse` is **vectorised** and returns a vector the
same length as its input. Passing a vector to `if` is an error.

### The `apply` family — R's alternative to loops

| Function | Input | Returns |
|---|---|---|
| `apply(m, MARGIN, f)` | matrix/array | `MARGIN=1` rows, `2` columns |
| `lapply(x, f)` | list/vector | a **list** |
| `sapply(x, f)` | list/vector | **simplified** — vector or matrix |
| `vapply(x, f, type)` | list/vector | simplified, with a type check |
| `mapply(f, x, y)` | several | multivariate version of `sapply` |
| `tapply(x, group, f)` | vector + factor | grouped summary |

```r
m <- matrix(1:6, nrow = 2)
apply(m, 1, sum)                 # row sums
apply(m, 2, mean)                # column means

sapply(df, class)                # class of every column
lapply(1:3, function(x) x^2)     # a list: 1, 4, 9
sapply(1:3, function(x) x^2)     # a vector: 1 4 9
tapply(df$marks, df$section, mean)   # mean marks per section
```

**Remember `MARGIN`: 1 = rows, 2 = columns.** The mnemonic is that a matrix is
written `[rows, columns]`, so 1 is the first position.

## 2.6 Functions

```r
greet <- function(name, greeting = "Hello") {
  message <- paste(greeting, name)
  return(message)
}

greet("Ravi")                      # "Hello Ravi"
greet("Ravi", "Welcome")           # "Welcome Ravi"
greet(greeting = "Hi", name = "A") # named arguments, any order
```

Three R-specific points:

1. **The last expression is returned automatically** — `return()` is optional.
   Most idiomatic R omits it.
2. **Arguments are lazily evaluated** — an argument is not computed until it is
   used, so an unused invalid argument causes no error.
3. **Everything is copied on modification.** A function cannot change its
   caller's variable, unlike C's call-by-address from Course 2.

Variadic arguments use `...`:

```r
total <- function(...) sum(...)
total(1, 2, 3)      # 6
```

## 2.7 Packages

```r
install.packages("dplyr")     # once, downloads from CRAN
library(dplyr)                # every session, loads it
require(dplyr)                # same but returns FALSE instead of erroring
dplyr::filter(df, x > 5)      # use without loading -- avoids name clashes
```

**`install.packages()` vs `library()`** is examinable: you install once, and
load in every new session. Confusing them is the commonest beginner error.

**`::` matters more than it looks.** Both `dplyr` and `stats` export `filter`,
so after `library(dplyr)` a call to `filter()` may not be the one you meant.
`dplyr::filter()` is unambiguous.

**Essential packages for this course:** `dplyr`, `tidyr`, `ggplot2`, `readr`,
`readxl`, `jsonlite`, `XML`, `forecast`, `plotly`, `shiny`. `install.packages("tidyverse")`
gets most of them at once.

## 2.8 Data input and output

| Format | Read | Write |
|---|---|---|
| **CSV** | `read.csv("f.csv")` · `readr::read_csv()` | `write.csv(df, "f.csv", row.names = FALSE)` |
| **Excel** | `readxl::read_excel("f.xlsx", sheet = 1)` | `writexl::write_xlsx(df, "f.xlsx")` |
| **JSON** | `jsonlite::fromJSON("f.json")` | `jsonlite::toJSON(df, pretty = TRUE)` |
| **XML** | `XML::xmlToDataFrame("f.xml")` | `XML::saveXML()` |
| **R native** | `readRDS("f.rds")` · `load("f.RData")` | `saveRDS(obj, "f.rds")` · `save()` |
| **Text** | `readLines("f.txt")` | `writeLines(x, "f.txt")` |

```r
df <- read.csv("students.csv", header = TRUE, stringsAsFactors = FALSE)
write.csv(df, "output.csv", row.names = FALSE)
```

Two arguments worth knowing:

- **`row.names = FALSE`** on `write.csv` — otherwise R adds an unwanted index
  column, and re-reading the file gives you a stray `X` column.
- **`stringsAsFactors`** — defaulted to `TRUE` before R 4.0 and silently turned
  every text column into a factor. It now defaults to `FALSE`. Older textbooks
  and exam papers still set it explicitly; know why.

`readr::read_csv()` (with an underscore) is faster than base `read.csv()`,
returns a tibble, and never converts strings to factors.

---

## 📝 Practice problems

### Problem 1

Predict the output:

```r
v <- c(10, 20, 30, 40, 50)
print(v[-2])
print(v[v > 25])
print(length(v[-1]))
```

**Solution.**

- `v[-2]` → **`10 30 40 50`**. Negative indexing *excludes*; it drops the 2nd
  element. It does **not** mean "second from the end".
- `v[v > 25]` → **`30 40 50`**. Boolean filtering keeps elements where the
  condition is TRUE.
- `length(v[-1])` → **`4`**. One element removed from five.

### Problem 2

Write an R function that takes a numeric vector and returns its mean, median and
standard deviation as a named list, handling `NA` values.

**Solution.**

```r
summarise_vector <- function(v) {
  if (!is.numeric(v)) stop("input must be numeric")
  list(
    mean   = mean(v,   na.rm = TRUE),
    median = median(v, na.rm = TRUE),
    sd     = sd(v,     na.rm = TRUE),
    n_missing = sum(is.na(v))
  )
}

summarise_vector(c(10, 20, NA, 40, 50))
# $mean 30   $median 30   $sd 18.257   $n_missing 1
```

`na.rm = TRUE` is essential — without it, a single `NA` makes every result `NA`.
Returning `n_missing` alongside is good practice: it tells the reader how much
data the summary is based on.

*Check:* the non-missing values are 10, 20, 40, 50 → mean 30, median 30,
sample sd = √[(400+100+100+400)/3] = √333.33 = 18.257 ✓

### Problem 3

Given a data frame `students` with columns `name`, `section`, `marks`, write R
to (a) filter students scoring above 75, (b) compute the mean mark per section,
(c) add a `grade` column.

**Solution.**

```r
# (a) base R
high <- students[students$marks > 75, ]

# (b) mean per section
tapply(students$marks, students$section, mean)

# (c) vectorised grade assignment
students$grade <- ifelse(students$marks >= 90, "A",
                  ifelse(students$marks >= 75, "B",
                  ifelse(students$marks >= 60, "C",
                  ifelse(students$marks >= 40, "D", "F"))))
```

Note **`ifelse`**, not `if` — the operation applies to a whole column. Using
`if` here would test only the first row and warn (or error in modern R).

Unit 3 shows the `dplyr` versions of all three, which are considerably more
readable.

---

## Exam questions from this unit

**Two marks**

1. What is the difference between `<-` and `=` in R?
2. Why does `v[-1]` not return the last element?
3. Distinguish `if` from `ifelse`.
4. Distinguish `install.packages()` from `library()`.
5. What does `MARGIN = 1` mean in `apply()`?
6. Why does `x == NA` not work?

**Five marks**

1. Explain the data structures in R with examples.
2. Explain the `apply` family with examples of each function.
3. Explain vectorisation and recycling with examples.
4. Explain reading and writing CSV, Excel, JSON and XML in R.

**Ten marks**

1. Explain R data types and structures in detail, with the differences from
   Python where relevant.
2. Explain control structures and functions in R with examples.

## Mistakes that cost marks

- Indexing from 0 — R starts at **1**
- Expecting `v[-1]` to give the last element
- Using `if` where a vectorised `ifelse` is needed
- Forgetting `na.rm = TRUE` and getting `NA` from every summary
- Testing `x == NA` instead of `is.na(x)`
- Forgetting `library()` after `install.packages()`
- `as.numeric()` on a factor, which returns the level codes
- Forgetting `row.names = FALSE` in `write.csv`
- Assuming `matrix()` fills row-wise — it fills **column-wise**
