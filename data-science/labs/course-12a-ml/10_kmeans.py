"""Experiment 10 — K-Means clustering.

Reproduces unit-5.md section 5.5, including the result worth remembering:
silhouette prefers k=2 on iris, where the truth is k=3.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

from fixtures import RANDOM_STATE, iris_frame

_, DATA = iris_frame()
X_RAW = DATA.data.to_numpy()
Y = DATA.target
Z = StandardScaler().fit_transform(X_RAW)


def the_elbow():
    """unit-5.md's WCSS table, including the k=1 arithmetic check."""
    rows = []
    for k in range(1, 7):
        km = KMeans(k, n_init=10, random_state=RANDOM_STATE).fit(Z)
        sil = silhouette_score(Z, km.labels_) if k > 1 else None
        rows.append((k, km.inertia_, sil))

    wcss = {k: w for k, w, _ in rows}
    sils = {k: s for k, _, s in rows if s is not None}

    assert round(wcss[1], 4) == 600.0, wcss[1]
    assert wcss[1] == len(Z) * Z.shape[1], "n x p, because each column has variance 1"
    assert round(wcss[2], 4) == 222.3617
    assert round(wcss[3], 4) == 139.8205
    assert round(wcss[6], 4) == 81.5444
    assert all(wcss[k] > wcss[k + 1] for k in range(1, 6)), \
        "WCSS falls monotonically -- which is why it alone cannot choose k"

    print(f"    {'k':>3} {'WCSS':>10} {'drop':>10} {'silhouette':>12}")
    for k, w, s in rows:
        drop = "" if k == 1 else f"{wcss[k - 1] - w:10.4f}"
        sil = "" if s is None else f"{s:12.4f}"
        print(f"    {k:3d} {w:10.4f} {drop:>10} {sil:>12}")
    print(f"       WCSS at k=1 is exactly {wcss[1]:.0f} = n x p = "
          f"{len(Z)} x {Z.shape[1]} -- a free check that the data really was")
    print("       standardised. The big drops are to k=2 and k=3, then it")
    print("       flattens: the elbow is at 2 or 3")
    return wcss, sils


def silhouette_disagrees_with_the_truth(sils):
    """The most instructive result in the unit."""
    km2 = KMeans(2, n_init=10, random_state=RANDOM_STATE).fit(Z)
    km3 = KMeans(3, n_init=10, random_state=RANDOM_STATE).fit(Z)

    ari2 = adjusted_rand_score(Y, km2.labels_)
    ari3 = adjusted_rand_score(Y, km3.labels_)

    assert round(sils[2], 4) == 0.5818
    assert round(sils[3], 4) == 0.4599
    assert sils[2] > sils[3], "silhouette PREFERS k=2"
    assert round(ari3, 4) == 0.6201, round(ari3, 4)
    assert ari3 > ari2, "yet k=3 agrees far better with the true species"
    assert len(set(Y)) == 3, "and there really are three species"

    print(f"    k=2: silhouette {sils[2]:.4f}   ARI vs species {ari2:.4f}")
    print(f"    k=3: silhouette {sils[3]:.4f}   ARI vs species {ari3:.4f}")
    print(f"    iris has {len(set(Y))} species")
    print("       SILHOUETTE SAYS 2. THE TRUTH IS 3. Nothing is broken: setosa")
    print("       is cleanly separate while versicolor and virginica overlap,")
    print("       so by a purely geometric measure two groups ARE tidier.")
    print("       An internal metric measures tidiness, not correctness --")
    print("       never choose k from silhouette alone")


def where_the_errors_fall():
    """Which species K-Means confuses, and why that is the expected answer."""
    km = KMeans(3, n_init=10, random_state=RANDOM_STATE).fit(Z)
    names = list(DATA.target_names)

    table = np.zeros((3, 3), dtype=int)
    for true, cluster in zip(Y, km.labels_):
        table[true, cluster] += 1

    # Setosa lands entirely in one cluster; the other two bleed into each other.
    setosa_row = table[names.index("setosa")]
    assert setosa_row.max() == 50 and setosa_row.sum() == 50, \
        "all 50 setosa in ONE cluster"
    versicolor = table[names.index("versicolor")]
    virginica = table[names.index("virginica")]
    assert (versicolor > 0).sum() >= 2 or (virginica > 0).sum() >= 2, \
        "at least one of the other two is split"

    print("    species      cluster0 cluster1 cluster2")
    for i, name in enumerate(names):
        print(f"    {name:12s} {table[i, 0]:8d} {table[i, 1]:8d} {table[i, 2]:8d}")
    print("       setosa is captured perfectly; versicolor and virginica are")
    print("       the pair that overlaps. That is exactly why silhouette")
    print("       prefers two clusters, and it is a property of the FLOWERS")


def initialisation_matters():
    """K-Means finds a LOCAL minimum. n_init exists for this reason."""
    single = KMeans(3, n_init=1, init="random",
                    random_state=7).fit(Z).inertia_
    many = KMeans(3, n_init=20, init="random",
                  random_state=7).fit(Z).inertia_
    plus = KMeans(3, n_init=10, init="k-means++",
                  random_state=RANDOM_STATE).fit(Z).inertia_

    assert many <= single, (many, single)
    assert round(plus, 4) == 139.8205

    print(f"    random init, n_init=1   WCSS {single:.4f}")
    print(f"    random init, n_init=20  WCSS {many:.4f}")
    print(f"    k-means++,   n_init=10  WCSS {plus:.4f}")
    print("       the objective never increases within a run, so K-Means always")
    print("       converges -- to a LOCAL minimum. Restarts and k-means++ are")
    print("       how that is managed, and both are scikit-learn defaults now")


def outliers_drag_the_centroid():
    """Weakness 4: the mean is not robust."""
    base = np.array([[1.0, 1.0], [1.2, 0.9], [0.9, 1.1], [1.1, 1.0]])
    with_outlier = np.vstack([base, [[50.0, 50.0]]])

    clean_centre = base.mean(axis=0)
    dragged = with_outlier.mean(axis=0)

    assert np.allclose(clean_centre, [1.05, 1.0])
    assert dragged[0] > 10, dragged
    # A medoid -- an actual data point -- is unmoved.
    medoid = base[np.argmin([np.abs(base - p).sum() for p in base])]
    assert np.allclose(medoid, [1.0, 1.0]) or np.allclose(medoid, [1.1, 1.0])

    print(f"    4 tight points, centroid {np.round(clean_centre, 4)}")
    print(f"    add ONE point at (50, 50): centroid {np.round(dragged, 4)}")
    print(f"    the medoid (a real data point) stays at {np.round(medoid, 4)}")
    print("       one outlier moved the centre by ~10 units. k-Medoids uses an")
    print("       actual data point and is unmoved -- that is its main")
    print("       advantage, along with accepting any distance metric")


def main():
    print("Experiment 10 -- K-Means clustering")
    print("  the elbow method on standardised iris:")
    wcss, sils = the_elbow()
    print("  silhouette against the ground truth:")
    silhouette_disagrees_with_the_truth(sils)
    print("  where the errors fall:")
    where_the_errors_fall()
    print("  initialisation:")
    initialisation_matters()
    print("  sensitivity to outliers:")
    outliers_drag_the_centroid()


if __name__ == "__main__":
    main()
