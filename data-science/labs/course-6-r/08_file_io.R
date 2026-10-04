# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 8: Read and write CSV, Excel, JSON and XML
# Python equivalent: python/08_file_io.py

# Step 1: Make a small data frame
df <- data.frame(name = c("Ananya","Charan","Divya"),
                 section = c("A","B","B"),
                 marks = c(85, 91, 55),
                 stringsAsFactors = FALSE)

# --- CSV ---
# Step 2: Write and read CSV
write.csv(df, "students.csv", row.names = FALSE)
back <- read.csv("students.csv", stringsAsFactors = FALSE)
# row.names = FALSE matters: without it R writes an extra index column and
# re-reading gives you a stray "X" column you did not ask for.

library(readr)                     # faster; returns a tibble; never factorises
write_csv(df, "students2.csv"); read_csv("students2.csv")

# --- EXCEL ---
# Step 3: Load the Excel packages
library(readxl)
# read_excel("students.xlsx", sheet = 1)
# excel_sheets("students.xlsx")    # list the sheet names first
library(writexl)
# write_xlsx(df, "students.xlsx")

# --- JSON ---
# Step 4: Write and read JSON
library(jsonlite)
write_json(df, "students.json", pretty = TRUE)
fromJSON("students.json")          # comes back as a data frame directly
toJSON(df, pretty = TRUE, auto_unbox = TRUE)
# JSON preserves TYPES -- numbers come back as numbers. CSV and XML do not.

# --- XML ---
# Step 5: Load the XML package
library(XML)
# doc <- xmlParse("students.xml")
# xmlToDataFrame(doc)
# Alternative, often easier: library(xml2); read_xml(); xml_find_all()

# --- R's own formats ---
# Step 6: Save and load R's own formats
saveRDS(df, "students.rds"); readRDS("students.rds")   # ONE object
save(df, file = "students.RData"); load("students.RData")  # several, by name

# saveRDS/readRDS is preferred: you choose the variable name on load.
# load() silently overwrites whatever names were saved.
