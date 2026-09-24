"""Experiment 3 — Dimensionality reduction with PCA.

Reproduces every figure in unit-2.md section 2.10, including the check that the
correlation-matrix eigenvalues sum to exactly p, and the disagreement between
the Kaiser criterion and the 95%-variance rule.
"""
import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from fixtures import RANDOM_STATE, iris_frame

_, DATA = iris_frame()
X = DATA.data.to_numpy()
y = DATA.target


def explained_variance():
    """The table in unit-2.md 2.10."""
    Z = StandardScaler().fit_transform(X)
    pca = PCA().fit(Z)
    ratio = pca.explained_variance_ratio_
    cumulative = np.cumsum(ratio)

    assert [round(v, 4) for v in ratio] == [0.7296, 0.2285, 0.0367, 0.0052]
    assert round(cumulative[1], 4) == 0.9581, round(cumulative[1], 4)
    assert round(cumulative[-1], 10) == 1.0

    # Eigenvalues of the CORRELATION matrix, which is what Kaiser refers to.
    eig = np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1]
    assert [round(v, 4) for v in eig] == [2.9185, 0.9140, 0.1468, 0.0207]
    assert round(eig.sum(), 10) == 4.0, "eigenvalues sum to p -- a free check"
    assert np.allclose(eig / eig.sum(), ratio, atol=1e-10), \
        "the RATIOS are identical however you compute the eigenvalues"

    print("  component  eigenvalue  explained  cumulative")
    for i, (e, r, c) in enumerate(zip(eig, ratio, cumulative), 1):
        print(f"    PC{i}       {e:9.4f}   {r * 100:7.2f}%   {c * 100:8.2f}%")
    print(f"  eigenvalues sum to {eig.sum():.4f} = p = {X.shape[1]}  <- check")
    print(f"  TWO components carry {cumulative[1] * 100:.2f}% of the variance")


def sklearn_uses_n_minus_one():
    """Why sklearn's explained_variance_ differs slightly, stated precisely."""
    Z = StandardScaler().fit_transform(X)
    pca = PCA().fit(Z)
    eig_corr = np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1]

    assert [round(v, 4) for v in pca.explained_variance_] == \
        [2.9381, 0.9202, 0.1477, 0.0209]
    assert round(pca.explained_variance_.sum(), 4) == 4.0268
    assert round(eig_corr.sum(), 4) == 4.0

    n = len(X)
    assert np.allclose(pca.explained_variance_, eig_corr * n / (n - 1), atol=1e-9), \
        "sklearn divides by n-1; StandardScaler divided by n"

    print(f"  sklearn explained_variance_ : "
          f"{[round(v, 4) for v in pca.explained_variance_]}  sum "
          f"{pca.explained_variance_.sum():.4f}")
    print(f"  correlation eigenvalues     : "
          f"{[round(v, 4) for v in eig_corr]}  sum {eig_corr.sum():.4f}")
    print(f"  the factor is exactly n/(n-1) = {n}/{n - 1} = {n / (n - 1):.6f}")
    print("       the RATIOS are identical, which is why the ratio is what you")
    print("       report and the raw eigenvalue is not")


def how_many_components():
    """Kaiser says 1, the 95% rule says 2. They disagree, and that is normal."""
    eig = np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1]
    cumulative = np.cumsum(eig / eig.sum())

    kaiser = int((eig > 1).sum())
    rule_90 = int(np.searchsorted(cumulative, 0.90) + 1)
    rule_95 = int(np.searchsorted(cumulative, 0.95) + 1)

    assert kaiser == 1, kaiser
    assert rule_90 == 2 and rule_95 == 2

    print(f"  Kaiser (eigenvalue > 1)      -> {kaiser} component")
    print(f"  cumulative variance >= 90%   -> {rule_90} components")
    print(f"  cumulative variance >= 95%   -> {rule_95} components")
    print("       THE RULES DISAGREE, and that is normal -- Kaiser is known to")
    print("       under-select when p is small. k is a hyperparameter: state")
    print("       which rule you used, or validate it downstream")


