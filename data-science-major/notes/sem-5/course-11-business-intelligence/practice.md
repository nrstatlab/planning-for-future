# Course 11 — Practice Questions with Worked Solutions

Exam-style questions across all five units, with solutions written the way an
answer script should be written — a definition, a table or diagram, a worked
example, and the point that earns the last two marks.

Every figure quoted comes from
`labs/course-11-bi/` and is checked by
`tools/run_bi_labs.py`.

---

## Section A — Two-mark questions

**1. Define Business Intelligence.**
The set of technologies, processes and practices that collect, integrate,
analyse and present an organisation's data in order to support **better and
faster business decisions**.

**2. Who coined the modern term "Business Intelligence", and when?**
**Howard Dresner of Gartner, in 1989.**

**3. What kind of decision does a DSS support?**
**Semi-structured** — where the rules are partly known, so the system does the
arithmetic and the human keeps the judgement.

**4. Name the four components of a DSS.**
Data management, model management (MBMS), user interface (dialogue management),
and the optional knowledge management component.

**5. Which operating systems does Power BI Desktop run on?**
**Windows only.** There is no macOS build.

**6. Give the difference between `COUNT` and `COUNTROWS`.**
`COUNT(column)` counts **non-blank values**; `COUNTROWS(table)` counts **rows**,
blanks included. On a complete column they agree, which is why the difference
surprises people.

**7. What does `.pbix` contain?**
The queries, the data model, the measures, and — in Import mode — a compressed
copy of the data.

**8. Give the difference between `.twb` and `.twbx`.**
`.twb` holds only the instructions and needs its data source. **`.twbx` is
packaged** — instructions plus the data extract. **Submit `.twbx`.**

**9. What does VizQL do?**
Translates a drag-and-drop action into **a database query and a visual encoding
in one step**. It is the patented idea Tableau was founded on.

**10. What do blue and green fields mean in Tableau?**
**Blue = discrete = headers. Green = continuous = axes.** It is not fixed by
field type — a date can be either.

**11. Name the three LOD keywords.**
`FIXED`, `INCLUDE`, `EXCLUDE`.

**12. What is the grain of a fact table?**
**What one row represents.** The sample model's grain is one row per product,
per store, per day.

**13. Give one example each of an additive, semi-additive and non-additive
measure.**
Additive: sales quantity. Semi-additive: stock on hand (does not sum over
time). Non-additive: margin %.

**14. What does cardinality 1:\* mean?**
One row on the dimension side matches **many** rows on the fact side. The "one"
side's key must be unique.

**15. What is a surrogate key?**
A meaningless integer key generated for a dimension row, used instead of a
natural business key. Compresses better and joins faster.

**16. Name the six dimensions of data quality.**
Accuracy, completeness, consistency, timeliness, validity, uniqueness.

**17. Give the difference between a slicer and a filter.**
**A slicer is a filter the user can see.** Both restrict rows; a slicer sits on
the canvas, a filter lives in the pane and may be hidden.

**18. What is drill-through?**
Jumping to a **different page** filtered to the selection you right-clicked —
as opposed to drilling *down*, which changes level in place.

**19. Why must a bar chart's axis start at zero?**
Because bar **length** encodes the value. A truncated axis exaggerates
differences and misleads.

**20. Name two accessibility requirements for a dashboard.**
Never encode by **colour alone** (add shape, label or position), and keep text
contrast at **4.5:1** or better. *(Also acceptable: alt text, tab order,
minimum 10–12 pt text.)*

---

## Section B — Five-mark questions

### 1. Explain the evolution of Business Intelligence

**Solution.** Five stages, each solving the previous stage's failure:

| Era | What existed | Why it changed |
|---|---|---|
| 1960s–70s | Decision Support Systems; fixed printed MIS reports | Reports took weeks; any change meant an IT request |
| 1980s | Executive Information Systems; **Dresner revives "BI" at Gartner, 1989** | Served only the top of the organisation |
| 1990s | **Data warehousing** — Inmon, **Kimball's dimensional model (1996)**, OLAP cubes | The model stabilised; tools stayed expensive and IT-owned |
| 2000s | Enterprise suites — Cognos, Business Objects, MicroStrategy | Licences and specialists made every question a project |
| 2010s→ | **Self-service BI** — Tableau, Power BI, Qlik | Where this course lives |

**The one-sentence summary:** reporting moved steadily away from IT and towards
the person with the question. Self-service BI is the end point — and the
governance problems of Unit 4 §4.6 are its direct cost.

