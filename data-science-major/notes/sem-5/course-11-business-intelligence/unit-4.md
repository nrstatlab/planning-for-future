# Unit 4 — Data Modeling and Relationships in BI Tools

**Syllabus topics:** Dimensional modeling — dimension, dimension table, fact,
fact table, schema; star and snowflake schemas. Power BI — relationships,
cardinality, cross-filtering. Tableau — joins (inner, left, full), blending.
Data governance — metadata, hierarchies, quality. Data model design best
practices — design and implement a data model in Power BI and Tableau; HR or
retail data model design and insights. Case study — retail BI for sales
optimization.

> **This is the unit that earns marks.** Units 2, 3 and 5 are tool operation —
> useful, quickly learned, and worth fewer marks than the hours they consume.
> This unit is where the thinking is, and where a wrong answer produces a
> dashboard that is confidently and silently incorrect.

---

## 4.1 A note on the overlap with Course 8

**If you took Course 8 (Data Mining), you have already studied half of this
unit.** Course 8 Unit 1 covered data warehousing, star and snowflake schemas,
fact constellations, fact and dimension tables, and OLAP cube operations. Do
not study that material twice.

| Topic | Where it was taught | What is new here |
|---|---|---|
| Fact and dimension tables | **Course 8 §1.4** | Nothing — revise it |
| Star and snowflake schemas | **Course 8 §1.5** | Nothing conceptually; §4.3 restates it because this syllabus lists it |
| Fact constellation | **Course 8 §1.5** | Not listed here, but still examinable |
| OLAP cube operations | **Course 8 §1.6** | Not in this syllabus; the drill-down in Unit 5 is the same idea |
| **Relationships and cardinality** | — | **New** — §4.4 |
| **Cross-filter direction** | — | **New**, and the source of the worst bugs — §4.5 |
| **Governance, metadata, hierarchies** | — | **New** — §4.6 |

**The genuinely new material is §4.4 to §4.6.** Everything before that is
Course 8 revision written in BI vocabulary — which is itself worth doing once,
because the exam asks it in *this* course's words.

---

## 4.2 Dimensional modeling — the vocabulary

### 🎯 The big idea

**Split every table into things you measure and things you measure them by.**

| | **Fact** | **Dimension** |
|---|---|---|
| Holds | **Measurements** — numbers you aggregate | **Context** — the words you slice by |
| Rows | **Many** — millions | Few — hundreds or thousands |
| Grows | Constantly, with events | Slowly |
| Columns | Foreign keys + numeric measures | Descriptive attributes |
| Example | A sale, a click, a hospital admission | Product, Store, Date, Customer |
| Question it answers | "How much?" | "By what?" |

**The test:** if you would ever put it on an axis or in a slicer, it is a
**dimension attribute**. If you would ever `SUM` it, it is a **fact measure**.

### 🔢 The grain — state it first, always

**The grain is what one row of the fact table represents.** Deciding it is the
first step in dimensional modelling and the first thing an examiner asks.

The sample fact table's grain is: **one row per product, per store, per day.**

Why it must be stated before anything else:

- **It fixes which dimensions can attach.** A dimension can only join if it is
  at, or above, the grain. Customer cannot join a fact grained per store-day,
  because a store-day has many customers.
- **It decides whether a measure is additive.** Quantity sums over any
  dimension. A stock *balance* does not sum over time — it is
  **semi-additive**, and summing January and February stock levels gives a
  meaningless number.
- **Mixed grain is a data bug that looks like a data model.** If some rows are
  daily and some monthly, every total is wrong and nothing warns you.

### 🔢 Types of measure — an easy five marks

| Type | Sums over | Example |
|---|---|---|
| **Additive** | **Every** dimension | Sales amount, quantity |
| **Semi-additive** | Some, but **not time** | Stock on hand, account balance, headcount |
| **Non-additive** | **No** dimension | Ratios, percentages, unit price |

**Margin % is non-additive** — which is exactly why Unit 2's average-of-averages
trap exists. You cannot add or average percentages; you must re-derive them
from their additive components. That connects the two units and is worth saying.

---

## 4.3 Star and snowflake schemas

### 🔢 The star

```
              dim_date                dim_store
                  \                     /
                   \                   /
                    +--- fact_sales --+
                   /                   \
                  /                     \
            dim_product              (measures: qty)
```

**One fact table in the middle, dimensions one join away, each denormalised
into a single table.** Product's category sits *in* `dim_product`, not in a
separate `dim_category`.

