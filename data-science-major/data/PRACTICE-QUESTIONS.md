# Practice questions

A question set for every dataset in `data/`, graded **warm-up** → **core** → **stretch**. Warm-ups check you can load the file and read it; core questions are the ones an exam asks; stretch questions are the ones worth arguing about in a viva.

**The answers are computed, not typed.** Every answer below is a function of the CSV, evaluated when this page is generated. Three figures I wrote from memory while building the datasets turned out wrong, and a wrong answer key is worse than none — the student who gets it right concludes they got it wrong.

Answers are folded away. Work the question first; the point is the method, and the number only tells you whether the method was right.

**266 questions over 50 datasets.**

---

## Used by several courses

### `data/shared/flowers.csv`

**Warm-up**

1. How many rows per species?
2. Which single measurement separates the species best?

**Core**

3. Split 70/30 and fit a k-NN classifier. Which two species does it confuse, and why is that expected?
4. What is the largest petal_length among alba, and the smallest among the other two?

**Stretch**

5. A classmate reports 100% accuracy. What went wrong?

<details><summary>Answers</summary>

1. alba 30; carinata 30; borealis 30
2. petal_length — its between-species spread is largest relative to the within-species spread
3. borealis and carinata — their petal_length ranges overlap (5.26 against 4.82), while alba is separable
4. alba max 2.24; others min 3.57 — no overlap at all
5. The label leaked, or they scored on the training set. Two species genuinely overlap here, so perfect separation is not available

</details>

### `data/shared/sales-transactions.csv`

**Warm-up**

1. How many transactions are in the file, and how many distinct products?
2. What is the total revenue?

**Core**

3. Build a pivot of revenue by region and product. What does each region total?
4. Which product earns the most, and what share of the total is it?
5. Group the dates by month. How many months appear, and why is that fewer than the span suggests?

**Stretch**

6. Compute month-on-month growth over a COMPLETE month range. What happens at April, and which Excel function exists for it?

<details><summary>Answers</summary>

1. 9 transactions over 4 products
2. 12,880
3. North 2,520; South 10,360
4. Rice 5kg — 5,600, 43.5% of the total
5. 4 months (2026-01, 2026-02, 2026-04, 2026-05) — March has no sale, and grouping omits empty periods rather than showing a zero
6. March is 0, so April divides by zero and gives #DIV/0! — that is what IFERROR is for. Dropping March instead makes April read +46.77%, two months of change labelled as one

</details>

---

## Course 1 — Office Automation

### `data/course-1-office/budget.csv`

**Warm-up**

1. What are total expenses and savings?
2. What is the savings rate?

**Core**

3. Use Goal Seek to reach savings of 20,000 by changing income. What income is needed?
4. Now Goal Seek a savings RATE of 30%. Why can you not read this one off the sheet?

**Stretch**

5. Ask Goal Seek for a 100% savings rate. What does it do, and why?
6. Build a one-variable data table over rent from 12,000 to 18,000. What is the slope?

<details><summary>Answers</summary>

1. expenses 33,000, savings 12,000
2. 26.67%
3. 53,000
4. 33,000/0.70 = 47,142.86 — the rate is not linear in income, so the answer is a division, not a subtraction
5. It exhausts its iterations and reports it may not have found a solution: the rate approaches 100% as income grows but never reaches it, so there is no root to find
6. Exactly -1: every rupee of rent is a rupee off savings. Savings run 15,000 down to 9,000

</details>

### `data/course-1-office/class-results.csv`

**Warm-up**

1. Compute each student's total and average.
2. Which subject has the lowest class average?

**Core**

3. Grade on the AVERAGE with A>=90, B>=75, C>=60, D>=40. What is the distribution?
4. A student passes only if they clear 40 in EVERY subject. Who fails, and how many would pass if you tested the average instead?

**Stretch**

5. Point the grade formula at the TOTAL instead of the average. What happens, and what does the weakest student get?

<details><summary>Answers</summary>

1. Class mean 68.43; highest total 485 (Sneha)
2. maths at 67.00
3. A 3; B 6; C 4; D 6; F 1
4. Divya, Ishita, Kavya, Rahul fail. Testing the average passes all but Kavya — three students who failed a paper would be passed in error
5. 19 of 20 get an A, and Kavya — who failed all five papers with 80/500 — is awarded a B. Nothing errors

</details>

### `data/course-1-office/payroll.csv`

**Warm-up**

1. Add DA (30% of basic), HRA (15%) and Gross. What is the total gross bill?
2. Who is paid most and least, net?

**Core**

3. Deduction is 10% of (Basic + DA). Write Net as a single multiple of Basic and verify it on one row.
4. Put the three rates in their own cells and reference them absolutely. Why does that earn marks over typing 0.30?

**Stretch**

5. Take the deduction on Basic alone instead. By how much does the monthly payroll rise?

<details><summary>Answers</summary>

1. 290,725
2. Faisal Ahmed 68,640; Chitra Devi 24,420
3. Net = 1.32 x Basic — e.g. Anitha Rao: 25,000 x 1.32 = 33,000
4. Changing the DA rate becomes a one-cell edit; hard-coded rates must be found in every formula and one will be missed
5. Net becomes 1.35 x Basic, so the bill rises by 3% of the basic total — 6,015 a month, with no error shown anywhere

</details>

---

## Course 2 — Problem Solving Using C

### `data/course-2-c/employee-records.csv`

**Warm-up**

1. Define a struct for one record and read the file with fgets. How long must the name buffer be?
2. Print the total and average salary.

**Core**

3. Why does scanf("%s", name) fail on this file?
4. Sort the array of structs by salary descending and print the top three.
5. Linear-search for employee 107 and report the comparison count. How many would a binary search need?

**Stretch**

6. Write the records back with fprintf, read them again and compare. What breaks if a name contains a comma?

<details><summary>Answers</summary>

