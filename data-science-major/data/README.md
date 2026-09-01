# Practice datasets

One CSV per method, or close to it. Every file was **generated from a known truth** — the regression file from a slope of 6.0, the AR(2) series from phi = (0.6, −0.3), the three clusters from centres the generator chose — so you can **score your answer**, not merely produce one.

`tools/check_datasets.py` reads every file back off disk and recovers its planted truth. A dataset whose right answer nobody has checked is worse than no dataset, because a wrong answer then looks like a lesson.

```bash
python3 tools/make_datasets.py    # regenerate (deterministic)
python3 tools/check_datasets.py   # prove each truth is recoverable
```

**50 datasets.** Seeded, so regenerating gives byte-identical files; a diff after regenerating means something changed that should not have.

---

## Used by several courses

### `data/shared/flowers.csv`

90 rows · `species` · `sepal_length` · `sepal_width` · `petal_length` · `petal_width`

**Practise:** k-NN; decision trees (ID3, C4.5, CART); Naive Bayes; k-Means; hierarchical clustering; PCA; train/test split.

Built from three known centres. 'alba' separates cleanly; the other two overlap on purpose, so a perfect score means a leak.

<details><summary>What it was built from</summary>

- `rows` — 90
- `classes` — 3
- `per_class` — 30
- `separable_class` — alba
- `overlapping_pair` — ['borealis', 'carinata']
- `centres` — {'alba': [5.0, 3.4, 1.5, 0.2], 'borealis': [6.0, 2.8, 4.4, 1.3], 'carinata': [6.6, 3.0, 5.6, 2.0]}

</details>

### `data/shared/sales-transactions.csv`

9 rows · `product` · `region` · `date` · `quantity` · `unit_price` · `revenue`

**Practise:** pivot tables; GROUP BY; MapReduce; DAX measures; Hive and Spark aggregation; OLAP roll-up.

The same nine rows Courses 1, 8, 9, 11, 12 B and 15 B all analyse. Six different engines reach the same South total, which is only meaningful because they read the same rows.

<details><summary>What it was built from</summary>

- `total_revenue` — 12880
- `south_revenue` — 10360
- `north_revenue` — 2520
- `best_product` — Rice 5kg
- `best_product_revenue` — 5600
- `transactions` — 9

</details>

---

## Course 1 — Office Automation

### `data/course-1-office/budget.csv`

7 rows · `category` · `amount`

**Practise:** Goal Seek; Scenario Manager; one-variable data table.

A savings RATE of 30% is not linear in income: the answer is 33000/0.70, which is not a figure you can read off the sheet.

<details><summary>What it was built from</summary>

- `income` — 45000
- `total_expenses` — 33000
- `savings` — 12000
- `savings_rate` — 0.266667
- `income_for_20000_savings` — 53000
- `income_for_30pct_rate` — 47142.857142857

</details>

### `data/course-1-office/class-results.csv`

20 rows · `roll` · `name` · `maths` · `physics` · `chemistry` · `english` · `computers`

**Practise:** IF / nested IF / IFS; AND, OR, IFERROR; MIN, MAX, COUNTIF; descriptive statistics.

Grade on the AVERAGE. Point the formula at the total and 19 of the 20 get an A, including the student who failed all five papers.

<details><summary>What it was built from</summary>

- `students` — 20
- `subjects` — 5
- `grades_on_average` — {'A': 3, 'B': 6, 'C': 4, 'D': 6, 'F': 1}
- `failed_a_subject` — ['Divya', 'Ishita', 'Kavya', 'Rahul']
- `hardest_paper` — maths
- `maths_mean` — 67.0
- `grades_if_graded_on_total` — {'A': 19, 'B': 1}

</details>

### `data/course-1-office/payroll.csv`

6 rows · `name` · `emp_id` · `department` · `basic_pay`

**Practise:** SUM, AVERAGE, absolute references; VLOOKUP / XLOOKUP / INDEX+MATCH; conditional formatting.

Deduction is 10% of (Basic + DA), not of Basic -- which is why Net is 1.32 x Basic and not 1.35 x. Check one row and you have checked the sheet.

<details><summary>What it was built from</summary>

- `employees` — 6
- `total_basic` — 200500
- `da_rate` — 0.3
- `hra_rate` — 0.15
- `deduction_rate` — 0.1
- `gross_is` — 1.45 x basic
- `net_is` — 1.32 x basic
- `total_net` — 264660

</details>

---

## Course 2 — Problem Solving Using C

### `data/course-2-c/employee-records.csv`

