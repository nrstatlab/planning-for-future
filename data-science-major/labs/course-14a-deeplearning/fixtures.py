"""Shared data and settings for Course 14 A.

Everything is BUILT, not downloaded. MNIST, Fashion-MNIST, IMDb and every
pre-trained model live behind huggingface.co or a similar host, and this
environment's egress policy refuses those with a 403 at the gateway. So the
labs generate datasets with the same SHAPE and the same difficulty:

  * digits8x8  -- scikit-learn's bundled 8x8 handwritten digits, 1797 images.
                  Genuinely handwritten, genuinely a classification problem,
                  and small enough to train on a CPU in seconds.
  * shapes     -- 28x28 synthetic images in 4 classes, so a CNN has real
                  spatial structure to learn and its filters can be shown to
                  have learned edges.
  * reviews    -- 2000 short sentiment-labelled sentences, built from
                  templates with a KNOWN vocabulary, so what an LSTM learns
                  can be checked against the words that actually decide the
                  label.
  * sequences  -- a character-level corpus for the generation experiment.

Every generator takes a seed and is deterministic.
"""
import numpy as np

SEED = 42
DEVICE = "cpu"          # no GPU here, and none is needed at these sizes


def torch_seed():
    """Seed every source of randomness torch uses. Call before each model."""
    import torch
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    return torch


# ------------------------------------------------------------ digits

def digits(test_frac=0.25, seed=SEED):
    """scikit-learn's 8x8 digits: 1797 real handwritten samples, 10 classes."""
    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split
    d = load_digits()
    X = d.data.astype("float32") / 16.0            # 0..16 -> 0..1
    y = d.target.astype("int64")
    return train_test_split(X, y, test_size=test_frac, stratify=y,
                            random_state=seed)


# ------------------------------------------------------------ shapes

SHAPE_CLASSES = ("square", "circle", "triangle", "cross")


def shapes(n_per_class=500, size=28, seed=SEED, noise=0.15):
    """28x28 grayscale images of four shapes -- a real CNN problem.

    Built rather than downloaded, but the structure a CNN needs is genuinely
    there: local edges, orientation, and a class that depends on the SPATIAL
    ARRANGEMENT of strokes rather than on any single pixel.
    """
    rng = np.random.default_rng(seed)
    X, y = [], []
    for cls, name in enumerate(SHAPE_CLASSES):
        for _ in range(n_per_class):
            img = np.zeros((size, size), dtype="float32")
            r = rng.integers(6, 11)                  # radius / half-side
            cy = rng.integers(r + 2, size - r - 2)
            cx = rng.integers(r + 2, size - r - 2)
            yy, xx = np.mgrid[0:size, 0:size]
            dy, dx = yy - cy, xx - cx
            if name == "square":
                edge = (np.maximum(np.abs(dy), np.abs(dx)) == r)
                img[edge] = 1.0
            elif name == "circle":
                dist = np.sqrt(dy ** 2 + dx ** 2)
                img[(dist > r - 1.0) & (dist < r + 0.6)] = 1.0
            elif name == "triangle":
                for k in range(-r, r + 1):
                    row = cy + r - abs(k) * 0 - 0     # base row
                    img[min(size - 1, cy + r), np.clip(cx + k, 0, size - 1)] = 1.0
                for k in range(0, r + 1):
                    img[np.clip(cy + r - k, 0, size - 1),
                        np.clip(cx - r + k, 0, size - 1)] = 1.0
                    img[np.clip(cy + r - k, 0, size - 1),
                        np.clip(cx + r - k, 0, size - 1)] = 1.0
            else:                                     # cross
                img[np.clip(cy - r, 0, size - 1):np.clip(cy + r + 1, 0, size),
                    cx] = 1.0
                img[cy, np.clip(cx - r, 0, size - 1):
                        np.clip(cx + r + 1, 0, size)] = 1.0
            img += rng.normal(0, noise, (size, size)).astype("float32")
            X.append(np.clip(img, 0, 1))
            y.append(cls)
    X = np.stack(X)[:, None, :, :]                    # N, C, H, W
    y = np.array(y, dtype="int64")
    idx = rng.permutation(len(y))
    return X[idx], y[idx]


def shapes_split(test_frac=0.2, **kw):
    X, y = shapes(**kw)
    cut = int(len(y) * (1 - test_frac))
    return X[:cut], X[cut:], y[:cut], y[cut:]


# ------------------------------------------------------------ reviews

POSITIVE = ["excellent", "wonderful", "brilliant", "delightful", "superb",
            "loved", "gripping", "charming", "moving", "outstanding"]
NEGATIVE = ["awful", "terrible", "dreadful", "boring", "dull",
            "hated", "tedious", "disappointing", "weak", "predictable"]
NEUTRAL = ["film", "movie", "story", "cast", "script", "scene", "actor",
           "director", "plot", "ending", "the", "a", "was", "is", "very",
           "quite", "really", "and", "but", "with", "this", "that", "it"]


def reviews(n=2000, seed=SEED, max_len=20):
    """Short sentiment sentences with a KNOWN decisive vocabulary.

    Every sentence contains exactly one sentiment word, and the label is that
    word's polarity. So after training you can ask the model what it learned
    and CHECK it against the words that actually decide the answer -- which is
    impossible on a downloaded corpus.
    """
    rng = np.random.default_rng(seed)
    texts, labels = [], []
    for _ in range(n):
        pos = rng.random() < 0.5
        word = rng.choice(POSITIVE if pos else NEGATIVE)
        length = rng.integers(6, max_len)
        filler = list(rng.choice(NEUTRAL, size=length - 1))
        where = rng.integers(0, len(filler) + 1)
        tokens = filler[:where] + [word] + filler[where:]
        texts.append(" ".join(tokens))
        labels.append(int(pos))
    return texts, np.array(labels, dtype="int64")