1. the longest name is 13 characters, so char name[14] at minimum — allow more
2. total 331,500, average 33,150
3. every name contains a space, so %s stops at the first one and leaves the surname in the buffer, which the next scanf then reads into the wrong field. Use fgets and strtok
4. Faisal Ahmed 52,000; Daniel Joseph 45,000; Jyothi Varma 41,000
5. linear finds it at position 7 of 10; binary needs at most 4 comparisons on the sorted array
6. the round trip splits that field in two — which is why real CSV quotes fields, and why you should test with a name like "Rao, Anitha"

</details>

---

## Course 3 — Python Programming

### `data/course-3-python/students.csv`

**Warm-up**

1. Read it with csv.DictReader and total each student's three marks. Who scores highest?
2. What is the mean mark across every student and subject?

**Core**

3. Build a dict of name -> average and print those above the class average.
4. Which subject has the widest spread, and by what measure?

**Stretch**

5. Wrap the read in try/except and run it against a filename that does not exist. Which exception, and why not a bare except?

<details><summary>Answers</summary>

1. Nandini with 271
2. 68.2800
3. class average 68.28; 10 students are above it
4. maths — standard deviation 21.38 against 18.64 for statistics
5. FileNotFoundError. A bare except also swallows KeyboardInterrupt and your own typos, so the program fails silently instead of loudly

</details>

---

## Course 4 — Statistical Foundations

### `data/course-4-stats/before-after.csv`

**Warm-up**

1. Compute the gain for each subject. What is the mean gain?

**Core**

2. Run a paired t-test. What do you conclude?
3. Now run an INDEPENDENT t-test on the same two columns. Why is the evidence weaker?
4. Which test is a one-sample t-test in disguise, and on what?

**Stretch**

5. Run a Wilcoxon signed-rank test. When would you prefer it?

<details><summary>Answers</summary>

1. 3.8580 with sd 2.3244
2. t = 7.4227, p = 5e-07 — the improvement is real
3. p = 0.3206 against 5e-07. The unpaired test treats the between-subject spread (sd about 12.0) as noise; pairing removes it and leaves only the gain's own sd of 2.32
4. the paired test — it is a one-sample test of the differences against zero, and gives an identical statistic
5. when the differences are clearly non-normal or the sample is very small; here it agrees, because the gains were generated normal

</details>

### `data/course-4-stats/fertiliser-yield.csv`

**Warm-up**

1. Report the mean yield for each fertiliser.

**Core**

2. Run a one-way ANOVA at 5%. What do you conclude?
3. ANOVA says they differ. It does not say which. Which pair separates most?
4. Partition the total sum of squares into between and within.

**Stretch**

5. Why not run three separate t-tests instead?

<details><summary>Answers</summary>

1. A 38.4575; B 45.4700; C 50.1183
2. F = 35.3164, p = 6.31e-09 — not all three means are equal
3. C against A, a gap of 11.6608 — a post-hoc test is what licenses that claim
4. between + within = total; the F ratio is the between mean square divided by the within mean square
5. three tests at 5% give roughly a 14% chance of at least one false positive. ANOVA tests all three at once at 5%

</details>

### `data/course-4-stats/heights.csv`

**Warm-up**

1. Compute the mean, median and mode class.
2. Compute the range, variance and standard deviation.

**Core**

3. The data were drawn from N(165, 8). How far is your sample mean from 165, and is that surprising?
4. Test H0: mu = 165 at 5%. What do you conclude?

**Stretch**

5. Compute skewness and kurtosis. What would you expect from a normal sample of this size, and do you get it?

<details><summary>Answers</summary>

1. mean 165.3683, median 166.00
2. range 44.4, variance 56.2903, sd 7.5027
3. 0.3683 cm away; the standard error is 8/sqrt(60) = 1.0328, so it is well within one SE — sampling error, not a wrong answer
4. t = 0.3803 on 59 df — do not reject; the data are consistent with 165
5. skewness -0.6553, excess kurtosis 1.8338 — both near zero, but n=60 gives them large standard errors, so small departures mean little

</details>

### `data/course-4-stats/preference-survey.csv`

**Warm-up**

1. Build the 2x2 contingency table from the raw rows.
2. How many respondents in total?

**Core**

3. Compute the expected frequencies under independence.
4. Run the chi-square test of independence. Degrees of freedom, statistic, conclusion?

**Stretch**

5. Is the test valid here? What is the condition, and does Yates' correction change your conclusion?

<details><summary>Answers</summary>

1. female/coffee 50; female/tea 20; male/coffee 25; male/tea 45
2. 140
3. female/coffee 37.500; female/tea 32.500; male/coffee 37.500; male/tea 32.500
4. dof = 1, chi-square = 16.5415, p = 4.76e-05 — reject independence; preference is associated with gender
5. every expected count exceeds 5 (smallest 32.50), so the approximation holds. Yates' correction is applied by default for 2x2 and does not change the conclusion

</details>

### `data/course-4-stats/study-hours-marks.csv`

**Warm-up**

1. Draw the scatter plot. Does the relationship look linear?
2. Compute Karl Pearson's correlation coefficient.

**Core**

3. Fit the least-squares line of marks on hours. What are the slope and intercept, and what do they mean?
4. Show that R-squared equals r-squared for this fit.
5. Now fit hours on marks. Why is it not the same line?

**Stretch**

6. The data were built from marks = 12 + 6 x hours. How close did you get, and what explains the gap?

<details><summary>Answers</summary>

1. yes — a clear positive straight-line trend with constant scatter
2. r = 0.9722
3. marks = 11.9027 + 6.0044 x hours — about 6 marks per hour of study, and about 12 marks for a student who studies none
4. both are 0.945099
5. slope 0.1574 in the other direction; least squares minimises the error in the DEPENDENT variable, so swapping roles changes what is being minimised. The two lines cross at the means
6. slope 6.0044 against 6.0, intercept 11.9027 against 12.0 — the gap is the noise term (sd 4) and n = 40

</details>

### `data/course-4-stats/treatment-groups.csv`

**Warm-up**

