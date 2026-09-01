# Course 5 — Practice Questions with Solutions

The SQL answers below run against the three lab schemas in
`labs/course-5-dbms/`. Verify any of them with
`python3 tools/run_sql_labs.py`.

---

## Section A — Write the query

Use the Employee schema: `Departments(dept_id, dept_name, location)`,
`Employees(emp_id, first_name, last_name, email, phone, hire_date, job_title,
salary, dept_id, manager_id)`, `Projects(project_id, project_name, start_date,
end_date, dept_id)`, `Employee_Project(emp_id, project_id, hours_allocated)`.

### Q1 — Employees earning above the company average

```sql
SELECT first_name, last_name, salary
FROM Employees
WHERE salary > (SELECT AVG(salary) FROM Employees)
ORDER BY salary DESC;
```

A single-row subquery. The inner query runs once; its one value is compared
against every row.

### Q2 — Employees earning above their **own department's** average

```sql
SELECT e.first_name, e.last_name, e.salary, e.dept_id
FROM Employees e
WHERE e.salary > (SELECT AVG(salary) FROM Employees
                  WHERE dept_id = e.dept_id);
```

A **correlated** subquery — the inner query references `e.dept_id` from the
outer query, so it re-runs for every outer row. Note the difference from Q1:
one comparison value versus one per department.

### Q3 — Every department with its headcount, including empty departments

```sql
SELECT d.dept_name, COUNT(e.emp_id) AS headcount
FROM Departments d
LEFT JOIN Employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY headcount DESC;
```

Two things earn the marks here. **`LEFT JOIN`**, because "including empty
departments" means unmatched rows must survive — an `INNER JOIN` would drop
them. And **`COUNT(e.emp_id)`** rather than `COUNT(*)`: for a department with no
employees, the left join produces one row with all NULLs, so `COUNT(*)` would
report 1 while `COUNT(e.emp_id)` correctly reports 0.

### Q4 — Each employee alongside their manager

```sql
SELECT e.first_name || ' ' || e.last_name AS employee,
       COALESCE(m.first_name || ' ' || m.last_name, 'No manager') AS manager
FROM Employees e
LEFT JOIN Employees m ON e.manager_id = m.emp_id;
```

A **self join** — the table joined to itself with two aliases. `LEFT JOIN`
because top-level managers have `manager_id` NULL and must still appear.
`COALESCE` replaces the resulting NULL with readable text.

### Q5 — Employees working on more than one project

```sql
SELECT e.first_name, e.last_name, COUNT(ep.project_id) AS project_count
FROM Employees e
JOIN Employee_Project ep ON e.emp_id = ep.emp_id
GROUP BY e.emp_id, e.first_name, e.last_name
HAVING COUNT(ep.project_id) > 1;
```

`HAVING`, not `WHERE` — the condition is on an aggregate, which does not exist
until after grouping.

### Q6 — Departments whose average salary exceeds 70,000

```sql
SELECT d.dept_name, ROUND(AVG(e.salary), 2) AS avg_salary
FROM Departments d
JOIN Employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING AVG(e.salary) > 70000;
```

### Q7 — Employees hired in the last 90 days

```sql
-- Oracle
SELECT first_name, hire_date FROM Employees
WHERE hire_date >= SYSDATE - 90;

-- SQLite
SELECT first_name, hire_date FROM Employees
WHERE julianday('now') - julianday(hire_date) <= 90;
```

Date arithmetic is the least portable part of SQL. Oracle subtracts days from
`SYSDATE` directly; SQLite needs `julianday`; MySQL uses `DATE_SUB(NOW(),
INTERVAL 90 DAY)`.

### Q8 — Total hours per project, highest first

```sql
SELECT p.project_name, SUM(ep.hours_allocated) AS total_hours
FROM Projects p
JOIN Employee_Project ep ON p.project_id = ep.project_id
GROUP BY p.project_id, p.project_name
ORDER BY total_hours DESC;
```

---

## Section B — Find and fix the error

### Q9
```sql
SELECT dept_id, AVG(salary) FROM Employees WHERE AVG(salary) > 60000;
```
**Error:** an aggregate in `WHERE`. `WHERE` filters rows *before* grouping, so
the average does not exist yet. There is also no `GROUP BY`.

**Fix:**
```sql
SELECT dept_id, AVG(salary) FROM Employees
GROUP BY dept_id HAVING AVG(salary) > 60000;
```

### Q10
```sql
SELECT first_name, last_name, dept_id FROM Employees GROUP BY dept_id;
```
**Error:** `first_name` and `last_name` are neither in `GROUP BY` nor inside an
aggregate. Which of the many first names in a department should be shown?

**Fix:** either group by all three columns, or aggregate:
```sql
SELECT dept_id, COUNT(*) AS headcount FROM Employees GROUP BY dept_id;
```

### Q11
```sql
SELECT * FROM Employees WHERE manager_id = NULL;
```
**Error:** nothing equals NULL, not even NULL. This returns zero rows always.

**Fix:** `WHERE manager_id IS NULL`

### Q12
```sql
UPDATE Employees SET salary = salary * 1.1;
```
**Error:** no `WHERE` clause — every employee in the company gets a raise.

**Fix:** add a `WHERE`. Better habit: write it as a `SELECT` first to see which
rows match, then convert it.