### 2. Explain the components of a Decision Support System

**Solution.** Draw the four boxes:

```
                    ┌─────────────────────┐
                    │   User Interface    │  ← the manager
                    │  (Dialogue mgmt)    │
                    └──────────┬──────────┘
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │     Data     │ │    Model     │ │  Knowledge   │
      │  Management  │ │  Management  │ │  Management  │
      │   (DBMS)     │ │   (MBMS)     │ │  (optional)  │
      └──────────────┘ └──────────────┘ └──────────────┘
```

- **Data management** — the database and its DBMS; internal, external and
  personal data.
- **Model management (MBMS)** — statistical, financial, optimisation and
  simulation models. *This is what makes it a DSS rather than a report.*
- **User interface** — dialogue management; how the manager asks and sees.
- **Knowledge management** — rules and expertise; optional, and makes it an
  *intelligent* DSS.

**Do not drop the user interface** — it is the component people forget, and it
is a quarter of the marks.

### 3. Compare Import and DirectQuery

**Solution.**

| | **Import** | **DirectQuery** |
|---|---|---|
| Where the data sits | Copied into the `.pbix`, compressed in memory | Stays in the source; queries sent live |
| Speed | **Fast** — in-memory columnar engine | The source's speed |
| Freshness | As of the last refresh | **Live** |
| Size limit | Model limits apply (1 GB on Pro) | None — no copy is made |
| DAX available | **All of it** | A restricted subset |
| Load on source | Only at refresh | Every interaction |

**Import is the default and the right answer unless told otherwise.** Choose
DirectQuery only when the data is too large to copy or must be to-the-second.

### 4. Explain the Tableau filter order of operations and why it matters

**Solution.** Filters do not apply simultaneously:

```
1. Extract filters            (what enters the .hyper at all)
2. Data source filters        (applied to every worksheet)
3. Context filters            (create a temporary subset)
4. Dimension filters          (the normal ones)
5. Measure filters            (after aggregation)
6. Table calculation filters  (last; hide without recomputing)
```

**Why it matters — the worked case.** Asking for the **top 2 stores in North**:

| Approach | Result |
|---|---|
| Top-N first, then filter to North | **0 rows** — the overall top 2 are both South |
| Filter to North first, then Top-N | **2 rows** (₹1,920 and ₹600) |

**The fix: promote the region filter to a context filter**, so it runs at step
3, before the Top-N. That is what context filters are for.

Also note **`FIXED` LOD expressions are evaluated before dimension filters**,
which is why filtering a region does not change a `{FIXED [Region] : …}`
result — and why a context filter is the fix there too.

### 5. Why does every model need a dedicated Date dimension?

**Solution.** Three reasons, and give all three:

1. **Time intelligence requires it.** `TOTALYTD`, `SAMEPERIODLASTYEAR` and the
   rest need a table with **one row per date and no gaps**. A date column in
   the fact table has gaps by definition.
2. **Days with no activity disappear.** A fact-derived date list has no row for
   a day nothing sold, so a line chart silently skips it — and a flat line
   reads very differently from an absent one.
3. **It is where fiscal periods, holidays and week numbers live.** Your fiscal
   year probably does not start in January, and that logic belongs in one table
   rather than in every measure.

Then: **Modeling → Mark as Date Table**, which is what unlocks the time
intelligence functions.

### 6. Distinguish a dashboard, a report and a scorecard

**Solution.**

| | **Dashboard** | **Report** | **Scorecard** |
|---|---|---|---|
| Purpose | **Monitor** | **Analyse** | **Track against targets** |
| Size | One screen | Many pages | One screen |
| Detail | Summary, with drill-down | Full detail | KPIs vs targets only |
| Question | "Is anything wrong?" | "What exactly happened?" | "Are we on track?" |
| Frequency | Glanced at daily | Read occasionally | Reviewed monthly |

**A scorecard is a dashboard where every metric has a target.** Name the
**Balanced Scorecard** (Kaplan and Norton — financial, customer, internal
process, learning and growth) if the question mentions strategy.

**The test that applies to all three:** *when this number moves, who does
what?* If nobody can answer, do not build it.

---

## Section C — Ten-mark questions

### 1. Distinguish BI, Data Analytics and Data Science, with an example

**Solution.**

**The one-line distinction first:** BI reports *what happened*, analytics
explains *why*, data science predicts *what happens next*.

