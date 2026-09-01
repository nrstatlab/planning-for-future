# Unit 4 — Structured Query Language

**Syllabus topics:** Introduction, commands in SQL, data types in SQL, Data
Definition Language, selection operation, projection operation, aggregate
functions, Data Manipulation Language, table modification commands, join
operation, set operations, view, sub query.

---

SQL is what the lab exam tests and what you will use for the rest of your
career. Type every example.

Every query in this unit is executable and was verified against the three lab
schemas — see `labs/course-5-dbms/` and run
`python3 tools/run_sql_labs.py`.

## 4.1 SQL command categories

| Category | Commands | Purpose |
|---|---|---|
| **DDL** | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME` | Define structure |
| **DML** | `INSERT`, `UPDATE`, `DELETE` | Change data |
| **DQL** | `SELECT` | Retrieve data |
| **DCL** | `GRANT`, `REVOKE` | Permissions |
| **TCL** | `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Transactions |

**`DELETE` vs `TRUNCATE` vs `DROP`** — a guaranteed exam question:

| | `DELETE` | `TRUNCATE` | `DROP` |
|---|---|---|---|
| Type | DML | DDL | DDL |
| Removes | Selected rows | All rows | The whole table |
| `WHERE` clause | Yes | No | No |
| Rollback | Possible | Not (auto-commits) | Not |
| Speed | Slower (row by row) | Faster | Fast |
| Structure remains | Yes | Yes | **No** |

## 4.2 Data types

| Category | Oracle | Standard / MySQL |
|---|---|---|
| Fixed-length text | `CHAR(n)` | `CHAR(n)` |
| Variable text | `VARCHAR2(n)` | `VARCHAR(n)` |
| Large text | `CLOB` | `TEXT` |
| Integer | `NUMBER(p)` | `INT`, `SMALLINT`, `BIGINT` |
| Decimal | `NUMBER(p,s)` | `DECIMAL(p,s)`, `NUMERIC` |
| Floating point | `FLOAT` | `FLOAT`, `DOUBLE` |
| Date | `DATE` (includes time in Oracle) | `DATE` |
| Timestamp | `TIMESTAMP` | `TIMESTAMP`, `DATETIME` |
| Binary | `BLOB` | `BLOB` |

**`CHAR` vs `VARCHAR`:** `CHAR(10)` always occupies 10 characters, padding with
spaces; `VARCHAR(10)` stores only what you put in. Use `CHAR` for genuinely
fixed-width codes, `VARCHAR` for everything else.

**Oracle's `DATE` includes a time component**, unlike the SQL standard. This
catches people constantly when comparing dates.

## 4.3 Data Definition Language

### CREATE TABLE with constraints

```sql
CREATE TABLE Employees (
    emp_id     INTEGER      PRIMARY KEY,
    first_name VARCHAR(50)  NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    salary     DECIMAL(10,2) CHECK (salary > 0),
    hire_date  DATE         DEFAULT CURRENT_DATE,
    dept_id    INTEGER,
    manager_id INTEGER,
    FOREIGN KEY (dept_id)    REFERENCES Departments(dept_id),
    FOREIGN KEY (manager_id) REFERENCES Employees(emp_id)   -- self-referential
);
```

### The constraints

| Constraint | Enforces |
|---|---|
| `NOT NULL` | The column must have a value |
| `UNIQUE` | No two rows share a value |
| `PRIMARY KEY` | `UNIQUE` + `NOT NULL`; one per table |
| `FOREIGN KEY` | The value must exist in the referenced table |
| `CHECK` | An arbitrary condition |
| `DEFAULT` | A value used when none is supplied |

**`PRIMARY KEY` vs `UNIQUE`:** a primary key cannot be NULL and there is only
one per table; a `UNIQUE` column may accept NULLs and a table may have several.

All six constraint types are exercised and proven in the labs — the runner
deliberately attempts nine illegal operations and confirms each is rejected.

### ALTER TABLE

