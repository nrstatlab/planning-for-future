# Experiment 5 -- simulate NameNode/DataNode failure and observe fault tolerance and recovery
#
# *** NOT EXECUTED ***
# This is the command sequence / program you submit on a real Hadoop cluster.
# Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
# the verification environment -- the Debian repositories that host them are
# blocked by the egress policy -- so this file has NEVER BEEN RUN here.
# Nothing in the notes claims an output for it.
#
# The runnable half is 05_fault_tolerance.py, which models which blocks survive which failures
#
# --- DataNode failure -------------------------------------------------------
hdfs dfsadmin -report | grep -E "Name:|Decommission"
hdfs fsck /user/student/big/big.bin -files -blocks -locations > before.txt

# kill one DataNode (on a multi-node cluster, pick one that holds a replica)
jps | grep DataNode
kill -9 <datanode_pid>

# the file is STILL READABLE, immediately -- other replicas serve it
hdfs dfs -cat /user/student/big/big.bin | wc -c

# the NameNode does not react at once: dfs.heartbeat.interval (3 s) and
# dfs.namenode.heartbeat.recheck-interval (5 min) give
#   10 * 3 + 2 * 300 = 630 seconds  before the node is declared DEAD
sleep 660
hdfs dfsadmin -report | grep -A2 "Dead datanodes"
hdfs fsck / | grep -E "Under-replicated|Missing"
#   under-replicated blocks appear, then disappear as HDFS re-replicates

# bring it back
$HADOOP_HOME/bin/hdfs --daemon start datanode
hdfs fsck / | grep -E "Over-replicated"    # briefly over-replicated, then trimmed

# --- NameNode failure -------------------------------------------------------
jps | grep NameNode
kill -9 <namenode_pid>
hdfs dfs -ls /              # FAILS. The cluster is unusable. Nothing was lost,
                            # but nothing is reachable either.

$HADOOP_HOME/bin/hdfs --daemon start namenode
hdfs dfsadmin -safemode get # ON -- it is collecting block reports
hdfs dfsadmin -safemode wait
#   safe mode leaves once dfs.namenode.safemode.threshold-pct (0.999) of
#   blocks have reported. On a large cluster this takes MINUTES, and it is
#   why HA exists.

# --- what recovery actually reads ------------------------------------------
ls -la /usr/local/hadoop_store/hdfs/namenode/current/
#   fsimage_00000000000000012345   the namespace at a checkpoint
#   edits_inprogress_...           every change since
#   VERSION                        clusterID -- must match the DataNodes'
# The BLOCK MAP is in NONE of these. It is rebuilt from block reports.
