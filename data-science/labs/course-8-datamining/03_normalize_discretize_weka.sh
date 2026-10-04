#!/usr/bin/env bash
# Experiment 3 in WEKA 3.8.7, from the command line: normalise and discretise.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 03_normalize_discretize_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Normalise every numeric attribute to [0, 1] (filter Normalize)
weka weka.filters.unsupervised.attribute.Normalize -i $DATA/iris.arff -o iris-normalised.arff
weka weka.core.Instances iris-normalised.arff

# Step 2: Discretise into 3 equal-width bins (filter Discretize, bins = 3)
weka weka.filters.unsupervised.attribute.Discretize -B 3 -R first-last -i $DATA/iris.arff -o iris-width.arff
grep "^@attribute" iris-width.arff

# Step 3: And into 3 equal-frequency bins (useEqualFrequency = True)
weka weka.filters.unsupervised.attribute.Discretize -B 3 -F -R first-last -i $DATA/iris.arff -o iris-freq.arff
grep "^@attribute" iris-freq.arff

# Step 4: Discretise using the class, by Fayyad-Irani MDL (the supervised Discretize)
weka weka.filters.supervised.attribute.Discretize -R first-last -c last -i $DATA/iris.arff -o iris-supervised.arff
grep "^@attribute" iris-supervised.arff