1. Report n, mean and sd for each group.
2. What is the observed difference in means?

**Core**

3. Test whether the treatment mean is higher, at 5%.
4. Build a 95% confidence interval for the difference.

**Stretch**

5. Run a one-way ANOVA on the same two groups. How does F relate to t?

<details><summary>Answers</summary>

1. control n=25 mean 70.1452 sd 4.9487; treatment n=25 mean 76.4164 sd 6.6114
2. 6.2712
3. t = 3.7969, p = 0.000412 — reject H0
4. centred on 6.27; it excludes zero, which is the same conclusion the test reached
5. F = 14.4163 = t^2 = 14.4163. With two groups the two tests are algebraically the same

</details>

---

## Course 5 — Database Management Systems

### `data/course-5-dbms/assignments.csv`

**Warm-up**

1. What is the primary key of this table?

**Core**

2. Total hours committed per project.
3. Which employee works on more than one project?
4. List employees on NO project. Which SQL construct answers this cleanly?

**Stretch**

5. Find employees assigned to EVERY project. What is this class of query called?

<details><summary>Answers</summary>

1. the composite (emp_id, project_id) — neither column alone is unique
2. P1 55; P2 75; P3 20; P4 48
3. E104
4. E106 — NOT EXISTS, or a LEFT JOIN with IS NULL. An inner join can never answer it, because the rows are not there to be joined
5. relational division — none qualify here, since no employee appears on all four projects

</details>

### `data/course-5-dbms/departments.csv`

**Warm-up**

1. Write CREATE TABLE for it, choosing types and the key.

**Core**

2. Which city hosts more than one department?
3. Why must dept_id be declared NOT NULL as well as PRIMARY KEY?

<details><summary>Answers</summary>

1. dept_id CHAR(2) PRIMARY KEY, dept_name VARCHAR(40) NOT NULL, city VARCHAR(40) — 4 rows
2. Hyderabad (2)
3. it need not be: PRIMARY KEY implies NOT NULL and UNIQUE. Saying so explicitly documents the intent, and is the safer habit

</details>

### `data/course-5-dbms/employees.csv`

**Warm-up**

1. How many employees, and what is the salary bill?
2. Average salary per department.

**Core**

3. Join employees to departments and list name with dept_name. How many rows come back?
4. Self-join to show each employee beside their manager. Why does an INNER join return fewer rows than a LEFT join?
5. Which departments have an average salary above the company average? Use GROUP BY with HAVING.

**Stretch**

6. Find employees earning more than their own manager.

<details><summary>Answers</summary>

1. 7 employees, 230,500
2. D1 26,500; D2 35,667; D3 18,500; D4 52,000
3. 7 — every employee has a valid dept_id, so an inner join loses nobody
4. inner returns 5, left returns 7 — the 2 employees with no manager have nothing to match, and only the LEFT join keeps them
5. D2; D4 (company average 32,929)
6. Esha Nair over Anitha Rao

</details>

### `data/course-5-dbms/projects.csv`

**Warm-up**

1. Total and average project budget.

**Core**

2. Which department owns the largest total budget?
3. Write a three-table join: employee name, department name, project name. What join order avoids a cartesian product?

<details><summary>Answers</summary>

1. total 1,810,000, average 452,500
2. D2 with 1,440,000
3. employees -> departments -> projects, joining on dept_id each time. Joining employees to projects directly has no shared key

</details>

### `data/course-5-dbms/unnormalised-orders.csv`

**Warm-up**

1. Which normal form does this table break first, and why?

**Core**

2. Decompose it to 3NF. How many tables, and what are their keys?
3. Which columns depend on the customer rather than the order, and which normal form does that violate?

**Stretch**

4. Change one customer's phone number in the ORIGINAL table. How many rows must you touch, and what is that anomaly called?
5. What happens if you want to record a new product nobody has ordered yet?

<details><summary>Answers</summary>

1. 1NF — items, quantities and unit_prices each pack several values into one cell
2. four: customers(customer_id), products(product_id), orders(order_id), order_items(order_id, product_id)
3. customer_city and customer_phone — a transitive dependency through customer_name, which is 3NF
4. 2 rows for Anitha Rao — the update anomaly. Miss one and the table contradicts itself
5. you cannot — there is no row to put it in without inventing a fake order. That is the insert anomaly

</details>

---

## Course 6 — Data Science with R

### `data/course-6-r/car-mileage.csv`

**Warm-up**

1. read.csv it and run str(). How many observations and variables, and which are factors?
2. How many service_months are missing?

**Core**

3. Fit lm(mpg ~ weight_t + cylinders). Report the coefficients.
4. The data were built from 34 - 7.5*weight - 0.8*(cyl-4). How close is your fit?
5. Use tapply or dplyr to get mean mpg by cylinder count.

**Stretch**

6. Read the file WITHOUT na.strings and inspect service_months. What has R done, and why does it matter?
7. ggplot mpg against weight, coloured by transmission, with a fitted line per group. Do the slopes differ?

<details><summary>Answers</summary>

1. 50 observations, 6 variables; transmission is a factor with 2 levels, cylinders is numeric but has only 3 values
2. 3 — rows CAR008, CAR024, CAR042
3. intercept 35.6383, weight -7.3292, cylinders -0.5983
4. weight -7.329 against -7.5 and cylinders -0.598 against -0.8 — the intercept absorbs the (cyl-4) shift
5. 4 cyl 21.0612; 6 cyl 20.4767; 8 cyl 19.4693
6. the blanks make it character, so R makes the whole column a factor and mean() returns NA with a warning. Every numeric operation on that column silently stops working
7. geom_smooth(method='lm') per group; the generator put no transmission effect in, so any difference you see is noise

</details>

---

## Course 7 — Web Technologies

### `data/course-7-web/products.csv`

**Warm-up**

1. Convert the file to JSON and render it as an HTML table with JavaScript. How many rows and columns?
2. What is the total value of stock on hand?

**Core**

