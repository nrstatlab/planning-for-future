# Experiment 3 -- demonstrate the Hadoop architecture components using sample logs
#
# *** NOT EXECUTED ***
# This is the command sequence / program you submit on a real Hadoop cluster.
# Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
# the verification environment -- the Debian repositories that host them are
# blocked by the egress policy -- so this file has NEVER BEEN RUN here.
# Nothing in the notes claims an output for it.
#
# The runnable half is 06_yarn_scheduling.py, which runs the scheduler the logs describe
#
jps                                   # the five daemons, one JVM each

# --- what each daemon writes, and what to read it for ----------------------
tail -f $HADOOP_HOME/logs/hadoop-*-namenode-*.log
#   BlockStateChange lines: every allocation and replication decision
#   "STATE* Safe mode ON" and its exit -- the block-report count
tail -f $HADOOP_HOME/logs/hadoop-*-datanode-*.log
#   "Receiving BP-...:blk_..." -- a block landing, with its pipeline
tail -f $HADOOP_HOME/logs/yarn-*-resourcemanager-*.log
#   "Assigned container container_..." -- the scheduler, deciding
tail -f $HADOOP_HOME/logs/yarn-*-nodemanager-*.log
#   "Starting resource-monitoring for container_..." -- the container's life

# --- run something, then read the logs back --------------------------------
hdfs dfs -put /var/log/syslog /user/student/logs/
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
    wordcount /user/student/logs /user/student/wc-out

yarn application -list -appStates ALL
yarn application -status application_1699999999999_0001
yarn logs -applicationId application_1699999999999_0001   # AGGREGATED logs

# --- the trace to follow, in order -----------------------------------------
#   RM log         : application submitted, ApplicationMaster container assigned
#   NM log         : AM container started
#   RM log         : AM requests N map containers; scheduler assigns them
#   NM logs        : each map task starts, reports progress
#   NameNode log   : block reads served, LOCAL where possible
#   RM log         : reduce containers assigned after map progress passes 5%
#   NM log         : reduce fetches map outputs -- THE SHUFFLE, over HTTP
#   RM log         : application FINISHED, SUCCEEDED
#
# The one line worth finding is the shuffle fetch. It is the only step where
# data crosses the network in bulk, and it is what the combiner in
# experiment 7 exists to shrink.
