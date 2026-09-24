# Unit 3 — Data Preparation, Visualization and Storytelling with Tableau

**Syllabus topics:** Introduction to Tableau; characteristics of Tableau;
Tableau architecture and components — Tableau Public, Desktop, Reader, Online,
Server; the Tableau interface — shelves, marks card, views; Tableau extensions;
data connection and preparation — cleaning, pivoting, filtering; calculated
fields and LOD expressions; basic visualizations — bar, line, tree, geo maps,
scatter plots; storytelling with Tableau; creating a Tableau story. Case study
— HR analytics.

> Figures here come from the same sample star schema as Unit 2
> (`fixtures.py`) and are asserted by
> the lab scripts.

---

## 3.1 What Tableau is, and its characteristics

### 🎯 The big idea

**Tableau optimises for the speed of the next question.**

Power BI's centre of gravity is the model — get the star schema and the
measures right, and reporting follows. Tableau's is the **view**: drag a field,
see a chart, change your mind, drag another. Both end in a dashboard; they
differ in what they make effortless.

That difference is the honest answer to "compare Power BI and Tableau", and it
is more useful than a feature list.

### Characteristics the syllabus wants named

| Characteristic | What it means |
|---|---|
| **Drag-and-drop visual analytics** | Build charts without writing code |
| **VizQL** | Tableau's core technology: drag actions are translated into a **query plus a visual encoding** in one step. This is the patented idea Tableau was founded on |
| **Show Me** | Suggests appropriate chart types for the fields you have selected |
| **Live and extract connections** | Query the source directly, or take a compressed **.hyper** extract |
| **Broad connectivity** | Files, databases, cloud services, web data connectors |
| **In-memory data engine** | The Hyper engine, for fast extracts |
| **Blending** | Combine data from **different sources** at an aggregated level (§3.6) |
| **Mobile-ready** | Dashboards adapt to device layouts |
| **Storytelling** | The **Story** object — sequenced dashboards with captions (§3.8) |

### 💡 Live vs Extract — Tableau's version of Import vs DirectQuery

| | **Live** | **Extract (.hyper)** |
|---|---|---|
| Data | Queried at the source, every interaction | **Snapshot** in Tableau's engine |
| Freshness | **Real-time** | As of the last extract refresh |
| Speed | The source's speed | **Usually much faster** |
| Load on source | Every interaction hits it | Only at refresh |
| Use when | Data must be current | Almost always |

**The mapping to remember:** Live ≈ DirectQuery, Extract ≈ Import. Same
trade-off, different vendor's words — and saying so earns the comparison mark.

---

## 3.2 Architecture and components

### 🔢 The five products the syllabus names

| Product | What it is | Cost | Can it author? | Can it publish? |
|---|---|---|---|---|
| **Tableau Desktop** | The full authoring tool | Paid (Creator) | **Yes** | Yes |
| **Tableau Public** | Free Desktop, with a catch | **Free** | **Yes** | Only to the **public** web |
| **Tableau Reader** | Free viewer for `.twbx` files | **Free** | No | No |
| **Tableau Server** | Self-hosted sharing platform | Paid | No | Hosts published work |
| **Tableau Online** (now Tableau Cloud) | Server, hosted by Tableau | Paid | No | Hosts published work |

### ⚠️ Tableau Public makes everything public

**Anything you save to Tableau Public is visible to the entire internet, and
downloadable.** It cannot save locally in the usual way — the workbook lives on
their servers.

For labs with sample data that is fine, and experiments 8, 9 and 12 rely on it.
**Never put real student, employee or customer data in it.** This is the single
most important warning in the unit, and it is a genuine, repeated real-world
data breach.

### File types — a two-mark question

| Extension | Contains |
|---|---|
| `.twb` | The workbook — **just the instructions**, no data. Needs the source |
| **`.twbx`** | **Packaged** workbook — instructions **plus** the data extract. This is what you hand in |
| `.hyper` | The extract itself |
| `.tds` / `.tdsx` | A saved data source |

**Hand in `.twbx`.** A `.twb` on the examiner's machine opens with no data, and
it is the commonest way to lose lab marks.

### The architecture, for the diagram question