| | **Business Intelligence** | **Data Analytics** | **Data Science** |
|---|---|---|---|
| Question | *What happened?* | *Why did it happen?* | *What will happen, and what should we do?* |
| Analytics type | Descriptive | Descriptive + diagnostic | **Predictive + prescriptive** |
| Time direction | **Backward** | Backward, seeking cause | **Forward** |
| Data | Structured, internal, warehoused | Structured, some external | **Any** — text, image, streaming |
| Method | Aggregation, slicing, drill-down | Statistical testing, segmentation | Machine learning, modelling |
| Output | Dashboards, scheduled reports | An analysis answering a question | A **model** that keeps producing answers |
| Repeats? | **Yes — the same view daily** | Usually once per question | Runs continuously |

**Then the worked illustration** — this is what separates a 6 from a 9. One
retail sales table, three jobs:

- **BI:** *"Sales by region last quarter?"* → a dashboard: South ₹4.2 crore,
  +8% QoQ, refreshed nightly, opened every Monday by regional managers.
- **Analytics:** *"Why did South grow 8% while North fell 3%?"* → a one-off
  analysis: South's growth traces to one product line after a price cut; North
  lost two large accounts.
- **Data science:** *"Which customers churn next quarter, and what offer
  retains them?"* → a model scoring every customer weekly, with an uplift
  estimate per offer.

**Close with the relationship, not just the difference.** They are a *sequence*
over the same warehouse. BI is usually the prerequisite: a data science team
with no agreed definition of "revenue" will model a number nobody trusts. The
semantic layer BI builds is what makes the other two trustworthy.

### 2. Compare star and snowflake schemas. Which for retail sales, and why?

**Solution.**

**Definitions and diagrams.**

```
STAR                              SNOWFLAKE
   dim_date   dim_store            dim_supplier -- dim_product -- fact_sales
        \       /                                                     |
      fact_sales                                                  dim_store
        /                                                             |
   dim_product                                                    dim_date
```

A **star** has denormalised dimensions, each one join from the fact. A
**snowflake** normalises a dimension into further levels — in the worked model,
`dim_product` carries `supplier_key` pointing at `dim_supplier`, and that one
edge is what makes it a snowflake.

| | **Star** | **Snowflake** |
|---|---|---|
| Dimensions | Denormalised, one table each | Normalised into levels |
| Joins per query | **Fewer** | More |
| Query speed | **Faster** | Slower |
| Storage | Slightly more | Slightly less |
| Readability | **High** — business users can read it | Lower |
| Shared attributes | Updated in many rows | **Updated in one place** |

**Choose the star**, and justify it: joins cost query time, storage is cheap,
and BI engines are optimised for the star. Give the honest exception —
snowflake a dimension when it is genuinely huge, or when an attribute is
**shared across products and changes independently**, which is exactly why
`dim_supplier` is kept separate in the worked model.

**Then the strongest part of the answer: never one flat table.** Four reasons:

| # | Reason | The evidence |
|:---:|---|---|
| 1 | **Storage** | Star 92 cells vs flat 144 on the sample; at a million fact rows the flat table costs **4.00×** |
| 2 | **Redundancy invites inconsistency** | "Vijayawada" is stored 4 times; mistype one and you have **4 stores** in every chart |
| 3 | **Slower filtering** | A region slicer scans the whole fact table instead of a 3-row dimension |
| 4 | **You cannot report what did not happen** | Remove P4's sales and the flat table shows **3 products** — P4 is invisible. The star shows **4**, with P4 blank |

**Reason 4 is the decisive one.** *"Which products sold nothing last month?"* is
unanswerable from a flat table and trivial from a star. Lead with it.

### 3. Distinguish joining from blending in Tableau, illustrating the fan trap

**Solution.**

| | **Join** | **Blending** |
|---|---|---|
| When | At the data source, **before** aggregation | At the view, **after** aggregation |
| Sources | Usually one connection | **Different** sources |
| Result | Row-level combination | Aggregate-level match |
| Duplication risk | **Yes — the fan trap** | **No** |
| Type | Any join type | Effectively a **left join** from the primary |

**The fan trap, with numbers.** 9 sales rows joined to a targets table holding
**2 rows per store**, on store alone:

| | Correct | After the join |
|---|---:|---:|
| Rows | 9 | **18** |
| `SUM(Revenue)` | ₹12,880 | **₹25,760** |
| `SUM(Target)` | ₹20,800 | **₹66,700** |

Explain **both** inflations, because they differ:

- **Revenue doubled uniformly** — every sales row met 2 target rows.
- **Targets inflated unevenly** — each target row met that store's sales rows:
  T1's ₹10,500 × 4 = ₹42,000, T2's ₹6,200 × 2 = ₹12,400, T3's ₹4,100 × 3 =
  ₹12,300.

