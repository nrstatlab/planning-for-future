"""Experiment 12 -- capture and store log/streaming data using Flume.

Flume is not installed. `12_flume.conf` carries the real agent configuration,
marked NOT EXECUTED. What runs here is the AGENT'S SEMANTICS: a source, a
channel with a bounded capacity, a sink with a batch size, and what actually
happens when the sink is slower than the source -- which is the only Flume
question worth asking.
"""
from collections import deque

import fixtures as f


class Channel:
    """A bounded buffer. Flume's memory channel, minus the threads.

    The capacity is the whole story: a full channel makes the SOURCE block,
    which is back-pressure, which is the correct behaviour and the one that
    surprises people.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.q = deque()
        self.rejected = 0
        self.high_water = 0

    def put(self, event):
        if len(self.q) >= self.capacity:
            self.rejected += 1
            return False
        self.q.append(event)
        self.high_water = max(self.high_water, len(self.q))
        return True

    def take(self, n):
        out = [self.q.popleft() for _ in range(min(n, len(self.q)))]
        return out


def interceptor(event):
    """Flume interceptors add HEADERS; they do not change the body."""
    ip = event.split(" ", 1)[0]
    status = event.rsplit(" ", 2)[-2]
    return {"headers": {"host": ip, "status": status}, "body": event}


def run_agent(events, capacity, batch, sink_every):
    """Drive one source -> channel -> sink agent, tick by tick."""
    chan = Channel(capacity)
    delivered, tick = [], 0
    src = list(events)
    while src or chan.q:
        if src:
            chan.put(interceptor(src.pop(0)))
        if tick % sink_every == 0:
            delivered.extend(chan.take(batch))
        tick += 1
    delivered.extend(chan.take(len(chan.q)))
    return chan, delivered, tick


def main():
    print("  Experiment 12 -- a Flume agent, semantics first")

    logs = f.access_logs(40)
    print(f"\n    source: {len(logs)} access-log lines")
    print(f"      {logs[0]}")

    ev = interceptor(logs[0])
    print(f"\n    after the interceptor:")
    print(f"      headers {ev['headers']}")
    print(f"      body    (unchanged, {len(ev['body'])} chars)")
    assert ev["headers"]["host"] == "10.0.0.1"
    assert ev["headers"]["status"] == "200"
    assert ev["body"] == logs[0]
    print("""         an interceptor adds HEADERS and leaves the body alone.
         Headers are what a multiplexing channel selector routes on,
         so 'send 500s to the alert sink and everything else to HDFS'
         is a header rule, not code""")

    # ---- a healthy agent -------------------------------------------------
    chan, delivered, ticks = run_agent(logs, capacity=100, batch=10, sink_every=1)
    print(f"\n    capacity 100, batch 10, sink every tick:")
    print(f"      delivered {len(delivered)} of {len(logs)}, "
          f"rejected {chan.rejected}, peak channel depth {chan.high_water}")
    assert len(delivered) == len(logs) and chan.rejected == 0
    assert chan.high_water <= 10

    # ---- a slow sink -----------------------------------------------------
    chan2, delivered2, _ = run_agent(logs, capacity=8, batch=4, sink_every=6)
    print(f"\n    capacity 8, batch 4, sink every 6th tick (a SLOW sink):")
    print(f"      delivered {len(delivered2)} of {len(logs)}, "
          f"rejected {chan2.rejected}, peak depth {chan2.high_water}")
    assert chan2.rejected > 0, "a slow sink must fill the channel"
    assert chan2.high_water == 8
    print(f"""         {chan2.rejected} events were REFUSED by the channel, because the
         sink could not drain it. In a real agent the source then
         BLOCKS rather than dropping -- back-pressure travels back up
         the pipe to the web server. 'Flume lost my events' almost
         always means 'the channel was full and the source gave up'""")

    print("\n    the fix, and its cost:")
    for cap in (8, 20, 100):
        c, d, _ = run_agent(logs, capacity=cap, batch=4, sink_every=6)
        print(f"      capacity {cap:>4}: rejected {c.rejected:>3}, "
              f"peak depth {c.high_water:>3}")
    print("""         a bigger channel absorbs a longer burst and buys nothing
         if the sink is permanently slower than the source. Buffers
         smooth BURSTS; they cannot fix a throughput deficit, and
         that sentence answers most Flume tuning questions""")

    # ---- channel types ---------------------------------------------------
    print("\n    channel types, and what you are choosing between:")
    print(f"      {'channel':<12}{'survives a crash?':<20}{'throughput'}")
    for name, durable, tput in (
            ("memory", "NO -- events lost", "highest"),
            ("file", "yes -- WAL on disk", "roughly 10x slower"),
            ("Kafka", "yes -- replicated", "high, but another cluster")):
        print(f"      {name:<12}{durable:<20}{tput}")
    print("""         a memory channel plus 'we must not lose events' is a
         contradiction, and it is the most common Flume misconfig.
         Choose the channel from the durability requirement, then
         size the cluster for whatever throughput that leaves""")

    # ---- what the sink writes -------------------------------------------
    from collections import Counter
    by_status = Counter(e["headers"]["status"] for e in delivered)
    by_host = Counter(e["headers"]["host"] for e in delivered)
    print(f"\n    what landed in HDFS, by header:")
    print(f"      status: {dict(sorted(by_status.items()))}")
    print(f"      host  : {dict(sorted(by_host.items()))}")
    assert sum(by_status.values()) == 40
    assert by_status["200"] == 24 and by_status["404"] == 8
    assert len(by_host) == 4 and all(v == 10 for v in by_host.values())
    print("""         24 successes, 8 not-founds and 8 server errors, evenly
         over four hosts. That breakdown is what experiment 17 reads
         back with Spark -- ingestion and analysis on the same bytes,
         which is the point of building the pipeline at all""")

    # ---- the file-per-batch trap ----------------------------------------
    print("\n    the HDFS sink's rollover settings:")
    print(f"      {'setting':<24}{'default':<12}{'what it does'}")
    for k, v, w in (("hdfs.rollInterval", "30 sec", "close the file on a timer"),
                    ("hdfs.rollSize", "1024 bytes", "close it at a size"),
                    ("hdfs.rollCount", "10 events", "close it after N events")):
        print(f"      {k:<24}{v:<12}{w}")
    files = -(-len(logs) // 10)
    print(f"\n      at the DEFAULTS, {len(logs)} events produce ~{files} HDFS files")
    assert files == 4
    print("""         and every one of them is a few hundred bytes. Left alone,
         Flume's defaults manufacture the small-files problem from
         experiment 4 at a rate of two per minute. Set rollCount to 0
         and rollSize to a block, or run a compaction job -- this is
         the single most common Flume-in-production mistake""")


if __name__ == "__main__":
    main()
