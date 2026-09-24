# Unit 1 — Introduction to Business Intelligence and Decision Support Systems

**Syllabus topics:** Business Intelligence — definition, scope and
evolution; Business Intelligence vs. Data Analytics vs. Data Science; BI
lifecycle; applications of BI in functional domains — finance, HR, marketing,
retail, education, healthcare, etc.; BI maturity models and organizational
readiness to BI adoption. Decision Support Systems (DSS) — concepts,
components and architecture. BI tools overview — Power BI, Tableau and other
tools; comparison and suitability of BI tools. Case study — a retail chain's
BI strategy to optimize inventory.

> The syllabus prints "Business IntelligenceI vs. Data Analytics vs. Data
> Science" — a stray capital `I` has attached itself to the term. Cosmetic, and
> recorded in [SYLLABUS-REVIEW.md](../../../SYLLABUS-REVIEW.md) with the other
> Semester V text defects.

---

## 1.1 What Business Intelligence is

### 🎯 The big idea

**BI turns the data a business already has into decisions it would not
otherwise have made.**

Every part of that sentence is load-bearing:

- **already has** — BI works on internal, historical, operational data. Sales
  records, HR records, stock movements. Not surveys, not experiments.
- **decisions** — not insights, not reports. If nobody acts differently, the
  dashboard failed, however pretty it is.
- **would not otherwise have made** — the value is the *change*, and that is
  what a BI project is judged on.

### The definition to write in the exam

> **Business Intelligence is the set of technologies, processes and practices
> that collect, integrate, analyse and present an organisation's data in order
> to support better and faster business decisions.**

Turban's phrasing, which the textbook uses, is worth knowing too: BI is an
**umbrella term** covering architectures, tools, databases, analytical tools,
applications and methodologies — the point being that BI is not one product.

### Scope — what is in and what is out

| In scope | Out of scope |
|---|---|
| Historical and current internal data | Primary research and experiments |
| Descriptive and diagnostic questions — *what happened, why* | Deep predictive modelling (that is Course 12 A) |
| Repeatable reporting and dashboards | One-off exploratory analysis |
| Data integration, ETL, warehousing | Real-time transaction processing (that is Course 5) |
| Self-service access for non-technical users | Anything needing code to read |

### 📖 Where it came from

The evolution matters because the exam asks for it, and because each stage
solved the previous stage's failure.

| Era | What existed | Why it changed |
|---|---|---|
| **1960s–70s** | Decision Support Systems; management information systems producing fixed printed reports | Reports took weeks; changing one meant a request to IT |
| **1980s** | Executive Information Systems; the term *Business Intelligence* revived by **Howard Dresner of Gartner in 1989** | EIS served only the top of the organisation |
| **1990s** | **Data warehousing** — Inmon's enterprise warehouse, **Kimball's dimensional model (1996)**, OLAP cubes | The model stabilised; the tools stayed expensive and IT-owned |
| **2000s** | Enterprise BI suites — Cognos, Business Objects, MicroStrategy | Licences and specialists made every question a project |
| **2010s** | **Self-service BI** — Tableau, Power BI, Qlik. The analyst builds their own report | This is where the course lives |
| **2020s** | Cloud-native BI, augmented analytics, natural-language query | Semantic layers and governance become the hard part again |

**The one-sentence summary of fifty years:** *the reporting moved steadily away
from IT and towards the person who has the question.* Self-service BI is the
end point of that trend, and the governance problems in Unit 4 §4.6 are its
direct cost.

---

## 1.2 BI vs. Data Analytics vs. Data Science

### ⚠️ This is the most-asked question in the course

It is Outcome 1, it is Activity 1, and it appears on the paper nearly every
year. Answer it with a table and a worked example, not a paragraph.

### 🔢 The comparison