10 rows · `emp_no` · `name` · `salary` · `years` · `department`

**Practise:** struct and array of structs; fgets, sscanf, strtok; fopen / fscanf / fprintf; string functions (strlen, strcpy, strcmp); sorting an array of structs; linear and binary search.

Ten records for the file-handling and structure practicals. The names contain spaces on purpose: scanf("%s") reads 'Anitha' and leaves 'Rao' in the buffer, which is the bug every student writes once.

<details><summary>What it was built from</summary>

- `rows` — 10
- `total_salary` — 331500
- `highest_paid` — Faisal Ahmed
- `longest_name_length` — 13
- `departments` — 4
- `note_for_c` — names contain a space, so scanf("%s") stops at the first one -- use fgets and strtok

</details>

---

## Course 3 — Python Programming

### `data/course-3-python/students.csv`

25 rows · `roll` · `name` · `python` · `maths` · `statistics`

**Practise:** file handling; the csv module; dictionaries; list comprehensions; exception handling.

Read it with csv.DictReader, total per student, and handle a missing file with try/except -- the three things practical 11 asks for.

<details><summary>What it was built from</summary>

- `rows` — 25
- `grand_total` — 5121
- `mean_of_all_marks` — 68.28

</details>

---

## Course 4 — Statistical Foundations

### `data/course-4-stats/before-after.csv`

20 rows · `subject` · `before` · `after`

**Practise:** paired t-test; one-sample t-test on the differences; Wilcoxon signed-rank test.

The pairing is the point: run an INDEPENDENT t-test on the same two columns and watch the evidence weaken, because the between-subject variation is no longer removed.

<details><summary>What it was built from</summary>

- `n` — 20
- `true_mean_gain` — 4.0
- `gain_sd` — 2.5
- `expect` — paired t-test rejects; the unpaired test is weaker

</details>

### `data/course-4-stats/fertiliser-yield.csv`

36 rows · `fertiliser` · `yield`

**Practise:** one-way ANOVA; the F distribution; post-hoc comparison; CRD in Design of Experiments.

Three fertilisers, twelve plots each. A and B are close; C is clearly higher. ANOVA says 'not all equal' -- it does not say WHICH, which is why the post-hoc test exists.

<details><summary>What it was built from</summary>

- `groups` — 3
- `n_per_group` — 12
- `true_means` — {'A': 40.0, 'B': 44.0, 'C': 50.0}
- `within_sd` — 4.0
- `expect` — one-way ANOVA rejects; C differs most

</details>

### `data/course-4-stats/heights.csv`

60 rows · `student_id` · `height_cm`

**Practise:** mean, median, mode; variance and standard deviation; skewness and kurtosis; the normal distribution; one-sample t-test against 165.

Drawn from N(165, 8). The sample mean will not be exactly 165 -- the gap between it and the population value IS the sampling error the course is about.

<details><summary>What it was built from</summary>

- `n` — 60
- `population_mean` — 165.0
- `population_sd` — 8.0
- `sample_mean` — 165.368333
- `sample_sd` — 7.502689

</details>

### `data/course-4-stats/preference-survey.csv`

140 rows · `gender` · `preference`

**Practise:** chi-square test of independence; contingency tables; expected frequencies; Yates' correction.

One row per respondent, so you must build the contingency table yourself first -- which is the half of the question students skip.

<details><summary>What it was built from</summary>

- `respondents` — 140
- `table` — {'male/tea': 45, 'male/coffee': 25, 'female/tea': 20, 'female/coffee': 50}
- `expect` — chi-square test of independence rejects
- `degrees_of_freedom` — 1

</details>

### `data/course-4-stats/study-hours-marks.csv`

40 rows · `hours` · `marks`

**Practise:** scatter plot; Karl Pearson's correlation coefficient; least-squares regression; the two regression lines; coefficient of determination.

Built from marks = 12 + 6 x hours + noise. Fit it and you should recover a slope near 6 -- and the two regression lines (y on x, x on y) will NOT coincide.

<details><summary>What it was built from</summary>

- `n` — 40
- `true_intercept` — 12.0
- `true_slope` — 6.0
- `noise_sd` — 4.0
- `expect_r_above` — 0.9
- `identity_to_check` — R-squared = r-squared, and t-squared = F

</details>

### `data/course-4-stats/treatment-groups.csv`

50 rows · `group` · `score`

**Practise:** independent two-sample t-test; F-test for equal variances; confidence interval for a difference of means; Mann-Whitney U (non-parametric).

