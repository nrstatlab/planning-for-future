# Practical Lab

**15 experiments**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results.

Code lives in `labs/course-11-bi/`.

> **On the tooling.** Power BI Desktop is **Windows-only** and Tableau Desktop
> is proprietary; neither can be installed in the environment these notes are
> verified in. So each experiment has two halves:
>
> - **The click-path** — the exact menus, panes and dialogs, in a box under **3. Steps**.
>   It is **not run here**. **This is what the lab examiner will ask you to
>   demonstrate.**
> - **A Python equivalent that runs** — the same transformation, measure or
>   join, executed and asserted by
>   `tools/data-science/run_bi_labs.py`. Its steps, its code and what it printed are under
>   **3. Steps**, **4. Programme** and **5. Execution and Results**.
>
> **Eleven of the fifteen have a runnable half.** Experiments 1, 2, 8 and 12
> are pure tool operation with nothing to compute, so they are click-path only
> and say so. The runner asserts that list against what is on disk, so an
> experiment cannot quietly go missing.
>
> The Python halves are **not a substitute for the tools**. They exist so every
> figure in these notes is produced by running code — when Unit 3 claims a fan
> trap turns ₹12,880 into ₹25,760, experiment 14 proves it.

```bash
pip install -r tools/requirements.txt
python3 tools/data-science/run_bi_labs.py
```

## Getting the tools

| Tool | How | Catch |
|---|---|---|
| **Power BI Desktop** | Free from the Microsoft Store or download centre | **Windows only.** Mac users need a VM or Parallels |
| **Power BI Service** | app.powerbi.com, free tier | **Sharing needs Pro** on both sides |
| **Tableau Public** | Free download, no licence | **Everything you save is published to the open web** |
| **Tableau Desktop** | 14-day trial, or a free **student licence** (1 year, with proof of enrolment) | Apply early — approval takes days |

<div class="warn" markdown="1">
<span class="label">READ THIS BEFORE EXPERIMENT 8</span>

**Tableau Public publishes your workbook to the internet and lets anyone
download it.** For the sample datasets these experiments use, that is fine
and intended. **Never put real student, employee, patient or customer data in
it.** Check what is in the extract before you press Save. This is a genuine,
repeated real-world data breach, not a theoretical worry.
</div>

## What to submit

| Tool | File | Why |
|---|---|---|
| Power BI | **`.pbix`** | Contains queries, model, measures and data |
| Tableau | **`.twbx`** | **Packaged.** A `.twb` carries no data and opens empty |

**Submitting a `.twb` is the commonest way to lose lab marks.**

---

## Experiment 1 — Exploring BI tools: Power BI vs Tableau

### 1. Question

Explore the BI tools: compare Power BI with Tableau.

### 2. Aim

Load the same data into both tools, build one chart in each, and compare them from experience.

### 3. Steps

1. **Install both tools.**
2. **Load the same CSV into each.**
3. **Build one bar chart in each.**
4. **Fill in the comparison table** from what you actually experienced, not from a blog:

| Criterion | Power BI | Tableau |
|---|---|---|
| Time to first chart | | |
| Where you got stuck | | |
| Data preparation | Power Query | Data Source tab / Prep |
| Calculation language | DAX, M | Calculated fields, LOD |
| Desktop OS | Windows only | Windows and macOS |
| Cost to share | Pro per user | Public free (and public) |

### 4. Programme

There is no program: this is a comparison, not a computation — **click-path only**.

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Power BI Desktop, which runs only on Windows, and Tableau Desktop or Tableau Public, which this environment cannot install, so nothing on this page claims to have done it.
</div>

**For the viva:** the differences that decide real deployments are **cost,
existing stack, who builds the reports, and macOS** — not the feature list. The
tools have converged. Unit 1 §1.7 has the full comparison.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A comparison table filled in from your own use of both tools.
</div>


## Experiment 2 — A simple retail dashboard in both tools

### 1. Question

Build a simple retail dashboard in Power BI and in Tableau.

### 2. Aim

Build the same three-visual dashboard twice, once in each tool.

### 3. Steps

Use the star schema from `fixtures.py` — export it to CSV first, or use any retail dataset.

1. **In Power BI:** Get Data → Text/CSV → Transform Data → set types → Close &
   Apply → Model view → check relationships → build three visuals (a card, a
   ranked bar, a line) → arrange per Unit 5 §5.5.
