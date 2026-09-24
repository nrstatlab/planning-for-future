"""Experiment 8 — K-Means clustering.

Reproduces Unit 5 section 5.2's 1-D trace and Practice Problem 1's 2-D trace
exactly, then demonstrates the elbow and silhouette methods on iris.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler


def kmeans_by_hand(points, centroids, max_iter=100):
    """Plain Lloyd's algorithm, so every iteration can be printed and checked.

    Ties go to the LOWER-indexed centroid, which is what the notes assume.
    """
    points = np.asarray(points, dtype=float)
    centroids = np.asarray(centroids, dtype=float)
    history = []

    for _ in range(max_iter):
        d = np.linalg.norm(points[:, None] - centroids[None], axis=-1)
        labels = d.argmin(axis=1)                       # argmin breaks ties low
        new = np.array([points[labels == k].mean(axis=0) for k in range(len(centroids))])
        history.append((labels.copy(), centroids.copy()))
        if np.allclose(new, centroids):
            return labels, centroids, history
        centroids = new
    return labels, centroids, history


def wcss(points, labels, centroids):
    points = np.asarray(points, dtype=float)
    return float(sum(((points[labels == k] - centroids[k]) ** 2).sum()
                     for k in range(len(centroids))))


def unit5_one_dimensional():
    """Section 5.2: points 2,4,10,12,3,20,30,11 with c = 2, 4."""
    X = np.array([[2], [4], [10], [12], [3], [20], [30], [11]], dtype=float)
    labels, cent, hist = kmeans_by_hand(X, [[2.0], [4.0]])

    c1 = sorted(X[labels == 0].ravel().tolist())
    c2 = sorted(X[labels == 1].ravel().tolist())
    assert c1 == [2, 3, 4], c1
    assert c2 == [10, 11, 12, 20, 30], c2
    assert round(float(cent[0][0]), 4) == 3.0
    assert round(float(cent[1][0]), 4) == 16.6

    w = wcss(X, labels, cent)
    assert round(w, 2) == 289.20, w

    # The outlier 30 alone contributes 62.5% of cluster 2's error.
    c2_err = float(((X[labels == 1] - cent[1]) ** 2).sum())
    share = (30 - 16.6) ** 2 / c2_err
    assert round(c2_err, 2) == 287.20
    assert round(share * 100, 1) == 62.5

    # Convergence took three passes: two that moved, one that confirmed.
    assert len(hist) == 3, f"the notes show three iterations, got {len(hist)}"

    print(f"  5.2 1-D: C1={c1} c=3.0, C2={c2} c=16.6, WCSS={w:.1f}")
    print(f"       the single outlier 30 contributes {share:.1%} of C2's error")


def unit5_practice_1():
    """Practice Problem 1: eight 2-D points, initial centroids A and C."""
    names = list("ABCDEFGH")
    X = np.array([[2, 10], [2, 5], [8, 4], [5, 8], [7, 5], [6, 4], [1, 2], [4, 9]],
                 dtype=float)
    labels, cent, hist = kmeans_by_hand(X, [[2.0, 10.0], [8.0, 4.0]])

    c1 = sorted(names[i] for i in range(8) if labels[i] == 0)
    c2 = sorted(names[i] for i in range(8) if labels[i] == 1)
    assert c1 == ["A", "B", "D", "H"], c1
    assert c2 == ["C", "E", "F", "G"], c2

    assert [round(v, 4) for v in cent[0]] == [3.25, 8.0], cent[0]
    assert [round(v, 4) for v in cent[1]] == [5.5, 3.75], cent[1]

    w = wcss(X, labels, cent)
    assert round(w, 2) == 54.50, w

    # G(1,2) is the far point: 42.8% of the total error.
    g_err = float(((X[6] - cent[1]) ** 2).sum())
    assert round(g_err, 4) == 23.3125
    assert round(g_err / w * 100, 1) == 42.8

    assert len(hist) == 2, "the notes show convergence after two iterations"

    print(f"  Practice 1: C1={c1} at (3.25, 8.0), C2={c2} at (5.5, 3.75)")
    print(f"       WCSS={w:.2f}; G alone contributes {g_err / w:.1%}")


def sklearn_agrees():
    """scikit-learn, given the same initial centroids, must land in the same place."""
    X = np.array([[2, 10], [2, 5], [8, 4], [5, 8], [7, 5], [6, 4], [1, 2], [4, 9]],
                 dtype=float)
    km = KMeans(n_clusters=2, init=np.array([[2.0, 10.0], [8.0, 4.0]]),
                n_init=1, random_state=0).fit(X)
    assert round(float(km.inertia_), 2) == 54.50, km.inertia_
    centres = sorted(tuple(round(v, 4) for v in c) for c in km.cluster_centers_)
    assert centres == [(3.25, 8.0), (5.5, 3.75)], centres
    print(f"  sklearn KMeans: inertia {km.inertia_:.2f} -- identical")


def initialisation_matters():
    """Section 5.2 weakness 2: K-Means finds only a LOCAL optimum."""
    rng = np.random.default_rng(0)
    X = np.vstack([rng.normal([0, 0], 0.5, (40, 2)),
                   rng.normal([5, 5], 0.5, (40, 2)),
                   rng.normal([0, 5], 0.5, (40, 2))])

    inertias = {KMeans(n_clusters=3, init="random", n_init=1,
                       random_state=s).fit(X).inertia_ for s in range(30)}
    assert len(inertias) > 1, "different seeds must give different local optima"

    best_single = min(inertias)
    multi = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X).inertia_
    assert multi <= max(inertias) + 1e-9

    print(f"  initialisation: {len(inertias)} distinct optima across 30 seeds "
          f"({min(inertias):.2f} to {max(inertias):.2f})")
    print(f"       n_init=10 finds {multi:.2f} -- which is why it is the default")


def choosing_k():
    """Elbow and silhouette on iris."""
    X, y = load_iris(return_X_y=True)
    Xs = StandardScaler().fit_transform(X)

    print("      k    WCSS  silhouette  Davies-Bouldin")
    sil = {}
    prev = None
    for k in range(2, 8):
        km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Xs)
        s = silhouette_score(Xs, km.labels_)
        db = davies_bouldin_score(Xs, km.labels_)
        sil[k] = s
        print(f"      {k}  {km.inertia_:7.2f}     {s:.4f}        {db:.4f}")
        if prev is not None:
            assert km.inertia_ < prev, "WCSS must fall monotonically with k"
        prev = km.inertia_

    best = max(sil, key=sil.get)
    assert best == 2, f"silhouette peaks at k=2 on scaled iris, got {best}"

    print(f"       silhouette peaks at k={best}, though iris has 3 species --")
    print(f"       two of them overlap, so the DATA says 2 and the LABELS say 3.")
    print(f"       That is exactly why clustering has no single right answer.")


def main():
    print("Experiment 8 -- K-Means")
    unit5_one_dimensional()
    unit5_practice_1()
    sklearn_agrees()
    initialisation_matters()
    choosing_k()
    print("  all Unit 5 K-Means calculations reproduced")


if __name__ == "__main__":
    main()