3. Filter to in-stock items only. How many remain, and what array method does it?
4. Sort by price descending and list the top three.
5. Group by category and total the stock. Which method chain does this in JavaScript?

**Stretch**

6. Build a form that only accepts an SKU present in the file. Which validation approach, and what does it miss?

<details><summary>Answers</summary>

1. 8 rows, 7 columns
2. 35,555
3. 5 remain — Array.prototype.filter
4. Rice 5kg (280); Tea 500g (210); Shampoo 200ml (140)
5. Grocery 60; Personal Care 7; Stationery 405 — reduce into an object keyed by category
6. a datalist or a fetch-and-check against the list. Client-side validation is a convenience, not a guarantee — anyone can post past it, so the server must check again

</details>

---

## Course 8 — Data Mining

### `data/course-8-datamining/cluster-points.csv`

**Warm-up**

1. Plot x against y. How many groups do you see by eye, and what else is on the plot?

**Core**

2. Drop true_cluster and run k-Means with k=3. Report the centres.
3. Use the elbow method to choose k. Does it agree?
4. Run DBSCAN with eps=0.9 and min_samples=4. How many points does it call noise, and how many of those really are?

**Stretch**

5. k-Means put every noise point in some cluster. Why can it not do otherwise, and when does that matter?
6. Score both against true_cluster with the adjusted Rand index. Which wins, and is that fair?

<details><summary>Answers</summary>

1. 3 tight groups plus 10 scattered points
2. (1.952, 2.050); (4.852, 9.159); (8.114, 3.156)
3. the inertia drop flattens after k=3, which matches the three planted centres
4. it labels 8 as noise, of which 7 of the 10 planted noise points are correctly caught
5. k-Means partitions — every point must belong somewhere, so outliers drag centres towards themselves. It matters whenever 'none of the above' is a real answer, such as fraud or sensor faults
6. DBSCAN, because the index rewards labelling noise correctly. Comparing on the clustered points alone is the fairer test

</details>

### `data/course-8-datamining/market-basket.csv`

**Warm-up**

1. Reshape long to baskets. How many transactions and distinct items?
2. Compute the support of every single item.

**Core**

3. At minimum support 0.3, which 1-itemsets survive to the next level?
4. Compute support, confidence and lift for bread -> butter.
5. Confidence for butter -> bread is different. Why, and what does that tell you about rules?

**Stretch**

6. State the Apriori property and show one 2-itemset it lets you skip counting.

<details><summary>Answers</summary>

1. 12 transactions, 5 items
2. bread 0.6667; butter 0.6667; eggs 0.3333; jam 0.3333; milk 0.5000
3. bread; butter; eggs; jam; milk
4. support 0.5833, confidence 0.8750, lift 1.3125
5. 0.8750 — confidence is not symmetric, because it divides by a different antecedent. Lift is symmetric; confidence is not
6. no superset of an infrequent set can be frequent. At support 0.3, jam (0.33) fails, so every pair containing jam is pruned without being counted

</details>

### `data/course-8-datamining/warehouse-facts.csv`

**Warm-up**

1. State the grain of this fact table in one sentence.
2. Total revenue across the whole cube.

**Core**

3. Roll up from city to region to all. Do the totals agree at every level?
4. Slice to one month and dice by region and category. Which OLAP operations are these?
5. Which region-category pair earns most?

**Stretch**

6. Join this to a store dimension that has two rows per city and total the revenue. What has happened?

<details><summary>Answers</summary>

1. one row per month per city per product — 144 rows = 12 x 3 x 4
2. 289,300
3. they must, and they do: 289,300 = 289,300 = 289,300
4. slice fixes one dimension to a single value; dice takes a sub-cube across several. Drill-down goes region -> city
5. South / Grocery — 141,890
6. every fact row matches twice and the total doubles — a fan trap. The join has changed the grain without saying so

</details>

---

## Course 9 — Python for Data Analysis

### `data/course-9-python-da/messy-customers.csv`

**Warm-up**

1. Load it and count missing values per column.
2. How many rows, and how many are duplicates?

**Core**

3. Clean the city column. How many distinct cities before and after?
4. Find the rows with leading or trailing whitespace. Which columns, and why is str.strip not enough on its own?
5. Detect outliers in salary with the IQR rule. Which row, and by how much?
6. Which age is impossible, and which email fails a naive check?

**Stretch**

7. Decide dropna against fillna for each column and justify it. What is your final row count?

<details><summary>Answers</summary>

1. email 1; age 2; salary 2; joined 1 — 6 empty cells in all
2. 12 rows, 1 exact duplicate (customer_id C002)
3. 5 before, 3 after stripping and lowercasing
4. name on C001 and city on C007. Strip fixes the edges; it does not fix case, so 'Hyderabad' and 'hyderabad' still differ afterwards
5. Q1 45,500, Q3 61,000, upper fence 84,250 — one salary of 1,200,000 sits far beyond it
6. age 150, and 'not-an-email' has no @
7. 11 after removing the duplicate. Age and salary are candidates for median fill; a missing joined date probably cannot be invented, so that row may have to go or stay flagged

</details>

### `data/course-9-python-da/monthly-sales.csv`

**Warm-up**

1. How many rows, months and regions?
2. Mean revenue per region.

**Core**

3. pivot_table it into a months-by-regions grid. What shape?
4. melt it back. Do you recover the original row count?
5. Which month had the highest total across all regions?
6. Plot a 3-month rolling mean per region. What does it reveal that the raw series hides?

**Stretch**

7. Separate trend from season. The data were built with a trend of +400 a month and an amplitude of 6000. Can you recover both?

<details><summary>Answers</summary>

1. 72 rows, 24 months, 3 regions
2. East 31,507; North 42,569; South 57,006
3. 24 x 3, with no gaps
4. yes — 72 rows, the same 72
5. 2025-03 with 154,608
6. the upward trend — the 12-month season dominates the raw plot and the rolling mean damps it
7. regress revenue on a month index per region for the trend; average the residuals by calendar month for the season

</details>

---

