# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 6: Scaling, normalisation and encoding
# Python equivalent: python/06_feature_engineering.py

# Step 1: Enter the marks and sections
marks <- c(85, 62, 91, 55, 74, 79, 48, 88, 68, 41)
section <- factor(c("A","A","B","B","A","C","C","B","A","C"))

# --- MIN-MAX NORMALISATION: x' = (x - min)/(max - min) -> [0, 1] ---
# Step 2: Normalise to [0, 1] by min-max
normalise <- function(x) (x - min(x)) / (max(x) - min(x))
normalise(marks)
range(normalise(marks))    # must be exactly 0 and 1

# --- STANDARDISATION: x' = (x - mean)/sd -> mean 0, sd 1 ---
# Step 3: Standardise to mean 0 and SD 1
scale(marks)               # returns a matrix; use as.vector() for a vector
as.vector(scale(marks))
mean(scale(marks)); sd(scale(marks))    # ~0 and exactly 1

# NOTE: scale() uses sd(), which divides by n-1. Python's
# sklearn StandardScaler divides by n. The values differ slightly --
# harmless for modelling, but do not expect identical numbers.

# --- ONE-HOT ENCODING ---
# Step 4: One-hot encode the sections
model.matrix(~ section - 1)     # the -1 drops the intercept -> k columns
model.matrix(~ section)         # keeps intercept -> k-1 columns (reference = A)

# For MODELLING use the k-1 form: k columns are perfectly collinear
# (they sum to 1), which is the dummy variable trap. lm() and glm() handle
# factors automatically, so you rarely encode by hand.

# --- LABEL / ORDINAL ENCODING (only for genuinely ordered categories) ---
# Step 5: Encode an ordered category, and avoid the factor trap
sizes <- factor(c("small","large","medium"),
                levels = c("small","medium","large"), ordered = TRUE)
as.numeric(sizes)          # 1 3 2 -- correct here, because the order is real

# THE CLASSIC BUG: as.numeric() on an unordered factor returns LEVEL CODES,
# not the values. For a factor of numbers use:
f <- factor(c("10","20","30"))
as.numeric(f)                    # 1 2 3   <- WRONG
as.numeric(as.character(f))      # 10 20 30 <- correct

# --- BINNING ---
# Step 6: Bin the marks into classes
cut(marks, breaks = c(0, 40, 50, 60, 75, 100),
    labels = c("Fail","Pass","Second","First","Distinction"),
    right = FALSE)
table(cut(marks, breaks = c(0, 40, 50, 60, 75, 100),
          labels = c("Fail","Pass","Second","First","Distinction"),
          right = FALSE))
