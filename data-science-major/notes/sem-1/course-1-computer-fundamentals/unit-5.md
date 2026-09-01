# Unit 5 — Data Analysis and Visualization

**Syllabus topics:** Conditional formatting — custom rules, colour scales,
icon sets, data bars. Data analysis tools — pivot tables and pivot charts, data
validation (drop-downs, input messages, error alerts), what-if analysis (Goal
Seek, Scenario Manager, data tables). Charts and dashboards — creating
interactive dashboards, using slicers with pivot tables, combo charts and
sparklines. Productivity tips — named ranges, freeze panes, split view.

---

This unit is where the course stops being about a tool and starts being about
**analysis**. Pivot tables are genuinely the most valuable thing here — they do
in four drags what would otherwise take a page of formulas.

## 5.1 Conditional formatting

*(Also briefly in Unit 4 — this is the substantive treatment. Review finding
**D9**.)*

**Home → Conditional Formatting.**

| Type | Effect | Good for |
|---|---|---|
| **Highlight Cells Rules** | Colour cells meeting a condition | Flagging failures, duplicates |
| **Top/Bottom Rules** | Top 10, bottom 10%, above average | Finding extremes |
| **Data Bars** | An in-cell bar proportional to the value | Comparing magnitudes at a glance |
| **Colour Scales** | A 2- or 3-colour gradient | Heat maps |
| **Icon Sets** | Arrows, traffic lights, flags | Status indicators |
| **New Rule → formula** | Anything you can express | Whole-row highlighting |

### Custom rules with a formula

The powerful option. To highlight the **entire row** where column C is below 40:

1. Select the whole data range, e.g. `A2:F50`
2. Conditional Formatting → New Rule → *Use a formula to determine which cells
   to format*
3. Enter `=$C2<40`
4. Choose the format

**The mixed reference is the whole trick.** `$C` locks the column so every cell
in the row is tested against column C; the row number `2` is relative, so each
row tests its own value. Write `$C$2` and every row is tested against one cell;
write `C2` and each cell tests the column beside it.

### Other useful formula rules

```excel
=COUNTIF($A$2:$A$50, A2)>1        highlight duplicates
=A2=MAX($A$2:$A$50)               highlight the maximum
=WEEKDAY(A2,2)>5                  highlight weekend dates
=AND($C2>=40, $D2>=40)            highlight rows passing both subjects
```

**Managing rules:** Conditional Formatting → Manage Rules. Rules apply in order,
and *Stop If True* prevents later rules from overriding an earlier one.

## 5.2 Pivot tables

### 🎯 What a pivot table is

A tool that **summarises a large table by categories** — instantly, and without
writing a single formula. Ten thousand sales rows become "total revenue by
region by month" in four drags.

### The four areas

```
        ┌──────────────────────────────────────────┐
        │  FILTERS      (slice the whole table)    │
        ├──────────────┬───────────────────────────┤
        │              │  COLUMNS                  │
        │              │  (categories across)      │
        ├──────────────┼───────────────────────────┤
        │  ROWS        │  VALUES                   │
        │ (categories  │  (the numbers, aggregated)│
        │  down)       │                           │
        └──────────────┴───────────────────────────┘
```

| Area | Holds | Example |
|---|---|---|
| **Rows** | A category, listed down the side | Region |
| **Columns** | A category, spread across the top | Month |
| **Values** | The numbers, aggregated | Sum of Revenue |
| **Filters** | A category filtering the whole table | Year |

### Creating one

1. Click any cell inside your data
2. **Insert → PivotTable**
3. Confirm the range and choose where to put it
4. Drag fields into the four areas

**Your source data must have a header row and no blank rows or columns.** That
is the commonest reason a pivot table refuses to build or produces odd results.

### Value settings

Click a field in Values → **Value Field Settings**:

| Summarise by | Sum, Count, Average, Max, Min, Product, StdDev |
|---|---|
| **Show Values As** | % of Grand Total, % of Column, Difference From, Running Total, Rank |

**"Show Values As → % of Grand Total"** is the feature most people never
discover, and it turns raw numbers into shares instantly.

### Grouping

Right-click a row label → **Group**:

- **Dates** group into days, months, quarters, years
- **Numbers** group into bands, e.g. ages into 10-year brackets

Grouping dates by month and year is how you turn a list of transactions into a
monthly trend.

### Refreshing

A pivot table is a **snapshot**. Changing the source data does not update it
until you press **Refresh** (Alt+F5), or **Refresh All** (Ctrl+Alt+F5).

Forgetting this is how people present stale numbers. If a pivot disagrees with
the source, refresh before assuming anything is broken.

### Pivot charts

**Insert → PivotChart**, or select the pivot and Insert → Chart. It stays linked
to the pivot table, so filtering the pivot updates the chart.

## 5.3 Slicers — making a dashboard interactive

A **slicer** is a set of clickable buttons that filters a pivot table.

1. Click the pivot table
2. **PivotTable Analyze → Insert Slicer**
3. Tick the fields to filter by
4. Click buttons to filter; Ctrl+click for several

