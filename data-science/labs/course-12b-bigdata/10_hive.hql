-- Experiment 10 -- Hive queries for structured data analysis -- tables and partitions
--
-- Run it: hive -f 10_hive.hql, with sales.csv in /user/student/sales. It was run on a Hadoop 3.3.6 cluster where these labs
-- are checked (tools/data-science/hadoop_lab.py), and the lab page shows what it printed.
-- [Changed: this said the file had never been run, as the Hadoop stack could not be
-- installed there. It installs from archive.apache.org: tools/data-science/setup_hadoop.sh.]
--
-- The runnable half is 10_hive_duckdb.py, which runs the same SQL through DuckDB
--
-- run with:  hive -f 10_hive.hql       or  beeline -u jdbc:hive2://localhost:10000

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS retail;
USE retail;

-- Step 2: Lay an external table over the file
-- an EXTERNAL table over data you did not produce: DROP TABLE will not
-- delete the files. Use this for anything you cannot recreate.
CREATE EXTERNAL TABLE IF NOT EXISTS sales_raw (
    date_key   STRING,
    store      STRING,
    region     STRING,
    product    STRING,
    category   STRING,
    qty        INT,
    list_price DOUBLE
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/student/sales/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Step 3: Create the partitioned, bucketed table
-- the table you actually query: PARTITIONED and columnar
CREATE TABLE IF NOT EXISTS sales (
    date_key   STRING,
    store      STRING,
    region     STRING,
    product    STRING,
    category   STRING,
    qty        INT,
    list_price DOUBLE,
    revenue    DOUBLE
)
PARTITIONED BY (quarter STRING)
CLUSTERED BY (store) INTO 3 BUCKETS
STORED AS PARQUET;

-- Step 4: Load it with dynamic partitions
-- dynamic partitioning: Hive reads the LAST select column as the partition
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

INSERT OVERWRITE TABLE sales PARTITION (quarter)
SELECT date_key, store, region, product, category, qty, list_price,
       qty * list_price AS revenue,
       CASE WHEN date_key IN ('D1','D2') THEN 'Q1' ELSE 'Q2' END AS quarter
FROM sales_raw;

SHOW PARTITIONS sales;
DESCRIBE FORMATTED sales;

-- Step 5: Aggregate by region
-- the aggregate verified against Course 11's DAX and experiment 10's DuckDB
SELECT region, SUM(revenue) AS revenue, SUM(qty) AS units
FROM sales
GROUP BY region
ORDER BY revenue DESC;
--   expected: South 10360, North 2520

-- Step 6: Prune a partition
-- PARTITION PRUNING: read one directory, not the table
EXPLAIN DEPENDENCY SELECT SUM(revenue) FROM sales WHERE quarter = 'Q2';
--   input_partitions lists quarter=Q2 alone: one directory is read. If the
--   filter is on a non-partition column it lists every partition, and no
--   amount of indexing will save it -- Hive dropped indexes in version 3.
-- [Corrected: this was a plain EXPLAIN, with the advice to look for
--  "partition values:[Q2]" in the plan. Hive 3's plan does not print that
--  line; its TableScan says 4 rows (Q2's four of nine) but names no partition.
--  EXPLAIN DEPENDENCY names the partitions a query reads.]

SELECT category, product, SUM(qty) AS units, SUM(revenue) AS revenue
FROM sales
WHERE quarter = 'Q2'          -- prunes DIRECTORIES, before the job starts
GROUP BY category, product
HAVING SUM(revenue) > 1000    -- filters GROUPS, in the reducer
ORDER BY revenue DESC;

-- Step 7: Rank with a window function
-- a window function, which is where Hive stops looking like MapReduce
SELECT region, product, revenue,
       RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS rnk
FROM sales;

-- Step 8: Tune, and compute statistics
-- the settings worth knowing
-- SET hive.execution.engine = tez;      -- mr is deprecated and slow
-- [Corrected: this line ran. Tez is a separate install, and where it is not
--  installed the next query dies with NoClassDefFoundError:
--  org/apache/tez/runtime/api/Event -- and the CLI then hangs instead of
--  exiting. Set it only where Tez is installed; this runs on MapReduce.]
SET hive.vectorized.execution.enabled = true;
SET hive.cbo.enable = true;              -- cost-based optimiser, needs stats
ANALYZE TABLE sales PARTITION(quarter) COMPUTE STATISTICS FOR COLUMNS;