### 🔢 The snowflake

```
   dim_supplier --- dim_product --- fact_sales --- dim_store
                                         |
                                     dim_date
```

**A dimension normalised into further levels.** In the sample model,
`dim_product` carries `supplier_key` pointing at `dim_supplier` — that single
edge is what makes it a snowflake rather than a star.

### 🔢 Star vs snowflake — the comparison the exam wants

| | **Star** | **Snowflake** |
|---|---|---|
| Dimensions | **Denormalised** — one table each | **Normalised** into levels |
| Joins to answer a query | **Fewer** | More |
| Query speed | **Faster** | Slower |
| Storage | Slightly more (redundancy) | Slightly less |
| Redundancy | Accepted deliberately | Eliminated |
| Ease of understanding | **High** — business users can read it | Lower |
| Maintenance of shared attributes | Update in many rows | **Update in one place** |
| Use when | **Almost always** in BI | Dimensions are huge, or shared across facts |

**The default is a star, and say so.** Storage is cheap and joins are not; BI
tools are optimised for the star. Snowflake only when a dimension is genuinely
enormous, or an attribute is shared and changes often.

### ⚠️ "Why not just one flat table?" — the question worth answering properly

Beginners import one wide spreadsheet and build on it. It works, and then it
does not. Measured on the sample model, and asserted in
`13_data_model.py`:

| Model | Cells stored |
|---|---:|
| Star — fact (9×4) + three dimensions (4×6, 3×4, 4×5) | **92** |
| One flat table — 9 rows × 16 columns | **144** |

At nine rows the difference is trivial. **The ratio is what matters, because
dimensions do not grow and the fact table does:**

| Fact rows | Star | Flat | Flat ÷ Star |
|---:|---:|---:|---:|
| 9 | 92 | 144 | 1.57× |
| 1,000 | 4,056 | 16,000 | 3.94× |
| 1,000,000 | 4,000,056 | 16,000,000 | **4.00×** |

**Four times the storage, converging.** And storage is the *least* of it:

1. **Redundancy invites inconsistency.** "Vijayawada" is stored on every one of
   the four rows for that store. Spell it "Vijaywada" on one and you now have
   two stores.
2. **Filtering is slower.** A slicer on region must scan the whole fact table
   rather than a three-row dimension.
3. **You cannot show what did not happen.** A store with no sales has no rows,
   so it vanishes from the report. In a star it exists in `dim_store` and shows
   as blank — which is the answer the business needs.
4. **Attributes cannot be updated in one place.** Rename a category and you
   rewrite a million rows.

**Point 3 is the one that convinces people.** "Which products sold nothing last
month?" is unanswerable from a flat table and trivial from a star.

---

## 4.4 Power BI relationships and cardinality

### 🎯 The big idea

**A relationship is a join you declare once in the model instead of writing in
every query, and it propagates filters.** That second half is what makes it
different from a SQL join.

When a user clicks "South" on a store slicer, the filter travels
`dim_store → fact_sales` and every measure recalculates. Nothing was joined at
query time; the filter simply flowed along the relationship.

### 🔢 Cardinality

| Cardinality | Meaning | In the sample model |
|---|---|---|
| **One-to-many (1:*)** | One dimension row, many fact rows | **`dim_product` → `fact_sales`**. The normal case |
| Many-to-one (*:1) | The same thing, stated from the fact side | `fact_sales` → `dim_store` |
| One-to-one (1:1) | One row each side | Rare; usually means the tables should be merged |
| **Many-to-many (*:*)** | Neither side is unique | **Avoid.** Almost always a missing bridge table |

**The "one" side must be genuinely unique.** Power BI refuses to create a 1:*
relationship if the key repeats — and that refusal is usually telling you the
grain is wrong, not that the tool is being difficult.

### ⚠️ Many-to-many is a warning, not a feature

Power BI added many-to-many relationships, and they are usually the wrong
answer. The right answer is a **bridge (junction) table** — which is Course 5's
junction table and Course 10's junction collection, unchanged.

**Students → Courses** is many-to-many; the fix is an `enrollments` table with
one row per pairing, related 1:* from each side. Course 10 §4.2 made exactly
this argument about MongoDB, and the reasoning survives the move to a BI tool.

### Active and inactive relationships

**Only one relationship between two tables can be active at a time.** With both
an Order Date and a Ship Date pointing at `dim_date`, one is active (solid) and
one inactive (dashed). Activate the other for a specific measure with
`USERELATIONSHIP`:

