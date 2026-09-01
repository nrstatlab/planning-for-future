# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 8: Read and write CSV, Excel, JSON and XML
# Python equivalent: python/08_file_io.py

df <- data.frame(name = c("Ananya","Charan","Divya"),
                 section = c("A","B","B"),
                 marks = c(85, 91, 55),
                 stringsAsFactors = FALSE)

# --- CSV ---
write.csv(df, "students.csv", row.names = FALSE)
back <- read.csv("students.csv", stringsAsFactors = FALSE)
# row.names = FALSE matters: without it R writes an extra index column and
# re-reading gives you a stray "X" column you did not ask for.

library(readr)                     # faster; returns a tibble; never factorises
write_csv(df, "students2.csv"); read_csv("students2.csv")

# --- EXCEL ---
library(readxl)
# read_excel("students.xlsx", sheet = 1)
# excel_sheets("students.xlsx")    # list the sheet names first
library(writexl)
# write_xlsx(df, "students.xlsx")

# --- JSON ---
library(jsonlite)
write_json(df, "students.json", pretty = TRUE)
fromJSON("students.json")          # comes back as a data frame directly
toJSON(df, pretty = TRUE, auto_unbox = TRUE)
# JSON preserves TYPES -- numbers come back as numbers. CSV and XML do not.

# --- XML ---
library(XML)
# doc <- xmlParse("students.xml")
# xmlToDataFrame(doc)
# Alternative, often easier: library(xml2); read_xml(); xml_find_all()

# --- R's own formats ---
saveRDS(df, "students.rds"); readRDS("students.rds")   # ONE object
save(df, file = "students.RData"); load("students.RData")  # several, by name

# saveRDS/readRDS is preferred: you choose the variable name on load.
# load() silently overwrites whatever names were saved.
