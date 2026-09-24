# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 6: Scaling, normalisation and encoding
# Python equivalent: python/06_feature_engineering.py

marks <- c(85, 62, 91, 55, 74, 79, 48, 88, 68, 41)
section <- factor(c("A","A","B","B","A","C","C","B","A","C"))

# --- MIN-MAX NORMALISATION: x' = (x - min)/(max - min) -> [0, 1] ---
normalise <- function(x) (x - min(x)) / (max(x) - min(x))
normalise(marks)
range(normalise(marks))    # must be exactly 0 and 1

# --- STANDARDISATION: x' = (x - mean)/sd -> mean 0, sd 1 ---
scale(marks)               # returns a matrix; use as.vector() for a vector
as.vector(scale(marks))
mean(scale(marks)); sd(scale(marks))    # ~0 and exactly 1

# NOTE: scale() uses sd(), which divides by n-1. Python's
# sklearn StandardScaler divides by n. The values differ slightly --
# harmless for modelling, but do not expect identical numbers.

# --- ONE-HOT ENCODING ---
model.matrix(~ section - 1)     # the -1 drops the intercept -> k columns
model.matrix(~ section)         # keeps intercept -> k-1 columns (reference = A)

# For MODELLING use the k-1 form: k columns are perfectly collinear
# (they sum to 1), which is the dummy variable trap. lm() and glm() handle
# factors automatically, so you rarely encode by hand.

# --- LABEL / ORDINAL ENCODING (only for genuinely ordered categories) ---
sizes <- factor(c("small","large","medium"),
                levels = c("small","medium","large"), ordered = TRUE)
as.numeric(sizes)          # 1 3 2 -- correct here, because the order is real

# THE CLASSIC BUG: as.numeric() on an unordered factor returns LEVEL CODES,
# not the values. For a factor of numbers use:
f <- factor(c("10","20","30"))
as.numeric(f)                    # 1 2 3   <- WRONG
as.numeric(as.character(f))      # 10 20 30 <- correct

# --- BINNING ---
cut(marks, breaks = c(0, 40, 50, 60, 75, 100),
    labels = c("Fail","Pass","Second","First","Distinction"),
    right = FALSE)
table(cut(marks, breaks = c(0, 40, 50, 60, 75, 100),
          labels = c("Fail","Pass","Second","First","Distinction"),
          right = FALSE))
