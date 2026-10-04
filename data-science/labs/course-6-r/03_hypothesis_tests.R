# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 3: t-test and Chi-Square test
# Python equivalent: python/03_hypothesis_tests.py
# Same data as Course 4 Unit 5, so the numbers must agree with those notes.

# Step 1: Enter the two groups
group_a <- c(78, 82, 75, 88, 79, 84, 80, 86, 77, 83)
group_b <- c(72, 75, 70, 78, 74, 71, 76, 73, 69, 77)

# --- TWO-SAMPLE t-TEST ---
# Step 2: Run the pooled two-sample t-test
t.test(group_a, group_b, var.equal = TRUE)
#   t = 4.7541, df = 18, p-value = 0.000159
#   -> reject H0: the two group means differ significantly
#   mean of A = 81.20, mean of B = 73.50, pooled variance = 13.1167

# Step 3: Run Welch's test, and check the equal-variance assumption
# var.equal = TRUE gives the POOLED t-test (Course 4 Unit 5).
# Omit it and R runs Welch's t-test instead, which does not assume equal
# variances and reports fractional degrees of freedom. Both are defensible;
# know which one you asked for.
t.test(group_a, group_b)          # Welch -- note the different df

# Check the equal-variance assumption first:
var.test(group_a, group_b)        # F = 1.8618, p = 0.3682 -> variances OK

# Step 4: Run the one-sample and paired t-tests
# One-sample and paired variants:
t.test(group_a, mu = 80)
t.test(group_a, group_b, paired = TRUE)

# --- CHI-SQUARE TEST OF INDEPENDENCE ---
# Step 5: Test region against purchase type by chi-square
observed <- matrix(c(30, 70, 45, 55, 25, 75), nrow = 3, byrow = TRUE,
                   dimnames = list(c("North", "South", "East"),
                                   c("Premium", "Standard")))
observed
chisq.test(observed)
#   X-squared = 9.75, df = 2, p-value = 0.007635
#   -> reject H0: region and purchase type ARE associated

# Step 6: Check the expected counts and the residuals
result <- chisq.test(observed)
result$expected     # all 33.33 / 66.67 -- every one >= 5, assumption satisfied
result$residuals    # which cells contribute most to the statistic

# NOTE byrow = TRUE. R's matrix() fills COLUMN-wise by default, so omitting it
# silently transposes your table and changes the answer.
