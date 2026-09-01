-- =====================================================================
-- Course 5 (DBMS) Lab -- Experiment 2: Online Bookstore
-- Syllabus source: pages 29-32
--
-- NUMBERING NOTE (SYLLABUS-REVIEW.md finding D4): the official list skips
-- items 12 and 19. Both are reconstructed below, marked [RECONSTRUCTED].
--
-- Dialect: SQLite (executable via tools/run_sql_labs.py). Oracle equivalents
-- for the date functions are given inline -- these differ the most between
-- vendors and are a favourite exam topic.
-- =====================================================================

DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Authors;

-- ---------------------------------------------------------------------
-- SECTION A: DDL (schema design and constraints)
-- ---------------------------------------------------------------------

-- Q1. Create all four tables with primary keys, foreign keys, appropriate
--     data types and NOT NULL constraints.
CREATE TABLE Authors (
    author_id   INTEGER PRIMARY KEY,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    nationality VARCHAR(50)              -- NULL allowed
);

CREATE TABLE Books (
    book_id          INTEGER PRIMARY KEY,
    title            VARCHAR(200) NOT NULL,
    author_id        INTEGER,
    publication_year INTEGER,
    price            DECIMAL(10,2),
    FOREIGN KEY (author_id) REFERENCES Authors(author_id)
);

CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    first_name  VARCHAR(50)  NOT NULL,
    last_name   VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    address     VARCHAR(200) NOT NULL
);

CREATE TABLE Orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER,
    book_id     INTEGER,
    order_date  DATE    NOT NULL,
    quantity    INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (book_id)     REFERENCES Books(book_id)
);

-- Q2. Alter Books so that price must be greater than 0.
--     Oracle:  ALTER TABLE Books ADD CONSTRAINT chk_price CHECK (price > 0);
--     SQLite cannot ADD CONSTRAINT after creation, so the check belongs in
--     CREATE TABLE. Shown here as the Oracle statement, commented out:
--     ALTER TABLE Books ADD CONSTRAINT chk_price CHECK (price > 0);

-- Q3. Add a unique phone_number column to Customers.
ALTER TABLE Customers ADD COLUMN phone_number VARCHAR(15);
CREATE UNIQUE INDEX idx_customers_phone ON Customers(phone_number);
--     Oracle: ALTER TABLE Customers ADD (phone_number VARCHAR2(15) UNIQUE);

-- Q4. Drop the phone_number column from Customers.
DROP INDEX IF EXISTS idx_customers_phone;
ALTER TABLE Customers DROP COLUMN phone_number;

-- ---------------------------------------------------------------------
-- SECTION B: DML
-- ---------------------------------------------------------------------

-- Q5. Insert at least 7 records into each table (official sample data).
INSERT INTO Authors (author_id, first_name, last_name, nationality) VALUES
    (1, 'Jane',    'Austen',         'British'),
    (2, 'George',  'Orwell',         'British'),
    (3, 'Gabriel', 'Garcia Marquez', 'Colombian'),
    (4, 'Toni',    'Morrison',       'American'),
    (5, 'Mark',    'Twain',          'American'),
    (6, 'Harper',  'Lee',            'American'),
    (7, 'Fyodor',  'Dostoevsky',     'Russian');

INSERT INTO Books (book_id, title, author_id, publication_year, price) VALUES
    (101, 'Pride and Prejudice',            1, 1813, 12.99),
    (102, '1984',                           2, 1949,  9.50),
    (103, 'One Hundred Years of Solitude',  3, 1967, 15.00),
    (104, 'Beloved',                        4, 1987, 11.25),
    (105, 'Animal Farm',                    2, 1945,  8.75),
    (106, 'Adventures of Huckleberry Finn', 5, 1884, 10.50),
    (107, 'To Kill a Mockingbird',          6, 1960, 14.00);

