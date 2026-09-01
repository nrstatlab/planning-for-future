# Course 5 Lab — Database Management Systems

**3 experiments plus PL/SQL**

All SQL is in `labs/course-5-dbms/`:

| File | Contents | Verified? |
|---|---|---|
| `01_inventory.sql` | Experiment 1 — Inventory Management | ✅ executed |
| `02_bookstore.sql` | Experiment 2 — Online Bookstore | ✅ executed |
| `03_employee.sql` | Experiment 3 — Employee DB, sections A–D | ✅ executed |
| `04_plsql_oracle.sql` | Experiment 3 section E — PL/SQL | ⚠ desk-checked only |

```bash
python3 tools/run_sql_labs.py
```

This loads each schema with its official sample data, runs every statement, and
then deliberately attempts nine illegal operations to confirm the constraints
reject them. Current result: **118 statements executed, 70 SELECT queries
returning 301 rows, 9/9 constraints enforced**.

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

Two tables, `Products` and `Suppliers`, with a foreign key between them.

**Constraints exercised:** `PRIMARY KEY`, `NOT NULL`, `CHECK (price > 0)`,
`CHECK (stock_qty >= 0)`, `UNIQUE` on contact number, `FOREIGN KEY`.

**Sections:** A = DDL (create), B = DML (insert, update, delete), C = DQL
(24 queries covering comparison, `BETWEEN`, `LIKE`, aggregates, `GROUP BY`,
joins).

**Worth practising:** question 17, "count how many suppliers supply each
product", needs a `LEFT JOIN` — a product with no supplier must still appear
with a count of zero. `INNER JOIN` silently drops it.

## Experiment 2 — Online Bookstore

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

Section C also covers `GROUP BY` with `HAVING` — question 35, "customers who
have ordered more than 2 books in total", is the standard `HAVING` question.

## Experiment 3 — Employee Database

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

Section D is the joins section, and the **self join** (each employee with their
manager) is the one most likely to appear in a viva.

## Section E — PL/SQL

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

**The distinction between questions 5 and 6 is the point.** Question 5 is about
individual rows, so it needs `FOR EACH ROW` and `:NEW.salary`. Question 6 is
about *when the statement runs*, so it is statement-level and has no `:NEW` at
all. Be ready to explain why in the viva.

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
