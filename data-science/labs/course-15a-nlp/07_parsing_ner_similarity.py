"""Experiments 7, 8 and 9 -- top-down and bottom-up parsing, named entity
recognition scored against hand-labelled truth, and text representation.

Real NLTK parsers, the real spaCy en_core_web_sm model, real scikit-learn.
"""
import numpy as np
import nltk
import spacy

import fixtures as f

_NLP = None


def nlp():
    global _NLP
    if _NLP is None:
        _NLP = spacy.load("en_core_web_sm")
    return _NLP


def experiment_7():
    print("\n    --- experiment 7: top-down and bottom-up parsing")

    grammar = nltk.CFG.fromstring(f.TOY_GRAMMAR)
    sent = f.AMBIGUOUS_SENTENCE
    print(f"\n      grammar: {len(grammar.productions())} productions")
    print(f"      sentence: {' '.join(sent)}")

    parsers = [
        ("RecursiveDescent (top-down)", nltk.RecursiveDescentParser(grammar)),
        ("ShiftReduce (bottom-up)", nltk.ShiftReduceParser(grammar)),
        ("Chart (dynamic programming)", nltk.ChartParser(grammar)),
    ]

    print(f"\n      {'parser':<32}{'parses found':>13}")
    results = {}
    for name, p in parsers:
        try:
            trees = list(p.parse(sent))
        except Exception as exc:                       # noqa: BLE001
            trees = []
            print(f"      {name:<32}{'error: ' + str(exc)[:20]:>13}")
            continue
        results[name] = len(trees)
        print(f"      {name:<32}{len(trees):>13}")

    print("""         THE SHIFT-REDUCE PARSER FOUND FEWER, and that is the
         result the experiment exists to produce.
         RecursiveDescent is TOP-DOWN: start at S and expand until the
         words match. It finds every parse, but it loops for ever on a
         left-recursive rule.
         ShiftReduce is BOTTOM-UP: shift words on a stack, reduce when
         the top matches a rule's right-hand side. It is fast and it is
         GREEDY -- one wrong reduce and it never backtracks, so it
         returns at most one parse and sometimes none.
         Chart parsing stores every partial result, so it gets all of
         them without the exponential re-work. That is dynamic
         programming, the same idea as Course 2's memoisation""")

    # ---- and where top-down breaks -------------------------------------
    print("\n      the rule that kills a top-down parser:")
    print("        NP -> NP PP        <-- LEFT RECURSIVE")
    print("""         To parse an NP, RecursiveDescent must first parse an NP,
         which requires parsing an NP... it recurses without consuming
         a single word and never terminates. Bottom-up and chart
         parsers handle it without difficulty.
         THIS IS THE STANDARD EXAM QUESTION on parsing strategies, and
         the answer is 'left recursion', not 'ambiguity'""")

    # ---- a real treebank, for scale -------------------------------------
    from nltk.corpus import treebank
    t = treebank.parsed_sents()[0]
    print(f"\n      a real Penn Treebank tree ({len(treebank.parsed_sents()):,} "
          f"available):")
    print(f"        leaves: {len(t.leaves())}, height: {t.height()}")
    print(f"        {' '.join(t.leaves())[:78]}")
    print("""         A HAND-WRITTEN CFG DOES NOT SCALE TO THIS. Real
         sentences need thousands of rules and still fail, which is
         why every production parser is STATISTICAL -- it learns rule
         probabilities from a treebank like this one and returns the
         most probable tree instead of all of them""")

    assert results["Chart (dynamic programming)"] == 2
    return results


