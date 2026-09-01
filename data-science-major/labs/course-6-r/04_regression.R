# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 4: Correlation and simple linear regression
# Python equivalent: python/04_regression.py
# Same data as Course 4 Unit 4 -- coefficients must match those notes.

hours  <- c(2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
scores <- c(52, 55, 61, 64, 70, 72, 78, 82, 85, 91)
df <- data.frame(hours, scores)

cor(hours, scores)                       # 0.997904 -- Pearson
cor(hours, scores, method = "spearman")  # rank correlation
cov(hours, scores)

plot(hours, scores, pch = 19, col = "#1e7fbf",
     main = "Exam score against study hours")

model <- lm(scores ~ hours, data = df)
summary(model)
#   (Intercept)  43.0303   Std.Error 1.0847   t 39.671
#   hours         4.3030   Std.Error 0.0987   t 43.615   p 8.42e-11
#   Multiple R-squared: 0.995812      F: 1902.26 on 1 and 8 DF
#
#   Fitted line:  scores = 43.0303 + 4.3030 * hours
#   Each extra hour of study is ASSOCIATED WITH about 4.3 more marks.

abline(model, col = "red", lwd = 2)

coef(model)
confint(model)
predict(model, newdata = data.frame(hours = 7.5))    # 75.30
residuals(model)
par(mfrow = c(2, 2)); plot(model); par(mfrow = c(1, 1))   # diagnostics

anova(model)     # SS_reg = 1527.58, SS_res = 6.42, F = 1902.26

# TWO FREE ARITHMETIC CHECKS for simple regression (Course 4 Unit 4):
#   R-squared == r^2        0.997904^2 = 0.995812  ✓
#   F         == t^2        43.615^2   = 1902.26   ✓
