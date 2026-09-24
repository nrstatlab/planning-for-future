-- =====================================================================
-- Course 5 (DBMS) Lab -- Experiment 3: Employee Database
-- Syllabus source: pages 33-37 (Sections A-D; Section E PL/SQL is in
-- 04_plsql_oracle.sql because SQLite cannot execute PL/SQL)
--
-- NUMBERING NOTE (SYLLABUS-REVIEW.md finding D4): the official list skips
-- item 8. It is reconstructed below, marked [RECONSTRUCTED].
--
-- Dialect: SQLite (executable via tools/run_sql_labs.py); Oracle noted inline.
-- =====================================================================

PRAGMA foreign_keys = ON;   -- SQLite needs this; other DBMSs enforce FKs always

DROP TABLE IF EXISTS Employee_Project;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Departments;

-- ---------------------------------------------------------------------
-- SECTION A: DDL
-- ---------------------------------------------------------------------

-- Q1. Create the tables with the specified constraints.
CREATE TABLE Departments (
    dept_id   INTEGER PRIMARY KEY,
    dept_name VARCHAR(50) UNIQUE NOT NULL,
    location  VARCHAR(50) NOT NULL
);

CREATE TABLE Employees (
    emp_id     INTEGER PRIMARY KEY,
    first_name VARCHAR(50)  NOT NULL,
    last_name  VARCHAR(50)  NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    phone      VARCHAR(20)  CHECK (phone LIKE '___-___-____'),
    hire_date  DATE         NOT NULL,
    job_title  VARCHAR(50)  NOT NULL,
    salary     DECIMAL(10,2) CHECK (salary > 0),
    dept_id    INTEGER,
    manager_id INTEGER,
    FOREIGN KEY (dept_id)    REFERENCES Departments(dept_id),
    FOREIGN KEY (manager_id) REFERENCES Employees(emp_id)   -- self-referential
);

