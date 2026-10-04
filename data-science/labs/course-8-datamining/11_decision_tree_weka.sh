#!/usr/bin/env bash
# Experiment 11 in WEKA 3.8.7, from the command line: a decision tree with J48.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 11_decision_tree_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Build J48 on the weather data, and cross-validate it 10 ways (Classify tab)
weka weka.classifiers.trees.J48 -C 0.25 -M 2 -t $DATA/weather.nominal.arff

# Step 2: The same tree, unpruned (unpruned = True)
weka weka.classifiers.trees.J48 -U -M 2 -t $DATA/weather.nominal.arff -o
