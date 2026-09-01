# Course 11 — Practical Lab

**15 experiments**

Code lives in `labs/course-11-bi/`.

> **On the tooling.** Power BI Desktop is **Windows-only** and Tableau Desktop
> is proprietary; neither can be installed in the environment these notes are
> verified in. So each experiment has two halves:
>
> - **The click-path** — the exact menus, panes and dialogs, written out below.
>   Marked **NOT EXECUTED**. **This is what the lab examiner will ask you to
>   demonstrate.**
> - **A Python equivalent that runs** — the same transformation, measure or
>   join, executed and asserted by
>   `tools/run_bi_labs.py`.
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
python3 tools/run_bi_labs.py
```

## Getting the tools

| Tool | How | Catch |
|---|---|---|
| **Power BI Desktop** | Free from the Microsoft Store or download centre | **Windows only.** Mac users need a VM or Parallels |
| **Power BI Service** | app.powerbi.com, free tier | **Sharing needs Pro** on both sides |
| **Tableau Public** | Free download, no licence | **Everything you save is published to the open web** |
| **Tableau Desktop** | 14-day trial, or a free **student licence** (1 year, with proof of enrolment) | Apply early — approval takes days |

> ### ⚠️ Read this before experiment 8
>
> **Tableau Public publishes your workbook to the internet and lets anyone
> download it.** For the sample datasets these experiments use, that is fine
> and intended. **Never put real student, employee, patient or customer data in
> it.** Check what is in the extract before you press Save. This is a genuine,
> repeated real-world data breach, not a theoretical worry.

## What to submit

| Tool | File | Why |
|---|---|---|
| Power BI | **`.pbix`** | Contains queries, model, measures and data |
| Tableau | **`.twbx`** | **Packaged.** A `.twb` carries no data and opens empty |

**Submitting a `.twb` is the commonest way to lose lab marks.**

---

## Experiment 1 — Exploring BI tools: Power BI vs Tableau

**Click-path only** — a comparison, not a computation.

Install both, load the same CSV into each, and build one bar chart in each.
Then fill in this table from what you actually experienced, not from a blog:

| Criterion | Power BI | Tableau |
|---|---|---|
| Time to first chart | | |
| Where you got stuck | | |
| Data preparation | Power Query | Data Source tab / Prep |
| Calculation language | DAX, M | Calculated fields, LOD |
| Desktop OS | Windows only | Windows and macOS |
| Cost to share | Pro per user | Public free (and public) |

**For the viva:** the differences that decide real deployments are **cost,
existing stack, who builds the reports, and macOS** — not the feature list. The
tools have converged. Unit 1 §1.7 has the full comparison.

## Experiment 2 — A simple retail dashboard in both tools

**Click-path only.**

Use the star schema from
`fixtures.py` — export it to CSV
first, or use any retail dataset.

**In Power BI:** Get Data → Text/CSV → Transform Data → set types → Close &
Apply → Model view → check relationships → build three visuals (a card, a
ranked bar, a line) → arrange per Unit 5 §5.5.

**In Tableau:** Connect → Text file → drag the fact and dimension tables onto
the canvas → Sheet 1 → build the same three views → New Dashboard → drag them
in.

**Build the same dashboard twice and note where each tool made you stop and
think.** That comparison is worth more than either dashboard.

## Experiment 3 — Connecting to different data sources in Power BI

**Both halves.** `03_data_sources.py`

```
Get Data -> Excel Workbook   -> pick the TABLE, not the sheet
Get Data -> Text/CSV         -> CHECK the delimiter and encoding in the preview
Get Data -> Web              -> paste a JSON URL, then expand records and lists
Get Data -> Folder           -> Combine, for many identically shaped files
```

The Python half runs each format and demonstrates its **silent** failure mode:

| Trap | What happens | Asserted |
|---|---|---|
| Wrong delimiter | A semicolon CSV read as comma gives **one column**, no error | ✓ |
| Wrong encoding | UTF-8 read as Latin-1 turns `Vijayawāda` into `VijayawÄda` | ✓ |
| Sheet, not table | The header becomes `"Monthly Sales Report"` and 4 junk rows load | ✓ |
| Nested JSON | Cells contain dicts and lists until `json_normalize` flattens them | ✓ |

**All four fail silently.** That is why the preview pane exists, and why you
look at it before pressing Load.

**Also asserted:** the Import vs DirectQuery comparison. Import is the default.

## Experiment 4 — Data cleaning and transformation with Power Query

**Both halves.** `04_power_query.py`

```
Transform -> Format -> Trim / Capitalize Each Word
Transform -> Fill -> Down
Home      -> Remove Rows -> Remove Duplicates
Transform -> Replace Values
Transform -> Unpivot Columns
Home      -> Merge Queries / Append Queries
Transform -> Group By
```

Asserted: every step above, and the one that matters most —

### ⚠️ Step order changes the answer

The same two steps in two orders, on the same seven rows:

| Order | Rows left | Total |
|---|---:|---:|
| De-duplicate, **then** clean | 6 | **₹7,660** |
| Clean, **then** de-duplicate | 4 | **₹5,280** |

A difference of **₹2,380**. `"  Vijayawada "` and `"Vijayawada"` are not
duplicates until they have been trimmed, so de-duplicating first misses them.

**Clean before you de-duplicate** — and this is why Applied Steps is an
*ordered list* and not a set.

Also asserted: replacing `"n/a"` with **null** gives a mean of 1,393.33 and
with **0** gives 1,194.29, while the **sum is identical** either way. Ratios
and averages move; totals do not.

## Experiment 5 — Student performance: clean, reshape, visualize

**Both halves.** `05_student_performance.py`

The higher-education case from Unit 1 §1.4 and Unit 2 §2.7.

```
Remove Duplicates on (student, semester, subject)
Select the subject columns -> Unpivot Columns
Trim, then Change Type to whole number
Replace Values: "AB" -> null
```

### ⚠️ The "AB" decision is the examinable part

| Absent recorded as | Mean | n | Pass rate |
|---|---:|---:|---:|
| **null** (excluded) | **72.9167** | 12 | **100.00%** |
| **0** (counted) | **58.3333** | 15 | **80.00%** |

**A gap of 14.58 marks and 20 percentage points.** Neither is wrong — but the
dashboard must say which it did, or two departments will report different pass
rates from one file. That is a governance point (Unit 4 §4.6) arriving early.

**Also asserted:** subject averages (Maths 74.75, Stats 76.00, Python 68.00,
n = 4 each), programme averages (BSc-DS 80.25 over 8 marks, BSc-STAT 58.25 over
**4**), and the rate-measure shape — `CALCULATE` in the numerator, plain
`COUNTROWS` in the denominator.

## Experiment 6 — Implementing DAX functions

**Both halves.** `06_dax_functions.py`

```dax
Total Qty     = SUM(fact_sales[qty])
Line Count    = COUNTROWS(fact_sales)
Avg Qty       = AVERAGE(fact_sales[qty])
Total Revenue = SUMX(fact_sales, fact_sales[qty] * RELATED(dim_product[list_price]))
South Revenue = CALCULATE([Total Revenue], dim_store[region] = "South")
Pct of Total  = DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(dim_store)))
Order Size    = IF([Total Qty] > 10, "Large", "Small")
```

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

**The last two are the most valuable numbers in the course.** The gap is
**2.3939 percentage points**, and the script also asserts that the correct
answer *is* the revenue-weighted average of the row margins — which is what
"aggregate, then divide" means.

## Experiment 7 — Creating basic visualizations in Power BI

**Both halves.** `07_visualizations.py`

```
Visualizations pane -> Card    -> drop a measure
                    -> Stacked bar chart -> Axis: category, Values: revenue
                    -> Line chart -> Axis: a continuous date
                    -> Matrix    -> Rows: region, Columns: category
