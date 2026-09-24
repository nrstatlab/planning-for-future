"""Practical 10 — Detect, drop, fill and replace missing values."""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from fixtures import students


def detection():
    df = students()
    df.loc[0, "maths"] = np.nan
    df.loc[1, ["maths", "stats"]] = np.nan

    assert df.isna().sum().to_dict()["maths"] == 2
    assert df.isna().sum().sum() == 3
    assert round(float(df.isna().mean()["maths"]), 2) == 0.40, "40% of maths missing"
    assert df.isna().any(axis=1).sum() == 2, "two rows have at least one gap"

    print(f"  isna().mean() gives PROPORTIONS: {df.isna().mean().round(2).to_dict()}")


def nan_never_equals_nan():
    assert (np.nan == np.nan) is False, "IEEE 754"
    df = students()
    df.loc[0, "maths"] = np.nan
    assert len(df[df.maths == np.nan]) == 0, "ALWAYS empty -- never write this"
    assert len(df[df.maths.isna()]) == 1, "isna() is the only way"
    print("  df[df.x == np.nan] is always empty; use .isna()")


def nan_upcasts_integers():
    assert pd.Series([1, 2, 3]).dtype == np.int64
    assert pd.Series([1, 2, np.nan]).dtype == np.float64, "no NaN in int64"
    nullable = pd.Series([1, 2, pd.NA], dtype="Int64")
    assert str(nullable.dtype) == "Int64", "a NULLABLE integer keeps the type"
    assert nullable.isna().sum() == 1
    print("  one NaN upcasts int64 -> float64; dtype='Int64' keeps it an integer")


def dropping_is_aggressive():
    df = students()
    df.loc[0, "maths"] = np.nan
    df.loc[1, "stats"] = np.nan
    df.loc[2, "name"] = None

    assert len(df) == 5
    assert len(df.dropna()) == 2, "one NaN anywhere removes the whole row"
    assert len(df.dropna(subset=["maths"])) == 4, "only maths matters"
    assert len(df.dropna(how="all")) == 5, "no row is entirely empty"
    assert df.dropna(axis=1).shape[1] == 2, "dropping COLUMNS instead"

    print(f"  dropna() keeps {len(df.dropna())} of {len(df)} rows -- check before committing")


def variance_shrinkage():
    """Mean imputation preserves the mean and DESTROYS the spread."""
    rng = np.random.default_rng(42)
    full = rng.normal(50, 10, 1000)

    holed = full.copy()
    holed[rng.choice(1000, 300, replace=False)] = np.nan
    assert np.isnan(holed).sum() == 300

    imputed = SimpleImputer(strategy="mean").fit_transform(
        holed.reshape(-1, 1)).ravel()

    assert abs(np.nanmean(holed) - imputed.mean()) < 1e-9, "the MEAN is preserved"
    assert imputed.std() < np.nanstd(holed), "the SPREAD is not"

    shrink = 1 - imputed.std() / np.nanstd(holed)
    # Filling 30% with a constant removes their contribution to the spread, so
    # the sd falls by roughly 1 - sqrt(0.7) = 16.3%.
    predicted = 1 - np.sqrt(0.7)
    assert abs(shrink - predicted) < 0.03, f"{shrink:.4f} vs predicted {predicted:.4f}"

    print(f"  30% mean-imputed: sd {np.nanstd(holed):.4f} -> {imputed.std():.4f}, "
          f"{shrink:.1%} lost")
    print(f"       predicted 1 - sqrt(0.7) = {predicted:.1%} -- every correlation weakens")


def median_beats_mean_on_skew():
    s = pd.Series([25, 30, np.nan, 35, 40, np.nan, 28, 200])
    known = s.dropna()

    assert known.sum() == 358 and len(known) == 6
    assert round(float(known.mean()), 2) == 59.67
    assert known.median() == 32.5

    assert s.fillna(known.mean()).iloc[2] > s.fillna(known.median()).iloc[2]
    print(f"  with one 200 present: mean {known.mean():.2f}, median "
          f"{known.median():.1f} -- prefer the median")


def replace_sentinels_first():
    """A sentinel left in place corrupts every statistic computed after it."""
    df = pd.DataFrame({"marks": [88, -999, 94, 71, -999, 52]})

    corrupted = df.marks.mean()
    assert corrupted < 0, "the -999s drag the mean below zero"

    df["marks"] = df.marks.replace(-999, np.nan)
    honest = df.marks.mean()
    assert round(float(honest), 2) == 76.25

    print(f"  sentinels: mean is {corrupted:.2f} with -999 present, "
          f"{honest:.2f} after replacing")
    print(f"       convert sentinels BEFORE computing anything")


def imputation_order_matters():
    """Fit on the training split only, or the test set leaks in."""
    train = np.array([[10.0], [12.0], [np.nan], [11.0]])
    test = np.array([[1000.0], [np.nan]])

    correct = SimpleImputer(strategy="mean").fit(train)
    leaky = SimpleImputer(strategy="mean").fit(np.vstack([train, test]))

    assert round(float(correct.statistics_[0]), 4) == 11.0
    assert float(leaky.statistics_[0]) > 200, "the test set's 1000 has leaked in"

    print(f"  leakage: fit on train {correct.statistics_[0]:.2f} vs "
          f"fit on everything {leaky.statistics_[0]:.2f}")


def missingness_is_information():
    df = pd.DataFrame({"income": [30000, np.nan, 52000, np.nan, 61000]})
    df["income_missing"] = df.income.isna().astype(int)
    assert df.income_missing.tolist() == [0, 1, 0, 1, 0]
    print("  add an indicator BEFORE imputing -- a tree often finds it predictive")


def ffill_needs_an_ordering():
    ts = pd.Series([10.0, np.nan, np.nan, 13.0, np.nan],
                   index=pd.date_range("2026-08-26", periods=5))
    assert ts.ffill().tolist() == [10.0, 10.0, 10.0, 13.0, 13.0]
    b = ts.bfill()
    assert b.iloc[:4].tolist() == [10.0, 13.0, 13.0, 13.0]
    assert np.isnan(b.iloc[4]), "bfill cannot fill a TRAILING gap -- nothing follows"
    assert ts.ffill(limit=1).isna().sum() == 1, "at most one consecutive fill"
    assert ts.interpolate().tolist() == [10.0, 11.0, 12.0, 13.0, 13.0]

    print("  ffill carries the last value forward; interpolate fills linearly")
    print("       both are meaningless on UNORDERED rows")


def main():
    print("Practical 10 -- Missing data")
    detection()
    nan_never_equals_nan()
    nan_upcasts_integers()
    dropping_is_aggressive()
    variance_shrinkage()
    median_beats_mean_on_skew()
    replace_sentinels_first()
    imputation_order_matters()
    missingness_is_information()
    ffill_needs_an_ordering()


if __name__ == "__main__":
    main()
