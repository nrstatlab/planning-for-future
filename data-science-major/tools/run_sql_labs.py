#!/usr/bin/env python3
"""Execute the DBMS lab SQL scripts against SQLite and report the results.

The syllabus targets Oracle, but no Oracle instance is available here and the
sqlite3 CLI is not installed either -- so this runner uses Python's built-in
sqlite3 module. Scripts 01-03 are written to run unmodified; the PL/SQL in
04_plsql_oracle.sql is Oracle-only and is NOT executed by this runner.

It also checks that the constraints actually reject bad data, since a CHECK or
FOREIGN KEY that silently does nothing is worse than no constraint at all.

Usage: python3 tools/run_sql_labs.py
"""
import pathlib
import sqlite3
import sys

LAB_DIR = pathlib.Path(__file__).resolve().parent.parent / "labs" / "course-5-dbms"

# Statements that must FAIL, proving each constraint is enforced.
CONSTRAINT_TESTS = {
    "01_inventory.sql": [
        ("CHECK price > 0",
         "INSERT INTO Products (product_id, product_name, price, stock_qty)"
         " VALUES (6, 'Eraser', -5.00, 10)"),
        ("PRIMARY KEY uniqueness",
         "INSERT INTO Products (product_id, product_name, price, stock_qty)"
         " VALUES (1, 'Duplicate', 10.00, 5)"),
        ("NOT NULL on product_name",
         "INSERT INTO Products (product_id, product_name, price, stock_qty)"
         " VALUES (7, NULL, 10.00, 5)"),
    ],
    "02_bookstore.sql": [
        ("UNIQUE email",
         "INSERT INTO Customers (customer_id, first_name, last_name, email, address)"
         " VALUES (208, 'Dup', 'Email', 'alice.s@example.com', 'somewhere')"),
        ("NOT NULL on order_date",
         "INSERT INTO Orders (order_id, customer_id, book_id, order_date, quantity)"
         " VALUES (308, 201, 101, NULL, 1)"),
    ],
    "03_employee.sql": [
        ("CHECK salary > 0",
         "INSERT INTO Employees (emp_id, first_name, last_name, email, phone,"
         " hire_date, job_title, salary, dept_id, manager_id) VALUES"
         " (111, 'Test', 'User', 't@corp.com', '111-222-3333', '2024-01-01',"
         " 'Tester', -5000, 1, NULL)"),
        ("FOREIGN KEY dept_id",
         "UPDATE Employees SET dept_id = 99 WHERE emp_id = 102"),
        ("CHECK phone format",
         "INSERT INTO Employees (emp_id, first_name, last_name, email, phone,"
         " hire_date, job_title, salary, dept_id, manager_id) VALUES"
         " (112, 'Bad', 'Phone', 'b@corp.com', 'not-a-phone', '2024-01-01',"
         " 'Tester', 50000, 1, NULL)"),
        ("UNIQUE dept_name",
         "INSERT INTO Departments (dept_id, dept_name, location)"
         " VALUES (11, 'HR', 'Boston')"),
    ],
}


def strip_comments(line):
    """Remove a trailing -- comment, ignoring -- that appears inside quotes."""
    in_string = False
    for i, ch in enumerate(line):
        if ch == "'":
            in_string = not in_string
        elif ch == "-" and not in_string and line[i:i + 2] == "--":
            return line[:i]
    return line


def split_statements(sql):
    """Split into executable statements, dropping SQL comments.

    Comments must be stripped before splitting: a trailing comment after a
    semicolon ("PRAGMA foreign_keys = ON;  -- note") would otherwise be glued
    onto the front of the next statement and fail to parse.
    """
    cleaned = [strip_comments(line) for line in sql.splitlines()]
    return [s.strip() for s in "\n".join(cleaned).split(";") if s.strip()]


def run_script(path):
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    statements = split_statements(path.read_text())

    executed = queries = 0
    rows_returned = 0
    for stmt in statements:
        try:
            cur = conn.execute(stmt)
        except sqlite3.Error as exc:
            print(f"    ERROR in statement: {stmt.splitlines()[0][:70]}...")
            print(f"      {exc}")
            conn.close()
            return None
        executed += 1
        if stmt.lstrip().upper().startswith("SELECT"):
            queries += 1
            rows_returned += len(cur.fetchall())
    conn.commit()
    return conn, executed, queries, rows_returned


def main():
    total_fail = 0
    for name in ("01_inventory.sql", "02_bookstore.sql", "03_employee.sql"):
        path = LAB_DIR / name
        print(f"{name}")
        result = run_script(path)
        if result is None:
            total_fail += 1
            continue
        conn, executed, queries, rows = result
        print(f"    {executed} statements executed, {queries} SELECT queries, "
              f"{rows} rows returned")

        for label, stmt in CONSTRAINT_TESTS.get(name, []):
            try:
                conn.execute(stmt)
            except sqlite3.Error:
                print(f"    constraint enforced: {label}")
            else:
                print(f"    CONSTRAINT NOT ENFORCED: {label}")
                total_fail += 1
        conn.close()
        print()

    print("04_plsql_oracle.sql   NOT EXECUTED -- Oracle PL/SQL, "
          "desk-checked only (see SYLLABUS-REVIEW.md)")
    print()
    if total_fail:
        print(f"FAILURES: {total_fail}")
        return 1
    print("All SQL labs executed successfully and all constraints enforced.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
