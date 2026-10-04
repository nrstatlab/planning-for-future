#!/usr/bin/env bash
# Experiment 5 in WEKA 3.8.7, from the command line: summarise the data.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 05_summarize_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Summarise every attribute (the Preprocess panel)
weka weka.core.Instances $DATA/iris.arff

# Step 2: Summarise each class on its own (filter RemoveWithValues, one species at a time)
for species in 1 2 3; do
  weka weka.filters.unsupervised.instance.RemoveWithValues -C last -L $species -V -i $DATA/iris.arff -o iris-$species.arff
  weka weka.core.Instances iris-$species.arff
done
