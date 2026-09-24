# Experiment 11 -- import data from an RDBMS into Hadoop using Sqoop
#
# *** NOT EXECUTED ***
# This is the command sequence / program you submit on a real Hadoop cluster.
# Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
# the verification environment -- the Debian repositories that host them are
# blocked by the egress policy -- so this file has NEVER BEEN RUN here.
# Nothing in the notes claims an output for it.
#
# The runnable half is 11_sqoop_equivalent.py, which does the same import from a real SQLite database
#
# --- list what is there -----------------------------------------------------
sqoop list-databases --connect jdbc:mysql://dbhost:3306 \
                     --username student --password-file /user/student/.pw
sqoop list-tables --connect jdbc:mysql://dbhost:3306/retail \
                  --username student --password-file /user/student/.pw
# NEVER use --password on the command line: it lands in `ps` and in the
# shell history. --password-file, on HDFS, mode 400.

# --- a full import, parallel by primary key --------------------------------
sqoop import \
  --connect jdbc:mysql://dbhost:3306/retail \
  --username student --password-file /user/student/.pw \
  --table orders \
  --split-by order_id \          # Sqoop runs SELECT MIN/MAX on THIS column
  --num-mappers 4 \              # 4 range queries, 4 connections
  --target-dir /user/student/orders \
  --as-parquetfile \
  --compress --compression-codec snappy \
  --null-string '\\N' --null-non-string '\\N'
#   ^ without the null flags, SQL NULL becomes the literal string "null"
#     and every downstream count is wrong

# --- import a query instead of a table -------------------------------------
sqoop import \
  --connect jdbc:mysql://dbhost:3306/retail \
  --query 'SELECT o.*, c.region FROM orders o JOIN customers c
           ON o.cust_id = c.id WHERE $CONDITIONS' \
  --split-by o.order_id \
  --target-dir /user/student/orders_enriched
#   $CONDITIONS is MANDATORY and not optional decoration: Sqoop substitutes
#   each mapper's range predicate there. Omit it and the import fails.

# --- straight into Hive -----------------------------------------------------
sqoop import ... --hive-import --hive-database retail --hive-table orders \
                 --create-hive-table

# --- incremental ------------------------------------------------------------
sqoop import ... --incremental append       --check-column order_id  --last-value 90
sqoop import ... --incremental lastmodified --check-column updated_at \
                 --last-value '2026-08-01 00:00:00' --merge-key order_id

# a saved job REMEMBERS --last-value for you
sqoop job --create orders_inc -- import ... --incremental append \
          --check-column order_id --last-value 0
sqoop job --exec orders_inc
sqoop job --show orders_inc

# --- export, back to the RDBMS ---------------------------------------------
sqoop export \
  --connect jdbc:mysql://dbhost:3306/retail \
  --table order_summary \
  --export-dir /user/student/out/by_category \
  --update-mode allowinsert --update-key category \
  --batch
#   an export is NOT transactional across mappers. If mapper 3 fails, the
#   rows mappers 1 and 2 wrote are already committed. Use --staging-table
#   when that matters.

# --- the three that bite ----------------------------------------------------
# 1. no primary key and no --split-by  -> Sqoop refuses; use -m 1
# 2. --split-by on a skewed column     -> one mapper does most of the work
# 3. neither mode notices a DELETE     -> re-import fully, periodically
