#!/usr/bin/env bash
# Experiment 8 in WEKA 3.8.7, from the command line: K-Means.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 08_kmeans_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Cluster iris into 3, ignoring the class, then compare with it (SimpleKMeans, classes to clusters)
weka weka.clusterers.SimpleKMeans -N 3 -S 10 -t $DATA/iris.arff -c last

# Step 2: The same with another seed, which can change the answer (seed = 31). Most
# seeds find the clustering above; this one stops in a worse local optimum.
weka weka.clusterers.SimpleKMeans -N 3 -S 31 -t $DATA/iris.arff -c last
