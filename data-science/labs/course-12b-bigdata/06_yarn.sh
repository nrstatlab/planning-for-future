# Experiment 6 -- configure YARN, run sample applications, observe ResourceManager and NodeManager roles
#
# Run it: bash 06_yarn.sh, with a cluster running. It was run on a Hadoop 3.3.6 cluster where these labs
# are checked (tools/data-science/hadoop_lab.py), and the lab page shows what it printed.
# [Changed: this said the file had never been run, as the Hadoop stack could not be
# installed there. It installs from archive.apache.org: tools/data-science/setup_hadoop.sh.]
#
# The runnable half is 06_yarn_scheduling.py, which runs FIFO, Fair and Capacity on one workload
#
# Step 1: Read the configuration that matters
#   yarn.nodemanager.resource.memory-mb        8192   RAM this node offers
#   yarn.nodemanager.resource.cpu-vcores          8   cores this node offers
#   yarn.scheduler.minimum-allocation-mb       1024   container granularity
#   yarn.scheduler.maximum-allocation-mb       8192   biggest single container
#   yarn.resourcemanager.scheduler.class
#       org.apache.hadoop.yarn.server.resourcemanager.scheduler.
#       capacity.CapacityScheduler
#   yarn.nodemanager.aux-services      mapreduce_shuffle
#       ^ without this the shuffle has no server and every job hangs at 33%

# Step 2: Set up the queues
#   yarn.scheduler.capacity.root.queues                 production,adhoc
#   yarn.scheduler.capacity.root.production.capacity    75
#   yarn.scheduler.capacity.root.adhoc.capacity         25
#   yarn.scheduler.capacity.root.adhoc.maximum-capacity 50   <- ELASTICITY

yarn rmadmin -refreshQueues        # queues reload WITHOUT restarting the RM
yarn queue -status production 2>/dev/null | grep -E "Queue Name|Capacity"
yarn queue -status adhoc 2>/dev/null | grep -E "Queue Name|Capacity"

# Step 3: Run the sample applications
EX=$(ls $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar)
yarn jar $EX pi 4 1000 2>&1 | grep -E "Estimated value|Job Finished"
yarn jar $EX teragen 100000 /user/student/terasort-in 2>&1 | grep -E "completed successfully"
yarn jar $EX terasort /user/student/terasort-in /user/student/terasort-out 2>&1 | grep -E "completed successfully"
yarn jar $EX teravalidate /user/student/terasort-out /user/student/terasort-check 2>&1 | grep -E "completed successfully"
hdfs dfs -cat /user/student/terasort-check/part-r-00000
#   no "misorder" line: the output is in order. The checksum is of the rows.
# [Corrected: teragen wrote 10,000,000 rows -- a gigabyte, three on disk with
# replication 3 -- which is slow on one machine and proves nothing more than
# 100,000 rows (10 MB) do. teravalidate is added: it is what says the sort worked.]

# Step 4: Submit to a named queue
# submit into a named queue and watch where it lands
yarn jar $EX pi -Dmapreduce.job.queuename=adhoc 4 1000 2>&1 | grep -E "Estimated value"
yarn application -list -appStates FINISHED 2>/dev/null | awk -F'\t' 'NR>2{print $2 " | " $5 " | " $7}' | sort
# [Corrected: this was `yarn jar ...examples-*.jar`, with three dots typed
# where the path goes; the path is set once, in EX, above.]

# Step 5: Observe the nodes and queues
# a job's client returns when the job reports success, and its last container is
# released a moment later; wait for that, so what follows is the idle cluster
until yarn node -list 2>/dev/null | grep -qE "RUNNING.*[[:space:]]0$"; do sleep 1; done
yarn node -list -all 2>/dev/null | tail -n +2  # every NodeManager, its state and containers
yarn queue -status adhoc 2>/dev/null | grep -E "Current Capacity|Maximum Capacity"

# Step 6: Kill a job
# a job to kill: start one that runs a while, and kill it by its id
yarn jar $EX pi 4 1000000000 > /dev/null 2>&1 &
sleep 15
APP=$(yarn application -list 2>/dev/null | awk '/^application_/{print $1}' | head -1)
yarn application -list 2>/dev/null | awk -F'\t' 'NR>2{print $2 " | " $6}'
yarn application -kill $APP 2>&1 | grep -E "Killed application|Killing application"
wait
yarn application -status $APP 2>/dev/null | grep -E "Final-State"
# [Corrected: this killed application_1699999999999_0002, an id from someone
# else's cluster; the id is taken from the list.]
#
# yarn top                         # like top(1), for the cluster
#   -- a full-screen display that runs until you press q, so it is not run here.

#   http://localhost:8088/cluster/scheduler   the queue tree, live
#
# What to look for: submit a big job and a small one into different queues,
# and watch the adhoc job start IMMEDIATELY even though production is full.
# That guarantee is what a queue is, and it is the whole answer to
# "what does the Capacity Scheduler do".