```
        Data sources (files, databases, cloud)
                        |
                  Data Connection
                (Live  or  Extract)
                        |
              +--- Tableau Desktop ---+          authoring
              |     (VizQL engine)    |
              +-----------+-----------+
                          | publish
        +-----------------+-----------------+
        |                 |                 |
  Tableau Server    Tableau Online     Tableau Public
   (self-hosted)     (SaaS)             (free, public)
        |                 |                 |
        +-----------------+-----------------+
                          |
              Browser / Mobile / Reader        consumption
```

Server's own components — Gateway, Application Server, VizQL Server, Data
Server, Backgrounder, Repository — are worth naming if the question says
"explain Tableau Server architecture". **Backgrounder runs extract refreshes**
and **Repository is the PostgreSQL database holding metadata**; those two are
the ones asked about.

---

## 3.3 The interface — shelves, marks card, views

### 🔢 The vocabulary you must have exactly right

| Element | What it does |
|---|---|
| **Data pane** | Fields, split into **Dimensions** (blue, discrete) and **Measures** (green, continuous) |
| **Columns shelf** | Fields across the **x-axis** |
| **Rows shelf** | Fields down the **y-axis** |
| **Filters shelf** | Restricts what is shown |
| **Pages shelf** | Splits the view into a flip-book — animation over time |
| **Marks card** | Controls how each mark **looks**: Colour, Size, Label, Detail, Tooltip, Shape/Path/Angle |
| **View** | The chart itself — one worksheet |
| **Show Me** | Suggests chart types for the selected fields |

### ⚠️ Blue vs green is the concept, not a colour scheme

This is the distinction that confuses everyone, and it is examined.

| | **Blue — Discrete** | **Green — Continuous** |
|---|---|---|
| Produces | **Headers** | **Axes** |
| Values | Distinct, finite, ordered by sort | A continuous range |
| Typically | Dimensions | Measures |
| Example | Region, Product | Revenue, Profit |

**But it is not fixed by field type.** A date can be either: discrete `YEAR` for
one header per year, continuous for a real time axis. Converting between them
changes the chart entirely, and "why did my line chart become bars?" is nearly
always this.

### Tableau extensions

**Dashboard extensions** are web applications embedded in a dashboard zone that
can read and write the dashboard's data — write-back forms, custom filters,
third-party visuals from the Extension Gallery. **Analytics extensions**
connect Tableau to an external engine — Python via **TabPy** or R via
**Rserve** — so a calculated field can call a model.

**TabPy is the bridge to Course 12 A:** train a model in scikit-learn, expose it
through TabPy, and a Tableau calculated field can score rows live. Worth naming
in the viva; rarely needed at this level.

---

## 3.4 Data connection and preparation

| Task | Where | Note |
|---|---|---|
| Connect | Data Source tab | Choose Live or Extract here |
| **Join** | Data Source tab, drag a second table | Inner, Left, Right, Full — §3.6 |
| **Union** | Drag a table beneath another | Stacks rows; `pd.concat` |
| **Pivot** | Select columns → **Pivot** | Wide → long. **This is Unpivot under a different name** |
| **Split** | Column menu → Split | Splits on a delimiter |
| Rename / alias | Column menu | Aliases change display, not data |
| Hide fields | Column menu | Reduces clutter and extract size |
| Data Interpreter | Checkbox on the Data Source tab | **Cleans Excel files with title rows and merged cells** — try it first on any spreadsheet |
| Filter | Filters shelf, or a data source filter | See the order below |

### Cleaning, specifically

The syllabus names **cleaning, pivoting and filtering** as three things, so
answer them as three. Cleaning in Tableau happens on the Data Source tab, and
these are the tools:

| Tool | Fixes | Note |
|---|---|---|
| **Data Interpreter** | Title rows, blank rows, merged cells, sub-headers in Excel | **A checkbox on the Data Source tab.** Try it first on any spreadsheet — it often does the whole job |
| **Split / Custom Split** | `T1-Vijayawada` → two fields | Splits on a delimiter or a fixed position |
| **Rename** | Cryptic source column names | Changes the field name in Tableau only |
| **Aliases** | Display values — `S` shown as `South` | **Changes display only, never the stored value** |
| **Change data type** | Numbers imported as text | The `#`/`Abc` icon on the field |
| **Hide fields** | Columns you will never use | Shrinks the extract as well as the clutter |
| **Group** | Merging `GUNTUR`, `Guntur`, `guntur` into one member | A display-level grouping |
| **Tableau Prep Builder** | Anything heavier — a separate visual ETL tool | Its output is a `.hyper` or a published data source |

