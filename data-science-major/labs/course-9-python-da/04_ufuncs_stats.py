"""Practical 4 — Universal functions and mathematical/statistical functions."""
import numpy as np
import pandas as pd
from fixtures import COURSE4_SAMPLE


def unary_ufuncs():
    a = np.array([1.0, 4.0, 9.0, 16.0])
    assert np.sqrt(a).tolist() == [1.0, 2.0, 3.0, 4.0]
    assert np.abs(np.array([-1, -2, 3])).tolist() == [1, 2, 3]
    assert np.sign(np.array([-3, 0, 5])).tolist() == [-1, 0, 1]

    b = np.array([1.2, 1.5, 1.8, -1.5])
    assert np.floor(b).tolist() == [1.0, 1.0, 1.0, -2.0]
    assert np.ceil(b).tolist() == [2.0, 2.0, 2.0, -1.0]
    assert np.trunc(b).tolist() == [1.0, 1.0, 1.0, -1.0]

    assert round(float(np.exp(1)), 6) == 2.718282
    assert np.log(np.e) == 1.0, "np.log is the NATURAL logarithm"
    assert np.log10(1000.0) == 3.0
    assert np.log2(8.0) == 3.0
    assert round(float(np.sin(np.pi / 2)), 10) == 1.0, "radians, not degrees"

    print("  unary ufuncs: sqrt, floor/ceil/trunc, exp, log (NATURAL), sin (radians)")


def maximum_versus_max():
    """A binary ufunc against a reduction -- routinely confused."""
    assert np.maximum([1, 5, 3], [4, 2, 6]).tolist() == [4, 5, 6], "PAIRWISE"
    assert np.max([1, 5, 3]) == 5, "the largest ONE value"
    assert np.minimum([1, 5, 3], [4, 2, 6]).tolist() == [1, 2, 3]
    assert np.min([1, 5, 3]) == 1
    print("  np.maximum pairs element-wise; np.max reduces to one value")


def nan_propagates():
    a = np.array([1.0, np.nan, 3.0])
    assert np.isnan(a.sum()), "one NaN poisons the whole reduction"
    assert np.nansum(a) == 4.0
    assert np.nanmean(a) == 2.0
    assert np.isnan(a).tolist() == [False, True, False]
    print("  NaN propagates through sum(); nansum/nanmean skip it")


def statistics():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    assert a.sum() == 21
    assert a.sum(axis=0).tolist() == [5, 7, 9]
    assert a.sum(axis=1).tolist() == [6, 15]
    assert a.mean() == 3.5
    assert a.min() == 1 and a.max() == 6
    assert a.argmin() == 0 and a.argmax() == 5, "argmin/argmax give the INDEX"
    assert a.cumsum().tolist() == [1, 3, 6, 10, 15, 21]
    assert np.median(a) == 3.5
    assert round(float(a.std()), 4) == 1.7078
    assert round(float(a.var()), 4) == 2.9167

    b = np.array([3, 1, 2])
    assert np.sort(b).tolist() == [1, 2, 3]
    assert b.tolist() == [3, 1, 2], "np.sort returns a COPY"
    assert np.argsort(b).tolist() == [1, 2, 0]
    b.sort()
    assert b.tolist() == [1, 2, 3], "the METHOD sorts in place"

    assert np.unique(np.array([3, 1, 3, 2, 1])).tolist() == [1, 2, 3]

    print(f"  statistics: sum {a.sum()}, per-column {a.sum(axis=0).tolist()}, "
          f"argmax {a.argmax()}, std {a.std():.4f}")


def ddof_is_the_examinable_one():
    """NumPy defaults to the POPULATION formula; Pandas to the SAMPLE one."""
    x = COURSE4_SAMPLE.to_numpy()
    assert x.tolist() == [2, 4, 4, 4, 5, 5, 7, 9]

    np_pop = float(np.std(x))
    np_sam = float(np.std(x, ddof=1))
    pd_default = float(pd.Series(x).std())

    assert np_pop == 2.0, "numpy default: ddof=0, POPULATION"
    assert round(np_sam, 4) == 2.1381, "ddof=1: SAMPLE"
    assert round(pd_default, 4) == 2.1381, "pandas default: ddof=1, SAMPLE"
    assert np_pop != pd_default, "the two libraries DISAGREE by default"

    # Course 4 taught the sample formula, so Pandas agrees and NumPy does not.
    assert round(pd_default, 4) == round(np_sam, 4)

    print(f"  ddof: np.std {np_pop} (population) vs pd.Series.std "
          f"{pd_default:.4f} (sample)")
    print(f"       SAME DATA, TWO LIBRARIES, TWO ANSWERS -- pass ddof explicitly")


def random_generation():
    rng = np.random.default_rng(42)
    r1 = rng.random(5)
    rng2 = np.random.default_rng(42)
    assert np.allclose(r1, rng2.random(5)), "same seed, same numbers"

    rng = np.random.default_rng(0)
    dice = rng.integers(1, 7, size=1000)
    assert dice.min() >= 1 and dice.max() <= 6, "high is EXCLUSIVE"

    # Two dice: P(sum = 7) is 6/36 exactly.
    rng = np.random.default_rng(0)
    rolls = rng.integers(1, 7, size=(10_000, 2))
    p7 = float((rolls.sum(axis=1) == 7).mean())
    exact = 6 / 36
    assert abs(p7 - exact) < 0.01, f"{p7} vs {exact}"

    print(f"  P(sum=7) simulated {p7:.4f} vs exact {exact:.4f} -- Course 4's")
    print(f"       classical probability confirmed empirically")


def main():
    print("Practical 4 -- Universal functions and statistics")
    unary_ufuncs()
    maximum_versus_max()
    nan_propagates()
    statistics()
    ddof_is_the_examinable_one()
    random_generation()


if __name__ == "__main__":
    main()
