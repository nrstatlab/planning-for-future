# Course 11 — Business Intelligence Tools

**Semester V**

**This is the one Semester V course everyone takes.** Courses 12 and 13 fork
into Track A and Track B; this one does not.

---

## The one thing to understand before anything else

**BI is not analytics with nicer charts. It is a different job.**

Course 9 taught you to answer a question nobody had asked before. BI is about
answering the *same* question every Monday morning, for someone who will not
write code, fast enough that they act on it in the meeting.

That constraint drives every design decision in this course — why the data is
modelled as a star, why measures are pre-aggregated, why a dashboard shows six
numbers and not sixty.

| | Data science (Course 9) | Business intelligence (here) |
|---|---|---|
| Question | New each time, often exploratory | **Known in advance**, asked repeatedly |
| Audience | You, and other analysts | **A manager who will not write code** |
| Output | A notebook, a model, a finding | **A dashboard someone opens unprompted** |
| Time frame | Mostly the past *and* a prediction | Mostly **what happened, and how it is trending** |
| Success | The finding is correct and new | **A decision changed** |
| Data shape | Whatever you were given | A deliberately modelled **star schema** |

**The exam's favourite question is the first row of that table.** "Differentiate
BI, Data Analytics and Data Science" is Outcome 1, Activity 1, and a near
certainty on the paper. §1.2 answers it properly.

## Where it sits in the degree

You have met more of this course than you think.

| From | You have | Used here |
|---|---|---|
| **Course 1** | Excel, pivot tables, slicers, dashboards, VLOOKUP | Power BI *is* those ideas at scale. A pivot table is a `$group`; a slicer is a slicer |
| **Course 8, Unit 1** | Star and snowflake schemas, fact and dimension tables, OLAP cubes | **Unit 4 here is that unit again.** See §4.1 — do not study it twice |
| **Course 5** | SQL joins, cardinality, keys | Tableau's joins are SQL joins; Power BI relationships are joins declared once instead of written each time |
| **Course 9** | pandas, matplotlib, Seaborn, Plotly | Power Query is `pandas` with a mouse. Every transformation here has a one-line pandas equivalent, and the labs give it |
| **Course 4** | Aggregation, distributions, correlation | What the measures actually *mean*, and why an average of averages is wrong |

**If you did Course 1 Unit 5 properly, you already know what a dashboard is
for.** The new material is the modelling in Unit 4 and the tooling in Units 2–3.

## Course objectives (verbatim)

1. Introduce foundational concepts of Business Intelligence (BI) and Decision
   Support Systems (DSS), including their scope, evolution, and organizational
   relevance.
2. Familiarize students with leading BI tools such as Power BI and Tableau,
   highlighting their ecosystems, interfaces, and comparative strengths.
3. Develop skills in data preparation and transformation, using Power Query and
4. Enable effective data visualization and storytelling, leveraging charts,
   dashboards, and advanced features to communicate insights.
5. Equip learners with data modeling techniques, including dimensional
   modeling, relationships, joins, and governance principles for robust BI
   solutions.

> **Objective 3 is printed exactly as shown.** It stops at "using Power Query
> and" — the sentence runs straight into objective 4 with its ending missing.
> From Unit 3 and Outcome 2 it was presumably "…using Power Query and
> Tableau's data preparation features." Recorded as a finding in
> [SYLLABUS-REVIEW.md](../../../SYLLABUS-REVIEW.md).

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | BI concepts and Decision Support Systems | [unit-1.md](unit-1.md) | Easy | 3 |
| 2 | Power BI — preparation and visualization | [unit-2.md](unit-2.md) | Moderate | 3 |
| 3 | Tableau — preparation, visualization, storytelling | [unit-3.md](unit-3.md) | Moderate | 3 |
| 4 | Data modeling and relationships | [unit-4.md](unit-4.md) | **Hard** | 3 |
| 5 | Dashboard design and business insights | [unit-5.md](unit-5.md) | Moderate | 3 |

**Unit 4 is the hard one and the one that earns marks.** Units 2, 3 and 5 are
largely tool operation — genuinely useful, quickly learned, and worth fewer
marks than the time they take. Unit 4 is where the thinking is, and where a
wrong answer produces a dashboard that is confidently, silently incorrect.

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 15 experiments
- `labs/course-11-bi/` — code
- `data/course-11-bi/` — **practice datasets**, CSV: `dim-date.csv`, `dim-product.csv`, `dim-store.csv`, `fact-sales.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.
  Also `sales-transactions.csv` in `data/shared/`, which several courses
  analyse so their answers can be compared.

> **On the lab code.** Power BI Desktop is Windows-only and Tableau Desktop is
> proprietary; neither can be installed in the environment these notes are
> verified in. So each experiment has two halves:
>
> - **The click-path** — the exact sequence of menus, panes and dialogs you
>   would follow in the tool, written out in [lab.md](lab.md). Marked
>   **NOT EXECUTED**. That is what the lab examiner will ask you to demonstrate.
> - **A Python equivalent that runs** — the same transformation, the same
>   measure, the same join — executed and asserted by
>   `tools/run_bi_labs.py`.
>
> The equivalents are not a substitute for the tools, and the notes never
> pretend otherwise. They exist so that **the numbers in these notes are
> checked** — when the notes claim a fan trap inflates a sales total from
> ₹4,500 to ₹10,500, code proves it.

## Textbooks

- Turban, Sharda & Delen, *Decision Support and Business Intelligence Systems*,
  9th ed., Pearson, 2014 — the theory in Units 1 and 5.
- Milligan, *Learning Tableau 2022*, 6th ed., Packt — Unit 3.
- Bakhshi, *Expert Data Modeling with Power BI*, 2nd ed., Packt, 2023 —
  **Unit 4, which is the unit worth buying a book for.**
- Russo & Ferrari, *The Definitive Guide to DAX*, 2nd ed., Microsoft Press —
  the DAX reference. More than the course needs, and the right book anyway.
- Loth, *Visual Analytics with Tableau*, Addison-Wesley, 2019.

**Free and genuinely good:** Microsoft Learn's Power BI learning paths, and
Tableau's own Learning Hub. Both are named in the prescribed reading.

## How to study this course

1. **Install Power BI Desktop.** It is a free download for Windows, and it is
   what the lab exam uses. Tableau Public is free too and needs no licence —
   its one catch is that everything you save is **public**, so never put real
   data in it.
2. **Do not learn the menus, learn the model.** Menus change with each release
   and you can find them. The star schema in Unit 4 has not changed since
   Kimball described it in 1996, and it is what the ten-mark questions ask.
3. **Build one dashboard end to end, early.** Load a CSV, clean it, model it,
   chart it, publish it. The whole course makes more sense afterwards, and
   experiment 2 is exactly that.
4. **For every visual you make, ask who would act on it and how.** That is
   Unit 5's entire content, and it is the difference between a dashboard and a
   wall of charts.
