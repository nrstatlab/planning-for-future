"""Run 11_sqoop.sh against a real MySQL database (MariaDB) and a cluster.

The database is made here: retail.orders holds 90 rows, ten copies of the nine shared sales
rows as 11_sqoop_equivalent.py builds them; retail.customers has no primary key (the case the
script's -m 1 is for); order_summary is the export's target; and the user student has the
password the script's password file holds. Hive's metastore is created for the Hive import.
"""
import pathlib
import shutil

import hadoop_lab
import fixtures as f

rows = []
for i in range(90):
    r = f.SALES_DF.iloc[i % 9]
    rows.append(f"({i + 1}, {i % 6 + 1}, '{r['store']}', '{r['region']}', '{r['product']}', "
                f"'{r['category']}', {int(r['qty'])}, {float(r['revenue'])}, '2026-08-01 09:00:00')")
SQL = f"""
CREATE DATABASE retail;
CREATE TABLE retail.orders (order_id INT PRIMARY KEY, cust_id INT, store VARCHAR(20),
  region VARCHAR(10), product VARCHAR(20), category VARCHAR(20), qty INT, revenue DOUBLE,
  updated_at DATETIME);
INSERT INTO retail.orders VALUES {", ".join(rows)};
CREATE TABLE retail.customers (id INT, name VARCHAR(20), region VARCHAR(10));
INSERT INTO retail.customers VALUES (1,'Asha','South'),(2,'Ravi','South'),(3,'Meena','North'),
  (4,'Kiran','South'),(5,'Bhanu','North'),(6,'Latha','South');
CREATE TABLE retail.order_summary (category VARCHAR(20) PRIMARY KEY, orders INT, units INT,
  revenue DOUBLE);
CREATE USER 'student'@'localhost' IDENTIFIED BY 'student-pw';
CREATE USER 'student'@'127.0.0.1' IDENTIFIED BY 'student-pw';
GRANT ALL ON retail.* TO 'student'@'localhost';
GRANT ALL ON retail.* TO 'student'@'127.0.0.1';
"""
# Sqoop warns, on every command, that HCatalog and Accumulo are missing; the lab uses neither,
# so the two are pointed at an empty folder, which quietens it.
empty = pathlib.Path("no-such-tool").resolve()
empty.mkdir(exist_ok=True)
# Sqoop keeps saved jobs in ~/.sqoop, which would outlive the run; its conf points them at this
# run's folder instead, so each run starts with none.
conf = pathlib.Path("sqoop-conf").resolve()
shutil.copytree(hadoop_lab.PREFIX / hadoop_lab.TOOLS["sqoop"] / "conf", conf, dirs_exist_ok=True)
(conf / "sqoop-site.xml").write_text(hadoop_lab.site({
    "sqoop.metastore.client.autoconnect.url": f"jdbc:hsqldb:file:{conf}/meta.db;shutdown=true"}))
with hadoop_lab.mariadb(SQL):
    hadoop_lab.job("11_sqoop.sh", [
        "hdfs dfs -mkdir -p /user/student /user/hive/warehouse /tmp/hive",
        "hdfs dfs -chmod 733 /tmp/hive && hdfs dfs -chmod g+w /user/hive/warehouse",
        "schematool -dbType derby -initSchema 2>&1 | grep -E 'schemaTool completed'",
        "hive -e 'CREATE DATABASE retail' 2>/dev/null | grep -v '^WARN'",
    ], then_file=True, extra_env={"HCAT_HOME": str(empty), "ACCUMULO_HOME": str(empty),
                                 "SQOOP_CONF_DIR": str(conf)})
