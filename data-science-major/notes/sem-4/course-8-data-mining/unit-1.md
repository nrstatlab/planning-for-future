# Unit 1 — Data Warehousing

**Syllabus topics:** Introduction to Data Warehouse, differences between
database systems and data warehouse, data warehouse characteristics, data
warehouse architecture and its components, data modeling, schema design, star
and snowflake schema, fact constellation, fact table, OLAP cube, OLAP
operations.

> The syllabus writes this unit's number as `Unit-1:` while every other course
> in the programme writes `Unit 1.` — one of the inconsistencies recorded in
> [SYLLABUS-REVIEW.md](../../../SYLLABUS-REVIEW.md).

---

## 1.1 What a data warehouse is

### 🎯 The big idea

An operational database is built to **record** what is happening right now, as
fast as possible. A data warehouse is built to **analyse** what has happened,
over years, across every system the organisation runs. Those two goals pull
the design in opposite directions, which is why you need two databases and not
one.

**Bill Inmon's definition**, which is the one to quote:

> A data warehouse is a **subject-oriented**, **integrated**, **time-variant**,
> **non-volatile** collection of data in support of management's
> decision-making process.

Those four adjectives are a guaranteed exam question. Learn them as four
claims, each with a consequence:

| Characteristic | Meaning | Consequence |
|---|---|---|
| **Subject-oriented** | Organised around *subjects* — sales, customer, product — not around applications | You ask "what did we sell?", not "what is in the billing system?" |
| **Integrated** | One consistent format, drawn from many sources | Gender stored as `M/F` here and `1/0` there must be reconciled **before** loading |
| **Time-variant** | Every record carries a time dimension; history is kept | You can compare this March with last March |
| **Non-volatile** | Loaded and read, never updated in place by users | A report run twice gives the same answer twice |

**Non-volatile is the one students misstate.** It does not mean the warehouse
never changes — new data is loaded on a schedule. It means users do not
`UPDATE` or `DELETE` rows. Operational systems overwrite an address when a
customer moves; a warehouse keeps both, with dates, because "where did our
customers live in 2024?" is a question someone will ask.

## 1.2 Database systems versus data warehouses

### 🔢 OLTP versus OLAP

This table is the most examined content in the unit.

| | **OLTP** (operational database) | **OLAP** (data warehouse) |
|---|---|---|
| Full name | On-Line **Transaction** Processing | On-Line **Analytical** Processing |
| Purpose | Run the business | Analyse the business |
| Users | Clerks, customers, applications | Analysts, managers, executives |
| Typical operation | Insert, update, delete one row | Read millions of rows, aggregate |
| Data | Current, detailed | Historical, summarised **and** detailed |
| Time span | Days to months | 5–10 years |
| Design | **Normalised** (3NF) — avoid redundancy | **Denormalised** (star) — avoid joins |
| Query complexity | Simple, known in advance | Complex, ad hoc |
| Queries per second | Thousands | A few |
| Rows per query | Tens | Millions |
| Size | MB to GB | GB to PB |
| Priority | Throughput, concurrency | Query response time |
| Backup | Critical — data is irreplaceable | Reloadable from sources |
| Access | Read/write | **Read-mostly** |

**Worked example.** "Add ₹450 to Asha's account" is OLTP: one row, must be
atomic, must be instant, happens ten thousand times a minute. "What was the
average transaction value per branch per quarter for the last five years?" is
OLAP: fifty million rows, runs once, and nobody minds if it takes a minute.

Running the second query on the OLTP database would lock tables and stall the
first. **That is the real reason warehouses exist** — not storage, but
isolation of workloads.

## 1.3 Architecture and components

```
   SOURCES              STAGING              WAREHOUSE            ACCESS
┌────────────┐      ┌─────────────┐      ┌──────────────┐    ┌────────────┐
│ OLTP DBs   │      │             │      │              │    │ Reporting  │
│ Flat files │─────►│  EXTRACT    │─────►│ Central      │───►│ OLAP tools │
│ ERP / CRM  │      │  TRANSFORM  │      │ warehouse    │    │ Data mining│
│ Web logs   │      │  LOAD       │      │              │    │ Dashboards │
│ External   │      │  (ETL)      │      │ ┌──────────┐ │    └────────────┘
└────────────┘      └─────────────┘      │ │Data marts│ │
                           │             │ └──────────┘ │
                           ▼             └──────────────┘
                    ┌─────────────┐             │
                    │  METADATA   │◄────────────┘
                    └─────────────┘
```