### ⚠️ An alias is not a fix

**Aliases change what is displayed; the underlying value is untouched.** So an
alias cannot repair a join key, cannot fix a duplicate caused by casing, and
does not travel to another workbook.

If two spellings must genuinely become one value, use a **Group**, a calculated
field, or fix it upstream — asserted in
`10_tableau_prep.py`, which
shows the displayed values changing while the stored ones stay `S` and `N`.

### ⚠️ Tableau's "Pivot" means Power Query's "Unpivot"

Same operation, opposite name. Tableau's Pivot turns a column per month into
one row per month — which Power Query calls **Unpivot** and pandas calls
**`melt`**. Getting the vocabulary right per tool is worth a mark, and mixing
them up loses one.

### 🔢 The filter order of operations — a favourite exam question

Filters do not all apply at once. This is the order:

```
1. Extract filters        (what enters the .hyper at all)
2. Data source filters    (applied to every worksheet)
3. Context filters        (create a temporary subset)
4. Dimension filters      (the normal ones)
5. Measure filters        (after aggregation)
6. Table calculation filters  (applied LAST, hides without recomputing)
```

**Why it matters:** a Top-10 filter computed *before* a region filter gives the
top 10 overall, not the top 10 in that region. Promoting the region filter to a
**context filter** fixes it, because context filters run first. That specific
scenario is the exam question.

---

## 3.5 Calculated fields and LOD expressions

### Calculated fields — the three kinds

| Kind | Computed | Example |
|---|---|---|
| **Row-level** | Per underlying row, before aggregation | `[Qty] * [Price]` |
| **Aggregate** | After aggregation, at the view's level | `SUM([Profit]) / SUM([Revenue])` |
| **Table calculation** | On the **result table**, after the query | `RUNNING_SUM`, `RANK`, `WINDOW_AVG`, `% Difference` |

### ⚠️ The same trap as Unit 2, in Tableau's words

```
WRONG:  AVG([Profit] / [Revenue])     -- row-level divide, then average
RIGHT:  SUM([Profit]) / SUM([Revenue])
```

Over the sample data those give **29.7619%** and **27.3680%** respectively —
the same two numbers as Unit 2 §2.4, because it is the same mistake. Tableau
makes it easier to commit, because dragging a ratio field onto a shelf
aggregates it with `AVG` by default.

**Aggregate, then divide.**

### 🎯 LOD expressions — the hardest and most examined idea in the unit

**A Level Of Detail expression computes an aggregate at a level of detail
different from the view's.**

Normally a view's granularity is whatever dimensions are on the shelves. LOD
expressions break that link.

| Keyword | Meaning | Level used |
|---|---|---|
| **`FIXED`** | Ignore the view entirely | **Only** the dimensions you name |
| **`INCLUDE`** | The view's dimensions **plus** the ones you name | Finer than the view |
| **`EXCLUDE`** | The view's dimensions **minus** the ones you name | Coarser than the view |

```
{FIXED   [Region] : SUM([Revenue])}
{INCLUDE [Product] : SUM([Revenue])}
{EXCLUDE [Product] : SUM([Revenue])}
```

### 🔢 A worked FIXED example — asserted in the lab

Put **store** on Rows and `SUM(Revenue)` on Columns. Then add
`{FIXED [Region] : SUM([Revenue])}`:

| store | region | `SUM(Revenue)` | `{FIXED [Region]: SUM([Revenue])}` |
|---|---|---:|---:|
| Vijayawada | South | ₹6,160 | **₹10,360** |
| Guntur | South | ₹4,200 | **₹10,360** |
| Hyderabad | North | ₹2,520 | **₹2,520** |

**The two South stores both show ₹10,360** — the region's total, not their own.
The LOD ignored the store dimension on Rows and aggregated at region level.

That immediately gives the measure everyone actually wants:

```
Pct of Region = SUM([Revenue]) / SUM({FIXED [Region] : SUM([Revenue])})
```