Format pane -> Y axis -> Start at zero
```

A chart cannot be asserted; the **data behind it** can, and that is where
visuals go wrong. Asserted: four card values, the ranked bar (Grocery ₹9,800,
Personal ₹1,680, Stationery ₹1,400), the quarterly line (Q1 ₹7,660 → Q2 ₹5,220,
**−31.85%**), and the region × category matrix with margins.

The two charts are rendered to `labs/course-11-bi/output/` so the shapes can be
looked at.

### 💡 The pie chart check, computed

Category shares are 76.09%, 13.04% and 10.87%. The two small slices differ by
**2.17 points** — nearly indistinguishable as angles, obvious as bar lengths.
The script also notes that the *rounded* labels total **100.0001%**, which is
why a pie's printed percentages so often fail to add up.

## Experiment 8 — Tableau basics and connecting to data

**Click-path only.**

```
Connect -> To a File -> Text file / Microsoft Excel
Data Source tab -> drag tables to the canvas -> choose Live or Extract
Sheet 1 -> drag a dimension to Rows, a measure to Columns
Server -> Tableau Public -> Save to Tableau Public As...
```

**Before you save: re-read the warning at the top of this page.** Tableau
Public makes the workbook and its data available to anyone.

**For the viva:** blue = discrete = **headers**; green = continuous = **axes**.
It is not about field type — a date can be either, and converting between them
changes the chart entirely.

## Experiment 9 — Employee turnover in Tableau, with LOD expressions

**Both halves.** `09_hr_lod.py`

```
Attrition Rate  = SUM([Is Leaver]) / COUNTD([Emp Id])
Company Rate    = {FIXED : [Attrition Rate]}
Gap vs Company  = [Attrition Rate] - [Company Rate]
```

Asserted on 15 employees across 4 departments:

| department | n | leavers | attrition | company | gap |
|---|---:|---:|---:|---:|---:|
| Support | 1 | 1 | **100.00%** | 33.33% | +66.67 |
| Sales | 5 | 2 | 40.00% | 33.33% | +6.67 |
| HR | 3 | 1 | 33.33% | 33.33% | +0.00 |
| Engineering | 6 | 1 | 16.67% | 33.33% | −16.67 |

**`{FIXED : …}` with no dimension is constant on every row** — that is what
makes the company benchmark possible at all.

### ⚠️ Support tops the chart and is not the problem

**One employee. One leaver. 100%.** One person's decision moved it 100 points.
The script asserts that suppressing departments with fewer than 3 people leaves
Engineering, HR and Sales — the standard fix. **Show headcount beside every
rate.** That is Course 4's sampling variability, in an HR chart.

**Also asserted:** everyone who left had ≤1.5 years' tenure (mean 1.0 against
5.0 for stayers) — the actual finding, from two measures; and that `INCLUDE`
gives Sales **687,500** against the view's **554,000**, because it averages the
four Execs and the one Manager as *two* numbers. **That is the
average-of-averages trap wearing Tableau's clothes.**

## Experiment 10 — Cleaning, pivoting and filtering in Tableau

**Both halves.** `10_tableau_prep.py`

```
Data Source tab -> select the quarter columns -> Pivot
Column menu -> Split / Custom Split
Column menu -> Aliases...
Filters shelf -> right-click a filter -> Add to Context
```

### ⚠️ Tableau's "Pivot" is Power Query's "Unpivot"

Opposite names, same operation. `melt` in pandas. Getting the vocabulary right
per tool is worth a mark.

### ⚠️ Filter order — the exam question, demonstrated

Asking for the **top 2 stores in North**:

| Approach | Result |
|---|---|
| Rank first, then filter to North | **0 rows** — the overall top 2 is all South |
| Filter to North first, then rank | **2 rows**, ₹1,920 and ₹600 |

**Promote the region filter to a context filter** so it runs before the Top-N.
The full six-step order is asserted so it cannot be misremembered.

**Also asserted:** an **alias changes only the display**. The stored value is
untouched — so an alias cannot fix a join key.

## Experiment 11 — Creating visualizations in Tableau

**Both halves.** `11_tableau_viz.py`

```
Rows / Columns shelves -> dimensions and measures
Marks card -> Colour, Size, Label, Detail, Tooltip
Show Me -> suggested chart types
Two measures on Rows -> right-click the second axis -> Dual Axis -> Synchronize Axis
```

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

## Experiment 12 — Creating a Tableau story

**Click-path only.**

```
New Story -> drag a sheet or dashboard onto the story point
Caption box -> replace the default text with the CLAIM
Duplicate -> change ONE thing (a filter, a highlight, an annotation)
Right-click a mark -> Annotate -> Mark / Point / Area
Server -> Tableau Public -> Save
```

**The structure that works** (Unit 3 §3.8):

```
Context -> Complication -> Cause -> Consequence -> Call to action
```

**Each story point makes exactly one claim.** The commonest failure is seven
points showing the same dashboard with different filters and no argument.

**Submit the published link**, and check it opens in a private browser window —
that is how the examiner will open it.

## Experiment 13 — Designing data models in Power BI

**Both halves.** `13_data_model.py`

```
Model view -> drag product_key from fact_sales to dim_product
Double-click the relationship -> Cardinality: Many to one (*:1)
                              -> Cross filter direction: Single
