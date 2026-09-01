# Unit 5 — Dashboard Design and Business Insights

**Syllabus topics:** Introduction to dashboards; when to use dashboards;
dashboard components; principles of effective visualization and dashboarding;
advanced visualizations — parameters, slicers, filters, drilldowns, graphs and
maps; dashboard design — layout, alignment, accessibility; publishing
dashboards — Power BI Service, Tableau Public; storytelling and insight
communication; build a complete BI dashboard using either tool. Case study —
a business decision-making scenario such as sales forecasting or budgeting.

---

## 5.1 What a dashboard is, and when to use one

### 🎯 The big idea

**A dashboard is a single screen of the few numbers a specific person needs to
do their job, updated automatically.**

Every word is a constraint that gets violated in practice:

- **single screen** — if it scrolls, it is a report
- **few** — five to nine visuals, not thirty
- **specific person** — "everyone" is not an audience
- **needs to do their job** — not "might find interesting"
- **automatically** — a dashboard someone rebuilds by hand is a report

### 🔢 Dashboard vs report vs scorecard

| | **Dashboard** | **Report** | **Scorecard** |
|---|---|---|---|
| Purpose | **Monitor** | **Analyse** | **Track against targets** |
| Size | One screen | Many pages | One screen |
| Time | Current status | A period, in depth | Progress toward a goal |
| Detail | Summary, with drill-down | **Full detail** | KPIs vs targets only |
| Question | "Is anything wrong?" | "What exactly happened?" | "Are we on track?" |
| Frequency | Glanced at daily | Read occasionally | Reviewed monthly |

**A scorecard is a dashboard where every metric has a target.** Balanced
Scorecard — Kaplan and Norton's four perspectives (financial, customer,
internal process, learning and growth) — is worth naming if the question asks
about strategic dashboards.

### ⚠️ When NOT to use a dashboard

A genuinely good answer names these, because it shows judgement:

| Situation | Use instead |
|---|---|
| The question is asked **once** | An analysis, a slide, an email |
| The answer needs a **paragraph of explanation** | A written report |
| Nobody will act on any value it can show | **Nothing.** Do not build it |
| The data is unreliable | Fix the data first — a dashboard makes bad data authoritative |
| The user needs **row-level detail** | A paginated report or an export |
| The decision is made once a year | A one-off analysis |

**The test from Unit 1 §1.3 applies here too:** *when this number moves, who
does what?* If nobody can answer, the dashboard should not be built.

---

## 5.2 Dashboard components

| Component | Purpose | Guidance |
|---|---|---|
| **KPI cards** | The headline numbers | **3–5**, top row, with comparison to target or prior period |
| **Trend chart** | Direction over time | Almost always earns its space |
| **Breakdown** | Composition by category | Bar, ranked. Rarely a pie |
| **Detail table** | The rows behind the summary | Bottom, or on a drill-through page |
| **Slicers / filters** | Let the user narrow | Left or top edge, consistently placed |
| **Title and timestamp** | What this is, **and how fresh** | The timestamp is not optional |
| **Legend** | Decode the colours | Better still, label directly and delete it |

### ⚠️ A number with no comparison is not information

"Revenue ₹12,880" tells nobody anything. **₹12,880, up 8% on last quarter,
against a target of ₹14,000** supports a decision.

Every KPI card should carry at least one of:

- versus **target**
- versus **prior period** (last month, last year)
- versus a **peer** (other regions, other stores)
- a **sparkline** showing the recent trend

This is the highest-value single rule in the unit and it is cheap to apply.

---

## 5.3 Principles of effective visualization

### 🔢 The principles the exam wants

| Principle | Meaning | Violation |
|---|---|---|
| **Purpose first** | Every visual answers a stated question | "Because we had the data" |
| **Data-ink ratio** (Tufte) | Maximise ink that carries data; delete the rest | 3-D bars, heavy gridlines, drop shadows |
| **Choose the right encoding** | Position > length > angle > area > colour, in accuracy | A pie where a bar belongs |
| **Zero baseline on bars** | Bar **length** is the message | Truncated axis exaggerating a difference |
| **Consistent colour meaning** | One colour, one thing, across the whole dashboard | Red meaning "loss" here and "region A" there |
| **Order deliberately** | Sort by value unless there is a natural order | Alphabetical by accident |
| **Label directly** | Put labels on the marks | Forcing a trip to the legend |
| **Show uncertainty** | A small denominator is not a fact | 25% attrition from a team of four |
| **Progressive disclosure** | Summary first, detail on demand | Everything at once |

