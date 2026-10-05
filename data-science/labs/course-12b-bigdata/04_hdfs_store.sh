# Experiment 4 -- store and retrieve large files in HDFS -- block distribution and replication
#
# Run it: bash 04_hdfs_store.sh, with a cluster running. It was run on a Hadoop 3.3.6 cluster where these labs
# are checked (tools/data-science/hadoop_lab.py), and the lab page shows what it printed.
# [Changed: this said the file had never been run, as the Hadoop stack could not be
# installed there. It installs from archive.apache.org: tools/data-science/setup_hadoop.sh.]
#
# The runnable half is 04_blocks_replication.py, which computes every figure below
#
# make a file bigger than one block so there is something to distribute
# Step 1: Make a 300 MB file
dd if=/dev/urandom of=big.bin bs=1M count=300      # 300 MB -> 3 blocks

# Step 2: Put it in HDFS
hdfs dfs -mkdir -p /user/student/big
hdfs dfs -put big.bin /user/student/big/

# how many blocks, and where are they?
# Step 3: Find its blocks and their replicas
hdfs fsck /user/student/big/big.bin -files -blocks -locations
#   expect: 3 blocks -- 128 MB, 128 MB, 44 MB
#   the LAST BLOCK IS SHORT. HDFS does not pad.

# Step 4: Change its replication
hdfs dfs -stat "%r" /user/student/big/big.bin      # replication factor
hdfs dfs -setrep -w 2 /user/student/big/big.bin    # -w waits for completion
hdfs fsck /user/student/big/big.bin -files -blocks # now 2 locations per block

# a non-default block size, set PER FILE at write time
# Step 5: Write it again with 64 MB blocks
hdfs dfs -D dfs.blocksize=67108864 -put big.bin /user/student/big/small-blocks.bin
hdfs fsck /user/student/big/small-blocks.bin -files -blocks
#   expect: 5 blocks -- four of 64 MB and a last one of 44 MB -- more blocks,
#   more NameNode objects, more map tasks (one per block by default)
# [Corrected: this said "5 blocks of 64 MB". 300 MB is 4 x 64 + 44: the last
# block is short here too, as it is above.]

# retrieve and verify
# Step 6: Get it back, and compare
hdfs dfs -get /user/student/big/big.bin ./back.bin
md5sum big.bin back.bin                            # must match

hdfs dfsadmin -report | grep -E "Name|DFS Used|Remaining"
