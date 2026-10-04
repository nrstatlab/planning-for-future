# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 14: Confusion matrix, accuracy and ROC
# Python equivalent: python/14_evaluation.py
# Same counts as Course 6 Unit 4 Problem 1: TP=80 FP=20 FN=40 TN=860

library(caret); library(pROC)

# Step 1: Make the actual and predicted labels
actual    <- factor(c(rep(1, 120), rep(0, 880)))
predicted <- factor(c(rep(1, 80), rep(0, 40), rep(1, 20), rep(0, 860)))

# Step 2: Build the confusion matrix and its metrics
cm <- confusionMatrix(predicted, actual, positive = "1")
cm
#   Accuracy    : 0.9400
#   Sensitivity : 0.6667   <- RECALL
#   Specificity : 0.9773
#   Pos Pred Val: 0.8000   <- PRECISION
#   F1          : 0.7273

cm$table         # the confusion matrix itself
cm$byClass       # every derived metric

# THE ACCURACY PARADOX:
# 88% of these patients are healthy, so "always predict healthy" already
# scores 0.88. This model's 0.94 beats that by only 0.06 -- and it MISSES
# 40 of the 120 real cases. Accuracy alone conceals that entirely.

# --- ROC and AUC: need SCORES, not hard labels ---
# probs <- predict(model, test, type = "prob")[, "1"]
# Step 3: Make scores for the ROC curve
set.seed(42)
probs <- ifelse(actual == 1, rbeta(1000, 5, 2), rbeta(1000, 2, 5))

# Step 4: Draw the ROC curve, and find the AUC
r <- roc(actual, probs)
auc(r)                       # ~0.96
plot(r, main = "ROC curve"); abline(a = 0, b = 1, lty = 2)

# AUC is the probability that the model ranks a random POSITIVE above a
# random NEGATIVE. 0.5 is the diagonal -- no better than guessing.
# Its advantage over accuracy is that it is THRESHOLD-INDEPENDENT.

# Step 5: Find the best threshold
coords(r, "best", ret = c("threshold", "sensitivity", "specificity"))