2. **In Tableau:** Connect → Text file → drag the fact and dimension tables onto
   the canvas → Sheet 1 → build the same three views → New Dashboard → drag them
   in.
3. **Note where each tool made you stop and think.**

### 4. Programme

There is no program — **click-path only**.

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Power BI Desktop, which runs only on Windows, and Tableau Desktop or Tableau Public, which this environment cannot install, so nothing on this page claims to have done it.
</div>

**Build the same dashboard twice and note where each tool made you stop and
think.** That comparison is worth more than either dashboard.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The same dashboard in both tools, and a note of where each one made you stop and think.
</div>


## Experiment 3 — Connecting to different data sources in Power BI

### 1. Question

Connect Power BI to different data sources: Excel, CSV, the web and a folder.

### 2. Aim

Load each kind of source, and catch the way each one fails silently.

### 3. Steps

**In Python**, `03_data_sources.py`:

1. **Load a CSV, and check it round-trips.**
2. **Read a semicolon file as comma-separated.**
3. **Read UTF-8 as Latin-1.**
4. **Load a sheet, and then a table.**
5. **Flatten a web API's nested JSON.**
6. **Compare Import with DirectQuery.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN POWER BI</span>

```
Get Data -> Excel Workbook   -> pick the TABLE, not the sheet
Get Data -> Text/CSV         -> CHECK the delimiter and encoding in the preview
Get Data -> Web              -> paste a JSON URL, then expand records and lists
Get Data -> Folder           -> Combine, for many identically shaped files
```
</div>


<div class="formula" markdown="1">
<span class="label">THE TRAPS</span>

The Python half runs each format and demonstrates its **silent** failure mode:

| Trap | What happens | Asserted |
|---|---|---|
| Wrong delimiter | A semicolon CSV read as comma gives **one column**, no error | ✓ |
| Wrong encoding | UTF-8 read as Latin-1 turns `Vijayawāda` into `VijayawÄda` | ✓ |
| Sheet, not table | The header becomes `"Monthly Sales Report"` and 4 junk rows load | ✓ |
| Nested JSON | Cells contain dicts and lists until `json_normalize` flattens them | ✓ |
</div>


### 4. Programme

**In Python**, `03_data_sources.py`:

