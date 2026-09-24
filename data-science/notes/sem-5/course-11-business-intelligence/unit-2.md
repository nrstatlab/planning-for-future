# Unit 2 — Data Preparation and Visualization with Power BI

**Syllabus topics:** Introduction to Power BI; the Power BI ecosystem —
Desktop, Service, Mobile; the Power BI interface; data sources — Excel, CSV,
SQL Server, Web APIs; Power Query — data preparation, cleaning and
transformation; connect, transform and model a dataset; basic DAX functions —
SUM, COUNT, AVERAGE, CALCULATE, IF; creating simple visualizations — charts,
tables, cards; sharing reports via the Power BI Service. Case studies —
student performance analysis in higher education; analyzing a finance dataset.

> **All figures in this unit are computed from the sample star schema in
> `labs/course-11-bi/fixtures.py`**
> and asserted by the lab scripts, so the notes and the code check each other.
> The fact table is nine rows — small enough to verify every number by hand.

---

## 2.1 The Power BI ecosystem

### 🎯 The big idea

**Power BI is three products around one file format, and knowing which does
what is the first exam question on this unit.**

| Product | Runs on | What you do in it | Cost |
|---|---|---|---|
| **Power BI Desktop** | **Windows only** | **Build** — connect, transform, model, design reports | **Free** |
| **Power BI Service** | The browser (app.powerbi.com) | **Share** — publish, workspaces, dashboards, scheduled refresh, row-level security | Free tier; **Pro** per user to share |
| **Power BI Mobile** | iOS, Android, Windows | **Consume** — view, filter, receive alerts. Not authoring | Free |

```
   Power BI Desktop  --publish-->  Power BI Service  -->  Power BI Mobile
   (build the .pbix)               (share and refresh)     (consume)
        Windows                         browser              phone
```

### ⚠️ Three things students get wrong here

1. **Desktop is Windows-only.** No macOS build exists. Mac users run a VM,
   Parallels, or work in the Service. This is examined, and per Unit 1 §1.7 it
   decides real tool choices.
2. **A report is not a dashboard — in Power BI they are different objects.**

   | | **Report** | **Dashboard** |
   |---|---|---|
   | Built in | Desktop or Service | **Service only** |
   | Pages | Multiple | **One canvas** |
   | Made of | Visuals bound to a dataset | **Tiles pinned** from one or more reports |
   | Data sources | One dataset | **Several datasets** |
   | Interactivity | Slicers, filters, cross-filtering | Limited |

   Tableau uses the two words the other way round, which is why this trips
   people who learn both.
3. **`.pbix` contains everything** — the queries, the model, the measures, and
   in Import mode a compressed copy of the data. That is why the file is large,
   and why you never email one holding real data.

### The interface — six things to be able to name

| Area | What it does |
|---|---|
| **Ribbon** | Home, Insert, Modeling, View |
| **Canvas** | Where visuals are placed |
| **Visualizations pane** | Choose a chart type; drop fields into its wells (Axis, Legend, Values) |
| **Data / Fields pane** | Tables, columns and measures in the model |
| **Filters pane** | Filters at visual, page and report level |
| **The three view icons** (left edge) | **Report** · **Table** (Data) · **Model** |

**Model view is the one that matters and the one beginners never open.** It is
where relationships live, and Unit 4 is entirely about what you do there.

---

## 2.2 Connecting to data

| Source | How | Watch for |
|---|---|---|
| **Excel** | Get Data → Excel Workbook | Choose the **Table**, not the sheet, when one exists — sheets bring blank rows and merged cells |
| **CSV / Text** | Get Data → Text/CSV | **Check delimiter and encoding.** UTF-8 vs ANSI silently mangles names |
| **SQL Server** | Get Data → SQL Server | Choose **Import** or **DirectQuery**; write a query rather than importing a table you will filter later |
| **Web API** | Get Data → Web | Returns JSON; Power Query parses it into records and lists that you expand |
| Folder | Get Data → Folder | Combines many identically-shaped files — the right answer to "twelve monthly CSVs" |

### 🔢 Import vs DirectQuery — an examinable choice

| | **Import** | **DirectQuery** |
|---|---|---|
| Where data sits | **Copied into the .pbix**, compressed in memory | **Stays in the source**; queries sent live |
| Speed | **Fast** — in-memory columnar engine | Depends on the source, usually slower |
| Freshness | As of the last **refresh** | **Live** |
| Size | Model limits apply (1 GB on Pro) | No copy, so no limit |
| DAX | **All of it** | A restricted subset |
| Use when | Almost always | Data is too large to copy, or must be to-the-second |

