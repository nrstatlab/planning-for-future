"""A MapReduce engine in forty lines, written out in full.

Hadoop cannot be installed here, but MapReduce is not Hadoop -- it is a
programming model, and the model fits on one screen. Writing it explicitly is
worth more than running someone else's word count, because it makes the
SHUFFLE visible, and the shuffle is the part students never see and the part
that costs the money.

Every experiment that says "MapReduce" in this course runs through this
engine, so the map and reduce functions written here are the same ones you
would submit to a real cluster -- only the scheduler differs.
"""
from collections import defaultdict


def run(pairs, mapper, reducer, combiner=None, reducers=1, trace=None):
    """Run one MapReduce job.

    pairs     -- the input, as (key, value) records
    mapper    -- (k, v) -> iterable of (k2, v2)
    reducer   -- (k2, [v2, ...]) -> iterable of (k3, v3)
    combiner  -- optional map-side reducer, same signature as reducer
    reducers  -- number of reduce partitions; hash(key) %% reducers picks one
    trace     -- optional dict, filled with the intermediate counts

    Returns the reduce output, sorted by key.
    """
    # ---- MAP -------------------------------------------------------------
    # One input record is treated as one INPUT SPLIT, i.e. one map task. That
    # distinction matters for the combiner: a real combiner runs INSIDE a
    # single map task and can only merge what that task produced. Combining
    # globally would flatter the numbers and teach the wrong thing.
    per_task = [list(mapper(k, v)) for k, v in pairs]
    mapped = [kv for task in per_task for kv in task]

    # ---- COMBINE (optional, map-side, PER TASK) --------------------------
    if combiner is None:
        combined = mapped
    else:
        combined = []
        for task in per_task:
            grouped = defaultdict(list)
            for k, v in task:
                grouped[k].append(v)
            for k in sorted(grouped):
                combined.extend(combiner(k, grouped[k]))

    # ---- SHUFFLE AND SORT ------------------------------------------------
    # This is the network step. Every record here crosses the wire, which is
    # why the combiner exists and why a bad key design is a bad job.
    partitions = [defaultdict(list) for _ in range(reducers)]
    for k, v in combined:
        partitions[_partition(k, reducers)][k].append(v)

    # ---- REDUCE ----------------------------------------------------------
    out = []
    for part in partitions:
        for k in sorted(part):
            out.extend(reducer(k, part[k]))

    if trace is not None:
        trace["map_output"] = len(mapped)
        trace["shuffled"] = len(combined)
        trace["partition_sizes"] = [sum(len(v) for v in p.values())
                                    for p in partitions]
        trace["distinct_keys"] = len({k for k, _ in combined})

    return sorted(out)


def _partition(key, reducers):
    """Hadoop's default partitioner: (hash & MAXINT) %% numReduceTasks.

    Python's hash() is salted per process for strings, so this uses a stable
    hash instead -- otherwise the partition sizes would change between runs
    and nothing here would be reproducible.
    """
    h = 0
    for ch in str(key):
        h = (h * 31 + ord(ch)) & 0x7FFFFFFF
    return h % reducers
