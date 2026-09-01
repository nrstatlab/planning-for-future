"""Experiment 11 — k-Nearest Neighbour classification.

unit-4.md section 4.4 makes two claims that look contradictory until you read
them carefully, and both are measured here:

  * scaling can be the difference between 0.5500 and 0.9750
  * on iris it barely matters, and here it slightly HURT

The rule is about differing units, not ritual.
"""
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from fixtures import RANDOM_STATE, iris_frame

_, DATA = iris_frame()
X, Y = DATA.data.to_numpy(), DATA.target
XTR, XTE, YTR, YTE = train_test_split(
    X, Y, test_size=0.3, random_state=RANDOM_STATE, stratify=Y)


def scaling_when_units_differ():
    """The case the rule exists for: age in years, income in rupees."""
    rng = np.random.default_rng(0)
    n = 400
    age = rng.uniform(20, 60, n)
    income = rng.uniform(200000, 2000000, n)
    y = (age > 40).astype(int)              # the truth depends on AGE ALONE
    Xd = np.c_[age, income]

    xtr, xte, ytr, yte = train_test_split(
        Xd, y, test_size=0.3, random_state=RANDOM_STATE, stratify=y)

    unscaled = KNeighborsClassifier(5).fit(xtr, ytr).score(xte, yte)
    scaled = make_pipeline(StandardScaler(),
                           KNeighborsClassifier(5)).fit(xtr, ytr).score(xte, yte)

    ratio = Xd[:, 1].std() / Xd[:, 0].std()

    assert round(unscaled, 4) == 0.5500, unscaled
    assert round(scaled, 4) == 0.9750, scaled
    assert ratio > 40000, ratio
    assert scaled - unscaled > 0.40

    print(f"  standard deviations: age {Xd[:, 0].std():.2f} years, "
          f"income {Xd[:, 1].std():,.0f} rupees  ->  ratio {ratio:,.0f}x")
    print(f"    UNSCALED k-NN (k=5): {unscaled:.4f}   <- barely better than a coin")
    print(f"    SCALED   k-NN (k=5): {scaled:.4f}")
    print("       Euclidean distance is essentially income alone, and income is")
    print("       IRRELEVANT to the true rule. The classifier is not weak; it")
    print("       is being asked the wrong question")


def scaling_when_units_do_not_differ():
    """Iris, where all four features are centimetres. The honest nuance."""
    spreads = X.std(axis=0)
    ratio = spreads.max() / spreads.min()

    unscaled = KNeighborsClassifier(5).fit(XTR, YTR).score(XTE, YTE)
    scaled = make_pipeline(StandardScaler(),
                           KNeighborsClassifier(5)).fit(XTR, YTR).score(XTE, YTE)

    assert round(ratio, 2) == 4.05, round(ratio, 2)
    assert round(unscaled, 4) == 0.9778, unscaled
    assert round(scaled, 4) == 0.9111, scaled
    assert unscaled > scaled, "scaling made it WORSE here"

    print(f"  iris feature sds (all cm): {np.round(spreads, 3)}  "
          f"ratio {ratio:.2f}x")
    print(f"    UNSCALED k-NN (k=5): {unscaled:.4f}")
    print(f"    SCALED   k-NN (k=5): {scaled:.4f}   <- slightly WORSE")
    print("       a 4x spread is not an imbalance worth correcting, and on a")
    print("       45-row test set a 3-point difference is noise. SCALE WHEN")
    print("       UNITS DIFFER -- iris is the case where they do not")