| Component | Role |
|---|---|
| **Data sources** | Operational databases, files, external feeds |
| **Staging area** | Where raw extracts land and are cleaned, before loading |
| **ETL** | Extract, Transform, Load — the pipeline that fills the warehouse |
| **Warehouse database** | The integrated, historical store |
| **Data marts** | Department-sized subsets — sales mart, finance mart |
| **Metadata repository** | Data *about* the data: sources, transformations, definitions, refresh times |
| **OLAP server** | Serves the cube — ROLAP, MOLAP or HOLAP |
| **Front-end tools** | Reporting, dashboards, ad-hoc query, mining |

### ETL

| Stage | What happens |
|---|---|
| **Extract** | Pull from each source, usually on a schedule, ideally only what changed |
| **Transform** | Clean, standardise, deduplicate, derive, aggregate, look up surrogate keys |
| **Load** | Insert into fact and dimension tables, refresh indexes and aggregates |

**Transform is where the work is.** Two systems calling the same customer
`Asha Kumari` and `KUMARI, ASHA`; one storing dates as `DD/MM/YYYY` and
another as `YYYY-MM-DD`; three definitions of "active customer". Integration
means resolving all of that *before* the data lands, because after it lands
every report inherits the mess.

### ⚠️ ETL versus ELT

Modern cloud warehouses often invert the last two steps: **ELT** loads raw
data first and transforms inside the warehouse, using its own compute. The
syllabus teaches ETL, which is correct and still ubiquitous; knowing that ELT
exists and *why* — cheap elastic compute makes it viable — is the kind of
remark that lifts an answer.

### Three-tier architecture

| Tier | Contains |
|---|---|
| **Bottom** | The warehouse database server, plus ETL and metadata |
| **Middle** | The OLAP server (ROLAP / MOLAP / HOLAP) |
| **Top** | Front-end clients — query, reporting, analysis, mining |

| OLAP server | Storage | Trade-off |
|---|---|---|
| **ROLAP** | Relational tables | Scales to huge data; slower |
| **MOLAP** | A multidimensional array (the cube) | Very fast; poor with sparse data, size-limited |
| **HOLAP** | Detail relational, summaries multidimensional | The usual compromise |

### 💡 Data warehouse versus data mart versus data lake

| | Data warehouse | Data mart | Data lake |
|---|---|---|---|
| Scope | Whole enterprise | One department | Whole enterprise |
| Data | Cleaned, structured | Cleaned, structured | **Raw**, any format |
| Schema | On **write** | On write | On **read** |
| Users | Analysts across the firm | One department | Data scientists, engineers |
| Cost and time to build | High | Low | Low to ingest, high to use |

**Schema-on-read versus schema-on-write** is the essential difference of the
lake: you dump the data now and decide what it means later. That is flexible
and it is also how a lake becomes a *swamp* — undocumented, untrusted, unused.
Warehouses are more work up front and more trustworthy afterwards.

## 1.4 Data modeling: the multidimensional model

### 🎯 The big idea

Analysts do not think in tables, they think in **measures sliced by
dimensions**: *sales* (measure) by *product*, *store* and *month*
(dimensions). The multidimensional model makes the database match that
thought.

| Term | Meaning | Example |
|---|---|---|
| **Fact** | A measurable business event | One line on one receipt |
| **Measure** | The numeric value being analysed | `quantity`, `amount` |
| **Dimension** | A perspective for slicing | Product, Store, Time, Customer |
| **Attribute** | A field of a dimension | `product.category`, `store.city` |
| **Hierarchy** | Levels within a dimension | Day → Month → Quarter → Year |
| **Granularity** | What one fact row represents | "one product on one receipt" |
| **Cube** | Facts arranged along dimensions | Sales by product × store × month |

### ⚠️ Decide the grain first

**"What does one row of the fact table mean?"** must be answered before
anything else is designed, in one sentence, and it must be the *finest* grain
you can afford. Store daily totals and you can always aggregate to monthly;
store monthly and the daily question is unanswerable forever.

Getting this wrong is the most expensive mistake in warehouse design, because
correcting it means reloading everything.

## 1.5 Fact tables and dimension tables

