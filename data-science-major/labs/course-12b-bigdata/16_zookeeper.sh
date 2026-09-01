# Experiment 16 -- demonstrate coordination with ZooKeeper
#
# *** NOT EXECUTED ***
# This is the command sequence / program you submit on a real Hadoop cluster.
# Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
# the verification environment -- the Debian repositories that host them are
# blocked by the egress policy -- so this file has NEVER BEEN RUN here.
# Nothing in the notes claims an output for it.
#
# The runnable half is 16_zookeeper_model.py, which runs leader election, locking and quorum maths
#
# --- a 3-server ensemble ----------------------------------------------------
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

zkServer.sh start
zkServer.sh status                  # "Mode: leader" on exactly one host
echo srvr | nc localhost 2181       # four-letter command: state and zxid
echo mntr | nc localhost 2181       # metrics, including outstanding requests

# --- the tree ---------------------------------------------------------------
zkCli.sh -server localhost:2181
  ls /
  create /app "config-v1"
  get /app
  set /app "config-v2"
  stat /app                         # dataVersion increments; cZxid, mZxid
  ls -R /

# --- ephemeral: the node dies with the session -----------------------------
  create -e /app/worker-1 "alive"
  ls /app                           # [worker-1]
  quit
# reconnect: the session ended, so the ephemeral node is GONE
zkCli.sh -server localhost:2181
  ls /app                           # []

# --- sequential: numbered by a single authority ----------------------------
  create -s /app/task- "t"          # -> /app/task-0000000000
  create -s /app/task- "t"          # -> /app/task-0000000001
  create -s /app/task- "t"          # -> /app/task-0000000002

# --- leader election, the standard recipe ----------------------------------
#   1. every candidate: create -e -s /election/n-
#   2. read the children; LOWEST sequence number is the leader
#   3. everyone else watches the node IMMEDIATELY BELOW their own
#      -- not the leader. Watching the leader wakes every candidate on one
#         failure: the HERD EFFECT.
  create /election ""
  create -e -s /election/n- "nn1"
  ls /election
  get -w /election/n-0000000000     # -w sets a ONE-SHOT watch

# --- who relies on this -----------------------------------------------------
  ls /hbase                         # master, rs, meta-region-server
  ls /hadoop-ha/mycluster           # ActiveStandbyElectorLock  <- NameNode HA
  ls /rmstore                       # YARN ResourceManager HA
#
# Every HA story in the Hadoop ecosystem ends here.

zkCli.sh -server localhost:2181 deleteall /app
zkServer.sh stop
