"""Experiment 5 -- simulate NameNode/DataNode failure and observe fault
tolerance and recovery.

`05_fault_tolerance.sh` carries the commands. What runs here is the model:
which blocks survive which failures, and why the NameNode is the one failure
that is different in kind.
"""
import itertools

from blocks import blocks_for, placement


def surviving(plan, rack_of, dead_nodes=(), dead_racks=()):
    """Blocks with at least one live replica, and blocks fully lost."""
    dead = set(dead_nodes) | {d for d in rack_of if rack_of[d] in dead_racks}
    live, lost = [], []
    for i, nodes in enumerate(plan):
        (live if any(n not in dead for n in nodes) else lost).append(i)
    return live, lost


def main():
    print("  Experiment 5 -- fault tolerance and recovery")

    n, _ = blocks_for(1024 * 1024 * 1024)
    plan, rack_of = placement(n, 3, datanodes=6, racks=2)
    print(f"\n    a 1 GB file: {n} blocks, replication 3, 6 nodes, 2 racks")

    print(f"\n    {'failure':<28}{'blocks live':>12}{'blocks lost':>12}  verdict")
    scenarios = [
        ("1 DataNode  (n1)",        dict(dead_nodes=[1])),
        ("2 DataNodes (n1, n3)",    dict(dead_nodes=[1, 3])),
        ("3 DataNodes (n1, n3, n5)", dict(dead_nodes=[1, 3, 5])),
        ("3 DataNodes (n0, n1, n3)", dict(dead_nodes=[0, 1, 3])),
        ("a whole rack (r1)",       dict(dead_racks=[1])),
        ("both racks",              dict(dead_racks=[0, 1])),
    ]
    for label, kw in scenarios:
        live, lost = surviving(plan, rack_of, **kw)
        verdict = "no data loss" if not lost else f"DATA LOSS on {len(lost)}"
        print(f"    {label:<28}{len(live):>12}{len(lost):>12}  {verdict}")

    live, lost = surviving(plan, rack_of, dead_racks=[1])
    assert lost == [], "losing one whole rack must not lose data"
    live, lost = surviving(plan, rack_of, dead_nodes=[1, 3, 5])
    assert lost == [], "n1, n3, n5 IS rack 1 -- the same failure, renamed"
    print("""         losing an ENTIRE RACK loses nothing, because every block
         keeps one replica on the other rack. That is precisely what
         the placement policy bought, and it is the answer to 'why
         rack awareness?'
         Note rows 3 and 4: n1, n3, n5 ARE rack 1, so those are the
         same failure written two ways -- and both are survivable.
         Three failures only hurt when they straddle the racks, as
         (n0, n1, n3) does""")

    print("\n    the worst case, by brute force -- how many DataNode failures")
    print("    can this layout survive with certainty?")
    worst = None
    for k in range(1, 7):
        bad = [combo for combo in itertools.combinations(range(6), k)
               if surviving(plan, rack_of, dead_nodes=combo)[1]]
        total = len(list(itertools.combinations(range(6), k)))
        print(f"      {k} node(s) down: {len(bad):>3} of {total:>3} "
              f"combinations lose data")
        if bad and worst is None:
            worst = k
    assert worst == 3, "replication 3 tolerates ANY 2 failures, not any 3"
    print("""         ANY TWO failures are survivable; some threes are not.
         Replication factor R tolerates R-1 arbitrary failures --
         and note that most 3-node combinations are still fine, so
         'replication 3 fails at 3 nodes' is only true of the worst
         case, which is the honest way to state it""")

    print("\n    re-replication after a DataNode is declared dead:")
    print("      1. DataNode misses heartbeats (default: 3 sec interval)")
    print("      2. NameNode waits 10 * 3 sec + 2 * 5 min = 10 min 30 sec")
    print("      3. its blocks are now UNDER-REPLICATED (2 of 3)")
    print("      4. NameNode schedules copies from surviving replicas")
    print("      5. replication returns to 3; no client ever saw an error")
    stale = 10 * 3 + 2 * 5 * 60
    assert stale == 630
    print(f"""         the {stale}-second default is deliberately LONG. A node
         that reboots in five minutes should not trigger a cluster-wide
         copy storm, so HDFS trades a longer window of reduced
         redundancy for far less needless network traffic""")

    print("\n    the NameNode is a different kind of failure:")
    print(f"      {'component':<22}{'holds':<34}{'lost on crash?'}")
    for comp, holds, lost_ in (
            ("fsimage (on disk)", "the namespace at a checkpoint", "no"),
            ("edit log (on disk)", "changes since the checkpoint", "no"),
            ("block map (in RAM)", "block -> DataNode locations", "YES"),
    ):
        print(f"      {comp:<22}{holds:<34}{lost_}")
    print("""         the block MAP is never persisted -- it is rebuilt from
         DataNode block reports at startup, which is why a large
         NameNode takes minutes to leave safe mode. The namespace
         survives; the locations are reconstructed""")

    print("\n    the three answers to NameNode failure, in historical order:")
    print(f"      {'mechanism':<26}{'recovers':<16}{'automatic?'}")
    for m, r, a in (("Secondary NameNode", "checkpoint only", "no -- NOT a standby"),
                    ("NameNode HA (2 NNs)", "full", "yes, via ZooKeeper"),
                    ("HDFS Federation", "n/a -- scales namespace", "n/a")):
        print(f"      {m:<26}{r:<16}{a}")
    print("""         the Secondary NameNode is the most misleadingly named
         component in Hadoop: it merges fsimage with the edit log so
         restarts stay fast, and it CANNOT take over. HA needs two
         NameNodes, a shared edit log (QJM) and ZooKeeper for failover
         -- which is exactly why experiment 16 exists""")


if __name__ == "__main__":
    main()
