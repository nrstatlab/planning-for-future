"""Practical 3 — Indexing, slicing, boolean and fancy indexing."""
import numpy as np


def basic_slicing():
    a = np.arange(10)
    assert a[0] == 0 and a[-1] == 9
    assert a[2:5].tolist() == [2, 3, 4]
    assert a[:3].tolist() == [0, 1, 2]
    assert a[::2].tolist() == [0, 2, 4, 6, 8]
    assert a[::-1].tolist() == list(range(9, -1, -1))

    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert m[1, 2] == 6
    assert m[1][2] == 6, "works, but builds a temporary row first"
    assert m[1].tolist() == [4, 5, 6]
    assert m[:, 1].tolist() == [2, 5, 8]
    assert m[0:2, 1:3].tolist() == [[2, 3], [5, 6]]
    assert m[::2, ::2].tolist() == [[1, 3], [7, 9]]
    print("  slicing: comma for 2-D, m[:, 1] for a column, strides work per axis")


def views_and_copies():
    """The behaviour that differs from Python lists and causes real bugs."""
    lst = [1, 2, 3, 4, 5]
    s = lst[1:4]
    s[0] = 99
    assert lst == [1, 2, 3, 4, 5], "list slicing COPIES"

    a = np.array([1, 2, 3, 4, 5])
    v = a[1:4]
    v[0] = 99
    assert a.tolist() == [1, 99, 3, 4, 5], "array slicing is a VIEW"
    assert a[1:4].base is a, "a view knows its parent"

    b = np.array([1, 2, 3, 4, 5])
    f = b[[0, 2]]
    f[0] = 99
    assert b.tolist() == [1, 2, 3, 4, 5], "fancy indexing COPIES"
    assert b[[0, 2]].base is not b

    c = np.array([1, 2, 3, 4, 5])
    mask = c[c > 2]
    mask[0] = 99
    assert c.tolist() == [1, 2, 3, 4, 5], "boolean masking COPIES"

    d = np.array([1, 2, 3, 4, 5])
    e = d[1:4].copy()
    e[0] = 99
    assert d.tolist() == [1, 2, 3, 4, 5], ".copy() opts out of the view"

    print("  slice -> VIEW; boolean and fancy -> COPY; .copy() when you mean it")


def boolean_indexing():
    marks = np.array([72, 45, 91, 66, 38, 88])

    assert (marks > 50).tolist() == [True, False, True, True, False, True]
    assert marks[marks > 50].tolist() == [72, 91, 66, 88]
    assert marks[marks > 50].mean() == 79.25
    assert marks[(marks > 50) & (marks < 90)].tolist() == [72, 66, 88]
    assert sorted(marks[(marks < 40) | (marks > 90)].tolist()) == [38, 91]
    assert marks[~(marks > 50)].tolist() == [45, 38]

    assert (marks > 50).sum() == 4, "True counts as 1"
    assert round(float((marks > 50).mean()), 4) == 0.6667, "the PROPORTION"
    assert (marks > 50).any() and not (marks > 50).all()
    assert np.where(marks > 50)[0].tolist() == [0, 2, 3, 5], "the INDICES"

    graded = np.where(marks >= 50, "Pass", "Fail")
    assert graded.tolist() == ["Pass", "Fail", "Pass", "Pass", "Fail", "Pass"]

    print("  boolean: (cond).sum() counts, (cond).mean() gives the proportion")


def and_raises():
    """Python's `and` cannot reduce an array to one truth value."""
    marks = np.array([72, 45, 91, 66, 38, 88])
    try:
        marks[(marks > 50) and (marks < 90)]
        raise AssertionError("expected ValueError from `and`")
    except ValueError as e:
        assert "ambiguous" in str(e)
    print("  `and` raises 'truth value is ambiguous' -- use & with parentheses")


def fancy_indexing():
    a = np.array([10, 20, 30, 40, 50])
    assert a[[0, 2, 4]].tolist() == [10, 30, 50]
    assert a[[4, 4, 0]].tolist() == [50, 50, 10], "repeats and any order allowed"

    m = np.arange(12).reshape(3, 4)
    assert m[[0, 2]].tolist() == [[0, 1, 2, 3], [8, 9, 10, 11]]

    # Two index arrays are PAIRED position by position -- three elements,
    # not a 3x3 block. np.ix_ is what gives the submatrix.
    assert m[[0, 1, 2], [1, 2, 3]].tolist() == [1, 6, 11]
    assert m[np.ix_([0, 2], [1, 3])].tolist() == [[1, 3], [9, 11]]
    assert m[np.ix_([0, 2], [1, 3])].shape == (2, 2)

    print("  fancy: m[[0,1,2],[1,2,3]] pairs -> 3 elements; np.ix_ -> the 2x2 block")


def reshaping():
    a = np.arange(12)
    assert a.reshape(3, 4).shape == (3, 4)
    assert a.reshape(3, -1).shape == (3, 4), "-1 means 'work it out'"
    assert a.reshape(-1, 1).shape == (12, 1)

    try:
        a.reshape(5, 3)
        raise AssertionError("expected a size mismatch")
    except ValueError:
        pass

    m = np.arange(6).reshape(2, 3)
    assert m.T.shape == (3, 2)
    assert m.T.base is not None, ".T is a VIEW -- transposing costs nothing"
    assert np.swapaxes(m, 0, 1).tolist() == m.T.tolist()

    t = np.arange(24).reshape(2, 3, 4)
    assert t.transpose(1, 0, 2).shape == (3, 2, 4)
    assert np.swapaxes(t, 0, 2).shape == (4, 3, 2)

    # concatenate joins along an EXISTING axis; stack ADDS one.
    x, y = np.array([1, 2]), np.array([3, 4])
    assert np.concatenate([x, y]).shape == (4,)
    assert np.stack([x, y]).shape == (2, 2)

    print("  reshape(-1) infers; .T is a view; concatenate keeps ndim, stack adds one")


def main():
    print("Practical 3 -- Indexing and slicing")
    basic_slicing()
    views_and_copies()
    boolean_indexing()
    and_raises()
    fancy_indexing()
    reshaping()


if __name__ == "__main__":
    main()