| | **Business Intelligence** | **Data Analytics** | **Data Science** |
|---|---|---|---|
| **Question** | *What happened?* | *Why did it happen?* | *What will happen, and what should we do?* |
| **Analytics type** | Descriptive | Descriptive + **diagnostic** | **Predictive + prescriptive** |
| **Time direction** | **Backward** | Backward, seeking cause | **Forward** |
| **Data** | Structured, internal, warehoused | Structured, some external | **Any** — structured, text, image, streaming |
| **Method** | Aggregation, slicing, drill-down | Statistical testing, segmentation, cohort analysis | Machine learning, statistical modelling |
| **Tools** | Power BI, Tableau, SQL | SQL, Excel, Python, R | Python, R, scikit-learn, TensorFlow |
| **Output** | Dashboards, scheduled reports, KPIs | An analysis answering a question | A **model** that keeps producing answers |
| **Audience** | Managers and executives | Analysts and managers | Product, engineering, and the business |
| **Repeats?** | **Yes — the same view daily** | Usually once per question | The model runs continuously |
| **Skills** | Modelling, visualisation, domain | Statistics, SQL, domain | Programming, mathematics, ML |

### 💡 One dataset, three jobs

Take a retail chain's sales table. The distinction becomes obvious:

| Discipline | The actual question | The actual answer |
|---|---|---|
| **BI** | "What were sales by region last quarter?" | A dashboard: South ₹4.2 crore, up 8% on Q3, with a regional map and a trend line |
| **Data analytics** | "Why did South grow 8% while North fell 3%?" | An analysis: South's growth is almost entirely one product line after a price cut; North lost two large accounts |
| **Data science** | "Which customers will churn next quarter, and what should we offer them?" | A model scoring every customer weekly, plus an uplift estimate per offer |

**Say this out loud in the viva.** One dataset, three questions, three
deliverables — that shows you understand the distinction rather than having
memorised a table.

### 💡 The relationship, not just the difference

They are not rivals; they are a sequence, and a good answer says so:

```
      BI                Data Analytics          Data Science
  what happened   →      why it happened    →   what happens next
  (the baseline)        (the explanation)       (the prediction)
       │                                              │
       └──────── the same warehouse feeds both ───────┘
```

**BI is usually the prerequisite.** A data science team with no reliable
definition of "revenue" will build a model on a number nobody trusts. The
semantic layer BI builds — one agreed definition of each measure — is what
makes the later work possible. That point is worth a mark on its own.

---

## 1.3 The BI lifecycle

### 🎯 The big idea

**A BI project is a loop, not a line.** The last stage feeds the first, and a
project that stops after "deploy" is a project that gets abandoned.

### 🔢 The stages

```
   1. Business          2. Data              3. Data
      requirements  →      identification →     integration (ETL)
           ↑                                          │
           │                                          ▼
   6. Monitor and       5. Reporting and       4. Data
      improve       ←      visualization   ←      storage & modelling
```

| # | Stage | What happens | Where it goes wrong |
|:---:|---|---|---|
| 1 | **Business requirements** | Identify the decision, the decision-maker, and the KPI | Asking "what data do you have?" instead of "what will you do differently?" |
| 2 | **Data identification** | Find the sources — ERP, CRM, spreadsheets, APIs | Discovering halfway that the key field does not exist |
| 3 | **Data integration (ETL)** | Extract, transform, load; clean and conform | **Usually 60–80% of the effort.** Always underestimated |
| 4 | **Storage and modelling** | Warehouse or mart; build the **star schema** | Loading raw operational tables and calling it a model — Unit 4 |
| 5 | **Reporting and visualization** | Dashboards, reports, self-service datasets | Charting everything available rather than what is needed |
| 6 | **Monitor and improve** | Usage tracking, feedback, new requirements | Skipping it, so nobody notices the dashboard went stale |

### ⚠️ Stage 1 is the one that decides whether the project succeeds

**Start from the decision, not the data.** The test for a good requirement is:
*"When this number moves, who does what?"* If nobody can answer, the dashboard
will be built, admired once, and never opened again.

That is not a soft point — it is the most common cause of BI project failure,
and it is a legitimate five-mark answer.

---

## 1.4 Applications of BI across functional domains

The syllabus names six domains and expects an example from each. Learn one
concrete KPI per domain rather than vague phrases.

