---
layout: note
title: "Study Plan — B.Sc. (Hons) Data Science Major"
section: "Data Science Major"
---

# Study Plan — B.Sc. (Hons) Data Science Major

A week-by-week schedule for the five courses this repository covers, weighted
by the difficulty established in [`SYLLABUS-REVIEW.md`](SYLLABUS-REVIEW.html).

**The weighting is the point.** An even split across five units is the wrong
plan when one unit holds three units' worth of material. Where a unit gets more
weeks than its neighbours below, the review explains why.

---

## Semester I — 15 weeks

Two courses, 8 credits. The lightest semester of the degree; use the slack to
build programming habits that will carry you through the next two years.

| Week | Course 1 — Computer Fundamentals | Course 2 — Problem Solving Using C |
|:---:|---|---|
| 1 | Unit 1 — number systems: binary, decimal | Unit 1 — software types, compiler vs interpreter |
| 2 | Unit 1 — octal, hex, conversions | Unit 1 — algorithms, flowcharts, C history |
| 3 | Unit 1 — binary arithmetic, complements, generations | Unit 1 — tokens, data types, operators, I/O |
| 4 | Unit 2 — memory hierarchy, storage | Unit 2 — if, if-else, else-if ladder |
| 5 | Unit 2 — types of computers, networks | Unit 2 — switch, loops |
| 6 | Unit 2 — topologies, Internet basics | Unit 2 — break, continue, goto; **patterns** |
| 7 | **Revision 1** — Units 1–2 both courses | **Revision 1** |
| 8 | Unit 3 — Word: formatting, styles, tables | Unit 3 — 1-D arrays, memory representation |
| 9 | Unit 3 — mail merge, presentations, shortcuts | Unit 3 — 2-D arrays, matrix operations |
| 10 | Unit 4 — cell referencing, basic functions | Unit 3 — strings, string functions |
| 11 | Unit 4 — logical and text functions | **Unit 4 — pointers** ⚠ |
| 12 | Unit 4 — VLOOKUP, XLOOKUP, INDEX+MATCH | **Unit 4 — functions, recursion, parameter passing** ⚠ |
| 13 | Unit 5 — pivot tables, slicers | **Unit 4 — storage classes** ⚠ |
| 14 | Unit 5 — what-if analysis, dashboards | Unit 5 — dynamic memory, structures, unions |
| 15 | **Revision 2** — full syllabus | Unit 5 — file handling; **Revision 2** |

**Course 2 Unit 4 gets three weeks** (11–13). It is the hardest material in the
first year, and the syllabus mislabels it "Functions" when it opens with
pointers — see finding **D5**. Draw memory diagrams for every pointer example.

---

## Semester II — 15 weeks

Two courses, 8 credits. **The most important semester in the degree.** Python
and statistics are the foundation of everything from Semester III onward.

| Week | Course 3 — Python | Course 4 — Statistics |
|:---:|---|---|
| 1 | Unit 1 — features, modes, identifiers, types | Unit 1 — probability rules, axioms |
| 2 | Unit 1 — operators, precedence, I/O | Unit 1 — conditional probability, **Bayes** ⚠ |
| 3 | Unit 2 — control flow, `for…else` | Unit 1 — central tendency, dispersion |
| 4 | Unit 2 — functions, arguments, scope, lambda | Unit 2 — random variables, PMF/PDF/CDF |
| 5 | Unit 3 — strings and lists | Unit 2 — expectation, variance, moments |
| 6 | Unit 3 — tuples, sets | **Unit 3 — binomial, Poisson** |
| 7 | **Revision 1** — Units 1–3 | **Revision 1**; Unit 3 — geometric, negative binomial |
| 8 | Unit 3 — dictionaries, comprehensions | **Unit 3 — normal distribution, z-scores** |
| 9 | **Unit 4 — file handling, CSV** ⚠ | **Unit 3 — exponential, gamma, CLT** |
| 10 | **Unit 4 — exception handling** ⚠ | **Unit 4 — covariance, correlation** |
| 11 | **Unit 4 — classes, objects, encapsulation** ⚠ | **Unit 4 — regression, least squares** |
| 12 | **Unit 4 — inheritance, MRO, polymorphism** ⚠ | **Unit 4 — residuals, R², ANOVA** |
| 13 | Unit 5 — linked lists, stacks, queues | **Unit 5 — estimation, confidence intervals** |
| 14 | Unit 5 — priority queues; Tkinter | **Unit 5 — z-test, t-test** |
| 15 | **Revision 2** — full syllabus | **Unit 5 — chi-square, F-test, errors, power** |

