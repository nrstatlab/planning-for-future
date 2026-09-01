"""Experiments 3, 4, 5 and 6 -- ambiguity, tokenization, stopwords, and
stemming against lemmatization.

Real NLTK, real spaCy, real corpora throughout.
"""
import nltk
import spacy

import fixtures as f

_NLP = None


def nlp():
    global _NLP
    if _NLP is None:
        _NLP = spacy.load("en_core_web_sm")
    return _NLP


def experiment_3():
    print("\n    --- experiment 3: lexical and structural ambiguity")

    print(f"\n      {'sentence':<40}{'kind'}")
    for sent, kind, _ in f.AMBIGUOUS:
        print(f"      {sent:<40}{kind}")

    print("""         THE TWO KINDS, AND THE DISTINCTION IS EXAMINED:
         LEXICAL ambiguity is one WORD with several senses. The
         sentence has ONE structure and several meanings.
         STRUCTURAL ambiguity is one word sequence with several
         PARSE TREES. The words are unambiguous; the grouping is not""")

    for sent, kind, why in f.AMBIGUOUS:
        print(f"\n      {sent}")
        print(f"        {kind}: {why}")

    # ---- lexical ambiguity, measured through WordNet ---------------------
    from nltk.corpus import wordnet as wn
    print("\n      lexical ambiguity is COUNTABLE -- WordNet senses:")
    print(f"      {'word':<12}{'senses':>8}   first three glosses")
    for word in ("bank", "duck", "run", "set", "telescope", "monsoon"):
        syns = wn.synsets(word)
        gl = "; ".join(s.definition()[:34] for s in syns[:3])
        print(f"      {word:<12}{len(syns):>8}   {gl[:70]}")
    print("""         'SET' HAS MORE SENSES THAN ANY OTHER ENGLISH WORD, and
         WordNet puts a number on it. That number is what word sense
         disambiguation has to choose between, and it is why WSD is
         hard: the classes are many, fine-grained, and unbalanced""")

    n_bank = len(wn.synsets("bank"))
    assert n_bank > 10, f"'bank' should be highly ambiguous, got {n_bank}"

    # ---- structural ambiguity, shown as trees ----------------------------
    print("\n      structural ambiguity, as actual parse trees:")
    grammar = nltk.CFG.fromstring(f.TOY_GRAMMAR)
    parser = nltk.ChartParser(grammar)
    trees = list(parser.parse(f.AMBIGUOUS_SENTENCE))
    print(f"        '{' '.join(f.AMBIGUOUS_SENTENCE)}' has "
          f"{len(trees)} parses")
    for i, t in enumerate(trees):
        print(f"\n        parse {i + 1}:")
        for line in str(t).splitlines():
            print(f"          {line}")
    assert len(trees) == 2, f"expected exactly 2 parses, got {len(trees)}"
    print("""         TWO TREES, BOTH GRAMMATICAL. In one, the PP attaches to
         the VP -- I used the telescope. In the other it attaches to
         the NP -- the man had it. Nothing in the grammar prefers
         either, and nothing in the sentence resolves it.
         THIS IS WHY PARSING IS NOT ENOUGH. A parser gives you the
         possible structures; choosing between them needs world
         knowledge, which is what a statistical parser learns and a
         hand-written CFG cannot have""")
    return len(trees)