```sql
ALTER TABLE Employees ADD COLUMN bonus DECIMAL(8,2) DEFAULT 0;
ALTER TABLE Employees DROP COLUMN bonus;
ALTER TABLE Employees MODIFY salary DECIMAL(12,2);        -- Oracle
ALTER TABLE Employees ALTER COLUMN salary TYPE NUMERIC;   -- PostgreSQL
ALTER TABLE Books ADD CONSTRAINT chk_price CHECK (price > 0);
ALTER TABLE Books DROP CONSTRAINT chk_price;
```

`MODIFY` is Oracle/MySQL; PostgreSQL uses `ALTER COLUMN`; **SQLite supports
neither**, and cannot add a constraint after creation. The lab files note this
where it matters.

## 4.4 Data Manipulation Language

```sql
INSERT INTO Products (product_id, product_name, price, stock_qty)
VALUES (1, 'Pen', 10.00, 100);

INSERT INTO Products VALUES (2, 'Notebook', 50.00, 200);    -- all columns, in order

INSERT INTO Products (product_id, product_name, price, stock_qty) VALUES
    (3, 'Stapler', 120.00, 50),
    (4, 'Marker',   25.00, 80);                             -- multi-row

UPDATE Products SET price = price * 1.05 WHERE product_id = 1;

DELETE FROM Suppliers WHERE supplier_id = 105;
```

**`UPDATE` and `DELETE` without a `WHERE` clause affect every row.** This is the
most expensive mistake in SQL. Habit worth forming: write the `WHERE` clause
*first*, run it as a `SELECT` to see which rows match, then convert it to the
`UPDATE` or `DELETE`.

## 4.5 SELECT — projection and selection

```sql
SELECT * FROM Products;                              -- all columns
SELECT product_name, price FROM Products;            -- PROJECTION (π)
SELECT * FROM Products WHERE price > 50;             -- SELECTION (σ)
SELECT DISTINCT dept_id FROM Employees;              -- remove duplicates
```

Note the terminology trap: SQL's **`SELECT` clause performs the projection**,
and the **`WHERE` clause performs the selection**. This is the reverse of what
the keywords suggest, and exams test it.

### WHERE operators

| Operator | Use |
|---|---|
| `=` `<>` `!=` `<` `>` `<=` `>=` | Comparison |
| `BETWEEN a AND b` | Inclusive range |
| `IN (v1, v2, …)` | Membership |
| `LIKE` | Pattern matching |
| `IS NULL` / `IS NOT NULL` | Null test |
| `AND` `OR` `NOT` | Combination |

### LIKE wildcards

| Wildcard | Matches |
|---|---|
| `%` | Any sequence of characters, including none |
| `_` | Exactly one character |

```sql
WHERE name LIKE 'A%'        -- starts with A
WHERE name LIKE '%son'      -- ends with son
WHERE name LIKE '%an%'      -- contains an
WHERE name LIKE '_a%'       -- second letter is a
WHERE name LIKE '_____'     -- exactly five characters
```

### NULL handling — an exam favourite

**NULL means "unknown", not "zero" and not "empty string".**

```sql
WHERE salary = NULL      -- ALWAYS FALSE, never matches anything
WHERE salary IS NULL     -- correct
```

Any arithmetic with NULL yields NULL: `5 + NULL` is NULL. Aggregate functions
**ignore NULLs**, except `COUNT(*)` which counts rows regardless.

```sql
SELECT COUNT(*), COUNT(manager_id) FROM Employees;
-- differ, because employees with no manager have manager_id NULL
```

`COALESCE(x, replacement)` substitutes a value for NULL, and `NVL` does the
same in Oracle.

### ORDER BY

```sql
SELECT name, salary FROM Employees ORDER BY salary DESC, name ASC;
```

`ASC` is the default. Without `ORDER BY` the order is **undefined** — a relation
is a set. Never rely on rows coming back in insertion order.

### Limiting rows

```sql
SELECT * FROM Books ORDER BY price DESC LIMIT 1;                  -- MySQL, SQLite, PostgreSQL
SELECT * FROM Books ORDER BY price DESC FETCH FIRST 1 ROWS ONLY;  -- Oracle 12c+
SELECT * FROM (SELECT * FROM Books ORDER BY price DESC) WHERE ROWNUM <= 1;  -- Oracle 11g
```