```sql
-- Dimension: wide, descriptive, relatively few rows
CREATE TABLE DimProduct (
  product_key   INT PRIMARY KEY,     -- SURROGATE key, not the source's SKU
  sku           VARCHAR(20),         -- the natural/business key
  product_name  VARCHAR(100),
  brand         VARCHAR(50),
  category      VARCHAR(50),
  department    VARCHAR(50)
);

-- Fact: narrow, numeric, enormous
CREATE TABLE FactSales (
  product_key  INT REFERENCES DimProduct(product_key),
  store_key    INT REFERENCES DimStore(store_key),
  date_key     INT REFERENCES DimDate(date_key),
  customer_key INT REFERENCES DimCustomer(customer_key),
  quantity     INT,                  -- measure
  amount       DECIMAL(12,2),        -- measure
  discount     DECIMAL(12,2),        -- measure
  PRIMARY KEY (product_key, store_key, date_key, customer_key)
);
```

| | Fact table | Dimension table |
|---|---|---|
| Contains | Foreign keys + **numeric measures** | Descriptive **attributes** |
| Rows | Millions to billions | Hundreds to millions |
| Columns | Few, mostly numeric | Many, mostly text |
| Growth | Constant — every event adds a row | Slow |
| Normalised? | Already narrow | **Deliberately denormalised** |
| Key | Composite of the dimension keys | A single surrogate key |

### 🔢 Types of measure

| Type | Can be summed across | Example |
|---|---|---|
| **Additive** | **All** dimensions | Sales amount, quantity |
| **Semi-additive** | Some, but **not time** | Account balance, stock on hand |
| **Non-additive** | **None** | Ratios, percentages, unit price |

**This distinction matters.** Summing Monday's and Tuesday's closing stock
gives a meaningless number — you want the *last* value, not the total. And
averaging a column of percentages is almost always wrong: to get the overall
margin you sum the profits and sum the revenues, then divide.

### Types of fact table

| Type | One row is | Example |
|---|---|---|
| **Transaction** | One event | One sale line |
| **Periodic snapshot** | A regular measurement | Daily closing balance |
| **Accumulating snapshot** | A process, updated as it progresses | An order, with dates for placed/picked/shipped/delivered |
| **Factless** | An event with no measure | A student attended a class |

A **factless fact table** records that something happened when there is
nothing to measure — attendance, a promotion being in effect. Counting rows
*is* the measure. It is a favourite two-mark question precisely because the
name sounds like a contradiction.

### 💡 Why surrogate keys

Every dimension gets a meaningless integer key of the warehouse's own, rather
than reusing the source system's identifier. Four reasons:

1. Source systems reuse and recycle their keys; the warehouse must not.
2. Two merged sources may use the same key for different things.
3. Integers join faster and index smaller than composite text keys.
4. **Slowly changing dimensions need it**: when a customer moves city, you
   insert a *new* row with a new surrogate key and an effective-date range, so
   old facts still point at the old row and history stays correct. That is a
   Type 2 SCD, and it is impossible if the key is the customer's own ID.

## 1.6 Star, snowflake and fact constellation

### 🔢 Star schema

One fact table surrounded by denormalised dimensions. Every dimension is
**one join away**.

```
              DimDate
                 │
  DimProduct ── FactSales ── DimStore
                 │
             DimCustomer
```

```sql
SELECT p.category, s.city, SUM(f.amount)
FROM   FactSales f
JOIN   DimProduct p ON p.product_key = f.product_key
JOIN   DimStore   s ON s.store_key   = f.store_key
GROUP  BY p.category, s.city;
```

### Snowflake schema

The dimensions are **normalised** into sub-dimensions, so hierarchies become
separate tables.

```
                        DimDate
                           │
DimDepartment ─ DimCategory ─ DimProduct ─ FactSales ─ DimStore ─ DimCity ─ DimState
```

```sql
SELECT c.category_name, ci.city_name, SUM(f.amount)
FROM   FactSales f
JOIN   DimProduct  p  ON p.product_key  = f.product_key
JOIN   DimCategory c  ON c.category_key = p.category_key   -- extra join
JOIN   DimStore    s  ON s.store_key    = f.store_key
JOIN   DimCity     ci ON ci.city_key    = s.city_key       -- extra join
GROUP  BY c.category_name, ci.city_name;
```

### Fact constellation (galaxy schema)

**Multiple fact tables sharing dimensions.** The shared dimensions are called
**conformed dimensions**, and they are what make cross-process analysis
possible.

```
   DimProduct ─────┬───── FactSales ───── DimStore
        │          │                         │
        └──── FactInventory ─────────────────┘
                   │
                DimDate  (shared by both)
```

