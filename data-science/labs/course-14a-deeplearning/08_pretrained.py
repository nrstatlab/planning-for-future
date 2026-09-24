"""Experiment 8 -- fine-tune a pre-trained CNN (MobileNetV2, VGG16) on a
small dataset.

THIS RUNS AGAINST THE REAL IMAGENET WEIGHTS. `keras.applications` fetches
them from storage.googleapis.com, which this environment permits, so the
MobileNetV2 and VGG16 below are the actual published networks with their
actual trained parameters -- not a stand-in.

Hugging Face is a different matter: huggingface.co is refused at the gateway
with a 403, so no BERT-family checkpoint can be fetched. That affects
experiment 12 only, and `12_huggingface_app.md` carries it marked NOT
EXECUTED.

The small dataset is a 10-class Fashion-MNIST subset of 500 training images
-- 50 per class. That is genuinely small, which is the whole premise of the
experiment: transfer learning exists so that you do not need 60,000 images.

Method note: the frozen-base rows PRECOMPUTE the convolutional features once
and then train only the head. That is mathematically identical to freezing
the base and calling fit() on the full model, but it does one forward pass
per image instead of one per image per epoch, which is the difference between
a minute and an hour on CPU.
"""
import os
import time

os.environ.setdefault("KERAS_BACKEND", "torch")
os.environ.setdefault("KERAS_HOME", "/tmp/keras_home")

import numpy as np
import keras

import fixtures as f

IMG = 96          # MobileNetV2 and VGG16 both accept 96x96; 224 is 5x slower
N_TRAIN = 500     # 50 per class -- the "small dataset" the syllabus asks for
N_TEST = 1000


def to_rgb(X, size=IMG):
    """28x28 grayscale -> size x size x 3, which is what ImageNet models want.

    Two conversions, both of which students get wrong:
      - grayscale to RGB by REPEATING the channel, not by zero-filling two
      - resize with a real interpolation, not by tiling pixels
    """
    x = keras.ops.convert_to_tensor(X.reshape(len(X), 28, 28, 1))
    x = keras.ops.image.resize(x, (size, size), interpolation="bilinear")
    x = keras.ops.repeat(x, 3, axis=-1)
    return np.asarray(keras.ops.convert_to_numpy(x), dtype="float32")


