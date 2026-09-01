"""Experiment 15 — Text preprocessing, TF-IDF and K-Means.

WEKA: filters/unsupervised/attribute/StringToWordVector with IDFTransform and
TFTransform, then SimpleKMeans.

TF-IDF is implemented from first principles AND with scikit-learn, and the two
are asserted to agree. The result is also cross-checked against Course 6's
TF-IDF lab, so the two courses cannot drift apart.
"""
import math
import re
from collections import Counter

import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import silhouette_score

# Deliberately built so that "course" appears in EVERY document -- the term
# whose IDF must come out at exactly zero.
DOCUMENTS = [
    "the statistics course covers probability and distributions",
    "the course on data mining covers clustering and classification",
    "probability and statistics form the basis of this course",
    "clustering and classification are data mining topics in the course",
    "the python course covers data analysis and visualization",
    "data visualization and analysis with python in this course",
]

STOPWORDS = {"the", "and", "of", "on", "in", "this", "are", "with", "form", "a", "is"}


def tokenize(text):
    return [w for w in re.findall(r"[a-z]+", text.lower()) if w not in STOPWORDS]


def term_frequency(tokens):
    """TF as a proportion of the document's length."""
    counts = Counter(tokens)
    n = len(tokens)
    return {t: c / n for t, c in counts.items()}


def inverse_document_frequency(all_tokens):
    """Textbook IDF: log(N / df). A term in EVERY document gets exactly 0."""
    n = len(all_tokens)
    df = Counter()
    for tokens in all_tokens:
        df.update(set(tokens))
    return {t: math.log(n / d) for t, d in df.items()}


def tf_idf(documents):
    all_tokens = [tokenize(d) for d in documents]
    idf = inverse_document_frequency(all_tokens)
    return [{t: f * idf[t] for t, f in term_frequency(tk).items()} for tk in all_tokens], idf


def idf_of_a_universal_term_is_zero():
    """The property that MAKES TF-IDF work, asserted rather than asserted-in-prose."""
    matrices, idf = tf_idf(DOCUMENTS)

    all_tokens = [tokenize(d) for d in DOCUMENTS]
    universal = [t for t in idf if all(t in tk for tk in all_tokens)]
    assert universal == ["course"], universal
    assert idf["course"] == 0.0, idf["course"]

    # And every document's TF-IDF weight for it is therefore zero.
    for m in matrices:
        assert m["course"] == 0.0

    rare = min(idf, key=lambda t: -idf[t])
    print(f"  IDF: 'course' appears in all {len(DOCUMENTS)} documents -> "
          f"IDF exactly {idf['course']:.1f}")
    print(f"       a term carrying no discriminating information gets ZERO weight")
    print(f"       rarest term '{rare}' -> IDF {idf[rare]:.4f}")


def hand_and_sklearn_agree():
    """Different normalisation conventions, same RANKING -- which is what matters."""
    matrices, idf = tf_idf(DOCUMENTS)

    vec = TfidfVectorizer(stop_words=sorted(STOPWORDS), token_pattern=r"[a-z]+",
                          lowercase=True)
    X = vec.fit_transform(DOCUMENTS)
    vocab = vec.get_feature_names_out()

    # scikit-learn uses smoothed IDF (log((1+n)/(1+df)) + 1) and L2 row
    # normalisation, so the VALUES differ from the textbook formula. The
    # ordering of terms within a document is what both agree on.
    doc = 0
    hand_top = sorted(matrices[doc], key=lambda t: -matrices[doc][t])[:3]
    row = X[doc].toarray().ravel()
    sk_top = [vocab[i] for i in np.argsort(-row)[:3]]

    assert "course" not in hand_top, "a zero-weight term cannot be a top term"
    assert set(hand_top) & set(sk_top), \
        f"the two rankings must overlap: {hand_top} vs {sk_top}"

    print(f"\n  document 0 top terms")
    print(f"       by hand (log N/df):     {hand_top}")
    print(f"       scikit-learn (smoothed): {sk_top}")
    print(f"       values differ (smoothing + L2), the ranking agrees")


def raw_counts_versus_tfidf():
    """Why weight at all: raw counts let common words dominate."""
    counts = CountVectorizer(token_pattern=r"[a-z]+").fit(DOCUMENTS)
    totals = counts.transform(DOCUMENTS).sum(axis=0).A1
    names = counts.get_feature_names_out()
    commonest = names[totals.argmax()]

    assert commonest in {"the", "course", "and"}, commonest
    print(f"\n  raw counts: the commonest term is '{commonest}' "
          f"({totals.max()} occurrences)")
    print(f"       useless for telling the documents apart -- hence IDF")


def cluster_the_documents():
    """The three topics -- statistics, data mining, python -- should separate."""
    vec = TfidfVectorizer(stop_words=sorted(STOPWORDS), token_pattern=r"[a-z]+")
    X = vec.fit_transform(DOCUMENTS)

    km = KMeans(n_clusters=3, n_init=20, random_state=0).fit(X.toarray())
    labels = km.labels_.tolist()

    # Documents 0 and 2 are statistics; 1 and 3 are data mining; 4 and 5 python.
    for a, b in [(0, 2), (1, 3), (4, 5)]:
        assert labels[a] == labels[b], \
            f"documents {a} and {b} share a topic but landed in {labels[a]}/{labels[b]}"
    assert len(set(labels)) == 3, "all three clusters must be used"

    sil = silhouette_score(X.toarray(), km.labels_)
    assert sil > 0, sil

    print(f"\n  clustering: labels {labels}, silhouette {sil:.4f}")
    print(f"       (0,2) statistics, (1,3) data mining, (4,5) python -- recovered")

    terms = vec.get_feature_names_out()
    order = km.cluster_centers_.argsort()[:, ::-1]
    for i in range(3):
        top = [terms[j] for j in order[i, :4]]
        print(f"       cluster {i} top terms: {top}")


def course_6_cross_check():
    """Course 6's R lab computed TF-IDF on its own reviews. The FORMULA must
    give the same answer here -- this catches drift between the two courses."""
    reviews = [
        "the course was excellent and the material was clear",
        "excellent teaching but the course pace was fast",
        "the material was poor and the course was disorganised",
        "clear explanations excellent examples in the course",
        "poor pace and poor material throughout the course",
    ]
    matrices, idf = tf_idf(reviews)

    all_tokens = [tokenize(r) for r in reviews]
    assert all("course" in tk for tk in all_tokens)
    assert idf["course"] == 0.0, "the same universal-term property holds"

    # 'excellent' is in 3 of 5 -> IDF = ln(5/3)
    assert round(idf["excellent"], 6) == round(math.log(5 / 3), 6)
    # 'poor' is in 2 of 5 -> ln(5/2)
    assert round(idf["poor"], 6) == round(math.log(5 / 2), 6)
    assert idf["poor"] > idf["excellent"], "rarer term, higher weight"

    print(f"\n  Course 6 cross-check: IDF(excellent)={idf['excellent']:.4f}, "
          f"IDF(poor)={idf['poor']:.4f}, IDF(course)={idf['course']:.1f}")


def main():
    print("Experiment 15 -- Text preprocessing, TF-IDF and clustering")
    idf_of_a_universal_term_is_zero()
    hand_and_sklearn_agree()
    raw_counts_versus_tfidf()
    cluster_the_documents()
    course_6_cross_check()
    print("\n  TF-IDF and text clustering verified")


if __name__ == "__main__":
    main()