| Domain | What BI is used for | A KPI you can name |
|---|---|---|
| **Finance** | Budget vs. actual, cash flow, profitability by product, cost centre analysis, fraud flags | **Gross margin %**, working-capital days |
| **HR** | Headcount, attrition, recruitment funnel, absenteeism, training completion, diversity | **Attrition rate** = leavers ÷ average headcount |
| **Marketing** | Campaign ROI, channel attribution, funnel conversion, customer acquisition cost | **CAC** and **ROAS** (return on ad spend) |
| **Retail** | Sales by store and SKU, stock cover, shrinkage, basket analysis, footfall conversion | **Stock turnover** = COGS ÷ average inventory |
| **Education** | Enrolment and retention, pass rates, subject-wise performance, placement statistics | **Pass rate**, student–staff ratio |
| **Healthcare** | Bed occupancy, average length of stay, readmission, waiting times, clinical outcomes | **Readmission rate within 30 days** |

### 💡 Two of these are lab experiments

Experiment 5 is the **education** case — a student performance dataset — and
experiment 9 is the **HR** case, employee turnover. Both appear again as case
studies in Units 2 and 3. They are the two domains to know in detail.

---

## 1.5 BI maturity models and organizational readiness

### 🎯 The big idea

**Maturity models exist because buying the tool is the easy part.** An
organisation that cannot agree what "customer" means will not be rescued by
Power BI, and a maturity model is how you say that to management politely.

### 🔢 The five levels

Several models exist — Gartner's, TDWI's, the BI Maturity Model of Eckerson.
They differ in naming; the shape is the same, and any of them earns the mark.

| Level | Name | What it looks like | What people say |
|:---:|---|---|---|
| 1 | **Initial / Ad hoc** | Spreadsheets on individual laptops; no single source | "Whose number is right?" |
| 2 | **Repeatable / Basic** | Standard reports from IT; still backward-looking | "I'll raise a ticket for that report" |
| 3 | **Defined / Managed** | A warehouse exists; dashboards are shared; definitions agreed | "That's on the sales dashboard" |
| 4 | **Managed / Advanced** | Self-service with governance; KPIs tied to strategy | "Let me slice that myself" |
| 5 | **Optimized / Innovative** | Predictive and prescriptive; BI embedded in operations | "The system already reordered it" |

**The most common real-world state is level 1 or 2**, and the most common
failure is buying level-5 tooling for a level-1 organisation.

### Organizational readiness — what to assess before starting

| Dimension | The question to ask | A bad sign |
|---|---|---|
| **Sponsorship** | Is there an executive who wants this and will decide? | The project is owned by IT alone |
| **Data quality** | Is the source data complete, accurate and timely? | Key fields are free text |
| **Data culture** | Do people currently decide with evidence? | Decisions are made and then justified |
| **Skills** | Can anyone model data, not just build charts? | Everyone is a chart builder |
| **Governance** | Is there one agreed definition of each measure? | Three departments report three revenue figures |
| **Infrastructure** | Can the data get out of the source systems? | The ERP has no export and no API |

### 💡 The honest summary

**Technology is rarely the constraint.** The gap between level 2 and level 3 is
almost entirely organisational — agreeing definitions, assigning ownership, and
getting people to use one number. Say that in the exam and you are answering
the question the model was designed to raise.

---

## 1.6 Decision Support Systems

### 🎯 The big idea

**A DSS is an interactive computer system that helps a manager use data and
models to make a decision that is not fully structured.**

The phrase *not fully structured* is the whole point. A payroll system handles
a **structured** decision — the rules are known, so automate it. Choosing which
warehouse to build is **unstructured** — judgement is required, and no system
should make it for you. A DSS serves the **semi-structured** middle: it does
the arithmetic and the what-if, and leaves the judgement to the human.

### 🔢 The classification of decisions — Simon's framework

| Type | Rules known? | Example | Right response |
|---|---|---|---|
| **Structured** | Fully | Reorder when stock < 20 | **Automate it** |
| **Semi-structured** | Partly | Setting next quarter's price | **A DSS** |
| **Unstructured** | No | Entering a new country | Judgement, informed by data |

