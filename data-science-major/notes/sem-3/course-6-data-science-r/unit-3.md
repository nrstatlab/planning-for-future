# Unit 3 — Data Handling and Visualization in R

**Syllabus topics:** Data frames, lists, matrices. Data wrangling with
`dplyr` and `tidyr`. Handling missing data. Working with date/time in R.
Visualization with `ggplot2` — grammar of graphics, aesthetics, geometries,
scales. Faceting and layering techniques. Visualizing categorical and numerical
data. Customizing and exporting plots.

---

This is the unit that makes R worth learning. `dplyr` and `ggplot2` are the two
best-designed libraries in either language, and this is the material you will
still be using in five years.

## 3.1 The pipe

Before anything else, learn the pipe. It is what makes `dplyr` readable.

```r
# Without the pipe -- read inside-out, which is backwards
arrange(summarise(group_by(filter(df, marks > 40), section), avg = mean(marks)), desc(avg))

# With the pipe -- read top to bottom, like a sentence
df %>%
  filter(marks > 40) %>%
  group_by(section) %>%
  summarise(avg = mean(marks)) %>%
  arrange(desc(avg))
```

`x %>% f(y)` means `f(x, y)` — the left side becomes the first argument of the
right. Read `%>%` aloud as **"and then"**.

R 4.1 added a native pipe `|>` with the same meaning. `%>%` (from `magrittr`,
re-exported by `dplyr`) remains more common and slightly more flexible.
**Ctrl+Shift+M** types it in RStudio.

## 3.2 The five `dplyr` verbs

### 🎯 The big idea

Almost every data-manipulation task is a combination of five operations. `dplyr`
gives each one a verb, and the pipe chains them.

| Verb | Does | SQL equivalent |
|---|---|---|
| `filter()` | Keep **rows** matching a condition | `WHERE` |
| `select()` | Keep **columns** | `SELECT` |
| `mutate()` | Create or modify columns | computed column |
| `arrange()` | Sort rows | `ORDER BY` |
| `summarise()` | Collapse to summary statistics | aggregate functions |
| `group_by()` | Split into groups for the above | `GROUP BY` |

**The SQL column is not decoration** — you learned all of this in Course 5. A
`dplyr` chain and a SQL query express the same operations; recognising that
makes both easier.

```r
library(dplyr)

students %>%
  filter(marks > 40, section == "A") %>%     # comma = AND
  select(name, marks, section) %>%
  mutate(grade = case_when(
    marks >= 90 ~ "A",
    marks >= 75 ~ "B",
    marks >= 60 ~ "C",
    TRUE        ~ "F"                         # the else branch
  )) %>%
  arrange(desc(marks))
```

### `case_when` — the readable nested ifelse

`case_when` replaces the four-deep `ifelse` stack from Unit 2. Conditions are
tested top to bottom; `TRUE ~ value` is the catch-all. This is `dplyr`'s
equivalent of SQL's `CASE`.

### Grouped summaries

```r
students %>%
  group_by(section) %>%
  summarise(
    n        = n(),
    avg      = mean(marks, na.rm = TRUE),
    highest  = max(marks),
    pass_pct = mean(marks >= 40) * 100        # mean of a logical = proportion
  ) %>%
  arrange(desc(avg))
```

**`mean()` of a logical vector gives a proportion**, because TRUE counts as 1
and FALSE as 0. `mean(marks >= 40) * 100` is the pass percentage in one
expression — an idiom worth remembering.

**Always `ungroup()`** after a `group_by()` if the result feeds further
operations; a lingering grouping causes surprising results downstream.

### Useful extras

```r
distinct(df, section)              # unique rows -- SQL's DISTINCT
slice_max(df, marks, n = 3)        # top 3 rows by marks
count(df, section)                 # shorthand for group_by + summarise(n())
rename(df, score = marks)          # rename a column
relocate(df, marks, .before = name)  # reorder columns
```

### Joins — the same seven from Course 5

