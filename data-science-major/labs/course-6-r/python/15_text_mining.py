"""Experiment 15 (Python equivalent) -- text mining and word frequency.

R version: ../15_text_mining.R  (tm + wordcloud)
No word cloud is drawn here -- the frequencies that WOULD drive one are what
matter, and those are verifiable. The R script draws the cloud.
"""
import math, re
from collections import Counter

STOPWORDS = {
    "the", "is", "at", "which", "on", "a", "an", "and", "or", "but", "in",
    "with", "to", "for", "of", "as", "by", "that", "this", "it", "from",
    "be", "are", "was", "were", "has", "have", "had", "i", "you", "we",
}

REVIEWS = [
    "The data science course is excellent and the teaching is excellent",
    "Excellent course with excellent practical data examples",
    "The practical sessions are useful but the course is fast",
    "Data analysis practical work is the best part of this course",
    "Teaching on this course is good and the data examples are practical",
]
# Note: "course" and "data" deliberately appear in EVERY review, so the TF-IDF
# demonstration below has something real to weight to zero.


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)          # remove punctuation, digits
    tokens = text.split()
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


def stem(word):
    """A crude Porter-style suffix stripper, enough to show the idea."""
    for suffix in ("ing", "edly", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def term_document_matrix(docs):
    tokenised = [preprocess(d) for d in docs]
    vocab = sorted({t for doc in tokenised for t in doc})
    return vocab, [[doc.count(t) for doc in tokenised] for t in vocab]


def tfidf(vocab, tdm, n_docs):
    out = {}
    for term, row in zip(vocab, tdm):
        tf = sum(row)
        df = sum(1 for c in row if c > 0)
        out[term] = tf * math.log(n_docs / df)
    return out


if __name__ == "__main__":
    print("PREPROCESSING                  R: tm_map(corpus, ...)")
    print(f"  original : {REVIEWS[0]}")
    print(f"  cleaned  : {' '.join(preprocess(REVIEWS[0]))}")
    print(f"  stemmed  : {' '.join(stem(t) for t in preprocess(REVIEWS[0]))}")

    all_tokens = [t for d in REVIEWS for t in preprocess(d)]
    freq = Counter(all_tokens)
    print(f"\nWORD FREQUENCY                 R: sort(rowSums(as.matrix(dtm)))")
    print(f"  {len(all_tokens)} tokens after stop-word removal, "
          f"{len(freq)} unique")
    for word, n in freq.most_common(8):
        print(f"    {word:<12} {n}  {'#' * n * 3}")

    vocab, tdm = term_document_matrix(REVIEWS)
    print(f"\nTERM-DOCUMENT MATRIX           {len(vocab)} terms x {len(REVIEWS)} docs")
    print(f"    {'term':<12}" + "".join(f"D{i+1:<3}" for i in range(len(REVIEWS))))
    for term, row in list(zip(vocab, tdm))[:6]:
        print(f"    {term:<12}" + "".join(f"{c:<4}" for c in row))

    scores = tfidf(vocab, tdm, len(REVIEWS))
    print("\nTF-IDF                         TF x log(N / DF)")
    for term, sc in sorted(scores.items(), key=lambda kv: -kv[1])[:6]:
        df = sum(1 for c in tdm[vocab.index(term)] if c > 0)
        print(f"    {term:<12} tf={sum(tdm[vocab.index(term)]):<3} "
              f"df={df:<3} tfidf={sc:.4f}")

    in_all = [t for t in vocab if all(c > 0 for c in tdm[vocab.index(t)])]
    assert in_all, "the demonstration needs at least one ubiquitous term"
    print(f"\n  terms appearing in EVERY document: {in_all}")
    for t in in_all:
        print(f"    '{t}' -> tf-idf = {scores[t]:.4f}  (log(5/5) = 0)")
    print("  A term in every document carries no discriminating information,")
    print("  so TF-IDF weights it to exactly zero. That is the whole point.")

    for t in in_all:
        assert abs(scores[t]) < 1e-12, f"{t} should have zero tf-idf"
    print("\n  ubiquitous terms correctly weighted to zero ✓")