**No error is raised.** The totals simply become wrong.

**The three fixes:**

1. **Join on the full grain** — store *and* quarter → 9 rows, revenue ₹12,880
   correct. But the naive target sum is still ₹32,900, because a target row
   still repeats once per sales row at that grain.
2. **Blend** — aggregate each source to the linking field first, then match →
   3 rows, revenue ₹12,880 **and** target ₹20,800, both correct in one step.
3. **`{FIXED [Store] : SUM([Target])}`** — recovers ₹20,800 even from the
   broken join, but only patches that measure; revenue stays doubled.

**Close with the sentence that explains blending:** it is a **left join
performed after aggregation**. That is why it cannot duplicate, and equally why
it cannot give you row-level detail from the secondary source.

### 4. Distinguish calculated columns from measures, with a worked example

**Solution.**

| | **Calculated column** | **Measure** |
|---|---|---|
| Evaluated | Once, at refresh | **Every time a visual renders** |
| Context | **Row context** — sees one row | **Filter context** — sees a filtered table |
| Stored | Yes; costs memory | No |
| Placed on | Rows, columns, slicers, axis | **Values only** |
| Use when | You must slice or group by it | You need a number that responds to selection |

**Rule: default to a measure.**

**The worked example.** Nine sales rows carrying profit and revenue:

```dax
-- WRONG: a calculated column, then AVERAGE
Margin Pct (col) = DIVIDE(fact_sales[profit], fact_sales[revenue])
Avg Margin       = AVERAGE(fact_sales[Margin Pct (col)])   -- 29.7619%

-- RIGHT: a measure
Margin Pct = DIVIDE([Total Profit], [Total Revenue])       -- 27.3680%
```

| Approach | Result |
|---|---:|
| `AVERAGE` of the per-row margin column | **29.7619%** |
| `SUM(profit) ÷ SUM(revenue)` | **27.3680%** |

**A gap of 2.3939 percentage points.** The column is wrong because it weights a
₹600 line and a ₹2,800 line equally; the measure weights each by its revenue,
which is what "margin" means. The correct answer is exactly the
**revenue-weighted average** of the row margins.

**State the rule: aggregate, then divide — never divide, then average.** Every
ratio in BI obeys it: margin, conversion rate, average order value, cost per
acquisition. Add that the column also costs memory in every query while the
measure stores nothing.

### 5. Explain LOD expressions with a worked example

**Solution.**

**Definition:** a Level Of Detail expression computes an aggregate at a level
of detail **different from the view's**, breaking the normal rule that
granularity is set by the dimensions on the shelves.

| Keyword | Level used |
|---|---|
| **`FIXED`** | **Only** the dimensions named; the view is ignored |
| **`INCLUDE`** | The view's dimensions **plus** the named ones |
| **`EXCLUDE`** | The view's dimensions **minus** the named ones |

**The worked example.** A view of revenue by **store**, with
`{FIXED [Region] : SUM([Revenue])}` added:

| store | region | `SUM(Revenue)` | `{FIXED [Region]:…}` |
|---|---|---:|---:|
| Vijayawada | South | ₹6,160 | **₹10,360** |
| Guntur | South | ₹4,200 | **₹10,360** |
| Hyderabad | North | ₹2,520 | **₹2,520** |

Both South stores show the **region** total. Then derive the measure everyone
actually wants:

```
Pct of Region = SUM([Revenue]) / SUM({FIXED [Region] : SUM([Revenue])})
```

→ Vijayawada **59.46%**, Guntur **40.54%**, Hyderabad **100.00%**. The two
South figures sum to 100%, which is the check that the LOD is doing what you
meant.

**Two points that show depth:**

1. **`FIXED` is computed before dimension filters**, so filtering to one region
   does not change it. Promote the filter to a **context filter** to make it
   apply.
2. **The Power BI equivalent** is
   `CALCULATE(SUM(revenue), ALLEXCEPT(dim_store, dim_store[region]))`. Both
   tools solve the same problem and both make it the hardest thing in the tool.

**A warning worth adding:** an LOD is not automatically the right answer.
Averaging salary by department gives ₹554,000 for Sales, but
`{INCLUDE [Role]}` gives **₹687,500**, because it averages the four Execs and
the one Manager as *two* numbers. That is the average-of-averages trap in LOD
form — the syntax is easy, the reason must be deliberate.

