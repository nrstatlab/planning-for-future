#!/usr/bin/env bash
# Experiment 6 in WEKA 3.8.7, from the command line: association rules with Apriori.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 06_apriori_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Mine the supermarket data with Apriori, for the 10 best rules (Associate tab)
weka weka.associations.Apriori -N 10 -T 0 -C 0.9 -D 0.05 -U 1.0 -M 0.1 -t $DATA/supermarket.arff

# Step 2: The same data, ranked by lift instead of confidence (metricType = Lift)
weka weka.associations.Apriori -N 10 -T 1 -C 1.1 -D 0.05 -U 1.0 -M 0.1 -t $DATA/supermarket.arff
