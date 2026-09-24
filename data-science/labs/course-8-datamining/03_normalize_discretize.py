"""Experiment 3 — Normalization and discretization.

WEKA equivalents: filters/unsupervised/attribute/{Normalize, Standardize,
Discretize} and filters/supervised/attribute/Discretize.

Reproduces Unit 2 sections 2.9 and 2.10 exactly.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import (MinMaxScaler, StandardScaler, RobustScaler,
                                   KBinsDiscretizer)


def unit2_normalisation():
    """Section 2.10: income 73600, min 12000, max 98000, mu 54000, sd 16000."""
    x, lo, hi, mu, sd = 73600, 12000, 98000, 54000, 16000

    assert round((x - lo) / (hi - lo), 4) == 0.7163
    assert round((x - mu) / sd, 4) == 1.225
    j = len(str(hi))                       # smallest j with max|x'| < 1
    assert j == 5 and round(x / 10 ** j, 4) == 0.736

    print(f"  2.10: min-max {(x-lo)/(hi-lo):.4f}, z-score {(x-mu)/sd:.4f}, "
          f"decimal {x/10**j:.4f}")


def outlier_destroys_minmax():
    """Section 2.10: one outlier crushes every other value into a tiny range."""
    v = np.array([[10.0], [12.0], [11.0], [13.0], [1000.0]])
    scaled = MinMaxScaler().fit_transform(v).ravel()

    assert [round(s, 4) for s in scaled] == [0.0, 0.002, 0.001, 0.003, 1.0], scaled
    assert scaled[:4].max() < 0.01, "four sensible values inside 1% of the range"

    z = StandardScaler().fit_transform(v).ravel()
    r = RobustScaler().fit_transform(v).ravel()
    assert abs(z[:4]).max() < abs(z[4]), "z-score also flags the outlier, less brutally"
    assert abs(r[:4]).max() < 2, "robust scaling keeps the sensible values sensible"

    print(f"  outlier: min-max gives {[round(float(s), 4) for s in scaled]}")
    print(f"       robust  gives {[round(float(s), 2) for s in r]}")
    print(f"       min-max crushes the four real values into 0.3% of the range;")
    print(f"       robust keeps them spread and leaves the outlier VISIBLE as one")


def unit2_binning():
    """Section 2.6: prices 4,8,9,15,21,21,24,25,26,28,29,34 in equal-frequency
    bins of depth 4, smoothed three ways."""
    v = [4, 8, 9, 15, 21, 21, 24, 25, 26, 28, 29, 34]
    bins = [v[0:4], v[4:8], v[8:12]]

    means = [sum(b) / len(b) for b in bins]
    assert means == [9.0, 22.75, 29.25], means

    medians = [float(np.median(b)) for b in bins]
    assert medians[0] == 8.5

    def boundaries(b):
        lo, hi = min(b), max(b)
        return [lo if abs(x - lo) <= abs(x - hi) else hi for x in b]

    assert boundaries(bins[0]) == [4, 4, 4, 15], boundaries(bins[0])

    print(f"  2.6: bin means {means}; bin-1 boundaries {boundaries(bins[0])}")


def unit2_discretization():
    """Section 2.9: ages 8,15,22,25,31,38,44,51,67 into 3 bins."""
    ages = np.array([8, 15, 22, 25, 31, 38, 44, 51, 67], dtype=float)

    rng = ages.max() - ages.min()
    assert rng == 59
    width = rng / 3
    assert round(width, 2) == 19.67
    edges = [ages.min() + width, ages.min() + 2 * width]
    assert [round(e, 2) for e in edges] == [27.67, 47.33], edges

    ew = KBinsDiscretizer(n_bins=3, encode="ordinal", strategy="uniform",
                          quantile_method="averaged_inverted_cdf"
                          ).fit(ages.reshape(-1, 1))
    got = [round(float(e), 2) for e in ew.bin_edges_[0]]
    assert got == [8.0, 27.67, 47.33, 67.0], got
    counts = np.bincount(ew.transform(ages.reshape(-1, 1)).ravel().astype(int))
    assert counts.tolist() == [4, 3, 2], "equal WIDTH gives uneven counts"

    ef = KBinsDiscretizer(n_bins=3, encode="ordinal", strategy="quantile",
                          quantile_method="averaged_inverted_cdf"
                          ).fit(ages.reshape(-1, 1))
    fcounts = np.bincount(ef.transform(ages.reshape(-1, 1)).ravel().astype(int))
    assert fcounts.tolist() == [3, 3, 3], "equal FREQUENCY gives equal counts"

    print(f"  2.9: equal-width edges {got} -> counts {counts.tolist()}")
    print(f"       equal-frequency -> counts {fcounts.tolist()}")


def binarization_trap():
    """Section 2.9: integer-encoding an UNORDERED category is a bug."""
    colours = ["red", "green", "blue", "red"]

    integer = pd.Series(colours).map({"red": 1, "green": 2, "blue": 3})
    # Under this encoding green is exactly BETWEEN red and blue, which is false.
    assert integer[1] == (integer[0] + integer[2]) / 2, \
        "the arithmetic that integer encoding invents"

    onehot = pd.get_dummies(pd.Series(colours), prefix="is")
    assert list(onehot.columns) == ["is_blue", "is_green", "is_red"]
    assert onehot.sum(axis=1).tolist() == [1, 1, 1, 1], "exactly one 1 per row"

    # The dummy variable trap: k columns are perfectly collinear.
    dropped = pd.get_dummies(pd.Series(colours), drop_first=True)
    assert dropped.shape[1] == 2, "k-1 columns for linear models"

    # An ORDERED category is different -- integers preserve real information.
    ordinal = pd.Series(["low", "high", "medium"]).map({"low": 1, "medium": 2, "high": 3})
    assert ordinal.tolist() == [1, 3, 2]

    print("  one-hot for unordered, integers only where the order is real")
    print("       (k-1 columns for linear models -- the dummy variable trap)")


def which_algorithms_need_scaling():
    """Section 2.10: trees do NOT need scaling; distance methods do."""
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.datasets import load_iris
    from sklearn.model_selection import cross_val_score

    X, y = load_iris(return_X_y=True)
    X_skewed = X.copy()
    X_skewed[:, 0] *= 10000                 # blow up one feature's scale

    tree_raw = cross_val_score(DecisionTreeClassifier(random_state=0), X, y, cv=5).mean()
    tree_skew = cross_val_score(DecisionTreeClassifier(random_state=0), X_skewed, y, cv=5).mean()
    assert abs(tree_raw - tree_skew) < 1e-12, \
        "a tree splits on ORDER, which scaling does not change"

    knn_raw = cross_val_score(KNeighborsClassifier(), X, y, cv=5).mean()
    knn_skew = cross_val_score(KNeighborsClassifier(), X_skewed, y, cv=5).mean()
    assert knn_skew < knn_raw, "k-NN is broken by the rescaled feature"

    print(f"  scaling: tree {tree_raw:.4f} -> {tree_skew:.4f} (IDENTICAL); "
          f"k-NN {knn_raw:.4f} -> {knn_skew:.4f} (broken)")


def main():
    print("Experiment 3 -- Normalization and discretization")
    unit2_normalisation()
    outlier_destroys_minmax()
    unit2_binning()
    unit2_discretization()
    binarization_trap()
    which_algorithms_need_scaling()
    print("  all Unit 2 transformation claims verified")


if __name__ == "__main__":
    main()
