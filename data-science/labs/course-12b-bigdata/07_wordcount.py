"""Experiment 7 -- a simple MapReduce program for word count.

This is the "hello world" of MapReduce, and it is worth more than it looks:
the shuffle between map and reduce is the only part of the model that costs
real money on a cluster, and word count is the smallest program that makes it
visible.

Runs through the engine in mapreduce.py, and then through REAL PYSPARK if the
Spark virtual environment is present (see tools/setup_spark.sh).
"""
from mapreduce import run
import fixtures as f

INPUT = sorted(f.DOCS.items())


def mapper(name, line):
    """(filename, line) -> (word, 1) for every word."""
    for word in line.split():
        yield word, 1


def reducer(word, counts):
    """(word, [1, 1, ...]) -> (word, total)."""
    yield word, sum(counts)


def main():
    print("  Experiment 7 -- word count in MapReduce")

    print(f"\n    input: {len(INPUT)} documents, "
          f"{sum(len(t.split()) for _, t in INPUT)} words")

    trace = {}
    result = run(INPUT, mapper, reducer, trace=trace)
    counts = dict(result)

    print(f"\n    {'phase':<26}{'records':>9}")
    print(f"    {'map output':<26}{trace['map_output']:>9}")
    print(f"    {'shuffled across network':<26}{trace['shuffled']:>9}")
    print(f"    {'reduce output':<26}{len(result):>9}")
    assert trace["map_output"] == 48
    assert len(result) == 26

    print("\n    the top words:")
    for w, c in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:6]:
        print(f"      {w:<10}{c:>3}")
    assert counts["the"] == 5 and counts["dog"] == 4
    assert counts["big"] == 4 and counts["data"] == 4
    assert sum(counts.values()) == 48
    print("""         the counts sum back to 48, the map output. Nothing was
         created or lost -- reduce is a REGROUPING, and if your
         totals do not reconcile, your reducer is not associative""")

    # ---- the combiner ----------------------------------------------------
    ctrace = {}
    combined = run(INPUT, mapper, reducer, combiner=reducer, trace=ctrace)
    assert combined == result, "a combiner must not change the answer"
    saved = trace["shuffled"] - ctrace["shuffled"]
    pct = 100 * saved / trace["shuffled"]
    print(f"\n    with a combiner (the reducer, run map-side, PER TASK):")
    print(f"      shuffled {trace['shuffled']} -> {ctrace['shuffled']} "
          f"({saved} fewer records, {pct:.2f}%)")
    print(f"""         same answer, {pct:.1f}% less network. And note how SMALL that
         saving is: these documents are 5 to 11 words, so there is
         almost nothing to merge within one split. On a 128 MB split
         of real text the same combiner cuts the shuffle by orders of
         magnitude. The combiner's value scales with SPLIT SIZE, which
         is the point this tiny dataset makes by failing to impress""")

    print("\n    when a combiner is NOT safe:")
    print(f"      {'reducer computes':<22}{'combiner-safe?':<16}why")
    for what, safe, why in (
            ("sum", "yes", "associative and commutative"),
            ("max", "yes", "max of maxes is the max"),
            ("count", "yes", "if the combiner emits partial counts"),
            ("MEAN", "NO", "mean of means is not the mean"),
            ("median", "NO", "needs every value at once")):
        print(f"      {what:<22}{safe:<16}{why}")
    # prove the mean case rather than asserting it
    groups = [[1, 1, 1, 10], [10]]
    naive = sum(sum(g) / len(g) for g in groups) / len(groups)
    true = sum(sum(g) for g in groups) / sum(len(g) for g in groups)
    print(f"\n      mean of means = {naive:.4f}, true mean = {true:.4f}")
    assert abs(naive - true) > 1
    print(f"""         {naive:.4f} against {true:.4f} on five numbers. To average safely,
         emit (sum, count) pairs from the combiner and divide only in
         the reducer -- and that is the same average-of-averages trap
         Course 11 met in DAX, in a different costume""")

    # ---- partitioning ----------------------------------------------------
    print("\n    3 reduce tasks instead of 1:")
    ptrace = {}
    three = run(INPUT, mapper, reducer, reducers=3, trace=ptrace)
    assert three == result, "the number of reducers must not change the answer"
    sizes = ptrace["partition_sizes"]
    print(f"      partition sizes: {sizes}   (total {sum(sizes)})")
    print(f"      largest / smallest = {max(sizes) / min(sizes):.2f}")
    print("""         hash partitioning is only as balanced as the KEY
         DISTRIBUTION. Natural language is Zipfian, so a real corpus
         skews far worse than this -- one reducer gets 'the' and
         finishes last, and the job's wall clock is that reducer.
         Skew, not volume, is what usually kills a MapReduce job""")

    return counts


if __name__ == "__main__":
    main()
