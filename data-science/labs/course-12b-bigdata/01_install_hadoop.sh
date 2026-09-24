# Experiment 1 -- installation and setup of a Hadoop single-node cluster
#
# *** NOT EXECUTED ***
# This is the command sequence / program you submit on a real Hadoop cluster.
# Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
# the verification environment -- the Debian repositories that host them are
# blocked by the egress policy -- so this file has NEVER BEEN RUN here.
# Nothing in the notes claims an output for it.
#
# The runnable half is none -- installation has no query logic to verify
#
# --- prerequisites ----------------------------------------------------------
java -version                       # Hadoop 3.x needs Java 8 or 11
sudo adduser hadoop && su - hadoop

# passwordless ssh to localhost: the start scripts ssh even in "single node"
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
ssh localhost                       # must succeed WITHOUT a password

# --- install ----------------------------------------------------------------
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzf hadoop-3.3.6.tar.gz && sudo mv hadoop-3.3.6 /usr/local/hadoop

cat >> ~/.bashrc <<'EOF'
export HADOOP_HOME=/usr/local/hadoop
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
EOF
source ~/.bashrc

# --- the four files you must edit ------------------------------------------
# $HADOOP_CONF_DIR/core-site.xml
#   fs.defaultFS            hdfs://localhost:9000
# $HADOOP_CONF_DIR/hdfs-site.xml
#   dfs.replication         1          <- 1, not 3: there is only one node
#   dfs.namenode.name.dir   file:///usr/local/hadoop_store/hdfs/namenode
#   dfs.datanode.data.dir   file:///usr/local/hadoop_store/hdfs/datanode
# $HADOOP_CONF_DIR/mapred-site.xml
#   mapreduce.framework.name  yarn
# $HADOOP_CONF_DIR/yarn-site.xml
#   yarn.nodemanager.aux-services  mapreduce_shuffle

# --- format and start -------------------------------------------------------
hdfs namenode -format               # ONCE. Re-formatting destroys the cluster.
start-dfs.sh
start-yarn.sh

jps                                 # expect: NameNode, DataNode,
                                    # SecondaryNameNode, ResourceManager,
                                    # NodeManager  -- five processes
# web UIs
#   http://localhost:9870   NameNode
#   http://localhost:8088   ResourceManager

# --- the three failures everyone hits --------------------------------------
# 1. JAVA_HOME not set INSIDE hadoop-env.sh (the shell export is not enough)
# 2. re-running `hdfs namenode -format` after storing data: the DataNode's
#    clusterID no longer matches the NameNode's, and the DataNode will not
#    start. Fix: delete the datanode directory, or edit its VERSION file.
# 3. ssh localhost prompting for a password -- start-dfs.sh hangs for ever