def pca_is_unsupervised_and_it_shows():
    """PCA maximises variance, not separation. Compare with LDA."""
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

    Z = StandardScaler().fit_transform(X)
    pcs = PCA(n_components=2).fit_transform(Z)
    lds = LinearDiscriminantAnalysis(n_components=2).fit_transform(Z, y)

    # Both give 2-D; judge them by how separable the classes become.
    pca_cv = cross_val_score(LogisticRegression(max_iter=1000), pcs, y, cv=5).mean()
    lda_cv = cross_val_score(LogisticRegression(max_iter=1000), lds, y, cv=5).mean()
    raw_cv = cross_val_score(
        make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        X, y, cv=5).mean()

    assert pcs.shape == lds.shape == (150, 2)
    assert lda_cv >= pca_cv, (lda_cv, pca_cv)

    print(f"  logistic regression, 5-fold CV accuracy on 2 dimensions:")
    print(f"    PCA (unsupervised, maximises VARIANCE)   {pca_cv:.4f}")
    print(f"    LDA (supervised, maximises SEPARATION)   {lda_cv:.4f}")
    print(f"    all 4 original features                  {raw_cv:.4f}")
    print("       PCA never looks at y. When the goal is separating classes,")
    print("       LDA is the supervised alternative -- and here it matches or")
    print("       beats PCA on the same number of dimensions")


def pca_needs_standardising():
    """Without scaling, PCA reports whichever feature has the largest units."""
    # Blow up one feature's units: sepal length in micrometres.
    X_mixed = X.copy()
    X_mixed[:, 0] *= 10000

    raw = PCA().fit(X_mixed)
    scaled = PCA().fit(StandardScaler().fit_transform(X_mixed))

    # Unscaled, PC1 is essentially the inflated column alone.
    loading = abs(raw.components_[0])
    assert loading.argmax() == 0
    assert round(loading[0], 6) == 1.0, round(loading[0], 6)
    assert round(raw.explained_variance_ratio_[0], 6) == 1.0

    assert round(scaled.explained_variance_ratio_[0], 4) == 0.7296, \
        "standardised, the units cancel and the real answer returns"

    print("  sepal length rescaled to micrometres (x10,000):")
    print(f"    UNSCALED PCA: PC1 explains "
          f"{raw.explained_variance_ratio_[0] * 100:.4f}% and its loading on the")
    print(f"      inflated column is {loading[0]:.4f} -- PC1 IS that column")
    print(f"    STANDARDISED: PC1 explains "
          f"{scaled.explained_variance_ratio_[0] * 100:.2f}%, unchanged from before")
    print("       PCA maximises variance and variance has units. Without")
    print("       standardising it reports your choice of measurement scale")


def reconstruction_error():
    """What 'losing 4.19% of the information' actually means."""
    Z = StandardScaler().fit_transform(X)
    for k in (1, 2, 3, 4):
        pca = PCA(n_components=k).fit(Z)
        back = pca.inverse_transform(pca.transform(Z))
        mse = float(((Z - back) ** 2).mean())
        kept = pca.explained_variance_ratio_.sum()
        if k == 2:
            assert round(kept, 4) == 0.9581
            assert round(mse, 4) == 0.0419, round(mse, 4)
        if k == 4:
            assert round(mse, 10) == 0.0, "keeping every component loses nothing"
        print(f"    k={k}: variance kept {kept * 100:6.2f}%   "
              f"reconstruction MSE {mse:.4f}")
    print("       at k=2 the MSE is 0.0419 -- exactly 1 minus the 0.9581 kept.")
    print("       'Losing 4.19% of the variance' is literally the squared error")
    print("       you would make rebuilding the original four columns")


def main():
    print("Experiment 3 -- Principal Component Analysis")
    explained_variance()
    sklearn_uses_n_minus_one()
    how_many_components()
    pca_is_unsupervised_and_it_shows()
    pca_needs_standardising()
    print("  reconstruction error by number of components:")
    reconstruction_error()


if __name__ == "__main__":
    main()