A real difference of 5 marks with sd 6 and n=25 per group. The test SHOULD reject -- if yours does not, check which tail you used.

<details><summary>What it was built from</summary>

- `n_per_group` — 25
- `control_mean` — 70.0
- `treatment_mean` — 75.0
- `true_difference` — 5.0
- `common_sd` — 6.0
- `expect` — reject H0 at 5%

</details>

---

## Course 5 — Database Management Systems

### `data/course-5-dbms/assignments.csv`

7 rows · `emp_id` · `project_id` · `hours_per_week`

**Practise:** many-to-many resolution; composite keys; EXISTS / NOT EXISTS; division queries.

The junction table. 'Which employees work on NO project?' is the NOT EXISTS question, and E106 is the answer.

<details><summary>What it was built from</summary>

- `rows` — 7
- `composite_primary_key` — ['emp_id', 'project_id']
- `employees_on_two_projects` — ['E104']
- `employees_on_no_project` — ['E106']

</details>

### `data/course-5-dbms/departments.csv`

4 rows · `dept_id` · `dept_name` · `city`

**Practise:** CREATE TABLE; primary keys; SELECT ... WHERE.

The one-side of the one-to-many with employees.

<details><summary>What it was built from</summary>

- `rows` — 4
- `primary_key` — dept_id

</details>

### `data/course-5-dbms/employees.csv`

7 rows · `emp_id` · `name` · `dept_id` · `salary` · `hired` · `manager_id`

**Practise:** INNER / LEFT / RIGHT / FULL JOIN; self join; GROUP BY with HAVING; subqueries; referential integrity.

manager_id is a self-referencing foreign key and two rows are NULL. An INNER self-join loses those two; a LEFT join keeps them -- that difference is the exam question.

<details><summary>What it was built from</summary>

- `rows` — 7
- `foreign_keys` — ['dept_id -> departments', 'manager_id -> employees']
- `employees_with_no_manager` — 2
- `total_salary` — 230500
- `inner_join_with_departments_rows` — 7
- `self_join_manager_rows` — 5

</details>

### `data/course-5-dbms/projects.csv`

4 rows · `project_id` · `project_name` · `dept_id` · `budget`

**Practise:** aggregate functions; ORDER BY; correlated subqueries.

Every project belongs to a department, so a three-table join runs employees -> departments -> projects.

<details><summary>What it was built from</summary>

- `rows` — 4
- `total_budget` — 1810000

</details>

### `data/course-5-dbms/unnormalised-orders.csv`

4 rows · `order_id` · `order_date` · `customer_name` · `customer_city` · `customer_phone` · `items` · `quantities` · `unit_prices`

**Practise:** 1NF, 2NF, 3NF, BCNF; functional dependencies; decomposition; update, insert and delete anomalies.

Normalise it to 3NF and count the tables. Then change Anitha's phone number in the ORIGINAL file and see how many rows you have to touch -- that is the update anomaly, not a definition.

<details><summary>What it was built from</summary>

- `rows` — 4
- `violates` — 1NF -- items, quantities and unit_prices are repeating groups in one cell
- `then_violates` — 2NF and 3NF -- customer city and phone depend on the customer, not the order
- `target` — orders, order_items, customers, products -- four tables
- `repeated_customer` — Anitha Rao appears in O1001 and O1003

</details>

---

## Course 6 — Data Science with R

### `data/course-6-r/car-mileage.csv`

50 rows · `car_id` · `mpg` · `weight_t` · `cylinders` · `transmission` · `service_months`

**Practise:** data frames and factors; read.csv and str(); is.na / na.omit; lm() multiple regression; aggregate and tapply; dplyr verbs; ggplot2 scatter with a fitted line.

Fit mpg ~ weight_t + cylinders and you should recover about -7.5 and -0.8. Three service_months are blank on purpose: read it without na.strings and R will make the whole column a factor.

<details><summary>What it was built from</summary>

- `rows` — 50
- `true_intercept` — 34.0
- `weight_coefficient` — -7.5
- `cylinder_coefficient` — -0.8
- `noise_sd` — 1.6
- `missing_service_months` — 3
- `cylinder_levels` — [4, 6, 8]

</details>

---

## Course 7 — Web Technologies

### `data/course-7-web/products.csv`

8 rows · `sku` · `name` · `category` · `price` · `stock` · `rating` · `status`

**Practise:** rendering a table from JSON; the Fetch API; array filter / map / reduce; sorting a table by column; form validation against a list.

Convert it to JSON, render it as a table, then filter by category and sort by price -- experiments 14 and 16 in one file. Two rows are out of stock, so your filter has something to remove.