```dax
Revenue by Ship Date =
    CALCULATE([Total Revenue], USERELATIONSHIP(fact[ship_date], dim_date[date]))
```

**The alternative is a role-playing dimension** — a second date table for
shipping. Both are correct; `USERELATIONSHIP` keeps one date table, and a
second table is easier for users to understand. Name both and say which you
would choose, and why.

---

## 4.5 Cross-filter direction — where the worst bugs come from

### 🎯 The big idea

**Cross-filter direction decides which way a filter travels along a
relationship.**

| Direction | Filters flow | Default for |
|---|---|---|
| **Single** | **Dimension → fact only** | 1:* relationships |
| **Both** (bidirectional) | Fact → dimension as well | Nothing, by default |

Single direction is the default because it is unambiguous: dimensions filter
facts, and facts do not filter dimensions.

### ⚠️ Turning on bidirectional filtering is the commonest self-inflicted wound

It looks harmless and it solves the immediate problem. Then:

1. **Ambiguity.** With several dimensions bidirectional, more than one filter
   path can exist between two tables. Power BI may refuse to create the
   relationship — or, worse, pick a path and give you a number with no warning.
2. **Performance.** Filters propagate further, and every measure gets slower.
3. **Wrong totals.** In a model with two fact tables sharing a dimension,
   bidirectional filtering lets fact A filter the dimension, which then filters
   fact B — so a slicer on one fact silently changes the other's totals.

**The rule: leave it single, and solve the problem you thought needed
bidirectional with a measure instead.** `CROSSFILTER` inside `CALCULATE` turns
it on for one measure only, which is nearly always the right scope:

```dax
Products Sold = CALCULATE(DISTINCTCOUNT(dim_product[product_key]),
                          CROSSFILTER(fact_sales[product_key],
                                      dim_product[product_key], BOTH))
```

### 💡 The legitimate use

A slicer that should only show values that actually occur in the fact table —
"show me only products that sold" — genuinely needs the fact to filter the
dimension. That is the real use case, it is narrow, and doing it per-measure
with `CROSSFILTER` is better than doing it model-wide.

---

## 4.6 Tableau — joins and blending

The syllabus lists **joins (inner, left, full) and blending** in this unit,
beside Power BI's relationships. Unit 3 §3.6 covered them as tool operation;
here they belong to the *modelling* question, and the comparison with Power
BI's relationships is what this unit adds.

### 🔢 The join types

| Join | Keeps | On 4 stores, sales for 3, plus an orphan sale |
|---|---|---:|
| **Inner** | Only rows matching on both sides | **3 rows** |
| **Left** | All of the left, matched from the right | **4 rows** |
| **Right** | All of the right, matched from the left | **4 rows** |
| **Full outer** | Everything from both | **5 rows** |

All four counts are asserted in
`14_joins_blending.py`.
**Inner loses both the store that sold nothing and the sale with no store;
full outer keeps both and is how you find them.** "Which stores sold nothing?"
is a **left join filtered to null** — the same question §4.3 used to argue
against a flat table.

### 🔢 Joins against Power BI relationships — the comparison this unit wants

| | **Tableau join** | **Power BI relationship** |
|---|---|---|
| Declared | On the Data Source tab, **per data source** | Once, in **Model view** |
| When it runs | At query time, materialising rows | **Never materialised** — it propagates *filters* |
| Result | A **wider table** with more rows | Tables stay separate |
| Duplication risk | **Yes — the fan trap** | Low: 1:\* is enforced |
| Direction | Not applicable | **Cross-filter direction** — §4.5 |
| Reuse | Per source | Model-wide |

**The conceptual difference is the one to state:** a join *combines rows*; a
relationship *propagates filters*. That is why a Power BI model can hold six
tables and never duplicate anything, while one careless Tableau join doubles
your revenue.

### ⚠️ Blending, and why it cannot fan out

**Blending is a left join performed after aggregation.** Each source is
aggregated to the linking field first, then the results are matched.

| | **Join** | **Blending** |
|---|---|---|
| When | Before aggregation | **After** aggregation |
| Sources | Usually one connection | **Different** sources — Excel + SQL + Sheets |
| Granularity | Row level | **The linking field's level** |
| Duplication | **Possible** | **Impossible** |
| Type | Any | Effectively a left join from the **primary** |

