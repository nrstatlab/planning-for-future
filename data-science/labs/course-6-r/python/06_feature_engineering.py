"""Experiment 6 (Python equivalent) -- scaling, normalisation, encoding.

R version: ../06_feature_engineering.R  (scale(), model.matrix(), cut())
"""
from _shared import STUDENTS


def min_max(v):
    lo, hi = min(v), max(v)
    return [(x - lo) / (hi - lo) for x in v]


def standardise(v, sample=True):
    n = len(v)
    m = sum(v) / n
    div = (n - 1) if sample else n
    sd = (sum((x - m) ** 2 for x in v) / div) ** 0.5
    return [(x - m) / sd for x in v], m, sd


def one_hot(values):
    levels = sorted(set(values))
    return levels, [[1 if v == lv else 0 for lv in levels] for v in values]


def bin_values(v, edges, labels):
    out = []
    for x in v:
        for i in range(len(edges) - 1):
            if edges[i] <= x < edges[i + 1]:
                out.append(labels[i]); break
        else:
            out.append(labels[-1])
    return out


if __name__ == "__main__":
    marks = [r[4] for r in STUDENTS]
    sections = [r[1] for r in STUDENTS]

    print("MIN-MAX NORMALISATION          x' = (x - min)/(max - min)")
    nm = min_max(marks)
    for m, v in list(zip(marks, nm))[:5]:
        print(f"    {m:>3} -> {v:.4f}")
    print(f"    range check: min={min(nm):.4f}  max={max(nm):.4f}   (must be 0 and 1)")

    print("\nSTANDARDISATION                R: scale(x)  -- uses n-1")
    st, mean, sd = standardise(marks)
    print(f"    mean = {mean:.4f}   sd (n-1) = {sd:.4f}")
    for m, v in list(zip(marks, st))[:5]:
        print(f"    {m:>3} -> {v:+.4f}")
    chk_m = sum(st) / len(st)
    chk_s = (sum((x - chk_m) ** 2 for x in st) / (len(st) - 1)) ** 0.5
    print(f"    check: mean={chk_m:.10f} sd={chk_s:.6f}   (must be 0 and 1)")

    print("\nONE-HOT ENCODING               R: model.matrix(~ section - 1)")
    levels, encoded = one_hot(sections)
    print(f"    levels: {levels}")
    for s, e in list(zip(sections, encoded))[:5]:
        print(f"    {s} -> {e}")
    print("    NOTE: for a linear model R drops one level as the reference,")
    print("          giving k-1 columns and avoiding the dummy variable trap.")

    print("\nBINNING                        R: cut(marks, breaks = ...)")
    labels = ["Fail", "Pass", "Second", "First", "Distinction"]
    binned = bin_values(marks, [0, 40, 50, 60, 75, 101], labels)
    counts = {}
    for b in binned:
        counts[b] = counts.get(b, 0) + 1
    for lab in labels:
        print(f"    {lab:<12} {counts.get(lab, 0)}")

    assert abs(min(nm)) < 1e-12 and abs(max(nm) - 1) < 1e-12
    assert abs(chk_m) < 1e-10 and abs(chk_s - 1) < 1e-10
    print("\n  normalisation spans [0,1] and standardisation gives mean 0, sd 1 ✓")