### Why the weighting

**Course 3 Unit 4 gets four weeks (9–12), not two.** It contains file handling
*and* exception handling *and* the whole of object-oriented programming — three
units compressed into one. Compare Unit 1, which covers only literals and
operators. Finding **D6**.

**Course 4 Units 3, 4 and 5 get three weeks each.** Distributions, regression
and inference are where the marks and the difficulty both are.

**Bayes' theorem is scheduled in week 2** even though it is not in the syllabus
unit list, because it is examined. Finding **D1**.

---

## Semester III — 15 weeks (Course 5 only)

Three courses run this semester; only DBMS is covered here. Adjust for Data
Science with R and Web Technologies when you have those syllabi.

| Week | Course 5 — Database Management Systems |
|:---:|---|
| 1 | Unit 1 — data vs information, file-based systems and their drawbacks |
| 2 | Unit 1 — database approach, three-schema architecture, data independence |
| 3 | Unit 2 — ER building blocks, entity and attribute classification |
| 4 | Unit 2 — relationships, cardinality, participation |
| 5 | Unit 2 — **reducing ER to tables**; EER, generalization, specialization |
| 6 | Unit 3 — relational model, keys, integrity constraints |
| 7 | **Revision 1**; Unit 3 — relational algebra |
| 8 | **Unit 3 — functional dependencies, 1NF, 2NF** |
| 9 | **Unit 3 — 3NF, BCNF, worked normalization** |
| 10 | Unit 4 — DDL, constraints, DML |
| 11 | Unit 4 — SELECT, WHERE, aggregates, GROUP BY, HAVING |
| 12 | **Unit 4 — joins** (inner, left, self, three-table) |
| 13 | Unit 4 — set operations, subqueries, views |
| 14 | Unit 5 — PL/SQL blocks, control structures, cursors, exceptions |
| 15 | **Unit 5 — procedures, functions, TRIGGERS** ⚠; **Revision 2** |

**Triggers are scheduled in week 15** despite being absent from the Unit 5
syllabus list. Two of the six PL/SQL lab questions are trigger problems.
Finding **D2**.

Weeks 8–9 on normalization and week 12 on joins carry the most exam weight in
this course.

---

## Before Semester IV — a statistics refresher

**Two weeks, during the break before Semester IV begins.**

Regression, correlation and hypothesis testing are taught in Semester II. Their
first real application is Data Mining in **Semester IV**, and Machine Learning
is a Year III elective in **Semester V** — three semesters after the theory.
Statistical intuition decays without use. Finding **D10**.

| Day | Revise |
|---|---|
| 1–2 | Descriptive statistics, distributions ([formula sheet](notes/sem-2/course-4-statistical-foundations/formula-sheet.html)) |
| 3–4 | Correlation and regression; re-run [`04_correlation_regression.py`](labs/course-4-stats/python/04_correlation_regression.py) |
| 5–6 | Hypothesis testing; re-run [`05_inference_hypothesis_tests.py`](labs/course-4-stats/python/05_inference_hypothesis_tests.py) |
| 7–10 | Bridge the Excel/Python gap — redo the stats labs in Python (finding **D8**) |
| 11–14 | Python revision: NumPy and Pandas basics, ready for Course 9 |

That last block matters. The Semester II stats lab is entirely Excel, so you
arrive in Semester IV able to run a regression in a spreadsheet but not in the
language you spent a semester learning.

---

## Weekly rhythm

A schedule you can actually keep beats an ambitious one you abandon in week 3.

