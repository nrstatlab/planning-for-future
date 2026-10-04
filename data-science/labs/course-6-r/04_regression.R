# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 4: Correlation and simple linear regression
# Python equivalent: python/04_regression.py
# Same data as Course 4 Unit 4 -- coefficients must match those notes.

# Step 1: Enter the hours and scores
hours  <- c(2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
scores <- c(52, 55, 61, 64, 70, 72, 78, 82, 85, 91)
df <- data.frame(hours, scores)

# Step 2: Measure the correlation, and plot the points
cor(hours, scores)                       # 0.997904 -- Pearson
cor(hours, scores, method = "spearman")  # rank correlation
cov(hours, scores)

plot(hours, scores, pch = 19, col = "#1e7fbf",
     main = "Exam score against study hours")

# Step 3: Fit the regression line
model <- lm(scores ~ hours, data = df)
summary(model)
#   (Intercept)  43.0303   Std.Error 0.7011   t 61.38
#   hours         4.3030   Std.Error 0.0987   t 43.615   p 8.43e-11
#   [Corrected: this gave the intercept's standard error as 1.0847 and its
#   t as 39.671. R prints 0.70111 and 61.38, and by hand
#   SE = 0.8961 x sqrt(1/10 + 6.5^2/82.5) = 0.7011.]
#   Multiple R-squared: 0.995812      F: 1902.26 on 1 and 8 DF
#
#   Fitted line:  scores = 43.0303 + 4.3030 * hours
#   Each extra hour of study is ASSOCIATED WITH about 4.3 more marks.

abline(model, col = "red", lwd = 2)

# Step 4: Use the model: coefficients, intervals, a prediction, residuals
coef(model)
confint(model)
predict(model, newdata = data.frame(hours = 7.5))    # 75.30
residuals(model)
par(mfrow = c(2, 2)); plot(model); par(mfrow = c(1, 1))   # diagnostics

# Step 5: Read the ANOVA table
anova(model)     # SS_reg = 1527.58, SS_res = 6.42, F = 1902.26

# TWO FREE ARITHMETIC CHECKS for simple regression (Course 4 Unit 4):
#   R-squared == r^2        0.997904^2 = 0.995812  ✓
#   F         == t^2        43.615^2   = 1902.26   ✓
