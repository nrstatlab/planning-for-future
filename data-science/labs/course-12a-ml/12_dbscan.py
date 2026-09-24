"""Experiment 12 — DBSCAN.

The cleanest experiment in Unit 5: on two interleaved crescents DBSCAN scores
ARI 1.0000 and K-Means 0.2475. The reason is structural, not a matter of
tuning, and this script demonstrates that too.
"""
import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from fixtures import RANDOM_STATE, iris_frame

XM, YM = make_moons(n_samples=300, noise=0.06, random_state=RANDOM_STATE)


def dbscan_beats_kmeans_on_non_convex_clusters():
    """unit-5.md 5.8's headline result."""
    km = KMeans(2, n_init=10, random_state=RANDOM_STATE).fit(XM)
    db = DBSCAN(eps=0.25, min_samples=5).fit(XM)

    ari_km = adjusted_rand_score(YM, km.labels_)
    ari_db = adjusted_rand_score(YM, db.labels_)
    clusters = len(set(db.labels_) - {-1})
    noise = int((db.labels_ == -1).sum())

    assert round(ari_km, 4) == 0.2475, round(ari_km, 4)
    assert round(ari_db, 4) == 1.0000, round(ari_db, 4)
    assert clusters == 2 and noise == 0

    print(f"  two interleaved crescents, 300 points:")
    print(f"    K-Means (k=2)  ARI {ari_km:.4f}")
    print(f"    DBSCAN         ARI {ari_db:.4f}   "
          f"{clusters} clusters, {noise} noise points")
    print("       DBSCAN recovers them PERFECTLY; K-Means is barely better")
    print("       than random")


def no_k_can_save_kmeans_here():
    """It is not a tuning problem. That is the point worth proving."""
    best = 0.0
    for k in range(2, 11):
        km = KMeans(k, n_init=10, random_state=RANDOM_STATE).fit(XM)
        best = max(best, adjusted_rand_score(YM, km.labels_))

    assert best < 0.55, best

    print(f"  the best ARI K-Means achieves over k = 2..10: {best:.4f}")
    print("       K-Means assigns each point to the NEAREST CENTROID, so its")
    print("       boundaries are straight perpendicular bisectors. A crescent")
    print("       cannot be carved out that way at ANY k. This is structural,")
    print("       not a tuning failure -- which is why the right answer is a")
    print("       different algorithm and not a better k")


def core_border_and_noise():
    """The three kinds of point, counted."""
    db = DBSCAN(eps=0.25, min_samples=5).fit(XM)

    core = np.zeros(len(XM), dtype=bool)
    core[db.core_sample_indices_] = True
    clustered = db.labels_ != -1
    border = clustered & ~core
    noise = ~clustered

    assert core.sum() + border.sum() + noise.sum() == len(XM)
    assert core.sum() > 0
    assert noise.sum() == 0, "this eps leaves no noise on clean crescents"

    # Tighten eps until noise appears -- that is what the parameter does.
    tight = DBSCAN(eps=0.10, min_samples=5).fit(XM)
    tight_noise = int((tight.labels_ == -1).sum())
    assert tight_noise > 0, "a smaller neighbourhood makes more points noise"

    print(f"  eps=0.25: core {core.sum()}, border {border.sum()}, "
          f"noise {noise.sum()}   (total {len(XM)})")
    print(f"  eps=0.10: noise rises to {tight_noise} points, "
          f"{len(set(tight.labels_) - {-1})} clusters")
    print("       a CORE point has >= min_samples neighbours within eps; a")
    print("       BORDER point is within eps of a core but is not core itself;")
    print("       everything else is NOISE and belongs to no cluster. K-Means")
    print("       has no such category -- it forces every point into a cluster")


def choosing_eps_with_a_k_distance_plot():
    """The standard heuristic, computed."""
    min_samples = 5
    neighbours = NearestNeighbors(n_neighbors=min_samples).fit(XM)
    distances, _ = neighbours.kneighbors(XM)
    kth = np.sort(distances[:, -1])

    # The elbow is where the sorted curve turns up sharply.
    knee = float(np.percentile(kth, 95))

    assert kth[0] <= kth[-1], "sorted ascending"
    assert 0.05 < knee < 0.35, knee

    working = DBSCAN(eps=knee, min_samples=min_samples).fit(XM)
    assert len(set(working.labels_) - {-1}) >= 1

    print(f"  k-distance plot with k = min_samples = {min_samples}:")
    print(f"    median {np.median(kth):.4f}, 95th percentile {knee:.4f}, "
          f"max {kth[-1]:.4f}")
    print(f"    eps = {knee:.4f} gives "
          f"{len(set(working.labels_) - {-1})} clusters, "
          f"{int((working.labels_ == -1).sum())} noise")
    print("       sort every point's distance to its k-th neighbour and take")
    print("       the ELBOW. Below it points are inside a dense region; above")
    print("       it they are not. minPts >= p+1, often 2p")


