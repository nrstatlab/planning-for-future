# Course 6 — Practice Questions with Solutions

Every numeric answer here was produced by the executed Python equivalents in
`labs/course-6-r/python/`.

---

## Section A — Predict the output

### Q1
```r
v <- c(10, 20, 30, 40, 50)
print(v[-2])
print(v[c(TRUE, FALSE)])
print(length(v[-1]))
```

**Answer: `10 30 40 50`, then `10 30 50`, then `4`.**

- `v[-2]` **excludes** the 2nd element. R has no negative-from-the-end
  indexing; `tail(v, 1)` gives the last element.
- `c(TRUE, FALSE)` is **recycled** to length 5 as `T F T F T`, keeping
  positions 1, 3 and 5.
- One element removed from five leaves four.

### Q2
```r
x <- c(1, 2, 3, NA, 5)
print(mean(x))
print(mean(x, na.rm = TRUE))
print(x == NA)
```

**Answer: `NA`, then `2.75`, then `NA NA NA NA NA`.**

Any arithmetic involving `NA` yields `NA` — hence the first. `na.rm = TRUE`
drops it, leaving mean(1,2,3,5) = 11/4 = 2.75. And `== NA` compares with an
unknown value, so every result is unknown. Use `is.na(x)`.

### Q3
```r
print(class(10))
print(class(10L))
print(1:3 + c(10, 20))
```

**Answer: `"numeric"`, `"integer"`, then `11 22 13` with a warning.**

`10` is a double; `10L` forces an integer. The third recycles `c(10,20)` to
`10 20 10`, giving 11, 22, 13 — and warns because 3 is not a multiple of 2.
**That warning is a bug signal**; check your lengths when you see it.

---

## Section B — Find and fix

### Q4
```r
df$grade <- if (df$marks >= 40) "Pass" else "Fail"
```
**Error:** `if` takes a **single** condition; `df$marks` is a whole column.
Modern R errors; older R silently used only the first row.
**Fix:** `df$grade <- ifelse(df$marks >= 40, "Pass", "Fail")`

### Q5
```r
library(dplyr)
result <- df %>% filter(marks > 50) + select(name, marks)
```
**Error:** `+` between `dplyr` verbs. `+` combines **ggplot2 layers**; `%>%`
chains data operations.
**Fix:** `df %>% filter(marks > 50) %>% select(name, marks)`

### Q6
```r
km <- kmeans(customers, centers = 3)
```
**Errors:** no scaling and no `nstart`.
**Fix:** `km <- kmeans(scale(customers), centers = 3, nstart = 25)`

Without `scale()` a variable in rupees swamps one in years — the variance ratio
in the lab data is about **4 billion to 1**. Without `nstart` you get whatever
single random start produced.

### Q7
```r
f <- factor(c("10", "20", "30"))
values <- as.numeric(f)
```
**Error:** returns the **level codes** `1 2 3`, not `10 20 30`.
**Fix:** `as.numeric(as.character(f))`

---

## Section C — Write the code

### Q8 — Top 3 sections by average marks, in `dplyr`

```r
students %>%
  filter(!is.na(marks)) %>%
  group_by(section) %>%
  summarise(n = n(), avg = mean(marks), .groups = "drop") %>%
  arrange(desc(avg)) %>%
  slice_head(n = 3)
```

The same six operations as the SQL you know from Course 5:
`SELECT section, AVG(marks) … GROUP BY section ORDER BY … LIMIT 3`.

### Q9 — Impute missing marks with the median, but only where sensible

```r
impute_median <- function(x, max_missing = 0.3) {
  pct <- mean(is.na(x))
  if (pct > max_missing) {
    warning(sprintf("%.0f%% missing -- too much to impute", pct * 100))
    return(x)
  }
  ifelse(is.na(x), median(x, na.rm = TRUE), x)
}
```

**Median, not mean**, because an outlier has already distorted the mean — the
lab data shows mean 79.06 against median 68.00 with one 250 present. And the
guard matters: imputing a column that is 60% missing invents most of it.

### Q10 — ggplot2: boxplot of marks by section, faceted by gender

```r
ggplot(students, aes(x = section, y = marks, fill = section)) +
  geom_boxplot(alpha = 0.7, outlier.colour = "red") +
  facet_wrap(~ gender) +
  labs(title = "Marks by section", x = "Section", y = "Marks") +
  theme_minimal() +
  theme(legend.position = "none")
```

`fill` (not `colour`) for the box interior, and the legend removed because the
x-axis already labels the sections.

---

## Section D — Long answers

### Q11 — A classifier reports 94% accuracy. Evaluate it.

Given TP = 80, FP = 20, FN = 40, TN = 860:

| Metric | Value |
|---|---|
| Accuracy | **0.940** |
| Precision | **0.800** |
| Recall | **0.667** |
| Specificity | **0.977** |
| F1 | **0.727** |

**The verdict: 94% is misleading.** 88% of these cases are negative, so
"always predict negative" already scores 0.88 — the model adds only 0.06. And
recall of 0.667 means it **misses 40 of 120 real cases**.

For disease screening that is unacceptable: lower the threshold, accept more
false positives, raise recall. Report the confusion matrix and per-class recall,
never accuracy alone.

*(These are the numbers in
`14_evaluation.py`, which
asserts them.)*

### Q12 — Explain the ARIMA workflow on a trending seasonal series

1. **Plot it.** Growing seasonal swing → multiplicative → take logs.
2. **Decompose** — `decompose()` or `stl()` to see trend, seasonal, remainder.
3. **Test stationarity** — `adf.test()` (H₀ = non-stationary) and `kpss.test()`
   (H₀ = stationary). Opposite nulls; write down which you are using.
4. **Difference** — `diff()` for the trend, `diff(lag = 12)` for seasonality.
   `ndiffs()`/`nsdiffs()` say how many.
5. **Identify orders** — ACF and PACF of the **differenced** series. PACF gives
   p, ACF gives q.
6. **Fit** — `auto.arima()` searches by AIC.
7. **Check residuals** — `checkresiduals()`. They must be white noise; you want
   a **large** Ljung-Box p-value.
8. **Forecast** — `forecast(fit, h = 24)`, back-transform with `exp()`.

**A point worth making that most answers miss:** step 5 must come *after* step
4. On the raw airline series the ACF just decays monotonically — the trend
swamps everything and the 12-month seasonality is **invisible**. Only after
differencing does the ACF oscillate, peaking at lag 12 and troughing at lag 6.
`16_arima.py` demonstrates
exactly this and asserts both patterns.

---

## Quick self-test

1. Why does `v[-1]` not give the last element?
2. What does `mean(x >= 40)` compute for a numeric vector `x`?
3. Which is `MARGIN = 2` in `apply()` — rows or columns?
4. Why must you `scale()` before `kmeans()`?
5. State the null hypothesis of the ADF test.
6. Which plot gives the AR order, and which the MA order?
7. Why is `geom_col()` sometimes needed instead of `geom_bar()`?
8. Why is `filtered()` written with parentheses in Shiny?

**Answers:** 1. Negative indexing **excludes**; use `tail(v,1)`. · 2. The
**proportion** at or above 40, since TRUE counts as 1. · 3. **Columns**. ·
4. Distance is scale-dependent; an unscaled large-range variable dominates. ·
5. **Non-stationary** (a unit root is present). · 6. **PACF** gives p, **ACF**
gives q. · 7. `geom_bar()` counts rows; `geom_col()` uses a value you supply. ·
8. It is a reactive — the parentheses fetch its current **value**.