### 🔢 The four components of a DSS

This is a standard diagram question. Learn the four boxes and the arrows.

```
                    ┌─────────────────────┐
                    │   User Interface    │  ← the manager
                    │  (Dialogue mgmt)    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │  Data        │ │  Model       │ │  Knowledge   │
      │  Management  │ │  Management  │ │  Management  │
      │  (the DBMS)  │ │  (the MBMS)  │ │  (optional)  │
      └──────────────┘ └──────────────┘ └──────────────┘
```

| Component | Holds | Example |
|---|---|---|
| **Data management** | The database and its DBMS; internal, external and personal data | Sales history, market data |
| **Model management** | The **MBMS** — statistical, financial, optimisation and simulation models | A forecasting model, a linear program |
| **User interface** | Dialogue management — how the manager asks and sees | The dashboard, the what-if panel |
| **Knowledge management** | Rules and expertise; makes it an *intelligent* DSS | "Never reorder below the supplier's minimum" |

**The knowledge component is optional** — a DSS with one is sometimes called an
**intelligent DSS** or **expert support system**, which is where this course
touches Course 13 A's expert systems.

### 🔢 DSS versus BI — the comparison that gets asked

| | **DSS** (1970s–80s) | **BI** (1990s–) |
|---|---|---|
| Focus | **Models** — what-if, optimisation, simulation | **Data** — aggregation and reporting |
| Users | A few managers, often one decision | Many users across the organisation |
| Data volume | Small, often hand-loaded | Large, warehoused, automated |
| Question | "What if I change this?" | "What is happening?" |
| Built | Per decision, often bespoke | As a platform, reused |

**BI absorbed DSS rather than replacing it.** A modern BI tool's what-if
parameter (Unit 5) *is* a DSS model component, and a Power BI report with a
scenario slider is a small DSS. Saying that connects the two halves of this
unit and is worth the mark.

---

## 1.7 BI tools overview and comparison

### 🔢 Power BI vs. Tableau — the comparison to learn

Units 2 and 3 cover each tool in detail; this is the side-by-side the exam
wants, and experiment 1 is exactly this comparison.

| | **Power BI** | **Tableau** |
|---|---|---|
| **Vendor** | Microsoft | Salesforce (acquired 2019) |
| **Cost** | **Lower.** Desktop free; Pro per-user | Higher; Public is free but everything is published publicly |
| **Desktop OS** | **Windows only** | Windows and macOS |
| **Learning curve** | Gentler if you know Excel | Gentler for pure visual exploration |
| **Strongest at** | **Data modelling and DAX**; Microsoft integration | **Visual analytics** — fastest path from question to chart |
| **Calculation language** | **DAX** (plus M in Power Query) | **Calculated fields** and **LOD expressions** |
| **Data prep** | **Power Query** — genuinely strong, reusable steps | Built-in prep, plus Tableau Prep as a separate tool |
| **Ecosystem** | Excel, Azure, SQL Server, Teams | Broad connectors; strong server story |
| **Governance** | Mature — workspaces, sensitivity labels | Mature at the server tier |
| **Best when** | You are a Microsoft shop and the model is complex | Exploration and presentation quality matter most |

### 💡 Suitability — choosing between them, and the answer that earns marks

**"It depends on the organisation, not the feature list."** Then give criteria:

1. **Existing stack.** Microsoft 365 and Azure make Power BI the default; it
   is cheaper and it already knows how to log people in.
2. **Cost at scale.** Power BI Pro per user is materially cheaper than Tableau
   Creator, and it decides most large deployments.
3. **Who builds the reports.** Business users with Excel habits → Power BI.
   Dedicated analysts who explore → Tableau.
4. **Model complexity.** Many tables and complex measures → Power BI and DAX.
5. **macOS.** Power BI Desktop does not run on it. This decides more
   evaluations than anyone admits.

**The tools have converged.** Anything either can do, the other can now mostly
do too. Say so — the differences that matter are cost, ecosystem and the people
who will use it.

**Suitability by scenario**, which is how the question is usually phrased:

