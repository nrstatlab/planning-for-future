# Experiment 16 -- demonstrate coordination with ZooKeeper
#
# Run it: bash 16_zookeeper.sh -- it starts and stops its own ensemble. It was run on a Hadoop 3.3.6 cluster where these labs
# are checked (tools/data-science/hadoop_lab.py), and the lab page shows what it printed.
# [Changed: this said the file had never been run, as the Hadoop stack could not be
# installed there. It installs from archive.apache.org: tools/data-science/setup_hadoop.sh.]
#
# The runnable half is 16_zookeeper_model.py, which runs leader election, locking and quorum maths
#
# Step 1: Configure three servers
# conf/zoo.cfg, identical on all three:
#   tickTime=2000
#   initLimit=10
#   syncLimit=5
#   dataDir=/var/lib/zookeeper
#   clientPort=2181
#   server.1=zk1:2888:3888
#   server.2=zk2:2888:3888
#   server.3=zk3:2888:3888
# and on each host:  echo <id> > /var/lib/zookeeper/myid
#
# THREE, FIVE OR SEVEN. Four servers need a quorum of 3 and tolerate one
# failure -- exactly what three tolerate -- so the fourth machine buys nothing
# and slows every write.
#
# Here the three servers run on ONE machine, so each needs its own client port,
# its own pair of quorum ports and its own data directory; otherwise the file
# is the one above. The four-letter commands must also be allowed by name:
for id in 1 2 3; do
  mkdir -p zk$id && echo $id > zk$id/myid
  cat > zk$id.cfg <<EOF
tickTime=2000
initLimit=10
syncLimit=5
dataDir=$PWD/zk$id
clientPort=218$id
server.1=localhost:2888:3888
server.2=localhost:2889:3889
server.3=localhost:2890:3890
4lw.commands.whitelist=srvr,mntr
EOF
done
# [Corrected: the ensemble was described in comments, and `zkServer.sh start`
# started ONE server. These are the zoo.cfg above for three servers on one
# host, and each is started below.]

# Step 2: Start them, and see the leader
for id in 1 2 3; do ZOO_LOG_DIR=zk$id zkServer.sh start $PWD/zk$id.cfg 2>&1 | tail -1; done
sleep 10                            # they elect a leader
for id in 1 2 3; do zkServer.sh status $PWD/zk$id.cfg 2>&1 | grep Mode; done
#                                     "Mode: leader" on exactly one server
echo srvr | nc localhost 2181 | grep -E "Mode|Zxid|Node count"     # state and zxid
echo mntr | nc localhost 2181 | grep -E "zk_server_state|zk_znode_count|zk_outstanding_requests"

# Step 3: Build the tree
zkCli.sh -server localhost:2181 2>&1 <<'EOF'
ls /
create /app "config-v1"
get /app
set /app "config-v2"
stat /app
ls -R /
quit
EOF
#   stat: dataVersion increments; cZxid, mZxid

# Step 4: Make an ephemeral node
zkCli.sh -server localhost:2181 2>&1 <<'EOF'
create -e /app/worker-1 "alive"
ls /app
quit
EOF
# reconnect: the session ended, so the ephemeral node is GONE
zkCli.sh -server localhost:2182 2>&1 <<'EOF'
ls /app
quit
EOF
#   (asked of a different server: every one of them has the same tree)

# Step 5: Make sequential nodes
zkCli.sh -server localhost:2181 2>&1 <<'EOF'
create -s /app/task- "t"
create -s /app/task- "t"
create -s /app/task- "t"
quit
EOF
#   -> /app/task-0000000001, -0000000002, -0000000003
# [Corrected: this said -0000000000, -0000000001, -0000000002. The number is
# kept by the PARENT, /app, and counts every child it has had: worker-1 above
# took the first, though it is gone. Never assume a sequence starts at 0.]

# Step 6: Elect a leader
#   1. every candidate: create -e -s /election/n-
#   2. read the children; LOWEST sequence number is the leader
#   3. everyone else watches the node IMMEDIATELY BELOW their own
#      -- not the leader. Watching the leader wakes every candidate on one
#         failure: the HERD EFFECT.
zkCli.sh -server localhost:2181 2>&1 <<'EOF'
create /election ""
create -e -s /election/n- "nn1"
create -e -s /election/n- "nn2"
ls /election
get -w /election/n-0000000000
quit
EOF
#   get -w sets a ONE-SHOT watch

# Step 7: Look for the systems that use it
zkCli.sh -server localhost:2181 2>&1 <<'EOF'
ls /hbase
ls /hadoop-ha/mycluster
ls /rmstore
quit
EOF
#   /hbase                 master, rs, meta-region-server
#   /hadoop-ha/mycluster   ActiveStandbyElectorLock  <- NameNode HA
#   /rmstore               YARN ResourceManager HA
# Nothing uses this ensemble, so none of them exists here. Every HA story in
# the Hadoop ecosystem ends in znodes like these.

zkCli.sh -server localhost:2181 deleteall /app 2>/dev/null | tail -1
for id in 1 2 3; do zkServer.sh stop $PWD/zk$id.cfg 2>&1 | tail -1; done
# [Corrected: the zkCli.sh commands were indented under `zkCli.sh -server ...`,
# as typed at its prompt. Run as a script, the shell runs them itself -- `ls /`
# lists the machine's root directory, and `create` is "command not found".
# Each session is a here-document here, typed into zkCli.sh.]
