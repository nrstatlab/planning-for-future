"""Experiment 4 — Attribute selection and PCA.

WEKA: Select attributes tab (InfoGainAttributeEval + Ranker, WrapperSubsetEval
+ BestFirst) and filters/unsupervised/attribute/PrincipalComponents.
"""
import numpy as np
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier


def filter_ranking():
    """WEKA's InfoGainAttributeEval + Ranker."""
    X, y = load_iris(return_X_y=True)
    names = load_iris().feature_names

    mi = mutual_info_classif(X, y, random_state=0)
    ranked = sorted(zip(names, mi), key=lambda p: -p[1])

    # Petal measurements dominate on iris -- the visual separation of Exp 5.
    top_two = {n for n, _ in ranked[:2]}
    assert top_two == {"petal length (cm)", "petal width (cm)"}, top_two

    print("  info gain ranking (WEKA: InfoGainAttributeEval + Ranker)")
    for n, v in ranked:
        print(f"    {v:.4f}  {n}")


def wrapper_selection():
    """WEKA's WrapperSubsetEval: trains the model on each candidate subset."""
    X, y = load_iris(return_X_y=True)
    rfe = RFE(LogisticRegression(max_iter=1000), n_features_to_select=2).fit(X, y)
    kept = [n for n, k in zip(load_iris().feature_names, rfe.support_) if k]
    assert len(kept) == 2

    full = cross_val_score(DecisionTreeClassifier(random_state=0), X, y, cv=5).mean()
    subset = cross_val_score(DecisionTreeClassifier(random_state=0),
                             X[:, rfe.support_], y, cv=5).mean()

    print(f"  wrapper (RFE) kept: {kept}")
    print(f"       4 attributes {full:.4f} vs 2 attributes {subset:.4f}")
    print(f"       half the features, essentially the same accuracy")


def unit2_eigenvalue_table():
    """Section 2.7's worked example: eigenvalues 4.2, 2.1, 0.9, 0.5, 0.3."""
    lam = np.array([4.2, 2.1, 0.9, 0.5, 0.3])
    total = lam.sum()
    assert round(float(total), 4) == 8.0

    prop = lam / total
    cum = np.cumsum(prop)
    assert [round(float(p) * 100, 2) for p in prop[:3]] == [52.50, 26.25, 11.25]
    assert round(float(cum[2]) * 100, 2) == 90.00, "three components give 90%"
    assert int((lam > 1).sum()) == 2, "Kaiser's criterion keeps two"

    print(f"  2.7: three components retain {cum[2]:.1%}; "
          f"Kaiser (lambda>1) keeps {int((lam > 1).sum())}")


def practice_3_eigenvalues():
    """Practice Problem 3: twelve eigenvalues, 90% at five components."""
    lam = np.array([5.4, 2.8, 1.6, 1.1, 0.8, 0.4, 0.3, 0.2, 0.2, 0.1, 0.1, 0.0])
    assert round(float(lam.sum()), 4) == 13.0
    cum = np.cumsum(lam) / lam.sum()

    k90 = int(np.searchsorted(cum, 0.90 - 1e-9) + 1)
    assert k90 == 5, k90
    assert round(float(cum[4]) * 100, 2) == 90.00
    assert int((lam > 1).sum()) == 4, "Kaiser keeps four, retaining 83.85%"
    assert round(float(cum[3]) * 100, 2) == 83.85

    print(f"  Practice 3: 90% at k={k90}; Kaiser gives k=4 at {cum[3]:.2%}")
    print(f"       the two rules DISAGREE, which is normal")


def pca_needs_standardising():
    """Section 2.7: without standardising, PC1 is just the biggest-variance column."""
    X, _ = load_iris(return_X_y=True)
    X_mixed = X.copy()
    X_mixed[:, 0] *= 10000                     # pretend one column is in rupees

    raw = PCA(n_components=2).fit(X_mixed)
    # PC1 is now dominated by that one column.
    assert abs(raw.components_[0][0]) > 0.99, \
        "unstandardised PCA just picks the largest-variance column"
    assert raw.explained_variance_ratio_[0] > 0.999

    std = PCA(n_components=2).fit(StandardScaler().fit_transform(X_mixed))
    assert abs(std.components_[0][0]) < 0.9, "standardised, PC1 blends the columns"

    print(f"  standardising: raw PC1 loading on the inflated column "
          f"{abs(raw.components_[0][0]):.4f} ({raw.explained_variance_ratio_[0]:.4%} "
          f"of variance)")
    print(f"       standardised: {abs(std.components_[0][0]):.4f} -- a real combination")


def pca_costs_interpretability():
    """Section 2.7: components are combinations, so no component is 'age'."""
    X, y = load_iris(return_X_y=True)
    Xs = StandardScaler().fit_transform(X)
    p = PCA(n_components=2).fit(Xs)

    names = load_iris().feature_names
    for i, comp in enumerate(p.components_, 1):
        terms = " ".join(f"{c:+.3f}*{n.split(' ')[0][:5]}" for c, n in zip(comp, names))
        print(f"    PC{i} = {terms}")

    assert all(abs(c).min() > 0.01 for c in p.components_), \
        "EVERY original attribute contributes to every component"
    assert p.explained_variance_ratio_.sum() > 0.95

    print(f"       {p.explained_variance_ratio_.sum():.2%} of variance in 2 of 4 "
          f"dimensions -- but nothing is 'petal length' any more")


def main():
    print("Experiment 4 -- Feature selection and PCA")
    filter_ranking()
    wrapper_selection()
    unit2_eigenvalue_table()
    practice_3_eigenvalues()
    pca_needs_standardising()
    pca_costs_interpretability()
    print("  all Unit 2 dimensionality claims verified")


if __name__ == "__main__":
    main()