### 💡 Tufte's data-ink ratio, applied in one minute

Open any default chart and delete: the border, the background fill, heavy
gridlines, the redundant legend, and every decimal place nobody reads. The
chart gets easier to read every time. **Nothing you delete in that list has
ever carried information.**

### ⚠️ Pie charts, honestly

Not banned, but narrow: **parts of one whole, five slices or fewer, and only
when "roughly half" is the message rather than a ranking.** Humans compare
angles badly and lengths well. Two pies side by side are worse still — nobody
can compare across them.

**A ranked bar chart is the right answer to most questions a pie is used for.**

### Accessibility — a real requirement, not a footnote

| Requirement | What to do |
|---|---|
| **Colour blindness** (~8% of men) | Never encode by colour **alone**; add shape, label or position. Avoid red/green pairs |
| **Contrast** | At least 4.5:1 for text against its background |
| **Text size** | Nothing below 10–12 pt; dashboards get shown on projectors |
| **Alt text** | Set it on every visual — screen readers use it |
| **Tab order** | Set it, so keyboard users move sensibly |
| **Not by colour alone** | A red cell must also carry a symbol or a number |

**Red/green for good/bad is the single commonest accessibility failure**, and
it is exactly the pair most affected by the most common colour blindness. Use
blue/orange, or add symbols.

---

## 5.4 Advanced visualizations — the four interactive features

### 🔢 Slicers, filters, parameters, drilldowns

| Feature | What it does | Changes |
|---|---|---|
| **Filter** | Restricts data for a visual, page or report | The **data shown** |
| **Slicer** | An **on-canvas** filter the user can see and click | The data shown |
| **Parameter** | A user-chosen **value** feeding a calculation | **What is calculated** |
| **Drilldown** | Moves **down a hierarchy** in place | The **level of detail** |
| **Drill-through** | Jumps to another page filtered to the selection | The **page** |

### ⚠️ Slicer versus filter is a two-mark question

**A slicer is a filter the user can see.** Both restrict data; a filter lives in
the Filters pane (and may be hidden), a slicer occupies canvas space and
invites interaction. Put on canvas the two or three the user changes often;
leave the rest in the pane.

### 🎯 Parameters are the DSS component from Unit 1

**A parameter changes an input to a calculation, not the rows shown.** That is
the distinction, and it is what makes parameters the **what-if** feature — and
therefore the model-management component of a DSS (Unit 1 §1.6) living inside a
BI tool.

```
Filter:    "Show me the South region"           -> fewer rows
Parameter: "What if we raise prices by 5%?"     -> different numbers, same rows
```

In Power BI: **Modeling → New parameter → Numeric range**, which creates a
table and a measure you use in DAX. In Tableau: a parameter plus a calculated
field that references it.

```dax
Projected Revenue = [Total Revenue] * (1 + 'Price Change'[Price Change Value])
```

**Say the DSS connection in the viva.** A what-if parameter is a small DSS, and
it ties Unit 5 back to Unit 1.

### Graphs and maps as advanced visuals

The syllabus lists "Graphs and Maps" alongside the interactive features, and
both mean something more specific here than the basic charts of Unit 2.

| Visual | What it adds | Use it when |
|---|---|---|
| **Combo chart** (column + line) | Two units on one canvas — revenue as columns, margin % as a line | A total and a **rate** must be read together |
| **Waterfall** | Shows how a total got from A to B, step by step | Explaining a **variance**: budget → actual |
| **Scatter / bubble** | Two measures, plus size and colour | Looking for a **relationship**, not a ranking |
| **Decomposition tree** | Interactive, user-chosen drill path | "Why is this number what it is?" — the user picks the order |
| **Key influencers** | Ranks what drives a metric | An automated first pass at a diagnostic question |
| **Small multiples** | The same chart repeated per category | Comparing **shapes** across many categories |
| **Gauge / KPI** | Value against a target | A target genuinely exists. Otherwise it is decoration |

**Maps**, specifically:

| Map type | Encodes | Watch for |
|---|---|---|
| **Filled (choropleth)** | A value as **area colour** | **Area is not population.** Large empty districts dominate the eye |
| **Bubble / symbol** | A value as **circle size** at a point | Overlapping bubbles in dense cities |
| **Density / heat** | Concentration of points | Good for "where", useless for "how much" |
| **Shape map** | Custom regions from a shapefile | Needed for sales territories, which are not administrative areas |