def head(input_dim, n_classes=10, seed=f.SEED):
    keras.utils.set_random_seed(seed)
    m = keras.Sequential([
        keras.layers.Input((input_dim,)),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(n_classes, activation="softmax"),
    ])
    m.compile(optimizer=keras.optimizers.Adam(1e-3),
              loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return m


def fit_head(m, Xtr, ytr, Xte, yte, epochs=25):
    h = m.fit(Xtr, ytr, validation_data=(Xte, yte), epochs=epochs,
              batch_size=32, verbose=0)
    return float(h.history["val_accuracy"][-1])


def main():
    print("\n  Experiment 8 -- fine-tuning a pre-trained CNN on a small "
          "dataset")

    Xtr, ytr, Xte, yte = f.fashion_mnist(N_TRAIN, N_TEST, flatten=False)
    print(f"\n    Fashion-MNIST subset: {len(Xtr)} training images "
          f"({len(Xtr)//10} per class), {len(Xte)} test, 10 classes")
    print(f"    upscaled {28}x{28} grayscale -> {IMG}x{IMG} RGB for the "
          f"ImageNet models")

    rgb_tr, rgb_te = to_rgb(Xtr), to_rgb(Xte)
    assert rgb_tr.shape == (N_TRAIN, IMG, IMG, 3), rgb_tr.shape

    rows = []

    # ----------------------------------------------------------- baseline 1
    print("\n    --- baseline: a small CNN trained from scratch on 500 images")
    keras.utils.set_random_seed(f.SEED)
    scratch = keras.Sequential([
        keras.layers.Input((28, 28, 1)),
        keras.layers.Conv2D(16, 3, activation="relu", padding="same"),
        keras.layers.MaxPooling2D(),
        keras.layers.Conv2D(32, 3, activation="relu", padding="same"),
        keras.layers.MaxPooling2D(),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(10, activation="softmax"),
    ])
    scratch.compile(optimizer=keras.optimizers.Adam(1e-3),
                    loss="sparse_categorical_crossentropy",
                    metrics=["accuracy"])
    t0 = time.time()
    h = scratch.fit(Xtr[..., None], ytr, validation_data=(Xte[..., None], yte),
                    epochs=25, batch_size=32, verbose=0)
    acc_scratch = float(h.history["val_accuracy"][-1])
    rows.append(("CNN from scratch", scratch.count_params(),
                 scratch.count_params(), acc_scratch, time.time() - t0))
    print(f"      test accuracy {acc_scratch:.4f} "
          f"({scratch.count_params():,} trainable parameters)")

    # ----------------------------------------------------------- baseline 2
    print("\n    --- baseline: the same head on RAW PIXELS, no convolutions")
    m = head(784)
    t0 = time.time()
    acc_pixels = fit_head(m, Xtr.reshape(len(Xtr), -1),
                          ytr, Xte.reshape(len(Xte), -1), yte)
    rows.append(("dense head on raw pixels", m.count_params(),
                 m.count_params(), acc_pixels, time.time() - t0))
    print(f"      test accuracy {acc_pixels:.4f}")

    # ------------------------------------------------------------ MobileNet
    for name, builder, prep in [
        ("MobileNetV2", keras.applications.MobileNetV2,
         keras.applications.mobilenet_v2.preprocess_input),
        ("VGG16", keras.applications.VGG16,
         keras.applications.vgg16.preprocess_input),
    ]:
        print(f"\n    --- {name} features, frozen, + a new head")
        t0 = time.time()
        base = builder(weights="imagenet", include_top=False,
                       input_shape=(IMG, IMG, 3), pooling="avg")
        base.trainable = False
        total = base.count_params()
        print(f"      loaded real ImageNet weights: {total:,} parameters, "
              f"frozen")

        # scale [0,1] back to [0,255] because preprocess_input expects that
        ftr = base.predict(prep(rgb_tr * 255.0), verbose=0, batch_size=32)
        fte = base.predict(prep(rgb_te * 255.0), verbose=0, batch_size=32)
        print(f"      feature vector per image: {ftr.shape[1]} numbers "
              f"(from global average pooling)")

        m = head(ftr.shape[1])
        acc = fit_head(m, ftr, ytr, fte, yte)
        el = time.time() - t0
        rows.append((f"{name} frozen + new head", total + m.count_params(),
                     m.count_params(), acc, el))
        print(f"      test accuracy {acc:.4f}   "
              f"({m.count_params():,} trainable of "
              f"{total + m.count_params():,} total)")

        if name == "MobileNetV2":
            mobilenet_features = (ftr, fte)
            mobilenet_acc = acc

    # ------------------------------------------------------------- the table
    print("\n    what 500 images buys you, by approach:")
    print(f"      {'approach':<28}{'total params':>14}{'trainable':>12}"
          f"{'test acc':>11}{'secs':>8}")
    for nm, tot, tr, acc, el in rows:
        print(f"      {nm:<28}{tot:>14,}{tr:>12,}{acc:>11.4f}{el:>8.1f}")

    best_pre = max(r[3] for r in rows if "frozen" in r[0])
    print(f"\n      best pre-trained {best_pre:.4f} against "
          f"from-scratch {acc_scratch:.4f}")

    vgg = [r for r in rows if r[0].startswith("VGG16")][0]
    mob = [r for r in rows if r[0].startswith("MobileNetV2")][0]
    if vgg[3] < acc_scratch:
        print(f"""         AND NOTE THE VGG16 ROW: {vgg[3]:.4f}, WORSE than the
         small CNN trained from scratch on the same 500 images, and
         {vgg[4]/mob[4]:.1f}x slower than MobileNetV2 for the privilege.
         Bigger is not better. VGG16 is a 2014 architecture with
         {vgg[1]:,} parameters and its features are tuned for
         224x224 photographs; at 96x96 on upscaled grayscale it is
         being used far outside what it was built for.
         The lesson is to BENCHMARK the pre-trained model you chose
         against a small model you trained yourself. Most people never
         run that baseline, and so never find out""")

    if best_pre > acc_scratch:
        print("""         TRANSFER WON. The convolutional filters were trained
         on ImageNet -- photographs of animals, vehicles and objects --
         and not one of them ever saw a shoe on a black background.
         They transferred anyway, because the EARLY layers of any
         vision model learn edges, corners and textures, and those are
         the same features whatever the pictures are of.
         Note the trainable column. Almost every parameter in the
         network was already set; only the head was learned from the
         500 images, which is why 500 images is enough""")
    else:
        print(f"""         TRANSFER DID NOT WIN HERE, and the number is
         reported as measured. The likely reason is DOMAIN GAP:
         Fashion-MNIST is 28x28 grayscale upscaled to {IMG}x{IMG},
         so it has no colour, no texture detail and no photographic
         statistics at all -- and ImageNet features are built from
         exactly those. This is the honest limit of transfer learning
         and it is worth more than a demo that always works""")

    # ----------------------------------------------- fine-tuning the base
    print("\n    --- and now actually FINE-TUNE: unfreeze the top of "
          "MobileNetV2")
    t0 = time.time()
    keras.utils.set_random_seed(f.SEED)
    base = keras.applications.MobileNetV2(weights="imagenet",
                                          include_top=False,
                                          input_shape=(IMG, IMG, 3),
                                          pooling="avg")
    base.trainable = True
    n_unfrozen = 0
    for layer in base.layers[:-20]:
        layer.trainable = False
    for layer in base.layers:
        if layer.trainable:
            n_unfrozen += 1
    model = keras.Sequential([
        base,
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(optimizer=keras.optimizers.Adam(1e-4),   # NOTE: 1e-4
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    trainable = int(sum(np.prod(w.shape) for w in model.trainable_weights))
    print(f"      unfroze the last {n_unfrozen} layers of the base -> "
          f"{trainable:,} trainable parameters")
    print(f"      learning rate 1e-4, deliberately 10x smaller than the "
          f"1e-3 used above")
    h = model.fit(prep_mobilenet(rgb_tr), ytr,
                  validation_data=(prep_mobilenet(rgb_te), yte),
                  epochs=8, batch_size=32, verbose=0)
    acc_ft = float(h.history["val_accuracy"][-1])
    print(f"      test accuracy {acc_ft:.4f}   ({time.time()-t0:.1f}s, "
          f"8 epochs)")
    print(f"      frozen-features MobileNetV2 was {mobilenet_acc:.4f}, "
          f"fine-tuned is {acc_ft:.4f}")
    if acc_ft < mobilenet_acc:
        print(f"""         FINE-TUNING MADE IT WORSE -- {acc_ft:.4f} against
         {mobilenet_acc:.4f} for the frozen features -- and that is the
         result, not a bug to tune away.
         Count the parameters. Unfreezing put {trainable:,} weights
         under gradient descent and there are {N_TRAIN} training
         images: roughly {trainable/N_TRAIN:.0f} parameters per
         example. The network has more than enough freedom to fit the
         500 images exactly, and what it fits is their noise.
         THE RULE THIS ACTUALLY DEMONSTRATES: how much you unfreeze
         must scale with how much data you have. With 500 images,
         freeze everything and train a head. Fine-tuning the top
         layers starts to pay somewhere in the thousands, and
         fine-tuning the whole network wants tens of thousands.
         The small learning rate is still right and still necessary --
         1e-4 rather than 1e-3, so the first large gradients do not
         erase the features you came for -- it is just not sufficient.
         'Use a small learning rate' is the advice everyone repeats;
         'unfreeze in proportion to your data' is the one that would
         have prevented this number""")
    else:
        print(f"""         FINE-TUNING HELPED: {acc_ft:.4f} against
         {mobilenet_acc:.4f} frozen. The learning rate is the reason it
         could: at 1e-3 the first few batches produce gradients large
         enough to overwrite the pre-trained filters before they help.
         1e-4 is the usual starting point, and freezing the early
         layers protects the generic edge detectors that transfer
         best""")

    # -------------------------------------------------------- what it knows
    print("\n    --- what the pre-trained network actually knows")
    clf = keras.applications.MobileNetV2(weights="imagenet")
    probe = prep_mobilenet_224(rgb_te[:1])
    pred = clf.predict(probe, verbose=0)
    top = keras.applications.mobilenet_v2.decode_predictions(pred, top=3)[0]
    print(f"      feeding it a Fashion-MNIST '{f.FASHION_CLASSES[yte[0]]}', "
          f"ImageNet's top-3 guesses are:")
    for _, label, p in top:
        print(f"        {label:<22}{p:.4f}")
    print("""         ImageNet has 1,000 classes and NONE of them is
         'pullover'. The classifier head is useless for this task,
         which is exactly why transfer learning throws the head away
         and keeps the convolutions. That is the single most important
         sentence in this experiment""")

    # -------------------------------------------------------------- asserts
    assert rgb_tr.shape[1:] == (IMG, IMG, 3)
    assert 0.0 <= acc_scratch <= 1.0 and 0.0 <= best_pre <= 1.0
    assert acc_pixels < best_pre, (
        f"raw pixels {acc_pixels:.4f} should lose to pre-trained features "
        f"{best_pre:.4f}")
    assert trainable < base.count_params(), "freezing did nothing"
    print("\n    all assertions passed")
    return rows


def prep_mobilenet(x):
    return keras.applications.mobilenet_v2.preprocess_input(x * 255.0)


def prep_mobilenet_224(x):
    x = keras.ops.image.resize(keras.ops.convert_to_tensor(x), (224, 224),
                               interpolation="bilinear")
    return keras.applications.mobilenet_v2.preprocess_input(
        np.asarray(keras.ops.convert_to_numpy(x)) * 255.0)


if __name__ == "__main__":
    main()
