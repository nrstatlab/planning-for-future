"""Practical 1 — Create and manipulate NumPy ndarrays; explore data types."""
import numpy as np


def creating():
    a = np.array([1, 2, 3])
    assert a.tolist() == [1, 2, 3]

    assert np.zeros(5).tolist() == [0.0] * 5
    assert np.zeros((2, 3)).shape == (2, 3)
    assert np.ones((2, 3)).sum() == 6
    assert np.full((2, 3), 7).ravel().tolist() == [7] * 6
    assert np.eye(3).trace() == 3.0
    assert np.diag([1, 2, 3]).sum() == 6

    assert np.arange(10).tolist() == list(range(10))
    assert np.arange(2, 10, 2).tolist() == [2, 4, 6, 8]
    assert np.linspace(0, 1, 5).tolist() == [0.0, 0.25, 0.5, 0.75, 1.0]

    # arange with a float step: the COUNT is not always what the arithmetic
    # suggests, because of floating-point accumulation. linspace asks for a
    # count and delivers it.
    assert np.linspace(0, 1, 11).size == 11
    assert np.arange(0, 0.3, 0.1).size == 3

    rng = np.random.default_rng(42)
    r = rng.random((2, 3))
    assert r.shape == (2, 3) and (0 <= r).all() and (r < 1).all()

    print("  creation: zeros, ones, full, eye, arange, linspace, rng -- all as documented")


def attributes():
    a = np.array([[1, 2], [3, 4]])
    assert a.ndim == 2
    assert a.shape == (2, 2)
    assert a.size == 4
    assert a.dtype == np.int64
    assert a.itemsize == 8
    assert a.nbytes == 32

    # A 1-D array's shape is a 1-TUPLE, not an int and not (n, 1).
    assert np.array([1, 2, 3]).shape == (3,)
    assert np.array([1, 2, 3]).reshape(-1, 1).shape == (3, 1)

    print(f"  attributes: ndim {a.ndim}, shape {a.shape}, size {a.size}, "
          f"itemsize {a.itemsize}, nbytes {a.nbytes}")


def dtype_traps():
    # 1. Integer overflow WRAPS, silently.
    assert (np.array([127], dtype=np.int8) + 1)[0] == -128

    # 2. Assigning a float into an int array TRUNCATES, silently.
    a = np.array([1, 2, 3])
    a[0] = 3.7
    assert a.tolist() == [3, 2, 3]

    # ...and then true division still gives float64
    assert (a / 2).tolist() == [1.5, 1.0, 1.5]
    assert (a // 2).tolist() == [1, 1, 1]

    # 3. One string makes EVERYTHING a string.
    assert np.array([1, 2, "3"]).dtype.str == "<U21"

    # 4. Mixing int and float upcasts to float.
    assert np.array([1, 2, 3.5]).dtype == np.float64

    # astype always COPIES
    b = np.array([1, 2, 3])
    c = b.astype(np.float64)
    c[0] = 99
    assert b[0] == 1, "astype must not alias"

    print("  dtypes: int8 127+1 -> -128; 3.7 into int -> 3; one string -> all strings")


def empty_is_not_zeros():
    """np.empty hands you whatever was in that memory."""
    e = np.empty((2, 3))
    assert e.shape == (2, 3)
    # We cannot assert its CONTENTS -- that is exactly the point.
    z = np.zeros((2, 3))
    assert z.sum() == 0.0
    print("  np.empty allocates without zeroing -- faster, and a bug if unfilled")


def main():
    print("Practical 1 -- ndarray basics and dtypes")
    creating()
    attributes()
    dtype_traps()
    empty_is_not_zeros()


if __name__ == "__main__":
    main()
