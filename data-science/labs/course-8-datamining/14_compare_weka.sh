#!/usr/bin/env bash
# Experiment 14 in WEKA 3.8.7, from the command line: compare classifiers.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 14_compare_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Five classifiers on the same data, the same 10 folds (seed 1): accuracy, the confusion matrix, ROC area
for c in weka.classifiers.rules.ZeroR weka.classifiers.trees.J48 weka.classifiers.bayes.NaiveBayes weka.classifiers.lazy.IBk weka.classifiers.rules.JRip; do
  weka $c -t $DATA/vote.arff -x 10 -s 1 -o
done
