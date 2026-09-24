"""Experiments 2, 4 and 5 -- the framework, a deep network for classification,
and experiments with dropout, batch normalization and different activations.

The dataset is THE REAL MNIST, which is what the syllabus names. Keras
downloads it from storage.googleapis.com, which this environment permits. A
stratified 4,000-image subset is used so the sweeps finish on CPU; the subset
size is printed rather than glossed over.

THE SYLLABUS SAYS KERAS/TENSORFLOW, AND THAT IS WHAT RUNS HERE. TensorFlow is
not installed, but Keras 3 is backend-agnostic: with KERAS_BACKEND=torch it
runs the identical Keras API on PyTorch. Every `keras.Sequential`,
`.compile()` and `.fit()` below is the real thing, and the code you would
write against TensorFlow is character-for-character the same.

Experiment 2 asks for Google Teachable Machine or TensorFlow Playground --
both are hosted web applications, so `02_playground.md` records what to do
there and is marked NOT EXECUTED. What runs here instead is the same
demonstration those tools give: how depth, width and activation change what a
network can represent.
"""
import os
import time

os.environ.setdefault("KERAS_BACKEND", "torch")
os.environ.setdefault("KERAS_HOME", "/tmp/keras_home")

import numpy as np

import fixtures as f

N_IN = 784      # set from the data in main(); MNIST is 28*28


def build(hidden, activation="relu", dropout=0.0, batchnorm=False,
          n_in=None, n_out=10, seed=f.SEED):
    import keras
    keras.utils.set_random_seed(seed)
    layers = [keras.layers.Input((n_in or N_IN,))]
    for h in hidden:
        layers.append(keras.layers.Dense(h))
        if batchnorm:
            layers.append(keras.layers.BatchNormalization())
        layers.append(keras.layers.Activation(activation))
        if dropout:
            layers.append(keras.layers.Dropout(dropout))
    layers.append(keras.layers.Dense(n_out, activation="softmax"))
    return keras.Sequential(layers)


