"""Practical 14 — Dummy variables, permutation and random sampling."""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from fixtures import students


def one_hot_and_the_trap():
    s = pd.Series(["DS", "Stats", "Maths", "DS"])

    d = pd.get_dummies(s, dtype=int)
    assert list(d.columns) == ["DS", "Maths", "Stats"]
    assert (d.sum(axis=1) == 1).all(), "every row sums to 1 -- THE COLLINEARITY"

    # DS is an exact linear function of the other two: the singularity itself.
    assert (d.DS == 1 - d.Maths - d.Stats).all()

    dropped = pd.get_dummies(s, drop_first=True, dtype=int)
    assert list(dropped.columns) == ["Maths", "Stats"], "k-1 columns"
    assert dropped.iloc[0].tolist() == [0, 0], "DS is the all-zeros REFERENCE"
    assert not (dropped.sum(axis=1) == 1).all(), "no longer collinear"

    prefixed = pd.get_dummies(s, prefix="dept", dtype=int)
    assert list(prefixed.columns)[0] == "dept_DS"

    with_na = pd.get_dummies(pd.Series(["DS", None]), dummy_na=True, dtype=int)
    assert with_na.shape[1] == 2, "dummy_na adds a column for the missing value"

    print("  k dummies sum to 1 in every row -- perfectly collinear, XtX singular")
    print("       drop_first=True -> k-1, with the dropped level as the reference")
    print("       LINEAR models: drop. TREES: keep all k, or you hide a category")


def multi_label():
    skills = pd.Series(["python,sql", "sql,r", "python"])
    d = skills.str.get_dummies(sep=",")
    assert sorted(d.columns) == ["python", "r", "sql"]
    assert d.loc[0].sum() == 2, "one row, TWO skills"
    print("  str.get_dummies(sep=',') turns 'python,sql' into indicator columns")


def ordinal_versus_nominal():
    # An ORDERED category: integers preserve real information.
    size = pd.Series(["S", "L", "M"]).map({"S": 1, "M": 2, "L": 3})
    assert size.tolist() == [1, 3, 2]

    # An UNORDERED one: integer encoding INVENTS an ordering.
    colour = pd.Series(["red", "green", "blue"]).map({"red": 1, "green": 2, "blue": 3})
    assert colour.iloc[1] == (colour.iloc[0] + colour.iloc[2]) / 2, \
        "this says green is the AVERAGE of red and blue -- nonsense a distance " \
        "model will act on"

    print("  integer-encode ORDERED categories only: 'green' is not the mean of")
    print("       'red' and 'blue', but k-NN and K-Means would believe it is")


def sampling_and_reproducibility():
    df = students()

    a = df.sample(n=3, random_state=42)
    b = df.sample(n=3, random_state=42)
    assert a.equals(b), "the same seed gives the same rows"

    assert len(df.sample(frac=0.4, random_state=0)) == 2
    shuffled = df.sample(frac=1, random_state=0)
    assert len(shuffled) == len(df) and set(shuffled.roll) == set(df.roll)
    assert shuffled.roll.tolist() != df.roll.tolist(), "a genuine shuffle"

    boot = df.sample(n=5, replace=True, random_state=1)
    assert len(boot) == 5
    assert boot.roll.duplicated().any(), "with replacement, rows CAN repeat"

    rng = np.random.default_rng(0)
    order = rng.permutation(len(df))
    assert sorted(order.tolist()) == list(range(len(df)))
    assert len(df.take(order)) == len(df)

    print("  random_state makes sampling reproducible -- without it, an accuracy")
    print("       you report cannot be checked, by you or by anyone else")


def bootstrap_out_of_bag():
    """Where the .632 in Course 8's .632 bootstrap comes from."""
    n = 10_000
    rng = np.random.default_rng(0)
    drawn = set(rng.integers(0, n, n).tolist())
    oob = 1 - len(drawn) / n

    assert abs(oob - 1 / np.e) < 0.01, f"{oob:.4f} vs 1/e = {1/np.e:.4f}"

    print(f"  bootstrap: {oob:.1%} of rows are never drawn, matching 1/e = "
          f"{1/np.e:.1%}")
    print(f"       so ~63.2% appear -- the '.632' bootstrap, and how bagging works")


def stratification():
    """Plain sampling can miss a small class entirely."""
    big = pd.DataFrame({"dept": ["DS"] * 8 + ["Stats"] * 2, "m": range(10)})

    # Unstratified: at least one seed produces a sample with NO Stats at all.
    missed = [s for s in range(30)
              if "Stats" not in set(big.sample(frac=0.5, random_state=s).dept)]
    assert missed, "an unstratified sample CAN lose the minority class"

    # Stratified with Pandas. NOTE: Pandas 3 EXCLUDES the grouping column from
    # each group, so the columns must be named explicitly to keep 'dept'.
    strat = (big.groupby("dept", group_keys=False)[big.columns.tolist()]
                .apply(lambda g: g.sample(frac=0.5, random_state=0)))
    assert strat.dept.value_counts().to_dict() == {"DS": 4, "Stats": 1}

    naive = big.groupby("dept", group_keys=False).apply(
        lambda g: g.sample(frac=0.5, random_state=0))
    assert "dept" not in naive.columns, \
        "Pandas 3: groupby().apply() drops the grouping column"

    # scikit-learn is clearer for a train/test split
    train, test = train_test_split(big, test_size=0.5, random_state=0,
                                   stratify=big.dept)
    assert train.dept.value_counts().to_dict() == {"DS": 4, "Stats": 1}

    print(f"  unstratified 50% samples lost 'Stats' entirely on "
          f"{len(missed)} of 30 seeds")
    print(f"       stratified always gives DS 4, Stats 1")
    print(f"       Pandas 3 note: groupby().apply() DROPS the grouping column --")
    print(f"       name the columns, or use train_test_split(stratify=...)")


def main():
    print("Practical 14 -- Dummy variables and sampling")
    one_hot_and_the_trap()
    multi_label()
    ordinal_versus_nominal()
    sampling_and_reproducibility()
    bootstrap_out_of_bag()
    stratification()


if __name__ == "__main__":
    main()
