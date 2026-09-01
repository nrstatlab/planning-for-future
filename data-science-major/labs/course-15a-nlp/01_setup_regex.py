"""Experiments 1 and 2 -- the toolchain inventory, and regular expressions.

Everything here is real NLTK and real spaCy against real corpora. Nothing in
this file is simulated.
"""
import re

import fixtures as f


def experiment_1():
    print("\n    --- experiment 1: what is actually installed")

    import nltk
    import spacy
    import sklearn
    import spacy.util

    print(f"\n      NLTK    {nltk.__version__}")
    print(f"      spaCy   {spacy.__version__}")
    print(f"      sklearn {sklearn.__version__}")

    models = spacy.util.get_installed_models()
    print(f"      spaCy models installed: {models}")
    assert models, "no spaCy model -- run: python -m spacy download en_core_web_sm"

    nlp = spacy.load("en_core_web_sm")
    print(f"\n      en_core_web_sm pipeline: {nlp.pipe_names}")
    print("""         READ THAT PIPELINE. Each name is a component that runs in
         order on every document: the tagger before the parser, the
         parser before the entity recogniser. When spaCy is slow, the
         fix is usually nlp.pipe(..., disable=[...]) -- turn off the
         components you are not using""")

    print("\n      the NLTK corpora this course uses:")
    from nltk.corpus import (brown, treebank, movie_reviews, reuters,
                             gutenberg, stopwords, wordnet)
    rows = [
        ("brown", f"{len(brown.words()):,} words",
         f"{len(brown.categories())} genres"),
        ("treebank", f"{len(treebank.parsed_sents()):,} parsed sentences",
         "hand-annotated syntax"),
        ("movie_reviews", f"{len(movie_reviews.fileids()):,} documents",
         f"{movie_reviews.categories()}"),
        ("reuters", f"{len(reuters.fileids()):,} documents",
         f"{len(reuters.categories())} topics"),
        ("gutenberg", f"{len(gutenberg.fileids())} texts", "literary prose"),
        ("stopwords", f"{len(stopwords.words('english'))} English words",
         f"{len(stopwords.fileids())} languages"),
        ("wordnet", f"{len(list(wordnet.all_synsets())):,} synsets",
         "a lexical database, not a corpus"),
    ]
    print(f"      {'corpus':<16}{'size':<32}{'note'}")
    for name, size, note in rows:
        print(f"      {name:<16}{size:<32}{note}")

    print("""         WORDNET IS NOT A CORPUS and the distinction is examined.
         A corpus is text somebody wrote; WordNet is a hand-built
         network of word SENSES, with synonymy, hypernymy and
         antonymy between them. The lemmatiser in experiment 6 needs
         it precisely because lemmatisation requires knowing that
         'better' is a form of 'good', which no amount of text will
         tell you by itself""")

    assert len(brown.words()) > 1_000_000
    assert len(movie_reviews.fileids()) == 2000
    return len(models)


def score(found, truth, label):
    """Precision, recall and F1 against a hand-labelled list."""
    found_s, truth_s = set(found), set(truth)
    tp = len(found_s & truth_s)
    prec = tp / len(found_s) if found_s else 0.0
    rec = tp / len(truth_s) if truth_s else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    print(f"      {label:<12}{prec:>10.3f}{rec:>9.3f}{f1:>8.3f}"
          f"{len(found_s):>8}{len(truth_s):>8}")
    missed = truth_s - found_s
    spurious = found_s - truth_s
    return prec, rec, f1, missed, spurious


