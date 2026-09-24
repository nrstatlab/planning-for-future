# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 12: Visualise data with ggplot2
# No Python equivalent -- this demonstrates ggplot2's grammar specifically.

library(ggplot2)

students <- data.frame(
  name    = c("Ananya","Bhavana","Charan","Divya","Eshwar",
              "Fiona","Gopal","Harika","Ismail","Jyothi"),
  section = c("A","A","B","B","A","C","C","B","A","C"),
  gender  = c("F","F","M","F","M","F","M","F","M","F"),
  hours   = c(9, 5, 11, 4, 7, 8, 3, 10, 6, 2),
  marks   = c(85, 62, 91, 55, 74, 79, 48, 88, 68, 41)
)

# --- SCATTER: two numeric variables ---
ggplot(students, aes(x = hours, y = marks, colour = section)) +
  geom_point(size = 3, alpha = 0.8) +
  geom_smooth(method = "lm", se = TRUE, colour = "grey40") +
  labs(title = "Marks against study hours",
       x = "Hours studied per week", y = "Marks out of 100",
       colour = "Section") +
  theme_minimal()

# --- BAR: counts per category ---
ggplot(students, aes(x = section, fill = section)) +
  geom_bar() +                       # geom_bar COUNTS rows for you
  labs(title = "Students per section") +
  theme_minimal() + theme(legend.position = "none")

# --- COLUMN: a value you already have ---
avg <- aggregate(marks ~ section, data = students, FUN = mean)
ggplot(avg, aes(x = section, y = marks, fill = section)) +
  geom_col() +                       # geom_col uses YOUR value as the height
  labs(title = "Mean marks per section")

# geom_bar() vs geom_col() is the classic exam question:
#   geom_bar  default stat = "count"    -> it counts rows
#   geom_col  default stat = "identity" -> it uses your y value
# Reaching for geom_bar when you already have the value gives bars of height 1.

# --- HISTOGRAM: distribution of one numeric variable ---
ggplot(students, aes(x = marks)) +
  geom_histogram(bins = 6, fill = "#1e7fbf", colour = "white") +
  labs(title = "Distribution of marks")

# --- BOXPLOT: distribution by group, with outliers ---
ggplot(students, aes(x = section, y = marks, fill = section)) +
  geom_boxplot(alpha = 0.7, outlier.colour = "red") +
  facet_wrap(~ gender) +             # small multiples
  labs(title = "Marks by section", subtitle = "Split by gender") +
  theme_minimal() + theme(legend.position = "none")

# NOTE for boxplots: fill = interior, colour = outline. Using colour where you
# meant fill gives an outlined but empty box.

# --- EXPORT ---
p <- ggplot(students, aes(hours, marks)) + geom_point()
ggsave("marks_plot.png", plot = p, width = 8, height = 5, dpi = 300)
ggsave("marks_plot.pdf", plot = p, width = 8, height = 5)   # vector, for print

# Always pass plot = explicitly. ggsave() otherwise saves the LAST plot
# displayed, which in a script is rarely the one you meant.

# LAYERS COMBINE WITH +, NOT %>%. Mixing them is the commonest ggplot2 error.
