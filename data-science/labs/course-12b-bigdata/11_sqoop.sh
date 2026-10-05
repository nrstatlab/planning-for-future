# Experiment 11 -- import data from an RDBMS into Hadoop using Sqoop
#
# Run it: bash 11_sqoop.sh, with MySQL and a cluster running. It was run on a Hadoop 3.3.6 cluster where these labs
# are checked (tools/data-science/hadoop_lab.py), and the lab page shows what it printed.
# [Changed: this said the file had never been run, as the Hadoop stack could not be
# installed there. It installs from archive.apache.org: tools/data-science/setup_hadoop.sh.]
#
# The runnable half is 11_sqoop_equivalent.py, which does the same import from a real SQLite database
#
# The database: MySQL (MariaDB) on this machine, with retail.orders -- 90 rows,
# ten copies of the nine shared sales rows -- and retail.customers.
# [Corrected: the commands connected to dbhost, a name for your database
# server; it is localhost here. Every command below ran.]

# Step 1: Store the password
echo -n "student-pw" > .pw
hdfs dfs -put .pw /user/student/.pw && rm .pw
hdfs dfs -chmod 400 /user/student/.pw
# [Changed: these three lines are added -- the commands below read the file.]

# Step 2: List the databases and tables
sqoop list-databases --connect jdbc:mysql://localhost:3306 \
                     --username student --password-file /user/student/.pw 2>/dev/null
sqoop list-tables --connect jdbc:mysql://localhost:3306/retail \
                  --username student --password-file /user/student/.pw 2>/dev/null
# NEVER use --password on the command line: it lands in `ps` and in the
# shell history. --password-file, on HDFS, mode 400.

# Step 3: Import a table, in parallel
#   --split-by order_id   Sqoop runs SELECT MIN/MAX on THIS column
#   --num-mappers 4       4 range queries, 4 connections
#   the null flags        without them, SQL NULL becomes the literal string
#                         "null" and every downstream count is wrong
sqoop import \
  --connect jdbc:mysql://localhost:3306/retail \
  --username student --password-file /user/student/.pw \
  --table orders \
  --split-by order_id \
  --num-mappers 4 \
  --target-dir /user/student/orders \
  --as-parquetfile \
  --compress --compression-codec snappy \
  --null-string '\\N' --null-non-string '\\N' \
  2>&1 | grep -E "BoundingValsQuery|Retrieved [0-9]+ records|ERROR|Exception:" | sed -E 's/^[0-9-]+ [0-9:,]+ //'
hdfs dfs -ls /user/student/orders | awk 'NR>1{print $NF}' | grep -v "^/user/student/orders/\.metadata"
# [Corrected: the comments sat after the backslashes, as `--split-by order_id \  # ...`.
# A backslash then escapes the space, not the newline, so the command ended at the
# comment and each following option ran as a command of its own -- `--num-mappers:
# command not found`. A comment cannot sit on a continued line.]

# Step 4: Import a query
#   $CONDITIONS is MANDATORY and not optional decoration: Sqoop substitutes
#   each mapper's range predicate there. Omit it and the import fails.
sqoop import \
  --connect jdbc:mysql://localhost:3306/retail \
  --username student --password-file /user/student/.pw \
  --query 'SELECT o.*, c.region AS cust_region FROM orders o JOIN customers c
           ON o.cust_id = c.id WHERE $CONDITIONS' \
  --split-by o.order_id \
  --target-dir /user/student/orders_enriched \
  2>&1 | grep -E "Retrieved [0-9]+ records|ERROR|Exception:" | sed -E 's/^[0-9-]+ [0-9:,]+ //'
hdfs dfs -cat /user/student/orders_enriched/part-m-00000 | head -2
# [Corrected: the query was `SELECT o.*, c.region`. orders has a region column
# of its own, so the result had two columns named region, and Sqoop, which makes
# one Java field per column, stopped: "Import failed: Duplicate Column identifier
# specified: 'region'". Every column of a --query import needs its own name.]

