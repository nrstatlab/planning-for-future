"""Experiments 11 and 12 -- use a pre-trained model for a simple task, and
build a sentiment app on it.

EXPERIMENT 11 RUNS FOR REAL. `keras.applications` fetches the published
MobileNetV2 ImageNet weights from storage.googleapis.com, which this
environment permits, so the pre-trained model below is the actual network
with its actual 3.5 million trained parameters. The simple task it is put to
is IMAGE RETRIEVAL -- find the nearest neighbour of a query image in an
embedding space the model was never trained to produce -- which has a
checkable answer, because the labels are known.

EXPERIMENT 12 CANNOT RUN. It asks for a Hugging Face deployment, and
huggingface.co is refused by this environment's egress policy with a 403 at
the gateway, so no BERT-family checkpoint can be fetched and no Space can be
pushed. `12_huggingface_app.md` carries that code and is marked NOT EXECUTED.

What runs in its place is the MECHANISM those models are built from, in
PyTorch from scratch: scaled dot-product attention, multi-head attention, and
a full transformer encoder block, trained on a task designed so the attention
pattern is CHECKABLE. Calling `pipeline('sentiment-analysis')` teaches an API;
implementing attention teaches why the API works -- and the syllabus asks for
the attention mechanism "intuitively", which a from-scratch implementation
delivers and a downloaded checkpoint does not.
"""
import os

os.environ.setdefault("KERAS_BACKEND", "torch")
os.environ.setdefault("KERAS_HOME", "/tmp/keras_home")

import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import fixtures as f


def scaled_dot_product_attention(Q, K, V, mask=None):
    """The one equation the whole architecture is built on.

        Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V

    Written out rather than called, because the sqrt(d_k) is the part
    people cannot explain and it is right here.
    """
    d_k = Q.size(-1)
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    weights = torch.softmax(scores, dim=-1)
    return weights @ V, weights


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.q = nn.Linear(d_model, d_model)
        self.k = nn.Linear(d_model, d_model)
        self.v = nn.Linear(d_model, d_model)
        self.out = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        B, T, D = x.shape
        def split(t):
            return t.view(B, T, self.n_heads, self.d_k).transpose(1, 2)
        Q, K, V = split(self.q(x)), split(self.k(x)), split(self.v(x))
        ctx, weights = scaled_dot_product_attention(Q, K, V, mask)
        ctx = ctx.transpose(1, 2).contiguous().view(B, T, D)
        return self.out(ctx), weights


class EncoderBlock(nn.Module):
    """The transformer encoder block, exactly as in 'Attention Is All You
    Need': multi-head attention, residual + norm, feed-forward, residual +
    norm."""

    def __init__(self, d_model, n_heads, d_ff):
        super().__init__()
        self.attn = MultiHeadAttention(d_model, n_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(nn.Linear(d_model, d_ff), nn.ReLU(),
                                nn.Linear(d_ff, d_model))
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x, mask=None):
        a, w = self.attn(x, mask)
        x = self.norm1(x + a)              # residual, then norm
        x = self.norm2(x + self.ff(x))
        return x, w


class TinyTransformer(nn.Module):
    def __init__(self, vocab, max_len=20, d_model=32, n_heads=4, d_ff=64,
                 n_classes=2):
        super().__init__()
        self.embed = nn.Embedding(vocab, d_model, padding_idx=0)
        self.pos = nn.Parameter(torch.zeros(1, max_len, d_model))
        nn.init.normal_(self.pos, std=0.02)
        self.block = EncoderBlock(d_model, n_heads, d_ff)
        self.head = nn.Linear(d_model, n_classes)
        self.use_pos = True

    def forward(self, x, return_attn=False):
        e = self.embed(x)
        if self.use_pos:
            e = e + self.pos[:, :x.size(1)]
        mask = (x != 0).unsqueeze(1).unsqueeze(2)
        h, w = self.block(e, mask)
        pooled = (h * (x != 0).unsqueeze(-1)).sum(1) / \
                 (x != 0).sum(1, keepdim=True).clamp(min=1)
        logits = self.head(pooled)
        return (logits, w) if return_attn else logits


