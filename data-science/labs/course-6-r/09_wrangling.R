# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 9: Data wrangling with dplyr and tidyr
# Python equivalent: python/09_wrangling.py (annotated with these dplyr calls)

library(dplyr); library(tidyr)

students <- data.frame(
  name    = c("Ananya","Bhavana","Charan","Divya","Eshwar",
              "Fiona","Gopal","Harika","Ismail","Jyothi"),
  section = c("A","A","B","B","A","C","C","B","A","C"),
  hours   = c(9, 5, 11, 4, 7, 8, 3, 10, 6, 2),
  marks   = c(85, 62, 91, 55, 74, 79, 48, 88, 68, 41),
  stringsAsFactors = FALSE
)

# --- THE FIVE VERBS, chained with the pipe ---
students %>%
  filter(marks > 60) %>%                    # rows      -- SQL WHERE
  select(name, section, marks) %>%          # columns   -- SQL SELECT
  mutate(grade = case_when(                 # new column
    marks >= 90 ~ "A",
    marks >= 75 ~ "B",
    marks >= 60 ~ "C",
    TRUE        ~ "F")) %>%                 # TRUE ~ is the else branch
  arrange(desc(marks))                      # sort      -- SQL ORDER BY

# --- GROUPED SUMMARY -- SQL's GROUP BY ---
students %>%
  group_by(section) %>%
  summarise(n        = n(),
            avg      = mean(marks),
            highest  = max(marks),
            pass_pct = mean(marks >= 40) * 100,   # mean of a logical!
            .groups  = "drop") %>%
  arrange(desc(avg))

# mean() of a logical vector gives a PROPORTION, because TRUE counts as 1.
# .groups = "drop" ungroups the result -- omit it and later operations
# silently stay grouped, which is a common source of confusion.

# --- USEFUL EXTRAS ---
students %>% count(section)
students %>% distinct(section)
students %>% slice_max(marks, n = 3)
students %>% rename(score = marks)

# --- JOINS: the same seven as Course 5 ---
sections <- data.frame(section = c("A","B","C","D"),
                       teacher = c("Rao","Devi","Kumar","Reddy"))
inner_join(students, sections, by = "section")
left_join (students, sections, by = "section")
anti_join (sections, students, by = "section")   # section D has no students

# --- RESHAPING with tidyr ---
wide <- data.frame(name = c("A","B"), maths = c(85,72),
                   science = c(78,88), english = c(92,65))

long <- wide %>%
  pivot_longer(cols = c(maths, science, english),
               names_to = "subject", values_to = "marks")
long           # 6 rows: one per student-subject pair

long %>% pivot_wider(names_from = subject, values_from = marks)   # back again

# ggplot2 WANTS LONG DATA. That is the practical reason this matters:
# to draw one bar per subject, subject must be a COLUMN, not three columns.
