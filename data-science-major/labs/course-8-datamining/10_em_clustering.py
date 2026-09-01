"""Experiment 10 — EM clustering, compared with K-Means.

WEKA: Cluster tab -> EM, with numClusters = -1 to let cross-validation choose k.

The point of the experiment is SOFT assignment: EM gives each point a
probability of membership in every cluster, where K-Means gives a hard label.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler


def soft_versus_hard():
    """Two overlapping Gaussians: the boundary points are the interesting ones."""
    rng = np.random.default_rng(7)
    X = np.vstack([rng.normal(0.0, 1.0, (200, 1)),
                   rng.normal(3.0, 1.0, (200, 1))])

    km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)
    em = GaussianMixture(n_components=2, random_state=0).fit(X)

    probs = em.predict_proba(X)
    confidence = probs.max(axis=1)

    # K-Means labels are 0/1 with no notion of confidence.
    assert set(np.unique(km.labels_)) == {0, 1}
    assert probs.shape == (400, 2)
    assert np.allclose(probs.sum(axis=1), 1.0), "each row is a distribution"

    uncertain = int((confidence < 0.8).sum())
    assert uncertain > 0, "overlapping Gaussians MUST produce uncertain points"

    boundary = X[confidence.argmin()][0]
    assert 0.5 < boundary < 2.5, f"the least certain point sits between the means: {boundary}"

    print(f"  soft assignment: {uncertain} of 400 points have max probability "
          f"below 0.8")
    print(f"       least certain point x={boundary:.3f}, probabilities "
          f"{np.round(probs[confidence.argmin()], 3).tolist()}")
    print(f"       K-Means would give that point a confident 0 or 1 and tell")
    print(f"       you nothing about the doubt")


def em_finds_elliptical_clusters():
    """K-Means assumes spherical clusters; EM does not -- but EM is ALSO
    initialisation-sensitive, and this example shows how to handle that.

    Two long, thin, parallel ellipses. K-Means splits along the high-variance
    x direction and cuts BOTH ellipses in half, scoring near chance. EM can
    recover them, but its default k-means initialisation reaches a bad local
    optimum on most seeds. The fix is the same as K-Means's: run several
    initialisations and KEEP THE BEST OBJECTIVE -- here the log likelihood.
    """
    rng = np.random.default_rng(0)
    a = rng.multivariate_normal([0, 0], [[9.0, 0.0], [0.0, 0.15]], 300)
    b = rng.multivariate_normal([0, 3], [[9.0, 0.0], [0.0, 0.15]], 300)
    X = np.vstack([a, b])
    truth = np.r_[np.zeros(300), np.ones(300)]

    def accuracy(labels):
        agree = (labels == truth).mean()
        return max(agree, 1 - agree)            # cluster labels are arbitrary

    km_acc = accuracy(KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(X))
    assert km_acc < 0.60, f"K-Means should be near chance here, got {km_acc}"

    # EM's DEFAULT initialisation is k-means, so it inherits exactly the blind
    # spot we just demonstrated -- and lands in the same bad optimum on every
    # seed. That is worth seeing before fixing it.
    default = [GaussianMixture(n_components=2, covariance_type="full",
                               random_state=s, n_init=1).fit(X) for s in range(4)]
    assert len({round(g.score(X), 4) for g in default}) == 1, \
        "k-means initialisation gives EM the same (bad) answer every time"
    assert accuracy(default[0].predict(X)) < 0.60

    # Initialising from random data points instead lets EM escape it.
    runs = []
    for seed in range(8):
        g = GaussianMixture(n_components=2, covariance_type="full",
                            init_params="random_from_data",
                            random_state=seed, n_init=1).fit(X)
        runs.append((g.score(X), accuracy(g.predict(X))))

    logliks = [r[0] for r in runs]
    assert max(logliks) - min(logliks) > 0.1, \
        "EM must reach genuinely different local optima across seeds"

    # The decisive point: the run with the BEST log likelihood is also the
    # accurate one. Selecting by the objective finds the right answer without
    # ever consulting the labels -- which is what makes it usable in practice.
    best_loglik, best_acc = max(runs, key=lambda r: r[0])
    worst_loglik, worst_acc = min(runs, key=lambda r: r[0])
    assert best_acc > 0.95, f"the best-likelihood run should be accurate, got {best_acc}"
    assert worst_acc < 0.60, f"the worst should not be, got {worst_acc}"
    assert best_acc > km_acc

    print(f"\n  elliptical clusters: K-Means {km_acc:.4f} (near chance --")
    print(f"       it splits along x and cuts BOTH ellipses)")
    print(f"       EM with its DEFAULT k-means init: {accuracy(default[0].predict(X)):.4f} "
          f"on every seed -- it inherits the same blind spot")
    print(f"       EM across 8 seeds: log likelihood {min(logliks):.4f} to "
          f"{max(logliks):.4f}")
    print(f"       best-likelihood run  {best_loglik:.4f} -> accuracy {best_acc:.4f}")
    print(f"       worst-likelihood run {worst_loglik:.4f} -> accuracy {worst_acc:.4f}")
    print(f"       selecting by the OBJECTIVE finds the right clustering without")
    print(f"       ever looking at the labels -- so n_init matters for EM too")


def choose_k_by_bic():
    """WEKA's numClusters = -1 uses cross-validation; the usual Python
    equivalent is BIC, which penalises parameters."""
    X, _ = load_iris(return_X_y=True)
    Xs = StandardScaler().fit_transform(X)

    print("\n      k       BIC       AIC   loglik")
    scores = {}
    for k in range(1, 7):
        g = GaussianMixture(n_components=k, covariance_type="full",
                            random_state=0, n_init=3).fit(Xs)
        scores[k] = g.bic(Xs)
        print(f"      {k}  {g.bic(Xs):9.2f} {g.aic(Xs):9.2f}  {g.score(Xs):7.4f}")

    best = min(scores, key=scores.get)
    assert 1 <= best <= 6
    assert scores[best] == min(scores.values())

    print(f"       BIC is LOWEST at k={best}")
    print(f"       (lower BIC is better -- the opposite of a log likelihood,")
    print(f"        which always improves with more components)")

    # Log likelihood alone would always choose the largest k -- that is why a
    # penalty term is needed at all.
    logliks = [GaussianMixture(n_components=k, covariance_type="full",
                               random_state=0, n_init=3).fit(Xs).score(Xs)
               for k in range(1, 7)]
    assert logliks == sorted(logliks), "log likelihood never falls as k rises"


def kmeans_is_a_special_case():
    """K-Means is EM with spherical equal-variance Gaussians and hard assignment."""
    rng = np.random.default_rng(3)
    X = np.vstack([rng.normal([0, 0], 0.6, (150, 2)),
                   rng.normal([4, 4], 0.6, (150, 2))])

    km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)
    em = GaussianMixture(n_components=2, covariance_type="spherical",
                         random_state=0, n_init=5).fit(X)

    a = np.sort(km.cluster_centers_, axis=0)
    b = np.sort(em.means_, axis=0)
    assert np.allclose(a, b, atol=0.15), f"\n{a}\n{b}"

    print(f"\n  on well-separated spherical data the two agree to within 0.15:")
    print(f"       K-Means centres {np.round(a, 3).tolist()}")
    print(f"       EM       means  {np.round(b, 3).tolist()}")


def main():
    print("Experiment 10 -- EM clustering")
    soft_versus_hard()
    em_finds_elliptical_clusters()
    choose_k_by_bic()
    kmeans_is_a_special_case()
    print("\n  EM behaviour verified")


if __name__ == "__main__":
    main()
