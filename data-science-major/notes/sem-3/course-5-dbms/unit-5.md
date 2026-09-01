# Unit 5 — PL/SQL (and Triggers)

**Syllabus topics:** Introduction, shortcomings of SQL, structure of PL/SQL,
PL/SQL language elements, data types, operator precedence, control structures,
steps to create a PL/SQL program, iterative control, procedures, functions.

---

> ## ⚠ Triggers are examined but are not in this unit's syllabus
>
> The unit list above — copied verbatim — ends at "procedures, functions".
> **Triggers are not mentioned.** Neither are they in Course Outcome 5.
>
> But they *are* required in three separate places:
>
> - **Course Objective 5:** "…incorporating control structures, functions,
>   procedures, and **database triggers**"
> - **The prescribed activities:** "…using Procedures and functions, Control
>   structures (IF, LOOP), **Triggers for automated updates**"
> - **Lab Section E:** questions 5 and 6 are **both** trigger problems
>
> Two of the six PL/SQL lab questions are triggers. Study §5.8 below. See
> [`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D2**.

---

## 5.1 Shortcomings of SQL

SQL is a **declarative** language: you state what you want and the DBMS decides
how to get it. That is its strength, and also its limit.

| Shortcoming | Consequence |
|---|---|
| **No procedural constructs** | No `IF`, no loops, no variables in plain SQL |
| **One statement at a time** | Each is sent, executed and returned separately |
| **Network overhead** | Ten related statements mean ten round trips to the server |
| **No error handling** | A failed statement simply returns an error to the client |
| **No code reuse** | Business logic gets copied into every application |
| **No row-by-row processing** | Cannot easily iterate through a result set |

**PL/SQL** — Procedural Language extensions to SQL — adds all of this. Its
decisive advantage is that a whole block is sent to the server **once** and
executes there, so ten statements cost one round trip rather than ten.

## 5.2 Structure of a PL/SQL block

PL/SQL is a **block-structured** language. Every program is a block with up to
four parts:

```sql
DECLARE                       -- optional: variables, cursors, exceptions
    v_salary NUMBER(10,2);
    v_name   VARCHAR2(50);
BEGIN                         -- mandatory: the executable statements
    SELECT salary, first_name INTO v_salary, v_name
      FROM Employees WHERE emp_id = 101;
    DBMS_OUTPUT.PUT_LINE(v_name || ' earns ' || v_salary);
EXCEPTION                     -- optional: error handling
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No such employee');
END;                          -- mandatory
/
```

| Section | Required? | Contains |
|---|---|---|
| `DECLARE` | Optional | Variables, constants, cursors, user-defined exceptions |
| `BEGIN` | **Mandatory** | The executable statements |
| `EXCEPTION` | Optional | Error handlers |
| `END;` | **Mandatory** | Terminates the block |

**The `/` on its own line** tells SQL*Plus to execute the block. Forgetting it
means nothing happens — the tool waits for more input.

**`SET SERVEROUTPUT ON`** must be run first, or `DBMS_OUTPUT.PUT_LINE` produces
no visible output at all. This is the single most common reason a student's
PL/SQL "does not work" in a lab exam, and it is not an error — the code runs
correctly and the output is simply discarded.

### Types of block

| Type | Description |
|---|---|
| **Anonymous** | Unnamed, not stored; compiled each time |
| **Named** | Procedures and functions, stored in the database |
| **Triggers** | Named blocks fired automatically by events |

## 5.3 Language elements

### Variables and constants

```sql
DECLARE
    v_count     NUMBER := 0;                    -- initialised
    v_name      VARCHAR2(50);
    c_tax_rate  CONSTANT NUMBER := 0.30;        -- cannot be changed
    v_salary    Employees.salary%TYPE;          -- ANCHORED to a column type
    v_emp_row   Employees%ROWTYPE;              -- a whole row
BEGIN
    ...
END;
```

**`%TYPE` and `%ROWTYPE` are the mark-earning features here.** `%TYPE` makes a
variable inherit a column's data type, so if the column changes from
`NUMBER(8,2)` to `NUMBER(12,2)` your code still compiles. `%ROWTYPE` declares a
record matching an entire row, so `v_emp_row.first_name` works without
declaring each field.

### Naming conventions

`v_` for variables, `c_` for constants, `p_` for parameters, `cur_` for cursors.
Not enforced, but expected — and it prevents the classic bug where a parameter
named `emp_id` collides with the column `emp_id` in a `WHERE` clause.

### Data types

| Category | Types |
|---|---|
| Numeric | `NUMBER`, `PLS_INTEGER`, `BINARY_INTEGER`, `FLOAT` |
| Character | `VARCHAR2`, `CHAR`, `LONG`, `CLOB` |
| Date | `DATE`, `TIMESTAMP`, `INTERVAL` |
| Boolean | **`BOOLEAN`** — exists in PL/SQL but **not** in SQL tables |
| Composite | `RECORD`, `TABLE` (collections) |
| LOB | `BLOB`, `CLOB`, `BFILE` |

`BOOLEAN` is PL/SQL-only. You cannot create a table column of type `BOOLEAN` in
Oracle — use `NUMBER(1)` or `CHAR(1)`. That asymmetry is a common exam question.

### Operator precedence

Highest to lowest:

```
**                              exponentiation
+, -                            unary identity and negation
*, /                            multiplication, division
+, -, ||                        addition, subtraction, concatenation
=, <>, <, >, <=, >=, IS NULL,
  LIKE, BETWEEN, IN             comparison
NOT
AND
OR
```

`||` is the **concatenation** operator — Oracle uses it, not `+`.

## 5.4 Control structures

### Conditional

```sql
IF salary > 100000 THEN
    grade := 'A';
ELSIF salary > 50000 THEN            -- ELSIF, not ELSEIF or ELSE IF
    grade := 'B';
ELSE
    grade := 'C';
END IF;                              -- END IF has a space
```

```sql
CASE grade
    WHEN 'A' THEN bonus := 5000;
    WHEN 'B' THEN bonus := 3000;
    ELSE bonus := 1000;
END CASE;

CASE                                 -- searched CASE
    WHEN salary > 100000 THEN grade := 'A';
    WHEN salary > 50000  THEN grade := 'B';
    ELSE grade := 'C';
END CASE;
```

**`ELSIF`** is spelled with no second E. **`END IF`** is two words. Both are
routine syntax-error marks.

### Iterative control

```sql
-- Basic loop -- needs an explicit EXIT or it never ends
LOOP
    v_counter := v_counter + 1;
    EXIT WHEN v_counter > 10;
END LOOP;

-- WHILE loop -- test before each iteration
WHILE v_counter <= 10 LOOP
    v_counter := v_counter + 1;
END LOOP;

-- FOR loop -- the counter is declared implicitly
FOR i IN 1..10 LOOP
    DBMS_OUTPUT.PUT_LINE(i);
END LOOP;

FOR i IN REVERSE 1..10 LOOP          -- counts down: 10, 9, 8 …
    DBMS_OUTPUT.PUT_LINE(i);
END LOOP;

-- CURSOR FOR loop -- opens, fetches and closes automatically
FOR rec IN (SELECT first_name, salary FROM Employees) LOOP
    DBMS_OUTPUT.PUT_LINE(rec.first_name || ': ' || rec.salary);
END LOOP;
```

**In a numeric `FOR` loop the counter is declared automatically** and is
read-only inside the loop — you cannot assign to `i`. Even with `REVERSE`, the
range is written low..high.

## 5.5 Cursors

A **cursor** is a pointer to the result set of a query.

### Implicit cursors

Created automatically for every SQL statement. Their attributes are useful:

| Attribute | Meaning |
|---|---|
| `SQL%FOUND` | TRUE if the statement affected at least one row |
| `SQL%NOTFOUND` | TRUE if it affected none |
| `SQL%ROWCOUNT` | **How many rows were affected** |
| `SQL%ISOPEN` | Always FALSE for implicit cursors |

`SQL%ROWCOUNT` after an `UPDATE` is how you report "5 employees received a
bonus" — used in the `GiveBonus` procedure in the lab.

### Explicit cursors

```sql
DECLARE
    CURSOR cur_emp IS SELECT emp_id, first_name, salary FROM Employees;
    v_emp cur_emp%ROWTYPE;
BEGIN
    OPEN cur_emp;
    LOOP
        FETCH cur_emp INTO v_emp;
        EXIT WHEN cur_emp%NOTFOUND;      -- test AFTER the fetch
        DBMS_OUTPUT.PUT_LINE(v_emp.first_name);
    END LOOP;
    CLOSE cur_emp;
END;
```

The four steps: **DECLARE → OPEN → FETCH → CLOSE**.

`EXIT WHEN cur%NOTFOUND` must come **after** the `FETCH`, or the last row is
processed twice.

A **cursor FOR loop** does all four steps for you and cannot leak an open
cursor — prefer it unless you need fine control.

## 5.6 Exception handling

```sql
BEGIN
    SELECT salary INTO v_salary FROM Employees WHERE emp_id = p_id;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No employee with id ' || p_id);
    WHEN TOO_MANY_ROWS THEN
        DBMS_OUTPUT.PUT_LINE('More than one row matched');
    WHEN OTHERS THEN                          -- catch-all; must be LAST
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END;
```

### Predefined exceptions

| Exception | Raised when |
|---|---|
| `NO_DATA_FOUND` | `SELECT INTO` returns no rows |
| `TOO_MANY_ROWS` | `SELECT INTO` returns more than one row |
| `ZERO_DIVIDE` | Division by zero |
| `DUP_VAL_ON_INDEX` | A unique constraint is violated |
| `INVALID_NUMBER` | A string will not convert to a number |
| `VALUE_ERROR` | An arithmetic or conversion error |
| `CURSOR_ALREADY_OPEN` | Opening an already-open cursor |
| `OTHERS` | Anything not handled above |

**`SELECT INTO` raises `NO_DATA_FOUND` when it finds nothing** — it does not
return NULL. Every `SELECT INTO` should have a handler.

`SQLCODE` gives the error number and `SQLERRM` the message.

### User-defined exceptions

```sql
DECLARE
    e_negative_salary EXCEPTION;
BEGIN
    IF p_salary < 0 THEN
        RAISE e_negative_salary;
    END IF;
EXCEPTION
    WHEN e_negative_salary THEN
        DBMS_OUTPUT.PUT_LINE('Salary cannot be negative');
END;
```

`RAISE_APPLICATION_ERROR(-20001, 'message')` raises an error that reaches the
**calling application**, not just the block. The error number must be between
−20000 and −20999. This is what triggers use to reject a bad row.

## 5.7 Procedures and functions

### Procedure

```sql
CREATE OR REPLACE PROCEDURE GetEmpInfo (p_emp_id IN NUMBER)
IS
    v_name   VARCHAR2(101);
    v_salary Employees.salary%TYPE;
BEGIN
    SELECT first_name || ' ' || last_name, salary
      INTO v_name, v_salary
      FROM Employees WHERE emp_id = p_emp_id;

    DBMS_OUTPUT.PUT_LINE(v_name || ' earns ' || v_salary);
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No employee found');
END;
/

EXEC GetEmpInfo(101);
```

### Function

```sql
CREATE OR REPLACE FUNCTION get_annual_salary (p_emp_id IN NUMBER)
RETURN NUMBER
IS
    v_salary Employees.salary%TYPE;
BEGIN
    SELECT salary INTO v_salary FROM Employees WHERE emp_id = p_emp_id;
    RETURN v_salary * 12;
EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN 0;
END;
/

SELECT first_name, get_annual_salary(emp_id) AS annual FROM Employees;
```

### Procedure vs function — a guaranteed exam question

| | Procedure | Function |
|---|---|---|
| Returns a value | Optional, via `OUT` parameters | **Mandatory**, via `RETURN` |
| `RETURN` clause in the header | No | **Yes** |
| Called as | A statement: `EXEC p;` | Part of an expression |
| Usable in a `SELECT` | **No** | **Yes** (if it modifies nothing) |
| Purpose | Perform an action | Compute a value |

### Parameter modes

| Mode | Direction | Use |
|---|---|---|
| `IN` | Passed in, read-only | The default |
| `OUT` | Returned to the caller | Output values |
| `IN OUT` | Both | Modified in place |

```sql
CREATE OR REPLACE PROCEDURE calc_bonus (
    p_emp_id IN  NUMBER,
    p_bonus  OUT NUMBER)
IS
BEGIN
    SELECT salary * 0.10 INTO p_bonus FROM Employees WHERE emp_id = p_emp_id;
END;
/
```

`IN` parameters cannot be assigned to inside the procedure.

## 5.8 Triggers — off-syllabus but examined

> Not in the Unit 5 topic list, but required by Course Objective 5, the
> prescribed activities, and two of the six PL/SQL lab questions. Finding **D2**.

### What a trigger is

A **stored block that fires automatically** in response to an event — you never
call it. The database calls it for you, and it cannot be bypassed.

```sql
CREATE OR REPLACE TRIGGER trigger_name
{BEFORE | AFTER | INSTEAD OF} {INSERT | UPDATE | DELETE} ON table_name
[FOR EACH ROW]
[WHEN (condition)]
DECLARE
    ...
BEGIN
    ...
END;
/
```

### Classification

**By timing:**

| Timing | Fires | Use for |
|---|---|---|
| `BEFORE` | Before the operation | **Validation** — reject a bad row before it is written |
| `AFTER` | After the operation | **Auditing** — log what happened |
| `INSTEAD OF` | Replaces the operation | Making a complex view updatable |

**By level:**

| Level | Syntax | Fires |
|---|---|---|
| **Row-level** | `FOR EACH ROW` | Once **per affected row** |
| **Statement-level** | omit `FOR EACH ROW` | Once **per statement** |

An `UPDATE` touching 100 rows fires a row-level trigger 100 times and a
statement-level trigger once. Choosing the wrong level is the standard exam
trap.

### `:NEW` and `:OLD`

Available only in **row-level** triggers:

| Pseudo-record | `INSERT` | `UPDATE` | `DELETE` |
|---|---|---|---|
| `:NEW` | The row being inserted | The new values | undefined |
| `:OLD` | undefined | The old values | The row being deleted |

`:NEW` values may be **assigned** in a `BEFORE` trigger — that is how you
default or normalise a column. In an `AFTER` trigger the row is already written,
so assignment is not allowed.

### Lab question 5 — reject a salary below 30,000

```sql
CREATE OR REPLACE TRIGGER trg_min_salary
BEFORE INSERT OR UPDATE OF salary ON Employees
FOR EACH ROW
BEGIN
    IF :NEW.salary < 30000 THEN
        RAISE_APPLICATION_ERROR(
            -20002,
            'Salary cannot be less than 30,000. Attempted: ' || :NEW.salary);
    END IF;
END;
/
```

**`BEFORE`** because the row must be rejected before it is written.
**`FOR EACH ROW`** because the rule is about individual rows.
**`RAISE_APPLICATION_ERROR`** aborts the statement and rolls it back.

### Lab question 6 — block weekend changes

```sql
CREATE OR REPLACE TRIGGER trg_no_weekend_changes
BEFORE INSERT OR UPDATE OR DELETE ON Employees
DECLARE
    v_day VARCHAR2(3);
BEGIN
    v_day := TO_CHAR(SYSDATE, 'DY', 'NLS_DATE_LANGUAGE=ENGLISH');
    IF v_day IN ('SAT', 'SUN') THEN
        RAISE_APPLICATION_ERROR(
            -20003,
            'Changes are not allowed at the weekend (' || v_day || ')');
    END IF;
END;
/
```

**No `FOR EACH ROW`** — this is a **statement-level** trigger, because the rule
concerns *when the statement runs*, not any particular row. Making it row-level
would work but fire needlessly for every row.

Note the explicit `NLS_DATE_LANGUAGE`. Without it, `TO_CHAR(SYSDATE,'DY')`
returns the day name in the session's language, so comparing against
`'SAT'`/`'SUN'` silently fails on a differently-configured session.

### Advantages and disadvantages

**Advantages:** enforce complex business rules that constraints cannot express;
maintain an audit trail; derive values automatically; cannot be bypassed by any
application.

**Disadvantages:** invisible — a debugging session can be baffling until you
discover a trigger is firing; cascading triggers are hard to reason about; they
add overhead to every affected statement; and excessive use scatters business
logic across the database.

### The mutating table error

A row-level trigger **cannot query or modify the table it is defined on**.
Attempting it raises `ORA-04091: table is mutating`. The usual workaround is a
compound trigger or a statement-level trigger. Worth mentioning in a long
answer.

### Managing triggers

```sql
ALTER TRIGGER trg_min_salary DISABLE;
ALTER TRIGGER trg_min_salary ENABLE;
DROP TRIGGER trg_min_salary;
SELECT trigger_name, status FROM user_triggers;
```

---

## 5.9 Steps to create and run a PL/SQL program

1. `SET SERVEROUTPUT ON` — otherwise no output appears
2. Write the block, with `DECLARE` / `BEGIN` / `EXCEPTION` / `END;`
3. Terminate with `/` on its own line
4. Execute — the whole block is sent to the server as one unit
5. For named blocks, `CREATE OR REPLACE` compiles and stores it
6. On a compilation error, `SHOW ERRORS` displays the details
7. Call it with `EXEC procedure_name(args)` or inside a `SELECT` for a function

---

## Exam questions from this unit

**Two marks**

1. State any three shortcomings of SQL that PL/SQL addresses.
2. What are `%TYPE` and `%ROWTYPE`?
3. Differentiate a procedure from a function.
4. What is the difference between a row-level and a statement-level trigger?
5. When are `:NEW` and `:OLD` available?
6. Why must `SET SERVEROUTPUT ON` be run first?

**Five marks**

1. Explain the structure of a PL/SQL block with an example.
2. Explain the control structures available in PL/SQL.
3. Explain cursors — implicit, explicit, and their attributes.
4. Explain exception handling with predefined and user-defined exceptions.
5. Explain triggers — types, timing, levels — with an example.

**Ten marks**

1. Explain PL/SQL in detail — block structure, data types, control structures,
   cursors and exception handling — with examples.
2. Write and explain a procedure, a function and a trigger for a payroll
   system.
3. Explain triggers fully: syntax, classification, `:NEW`/`:OLD`, advantages,
   disadvantages, and the mutating table problem.

## Mistakes that cost marks

- Forgetting `SET SERVEROUTPUT ON` and concluding the code is broken
- Omitting the `/` that executes the block
- Writing `ELSEIF` or `ELSE IF` instead of **`ELSIF`**
- Writing `ENDIF` instead of **`END IF`**
- Forgetting the semicolon after `END`
- Using `+` for concatenation instead of `||`
- No handler for `NO_DATA_FOUND` on a `SELECT INTO`
- Putting `WHEN OTHERS` before the specific handlers
- Testing `%NOTFOUND` before the `FETCH` instead of after
- Using `:NEW` in a statement-level trigger, where it does not exist
- Declaring a table column as `BOOLEAN` — that type is PL/SQL-only
