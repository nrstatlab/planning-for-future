"""Experiment 4 -- store and retrieve a large file in HDFS: blocks, block
distribution and the replication factor.

Hadoop is not installed here, so `04_hdfs_store.sh` carries the commands you
actually type. What runs here is the ARITHMETIC, which is the part that gets
examined and the part students get wrong.
"""
from blocks import BLOCK, MB, blocks_for, namenode_memory, placement


def main():
    print("  Experiment 4 -- HDFS blocks, distribution and replication")

    print("\n    block sizing (default block = 128 MB):")
    print(f"    {'file':>10}  {'blocks':>6}  {'last block':>12}  {'disk used':>12}")
    for mb in (1, 128, 129, 260, 1024, 5000):
        n, last = blocks_for(mb * MB)
        print(f"    {mb:>7} MB  {n:>6}  {last / MB:>9.2f} MB  {mb:>9} MB")
    print("""         a 260 MB file is 128 + 128 + 4, NOT three full blocks.
         An HDFS block is a logical MAXIMUM; the last block occupies
         only what it needs. HDFS wastes no space on block padding --
         which is the opposite of what the word 'block' suggests, and
         the mistake to avoid in the exam""")

    n1, last1 = blocks_for(1 * MB)
    assert (n1, last1) == (1, 1 * MB)
    n260, last260 = blocks_for(260 * MB)
    assert n260 == 3 and last260 == 4 * MB
    n128, _ = blocks_for(128 * MB)
    n129, _ = blocks_for(129 * MB)
    assert (n128, n129) == (1, 2), "one byte over a block boundary costs a block"
    print("\n    128 MB -> 1 block, 129 MB -> 2 blocks")
    print("""         one byte past the boundary costs a whole block OBJECT
         in NameNode memory, though almost no disk. Metadata is the
         scarce resource in HDFS, not disk""")

    print("\n    a 1 GB file, replication 3, 6 DataNodes across 2 racks:")
    n, last = blocks_for(1024 * MB)
    plan, rack_of = placement(n, 3, datanodes=6, racks=2)
    print(f"    {n} blocks (last = {last / MB:.0f} MB)")
    print(f"    {'block':>6}  {'replicas (node/rack)':<34}  racks used")
    for i, nodes in enumerate(plan):
        desc = "  ".join(f"n{d}/r{rack_of[d]}" for d in nodes)
        print(f"    {i:>6}  {desc:<34}  {len({rack_of[d] for d in nodes})}")
    for nodes in plan:
        assert len({rack_of[d] for d in nodes}) == 2, "must span two racks"
        assert len(set(nodes)) == 3, "three replicas on three distinct nodes"
    print("""         every block spans EXACTLY TWO racks: one replica on the
         writer's rack, two on another. Two racks survive a rack
         failure; a third rack would double cross-rack write traffic
         to buy very little. That trade is the whole policy""")

    raw = 1024
    print(f"\n    storage cost: {raw} MB of data at replication 3 "
          f"occupies {raw * 3} MB of disk")
    print(f"    the same data with erasure coding (RS-6-3) would occupy "
          f"{raw * 9 // 6} MB")
    assert raw * 3 == 3072 and raw * 9 // 6 == 1536
    print("""         replication costs 200% overhead for 3x durability;
         RS-6-3 erasure coding costs 50% for comparable durability,
         at the price of expensive reconstruction reads. HDFS added
         erasure coding in 3.0 for exactly this reason -- COLD data""")

    print("\n    the small-files problem, in NameNode RAM (~150 bytes/object):")
    print(f"    {'scenario':<26}{'files':>12}{'blocks':>12}{'NameNode RAM':>16}")
    for label, files, size_each in (
            ("one 1 GB file", 1, 1024 * MB),
            ("1,000 x 1 MB files", 1000, 1 * MB),
            ("1,000,000 x 1 KB files", 1_000_000, 1024)):
        total_blocks = sum(blocks_for(size_each)[0] for _ in range(1)) * files
        ram = namenode_memory(files, total_blocks)
        print(f"    {label:<26}{files:>12,}{total_blocks:>12,}"
              f"{ram / MB:>13.2f} MB")
    one = namenode_memory(1, 8)
    many = namenode_memory(1_000_000, 1_000_000)
    assert many // one > 200_000
    print(f"""         the same 1 GB costs {one} bytes as one file and
         {many / MB:.0f} MB as a million small ones -- a factor of
         {many // one:,}. HDFS was built for few large files, and this
         single table is the reason""")


if __name__ == "__main__":
    main()
