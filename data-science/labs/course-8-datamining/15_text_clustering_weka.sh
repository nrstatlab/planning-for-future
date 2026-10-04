#!/usr/bin/env bash
# Experiment 15 in WEKA 3.8.7, from the command line: text to TF-IDF vectors, then K-Means.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 15_text_clustering_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Turn the documents into TF-IDF vectors (filter StringToWordVector)
# wordsToKeep is 100 here, not the click-path's 1000, so that K-Means's table of
# centroids, one row per word, fits on a page. It works the same either way.
weka weka.filters.unsupervised.attribute.StringToWordVector -T -I -L -W 100 -R first -i $DATA/ReutersCorn-train.arff -o reuters-tfidf.arff
grep -c "^@attribute" reuters-tfidf.arff

# Step 2: Cluster the vectors into 2 with K-Means, and compare with the class (SimpleKMeans)
weka weka.clusterers.SimpleKMeans -N 2 -S 10 -t reuters-tfidf.arff -c first   # the class comes first now
