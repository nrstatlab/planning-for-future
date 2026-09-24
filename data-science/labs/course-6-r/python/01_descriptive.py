"""Experiment 1 (Python equivalent) -- mean, median, mode, variance, SD.

R version: ../01_descriptive.R
The R script quotes these numbers; this file is what verifies them.
"""

import statistics
from collections import Counter

from _shared import MARKS


def describe(values):
    n = len(values)
    mean = sum(values) / n
    ordered = sorted(values)
    median = (statistics.median(values))
    counts = Counter(values)
    top = max(counts.values())
    modes = sorted(v for v, c in counts.items() if c == top)

    # R's var() and sd() are the SAMPLE versions -- divide by n-1.
    sample_var = sum((x - mean) ** 2 for x in values) / (n - 1)
    pop_var = sum((x - mean) ** 2 for x in values) / n

    return {
        "n": n, "mean": mean, "median": median,
        "mode": modes if top > 1 else None,
        "sample_var": sample_var, "sample_sd": sample_var ** 0.5,
        "pop_var": pop_var, "pop_sd": pop_var ** 0.5,
        "range": max(values) - min(values),
    }


if __name__ == "__main__":
    r = describe(MARKS)
    print("EXPERIMENT 1 -- Descriptive statistics")
    print(f"  n            = {r['n']}")
    print(f"  mean         = {r['mean']:.4f}")
    print(f"  median       = {r['median']:.4f}")
    print(f"  mode         = {r['mode'] if r['mode'] else 'none (all values unique)'}")
    print(f"  range        = {r['range']}")
    print(f"  var  (n-1)   = {r['sample_var']:.4f}   <- R's var()")
    print(f"  sd   (n-1)   = {r['sample_sd']:.4f}   <- R's sd()")
    print(f"  var  (n)     = {r['pop_var']:.4f}   <- population")
    print(f"  sd   (n)     = {r['pop_sd']:.4f}")

    assert abs(r["mean"] - statistics.mean(MARKS)) < 1e-9
    assert abs(r["sample_var"] - statistics.variance(MARKS)) < 1e-9
    assert abs(r["pop_var"] - statistics.pvariance(MARKS)) < 1e-9
    print("\n  cross-checked against the statistics module ✓")
    print("\n  NOTE: R's var() and sd() use n-1. R has no built-in mode();")
    print("        the R script defines one, as the syllabus expects.")
