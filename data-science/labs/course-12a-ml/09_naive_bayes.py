"""Experiment 9 — Naive Bayes classification.

Two things unit-4.md section 4.3 claims and this script proves:

  * a single zero probability destroys the whole posterior, because the
    likelihood is a PRODUCT -- and Laplace smoothing fixes it
  * the independence assumption is measurably FALSE on real data, and Naive
    Bayes classifies well anyway
"""
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB

from fixtures import RANDOM_STATE, iris_frame

_, DATA = iris_frame()
X, Y = DATA.data.to_numpy(), DATA.target


def bayes_by_hand():
    """The posterior computed from counts, exactly as Course 8 did."""
    # 14 days: 9 Play=Yes, 5 Play=No. Predict for (Sunny, Cool, High, Strong).
    prior = {"Yes": 9 / 14, "No": 5 / 14}
    likelihood = {
        "Yes": {"Sunny": 2 / 9, "Cool": 3 / 9, "High": 3 / 9, "Strong": 3 / 9},
        "No":  {"Sunny": 3 / 5, "Cool": 1 / 5, "High": 4 / 5, "Strong": 3 / 5},
    }

    posterior = {}
    for label in ("Yes", "No"):
        product = prior[label]
        for value in likelihood[label].values():
            product *= value
        posterior[label] = product

    assert round(posterior["Yes"], 6) == 0.005291, round(posterior["Yes"], 6)
    assert round(posterior["No"], 6) == 0.020571, round(posterior["No"], 6)
    assert posterior["No"] > posterior["Yes"]

    total = sum(posterior.values())
    normalised = {k: v / total for k, v in posterior.items()}
    # 0.020571 / (0.005291 + 0.020571) = 0.020571 / 0.025862 = 0.79541
    assert round(normalised["No"], 4) == 0.7954, round(normalised["No"], 4)
    assert round(sum(normalised.values()), 10) == 1.0

    print(f"  P(Yes) x likelihoods = {posterior['Yes']:.6f}")
    print(f"  P(No)  x likelihoods = {posterior['No']:.6f}   <- larger")
    print(f"  normalised: No {normalised['No'] * 100:.2f}%, "
          f"Yes {normalised['Yes'] * 100:.2f}%")
    print("       these are exactly Course 8's figures. The evidence P(X) is")
    print("       the same for both classes, so it can be dropped for the")
    print("       COMPARISON and restored only to normalise")


def one_zero_destroys_the_posterior():
    """The zero-frequency problem, and why it is fatal rather than merely bad."""
    prior = 9 / 14
    likelihoods = [2 / 9, 3 / 9, 3 / 9, 3 / 9]

    healthy = prior * np.prod(likelihoods)
    with_zero = prior * np.prod(likelihoods[:3] + [0.0])

    assert round(healthy, 6) == 0.005291
    assert with_zero == 0.0, "ONE zero drives the entire product to zero"

    # Laplace smoothing: (count + 1) / (total + number of distinct values).
    smoothed = prior * np.prod(likelihoods[:3] + [(0 + 1) / (9 + 2)])
    assert smoothed > 0.0
    # (9/14)(2/9)(3/9)(3/9)(1/11) = 0.015873 x 0.090909 = 0.001443
    assert round(smoothed, 6) == 0.001443, round(smoothed, 6)

    print(f"  all four features observed      posterior {healthy:.6f}")
    print(f"  ONE feature never seen with Yes posterior {with_zero:.6f}   <- zero")
    print(f"  with Laplace smoothing (+1)     posterior {smoothed:.6f}")
    print("       the likelihood is a PRODUCT, so a single unseen feature value")
    print("       vetoes the class no matter how strongly the other three")
    print("       support it. Laplace smoothing replaces the 0 with 1/(n+k)")


