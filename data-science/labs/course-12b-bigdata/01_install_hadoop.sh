# Experiment 1 -- installation and setup of a Hadoop single-node cluster
#
# Run it: bash 01_install_hadoop.sh, on Linux with Java 11 installed. It was run where these
# labs are checked, in an empty home directory, and the lab page shows what it printed.
# [Changed: this said the file had never been run, as Hadoop could not be installed there. It
# installs from archive.apache.org, and the corrections below are what running it found.]
#
# The runnable half is none -- installation has no query logic to verify
#
# Step 1: Check the prerequisites
java -version                       # Hadoop 3.x needs Java 8 or 11

# On your own machine, run Hadoop as its own user, with passwordless ssh to
# localhost -- start-dfs.sh and start-yarn.sh ssh to every host they start a
# daemon on, even in "single node":
#   sudo adduser hadoop && su - hadoop
#   ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
#   cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
#   chmod 600 ~/.ssh/authorized_keys
#   ssh localhost                   # must succeed WITHOUT a password
# Where this was run there is no ssh server, so the daemons are started one by
# one below, with the same commands start-dfs.sh runs on each host.

# Step 2: Download and unpack Hadoop
[ -f hadoop-3.3.6.tar.gz ] || \
  curl -fO https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzf hadoop-3.3.6.tar.gz && mv hadoop-3.3.6 ~/hadoop
# [Corrected: the download was from dlcdn.apache.org, which keeps only the
# current releases -- 3.3.6 is no longer there, and wget got a 404. Every
# release stays in archive.apache.org. And it was moved to /usr/local/hadoop
# with sudo; your home directory needs no sudo.]

cat >> ~/.bashrc <<'EOF'
export HADOOP_HOME=~/hadoop
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
EOF
source ~/.bashrc

# Step 3: Write the four configuration files
cat > $HADOOP_CONF_DIR/core-site.xml <<'EOF'
<configuration>
  <property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property>
</configuration>
EOF
cat > $HADOOP_CONF_DIR/hdfs-site.xml <<EOF
<configuration>
  <!-- 1, not 3: there is only one node -->
  <property><name>dfs.replication</name><value>1</value></property>
  <property><name>dfs.namenode.name.dir</name><value>file://$HOME/hadoop_store/hdfs/namenode</value></property>
  <property><name>dfs.datanode.data.dir</name><value>file://$HOME/hadoop_store/hdfs/datanode</value></property>
</configuration>
EOF
cat > $HADOOP_CONF_DIR/mapred-site.xml <<EOF
<configuration>
  <property><name>mapreduce.framework.name</name><value>yarn</value></property>
  <property><name>yarn.app.mapreduce.am.env</name><value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value></property>
  <property><name>mapreduce.map.env</name><value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value></property>
  <property><name>mapreduce.reduce.env</name><value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value></property>
</configuration>
EOF
cat > $HADOOP_CONF_DIR/yarn-site.xml <<'EOF'
<configuration>
  <property><name>yarn.nodemanager.aux-services</name><value>mapreduce_shuffle</value></property>
</configuration>
EOF
echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_CONF_DIR/hadoop-env.sh
# [Corrected: the four files were listed as property names only; they are
# written out here, under your home directory rather than /usr/local, which
# needs no sudo. Hadoop 3 also needs HADOOP_MAPRED_HOME passed to MapReduce's
# containers, or every job fails with "Could not find or load main class
# org.apache.hadoop.mapreduce.v2.app.MRAppMaster".]

# Step 4: Format HDFS, and start the five daemons
hdfs namenode -format 2>&1 | grep "has been successfully formatted"
#   ONCE. Re-formatting destroys the cluster. (It prints a hundred log lines;
#   this is the one that says it worked.)
hdfs --daemon start namenode
hdfs --daemon start datanode
hdfs --daemon start secondarynamenode
yarn --daemon start resourcemanager
yarn --daemon start nodemanager
#   = start-dfs.sh and start-yarn.sh, which run exactly these on each host,
#     over ssh

sleep 15                            # the DataNode and NodeManager register
jps | awk '{print $2}' | sort       # expect: NameNode, DataNode,
                                    # SecondaryNameNode, ResourceManager,
                                    # NodeManager  -- five processes, and Jps
hdfs dfsadmin -report 2>/dev/null | grep "Live datanodes"
hdfs dfs -mkdir -p /user/$USER && hdfs dfs -ls /user
# web UIs -- 200 means each is up:
curl -sL -o /dev/null -w "NameNode        http://localhost:9870  %{http_code}\n" http://localhost:9870
curl -s -o /dev/null -w "ResourceManager http://localhost:8088  %{http_code}\n" http://localhost:8088/cluster

# Step 5: Stop them
yarn --daemon stop nodemanager
yarn --daemon stop resourcemanager
hdfs --daemon stop secondarynamenode
hdfs --daemon stop datanode
hdfs --daemon stop namenode
#   = stop-yarn.sh and stop-dfs.sh

# --- the three failures everyone hits --------------------------------------
# 1. JAVA_HOME not set INSIDE hadoop-env.sh (the shell export is not enough)
# 2. re-running `hdfs namenode -format` after storing data: the DataNode's
#    clusterID no longer matches the NameNode's, and the DataNode will not
#    start. Fix: delete the datanode directory, or edit its VERSION file.
# 3. ssh localhost prompting for a password -- start-dfs.sh hangs for ever
