# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 5: Exploratory Data Analysis
# Python equivalent: python/05_eda.py
# Step 1: Load the data
data(iris)                       # or read.csv("yourfile.csv")

# Step 2: Look at its structure and summary
str(iris)                        # structure: 150 obs. of 5 variables
dim(iris); nrow(iris); ncol(iris)
head(iris); tail(iris)
summary(iris)                    # min, Q1, median, mean, Q3, max per column

# Step 3: Check for missing values
colSums(is.na(iris))             # missing values per column
sum(complete.cases(iris))        # rows with no NA at all

# Step 4: Count the categories
table(iris$Species)              # categorical counts
prop.table(table(iris$Species))  # as proportions

# Step 5: Plot the distributions, and find the outliers
hist(iris$Sepal.Length, breaks = 10, col = "#1e7fbf",
     main = "Distribution of sepal length")
boxplot(Sepal.Length ~ Species, data = iris, col = "#059669")
boxplot(iris$Sepal.Length)$out    # the outlier values themselves
pairs(iris[, 1:4], col = iris$Species)   # scatterplot matrix

# Step 6: Find the correlations
cor(iris[, 1:4])                 # correlation matrix -- numeric columns only

# Step 7: Judge the skew from the mean and median
# Skewness needs a package; the sign is what matters
# library(e1071); skewness(iris$Sepal.Length)
# mean > median  -> right-skewed ; mean < median -> left-skewed
mean(iris$Sepal.Length); median(iris$Sepal.Length)
