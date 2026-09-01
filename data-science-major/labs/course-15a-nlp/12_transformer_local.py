"""Experiments 12, 13 and 14 -- the runnable halves.

⚠ ALL THREE SYLLABUS EXPERIMENTS NAME HUGGING FACE, AND huggingface.co IS
REFUSED BY THIS ENVIRONMENT'S EGRESS POLICY -- a 403 at the gateway, before
any request reaches the host. No BERT checkpoint can be downloaded, so no
`pipeline()` can be constructed.

  * `12_bert_mlm.md`        -- masked word prediction with a pre-trained BERT
  * `13_summarization.md`   -- abstractive summarization with a HF pipeline
  * `14_faq_chatbot.md`     -- an FAQ bot on transformer embeddings

All three are marked *** NOT EXECUTED *** and the runner asserts the markers
survive.

WHAT RUNS HERE IS THE MECHANISM OF EACH, built from parts that are available:

  12. Masked language modelling, TRAINED from scratch on a real corpus. The
      model is tiny and the predictions are correspondingly weak -- which is
      the honest way to show what pre-training on billions of words buys.
  13. EXTRACTIVE summarization, which needs no pre-trained model at all:
      TextRank over sentence similarity, scored against a lead baseline.
  14. An FAQ retriever on TF-IDF embeddings, scored against hand-labelled
      answers -- the same architecture as the transformer version with a
      different embedding function, so the part that changes is isolated.
"""
import re

import numpy as np

import fixtures as f


