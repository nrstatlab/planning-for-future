# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 7: Variables, control structures and functions
# No Python equivalent -- this experiment demonstrates R SYNTAX, so a
# translation would teach nothing.

# --- VARIABLES AND TYPES ---
# Step 1: Make a variable of each type
x <- 10L          # integer (note the L)
y <- 3.14         # numeric / double
name <- "Ravi"    # character
flag <- TRUE      # logical
z <- 3 + 4i       # complex

class(x); class(y); class(name); class(flag)
# NOTE: class(10) is "numeric", NOT "integer". Write 10L for an integer.

# --- VECTORS: R's fundamental unit ---
# Step 2: Index and compute on vectors
v <- c(10, 20, 30, 40, 50)
v[1]        # 10  -- R indexes from 1, not 0
v[-1]       # 20 30 40 50  -- negative EXCLUDES; it is not "from the end"
v[v > 25]   # 30 40 50
length(v)

v * 2       # 20 40 60 80 100  -- VECTORISED, no loop needed
c(1,2,3,4) + c(10,20)   # 11 22 13 24 -- RECYCLING of the shorter vector

# --- CONTROL STRUCTURES ---
# Step 3: Branch with if and ifelse()
marks <- 72
if (marks >= 40) {
  print("Pass")
} else if (marks >= 30) {
  print("Supplementary")
} else {
  print("Fail")
}

# ifelse() is VECTORISED -- use it on a whole column, never if()
ifelse(v > 25, "high", "low")

# Step 4: Loop with for, while and repeat
for (i in 1:5) print(i)
for (nm in c("A", "B", "C")) print(nm)

i <- 1
while (i <= 5) { print(i); i <- i + 1 }

repeat { i <- i + 1; if (i > 10) break }

# --- THE apply FAMILY: R's idiomatic alternative to loops ---
# Step 5: Apply a function across a matrix or a list
m <- matrix(1:6, nrow = 2)
apply(m, 1, sum)     # row sums     -- MARGIN 1 = rows
apply(m, 2, mean)    # column means -- MARGIN 2 = columns
sapply(1:5, function(k) k^2)          # 1 4 9 16 25 -- returns a vector
lapply(1:3, function(k) k^2)          # returns a LIST

# --- FUNCTIONS ---
# Step 6: Write functions, with default and variadic arguments
grade <- function(marks, pass_mark = 40) {
  if (marks >= 90) return("A")
  if (marks >= 75) return("B")
  if (marks >= 60) return("C")
  if (marks >= pass_mark) return("D")
  "F"                      # the last expression is returned automatically
}
grade(85)                  # "B"
grade(35, pass_mark = 30)  # "D" -- named argument

total <- function(...) sum(...)     # variadic
total(1, 2, 3, 4)                   # 10