### ⚠️ Use a map only when the question is genuinely geographic

A map is the most seductive visual on the list and the most often misused.
**If the question is "which region sold most?", a ranked bar chart answers it
better** — you can read the order instantly, which no map allows.

Use a map when **location itself is the variable**: distance to a store,
clustering, coverage gaps, routing. "Which of our districts have no outlet
within 20 km?" is a map question. "Rank the districts by sales" is not.

The choropleth trap is worth stating: colouring districts by *total* sales
makes large rural districts look important because they are big on screen.
**Normalise** — sales per capita, or per outlet — or use bubbles, whose size
you control.

### Drilldown and hierarchies

Drilldown needs a **hierarchy defined in the model** (Unit 4 §4.6). Given
`Region → City → Store`, the user expands from region to city to store in place.

| Control | Effect |
|---|---|
| **Drill down** (single item) | Expand the selected item one level |
| **Expand all** | Add the next level for **every** item |
| **Drill up** | Back a level |
| **Drill through** | Jump to a detail page filtered to the selection |

**Drill-through is the right answer to "users want the underlying rows".** Keep
the summary clean, and put the detail table on a drill-through page rather than
on the dashboard.

---

## 5.5 Layout, alignment and design

### 🔢 The F-pattern and the inverted pyramid

Readers of a left-to-right script scan in an **F**: across the top, across
again lower, then down the left edge. Design for it.

```
+--------------------------------------------------+
|  Title                          As at 27-08-2026 |
+--------------------------------------------------+
|  [KPI]   [KPI]   [KPI]   [KPI]                   |  <- most important, top-left
+--------------------------------------------------+
|                              |                   |
|   Trend over time            |   Breakdown       |  <- supporting
|                              |   by category     |
+------------------------------+-------------------+
|   Detail table / exceptions                      |  <- detail, on demand
+--------------------------------------------------+
| [slicers]                                        |
+--------------------------------------------------+
```

**Top-left is the most valuable real estate on the screen.** Put the number the
user came for there. The commonest layout mistake is putting the company logo
in it.

### The rules that make a dashboard look professional

1. **Align to a grid.** Misalignment by three pixels reads as carelessness even
   when nobody consciously notices it.
2. **Use a consistent gutter** between visuals — one spacing, everywhere.
3. **Limit the palette.** One accent colour, a neutral, and semantic colours
   reserved for meaning.
4. **One font, two or three sizes.** Never more than two fonts.
5. **Group related visuals** with whitespace, not boxes and borders.
6. **Fix the visual sizes.** Six charts of six sizes look accidental.
7. **Round sensibly.** ₹12.9K on a card; ₹12,880 in the detail table. Never
   ₹12,880.0000.
8. **Whitespace is not wasted space.** It is what makes the rest readable.
9. **Same filters, same place, every page.**

### ⚠️ The scroll test, and the five-second test

- **Scroll test:** if the dashboard scrolls, it is not a dashboard. Split it, or
  cut it.
- **Five-second test:** show it to someone for five seconds, take it away, and
  ask what the main message was. If they cannot say, the hierarchy is wrong —
  not their attention.

---

## 5.6 Publishing

| | **Power BI Service** | **Tableau Public** |
|---|---|---|
| Publish from | Desktop → Publish → workspace | Desktop → Server → Tableau Public → Save |
| Who can see it | Whoever you grant access to | **Everyone on the internet** |
| Cost to share | **Pro licence both sides** | Free |
| Refresh | Scheduled (8/day Pro, 48 Premium); gateway for on-prem | **Manual re-publish**, or a linked Google Sheet |
| Row-level security | Yes | No |
| Right for | Real organisational data | Portfolios, coursework, public data |

### ⚠️ The same warning as Unit 3, because it matters most here

**Tableau Public publishes to the open web and allows download of the
workbook.** For lab experiments 8, 9 and 12 that is intended and fine. For
anything containing real student, employee or customer data it is a data
breach. Check what is in the extract before you press Save.

### 💡 Publishing is not the end of the job

| After publishing | Why |
|---|---|
| Set **scheduled refresh** and alert on failure | A silently stale dashboard is worse than none |
| Add the **data-as-at timestamp** to the canvas | Users must see freshness without asking |
| Check **usage metrics** after a month | Nobody opening it is the finding |
| Write **one paragraph** of what it is for | Six months on, nobody remembers |