def experiment_4():
    print("\n    --- experiment 4: tokenization, NLTK against spaCy")

    hard = ("Dr. Reddy didn't visit the U.S.A. in 2024. He said, \"It's "
            "far!\" -- the trip cost Rs. 1,20,000. Email: a.b@nri.ac.in")

    print(f"\n      the sentence: {hard}")

    nltk_sents = nltk.sent_tokenize(hard)
    spacy_doc = nlp()(hard)
    spacy_sents = [s.text for s in spacy_doc.sents]
    naive_sents = [s for s in hard.split(".") if s.strip()]

    print(f"\n      {'method':<22}{'sentences':>11}")
    print(f"      {'split on ., naive':<22}{len(naive_sents):>11}")
    print(f"      {'NLTK sent_tokenize':<22}{len(nltk_sents):>11}")
    print(f"      {'spaCy':<22}{len(spacy_sents):>11}")
    for i, s in enumerate(nltk_sents):
        print(f"        NLTK  {i + 1}: {s}")
    for i, s in enumerate(spacy_sents):
        print(f"        spaCy {i + 1}: {s}")
    print("""         BOTH TRAINED TOKENISERS BEAT THE NAIVE SPLIT, and they
         do NOT agree with each other. Neither is 'correct' in the
         abstract -- they were trained on different annotations, and
         the abbreviations here (Dr., U.S.A., Rs.) are exactly where
         annotation guidelines differ.
         REPORT WHICH TOKENISER YOU USED. Two papers with different
         tokenisers are not directly comparable, and this is the
         reason""")

    nltk_words = nltk.word_tokenize(hard)
    spacy_words = [t.text for t in spacy_doc]
    naive_words = hard.split()

    print(f"\n      {'method':<22}{'tokens':>8}")
    print(f"      {'split on whitespace':<22}{len(naive_words):>8}")
    print(f"      {'NLTK word_tokenize':<22}{len(nltk_words):>8}")
    print(f"      {'spaCy':<22}{len(spacy_words):>8}")

    print("\n      where they differ, token by token:")
    only_nltk = [t for t in nltk_words if t not in spacy_words]
    only_spacy = [t for t in spacy_words if t not in nltk_words]
    print(f"        NLTK only : {only_nltk}")
    print(f"        spaCy only: {only_spacy}")
    print("""         LOOK AT THE CONTRACTION. NLTK splits "didn't" into
         'did' + "n't"; spaCy also splits it but writes the pieces
         differently, and the quotation marks are treated differently
         again. Neither is wrong. Both are CHOICES, and a downstream
         model trained on one tokenisation degrades on the other""")

    assert len(nltk_sents) < len(naive_sents)
    assert len(spacy_sents) < len(naive_sents)
    return len(nltk_words), len(spacy_words)


def experiment_5():
    print("\n    --- experiment 5: stopwords and what removing them costs")

    from nltk.corpus import stopwords, brown
    sw = set(stopwords.words("english"))
    print(f"\n      NLTK's English stopword list: {len(sw)} words")
    print(f"      a sample: {sorted(sw)[:14]}")

    words = [w.lower() for w in brown.words()[:100000] if w.isalpha()]
    kept = [w for w in words if w not in sw]
    print(f"\n      on 100,000 words of the Brown corpus:")
    print(f"        before {len(words):>8,} tokens")
    print(f"        after  {len(kept):>8,} tokens")
    reduction = 100 * (1 - len(kept) / len(words))
    print(f"        reduction {reduction:>6.1f}%")
    print(f"        distinct types: {len(set(words)):,} -> {len(set(kept)):,}")
    print("""         ROUGHLY HALF THE TOKENS AND ALMOST NONE OF THE TYPES.
         Stopwords are few words repeated constantly, so removing them
         cuts the token count hugely and the vocabulary barely at all.
         For a bag-of-words model that is close to free""")

    print("\n      and now the cases where removing them destroys the meaning:")
    pairs = [
        ("to be or not to be", "the entire phrase is stopwords"),
        ("The film was not good", "'not' is a stopword -- NEGATION IS LOST"),
        ("It is a war of all against all", "only 'war' survives"),
        ("Who is she?", "nothing survives"),
    ]
    print(f"      {'sentence':<32}{'after removal':<22}{'note'}")
    for sent, note in pairs:
        after = " ".join(w for w in f.tokens(sent) if w not in sw)
        print(f"      {sent:<32}{after or '(empty)':<22}{note}")
    print("""         'THE FILM WAS NOT GOOD' BECOMES 'FILM GOOD'. That is the
         single most damaging thing stopword removal does, and it is
         why a sentiment classifier that strips stopwords can be worse
         than one that does not.
         THE RULE: remove stopwords for TOPIC tasks, where you want
         what a document is about. Keep them for tasks where the
         function words carry the meaning -- sentiment, negation,
         question answering, anything syntactic.
         Experiment 10 measures this rather than asserting it""")

    assert reduction > 40, f"expected a large token reduction, got {reduction:.1f}%"
    return reduction


