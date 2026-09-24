-- Experiment 9 -- data analysis with Pig Latin
--
-- *** NOT EXECUTED ***
-- This is the command sequence / program you submit on a real Hadoop cluster.
-- Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
-- the verification environment -- the Debian repositories that host them are
-- blocked by the egress policy -- so this file has NEVER BEEN RUN here.
-- Nothing in the notes claims an output for it.
--
-- The runnable half is 09_pig_equivalent.py, which walks the same dataflow relation by relation
--
-- run with:  pig -x mapreduce 09_analysis.pig
--       or:  pig -x local 09_analysis.pig

sales = LOAD '/user/student/sales/sales.csv' USING PigStorage(',')
        AS (date_key:chararray, store:chararray, region:chararray,
            product:chararray, category:chararray,
            qty:int, list_price:double);

-- a relation per step. This is the point of Pig.
priced   = FOREACH sales GENERATE *, qty * list_price AS revenue;
bulk     = FILTER priced BY qty >= 6;
by_cat   = GROUP bulk BY category;
totals   = FOREACH by_cat GENERATE
               group AS category,
               COUNT(bulk)        AS orders,
               SUM(bulk.qty)      AS units,
               SUM(bulk.revenue)  AS revenue;
ranked   = ORDER totals BY revenue DESC;

DESCRIBE ranked;      -- the SCHEMA, without running anything
ILLUSTRATE ranked;    -- sample rows pushed through EVERY step -- Pig's
                      -- best feature and the one with no SQL equivalent
EXPLAIN ranked;       -- logical, physical and MapReduce plans

STORE ranked INTO '/user/student/out/by_category' USING PigStorage(',');
-- ^ NOTHING ABOVE THIS LINE HAS RUN. Pig is lazy: LOAD/FILTER/GROUP build a
--   plan, and STORE or DUMP compiles it into MapReduce jobs and submits them.

-- a join, and the hint that decides how it is executed
stores  = LOAD '/user/student/dim/stores.csv' USING PigStorage(',')
          AS (store:chararray, city:chararray, region:chararray);
joined  = JOIN priced BY store, stores BY store USING 'replicated';
--                                              ^^^^^^^^^^^^^^^^^^
--   'replicated' = a MAP-SIDE join: the small relation is loaded into memory
--   on every mapper, so there is NO SHUFFLE. It fails with an OOM if the
--   right-hand relation does not fit. The default is a reduce-side join.
--   Other strategies: 'skewed' (for one hot key), 'merge' (both sorted).

-- FLATTEN, which has no clean SQL equivalent
tags    = LOAD '/user/student/tags.csv' AS (product:chararray, taglist:chararray);
split_t = FOREACH tags GENERATE product,
              FLATTEN(TOKENIZE(taglist, ';')) AS tag;
DUMP split_t;   -- one row per (product, tag) pair, from one row per product