---

## 5.7 Storytelling and insight communication

### 🎯 The big idea

**A chart shows what happened. A story says what it means and what to do.**

The gap between them is where BI either earns its budget or does not.

### 🔢 The structure that works

```
   Context  ->  Complication  ->  Cause  ->  Consequence  ->  Call to action
```

| Step | Says | Example |
|---|---|---|
| **Context** | The normal state | "Revenue runs ₹12–13 lakh a quarter" |
| **Complication** | What changed | "Q2 fell 11% in South" |
| **Cause** | Why | "Two large accounts churned in April" |
| **Consequence** | Why it matters | "That is 8% of annual revenue if unrecovered" |
| **Call to action** | What to do | "Assign a retention owner to the top 10 accounts this quarter" |

**The call to action is what distinguishes BI from reporting**, and it is what
the ten-mark storytelling question wants to see.

### The rules of insight communication

1. **Lead with the finding, not the method.** "South fell 11%" first; how you
   calculated it only if asked.
2. **One message per visual.** If a chart needs two sentences to explain, it is
   two charts.
3. **Annotate on the chart.** An arrow saying "price change here" beats a
   paragraph below it.
4. **Quantify the consequence in the units the audience cares about** — rupees,
   customers, days. Not percentages alone.
5. **Say what you do not know.** "This is two months of data; the trend may not
   hold" builds more trust than false confidence.
6. **Recommend something.** An analysis with no recommendation puts the work
   back on the audience.

### ⚠️ Correlation, again

Course 4 taught it and BI is where it gets violated. A dashboard showing two
lines moving together will be read as cause and effect by whoever sees it.
**If you cannot support the causal claim, do not put the two lines on one
chart** — or annotate it explicitly. This is a legitimate exam point about
ethical insight communication.

---

## 5.8 Case study — sales forecasting and budgeting

The syllabus sets a decision-making scenario here. Sales forecasting exercises
every part of the unit.

**The decision.** How much stock to buy and what quota to set per region for
next quarter. Decided by the sales director, quarterly.

**The dashboard:**

| Zone | Contents |
|---|---:|
| KPI row | Revenue QTD vs target · Forecast for quarter-end · Variance % · Pipeline coverage |
| Trend | Actual by month, forecast continuing it as a **dashed line with a confidence band** |
| Breakdown | Revenue by region, ranked, with target markers |
| What-if | **Parameters**: growth rate, price change, win rate |
| Detail | Drill-through to accounts, for the account owner |

### ⚠️ Three traps in this case, and they are all examinable

1. **Show the forecast's uncertainty.** A single forecast line will be treated
   as a promise. A band — or three scenarios, low/expected/high — communicates
   what a point estimate cannot. This is Course 4's confidence interval doing
   its actual job.
2. **Do not draw the forecast in the same style as the actuals.** Dashed,
   lighter, and clearly labelled, with a vertical rule at "today". Otherwise
   people will quote a forecast as an actual within the week.
3. **Budget variance needs both absolute and percentage.** A region 50% under
   budget on ₹2 lakh matters less than one 5% under on ₹2 crore. **Show both,
   and sort by the absolute figure**, because that is the one that decides where
   attention goes.

**The what-if parameter is what makes it a decision tool rather than a report.**
Let the director move the growth-rate slider and watch the quarter-end forecast
move; that closes the loop back to Unit 1's Decision Support System, and saying
so is a good way to end a ten-mark answer.

---

## Practice problems

### Problem 1

What makes a dashboard effective? List and explain the principles, and describe
a good layout. *(10 marks)*

**Solution.**

Open with the definition and its constraints: **one screen, few visuals, a
specific person, something they act on, refreshed automatically.**

Then the principles from §5.3 — purpose first; data-ink ratio; right encoding
(position beats length beats angle beats area beats colour); zero baseline on
bars; consistent colour meaning; deliberate ordering; direct labelling; show
uncertainty; progressive disclosure. Explain each in a line.

Then the layout, drawn: title and timestamp at the top; **3–5 KPI cards on the
top row, most important top-left**; trend and breakdown in the middle; detail
at the bottom or on a drill-through page; slicers in a consistent position.
Mention the **F-pattern** as the justification.

