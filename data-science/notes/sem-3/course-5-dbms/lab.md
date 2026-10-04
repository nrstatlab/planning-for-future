# Lab — Database Management Systems

**3 experiments plus PL/SQL**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme,
5. Execution and Results.

All SQL is in `labs/course-5-dbms/`:

| File | Contents | Verified? |
|---|---|---|
| `01_inventory.sql` | Experiment 1 — Inventory Management | ✅ executed |
| `02_bookstore.sql` | Experiment 2 — Online Bookstore | ✅ executed |
| `03_employee.sql` | Experiment 3 — Employee DB, sections A–D | ✅ executed |
| `04_plsql_oracle.sql` | Experiment 3 section E — PL/SQL | ⚠ desk-checked only |

```bash
python3 tools/data-science/run_sql_labs.py
```

This loads each schema with its official sample data, runs every statement, and
then deliberately attempts nine illegal operations to confirm the constraints
reject them. Current result: **118 statements executed, 70 SELECT queries
returning 301 rows, 9/9 constraints enforced**.

The output under **5. Execution and Results** is the `sqlite3` shell's, in box mode, from running
each script on a new database. So that you can tell which result answers which question, each
question's number and text are printed before it; a question that only creates or changes data
prints nothing but its label. The constraint tests come last, each statement with the error the
database gave. To see the tables yourself:

```bash
sqlite3 -box inventory.db < labs/course-5-dbms/01_inventory.sql
```

Two questions ask about *today*: Experiment 2's question 27 and Experiment 3's questions 27
and 28. Their answers change with the date you run them, so the output shown was made with the
clock set to 4 October 2026.

**The PL/SQL file is not executed.** PL/SQL is Oracle-specific, SQLite cannot
run it, and no Oracle instance was available. Those blocks are written to Oracle
syntax and reviewed by hand — run them on your college's Oracle installation
before relying on them. This is stated in the file itself rather than left for
you to discover.

---

## A note on question numbering

The official question lists have gaps — numbers that were dropped when the PDF
was produced:

| Experiment | Missing numbers |
|---|---|
| 1 — Inventory | 3, 13, 20, 22 |
| 2 — Bookstore | 12, 19 |
| 3 — Employee | 8 |
| 3 — Section E (PL/SQL) | 2 |

Some lost their text entirely; others left orphans. PL/SQL question 2 survives
only as the dangling fragment *"If yes, print 'High Salary'; Otherwise print
'Standard Salary'"*, with no question in front of it.

The lab files **reconstruct each missing item and mark it `[RECONSTRUCTED]`**,
so you can tell the reconstruction from the official text. Two items in
Experiment 1 (questions 6 and 8) are also cut off mid-sentence — "Update the
stock quantity of" — and are completed the same way.

