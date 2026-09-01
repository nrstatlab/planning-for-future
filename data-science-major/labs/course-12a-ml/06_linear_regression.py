"""Experiment 6 — Simple and multiple linear regression.

Refits COURSE 4's worked example with scikit-learn and asserts it reproduces
the hand-computed slope 4.3030, intercept 43.0303 and R^2 0.9958. If the two
courses ever disagree, this test says so.

Then multiple regression, multicollinearity, and the polynomial degree /
conditioning result from unit-3.md section 3.5.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

from fixtures import RANDOM_STATE, STUDY, study_xy


def simple_linear_regression_matches_course_4():
    X, y = study_xy()
    model = LinearRegression().fit(X, y)
    pred = model.predict(X)

    slope = float(model.coef_[0])
    intercept = float(model.intercept_)

    assert round(slope, 4) == 4.3030, slope
    assert round(intercept, 4) == 43.0303, intercept
    assert round(model.score(X, y), 4) == 0.9958
    assert round(float(np.sqrt(mean_squared_error(y, pred))), 4) == 0.8015
    assert round(float(mean_absolute_error(y, pred)), 4) == 0.7394

    # Two checks Course 4 gave, verified rather than asserted in prose.
    assert abs((y - pred).sum()) < 1e-10, "least-squares residuals sum to zero"
    r = float(np.corrcoef(X.ravel(), y)[0, 1])
    assert round(r ** 2, 4) == round(model.score(X, y), 4), "R^2 = r^2"

    print(f"  slope     {slope:.4f}   (Course 4 computed 4.3030)")
    print(f"  intercept {intercept:.4f}  (Course 4 computed 43.0303)")
    print(f"  R^2       {model.score(X, y):.4f}   (Course 4 computed 0.9958)")
    print(f"  RMSE {np.sqrt(mean_squared_error(y, pred)):.4f}   "
          f"MAE {mean_absolute_error(y, pred):.4f}")
    print(f"  residuals sum to {(y - pred).sum():.1e}   r^2 = {r ** 2:.4f} = R^2")
    print("       scikit-learn reproduces Course 4's hand arithmetic exactly")
    return model


def prediction_and_the_extrapolation_trap(model):
    inside = float(model.predict([[7.5]])[0])
    outside = float(model.predict([[50]])[0])

    assert round(inside, 4) == 75.3030, inside
    assert round(outside, 4) == 258.1818, outside
    assert outside > 100, "a percentage score above 100 -- impossible"

    print(f"  x = 7.5 (inside the observed range 2-11) -> {inside:.4f} marks")
    print(f"  x = 50  (far outside it)                 -> {outside:.4f} marks")
    print("       258 marks out of 100. Nothing in the code warns you; the")
    print("       model has no evidence beyond the range it was fitted on")


def multiple_regression_and_multicollinearity():
    """A duplicate-ish predictor destabilises coefficients, not predictions."""
    rng = np.random.default_rng(RANDOM_STATE)
    n = 200
    x1 = rng.normal(0, 1, n)
    x2 = x1 * 0.98 + rng.normal(0, 0.05, n)      # almost a copy of x1
    x3 = rng.normal(0, 1, n)
    y = 3 * x1 + 2 * x3 + rng.normal(0, 0.5, n)

    clean = LinearRegression().fit(np.c_[x1, x3], y)
    collinear = LinearRegression().fit(np.c_[x1, x2, x3], y)

    corr = float(np.corrcoef(x1, x2)[0, 1])
    assert corr > 0.99, corr

    # Predictions barely change; the COEFFICIENTS do.
    r2_clean = clean.score(np.c_[x1, x3], y)
    r2_coll = collinear.score(np.c_[x1, x2, x3], y)
    assert abs(r2_clean - r2_coll) < 0.01, (r2_clean, r2_coll)
    assert abs(collinear.coef_[0] - 3.0) > abs(clean.coef_[0] - 3.0), \
        "the x1 coefficient moved away from its true value of 3"

    # Ridge is the standard remedy.
    ridge = make_pipeline(StandardScaler(), Ridge(alpha=1.0)).fit(
        np.c_[x1, x2, x3], y)

    print(f"  x1 and x2 correlate {corr:.4f}; the truth is y = 3*x1 + 2*x3")
    print(f"    without x2: coefficients {np.round(clean.coef_, 4)}  R^2 {r2_clean:.4f}")
    print(f"    with    x2: coefficients {np.round(collinear.coef_, 4)}  R^2 {r2_coll:.4f}")
    print(f"    ridge      : coefficients {np.round(ridge[-1].coef_, 4)}")
    print("       R^2 barely moved -- PREDICTION is fine. The coefficients split")
    print("       the shared effect arbitrarily between x1 and x2, so they can")
    print("       no longer be interpreted. Multicollinearity breaks explanation,")
    print("       not prediction, and Ridge is the standard remedy")


def r2_never_decreases_but_adjusted_r2_does():
    """Add PURE NOISE as predictors, over many random draws.

    One draw proves nothing here, because adjusted R^2 can rise by chance.
    The claim that is actually true is about the DISTRIBUTION: R^2 rises every
    single time, while adjusted R^2 rises only about as often as it falls and
    has no upward drift. That is what this measures.
    """
    n, trials, extra = 100, 300, 5

    def adjusted(r2, p):
        return 1 - (1 - r2) * (n - 1) / (n - p - 1)

    rose_r2 = rose_adj = 0
    deltas_r2, deltas_adj = [], []
    for seed in range(trials):
        rng = np.random.default_rng(seed)
        x = rng.normal(0, 1, n)
        y = 3 * x + rng.normal(0, 1, n)

        X1 = x.reshape(-1, 1)
        r2_one = LinearRegression().fit(X1, y).score(X1, y)

        Xk = np.c_[x, rng.normal(0, 1, (n, extra))]     # pure noise columns
        r2_many = LinearRegression().fit(Xk, y).score(Xk, y)

        rose_r2 += r2_many > r2_one
        rose_adj += adjusted(r2_many, 1 + extra) > adjusted(r2_one, 1)
        deltas_r2.append(r2_many - r2_one)
        deltas_adj.append(adjusted(r2_many, 1 + extra) - adjusted(r2_one, 1))

    assert rose_r2 == trials, (rose_r2, trials)
    assert rose_adj < trials // 2, rose_adj
    assert np.mean(deltas_r2) > 0.004
    assert abs(np.mean(deltas_adj)) < 0.001, np.mean(deltas_adj)
    assert min(deltas_r2) > 0, "R^2 never fell, not once"

    print(f"  {trials} random datasets, adding {extra} columns of PURE NOISE:")
    print(f"    R^2 rose in          {rose_r2:3d}/{trials}  "
          f"({rose_r2 / trials * 100:5.1f}%)   mean change {np.mean(deltas_r2):+.6f}")
    print(f"    adjusted R^2 rose in {rose_adj:3d}/{trials}  "
          f"({rose_adj / trials * 100:5.1f}%)   mean change {np.mean(deltas_adj):+.6f}")
    print(f"    smallest R^2 change seen: {min(deltas_r2):+.6f}  <- still positive")
    print("       R^2 rose EVERY time, because adding a column can only give")
    print("       least squares more freedom. Adjusted R^2 penalises the extra")
    print("       parameters, rises about as often as it falls, and has no")
    print("       upward drift -- which is why it can compare models of")
    print("       different sizes and R^2 cannot")


def polynomial_degree_and_conditioning():
    """unit-3.md 3.5: degree 9 interpolates 10 points -- if you standardise."""
    X, y = study_xy()

    raw, scaled, conditions = {}, {}, {}
    for d in (1, 2, 3, 5, 9):
        raw[d] = make_pipeline(PolynomialFeatures(d),
                               LinearRegression()).fit(X, y).score(X, y)
        scaled[d] = make_pipeline(StandardScaler(), PolynomialFeatures(d),
                                  LinearRegression()).fit(X, y).score(X, y)
        conditions[d] = float(np.linalg.cond(PolynomialFeatures(d).fit_transform(X)))

    assert round(raw[1], 6) == 0.995812
    assert round(scaled[9], 6) == 1.000000, "10 points, degree 9 -> exact fit"
    assert round(raw[9], 6) == 0.981546, "unscaled, it fails NUMERICALLY"
    assert raw[9] < raw[1], "and ends up worse than a straight line"
    assert conditions[9] > 1e13 and conditions[1] < 1e2

    print(f"    {'degree':>7} {'R2 unscaled':>13} {'R2 scaled':>11} {'condition no.':>15}")
    for d in (1, 2, 3, 5, 9):
        print(f"    {d:>7} {raw[d]:13.6f} {scaled[d]:11.6f} {conditions[d]:15.2e}")
    print("       standardised, degree 9 fits 10 points EXACTLY (R^2 = 1.0) --")
    print("       9 coefficients plus an intercept for 10 points. That is")
    print("       overfitting made visible.")
    print("       UNSTANDARDISED it scores 0.9815, worse than a straight line,")
    print("       because the condition number reaches 2.7e13 and the solve")
    print("       loses its precision. Standardise before PolynomialFeatures")


def ridge_and_lasso():
    """L2 shrinks; L1 shrinks to exactly zero and therefore selects."""
    rng = np.random.default_rng(RANDOM_STATE)
    n, p = 100, 12
    X = rng.normal(0, 1, (n, p))
    true = np.zeros(p)
    true[:3] = [4.0, -3.0, 2.0]                  # only 3 of 12 matter
    y = X @ true + rng.normal(0, 0.5, n)

    ols = LinearRegression().fit(X, y)
    ridge = Ridge(alpha=10.0).fit(X, y)
    lasso = Lasso(alpha=0.3).fit(X, y)

    ols_zero = int(np.sum(np.abs(ols.coef_) < 1e-8))
    ridge_zero = int(np.sum(np.abs(ridge.coef_) < 1e-8))
    lasso_zero = int(np.sum(np.abs(lasso.coef_) < 1e-8))

    assert ols_zero == 0 and ridge_zero == 0
    assert lasso_zero >= 7, lasso_zero
    assert all(abs(lasso.coef_[i]) > 1.0 for i in range(3)), \
        "Lasso kept the three real predictors"

    print(f"  12 predictors, only 3 of which matter:")
    print(f"    OLS   : {ols_zero:2d} coefficients exactly zero")
    print(f"    Ridge : {ridge_zero:2d} coefficients exactly zero  (shrunk, not removed)")
    print(f"    Lasso : {lasso_zero:2d} coefficients exactly zero  <- it SELECTED")
    print(f"    Lasso's first three: {np.round(lasso.coef_[:3], 4)}  (true 4, -3, 2)")
    print("       that is the difference: L2 shrinks toward zero, L1 shrinks TO")
    print("       zero, which makes Lasso an embedded feature-selection method")


def main():
    print("Experiment 6 -- Simple and multiple linear regression")
    model = simple_linear_regression_matches_course_4()
    prediction_and_the_extrapolation_trap(model)
    multiple_regression_and_multicollinearity()
    r2_never_decreases_but_adjusted_r2_does()
    print("  polynomial degree, with and without standardising:")
    polynomial_degree_and_conditioning()
    ridge_and_lasso()


if __name__ == "__main__":
    main()