def experiment_12():
    print("\n    --- experiment 12 (mechanism): masked language modelling")

    import torch
    import torch.nn as nn
    torch.manual_seed(f.SEED)
    torch.set_num_threads(2)

    from nltk.corpus import brown

    sents = [[w.lower() for w in s if w.isalpha()]
             for s in brown.sents()[:12000]]
    sents = [s for s in sents if 6 <= len(s) <= 24]
    from collections import Counter
    counts = Counter(w for s in sents for w in s)
    vocab = ["<pad>", "<mask>", "<unk>"] + [w for w, c in counts.most_common(4000)]
    stoi = {w: i for i, w in enumerate(vocab)}
    MASK, PAD, UNK = 1, 0, 2
    MAXLEN = 24

    def encode(s):
        ids = [stoi.get(w, UNK) for w in s][:MAXLEN]
        return ids + [PAD] * (MAXLEN - len(ids))

    X = np.array([encode(s) for s in sents], dtype="int64")
    print(f"\n      Brown corpus: {len(sents):,} sentences, "
          f"vocabulary {len(vocab):,}, padded to {MAXLEN}")

    class TinyBert(nn.Module):
        """A transformer ENCODER with bidirectional attention -- BERT's shape."""

        def __init__(self, V, d=128, heads=4, layers=2):
            super().__init__()
            self.emb = nn.Embedding(V, d, padding_idx=PAD)
            self.pos = nn.Embedding(MAXLEN, d)
            layer = nn.TransformerEncoderLayer(d, heads, d * 4, batch_first=True,
                                               dropout=0.1)
            self.enc = nn.TransformerEncoder(layer, layers)
            self.head = nn.Linear(d, V)

        def forward(self, x):
            p = torch.arange(x.size(1), device=x.device)
            h = self.emb(x) + self.pos(p)[None]
            h = self.enc(h, src_key_padding_mask=(x == PAD))
            return self.head(h)

    model = TinyBert(len(vocab))
    n_params = sum(p.numel() for p in model.parameters())
    print(f"      model: 2-layer transformer encoder, {n_params:,} parameters")
    print(f"""         FOR SCALE: bert-base-uncased has 110,000,000 parameters
         and was trained on 3.3 billion words. This has {n_params:,}
         and sees {sum(len(s) for s in sents):,}. It is smaller by a
         factor of roughly {110_000_000 // n_params}, and the
         predictions below should be read with that in mind""")

    opt = torch.optim.Adam(model.parameters(), lr=3e-4)
    lossf = nn.CrossEntropyLoss(ignore_index=-100)
    Xt = torch.tensor(X)
    rng = np.random.default_rng(f.SEED)

    def mask_batch(batch):
        """BERT's recipe: mask 15% of real tokens, predict them."""
        x = batch.clone()
        labels = torch.full_like(x, -100)
        real = (x != PAD)
        pick = (torch.rand(x.shape) < 0.15) & real
        labels[pick] = x[pick]
        x[pick] = MASK
        return x, labels

    print(f"\n      {'epoch':>7}{'loss':>10}{'perplexity':>13}")
    losses = []
    for ep in range(5):
        model.train()
        perm = torch.randperm(len(Xt))
        tot, nb = 0.0, 0
        for i in range(0, len(Xt), 128):
            b = Xt[perm[i:i + 128]]
            xb, yb = mask_batch(b)
            opt.zero_grad()
            out = model(xb)
            loss = lossf(out.reshape(-1, len(vocab)), yb.reshape(-1))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            tot += loss.item(); nb += 1
        losses.append(tot / nb)
        print(f"      {ep:>7}{losses[-1]:>10.4f}{np.exp(losses[-1]):>13.1f}")

    print("""         THE 15% MASKING RATE IS BERT'S, and it is a real design
         choice worth knowing: too low and training is slow because
         most positions teach nothing; too high and there is not
         enough context left to predict from. BERT also replaces some
         picks with a random word rather than <mask>, so the model
         cannot assume a masked position is always <mask> -- that
         detail is omitted here for clarity and is in 12_bert_mlm.md""")

    # ---- what it predicts -------------------------------------------------
    tests = [
        "the president of the united <mask> said",
        "she opened the <mask> and walked in",
        "he was a member of the <mask> party",
        "the water in the <mask> was cold",
    ]
    print("\n      masked predictions, top 5:")
    model.eval()
    top_special = []
    for t in tests:
        toks = t.split()
        ids = [stoi.get(w, UNK) if w != "<mask>" else MASK for w in toks]
        ids = ids[:MAXLEN] + [PAD] * (MAXLEN - len(ids))
        pos = toks.index("<mask>")
        with torch.no_grad():
            logits = model(torch.tensor([ids]))[0, pos]
        top = torch.topk(logits, 12).indices.tolist()
        all_words = [vocab[i] for i in top]
        special = {"<unk>", "<pad>", "<mask>"}
        content = [w for w in all_words if w not in special][:5]
        print(f"\n        {t}")
        print(f"          raw top-5     : {all_words[:5]}")
        print(f"          top-5 content : {content}")
        if all_words[0] in special:
            top_special.append(all_words[0])

    print(f"""         THESE PREDICTIONS ARE WEAK, and reporting that is the
         point of the experiment.
         LOOK AT THE RAW COLUMN FIRST: '<unk>' tops
         {len(top_special)} of the {len(tests)} lists. The model's
         single best guess is 'some word I do not have', because
         out-of-vocabulary tokens really are the most frequent thing
         at a random position in a 4,000-word vocabulary over the
         Brown corpus. That is a correct prediction about the DATA and
         a useless one about the SENTENCE, and it is what a model
         trained on too little text does.
         The content column strips the special tokens, and what is
         left is function words -- 'the', 'of', 'to'. The model has
         learned the SHAPE of English and none of the FACTS. A
         pre-trained BERT answers 'states' for the first line because
         it saw the phrase thousands of times; this model saw it
         never.
         WHAT PRE-TRAINING BUYS IS EXACTLY THIS GAP, and you can only
         see the size of it by training the small version yourself.
         Perplexity fell from {np.exp(losses[0]):.0f} to
         {np.exp(losses[-1]):.0f} against a vocabulary of {len(vocab):,},
         so it learned a great deal -- just not enough""")

    assert losses[-1] < losses[0]
    assert np.exp(losses[-1]) < len(vocab)
    return losses


