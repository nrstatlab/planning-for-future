"""Experiments 1 and 3 -- build a perceptron from scratch in Python, and
visualize activation functions and their gradients.

NO FRAMEWORK IS USED HERE. Everything is NumPy, because the point of this
experiment is that a neural network is arithmetic you could do by hand, and
importing Keras hides exactly the part that is being taught.

The syllabus's own activity for Outcome 2 says the same thing: "implement a
simple 3-layer neural network from scratch in Python/NumPy (without
Keras/TensorFlow) to observe propagation and optimization effects."
"""
import numpy as np

import fixtures as f


# ------------------------------------------------------------ activations

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))


def d_sigmoid(z):
    s = sigmoid(z)
    return s * (1 - s)


def tanh(z):
    return np.tanh(z)


def d_tanh(z):
    return 1 - np.tanh(z) ** 2


def relu(z):
    return np.maximum(0, z)


def d_relu(z):
    return (z > 0).astype(float)


def leaky_relu(z, a=0.01):
    return np.where(z > 0, z, a * z)


def d_leaky_relu(z, a=0.01):
    return np.where(z > 0, 1.0, a)


def softmax(z):
    z = z - z.max(axis=1, keepdims=True)      # subtract the max: see below
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


# ------------------------------------------------------------ perceptron

class Perceptron:
    """Rosenblatt's 1958 perceptron. A linear classifier with a step
    activation, trained by the perceptron learning rule -- not by gradient
    descent, because a step function has no useful gradient."""

    def __init__(self, n_features, lr=0.1):
        self.w = np.zeros(n_features)
        self.b = 0.0
        self.lr = lr

    def predict(self, X):
        return (X @ self.w + self.b > 0).astype(int)

    def fit(self, X, y, epochs=20):
        history = []
        for _ in range(epochs):
            errors = 0
            for xi, target in zip(X, y):
                pred = int(xi @ self.w + self.b > 0)
                update = self.lr * (target - pred)
                if update != 0:
                    self.w += update * xi
                    self.b += update
                    errors += 1
            history.append(errors)
            if errors == 0:
                break
        return history