With `DimProduct` and `DimDate` conformed across both facts, "how did stock
levels affect sales?" becomes answerable. Without conformed dimensions the two
marts cannot be compared at all, and you have two truths in one company.

### 🔢 The comparison

| | Star | Snowflake | Fact constellation |
|---|---|---|---|
| Fact tables | One | One | **Multiple** |
| Dimensions | Denormalised | **Normalised** | Shared (conformed) |
| Joins per query | Fewest | More | Varies |
| Query speed | **Fastest** | Slower | Depends |
| Redundancy | High | **Low** | High |
| Storage | More | Less | Most |
| Complexity | **Simplest** | Moderate | Highest |
| Maintenance | Update in many rows | Update in one place | Complex |
| Best for | Data marts, most warehouses | Very large dimensions | Enterprise warehouses |

### ⚠️ This unit contradicts Course 5, deliberately

Course 5 taught you to normalise: eliminate redundancy, avoid update
anomalies, reach 3NF. Star schemas throw that away — `DimProduct` repeats the
category name on every row of the same category, exactly the redundancy 2NF
forbids.

**It is not a mistake, and saying why earns marks.** Normalisation optimises
for *writes*: many small updates, each touching one place. A warehouse barely
writes — it loads on a schedule, then serves millions of reads. Denormalising
trades cheap storage for fewer joins, and a query with three joins beats one
with nine.

The update anomalies normalisation prevents simply do not arise, because users
never update. The load process rewrites the dimension, all rows at once.

**Storage is cheap; analyst time is not.** That single sentence is the whole
justification.

## 1.7 The OLAP cube

A **cube** arranges measures along dimensions. Three dimensions make a literal
cube; more than three is a **hypercube**, and the name persists anyway.

```
                 Product
                   ▲
                   │  ┌────┬────┬────┐
                   │ ╱    ╱    ╱    ╱│
                   │┌────┬────┬────┐ │
                   ││    │    │    │ │ ──► Time
                   │├────┼────┼────┤ │
                   ││ 45 │ 62 │ 51 │ │     each cell = a measure
                   │└────┴────┴────┘╱      e.g. sales of Product P
                   ╱                       in Store S in Month M
              Store
```

Each **cell** holds the measures for one combination of dimension members.

**Cubes are sparse.** A shop with 50,000 products, 200 stores and 1,000 days
has ten billion possible cells, but most products do not sell in most stores on
most days. Real cubes are often over 95% empty, which is exactly why MOLAP's
dense array storage struggles and ROLAP — which stores only the rows that
exist — scales better.

### Lattice of cuboids

For *n* dimensions there are **2ⁿ cuboids**, from the finest (the base cuboid,
all dimensions) to the coarsest (the apex cuboid, a single grand total).

With Product, Store and Time — n = 3, so 2³ = **8 cuboids**:

```
                 (apex: grand total)
                 /        |        \
          (Product)    (Store)    (Time)
            /    \      /    \     /   \
   (Product,Store) (Product,Time) (Store,Time)
                 \        |        /
              (Product, Store, Time)   ← base cuboid
```

Pre-computing all 2ⁿ cuboids makes every query instant and is usually
impossible — with 10 dimensions that is 1,024 cuboids, and with hierarchies
far more. Choosing **which** to materialise is the central engineering problem
of cube design.

## 1.8 OLAP operations

Five operations. Each is a guaranteed exam question, and each is easiest to
learn with a concrete before-and-after.

### 🔢 The five operations

| Operation | Effect | Direction |
|---|---|---|
| **Roll-up** | Aggregate — climb a hierarchy, or drop a dimension | Less detail |
| **Drill-down** | The reverse — descend a hierarchy, or add one | More detail |
| **Slice** | Fix **one** dimension to a single value | One dimension fewer |
| **Dice** | Restrict **several** dimensions to ranges | A sub-cube |
| **Pivot (rotate)** | Turn the cube — swap the axes | Same data, new view |

**Roll-up.** Sales by *city* → sales by *state*. You have climbed the location
hierarchy, and the number of rows fell.

```sql
-- from
SELECT city,  SUM(amount) FROM ... GROUP BY city;
-- to
SELECT state, SUM(amount) FROM ... GROUP BY state;
```

**Drill-down.** Sales by *quarter* → sales by *month*. More rows, more detail.
This is what happens when a manager clicks a bar on a dashboard.

