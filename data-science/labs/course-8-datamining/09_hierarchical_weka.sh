#!/usr/bin/env bash
# Experiment 9 in WEKA 3.8.7, from the command line: hierarchical clustering.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 09_hierarchical_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Cluster iris by single linkage, and print the tree (HierarchicalClusterer, printNewick)
weka weka.clusterers.HierarchicalClusterer -N 3 -L SINGLE -P -t $DATA/iris.arff -c last

# Step 2: The same by complete linkage
weka weka.clusterers.HierarchicalClusterer -N 3 -L COMPLETE -t $DATA/iris.arff -c last
