# Experiment 6 -- configure YARN, run sample applications, observe ResourceManager and NodeManager roles
#
# *** NOT EXECUTED ***
# This is the command sequence / program you submit on a real Hadoop cluster.
# Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
# the verification environment -- the Debian repositories that host them are
# blocked by the egress policy -- so this file has NEVER BEEN RUN here.
# Nothing in the notes claims an output for it.
#
# The runnable half is 06_yarn_scheduling.py, which runs FIFO, Fair and Capacity on one workload
#
# --- yarn-site.xml, the properties that matter ------------------------------
#   yarn.nodemanager.resource.memory-mb        8192   RAM this node offers
#   yarn.nodemanager.resource.cpu-vcores          8   cores this node offers
#   yarn.scheduler.minimum-allocation-mb       1024   container granularity
#   yarn.scheduler.maximum-allocation-mb       8192   biggest single container
#   yarn.resourcemanager.scheduler.class
#       org.apache.hadoop.yarn.server.resourcemanager.scheduler.
#       capacity.CapacityScheduler
#   yarn.nodemanager.aux-services      mapreduce_shuffle
#       ^ without this the shuffle has no server and every job hangs at 33%

# --- capacity-scheduler.xml -------------------------------------------------
#   yarn.scheduler.capacity.root.queues                 production,adhoc
#   yarn.scheduler.capacity.root.production.capacity    75
#   yarn.scheduler.capacity.root.adhoc.capacity         25
#   yarn.scheduler.capacity.root.adhoc.maximum-capacity 50   <- ELASTICITY

yarn rmadmin -refreshQueues        # queues reload WITHOUT restarting the RM

# --- run the sample applications -------------------------------------------
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
    pi 4 1000
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
    teragen 10000000 /user/student/terasort-in
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
    terasort /user/student/terasort-in /user/student/terasort-out

# submit into a named queue and watch where it lands
yarn jar ...examples-*.jar pi -Dmapreduce.job.queuename=adhoc 4 1000

# --- observe ----------------------------------------------------------------
yarn node -list -all               # every NodeManager, its state and containers
yarn queue -status adhoc           # used / guaranteed / maximum capacity
yarn application -list
yarn application -kill application_1699999999999_0002
yarn top                           # like top(1), for the cluster

#   http://localhost:8088/cluster/scheduler   the queue tree, live
#
# What to look for: submit a big job and a small one into different queues,
# and watch the adhoc job start IMMEDIATELY even though production is full.
# That guarantee is what a queue is, and it is the whole answer to
# "what does the Capacity Scheduler do".