```r
inner_join(students, sections, by = "section_id")
left_join (students, sections, by = "section_id")
right_join(students, sections, by = "section_id")
full_join (students, sections, by = "section_id")
semi_join (students, sections, by = "section_id")   # rows in x with a match
anti_join (students, sections, by = "section_id")   # rows in x with NO match
```

`anti_join` has no direct SQL keyword and is genuinely useful: "which students
have no matching section record?" is a data-quality question you will ask often.

## 3.3 `tidyr` — reshaping

### 🎯 The big idea

**Tidy data** has one variable per column, one observation per row, one value
per cell. Most real data does not arrive that way, and `tidyr` reshapes it.

### Wide vs long

**Wide** — one row per student, one column per subject:

| name | maths | science | english |
|---|---|---|---|
| A | 85 | 78 | 92 |
| B | 72 | 88 | 65 |

**Long** — one row per student-subject pair:

| name | subject | marks |
|---|---|---|
| A | maths | 85 |
| A | science | 78 |
| A | english | 92 |
| B | maths | 72 |
| … | … | … |

```r
library(tidyr)

long <- wide %>%
  pivot_longer(cols = c(maths, science, english),
               names_to = "subject", values_to = "marks")

wide <- long %>%
  pivot_wider(names_from = subject, values_from = marks)
```

**`ggplot2` wants long data.** That is the practical reason this matters: to
plot marks by subject with one bar per subject, the subject must be a *column*,
not spread across three. Almost every "why won't my plot work" question is
really "your data is wide and should be long".

*(Older code uses `gather()` and `spread()`. They still work but are retired —
`pivot_longer`/`pivot_wider` replaced them and are clearer.)*

### Other `tidyr` verbs

```r
separate(df, full_name, into = c("first", "last"), sep = " ")
unite(df, full_name, first, last, sep = " ")
drop_na(df)                       # rows with any NA
replace_na(df, list(marks = 0))   # fill NAs per column
fill(df, section)                 # carry the last value forward
```

## 3.4 Handling missing data

### Finding it

```r
sum(is.na(df))                        # total NAs
colSums(is.na(df))                    # per column -- the useful one
mean(is.na(df$marks)) * 100           # percentage missing in a column
complete.cases(df)                    # rows with no NA at all
```

### Dealing with it

| Strategy | R | When it is right |
|---|---|---|
| **Remove rows** | `na.omit(df)`, `drop_na(df)` | Few missing, and missing at random |
| **Remove column** | `df %>% select(-col)` | The column is mostly empty |
| **Mean/median impute** | `ifelse(is.na(x), mean(x, na.rm=TRUE), x)` | Numeric, roughly symmetric |
| **Mode impute** | manual | Categorical |
| **Forward fill** | `tidyr::fill()` | Time series |
| **Model-based** | `mice`, `missForest` packages | Missingness has structure |
| **Keep as a category** | `"Unknown"` | Missingness is itself informative |

### 💡 Why "just delete the rows" is often wrong

Deleting incomplete rows is only safe when data is **Missing Completely At
Random (MCAR)**. If it is not, deletion introduces bias.

Suppose high earners decline to state their income. Drop those rows and your
average income is now too low — and every conclusion downstream is wrong in the
same direction. The missingness carried information, and deletion threw it away.

The three mechanisms, worth naming in an exam:

| Mechanism | Meaning |
|---|---|
| **MCAR** | Missingness unrelated to anything — safe to delete |
| **MAR** | Related to *observed* variables — imputation can work |
| **MNAR** | Related to the *missing value itself* — hardest; needs domain thought |

The income example is **MNAR**, the difficult case.

## 3.5 Dates and times

```r
as.Date("2026-08-26")                       # ISO -- the safe default
as.Date("26/08/2026", format = "%d/%m/%Y")
Sys.Date(); Sys.time()

library(lubridate)                          # far easier than base R
dmy("26-08-2026"); ymd("2026-08-26")
year(d); month(d); day(d); wday(d, label = TRUE)
d + days(30); d %m+% months(1)
difftime(d2, d1, units = "days")
```

| Code | Means |
|---|---|
| `%Y` | 4-digit year |
| `%y` | 2-digit year |
| `%m` | month number |
| `%B` / `%b` | full / abbreviated month name |
| `%d` | day of month |
| `%A` / `%a` | full / abbreviated weekday |
| `%H:%M:%S` | time |