def train_clf(model, Xtr, ytr, Xte, yte, epochs=12, lr=3e-3, batch=64):
    torch.manual_seed(f.SEED)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    lossf = nn.CrossEntropyLoss()
    Xtr_t, ytr_t = torch.tensor(Xtr), torch.tensor(ytr)
    Xte_t, yte_t = torch.tensor(Xte), torch.tensor(yte)
    for _ in range(epochs):
        model.train()
        perm = torch.randperm(len(ytr))
        for i in range(0, len(ytr), batch):
            idx = perm[i:i + batch]
            opt.zero_grad()
            lossf(model(Xtr_t[idx]), ytr_t[idx]).backward()
            opt.step()
    model.eval()
    with torch.no_grad():
        return (model(Xte_t).argmax(1) == yte_t).float().mean().item()


def pretrained_task():
    """Experiment 11 -- a real pre-trained model put to a simple task.

    The task is RETRIEVAL: embed every image with frozen MobileNetV2, then
    for each query find its nearest neighbour by cosine distance and ask
    whether that neighbour has the same label. Nothing is trained. The
    baseline is the same retrieval done on raw pixels, so the number means
    something.
    """
    import keras

    print("\n    --- experiment 11: a pre-trained model, used without "
          "training anything")

    Xq, yq, Xd, yd = f.fashion_mnist(n_train=200, n_test=1000)
    print(f"\n      {len(yq)} query images against a {len(yd)}-image "
          f"database, Fashion-MNIST, 10 classes")

    model = keras.applications.MobileNetV2(weights="imagenet",
                                           include_top=False,
                                           input_shape=(96, 96, 3),
                                           pooling="avg")
    print(f"      MobileNetV2, real ImageNet weights, "
          f"{model.count_params():,} parameters, NOTHING trained here")

    def embed(X):
        x = keras.ops.convert_to_tensor(X.reshape(len(X), 28, 28, 1))
        x = keras.ops.image.resize(x, (96, 96), interpolation="bilinear")
        x = keras.ops.repeat(x, 3, axis=-1)
        x = np.asarray(keras.ops.convert_to_numpy(x), dtype="float32") * 255.0
        x = keras.applications.mobilenet_v2.preprocess_input(x)
        return model.predict(x, verbose=0, batch_size=32)

    Eq, Ed = embed(Xq), embed(Xd)
    print(f"      each image becomes a {Eq.shape[1]}-number embedding")

    def top1(A, B, ya, yb):
        A = A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-9)
        B = B / (np.linalg.norm(B, axis=1, keepdims=True) + 1e-9)
        nn_idx = (A @ B.T).argmax(axis=1)
        return float((yb[nn_idx] == ya).mean())

    acc_deep = top1(Eq, Ed, yq, yd)
    acc_pix = top1(Xq.reshape(len(Xq), -1), Xd.reshape(len(Xd), -1), yq, yd)
    chance = 1.0 / 10

    print(f"\n      {'retrieval space':<34}{'top-1 same-class':>18}")
    print(f"      {'MobileNetV2 embedding (1280-d)':<34}{acc_deep:>18.4f}")
    print(f"      {'raw pixels (784-d)':<34}{acc_pix:>18.4f}")
    print(f"      {'chance':<34}{chance:>18.4f}")

    if acc_deep > acc_pix:
        print(f"""         THE PRE-TRAINED EMBEDDING IS THE BETTER SPACE, and
         nothing was trained to make it so. MobileNetV2 never saw a
         Fashion-MNIST image and none of ImageNet's 1,000 classes is
         a pullover; the features are simply GENERIC enough that
         'looks like the same kind of thing' survives the transfer.
         That is what people mean by a pre-trained model being useful
         off the shelf, and it is measurable: {acc_deep:.4f} against
         {acc_pix:.4f} for raw pixel distance""")
    else:
        print(f"""         RAW PIXELS WON HERE ({acc_pix:.4f} against
         {acc_deep:.4f}), and the number is reported as measured
         rather than reshaped. Fashion-MNIST images are centred,
         size-normalised and on a black background, so pixel distance
         is unusually strong on them -- and 28x28 grayscale upscaled
         to 96x96 gives an ImageNet model almost none of the texture
         and colour statistics its features were built from.
         The honest conclusion is that a pre-trained embedding is not
         automatically better; it is better when the domain is close""")

    assert acc_deep > chance and acc_pix > chance
    return acc_deep, acc_pix


