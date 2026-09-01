# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 11: Working with dates and times
# Python equivalent: python/11_dates.py

# --- BASE R ---
d <- as.Date("2026-08-26")                       # ISO is the safe default
d2 <- as.Date("26/08/2026", format = "%d/%m/%Y")
Sys.Date(); Sys.time()

format(d, "%d-%m-%Y")      # "26-08-2026"
format(d, "%d %B %Y")      # "26 August 2026"
weekdays(d); months(d)

d + 30                     # date arithmetic works directly
difftime(as.Date("2026-12-25"), d, units = "days")   # 121 days

# --- lubridate: much easier ---
library(lubridate)
ymd("2026-08-26"); dmy("26-08-2026"); mdy("08-26-2026")
year(d); month(d); day(d); wday(d, label = TRUE)
d + days(30); d + months(1); d + years(1)
d %m+% months(1)     # SAFE month addition
# 31 Jan %m+% months(1) gives 28 Feb, not an invalid 31 Feb.

# --- WHY DATES MUST NOT BE STORED AS TEXT ---
as_text <- c("10/01/2026", "02/01/2026", "21/12/2025")
sort(as_text)
#   "02/01/2026" "10/01/2026" "21/12/2025"
#   ALPHABETICAL: the 2025 date sorts LAST. This is wrong and silent.

as_dates <- dmy(as_text)
sort(as_dates)
#   "2025-12-21" "2026-01-02" "2026-01-10"   <- correct chronological order

# Same lesson as Course 5: a date column stored as VARCHAR sorts and compares
# alphabetically, which is almost never what you want.

# --- FORMAT CODES (also used by format() in base R) ---
#   %Y 4-digit year   %y 2-digit year   %m month number
#   %B full month     %b abbreviated    %d day of month
#   %A full weekday   %a abbreviated    %H:%M:%S time
