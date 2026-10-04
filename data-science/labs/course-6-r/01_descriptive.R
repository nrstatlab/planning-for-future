# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 1: Mean, Median, Mode, Variance, Standard Deviation
# Python equivalent: python/01_descriptive.py

# Step 1: Enter the marks
marks <- c(45, 67, 78, 52, 89, 91, 73, 64, 58, 82,
           76, 69, 71, 85, 60, 55, 93, 48, 79, 66)

# --- Central tendency ---
# Step 2: Find the centre: mean, median and mode
mean(marks)      # 70.05
median(marks)    # 70.00

# R has NO built-in mode() for the statistical mode -- mode() reports the
# storage type. Define one, which the syllabus expects you to know:
statistical_mode <- function(v) {
  freq <- table(v)
  as.numeric(names(freq)[freq == max(freq)])
}
statistical_mode(marks)   # every value occurs once here, so all 20 are returned

# --- Dispersion ---
# Step 3: Measure the spread: variance, SD, range and quartiles
var(marks)       # 202.8921   <- R's var() divides by n-1 (SAMPLE)
sd(marks)        #  14.2440   <- likewise
range(marks)     # 45 93
diff(range(marks))  # 48
IQR(marks)
quantile(marks)

# Step 4: Convert to the population variance
# Population variance, if you need it, must be computed explicitly:
n <- length(marks)
var(marks) * (n - 1) / n     # 192.7475
sqrt(var(marks) * (n - 1) / n)   # 13.8834

# --- Everything at once ---
# Step 5: Summarise everything at once
summary(marks)

# NOTE FOR THE EXAM: R's var() and sd() are the n-1 versions. If a question
# asks for the population variance you must convert, as above. This is the
# same n vs n-1 distinction as Course 4 Unit 1.