# Step 5: Import into Hive
export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$HIVE_HOME/lib/hive-common-3.1.3.jar
# [Corrected: Sqoop reads Hive's settings with Hive's own HiveConf class, and
# without that jar on HADOOP_CLASSPATH it fails with "ClassNotFoundException:
# org.apache.hadoop.hive.conf.HiveConf". Only that jar: with all of Hive's lib/,
# as is often advised, Sqoop runs Hive inside its own JVM, under a security
# manager it installs, and Hive's Derby metastore is refused -- "access denied
# org.apache.derby.security.SystemPermission( "engine", "usederbyinternals" )",
# ten retries, then failure. With just HiveConf it runs the hive command instead.]
sqoop import \
  --connect jdbc:mysql://localhost:3306/retail \
  --username student --password-file /user/student/.pw \
  --table customers -m 1 \
  --hive-import --hive-database retail --hive-table customers \
  --create-hive-table 2>&1 | grep -E "Hive import complete|ERROR|Exception:" | sed -E 's/^[0-9-]+ [0-9:,]+ //'
hive -e "SELECT region, COUNT(*) FROM retail.customers GROUP BY region" 2>/dev/null | grep -v "^WARN"
# [Corrected: this was `sqoop import ... --hive-import`, with three dots where
# the connection and the table go; and a table with no primary key needs -m 1.]

# Step 6: Import only what is new
# ten new orders arrive in the database
mysql -h 127.0.0.1 -u student -pstudent-pw retail -e \
  "INSERT INTO orders SELECT order_id + 90, cust_id, store, region, product, category, qty, revenue, NOW()
   FROM orders WHERE order_id <= 10"
sqoop import \
  --connect jdbc:mysql://localhost:3306/retail \
  --username student --password-file /user/student/.pw \
  --table orders --target-dir /user/student/orders_inc -m 1 \
  --incremental append --check-column order_id --last-value 90 \
  2>&1 | grep -E "Retrieved [0-9]+ records|--last-value|ERROR|Exception:" | sed -E 's/^[0-9-]+ [0-9:,]+ //'
# lastmodified needs a timestamp column, and --merge-key so an updated row
# REPLACES its old copy rather than being added beside it:
#   sqoop import ... --incremental lastmodified --check-column updated_at \
#                    --last-value '2026-08-01 00:00:00' --merge-key order_id

# a saved job REMEMBERS --last-value for you
sqoop job --create orders_inc -- import \
  --connect jdbc:mysql://localhost:3306/retail \
  --username student --password-file /user/student/.pw \
  --table orders --target-dir /user/student/orders_job -m 1 \
  --incremental append --check-column order_id --last-value 0 2>/dev/null
sqoop job --exec orders_inc 2>&1 | grep -E "Retrieved [0-9]+ records|ERROR|Exception:" | sed -E 's/^[0-9-]+ [0-9:,]+ //'
sqoop job --show orders_inc 2>/dev/null | grep -E "incremental.last.value|incremental.col"
# [Corrected: these were `sqoop job --create orders_inc -- import ...`, with the
# connection and table left out as three dots.]
# [Noted: Sqoop 1.4.7 does not ship the org.json jar its saved jobs need. Without
# it, --create fails with "NoClassDefFoundError: org/json/JSONObject" yet keeps
# the job's name, with none of its options, and --exec then says "--table or
# --query is required for import". setup_hadoop.sh adds the jar.]

# Step 7: Export back to the database
#   an export is NOT transactional across mappers. If mapper 3 fails, the
#   rows mappers 1 and 2 wrote are already committed. Use --staging-table
#   when that matters.
mysql -h 127.0.0.1 -u student -pstudent-pw retail -B -N -e \
  "SELECT category, COUNT(*), SUM(qty), SUM(revenue) FROM orders GROUP BY category" \
  | tr '\t' ',' > by_category.csv
hdfs dfs -mkdir -p /user/student/out/by_category
hdfs dfs -put by_category.csv /user/student/out/by_category/
sqoop export \
  --connect jdbc:mysql://localhost:3306/retail \
  --username student --password-file /user/student/.pw \
  --table order_summary \
  --export-dir /user/student/out/by_category \
  --update-mode allowinsert --update-key category \
  --batch 2>&1 | grep -E "Exported [0-9]+ records|ERROR|Exception:" | sed -E 's/^[0-9-]+ [0-9:,]+ //'
mysql -h 127.0.0.1 -u student -pstudent-pw retail -e "SELECT * FROM order_summary ORDER BY category"
# [Changed: the summary to export is made here from the database itself; the
# script assumed it was already on HDFS.]

# --- the three that bite ----------------------------------------------------
# 1. no primary key and no --split-by  -> Sqoop refuses; use -m 1
# 2. --split-by on a skewed column     -> one mapper does most of the work
# 3. neither mode notices a DELETE     -> re-import fully, periodically