def choosing_k():
    """Small k = high variance; large k = high bias; k=n = the majority class."""
    rows = []
    for k in (1, 3, 5, 11, 25, 51, len(YTR)):
        model = make_pipeline(StandardScaler(), KNeighborsClassifier(k))
        model.fit(XTR, YTR)
        train = model.score(XTR, YTR)
        test = model.score(XTE, YTE)
        cv = cross_val_score(
            make_pipeline(StandardScaler(), KNeighborsClassifier(k)),
            X, Y, cv=5).mean()
        rows.append((k, train, test, cv))

    by_k = {k: (tr, te, cv) for k, tr, te, cv in rows}

    n_train = len(YTR)
    assert by_k[1][0] == 1.0, "k=1 always gets its own training points right"
    # k = n_train votes over EVERY training point, so it returns one fixed
    # class -- 1/3 on three balanced species, on both train and test.
    assert round(by_k[n_train][0], 4) == 0.3333, by_k[n_train]
    assert round(by_k[n_train][1], 4) == 0.3333, by_k[n_train]
    # Its CV score is higher (0.6667) only because each CV fold trains on 120
    # rows, so k=105 is NOT all of them there. Worth noticing, not hiding.
    assert round(by_k[n_train][2], 4) == 0.6667, by_k[n_train]
    assert by_k[5][2] > by_k[n_train][2]
    assert by_k[51][1] < by_k[11][1], "large k over-smooths"

    print(f"    {'k':>5} {'train':>8} {'test':>8} {'5-fold CV':>10}")
    for k, tr, te, cv in rows:
        note = ""
        if k == 1:
            note = "  <- perfect on train, by construction"
        elif k == len(YTR):
            note = "  <- k = n_train: one fixed class"
        print(f"    {k:5d} {tr:8.4f} {te:8.4f} {cv:10.4f}{note}")
    print(f"       at k = n_train ({len(YTR)}) every query sees the same {len(YTR)} votes,")
    print("       so it returns ONE class: 0.3333 on three balanced species.")
    print("       Its CV column reads 0.6667 only because each CV fold trains")
    print("       on 120 rows, so k=105 is not all of them there.")
    print("       k=1 scores 1.0000 on training because every point is its own")
    print("       nearest neighbour -- that is not learning either. k is a")
    print("       HYPERPARAMETER: choose it on validation folds, and use an odd")
    print("       k for binary problems to avoid ties")


def distance_metrics():
    """Euclidean, Manhattan and Chebyshev, on the same split."""
    results = {}
    for metric in ("euclidean", "manhattan", "chebyshev"):
        model = make_pipeline(StandardScaler(),
                              KNeighborsClassifier(5, metric=metric))
        results[metric] = cross_val_score(model, X, Y, cv=5).mean()

    assert all(0.85 < v < 1.0 for v in results.values()), results
    assert max(results.values()) - min(results.values()) < 0.05, \
        "on well-scaled low-dimensional data the metric barely matters"

    print("    metric        5-fold CV")
    for metric, score in results.items():
        print(f"    {metric:12s} {score:10.4f}")
    print("       nearly identical here. The metric matters in HIGH dimensions,")
    print("       and for text -- where cosine distance ignores document length")
    print("       and Euclidean does not")


def lazy_learning_has_a_cost():
    """Training is instant; prediction is O(n) per query."""
    import time

    model = KNeighborsClassifier(5)
    t0 = time.perf_counter()
    model.fit(XTR, YTR)
    fit_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(20):
        model.predict(XTE)
    predict_time = (time.perf_counter() - t0) / 20

    assert fit_time >= 0 and predict_time >= 0
    assert model.n_samples_fit_ == len(XTR), "it stored every training row"

    print(f"    fit stored {model.n_samples_fit_} rows in {fit_time * 1000:.3f} ms")
    print(f"    one predict over {len(XTE)} rows: {predict_time * 1000:.3f} ms")
    print("       a LAZY learner: fitting just stores, and all the work happens")
    print("       at prediction time. That is the opposite of every other model")
    print("       in this course, and it is why k-NN scales badly to large n")


def main():
    print("Experiment 11 -- k-Nearest Neighbour classification")
    print("  scaling, when the units genuinely differ:")
    scaling_when_units_differ()
    print("  scaling, when they do not:")
    scaling_when_units_do_not_differ()
    print("  choosing k:")
    choosing_k()
    print("  distance metrics:")
    distance_metrics()
    print("  the cost of lazy learning:")
    lazy_learning_has_a_cost()


if __name__ == "__main__":
    main()