**The key feature — Report Connections:** one slicer can control **several**
pivot tables at once. Right-click the slicer → Report Connections → tick every
pivot it should drive.

That is what turns a collection of separate pivots into a genuine
**dashboard**: click "South" once and every chart on the page updates together.

**Timeline slicers** (Insert → Timeline) do the same for dates, with a
drag-to-select range.

## 5.4 Data validation

**Data → Data Validation** restricts what may be entered into a cell. It is the
difference between a spreadsheet that collects clean data and one that collects
whatever people happen to type.

### The three tabs

Every validation rule has three parts, and the syllabus names all three:

| Tab | Purpose |
|---|---|
| **Settings** | The rule itself — what is allowed |
| **Input Message** | A hint shown when the cell is selected, *before* typing |
| **Error Alert** | The message shown when an invalid entry is attempted |

### Validation criteria

| Criterion | Allows | Example |
|---|---|---|
| **List** | Only values from a list — creates a **dropdown** | Course names |
| **Whole number** | Integers in a range | Roll numbers 1–500 |
| **Decimal** | Decimals in a range | Marks 0–100 |
| **Date** | Dates in a range | DOB between 1990 and 2010 |
| **Time** | Times in a range | Slots 09:00–17:00 |
| **Text length** | A length range | A 10-digit phone number |
| **Custom** | Anything expressible as a formula | `=ISNUMBER(SEARCH("@",E2))` |

### Creating a dropdown list

1. Select the cells
2. **Data → Data Validation → Settings**
3. Allow: **List**
4. Source: either type `BSc,BCom,BA` directly, or point at a range like
   `=$H$2:$H$10`
5. Tick **In-cell dropdown**

**Putting the source list on another sheet** keeps the form clean. Name the
range (see §5.8) and use the name as the source — a named range works across
sheets where a raw reference sometimes will not.

### Error alert styles

| Style | Behaviour |
|---|---|
| **Stop** | Rejects the entry outright |
| **Warning** | Warns, but allows the user to continue |
| **Information** | Informs only; always allows |

**Choose Stop for data that must be clean** — a roll number, a course code.
Choose Warning where an unusual value might still be legitimate.

### Finding what slipped through

Validation applies to what is typed *after* the rule is set. Values already in
the cells, or pasted in, are not checked.

**Data → Data Validation → Circle Invalid Data** draws a red ring around every
cell that breaks its rule — the way to audit an existing sheet.

**Pasting bypasses validation entirely.** This surprises people: a paste
overwrites the rule along with the value. Protect the sheet if that matters.

Lab experiment 12 requires a student registration form using dropdowns, input
messages and error alerts together.

## 5.5 What-if analysis

Three tools that run the calculation **backwards** or across scenarios.

### Goal Seek

> "I know the answer I want. What input produces it?"

**Data → What-If Analysis → Goal Seek**

| Field | Meaning |
|---|---|
| **Set cell** | The formula cell whose result you want to fix |
| **To value** | The target result |
| **By changing cell** | The input Excel may adjust |

*Example.* Your budget shows savings of ₹5,000 and you want ₹15,000. Set cell =
savings, To value = 15000, By changing cell = income. Goal Seek reports the
income required.

**Limitations:** one input, one target, and the changing cell must contain a
**value**, not a formula.

### Scenario Manager

> "Compare several complete sets of assumptions."

**Data → What-If Analysis → Scenario Manager**

Define named scenarios — *Best case*, *Worst case*, *Realistic* — each storing
values for up to 32 changing cells. Switch between them with **Show**, or
produce a side-by-side **Summary** report.

*Example.* Best case: sales +20%, costs −5%. Worst case: sales −15%, costs +10%.
One click switches the whole model between them.

### Data tables

> "Show the result for many input values at once."

**One-variable data table:**

1. List the input values down a column
2. Put the formula one row up and one column right of the list
3. Select the whole block
4. Data → What-If Analysis → Data Table
5. Leave *Row input cell* blank; set *Column input cell* to the input the
   formula uses

**Two-variable data table:** inputs down a column *and* across a row, with the
formula in the top-left corner of the block. Fill in both input cells.

### Which tool?

| Question | Tool |
|---|---|
| "What input gives me this exact result?" | **Goal Seek** |
| "Compare these complete sets of assumptions" | **Scenario Manager** |
| "Show me the result for every value from 1% to 10%" | **Data Table** |
| "Optimise with multiple constraints" | **Solver** (an add-in, beyond this syllabus) |

## 5.6 Combo charts and sparklines

### Combo charts

Two data series with **different scales** on one chart — revenue in rupees and
growth in percent, say.

1. Insert → Combo Chart → Create Custom Combo Chart
2. Choose a chart type per series (column for revenue, line for growth)
3. Tick **Secondary Axis** for the series with the different scale

**Without a secondary axis** the percentage line lies flat against the rupee
scale and is invisible. This is exactly what the secondary axis exists for.

### Sparklines

A tiny chart **inside a single cell**, showing a trend beside the numbers.

**Insert → Sparklines →** Line, Column or Win/Loss.