**Import is the default and the right answer unless told otherwise.** "Import,
unless the data is too large to copy or must be real-time" earns the mark.

---

## 2.3 Power Query — where the real work happens

### 🎯 The big idea

**Power Query records your cleaning as an ordered list of steps and replays it
on every refresh.** You are not editing data; you are writing a recipe.

That is the most important idea in this unit, and it is what separates it from
cleaning in Excel. Fix a file in Excel and you have fixed one file. Fix it in
Power Query and it is fixed every month for ever, with the Applied Steps pane
documenting exactly what you did.

The language underneath is **M** — case-sensitive, and *not* DAX.

### 🔢 The transformations to know

Each has a pandas equivalent, given because
`labs/course-11-bi/` runs them and asserts the
result. Learning the pair makes both stick.

| Power Query (ribbon) | What it does | pandas |
|---|---|---|
| Remove Columns | Drop fields | `df.drop(columns=[...])` |
| Keep / Remove Rows | Filter | `df[df.qty > 0]` |
| **Remove Duplicates** | De-duplicate | `df.drop_duplicates()` |
| **Replace Values** | Substitute | `df.replace(...)` |
| **Fill Down** | Carry a value into the blanks below | `df.ffill()` |
| Change Type | Set the data type | `astype(...)` |
| **Split Column** | By delimiter or position | `str.split(expand=True)` |
| Merge Columns | Concatenate | `df.a + df.b` |
| **Unpivot Columns** | Wide → long | **`pd.melt`** |
| Pivot Column | Long → wide | `df.pivot` |
| **Merge Queries** | **Join** two tables | `pd.merge` |
| **Append Queries** | Stack rows | `pd.concat` |
| Group By | Aggregate | `df.groupby().agg()` |
| Add Custom Column | Computed column | `df.assign(...)` |

### ⚠️ Unpivot is the one that gets examined

Spreadsheets arrive **wide** — a column per month — and BI tools need **long**,
one row per observation.

```
WIDE (as received)                  LONG (what a BI tool needs)
store   Jan    Feb                  store   month   sales
T1      5000   5200        →        T1      Jan     5000
T2      3000   3100                 T1      Feb     5200
                                    T2      Jan     3000
                                    T2      Feb     3100
```

**Why it matters:** the wide form cannot be charted over time without naming
every column, and it breaks the moment February's column arrives. The long form
charts itself and never needs editing. Course 9 Unit 5 called this `melt` — it
is the same operation, and the same reasoning.

### 💡 Power Query or DAX? The rule that decides it

> **If it can be done in Power Query, do it in Power Query.**

| Do it in **Power Query** (M) | Do it in **DAX** |
|---|---|
| Cleaning, shaping, fixing types | Aggregations over the model |
| Splitting, merging, unpivoting | Anything depending on **user selection** |
| Joins that should be permanent | Time intelligence (YTD, prior year) |
| Anything computable **once, at refresh** | Anything computed **per visual** |

**Why:** Power Query runs once at refresh and its output is compressed by the
storage engine. DAX runs on every interaction. A calculated column written in
DAX costs memory in every query; the same column made in Power Query is usually
cheaper.

---

## 2.4 DAX — the parts the syllabus names

### 🎯 The one distinction that governs everything

**A calculated column is computed row by row, at refresh, and stored. A measure
is computed at query time, in whatever filter the visual supplies, and stores
nothing.**

| | **Calculated column** | **Measure** |
|---|---|---|
| Evaluated | Once, at refresh | **Every time a visual renders** |
| Context | **Row context** — sees one row | **Filter context** — sees a filtered table |
| Stored | Yes; costs memory | No |
| Can be placed on | Rows, columns, slicers, axis | **Values only** |
| Write one when | You need to slice or group by it | You need a number that responds to selection |

**Default to a measure.** Create a calculated column only when the result must
appear on an axis or in a slicer.

### 🔢 The five functions the syllabus names

```dax
Total Qty     = SUM(fact_sales[qty])
Order Lines   = COUNT(fact_sales[qty])           -- non-blank values
Line Count    = COUNTROWS(fact_sales)            -- rows; prefer this
Avg Qty       = AVERAGE(fact_sales[qty])
Order Size    = IF([Total Qty] > 10, "Large", "Small")
South Revenue = CALCULATE([Total Revenue], dim_store[region] = "South")
```

