-- =====================================================================
-- Course 5 (DBMS) Lab -- Experiment 3, Section E: PL/SQL Programming
-- Syllabus source: page 37
--
-- *** NOT EXECUTED IN VERIFICATION ***
-- PL/SQL is Oracle-specific. No Oracle instance is available in the
-- environment where these labs were checked, and SQLite cannot run PL/SQL, so
-- tools/run_sql_labs.py deliberately skips this file. Everything below is
-- written to Oracle syntax and desk-checked by hand -- run it on your college's
-- Oracle installation (SQL*Plus or SQL Developer) before relying on it.
--
-- Two notes before you start:
--   * Triggers are NOT listed in syllabus Unit 5, but questions 5 and 6 below
--     require them, and so do the course objective and the activities. See
--     SYLLABUS-REVIEW.md finding D2.
--   * Question 2 is missing from the official list -- only its tail survives,
--     "If yes, print 'High Salary'; Otherwise print 'Standard Salary'". It is
--     reconstructed below. See finding D4.
--
-- Run SET SERVEROUTPUT ON first, or DBMS_OUTPUT.PUT_LINE prints nothing --
-- the single most common reason a PL/SQL block "does not work" in a lab exam.
-- =====================================================================

SET SERVEROUTPUT ON;

-- ---------------------------------------------------------------------
-- Q1. Procedure GetEmpInfo: take emp_id as input, display name, salary and
--     department.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE GetEmpInfo (p_emp_id IN NUMBER)
IS
    v_first_name Employees.first_name%TYPE;   -- %TYPE inherits the column type,
    v_last_name  Employees.last_name%TYPE;    -- so the code survives a schema
    v_salary     Employees.salary%TYPE;       -- change
    v_dept_name  Departments.dept_name%TYPE;
BEGIN
    SELECT e.first_name, e.last_name, e.salary, d.dept_name
      INTO v_first_name, v_last_name, v_salary, v_dept_name
      FROM Employees e
      JOIN Departments d ON e.dept_id = d.dept_id
     WHERE e.emp_id = p_emp_id;

    DBMS_OUTPUT.PUT_LINE('Employee  : ' || v_first_name || ' ' || v_last_name);
    DBMS_OUTPUT.PUT_LINE('Salary    : ' || TO_CHAR(v_salary, '999,999.99'));
    DBMS_OUTPUT.PUT_LINE('Department: ' || v_dept_name);

EXCEPTION
    -- SELECT INTO raises NO_DATA_FOUND when it matches nothing, and
    -- TOO_MANY_ROWS when it matches more than one. Handle both.
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No employee found with id ' || p_emp_id);
    WHEN TOO_MANY_ROWS THEN
        DBMS_OUTPUT.PUT_LINE('More than one employee matched id ' || p_emp_id);
END;
/

-- Call it:
--   EXEC GetEmpInfo(101);