### 6. Design a data model for an HR analytics dashboard

**Solution.**

**Two fact tables, because there are two grains** — say this first:

- `fact_headcount` — **one row per employee per month** (a periodic snapshot)
- `fact_movement` — **one row per joining or leaving event** (a transaction fact)

**Dimensions:** `dim_employee` (id, name, gender, date of birth, education),
`dim_department`, `dim_role` (role, grade, band), `dim_date`, `dim_location`.

**Relationships:** 1:\* from every dimension to both facts, **single**
cross-filter direction. Both facts share `dim_date`, `dim_department` and
`dim_employee` — which makes this a **fact constellation**.

**Measures:**

```dax
Headcount      = DISTINCTCOUNT(fact_headcount[emp_id])
Leavers        = CALCULATE(COUNTROWS(fact_movement), fact_movement[type] = "Exit")
Avg Headcount  = AVERAGEX(VALUES(dim_date[month]), [Headcount])
Attrition Rate = DIVIDE([Leavers], [Avg Headcount])
Gap vs Company = [Attrition Rate] - CALCULATE([Attrition Rate], ALL(dim_department))
```

**The three points that earn the top marks:**

1. **Headcount is semi-additive.** It does not sum over time — twelve monthly
   headcounts of 100 is 100 people, not 1,200. Hence `AVERAGEX` over months in
   the denominator, never `SUM`.
2. **Show headcount beside every rate.** On the worked data, Support shows
   **100% attrition** from **one employee and one leaver**, while Engineering
   shows 16.67% from six. Support tops the chart and is not the problem.
   **Suppress rates below a minimum denominator** — with n ≥ 3 only
   Engineering, HR and Sales remain reportable.
3. **`{FIXED : …}` with no dimension gives the company benchmark**, constant on
   every row, which is what makes "gap vs company" possible at all.

**A finding worth quoting:** on the worked data every leaver had **≤1.5 years'
tenure** — mean 1.0 against 5.0 for stayers. Two measures, one clear
recommendation: the problem is the first eighteen months.

### 7. Design a dashboard for sales forecasting and budgeting

**Solution.**

**Start with the decision, not the charts.** How much stock to buy and what
quota to set per region next quarter; decided quarterly by the sales director.

**The layout** (Unit 5 §5.5), designed for the F-pattern:

```
+--------------------------------------------------+
|  Sales Forecast — Q3            As at 27-08-2026  |
+--------------------------------------------------+
|  [Rev QTD]  [Forecast]  [Variance %]  [Coverage]  |  ← 4 cards, top-left first
+--------------------------------------------------+
|  Actual (solid) + forecast (dashed, with band)   |
|                              |  Revenue by region |
|                              |  ranked, w/ target |
+------------------------------+-------------------+
|  What-if: growth rate | price change | win rate  |
+--------------------------------------------------+
|  [region] [product] slicers                      |
+--------------------------------------------------+
```

**The three traps, which is where the marks are:**

1. **Show the forecast's uncertainty.** A single line is read as a promise. Use
   a confidence band, or low/expected/high scenarios. This is Course 4's
   confidence interval doing its actual job.
2. **Style the forecast differently from the actuals** — dashed, lighter,
   labelled, with a vertical rule at "today". Otherwise a forecast is quoted as
   an actual within the week.
3. **Show variance in both rupees and percent, sorted by rupees.** A region 50%
   under budget on ₹2 lakh matters less than one 5% under on ₹2 crore.

**The what-if parameter is what makes it a decision tool rather than a
report.** At −5%, 0%, +5% and +10% the projected revenue is ₹12,236 / ₹12,880 /
₹13,524 / ₹14,168 — and **the row count is 9 in every scenario**, because a
parameter changes the calculation, not the data. That closes the loop back to
Unit 1's DSS model component, and it is a good way to end the answer.

---

## The five things most likely to be examined

1. **BI vs Data Analytics vs Data Science** — Outcome 1, Activity 1, and nearly
   every paper. Answer with a table *and* one dataset described three ways.
2. **Star vs snowflake, and why never one flat table** — the modelling question,
   and the four-reason answer with "cannot report what did not happen" last.
3. **The fan trap** — joining on a partial key inflates totals silently.
   ₹12,880 → ₹25,760. Know the three fixes.
4. **Calculated column vs measure, and aggregate-then-divide** — 29.76% vs
   27.37%. The single most transferable idea in the course.
5. **LOD expressions / `CALCULATE`** — computing at a level other than the
   view's. Same problem in both tools, hardest thing in both tools.
