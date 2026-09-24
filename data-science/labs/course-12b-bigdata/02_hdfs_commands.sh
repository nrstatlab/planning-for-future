# Experiment 2 -- explore the Hadoop directory structure and basic hadoop fs commands
#
# *** NOT EXECUTED ***
# This is the command sequence / program you submit on a real Hadoop cluster.
# Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
# the verification environment -- the Debian repositories that host them are
# blocked by the egress policy -- so this file has NEVER BEEN RUN here.
# Nothing in the notes claims an output for it.
#
# The runnable half is none -- these are filesystem commands, verified by the arithmetic in 04
#
hdfs dfs -mkdir -p /user/student/sales
hdfs dfs -ls /user/student
hdfs dfs -ls -R /user                 # recursive
hdfs dfs -put sales.csv /user/student/sales/
hdfs dfs -cat /user/student/sales/sales.csv | head
hdfs dfs -tail /user/student/sales/sales.csv
hdfs dfs -get /user/student/sales/sales.csv ./back.csv
hdfs dfs -cp  /user/student/sales/sales.csv /user/student/copy.csv
hdfs dfs -mv  /user/student/copy.csv /user/student/moved.csv
hdfs dfs -rm -r /user/student/sales   # goes to .Trash, not to nothing
hdfs dfs -du -h /user/student
hdfs dfs -df -h /
hdfs dfs -count /user/student         # DIRS FILES BYTES
hdfs dfs -chmod 640 /user/student/moved.csv
hdfs dfs -chown student:analysts /user/student/moved.csv
hdfs dfs -setrep -w 2 /user/student/moved.csv     # change replication
hdfs dfs -stat "%r %o %b" /user/student/moved.csv # replication blocksize bytes

hdfs fsck /user/student -files -blocks -locations  # WHERE each block lives
hdfs dfsadmin -report                              # per-DataNode capacity
hdfs dfsadmin -safemode get                        # ON during startup

# --- the four things that surprise people ----------------------------------
# 1. `hadoop fs` and `hdfs dfs` are the same command. `hadoop fs` also works
#    on local and S3 paths; `hdfs dfs` is HDFS only.
# 2. THERE IS NO `cd`. HDFS has no working directory -- every path is
#    absolute, or relative to /user/$USER.
# 3. `-rm` moves to .Trash and still costs quota for a day. Use -skipTrash
#    when you mean it.
# 4. There is no in-place edit. HDFS is WRITE-ONCE, APPEND-ONLY: to change one
#    byte you rewrite the file. That single constraint is why HDFS can drop
#    file locking, and why it suits analytics and not OLTP.