**Always store dates as `Date`, never as text.** A character date sorts
alphabetically — `"10/01/2026"` before `"02/01/2026"` — and cannot be
subtracted. This is the same discipline as Course 5's date columns.

`%m+%` adds months safely: 31 January `%m+% months(1)` gives 28 February rather
than an invalid date.

## 3.6 `ggplot2` and the grammar of graphics

### 🎯 The big idea

Every statistical graphic is built from the same handful of components. Name the
data, say which variables map to which visual properties, choose a shape to draw
— and the plot follows. That is the **grammar of graphics**.

### The seven components

| Component | Role | Required? |
|---|---|---|
| **Data** | The data frame | Yes |
| **Aesthetics** (`aes`) | Variable → visual property (x, y, colour, size, shape, fill, alpha) | Yes |
| **Geometries** (`geom_`) | The marks drawn — points, bars, lines | Yes |
| **Statistics** (`stat_`) | Transformations — counts, bins, smoothers | Often implicit |
| **Scales** | How values map to the property — axes, colour scales | Defaults supplied |
| **Coordinates** | Cartesian, polar, flipped | Defaults supplied |
| **Facets** | Split into sub-plots | Optional |
| **Themes** | Non-data appearance | Optional |

```r
library(ggplot2)

ggplot(data = students, aes(x = hours, y = marks, colour = section)) +
  geom_point(size = 3, alpha = 0.7) +
  geom_smooth(method = "lm", se = TRUE) +
  labs(title = "Marks against study hours",
       x = "Hours studied per week", y = "Marks out of 100",
       colour = "Section") +
  theme_minimal()
```

**Layers combine with `+`, not `%>%`.** Mixing the two is the single most common
`ggplot2` error: the pipe passes data along a chain, `+` adds layers to a plot.

### Choosing a geometry

| Geometry | Shows | Data |
|---|---|---|
| `geom_point()` | Relationship | 2 numeric |
| `geom_line()` | Trend over an ordered variable | time + numeric |
| `geom_bar()` | Counts per category | 1 categorical |
| `geom_col()` | Values per category | categorical + numeric |
| `geom_histogram()` | Distribution | 1 numeric |
| `geom_boxplot()` | Distribution and outliers by group | categorical + numeric |
| `geom_violin()` | Distribution shape by group | categorical + numeric |
| `geom_density()` | Smoothed distribution | 1 numeric |
| `geom_smooth()` | Fitted trend | 2 numeric |
| `geom_tile()` | Heatmap | 2 categorical + numeric |

**`geom_bar()` vs `geom_col()`** is a reliable two-mark question. `geom_bar()`
counts rows for you (its default stat is `"count"`). `geom_col()` uses a value
you supply as the height (`stat = "identity"`). Wanting a bar of a value you
already have and reaching for `geom_bar()` is why people get a bar of height 1.

### Faceting — small multiples

```r
p + facet_wrap(~ section)                  # one panel per section, wrapped
p + facet_grid(gender ~ section)           # a grid: rows × columns
p + facet_wrap(~ section, scales = "free_y")   # independent y axes
```

Faceting is often better than colouring by group: with six or more groups,
colours become indistinguishable while six small panels stay readable.

### Scales, labels and themes

```r
+ scale_x_continuous(limits = c(0, 100), breaks = seq(0, 100, 20))
+ scale_y_log10()
+ scale_colour_brewer(palette = "Set2")
+ scale_fill_manual(values = c("A" = "#0f4c81", "B" = "#1e7fbf"))
+ coord_flip()                              # horizontal bars
+ theme_minimal() / theme_bw() / theme_classic()
+ theme(legend.position = "bottom",
        axis.text.x = element_text(angle = 45, hjust = 1))
```

### Exporting

```r
ggsave("plot.png", plot = p, width = 8, height = 5, dpi = 300)
ggsave("plot.pdf", plot = p, width = 8, height = 5)    # vector -- scales cleanly
```

