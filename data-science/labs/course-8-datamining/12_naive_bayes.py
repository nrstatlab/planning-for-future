"""Experiment 12 — Naive Bayes, and comparison with the decision tree.

Reproduces Unit 4 section 4.12's hand calculation exactly, demonstrates the
zero-frequency problem, fixes it with Laplace smoothing, and runs the PAIRED
t-test that WEKA's Experimenter does.
"""
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.naive_bayes import CategoricalNB, GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedKFold, cross_val_score
from weather import weather_frame


def posteriors(df, query, alpha=0.0, target="Play"):
    """Unnormalised P(X|C)P(C) for each class, with optional Laplace smoothing.

    alpha = 0 is the raw count estimate; alpha = 1 is add-one smoothing, where
    the denominator gains k, the number of DISTINCT VALUES of that attribute --
    which is the step students most often omit.
    """
    n = len(df)
    out = {}
    for cls, sub in df.groupby(target):
        p = len(sub) / n                       # the prior
        for attribute, value in query.items():
            k = df[attribute].nunique()
            p *= (int((sub[attribute] == value).sum()) + alpha) / (len(sub) + alpha * k)
        out[cls] = p
    return out


def normalise(d):
    total = sum(d.values())
    return {k: v / total for k, v in d.items()}


def unit4_hand_calculation():
    df = weather_frame()
    X = {"Outlook": "Sunny", "Temperature": "Cool",
         "Humidity": "High", "Wind": "Strong"}

    post = posteriors(df, X)
    assert round(post["Yes"], 6) == 0.005291, post
    assert round(post["No"], 6) == 0.020571, post

    # The exact fractions the notes show
    assert abs(post["Yes"] - 486 / 91854) < 1e-12
    assert abs(post["No"] - 180 / 8750) < 1e-12

    norm = normalise(post)
    assert round(norm["No"], 4) == 0.7954
    assert round(norm["Yes"], 4) == 0.2046
    assert max(post, key=post.get) == "No"

    print(f"  4.12: P(X|Yes)P(Yes) = {post['Yes']:.6f}, "
          f"P(X|No)P(No) = {post['No']:.6f} -> predict No ({norm['No']:.1%})")


def practice_3():
    """Practice Problem 3: X = (Rain, Mild, Normal, Weak) -> Yes."""
    df = weather_frame()
    X = {"Outlook": "Rain", "Temperature": "Mild",
         "Humidity": "Normal", "Wind": "Weak"}

    raw = normalise(posteriors(df, X))
    assert round(raw["Yes"], 4) == 0.9025 and round(raw["No"], 4) == 0.0975

    smoothed = normalise(posteriors(df, X, alpha=1.0))
    # 0.8546 from exact fractions. The notes show 0.8547 because they multiply
    # the 4-decimal rounded factors, which is what you do by hand -- the two
    # differ in the fourth decimal and agree on everything that matters.
    assert round(smoothed["Yes"], 4) == 0.8546, smoothed
    assert max(smoothed, key=smoothed.get) == "Yes", "the argmax must not change"

    print(f"  Practice 3: P(Yes|X) {raw['Yes']:.4f} raw -> {smoothed['Yes']:.4f} "
          f"smoothed; argmax unchanged")


def zero_frequency():
    """The whole product collapses to zero from ONE unseen value."""
    df = weather_frame()
    X = {"Outlook": "Overcast", "Temperature": "Hot",
         "Humidity": "High", "Wind": "Strong"}

    # No Overcast day has Play = No.
    assert ((df.Outlook == "Overcast") & (df.Play == "No")).sum() == 0

    raw = posteriors(df, X)
    assert raw["No"] == 0.0, "one zero count vetoes the entire class"

    smoothed = posteriors(df, X, alpha=1.0)
    assert smoothed["No"] > 0.0, "Laplace smoothing removes the veto"

    # The smoothed Outlook|No distribution from the notes
    no = df[df.Play == "No"]
    k = df.Outlook.nunique()
    dist = {v: (int((no.Outlook == v).sum()) + 1) / (len(no) + k)
            for v in ["Overcast", "Sunny", "Rain"]}
    assert dist == {"Overcast": 0.125, "Sunny": 0.5, "Rain": 0.375}, dist
    assert abs(sum(dist.values()) - 1.0) < 1e-12, "still a valid distribution"

    print(f"  zero-frequency: P(X|No)P(No) = {raw['No']} raw -> "
          f"{smoothed['No']:.8f} smoothed")
    print(f"       P(Outlook|No) smoothed = {dist}, sums to 1.0")


def log_space_is_necessary():
    """Section 4.12: a product of many small probabilities UNDERFLOWS."""
    probs = np.full(400, 0.1)
    assert np.prod(probs) == 0.0, "400 factors of 0.1 underflow to exactly zero"
    logsum = np.sum(np.log(probs))
    assert np.isfinite(logsum) and logsum < 0
    print(f"  underflow: prod = {np.prod(probs)} but sum of logs = {logsum:.1f} "
          f"-- which is why implementations use logs")


def paired_t_test():
    """What WEKA's Experimenter -> Paired T-Tester does.

    Comparing two accuracy figures from a single split proves nothing. The
    correct method is a paired t-test over the cross-validation folds -- the
    same test as Course 4, Unit 5.
    """
    X, y = load_iris(return_X_y=True)
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    tree = cross_val_score(DecisionTreeClassifier(random_state=0), X, y, cv=cv)
    bayes = cross_val_score(GaussianNB(), X, y, cv=cv)

    t, p = stats.ttest_rel(tree, bayes)

    assert len(tree) == len(bayes) == 10
    assert all(0 <= a <= 1 for a in tree) and all(0 <= a <= 1 for a in bayes)

    verdict = "significantly different" if p < 0.05 else "NOT significantly different"
    print(f"  paired t-test over 10 folds:")
    print(f"       tree  {tree.mean():.4f} +/- {tree.std():.4f}")
    print(f"       bayes {bayes.mean():.4f} +/- {bayes.std():.4f}")
    print(f"       t = {t:.4f}, p = {p:.4f} -> {verdict} at alpha = 0.05")


def sklearn_agrees():
    """CategoricalNB with alpha=1 must reach the same conclusion as the notes."""
    df = weather_frame()
    codes = {c: {v: i for i, v in enumerate(sorted(df[c].unique()))}
             for c in df.columns[:-1]}
    X = np.array([[codes[c][row[c]] for c in df.columns[:-1]]
                  for _, row in df.iterrows()])
    y = (df.Play == "Yes").astype(int).to_numpy()

    clf = CategoricalNB(alpha=1.0).fit(X, y)
    q = np.array([[codes["Outlook"]["Sunny"], codes["Temperature"]["Cool"],
                   codes["Humidity"]["High"], codes["Wind"]["Strong"]]])
    pred = clf.predict(q)[0]
    prob = clf.predict_proba(q)[0]

    assert pred == 0, "smoothed sklearn must also predict No"
    print(f"  sklearn CategoricalNB(alpha=1): predicts "
          f"{'Yes' if pred else 'No'} with P(No) = {prob[0]:.4f}")


def main():
    print("Experiment 12 -- Naive Bayes")
    unit4_hand_calculation()
    practice_3()
    zero_frequency()
    log_space_is_necessary()
    sklearn_agrees()
    paired_t_test()
    print("  all Unit 4 Bayes calculations reproduced")


if __name__ == "__main__":
    main()
