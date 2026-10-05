# Experiment 5 -- simulate NameNode/DataNode failure and observe fault tolerance and recovery
# Run it: bash 05_fault_tolerance.sh, with a cluster running. It was run on a Hadoop 3.3.6 cluster where these labs
# are checked (tools/data-science/hadoop_lab.py), and the lab page shows what it printed.
# [Changed: this said the file had never been run, as the Hadoop stack could not be
# installed there. It installs from archive.apache.org: tools/data-science/setup_hadoop.sh.]
# The runnable half is 05_fault_tolerance.py, which models which blocks survive which failures
# Step 1: Have the 300 MB file
hdfs dfs -test -e /user/student/big/big.bin || {
  dd if=/dev/urandom of=big.bin bs=1M count=300 status=none
  hdfs dfs -mkdir -p /user/student/big && hdfs dfs -put big.bin /user/student/big/; }

# Step 2: Kill a DataNode, and read the file
hdfs dfsadmin -report 2>/dev/null | grep -E "^Name:|Live datanodes"
hdfs fsck /user/student/big/big.bin -files -blocks -locations > before.txt 2>/dev/null
grep -o "DatanodeInfoWithStorage" before.txt | wc -l   # 3 blocks x 3 replicas = 9

# kill one DataNode. jps shows four here -- this cluster runs four on one
# machine, as a multi-node cluster runs one per host -- so pick it by its pid file
jps | grep -c DataNode
kill -9 $(cat ${HADOOP_PID_DIR:-/tmp}/hadoop-$USER-datanode.pid)
# [Corrected: `kill -9 <datanode_pid>` was a placeholder. A DataNode writes its
# pid to $HADOOP_PID_DIR (by default /tmp) as hadoop-<user>-datanode.pid.]

# the file is STILL READABLE, immediately -- other replicas serve it
hdfs dfs -cat /user/student/big/big.bin 2>client.log | wc -c
#   every byte. A client tries a block's replicas in turn: if it tries the dead
#   node first it logs a warning (kept in client.log here) and reads another
#   replica. Which it tries first differs from read to read.

# the NameNode does not react at once: dfs.heartbeat.interval (3 s) and
# dfs.namenode.heartbeat.recheck-interval (5 min) give
#   10 * 3 + 2 * 300 = 630 seconds  before the node is declared DEAD
# This cluster sets the recheck interval to 15 s, so 10 * 3 + 2 * 15 = 60 s:
# Step 3: Wait for it to be declared dead
sleep 75
hdfs dfsadmin -report -dead 2>/dev/null | grep -E "Dead datanodes"
hdfs fsck / 2>/dev/null | grep -E "Under-replicated|Missing blocks:"
#   under-replicated blocks appear, then disappear as HDFS re-replicates --
#   on a cluster this small, within seconds of the node being declared dead,
#   so by now the copies are made. fsck has where every replica now lives:
hdfs fsck /user/student/big/big.bin -files -blocks -locations 2>/dev/null \
  | grep -oE "DatanodeInfoWithStorage\[[0-9.:]+" | sort | uniq -c
#   3 blocks x 3 replicas on the three nodes still alive: each has all three.
#   Whichever blocks the dead node held were copied again.
# [Corrected: this counted the NameNode's "to replicate blk_" log lines, as
# Hadoop 2 logged each order. Hadoop 3 logs them only at DEBUG, so the count
# is 0 however many blocks were copied; where the replicas are is the evidence.]
# [Corrected: this waited 660 s, for the default 630 s. The wait follows the
# setting; dfsadmin -report -dead lists only the dead.]

# Step 4: Bring it back
# bring it back
$HADOOP_HOME/bin/hdfs --daemon start datanode
sleep 15
hdfs fsck / 2>/dev/null | grep -E "Over-replicated"    # briefly over-replicated, then trimmed

# Step 5: Kill the NameNode, and restart it
jps | grep -c NameNode              # NameNode and SecondaryNameNode
kill -9 $(cat ${HADOOP_PID_DIR:-/tmp}/hadoop-$USER-namenode.pid)
hdfs dfs -ls / 2>&1 | grep -m 1 -o "Call From .* failed on connection exception"
                            # FAILS. The cluster is unusable. Nothing was lost,
                            # but nothing is reachable either.

$HADOOP_HOME/bin/hdfs --daemon start namenode
sleep 5
hdfs dfsadmin -safemode get # ON -- it is collecting block reports
hdfs dfsadmin -safemode wait
#   safe mode leaves once dfs.namenode.safemode.threshold-pct (0.999) of
#   blocks have reported. On a large cluster this takes MINUTES, and it is
#   why HA exists.
hdfs dfs -cat /user/student/big/big.bin | wc -c   # every byte, still

# Step 6: Read what recovery reads
ls $(hdfs getconf -confKey dfs.namenode.name.dir | sed 's|^file://||')/current/ | sed -E 's/[0-9]{19}/N/g' | sort -u
#   fsimage_N                      the namespace at a checkpoint
#   edits_N-N, edits_inprogress_N  every change since
#   VERSION                        clusterID -- must match the DataNodes'
# [Corrected: this listed /usr/local/hadoop_store/hdfs/namenode/current, the
# directory experiment 1 configured on its machine. hdfs getconf asks the
# cluster where its own is; the transaction numbers are shown as N.]
# The BLOCK MAP is in NONE of these. It is rebuilt from block reports.