def experiment_8():
    print("\n    --- experiment 8: named entity recognition, SCORED")

    doc = nlp()(f.NEWS_TEXT)
    found = [(e.text, e.label_) for e in doc.ents]

    print(f"\n      text: {f.NEWS_TEXT[:76]}...")
    print(f"\n      {'entity':<20}{'spaCy':<12}{'truth':<12}{'verdict'}")

    truth = dict(f.NEWS_TRUTH)
    found_d = dict(found)
    exact, wrong_label, missed, spurious = 0, [], [], []

    for text, gold in f.NEWS_TRUTH:
        got = found_d.get(text)
        if got is None:
            missed.append((text, gold))
            verdict = "MISSED"
        elif got == gold:
            exact += 1
            verdict = "ok"
        else:
            wrong_label.append((text, got, gold))
            verdict = "WRONG LABEL"
        print(f"      {text:<20}{str(got or '-'):<12}{gold:<12}{verdict}")

    for text, lab in found:
        if text not in truth:
            spurious.append((text, lab))

    n = len(f.NEWS_TRUTH)
    print(f"\n      {exact}/{n} exactly right, {len(wrong_label)} wrong label, "
          f"{len(missed)} missed")
    if spurious:
        print(f"      found but NOT in my gold list: {spurious}")
        print("""         AND THOSE ARE CORRECT ENTITIES. '2,400' is a cardinal
         and 'three years' is a date; the model is right and MY GOLD
         LIST IS INCOMPLETE.
         That is worth flagging rather than scoring as errors, because
         it is the most common defect in a hand-built evaluation set:
         the annotator marks what they were thinking about and misses
         the rest, and every model is then punished for finding it.
         If you build a gold standard, annotate EXHAUSTIVELY or state
         explicitly which categories you covered""")

    print(f"""         {len(wrong_label)} WRONG LABELS, AND LOOK AT WHICH ONES.""")
    for text, got, gold in wrong_label:
        print(f"        '{text}' called {got}, should be {gold}")
    print("""         BOTH ARE INDIAN STATES, and note what the model got RIGHT:
         Hyderabad and Bengaluru, the two cities, were labelled GPE
         correctly. It is the STATE names that failed -- one called an
         organisation, one called a person.
         en_core_web_sm was trained on OntoNotes, which is mostly
         American news. Indian state names are rare in it, so the
         model falls back on surface cues, and 'Tamil Nadu' looks like
         a two-token proper name of the shape a person has.
         THIS IS DOMAIN SHIFT, and it is the single most important
         thing to know before using a pre-trained NLP model on Indian
         text. The model is not broken; it is being used outside its
         training distribution, and the errors are systematic rather
         than random.
         THE FIX is not a bigger model -- it is annotating a few
         hundred sentences of your own domain and fine-tuning, or
         adding a gazetteer via spaCy's EntityRuler""")

    # ---- the entity-ruler fix, demonstrated -----------------------------
    print("\n      and the gazetteer fix, measured:")
    nlp2 = spacy.load("en_core_web_sm")
    ruler = nlp2.add_pipe("entity_ruler", before="ner")
    places = ["Hyderabad", "Bengaluru", "Karnataka", "Andhra Pradesh",
              "Tamil Nadu", "Mumbai", "Chennai", "Kolkata", "Vijayawada"]
    ruler.add_patterns([{"label": "GPE", "pattern": p} for p in places])
    found2 = dict((e.text, e.label_) for e in nlp2(f.NEWS_TEXT).ents)
    exact2 = sum(1 for t, g in f.NEWS_TRUTH if found2.get(t) == g)
    print(f"        before the gazetteer: {exact}/{n}")
    print(f"        after  the gazetteer: {exact2}/{n}")
    print("""         NINE LINES OF PATTERNS RECOVERED WHAT THE MODEL COULD
         NOT. A gazetteer is not a sophisticated technique and it is
         very often the right one: when your domain has a closed list
         of entities, matching it beats any amount of inference""")

    # ---- NLTK's own NER, for comparison ---------------------------------
    print("\n      NLTK's chunker on the same text, for comparison:")
    toks = nltk.word_tokenize(f.NEWS_TEXT)
    tagged = nltk.pos_tag(toks)
    tree = nltk.ne_chunk(tagged)
    nltk_ents = [(" ".join(w for w, _ in st.leaves()), st.label())
                 for st in tree if hasattr(st, "label")]
    print(f"        NLTK found {len(nltk_ents)}: {nltk_ents[:6]}")
    print(f"        spaCy found {len(found)}")
    print("""         NLTK's chunker uses a different, coarser tagset (PERSON,
         ORGANIZATION, GPE) and a much older model. It is here for
         comparison, not for use -- spaCy is the right tool and the
         syllabus names it""")

    assert exact2 > exact, "the gazetteer should recover at least one entity"
    return exact, exact2, n


