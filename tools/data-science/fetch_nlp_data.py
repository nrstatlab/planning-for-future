#!/usr/bin/env python3
"""Fetch the NLTK corpora Course 15 A needs.

NLTK's downloader refuses to fetch through an HTTP proxy by default: it
cannot pin the validated IP, so it declines rather than risk SSRF (CWE-918).
This environment's egress goes through a pre-configured, trusted agent proxy,
so the opt-in below is the correct answer -- and it is an opt-in to a trusted
proxy, NOT a disabling of TLS verification, which nothing here does.

Run once:  python3 tools/fetch_nlp_data.py
"""
import os
import sys

os.environ.setdefault("NLTK_ALLOW_PROXIED_URLOPEN", "1")

PACKAGES = [
    ("punkt",                          "sentence tokenizer (experiments 3, 4)"),
    ("punkt_tab",                      "its table-driven successor"),
    ("stopwords",                      "stopword lists (experiment 5)"),
    ("wordnet",                        "the lemmatizer's dictionary (experiment 6)"),
    ("omw-1.4",                        "WordNet's multilingual links"),
    ("averaged_perceptron_tagger",     "POS tagger"),
    ("averaged_perceptron_tagger_eng", "its English model"),
    ("treebank",                       "parsed sentences (experiment 7)"),
    ("brown",                          "1.16M tagged words (experiments 5, 9)"),
    ("movie_reviews",                  "2,000 labelled reviews (experiment 10)"),
    ("gutenberg",                      "18 literary texts (experiment 11)"),
    ("reuters",                        "10,788 news documents (experiments 8, 9)"),
    ("names",                          "male and female name lists"),
    ("conll2000",                      "chunked text, for shallow parsing"),
    ("universal_tagset",               "the coarse tagset, for comparison"),
    ("maxent_ne_chunker_tab",          "NLTK's own NER, to compare with spaCy"),
    ("words",                          "an English word list, which NER needs"),
]


def main():
    import nltk
    ok, bad = [], []
    for pkg, why in PACKAGES:
        try:
            if nltk.download(pkg, quiet=True):
                ok.append(pkg)
                print(f"  {pkg:34} OK    -- {why}")
            else:
                bad.append(pkg)
                print(f"  {pkg:34} FAILED-- {why}")
        except Exception as exc:                       # pragma: no cover
            bad.append(pkg)
            print(f"  {pkg:34} ERROR -- {type(exc).__name__}")
    print(f"\n{len(ok)} of {len(PACKAGES)} corpora available.")
    if bad:
        print("""
Missing corpora make experiments 3-7 skip rather than fail. If the download
was refused, check that NLTK_ALLOW_PROXIED_URLOPEN=1 is set -- this script
sets it, but a shell that pre-set it to 0 wins.""")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