Against the sample data, asserted in
`06_dax_functions.py`:

| Measure | Value |
|---|---:|
| `Total Qty` | **87** |
| `COUNTROWS(fact_sales)` | **9** |
| `Avg Qty` | **9.667** (87 ÷ 9) |
| `Total Revenue` = `SUMX(fact_sales, qty × list_price)` | **₹12,880** |
| `Total Profit` | **₹3,525** |

### ⚠️ COUNT vs COUNTROWS vs DISTINCTCOUNT

| Function | Counts | Here |
|---|---|---:|
| `COUNT(col)` | **Non-blank values** in a column | 9 |
| `COUNTROWS(table)` | **Rows**, blanks included | 9 |
| `DISTINCTCOUNT(col)` | **Distinct values** | `DISTINCTCOUNT(product_key)` = **4** |

**`COUNT` ignores blanks and `COUNTROWS` does not.** On a column with missing
values they disagree, and that disagreement is the exam question. Prefer
`COUNTROWS` when you mean "how many rows".

### 🔢 CALCULATE — the function the whole language turns on

**`CALCULATE` evaluates an expression in a filter context that you modify.** It
is the only way to make a measure override what the visual is filtering, and it
is the most examined function in DAX.

```dax
South Revenue = CALCULATE([Total Revenue], dim_store[region] = "South")
```

Put both measures in a table sliced by region and this appears — asserted in
the lab:

| region | `[Total Revenue]` | `[South Revenue]` |
|---|---:|---:|
| North | ₹2,520 | **₹10,360** |
| South | ₹10,360 | **₹10,360** |
| **Total** | **₹12,880** | ₹10,360 |

**Read the North row carefully.** `[South Revenue]` shows ₹10,360 *on the North
row*. The filter inside `CALCULATE` **replaced** that row's region filter rather
than adding to it. That surprise is the point of the function, and the answer to
"explain CALCULATE with an example".

### 🔢 The modifiers, and % of total

| Modifier | Effect |
|---|---|
| `ALL(table/column)` | **Remove** filters — the basis of every "% of total" |
| `ALLEXCEPT(t, cols)` | Remove all filters except the named ones |
| `ALLSELECTED()` | Respect the user's slicers, ignore the visual's own grouping |
| `KEEPFILTERS(...)` | **Intersect** with the existing filter instead of replacing it |
| `REMOVEFILTERS(...)` | The modern, clearer spelling of `ALL` |

```dax
Pct of Total = DIVIDE([Total Revenue],
                      CALCULATE([Total Revenue], ALL(dim_store)))
```

| region | Revenue | Pct of Total |
|---|---:|---:|
| South | ₹10,360 | **80.43%** |
| North | ₹2,520 | **19.57%** |

**Use `DIVIDE`, never `/`.** `DIVIDE(a, b)` returns blank on a zero
denominator; `a / b` raises an error that breaks the entire visual.

### ⚠️ The average-of-averages trap — the most valuable thing in this unit

Write margin % as a **calculated column** and then average it, and the answer is
wrong. Both numbers below are asserted in the lab.

```dax
-- WRONG: a calculated column, then AVERAGE
Margin Pct (col) = DIVIDE(fact_sales[profit], fact_sales[revenue])
Avg Margin       = AVERAGE(fact_sales[Margin Pct (col)])   -- 29.76%

-- RIGHT: a measure, aggregating first
Margin Pct = DIVIDE([Total Profit], [Total Revenue])       -- 27.37%
```

| Approach | Result |
|---|---:|
| `AVERAGE` of the per-row margin column | **29.7619%** |
| `SUM(profit) ÷ SUM(revenue)` | **27.3680%** |

**Why they differ:** averaging the column treats a ₹600 line and a ₹2,800 line
as equally important. The measure weights each line by its revenue, which is
what "margin" means. The gap here is 2.4 points; on real data it can invert a
ranking.

**The rule: aggregate, then divide — never divide, then average.** Every ratio
in BI obeys it: margin, conversion rate, average order value, cost per
acquisition.

### `IF` and `SWITCH`

```dax
Order Size = IF([Total Qty] > 10, "Large", "Small")

Band = SWITCH(TRUE(),
        [Total Qty] > 15, "Large",
        [Total Qty] > 8,  "Medium",
        "Small")
```

