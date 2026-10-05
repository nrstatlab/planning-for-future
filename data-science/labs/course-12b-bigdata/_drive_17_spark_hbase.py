"""Run 17_spark_hbase.scala in spark-shell, against HBase in standalone mode holding the nine
sales rows.

HBase is started as for 15_hbase.rb, and the nine rows are put into 'sales' with the row key
region#store#date#product, sales:qty and sales:revenue -- the table the Scala reads. Spark is the
PySpark install from tools/data-science/setup_spark.sh, whose spark-shell runs on Java 21; HBase
runs on Java 8. spark-shell -i runs the file and stays at its prompt, so its input is closed: it
prints its banner, the file's output, and the prompt it leaves at."""
import pathlib
import re

import hadoop_lab
import fixtures as f

here = pathlib.Path.cwd()
conf = here / "hbase-conf"
conf.mkdir(exist_ok=True)
(conf / "hbase-site.xml").write_text(hadoop_lab.site({
    "hbase.cluster.distributed": "false",
    "hbase.rootdir": f"file://{here}/hbase-root",
    "hbase.zookeeper.property.dataDir": f"{here}/hbase-zk",
    "hbase.unsafe.stream.capability.enforce": "false",
}))
puts = ["create 'sales', 'info', 'sales'"]
for r in f.SALES_DF.itertuples(index=False):
    key = f"{r.region}#{r.store}#{r.date_key}#{r.product.split()[0]}"
    puts += [f"put 'sales', '{key}', 'sales:qty', '{int(r.qty)}'",
             f"put 'sales', '{key}', 'sales:revenue', '{float(r.revenue):.1f}'"]
puts += ["count 'sales'", "flush 'sales'"]
(here / "load_sales.hbase").write_text("\n".join(puts) + "\n")
spark_home = next(pathlib.Path("/tmp/sparkenv/lib").glob("python3*/site-packages/pyspark"))
hadoop_lab.job("17_spark_hbase.scala", [
    "start-hbase.sh > /dev/null 2>&1",
    "sleep 20",
    "hbase shell -n < load_sales.hbase 2>&1 | grep -E 'row\\(s\\)$|^=> [0-9]+$'",
    "JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64 $SPARK_HOME/bin/spark-shell --master 'local[*]' "
    "--conf spark.ui.enabled=false "
    "--jars $(ls $HBASE_HOME/lib/*.jar | tr '\\n' ',') -i 17_spark_hbase.scala < /dev/null 2>spark.log",
    "awk '/ERROR|Exception/' spark.log | sed -E 's/^[0-9/]+ [0-9:]+ //' | sort -u | head -5",
    "stop-hbase.sh 2>&1 | tail -1",
], hadoop=False, extra_env={"HBASE_CONF_DIR": str(conf), "HBASE_LOG_DIR": str(here / "hbase-logs"),
                            "HBASE_PID_DIR": str(here / "hbase-pids"), "HBASE_ROOT_LOGGER": "ERROR,console",
                            "HBASE_DISABLE_HADOOP_CLASSPATH_LOOKUP": "true",
                            "SPARK_HOME": str(spark_home)})
