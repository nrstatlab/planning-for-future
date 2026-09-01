# Course 5 — Database Management Systems

**Semester III**

---

## Why this course matters

Data science begins with data, and most of the world's structured data lives in
a relational database. Before you can analyse anything you have to get it out,
and getting it out means SQL.

SQL is also the most durable skill in this degree. Libraries come and go;
`SELECT ... FROM ... WHERE ... GROUP BY` has been essentially unchanged since
1974 and will outlast whatever framework is fashionable when you graduate.

## One thing you must know before you start

**Triggers are examined but are not in the syllabus units.** Unit 5 lists
control structures, procedures and functions — no triggers. Yet Course
Objective 5 names "database triggers", the prescribed activities require them,
and **two of the six PL/SQL lab questions are trigger problems**.

Study them. They are covered in [unit-5.md](unit-5.md). See
[`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D2**.

## Course objectives (verbatim)

1. To understand the fundamentals of data, information, and the evolution from
   file-based systems to modern database management systems.
2. To develop the ability to design conceptual data models using Entity-
   Relationship (ER) and Enhanced ER diagrams.
3. To explore relational model principles, such as keys, integrity constraints
   and normalization.
4. To perform data definition and manipulation using SQL commands including
   queries, joins, subqueries, views, and set operations.
5. To apply procedural logic using PL/SQL, incorporating control structures,
   functions, procedures, and **database triggers**.

*(Objective 5 names triggers; Course Outcome 5 and Unit 5 both drop them.)*

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | Overview of DBMS | [unit-1.md](unit-1.md) | Easy | 2 |
| 2 | Entity-Relationship model | [unit-2.md](unit-2.md) | Moderate | 3 |
| 3 | Relational model and normalization | [unit-3.md](unit-3.md) | **Hard** | 3 |
| 4 | Structured Query Language | [unit-4.md](unit-4.md) | Moderate | 4 |
| 5 | PL/SQL (and triggers) | [unit-5.md](unit-5.md) | **Hard** | 3 |

Units 3 and 4 carry the most marks. Unit 3 because normalization is
conceptually difficult; Unit 4 because SQL is what the lab exam tests.

## Also here

- [practice.md](practice.md) — exam-style questions with solutions
- [lab.md](lab.md) — the three experiments plus PL/SQL
- `labs/course-5-dbms/` — executable SQL
- `data/course-5-dbms/` — **practice datasets**, CSV: `assignments.csv`, `departments.csv`, `employees.csv`, `projects.csv`, `unnormalised-orders.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.

## Textbooks

- Silberschatz, Korth & Sudarshan, *Database System Concepts*, McGraw-Hill,
  7th edition — **the standard reference**
- Raghu Ramakrishnan, *Database Management Systems*, McGraw-Hill

**References:** Elmasri & Navathe, *Fundamentals of Database Systems* (Pearson)
· C. J. Date, *An Introduction to Database Systems* (Pearson)

## How to study this course

1. **Write SQL constantly.** Reading queries teaches nothing. Install SQLite
   (or use the Python `sqlite3` module, which needs no installation at all) and
   type every example.
2. **Draw the ER diagram before writing any schema.** Design errors are cheap
   to fix on paper and expensive to fix in a running database.
3. **Normalize by hand.** The exam gives you an unnormalized table and asks for
   3NF. Practise the decomposition until the steps are automatic.
4. **Trace query results mentally.** "What does this JOIN return if the right
   table has no matching row?" is the standard viva question.
5. **Know your dialect.** The syllabus targets **Oracle**. SQLite and MySQL
   differ in date functions, `LIMIT` vs `ROWNUM`, and PL/SQL. The notes flag
   these differences where they matter.