| store | Pct of Region |
|---|---:|
| Vijayawada | **59.46%** |
| Guntur | **40.54%** |
| Hyderabad | **100.00%** |

Hyderabad is 100% because it is the only North store. Both South figures sum to
100%, which is the check that the LOD is doing what you meant.

### 💡 The Power BI translation

`{FIXED [Region] : SUM([Revenue])}` is
`CALCULATE(SUM(revenue), ALLEXCEPT(dim_store, dim_store[region]))`.

**Both tools solve the same problem — computing at a level other than the
visual's — and both make it the hardest thing in the tool.** Saying this shows
you understand the concept rather than one vendor's syntax.

### ⚠️ FIXED ignores dimension filters — the classic surprise

`FIXED` is computed **before** dimension filters are applied, so filtering to
one region does *not* change a `FIXED [Region]` result. To make a filter apply,
promote it to a **context filter** — context filters run before LOD
expressions. This is the same order-of-operations table as §3.4, and it is why
that table is worth learning.

---

## 3.6 Joins and blending — and the trap between them

### Joins

Tableau's joins are SQL joins, done at the data source. Course 5's diagrams
apply unchanged.

| Join | Keeps |
|---|---|
| **Inner** | Only matching rows from both |
| **Left** | All of the left, matching from the right |
| **Right** | All of the right, matching from the left |
| **Full outer** | Everything from both |

### ⚠️ The fan trap — the most valuable numeric example in this course

**Join two tables that both have many rows per key, and your totals inflate.**
Nothing warns you; the numbers simply become wrong.

Take the nine sales rows and a targets table with **two rows per store** (one
per quarter). Join them **on store alone**:

| | Correct | After the join |
|---|---:|---:|
| Rows | 9 | **18** |
| `SUM(Revenue)` | ₹12,880 | **₹25,760** |
| `SUM(Target)` | ₹20,800 | **₹66,700** |

**Revenue doubled** — every sales row was duplicated once per target row.
**Targets more than tripled** — each target row was duplicated once per that
store's sales rows (Vijayawada has 4, Guntur 2, Hyderabad 3).

All four figures are asserted in
`14_joins_blending.py`.

### The three fixes

| Fix | How |
|---|---|
| **Join on the full grain** | Join on **store *and* quarter**, not store alone → back to 9 rows and ₹12,880 |
| **Blend instead of join** | Blending aggregates **first**, then matches — so nothing duplicates |
| **LOD** | `{FIXED [Store] : SUM([Target])}` de-duplicates the target side |

### 🔢 Joining vs blending — the comparison

| | **Join** | **Blending** |
|---|---|---|
| When | At the **data source**, before aggregation | At the **view**, after aggregation |
| Sources | Usually **one** connection | **Different** sources — Excel + SQL + Google Sheets |
| Result | **Row-level** combination | **Aggregate-level** match |
| Duplication risk | **Yes — the fan trap** | **No** |
| Type | Any join type | Effectively a **left join** from the primary source |
| Set up | Data Source tab | Automatic on a shared field; the linking icon 🔗 |

**Blending is a left join performed after aggregation.** That one sentence
explains both why blending avoids the fan trap and why it cannot give you
row-level detail from the secondary source. It is the answer to the ten-mark
"distinguish joining and blending" question.

**Primary and secondary matter.** The first data source used in the view is
primary; blending keeps all its rows and matches from the secondary. Swap them
and the result changes — which surprises people who think of it as symmetric.

---

## 3.7 Basic visualizations

| Chart | Build it by | Use for |
|---|---|---|
| **Bar** | Dimension on Rows, Measure on Columns | Comparing categories. **The default answer** |
| **Line** | Continuous date on Columns, Measure on Rows | Trend over time |
| **Tree map** | Show Me → Treemap; Size and Colour on Marks | **Part-to-whole with many categories** — where a pie fails |
| **Geo map** | Double-click a geographic field | Genuinely spatial questions |
| **Scatter** | Measure on **both** shelves, dimension on Detail | **Correlation between two measures** |
| Heat map | Two dimensions, Colour on Marks | Density across a grid |
| Dual axis | Two measures on Rows → Dual Axis | Two units on one chart. **Synchronise the axes** |

### 💡 Geographic roles