**Slice.** Take the whole cube and fix `Time = Q1-2026`. A three-dimensional
cube becomes a two-dimensional table of Product × Store.

```sql
SELECT product, store, SUM(amount) FROM ... WHERE quarter = 'Q1-2026' GROUP BY product, store;
```

**Dice.** Restrict *several* dimensions at once — `Product ∈ {Dairy, Bakery}`
**and** `Store ∈ {Vijayawada, Guntur}` **and** `Time ∈ {Q1, Q2}`. A smaller
cube of the same dimensionality.

**Pivot.** Rows become columns: a table of *months down, products across*
becomes *products down, months across*. No aggregation, no filtering — the
same numbers, rearranged. It is what a spreadsheet PivotTable does, hence the
name.

### ⚠️ Slice versus dice

The distinction is examined constantly and is exactly this:

| | Slice | Dice |
|---|---|---|
| Dimensions constrained | **One** | **Two or more** |
| Value(s) | A **single** member | Ranges or sets |
| Result | A cube of *n − 1* dimensions | A **sub-cube** of *n* dimensions |
| SQL analogy | `WHERE d = 'x'` | `WHERE d1 IN (…) AND d2 IN (…)` |

Slice reduces the dimensionality; dice reduces the size but keeps the shape.

### Other operations

- **Drill-across** — query two fact tables through their conformed dimensions
  (this needs a constellation schema).
- **Drill-through** — go past the cube to the underlying detail rows.

### SQL's cube extensions

```sql
SELECT category, city, SUM(amount)
FROM   sales
GROUP  BY ROLLUP (category, city);      -- subtotals per category + grand total

SELECT category, city, SUM(amount)
FROM   sales
GROUP  BY CUBE (category, city);        -- ALL 2^2 = 4 combinations
```

`ROLLUP(a, b)` gives the hierarchy `(a,b)`, `(a)`, `()` — 3 groupings.
`CUBE(a, b)` gives all four: `(a,b)`, `(a)`, `(b)`, `()`. For *n* columns,
`ROLLUP` produces *n + 1* groupings and `CUBE` produces 2ⁿ.

---

## Practice problems

### Problem 1

A university wants to analyse examination results. Design a star schema. State
the grain in one sentence, name the fact table's measures, and give one
attribute hierarchy per dimension.

**Solution.**

**Grain:** one row per *student, per subject, per examination session*.

```sql
CREATE TABLE DimStudent (
  student_key INT PRIMARY KEY, roll_no VARCHAR(15),
  name VARCHAR(80), gender CHAR(1), category VARCHAR(20),
  programme VARCHAR(40), department VARCHAR(40), faculty VARCHAR(40));

CREATE TABLE DimSubject (
  subject_key INT PRIMARY KEY, subject_code VARCHAR(12),
  subject_name VARCHAR(80), credits INT,
  course_number INT, semester INT, year INT);

CREATE TABLE DimTime (
  time_key INT PRIMARY KEY, exam_date DATE,
  session VARCHAR(20), month VARCHAR(12), quarter CHAR(2), academic_year VARCHAR(9));

CREATE TABLE DimFaculty (
  faculty_key INT PRIMARY KEY, staff_id VARCHAR(12),
  name VARCHAR(80), designation VARCHAR(30), department VARCHAR(40));

CREATE TABLE FactResult (
  student_key INT, subject_key INT, time_key INT, faculty_key INT,
  marks_internal INT,          -- additive
  marks_external INT,          -- additive
  marks_total    INT,          -- additive
  credits_earned INT,          -- additive
  attendance_pct DECIMAL(5,2), -- NON-additive: never SUM this
  PRIMARY KEY (student_key, subject_key, time_key));
```

**Hierarchies:**

| Dimension | Hierarchy |
|---|---|
| Student | Faculty → Department → Programme → Student |
| Subject | Year → Semester → Subject |
| Time | Academic year → Quarter → Month → Date |
| Faculty | Department → Designation → Staff |

**The two points that earn the marks.** `attendance_pct` is
**non-additive** — the department's attendance is not the sum of its students'
percentages, it is total classes attended over total classes held, so the
*counts* should be stored instead. And the grain is stated per *subject*, not
per student: storing one row per student per session would make "how did
students do in Statistics?" unanswerable.

### Problem 2

Given a cube with dimensions Product (Item → Category → Department), Location
(City → State → Country) and Time (Day → Month → Quarter → Year), name the
OLAP operation for each and write the SQL sketch.