**`SWITCH(TRUE(), …)` is the DAX idiom for a nested `IF`.** Use it beyond two
branches; nested `IF`s become unreadable at three.

---

## 2.5 Simple visualizations

| Visual | Use for | Do not |
|---|---|---|
| **Bar / Column** | Comparing categories | Start the value axis anywhere but **zero** |
| **Line** | A trend **over time** | Use it for unordered categories |
| **Card** | **One** headline number | Fill a page with them |
| **Table / Matrix** | Exact values; a matrix is a pivot table | Use it when the *shape* is the point |
| **Pie / Donut** | Parts of a whole, **≤ 5 slices** | Use more slices, or compare across pies |
| **Map** | Genuinely geographic questions | Use it when a bar chart would rank better |
| **KPI** | A value against a target, with a trend | Show it without the target |

### 💡 Cards, and the one-number discipline

A **card** shows a single measure. The temptation is a row of eight; the
discipline is **three to five, above the fold, chosen because someone acts on
them**. Unit 5 §5.3 develops this.

**Format in the model, not the visual.** Set a measure's format string once (₹,
0 decimals) and every visual inherits it. Formatting per-visual is how one
report ends up showing ₹12,880.00 in one place and ₹12.88K in another.

---

## 2.6 Sharing via the Power BI Service

```
Desktop  --Publish-->  Workspace  -->  App  -->  colleagues
                            |
                            +-- Scheduled refresh (8/day Pro, 48 Premium)
                            +-- Row-level security (RLS)
                            +-- Dashboards (pinned tiles)
```

| Concept | What it is |
|---|---|
| **Workspace** | A container for reports and datasets, with roles — Admin, Member, Contributor, Viewer |
| **App** | A polished, read-only bundle published from a workspace. **This is how you share with the wider business** |
| **Dataset** | The model. Several reports can share one — which is how you avoid five versions of "revenue" |
| **Scheduled refresh** | Re-runs the Power Query steps on a timetable |
| **Gateway** | An agent letting the cloud Service reach an **on-premises** source |
| **Row-level security** | Filters rows by who is viewing — a store manager sees only their store |

### ⚠️ Publishing is free; sharing is not

Both sender and recipient need a **Pro** licence, unless the workspace sits on
Premium capacity. Students discover this the first time they try to send a
report to a classmate.

### 💡 Row-level security answers a common exam scenario

"How would you let each regional manager see only their own region?" — **RLS.**
Define a role with a DAX filter driven by `USERPRINCIPALNAME()`, assign users to
it, and one report serves everyone. Building three copies of the report is the
wrong answer, and it is the one most students give.

---

## 2.7 Case study — student performance in higher education

Lab experiment 5, and the education domain from Unit 1 §1.4.

**The data.** One row per student per subject per semester: `student_id`,
`semester`, `subject`, `marks`, `attendance_pct`, `programme`.

**The preparation, in Power Query:**

| Problem | Step |
|---|---|
| Marks arrive as text with stray spaces | Trim, then Change Type to whole number |
| Absent recorded as `"AB"` | Replace Values → `null`, so it is excluded rather than counted as zero |
| One column per subject | **Unpivot** to one row per subject |
| Duplicate rows from a re-upload | Remove Duplicates on (student, semester, subject) |
| Programme codes differ between years | Merge Queries against a mapping table |

### ⚠️ The `"AB"` decision changes the answer, so state it

Replacing absent with **0** drags the average down and treats absence as
failure. Replacing it with **null** excludes it, so the average describes only
students who sat the exam. **Neither is wrong — but the dashboard must say which
it did**, or two departments will report different pass rates from one file.
That is the governance point of Unit 4 §4.6, arriving early.

**The measures:**

```dax
Avg Marks   = AVERAGE(marks[marks])
Pass Rate   = DIVIDE(CALCULATE(COUNTROWS(marks), marks[marks] >= 40),
                     COUNTROWS(marks))
Distinction = CALCULATE(COUNTROWS(marks), marks[marks] >= 75)
Subject Rank= RANKX(ALL(dim_subject[subject]), [Avg Marks], , DESC)
```

Note `Pass Rate` — `CALCULATE` in the numerator, plain `COUNTROWS` in the
denominator. **That shape is every rate measure in BI**, and it is the pattern
worth memorising.

---

## Practice problems

### Problem 1

Distinguish a calculated column from a measure. Give an example where the wrong
choice produces a wrong answer. *(10 marks)*

**Solution.**

