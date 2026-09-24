"""Experiments 9 and 10 -- an LSTM for sentiment analysis, and text generation
with a character-level RNN.

REAL PYTORCH RNNs, REAL TRAINING. What is not real is the IMDb dataset, which
downloads from a host this environment's egress policy refuses. The reviews
here are generated with a KNOWN decisive vocabulary -- every sentence contains
exactly one sentiment word and the label is that word's polarity -- which
turns out to be BETTER for teaching than IMDb, because you can ask the trained
model what it learned and CHECK the answer against the words that actually
decide the label. On a downloaded corpus you cannot.

`09_imdb.md` records the IMDb/Keras code and is marked NOT EXECUTED.
"""
import numpy as np
import torch
import torch.nn as nn

import fixtures as f


class Recurrent(nn.Module):
    """One class, three cell types -- so the comparison is like for like."""

    def __init__(self, vocab, cell="lstm", emb=24, hidden=32, n_classes=2):
        super().__init__()
        self.embed = nn.Embedding(vocab, emb, padding_idx=0)
        rnn_cls = {"rnn": nn.RNN, "lstm": nn.LSTM, "gru": nn.GRU}[cell]
        self.rnn = rnn_cls(emb, hidden, batch_first=True)
        self.head = nn.Linear(hidden, n_classes)
        self.cell = cell

    def forward(self, x):
        e = self.embed(x)
        out, _ = self.rnn(e)
        return self.head(out[:, -1, :])          # the LAST hidden state


class CharRNN(nn.Module):
    def __init__(self, n_chars, emb=32, hidden=128):
        super().__init__()
        self.embed = nn.Embedding(n_chars, emb)
        self.lstm = nn.LSTM(emb, hidden, batch_first=True)
        self.head = nn.Linear(hidden, n_chars)

    def forward(self, x, state=None):
        e = self.embed(x)
        out, state = self.lstm(e, state)
        return self.head(out), state


def train_clf(model, Xtr, ytr, Xte, yte, epochs=8, lr=3e-3, batch=64):
    torch.manual_seed(f.SEED)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    lossf = nn.CrossEntropyLoss()
    Xtr_t, ytr_t = torch.tensor(Xtr), torch.tensor(ytr)
    Xte_t, yte_t = torch.tensor(Xte), torch.tensor(yte)
    curve = []
    for ep in range(epochs):
        model.train()
        perm = torch.randperm(len(ytr))
        for i in range(0, len(ytr), batch):
            idx = perm[i:i + batch]
            opt.zero_grad()
            lossf(model(Xtr_t[idx]), ytr_t[idx]).backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            te = (model(Xte_t).argmax(1) == yte_t).float().mean().item()
        curve.append(te)
    return curve