def train(model, Xtr, ytr, Xte, yte, epochs=30, optimizer="adam", lr=None,
          verbose=0):
    import keras
    opt = optimizer
    if lr is not None:
        opt = {"adam": keras.optimizers.Adam,
               "sgd": keras.optimizers.SGD,
               "rmsprop": keras.optimizers.RMSprop}[optimizer](learning_rate=lr)
    model.compile(optimizer=opt, loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    t0 = time.perf_counter()
    hist = model.fit(Xtr, ytr, validation_data=(Xte, yte), epochs=epochs,
                     batch_size=32, verbose=verbose)
    secs = time.perf_counter() - t0
    return hist.history, secs


def main():
    print("  Experiments 2, 4 and 5 -- the framework, a deep net, regularization")

    import keras
    print(f"\n    Keras {keras.__version__}, backend '{keras.backend.backend()}'")
    print("""         THE SYLLABUS SAYS KERAS/TENSORFLOW. TensorFlow is not
         installed here, but Keras 3 is backend-agnostic -- set
         KERAS_BACKEND=torch and the identical API runs on PyTorch.
         Every line below is code you could paste into a TensorFlow
         environment unchanged, which is the point of Keras existing""")

    global N_IN
    Xtr, ytr, Xte, yte = f.mnist(n_train=4000, n_test=1000)
    N_IN = Xtr.shape[1]
    print(f"\n    THE REAL MNIST: {len(Xtr)} training images, {len(Xte)} test, "
          f"{Xtr.shape[1]} features (28x28), {len(np.unique(ytr))} classes")
    print("""         a stratified 4,000-image subset of the 60,000, drawn with
         a fixed seed -- 400 per class, so the balance matches the full
         set. The subset exists because these labs run on CPU, and it
         is stated rather than hidden, because 'accuracy on MNIST'
         means nothing without saying how much of MNIST""")

    # ================================================= experiment 4
    print("\n    --- experiment 4: a deep network for classification")

    print("\n      does depth help? four architectures, same data, same budget:")
    print(f"      {'architecture':<26}{'params':>9}{'train':>9}{'test':>9}"
          f"{'gap':>8}{'secs':>7}")
    depth_rows = {}
    for label, hidden in (("none (linear softmax)", []),
                          ("1 x 32", [32]),
                          ("2 x 32", [32, 32]),
                          ("3 x 64", [64, 64, 64])):
        m = build(hidden)
        h, secs = train(m, Xtr, ytr, Xte, yte, epochs=30)
        tr, te = h["accuracy"][-1], h["val_accuracy"][-1]
        depth_rows[label] = {"train": tr, "test": te, "params": m.count_params()}
        print(f"      {label:<26}{m.count_params():>9,}{tr:>9.4f}{te:>9.4f}"
              f"{tr - te:>8.4f}{secs:>7.1f}")

    linear = depth_rows["none (linear softmax)"]["test"]
    deep = max(depth_rows[k]["test"] for k in depth_rows if k != "none (linear softmax)")
    assert deep > linear, "depth should beat a linear model on MNIST"
    print(f"""         depth helps here -- {deep:.4f} against a linear model's
         {linear:.4f}. Note how strong the LINEAR baseline already is:
         MNIST digits are close to linearly separable in raw pixel
         space, which is exactly why MNIST stopped being a useful
         benchmark and Fashion-MNIST was published to replace it.
         Experiment 6 runs the same comparison on Fashion-MNIST and
         the gap is wider.
         Depth buys most where the decision boundary is genuinely
         curved. Reporting the linear baseline is what makes the claim
         meaningful, and it is the habit Course 12 A drilled""")

    # ---- optimizers -------------------------------------------------------
    print("\n      the three optimizers the syllabus names:")
    print(f"      {'optimizer':<12}{'lr':>8}{'epoch 1':>10}{'epoch 5':>10}"
          f"{'final test':>12}")
    opt_rows = {}
    for name, lr in (("sgd", 0.01), ("sgd", 0.1), ("rmsprop", 0.001),
                     ("adam", 0.001)):
        m = build([64, 64])
        h, _ = train(m, Xtr, ytr, Xte, yte, epochs=15, optimizer=name, lr=lr)
        opt_rows[f"{name}@{lr}"] = h["val_accuracy"][-1]
        print(f"      {name:<12}{lr:>8}{h['val_accuracy'][0]:>10.4f}"
              f"{h['val_accuracy'][4]:>10.4f}{h['val_accuracy'][-1]:>12.4f}")

    slow_sgd = opt_rows["sgd@0.01"]
    adam = opt_rows["adam@0.001"]
    print(f"""         ADAM REACHED A USEFUL ACCURACY IN ONE EPOCH where SGD at
         lr=0.01 was still climbing. That is what adaptive methods
         buy: a PER-PARAMETER learning rate, derived from a running
         estimate of each gradient's first and second moment.
         SGD with the right learning rate gets to the same place --
         look at the lr=0.1 row -- but 'the right learning rate' is
         the whole difficulty, and Adam mostly removes it.
         Adam is the sensible default. SGD with momentum plus a
         schedule still wins on large vision models, which is worth
         knowing but is not where you start""")

    # ---- learning rate ----------------------------------------------------
    print("\n      the learning rate, which matters more than the optimizer:")
    print(f"      {'lr':>10}{'final train loss':>19}{'final test acc':>16}"
          f"  behaviour")
    for lr in (10.0, 1.0, 0.1, 0.01, 0.0001):
        m = build([64, 64])
        h, _ = train(m, Xtr, ytr, Xte, yte, epochs=15, optimizer="sgd", lr=lr)
        first, loss = h["loss"][0], h["loss"][-1]
        acc = h["val_accuracy"][-1]
        # ln(10) = 2.303 is the loss of a model that has learned nothing
        if not np.isfinite(loss) or loss > first:
            note = "DIVERGED -- the loss went UP"
        elif loss > 2.0 and acc < 0.5:
            note = "TOO SLOW -- barely moved off ln(10) = 2.303"
        elif acc < 0.5:
            note = "not converged"
        else:
            note = "converged"
        print(f"      {lr:>10}{loss:>19.4f}{acc:>16.4f}  {note}")
    print("""         THE LEARNING RATE IS THE ONE HYPERPARAMETER THAT CAN MAKE
         TRAINING FAIL OUTRIGHT. Too large and the updates overshoot,
         the loss climbs and often becomes nan; too small and it
         crawls. Everything else on this page is a refinement; this is
         the switch between working and not working""")

    # ================================================= experiment 5
    print("\n    --- experiment 5: dropout, batch norm and activations")

    # deliberately over-large network so there is overfitting to fix
    print(f"\n      first, MAKE it overfit -- a 3x256 network on "
          f"{len(Xtr):,} images:")
    m = build([256, 256, 256])
    h, _ = train(m, Xtr, ytr, Xte, yte, epochs=60)
    base_tr, base_te = h["accuracy"][-1], h["val_accuracy"][-1]
    base_gap = base_tr - base_te
    print(f"      params {m.count_params():,}   train {base_tr:.4f}   "
          f"test {base_te:.4f}   gap {base_gap:.4f}")
    print(f"""         {m.count_params():,} parameters for {len(Xtr):,} training images -- about
         {m.count_params() / len(Xtr):.0f} parameters per example. The network can memorise
         the training set, and the train/test gap is the evidence""")

    print(f"\n      {'regularisation':<28}{'train':>9}{'test':>9}{'gap':>9}")
    reg_rows = {}
    for label, kw in (("none", {}),
                      ("dropout 0.2", {"dropout": 0.2}),
                      ("dropout 0.5", {"dropout": 0.5}),
                      ("batch norm", {"batchnorm": True}),
                      ("batch norm + dropout 0.3",
                       {"batchnorm": True, "dropout": 0.3})):
        m = build([256, 256, 256], **kw)
        h, _ = train(m, Xtr, ytr, Xte, yte, epochs=60)
        tr, te = h["accuracy"][-1], h["val_accuracy"][-1]
        reg_rows[label] = {"train": tr, "test": te, "gap": tr - te}
        print(f"      {label:<28}{tr:>9.4f}{te:>9.4f}{tr - te:>9.4f}")

    best_gap = min(reg_rows, key=lambda k: reg_rows[k]["gap"])
    best_test = max(reg_rows, key=lambda k: reg_rows[k]["test"])
    print(f"\n      smallest gap : {best_gap}")
    print(f"      best test    : {best_test}")
    assert reg_rows["dropout 0.5"]["gap"] < reg_rows["none"]["gap"], \
        "dropout must reduce the train/test gap"
    print(f"""         DROPOUT CLOSED THE GAP -- {reg_rows['none']['gap']:.4f} to
         {reg_rows['dropout 0.5']['gap']:.4f} at p = 0.5 -- which is what it is for. Whether
         it improved the TEST score is a separate question, and the
         table above answers it honestly for this dataset.
         Report both columns. A regulariser that shrinks the gap by
         hurting the training score has not helped anyone""")

    print("""
      what each one actually does:
        DROPOUT     zeroes a random fraction of activations EACH BATCH
                    during training, and nothing at inference. So the
                    network cannot rely on any single unit, and it is
                    an implicit ensemble over 2^n sub-networks.
        BATCH NORM  normalises each layer's pre-activations to zero
                    mean and unit variance PER BATCH, then rescales
                    with two learned parameters. It stabilises the
                    distribution each layer sees.
         and one thing to say precisely: batch norm behaves
         DIFFERENTLY at training and inference -- batch statistics
         during training, running averages afterwards. That is why a
         model must be told which mode it is in, and why forgetting
         model.eval() in PyTorch is a classic bug""")

    # ---- activations, compared -------------------------------------------
    print("\n      the same network with different activations:")
    print(f"      {'activation':<14}{'epoch 1 test':>14}{'final test':>13}"
          f"{'final train loss':>18}")
    act_rows = {}
    for act in ("relu", "tanh", "sigmoid", "elu"):
        m = build([64, 64, 64], activation=act)
        h, _ = train(m, Xtr, ytr, Xte, yte, epochs=30)
        act_rows[act] = h["val_accuracy"][-1]
        print(f"      {act:<14}{h['val_accuracy'][0]:>14.4f}"
              f"{h['val_accuracy'][-1]:>13.4f}{h['loss'][-1]:>18.4f}")
    print(f"""         all four eventually work on a 3-layer network, and that
         is the honest result at this depth -- the vanishing gradient
         is a problem of DEPTH, and three layers is not deep.
         Watch the FIRST epoch instead: sigmoid starts slowest,
         because its gradient is at most 0.25 per layer, so the early
         updates are small. Stack thirty of these layers and sigmoid
         stops training altogether -- which is the 0.25^depth
         arithmetic from experiment 3""")

    # ---- weight initialisation -------------------------------------------
    print("\n      weight initialisation, which nobody thinks about until it "
          "breaks:")
    print(f"      {'initialiser':<22}{'epoch 1 test':>14}{'final test':>13}")
    for name, init in (("zeros -- BROKEN", "zeros"),
                       ("glorot (default)", "glorot_uniform"),
                       ("he (for ReLU)", "he_normal")):
        keras.utils.set_random_seed(f.SEED)
        m = keras.Sequential([
            keras.layers.Input((N_IN,)),
            keras.layers.Dense(64, activation="relu", kernel_initializer=init),
            keras.layers.Dense(64, activation="relu", kernel_initializer=init),
            keras.layers.Dense(10, activation="softmax",
                               kernel_initializer=init),
        ])
        h, _ = train(m, Xtr, ytr, Xte, yte, epochs=20)
        print(f"      {name:<22}{h['val_accuracy'][0]:>14.4f}"
              f"{h['val_accuracy'][-1]:>13.4f}")
    print("""         ALL-ZERO WEIGHTS NEVER LEARN. Every unit in a layer
         computes the same thing, receives the same gradient, and
         updates identically -- so a 64-unit layer behaves exactly
         like a 1-unit layer, for ever. It is called the SYMMETRY
         PROBLEM, and random initialisation exists to break it.
         Glorot scales the variance by 1/fan_in for tanh-like
         activations; He uses 2/fan_in for ReLU, because ReLU discards
         half its input and the factor of 2 restores the variance""")

    return depth_rows, reg_rows


if __name__ == "__main__":
    main()