## Course 10 — Document Oriented Database

### `data/course-10-mongodb/courses.csv`

**Warm-up**

1. How many courses, and what is the total capacity?

**Core**

2. $lookup students onto courses. How would you count enrolments per course?

**Stretch**

3. Add a schema validation rule that rejects a course with capacity below 1. What does MongoDB do to documents already in the collection?

<details><summary>Answers</summary>

1. 3 courses, 160 seats
2. $unwind the student enrolments first, then $group by course_id — $lookup alone gives you arrays, not counts
3. nothing — validation applies to writes from that point on. Existing bad documents stay until you find and fix them

</details>

### `data/course-10-mongodb/students.csv`

**Warm-up**

1. Import it so each student is one document. What must you do with enrolled_courses first?

**Core**

2. Model enrolments as an array of subdocuments pairing course with grade. Write one document out in full.
3. Find students enrolled in DSC301 with a grade of A. Which operator, and why is a plain dotted query wrong?
4. $unwind the enrolments and count per course. Which student disappears, and how do you keep them?
5. How many students per city?

**Stretch**

6. Would you embed the course document in each student, or reference it? Argue from this data.

<details><summary>Answers</summary>

1. split on ';' into an array — a bare import leaves one string, and no array operator will work on it
2. each of the two semicolon-separated columns has the same length per row, so element i of one pairs with element i of the other
3. $elemMatch — a dotted query matches if ANY element has the course and ANY element has the grade, which is not the same condition
4. S104 has no enrolments, so $unwind drops them. preserveNullAndEmptyArrays: true keeps them
5. Vijayawada 2; Hyderabad 2; Guntur 2
6. reference — a course's instructor would otherwise be duplicated into every enrolled student, and renaming one instructor would mean rewriting several documents

</details>

---

## Course 11 — Business Intelligence Tools

### `data/course-11-bi/dim-date.csv`

**Warm-up**

1. How many quarters appear, and how many months?

**Core**

2. Which calendar month is missing, and what breaks because of it?

**Stretch**

3. Why do BI tools want a dedicated date table rather than the dates already in the fact table?

<details><summary>Answers</summary>

1. 2 quarters, 4 months
2. March. A month-on-month growth measure has no March row to divide by, so April either divides by zero or silently compares to February
3. so that every date in the range exists, including the ones with no transactions. Time intelligence needs a continuous axis

</details>

### `data/course-11-bi/dim-product.csv`

**Warm-up**

1. Which column makes this a snowflake rather than a pure star?

**Core**

2. Compute the margin per product from unit_cost and list_price. Which has the best percentage margin?
3. Should margin be a calculated column or a measure? Why?

<details><summary>Answers</summary>

1. supplier_key — it points at a further dimension table instead of carrying the supplier's attributes inline
2. Notebook at 37.5%
3. a measure — margin percentage must be computed as total profit over total revenue at whatever grain the visual asks for. A calculated column would average the percentages, which is wrong

</details>

### `data/course-11-bi/dim-store.csv`

**Warm-up**

1. How many stores per region?

**Core**

2. A visual shows average revenue by region. Why can that mislead here?

**Stretch**

3. Add a slicer on region. What must you check before trusting the dashboard?

<details><summary>Answers</summary>

1. South 2; North 1
2. South has two stores and North one, so an average per STORE and a total per REGION tell different stories. Say which you mean
3. that every pivot is connected to the slicer through Report Connections — an unconnected visual keeps showing unfiltered data beside filtered ones

</details>

### `data/course-11-bi/fact-sales.csv`

**Warm-up**

1. State the grain, and give SUM and COUNT of qty.

**Core**

2. Join all three dimensions and compute revenue. What is the total, and the South total?
3. DISTINCTCOUNT of product_key against COUNTROWS. Why do they differ?
4. Write a measure for South revenue that ignores whatever region the visual is filtered to.

**Stretch**

5. Check the join added no rows. Why is that worth checking every time?

<details><summary>Answers</summary>

1. one row per product per store per day; SUM 87, COUNT 9, AVERAGE 9.6667
2. 12,880 total, 10,360 South
3. 4 against 9 — one counts distinct values, the other counts rows, and products repeat across days
4. CALCULATE(SUM(revenue), ALL(region), region = "South") — CALCULATE REPLACES filter context rather than adding to it
5. 9 rows in, 9 rows out — a many-to-many on any key would multiply the facts and inflate every total silently

</details>

---

## Course 12 A — Machine Learning

### `data/course-12a-ml/customer-segments.csv`

**Warm-up**

1. Compare the three columns' ranges. What do you notice?

**Core**

2. Cluster with k=3 WITHOUT scaling and score against true_segment.
3. Now scale first and score again.
4. Explain the difference in one sentence.

**Stretch**

5. Use PCA to plot the segments in two dimensions. Should you scale before PCA too?

<details><summary>Answers</summary>

1. annual_spend 1705.00-19188.00; visits_per_year 2.00-35.00; online_ratio 0.01-0.81 — five orders of magnitude apart
2. adjusted Rand index 0.9501
3. adjusted Rand index 1.0000
4. Euclidean distance is dominated by whichever feature has the largest numbers, so unscaled k-Means clusters on annual_spend alone and ignores the other two
5. yes, for the same reason — PCA maximises variance, and an unscaled large-range feature will take the first component by itself

</details>

### `data/course-12a-ml/house-prices.csv`

**Warm-up**

1. How many rows, and what is the price range?

**Core**

2. Split 80/20 and fit multiple linear regression. Report the coefficients.
3. Report MAE, RMSE and R-squared on the fit.
4. The data were built from 12 + 0.045*area + 3.5*beds - 0.25*age. How close are you?
5. Standardise the features and refit. What changes, and what does not?

**Stretch**

6. Add area squared. Does R-squared improve, and is that evidence of a better model?

<details><summary>Answers</summary>