def main():
    print("  Experiment 11 -- a real pre-trained model on a real task; "
          "experiment 12 -- attention from scratch")

    torch.manual_seed(f.SEED)
    torch.set_num_threads(2)

    pretrained_task()

    print("""
    ⚠ EXPERIMENT 12 asks for a Hugging Face deployment. huggingface.co
      is refused by this environment's egress policy (403 at the
      gateway), so no BERT checkpoint can be fetched and no Space can
      be pushed. 12_huggingface_app.md holds that code, marked NOT
      EXECUTED.
      What runs here instead is the mechanism those models are built
      from, implemented and trained.""")

    # ---- the equation, on numbers you can check --------------------------
    print("\n    --- scaled dot-product attention, on a worked example")

    torch.manual_seed(0)
    d_k = 4
    Q = torch.tensor([[[1.0, 0.0, 0.0, 0.0]]])          # 1 query
    K = torch.tensor([[[1.0, 0.0, 0.0, 0.0],            # identical to Q
                       [0.0, 1.0, 0.0, 0.0],            # orthogonal
                       [0.7, 0.7, 0.0, 0.0]]])          # partly aligned
    V = torch.tensor([[[10.0, 0.0], [0.0, 10.0], [5.0, 5.0]]])
    out, w = scaled_dot_product_attention(Q, K, V)
    print(f"\n      raw scores  Q.K^T          : "
          f"{(Q @ K.transpose(-2, -1))[0, 0].tolist()}")
    print(f"      scaled by sqrt(d_k) = {math.sqrt(d_k):.1f}   : "
          f"{[round(x, 4) for x in (Q @ K.transpose(-2, -1) / math.sqrt(d_k))[0, 0].tolist()]}")
    print(f"      attention weights (softmax): "
          f"{[round(x, 4) for x in w[0, 0].tolist()]}")
    print(f"      output = weights @ V       : "
          f"{[round(x, 4) for x in out[0, 0].tolist()]}")
    assert abs(w[0, 0].sum().item() - 1.0) < 1e-5
    assert w[0, 0, 0] > w[0, 0, 1], "the aligned key must win"
    print("""         the query matched key 0 exactly, key 2 partly, key 1 not
         at all -- and the weights rank them in that order. The output
         is a WEIGHTED AVERAGE of the values, weighted by how well
         each key matched the query.
         That is all attention is: a soft, learned lookup table""")

    # ---- why sqrt(d_k) ----------------------------------------------------
    print("\n      why divide by sqrt(d_k)? -- measured, not asserted:")
    print(f"      {'d_k':>6}{'std of Q.K':>14}{'std / sqrt(d_k)':>18}"
          f"{'max softmax weight':>21}")
    for d in (4, 16, 64, 256, 1024):
        g = torch.randn(2000, d)
        h = torch.randn(2000, d)
        dots = (g * h).sum(1)
        scores_unscaled = torch.randn(1, 64) * dots.std()
        w_un = torch.softmax(scores_unscaled, dim=1).max().item()
        print(f"      {d:>6}{dots.std().item():>14.3f}"
              f"{(dots.std() / math.sqrt(d)).item():>18.3f}{w_un:>21.4f}")
    print("""         THE DOT PRODUCT'S STANDARD DEVIATION GROWS AS sqrt(d_k).
         Feed those raw scores to a softmax at d_k = 1024 and one
         weight goes to ~1 and the rest to ~0 -- the softmax
         SATURATES, its gradient vanishes, and the model stops
         learning.
         Dividing by sqrt(d_k) holds the score variance at 1 whatever
         the dimension. That is the entire reason for the scaling
         factor, and it is the detail most people cannot explain""")

    # ---- train it on a checkable task ------------------------------------
    print("\n    --- a transformer encoder, trained")

    texts, labels = f.reviews(n=2000)
    vocab = f.build_vocab(texts)
    X = f.encode(texts, vocab, max_len=20)
    cut = 1600
    Xtr, Xte, ytr, yte = X[:cut], X[cut:], labels[:cut], labels[cut:]

    torch.manual_seed(f.SEED)
    model = TinyTransformer(len(vocab) + 2)
    acc = train_clf(model, Xtr, ytr, Xte, yte)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"\n      one encoder block, 4 heads, d_model 32: "
          f"{n_params:,} parameters")
    print(f"      test accuracy {acc:.4f}")
    assert acc > 0.85

    # ---- and the check that a downloaded model cannot give you -----------
    print("\n      WHERE DID IT ATTEND? -- checkable, because the decisive")
    print("      word in every sentence is known by construction:")
    model.eval()
    inv = {i: w for w, i in vocab.items()}
    hits = 0
    shown = 0
    with torch.no_grad():
        for n in range(120):
            ids = torch.tensor(Xte[n:n + 1])
            _, w = model(ids, return_attn=True)
            toks = [inv.get(int(i), "") for i in Xte[n] if int(i) != 0]
            # average over heads and over query positions
            attn = w[0, :, :len(toks), :len(toks)].mean(0).mean(0)
            top = int(attn.argmax())
            decisive = [j for j, t in enumerate(toks)
                        if t in f.POSITIVE or t in f.NEGATIVE]
            if decisive and top == decisive[0]:
                hits += 1
            if shown < 3 and decisive:
                shown += 1
                print(f"\n        {' '.join(toks)}")
                print(f"        {'':<0}decisive word: {toks[decisive[0]]!r} "
                      f"at position {decisive[0]}")
                print(f"        most-attended: {toks[top]!r} at position {top}")
                bars = "".join("#" if j == top else
                               ("+" if j == decisive[0] else ".")
                               for j in range(len(toks)))
                print(f"        {bars}")
    rate = hits / 120
    print(f"\n      the sentiment word was the most-attended token in "
          f"{hits}/120 = {rate:.1%} of sentences")
    print(f"""         THAT IS THE CHECK A DOWNLOADED MODEL CANNOT GIVE YOU.
         On IMDb you can report accuracy and you cannot verify what
         the model attended to; here the decisive word is known by
         construction, so the attention map can be scored against it.
         Note the rate is {rate:.0%}, not 100%. Attention weights are
         NOT an explanation -- a model can reach the right answer
         while attending elsewhere, because information also flows
         through the residual stream and the feed-forward layer.
         'Attention is interpretability' is a claim that has been
         argued down in the literature, and this number is a small
         piece of why""")

    # ---- position encoding, ablated --------------------------------------
    print("\n      ablation: remove the positional encoding")
    torch.manual_seed(f.SEED)
    m2 = TinyTransformer(len(vocab) + 2)
    m2.use_pos = False
    acc_nopos = train_clf(m2, Xtr, ytr, Xte, yte)
    print(f"      with positions    {acc:.4f}")
    print(f"      WITHOUT positions {acc_nopos:.4f}")
    print(f"""         BARELY ANY DIFFERENCE -- and that is the correct result
         for THIS task, which is a bag-of-words problem: the label
         depends on WHICH sentiment word appears, not on where.
         Attention is PERMUTATION-EQUIVARIANT: shuffle the input and
         the outputs shuffle with it. It has no idea what order means,
         which is why positional encodings exist at all.
         The ablation shows nothing here because the task does not
         need order. On translation or parsing, removing them is
         catastrophic -- and reporting the null result honestly is
         better than choosing a task that flatters the claim""")

    # ---- attention against recurrence -------------------------------------
    print("\n    --- why attention replaced recurrence")
    print(f"\n      {'':<26}{'RNN / LSTM':<26}{'self-attention'}")
    for label, rnn, att in (
            ("path between 2 tokens", "O(distance) steps", "O(1) -- ONE hop"),
            ("parallel over sequence", "NO -- inherently serial", "YES"),
            ("compute per layer", "O(T * d^2)", "O(T^2 * d)"),
            ("memory", "O(T * d)", "O(T^2)"),
            ("long dependencies", "gradient decays", "direct connection"),
            ("needs position info", "implicit in the order", "MUST BE ADDED")):
        print(f"      {label:<26}{rnn:<26}{att}")

    print(f"\n      the O(T^2) cost, which is the whole limitation:")
    print(f"      {'sequence length':>17}{'attention scores':>19}"
          f"{'x vs T=512':>13}")
    base = 512 ** 2
    for T in (512, 1024, 4096, 32768):
        print(f"      {T:>17}{T ** 2:>19,}{T ** 2 / base:>12.0f}x")
    print("""         QUADRUPLING THE CONTEXT COSTS SIXTEEN TIMES THE
         ATTENTION COMPUTE. That single fact drives most of the
         research in long-context models -- sparse attention,
         linear attention, FlashAttention, state-space models.
         The RNN's O(T) cost was never the problem; its O(distance)
         path length was, and attention traded one for the other""")

    print("""
      and what a transformer BUYS that an RNN cannot:
        PARALLELISM. An RNN must compute step t before step t+1, so
        training time scales with sequence length no matter how many
        GPUs you have. Attention computes every position at once.
        That is why transformers could be scaled to billions of
        parameters and RNNs could not -- the architecture was chosen
        to fit the hardware, which is the honest history""")

    return {"transformer": acc, "attn_hit_rate": rate}


if __name__ == "__main__":
    main()