def experiment_2():
    print("\n    --- experiment 2: regular expressions, scored against truth")

    text = f.CONTACT_TEXT

    patterns = {
        "emails": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "hashtags": r"#[A-Za-z][A-Za-z0-9_]*",
        "dates": (r"\d{1,2}/\d{1,2}/\d{4}"
                  r"|\d{4}-\d{2}-\d{2}"
                  r"|(?:January|February|March|April|May|June|July|August"
                  r"|September|October|November|December)\s+\d{1,2},\s+\d{4}"),
        "phones": (r"\+91[\s-]?\d{5}[\s-]?\d{5}"
                   r"|\(\d{3}\)\s?\d{4}\s?\d{4}"
                   r"|\b\d{3}-\d{4}-\d{4}\b"),
    }

    print(f"\n      {'pattern':<12}{'precision':>10}{'recall':>9}{'F1':>8}"
          f"{'found':>8}{'true':>8}")
    results = {}
    for name, pat in patterns.items():
        found = re.findall(pat, text)
        results[name] = score(found, f.CONTACT_TRUTH[name], name)

    print("""         SCORING A REGEX AGAINST HAND-LABELLED TRUTH is the whole
         difference between this and the usual version of this
         experiment. 'It found some emails' is not a result. The text
         contains deliberate near-misses -- 'asha at nrigroup dot ac
         dot in', the handle '@nri_official', 'C#', and a phone number
         too short to be one -- and a pattern that catches those has a
         precision problem you would never have noticed""")

    for name, (p, r, f1, missed, spurious) in results.items():
        if missed or spurious:
            print(f"\n      {name}: missed {sorted(missed)}, "
                  f"spurious {sorted(spurious)}")

    # ---- the trap everyone hits ------------------------------------------
    print("\n      the naive email pattern, and what it costs:")
    naive = r"\w+@\w+"
    naive_found = re.findall(naive, text)
    print(f"        r'\\w+@\\w+'  ->  {naive_found}")
    print("""         IT TRUNCATES. '\\w' does not match '.' or '-', so
         'asha.reddy@nrigroup.ac.in' comes back as 'reddy@nrigroup'.
         The result LOOKS like a list of emails, which is why this
         particular bug survives into production so often""")

    # ---- greedy vs lazy --------------------------------------------------
    print("\n      greedy against lazy, on the same string:")
    html = "<b>bold</b> and <i>italic</i>"
    print(f"        input        {html}")
    print(f"        r'<.*>'      {re.findall(r'<.*>', html)}")
    print(f"        r'<.*?>'     {re.findall(r'<.*?>', html)}")
    print("""         '*' IS GREEDY: it takes as much as it can and gives back
         only what it must, so '<.*>' swallows the whole line. '*?' is
         LAZY and stops at the first '>'. This single character is the
         most common cause of a regex that 'works on one example'""")

    # ---- and the honest limit -------------------------------------------
    print("\n      where regex stops being the right tool:")
    # (text, how many sentences a careful reader counts)
    tricky = [("Dr. Reddy went to Hyderabad. He arrived at 3 p.m. on Monday.",
               2),
              ("The B.Sc. (Hons) course costs Rs. 45,000 per year.", 1)]
    print(f"        {'true':>6}{'naive':>7}   text")
    counts = []
    for t, true_n in tricky:
        naive_n = len([s for s in t.split(".") if s.strip()])
        counts.append((true_n, naive_n))
        print(f"        {true_n:>6}{naive_n:>7}   {t}")
    print("""         SPLITTING ON '.' GIVES THE WRONG ANSWER on both, because
         'Dr.', 'p.m.', 'B.Sc.' and 'Rs.' all contain a full stop that
         does not end a sentence. Two real sentences are reported as
         five, and one is reported as four.
         That is why experiment 4 uses a trained tokeniser instead. A
         regex is right for a pattern you can write down; sentence
         boundaries are not one""")
    assert all(n > t for t, n in counts), "the naive split should over-count"

    for name, (p, r, f1, _, _) in results.items():
        assert f1 > 0.7, f"{name} F1 {f1:.3f} is too low to be useful"
    assert "reddy@nrigroup" in naive_found, "the naive pattern should truncate"
    return results


def main():
    print("  Experiments 1 and 2 -- the toolchain, and regular expressions")
    experiment_1()
    experiment_2()
    print("\n    all assertions passed")


if __name__ == "__main__":
    main()