-- ---------------------------------------------------------------------
-- Q2. [RECONSTRUCTED -- the official question text is missing; only its tail
--     survives as "If yes, print 'High Salary'; Otherwise print 'Standard
--     Salary'".]
--     Reconstructed as: check whether a given employee's salary exceeds
--     60,000 and print the appropriate message.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE CheckSalaryBand (p_emp_id IN NUMBER)
IS
    v_salary Employees.salary%TYPE;
    v_name   VARCHAR2(101);
    c_threshold CONSTANT NUMBER := 60000;
BEGIN
    SELECT salary, first_name || ' ' || last_name
      INTO v_salary, v_name
      FROM Employees
     WHERE emp_id = p_emp_id;

    IF v_salary > c_threshold THEN
        DBMS_OUTPUT.PUT_LINE(v_name || ': High Salary');
    ELSE
        DBMS_OUTPUT.PUT_LINE(v_name || ': Standard Salary');
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No employee found with id ' || p_emp_id);
END;
/

-- ---------------------------------------------------------------------
-- Q3. Display the top 10 rows of the Emp table by job and salary.
--     Uses an explicit cursor -- the syllabus lists iterative control, and
--     cursor FOR loops are the standard way to walk a result set.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE TopTenEmployees
IS
    CURSOR c_top IS
        SELECT emp_id, first_name, last_name, job_title, salary
          FROM Employees
         ORDER BY job_title ASC, salary DESC
         FETCH FIRST 10 ROWS ONLY;      -- Oracle 12c and later
        -- Oracle 11g and earlier:
        --   SELECT * FROM (SELECT ... ORDER BY job_title, salary DESC)
        --    WHERE ROWNUM <= 10;
    v_count NUMBER := 0;
BEGIN
    DBMS_OUTPUT.PUT_LINE(RPAD('ID', 8) || RPAD('Name', 25) ||
                         RPAD('Job Title', 22) || 'Salary');
    DBMS_OUTPUT.PUT_LINE(RPAD('-', 65, '-'));

    -- A cursor FOR loop opens, fetches and closes the cursor for you.
    FOR rec IN c_top LOOP
        v_count := v_count + 1;
        DBMS_OUTPUT.PUT_LINE(
            RPAD(rec.emp_id, 8) ||
            RPAD(rec.first_name || ' ' || rec.last_name, 25) ||
            RPAD(rec.job_title, 22) ||
            TO_CHAR(rec.salary, '999,999.99'));
    END LOOP;

    DBMS_OUTPUT.PUT_LINE('Rows displayed: ' || v_count);
END;
/

-- ---------------------------------------------------------------------
-- Q4. Stored procedure GiveBonus: take a department id, a designation and a
--     bonus amount, and add the bonus to the salary of every employee in that
--     department holding that designation.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE GiveBonus (
    p_dept_id     IN NUMBER,
    p_designation IN VARCHAR2,
    p_bonus       IN NUMBER)
IS
    v_rows_updated NUMBER;
BEGIN
    IF p_bonus <= 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Bonus must be greater than zero');
    END IF;

    UPDATE Employees
       SET salary = salary + p_bonus
     WHERE dept_id = p_dept_id
       AND UPPER(job_title) = UPPER(p_designation);

    v_rows_updated := SQL%ROWCOUNT;   -- implicit cursor attribute

    IF v_rows_updated = 0 THEN
        DBMS_OUTPUT.PUT_LINE('No employee matched department ' || p_dept_id ||
                             ' with designation ' || p_designation);
        ROLLBACK;
    ELSE
        DBMS_OUTPUT.PUT_LINE(v_rows_updated || ' employee(s) received a bonus of '
                             || p_bonus);
        COMMIT;
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
        RAISE;
END;
/

-- Call it:
--   EXEC GiveBonus(2, 'IT Analyst', 5000);

-- ---------------------------------------------------------------------
-- Q5. Trigger: prevent inserting an employee with a salary below 30,000.
--
--     NOTE: triggers are not in syllabus Unit 5 -- see review finding D2.
--     BEFORE INSERT so the row is rejected before it is ever written.
--     FOR EACH ROW makes it a row-level trigger, giving access to :NEW.
-- ---------------------------------------------------------------------
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

-- Test:
--   INSERT INTO Employees VALUES (120, 'Low', 'Paid', 'low@corp.com',
--       '111-222-3333', SYSDATE, 'Intern', 25000, 1, NULL);
--   -- expect ORA-20002

-- ---------------------------------------------------------------------
-- Q6. Trigger: block any insert, update or delete on the employee table at
--     the weekend.
--
--     This is a STATEMENT-level trigger (no FOR EACH ROW) -- the restriction
--     is about when the statement runs, not about any particular row.
--
--     TO_CHAR(SYSDATE,'DY') returns an abbreviated day name in the session's
--     language. Comparing against 'SAT'/'SUN' therefore breaks under a
--     different NLS_DATE_LANGUAGE; passing the language explicitly is safer.
-- ---------------------------------------------------------------------
CREATE OR REPLACE TRIGGER trg_no_weekend_changes
BEFORE INSERT OR UPDATE OR DELETE ON Employees
DECLARE
    v_day VARCHAR2(3);
BEGIN
    v_day := TO_CHAR(SYSDATE, 'DY', 'NLS_DATE_LANGUAGE=ENGLISH');

    IF v_day IN ('SAT', 'SUN') THEN
        RAISE_APPLICATION_ERROR(
            -20003,
            'Changes to the Employees table are not allowed at the weekend ('
            || v_day || ')');
    END IF;
END;
/

-- ---------------------------------------------------------------------
-- BONUS: a FUNCTION, since Unit 5 lists functions alongside procedures and
-- the difference is a standard viva question.
--
--   Procedure: performs an action; called as a statement (EXEC p;)
--   Function : returns a value; called inside an expression (SELECT f() ...)
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION get_annual_salary (p_emp_id IN NUMBER)
RETURN NUMBER
IS
    v_salary Employees.salary%TYPE;
BEGIN
    SELECT salary INTO v_salary FROM Employees WHERE emp_id = p_emp_id;
    RETURN v_salary * 12;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 0;
END;
/

-- Because it is a function, it can be used inside a query:
--   SELECT first_name, get_annual_salary(emp_id) AS annual FROM Employees;
