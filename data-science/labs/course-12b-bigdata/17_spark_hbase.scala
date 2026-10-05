// Experiment 17 -- process HBase datasets using Spark integration with Hadoop
//
// Run it: the spark-shell command below, with HBase running. It was run on a Hadoop 3.3.6 cluster where these labs
// are checked (tools/data-science/hadoop_lab.py), and the lab page shows what it printed.
// [Changed: this said the file had never been run, as the Hadoop stack could not be
// installed there. It installs from archive.apache.org: tools/data-science/setup_hadoop.sh.]
//
// The runnable half is 17_spark.py, which runs REAL PySpark -- only the HBase connector is missing
//
// run with:
//   spark-shell --master 'local[*]' \
//     --jars $(ls $HBASE_HOME/lib/*.jar | tr '\n' ',') \
//     -i 17_spark_hbase.scala
// [Corrected: the jars were in /usr/lib/hbase/lib, where some distributions put
// HBase; $HBASE_HOME is wherever yours is. `hbase mapredcp` lists the smaller
// set a job needs, and works the same. And --master yarn needs YARN containers
// running Java 17 for Spark 4; this cluster's run Java 8, so this runs
// local[*] -- the same code, on one machine.]

import org.apache.hadoop.hbase.{HBaseConfiguration, CellUtil}
import org.apache.hadoop.hbase.client.Result
import org.apache.hadoop.hbase.io.ImmutableBytesWritable
import org.apache.hadoop.hbase.mapreduce.TableInputFormat
import org.apache.hadoop.hbase.util.Bytes

// Step 1: Configure the HBase connection and scan
val conf = HBaseConfiguration.create()
conf.set("hbase.zookeeper.quorum", "localhost")        // ZooKeeper, again
// [Corrected: the quorum was zk1,zk2,zk3, experiment 16's three hosts. HBase
// here runs its own ZooKeeper, on localhost.]
conf.set(TableInputFormat.INPUT_TABLE, "sales")
// push the scan down: read one region, not the table
conf.set(TableInputFormat.SCAN_ROW_START, "South")
conf.set(TableInputFormat.SCAN_ROW_STOP,  "South~")
conf.set(TableInputFormat.SCAN_COLUMNS,   "sales:revenue sales:qty")

// Step 2: Read the table as an RDD, a partition per region
val hBaseRDD = sc.newAPIHadoopRDD(
  conf,
  classOf[TableInputFormat],
  classOf[ImmutableBytesWritable],
  classOf[Result])

// ONE SPARK PARTITION PER HBASE REGION. That is the whole integration:
// Spark reads regions in parallel, locally, without going through the
// RegionServer's RPC path for bulk scans.
println(s"partitions = ${hBaseRDD.getNumPartitions}")
// [Noted, from running it: straight after the puts this said partitions = 0,
// and every query below came back empty, with no error. The rows were still
// in the memstore, in no store file, so the region's size was 0 -- and
// TableInputFormat made no split for it. `flush 'sales'` in the HBase shell
// first; on a busy table the memstore flushes by itself.]

// Step 3: Map each row to a case class
case class Sale(rowKey: String, region: String, qty: Int, revenue: Double)

val sales = hBaseRDD.map { case (_, result) =>
  val key = Bytes.toString(result.getRow)
  val qty = Option(result.getValue(Bytes.toBytes("sales"), Bytes.toBytes("qty")))
              .map(b => Bytes.toString(b).toInt).getOrElse(0)
  val rev = Option(result.getValue(Bytes.toBytes("sales"), Bytes.toBytes("revenue")))
              .map(b => Bytes.toString(b).toDouble).getOrElse(0.0)
  Sale(key, key.split("#")(0), qty, rev)
}

// Step 4: Query it with Spark SQL
import spark.implicits._
val df = sales.toDF()
df.createOrReplaceTempView("sales")

spark.sql("""
  SELECT region, SUM(revenue) AS revenue, SUM(qty) AS units
  FROM sales GROUP BY region ORDER BY revenue DESC
""").show()
//   expected: South 10360 -- the same number Course 11's DAX, experiment 10's
//   SQL and experiment 17's PySpark all produce.
// [Corrected: this expected North 2520 as well. The scan above reads only the
// rows from 'South' to 'South~' -- that is the point of pushing it down -- so
// North is never read, and the query has one row.]

// --- writing BACK to HBase, in bulk ---------------------------------------
// Never use put() per row from a Spark job: that is one RPC per record and it
// will overwhelm the RegionServers. Write HFiles and load them:
//
//   df.rdd.map(toKeyValue).sortByKey()
//     .saveAsNewAPIHadoopFile(path, classOf[ImmutableBytesWritable],
//                             classOf[KeyValue], classOf[HFileOutputFormat2], conf)
//   LoadIncrementalHFiles.doBulkLoad(new Path(path), admin, table, locator)
//
// Bulk load bypasses the write path entirely -- no WAL, no memstore, no
// flush -- and is one to two orders of magnitude faster than put().

// --- when NOT to do this ---------------------------------------------------
// A full-table Spark scan of HBase is SLOWER than the same data in Parquet,
// because HBase stores every cell with its row key, family, qualifier and
// timestamp. HBase is for random reads and writes; Parquet is for scans.
// If every job you run is a full scan, the data is in the wrong store.