Tableau assigns a **geographic role** (Country, State, City, Postcode) and then
recognises place names automatically, generating latitude and longitude. When
places do not plot, it is nearly always because the role is unset or a name is
ambiguous — the **Edit Locations** dialog fixes it, and knowing that is worth a
lab mark.

### ⚠️ Scatter plots need a dimension on Detail

Drop two measures on the shelves and Tableau aggregates everything to **one
mark**. You must put the identifying dimension (product, store, employee) on
**Detail** to get one mark per thing. "My scatter plot has a single dot" is
always this.

---

## 3.8 Storytelling and creating a Tableau story

### 🎯 The big idea

**A dashboard answers "what is happening?" A story answers "what happened, why,
and what should we do?" — in a fixed order you control.**

| Object | What it is |
|---|---|
| **Worksheet** | One view |
| **Dashboard** | Several worksheets on one canvas, filterable together |
| **Story** | A **sequence of story points**, each a dashboard or sheet with a caption |

**Note the vocabulary difference from Power BI**, which the exam likes: in
Tableau a **dashboard** is authored in Desktop and combines worksheets; in
Power BI a dashboard is assembled in the Service from pinned tiles. The words
are swapped between the tools.

### Building a story

1. **New Story**, then drag a sheet or dashboard onto the first story point.
2. **Caption each point** — the caption is the narrative, and the default text
   is never good enough.
3. Use **Duplicate** to make the next point, then change *one* thing — a
   filter, a highlight, an annotation. Change one variable per step.
4. Add **annotations** to say what to look at.
5. Order the points as an argument, then **Publish**.

### 💡 The narrative arc that works

```
   Context   ->   Complication   ->   Cause   ->   Consequence   ->   Call to action
"Sales are    "But South fell    "Two large    "That is 8% of   "Reassign the
 ₹12.9 lakh"   11% in Q2"         accounts      annual revenue"   two accounts
                                  churned"                        this quarter"
```

**Each story point should make exactly one claim.** The commonest mistake is a
seven-point story where every point shows the same dashboard with a different
filter and no argument.

---

## 3.9 Case study — HR analytics

Lab experiment 9, and the HR domain from Unit 1 §1.4.

**The question:** why do employees leave, and which groups are most at risk?

**The data.** One row per employee: `emp_id`, `department`, `role`, `tenure_years`,
`salary`, `last_rating`, `left` (yes/no).

**The measures:**

| Measure | Formula |
|---|---|
| **Headcount** | `COUNTD([emp_id])` |
| **Attrition rate** | `SUM(IF [left]='Yes' THEN 1 ELSE 0 END) / COUNTD([emp_id])` |
| **Avg tenure of leavers** | `AVG(IF [left]='Yes' THEN [tenure_years] END)` |
| **Dept attrition vs company** | `[Attrition] - {FIXED : [Attrition]}` |

**That last one is why LOD matters here.** `{FIXED : ...}` with *no* dimension
computes over the whole table, giving the company-wide rate. Subtract it and
each department shows its gap from the company average — the single most useful
number on an HR attrition dashboard, and impossible without an LOD.

### ⚠️ The analytical trap in HR analytics

**Attrition rate on small departments is unstable and will mislead.** A team of
4 with one leaver shows 25%; a team of 200 with 40 leavers shows 20%. The small
team looks worse and is not — one person's decision moved it 25 points.

**Show headcount alongside every rate, and suppress rates below a minimum
denominator.** That is a Unit 5 dashboard-design point arriving early, and it is
also Course 4's sampling variability. Say so and you connect two courses.

---

## Practice problems

### Problem 1

Distinguish joining from blending in Tableau. Illustrate the fan trap
numerically. *(10 marks)*

**Solution.**

Give the comparison table from §3.6 — when each happens, one source vs several,
row-level vs aggregate-level, duplication risk, join types, setup.

Then the numeric illustration, which is what earns the top marks. Nine sales
rows, and a targets table with two rows per store (one per quarter). Joining on
**store alone**:

| | Correct | After the join |
|---|---:|---:|
| Rows | 9 | 18 |
| `SUM(Revenue)` | ₹12,880 | **₹25,760** |
| `SUM(Target)` | ₹20,800 | **₹66,700** |