| Day | Focus |
|---|---|
| **Mon–Fri** | Attend, then spend **1 hour per subject** the same evening consolidating |
| **Saturday** | **3 hours** — lab programs, typed and run, not copied |
| **Sunday** | **2 hours** — revise the week; **1 hour** — revise something from three weeks ago |

**The Sunday spaced-revision hour is the highest-value hour of the week.**
Re-reading this week's material feels productive and mostly is not; retrieving
three-week-old material is what moves it into long-term memory.

---

## Revision cycles

| Cycle | When | What |
|---|---|---|
| **Daily** | Same evening | Review the day's notes — 15 minutes |
| **Weekly** | Sunday | The week's units, plus one older topic |
| **Revision 1** | Week 7 | Units 1–3 of every course |
| **Revision 2** | Week 15 | Full syllabus, past papers |
| **Pre-exam** | Final fortnight | See below |

### The final fortnight

| Days | Activity |
|---|---|
| 14–11 | One full pass of every unit's notes |
| 10–8 | Formula sheets and the "mistakes that cost marks" section of each unit |
| 7–5 | **Past papers under timed conditions** |
| 4–3 | Practice problems; re-work anything you got wrong |
| 2–1 | Formula sheets and quick self-tests only — no new material |
| Exam eve | Sleep. Cramming past midnight costs more than it gains. |

**Past papers are the highest-value revision there is.** They reveal which
topics actually recur, how questions are phrased, and how marks are distributed
— none of which the syllabus tells you.

---

## Progress checklist

Tick a unit only when you can (a) explain it without notes and (b) solve a
problem on it unaided.

### Semester I

**Course 1 — Computer Fundamentals**
- [ ] Unit 1 — Number systems, evolution, block diagram, generations
- [ ] Unit 2 — Organization and networking
- [ ] Unit 3 — Word processing and presentations
- [ ] Unit 4 — Spreadsheet basics
- [ ] Unit 5 — Data analysis and visualization
- [ ] Lab — all 14 experiments

**Course 2 — Problem Solving Using C**
- [ ] Unit 1 — Introduction to programming
- [ ] Unit 2 — Control statements
- [ ] Unit 3 — Arrays and strings
- [ ] Unit 4 — Pointers, functions, storage classes ⚠
- [ ] Unit 5 — Dynamic memory, structures, files
- [ ] Lab — all 15 programs compiled and run

### Semester II

**Course 3 — Python Programming and Data Structures**
- [ ] Unit 1 — Basics
- [ ] Unit 2 — Control flow, functions, modules
- [ ] Unit 3 — Sequences, sets, dictionaries
- [ ] Unit 4 — Files, exceptions, OOP ⚠
- [ ] Unit 5 — Data structures and GUI
- [ ] Lab — all 18 programs run

**Course 4 — Statistical Foundations**
- [ ] Unit 1 — Probability and descriptive statistics (**including Bayes** ⚠)
- [ ] Unit 2 — Random variables, expectation, variance
- [ ] Unit 3 — Distributions
- [ ] Unit 4 — Correlation and regression
- [ ] Unit 5 — Inference and hypothesis testing
- [ ] Lab — all 15 experiments, **in Excel and in Python**

### Semester III

**Course 5 — Database Management Systems**
- [ ] Unit 1 — DBMS overview and three-schema architecture
- [ ] Unit 2 — ER and EER models
- [ ] Unit 3 — Relational model and normalization
- [ ] Unit 4 — SQL
- [ ] Unit 5 — PL/SQL (**including triggers** ⚠)
- [ ] Lab — all three experiments plus PL/SQL

---

## The four things that matter most

If you do nothing else from this plan:

1. **Type every lab program.** Reading code teaches nothing. All 52 programs in
   [`labs/`](labs/) run — type them, break them, fix them.
2. **Give Course 3 Unit 4 and Course 4 Units 3–5 double time.** They carry the
   difficulty and the marks.
3. **Study Bayes' theorem and database triggers**, though neither appears in
   its syllabus unit list. Both are examined.
4. **Do past papers under timed conditions**, starting a week before the exam.