1. 200 rows, 34.30 to 141.24 lakh
2. intercept 12.8380, area 0.043866, bedrooms 3.5773, age -0.2393 (full-data fit)
3. MAE 5.8349, RMSE 7.2067, R-squared 0.9251
4. area 0.04387 against 0.045, bedrooms 3.577 against 3.5, age -0.239 against -0.25
5. the coefficients change scale; the predictions and R-squared do not. Scaling matters for regularisation and distance methods, not for plain least squares
6. R-squared can only rise when you add a term, so it is not evidence. Compare on held-out data, or use adjusted R-squared

</details>

### `data/course-12a-ml/loan-approval.csv`

**Warm-up**

1. What fraction of applications were approved?

**Core**

2. Fit logistic regression with 5-fold cross-validation. What accuracy?
3. Build the confusion matrix and compute precision, recall and F1. Which matters more for a lender?
4. Standardise, then rank the features by coefficient size. Which matters most?

**Stretch**

5. credit_score has by far the biggest RAW coefficient in the rule that generated this data (0.008 against 0.00005 for income), yet income has the larger standardised effect. Explain.
6. You reach 100% accuracy. What has gone wrong?

<details><summary>Answers</summary>

1. 52.67%
2. 0.7767
3. recall on defaults if you fear bad loans; precision on approvals if you fear turning away good customers. The threshold is a business choice, not a statistical one
4. income +1.3450; credit_score +1.2816; debt -1.0221
5. a coefficient is per unit, and the units differ enormously. Income's spread is about 30,000 and credit score's about 160, so coefficient x spread — the effect over the range actually seen — favours income
6. a leak. The labels were drawn from a probability, so some applicants near the boundary went either way and no model can separate them

</details>

---

## Course 12 B — Big Data Technologies

### `data/course-12b-bigdata/web-logs.csv`

**Warm-up**

1. How many requests, distinct IPs and distinct paths?
2. What is the error rate (status 400 or above)?

**Core**

3. Count hits per path. Which is busiest?
4. Write this as a MapReduce. What does the mapper emit, what does the reducer receive, and what does a combiner change?
5. Total bytes per IP. Which IP transferred most?

**Stretch**

6. Do the same three counts a dict, a Hive GROUP BY and a Spark reduceByKey. Must they agree, and why bother?

<details><summary>Answers</summary>

1. 1200 requests, 25 IPs, 8 paths
2. 27.75%
3. /checkout with 165 hits
4. mapper emits (path, 1); reducer receives (path, [1,1,...]) and sums. A combiner sums locally first, cutting shuffle traffic without changing the answer — because addition is associative
5. 10.0.1.21 with 305,868 bytes
6. they must, and checking is how you learn to trust the distributed answer. If reduceByKey disagrees with the dict, the bug is yours, not Spark's

</details>

### `data/course-12b-bigdata/wordcount-corpus.csv`

**Warm-up**

1. Count the words by hand. How many in total, and how many distinct?
2. Which word appears most often, and how many times?

**Core**

3. Now run it as MapReduce and compare with your hand count.
4. Compute TF-IDF for 'dog' and for 'the'. Why does one score near zero?

**Stretch**

5. Lowercase and strip punctuation first. Does the answer change here, and would it on real text?

<details><summary>Answers</summary>

1. 44 words, 28 distinct
2. 'the' 7 times
3. the 7; quick 3; dog 3; brown 2; fox 2
4. 'the' appears in 4 of 5 documents, so its IDF is near zero — a word in every document distinguishes nothing
5. not here — the corpus is already clean lowercase. On real text it changes everything, which is why preprocessing is a step, not an afterthought

</details>

---

## Course 13 A — Artificial Intelligence

### `data/course-13a-ai/family-relations.csv`

**Warm-up**

1. Load it as parent/2 facts. How many facts and how many individuals?

**Core**

2. Define sibling(X,Y). What must you add to stop everyone being their own sibling?
3. Define grandparent(X,Z) :- parent(X,Y), parent(Y,Z). How many solutions?
4. Write ancestor/2 recursively. Which clause must come first, and why?

**Stretch**

5. Trace backtracking on grandparent(john, X). What does unification bind at each step?

<details><summary>Answers</summary>

1. 9 facts, 8 individuals
2. X \= Y — without it, sibling(mary, mary) succeeds through the same parent
3. 6 pairs
4. the base case parent(X,Y) first. Put the recursive clause first and a query with an unbound argument can loop forever
5. Y binds to each of john's children in turn, then Z to each of that child's children; on failure Prolog unbinds Z and retries the next Y

</details>

### `data/course-13a-ai/graph-edges.csv`

**Warm-up**

1. How many nodes and edges? Is the graph directed?

**Core**

2. Run BFS from Arad to Bucharest. What path, how many hops, what cost?
3. Run uniform-cost search. What changes?
4. Why is BFS's answer not wrong?

**Stretch**

5. Add a straight-line heuristic and run A*. What must the heuristic satisfy, and what happens if it does not?
6. Run DFS. Why can it return a much worse path?

<details><summary>Answers</summary>

1. 13 nodes, 16 edges, undirected — each row is traversable both ways
2. Arad-Sibiu-Fagaras-Bucharest, 3 hops, cost 450
3. Arad-Sibiu-Rimnicu-Pitesti-Bucharest, 4 hops, cost 418 — one hop longer and 32 cheaper
4. BFS optimises hops and UCS optimises cost. They answer different questions, and BFS is only optimal for cost when every edge costs the same
5. admissibility — it must never overestimate. An overestimate can prune the optimal path, and A* then returns a worse route while still claiming to be finished
6. it commits to one branch to its end. It is complete on a finite graph but optimal on neither hops nor cost

</details>

### `data/course-13a-ai/map-colouring.csv`

**Warm-up**

1. List each region's neighbours. Which region has none?

**Core**

2. Colour the map with 3 colours by backtracking. Give one valid assignment.
3. Show that 2 colours cannot work.
4. Apply the minimum-remaining-values heuristic. Which variable does it pick first, and which last?

**Stretch**