def build_vocab(texts, min_count=1):
    from collections import Counter
    counts = Counter(w for t in texts for w in t.split())
    words = [w for w, c in counts.most_common() if c >= min_count]
    # 0 = padding, 1 = unknown
    return {w: i + 2 for i, w in enumerate(words)}


def encode(texts, vocab, max_len=20):
    out = np.zeros((len(texts), max_len), dtype="int64")
    for i, t in enumerate(texts):
        ids = [vocab.get(w, 1) for w in t.split()][:max_len]
        out[i, :len(ids)] = ids
    return out


# ------------------------------------------------------------ char corpus

CORPUS = (
    "the quick brown fox jumps over the lazy dog. "
    "a neural network learns a function from examples. "
    "the gradient flows backward through every layer. "
    "deep learning stacks simple functions into complex ones. "
    "an attention head compares every token with every other token. "
    "the loss falls when the weights move down the gradient. "
) * 40


# ---------------------------------------------------------------- real data
#
# The syllabus names MNIST (experiment 4), Fashion-MNIST (experiment 6) and
# IMDb (experiment 9) by name, and all three are reachable from here, so the
# labs use the real thing rather than a stand-in. Keras caches them under
# KERAS_HOME after the first download.
#
# The synthetic generators above are still used, but for a different job: they
# are the CONTROLLED datasets, where the answer is known in advance, so a lab
# can check that the network learned the intended thing rather than merely
# reporting an accuracy. Real data cannot do that. Both belong in a course.

def _keras_datasets():
    import os
    os.environ.setdefault("KERAS_BACKEND", "torch")
    os.environ.setdefault("KERAS_HOME", "/tmp/keras_home")
    import keras
    return keras.datasets


MNIST_CLASSES = [str(d) for d in range(10)]

FASHION_CLASSES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
                   "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]


def _image_subset(loader, n_train, n_test, seed=SEED, flatten=False):
    """Load an MNIST-shaped dataset, scale to [0, 1] and take a subset.

    A subset, because these labs run on CPU: 60,000 images through a CNN for
    12 epochs takes over an hour and teaches nothing that 8,000 does not. The
    subset is drawn with a fixed seed and STRATIFIED, so the class balance is
    the same as the full set and the numbers are reproducible.
    """
    (Xtr, ytr), (Xte, yte) = loader.load_data()
    rng = np.random.default_rng(seed)

    def take(X, y, n):
        if n is None or n >= len(X):
            idx = np.arange(len(X))
        else:
            per = n // 10
            idx = np.concatenate([rng.choice(np.where(y == c)[0], per,
                                             replace=False)
                                  for c in range(10)])
        rng.shuffle(idx)
        X = X[idx].astype("float32") / 255.0
        y = y[idx].astype("int64")
        return (X.reshape(len(X), -1) if flatten else X), y

    Xtr, ytr = take(Xtr, ytr, n_train)
    Xte, yte = take(Xte, yte, n_test)
    return Xtr, ytr, Xte, yte


def mnist(n_train=8000, n_test=2000, seed=SEED, flatten=True):
    """The real MNIST handwritten digits, 28x28, 10 classes."""
    return _image_subset(_keras_datasets().mnist, n_train, n_test, seed,
                         flatten)


def fashion_mnist(n_train=8000, n_test=2000, seed=SEED, flatten=False):
    """The real Fashion-MNIST clothing images, 28x28, 10 classes.

    Same shape as MNIST and deliberately so -- it was published as a
    drop-in replacement because MNIST had become too easy to be a test of
    anything. Experiment 6 will show that difference as a number.
    """
    return _image_subset(_keras_datasets().fashion_mnist, n_train, n_test,
                         seed, flatten)


IMDB_NUM_WORDS = 10000
IMDB_MAX_LEN = 200


def imdb(n_train=8000, n_test=4000, num_words=IMDB_NUM_WORDS,
         max_len=IMDB_MAX_LEN, seed=SEED):
    """The real IMDb movie review dataset, 50,000 labelled reviews.

    Returns padded integer sequences. Index offset: Keras reserves 0 for
    padding, 1 for the start token and 2 for out-of-vocabulary, so the word
    index needs +3 to line up -- a detail that silently corrupts the decoded
    text of every tutorial that forgets it, and which `imdb_decoder` handles.
    """
    ds = _keras_datasets()
    (Xtr, ytr), (Xte, yte) = ds.imdb.load_data(num_words=num_words)
    rng = np.random.default_rng(seed)

    def take(X, y, n):
        idx = rng.choice(len(X), min(n, len(X)), replace=False)
        return X[idx], np.asarray(y)[idx].astype("float32")

    Xtr, ytr = take(Xtr, ytr, n_train)
    Xte, yte = take(Xte, yte, n_test)

    def pad(seqs):
        out = np.zeros((len(seqs), max_len), dtype="int64")
        for i, s in enumerate(seqs):
            s = s[-max_len:]          # keep the END of a long review
            out[i, max_len - len(s):] = s
        return out

    return pad(Xtr), ytr, pad(Xte), yte


def imdb_decoder(num_words=IMDB_NUM_WORDS):
    """Map IMDb integer ids back to words, with the +3 offset applied."""
    wi = _keras_datasets().imdb.get_word_index()
    inv = {v + 3: k for k, v in wi.items() if v + 3 < num_words}
    inv.update({0: "<pad>", 1: "<start>", 2: "<oov>"})

    def decode(seq, skip_pad=True):
        return " ".join(inv.get(int(i), "<oov>") for i in seq
                        if not (skip_pad and int(i) == 0))
    return decode