def the_independence_assumption_is_false():
    """Measure the correlation Naive Bayes assumes away."""
    corr = DATA.data.corr().to_numpy()
    off_diagonal = np.abs(corr[np.triu_indices(4, k=1)])

    assert len(off_diagonal) == 6
    assert off_diagonal.max() > 0.96, off_diagonal.max()
    assert (off_diagonal > 0.8).sum() >= 3

    # And yet it classifies well.
    scores = cross_val_score(GaussianNB(), X, Y, cv=5)
    assert round(scores.mean(), 4) == 0.9533, round(scores.mean(), 4)

    print(f"  iris feature correlations (off-diagonal): "
          f"{np.round(np.sort(off_diagonal)[::-1], 4)}")
    print(f"  three pairs correlate above 0.8, one above 0.96 --")
    print(f"  the conditional independence assumption is plainly FALSE")
    print(f"  GaussianNB 5-fold CV accuracy anyway: {scores.mean():.4f}")
    print("       that is the interesting part. Classification needs only the")
    print("       CORRECT CLASS TO SCORE HIGHEST, not the probabilities to be")
    print("       right -- so a badly wrong assumption still ranks correctly")


def gaussian_versus_multinomial():
    """Pick the variant that matches the feature type."""
    xtr, xte, ytr, yte = train_test_split(
        X, Y, test_size=0.3, random_state=RANDOM_STATE, stratify=Y)

    gaussian = GaussianNB().fit(xtr, ytr).score(xte, yte)
    assert round(gaussian, 4) == 0.9111, gaussian

    # MultinomialNB is for COUNTS. Text is its home ground.
    corpus = ["win money now", "cheap pills cheap", "meeting at noon",
              "project deadline tomorrow", "win a free prize now",
              "lunch meeting tomorrow", "free money free money",
              "please review the project"]
    labels = [1, 1, 0, 0, 1, 0, 1, 0]

    vec = CountVectorizer()
    counts = vec.fit_transform(corpus)
    text_model = MultinomialNB().fit(counts, labels)
    predicted = text_model.predict(vec.transform(["free money now",
                                                  "project meeting tomorrow"]))

    assert counts.shape[0] == 8
    assert list(predicted) == [1, 0], list(predicted)
    assert round(text_model.alpha, 4) == 1.0, "alpha=1 IS Laplace smoothing"

    print(f"  GaussianNB on iris (continuous features): {gaussian:.4f}")
    print(f"  MultinomialNB on {counts.shape[0]} short messages, "
          f"{counts.shape[1]} distinct words:")
    print(f"    'free money now'          -> {'SPAM' if predicted[0] else 'ham'}")
    print(f"    'project meeting tomorrow'-> {'SPAM' if predicted[1] else 'ham'}")
    print(f"    scikit-learn's alpha defaults to {text_model.alpha} -- that IS")
    print("       Laplace smoothing, on by default, because a word never seen")
    print("       with a class is otherwise guaranteed in any real vocabulary")


def why_text():
    """Why Naive Bayes owns spam filtering: the shape of the problem."""
    corpus = ["win money now"] * 50 + ["meeting at noon"] * 50
    vec = CountVectorizer()
    counts = vec.fit_transform(corpus)

    n, p = counts.shape
    density = counts.nnz / (n * p)

    assert density < 0.6, density
    assert p < n, "a toy corpus; real vocabularies are far LARGER than n"

    print(f"  a toy corpus: {n} documents, {p} distinct words, "
          f"{density * 100:.0f}% of the matrix non-zero")
    print("       real text has tens of thousands of features and a matrix")
    print("       that is >99% zeros. Naive Bayes is LINEAR in the number of")
    print("       features, trains in one pass, needs little data and updates")
    print("       incrementally as users mark mail -- which is exactly the")
    print("       shape of the spam problem")


def main():
    print("Experiment 9 -- Naive Bayes classification")
    bayes_by_hand()
    one_zero_destroys_the_posterior()
    the_independence_assumption_is_false()
    gaussian_versus_multinomial()
    why_text()


if __name__ == "__main__":
    main()
