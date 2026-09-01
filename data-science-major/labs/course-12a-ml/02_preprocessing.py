"""Experiment 2 — Data pre-processing techniques.

Unit 2 section 2.1 claims the ORDER of these steps matters and that getting it
wrong corrupts your evaluation silently. This script measures that, rather than
asserting it in prose.
"""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import (MinMaxScaler, OneHotEncoder, OrdinalEncoder,
                                   RobustScaler, StandardScaler)

from fixtures import RANDOM_STATE, churn


def scaling_compared():
    """Standard, min-max and robust, on data with one deliberate outlier."""
    x = np.array([10.0, 12.0, 11.0, 13.0, 12.0, 11.0, 250.0]).reshape(-1, 1)

    std = StandardScaler().fit_transform(x).ravel()
    mm = MinMaxScaler().fit_transform(x).ravel()
    rob = RobustScaler().fit_transform(x).ravel()

    assert round(std.mean(), 10) == 0.0
    assert round(std.std(), 10) == 1.0
    assert round(mm.min(), 10) == 0.0 and round(mm.max(), 10) == 1.0

    # The outlier crushes min-max: the six normal points land in a tiny band.
    normal_spread_mm = mm[:6].max() - mm[:6].min()
    normal_spread_rob = rob[:6].max() - rob[:6].min()
    # min-max: the six normal points span 3 of a total range of 240 -> 0.0125.
    # robust: they span 3 divided by the IQR of 1.5 -> 2.0. A factor of 160.
    assert round(normal_spread_mm, 4) == 0.0125, round(normal_spread_mm, 4)
    assert round(normal_spread_rob, 4) == 2.0, round(normal_spread_rob, 4)
    assert round(normal_spread_rob / normal_spread_mm, 6) == 160.0

    print("  x = [10, 12, 11, 13, 12, 11, 250]   (one outlier)")
    print(f"    {'standardised':16s} {np.round(std, 3)}")
    print(f"    {'min-max':16s} {np.round(mm, 4)}")
    print(f"    {'robust':16s} {np.round(rob, 3)}")
    print(f"  spread of the six NORMAL points after scaling:")
    print(f"    min-max {normal_spread_mm:.4f}   robust {normal_spread_rob:.4f}")
    print(f"    robust keeps them {normal_spread_rob / normal_spread_mm:.0f}x further apart")
    print("       min-max squeezed six distinct values into a 0.0125-wide band,")
    print("       because the outlier owns the whole range. Robust scaling uses")
    print("       the median and IQR, so the outlier does not set the scale")


def encoding_categoricals():
    """One-hot for nominal, ordinal for ordinal -- and why swapping them hurts."""
    colours = pd.DataFrame({"colour": ["Red", "Green", "Blue", "Red"]})
    sizes = pd.DataFrame({"size": ["S", "M", "L", "M"]})

    onehot = OneHotEncoder(sparse_output=False).fit_transform(colours)
    assert onehot.shape == (4, 3), onehot.shape
    assert onehot.sum(axis=1).tolist() == [1.0, 1.0, 1.0, 1.0], "exactly one 1 per row"

    ordinal = OrdinalEncoder(categories=[["S", "M", "L"]]).fit_transform(sizes)
    assert ordinal.ravel().tolist() == [0.0, 1.0, 2.0, 1.0]

    # The mistake: label-encoding a NOMINAL feature invents distances.
    bad = OrdinalEncoder().fit_transform(colours).ravel()
    order = dict(zip(colours["colour"], bad))
    d_red_green = abs(order["Red"] - order["Green"])
    d_red_blue = abs(order["Red"] - order["Blue"])
    assert d_red_green != d_red_blue, "the encoding has invented a distance"

    print(f"  nominal 'colour' one-hot -> shape {onehot.shape}, one 1 per row")
    print(f"  ordinal 'size' S<M<L     -> {ordinal.ravel().tolist()}  (order kept)")
    print(f"  colour LABEL-encoded     -> {bad.tolist()}")
    print(f"    distance Red-Green {d_red_green:.0f}, Red-Blue {d_red_blue:.0f}")
    print("       the encoder just told every distance-based model that Red is")
    print("       nearer one colour than another. That is not a fact about")
    print("       colours; it is a fact about alphabetical order")


def the_dummy_variable_trap():
    """k one-hot columns are perfectly collinear. Drop one for linear models."""
    colours = pd.DataFrame({"colour": ["Red", "Green", "Blue", "Red", "Green"]})

    full = OneHotEncoder(sparse_output=False).fit_transform(colours)
    dropped = OneHotEncoder(sparse_output=False, drop="first").fit_transform(colours)

    assert full.shape == (5, 3) and dropped.shape == (5, 2)
    # Every row of the full encoding sums to 1 -- perfect collinearity with the
    # intercept column a linear model adds.
    assert np.allclose(full.sum(axis=1), 1.0)
    # Dropping one column loses NO information: the dropped category is the
    # one where all remaining columns are zero.
    baseline_rows = (dropped.sum(axis=1) == 0).sum()
    assert baseline_rows == 1, baseline_rows

    print(f"  3 categories -> full one-hot {full.shape}, drop='first' {dropped.shape}")
    print(f"    every full row sums to 1.0 -> collinear with the intercept")
    print(f"    dropped encoding: {baseline_rows} row is all-zero = the baseline category")
    print("       drop one for LINEAR and LOGISTIC regression. Trees and")
    print("       regularised models do not care")