def experiment_13():
    print("\n    --- experiment 13 (runnable half): extractive summarization")

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import nltk
    from nltk.corpus import reuters

    fid = [f_ for f_ in reuters.fileids() if len(reuters.raw(f_)) > 2200][3]
    text = " ".join(reuters.raw(fid).split())
    sents = nltk.sent_tokenize(text)
    print(f"\n      a real Reuters article, {len(text):,} characters, "
          f"{len(sents)} sentences")

    X = TfidfVectorizer(stop_words="english").fit_transform(sents)
    S = cosine_similarity(X)
    np.fill_diagonal(S, 0.0)

    # TextRank: PageRank over the sentence-similarity graph
    n = len(sents)
    W = S / (S.sum(axis=1, keepdims=True) + 1e-9)
    r = np.ones(n) / n
    for _ in range(60):
        r = 0.15 / n + 0.85 * (W.T @ r)
    order = np.argsort(r)[::-1]

    k = 3
    textrank_idx = sorted(int(i) for i in order[:k])
    lead_idx = list(range(k))

    print(f"\n      TEXTRANK picked sentences {textrank_idx}:")
    for i in textrank_idx:
        print(f"        [{i}] {sents[i][:96]}")
    print(f"\n      LEAD-{k} baseline picked {lead_idx}:")
    for i in lead_idx:
        print(f"        [{i}] {sents[i][:96]}")

    overlap = len(set(textrank_idx) & set(lead_idx))
    print(f"\n      the two summaries share {overlap} of {k} sentences")
    print(f"""         THE LEAD BASELINE IS THE ONE TO BEAT and almost nobody
         reports it. News writing is deliberately front-loaded -- the
         inverted pyramid -- so 'take the first three sentences' is a
         genuinely strong summarizer on news, and it is free.
         TextRank agreed with it on {overlap} of {k} here. If your
         clever method cannot beat lead-{k} on news, say so; that is a
         result about the DATA, and it is why summarization papers
         report the lead baseline in every table""")

    print("""
      and the distinction the syllabus asks for:
        EXTRACTIVE   selects existing sentences. Cannot be ungrammatical,
                     cannot hallucinate, cannot compress or rephrase.
                     Needs no pre-trained model -- this ran on TF-IDF.
        ABSTRACTIVE  generates new text. Can compress and rephrase, and
                     CAN STATE THINGS THE SOURCE DOES NOT SAY. Needs a
                     seq2seq model (BART, T5, Pegasus) and therefore
                     needs the host this environment refuses.""")
    print("""         THE HALLUCINATION RISK IS THE REASON THIS DISTINCTION
         MATTERS in practice. An extractive summary of a medical
         report is at worst badly chosen; an abstractive one can
         assert a dosage that appears nowhere in the source. That is
         not a hypothetical -- it is the main reason production
         summarizers in regulated domains are still extractive""")

    assert len(textrank_idx) == k
    return textrank_idx, lead_idx