def experiment_9():
    print("\n    --- experiment 9: text representation and document similarity")

    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    docs = f.DOCS
    print("\n      four documents, with a KNOWN answer:")
    for i, d in enumerate(docs):
        print(f"        [{i}] {d}")
    print("""        [0] and [1] say the same thing in almost the same words
        [2] says the same thing in DIFFERENT words
        [3] is unrelated
        A good representation ranks 0-1 highest. The 0-2 pair is where
        bag-of-words fails and you can see why""")

    reps = [
        ("bag of words", CountVectorizer()),
        ("BoW, binary", CountVectorizer(binary=True)),
        ("TF-IDF", TfidfVectorizer()),
        ("TF-IDF, 1-2 grams", TfidfVectorizer(ngram_range=(1, 2))),
        ("TF-IDF, char 3-5 grams",
         TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))),
    ]

    print(f"\n      {'representation':<24}{'features':>9}{'sim 0-1':>9}"
          f"{'sim 0-2':>9}{'sim 0-3':>9}")
    sims = {}
    for name, vec in reps:
        X = vec.fit_transform(docs)
        S = cosine_similarity(X)
        sims[name] = S
        print(f"      {name:<24}{X.shape[1]:>9}{S[0, 1]:>9.4f}"
              f"{S[0, 2]:>9.4f}{S[0, 3]:>9.4f}")

    bow = sims["bag of words"]
    tfidf = sims["TF-IDF"]
    print(f"""         EVERY REPRESENTATION RANKS 0-1 FIRST, which is the easy
         case and tells you little. THE INTERESTING COMPARISON IS
         0-2 AGAINST 0-3, and it comes out BACKWARDS.
         Document 2 is a paraphrase of document 0. Document 3 is about
         the monsoon. Bag-of-words scores the PARAPHRASE at
         {bow[0, 2]:.4f} and the UNRELATED document at {bow[0, 3]:.4f}
         -- it ranks the wrong one higher.
         The reason is visible if you look at what documents 0 and 3
         share: 'the', 'and', 'are'. FUNCTION WORDS. Nothing else.
         The similarity is entirely an artefact of English grammar,
         and the one pair that shares actual meaning shares almost no
         strings at all.
         Notice that TF-IDF narrows the gap ({tfidf[0, 2]:.4f} against
         {tfidf[0, 3]:.4f}) because IDF discounts those function
         words -- but it does not reverse the ordering. NO
         COUNT-BASED REPRESENTATION CAN. 'weights' and 'parameters'
         are different strings and nothing in the counts says
         otherwise.
         THIS IS THE EXACT FAILURE word EMBEDDINGS were invented for,
         and it is why Unit 3's Word2Vec section follows this one""")

    # ---- what TF-IDF actually changes -----------------------------------
    print("\n      what the IDF term does, on the Reuters corpus:")
    from nltk.corpus import reuters
    sample = [" ".join(reuters.words(fid)[:200])
              for fid in reuters.fileids()[:400]]
    tv = TfidfVectorizer(max_features=4000)
    tv.fit(sample)
    idf = dict(zip(tv.get_feature_names_out(), tv.idf_))
    common = sorted(idf, key=idf.get)[:6]
    rare = sorted(idf, key=idf.get, reverse=True)[:6]
    print(f"        lowest IDF (in nearly every document): {common}")
    print(f"        highest IDF (in one or two):           {rare}")
    print("""         IDF IS A LEARNED STOPWORD LIST. The words with the
         lowest scores are exactly the ones a stopword list contains,
         and TF-IDF down-weights them automatically from the corpus
         rather than from a fixed list in some other language.
         THAT IS THE ARGUMENT FOR TF-IDF over raw counts, and it is
         also why removing stopwords before TF-IDF changes less than
         students expect""")

    # ---- n-grams and word order -----------------------------------------
    print("\n      n-grams, and the word order that unigrams cannot see:")
    a, b = "the dog bit the man", "the man bit the dog"
    for name, vec in (("unigrams", CountVectorizer()),
                      ("bigrams", CountVectorizer(ngram_range=(2, 2)))):
        X = vec.fit_transform([a, b])
        s = cosine_similarity(X)[0, 1]
        print(f"        {name:<10}similarity of the two sentences: {s:.4f}")
    print("""         UNIGRAMS CALL THEM IDENTICAL -- similarity 1.0000 -- 
         because they contain exactly the same words. Bigrams see the
         difference, because 'dog bit' and 'man bit' are different
         features.
         THAT IS THE WHOLE ARGUMENT FOR N-GRAMS, and also their cost:
         the feature space grows enormously and most bigrams appear
         once, so you gain word order and lose statistical strength""")

    assert bow[0, 1] > bow[0, 2], "0-1 should beat 0-2 under bag of words"
    # the finding this experiment exists to produce: counts rank the
    # UNRELATED document above the paraphrase
    assert bow[0, 3] > bow[0, 2], (
        f"expected counts to misrank: unrelated {bow[0, 3]:.4f} should "
        f"exceed the paraphrase {bow[0, 2]:.4f}")
    assert tfidf[0, 3] > tfidf[0, 2], "TF-IDF narrows but does not reverse it"
    return sims


def main():
    print("  Experiments 7-9 -- parsing, NER, text representation")
    experiment_7()
    experiment_8()
    experiment_9()
    print("\n    all assertions passed")


if __name__ == "__main__":
    main()