<details><summary>What it was built from</summary>

- `rows` — 8
- `categories` — 3
- `out_of_stock` — 2
- `total_stock_value` — 35555
- `highest_rated` — Notebook
- `cheapest_in_stock` — Notebook

</details>

---

## Course 8 — Data Mining

### `data/course-8-datamining/cluster-points.csv`

85 rows · `x` · `y` · `true_cluster`

**Practise:** k-Means and the elbow method; k-Medoids; DBSCAN; hierarchical clustering and dendrograms; silhouette score; BIRCH.

true_cluster is the answer key -- drop it before you cluster, then score against it. The ten rows labelled -1 are noise: k-Means cannot say so, DBSCAN can.

<details><summary>What it was built from</summary>

- `rows` — 85
- `true_k` — 3
- `points_per_cluster` — 25
- `noise_points` — 10
- `centres` — [(2.0, 2.0), (8.0, 3.0), (5.0, 9.0)]
- `expect` — k-Means finds 3 centres near those; DBSCAN with eps~0.9 and min_samples~4 labels most noise -1

</details>

### `data/course-8-datamining/market-basket.csv`

30 rows · `transaction_id` · `item`

**Practise:** Apriori; FP-Growth; support, confidence and lift; candidate generation and pruning; Partition and DIC.

Twelve baskets, one strong rule. Compute the support of every 1-itemset by hand first -- Apriori's whole trick is that it never counts a 2-itemset whose halves failed.

<details><summary>What it was built from</summary>

- `transactions` — 12
- `distinct_items` — 5
- `support_bread` — 0.6667
- `support_butter` — 0.6667
- `support_bread_and_butter` — 0.5833
- `confidence_bread_to_butter` — 0.875
- `lift_bread_to_butter` — 1.3125
- `planted_rule` — bread -> butter

</details>

### `data/course-8-datamining/warehouse-facts.csv`

144 rows · `month` · `region` · `city` · `category` · `product` · `quantity` · `revenue`

**Practise:** star schema; roll-up and drill-down; slice and dice; pivot; OLAP cube operations; measures against dimensions.

State the grain before you aggregate anything. Roll up city -> region -> all and the totals must agree at every level; if they do not, you have double-counted a join.

<details><summary>What it was built from</summary>

- `rows` — 144
- `months` — 12
- `regions` — 2
- `cities` — 3
- `categories` — 3
- `products` — 4
- `total_revenue` — 289300
- `south_revenue` — 193970
- `grain` — one row per month per city per product

</details>

---

## Course 9 — Python for Data Analysis

### `data/course-9-python-da/messy-customers.csv`

12 rows · `customer_id` · `name` · `email` · `city` · `age` · `salary` · `joined`

**Practise:** isnull and sum; dropna against fillna; drop_duplicates; str.strip, str.lower, str.contains; astype and to_datetime; IQR and z-score outlier detection; value_counts.

Six empty cells, one duplicated row, three spellings of Hyderabad, an age of 150 and a salary twenty times the next. Clean it and your row count should fall from 12 to 11 and your city count from 5 to 3.

<details><summary>What it was built from</summary>

- `rows` — 12
- `duplicate_rows` — 1
- `duplicate_id` — C002
- `unique_customers` — 11
- `missing_email` — 1
- `missing_age` — 2
- `missing_salary` — 2
- `missing_joined` — 1
- `total_missing_cells` — 6
- `leading_or_trailing_space` — ['C001 name', 'C007 city']
- `city_case_variants` — ['Hyderabad', 'hyderabad', 'HYDERABAD']
- `distinct_cities_after_cleaning` — 3
- `impossible_age` — {'C006': 150}
- `salary_outlier` — {'C007': 1200000}
- `invalid_email` — C008

</details>

### `data/course-9-python-da/monthly-sales.csv`

72 rows · `month` · `region` · `revenue`

**Practise:** groupby and agg; pivot_table; melt and stack; merge and join; resample and rolling means; matplotlib, Seaborn and Plotly.

Long format on purpose. pivot_table it into a 24 x 3 grid, plot the three lines, then melt it back -- and check you get the same 72 rows you started with.

<details><summary>What it was built from</summary>

- `rows` — 72
- `months` — 24
- `regions` — 3
- `trend_per_month` — 400
- `seasonal_amplitude` — 6000
- `region_base` — {'South': 52000, 'North': 38000, 'East': 27000}
- `shape` — long -- 72 rows, not a 24x3 grid