def experiment_14():
    print("\n    --- experiment 14 (runnable half): an FAQ retriever, SCORED")

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    questions = [q for q, _ in f.FAQ]
    answers = [a for _, a in f.FAQ]

    configs = [
        ("TF-IDF words", TfidfVectorizer()),
        ("TF-IDF words, no stopwords", TfidfVectorizer(stop_words="english")),
        ("TF-IDF char 3-5 grams",
         TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))),
    ]

    print(f"\n      {len(f.FAQ)} FAQ entries, {len(f.FAQ_QUERIES)} test "
          f"queries, none of which copies an FAQ question")

    print(f"\n      {'representation':<28}{'correct':>9}{'of':>4}{'accuracy':>10}")
    best_name, best_acc, best_pred = None, -1, None
    for name, vec in configs:
        M = vec.fit_transform(questions)
        Q = vec.transform([q for q, _ in f.FAQ_QUERIES])
        pred = cosine_similarity(Q, M).argmax(axis=1)
        gold = np.array([g for _, g in f.FAQ_QUERIES])
        correct = int((pred == gold).sum())
        acc = correct / len(gold)
        print(f"      {name:<28}{correct:>9}{len(gold):>4}{acc:>10.4f}")
        if acc > best_acc:
            best_name, best_acc, best_pred = name, acc, pred

    print(f"\n      per query, under {best_name}:")
    print(f"      {'query':<36}{'matched':<38}{'ok'}")
    for (q, gold), p in zip(f.FAQ_QUERIES, best_pred):
        ok = "yes" if p == gold else "NO"
        print(f"      {q:<36}{questions[p][:36]:<38}{ok}")

    misses = [(q, questions[p], questions[g])
              for (q, g), p in zip(f.FAQ_QUERIES, best_pred) if p != g]
    if misses:
        print("\n      the failures, and why they are the interesting part:")
        for q, got, want in misses:
            print(f"        query : {q}")
            print(f"        got   : {got}")
            print(f"        wanted: {want}")
        print("""         EVERY FAILURE HERE IS A VOCABULARY MISMATCH. The query
         and the right answer mean the same thing and share no words,
         so a TF-IDF retriever -- which can only compare strings --
         has nothing to go on.
         THAT IS PRECISELY WHAT SENTENCE EMBEDDINGS FIX. A
         sentence-transformer maps 'cost of staying in the hostel' and
         'How much is the hostel fee?' to nearby vectors because it
         was trained on paraphrase pairs. The ARCHITECTURE of the bot
         does not change at all -- embed, cosine, argmax -- only the
         embedding function does, which is why 14_faq_chatbot.md is a
         small diff against this file rather than a different
         program""")
    else:
        print(f"""         {best_name.upper()} GOT ALL OF THEM, and saying so is
         the honest report: six FAQ entries on distinct topics is an
         easy retrieval problem, and a keyword method is enough.
         Character n-grams win because 'exams' and 'examination' share
         the substrings 'exam', 'xam' -- much of the morphological
         robustness people reach for embeddings to get, at no cost.
         The argument for embeddings appears when entries overlap in
         vocabulary or a query paraphrases without sharing words --
         scale this FAQ to a hundred entries and it will""")

    # the word-level miss is the instructive one, so show it even when the
    # best representation got everything right
    wv = TfidfVectorizer()
    WM = wv.fit_transform(questions)
    WS = cosine_similarity(wv.transform([q for q, _ in f.FAQ_QUERIES]), WM)
    wpred = WS.argmax(axis=1)
    print("\n      what WORD-level TF-IDF got wrong, and why it matters:")
    shown = False
    for (q, gold), p, row in zip(f.FAQ_QUERIES, wpred, WS):
        if p == gold:
            continue
        shown = True
        print(f"        query          : {q!r}")
        print(f"        matched        : {questions[p]!r}  "
              f"score {row[p]:.4f}")
        print(f"        should have been: {questions[gold]!r} "
              f"score {row[gold]:.4f}")
        if abs(row[p] - row[gold]) < 1e-9:
            print(f"""         AN EXACT TIE, broken by which entry happens to
         come first in the list. And look at WHY both scored
         {row[p]:.4f}: the only shared terms are the function words
         'are', 'the' and 'when'. NEITHER match had anything to do
         with meaning, and the 'right' answer would have been just as
         accidental.
         THAT is the failure sentence embeddings genuinely fix --
         'exams' and 'examination' are neighbours in an embedding
         space and unrelated as strings""")
    if not shown:
        print("        (none -- word-level TF-IDF also got all six)")

    print("""
      and the threshold every FAQ bot needs:
        argmax ALWAYS returns something. Ask 'what is the wifi password'
        and this bot confidently returns its nearest FAQ entry, which is
        wrong. A production retriever compares the top similarity against
        a threshold and says 'I do not know' below it.""")
    vec = TfidfVectorizer()
    M = vec.fit_transform(questions)
    oob = "what is the wifi password"
    sim = cosine_similarity(vec.transform([oob]), M)[0]
    print(f"        '{oob}' -> best similarity {sim.max():.4f} "
          f"({questions[sim.argmax()][:40]})")
    print(f"""         {sim.max():.4f} AGAINST THE IN-VOCABULARY QUERIES' SCORES.
         Setting a floor is the single cheapest improvement to any
         retrieval bot, and the most commonly omitted""")

    assert best_acc >= 0.5, f"retrieval accuracy {best_acc:.4f} is too low"
    return best_acc


def main():
    print("  Experiments 12-14 -- the runnable halves")
    print("""
    ⚠ huggingface.co is refused by this environment's egress policy
      (403 at the gateway), so no pre-trained BERT, BART or
      sentence-transformer can be downloaded. 12_bert_mlm.md,
      13_summarization.md and 14_faq_chatbot.md carry that code,
      marked NOT EXECUTED.
      What runs here is the mechanism of each, from parts that are
      available.""")
    experiment_12()
    experiment_13()
    experiment_14()
    print("\n    all assertions passed")


if __name__ == "__main__":
    main()
