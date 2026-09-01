# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 10: Handle missing data and detect outliers
# Python equivalent: python/10_missing_outliers.py

x <- c(45, 67, NA, 52, 89, 91, NA, 64, 58, 82,
       76, 69, 71, 250, 60, 55, 93, 48, 79, NA)   # 250 is a planted outlier

# --- DETECTING MISSING VALUES ---
is.na(x)              # logical vector
sum(is.na(x))         # 3
which(is.na(x))       # 3 7 20  -- positions, 1-based
mean(is.na(x)) * 100  # 15% missing

# NEVER write x == NA. Comparing with an unknown value yields NA, never TRUE.
# This is the same trap as SQL's "= NULL" from Course 5.

# --- HANDLING ---
mean(x, na.rm = TRUE)          # 79.06 -- drag upward from the 250
median(x, na.rm = TRUE)        # 68.00 -- resistant
clean <- na.omit(x)            # drop the NAs

x_mean_imputed   <- ifelse(is.na(x), mean(x, na.rm = TRUE), x)
x_median_imputed <- ifelse(is.na(x), median(x, na.rm = TRUE), x)
# With an outlier present, MEDIAN imputation is the safer choice -- the mean
# has already been distorted by the very value you are trying to work around.

# --- OUTLIERS: the IQR rule ---
q <- quantile(clean, c(0.25, 0.75))
iqr <- IQR(clean)
lower <- q[1] - 1.5 * iqr        # 22.00
upper <- q[2] + 1.5 * iqr        # 118.00
clean[clean < lower | clean > upper]     # 250
boxplot(clean)$out                       # same answer, drawn

# --- OUTLIERS: the z-score rule ---
z <- (clean - mean(clean)) / sd(clean)
clean[abs(z) > 3]                # 250 here, z = 3.677

# MASKING -- why the IQR rule is preferred when outliers may cluster:
# add a second extreme value and the sd inflates enough that NEITHER is
# flagged by the z-score rule, while the IQR rule still catches both.
masked <- c(clean, 260)
zm <- (masked - mean(masked)) / sd(masked)
masked[abs(zm) > 3]              # returns NOTHING -- both outliers masked
qm <- quantile(masked, c(0.25, 0.75)); im <- IQR(masked)
masked[masked < qm[1] - 1.5*im | masked > qm[2] + 1.5*im]   # 250 260 -- caught