| Type | Shows |
|---|---|
| **Line** | The shape of a trend |
| **Column** | Relative magnitudes |
| **Win/Loss** | Only whether each value is positive or negative |

Highlight the high and low points via **Sparkline → Show → High Point / Low
Point**. Sparklines are ideal in a dashboard summary table: one row per product,
with a trend line beside the totals.

## 5.7 Building a dashboard

A **dashboard** presents the key numbers on one screen, updating as the viewer
filters.

### Structure

```
┌────────────────────────────────────────────────────────┐
│  TITLE                              [Slicer] [Slicer]  │
├──────────────┬──────────────┬──────────────┬───────────┤
│  KPI: Total  │  KPI: Growth │  KPI: Best   │ KPI: Avg  │
├──────────────┴──────────────┼──────────────┴───────────┤
│                             │                          │
│      Chart 1 (trend)        │    Chart 2 (by category) │
│                             │                          │
├─────────────────────────────┴──────────────────────────┤
│      Summary table with sparklines                     │
└────────────────────────────────────────────────────────┘
```

### How to build one

1. **Keep raw data on its own sheet** — never build on top of it
2. **Build the pivot tables** on a second, hidden sheet
3. **Create the charts** from those pivots
4. **Place everything on a clean dashboard sheet**
5. **Add slicers** and connect them to every pivot via Report Connections
6. **Tidy up:** remove gridlines (View → uncheck Gridlines), remove the row and
   column headers, lock the layout
7. **Protect the sheet** so viewers can filter but not break it

### Design principles

1. **The most important number, largest and top-left** — that is where eyes go
2. **Five to seven elements maximum** — more becomes noise
3. **Consistent colours** — one colour means one thing throughout
4. **No 3-D effects** — they distort the very comparison the chart exists to make
5. **Label directly** where possible, rather than making the reader consult a
   legend
6. **One screen** — a dashboard that needs scrolling is a report

## 5.8 Productivity features

### Named ranges

Give a range a name and use it in formulas.

**Creating one:** select the range → type a name in the Name Box → Enter. Or
**Formulas → Define Name**.

```excel
=SUM(B2:B50)          what is this?
=SUM(Sales)           obvious
=Revenue - Costs      readable at a glance
```

**Advantages:** formulas become self-documenting; a named range is absolute by
default, so no `$` needed; and the name works from any sheet in the workbook.

**Rules:** no spaces, cannot start with a digit, cannot look like a cell
reference (`A1` is not allowed as a name).

**Formulas → Name Manager** edits and deletes them.

### Freeze panes

Keep headers visible while scrolling. **View → Freeze Panes:**

| Option | Effect |
|---|---|
| **Freeze Top Row** | Row 1 stays visible |
| **Freeze First Column** | Column A stays visible |
| **Freeze Panes** | Everything above and left of the selected cell stays |

**To freeze both row 1 and column A, select cell B2 first**, then Freeze Panes.
The rule is that everything above and to the left of the selection freezes.

### Split view

**View → Split** divides the window into independently scrollable panes, so you
can compare row 5 with row 5000 side by side. Unlike freeze panes, both panes
scroll.

### Other useful features

| Feature | Purpose | Where |
|---|---|---|
| **Flash Fill** | Detects a pattern and fills the rest | Ctrl+E |
| **Remove Duplicates** | Delete duplicate rows | Data |
| **Text to Columns** | Split one column into several | Data |
| **Group / Outline** | Collapsible sections | Data |
| **Tables (Ctrl+T)** | Structured references, auto-expanding ranges | Insert |
| **Watch Window** | Monitor distant cells while editing | Formulas |
| **Trace Precedents/Dependents** | See which cells feed a formula | Formulas |

**Converting a range to a Table (Ctrl+T)** is worth the habit: the range grows
automatically as you add rows, formulas use readable names like
`Sales[Revenue]`, and any pivot table built on it expands with the data.

---

## Exam questions from this unit

**Two marks**

1. What is a pivot table?
2. What does a slicer do?
3. Differentiate Goal Seek from Scenario Manager.
4. What is a sparkline?
5. Which cell do you select to freeze both the top row and the first column?

**Five marks**

1. Explain the four areas of a pivot table with an example.
2. Explain the three what-if analysis tools and when each applies.
3. Explain conditional formatting with custom formula rules.
4. Explain the steps to build an interactive dashboard.
5. Explain named ranges and their advantages.

**Ten marks**

1. Explain pivot tables in detail — creation, the four areas, value settings,
   grouping, refreshing and pivot charts.
2. Explain how you would build a sales dashboard, covering pivot tables,
   charts, slicers, sparklines and layout.

## Mistakes that cost marks

- Forgetting to **refresh** a pivot table after the source data changes
- Source data with blank rows or a missing header row
- Using `$C$2` instead of `$C2` in a whole-row conditional formatting rule
- Pointing Goal Seek's "changing cell" at a formula instead of a value
- A combo chart without a secondary axis, leaving one series invisible
- Selecting the wrong cell before Freeze Panes
- Cramming fifteen charts onto a dashboard
