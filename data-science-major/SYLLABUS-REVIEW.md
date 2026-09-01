---
layout: note
title: "Syllabus Review — B.Sc. (Hons) Data Science Major, APSCHE AY 2025-26"
section: "Data Science Major"
---

# Syllabus Review — B.Sc. (Hons) Data Science Major, APSCHE AY 2025-26

A check of the official syllabus document, not a transcription of it. Every
finding below was verified against
[`docs/syllabus-extracted.md`](docs/syllabus-extracted.html); page numbers refer to
the source PDF.

**Read this before you start studying.** Two findings (D1 and D2) name topics that
are *examined but not listed in the syllabus units*. If you study only the unit
lists, you will walk into those questions unprepared.

---

## Summary

| ID | Finding | Severity |
|:---:|---|---|
| D1 | Bayes' theorem examined but absent from the units | **High** — affects marks |
| D2 | Database triggers examined but absent from the units | **High** — affects marks |
| D3 | Text truncated in three places in the official PDF | Medium |
| D4 | Lab question numbering broken in all three DBMS experiments | Low |
| D5 | Course 2 Unit 4 title does not match its content | Low |
| D6 | Course 3 Unit 4 carries roughly double a normal unit's load | Medium — affects planning |
| D7 | Course 3 Unit 5 fuses two unrelated subjects | Medium — affects planning |
| D8 | Statistics lab never uses Python, though Python is taught the same semester | Medium — affects skills |
| D9 | Conditional formatting duplicated across Course 1 Units 4 and 5 | Low |
| D10 | Three-semester gap between statistics and its first application | Medium |
| D11 | Course 2 activity list has an orphaned entry | Low |

**What is *not* wrong:** the credit arithmetic. Every course is 3 + 1 = 4 credits;
semester totals are 8, 8, 12, 12, 12, 8 for a **60-credit major**, consistent with
the structure table on pages 1–2.

---

## Findings that affect your marks

### D1 — Bayes' theorem is examined but never listed as a topic

**Page 20** (Course 4, Unit 1) lists the probability topics as: "Concept of
Uncertainty, Axioms and rules of probability, Conditional probability". Bayes'
theorem does not appear in Unit 1, or in any other unit of the course.