</details>

---

## Course 10 — Document Oriented Database

### `data/course-10-mongodb/courses.csv`

3 rows · `course_id` · `title` · `credits` · `instructor` · `capacity`

**Practise:** $lookup; normalised against embedded modelling; schema validation rules.

The referenced half of the model. Embed it into each student and then change an instructor's name -- count how many documents you must touch. That count is the argument for referencing.

<details><summary>What it was built from</summary>

- `rows` — 3
- `join_key` — course_id matches the ids inside students.enrolled_courses

</details>

### `data/course-10-mongodb/students.csv`

6 rows · `student_id` · `name` · `age` · `city` · `enrolled_courses` · `grades`

**Practise:** insertMany; find with $eq, $gt, $in; $elemMatch on arrays; embedded against referenced models; aggregation $unwind, $group, $lookup; multikey indexes.

Two semicolon-separated columns become ONE array of subdocuments. S104 has no enrolments -- so $unwind will drop that student unless you pass preserveNullAndEmptyArrays.

<details><summary>What it was built from</summary>

- `rows` — 6
- `student_with_no_enrolment` — S104
- `max_enrolments` — 3
- `distinct_cities` — 3
- `embedded_shape` — enrolments as an array of subdocuments
- `array_field_note` — semicolon-separated, so you split before you insert

</details>

---

## Course 11 — Business Intelligence Tools

### `data/course-11-bi/dim-date.csv`

4 rows · `date_key` · `date` · `year` · `month` · `quarter`

**Practise:** time intelligence; date hierarchies; grouping by month.

There is no March. Group by month and you get four rows, not five -- which is what breaks a month-on-month growth column.

<details><summary>What it was built from</summary>

- `rows` — 4
- `missing_month` — March -- there is no D-key for it
- `quarters` — {'Q1': 2, 'Q2': 2}

</details>

### `data/course-11-bi/dim-product.csv`

4 rows · `product_key` · `product` · `category` · `supplier_key` · `unit_cost` · `list_price`

**Practise:** dimensional modelling; star against snowflake; relationships and cardinality; Power Query.

Four products. The supplier column is the one edge that turns the star into a snowflake.

<details><summary>What it was built from</summary>

- `rows` — 4
- `role` — dimension
- `snowflake_edge` — supplier_key points at a further table, which is what makes this a snowflake rather than a pure star

</details>

### `data/course-11-bi/dim-store.csv`

3 rows · `store_key` · `store` · `region` · `opened`

**Practise:** slicers and cross-filtering; row-level security.

Two southern stores against one northern one -- so a naive average by region is not the same as a total by region.

<details><summary>What it was built from</summary>

- `rows` — 3
- `regions` — {'South': 2, 'North': 1}

</details>

### `data/course-11-bi/fact-sales.csv`

9 rows · `date_key` · `store_key` · `product_key` · `qty`

**Practise:** SUM, COUNT, DISTINCTCOUNT; CALCULATE and filter context; measure against calculated column; fan and chasm traps.

Join it to all three dimensions and you have the flat table a BI tool builds internally. Revenue is qty x list_price: 12,880 in total, 10,360 of it South.

<details><summary>What it was built from</summary>

- `rows` — 9
- `total_qty` — 87
- `total_revenue` — 12880
- `south_revenue` — 10360
- `north_revenue` — 2520
- `grain` — one row per product per store per day

</details>

---

## Course 12 A — Machine Learning

### `data/course-12a-ml/customer-segments.csv`

120 rows · `annual_spend` · `visits_per_year` · `online_ratio` · `true_segment`

**Practise:** k-Means; the elbow method; silhouette score; feature scaling before distance-based methods; hierarchical clustering; PCA for visualisation.

Cluster it WITHOUT scaling first. annual_spend runs to five figures and online_ratio is under 1, so unscaled k-Means clusters on spend alone. Then scale and watch the answer change.

<details><summary>What it was built from</summary>

- `rows` — 120
- `true_k` — 3
- `per_segment` — 40
- `profiles` — {'1': 'low spend, rare visits, mostly in store', '2': 'mid spend, monthly, mixed', '3': 'high spend, fortnightly, mostly online'}
- `note` — the three features are on wildly different scales

</details>

### `data/course-12a-ml/house-prices.csv`

200 rows · `area_sqft` · `bedrooms` · `age_years` · `price_lakh`

**Practise:** simple and multiple linear regression; train/test split; MAE, MSE, RMSE, R-squared; feature scaling; polynomial regression; regularisation.