That single sentence explains both of blending's properties: it cannot
duplicate rows (they were already aggregated away), and it cannot give you
row-level detail from the secondary source (for the same reason).

**Primary and secondary are not symmetric.** The first source used in the view
is primary; blending keeps all of its rows and matches from the secondary.
Swap them and the answer changes.

### 🔢 The fan trap, in modelling terms

Unit 3 §3.6 measured it: joining 9 sales rows to a targets table with two rows
per store, **on store alone**, turns ₹12,880 into **₹25,760** and ₹20,800 into
**₹66,700**, silently.

Stated as a *modelling* failure rather than a tool failure: **you joined two
fact tables at different grains through a shared dimension.** Sales is grained
per product-store-day; targets per store-quarter. Nothing legitimises combining
them at row level.

| Fix | Modelling reading |
|---|---|
| Join on store **and** quarter | Match the grains as far as they can be matched |
| **Blend** | Aggregate each fact to a common grain first |
| `{FIXED [Store] : SUM([Target])}` | Compute the target at *its own* grain, whatever the view |
| **In Power BI:** two fact tables sharing `dim_store` and `dim_date` | A **fact constellation** — and no join, so no fan trap |

**That last row is the answer this unit is looking for.** A star schema with
two fact tables sharing conformed dimensions cannot fan out, because the tables
are never joined — filters flow from the dimensions into each fact
independently. The fan trap is a symptom of modelling by joining.

## 4.7 Data governance — metadata, hierarchies, quality

### 🎯 The big idea

**Self-service BI's failure mode is five dashboards with five different revenue
figures, all defensible.** Governance is what prevents that, and it is
organisational before it is technical.

### Metadata

| Kind | What it is | Where in a BI tool |
|---|---|---|
| **Business metadata** | What a field *means* — "Revenue is net of returns, excludes GST" | Field descriptions, a data dictionary |
| **Technical metadata** | Types, keys, lineage, refresh schedules | The model view, lineage view |
| **Operational metadata** | Refresh history, failures, usage | Service monitoring |

**The single highest-value governance act is writing the business definition of
every measure into the model.** In Power BI that is a measure's Description; it
appears as a tooltip. It takes five minutes and prevents the five-figures
problem.

### Hierarchies

A **hierarchy** is an ordered set of levels within a dimension, giving
drill-down for free:

| Dimension | Hierarchy |
|---|---|
| Date | Year → Quarter → Month → Day |
| Store | Region → City → Store |
| Product | Category → Subcategory → Product |

**Define hierarchies in the model, not per visual.** Then every visual drills
consistently, and Unit 5's drilldowns work without extra configuration.

### ⚠️ Every model needs a proper Date dimension

**Do not use the date column in the fact table.** Create a separate date table,
mark it as a date table, and relate it.

Why it is not optional:

- **Time intelligence functions require it.** `TOTALYTD`, `SAMEPERIODLASTYEAR`
  and the rest need a table with **one row per date and no gaps**.
- **Days with no sales disappear otherwise.** A fact-derived date list has no
  row for a day nothing sold, so the line chart silently skips it — and a flat
  line reads very differently from an absent one.
- **It is where fiscal periods, holidays and week numbers live.** Your fiscal
  year probably does not start in January.

### Data quality — the six dimensions

| Dimension | Question | Failure |
|---|---|---|
| **Accuracy** | Does it match reality? | Price recorded as 100 instead of 1000 |
| **Completeness** | Is anything missing? | 12% of rows have no region |
| **Consistency** | Do sources agree? | CRM says 4,000 customers, billing says 4,120 |
| **Timeliness** | Is it current enough? | Yesterday's stock, in a live reorder decision |
| **Validity** | Does it obey the rules? | A date of 30 February; a negative quantity |
| **Uniqueness** | Any duplicates? | A re-upload doubled last month |

### 💡 Fix quality upstream, not in Power Query

You *can* patch bad data in Power Query, and sometimes you must. But a fix in
Power Query helps one report, while the same bad data flows into every other
system. **Escalate the root cause; patch only to keep moving.** Saying that
distinguishes a governance answer from a tooling answer.

---

## 4.8 Data model design best practices

A checklist worth memorising — it answers several ten-mark questions.

1. **State the grain first**, and write it down. Every later decision depends
   on it.
2. **Star, not snowflake**, unless a dimension is genuinely huge or shared.
3. **Never one flat table.** §4.3 gives four reasons; the "what did not
   happen?" one is decisive.