Add accessibility, because most answers omit it: never encode by colour alone,
4.5:1 contrast, alt text, and **avoid red/green**, which is both the commonest
choice and the worst for the commonest colour blindness.

Close with the two tests — the **scroll test** (if it scrolls it is a report)
and the **five-second test** (if the viewer cannot state the message, the
hierarchy is wrong).

### Problem 2

Distinguish filters, slicers, parameters and drilldowns. *(10 marks)*

**Solution.**

Give the table from §5.4, then make the two distinctions that carry the marks:

**Slicer vs filter:** both restrict which rows are shown; **a slicer is a
filter the user can see and click**, occupying canvas space. Filters live in
the pane and may be hidden. Put the two or three most-used on canvas.

**Filter vs parameter — the important one:** a filter changes **which rows are
shown**; a parameter changes **what is calculated**. Give the contrast:

```
Filter:    "Show me the South region"        -> fewer rows, same measures
Parameter: "What if we raise prices by 5%?"  -> same rows, different numbers
```

**Drilldown vs drill-through:** drilldown moves down a hierarchy *in place*
(Region → City → Store) and needs a hierarchy defined in the model;
drill-through jumps to a different page filtered to the selection, and is the
right way to give users row-level detail without cluttering the dashboard.

Finish with the connection worth stating: **a what-if parameter is the model
component of a Decision Support System** (Unit 1 §1.6) inside a BI tool.

### Problem 3

Design a dashboard for sales forecasting. Describe its components and the
traps. *(10 marks)*

**Solution.**

**Start with the decision, not the charts:** how much stock to buy and what
quota to set per region, decided quarterly by the sales director. Everything
follows from that.

**Components:** a KPI row (revenue QTD vs target, forecast to quarter-end,
variance %, pipeline coverage); a trend chart with actuals solid and forecast
dashed; a ranked regional breakdown with target markers; what-if parameters for
growth rate and price change; drill-through to account detail.

**The three traps, which is where the marks are:**

1. **Show uncertainty.** A single forecast line is read as a promise. Use a
   confidence band or low/expected/high scenarios — Course 4's confidence
   interval doing its job.
2. **Style the forecast differently.** Dashed, lighter, labelled, with a
   vertical rule at today. Otherwise a forecast gets quoted as an actual.
3. **Show variance in both rupees and percent, sorted by rupees.** 50% under on
   ₹2 lakh matters less than 5% under on ₹2 crore.

Close on the parameter: it is what makes this a decision tool rather than a
report, and it is Unit 1's DSS model component living inside a BI dashboard.

---

## Exam questions from this unit

**Two marks**

1. Give the difference between a slicer and a filter.
2. What is the data-ink ratio?
3. What is drill-through?
4. Why should a bar chart's axis start at zero?
5. Name two accessibility requirements for a dashboard.
6. What does a scorecard have that a dashboard need not?

**Five marks**

1. Distinguish a dashboard, a report and a scorecard.
2. Explain the components of a dashboard.
3. Explain parameters and how they differ from filters.
4. Describe dashboard layout principles.
5. Compare publishing to Power BI Service and Tableau Public.
6. When should you *not* build a dashboard?

**Ten marks**

1. Explain the principles of effective visualization and dashboard design.
2. Distinguish filters, slicers, parameters and drilldowns with examples.
3. Design a dashboard for a sales forecasting scenario and explain each choice.
4. Explain storytelling in BI and how insight should be communicated.

---

## Mistakes that cost marks

- **Defining a dashboard as "several charts on a page".** One screen, few
  visuals, one audience, something they act on, refreshed automatically.
- **A KPI with no comparison.** "₹12,880" is not information. Against target,
  prior period or peer — always.
- **Saying a parameter filters data.** It changes an input to a calculation.
  That distinction is the question.
- **Truncating a bar chart axis.** Length is the message; a truncated axis
  lies with it.
- **Red/green for good/bad.** The commonest choice and the worst for the
  commonest colour blindness.
- **Forgetting the timestamp.** Users cannot judge freshness, so they assume
  it is current — and eventually they are wrong.
- **Putting a detail table on the dashboard.** Use drill-through.
- **A forecast drawn like an actual.** It will be quoted as one.
- **Ending an analysis with a chart.** Finish with a recommendation, or the
  work lands back on the audience.
- **Omitting accessibility.** It is in the syllabus — "layout, alignment,
  accessibility" — and most answers skip the third word.
