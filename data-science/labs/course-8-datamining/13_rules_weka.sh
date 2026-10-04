#!/usr/bin/env bash
# Experiment 13 in WEKA 3.8.7, from the command line: rule-based classification.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 13_rules_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: ZeroR first, the baseline (rules/ZeroR)
weka weka.classifiers.rules.ZeroR -t $DATA/weather.nominal.arff -o

# Step 2: OneR, the single best attribute (rules/OneR)
weka weka.classifiers.rules.OneR -t $DATA/weather.nominal.arff

# Step 3: RIPPER (rules/JRip)
weka weka.classifiers.rules.JRip -F 3 -N 2.0 -t $DATA/weather.nominal.arff

# Step 4: PART, rules from partial trees (rules/PART)
weka weka.classifiers.rules.PART -t $DATA/weather.nominal.arff