Fit it and compare your coefficients with the four above. Then scale the features and refit: the coefficients change, the predictions do not, and knowing why is the point.

<details><summary>What it was built from</summary>

- `rows` — 200
- `intercept` — 12.0
- `area_coefficient` — 0.045
- `bedroom_coefficient` — 3.5
- `age_coefficient` — -0.25
- `noise_sd` — 8.0
- `expect_r2_above` — 0.85

</details>

### `data/course-12a-ml/loan-approval.csv`

300 rows · `income` · `debt` · `credit_score` · `approved`

**Practise:** logistic regression; k-NN; decision tree; Naive Bayes; SVM; confusion matrix, precision, recall, F1; ROC and AUC; cross-validation.

Generated from a logistic rule, so there IS an irreducible error rate -- a model reporting 100% has leaked the label. Compare your coefficients with the true ones, and note which feature matters most: credit_score has by far the biggest RAW coefficient, but income has the biggest effect, because a coefficient means nothing until you multiply it by the spread of its variable.

<details><summary>What it was built from</summary>

- `rows` — 300
- `positive_rate` — 0.5267
- `true_rule` — sigmoid(-6 + 0.00005*income - 0.00006*debt + 0.008*credit_score)
- `largest_raw_coefficient` — credit_score (0.008, which is 160x the coefficient on income)
- `largest_standardised_effect` — income -- because its spread is far wider, coefficient x SD comes out around 1.5 against 1.3 for credit_score
- `expect_accuracy_above` — 0.75

</details>

---

## Course 12 B — Big Data Technologies

### `data/course-12b-bigdata/web-logs.csv`

1200 rows · `timestamp` · `ip` · `path` · `status` · `bytes`

**Practise:** MapReduce word count and its shape; the shuffle and sort phase; combiners; Hive GROUP BY; Pig FOREACH GENERATE; Spark RDD reduceByKey and DataFrame agg.

Big enough that counting by hand is out and a map-reduce is in. Count hits per path, bytes per IP and the error rate three ways -- a dict, a GROUP BY and reduceByKey -- and the answers must agree.

<details><summary>What it was built from</summary>

- `rows` — 1200
- `distinct_ips` — 25
- `distinct_paths` — 8
- `status_counts` — {'200': 670, '301': 197, '404': 167, '500': 166}
- `total_bytes` — 5621404
- `error_rate` — 0.2775

</details>

### `data/course-12b-bigdata/wordcount-corpus.csv`

5 rows · `doc_id` · `text`

**Practise:** the canonical MapReduce word count; mapper, combiner, reducer; TF-IDF (Course 15 A uses the same file).

Small enough to count by hand, which is the point: work out the answer on paper, then make MapReduce agree with you.

<details><summary>What it was built from</summary>

- `documents` — 5
- `total_words` — 44
- `distinct_words` — 28
- `top_word` — the
- `top_word_count` — 7
- `count_of_dog` — 3
- `count_of_quick` — 3

</details>

---

## Course 13 A — Artificial Intelligence

### `data/course-13a-ai/family-relations.csv`

9 rows · `parent` · `child`

**Practise:** Prolog facts and rules; unification and backtracking; recursive rules (ancestor); first-order logic; forward and backward chaining.

Load it as parent/2 facts and define sibling, grandparent and a recursive ancestor. Six grandparent pairs -- count them by hand before you run it.

<details><summary>What it was built from</summary>

- `facts` — 9
- `individuals` — 8
- `siblings` — [['mary', 'peter'], ['alice', 'bob']]
- `grandparent_pairs` — 6
- `expect` — grandparent(X,Z) :- parent(X,Y), parent(Y,Z) yields 6

</details>

### `data/course-13a-ai/graph-edges.csv`

16 rows · `from_city` · `to_city` · `cost`

**Practise:** BFS, DFS, uniform-cost search; depth-limited and iterative deepening; greedy best-first and A*; admissible heuristics.

The classic map. BFS finds a three-hop route costing 450; uniform-cost finds a four-hop route costing 418. Fewest steps and cheapest are different questions, and this file proves it.

<details><summary>What it was built from</summary>

- `edges` — 16
- `nodes` — 13
- `undirected` — True
- `shortest_path_arad_to_bucharest` — ['Arad', 'Sibiu', 'Rimnicu', 'Pitesti', 'Bucharest']
- `shortest_cost` — 418
- `bfs_path_is_shorter_in_hops_but_costlier` — ['Arad', 'Sibiu', 'Fagaras', 'Bucharest']
- `bfs_path_cost` — 450

