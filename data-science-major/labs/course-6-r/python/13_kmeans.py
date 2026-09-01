"""Experiment 13 (Python equivalent) -- K-Means clustering.

R version: ../13_kmeans.R  (kmeans(scale(df), centers = 3, nstart = 25))

Includes the scaling demonstration from Unit 4: the same data clustered with
and without scale(), to show that forgetting it changes the answer.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

RNG = np.random.default_rng(42)

# Customers: annual income (rupees) and age. Deliberately different scales.
income = np.concatenate([RNG.normal(3_00_000, 40_000, 20),
                         RNG.normal(9_00_000, 60_000, 20),
                         RNG.normal(15_00_000, 80_000, 20)])
age = np.concatenate([RNG.normal(28, 4, 20), RNG.normal(45, 5, 20),
                      RNG.normal(38, 6, 20)])
X = np.column_stack([income, age])


def fit(data, k=3):
    km = KMeans(n_clusters=k, n_init=25, random_state=42)
    labels = km.fit_predict(data)
    return km, labels


if __name__ == "__main__":
    print("K-MEANS                        R: kmeans(scale(df), 3, nstart = 25)")
    print(f"  {X.shape[0]} customers, 2 features")
    print(f"  income range {income.min():,.0f} to {income.max():,.0f}")
    print(f"  age    range {age.min():.0f} to {age.max():.0f}")

    print("\nWITHOUT scaling")
    km_raw, lab_raw = fit(X)
    print(f"  silhouette = {silhouette_score(X, lab_raw):.4f}")
    for c in range(3):
        m = X[lab_raw == c]
        print(f"    cluster {c}: n={len(m):2d}  mean income={m[:,0].mean():>10,.0f}"
              f"  mean age={m[:,1].mean():5.1f}")

    print("\nWITH scaling                   R: scale() before kmeans()")
    Xs = StandardScaler().fit_transform(X)
    km_s, lab_s = fit(Xs)
    print(f"  silhouette = {silhouette_score(Xs, lab_s):.4f}")
    for c in range(3):
        m = X[lab_s == c]
        print(f"    cluster {c}: n={len(m):2d}  mean income={m[:,0].mean():>10,.0f}"
              f"  mean age={m[:,1].mean():5.1f}")

    print("\nELBOW METHOD                   R: sapply(1:10, ...$tot.withinss)")
    for k in range(1, 8):
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(Xs)
        bar = "#" * int(km.inertia_ / 6)
        print(f"    k={k}  WSS={km.inertia_:7.2f}  {bar}")

    agree = (lab_raw == lab_s).mean()
    best_agree = max(agree, 1 - agree)
    print(f"\n  Unscaled and scaled clusterings agree on {best_agree:.0%} of points"
          if best_agree < 1 else "\n  Both clusterings agree here")
    print("  With this data the income separation is so wide that both find it,")
    print("  but the unscaled version is driven by income ALONE -- age contributes")
    print("  essentially nothing, because a 20-year age gap is 20 units against an")
    print("  income gap of 600,000. Scaling is what lets age matter at all.")

    var_ratio = income.var() / age.var()
    print(f"\n  variance ratio income:age = {var_ratio:,.0f} : 1")
    assert var_ratio > 1000, "the scale problem must be real for the point to stand"
    print("  that ratio is why scale() is mandatory, not optional ✓")