**`ggsave` defaults to the last plot displayed** if you omit `plot =`. Specify
it explicitly in scripts, or you will save the wrong figure. Use PDF or SVG for
anything going into a printed report.

---

## 📝 Practice problems

### Problem 1

Write a `dplyr` chain that, from a data frame `sales(region, product, month, revenue)`,
finds the top 3 regions by total revenue in 2025.

**Solution.**

```r
sales %>%
  filter(format(month, "%Y") == "2025") %>%
  group_by(region) %>%
  summarise(total = sum(revenue, na.rm = TRUE), .groups = "drop") %>%
  arrange(desc(total)) %>%
  slice_head(n = 3)
```

Reading it as a sentence: take sales, **and then** keep 2025, **and then**
group by region, **and then** total the revenue, **and then** sort descending,
**and then** take the first three.

`.groups = "drop"` ungroups the result — without it the data frame stays grouped
and later operations behave unexpectedly.

The SQL you already know:

```sql
SELECT region, SUM(revenue) AS total FROM sales
WHERE YEAR(month) = 2025
GROUP BY region ORDER BY total DESC LIMIT 3;
```

Same six operations, same order.

### Problem 2

A data frame has 5% missing values in `marks` and 60% missing in `email`.
Recommend a strategy for each, with justification.

**Solution.**

**`marks` — 5% missing.** Small enough that either deletion or imputation is
defensible, so the question is *why* they are missing. If students were absent
at random, median imputation is reasonable and preserves sample size. If the
weakest students skipped the test, the data is **MNAR** — imputing the median
would inflate the apparent performance of exactly the group you care about. In
that case keep the rows and add an `was_absent` indicator column, so the model
can use the missingness itself as a signal.

**`email` — 60% missing.** Do not impute; there is no meaningful "average
email". Two options: drop the column if it plays no analytical role, or convert
it to a binary `has_email` feature. The latter is often surprisingly predictive
— customers who supply an email are usually more engaged.

**The general rule:** ask *why* the data is missing before choosing a method.
Percentage alone does not determine the answer.

### Problem 3

Write the `ggplot2` code for a boxplot of marks by section, coloured by section,
faceted by gender, with a title and a minimal theme.

**Solution.**

```r
ggplot(students, aes(x = section, y = marks, fill = section)) +
  geom_boxplot(alpha = 0.7, outlier.colour = "red") +
  facet_wrap(~ gender) +
  labs(title    = "Distribution of marks by section",
       subtitle = "Split by gender",
       x = "Section", y = "Marks out of 100", fill = "Section") +
  theme_minimal() +
  theme(legend.position = "none")
```

Two points that earn marks: **`fill`, not `colour`** — for a boxplot, `colour`
sets the outline and `fill` the body. And `legend.position = "none"` because the
x-axis already labels the sections, making the legend redundant. Removing
redundant ink is a real design principle, not a nicety.

---

## Exam questions from this unit

**Two marks**

1. What does the `%>%` operator do?
2. Distinguish `geom_bar()` from `geom_col()`.
3. What is tidy data?
4. Why does `ggplot2` prefer long-format data?
5. Distinguish `filter()` from `select()`.

**Five marks**

1. Explain the five `dplyr` verbs with examples.
2. Explain the grammar of graphics and its components.
3. Explain `pivot_longer()` and `pivot_wider()` with an example.
4. Explain strategies for handling missing data and when each applies.

**Ten marks**

1. Explain data wrangling in R with `dplyr` and `tidyr`, with a complete worked
   pipeline.
2. Explain `ggplot2` in detail — grammar, aesthetics, geometries, scales,
   faceting, themes and exporting.

## Mistakes that cost marks

- Using `%>%` between `ggplot2` layers instead of `+`
- `geom_bar()` when you have values already and need `geom_col()`
- Plotting wide data and wondering why the groups will not separate
- Forgetting `na.rm = TRUE` inside `summarise()`
- Leaving a data frame grouped after `group_by()`
- Storing dates as character strings
- Confusing `colour` (outline) with `fill` (interior)
- Imputing the mean without asking why the data is missing