def imputation_shrinks_variance():
    """Mean imputation is not free -- it distorts the distribution."""
    rng = np.random.default_rng(RANDOM_STATE)
    full = rng.normal(50, 10, 200)
    holed = full.copy()
    holed[rng.choice(200, 60, replace=False)] = np.nan

    imputed = SimpleImputer(strategy="mean").fit_transform(
        holed.reshape(-1, 1)).ravel()

    assert np.isnan(holed).sum() == 60
    assert not np.isnan(imputed).any()
    assert round(abs(imputed.mean() - np.nanmean(holed)), 10) == 0.0, \
        "mean imputation preserves the MEAN exactly"
    assert imputed.std() < np.nanstd(holed), "but it SHRINKS the spread"

    print(f"  200 values, 60 made missing (30%):")
    print(f"    observed      mean {np.nanmean(holed):7.4f}  sd {np.nanstd(holed):7.4f}")
    print(f"    mean-imputed  mean {imputed.mean():7.4f}  sd {imputed.std():7.4f}")
    print(f"    sd fell by {(1 - imputed.std() / np.nanstd(holed)) * 100:.1f}%")
    print("       the mean is preserved exactly and the SPREAD is not. Sixty")
    print("       identical values were inserted at the centre. Every")
    print("       correlation involving this column is now weaker than it was")


def a_was_missing_flag_keeps_the_signal():
    """When missingness is informative, the flag is worth more than the value."""
    rng = np.random.default_rng(RANDOM_STATE)
    n = 400
    y = rng.integers(0, 2, n)
    # Income is missing FAR more often for class 1 -- missing-not-at-random.
    income = rng.normal(50000, 12000, n)
    missing = rng.random(n) < np.where(y == 1, 0.6, 0.1)
    income[missing] = np.nan

    imputed = pd.Series(income).fillna(np.nanmean(income)).to_numpy()
    flag = missing.astype(int)

    Xa = imputed.reshape(-1, 1)
    Xb = np.c_[imputed, flag]
    cv_a = cross_val_score(LogisticRegression(), Xa, y, cv=5).mean()
    cv_b = cross_val_score(LogisticRegression(), Xb, y, cv=5).mean()

    assert cv_b > cv_a + 0.10, (cv_a, cv_b)

    print(f"  income missing 60% of the time for class 1, 10% for class 0:")
    print(f"    imputed value only        CV accuracy {cv_a:.4f}")
    print(f"    imputed value + was_missing flag       {cv_b:.4f}")
    print(f"    the flag alone is worth {cv_b - cv_a:+.4f}")
    print("       WHY a value is missing can matter more than what it was.")
    print("       Imputing erases that; one extra column keeps it")


def scaling_before_splitting_leaks():
    """The rule from unit-2.md 2.1, measured on the churn data."""
    df = churn()
    X = df[["tenure_months", "support_calls", "irrelevant"]].to_numpy()
    y = df["churned"].to_numpy()

    # WRONG: scale the whole dataset, then split.
    X_all_scaled = StandardScaler().fit_transform(X)
    Xtr_w, Xte_w, ytr_w, yte_w = train_test_split(
        X_all_scaled, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y)
    leaked = LogisticRegression(random_state=RANDOM_STATE).fit(
        Xtr_w, ytr_w).score(Xte_w, yte_w)

    # RIGHT: split first, and let a Pipeline fit the scaler on train only.
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y)
    clean = make_pipeline(
        StandardScaler(),
        LogisticRegression(random_state=RANDOM_STATE)).fit(Xtr, ytr).score(Xte, yte)

    # The scaler's own parameters differ, which is the mechanism of the leak.
    mean_all = StandardScaler().fit(X).mean_
    mean_train = StandardScaler().fit(Xtr).mean_
    assert not np.allclose(mean_all, mean_train), \
        "the two scalers learned DIFFERENT means -- that difference is the leak"

    print(f"  scale-then-split (leaky) test accuracy : {leaked:.4f}")
    print(f"  split-then-scale (Pipeline)            : {clean:.4f}")
    print(f"  scaler mean fitted on ALL data   : {np.round(mean_all, 4)}")
    print(f"  scaler mean fitted on TRAIN only : {np.round(mean_train, 4)}")
    print("       on this data the two scores happen to be close -- the point is")
    print("       NOT that leakage always inflates the number, but that the")
    print("       leaky score is not an estimate of anything, because the")
    print("       transformer saw the test rows. Use a Pipeline and the question")
    print("       cannot arise")


def main():
    print("Experiment 2 -- Data pre-processing techniques")
    scaling_compared()
    encoding_categoricals()
    the_dummy_variable_trap()
    imputation_shrinks_variance()
    a_was_missing_flag_keeps_the_signal()
    scaling_before_splitting_leaks()


if __name__ == "__main__":
    main()
