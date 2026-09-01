"""Experiment 2 — Data cleaning and missing values.

WEKA equivalent: filters/unsupervised/attribute/ReplaceMissingValues.

Demonstrates NUMERICALLY the variance shrinkage warned about in Unit 2 section
2.5 -- the reason mean imputation is more dangerous than it looks.
"""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer, KNNImputer


def unit2_worked_example():
    """Section 2.5: ages [25, 30, NULL, 35, 40, NULL, 28]."""
    ages = pd.Series([25, 30, np.nan, 35, 40, np.nan, 28])
    known = ages.dropna()

    assert known.sum() == 158 and len(known) == 5
    assert round(known.mean(), 4) == 31.6
    assert known.median() == 30

    # One outlier moves the mean far more than the median.
    with_outlier = pd.concat([known, pd.Series([200])])
    assert round(with_outlier.mean(), 1) == 59.7
    assert with_outlier.median() == 32.5

    print(f"  2.5: mean {known.mean():.1f}, median {known.median():.0f}; "
          f"add one 200 -> mean {with_outlier.mean():.1f}, "
          f"median {with_outlier.median():.1f}")


def variance_shrinkage():
    """Mean imputation keeps the mean and DESTROYS the spread."""
    rng = np.random.default_rng(42)
    full = rng.normal(50, 10, 1000)

    holed = full.copy()
    holed[rng.choice(1000, 300, replace=False)] = np.nan   # 30% missing

    imputed = SimpleImputer(strategy="mean").fit_transform(holed.reshape(-1, 1)).ravel()

    assert abs(np.nanmean(holed) - imputed.mean()) < 1e-9, "the MEAN is preserved"
    assert imputed.std() < np.nanstd(holed), "but the STANDARD DEVIATION shrinks"

    shrink = 1 - imputed.std() / np.nanstd(holed)
    # Filling 30% of the values with a constant removes their contribution to
    # the spread, so sd falls by roughly 1 - sqrt(0.7) = 16.3%.
    assert 0.10 < shrink < 0.25, shrink

    print(f"  variance shrinkage: sd {np.nanstd(holed):.4f} -> {imputed.std():.4f} "
          f"({shrink:.1%} lost) while the mean is unchanged")
    print(f"       every correlation weakens and every test becomes overconfident")


def imputation_strategies():
    """The methods from Unit 2's table, on data with a deliberate outlier."""
    df = pd.DataFrame({
        "age":    [25, 30, np.nan, 35, 40, np.nan, 28, 200],
        "income": [30000, 45000, 52000, np.nan, 61000, 38000, np.nan, 90000],
        "city":   ["VJA", "GNT", None, "VJA", "VJA", "GNT", None, "HYD"],
    })

    numeric = ["age", "income"]
    mean_i = pd.DataFrame(SimpleImputer(strategy="mean").fit_transform(df[numeric]),
                          columns=numeric)
    med_i = pd.DataFrame(SimpleImputer(strategy="median").fit_transform(df[numeric]),
                         columns=numeric)
    knn_i = pd.DataFrame(KNNImputer(n_neighbors=2).fit_transform(df[numeric]),
                         columns=numeric)
    mode_city = SimpleImputer(strategy="most_frequent").fit_transform(df[["city"]])

    # The 200 drags the mean-imputed value well above the median-imputed one.
    assert mean_i.age[2] > med_i.age[2], "the outlier inflates the mean"
    assert mode_city[2][0] == "VJA", "mode imputation picks the commonest city"
    assert not mean_i.isna().any().any() and not knn_i.isna().any().any()

    print(f"  imputed age: mean {mean_i.age[2]:.2f}, median {med_i.age[2]:.2f}, "
          f"kNN {knn_i.age[2]:.2f}")
    print(f"       the median is unmoved by the 200 -- prefer it on real data")


def missingness_is_information():
    """Section 2.5: add an indicator BEFORE imputing."""
    df = pd.DataFrame({"income": [30000, np.nan, 52000, np.nan, 61000]})
    df["income_missing"] = df.income.isna().astype(int)
    assert df.income_missing.tolist() == [0, 1, 0, 1, 0]
    print("  added an income_missing indicator -- a tree often finds it predictive")


def impute_after_splitting():
    """Fitting the imputer on ALL data leaks test information into training."""
    rng = np.random.default_rng(0)
    train = np.array([10.0, 12.0, np.nan, 11.0])
    test = np.array([1000.0, np.nan])

    correct = SimpleImputer(strategy="mean").fit(train.reshape(-1, 1))
    leaky = SimpleImputer(strategy="mean").fit(
        np.concatenate([train, test]).reshape(-1, 1))

    assert round(float(correct.statistics_[0]), 4) == 11.0
    assert float(leaky.statistics_[0]) > 200, "the test set's 1000 has leaked in"

    print(f"  leakage: fit on train only -> {correct.statistics_[0]:.2f}; "
          f"fit on everything -> {leaky.statistics_[0]:.2f}")


def main():
    print("Experiment 2 -- Missing values")
    unit2_worked_example()
    variance_shrinkage()
    imputation_strategies()
    missingness_is_information()
    impute_after_splitting()
    print("  all Unit 2 missing-data claims verified")


if __name__ == "__main__":
    main()