Modeling -> Mark as Date Table -> pick the date column
Right-click a key column -> Hide in report view
```

Asserted, against Unit 4 §4.3:

| Model | Cells |
|---|---:|
| Star — fact 36 + dimensions 56 | **92** |
| One flat table — 9 × 16 | **144** |

and the projection: at 1,000 fact rows the flat table costs **3.94×**; at a
million, **4.00×** — converging, because dimensions do not grow.

### 💡 But storage is the weakest of the four arguments

The script asserts the decisive one instead: **a flat table cannot report what
did not happen.** Remove P4's sales and the flat table shows **3 products** —
P4 is invisible. The star shows **4**, with P4 blank.

*"Which products sold nothing last month?"* is unanswerable from a flat table
and trivial from a star. **That is the argument to give in the exam.**

**Also asserted:** every dimension key is unique (so every relationship is
1:\*); one mistyped `"Vijaywada"` creates a **fourth store** in a flat table
and cannot happen in a star; and the three additivity classes — revenue totals
₹12,880 however you slice it, margin does not, and stock 50/48/55 sums to
**153 units that never existed**, which is why it needs its own snapshot fact
table.

## Experiment 14 — Joins and blending in Tableau

**Both halves.** `14_joins_blending.py`

```
Data Source tab -> drag the second table -> click the join icon
                -> Inner / Left / Right / Full Outer, and set the join clauses
Second connection -> Data menu -> the linking icon 🔗 on the shared field
```

### ⚠️ The fan trap — the most valuable numeric result in this course

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

## Experiment 15 — A dashboard with drill-downs, filters and slicers

**Both halves.** `15_dashboard_interactivity.py`

```
Model view -> right-click a column -> Create hierarchy -> add levels
Visual -> the drill icons (down arrow, forked arrow, up arrow)
Report page -> right-click -> Add drillthrough page
Modeling -> New parameter -> Numeric range
Insert -> Slicer
```

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