{{programme: course-11-bi/03_data_sources.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Power BI Desktop, which runs only on Windows, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `03_data_sources.py`:

{{output: course-11-bi/03_data_sources.py}}

**All four fail silently.** That is why the preview pane exists, and why you
look at it before pressing Load.

**Also asserted:** the Import vs DirectQuery comparison. Import is the default.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

All four traps are reproduced and fixed; each one fails without an error, which is why the preview pane exists.
</div>


## Experiment 4 — Data cleaning and transformation with Power Query

### 1. Question

Clean and transform data with Power Query.

### 2. Aim

Apply each Power Query step, and see that the order of the steps changes the answer.

### 3. Steps

**In Python**, `04_power_query.py`:

1. **Trim and clean the text.**
2. **See that changing case does not trim.**
3. **Fill down.**
4. **Replace values, and set the types.**
5. **Remove duplicates, on chosen columns.**
6. **Swap the order of two steps.**
7. **Unpivot.**
8. **Group by, and merge queries.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN POWER BI</span>

```
Transform -> Format -> Trim / Capitalize Each Word
Transform -> Fill -> Down
Home      -> Remove Rows -> Remove Duplicates
Transform -> Replace Values
Transform -> Unpivot Columns
Home      -> Merge Queries / Append Queries
Transform -> Group By
```
</div>


### 4. Programme

**In Python**, `04_power_query.py`:

{{programme: course-11-bi/04_power_query.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Power BI Desktop, which runs only on Windows, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `04_power_query.py`:

{{output: course-11-bi/04_power_query.py}}

<div class="warn" markdown="1">
<span class="label">STEP ORDER CHANGES THE ANSWER</span>

The same two steps in two orders, on the same seven rows:

| Order | Rows left | Total |
|---|---:|---:|
| De-duplicate, **then** clean | 6 | **₹7,660** |
| Clean, **then** de-duplicate | 4 | **₹5,280** |

A difference of **₹2,380**. `"  Vijayawada "` and `"Vijayawada"` are not
duplicates until they have been trimmed, so de-duplicating first misses them.

**Clean before you de-duplicate** — and this is why Applied Steps is an
*ordered list* and not a set.
</div>

Also asserted: replacing `"n/a"` with **null** gives a mean of 1,393.33 and
with **0** gives 1,194.29, while the **sum is identical** either way. Ratios
and averages move; totals do not.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Every step is reproduced; cleaning before de-duplicating leaves 4 rows and ₹5,280, the other order 6 rows and ₹7,660.
</div>


## Experiment 5 — Student performance: clean, reshape, visualize

### 1. Question

Clean, reshape and visualise a student performance dataset.

### 2. Aim

Clean and unpivot the marks, decide what an absence counts as, and build the pass-rate measure.

### 3. Steps

**In Python**, `05_student_performance.py`:

1. **Clean and unpivot the marks.**
2. **Record AB as null, and then as zero.**
3. **Compute the subject and programme averages.**
4. **Build the pass-rate measure.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN POWER BI</span>

The higher-education case from Unit 1 §1.4 and Unit 2 §2.7.

```
Remove Duplicates on (student, semester, subject)
Select the subject columns -> Unpivot Columns
Trim, then Change Type to whole number
Replace Values: "AB" -> null
```
</div>


### 4. Programme

**In Python**, `05_student_performance.py`:

{{programme: course-11-bi/05_student_performance.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Power BI Desktop, which runs only on Windows, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `05_student_performance.py`:

{{output: course-11-bi/05_student_performance.py}}

<div class="warn" markdown="1">
<span class="label">THE "AB" DECISION IS THE EXAMINABLE PART</span>

| Absent recorded as | Mean | n | Pass rate |
|---|---:|---:|---:|
| **null** (excluded) | **72.9167** | 12 | **100.00%** |
| **0** (counted) | **58.3333** | 15 | **80.00%** |

**A gap of 14.58 marks and 20 percentage points.** Neither is wrong — but the
dashboard must say which it did, or two departments will report different pass
rates from one file. That is a governance point (Unit 4 §4.6) arriving early.
</div>

**Also asserted:** subject averages (Maths 74.75, Stats 76.00, Python 68.00,
n = 4 each), programme averages (BSc-DS 80.25 over 8 marks, BSc-STAT 58.25 over
**4**), and the rate-measure shape — `CALCULATE` in the numerator, plain
`COUNTROWS` in the denominator.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Absences as null give a mean of 72.9167 and a 100% pass rate; as zero, 58.3333 and 80%.
</div>


## Experiment 6 — Implementing DAX functions

### 1. Question

Implement DAX functions: aggregation, iterators, CALCULATE, ALL, DIVIDE and IF.

### 2. Aim

Write each measure, and check every value against Unit 2's figures.

### 3. Steps

**In Python**, `06_dax_functions.py`:

1. **SUM, COUNT and AVERAGE.**
2. **See COUNT and COUNTROWS disagree on blanks.**
3. **SUMX, row by row.**
4. **CALCULATE, which replaces the filter.**
5. **KEEPFILTERS, which intersects it.**
6. **ALL, for a percentage of the total.**
7. **DIVIDE, against the slash.**
8. **Margin as a column and as a measure.**
9. **IF and SWITCH.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN POWER BI</span>

```dax
Total Qty     = SUM(fact_sales[qty])
Line Count    = COUNTROWS(fact_sales)
Avg Qty       = AVERAGE(fact_sales[qty])
Total Revenue = SUMX(fact_sales, fact_sales[qty] * RELATED(dim_product[list_price]))
South Revenue = CALCULATE([Total Revenue], dim_store[region] = "South")
Pct of Total  = DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(dim_store)))
Order Size    = IF([Total Qty] > 10, "Large", "Small")
```
</div>


<div class="formula" markdown="1">
<span class="label">THE VALUES</span>

Asserted, every one against the figures in Unit 2:

| Claim | Value |
|---|---:|
| `SUM(qty)` | 87 |
| `COUNTROWS` | 9 |
| `AVERAGE(qty)` | 9.667 |
| `SUMX(qty × price)` | **₹12,880** |
| `SUM(qty) × SUM(price)` — the wrong way | **₹140,940** |
| `[South Revenue]` on the **North** row | **₹10,360** |
| % of total | South 80.43%, North 19.57% |
| Margin as a **column**, averaged | **29.7619%** |
| Margin as a **measure** | **27.3680%** |
</div>


### 4. Programme

**In Python**, `06_dax_functions.py`:

{{programme: course-11-bi/06_dax_functions.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Power BI Desktop, which runs only on Windows, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `06_dax_functions.py`:

{{output: course-11-bi/06_dax_functions.py}}

**The last two are the most valuable numbers in the course.** The gap is
**2.3939 percentage points**, and the script also asserts that the correct
answer *is* the revenue-weighted average of the row margins — which is what
"aggregate, then divide" means.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

SUMX gives ₹12,880 where SUM × SUM gives ₹140,940; margin as a measure is 27.3680%, as an averaged column 29.7619%.
</div>


## Experiment 7 — Creating basic visualizations in Power BI

### 1. Question

Create basic visualizations in Power BI: cards, bar and line charts, and a matrix.

### 2. Aim

Compute the data behind each visual and check it, then draw the bar and line charts.

### 3. Steps

**In Python**, `07_visualizations.py`:

1. **Compute the card values.**
2. **Rank the bar chart's categories.**
3. **Order the line chart's quarters.**
4. **Build the matrix.**
5. **Check the pie chart's shares.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN POWER BI</span>

```
Visualizations pane -> Card    -> drop a measure
                    -> Stacked bar chart -> Axis: category, Values: revenue
                    -> Line chart -> Axis: a continuous date
                    -> Matrix    -> Rows: region, Columns: category
Format pane -> Y axis -> Start at zero
```
</div>


<div class="formula" markdown="1">
<span class="label">THE POINT</span>

A chart cannot be asserted; the **data behind it** can, and that is where
visuals go wrong. Asserted: four card values, the ranked bar (Grocery ₹9,800,
Personal ₹1,680, Stationery ₹1,400), the quarterly line (Q1 ₹7,660 → Q2 ₹5,220,
**−31.85%**), and the region × category matrix with margins.
</div>


### 4. Programme

**In Python**, `07_visualizations.py`:

{{programme: course-11-bi/07_visualizations.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Power BI Desktop, which runs only on Windows, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `07_visualizations.py`:

{{output: course-11-bi/07_visualizations.py}}

The two charts above are the ranked bar and the quarterly line, as the program drew
them. **Changed:** they were written to `output/`, which now holds what each program printed;
the program writes them to `plots/`.

<div class="example" markdown="1">
<span class="label">THE PIE CHART CHECK, COMPUTED</span>

Category shares are 76.09%, 13.04% and 10.87%. The two small slices differ by
**2.17 points** — nearly indistinguishable as angles, obvious as bar lengths.
The script also notes that the *rounded* labels total **100.0001%**, which is
why a pie's printed percentages so often fail to add up.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Grocery leads at ₹9,800; revenue falls 31.85% from Q1 to Q2; the two small pie slices differ by only 2.17 points.
</div>


## Experiment 8 — Tableau basics and connecting to data

### 1. Question

Learn Tableau's basics, and connect it to data.

### 2. Aim

Connect to a file, build a first view, and know what saving to Tableau Public does.

### 3. Steps

1. **Connect** → To a File → Text file / Microsoft Excel.
2. **On the Data Source tab**, drag tables to the canvas, and choose Live or Extract.
3. **On Sheet 1**, drag a dimension to Rows and a measure to Columns.
4. **Save:** Server → Tableau Public → Save to Tableau Public As… — but first re-read the
   warning at the top of this page.

### 4. Programme

There is no program — **click-path only**:

```
Connect -> To a File -> Text file / Microsoft Excel
Data Source tab -> drag tables to the canvas -> choose Live or Extract
Sheet 1 -> drag a dimension to Rows, a measure to Columns
Server -> Tableau Public -> Save to Tableau Public As...
```

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Tableau Desktop or Tableau Public, which this environment cannot install, so nothing on this page claims to have done it.
</div>

**Before you save: re-read the warning at the top of this page.** Tableau
Public makes the workbook and its data available to anyone.

**For the viva:** blue = discrete = **headers**; green = continuous = **axes**.
It is not about field type — a date can be either, and converting between them
changes the chart entirely.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A first view, and the difference between blue (discrete) and green (continuous) fields.
</div>


## Experiment 9 — Employee turnover in Tableau, with LOD expressions

### 1. Question

Analyse employee turnover in Tableau with level-of-detail expressions.

### 2. Aim

Compute attrition by department against a FIXED company rate, and see where a small denominator misleads.

### 3. Steps

**In Python**, `09_hr_lod.py`:

1. **Compute the headline measures.**
2. **Compare each department with a FIXED company rate.**
3. **Find the small denominator.**
4. **INCLUDE and EXCLUDE.**
5. **See FIXED ignore a dimension filter.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN TABLEAU</span>

```
Attrition Rate  = SUM([Is Leaver]) / COUNTD([Emp Id])
Company Rate    = {FIXED : [Attrition Rate]}
Gap vs Company  = [Attrition Rate] - [Company Rate]
```
</div>


<div class="formula" markdown="1">
<span class="label">THE TABLE</span>

Asserted on 15 employees across 4 departments:

| department | n | leavers | attrition | company | gap |
|---|---:|---:|---:|---:|---:|
| Support | 1 | 1 | **100.00%** | 33.33% | +66.67 |
| Sales | 5 | 2 | 40.00% | 33.33% | +6.67 |
| HR | 3 | 1 | 33.33% | 33.33% | +0.00 |
| Engineering | 6 | 1 | 16.67% | 33.33% | −16.67 |

**`{FIXED : …}` with no dimension is constant on every row** — that is what
makes the company benchmark possible at all.
</div>


### 4. Programme

**In Python**, `09_hr_lod.py`:

{{programme: course-11-bi/09_hr_lod.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Tableau Desktop or Tableau Public, which this environment cannot install, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `09_hr_lod.py`:

{{output: course-11-bi/09_hr_lod.py}}

<div class="warn" markdown="1">
<span class="label">SUPPORT TOPS THE CHART AND IS NOT THE PROBLEM</span>

**One employee. One leaver. 100%.** One person's decision moved it 100 points.
The script asserts that suppressing departments with fewer than 3 people leaves
Engineering, HR and Sales — the standard fix. **Show headcount beside every
rate.** That is Statistical Foundations for Data Science's sampling variability, in an HR chart.
</div>

**Also asserted:** everyone who left had ≤1.5 years' tenure (mean 1.0 against
5.0 for stayers) — the actual finding, from two measures; and that `INCLUDE`
gives Sales **687,500** against the view's **554,000**, because it averages the
four Execs and the one Manager as *two* numbers. **That is the
average-of-averages trap wearing Tableau's clothes.**

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Support's 100% is one person; the company rate is 33.33%; INCLUDE gives Sales 687,500 against the view's 554,000.
</div>


## Experiment 10 — Cleaning, pivoting and filtering in Tableau

### 1. Question

Clean, pivot and filter data in Tableau.

### 2. Aim

Pivot the quarter columns, and see that the order of the filters changes the answer.

### 3. Steps

**In Python**, `10_tableau_prep.py`:

1. **Pivot the quarter columns.**
2. **Rank, then filter, and the other way round.**
3. **Set out the order of operations.**
4. **Split, alias and clean.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN TABLEAU</span>

```
Data Source tab -> select the quarter columns -> Pivot
Column menu -> Split / Custom Split
Column menu -> Aliases...
Filters shelf -> right-click a filter -> Add to Context
```
</div>


<div class="formula" markdown="1">
<span class="label">THE VOCABULARY</span>

**Tableau's "Pivot" is Power Query's "Unpivot".** Opposite names, same operation.
`melt` in pandas. Getting the vocabulary right per tool is worth a mark.
</div>


### 4. Programme

**In Python**, `10_tableau_prep.py`:

{{programme: course-11-bi/10_tableau_prep.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Tableau Desktop or Tableau Public, which this environment cannot install, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `10_tableau_prep.py`:

{{output: course-11-bi/10_tableau_prep.py}}

<div class="warn" markdown="1">
<span class="label">FILTER ORDER — THE EXAM QUESTION, DEMONSTRATED</span>

Asking for the **top 2 stores in North**:

| Approach | Result |
|---|---|
| Rank first, then filter to North | **0 rows** — the overall top 2 is all South |
| Filter to North first, then rank | **2 rows**, ₹1,920 and ₹600 |

**Promote the region filter to a context filter** so it runs before the Top-N.
The full six-step order is asserted so it cannot be misremembered.
</div>

**Also asserted:** an **alias changes only the display**. The stored value is
untouched — so an alias cannot fix a join key.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Ranking before filtering finds no North store in the top 2; a context filter finds ₹1,920 and ₹600.
</div>


## Experiment 11 — Creating visualizations in Tableau

### 1. Question

Create visualizations in Tableau with the shelves and the Marks card.

### 2. Aim

Count the marks each view draws, fix the one-dot scatter, and synchronise a dual axis.

### 3. Steps

**In Python**, `11_tableau_viz.py`:

1. **Count the marks for each set of dimensions.**
2. **Fix the scatter plot with one dot.**
3. **Try each Marks card encoding.**
4. **Synchronise a dual axis.**
5. **Assign geographic roles.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN TABLEAU</span>

```
Rows / Columns shelves -> dimensions and measures
Marks card -> Colour, Size, Label, Detail, Tooltip
Show Me -> suggested chart types
Two measures on Rows -> right-click the second axis -> Dual Axis -> Synchronize Axis
```
</div>


<div class="formula" markdown="1">
<span class="label">THE RESULTS</span>

Asserted:

- **Granularity is set by the dimensions in the view.** No dimension → **1
  mark**. Region → 2. Store → 3. Store + category → **5, not 9**, because
  Tableau draws a mark only where data exists.
- **The scatter plot with one dot.** Two measures and no dimension aggregate to
  a single mark; product on **Detail** gives 4 marks and a correlation of
  **0.9591**. This is always the missing Detail dimension.
- **Colour and Detail split marks; Size, Label and Tooltip do not.** Detail is
  the dangerous one — it changes granularity and changes nothing visible.
- **Dual axis.** Revenue fell **31.85%** and profit only **22.86%**, so margin
  *rose* **3.43 points**. Two falling lines whose real story is the gap between
  them — which an unsynchronised dual axis rescales away. **Synchronize Axis.**
</div>


### 4. Programme

**In Python**, `11_tableau_viz.py`:

{{programme: course-11-bi/11_tableau_viz.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Tableau Desktop or Tableau Public, which this environment cannot install, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `11_tableau_viz.py`:

{{output: course-11-bi/11_tableau_viz.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Store and category give 5 marks, not 9; product on Detail gives the scatter 4 marks and r = 0.9591; margin rose 3.43 points.
</div>


## Experiment 12 — Creating a Tableau story

### 1. Question

Create a story in Tableau.

### 2. Aim

Build a story whose points each make one claim, and publish it.

### 3. Steps

1. **New Story:** drag a sheet or dashboard onto the story point.
2. **Caption box:** replace the default text with the CLAIM.
3. **Duplicate:** change ONE thing — a filter, a highlight, an annotation.
4. **Annotate:** right-click a mark → Annotate → Mark / Point / Area.
5. **Publish:** Server → Tableau Public → Save.

**The structure that works** (Unit 3 §3.8):

```
Context -> Complication -> Cause -> Consequence -> Call to action
```

### 4. Programme

There is no program — **click-path only**:

```
New Story -> drag a sheet or dashboard onto the story point
Caption box -> replace the default text with the CLAIM
Duplicate -> change ONE thing (a filter, a highlight, an annotation)
Right-click a mark -> Annotate -> Mark / Point / Area
Server -> Tableau Public -> Save
```

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Tableau Desktop or Tableau Public, which this environment cannot install, so nothing on this page claims to have done it.
</div>

**Each story point makes exactly one claim.** The commonest failure is seven
points showing the same dashboard with different filters and no argument.

**Submit the published link**, and check it opens in a private browser window —
that is how the examiner will open it.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A published story, each point making exactly one claim, that opens in a private browser window.
</div>


## Experiment 13 — Designing data models in Power BI

### 1. Question

Design a data model in Power BI: a star schema and its relationships.

### 2. Aim

Build the star, compare it with one flat table, and find the argument that decides between them.

### 3. Steps

**In Python**, `13_data_model.py`:

1. **Build the star.**
2. **Snowflake one dimension.**
3. **Count the cells, star against flat.**
4. **Ask what did not sell.**
5. **Mistype a store.**
6. **Sort the measures by additivity.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN POWER BI</span>

```
Model view -> drag product_key from fact_sales to dim_product
Double-click the relationship -> Cardinality: Many to one (*:1)
                              -> Cross filter direction: Single
Modeling -> Mark as Date Table -> pick the date column
Right-click a key column -> Hide in report view
```
</div>


<div class="formula" markdown="1">
<span class="label">THE STORAGE</span>

Asserted, against Unit 4 §4.3:

| Model | Cells |
|---|---:|
| Star — fact 36 + dimensions 56 | **92** |
| One flat table — 9 × 16 | **144** |

and the projection: at 1,000 fact rows the flat table costs **3.94×**; at a
million, **4.00×** — converging, because dimensions do not grow.
</div>


### 4. Programme

**In Python**, `13_data_model.py`:

{{programme: course-11-bi/13_data_model.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Power BI Desktop, which runs only on Windows, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `13_data_model.py`:

{{output: course-11-bi/13_data_model.py}}

<div class="example" markdown="1">
<span class="label">BUT STORAGE IS THE WEAKEST OF THE FOUR ARGUMENTS</span>

The script asserts the decisive one instead: **a flat table cannot report what
did not happen.** Remove P4's sales and the flat table shows **3 products** —
P4 is invisible. The star shows **4**, with P4 blank.

*"Which products sold nothing last month?"* is unanswerable from a flat table
and trivial from a star. **That is the argument to give in the exam.**
</div>

**Also asserted:** every dimension key is unique (so every relationship is
1:\*); one mistyped `"Vijaywada"` creates a **fourth store** in a flat table
and cannot happen in a star; and the three additivity classes — revenue totals
₹12,880 however you slice it, margin does not, and stock 50/48/55 sums to
**153 units that never existed**, which is why it needs its own snapshot fact
table.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The star holds 92 cells to the flat table's 144; the flat table shows 3 products where the star shows 4.
</div>


## Experiment 14 — Joins and blending in Tableau

### 1. Question

Combine data in Tableau with joins and with blending.

### 2. Aim

Reproduce the fan trap, fix it three ways, and compare the four join types.

### 3. Steps

**In Python**, `14_joins_blending.py`:

1. **Compute the correct totals.**
2. **Join on the store alone.**
3. **Fix one: join on the full grain.**
4. **Fix two: blend.**
5. **Fix three: a FIXED LOD.**
6. **Compare the four join types.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN TABLEAU</span>

```
Data Source tab -> drag the second table -> click the join icon
                -> Inner / Left / Right / Full Outer, and set the join clauses
Second connection -> Data menu -> the linking icon 🔗 on the shared field
```
</div>


### 4. Programme

**In Python**, `14_joins_blending.py`:

{{programme: course-11-bi/14_joins_blending.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Tableau Desktop or Tableau Public, which this environment cannot install, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `14_joins_blending.py`:

{{output: course-11-bi/14_joins_blending.py}}

<div class="warn" markdown="1">
<span class="label">THE FAN TRAP — THE MOST VALUABLE NUMERIC RESULT IN THIS COURSE</span>

9 sales rows joined to a targets table with **2 rows per store**, on store
alone:

| | Correct | After the join |
|---|---:|---:|
| Rows | 9 | **18** |
| `SUM(Revenue)` | ₹12,880 | **₹25,760** (×2) |
| `SUM(Target)` | ₹20,800 | **₹66,700** (×3.21) |

Revenue doubled uniformly; targets inflated **unevenly** — T1's ₹10,500 met 4
sales rows (₹42,000), T2's ₹6,200 met 2 (₹12,400), T3's ₹4,100 met 3
(₹12,300). **No error was raised.** Both numbers are simply wrong.
</div>

**Three fixes, all asserted:**

| Fix | Result |
|---|---|
| Join on **store *and* quarter** | 9 rows, revenue ₹12,880 ✓ — but the naive target sum is **still ₹32,900** |
| **Blend** (aggregate, then match) | 3 rows, revenue ₹12,880 ✓ **and** target ₹20,800 ✓ |
| `{FIXED [Store] : SUM([Target])}` | Recovers ₹20,800 even from the broken join |

**Note that fixing the grain fixed revenue but not the target.** A measure from
the "one" side always needs de-duplicating. **Blending is the only fix that
gets both right in one step** — because it is a *left join performed after
aggregation*, which is the sentence to say in the exam.

**Also asserted:** the four join types on data with a deliberate orphan —
inner 3 rows, left 4, right 4, full outer 5. *"Which stores sold nothing?"* is
a left join filtered to null.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The join on the store alone doubles revenue to ₹25,760 and inflates targets to ₹66,700; only blending gets both totals right in one step.
</div>


## Experiment 15 — A dashboard with drill-downs, filters and slicers

### 1. Question

Build an interactive dashboard with drill-downs, filters, slicers and parameters.

### 2. Aim

Drill, filter and vary a parameter, and see which of them changes the rows and which the calculation.

### 3. Steps

**In Python**, `15_dashboard_interactivity.py`:

1. **Drill down the hierarchy.**
2. **Drill into one item, and expand all.**
3. **Apply the filters.**
4. **Vary a parameter.**
5. **Drill through.**
6. **Tell the four features apart.**

<div class="formula" markdown="1">
<span class="label">THE CLICK-PATH, IN POWER BI</span>

```
Model view -> right-click a column -> Create hierarchy -> add levels
Visual -> the drill icons (down arrow, forked arrow, up arrow)
Report page -> right-click -> Add drillthrough page
Modeling -> New parameter -> Numeric range
Insert -> Slicer
```
</div>


<div class="formula" markdown="1">
<span class="label">THE RESULTS</span>

Asserted:

- **Drilling never changes the total.** Region → Store → Product gives 2, 3
  then **5** rows, all totalling ₹12,880. *If it changes when you drill, the
  model is wrong* — usually a fan trap.
- **Expand all ≠ drill down on one item.** Expand all keeps every region (3
  rows, ₹12,880); drilling into South filters to it (2 rows, ₹10,360). Users
  read both as "the number".
- **Filters intersect.** 9 rows → 6 (South) → 4 (South *and* Grocery). Which is
  why a dashboard with six slicers usually shows zero.
- **A parameter changes what is calculated, not which rows.** At −5%, 0%, +5%
  and +10% the projected revenue is ₹12,236 / ₹12,880 / ₹13,524 / ₹14,168 —
  and the row count is **9 in every scenario**. That is the distinction the
  exam wants, and it is the DSS model component (Unit 1 §1.6) inside a BI tool.
- **Drill-through** to a Grocery detail page gives 5 rows summing to ₹9,800,
  matching the summary tile.
</div>


### 4. Programme

**In Python**, `15_dashboard_interactivity.py`:

{{programme: course-11-bi/15_dashboard_interactivity.py}}

### 5. Execution and Results

<div class="warn" markdown="1">
<span class="label">NOT RUN HERE</span>

The click-path needs Power BI Desktop, which runs only on Windows, so nothing on this page claims to have done it. What follows is the Python half, which runs: the same operation, executed and asserted.
</div>

**In Python**, `15_dashboard_interactivity.py`:

{{output: course-11-bi/15_dashboard_interactivity.py}}

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Drilling keeps ₹12,880 at every level; filters cut 9 rows to 4; a parameter changes the projection and leaves 9 rows in every scenario.
</div>


---

## Lab examination

An hour, a dataset, one experiment number, then a viva.

**What costs marks:**

- Submitting a `.twb` instead of a `.twbx` — it opens with no data
- De-duplicating before trimming, so duplicates survive
- Using a calculated column where a measure was needed, then averaging it
- Writing `a / b` instead of `DIVIDE(a, b)`
- Joining on a partial key and not noticing the totals doubled
- Building one flat table and calling it a model
- Leaving cross-filter direction on **Both** to make a slicer work
- A scatter plot with one dot
- Using the fact table's date column instead of a date dimension
- A dashboard that scrolls
- Red/green for good/bad

**What earns them:**

- **Say the grain out loud before you model anything.** "One row per product
  per store per day." Every later decision follows from it.
- **Check a total after every join.** If revenue changed when you added a
  table, you have a fan trap. Say so, and fix it by joining on the full grain
  or by blending.
- **Explain a measure in business words.** "Margin is total profit over total
  revenue — not the average of the line margins, because that would weight a
  ₹600 line the same as a ₹2,800 one."
- **Justify the schema.** "Star, because joins cost query time and storage is
  cheap. `dim_supplier` is snowflaked because supplier attributes are shared
  across products and change independently."
- **State what a dashboard is for and who acts on it.** *"When this number
  moves, who does what?"* If you cannot answer, say so — that is the correct
  answer, and it shows judgement.
- **When asked why a number looks wrong, check the filter order.** A Top-N
  before a dimension filter ranks across everything. Promote it to a context
  filter.