4. **A dedicated Date dimension**, marked as such, with no gaps.
5. **Single cross-filter direction.** Use `CROSSFILTER` per measure where you
   truly need both.
6. **Integer surrogate keys** on relationships, not long text keys — they
   compress better and join faster.
7. **Hide keys and technical columns** from the report view. Users should see
   only what they can use.
8. **Measures, not calculated columns**, unless you must slice by the result.
9. **Name things for the business** — `Total Revenue`, not `sum_rev_calc_v2`.
10. **Write a description on every measure.** The cheapest governance there is.
11. **Remove columns you do not use.** They cost memory and confuse users.
12. **One dataset, many reports** — the semantic layer that stops definitions
    drifting.

---

## 4.9 Case study — retail BI for sales optimization

The syllabus sets this case here, and it is the natural ten-mark modelling
question. It continues Unit 1 §1.8's inventory case.

**The requirement.** Which products, in which stores, are driving and dragging
sales? Category managers decide range and promotion weekly.

**Step 1 — the grain.** *One row per product, per store, per day.* Daily
because promotions run for days and weekly would hide them; product × store
because that is the level at which the decision is made.

**Step 2 — the schema.**

```
   dim_date          dim_store
        \               /
         +- fact_sales -+          grain: product x store x day
        /               \          measures: qty, revenue, cost, discount
   dim_product      dim_promotion
        |
   dim_supplier                    (this edge makes it a snowflake)
```

**Step 3 — justify each decision.**

| Decision | Why |
|---|---|
| Separate `dim_date` | Time intelligence needs it; days with no sales must still appear |
| `dim_product` denormalised (category *inside* it) | Star; categories are few and change rarely |
| `dim_supplier` kept separate | Supplier attributes are shared across products and change independently — the one place a snowflake earns its keep |
| `dim_promotion` | A promotion has its own attributes — dates, discount, mechanic. It belongs to neither product nor store |
| `qty`, `revenue`, `cost` as additive measures | They sum over every dimension |
| Stock on hand **not** in this fact table | It is **semi-additive** — it does not sum over time. It needs its own snapshot fact table |

**Step 4 — the measures.**

```dax
Total Revenue  = SUMX(fact_sales, fact_sales[qty] * RELATED(dim_product[list_price]))
Total Cost     = SUMX(fact_sales, fact_sales[qty] * RELATED(dim_product[unit_cost]))
Gross Margin   = [Total Revenue] - [Total Cost]
Margin Pct     = DIVIDE([Gross Margin], [Total Revenue])
Revenue LY     = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
YoY Growth     = DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY])
Pct of Category= DIVIDE([Total Revenue],
                        CALCULATE([Total Revenue], ALLEXCEPT(dim_product, dim_product[category])))
```

### ⚠️ The modelling trap in this case

**Stock on hand does not belong in the sales fact table.** It is a *state*, not
an *event*: it has a value at every instant, not a value per transaction.

