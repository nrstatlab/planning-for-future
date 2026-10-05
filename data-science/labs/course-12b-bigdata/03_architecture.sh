# Experiment 3 -- demonstrate the Hadoop architecture components using sample logs
#
# Run it: bash 03_architecture.sh, with a cluster running. It was run on a Hadoop 3.3.6 cluster where these labs
# are checked (tools/data-science/hadoop_lab.py), and the lab page shows what it printed.
# [Changed: this said the file had never been run, as the Hadoop stack could not be
# installed there. It installs from archive.apache.org: tools/data-science/setup_hadoop.sh.]
#
# The runnable half is 06_yarn_scheduling.py, which runs the scheduler the logs describe
#
# Step 1: List the daemons
jps | awk '{print $2}' | sort         # the daemons, one JVM each

# Step 2: Run a job, and find it
hdfs dfs -mkdir -p /user/student/logs
hdfs dfs -put syslog /user/student/logs/
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
    wordcount /user/student/logs /user/student/wc-out 2>&1 | grep -E "Running job|completed successfully"
# [Corrected: this put /var/log/syslog, which many systems no longer have
# (journald keeps the log instead), into a directory that did not exist yet.
# Any text file will do; syslog here is a few lines of the lab's documents.]

APP=$(yarn application -list -appStates ALL 2>/dev/null | awk '/^application_/{print $1}' | tail -1)
yarn application -list -appStates ALL 2>/dev/null | awk -F'\t' 'NR>1{print $1 " | " $2 " | " $6 " | " $7}'
yarn application -status $APP 2>/dev/null | grep -E "Application-Name|State|Final-State"
sleep 10                              # the NodeManager uploads the logs when the job ends
yarn logs -applicationId $APP 2>/dev/null | grep "^Container: " | sort -u | sed -E 's/ on .*//'
# [Corrected: the commands used application_1699999999999_0001, an id from
# someone else's cluster. Every cluster numbers its own; take it from
# `yarn application -list`.]

# Step 3: Read each daemon's log
# [Corrected: these were `tail -f`, which never returns -- each would have to
# be stopped with Ctrl-C before the next. grep finds the lines described. And
# Hadoop 3 names the YARN logs hadoop-<user>-resourcemanager-<host>.log, not yarn-.]
grep -h -m 2 "BLOCK\* allocate" $HADOOP_LOG_DIR/hadoop-*-namenode-*.log | cut -c 25-
#   BlockStateChange lines: every allocation and replication decision
grep -h -m 1 "Receiving BP-" $HADOOP_LOG_DIR/hadoop-*-datanode-*.log | cut -c 25-
#   "Receiving BP-...:blk_..." -- a block landing, with its pipeline
grep -h -m 2 "Assigned container container_" $HADOOP_LOG_DIR/*-resourcemanager-*.log | cut -c 25-
#   "Assigned container container_..." -- the scheduler, deciding
grep -h -m 1 "Starting resource-monitoring for container_" $HADOOP_LOG_DIR/*-nodemanager-*.log | cut -c 25-
#   "Starting resource-monitoring for container_..." -- the container's life
yarn logs -applicationId $APP 2>/dev/null | grep -m 1 -oE "fetcher#[0-9]+ about to shuffle output of map [^ ]+"
#   in the reduce container's own log: one of the reduce's fetchers asks the
#   NodeManager's shuffle service, over HTTP, for a map's output -- THE SHUFFLE

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