def experiment_6():
    print("\n    --- experiment 6: stemming against lemmatization")

    from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
    porter, snow = PorterStemmer(), SnowballStemmer("english")
    lem = WordNetLemmatizer()

    words = ["running", "runs", "ran", "better", "geese", "studies",
             "studying", "was", "mice", "caring", "university",
             "universal", "organization", "arguing"]

    print(f"\n      {'word':<14}{'porter':<14}{'snowball':<14}"
          f"{'lemma (n)':<14}{'lemma (v)':<12}")
    rows = []
    for w in words:
        p, s = porter.stem(w), snow.stem(w)
        ln, lv = lem.lemmatize(w, "n"), lem.lemmatize(w, "v")
        rows.append((w, p, s, ln, lv))
        print(f"      {w:<14}{p:<14}{s:<14}{ln:<14}{lv:<12}")

    print("""         READ THREE ROWS CLOSELY.
         'ran' -> porter leaves it 'ran'; the lemmatiser WITH THE VERB
         TAG gives 'run'. A stemmer chops suffixes and 'ran' has none.
         'better' -> stemmers give 'better'; the lemmatiser as an
         adjective gives 'good'. That needs WordNet, not string
         surgery.
         'university' and 'universal' -> porter maps BOTH to 'univers'.
         Two unrelated words collapsed into one feature. That is
         OVER-STEMMING, and it is a real precision loss""")

    print("\n      lemmatization without a POS tag is barely lemmatization:")
    print(f"      {'word':<14}{'no tag':<14}{'tagged verb':<14}")
    for w in ("running", "ran", "was", "better", "studies"):
        print(f"      {w:<14}{lem.lemmatize(w):<14}{lem.lemmatize(w, 'v'):<14}")
    print(f"""         THE DEFAULT POS IS NOUN. Every tutorial that calls
         lemmatize(w) without a tag is asking 'what is the singular
         of this noun', which does nothing at all to a verb. This is
         the most common silent mistake in NLP coursework, and the
         column above is what it costs.
         AND LOOK AT 'was' -> '{lem.lemmatize("was")}'. Untagged, the
         lemmatiser stripped what it took for a plural 's' and
         produced a string that is not an English word at all. So the
         usual claim that 'lemmatization always returns a real word'
         is only true when the tag is right -- tagged as a verb it
         gives '{lem.lemmatize("was", "v")}', which is correct""")

    print(f"\n      {'':<14}{'stemming':<34}{'lemmatization'}")
    for label, a, b in [
        ("what it is", "chop affixes by rule", "map to a dictionary form"),
        ("needs", "nothing", "WordNet, and ideally a POS tag"),
        ("speed", "very fast", "slower"),
        ("output", "may not be a word ('univers')",
         "a real word IF the tag is right"),
        ("errors", "over- and under-stemming", "wrong sense without a tag"),
        ("use for", "search, retrieval, recall", "anything a human reads"),
    ]:
        print(f"      {label:<14}{a:<34}{b}")

    assert lem.lemmatize("ran", "v") == "run"
    assert lem.lemmatize("better", "a") == "good"
    assert porter.stem("university") == porter.stem("universal"), \
        "the over-stemming demonstration depends on this collision"
    return rows


def main():
    print("  Experiments 3-6 -- ambiguity, tokenization, stopwords, stemming")
    experiment_3()
    experiment_4()
    experiment_5()
    experiment_6()
    print("\n    all assertions passed")


if __name__ == "__main__":
    main()
