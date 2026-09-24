-- Experiment 10 -- Hive queries for structured data analysis -- tables and partitions
--
-- *** NOT EXECUTED ***
-- This is the command sequence / program you submit on a real Hadoop cluster.
-- Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
-- the verification environment -- the Debian repositories that host them are
-- blocked by the egress policy -- so this file has NEVER BEEN RUN here.
-- Nothing in the notes claims an output for it.
--
-- The runnable half is 10_hive_duckdb.py, which runs the same SQL through DuckDB
--
-- run with:  hive -f 10_hive.hql       or  beeline -u jdbc:hive2://localhost:10000

CREATE DATABASE IF NOT EXISTS retail;
USE retail;

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

-- the aggregate verified against Course 11's DAX and experiment 10's DuckDB
SELECT region, SUM(revenue) AS revenue, SUM(qty) AS units
FROM sales
GROUP BY region
ORDER BY revenue DESC;
--   expected: South 10360, North 2520

-- PARTITION PRUNING: read one directory, not the table
EXPLAIN SELECT SUM(revenue) FROM sales WHERE quarter = 'Q2';
--   look for "partition values:[Q2]" in the plan. If the filter is on a
--   non-partition column the plan reads everything, and no amount of
--   indexing will save it -- Hive dropped indexes in version 3.

SELECT category, product, SUM(qty) AS units, SUM(revenue) AS revenue
FROM sales
WHERE quarter = 'Q2'          -- prunes DIRECTORIES, before the job starts
GROUP BY category, product
HAVING SUM(revenue) > 1000    -- filters GROUPS, in the reducer
ORDER BY revenue DESC;

-- a window function, which is where Hive stops looking like MapReduce
SELECT region, product, revenue,
       RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS rnk
FROM sales;

-- the settings worth knowing
SET hive.execution.engine = tez;         -- mr is deprecated and slow
SET hive.vectorized.execution.enabled = true;
SET hive.cbo.enable = true;              -- cost-based optimiser, needs stats
ANALYZE TABLE sales PARTITION(quarter) COMPUTE STATISTICS FOR COLUMNS;
