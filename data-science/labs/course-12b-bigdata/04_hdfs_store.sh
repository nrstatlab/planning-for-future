# Experiment 4 -- store and retrieve large files in HDFS -- block distribution and replication
#
# *** NOT EXECUTED ***
# This is the command sequence / program you submit on a real Hadoop cluster.
# Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
# the verification environment -- the Debian repositories that host them are
# blocked by the egress policy -- so this file has NEVER BEEN RUN here.
# Nothing in the notes claims an output for it.
#
# The runnable half is 04_blocks_replication.py, which computes every figure below
#
# make a file bigger than one block so there is something to distribute
dd if=/dev/urandom of=big.bin bs=1M count=300      # 300 MB -> 3 blocks

hdfs dfs -mkdir -p /user/student/big
hdfs dfs -put big.bin /user/student/big/

# how many blocks, and where are they?
hdfs fsck /user/student/big/big.bin -files -blocks -locations
#   expect: 3 blocks -- 128 MB, 128 MB, 44 MB
#   the LAST BLOCK IS SHORT. HDFS does not pad.

hdfs dfs -stat "%r" /user/student/big/big.bin      # replication factor
hdfs dfs -setrep -w 2 /user/student/big/big.bin    # -w waits for completion
hdfs fsck /user/student/big/big.bin -files -blocks # now 2 locations per block

# a non-default block size, set PER FILE at write time
hdfs dfs -D dfs.blocksize=67108864 -put big.bin /user/student/big/small-blocks.bin
hdfs fsck /user/student/big/small-blocks.bin -files -blocks
#   expect: 5 blocks of 64 MB -- more blocks, more NameNode objects,
#   more map tasks (one per block by default)

# retrieve and verify
hdfs dfs -get /user/student/big/big.bin ./back.bin
md5sum big.bin back.bin                            # must match

hdfs dfsadmin -report | grep -E "Name|DFS Used|Remaining"
