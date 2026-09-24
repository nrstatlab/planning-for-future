"""HDFS block arithmetic and replica placement, shared by experiments 4 and 5.

Hadoop is not installed here, so `04_hdfs_store.sh` carries the commands you
actually type. What runs here is the ARITHMETIC, which is the part that gets
examined and the part students get wrong.
"""
import math

BLOCK = 128 * 1024 * 1024          # HDFS default since Hadoop 2
MB = 1024 * 1024


def blocks_for(size_bytes, block=BLOCK):
    """Number of blocks, and the size of the last one.

    HDFS blocks are the LAST-BLOCK-SHORT kind: a 260 MB file is 128 + 128 + 4,
    not three 128 MB blocks. This is the single most common exam mistake --
    an HDFS block is a logical maximum, not a fixed allocation on disk.
    """
    if size_bytes == 0:
        return 0, 0
    n = math.ceil(size_bytes / block)
    last = size_bytes - (n - 1) * block
    return n, last


def placement(n_blocks, replication, datanodes, racks):
    """Where each replica lands, under Hadoop's default rack-aware policy.

    Default policy for replication 3:
      replica 1 -- the local node (or a random node if the writer is off-cluster)
      replica 2 -- a node on a DIFFERENT rack
      replica 3 -- a different node on the SAME rack as replica 2

    Two racks, not three, because rack failures are rarer than node failures
    and cross-rack bandwidth is the scarce resource. That trade is the answer
    to 'why not one replica per rack?'
    """
    rack_of = {d: d % racks for d in range(datanodes)}
    plan = []
    for b in range(n_blocks):
        first = (b * 2) % datanodes
        chosen = [first]
        # replica 2: a node on a DIFFERENT rack, rotated per block so the
        # off-rack load spreads instead of hammering one node
        others = [d for d in range(datanodes) if rack_of[d] != rack_of[first]]
        chosen.append(others[b % len(others)])
        # replica 3+: same rack as replica 2, different node
        same = [d for d in others if d not in chosen]
        for offset in range(len(same)):
            if len(chosen) >= replication:
                break
            chosen.append(same[(b + offset) % len(same)])
        # anything still missing goes anywhere free
        for d in range(datanodes):
            if len(chosen) >= replication:
                break
            if d not in chosen:
                chosen.append(d)
        plan.append(chosen)
    return plan, rack_of


def namenode_memory(n_files, n_blocks_total, bytes_per_object=150):
    """The small-files problem, in bytes.

    The NameNode holds the ENTIRE namespace in RAM: roughly 150 bytes per
    file, directory and block object. That is why a million 1 KB files is a
    catastrophe and one 1 GB file is nothing.
    """
    return (n_files + n_blocks_total) * bytes_per_object


