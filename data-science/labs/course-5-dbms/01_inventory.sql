-- =====================================================================
-- Course 5 (DBMS) Lab -- Experiment 1: Inventory Management
-- Syllabus source: pages 28-29
--
-- NUMBERING NOTE (see SYLLABUS-REVIEW.md finding D4): the official question
-- list skips 3, 13, 20 and 22, and items 6 and 8 are cut off mid-sentence.
-- The missing items are reconstructed below and marked [RECONSTRUCTED] so you
-- can tell them from the official text.
--
-- Dialect: written for SQLite so the queries can be executed and checked
-- (see tools/run_sql_labs.py). Oracle differences are noted inline.
-- =====================================================================

-- ---------------------------------------------------------------------
-- SECTION A: DDL (Data Definition Language)
-- ---------------------------------------------------------------------

-- Q1. Create a database called InventoryDB.
--     Oracle:  CREATE DATABASE is a DBA operation; in practice you use an
--              existing instance and create a schema/user instead:
--                CREATE USER inventory IDENTIFIED BY password;
--     MySQL:   CREATE DATABASE InventoryDB;
--     SQLite:  a database is just a file -- opening it creates it.

-- Q2. Create the Products and Suppliers tables with the specified constraints.
DROP TABLE IF EXISTS Suppliers;
DROP TABLE IF EXISTS Products;

CREATE TABLE Products (
    product_id   INTEGER      PRIMARY KEY,
    product_name VARCHAR(50)  NOT NULL,
    price        DECIMAL(10,2) CHECK (price > 0),
    stock_qty    INTEGER      CHECK (stock_qty >= 0)
);

CREATE TABLE Suppliers (
    supplier_id   INTEGER     PRIMARY KEY,
    supplier_name VARCHAR(50) NOT NULL,
    contact_no    VARCHAR(20) UNIQUE,
    product_id    INTEGER,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Q3. [RECONSTRUCTED -- missing from the official list]
--     Add a column to Products recording when each item was last restocked.
ALTER TABLE Products ADD COLUMN last_restocked DATE;

-- ---------------------------------------------------------------------
-- SECTION B: DML (Data Manipulation Language)
-- ---------------------------------------------------------------------

-- Q4. Insert at least 5 rows into Products (official sample data).
INSERT INTO Products (product_id, product_name, price, stock_qty) VALUES
    (1, 'Pen',         10.00, 100),
    (2, 'Notebook',    50.00, 200),
    (3, 'Stapler',    120.00,  50),
    (4, 'Marker',      25.00,  80),
    (5, 'File Folder', 60.00, 150);

-- Q5. Insert at least 5 rows into Suppliers (official sample data).
INSERT INTO Suppliers (supplier_id, supplier_name, contact_no, product_id) VALUES
    (101, 'StationeryMart', '9876543210', 1),
    (102, 'PaperWorld',     '9876500000', 2),
    (103, 'OfficeSupplies', '9876512345', 3),
    (104, 'MarkerHub',      '9876522222', 4),
    (105, 'FileDepot',      '9876533333', 5);

-- Q6. Update the stock quantity of [a given product -- the official text is
--     truncated here]. Taking 'Pen' as the product:
UPDATE Products SET stock_qty = 150 WHERE product_name = 'Pen';

-- Q7. Delete a supplier with a specific supplier_id.
DELETE FROM Suppliers WHERE supplier_id = 105;

-- Q8. [Official text truncated] Reconstructed as: increase the price of every
--     product by 5%.
UPDATE Products SET price = price * 1.05;

-- ---------------------------------------------------------------------
-- SECTION C: DQL (SELECT queries)
-- ---------------------------------------------------------------------

-- Q9. Display all records from the Products table.
SELECT * FROM Products;

-- Q10. Display only product_name and price of all products.
SELECT product_name, price FROM Products;

-- Q11. List all products with a stock quantity less than 100.
SELECT product_name, stock_qty FROM Products WHERE stock_qty < 100;

-- Q12. Show all products in the 20 to 100 price range.
SELECT product_name, price FROM Products WHERE price BETWEEN 20 AND 100;

-- Q13. [RECONSTRUCTED -- missing from the official list]
--      List all products whose name starts with the letter 'S'.
SELECT product_name FROM Products WHERE product_name LIKE 'S%';

-- Q14. Find the average price of products.
SELECT ROUND(AVG(price), 2) AS average_price FROM Products;

-- Q15. Display the total number of products in the inventory.
SELECT COUNT(*) AS total_products FROM Products;

-- Q16. Show the maximum and minimum stock quantities.
SELECT MAX(stock_qty) AS max_stock, MIN(stock_qty) AS min_stock FROM Products;

-- Q17. Count how many suppliers supply each product.
SELECT p.product_name, COUNT(s.supplier_id) AS supplier_count
FROM Products p
LEFT JOIN Suppliers s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name;

-- Q18. Show all products where price > 50 AND stock_qty > 100.
SELECT product_name, price, stock_qty
FROM Products
WHERE price > 50 AND stock_qty > 100;

-- Q19. Show all products where price < 20 OR stock_qty < 80.
SELECT product_name, price, stock_qty
FROM Products
WHERE price < 20 OR stock_qty < 80;

-- Q20. [RECONSTRUCTED -- missing from the official list]
--      Display products ordered by price, highest first.
SELECT product_name, price FROM Products ORDER BY price DESC;

-- Q21. List all suppliers with the product they supply (INNER JOIN).
SELECT s.supplier_name, p.product_name, p.price
FROM Suppliers s
INNER JOIN Products p ON s.product_id = p.product_id;

-- Q22. [RECONSTRUCTED -- missing from the official list]
--      List every product together with its supplier, including products that
--      have no supplier (LEFT JOIN).
SELECT p.product_name, s.supplier_name
FROM Products p
LEFT JOIN Suppliers s ON p.product_id = s.product_id;

-- Q23. Find products whose name is exactly 5 characters long.
--      SQLite/MySQL/Oracle all support LENGTH().
SELECT product_name FROM Products WHERE LENGTH(product_name) = 5;

-- Q24. Find suppliers who supply products costing more than 100.
SELECT s.supplier_name, p.product_name, p.price
FROM Suppliers s
JOIN Products p ON s.product_id = p.product_id
WHERE p.price > 100;

-- ---------------------------------------------------------------------
-- CONSTRAINT CHECKS -- these SHOULD fail. Run them to prove the constraints
-- are doing their job; the runner expects each to raise an error.
-- ---------------------------------------------------------------------
-- INSERT INTO Products VALUES (6, 'Eraser', -5.00, 10, NULL);  -- CHECK price > 0
-- INSERT INTO Products VALUES (1, 'Duplicate', 10.00, 5, NULL); -- PRIMARY KEY
-- INSERT INTO Suppliers VALUES (106, 'Ghost', '9999999999', 99); -- FOREIGN KEY
