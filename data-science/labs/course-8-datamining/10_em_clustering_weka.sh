#!/usr/bin/env bash
# Experiment 10 in WEKA 3.8.7, from the command line: EM clustering.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 10_em_clustering_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Let EM choose the number of clusters by cross-validation (EM, numClusters = -1)
weka weka.clusterers.EM -N -1 -I 100 -t $DATA/iris.arff -c last

# Step 2: EM with 3 clusters, to compare with K-Means
weka weka.clusterers.EM -N 3 -I 100 -t $DATA/iris.arff -c last
