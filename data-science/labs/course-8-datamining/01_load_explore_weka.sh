#!/usr/bin/env bash
# Experiment 1 in WEKA 3.8.7, from the command line: load and explore ARFF and CSV.
# Each command runs the WEKA class that the Explorer runs for the same choice, and prints
# what the Explorer shows in its output pane. The click-path is on the lab page.
# Needs tools/data-science/setup_weka.sh; run as  bash 01_load_explore_weka.sh
set -euo pipefail
source "$(dirname "$0")/weka.sh"

# Step 1: Load the data, and read the Preprocess panel's summary (Open file...)
weka weka.core.Instances $DATA/weather.nominal.arff

# Step 2: Load the numeric version, whose temperature and humidity are numbers
weka weka.core.Instances $DATA/weather.numeric.arff

# Step 3: Save it as CSV, and load the CSV back (Save..., then Open file... as CSV)
weka weka.core.converters.CSVSaver -i $DATA/weather.numeric.arff -o weather.csv
cat weather.csv
weka weka.core.Instances weather.csv

# Step 4: Turn a numeric attribute into a nominal one (filter NumericToNominal)
weka weka.filters.unsupervised.attribute.NumericToNominal -R 2 -i weather.csv -o weather-nominal-temp.arff
weka weka.core.Instances weather-nominal-temp.arff
