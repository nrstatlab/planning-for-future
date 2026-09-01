# Course 1 — Computer Fundamentals and Office Automation

**Semester I**

---

## Why this course is not filler

It looks like the easy one, and in a sense it is. But two parts of it matter
more than they appear to.

**Number systems (Unit 1)** underpin everything a computer does. When you meet
bitwise operators in C, floating-point precision errors in Python, or a
character-encoding bug in a CSV file, this is the unit that explains them.

**Spreadsheets (Units 4–5)** are not a lesser tool. The Course 4 statistics lab
is entirely Excel-based, and Semester V's Business Intelligence course builds on
pivot tables and dashboards. VLOOKUP and pivot tables are the most widely used
data-analysis skills in the world by a very large margin.

This is also the course with the highest marks-per-hour ratio in the semester.
It is largely procedural and rewards practice rather than insight.

## Course objectives (verbatim)

1. Understand foundational computing concepts, including number systems, the
   evolution of computers, block diagrams, and generational progress.
2. Develop knowledge of computer architecture, focusing on system organization
   and networking fundamentals.
3. Acquire practical skills in document creation, formatting, and digital
   presentations using word processing tools.
4. Gain proficiency in spreadsheet operations, such as data entry, formulas,
   functions, and charting techniques.
5. Introduce data visualization and basic modelling principles, fostering
   analytical thinking in structuring and interpreting data sets.

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | Number systems, evolution, block diagram, generations | [unit-1.md](unit-1.md) | Moderate | 3 |
| 2 | Computer organization and networking | [unit-2.md](unit-2.md) | Easy | 3 |
| 3 | Word processing and presentations | [unit-3.md](unit-3.md) | Easy | 2 |
| 4 | Spreadsheet basics | [unit-4.md](unit-4.md) | Moderate | 3 |
| 5 | Data analysis and visualization | [unit-5.md](unit-5.md) | Moderate | 3 |

**Unit 1 is the only conceptually demanding one** — number-base conversions
need practice. Units 3 to 5 are hands-on: you learn them at a keyboard, not by
reading.

**Note:** conditional formatting appears in both Unit 4 ("Data Handling") and
Unit 5 (as a headline topic). Unit 5's treatment is the substantive one. See
[`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D9**.

## Also here

- [practice.md](practice.md) — questions with worked solutions
- [lab.md](lab.md) — all 14 lab experiments
- `labs/course-1-office/` — the code behind
  the figures. Excel cannot be installed in the environment these notes are
  verified in, so the eight experiments that compute something are recomputed
  and asserted there, along with every number-system conversion in Unit 1 and
  every text-function result in Unit 4. Run it with
  `python3 tools/run_office_labs.py`; it needs nothing but Python itself.
- `data/course-1-office/` — **practice datasets**, CSV: `budget.csv`, `class-results.csv`, `payroll.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.
  Also `sales-transactions.csv` in `data/shared/`, which several courses
  analyse so their answers can be compared.

For spreadsheet formulas in a statistical context, see
`labs/course-4-stats/excel-walkthroughs.md`,
which covers the same functions applied to real data analysis.

## Textbooks

- Reema Thareja, *Fundamentals of Computers*, OUP, 2nd edition
- V. Rajaraman, *Fundamentals of Computers*, PHI Learning
- Peter Norton, *Introduction to Computers*, McGraw Hill
- Randy Nordell, *Microsoft Office 365 In Practice*, McGraw Hill

**References:** Alexander & Kusleika, *Excel 2021 Bible* (Wiley) · Doug Lowe,
*Networking All-in-One For Dummies* (Wiley) · [learn.microsoft.com](https://learn.microsoft.com)
· [Google Workspace Learning Center](https://support.google.com/a/users/)

## How to study this course

1. **Practise conversions until they are automatic.** Binary to decimal, decimal
   to hex, and back. Ten minutes a day for a week is enough.
2. **Do everything at a keyboard.** You cannot learn VLOOKUP by reading about
   VLOOKUP.
3. **Memorise the shortcuts.** They are explicitly on the syllabus and they make
   the lab exam faster.
4. **Build one real dashboard.** Experiment 14 asks for one; doing it properly
   once teaches more than the previous thirteen.