| Scenario | Suitable tool | Because |
|---|---|---|
| A Microsoft 365 organisation, many report consumers | **Power BI** | Cost per user, and single sign-on already works |
| A complex model — many tables, hard measures | **Power BI** | DAX and the modelling layer are stronger |
| Analysts exploring data to find questions | **Tableau** | Fastest path from question to chart |
| Presentation and publication quality matter most | **Tableau** | Better defaults, and the Story object |
| The team is on macOS | **Tableau** | Power BI Desktop does not run on it |
| A student project with no budget | **Tableau Public** or **Power BI Desktop** | Both free — but Public publishes to the open web |
| Regulated data needing row-level security | **Power BI** | RLS is mature and per-user |

### Other tools worth naming

| Tool | Note |
|---|---|
| **Qlik Sense** | Associative in-memory engine; strong at exploration |
| **Looker** (Google) | **Code-first semantic layer** (LookML) — governance by design |
| **Google Data Studio / Looker Studio** | Free, web-based, weak modelling |
| **Apache Superset** | Open source, SQL-first, self-hosted |
| **MicroStrategy, Cognos, SAP BO** | The enterprise generation; still very widely deployed |
| **Excel** | Still the most-used BI tool on earth. Course 1 was not a detour |

---

## 1.8 Case study — a retail chain's BI strategy to optimize inventory

The syllabus sets this case at the end of Unit 1, and it is a good ten-mark
answer because it exercises every section above.

**The situation.** A chain of 120 stores. Stockouts on fast movers lose sales;
overstock on slow movers ties up cash and ends in markdowns. Head office sees
sales weekly, in a spreadsheet, three days late.

**Applying the lifecycle:**

| Stage | What it means here |
|---|---|
| 1. Requirements | The decision is **what to reorder, per store, per week**. Owner: the category manager. KPIs: stock cover in days, stockout rate, inventory turnover, markdown % |
| 2. Data identification | POS transactions, stock on hand, purchase orders, supplier lead times, the promotions calendar |
| 3. Integration | Nightly ETL; conform product codes across a legacy chain acquired two years ago — **this is where the effort goes** |
| 4. Modelling | Star schema: **fact = daily sales by store and SKU**; dimensions = Product, Store, Date, Supplier |
| 5. Visualization | A stock-cover dashboard, filtered by store and category, with drill-down to SKU and a stockout exception list |
| 6. Monitor | Track stockout rate weekly; check whether category managers actually open it |

**The measures that matter:**

| KPI | Formula | Reads as |
|---|---|---|
| **Stock cover (days)** | on-hand ÷ average daily sales | "We have 11 days left" |
| **Inventory turnover** | COGS ÷ average inventory | Higher = leaner |
| **Stockout rate** | SKU-days out of stock ÷ SKU-days | Lost sales |
| **Markdown %** | markdown value ÷ gross sales | Over-ordering, after the fact |

### ⚠️ The trap in this case, and it is a real one

**Stockout rate and inventory turnover pull in opposite directions.** Drive
turnover up hard enough and you will run out of stock; eliminate stockouts and
you will hold too much. A dashboard showing only one of them will optimise the
business into the other's failure.

**Always show the pair.** That observation — that KPIs must be balanced, not
maximised individually — is the point of the case study and is worth stating
whichever BI case the exam sets.

---

## Practice problems

### Problem 1

Distinguish Business Intelligence, Data Analytics and Data Science. Illustrate
with a single dataset. *(10 marks)*

**Solution.**

Open with the one-line distinction: **BI reports what happened, analytics
explains why, data science predicts what happens next.** Then the table from
§1.2 — question, analytics type, time direction, data, methods, tools, output,
audience.

Then the worked illustration, which is what separates a 6 from a 9. Using a
retail sales table:

- **BI:** "Sales by region, last quarter" → a dashboard, South ₹4.2 crore,
  +8% QoQ, refreshed nightly, opened by regional managers every Monday.
- **Analytics:** "Why did South grow 8% and North fall 3%?" → a one-off
  analysis; South's growth traces to one product line after a price cut, North
  lost two large accounts. Answers *why*.