Give the table from §2.4 — evaluation time, context, storage, placement. State
the rule: **default to a measure; use a column only when you must slice, group
or filter by the value.**

Then the worked example, which is where the marks are. Over nine sales rows
carrying profit and revenue:

- **As a calculated column:** `margin = profit / revenue` per row, then
  `AVERAGE` → **29.7619%**
- **As a measure:** `DIVIDE(SUM(profit), SUM(revenue))` → **27.3680%**

The column is wrong because it weights a ₹600 line and a ₹2,800 line equally;
the measure weights by revenue, which is what margin means.

**State the rule: aggregate, then divide — never divide, then average.** Add
that the calculated column also costs memory in every query while the measure
stores nothing.

### Problem 2

Explain `CALCULATE` with an example. *(5 marks)*

**Solution.**

`CALCULATE(expression, filter1, filter2, …)` evaluates the expression in a
filter context **modified** by the filters supplied. It is the only way a
measure can override what the visual is filtering.

```dax
South Revenue = CALCULATE([Total Revenue], dim_store[region] = "South")
```

Show the table, because the surprise *is* the answer:

| region | `[Total Revenue]` | `[South Revenue]` |
|---|---:|---:|
| North | ₹2,520 | ₹10,360 |
| South | ₹10,360 | ₹10,360 |

**On the North row `[South Revenue]` still shows South's figure** — the filter
argument replaced the row's own region filter rather than adding to it. Mention
`KEEPFILTERS`, which makes it intersect instead, and `ALL`, which removes
filters entirely and gives % of total.

### Problem 3

A colleague has twelve monthly CSV files with one column per product, and wants
a Power BI report that keeps working when January's file arrives. Describe your
approach. *(10 marks)*

**Solution.**

1. **Get Data → Folder**, not twelve separate imports. Power Query builds a
   sample-file function and applies it to every file; new files are picked up on
   refresh with no edit.
2. **Unpivot the product columns.** The wide shape cannot be charted over time
   without naming every column, and it breaks when a product is added.
3. **Set types explicitly** and check the CSV encoding — UTF-8 vs ANSI is the
   commonest silent corruption.
4. **Remove duplicates** on the natural key, because re-uploads happen.
5. **Model it** — a Date dimension marked as a date table, a Product dimension,
   and the unpivoted table as the fact. Not one flat table (Unit 4 §4.3).
6. **Write measures, not calculated columns**, so they respond to slicers.
7. **Publish, schedule refresh**, and add a gateway if the folder is
   on-premises.

The point to state explicitly: **every step is recorded and replayed.** Cleaning
in Excel fixes one file; cleaning in Power Query fixes every future file too.

---

## Exam questions from this unit

**Two marks**

1. Name the three components of the Power BI ecosystem.
2. Which operating systems does Power BI Desktop run on?
3. What does DAX stand for?
4. Give the difference between `COUNT` and `COUNTROWS`.
5. What does a `.pbix` file contain?
6. What is a Power BI gateway for?

**Five marks**

1. Distinguish a report from a dashboard in Power BI.
2. Compare Import and DirectQuery.
3. Explain `CALCULATE` with an example.
4. List and explain any six Power Query transformations.
5. Explain row-level security and when you would use it.
6. When would you transform in Power Query rather than in DAX?

**Ten marks**

1. Distinguish calculated columns from measures, with an example where the
   wrong choice gives a wrong answer.
2. Describe the Power Query steps to clean a student performance dataset.
3. Explain the Power BI ecosystem and the publish-and-share workflow.
4. Explain any five DAX functions with examples on a sample table.

---

## Mistakes that cost marks

- **Calling a calculated column a measure.** They differ in when they run, what
  context they see, and whether they cost memory.
- **Dividing then averaging.** 29.76% instead of 27.37%. Aggregate first.
- **Using `/` instead of `DIVIDE`.** A zero denominator errors the visual.
- **Saying `CALCULATE` "adds" a filter.** It **replaces** the filter on that
  column, unless wrapped in `KEEPFILTERS`.
- **Confusing report and dashboard.** In Power BI a dashboard is built in the
  Service from pinned tiles; Tableau reverses the words.
- **Cleaning in DAX what belongs in Power Query.** Costs memory on every query
  and never appears in Applied Steps.
- **Forgetting Desktop is Windows-only.** Examined, and a real constraint.
- **Assuming publishing means sharing.** Sharing needs Pro on both sides.
- **Leaving data wide.** If a chart needs a column named per month, unpivot it.