## 4.6 Aggregate functions

| Function | Returns |
|---|---|
| `COUNT(*)` | Number of rows |
| `COUNT(col)` | Number of **non-NULL** values |
| `SUM(col)` | Total |
| `AVG(col)` | Mean |
| `MIN(col)` / `MAX(col)` | Smallest / largest |

### GROUP BY and HAVING

```sql
SELECT d.dept_name, COUNT(e.emp_id) AS headcount, AVG(e.salary) AS avg_salary
FROM Departments d
JOIN Employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING AVG(e.salary) > 70000
ORDER BY avg_salary DESC;
```

**`WHERE` vs `HAVING` — asked in nearly every paper:**

| | `WHERE` | `HAVING` |
|---|---|---|
| Filters | Individual **rows** | **Groups** |
| Applied | **Before** grouping | **After** grouping |
| Aggregates allowed | **No** | **Yes** |

```sql
WHERE SUM(quantity) > 2      -- SYNTAX ERROR
HAVING SUM(quantity) > 2     -- correct
```

**Rule:** every column in the `SELECT` list must either appear in `GROUP BY` or
be inside an aggregate function.

### Logical order of evaluation

The clauses are *written* in one order and *evaluated* in another:

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

This explains two things that puzzle people: why `WHERE` cannot use an
aggregate (it runs before grouping), and why a column alias defined in `SELECT`
can be used in `ORDER BY` but not in `WHERE`.

## 4.7 Joins

**The single most important topic in this unit.**

| Join | Returns |
|---|---|
| `INNER JOIN` | Only rows matching in **both** tables |
| `LEFT [OUTER] JOIN` | All rows from the **left**, plus matches; NULLs where none |
| `RIGHT [OUTER] JOIN` | All rows from the **right**, plus matches |
| `FULL [OUTER] JOIN` | All rows from both sides |
| `CROSS JOIN` | Cartesian product — every combination |
| `SELF JOIN` | A table joined to itself |
| `NATURAL JOIN` | Automatic join on identically-named columns |

```sql
-- INNER: employees who have a department
SELECT e.first_name, d.dept_name
FROM Employees e INNER JOIN Departments d ON e.dept_id = d.dept_id;

-- LEFT: every department, even those with no employees
SELECT d.dept_name, e.first_name
FROM Departments d LEFT JOIN Employees e ON d.dept_id = e.dept_id;

-- SELF: each employee with their manager
SELECT e.first_name AS employee, m.first_name AS manager
FROM Employees e LEFT JOIN Employees m ON e.manager_id = m.emp_id;

-- THREE TABLES
SELECT e.first_name, p.project_name, ep.hours_allocated
FROM Employees e
JOIN Employee_Project ep ON e.emp_id = ep.emp_id
JOIN Projects p          ON ep.project_id = p.project_id;
```

**When to use `LEFT JOIN`:** whenever the question says "**including** those
with none" or "**all** departments". An `INNER JOIN` silently drops the empty
ones, which is exactly the wrong answer to that question.

The self join is worth special attention — the Employee table's `manager_id`
references its own primary key, so "list each employee with their manager"
requires joining the table to itself with two aliases.

**Avoid `NATURAL JOIN`.** It joins on *every* commonly-named column, so adding
an unrelated `created_at` column to both tables silently changes the results.

## 4.8 Set operations

| Operation | Returns |
|---|---|
| `UNION` | Rows in either, **duplicates removed** |
| `UNION ALL` | Rows in either, **duplicates kept** — faster |
| `INTERSECT` | Rows in both |
| `EXCEPT` (`MINUS` in Oracle) | Rows in the first but not the second |

```sql
SELECT name FROM Students UNION SELECT name FROM Teachers;
```

**Requirements:** the same number of columns, in the same order, with
compatible data types. `UNION ALL` is faster because it skips the
duplicate-removal sort — use it when you know there are no duplicates or do not
care.

Oracle uses `MINUS`; the standard, PostgreSQL and SQLite use `EXCEPT`. MySQL
supported neither until version 8.0.31.