</details>

### `data/course-13a-ai/map-colouring.csv`

9 rows · `region` · `neighbour`

**Practise:** constraint satisfaction; backtracking search; forward checking and arc consistency (AC-3); minimum-remaining-values heuristic.

Tasmania touches nothing, so it takes any colour -- a free variable that MRV should pick last. WA, NT and SA form a triangle, which is why two colours cannot work.

<details><summary>What it was built from</summary>

- `regions` — 7
- `adjacencies` — 9
- `isolated_region` — T
- `chromatic_number` — 3
- `expect` — 3 colours suffice; 2 do not, because WA-NT-SA is a triangle

</details>

---

## Course 13 B — Cloud Computing

### `data/course-13b-cloud/iam-policies.csv`

7 rows · `principal` · `action` · `resource` · `effect`

**Practise:** IAM policy evaluation; explicit deny against implicit deny; least privilege; wildcards in resource ARNs.

Carol has s3:* on the bucket AND an explicit Deny on delete. Explicit Deny wins -- so a wildcard Allow is not the same as unrestricted access, and dave, who appears nowhere, is denied by default.

<details><summary>What it was built from</summary>

- `statements` — 7
- `principals` — 3
- `rule` — an explicit Deny always beats an Allow, and anything not allowed is denied by default
- `alice_can_delete` — False
- `bob_can_read_salaries` — False
- `bob_can_read_other_reports` — True
- `carol_can_delete` — False
- `dave_can_read` — False

</details>

### `data/course-13b-cloud/storage-costs.csv`

3 rows · `tier` · `temperature` · `gb_stored` · `price_per_gb_month` · `retrieval_per_gb` · `egress_per_gb`

**Practise:** storage tiers and lifecycle policies; total cost of ownership; egress charges; capex against opex.

Work out the monthly bill, then the bill if you had to read every byte back once. The cheapest tier to STORE is the most expensive to READ, and that reversal is the exam answer.

<details><summary>What it was built from</summary>

- `tiers` — 3
- `monthly_storage_cost` — {'standard': 11.5, 'infrequent': 25.0, 'archive': 7.92}
- `total_monthly_storage` — 44.42
- `archive_is_cheaper_to_store_but` — retrieving all 8000 GB costs 160.00, which is twenty times its monthly storage bill
- `break_even_note` — archive only wins if you read it rarely

</details>

---

## Course 14 A — Deep Learning

### `data/course-14a-deeplearning/sensor-failures.csv`

400 rows · `temperature_c` · `vibration_mm_s` · `failed`

**Practise:** binary classification with a neural net; why depth helps; sigmoid output and binary cross-entropy; overfitting, dropout, early stopping.

The boundary is an ellipse, so a linear model cannot do well however long you train it. Five per cent of labels are flipped, so 0.95 is the ceiling -- anything above it is a leak.

<details><summary>What it was built from</summary>

- `rows` — 400
- `boundary` — elliptical: ((t-30)/9)^2 + ((v-5)/3)^2 > 1
- `label_noise` — 0.05
- `ceiling_accuracy` — 0.95
- `positive_rate` — 0.665
- `expect` — logistic regression plateaus near 0.65; one hidden layer reaches the low 0.9s

</details>

### `data/course-14a-deeplearning/xor.csv`

4 rows · `x1` · `x2` · `y`

**Practise:** the perceptron and its limit; activation functions; one hidden layer; backpropagation by hand.

Four rows that ended an AI winter. Train a single-layer perceptron until you are convinced it cannot exceed 3 of 4, then add one hidden layer.

<details><summary>What it was built from</summary>

- `rows` — 4
- `linearly_separable` — False
- `single_layer_perceptron_best_accuracy` — 0.75
- `why` — no straight line puts (0,1) and (1,0) on one side and (0,0) and (1,1) on the other
- `solved_by` — one hidden layer of 2 units with a non-linear activation

</details>

---

## Course 14 B — Time Series

### `data/course-14b-timeseries/ar2-series.csv`

300 rows · `t` · `value`

**Practise:** stationarity; ACF and PACF read together; AR, MA and ARMA; Yule-Walker and MLE estimation; AIC and BIC; the Ljung-Box test; ADF and KPSS.

Built from phi = (0.6, -0.3) after a 200-point burn-in. The PACF cutting off at lag 2 is how you would have identified the order without being told.

<details><summary>What it was built from</summary>

