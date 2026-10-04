#!/usr/bin/env bash
# Experiment 12 in WEKA 3.8.7, from the command line: Naive Bayes, compared with J48.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 12_naive_bayes_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Naive Bayes on the weather data, cross-validated 10 ways
weka weka.classifiers.bayes.NaiveBayes -t $DATA/weather.nominal.arff

# Step 2: J48 and Naive Bayes on the vote data, the same 10 folds (seed 1), for a fair comparison
weka weka.classifiers.trees.J48 -t $DATA/vote.arff -x 10 -s 1 -o
weka weka.classifiers.bayes.NaiveBayes -t $DATA/vote.arff -x 10 -s 1 -o