- **Data science:** "Which customers churn next quarter, and what offer
  retains them?" → a model scoring every customer weekly, with an uplift
  estimate per offer.

Close with the relationship: they are a **sequence over the same warehouse**,
not competitors, and BI's agreed definitions are what make the other two
trustworthy.

### Problem 2

Explain the BI lifecycle. At which stage do most BI projects fail, and why?
*(10 marks)*

**Solution.**

Draw the six-stage loop from §1.3 and describe each stage in a sentence, with
the loop from stage 6 back to stage 1 drawn explicitly — a BI system is
maintained, not delivered.

**Where they fail: stage 1, requirements.** Two reasons, and give both:

1. **The wrong question is asked.** Teams start from "what data do we have?"
   rather than "what decision will change?" The result is a technically correct
   dashboard nobody uses. The test is *"when this number moves, who does
   what?"* — if nobody can answer, do not build it.
2. **Stage 3 is where the effort actually goes** — ETL and data quality are
   60–80% of the work and are routinely estimated at 20%. So the project also
   fails on schedule, even when the requirement was right.

Add the honest note: failures are attributed to tools and blamed on stage 5,
because that is the stage people can see.

### Problem 3

What is a Decision Support System? Draw its architecture and distinguish it
from BI. *(10 marks)*

**Solution.**

**Definition:** an interactive computer-based system that helps managers use
data and models to solve **semi-structured** problems — decisions where the
rules are partly known, so the system does the arithmetic and the human keeps
the judgement.

Give Simon's three decision types (structured → automate; semi-structured → a
DSS; unstructured → judgement) since it justifies why a DSS exists at all.

Draw the four components from §1.6 — user interface (dialogue management) on
top, and data management, model management (the MBMS) and optional knowledge
management beneath — and name what each holds.

Then the DSS-vs-BI table: **DSS is model-centric, few users, per-decision;
BI is data-centric, many users, a platform.** Finish with the point that BI
absorbed DSS rather than replacing it, and that a what-if parameter in a Power
BI report is a model component — a small DSS inside a BI tool.

---

## Exam questions from this unit

**Two marks**

1. Define Business Intelligence.
2. What does DSS stand for, and what kind of decision does it support?
3. Name the four components of a DSS.
4. Who coined the modern term "Business Intelligence", and when?
5. Name any four BI tools.
6. What is a BI maturity model?

**Five marks**

1. Explain the evolution of Business Intelligence.
2. Describe the stages of the BI lifecycle.
3. Explain the components of a DSS with a diagram.
4. Compare Power BI and Tableau.
5. Explain BI applications in any four functional domains with a KPI for each.
6. What is organizational readiness for BI, and how is it assessed?

**Ten marks**

1. Distinguish BI, Data Analytics and Data Science with an example dataset.
2. Explain the BI lifecycle and identify where projects fail, and why.
3. Explain DSS architecture and distinguish DSS from BI.
4. Describe a BI maturity model and explain what moves an organisation between
   levels.
5. Case study: design a BI strategy for a retail chain optimising inventory.

---

## Mistakes that cost marks

- **Defining BI as "making charts".** BI is the whole pipeline from source data
  to decision. Visualisation is the last stage and the smallest one.
- **Saying data science is "advanced BI".** Different question, different
  direction in time, different output. They are not on one scale.
- **Listing lifecycle stages without the loop.** Stage 6 feeds stage 1. A
  lifecycle drawn as a straight line is missing the point of the word.
- **Giving DSS three components.** Four — and the fourth, knowledge
  management, is the optional one. Do not drop the user interface, which is the
  one people forget.
- **Claiming a DSS makes the decision.** It **supports** it. That word is in
  the name and examiners look for it.
- **Comparing Power BI and Tableau on features alone.** They have converged.
  The real criteria are cost, existing stack, who builds reports, and macOS.
- **Naming domains with no KPI.** "BI is used in HR" earns nothing; "attrition
  rate = leavers ÷ average headcount" earns the mark.
- **Treating maturity as a technology problem.** Levels 2→3 is about agreeing
  definitions and assigning ownership, not about buying a better tool.
