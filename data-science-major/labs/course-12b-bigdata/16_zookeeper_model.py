"""Experiment 16 -- demonstrate coordination with ZooKeeper.

ZooKeeper is not installed. `16_zookeeper.sh` carries the real `zkCli.sh`
session, marked NOT EXECUTED. What runs here is the COORDINATION LOGIC: a
znode tree with ephemeral and sequential nodes, leader election by the
standard recipe, a distributed lock, and the quorum arithmetic that decides
whether an ensemble can make progress at all.

The point: ZooKeeper is not a database and not a queue. It is a small,
strongly-consistent tree whose only interesting properties are (a) ephemeral
nodes vanish when a session dies and (b) sequential nodes are numbered by a
single authority. Every recipe is built from exactly those two facts.
"""


class ZooKeeper:
    def __init__(self):
        self.tree = {"/": {"data": None, "ephemeral": False, "children": []}}
        self.counter = {}
        self.sessions = {}
        self.watches = []

    def create(self, path, data=None, ephemeral=False, sequential=False,
               session=None):
        parent = path.rsplit("/", 1)[0] or "/"
        if parent not in self.tree:
            raise KeyError(f"no node {parent} -- ZooKeeper creates no parents")
        if sequential:
            n = self.counter.get(path, 0)
            self.counter[path] = n + 1
            path = f"{path}{n:010d}"
        if path in self.tree:
            raise FileExistsError(f"{path} exists -- create is ATOMIC")
        self.tree[path] = {"data": data, "ephemeral": ephemeral,
                           "children": [], "session": session}
        self.tree[parent]["children"].append(path)
        if ephemeral:
            self.sessions.setdefault(session, []).append(path)
        return path

    def children(self, path):
        return sorted(self.tree[path]["children"])

    def expire(self, session):
        """A session dies -- every ephemeral node it owns disappears."""
        gone = self.sessions.pop(session, [])
        for p in gone:
            parent = p.rsplit("/", 1)[0] or "/"
            self.tree[parent]["children"].remove(p)
            del self.tree[p]
            self.watches.append(("deleted", p))
        return gone


def quorum(n):
    return n // 2 + 1