- `n` — 300
- `model` — AR(2)
- `phi1` — 0.6
- `phi2` — -0.3
- `sigma` — 1.0
- `stationary` — True
- `expect` — ACF tails off, PACF cuts off after lag 2; a fitted AR(2) recovers roughly (0.6, -0.3)

</details>

### `data/course-14b-timeseries/macro-indicators.csv`

250 rows · `t` · `rates` · `inflation` · `unrelated`

**Practise:** VAR models; Granger causality; impulse response; state-space form and the Kalman filter; cointegration.

Causality is planted in ONE direction: rates move inflation, inflation does not move rates. Test both ways -- a Granger test that fires in both directions has found correlation, not cause. The third column is a control that should fire in neither.

<details><summary>What it was built from</summary>

- `n` — 250
- `rates_granger_causes_inflation` — True
- `inflation_granger_causes_rates` — False
- `unrelated_causes_nothing` — True
- `coefficients` — {'rates_ar1': 0.5, 'inflation_ar1': 0.3, 'rates_to_inflation': 0.6, 'unrelated_ar1': 0.4}

</details>

### `data/course-14b-timeseries/seasonal-sales.csv`

72 rows · `month` · `sales`

**Practise:** decomposition, additive against multiplicative; STL; seasonal differencing; SARIMA; Holt-Winters; forecast intervals.

A linear trend of +8 a month under a 12-month season. Difference once at lag 12 and the season goes; difference again at lag 1 and the trend goes. Doing it in the wrong order is the classic error.

<details><summary>What it was built from</summary>

- `n` — 72
- `years` — 6
- `period` — 12
- `trend_per_month` — 8.0
- `base_level` — 1000
- `seasonal_amplitude` — 220
- `noise_sd` — 35
- `expect` — differencing at lag 12 removes the season; SARIMA with s=12 fits; Holt-Winters recovers the trend

</details>

---

## Course 15 A — Natural Language Processing

### `data/course-15a-nlp/ner-sentences.csv`

5 rows · `sentence` · `expected_entities`

**Practise:** named entity recognition; POS tagging; chunking; evaluating NER against gold labels; precision and recall for extraction.

The gold labels are in the second column, so you can SCORE the tagger rather than eyeball it. Expect the model to get the cities right and to struggle with 'Andhra Pradesh' and 'Krishna'.

<details><summary>What it was built from</summary>

- `sentences` — 5
- `entity_types` — ['PERSON', 'ORG', 'GPE', 'LOC', 'DATE', 'MONEY']
- `total_entities` — 15
- `known_difficulty` — off-the-shelf English models mislabel Indian state and river names more often than city names

</details>

### `data/course-15a-nlp/sentiment-reviews.csv`

20 rows · `text` · `label`

**Practise:** tokenization; stopword removal; stemming and lemmatization; bag of words and TF-IDF; Naive Bayes and logistic regression for sentiment; train/test split on text.

Twenty reviews, balanced, labelled by hand so the accuracy you compute means something. One review is deliberately mixed.

<details><summary>What it was built from</summary>

- `rows` — 20
- `positive` — 10
- `negative` — 10
- `balanced` — True
- `labelled_by` — hand
- `note` — 'Works well but the cable is too short' is positive but contains a negative clause -- bag-of-words will find it hard, and that is the lesson

</details>

---

## Course 15 B — Data Engineering and MLOps

### `data/course-15b-mlops/loan-current.csv`

400 rows · `batch` · `income` · `debt` · `credit_score` · `approved`

**Practise:** population stability index; the Kolmogorov-Smirnov test; data drift against concept drift; retraining triggers and the metric gate; monitoring.

ONE feature moved. Detect which, and resist retraining on reflex: the inputs shifted but the input-to-label relationship did not, so a retrain buys almost nothing. Knowing that is the Unit 5 answer.

<details><summary>What it was built from</summary>

- `rows` — 400
- `credit_score_mean` — 585
- `income_mean` — 55000
- `drifted_feature` — credit_score -- the mean falls by 55 points
- `undrifted_features` — ['income', 'debt']
- `expect` — PSI and a KS test flag credit_score and NOT income; the relationship between features and label is unchanged, so retraining gains very little

</details>

### `data/course-15b-mlops/loan-reference.csv`

400 rows · `batch` · `income` · `debt` · `credit_score` · `approved`

**Practise:** training a baseline; MLflow experiment tracking; model registry; DVC data versioning.

Train on this one and register it. It is the reference every later batch is compared against.

<details><summary>What it was built from</summary>

- `rows` — 400
- `credit_score_mean` — 640
- `income_mean` — 55000
- `role` — the distribution the model was trained on

</details>