But **page 22** (Activities) prescribes: "Classroom Quiz (MCQs & short problems on
probability, conditional probability, **Bayes**)". And **page 23**, lab experiment
2, is a fragment reading only "a positive result." — the surviving tail of the
standard Bayes medical-testing problem ("*…given that the test returns a positive
result*").

**Consequence:** a topic that carries assessment weight sits outside the syllabus
list you would revise from.

**What to do:** study Bayes' theorem as though it were listed in Unit 1. It is
covered in [Course 4 Unit 1](notes/sem-2/course-4-statistical-foundations/unit-1.html),
where it is flagged as an off-syllabus-but-examined addition, with the
reconstructed medical-test problem worked in full.

### D2 — Database triggers are examined but never listed as a topic

**Page 25** (Course 5, Unit 5, PL/SQL) lists: "Introduction, Shortcomings of SQL,
Structure of PL/SQL, PL/SQL Language Elements, Data Types, Operators Precedence,
Control Structures, Steps to Create a PL/SQL Program, Iterative Control,
Procedures, Functions." **Triggers are not among them.**

Yet triggers are required in three separate places:

- **Page 24**, Course Objective 5: "…incorporating control structures, functions,
  procedures, and **database triggers**."
- **Page 27**, Activities: "Build a PL/SQL-based payroll or student grading system
  using: Procedures and functions, Control structures (IF, LOOP), **Triggers for
  automated updates**."
- **Page 37**, lab Section E items 5 and 6: "Create a trigger to prevent inserting
  employees with a salary less than 30,000" and "Create a trigger to avoid any
  transactions (insert, update, delete) on the EMP table on Saturday & Sunday."

Note also that Course Outcome 5 (page 24) drops triggers even though the Objective
names them — so the omission is consistent between the outcome and the unit, and
inconsistent with the assessment.

**What to do:** study triggers as part of Unit 5. Covered in
[Course 5 Unit 5](notes/sem-3/course-5-dbms/unit-5.html), with both lab triggers
written out.

---

## Defects in the document

### D3 — Truncated text in three places

1. **Page 20, Course Outcome 1** reads: "Apply the basic rules of probability,
   **conditisolve** problems involving uncertainty." Words have been dropped mid-
   sentence. The intended reading is almost certainly "…probability, conditional
   probability and Bayes' theorem to solve problems involving uncertainty" — which
   independently supports **D1**.
2. **Page 23, lab experiment 2** is just "a positive result." The question stem is
   gone. Reconstructed in the Course 4 lab notes.
3. **Page 2, elective note** reads: "students are required to select a pair of
   electives from one of the TWO specified domains. **is chosen**, courses 12 to 15
   to be chosen as 12 A, 13 A, 14 A and 15 A." The clause naming the two domains
   has been lost, so **the domains are never actually named anywhere in the
   document**. The A/B tracks can be inferred from the course titles (see
   [`SYLLABUS-MAP.md`](SYLLABUS-MAP.html) §1), but confirm the official names with
   your department before committing to a track in Year III.

### D4 — Lab question numbering is broken in all three DBMS experiments

Verified by extracting every numbered item:

| Experiment | Pages | Missing numbers |
|---|:---:|---|
| 1 — Inventory Management | 29 | 3, 13, 20, 22 |
| 2 — Online Bookstore | 31–32 | 12, 19 |
| 3 — Employee DB | 36–37 | 8 |
| 3 — Section E (PL/SQL) | 37 | 2 |

Some gaps lost their text entirely; others left orphans. PL/SQL item 2 is the
clearest case — its text survives as a dangling fragment, "If yes, print 'High
Salary'; Otherwise print 'Standard Salary'", with no question in front of it. The
intended question is evidently "write a PL/SQL block that checks whether an
employee's salary exceeds some threshold".

Section B of Experiment 1 also begins at 4, and items 6 and 8 are cut short
("Update the stock quantity of" — of what?).

**What to do:** the lab notes renumber cleanly and reconstruct the missing items,
marking each reconstruction as such so you can tell it from the official text.

### D5 — Course 2 Unit 4 is titled "Functions" but opens with pointers

**Page 10.** The unit is headed "Unit 4. Functions:" and its first topics are
"Pointers: Pointer data type, Pointer declaration, initialization, accessing
values using pointers. Pointer arithmetic, Pointers and arrays." Functions follow
*after* pointers, then storage classes.

Harmless to the content, but if you revise from unit titles you will not expect
pointers to be examined under "Functions". The notes cover them in the order
printed and flag the mismatch.

### D11 — Orphaned activity in Course 2

**Page 11.** Every activity in the document follows the pattern `Outcome: … /
Activity: … / Evaluation Method: …`. The "Recursive Problem Solver" activity
appears with no `Outcome:` heading above it, unlike its four siblings — its
outcome line was dropped. It maps to Course Outcome 4 (modular code using
functions, recursion and parameter passing).

---

## Design and sequencing issues

### D6 — Course 3 Unit 4 carries roughly double the load of a normal unit

**Page 15.** Unit 4 is "File Handling, Exception Handling & Object Oriented
Programming" and contains:

- file types, paths, open/close, read/write, CSV, `os`/`pathlib`
- syntax errors, built-in exceptions, `try-except`, `raise`, user-defined
  exceptions, assertions
- classes, objects, attributes, methods, constructors, destructors
- encapsulation with private and public members
- inheritance — single, multilevel **and** multiple — plus method overriding

That is three teachable units compressed into one. OOP alone is normally a full
unit. Compare Unit 1, which covers only literals, variables and operators.

**What to do:** budget roughly twice the study time for Unit 4 as for Unit 1. The
[study plan](STUDY-PLAN.html) already does this, splitting it across three weeks.

### D7 — Course 3 Unit 5 fuses two unrelated subjects

**Pages 15–16.** Unit 5 is "Abstract Data Structures and GUI Programming" —
linked lists, stacks, queues and priority queues, *and* Tkinter widgets and event
handling. These share nothing conceptually. Data structures are algorithmic and
carry the exam weight; Tkinter is applied and carries the lab weight (2 of the 18
lab programs).

**What to do:** treat them as two separate topics. The notes split
`unit-5.md` into two clearly divided halves.

### D8 — The statistics lab never touches Python

**Page 23.** Course 4's lab is headed "Advanced Spreadsheets/Excel Lab/PSPP Open
Source", and all 15 experiments are spreadsheet exercises — `NORM.DIST`,
`NORM.INV`, `EXPON.DIST`, the Data Analysis ToolPak, the Regression tool.

Meanwhile Course 3 teaches Python **in the same semester**. The two courses never
meet. Python-based data analysis waits until Semester IV, Course 9 ("Python for
Data Analysis and Visualization").

This is defensible pedagogically — a spreadsheet makes the arithmetic of variance
or a t-test visible in a way `scipy.stats.ttest_ind()` does not. But it means you
finish Semester II able to compute a regression in Excel and not in the language
you just spent a semester learning.

**What to do:** do each experiment **twice** — once in Excel exactly as prescribed
(that is what the exam tests) and once in Python (that is what the degree is for).
The Course 4 lab notes give both versions of all 15.

### D9 — Conditional formatting appears twice in Course 1

**Page 4.** Unit 4 lists "Data Handling: Sorting, filtering, **conditional
formatting**". Unit 5 then opens with "**Conditional Formatting**: Custom rules,
Color scales, Icon sets, Data bars" as a headline topic. Minor, but worth knowing
that Unit 5's treatment is the substantive one.

### D10 — Three-semester gap between statistics and its first real application

Regression, correlation and hypothesis testing are taught in **Semester II**
(Course 4). Their first genuine application is Data Mining in **Semester IV**, and
Machine Learning is a Year III elective in **Semester V** — three semesters after
the theory.

Statistical intuition decays without use. The [study plan](STUDY-PLAN.html)
schedules a short Course 4 refresher before Semester IV begins, so Data Mining
does not start with re-learning what a p-value is.

---

## Verification notes for this repository

The lab code in [`labs/`](labs/) was checked as follows:

| Language | Status |
|---|---|
| C (15 programs) | **Compiled and run.** `gcc -Wall -Wextra`, no warnings, output verified against expected results. |
| Python (16 of 18) | **Run.** Python 3.11. |
| Python — Tkinter (2 programs) | **Syntax-checked only.** `tkinter` is not installed in this environment, so `python3 -m py_compile` is the strongest check available. Marked in the files. |
| SQL — DDL/DML/queries | **Executed** against SQLite via `tools/run_sql_labs.py`, with schema and the official sample data loaded. |
| PL/SQL (procedures, functions, triggers) | **Desk-checked only, not executed.** The syllabus targets Oracle PL/SQL; SQLite cannot run it and no Oracle instance is available here. These blocks are written to Oracle syntax and reviewed by hand — verify them on your college's Oracle installation. |
| Excel/PSPP walkthroughs | **Not executable.** Written as step-by-step instructions with exact formulas; the Python equivalents of the same 15 experiments are provided and were run. |