def main():
    print("  Experiments 1 and 3 -- a perceptron from scratch, and activations")

    # ================================================= experiment 1
    print("\n    --- experiment 1: the perceptron")

    print("""
    the model, in one line:
        y_hat = step(w . x + b)
      trained by the PERCEPTRON RULE, not gradient descent:
        w <- w + lr * (y - y_hat) * x
         it only updates on a MISTAKE, and a step function has a zero
         gradient everywhere it is defined -- which is why this rule
         exists and why the step activation had to be replaced before
         deep networks were possible""")

    # ---- AND, OR: linearly separable -------------------------------------
    X_logic = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    print(f"\n      {'gate':<8}{'targets':<14}{'epochs to converge':>20}"
          f"{'accuracy':>11}")
    results = {}
    for gate, targets in (("AND", [0, 0, 0, 1]),
                          ("OR", [0, 1, 1, 1]),
                          ("NAND", [1, 1, 1, 0]),
                          ("XOR", [0, 1, 1, 0])):
        y = np.array(targets)
        p = Perceptron(2)
        hist = p.fit(X_logic, y, epochs=100)
        acc = (p.predict(X_logic) == y).mean()
        converged = len(hist) if hist[-1] == 0 else None
        results[gate] = acc
        print(f"      {gate:<8}{str(targets):<14}"
              f"{(converged if converged else 'NEVER'):>20}{acc:>11.2f}")

    assert results["AND"] == 1.0 and results["OR"] == 1.0
    assert results["XOR"] < 1.0, "a single perceptron cannot learn XOR"
    print(f"""         XOR NEVER CONVERGES, and it never will -- accuracy stuck
         at {results['XOR']:.2f}. A single perceptron draws ONE straight line,
         and no straight line separates {{(0,1),(1,0)}} from
         {{(0,0),(1,1)}}.
         Minsky and Papert proved this in 1969 and it stopped neural
         network research for a decade. The fix is not a better
         learning rule -- it is a HIDDEN LAYER, which is experiment 4""")

    # ---- solve XOR with one hidden layer ---------------------------------
    print("\n      the same XOR, with ONE hidden layer of 2 units:")
    rng = np.random.default_rng(f.SEED)
    y_xor = np.array([[0.], [1.], [1.], [0.]])
    W1 = rng.normal(0, 1, (2, 2))
    b1 = np.zeros((1, 2))
    W2 = rng.normal(0, 1, (2, 1))
    b2 = np.zeros((1, 1))
    lr = 0.5
    losses = []
    for epoch in range(4000):
        z1 = X_logic @ W1 + b1
        a1 = tanh(z1)
        z2 = a1 @ W2 + b2
        a2 = sigmoid(z2)
        loss = -np.mean(y_xor * np.log(a2 + 1e-9)
                        + (1 - y_xor) * np.log(1 - a2 + 1e-9))
        losses.append(loss)
        d2 = (a2 - y_xor) / len(X_logic)          # dL/dz2 for BCE + sigmoid
        dW2 = a1.T @ d2
        db2 = d2.sum(axis=0, keepdims=True)
        d1 = (d2 @ W2.T) * d_tanh(z1)
        dW1 = X_logic.T @ d1
        db1 = d1.sum(axis=0, keepdims=True)
        W2 -= lr * dW2
        b2 -= lr * db2
        W1 -= lr * dW1
        b1 -= lr * db1
    preds = (a2 > 0.5).astype(int).ravel()
    acc = (preds == y_xor.ravel().astype(int)).mean()
    print(f"      loss {losses[0]:.4f} -> {losses[-1]:.4f} over 4000 epochs")
    print(f"      predictions {preds.tolist()}, targets "
          f"{y_xor.ravel().astype(int).tolist()}, accuracy {acc:.2f}")
    assert acc == 1.0, "one hidden layer must solve XOR"
    print("""         ONE HIDDEN LAYER SOLVED IT. The hidden units learn a new
         representation in which the problem IS linearly separable,
         and the output layer draws its straight line there.
         That is the whole idea of depth: each layer re-describes the
         input so that the next layer's job is easier""")

    # ---- a 3-layer network, from scratch, on real digits ------------------
    print("\n    --- a 3-layer network on real handwritten digits")
    Xtr, Xte, ytr, yte = f.digits()
    n_in, n_hidden, n_out = Xtr.shape[1], 64, 10
    print(f"      {len(Xtr)} training images, {len(Xte)} test, "
          f"{n_in} pixels, {n_out} classes")

    rng = np.random.default_rng(f.SEED)
    # He initialisation for ReLU -- see experiment 5 for why it matters
    W1 = rng.normal(0, np.sqrt(2 / n_in), (n_in, n_hidden))
    b1 = np.zeros(n_hidden)
    W2 = rng.normal(0, np.sqrt(2 / n_hidden), (n_hidden, n_out))
    b2 = np.zeros(n_out)

    Y = np.eye(n_out)[ytr]
    lr, batch = 0.1, 32
    curve = []
    for epoch in range(60):
        order = rng.permutation(len(Xtr))
        for i in range(0, len(Xtr), batch):
            idx = order[i:i + batch]
            xb, yb = Xtr[idx], Y[idx]
            # ---- forward
            z1 = xb @ W1 + b1
            a1 = relu(z1)
            z2 = a1 @ W2 + b2
            a2 = softmax(z2)
            # ---- backward
            d2 = (a2 - yb) / len(xb)      # softmax + cross-entropy: see below
            dW2 = a1.T @ d2
            db2 = d2.sum(axis=0)
            d1 = (d2 @ W2.T) * d_relu(z1)
            dW1 = xb.T @ d1
            db1 = d1.sum(axis=0)
            for p, g in ((W1, dW1), (b1, db1), (W2, dW2), (b2, db2)):
                p -= lr * g
        if epoch % 15 == 0 or epoch == 59:
            tr = (softmax(relu(Xtr @ W1 + b1) @ W2 + b2).argmax(1) == ytr).mean()
            te = (softmax(relu(Xte @ W1 + b1) @ W2 + b2).argmax(1) == yte).mean()
            curve.append((epoch, tr, te))

    print(f"\n      {'epoch':>7}{'train acc':>12}{'test acc':>11}")
    for e, tr, te in curve:
        print(f"      {e:>7}{tr:>12.4f}{te:>11.4f}")
    final_test = curve[-1][2]
    assert final_test > 0.93, "a 3-layer net should clear 93% on 8x8 digits"

    from sklearn.linear_model import LogisticRegression
    lr_model = LogisticRegression(max_iter=2000).fit(Xtr, ytr)
    baseline = lr_model.score(Xte, yte)
    print(f"\n      {'model':<34}{'test accuracy':>15}")
    print(f"      {'majority class (baseline)':<34}"
          f"{np.bincount(yte).max() / len(yte):>15.4f}")
    print(f"      {'logistic regression':<34}{baseline:>15.4f}")
    print(f"      {'3-layer net, NumPy from scratch':<34}{final_test:>15.4f}")
    print(f"""         written entirely in NumPy -- no framework anywhere -- and
         it works. Quote the BASELINE alongside it, as Course 12 A
         insisted: {final_test:.4f} means something only against
         {baseline:.4f} from a linear model on the same split""")

    # ---- the two derivatives that look too simple to be right ------------
    print("""
      two gradients that look suspiciously simple, and both are exact:
        softmax + cross-entropy  ->  dL/dz = (a - y) / N
        sigmoid + binary CE      ->  dL/dz = (a - y) / N
         the exp in the softmax and the log in the cross-entropy
         CANCEL. That is not a convenience -- it is why this pairing is
         used everywhere, and why pairing softmax with squared error
         instead gives a gradient that vanishes when the model is
         confidently wrong""")

    # ================================================= experiment 3
    print("\n    --- experiment 3: activation functions and their gradients")

    zs = np.array([-6.0, -3.0, -1.0, 0.0, 1.0, 3.0, 6.0])
    print(f"\n      {'z':>6}{'sigmoid':>10}{'d/dz':>9}{'tanh':>9}{'d/dz':>9}"
          f"{'relu':>8}{'d/dz':>7}")
    for z in zs:
        print(f"      {z:>6.1f}{sigmoid(z):>10.4f}{d_sigmoid(z):>9.4f}"
              f"{tanh(z):>9.4f}{d_tanh(z):>9.4f}{relu(z):>8.2f}"
              f"{d_relu(z):>7.1f}")

    print(f"\n      {'function':<14}{'range':<18}{'max grad':>10}"
          f"  {'saturates?'}")
    for name, rng_, mx, sat in (
            ("sigmoid", "(0, 1)", 0.25, "BOTH ends"),
            ("tanh", "(-1, 1)", 1.00, "BOTH ends"),
            ("ReLU", "[0, inf)", 1.00, "at z < 0 only -- and permanently"),
            ("leaky ReLU", "(-inf, inf)", 1.00, "never"),
            ("softmax", "(0,1), sums to 1", 0.25, "yes, like sigmoid")):
        print(f"      {name:<14}{rng_:<18}{mx:>10.2f}  {sat}")

    # ---- the vanishing gradient, measured --------------------------------
    print("\n      the vanishing gradient, computed rather than asserted.")
    print("      Each column multiplies ONE layer's derivative `depth` times.")
    print("      'best case' uses each function's MAXIMUM derivative;")
    print("      'typical' uses a plausible mid-range value.")
    print(f"\n      {'depth':>7}{'sigmoid best':>15}{'sigmoid typ':>14}"
          f"{'tanh best':>12}{'tanh typ':>12}{'ReLU':>10}")
    for depth in (1, 5, 10, 20, 50):
        print(f"      {depth:>7}{0.25 ** depth:>15.2e}{0.10 ** depth:>14.2e}"
              f"{1.0 ** depth:>12.2e}{0.50 ** depth:>12.2e}"
              f"{1.0 ** depth:>10.2e}")
    sig_50 = 0.25 ** 50
    tanh_50 = 0.50 ** 50
    assert sig_50 < 1e-30 and tanh_50 < 1e-14
    print(f"""         BACKPROPAGATION MULTIPLIES the per-layer gradients. The
         sigmoid's largest possible derivative is 0.25, so through 50
         layers the very BEST case is 0.25^50 = {sig_50:.2e} -- and the
         typical case is far worse, because 0.25 occurs only at z = 0.
         That number is why sigmoid activations made deep networks
         untrainable, and why ReLU -- whose derivative is exactly 1
         wherever it is active -- is what made depth possible.
         AND READ THE TANH COLUMNS TOGETHER. Its best case is 1.0, so
         the 'best' column never decays -- but that maximum occurs
         only at z = 0. At a realistic 0.5 per layer, 50 layers give
         {tanh_50:.1e}. Tanh is better than sigmoid and still
         vanishes; only ReLU's exact 1.0 over its whole active range
         survives depth.
         Say '0.25 to the power of the depth' in an exam and you have
         explained the vanishing gradient""")

    # ---- ReLU's own failure ----------------------------------------------
    print("\n      and ReLU's own failure mode:")
    dead = np.array([-5.0, -2.0, -0.1])
    print(f"      for z < 0:  ReLU(z) = {relu(dead).tolist()}, "
          f"d/dz = {d_relu(dead).tolist()}")
    print(f"      leaky ReLU: {np.round(leaky_relu(dead), 3).tolist()}, "
          f"d/dz = {d_leaky_relu(dead).tolist()}")
    assert d_relu(dead).sum() == 0 and d_leaky_relu(dead).sum() > 0
    print("""         A DEAD RELU IS DEAD FOR EVER. Its gradient is exactly
         zero for every negative input, so once a unit's weights push
         it permanently negative, no gradient reaches it again and it
         never recovers.
         Leaky ReLU's 0.01 slope is small enough not to matter and
         non-zero enough to keep the unit alive. That is the entire
         argument for it""")

    # ---- the softmax stability trick -------------------------------------
    print("\n      the softmax stability trick, demonstrated:")
    big = np.array([[1000.0, 1001.0, 1002.0]])
    naive_ok = True
    with np.errstate(over="ignore", invalid="ignore"):
        naive = np.exp(big) / np.exp(big).sum()
        naive_ok = np.isfinite(naive).all()
    stable = softmax(big)
    print(f"      naive  exp(1000)/sum : "
          f"{'overflowed to nan/inf' if not naive_ok else naive.round(4)}")
    print(f"      stable (z - z.max)   : {stable.round(4)}")
    assert not naive_ok and np.isfinite(stable).all()
    print("""         subtracting the row maximum changes NOTHING
         mathematically -- the constant cancels top and bottom -- and
         it is the difference between a working softmax and a nan.
         Every framework does this internally, which is why you should
         pass LOGITS to a loss function rather than probabilities""")

    return final_test


if __name__ == "__main__":
    main()