INSERT INTO Customers (customer_id, first_name, last_name, email, address) VALUES
    (201, 'Alice',   'Smith',   'alice.s@example.com',   '12 Oak St, London'),
    (202, 'Bob',     'Johnson', 'bob.j@example.com',     '45 Pine Ave, Oxford'),
    (203, 'Charlie', 'Brown',   'charlie.b@example.com', '78 Maple Rd, Bristol'),
    (204, 'Diana',   'Prince',  'diana.p@example.com',   '34 Queen St, York'),
    (205, 'Edward',  'Norton',  'edward.n@example.com',  '22 River Ln, Leeds'),
    (206, 'Fiona',   'Hall',    'fiona.h@example.com',   '56 Lake Dr, Bath'),
    (207, 'Greg',    'Miller',  'greg.m@example.com',    '89 Park Ave, Glasgow');

INSERT INTO Orders (order_id, customer_id, book_id, order_date, quantity) VALUES
    (301, 201, 101, '2025-07-20', 1),
    (302, 202, 102, '2025-07-21', 2),
    (303, 201, 105, '2025-07-22', 1),
    (304, 203, 103, '2025-07-23', 1),
    (305, 204, 106, '2025-07-24', 1),
    (306, 205, 107, '2025-07-25', 3),
    (307, 206, 104, '2025-07-26', 2);

-- Q6. Increase the price of 'Animal Farm' by 10%.
UPDATE Books SET price = price * 1.10 WHERE title = 'Animal Farm';

-- Q7. Delete all orders made before 2025-07-21.
DELETE FROM Orders WHERE order_date < '2025-07-21';

-- Q8. Change the nationality of Gabriel Garcia Marquez to 'Latino-American'.
UPDATE Authors SET nationality = 'Latino-American'
WHERE first_name = 'Gabriel' AND last_name = 'Garcia Marquez';

-- ---------------------------------------------------------------------
-- SECTION C: SELECT queries
-- ---------------------------------------------------------------------

-- Q9. List all books published between 1900 and 2000.
SELECT title, publication_year FROM Books
WHERE publication_year BETWEEN 1900 AND 2000;

-- Q10. Find all customers whose email contains 'example.com'.
SELECT first_name, last_name, email FROM Customers
WHERE email LIKE '%example.com%';

-- Q11. Books priced between 10 and 15 AND published before 1950.
SELECT title, price, publication_year FROM Books
WHERE price BETWEEN 10 AND 15 AND publication_year < 1950;

-- Q12. [RECONSTRUCTED -- missing from the official list]
--      List every book together with its author's full name.
SELECT b.title, a.first_name || ' ' || a.last_name AS author
FROM Books b JOIN Authors a ON b.author_id = a.author_id;
--      Oracle uses || too; MySQL needs CONCAT(a.first_name,' ',a.last_name).

-- Q13. Books priced under 10 OR published after 1980.
SELECT title, price, publication_year FROM Books
WHERE price < 10 OR publication_year > 1980;

-- Q14. Orders placed after 2025-07-22.
SELECT * FROM Orders WHERE order_date > '2025-07-22';

-- Q15. All books written by author_id = 2.
SELECT title FROM Books WHERE author_id = 2;

-- Q16. Customers whose last name starts with 'B'.
SELECT first_name, last_name FROM Customers WHERE last_name LIKE 'B%';

-- Q17. Books with a price NOT between 9 and 13.
SELECT title, price FROM Books WHERE price NOT BETWEEN 9 AND 13;

-- Q18. Books whose publication_year is in (1813, 1945, 1987).
SELECT title, publication_year FROM Books
WHERE publication_year IN (1813, 1945, 1987);

-- Q19. [RECONSTRUCTED -- missing from the official list]
--      Find authors who have no nationality recorded.
SELECT first_name, last_name FROM Authors WHERE nationality IS NULL;
--      Note: use IS NULL, never "= NULL" -- comparing to NULL is never true.

-- Q20. Customers whose address contains the word 'Park'.
SELECT first_name, last_name, address FROM Customers
WHERE address LIKE '%Park%';

-- Q21. All books sorted by price, descending.
SELECT title, price FROM Books ORDER BY price DESC;

