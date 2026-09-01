"""Experiment 6 -- configure YARN, run sample applications, and observe the
ResourceManager and NodeManager roles.

`06_yarn.sh` carries the real commands. What runs here is the SCHEDULER, which
is the part of YARN that actually decides anything -- and the part where the
three policies give visibly different answers on the same queue.
"""

# (name, containers needed, seconds per container-slot, submitted at)
JOBS = [
    ("big_etl",  8, 10, 0),
    ("small_q1", 1,  2, 1),
    ("small_q2", 1,  2, 2),
    ("medium",   4,  5, 3),
]

CLUSTER = 8          # containers available cluster-wide


def fifo(jobs, capacity):
    """First in, first out. One job owns the cluster until it finishes."""
    now, done = 0, {}
    for name, need, secs, submitted in sorted(jobs, key=lambda j: j[3]):
        start = max(now, submitted)
        waves = -(-need // capacity)          # ceil
        now = start + waves * secs
        done[name] = (start, now, now - submitted)
    return done


def fair(jobs, capacity):
    """Fair scheduler: every RUNNING job gets an equal share of containers.

    Simulated one second at a time, which is crude but exactly right for
    showing the property that matters -- a one-container job does not wait
    behind an eight-container job.
    """
    remaining = {j[0]: j[1] * j[2] for j in jobs}   # container-seconds of work
    submitted = {j[0]: j[3] for j in jobs}
    done, t = {}, 0
    while any(v > 0 for v in remaining.values()):
        active = [n for n, v in remaining.items() if v > 0 and submitted[n] <= t]
        if not active:
            t += 1
            continue
        share = capacity / len(active)
        for n in active:
            remaining[n] -= share
            if remaining[n] <= 0 and n not in done:
                done[n] = (submitted[n], t + 1, t + 1 - submitted[n])
        t += 1
    return done


def capacity_sched(jobs, capacity, queues):
    """Capacity scheduler: queues get guaranteed percentages of the cluster.

    A job cannot exceed its queue's share even when the cluster is idle,
    unless elasticity is enabled -- which is the whole difference between
    'capacity' and 'fair'.
    """
    done = {}
    for qname, pct, members in queues:
        slots = max(1, int(capacity * pct / 100))
        qjobs = [j for j in jobs if j[0] in members]
        sub = fifo(qjobs, slots)
        for k, v in sub.items():
            done[k] = v
    return done


def main():
    print("  Experiment 6 -- YARN scheduling")

    print("\n    the workload, on an 8-container cluster:")
    print(f"      {'job':<10}{'containers':>11}{'sec/wave':>10}{'submitted':>11}")
    for name, need, secs, sub in JOBS:
        print(f"      {name:<10}{need:>11}{secs:>10}{sub:>11}")

    f = fifo(JOBS, CLUSTER)
    print("\n    FIFO scheduler:")
    print(f"      {'job':<10}{'start':>7}{'finish':>8}{'turnaround':>12}")
    for name, _, _, _ in JOBS:
        s, e, t = f[name]
        print(f"      {name:<10}{s:>7}{e:>8}{t:>12}")
    fifo_small = f["small_q1"][2]
    print(f"""         small_q1 needs ONE container for TWO seconds and waits
         {fifo_small} seconds, because big_etl took the whole cluster first.
         That is head-of-line blocking, and it is why nobody runs
         FIFO on a shared cluster""")

    fr = fair(JOBS, CLUSTER)
    print("\n    Fair scheduler:")
    print(f"      {'job':<10}{'start':>7}{'finish':>8}{'turnaround':>12}")
    for name, _, _, _ in JOBS:
        s, e, t = fr[name]
        print(f"      {name:<10}{s:>7}{e:>8}{t:>12}")
    fair_small = fr["small_q1"][2]
    assert fair_small < fifo_small
    print(f"""         small_q1 now finishes in {fair_small}s instead of {fifo_small}s.
         Fair sharing did not make the cluster faster -- big_etl
         finished LATER ({f['big_etl'][1]} -> {fr['big_etl'][1]}) -- it moved latency from
         the small job to the big one, which is almost always the
         trade you want on an interactive cluster""")

    total_fifo = sum(v[2] for v in f.values())
    total_fair = sum(v[2] for v in fr.values())
    work = sum(need * secs for _, need, secs, _ in JOBS)
    print(f"\n    total container-seconds of WORK: {work} either way")
    print(f"    total turnaround:  FIFO {total_fifo}   Fair {total_fair}")
    assert total_fair < total_fifo
    print(f"""         the work is identical -- {work} container-seconds, which on
         8 containers cannot finish before second {-(-work // CLUSTER)}. What changed is
         WAITING: FIFO made three jobs queue behind one, so total
         turnaround fell from {total_fifo} to {total_fair} without the cluster doing
         anything faster.
         Scheduling decides WHO waits. It cannot create throughput,
         but idle-while-queued is real waste and fair sharing removes
         it""")

    cap = capacity_sched(JOBS, CLUSTER, [
        ("production", 75, {"big_etl", "medium"}),
        ("adhoc",      25, {"small_q1", "small_q2"}),
    ])
    print("\n    Capacity scheduler -- production 75%, adhoc 25%:")
    print(f"      {'job':<10}{'queue':<12}{'start':>7}{'finish':>8}{'turnaround':>12}")
    for name, q in (("big_etl", "production"), ("medium", "production"),
                    ("small_q1", "adhoc"), ("small_q2", "adhoc")):
        s, e, t = cap[name]
        print(f"      {name:<10}{q:<12}{s:>7}{e:>8}{t:>12}")
    print("""         the adhoc queue holds 2 containers whatever else is
         running, so a short query has a GUARANTEE rather than a
         hope. The cost: those 2 containers sit idle when adhoc is
         empty, unless queue elasticity is turned on""")

    print("\n    who does what in YARN:")
    print(f"      {'component':<22}{'one per':<14}{'responsibility'}")
    for c, per, resp in (
            ("ResourceManager", "cluster", "global scheduling; hands out containers"),
            ("NodeManager", "node", "launches and monitors containers, reports health"),
            ("ApplicationMaster", "JOB", "negotiates containers, retries failed tasks"),
            ("Container", "task", "a bounded slice of CPU and RAM on one node")):
        print(f"      {c:<22}{per:<14}{resp}")
    print("""         ONE ApplicationMaster PER JOB is the change that defined
         YARN. In Hadoop 1 the JobTracker did both scheduling and job
         management for every job, so it was the bottleneck AND the
         single point of failure. Splitting them is why YARN can run
         Spark, Tez and Flink and not only MapReduce""")


if __name__ == "__main__":
    main()
