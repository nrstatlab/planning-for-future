# =====================================================================
# NOT EXECUTED IN VERIFICATION
#
# R could not be installed in the environment where this repository was
# verified -- the Debian package repositories are blocked by the network
# policy, and R is not available from PyPI or npm. This script is
# DESK-CHECKED ONLY: the syntax has been reviewed by hand, not run.
#
# The numbers quoted in the comments below come from the Python equivalent
# in python/, which WAS executed. So the statistics are machine-checked even
# though the R syntax is not. Run this in RStudio to confirm the syntax.
# =====================================================================
# Experiment 1: Mean, Median, Mode, Variance, Standard Deviation
# Python equivalent: python/01_descriptive.py

marks <- c(45, 67, 78, 52, 89, 91, 73, 64, 58, 82,
           76, 69, 71, 85, 60, 55, 93, 48, 79, 66)

# --- Central tendency ---
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
var(marks)       # 202.8921   <- R's var() divides by n-1 (SAMPLE)
sd(marks)        #  14.2440   <- likewise
range(marks)     # 45 93
diff(range(marks))  # 48
IQR(marks)
quantile(marks)

# Population variance, if you need it, must be computed explicitly:
n <- length(marks)
var(marks) * (n - 1) / n     # 192.7475
sqrt(var(marks) * (n - 1) / n)   # 13.8834

# --- Everything at once ---
summary(marks)

# NOTE FOR THE EXAM: R's var() and sd() are the n-1 versions. If a question
# asks for the population variance you must convert, as above. This is the
# same n vs n-1 distinction as Course 4 Unit 1.
