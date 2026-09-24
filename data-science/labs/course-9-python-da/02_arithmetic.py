"""Practical 2 — Arithmetic, broadcasting and why vectorising matters."""
import time
import numpy as np


def list_versus_array():
    """The first thing to get right coming from Course 3."""
    assert [1, 2, 3] + [4, 5, 6] == [1, 2, 3, 4, 5, 6], "lists CONCATENATE"
    assert (np.array([1, 2, 3]) + np.array([4, 5, 6])).tolist() == [5, 7, 9], "arrays ADD"

    assert [1, 2, 3] * 2 == [1, 2, 3, 1, 2, 3], "lists REPEAT"
    assert (np.array([1, 2, 3]) * 2).tolist() == [2, 4, 6], "arrays SCALE"

    print("  + concatenates lists and ADDS arrays; * repeats lists and SCALES arrays")


def elementwise():
    a = np.array([1, 2, 3, 4])
    b = np.array([10, 20, 30, 40])
    assert (a + b).tolist() == [11, 22, 33, 44]
    assert (a * b).tolist() == [10, 40, 90, 160]
    assert (b / a).tolist() == [10.0] * 4
    assert (a ** 2).tolist() == [1, 4, 9, 16]
    assert (a > 2).tolist() == [False, False, True, True]
    print("  element-wise arithmetic and comparison, no loop anywhere")


def broadcasting():
    a = np.array([[1, 2, 3], [4, 5, 6]])          # (2, 3)

    assert (a + 10).tolist() == [[11, 12, 13], [14, 15, 16]]
    assert (a + np.array([10, 20, 30])).tolist() == [[11, 22, 33], [14, 25, 36]]
    assert (a + np.array([[10], [20]])).tolist() == [[11, 12, 13], [24, 25, 26]]

    # Centring each COLUMN works: mean(axis=0) has shape (3,)
    assert a.mean(axis=0).shape == (3,)
    assert (a - a.mean(axis=0)).shape == (2, 3)

    # Centring each ROW does NOT, without keepdims -- and seeing the error is
    # what makes keepdims memorable.
    assert a.mean(axis=1).shape == (2,)
    try:
        a - a.mean(axis=1)
        raise AssertionError("expected a broadcasting ValueError")
    except ValueError as e:
        assert "broadcast" in str(e).lower() or "shape" in str(e).lower()

    assert a.mean(axis=1, keepdims=True).shape == (2, 1)
    assert (a - a.mean(axis=1, keepdims=True)).shape == (2, 3)
    assert (a - a.mean(axis=1)[:, np.newaxis]).shape == (2, 3)

    print("  broadcasting: (2,3)+(3,) per row, (2,3)+(2,1) per column")
    print("       centring rows NEEDS keepdims=True -- ValueError without it")


def axis_is_the_one_that_disappears():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    assert a.sum() == 21
    assert a.sum(axis=0).tolist() == [5, 7, 9], "axis=0 collapses ROWS -> per COLUMN"
    assert a.sum(axis=1).tolist() == [6, 15], "axis=1 collapses COLUMNS -> per ROW"
    assert a.sum(axis=0).shape == (3,)
    assert a.sum(axis=1).shape == (2,)
    print("  axis=0 -> [5 7 9] (one per column); axis=1 -> [6 15] (one per row)")


def vectorising_is_faster():
    """Best of three, to avoid an unwarmed single run misleading us."""
    n = 1_000_000
    lst = list(range(n))
    arr = np.arange(n, dtype=np.float64)
    lstf = [float(v) for v in lst]

    def best(fn, reps=3):
        t = float("inf")
        for _ in range(reps):
            s = time.perf_counter()
            fn()
            t = min(t, time.perf_counter() - s)
        return t

    cases = [
        ("x * 2",       lambda: [v * 2 for v in lstf],  lambda: arr * 2),
        ("sqrt(x)",     lambda: [v ** 0.5 for v in lstf], lambda: np.sqrt(arr)),
        ("dot product", lambda: sum(x * y for x, y in zip(lstf, lstf)),
                        lambda: arr @ arr),
    ]

    print(f"  vectorisation on {n:,} elements (best of 3)")
    for name, py, npf in cases:
        # Correctness first. This is the assertion that means something: the
        # two paths must agree, or the comparison is between two different
        # calculations and the timing is meaningless.
        py_result, np_result = py(), npf()
        assert np.allclose(np.asarray(py_result), np.asarray(np_result)), name

        p, q = best(py), best(npf)
        speedup = p / q
        print(f"    {name:12s} python {p*1000:7.1f} ms   numpy {q*1000:6.2f} ms"
              f"   {speedup:6.1f}x")

        # Only that NumPy wins is asserted, not by how much.
        #
        # This assertion used to demand a 10x floor, and it failed on a loaded
        # machine at 7.1x for the dot product -- a false alarm, because a wall
        # clock measures the machine, not the code. A threshold that fails
        # when nothing is wrong teaches the reader to ignore failures, which
        # is worse than having no threshold at all. So the factor is reported,
        # not asserted, and the number you see is the one this run measured.
        assert speedup > 1, f"{name} was not faster in NumPy ({speedup:.1f}x)"

    # A note on the dot product, because its number moves the most. `arr @ arr`
    # goes to BLAS, which is threaded and memory-bandwidth-bound, so what it
    # measures is partly the machine: this same line has been seen at 7x with
    # other work running on the box and at over 300x on an idle one, on the
    # same data. The two element-wise cases are far steadier because they are
    # dominated by allocating a million-element Python list.
    #
    # That spread is the argument against asserting a threshold here. It is
    # also the more useful lesson than any single figure: a timing is a
    # measurement of a machine at a moment, and quoting one as though it were
    # a property of the code is how benchmarks mislead.


def main():
    print("Practical 2 -- Arithmetic and broadcasting")
    list_versus_array()
    elementwise()
    broadcasting()
    axis_is_the_one_that_disappears()
    vectorising_is_faster()


if __name__ == "__main__":
    main()