## 4.9 Subqueries

A query nested inside another.

### Single-row subquery

```sql
SELECT first_name, salary FROM Employees
WHERE salary > (SELECT AVG(salary) FROM Employees);
```

### Multi-row subquery — needs `IN`, `ANY` or `ALL`

```sql
SELECT first_name FROM Employees
WHERE dept_id IN (SELECT dept_id FROM Departments WHERE location = 'New York');

WHERE salary > ALL (SELECT salary FROM Employees WHERE dept_id = 3)   -- above every one
WHERE salary > ANY (SELECT salary FROM Employees WHERE dept_id = 3)   -- above at least one
```

Using `=` where the subquery returns several rows raises an error. Use `IN`.

### Correlated subquery

The inner query references the outer one, so it re-runs for every outer row.

```sql
SELECT e.first_name, e.salary FROM Employees e
WHERE e.salary > (SELECT AVG(salary) FROM Employees WHERE dept_id = e.dept_id);
```

"Employees earning more than their own department's average." Correlated
subqueries are powerful but slow — the inner query runs once per outer row, so
a join is usually faster.

### EXISTS

```sql
SELECT d.dept_name FROM Departments d
WHERE EXISTS (SELECT 1 FROM Employees e WHERE e.dept_id = d.dept_id);
```

`EXISTS` stops at the first match, so it is often faster than `IN` for large
subqueries. `SELECT 1` is conventional — the column list is irrelevant.

### Subquery in FROM (an inline view)

```sql
SELECT dept_id, avg_sal FROM
    (SELECT dept_id, AVG(salary) AS avg_sal FROM Employees GROUP BY dept_id) t
WHERE avg_sal > 60000;
```

## 4.10 Views

A **view** is a stored query that behaves like a table. It holds no data of its
own.

```sql
CREATE VIEW HighEarners AS
SELECT emp_id, first_name, last_name, salary
FROM Employees WHERE salary > 70000;

SELECT * FROM HighEarners;      -- query it like a table

DROP VIEW HighEarners;
```

### Advantages

1. **Security** — expose selected columns while hiding salary or personal data
2. **Simplicity** — hide a complicated multi-table join behind one name
3. **Logical data independence** — the underlying tables can change while the
   view's interface stays constant
4. **Consistency** — one definition of "active customer" used everywhere

### Updatable views

A view is generally updatable only if it selects from a **single table**,
includes its primary key, and contains **no** `DISTINCT`, `GROUP BY`,
aggregates, `UNION` or subqueries in the select list.

A view over a `GROUP BY` cannot be updated: there is no way to know which
underlying rows an average should be changed in.

**Materialized views** (Oracle, PostgreSQL) *do* store their results, trading
freshness for speed. Ordinary views do not.

---

## Exam questions from this unit

**Two marks**

1. Differentiate `DELETE`, `TRUNCATE` and `DROP`.
2. Differentiate `WHERE` and `HAVING`.
3. What is the difference between `UNION` and `UNION ALL`?
4. Why does `WHERE salary = NULL` never match?
5. What is a correlated subquery?

**Five marks**

1. Explain the types of join with examples.
2. Explain the aggregate functions with `GROUP BY` and `HAVING`.
3. Explain views — creation, advantages and updatability.
4. Explain the constraints available in SQL with examples.
5. Explain subqueries with single-row, multi-row and correlated examples.

**Ten marks**

1. Explain SQL commands in detail with DDL, DML, DQL, DCL and TCL examples.
2. Given a schema, write queries demonstrating joins, aggregation, subqueries,
   set operations and views.

## Mistakes that cost marks

- `UPDATE` or `DELETE` with no `WHERE` clause
- `= NULL` instead of `IS NULL`
- An aggregate function in `WHERE` instead of `HAVING`
- A `SELECT` column missing from `GROUP BY`
- `INNER JOIN` where the question asks for "all X, including those with none"
- Using `=` with a subquery that returns several rows
- Assuming rows come back in a particular order without `ORDER BY`
- Mixing dialects — `LIMIT` in Oracle, `MINUS` in PostgreSQL