-- Q22. Authors in alphabetical order by last_name.
SELECT first_name, last_name FROM Authors ORDER BY last_name ASC;

-- Q23. Orders sorted by order_date, latest first.
SELECT order_id, order_date FROM Orders ORDER BY order_date DESC;

-- ------------------------- DATE FUNCTIONS ---------------------------
-- These differ most between vendors. SQLite versions run; Oracle given.

-- Q24. Orders placed in July 2025.
SELECT order_id, order_date FROM Orders
WHERE strftime('%Y-%m', order_date) = '2025-07';
--      Oracle: WHERE TO_CHAR(order_date, 'YYYY-MM') = '2025-07';

-- Q25. Estimated delivery date, 5 days after the order date.
SELECT order_id, order_date,
       DATE(order_date, '+5 days') AS estimated_delivery
FROM Orders;
--      Oracle: SELECT order_id, order_date, order_date + 5 AS estimated_delivery

-- Q26. Customers who placed an order at a weekend.
--      SQLite %w: 0 = Sunday, 6 = Saturday.
SELECT c.first_name, c.last_name, o.order_date,
       CASE strftime('%w', o.order_date)
            WHEN '0' THEN 'Sunday' WHEN '6' THEN 'Saturday' END AS day_name
FROM Orders o JOIN Customers c ON o.customer_id = c.customer_id
WHERE strftime('%w', o.order_date) IN ('0', '6');
--      Oracle: WHERE TO_CHAR(order_date, 'DY') IN ('SAT', 'SUN');

-- Q27. How many days have passed since the last order.
SELECT MAX(order_date) AS last_order,
       CAST(julianday('now') - julianday(MAX(order_date)) AS INTEGER) AS days_since
FROM Orders;
--      Oracle: SELECT SYSDATE - MAX(order_date) FROM Orders;

-- ------------------------ AGGREGATE FUNCTIONS -----------------------

-- Q28. Total number of books.
SELECT COUNT(*) AS total_books FROM Books;

-- Q29. Average price of all books.
SELECT ROUND(AVG(price), 2) AS average_price FROM Books;

-- Q30. The highest-priced book.
SELECT title, price FROM Books ORDER BY price DESC LIMIT 1;
--      Oracle 12c+: ... ORDER BY price DESC FETCH FIRST 1 ROWS ONLY;

-- Q31. How many orders each customer has placed.
SELECT c.first_name, c.last_name, COUNT(o.order_id) AS order_count
FROM Customers c LEFT JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name;

-- Q32. Total sales (price x quantity) per customer.
SELECT c.first_name, c.last_name,
       ROUND(SUM(b.price * o.quantity), 2) AS total_spent
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Books  b ON o.book_id = b.book_id
GROUP BY c.customer_id, c.first_name, c.last_name;

-- --------------------- GROUP BY and HAVING --------------------------

-- Q33. How many books each author has written.
SELECT a.first_name || ' ' || a.last_name AS author, COUNT(b.book_id) AS books
FROM Authors a LEFT JOIN Books b ON a.author_id = b.author_id
GROUP BY a.author_id, a.first_name, a.last_name;

-- Q34. Total quantity ordered per customer.
SELECT customer_id, SUM(quantity) AS total_quantity
FROM Orders GROUP BY customer_id;

-- Q35. Customers who have ordered more than 2 books in total.
--      HAVING filters groups; WHERE filters rows before grouping. Using
--      WHERE SUM(...) here is a syntax error -- a classic exam trap.
SELECT customer_id, SUM(quantity) AS total_quantity
FROM Orders GROUP BY customer_id HAVING SUM(quantity) > 2;

-- Q36. Total books sold per author.
SELECT a.last_name, SUM(o.quantity) AS copies_sold
FROM Authors a
JOIN Books  b ON a.author_id = b.author_id
JOIN Orders o ON b.book_id = o.book_id
GROUP BY a.author_id, a.last_name
ORDER BY copies_sold DESC;