See [`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D4**.

---

## Experiment 1 — Inventory Management

### 1. Question

Build an inventory database of products and their suppliers: create the Products and Suppliers tables with their constraints, insert the official sample data, change it, and answer the 24 questions set on it.

### 2. Aim

Define, fill and query two tables joined by a foreign key, using DDL, DML and DQL.

### 3. Steps

1. **Create the tables, with their constraints.** Section A, questions 1–3.
2. **Insert the sample data, then update and delete rows.** Section B, questions 4–8.
3. **Query the tables.** Section C, questions 9–24.

<div class="formula" markdown="1">
<span class="label">THE TABLES</span>

Two tables, `Products` and `Suppliers`, with a foreign key between them.

**Constraints exercised:** `PRIMARY KEY`, `NOT NULL`, `CHECK (price > 0)`,
`CHECK (stock_qty >= 0)`, `UNIQUE` on contact number, `FOREIGN KEY`.

**Sections:** A = DDL (create), B = DML (insert, update, delete), C = DQL
(24 queries covering comparison, `BETWEEN`, `LIKE`, aggregates, `GROUP BY`,
joins).
</div>


### 4. Programme

{{programme: course-5-dbms/01_inventory.sql}}

### 5. Execution and Results

{{output: course-5-dbms/01_inventory.sql}}

**Worth practising:** question 17, "count how many suppliers supply each
product", needs a `LEFT JOIN` — a product with no supplier must still appear
with a count of zero. `INNER JOIN` silently drops it. In the output, File Folder has no
supplier and is listed with 0.

Question 23 prints only its label: no product name in the sample data is five characters long, so
the query rightly returns no rows.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Both tables are created and filled, all 24 questions run, and the three constraint tests are all rejected: a negative price, a repeated `product_id` and a missing product name.
</div>


## Experiment 2 — Online Bookstore

### 1. Question

Build an online bookstore database of authors, books, customers and orders: create the four tables with their keys and constraints, alter them, insert the official sample data, change it, and answer the 36 questions set on it.

### 2. Aim

Design a four-table schema, and query it with conditions, date functions, aggregates and `GROUP BY` with `HAVING`.

### 3. Steps

1. **Create the four tables, then alter them.** Section A, questions 1–4.
2. **Insert the sample data, then update and delete rows.** Section B, questions 5–8.
3. **Select rows by condition, pattern and order.** Section C, questions 9–23.
4. **Use the date functions.** Questions 24–27.
5. **Summarise with the aggregate functions.** Questions 28–32.
6. **Group with GROUP BY and HAVING.** Questions 33–36.

<div class="formula" markdown="1">
<span class="label">THE DATE FUNCTIONS</span>

Four tables: `Authors`, `Books`, `Customers`, `Orders`.

This is the experiment with the **date functions**, which differ more between
vendors than anything else in SQL:

| Task | SQLite | Oracle |
|---|---|---|
| Orders in July 2025 | `strftime('%Y-%m', order_date) = '2025-07'` | `TO_CHAR(order_date,'YYYY-MM') = '2025-07'` |
| 5 days after order | `DATE(order_date, '+5 days')` | `order_date + 5` |
| Weekend orders | `strftime('%w', order_date) IN ('0','6')` | `TO_CHAR(order_date,'DY') IN ('SAT','SUN')` |
| Days since last order | `julianday('now') - julianday(...)` | `SYSDATE - MAX(order_date)` |

**Know which dialect your lab uses.** Writing `SYSDATE` in a MySQL exam, or
`LIMIT` in an Oracle one, loses marks even though the logic is right.
</div>


### 4. Programme

{{programme: course-5-dbms/02_bookstore.sql}}

### 5. Execution and Results

{{output: course-5-dbms/02_bookstore.sql}}

Section C also covers `GROUP BY` with `HAVING` — question 35, "customers who
have ordered more than 2 books in total", is the standard `HAVING` question. Here only customer
205 has, with 3.

Question 27 counts the days from the last order, 26 July 2025, to the day the script runs; on
4 October 2026 that is 435. Run it yourself and you will get a different number.

After question 6, Animal Farm costs 9.625: 10% on 8.75. The column is declared
`DECIMAL(10,2)`, but SQLite does not enforce the two decimal places, so it keeps all three.
Oracle's `NUMBER(10,2)` would round it to 9.63 as it is stored.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The four tables are created, altered and filled, all 36 questions run, and the two constraint tests are both rejected: a repeated email and an order with no date.
</div>


## Experiment 3 — Employee Database

### 1. Question

Build an employee database of departments, employees, projects and the employees' work on projects: create the tables with their constraints, insert the official sample data, change it, and answer the questions set in sections A–D, two of which must fail.

### 2. Aim

Build a schema with a self-referential and a many-to-many relationship, show that its constraints reject bad data, and query it with grouping and joins.

### 3. Steps

1. **Create the four tables, then add and drop a column.** Section A, questions 1–3.
2. **Insert the sample data, then update and delete rows.** Section B, questions 4–9. Questions 5 and 9 must fail, so the script leaves them as comments, and they are run separately, after it.
3. **Query, group and summarise the employees.** Section C, questions 10–28.
4. **Join the tables.** Section D, questions 29–34, then a self join.

<div class="formula" markdown="1">
<span class="label">THE DESIGN</span>

The largest: four tables including a **self-referential foreign key**
(`manager_id` references `Employees.emp_id`) and a **many-to-many** junction
table (`Employee_Project`).

Two design points worth understanding:

**Insert order matters.** Managers must be inserted before their reports, or the
self-referential foreign key has nothing to point at. The lab file inserts
employees 101, 104 and 106 (the managers) first for exactly this reason.

**Deletion order matters.** Question 7 deletes a resigned employee, but child
rows in `Employee_Project` reference them. Delete the children first, or the
foreign key blocks it. The lab uses emp_id 105 because nobody reports to them.
</div>


### 4. Programme

{{programme: course-5-dbms/03_employee.sql}}

### 5. Execution and Results

{{output: course-5-dbms/03_employee.sql}}

Section D is the joins section, and the **self join** (each employee with their
manager) is the one most likely to appear in a viva. It is the last query, labelled BONUS.

Questions 5 and 9 are among the constraint tests at the end: the negative salary breaks the
`CHECK`, and department 99 does not exist, so the foreign key refuses it.

Three questions print only their label, and rightly. Question 27: the sample employees were hired
between 2017 and 2023, so none in the last 90 days. Question 33: in the sample data each employee
works on one project. Question 28's years of experience are counted to 4 October 2026.

Diana Prince's salary shows as 99000.0 after question 8's 10% raise, not 99000. In binary
floating point 90000 × 1.10 is 99000.00000000001, so SQLite keeps it as a real number. Oracle's
`NUMBER` is decimal and stores exactly 99000.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The four tables are created and filled, sections A–D run, and all four constraint tests are rejected: a negative salary, a department that does not exist, a badly formed phone number and a repeated department name.
</div>


## Experiment 3, Section E — PL/SQL

### 1. Question

On the Employee database, write PL/SQL procedures, a cursor and triggers: the six questions of section E, question 2 reconstructed.

### 2. Aim

Write stored procedures, a cursor, row-level and statement-level triggers and a function in Oracle PL/SQL.

### 3. Steps

1. **A procedure that displays an employee's details.** Question 1.
2. **A procedure that prints the salary band.** Question 2, reconstructed.
3. **A cursor over the top 10 rows.** Question 3.
4. **A procedure that adds a bonus.** Question 4.
5. **A row-level trigger for the minimum salary.** Question 5.
6. **A statement-level trigger that blocks weekend changes.** Question 6.
7. **A function, for comparison.** Not set, but Unit 5 lists functions beside procedures.

<div class="formula" markdown="1">
<span class="label">THE SIX QUESTIONS</span>

Six questions. Question 2 is reconstructed (see above); questions 5 and 6 are
**triggers**, which the syllabus never lists as a topic.

| # | Task | Type |
|:---:|---|---|
| 1 | `GetEmpInfo` — display name, salary, department | Procedure |
| 2 | *[Reconstructed]* Check salary band and print High/Standard | Procedure |
| 3 | Top 10 rows by job and salary | Cursor |
| 4 | `GiveBonus` — update salaries by department and designation | Procedure |
| 5 | Prevent inserting a salary below 30,000 | **Row-level trigger** |
| 6 | Block all changes at the weekend | **Statement-level trigger** |
</div>


### 4. Programme

{{programme: course-5-dbms/04_plsql_oracle.sql}}

### 5. Execution and Results

{{not-run: course-5-dbms/04_plsql_oracle.sql | it is Oracle PL/SQL, which SQLite cannot run, and no Oracle database is available here; it was checked by hand against Oracle's syntax. Run it on your college's Oracle installation, in SQL*Plus or SQL Developer, after `SET SERVEROUTPUT ON`}}

**The distinction between questions 5 and 6 is the point.** Question 5 is about
individual rows, so it needs `FOR EACH ROW` and `:NEW.salary`. Question 6 is
about *when the statement runs*, so it is statement-level and has no `:NEW` at
all. Be ready to explain why in the viva.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

The procedures, cursor, triggers and function are written to Oracle's syntax and checked by hand; they have not been run here.
</div>


---

## Lab exam tips

1. **`SET SERVEROUTPUT ON` before any PL/SQL.** Without it `DBMS_OUTPUT`
   produces nothing and the code looks broken when it is not. This is the most
   common lab-exam failure.
2. **End PL/SQL blocks with `/`** on its own line.
3. **Create the tables and insert the sample data first**, then test each query.
   A query cannot be marked if the schema does not exist.
4. **Test constraints deliberately.** Try the negative salary and show that it
   is rejected — examiners give marks for demonstrating that a constraint works.
5. **Format your output.** Use column aliases (`AS headcount`) and `ORDER BY`.
   A readable result reads as a correct one.
6. **Comment each query** with the question number it answers.
7. **Watch the dialect.** Confirm whether your lab uses Oracle, MySQL or
   PostgreSQL before writing date functions or row limits.
8. **Expect a viva.** "Why a `LEFT JOIN` here?", "what happens if I drop this
   constraint?", "why is this trigger `BEFORE` and not `AFTER`?"