### Q13
```sql
SELECT e.first_name, d.dept_name
FROM Employees e, Departments d;
```
**Error:** no join condition, so this is a **Cartesian product** — every
employee paired with every department. With 9 employees and 10 departments that
is 90 meaningless rows.

**Fix:**
```sql
SELECT e.first_name, d.dept_name
FROM Employees e JOIN Departments d ON e.dept_id = d.dept_id;
```

---

## Section C — Normalization

### Q14 — Normalize to 3NF

Given:

| student_id | student_name | course_id | course_name | instructor | instructor_office |
|---|---|---|---|---|---|

with key `{student_id, course_id}`.

**Solution.**

**Step 1 — 1NF.** All values are atomic, so it is already in 1NF.

**Step 2 — Functional dependencies.**

- `student_id → student_name` — **partial** (depends on part of the key)
- `course_id → course_name, instructor` — **partial**
- `instructor → instructor_office` — **transitive**

**Step 3 — 2NF.** Remove partial dependencies:

```
STUDENT(student_id PK, student_name)
COURSE(course_id PK, course_name, instructor, instructor_office)
ENROLMENT(student_id FK, course_id FK, PRIMARY KEY(student_id, course_id))
```

**Step 4 — 3NF.** `COURSE` still has `course_id → instructor →
instructor_office`. Remove it:

```
STUDENT(student_id PK, student_name)
INSTRUCTOR(instructor PK, instructor_office)
COURSE(course_id PK, course_name, instructor FK)
ENROLMENT(student_id FK, course_id FK, PRIMARY KEY(student_id, course_id))
```

**Four tables in 3NF.** Every anomaly is resolved: a course can exist with no
students enrolled, an instructor's office is stored once, and deleting the last
enrolment no longer destroys the course.

### Q15 — Which normal form?

`SALES(invoice_no, item_code, item_name, quantity, price)` with key
`{invoice_no, item_code}`.

**Answer: 1NF only.**

`item_code → item_name, price` is a **partial** dependency — those two
attributes depend on only part of the composite key. That violates 2NF.

**Decomposed to 2NF:**
```
ITEM(item_code PK, item_name, price)
SALES(invoice_no FK, item_code FK, quantity, PRIMARY KEY(invoice_no, item_code))
```

There are no transitive dependencies left, so it is now in 3NF too.

---

## Section D — Long answers

### Q16 — ER diagram for a hospital, reduced to tables

**Entities:** PATIENT, DOCTOR, APPOINTMENT, DEPARTMENT, ROOM
**Relationships:** a doctor belongs to a department (1:N); a patient books many
appointments (1:N); a doctor attends many appointments (1:N); a patient may be
admitted to a room (1:1 while admitted)
**Specialization:** DOCTOR → SURGEON, PHYSICIAN (disjoint, partial)

```sql
DEPARTMENT(dept_id PK, dept_name, floor)
DOCTOR(doctor_id PK, name, specialisation, dept_id FK)
SURGEON(doctor_id PK FK, surgeries_performed)
PHYSICIAN(doctor_id PK FK, consultation_fee)
PATIENT(patient_id PK, name, dob, phone, address)
ROOM(room_no PK, room_type, charges_per_day)
ADMISSION(admission_id PK, patient_id FK, room_no FK, admit_date, discharge_date)
APPOINTMENT(appt_id PK, patient_id FK, doctor_id FK, appt_date, diagnosis)
```

Applying the reduction rules: strong entities become tables (Rule 1); the 1:N
relationships put the "one" side's key into the "many" side (Rule 4); the IS-A
subclasses share the superclass primary key (§2.7).

### Q17 — Explain triggers with the two lab examples

Cover: what a trigger is and how it differs from a procedure (fires
automatically; never called); the syntax; the classification by timing
(`BEFORE`, `AFTER`, `INSTEAD OF`) and by level (row vs statement); `:NEW` and
`:OLD`; then both lab triggers, explaining *why* each uses the level it does.

Finish with advantages, disadvantages and the mutating-table restriction. Full
treatment in [unit-5.md §5.8](unit-5.md); the code is in
`04_plsql_oracle.sql`.

**Remember:** triggers are not in the Unit 5 syllabus list, but two of six lab
questions require them.

---

## Quick self-test

1. What is the difference between `DELETE` and `TRUNCATE`?
2. Where does the foreign key go in a 1:N relationship?
3. Which normal form removes transitive dependencies?
4. Why does `COUNT(*)` differ from `COUNT(column)`?
5. What does a `LEFT JOIN` return that an `INNER JOIN` does not?
6. Which trigger timing would you use to validate a row before insertion?
7. What raises `NO_DATA_FOUND`?
8. Can a function be used inside a `SELECT`? Can a procedure?
9. What is the mutating table error?
10. State the entity integrity rule.

**Answers:** 1. `DELETE` is DML, supports `WHERE`, can be rolled back;
`TRUNCATE` is DDL, removes all rows, auto-commits. · 2. On the **many** side. ·
3. **3NF**. · 4. `COUNT(*)` counts rows; `COUNT(column)` skips NULLs. ·
5. Unmatched rows from the left table, padded with NULLs. · 6. **`BEFORE`**,
with `FOR EACH ROW`. · 7. A `SELECT INTO` that returns no rows. · 8. A function
yes; a procedure no. · 9. A row-level trigger querying or modifying the table it
is defined on. · 10. The primary key can never be NULL.
