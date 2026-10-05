-- Experiment 9 -- data analysis with Pig Latin
--
-- Run it: pig -x mapreduce 09_analysis.pig, with the input files on HDFS. It was run on a Hadoop 3.3.6 cluster where these labs
-- are checked (tools/data-science/hadoop_lab.py), and the lab page shows what it printed.
-- [Changed: this said the file had never been run, as the Hadoop stack could not be
-- installed there. It installs from archive.apache.org: tools/data-science/setup_hadoop.sh.]
--
-- The runnable half is 09_pig_equivalent.py, which walks the same dataflow relation by relation
--
-- run with:  pig -x mapreduce 09_analysis.pig
--       or:  pig -x local 09_analysis.pig

-- Step 1: Load the sales
sales = LOAD '/user/student/sales/sales.csv' USING PigStorage(',')
        AS (date_key:chararray, store_name:chararray, region:chararray,
            product:chararray, category:chararray,
            qty:int, list_price:double);

-- [Noted, from running it: sales.csv has a header row, and PigStorage has no
--  idea -- "Successfully read 10 records" for nine sales. The header's qty, the
--  word qty, becomes null and the FILTER below drops it without a word.
--  org.apache.pig.piggybank.storage.CSVExcelStorage can skip a header.]

-- Step 2: Build the dataflow, a relation per step
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

-- Step 3: Describe, illustrate and explain it
DESCRIBE ranked;      -- the SCHEMA, without running anything
ILLUSTRATE ranked;    -- sample rows pushed through EVERY step -- Pig's
                      -- best feature and the one with no SQL equivalent
EXPLAIN -brief ranked;  -- logical, physical and MapReduce plans
                        -- [Changed: -brief leaves the nested plans folded; in
                        --  full they run to some 400 lines]

-- Step 4: Store the result
STORE ranked INTO '/user/student/out/by_category' USING PigStorage(',');
-- ^ NOTHING ABOVE THIS LINE HAS RUN. Pig is lazy: LOAD/FILTER/GROUP build a
--   plan, and STORE or DUMP compiles it into MapReduce jobs and submits them.

-- Step 5: Join the stores, map-side
-- a join, and the hint that decides how it is executed
stores  = LOAD '/user/student/dim/stores.csv' USING PigStorage(',')
          AS (store_name:chararray, city:chararray, region:chararray);
joined  = JOIN priced BY store_name, stores BY store_name USING 'replicated';
--                                              ^^^^^^^^^^^^^^^^^^
--   'replicated' = a MAP-SIDE join: the small relation is loaded into memory
--   on every mapper, so there is NO SHUFFLE. It fails with an OOM if the
--   right-hand relation does not fit. The default is a reduce-side join.
--   Other strategies: 'skewed' (for one hot key), 'merge' (both sorted).
-- [Corrected: the field was called store, and STORE is a Pig keyword in any
--  case. LOAD ... AS accepted it, but JOIN ... BY store, stores BY store
--  failed to parse -- and Pig parses the whole script before it runs any
--  STORE, so the error lost the by_category output above as well.]
DUMP joined;
-- [Changed: DUMP joined is added. Nothing used joined, and Pig is lazy, so
--  the join was never run.]

-- Step 6: Flatten the tags
-- FLATTEN, which has no clean SQL equivalent
tags    = LOAD '/user/student/tags.csv' AS (product:chararray, taglist:chararray);
split_t = FOREACH tags GENERATE product,
              FLATTEN(TOKENIZE(taglist, ';')) AS tag;
DUMP split_t;   -- one row per (product, tag) pair, from one row per product
