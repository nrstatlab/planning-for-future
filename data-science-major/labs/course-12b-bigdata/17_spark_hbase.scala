// Experiment 17 -- process HBase datasets using Spark integration with Hadoop
//
// *** NOT EXECUTED ***
// This is the command sequence / program you submit on a real Hadoop cluster.
// Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
// the verification environment -- the Debian repositories that host them are
// blocked by the egress policy -- so this file has NEVER BEEN RUN here.
// Nothing in the notes claims an output for it.
//
// The runnable half is 17_spark.py, which runs REAL PySpark -- only the HBase connector is missing
//
// run with:
//   spark-shell --master yarn \
//     --jars $(ls /usr/lib/hbase/lib/*.jar | tr '\n' ',') \
//     -i 17_spark_hbase.scala

import org.apache.hadoop.hbase.{HBaseConfiguration, CellUtil}
import org.apache.hadoop.hbase.client.Result
import org.apache.hadoop.hbase.io.ImmutableBytesWritable
import org.apache.hadoop.hbase.mapreduce.TableInputFormat
import org.apache.hadoop.hbase.util.Bytes

val conf = HBaseConfiguration.create()
conf.set("hbase.zookeeper.quorum", "zk1,zk2,zk3")      // ZooKeeper, again
conf.set(TableInputFormat.INPUT_TABLE, "sales")
// push the scan down: read one region, not the table
conf.set(TableInputFormat.SCAN_ROW_START, "South")
conf.set(TableInputFormat.SCAN_ROW_STOP,  "South~")
conf.set(TableInputFormat.SCAN_COLUMNS,   "sales:revenue sales:qty")

val hBaseRDD = sc.newAPIHadoopRDD(
  conf,
  classOf[TableInputFormat],
  classOf[ImmutableBytesWritable],
  classOf[Result])

// ONE SPARK PARTITION PER HBASE REGION. That is the whole integration:
// Spark reads regions in parallel, locally, without going through the
// RegionServer's RPC path for bulk scans.
println(s"partitions = ${hBaseRDD.getNumPartitions}")

case class Sale(rowKey: String, region: String, qty: Int, revenue: Double)

val sales = hBaseRDD.map { case (_, result) =>
  val key = Bytes.toString(result.getRow)
  val qty = Option(result.getValue(Bytes.toBytes("sales"), Bytes.toBytes("qty")))
              .map(b => Bytes.toString(b).toInt).getOrElse(0)
  val rev = Option(result.getValue(Bytes.toBytes("sales"), Bytes.toBytes("revenue")))
              .map(b => Bytes.toString(b).toDouble).getOrElse(0.0)
  Sale(key, key.split("#")(0), qty, rev)
}

import spark.implicits._
val df = sales.toDF()
df.createOrReplaceTempView("sales")

spark.sql("""
  SELECT region, SUM(revenue) AS revenue, SUM(qty) AS units
  FROM sales GROUP BY region ORDER BY revenue DESC
""").show()
//   expected: South 10360, North 2520 -- the same numbers Course 11's DAX,
//   experiment 10's SQL and experiment 17's PySpark all produce.

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