5. Run AC-3 before search. What does arc consistency prune here, and when does it help most?

<details><summary>Answers</summary>

1. T — Tasmania appears in no adjacency, so it takes any colour
2. many exist; any assignment where WA, NT and SA all differ works
3. WA, NT and SA are mutually adjacent — a triangle needs 3
4. SA first — it has 5 neighbours, the most constrained; T last, being unconstrained
5. little on an uncoloured map with 3 values each; it earns its keep once some variables are assigned, or when domains are large

</details>

---

## Course 13 B — Cloud Computing

### `data/course-13b-cloud/iam-policies.csv`

**Warm-up**

1. How many statements and how many principals?

**Core**

2. Can alice delete reports/q1.csv? Show the evaluation.
3. Can bob read reports/salaries.csv? And reports/q1.csv?
4. carol has s3:* on the bucket. Can she delete?
5. dave appears nowhere. What can he do?

**Stretch**

6. State the evaluation order in full, and say which rule makes 'grant broadly, deny narrowly' workable.

<details><summary>Answers</summary>

1. 7 statements, 3 principals
2. no — she has an explicit Deny on s3:DeleteObject for reports/*, and Deny always wins
3. salaries.csv no — a specific Deny beats the wildcard Allow. q1.csv yes — the Allow applies and nothing denies it
4. no. A wildcard Allow is not unrestricted access when an explicit Deny names the action
5. nothing — anything not explicitly allowed is denied by default
6. explicit Deny, then explicit Allow, then implicit Deny. Because Deny is absolute, a broad Allow can be safely carved back with targeted Denies

</details>

### `data/course-13b-cloud/storage-costs.csv`

**Warm-up**

1. Monthly storage cost per tier, and in total.

**Core**

2. Which tier is cheapest per GB-month, and by what factor against the dearest?
3. Now cost a full retrieval of every byte in archive. Compare with its monthly storage bill.
4. Add egress for that retrieval. What is the true cost?

**Stretch**

5. How often must you read the archive tier before it stops being the cheapest option? State the assumption your answer depends on.

<details><summary>Answers</summary>

1. standard 11.50; infrequent 25.00; archive 7.92; total 44.42
2. archive — 23.2x cheaper than the dearest
3. retrieval 160.00 against storage 7.92 — about 20 months of storage in a single read
4. 880.00 — egress is charged on top and is usually the bigger surprise
5. roughly once every few years on these numbers; the answer depends entirely on how much of it you read each time, which is the assumption every cloud cost model hides

</details>

---

## Course 14 A — Deep Learning

### `data/course-14a-deeplearning/sensor-failures.csv`

**Warm-up**

1. What fraction of readings are failures?
2. Scatter temperature against vibration, coloured by label. What shape is the boundary?

**Core**

3. Fit logistic regression with cross-validation. What accuracy?
4. Now fit a network with one or two hidden layers.
5. Why can the linear model not be fixed by training longer?

**Stretch**

6. Five per cent of labels were flipped when the file was built. What does that imply about any accuracy above 0.95?

<details><summary>Answers</summary>

1. 66.50%
2. an ellipse — failures lie OUTSIDE a safe region in the middle
3. 0.6650
4. 0.9150 — about 25 points better
5. its decision boundary is a straight line and the true one is closed and curved. No amount of training changes the shape of the hypothesis
6. it is impossible on held-out data — the ceiling is 0.95. A higher figure means you scored on the training set or leaked the label

</details>

### `data/course-14a-deeplearning/xor.csv`

**Warm-up**

1. Plot the four points. Can you separate the 1s from the 0s with a straight line?

**Core**

2. Train a single-layer perceptron. What is the best accuracy it reaches, however long you train?
3. Add one hidden layer of two units with a non-linear activation. What happens?
4. Replace the activation with the identity. Does the hidden layer still help?

**Stretch**

5. Do one forward and one backward pass by hand on a 2-2-1 network. Where does the chain rule enter?

<details><summary>Answers</summary>

1. no — (0,1) and (1,0) are the 1s and they sit on opposite corners
2. 0.75 — three of the four. Exhausting the weight space confirms it: no line does better
3. it reaches 1.0. The hidden layer bends the space so a line in the new space is a curve in the old one
4. no — a stack of linear maps is a linear map. The non-linearity is what the hidden layer is FOR
5. at every layer: the gradient at a weight is the local derivative times the gradient flowing back from above. That product is backpropagation

</details>

---

## Course 14 B — Time Series

### `data/course-14b-timeseries/ar2-series.csv`

**Warm-up**

1. Plot the series. Does it look stationary, and what would tell you it was not?
2. Compute the lag-1 and lag-2 autocorrelations.

**Core**

3. Plot the ACF and PACF. What order do they suggest, and which plot tells you?
4. Estimate the coefficients with Yule-Walker.
5. Fit ARIMA(2,0,0) and compare AIC with ARIMA(1,0,0) and ARIMA(3,0,0). Which wins?

**Stretch**

6. Run ADF and KPSS. What does each test's null hypothesis say, and why run both?
7. Run Ljung-Box on the residuals. What are you hoping for?

<details><summary>Answers</summary>

1. yes — no trend and constant variance. A wandering level or growing swings would say otherwise
2. r1 = 0.5036, r2 = 0.0169
3. AR(2) — the PACF cuts off after lag 2 while the ACF tails off. For an MA process it is the other way round
4. phi1 = 0.6634, phi2 = -0.3173 (built from 0.6 and -0.3)
5. the AR(2) should, and if AR(3) edges it, check whether the third coefficient is distinguishable from zero
6. ADF's null is a unit root; KPSS's null is stationarity. They point opposite ways, so agreement is strong evidence and disagreement tells you the case is borderline
7. a LARGE p-value — you want to fail to reject, meaning no autocorrelation is left for the model to have captured

</details>

### `data/course-14b-timeseries/macro-indicators.csv`

**Warm-up**

1. Plot all three series. Which two look related?

**Core**

2. Test whether rates Granger-cause inflation.
3. Now test the reverse direction.
4. Test the control series in both directions. What should you find, and why does it matter?
5. Fit a VAR. How do you choose the lag order?

**Stretch**

6. Your test fires in BOTH directions on some other dataset. What have you found?

<details><summary>Answers</summary>

1. rates and inflation; the third is a control with no relationship
2. yes, strongly — the lagged rates improve the inflation model
3. no. The causality was planted one way only
4. nothing significant either way. A control that stays quiet is what tells you the test is not simply firing on everything
5. by information criterion — AIC or BIC over candidate lags, not by eye
6. feedback, or a common driver you have not modelled. Granger causality is about predictive precedence, not cause

</details>

### `data/course-14b-timeseries/seasonal-sales.csv`

**Warm-up**

1. How many months, and over how many years?

**Core**

2. Decompose into trend, season and remainder. Is the season additive or multiplicative here?
3. Which calendar month is strongest and which weakest?
4. Difference at lag 12. What does the standard deviation do?
5. Now difference again at lag 1. What is left?

**Stretch**

6. Fit SARIMA with s=12 and forecast 12 months. Do the intervals widen, and should they?
7. Compare Holt-Winters with SARIMA. When would you prefer each?

<details><summary>Answers</summary>

1. 72 months, 6 years
2. additive — the swing stays about the same size as the level rises
3. 4 at 1437.27, 9 at 984.12 — a swing of 453.15
4. 225.55 falls to 49.89 — the season is gone, the trend remains
5. close to noise. Doing the two in the wrong order leaves the season tangled in the trend
6. yes — uncertainty compounds with horizon. A forecast whose interval does not widen is not a forecast
7. Holt-Winters for a quick, robust seasonal forecast with little tuning; SARIMA when you want diagnostics and a model you can defend term by term

</details>

---

## Course 15 A — Natural Language Processing

### `data/course-15a-nlp/ner-sentences.csv`

**Warm-up**

1. How many sentences, and how many gold entities in total?
2. Which entity types appear, and how often?

**Core**

3. Run spaCy's NER and compare against the gold column. Compute precision and recall.
4. Which entities does an English model most often get wrong here?

**Stretch**

5. Your model tags 'Krishna' as PERSON. Is that a bug, and what would fix it?

<details><summary>Answers</summary>

1. 5 sentences, 15 entities
2. DATE 3; GPE 5; LOC 1; MONEY 1; ORG 3; PERSON 2
3. match on both span and type; a right span with the wrong label is a miss, not a hit
4. Indian state and river names — 'Andhra Pradesh' and 'Krishna' are far rarer in the training data than the city names
5. not a bug — it is a genuine ambiguity resolved by context the model lacks. Fine-tuning on Indian text, or a gazetteer, is what fixes it

</details>

### `data/course-15a-nlp/sentiment-reviews.csv`

**Warm-up**

1. How many reviews, and is the set balanced?
2. Tokenize and remove stopwords. How does the vocabulary shrink?

**Core**

3. Stem and lemmatize 'works', 'working', 'stopped'. Where do the two disagree?
4. Build bag-of-words and TF-IDF features and cross-validate Naive Bayes on each.
5. Which review is hardest, and why?

**Stretch**

6. With 20 reviews, how much should you trust a 5% difference between two models?

<details><summary>Answers</summary>

1. 20 reviews, 10 positive and 10 negative — balanced, so 0.5 is the coin-flip baseline
2. 106 raw tokens before stopword removal
3. a stemmer chops to a possibly non-word ('studi'); a lemmatizer returns a dictionary form ('study'). Stemming is faster, lemmatizing is correct
4. bag-of-words 0.8000, TF-IDF 0.7500
5. 'Works well but the cable is too short' — positive overall, but it carries negative words, and bag-of-words cannot see the 'but'
6. not at all. One review is 5% of the data, so the fold-to-fold spread swamps a gap that size

</details>

---

## Course 15 B — Data Engineering and MLOps

### `data/course-15b-mlops/loan-current.csv`

**Warm-up**

1. Compare each feature's mean against the reference batch. Which has moved?

**Core**

2. Compute the PSI for each feature against the reference.
3. The usual thresholds are 0.1 for 'investigate' and 0.2 for 'act'. What do you do?
4. Run a two-sample KS test on each feature. Does it agree with PSI?
5. Score the reference model on the new batch. Has accuracy collapsed?

**Stretch**

6. Your monitoring fires a retrain. Should you? Argue both sides.

<details><summary>Answers</summary>

1. income 54849.8 -> 53932.4; debt 25843.5 -> 25278.0; credit_score 649.5 -> 589.6
2. income 0.0262; debt 0.0378; credit_score 0.4909
3. credit_score at 0.491 clears the action threshold; the other two do not. Investigate the score feed first
4. income p=0.907; debt p=0.468; credit_score p=1.49e-16
5. no — the inputs shifted but the input-to-label relationship did not. This is DATA drift, not CONCEPT drift
6. retraining costs a deployment and gains almost nothing here, because the rule generating the label is unchanged. But a shifting input distribution is a warning that the population is changing, so investigate the cause rather than either retraining on reflex or ignoring it

</details>

### `data/course-15b-mlops/loan-reference.csv`

**Warm-up**

1. Summarise each feature: mean and spread.

**Core**

2. Train a classifier and log it with MLflow. What must you log for the run to be reproducible?
3. Register the model and tag it as the baseline. Why does the registry matter more than the file?

**Stretch**

4. Put the data under DVC. What goes into git, and what does not?

<details><summary>Answers</summary>

1. income mean 54849.8 sd 18503.3; debt mean 25843.5 sd 15002.7; credit_score mean 649.5 sd 87.6
2. parameters, metrics, the model artifact, the data version and the random seed. A metric with no parameters beside it proves nothing
3. it names which version is in production and lets you roll back. A file on disk records neither
4. a small pointer file goes into git; the bytes go to the DVC remote. That is how the repository stays small while the data is versioned

</details>

