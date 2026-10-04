#!/usr/bin/env bash
# Experiment 4 in WEKA 3.8.7, from the command line: attribute selection and PCA.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 04_feature_selection_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Rank the attributes by information gain (InfoGainAttributeEval, Ranker)
weka weka.attributeSelection.InfoGainAttributeEval -s "weka.attributeSelection.Ranker" -i $DATA/iris.arff

# Step 2: Choose a subset with a wrapper round J48 (WrapperSubsetEval, BestFirst)
weka weka.attributeSelection.WrapperSubsetEval -B weka.classifiers.trees.J48 -F 5 -R 1 -s "weka.attributeSelection.BestFirst" -i $DATA/iris.arff

# Step 3: Principal components of the four measurements, with their eigenvalues
# (PrincipalComponents, Ranker). The class is removed first: given it, this
# evaluator mixes the species into the components as three more numbers.
weka weka.filters.unsupervised.attribute.Remove -R last -i $DATA/iris.arff -o iris-measurements.arff
weka weka.attributeSelection.PrincipalComponents -R 0.95 -s "weka.attributeSelection.Ranker" -i iris-measurements.arff

# Step 4: Replace the attributes by the components, as the Preprocess filter does
# (filters/unsupervised/attribute/PrincipalComponents, varianceCovered = 0.95)
weka weka.filters.unsupervised.attribute.PrincipalComponents -R 0.95 -c last -i $DATA/iris.arff -o iris-pca.arff
grep "^@attribute" iris-pca.arff