Explain both inflations: revenue doubled because each sales row met two target
rows; targets tripled unevenly because each target row met that store's sales
rows (4, 2 and 3 respectively).

Give the three fixes — join on the full grain (store *and* quarter), blend, or
use `{FIXED [Store] : SUM([Target])}` — and close with the sentence that
explains blending: **it is a left join performed after aggregation**, which is
exactly why it cannot duplicate.

### Problem 2

What is an LOD expression? Explain FIXED, INCLUDE and EXCLUDE with an example.
*(10 marks)*

**Solution.**

**Definition:** an LOD expression computes an aggregate at a level of detail
different from the view's, breaking the normal rule that granularity is set by
whatever dimensions sit on the shelves.

The three keywords, with what level each uses: `FIXED` uses only the named
dimensions and ignores the view; `INCLUDE` uses the view's dimensions plus the
named ones; `EXCLUDE` uses the view's minus the named ones.

Then the worked example. A view of revenue by **store**, with
`{FIXED [Region] : SUM([Revenue])}` added:

| store | region | `SUM(Revenue)` | `{FIXED [Region]:…}` |
|---|---|---:|---:|
| Vijayawada | South | ₹6,160 | ₹10,360 |
| Guntur | South | ₹4,200 | ₹10,360 |
| Hyderabad | North | ₹2,520 | ₹2,520 |

Both South stores show the region total. Then derive `Pct of Region` — 59.46%,
40.54%, 100.00% — and note that the two South values sum to 100%, which is the
check.

Finish with two points that show depth: **FIXED is computed before dimension
filters**, so a region filter does not change it unless promoted to a context
filter; and the Power BI equivalent is `CALCULATE(..., ALLEXCEPT(...))`.

### Problem 3

Compare Tableau's products and explain which you would use for a college lab
exercise. *(5 marks)*

**Solution.**

Give the five-product table from §3.2 — Desktop (paid, full authoring), Public
(free, authoring, **publishes publicly only**), Reader (free, view `.twbx`
only), Server (self-hosted), Online/Cloud (SaaS).

**For a college lab: Tableau Public**, because it is free and needs no licence.
State the condition explicitly: **everything saved is publicly visible and
downloadable**, so it is fine for the sample datasets the lab supplies and must
never hold real student or employee data.

Add the file-type point: submit **`.twbx`**, the packaged workbook, because a
`.twb` carries no data and opens empty on the examiner's machine.

---

## Exam questions from this unit

**Two marks**

1. What does VizQL do?
2. Give the difference between `.twb` and `.twbx`.
3. What is the Marks card used for?
4. What do blue and green fields mean in Tableau?
5. Name the three LOD keywords.
6. What is a story point?

**Five marks**

1. Explain Tableau's architecture and its components.
2. Compare Live and Extract connections.
3. Explain the Tableau interface — shelves, marks card, views.
4. Explain the filter order of operations and why it matters.
5. Compare Tableau Public, Desktop and Reader.
6. How do you build a Tableau story? Describe the steps.

**Ten marks**

1. Distinguish joining from blending, illustrating the fan trap numerically.
2. Explain LOD expressions with a worked example.
3. Explain storytelling in Tableau and describe how you would build a story
   from an HR dataset.
4. Compare Tableau and Power BI across architecture, calculation language,
   data preparation and cost.

---

## Mistakes that cost marks

- **Saying Tableau's Pivot is the same as Power Query's Pivot.** It is the
  same as Power Query's **Unpivot**. Opposite names, same operation.
- **`AVG([Profit]/[Revenue])`.** 29.76% instead of 27.37%. Aggregate first.
- **Claiming blending is a kind of join at row level.** It matches **after**
  aggregation, which is precisely why it cannot duplicate rows.
- **Expecting a dimension filter to change a `FIXED` result.** It does not,
  unless the filter is promoted to a context filter.
- **Submitting a `.twb`.** No data. Submit `.twbx`.
- **Putting real data in Tableau Public.** It is published to the open web.
- **A scatter plot with one dot.** The identifying dimension is missing from
  the Detail shelf.
- **Confusing dashboard and story.** A dashboard is one canvas; a story is an
  ordered sequence of points with captions.
- **Reporting attrition rates without headcount.** Small denominators produce
  unstable percentages that will be believed.
