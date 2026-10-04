#!/usr/bin/env bash
# Experiment 2 in WEKA 3.8.7, from the command line: replace missing values.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 02_missing_values_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Load labor.arff, and count its missing values (the Missing column)
weka weka.core.Instances $DATA/labor.arff

# Step 2: Replace them, by mean and mode (filter ReplaceMissingValues)
weka weka.filters.unsupervised.attribute.ReplaceMissingValues -i $DATA/labor.arff -o labor-filled.arff

# Step 3: Count them again
weka weka.core.Instances labor-filled.arff
