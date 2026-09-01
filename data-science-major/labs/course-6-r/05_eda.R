# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 5: Exploratory Data Analysis
# Python equivalent: python/05_eda.py
data(iris)                       # or read.csv("yourfile.csv")

str(iris)                        # structure: 150 obs. of 5 variables
dim(iris); nrow(iris); ncol(iris)
head(iris); tail(iris)
summary(iris)                    # min, Q1, median, mean, Q3, max per column

colSums(is.na(iris))             # missing values per column
sum(complete.cases(iris))        # rows with no NA at all

table(iris$Species)              # categorical counts
prop.table(table(iris$Species))  # as proportions

hist(iris$Sepal.Length, breaks = 10, col = "#1e7fbf",
     main = "Distribution of sepal length")
boxplot(Sepal.Length ~ Species, data = iris, col = "#059669")
boxplot(iris$Sepal.Length)$out    # the outlier values themselves
pairs(iris[, 1:4], col = iris$Species)   # scatterplot matrix

cor(iris[, 1:4])                 # correlation matrix -- numeric columns only

# Skewness needs a package; the sign is what matters
# library(e1071); skewness(iris$Sepal.Length)
# mean > median  -> right-skewed ; mean < median -> left-skewed
mean(iris$Sepal.Length); median(iris$Sepal.Length)