CREATE TABLE Projects (
    project_id   INTEGER PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    start_date   DATE NOT NULL,
    end_date     DATE,
    dept_id      INTEGER,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

CREATE TABLE Employee_Project (
    emp_id          INTEGER,
    project_id      INTEGER,
    hours_allocated INTEGER CHECK (hours_allocated > 0),
    PRIMARY KEY (emp_id, project_id),          -- composite key, many-to-many
    FOREIGN KEY (emp_id)     REFERENCES Employees(emp_id),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

-- Q2. Add a bonus column with default 0.
ALTER TABLE Employees ADD COLUMN bonus DECIMAL(8,2) DEFAULT 0;

-- Q3. Drop the bonus column.
ALTER TABLE Employees DROP COLUMN bonus;
--     Oracle: ALTER TABLE Employees DROP COLUMN bonus;

-- ---------------------------------------------------------------------
-- SECTION B: DML
-- ---------------------------------------------------------------------

-- Q4. Insert 10 rows into each table (official sample data).
INSERT INTO Departments (dept_id, dept_name, location) VALUES
    (1,  'HR',            'New York'),
    (2,  'IT',            'San Francisco'),
    (3,  'Finance',       'Chicago'),
    (4,  'Marketing',     'Boston'),
    (5,  'Operations',    'Seattle'),
    (6,  'Legal',         'Washington D.C.'),
    (7,  'Sales',         'Dallas'),
    (8,  'R&D',           'Austin'),
    (9,  'Procurement',   'Denver'),
    (10, 'Customer Care', 'Miami');

-- Managers are inserted before their reports so the self-referential FK holds.
INSERT INTO Employees (emp_id, first_name, last_name, email, phone, hire_date,
                       job_title, salary, dept_id, manager_id) VALUES
    (101, 'Alice',  'Johnson', 'alice.j@corp.com',  '123-456-7890', '2020-03-15', 'HR Manager',         75000, 1, NULL),
    (104, 'Diana',  'Prince',  'diana.p@corp.com',  '456-789-0123', '2018-07-12', 'IT Manager',         90000, 2, NULL),
    (106, 'Fiona',  'Hall',    'fiona.h@corp.com',  '678-901-2345', '2017-11-01', 'Finance Manager',    85000, 3, NULL),
    (102, 'Bob',    'Smith',   'bob.s@corp.com',    '234-567-8901', '2019-05-20', 'IT Analyst',         65000, 2, 104),
    (103, 'Charlie','Brown',   'charlie.b@corp.com','345-678-9012', '2021-01-10', 'Finance Executive',  58000, 3, 106),
    (105, 'Ethan',  'Hunt',    'ethan.h@corp.com',  '567-890-1234', '2022-02-25', 'Marketing Lead',     62000, 4, NULL),
    (107, 'Greg',   'Miles',   'greg.m@corp.com',   '789-012-3456', '2023-04-15', 'IT Support',         45000, 2, 104),
    (108, 'Hannah', 'White',   'hannah.w@corp.com', '890-123-4567', '2021-09-05', 'HR Executive',       50000, 1, 101),
    (109, 'Ian',    'Scott',   'ian.s@corp.com',    '901-234-5678', '2020-11-20', 'Operations Analyst', 56000, 5, NULL),
    (110, 'Julia',  'Adams',   'julia.a@corp.com',  '012-345-6789', '2019-12-18', 'Legal Advisor',      70000, 6, NULL);

INSERT INTO Projects (project_id, project_name, start_date, end_date, dept_id) VALUES
    (201, 'Payroll System',     '2023-01-01', NULL, 3),
    (202, 'Website Upgrade',    '2023-02-10', NULL, 2),
    (203, 'Recruitment Drive',  '2023-03-05', NULL, 1),
    (204, 'Ad Campaign',        '2023-05-20', NULL, 4),
    (205, 'New CRM Tool',       '2023-04-15', NULL, 7),
    (206, 'Compliance Portal',  '2023-06-10', NULL, 6),
    (207, 'Inventory System',   '2023-07-01', NULL, 5),
    (208, 'AI Research',        '2023-08-05', NULL, 8),
    (209, 'Customer Feedback',  '2023-09-10', NULL, 10),
    (210, 'Procurement System', '2023-10-01', NULL, 9);

INSERT INTO Employee_Project (emp_id, project_id, hours_allocated) VALUES
    (102, 202, 120), (104, 202,  80), (103, 201, 100), (106, 201, 150),
    (101, 203,  50), (105, 204,  70), (107, 202,  60), (109, 207,  90),
    (110, 206, 110), (108, 203,  40);

-- Q5. Try inserting an employee with a negative salary -- SHOULD FAIL on the
--     CHECK constraint. Commented out so the script completes; the runner
--     tests it separately and expects an error.
-- INSERT INTO Employees VALUES (111,'Test','User','t@corp.com','111-222-3333',
--     '2024-01-01','Tester',-5000,1,NULL);

-- Q6. Increase the salary of emp_id 103 by 15%.
UPDATE Employees SET salary = salary * 1.15 WHERE emp_id = 103;

-- Q7. Delete an employee who has resigned.
--     emp_id 105 is used because nothing references them as a manager.
DELETE FROM Employee_Project WHERE emp_id = 105;   -- clear the child rows first
DELETE FROM Employees WHERE emp_id = 105;

-- Q8. [RECONSTRUCTED -- missing from the official list]
--     Give every IT department employee a 10% raise.
UPDATE Employees SET salary = salary * 1.10
WHERE dept_id = (SELECT dept_id FROM Departments WHERE dept_name = 'IT');

-- Q9. Change an employee's department to 'Research' -- SHOULD FAIL, because no
--     such department exists (foreign key violation). Tested by the runner.
-- UPDATE Employees SET dept_id = 99 WHERE emp_id = 102;

-- ---------------------------------------------------------------------
-- SECTION C: DQL
-- ---------------------------------------------------------------------

-- Q10. List all employees and their details.
SELECT * FROM Employees;

-- Q11. All employees in the HR department.
SELECT e.first_name, e.last_name, e.job_title
FROM Employees e JOIN Departments d ON e.dept_id = d.dept_id
WHERE d.dept_name = 'HR';

-- Q12. Employees with salaries between 50,000 and 80,000.
SELECT first_name, last_name, salary FROM Employees
WHERE salary BETWEEN 50000 AND 80000;

-- Q13. Employees hired after 2020.
SELECT first_name, last_name, hire_date FROM Employees
WHERE hire_date > '2020-12-31';

-- Q14. Employees in either the IT or Finance department.
SELECT e.first_name, e.last_name, d.dept_name
FROM Employees e JOIN Departments d ON e.dept_id = d.dept_id
WHERE d.dept_name IN ('IT', 'Finance');

-- Q15. Employees whose email ends with '@corp.com'.
SELECT first_name, email FROM Employees WHERE email LIKE '%@corp.com';

-- Q16. Salary > 60,000 AND located in New York.
SELECT e.first_name, e.last_name, e.salary, d.location
FROM Employees e JOIN Departments d ON e.dept_id = d.dept_id
WHERE e.salary > 60000 AND d.location = 'New York';

-- Q17. Employees in descending order of salary.
SELECT first_name, last_name, salary FROM Employees ORDER BY salary DESC;

-- Q18. Number of employees in each department.
SELECT d.dept_name, COUNT(e.emp_id) AS employee_count
FROM Departments d LEFT JOIN Employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name;

-- Q19. Average salary department-wise.
SELECT d.dept_name, ROUND(AVG(e.salary), 2) AS avg_salary
FROM Departments d JOIN Employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name;

-- Q20. Departments where the average salary exceeds 70,000.
SELECT d.dept_name, ROUND(AVG(e.salary), 2) AS avg_salary
FROM Departments d JOIN Employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING AVG(e.salary) > 70000;

-- Q21. Number of employees on each project.
SELECT p.project_name, COUNT(ep.emp_id) AS employee_count
FROM Projects p LEFT JOIN Employee_Project ep ON p.project_id = ep.project_id
GROUP BY p.project_id, p.project_name;

-- Q22. Departments with more than 3 employees.
SELECT d.dept_name, COUNT(e.emp_id) AS employee_count
FROM Departments d JOIN Employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING COUNT(e.emp_id) > 3;

-- Q23. Sum of all salaries department-wise.
SELECT d.dept_name, SUM(e.salary) AS total_salary
FROM Departments d JOIN Employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name;

-- Q24. Distinct department IDs present in Employees.
SELECT DISTINCT dept_id FROM Employees ORDER BY dept_id;

-- Q25. Employee names with their year of hire.
SELECT first_name, last_name, strftime('%Y', hire_date) AS hire_year
FROM Employees;
--      Oracle: TO_CHAR(hire_date, 'YYYY') or EXTRACT(YEAR FROM hire_date)

-- Q26. Employees grouped by year of hire.
SELECT strftime('%Y', hire_date) AS hire_year, COUNT(*) AS employees
FROM Employees GROUP BY hire_year ORDER BY hire_year;

-- Q27. Employees hired in the last 90 days.
SELECT first_name, last_name, hire_date FROM Employees
WHERE julianday('now') - julianday(hire_date) <= 90;
--      Oracle: WHERE hire_date >= SYSDATE - 90;
--      (The sample data is from 2017-2023, so this correctly returns nothing.)

-- Q28. Years of experience of every employee.
SELECT first_name, last_name, hire_date,
       CAST((julianday('now') - julianday(hire_date)) / 365.25 AS INTEGER)
           AS years_experience
FROM Employees ORDER BY years_experience DESC;
--      Oracle: MONTHS_BETWEEN(SYSDATE, hire_date)/12

-- ---------------------------------------------------------------------
-- SECTION D: Joins
-- ---------------------------------------------------------------------

-- Q29. All employees with their department names (INNER JOIN).
SELECT e.first_name, e.last_name, d.dept_name
FROM Employees e INNER JOIN Departments d ON e.dept_id = d.dept_id;

-- Q30. All departments with employees, including empty departments (LEFT JOIN).
SELECT d.dept_name, e.first_name, e.last_name
FROM Departments d LEFT JOIN Employees e ON d.dept_id = e.dept_id
ORDER BY d.dept_name;

-- Q31. Employees and the projects they work on (three-table join).
SELECT e.first_name, e.last_name, p.project_name, ep.hours_allocated
FROM Employees e
JOIN Employee_Project ep ON e.emp_id = ep.emp_id
JOIN Projects p          ON ep.project_id = p.project_id
ORDER BY e.first_name;

-- Q32. Projects with the total hours allocated.
SELECT p.project_name, SUM(ep.hours_allocated) AS total_hours
FROM Projects p JOIN Employee_Project ep ON p.project_id = ep.project_id
GROUP BY p.project_id, p.project_name
ORDER BY total_hours DESC;

-- Q33. Employees working on more than one project.
SELECT e.first_name, e.last_name, COUNT(ep.project_id) AS project_count
FROM Employees e JOIN Employee_Project ep ON e.emp_id = ep.emp_id
GROUP BY e.emp_id, e.first_name, e.last_name
HAVING COUNT(ep.project_id) > 1;

-- Q34. All projects handled by the Finance department.
SELECT p.project_name, p.start_date
FROM Projects p JOIN Departments d ON p.dept_id = d.dept_id
WHERE d.dept_name = 'Finance';

-- BONUS: SELF JOIN -- each employee alongside their manager. The syllabus
-- defines manager_id as self-referential, so this is a likely exam question.
SELECT e.first_name || ' ' || e.last_name AS employee,
       COALESCE(m.first_name || ' ' || m.last_name, 'No manager') AS manager
FROM Employees e LEFT JOIN Employees m ON e.manager_id = m.emp_id;