def main():
    print("  Experiment 16 -- ZooKeeper coordination")

    zk = ZooKeeper()
    zk.create("/hadoop-ha")
    zk.create("/hadoop-ha/mycluster")

    # ---- leader election -------------------------------------------------
    print("\n    leader election, the standard recipe:")
    print("      every candidate creates an EPHEMERAL SEQUENTIAL znode")
    print("      the LOWEST sequence number is the leader")
    print("      everyone else watches the node just below them")
    nodes = {}
    for host in ("nn1", "nn2", "nn3"):
        p = zk.create("/hadoop-ha/mycluster/lock-", data=host,
                      ephemeral=True, sequential=True, session=host)
        nodes[host] = p
        print(f"      {host} -> {p.rsplit('/', 1)[1]}")
    order = zk.children("/hadoop-ha/mycluster")
    leader = zk.tree[order[0]]["data"]
    print(f"\n      LEADER: {leader}")
    assert leader == "nn1"

    print("\n      nn1's session expires (its JVM was killed):")
    gone = zk.expire("nn1")
    order = zk.children("/hadoop-ha/mycluster")
    new_leader = zk.tree[order[0]]["data"]
    print(f"      {gone[0].rsplit('/', 1)[1]} vanished; new LEADER: {new_leader}")
    assert new_leader == "nn2" and len(order) == 2
    print("""         nobody ran a failover script. The ephemeral node was
         deleted BY THE SERVER when the heartbeat stopped, the watch
         fired, and nn2 saw itself at the head of the queue. That is
         how HDFS NameNode HA actually chooses its active node --
         which is the link back to experiment 5""")

    print("\n      why watch the node BELOW you, not the leader:")
    print(f"        {len(order) + 1} candidates all watching the leader means")
    print(f"        {len(order) + 1} clients woken by one failure -- the HERD EFFECT.")
    print("""        Watching your immediate predecessor wakes exactly ONE
        client per failure. The recipe is not arbitrary; it is a
        thundering-herd fix, and examiners like that you know why""")

    # ---- distributed lock ------------------------------------------------
    print("\n    a distributed lock is the SAME recipe:")
    zk.create("/locks")
    holders = []
    for client in ("jobA", "jobB"):
        p = zk.create("/locks/write-", data=client, ephemeral=True,
                      sequential=True, session=client)
        holders.append((client, p))
    first = zk.children("/locks")[0]
    print(f"      jobA and jobB both asked; {zk.tree[first]['data']} holds the lock")
    assert zk.tree[first]["data"] == "jobA"
    zk.expire("jobA")
    nxt = zk.children("/locks")[0]
    print(f"      jobA CRASHES -- lock passes to {zk.tree[nxt]['data']} automatically")
    assert zk.tree[nxt]["data"] == "jobB"
    print("""         the lock is released by the SESSION DYING, not by the
         client remembering to release it. A lock in a normal
         database survives the crash of whoever held it and deadlocks
         the system; an ephemeral znode cannot""")

    # ---- atomicity -------------------------------------------------------
    print("\n    create is ATOMIC, which is the other half of every recipe:")
    zk.create("/config", data="v1")
    try:
        zk.create("/config", data="v2")
        raise AssertionError("the second create must fail")
    except FileExistsError as exc:
        print(f"      second create -> {type(exc).__name__}")
    print("""         exactly one client wins a create, cluster-wide, with no
         further negotiation. 'Whoever creates /master is the master'
         is a complete election algorithm in one line, and it works
         only because ZooKeeper linearises writes""")

    # ---- quorum arithmetic -----------------------------------------------
    print("\n    ensemble sizing -- why every cluster has an ODD number:")
    print(f"      {'servers':>8}{'quorum':>8}{'can lose':>10}  {'verdict'}")
    for n in (1, 2, 3, 4, 5, 6, 7):
        q = quorum(n)
        tol = n - q
        verdict = ("no fault tolerance" if tol == 0 else
                   "same tolerance as " + str(n - 1) if n % 2 == 0 else "good")
        print(f"      {n:>8}{q:>8}{tol:>10}  {verdict}")
    assert quorum(3) == 2 and quorum(4) == 3
    assert (3 - quorum(3)) == (4 - quorum(4)) == 1
    print("""         3 servers tolerate 1 failure. FOUR SERVERS ALSO TOLERATE
         ONE -- the extra machine buys nothing and adds a write to
         every quorum. That is the whole reason ZooKeeper ensembles
         are 3, 5 or 7, and it is a two-line exam answer""")

    print("\n    what ZooKeeper is NOT:")
    print(f"      {'misuse':<34}{'why it fails'}")
    for m, w in (("a message queue", "no ordering guarantees across znodes"),
                 ("a data store", "1 MB per znode, whole tree in RAM"),
                 ("a cache", "every write is a quorum round trip"),
                 ("a service registry for 10k nodes", "watch storms")):
        print(f"      {m:<34}{w}")
    print("""         ZooKeeper stores COORDINATION STATE -- who is the leader,
         who holds the lock, what is the config -- and it is small,
         consistent and slow on purpose. Putting application data in
         it is the mistake that gets clusters into trouble""")

    print("\n    who uses it in this course:")
    for who, why in (("HDFS NameNode HA", "elects the ACTIVE NameNode (exp 5)"),
                     ("YARN ResourceManager HA", "elects the active RM (exp 6)"),
                     ("HBase", "tracks the master and the RegionServers (exp 15)"),
                     ("Kafka (pre-3.x)", "broker membership and controller")):
        print(f"      {who:<26}{why}")
    print("""         every HA story in the Hadoop ecosystem ends at
         ZooKeeper, which is why an experiment that looks like a
         detour is actually the keystone""")


if __name__ == "__main__":
    main()