Putting it there produces two failures — the grain becomes mixed, and `SUM` of
stock across days returns a number with no meaning (adding Monday's 50 units to
Tuesday's 48 gives 98 units that never existed).

**The fix is a second fact table**: a periodic snapshot, grained one row per
product per store per day, holding the closing balance. Both facts share
`dim_product`, `dim_store` and `dim_date` — which makes this a **fact
constellation**, exactly as Course 8 §1.5 defined it.

**That is the ten-mark answer.** Spotting that one requested measure needs its
own fact table, and naming the resulting schema, is what distinguishes a full
answer from a diagram.

---

## Practice problems

### Problem 1

Distinguish star and snowflake schemas. Which would you choose for a retail
sales model, and why? *(10 marks)*

**Solution.**

Define both — a star has denormalised dimensions one join from the fact; a
snowflake normalises dimensions into further levels. Draw both, using
`dim_product → dim_supplier` as the snowflake edge.

Give the comparison table from §4.3 — joins, speed, storage, redundancy,
readability, maintenance.

**Choose the star**, and justify with the numbers: joins cost query time, and
storage is cheap. Then give the exception honestly — snowflake a dimension when
it is genuinely huge, or when an attribute is shared across several dimensions
and changes often, which is why `dim_supplier` is separate in the worked model.

Finish with the strongest point: **never one flat table**, and give the four
reasons — 4× the storage at scale, redundancy causing inconsistent spellings,
slower filtering, and above all that a flat table **cannot show what did not
happen**, so a store with no sales disappears from the report entirely.

### Problem 2

What is cross-filter direction? Why is bidirectional filtering dangerous?
*(10 marks)*

**Solution.**

**Definition:** cross-filter direction decides which way a filter travels along
a relationship. Single (the default on 1:*) means dimension filters fact only;
Both means the fact can filter the dimension too.

**Why single is the default:** it is unambiguous. Dimensions describe facts;
facts do not describe dimensions.

**Three dangers, and give all three:**

1. **Ambiguity** — with several bidirectional relationships more than one
   filter path can exist between two tables. Power BI either refuses the
   relationship or silently picks a path, giving a number nobody can explain.
2. **Performance** — filters propagate further, so every measure slows.
3. **Wrong totals across fact tables** — with two facts sharing a dimension,
   fact A filters the dimension which then filters fact B, so a slicer on one
   silently changes the other's numbers.

**The right answer:** leave it single and scope it per measure with
`CROSSFILTER` inside `CALCULATE`. Give the legitimate use case — a slicer
showing only products that actually sold — and note that even that is better
done per-measure than model-wide.

### Problem 3

Design a data model for an HR analytics dashboard. State the grain, the tables,
the relationships and three measures. *(10 marks)*

**Solution.**

**Grain.** Two facts, because there are two grains, and saying so is the point:

- `fact_headcount` — **one row per employee per month** (a periodic snapshot)
- `fact_movement` — **one row per joining or leaving event** (a transaction fact)

**Dimensions:** `dim_employee` (id, name, gender, date of birth, education),
`dim_department`, `dim_role` (role, grade, band), `dim_date`, `dim_location`.

**Relationships:** 1:* from every dimension to both facts, single direction.
Both facts share `dim_date`, `dim_department` and `dim_employee` — a **fact
constellation**.

**Measures:**

```dax
Headcount      = DISTINCTCOUNT(fact_headcount[emp_id])
Leavers        = CALCULATE(COUNTROWS(fact_movement), fact_movement[type] = "Exit")
Avg Headcount  = AVERAGEX(VALUES(dim_date[month]), [Headcount])
Attrition Rate = DIVIDE([Leavers], [Avg Headcount])
```

**The two points that earn the top marks:**

1. **Headcount is semi-additive** — it does not sum over time. Twelve monthly
   headcounts of 100 is 100 people, not 1,200. Hence `AVERAGEX` over months in
   the denominator, not `SUM`.
2. **Show headcount beside every rate.** A four-person team with one leaver
   shows 25% attrition and is not in trouble; small denominators produce
   unstable percentages that get believed. Suppress rates below a minimum
   denominator.

---

## Exam questions from this unit

**Two marks**

1. What is the grain of a fact table?
2. Give one example each of an additive, semi-additive and non-additive measure.
3. What is a surrogate key?
4. What does cardinality 1:* mean?
5. Name the six dimensions of data quality.
6. What is a role-playing dimension?

**Five marks**

1. Distinguish fact tables from dimension tables.
2. Explain star and snowflake schemas with diagrams.
3. Explain cardinality and cross-filter direction in Power BI.
4. Why does every model need a dedicated Date dimension?
5. Explain metadata and its three kinds.
6. List and explain any six data model design best practices.

**Ten marks**

1. Compare star and snowflake schemas and justify a choice for retail sales.
2. Explain cross-filter direction and the dangers of bidirectional filtering.
3. Design a data model for an HR or retail scenario, stating grain, tables,
   relationships and measures.
4. Explain data governance in BI — metadata, hierarchies and quality.

---

## Mistakes that cost marks

- **Not stating the grain.** Every other modelling decision depends on it, and
  examiners look for it in the first line.
- **Putting a semi-additive measure in a transaction fact table.** Stock on
  hand needs its own snapshot fact. Summing it over time is meaningless.
- **Building one flat table.** Four reasons in §4.3; the decisive one is that
  you cannot report on what did not happen.
- **Turning on bidirectional filtering to fix a slicer.** Use `CROSSFILTER` in
  one measure instead.
- **Using the fact table's date column instead of a date dimension.** Time
  intelligence breaks and empty days vanish.
- **Calling many-to-many a solution.** It is a symptom; add a bridge table.
- **Confusing snowflake with fact constellation.** Snowflake = a normalised
  *dimension*. Constellation = several *fact* tables sharing dimensions.
- **Describing governance as software.** It is agreed definitions and
  ownership; the tool only records them.