(a) Sales by city → sales by country
(b) Sales for Q1 only, across all products and locations
(c) Sales of Dairy and Bakery, in Andhra Pradesh and Telangana, in Q1 and Q2
(d) Sales by year → sales by quarter
(e) A table of months-down-by-product-across becomes product-down-by-month-across

**Solution.**

| | Operation | Why |
|---|---|---|
| (a) | **Roll-up** | Climbing the Location hierarchy — City → State → Country |
| (b) | **Slice** | **One** dimension fixed to a **single** value |
| (c) | **Dice** | **Three** dimensions restricted to **sets** |
| (d) | **Drill-down** | Descending Time — Year → Quarter |
| (e) | **Pivot** | Axes exchanged; no aggregation and no filtering |

```sql
-- (a) roll-up
SELECT country, SUM(amount) FROM sales_cube GROUP BY country;

-- (b) slice
SELECT product, city, SUM(amount) FROM sales_cube
WHERE quarter = 'Q1' GROUP BY product, city;

-- (c) dice
SELECT product, state, quarter, SUM(amount) FROM sales_cube
WHERE category IN ('Dairy','Bakery')
  AND state    IN ('Andhra Pradesh','Telangana')
  AND quarter  IN ('Q1','Q2')
GROUP BY product, state, quarter;

-- (d) drill-down
SELECT year, quarter, SUM(amount) FROM sales_cube GROUP BY year, quarter;

-- (e) pivot -- no aggregation change, presentation only
SELECT * FROM (SELECT month, product, amount FROM sales_cube)
PIVOT (SUM(amount) FOR month IN ('Jan','Feb','Mar'));
```

### Problem 3

A retailer's cube has 4 dimensions. (a) How many cuboids? (b) If Time has
levels Day → Month → Quarter → Year and the others have 3 levels each, is 2ⁿ
still the answer? (c) Why not materialise them all?

**Solution.**

**(a)** 2⁴ = **16 cuboids**, from the base cuboid (all four dimensions) to the
apex (a single grand total).

**(b) No.** 2ⁿ counts only which dimensions are *present*. With hierarchies,
each dimension can be aggregated to any of its levels, so the count is the
**product of (levels + 1)** — the +1 being "dimension absent entirely":

```
Time: 4 levels → 5 choices
Three others: 3 levels each → 4 choices each
Total = 5 × 4 × 4 × 4 = 320 cuboids
```

**(c)** Storage and refresh time. 320 cuboids over a large fact table can
exceed the size of the raw data many times over, and **every one must be
recomputed on every load** — so a nightly ETL that took an hour now takes six.
The engineering answer is **partial materialisation**: pre-compute the cuboids
that are queried often or that many others can be derived from, and compute the
rest on demand.

---

## Exam questions from this unit

**Two marks**

1. Define a data warehouse (Inmon's definition).
2. What does "non-volatile" mean for a data warehouse?
3. Distinguish OLTP from OLAP.
4. Distinguish a fact table from a dimension table.
5. Distinguish slice from dice.
6. What is a factless fact table?
7. What is granularity, and why fix it first?
8. What is a conformed dimension?
9. Distinguish additive, semi-additive and non-additive measures.
10. How many cuboids does an n-dimensional cube have?

**Five marks**

1. Explain the four characteristics of a data warehouse.
2. Explain the three-tier data warehouse architecture with a diagram.
3. Explain ETL with an example of each stage.
4. Explain the five OLAP operations with examples.
5. Compare star and snowflake schemas.
6. Explain ROLAP, MOLAP and HOLAP.
7. Explain data warehouse, data mart and data lake.

**Ten marks**

1. Design a star schema for a given business case, state the grain, and
   explain every table and key decision.
2. Explain star, snowflake and fact constellation schemas exhaustively, with
   diagrams and a comparison.
3. Explain the data warehouse architecture and all OLAP operations with a
   worked cube.

## Mistakes that cost marks

- Saying a warehouse is "just a big database"
- Reading "non-volatile" as "never changes" — it means users do not update it
- Claiming warehouses are normalised — they are deliberately **de**normalised
- Confusing slice (one dimension, one value) with dice (several, ranges)
- Putting descriptive text in the fact table, or measures in a dimension
- Summing a semi-additive measure across time, or averaging percentages
- Reusing the source system's key instead of a surrogate key
- Confusing a data mart (departmental subset) with a data lake (raw store)
- Designing the schema before deciding the grain
- Saying a fact constellation has one fact table — it has several