def dbscan_struggles_with_varying_density():
    """Its real weakness: one eps cannot serve two densities."""
    dense, _ = make_blobs(n_samples=200, centers=[[0, 0]], cluster_std=0.20,
                          random_state=RANDOM_STATE)
    sparse, _ = make_blobs(n_samples=60, centers=[[3, 3]], cluster_std=1.60,
                           random_state=RANDOM_STATE)
    X = np.vstack([dense, sparse])
    truth = np.r_[np.zeros(200, dtype=int), np.ones(60, dtype=int)]

    outcomes = {}
    for eps in (0.30, 0.80, 1.50, 2.50):
        db = DBSCAN(eps=eps, min_samples=5).fit(X)
        outcomes[eps] = (len(set(db.labels_) - {-1}),
                         int((db.labels_ == -1).sum()),
                         adjusted_rand_score(truth, db.labels_))

    km = KMeans(2, n_init=10, random_state=RANDOM_STATE).fit(X)
    ari_km = adjusted_rand_score(truth, km.labels_)

    # Small eps: the ENTIRE sparse blob is discarded as noise, leaving 1 cluster.
    assert outcomes[0.30][0] == 1 and outcomes[0.30][1] == 60
    # Large eps: they MERGE into one cluster and the partition is destroyed.
    assert outcomes[1.50][0] == 1 and round(outcomes[1.50][2], 4) == 0.0178
    assert outcomes[2.50][0] == 1 and round(outcomes[2.50][2], 4) == 0.0000
    # No eps tried recovers TWO clusters with little noise.
    assert not any(c == 2 and n < 10 for c, n, _ in outcomes.values()), \
        "no single eps separates them cleanly"
    assert round(ari_km, 4) == 0.8335, round(ari_km, 4)

    print("    a dense blob (sd 0.20, n=200) and a sparse one (sd 1.60, n=60),")
    print("    centres only 3 units apart:")
    print(f"    {'eps':>6} {'clusters':>9} {'noise':>7} {'ARI':>8}  outcome")
    labels = {0.30: "sparse blob DISCARDED as noise",
              0.80: "sparse blob fragmented",
              1.50: "the two MERGED",
              2.50: "the two MERGED"}
    for eps, (clusters, noise, ari) in outcomes.items():
        print(f"    {eps:6.2f} {clusters:9d} {noise:7d} {ari:8.4f}  {labels[eps]}")
    print(f"    K-Means (k=2) on the same data: ARI {ari_km:.4f}")
    print("       NO SINGLE eps recovers both: too small and the sparse cluster")
    print("       becomes 60 noise points, too large and the two merge. That is")
    print("       DBSCAN's real weakness, and OPTICS is the fix.")
    print("       Note the ARI of 1.0000 at eps=0.30 -- that is a METRIC")
    print("       ARTIFACT: all 60 sparse points got the single label -1, which")
    print("       ARI scores as a consistent group. A cluster of noise is not a")
    print("       cluster, and this is why you look at the counts as well.")
    print("       K-Means wins here because both blobs ARE convex. Neither")
    print("       algorithm is better in general -- that is the answer to give")


def linkage_on_iris():
    """unit-5.md 5.7: Ward agrees best with the truth, single scores best."""
    _, data = iris_frame()
    Z = StandardScaler().fit_transform(data.data)
    y = data.target

    rows = []
    for link in ("ward", "complete", "average", "single"):
        labels = AgglomerativeClustering(3, linkage=link).fit_predict(Z)
        rows.append((link, adjusted_rand_score(y, labels),
                     silhouette_score(Z, labels)))

    by_link = {name: (ari, sil) for name, ari, sil in rows}
    assert round(by_link["ward"][0], 4) == 0.6153
    assert round(by_link["single"][1], 4) == 0.5046
    assert by_link["ward"][0] == max(a for _, a, _ in rows), "Ward: best ARI"
    assert by_link["single"][1] == max(s for _, _, s in rows), \
        "single: best silhouette"
    assert by_link["ward"][1] < by_link["single"][1]

    print(f"    {'linkage':10} {'ARI vs species':>15} {'silhouette':>12}")
    for link, ari, sil in rows:
        print(f"    {link:10} {ari:15.4f} {sil:12.4f}")
    print("       WARD has the best agreement with the truth and the WORST")
    print("       silhouette; single linkage is the reverse. The same lesson as")
    print("       experiment 10: an internal metric rewards geometric tidiness,")
    print("       and tidiness is not correctness. Ward is the sensible default")


def main():
    print("Experiment 12 -- DBSCAN and density-based clustering")
    dbscan_beats_kmeans_on_non_convex_clusters()
    no_k_can_save_kmeans_here()
    core_border_and_noise()
    choosing_eps_with_a_k_distance_plot()
    print("  the weakness:")
    dbscan_struggles_with_varying_density()
    print("  hierarchical linkage, for comparison:")
    linkage_on_iris()


if __name__ == "__main__":
    main()