def main():
    print("  Experiments 9 and 10 -- LSTM sentiment, and a character RNN")

    torch.manual_seed(f.SEED)
    torch.set_num_threads(2)

    # ================================================= experiment 9
    print("\n    --- experiment 9: sentiment analysis with an LSTM")

    texts, labels = f.reviews(n=2000)
    vocab = f.build_vocab(texts)
    X = f.encode(texts, vocab, max_len=20)
    cut = 1600
    Xtr, Xte = X[:cut], X[cut:]
    ytr, yte = labels[:cut], labels[cut:]
    print(f"\n      {len(ytr)} training sentences, {len(yte)} test, "
          f"vocabulary {len(vocab)} words, max length 20")
    print(f"      example: {texts[0]!r} -> {'positive' if labels[0] else 'negative'}")
    print(f"      class balance: {labels.mean():.3f} positive")

    print(f"\n      {'cell':<10}{'params':>9}{'epoch 1':>10}{'epoch 4':>10}"
          f"{'final':>9}")
    curves = {}
    for cell in ("rnn", "lstm", "gru"):
        torch.manual_seed(f.SEED)
        m = Recurrent(len(vocab) + 2, cell=cell)
        c = train_clf(m, Xtr, ytr, Xte, yte)
        curves[cell] = c
        print(f"      {cell.upper():<10}{sum(p.numel() for p in m.parameters()):>9,}"
              f"{c[0]:>10.4f}{c[3]:>10.4f}{c[-1]:>9.4f}")

    best = max(curves, key=lambda k: curves[k][-1])
    assert curves["lstm"][-1] > 0.85, "an LSTM must learn this task"
    rnn_f, lstm_f, gru_f = (curves["rnn"][-1], curves["lstm"][-1],
                            curves["gru"][-1])
    print(f"""         THE GATED CELLS WON, AND BY A LOT: LSTM {lstm_f:.4f} and
         GRU {gru_f:.4f} against the plain RNN's {rnn_f:.4f}. The RNN
         is barely above the {max(labels.mean(), 1-labels.mean()):.2f} you
         get by always guessing the majority class.
         That is a larger gap than 20-token sequences ought to produce,
         and the honest reading is that it is not only about memory
         length. The plain RNN has one weight matrix doing two jobs --
         carrying information forward AND deciding what to do with the
         new token -- and its gradients through 20 steps of tanh are
         already small enough to make optimisation slow. The gates give
         the LSTM a path where the gradient is multiplied by something
         close to 1.
         The vanishing-gradient arithmetic below states the limit case
         exactly, because a benchmark on 20 tokens cannot""")

    # ---- what did the model actually learn? ------------------------------
    print("\n      ASK THE MODEL WHAT IT LEARNED -- possible only because the")
    print("      decisive vocabulary is known:")
    torch.manual_seed(f.SEED)
    m = Recurrent(len(vocab) + 2, cell="lstm")
    train_clf(m, Xtr, ytr, Xte, yte)
    m.eval()
    scores = {}
    with torch.no_grad():
        for word in f.POSITIVE + f.NEGATIVE + f.NEUTRAL[:6]:
            if word not in vocab:
                continue
            seq = torch.tensor([[vocab[word]] + [0] * 19])
            logits = m(seq)
            p_pos = torch.softmax(logits, dim=1)[0, 1].item()
            scores[word] = p_pos
    pos_scores = [scores[w] for w in f.POSITIVE if w in scores]
    neg_scores = [scores[w] for w in f.NEGATIVE if w in scores]
    neu_scores = [scores[w] for w in f.NEUTRAL[:6] if w in scores]
    print(f"\n      {'group':<22}{'mean P(positive)':>19}{'n':>5}")
    for label, vals in (("POSITIVE words", pos_scores),
                        ("NEGATIVE words", neg_scores),
                        ("neutral words", neu_scores)):
        print(f"      {label:<22}{np.mean(vals):>19.4f}{len(vals):>5}")
    assert np.mean(pos_scores) > 0.8 and np.mean(neg_scores) < 0.2
    print(f"""         THE MODEL FOUND EXACTLY THE RIGHT WORDS. Fed a single
         token, it scores the positive vocabulary at {np.mean(pos_scores):.3f} and the
         negative at {np.mean(neg_scores):.3f}, with the neutral filler in between at
         {np.mean(neu_scores):.3f}.
         That check is only possible because the dataset was BUILT.
         On IMDb you can measure accuracy and you cannot verify what
         the model attended to -- which is why a generated dataset is
         the better teaching tool even though it is the smaller
         achievement""")

    # ---- and now the real IMDb dataset the syllabus names ----------------
    print("\n      NOW THE REAL THING: the IMDb dataset the syllabus names")
    imdb_tr, imdb_ytr, imdb_te, imdb_yte = f.imdb(n_train=6000, n_test=3000)
    # CrossEntropyLoss wants int64 class indices, not floats
    imdb_ytr = imdb_ytr.astype("int64")
    imdb_yte = imdb_yte.astype("int64")
    decode = f.imdb_decoder()
    print(f"      {len(imdb_ytr):,} training reviews, {len(imdb_yte):,} test, "
          f"vocabulary {f.IMDB_NUM_WORDS:,}, padded to {f.IMDB_MAX_LEN} tokens")
    print(f"      class balance: {imdb_ytr.mean():.3f} positive")
    sample = decode(imdb_tr[0])
    print(f"      a real review, label "
          f"{'positive' if imdb_ytr[0] else 'negative'}:")
    print(f"        \"{sample[:150]}...\"")
    print("""         these are real reviews written by real people: misspelt,
         sarcastic, full of plot summary that carries no sentiment at
         all. Nothing in them is guaranteed to be decisive the way the
         generated sentences above were""")

    print(f"\n      {'cell':<10}{'params':>11}{'epoch 1':>10}{'final test':>12}")
    imdb_res = {}
    for cell in ("rnn", "lstm", "gru"):
        torch.manual_seed(f.SEED)
        m = Recurrent(f.IMDB_NUM_WORDS, cell=cell, emb=32, hidden=64)
        c = train_clf(m, imdb_tr, imdb_ytr, imdb_te, imdb_yte, epochs=4,
                      lr=2e-3, batch=64)
        imdb_res[cell] = c[-1]
        print(f"      {cell.upper():<10}"
              f"{sum(p.numel() for p in m.parameters()):>11,}"
              f"{c[0]:>10.4f}{c[-1]:>12.4f}")

    majority = max(imdb_yte.mean(), 1 - imdb_yte.mean())
    best_imdb = max(imdb_res.values())
    print(f"\n      best {best_imdb:.4f} against a majority-class baseline of "
          f"{majority:.4f}")
    assert best_imdb > majority + 0.15, (
        f"IMDb accuracy {best_imdb:.4f} barely beats the {majority:.4f} "
        f"baseline")
    imdb_gap = imdb_res["lstm"] - imdb_res["rnn"]
    print(f"""         THE GAP BETWEEN CELLS NARROWED ON REAL DATA:
         LSTM {imdb_res['lstm']:.4f} against RNN {imdb_res['rnn']:.4f}, a
         difference of {imdb_gap:+.4f}, where the generated task gave
         {lstm_f - rnn_f:+.4f}.
         Sentiment in a real review is REDUNDANT -- 'terrible',
         'waste', 'boring' and 'awful' may all appear in the same
         paragraph -- so a model that catches any one of them scores.
         The generated task had exactly one decisive word per sentence
         and no redundancy at all, which is what made the gap so wide.
         Both numbers are real; they measure different things, and
         reporting only the one that flatters the LSTM would be the
         dishonest version of this lab""")

    # ---- the vanishing gradient, as arithmetic ---------------------------
    print("\n      why LSTM exists, in arithmetic rather than a benchmark:")
    print(f"      {'sequence length':>17}{'RNN gradient (w=0.5)':>24}"
          f"{'LSTM cell path':>18}")
    for T in (5, 10, 50, 100, 500, 1100):
        print(f"      {T:>17}{0.5 ** T:>24.2e}{1.0:>18.2f}")
    # 0.5**500 is 3.05e-151 -- vanishingly small but NOT zero. Underflow to
    # exactly zero happens past T=1074, the last power a float64 can hold.
    assert 0.5 ** 500 > 0.0
    assert 0.5 ** 1100 == 0.0
    print("""         A PLAIN RNN MULTIPLIES the same recurrent weight at every
         step, so the gradient decays geometrically with the sequence
         length. At 500 steps it is 3.05e-151 -- not literally zero, and
         it is worth being exact about that, because 'the gradient
         vanishes' is usually said as though floating point were the
         problem. It is not. 3.05e-151 is a perfectly representable
         number; it is just so much smaller than the other gradients in
         the sum that it changes no weight by any amount you could
         measure. Past 1,074 steps float64 does underflow to exactly
         zero, and the last row shows it.
         The LSTM's CELL STATE is an ADDITIVE path: c_t = f*c_{t-1} +
         i*g. With the forget gate near 1 the gradient along it is
         near 1 REGARDLESS of length, so information survives
         hundreds of steps.
         'Additive path instead of repeated multiplication' is the
         one-sentence answer to 'why LSTM?'""")

    print(f"\n      {'':<10}{'gates':<34}{'parameters vs RNN'}")
    for cell, gates, mult in (
            ("RNN", "none", "1x"),
            ("LSTM", "forget, input, output (+ cell)", "4x"),
            ("GRU", "reset, update", "3x")):
        print(f"      {cell:<10}{gates:<34}{mult}")
    print("""         GRU merges the LSTM's forget and input gates into one
         update gate and drops the separate cell state. Fewer
         parameters, usually indistinguishable accuracy, and faster --
         which is why GRU is a reasonable default and LSTM is the one
         you name in an exam""")

    # ================================================= experiment 10
    print("\n    --- experiment 10: character-level text generation")

    corpus = f.CORPUS
    chars = sorted(set(corpus))
    stoi = {c: i for i, c in enumerate(chars)}
    itos = {i: c for c, i in stoi.items()}
    data = np.array([stoi[c] for c in corpus], dtype="int64")
    seq_len = 40
    print(f"\n      corpus {len(corpus):,} characters, {len(chars)} distinct")

    X, Y = [], []
    for i in range(0, len(data) - seq_len - 1, 3):
        X.append(data[i:i + seq_len])
        Y.append(data[i + 1:i + seq_len + 1])
    X = torch.tensor(np.array(X))
    Y = torch.tensor(np.array(Y))
    print(f"      {len(X):,} training windows of {seq_len} characters")

    torch.manual_seed(f.SEED)
    model = CharRNN(len(chars))
    opt = torch.optim.Adam(model.parameters(), lr=3e-3)
    lossf = nn.CrossEntropyLoss()
    print(f"\n      {'epoch':>7}{'loss':>10}{'perplexity':>13}")
    for ep in range(12):
        model.train()
        perm = torch.randperm(len(X))
        total = 0.0
        for i in range(0, len(X), 64):
            idx = perm[i:i + 64]
            opt.zero_grad()
            logits, _ = model(X[idx])
            loss = lossf(logits.reshape(-1, len(chars)), Y[idx].reshape(-1))
            loss.backward()
            opt.step()
            total += loss.item() * len(idx)
        mean_loss = total / len(X)
        if ep % 3 == 0 or ep == 11:
            print(f"      {ep:>7}{mean_loss:>10.4f}{np.exp(mean_loss):>13.3f}")
    final_loss = mean_loss
    assert final_loss < 1.5, "the char RNN should learn this small corpus"

    print(f"""
      PERPLEXITY = exp(cross-entropy) = {np.exp(final_loss):.2f}
         read it as 'the model is as uncertain as if it were choosing
         uniformly among {np.exp(final_loss):.1f} characters'. A uniform guess over
         {len(chars)} characters would be perplexity {len(chars)}, so the model has
         gone from {len(chars)} to {np.exp(final_loss):.1f}. That is what perplexity is for --
         it puts a loss on a scale you can reason about""")

    # ---- generation, and the temperature knob ----------------------------
    def generate(seed_text, n=120, temperature=1.0):
        model.eval()
        ids = [stoi.get(c, 0) for c in seed_text]
        state = None
        out = list(seed_text)
        with torch.no_grad():
            x = torch.tensor([ids])
            logits, state = model(x, state)
            for _ in range(n):
                logits_last = logits[0, -1] / max(temperature, 1e-6)
                probs = torch.softmax(logits_last, dim=0)
                nxt = int(torch.multinomial(probs, 1))
                out.append(itos[nxt])
                logits, state = model(torch.tensor([[nxt]]), state)
        return "".join(out)

    print("\n      generated text at three temperatures, same seed:")
    for temp in (0.2, 0.7, 1.5):
        text = generate("the ", n=110, temperature=temp)
        print(f"\n        T = {temp}")
        print(f"          {text[:70]!r}")
        print(f"          {text[70:]!r}")

    lo = generate("the ", n=300, temperature=0.2)
    hi = generate("the ", n=300, temperature=1.5)
    lo_distinct = len(set(lo.split()))
    hi_distinct = len(set(hi.split()))
    print(f"\n      distinct words in 300 characters: "
          f"T=0.2 gives {lo_distinct}, T=1.5 gives {hi_distinct}")
    print("""         TEMPERATURE DIVIDES THE LOGITS BEFORE THE SOFTMAX.
           T -> 0    always pick the most likely character. Repetitive,
                     and it will loop.
           T = 1     sample from the model's actual distribution.
           T -> inf  uniform noise.
         Low temperature is SAFE AND BORING; high temperature is
         CREATIVE AND WRONG. Every text-generation API exposes this
         knob, and it is the same one -- which is worth knowing when
         somebody asks why an LLM 'made something up'""")

    print("""
      and the limitation this experiment makes obvious:
        a character RNN learns SPELLING and LOCAL GRAMMAR because
        those are decided within a few characters. It does not learn
        MEANING, because meaning depends on tokens hundreds of steps
        away -- which is exactly the dependency length an RNN cannot
        hold. That gap is what attention was invented to close, and it
        is experiment 11""")

    return {"lstm": curves["lstm"][-1], "perplexity": float(np.exp(final_loss))}


if __name__ == "__main__":
    main()
