"""Experiment 8 -- a MapReduce job for inverted index creation.

The inverted index is what a search engine is. Word count changes the VALUE
between map and reduce; the inverted index changes the KEY SPACE -- the map
output key is a word and the value is a document, which is exactly the
transposition a search index needs.
"""
from mapreduce import run
import fixtures as f

INPUT = sorted(f.DOCS.items())


def mapper(doc, text):
    """(doc, text) -> (word, doc) -- emit the document as the VALUE."""
    for pos, word in enumerate(text.split()):
        yield word, (doc, pos)


def reducer(word, postings):
    """(word, [(doc, pos), ...]) -> (word, posting list).

    The posting list is deduplicated by document and carries a frequency,
    which is what turns a boolean index into a ranked one.
    """
    per_doc = {}
    for doc, pos in postings:
        per_doc.setdefault(doc, []).append(pos)
    yield word, {d: len(p) for d, p in sorted(per_doc.items())}


def boolean_and(index, *words):
    """Intersect posting lists -- an AND query."""
    sets = [set(index.get(w, {})) for w in words]
    return sorted(set.intersection(*sets)) if sets else []


def boolean_or(index, *words):
    sets = [set(index.get(w, {})) for w in words]
    return sorted(set.union(*sets)) if sets else []


def main():
    print("  Experiment 8 -- inverted index in MapReduce")

    trace = {}
    index = dict(run(INPUT, mapper, reducer, trace=trace))

    print(f"\n    {len(INPUT)} documents in, {len(index)} index terms out")
    print(f"    map emitted {trace['map_output']} postings")
    assert trace["map_output"] == 48 and len(index) == 26

    print("\n    a slice of the index (term -> {doc: frequency}):")
    for w in ("dog", "quick", "big", "data", "machine"):
        entry = ", ".join(f"{d.replace('.txt', '')}:{c}"
                          for d, c in index[w].items())
        print(f"      {w:<10}{entry}")
    assert index["dog"] == {"doc1.txt": 1, "doc2.txt": 1,
                            "doc3.txt": 1, "doc6.txt": 1}
    assert index["quick"] == {"doc1.txt": 1, "doc3.txt": 2}
    print("""         'quick' appears TWICE in doc3, and the posting records
         that. Frequency is the difference between 'does this word
         occur' and 'how relevant is this document' -- boolean
         retrieval against ranked retrieval, in one number""")

    print("\n    queries answered from the index alone:")
    for q in (("quick", "fox"), ("big", "data"), ("dog", "machine")):
        hits = boolean_and(index, *q)
        pretty = [h.replace(".txt", "") for h in hits]
        print(f"      {' AND '.join(q):<24}-> {pretty if pretty else 'no match'}")
    assert boolean_and(index, "quick", "fox") == ["doc1.txt", "doc3.txt"]
    assert boolean_and(index, "big", "data") == ["doc4.txt", "doc5.txt"]
    assert boolean_and(index, "dog", "machine") == []
    hits_or = boolean_or(index, "dog", "machine")
    print(f"      {'dog OR machine':<24}-> "
          f"{[h.replace('.txt', '') for h in hits_or]}")
    assert len(hits_or) == 5
    print("""         NOT ONE DOCUMENT WAS READ to answer these. That is the
         entire point of an inverted index: query cost depends on the
         number of MATCHES, not on the size of the corpus. Scanning
         6 documents is cheap; scanning 6 billion is not""")

    # ---- the size trade --------------------------------------------------
    corpus_chars = sum(len(t) for _, t in INPUT)
    postings = sum(len(v) for v in index.values())
    print(f"\n    the index is not free:")
    print(f"      corpus       {corpus_chars:>5} characters")
    print(f"      index terms  {len(index):>5}")
    print(f"      postings     {postings:>5}")
    print(f"      ratio        {postings / len(INPUT):>5.1f} postings per document")
    print("""         a full-text index typically runs 20-40% of the corpus
         size, and that is BEFORE positions. Search is a space-for-time
         trade, and 'the index is bigger than I expected' is the normal
         outcome, not a mistake""")

    # ---- why this is a MapReduce job at all ------------------------------
    print("\n    why MapReduce suits this:")
    print("      map    is per-document and EMBARRASSINGLY PARALLEL")
    print("      reduce is per-term, and every posting for a term")
    print("             arrives at the same reducer by construction")
    print("""         the shuffle does the hard part -- gathering every
         mention of a word from every machine in the cluster -- and
         you never wrote a line of network code. That is the whole
         value proposition of the model""")

    print("\n    the skew, measured:")
    sizes = sorted(((w, sum(v.values())) for w, v in index.items()),
                   key=lambda kv: -kv[1])
    print(f"      largest posting list : {sizes[0][0]!r} with {sizes[0][1]}")
    print(f"      singleton terms      : "
          f"{sum(1 for _, n in sizes if n == 1)} of {len(sizes)}")
    assert sizes[0][0] == "the" and sizes[0][1] == 5
    print("""         'the' is the biggest list here and would be the biggest
         on any English corpus. Real engines drop stop words or split
         hot terms across reducers, because one reducer holding 'the'
         is the job's critical path""")

    return index


if __name__ == "__main__":
    main()
