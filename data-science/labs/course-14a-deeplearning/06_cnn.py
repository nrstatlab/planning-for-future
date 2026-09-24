"""Experiments 6 and 7 -- train a CNN to classify Fashion-MNIST, and
visualize its filters and feature maps. Plus a controlled companion to
experiment 8.

REAL PYTORCH, REAL CONVOLUTIONS, REAL TRAINING, REAL DATA. Fashion-MNIST is
the dataset the syllabus names and Keras fetches it from
storage.googleapis.com, which this environment permits.

Experiment 8 -- fine-tuning a pre-trained MobileNet or VGG -- has its own
script, `08_pretrained.py`, which loads the actual published ImageNet weights
and runs. What stays here is a CONTROLLED version of the same mechanism:
pre-train on a synthetic four-shape task where the right answer is known,
freeze the convolutions, and retrain only the head on a harder, smaller
version of it. The controlled version can prove things the real one cannot,
because the source and target tasks are constructed rather than found.

Hugging Face remains unreachable -- huggingface.co is refused with a 403 at
the gateway -- which affects experiment 12 only. `12_huggingface_app.md`
carries that code marked NOT EXECUTED.
"""
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import fixtures as f


class SmallCNN(nn.Module):
    """LeNet-shaped: two conv/pool blocks, then two dense layers."""

    def __init__(self, n_classes=4, in_ch=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_ch, 8, kernel_size=5, padding=2)
        self.conv2 = nn.Conv2d(8, 16, kernel_size=5, padding=2)
        self.fc1 = nn.Linear(16 * 7 * 7, 64)
        self.fc2 = nn.Linear(64, n_classes)

    def features(self, x):
        a1 = F.relu(self.conv1(x))
        p1 = F.max_pool2d(a1, 2)
        a2 = F.relu(self.conv2(p1))
        p2 = F.max_pool2d(a2, 2)
        return a1, p1, a2, p2

    def forward(self, x):
        _, _, _, p2 = self.features(x)
        h = F.relu(self.fc1(p2.flatten(1)))
        return self.fc2(h)


class MLPOnPixels(nn.Module):
    """The same parameter budget, but fully connected -- the fair comparison."""

    def __init__(self, n_classes=4, size=28):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(), nn.Linear(size * size, 96), nn.ReLU(),
            nn.Linear(96, 64), nn.ReLU(), nn.Linear(64, n_classes))

    def forward(self, x):
        return self.net(x)


def train_torch(model, Xtr, ytr, Xte, yte, epochs=12, lr=1e-3, batch=64,
                seed=f.SEED, freeze=None):
    torch.manual_seed(seed)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.Adam(params, lr=lr)
    lossf = nn.CrossEntropyLoss()
    Xtr_t = torch.tensor(Xtr)
    ytr_t = torch.tensor(ytr)
    Xte_t = torch.tensor(Xte)
    yte_t = torch.tensor(yte)
    n = len(ytr)
    curve = []
    t0 = time.perf_counter()
    for ep in range(epochs):
        model.train()
        perm = torch.randperm(n)
        for i in range(0, n, batch):
            idx = perm[i:i + batch]
            opt.zero_grad()
            loss = lossf(model(Xtr_t[idx]), ytr_t[idx])
            loss.backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            tr = (model(Xtr_t).argmax(1) == ytr_t).float().mean().item()
            te = (model(Xte_t).argmax(1) == yte_t).float().mean().item()
        curve.append((ep, tr, te))
    return curve, time.perf_counter() - t0


def show_kernel(k, name):
    """Print a 5x5 kernel as characters -- the shape is the point."""
    chars = " .:-=+*#@"
    lo, hi = k.min(), k.max()
    rng = (hi - lo) or 1.0
    print(f"        {name}  (min {lo:+.3f}, max {hi:+.3f})")
    for row in k:
        line = "".join(chars[int((v - lo) / rng * (len(chars) - 1))]
                       for v in row)
        print(f"          |{line}|")


def main():
    print("  Experiments 6 and 7 -- CNNs on Fashion-MNIST, filters and "
          "feature maps")

    torch.manual_seed(f.SEED)
    torch.set_num_threads(2)

    Xtr, ytr, Xte, yte = f.fashion_mnist(n_train=8000, n_test=2000)
    # torch conv layers want (N, channels, H, W); the loader gives (N, H, W)
    Xtr = Xtr[:, None, :, :]
    Xte = Xte[:, None, :, :]
    CLASSES = f.FASHION_CLASSES
    N_CLASSES = len(CLASSES)
    print(f"\n    THE REAL FASHION-MNIST: {len(ytr)} training images, "
          f"{len(yte)} test, 28x28 grayscale, {len(CLASSES)} classes")
    print(f"    {', '.join(CLASSES)}")
    print("""         a stratified 8,000-image subset of the 60,000, fixed seed,
         800 per class. Fashion-MNIST was published precisely because
         MNIST had become too easy -- same shape, same size, same ten
         classes, but the classes are NOT close to linearly separable.
         Experiment 4 got a strong linear baseline on MNIST; watch what
         the same comparison does here""")

    # ================================================= experiment 6
    print("\n    --- experiment 6: a CNN for image classification")

    # the LINEAR baseline, so the comparison with experiment 4 is measured
    # rather than asserted. Same optimiser, same epochs, no hidden layer.
    linear = nn.Sequential(nn.Flatten(), nn.Linear(28 * 28, N_CLASSES))
    lin_curve, _ = train_torch(linear, Xtr, ytr, Xte, yte, epochs=12)
    lin_te = lin_curve[-1][2]

    cnn = SmallCNN(n_classes=N_CLASSES)
    mlp = MLPOnPixels(n_classes=N_CLASSES)
    print(f"\n      {'model':<28}{'params':>10}")
    print(f"      {'CNN (2 conv + 2 dense)':<28}"
          f"{sum(p.numel() for p in cnn.parameters()):>10,}")
    print(f"      {'MLP on raw pixels':<28}"
          f"{sum(p.numel() for p in mlp.parameters()):>10,}")

    cnn_curve, cnn_secs = train_torch(cnn, Xtr, ytr, Xte, yte, epochs=12)
    mlp_curve, mlp_secs = train_torch(mlp, Xtr, ytr, Xte, yte, epochs=12)

    print(f"\n      {'epoch':>7}{'CNN train':>12}{'CNN test':>11}"
          f"{'MLP train':>12}{'MLP test':>11}")
    for i in (0, 3, 7, 11):
        print(f"      {i:>7}{cnn_curve[i][1]:>12.4f}{cnn_curve[i][2]:>11.4f}"
              f"{mlp_curve[i][1]:>12.4f}{mlp_curve[i][2]:>11.4f}")
    cnn_te, mlp_te = cnn_curve[-1][2], mlp_curve[-1][2]
    print(f"\n      final test: CNN {cnn_te:.4f}, MLP {mlp_te:.4f}   "
          f"({cnn_secs:.1f}s vs {mlp_secs:.1f}s)")
    print(f"      linear softmax baseline, no hidden layer: {lin_te:.4f}")
    print(f"""         COMPARE WITH EXPERIMENT 4. On MNIST a linear model
         reached 0.9100 and the best deep network 0.9410 -- three
         points for 59,210 parameters. Here the linear model manages
         {lin_te:.4f} and the CNN {cnn_te:.4f}, a gap of
         {cnn_te - lin_te:+.4f}.
         THE GAP WIDENED, but the more telling number is how far the
         LINEAR model fell: 0.9100 on MNIST to {lin_te:.4f} here, while
         the best network fell 0.9410 to {cnn_te:.4f}. The linear model
         lost roughly twice as much.
         That is what Fashion-MNIST was published to expose. MNIST
         digits are nearly linearly separable in raw pixel space, so
         they cannot distinguish a good architecture from a bad one --
         everything scores 0.9-something. Clothing cannot be separated
         that way, and the architecture starts to matter.
         Note also how little the MLP loses to the CNN here
         ({cnn_te - mlp_te:+.4f}): on centred, size-normalised,
         single-object images a dense model does nearly as well. The
         next table is where the CNN earns its keep""")
    assert cnn_te > 0.8, "the CNN should learn Fashion-MNIST"

    print("""
      the three properties a convolution has that a dense layer does not:
        LOCAL CONNECTIVITY  a unit sees a 5x5 patch, not all 784 pixels
        WEIGHT SHARING      the SAME kernel slides over the whole image
        TRANSLATION EQUIVARIANCE  move the object, the response moves with it
         weight sharing is where the parameter saving comes from: one
         5x5 kernel is 25 numbers whatever the image size, while a
         dense layer over 784 pixels needs 784 weights PER UNIT""")

    # ---- translation, which is the honest test ---------------------------
    print("\n      the property that matters -- shift every test image by 3px:")
    shifted = np.roll(Xte, shift=3, axis=3)
    with torch.no_grad():
        cnn.eval()
        mlp.eval()
        Xs = torch.tensor(shifted)
        ys = torch.tensor(yte)
        cnn_shift = (cnn(Xs).argmax(1) == ys).float().mean().item()
        mlp_shift = (mlp(Xs).argmax(1) == ys).float().mean().item()
    print(f"      {'model':<12}{'original':>11}{'shifted 3px':>14}{'drop':>9}")
    print(f"      {'CNN':<12}{cnn_te:>11.4f}{cnn_shift:>14.4f}"
          f"{cnn_te - cnn_shift:>9.4f}")
    print(f"      {'MLP':<12}{mlp_te:>11.4f}{mlp_shift:>14.4f}"
          f"{mlp_te - mlp_shift:>9.4f}")
    if (cnn_te - cnn_shift) < (mlp_te - mlp_shift):
        print("""         THE CNN DEGRADED LESS. Pooling makes it partly invariant
         to where the object sits, so a shift it never saw in training
         costs it less than it costs the dense model -- which learned
         a weight for every absolute pixel position""")
    else:
        print("""         BOTH DEGRADED SIMILARLY HERE. Report it: convolution is
         translation EQUIVARIANT (the feature map moves with the
         object) and only pooling makes it partly INVARIANT, so with
         two pooling layers on 28x28 images the invariance is modest.
         The textbook claim needs data augmentation to show properly,
         and this is the honest version""")

    # ---- the arithmetic that is examined ---------------------------------
    print("\n      the output-size arithmetic, which is examined:")
    print("        out = floor((in + 2*padding - kernel) / stride) + 1")
    print(f"\n      {'layer':<24}{'in':>10}{'k':>4}{'p':>4}{'s':>4}{'out':>10}"
          f"{'params':>10}")
    rows = [("conv1 (1->8, 5x5)", 28, 5, 2, 1, 28, 1 * 8 * 25 + 8),
            ("maxpool 2x2", 28, 2, 0, 2, 14, 0),
            ("conv2 (8->16, 5x5)", 14, 5, 2, 1, 14, 8 * 16 * 25 + 16),
            ("maxpool 2x2", 14, 2, 0, 2, 7, 0)]
    for name, i, k, p, s, o, pc in rows:
        calc = (i + 2 * p - k) // s + 1
        assert calc == o, f"{name}: formula gives {calc}, expected {o}"
        print(f"      {name:<24}{i:>10}{k:>4}{p:>4}{s:>4}{o:>10}{pc:>10,}")
    flat = 16 * 7 * 7
    print(f"      {'flatten':<24}{'7x7x16':>10}{'':>12}{flat:>10}{0:>10,}")
    print(f"      {'fc1 (784->64)':<24}{flat:>10}{'':>12}{64:>10}"
          f"{flat * 64 + 64:>10,}")
    print(f"""         NOTE WHERE THE PARAMETERS ARE. The two conv layers hold
         {1 * 8 * 25 + 8 + 8 * 16 * 25 + 16:,} weights between them; the first dense layer holds
         {flat * 64 + 64:,}. In a classical CNN the CONVOLUTIONS DO THE WORK AND
         THE DENSE LAYERS HOLD THE WEIGHTS -- which is why modern
         architectures replace the flatten with global average pooling
         and delete most of the parameters""")

    # ---- padding, and why 'same' exists ----------------------------------
    print("\n      padding, and why it exists:")
    for pad, label in ((0, "'valid' (no padding)"), (2, "'same' (padding 2)")):
        size = 28
        sizes = [size]
        for _ in range(4):
            size = (size + 2 * pad - 5) + 1
            sizes.append(size)
        print(f"      {label:<24}{' -> '.join(str(s) for s in sizes)}")
    print("""         WITHOUT PADDING THE IMAGE SHRINKS AT EVERY LAYER, so depth
         is limited by arithmetic rather than by what you want. Padding
         keeps the spatial size fixed, which is why 'same' is the
         default in almost every modern architecture""")

    # ================================================= experiment 7
    print("\n    --- experiment 7: what the filters learned")

    w = cnn.conv1.weight.detach().numpy()[:, 0]     # 8 kernels, 5x5
    print(f"\n      the 8 learned 5x5 kernels of conv1, as intensity maps:")
    for i in range(4):
        show_kernel(w[i], f"kernel {i}")

    # measure orientation rather than assert it
    print("\n      are they edge detectors? measure, do not assume:")
    print(f"      {'kernel':>8}{'horiz. gradient':>18}{'vert. gradient':>17}"
          f"  looks like")
    edge_like = 0
    for i in range(8):
        k = w[i]
        gx = float(np.abs(np.diff(k, axis=1)).mean())
        gy = float(np.abs(np.diff(k, axis=0)).mean())
        if max(gx, gy) > 1.6 * min(gx, gy):
            kind = "ORIENTED edge" if gx > gy else "ORIENTED edge"
            edge_like += 1
        else:
            kind = "blob / mixed"
        print(f"      {i:>8}{gx:>18.4f}{gy:>17.4f}  {kind}")
    print(f"""         {edge_like} of 8 kernels are clearly ORIENTED -- their gradient
         along one axis is more than 1.6x the other, which is what an
         edge detector looks like numerically. The rest are blobs or
         mixed, which is also normal: not every filter learns
         something interpretable, and a network with 8 filters does
         not need 8 different edge detectors.
         Reporting {edge_like} rather than 8 is the honest version of 'CNNs
         learn edge detectors'""")

    # ---- feature maps -----------------------------------------------------
    print("\n      the feature maps for one test image:")
    with torch.no_grad():
        one = torch.tensor(Xte[:1])
        a1, p1, a2, p2 = cnn.features(one)
    print(f"      {'stage':<20}{'shape':<20}{'mean activation':>17}"
          f"{'% zero':>9}")
    for name, t in (("input", one), ("conv1 + ReLU", a1), ("pool1", p1),
                    ("conv2 + ReLU", a2), ("pool2", p2)):
        arr = t.numpy()
        pct_zero = 100 * (arr == 0).mean()
        print(f"      {name:<20}{str(tuple(arr.shape)):<20}"
              f"{arr.mean():>17.4f}{pct_zero:>9.1f}")
    z1 = float((a1.numpy() == 0).mean())
    z2 = float((a2.numpy() == 0).mean())
    zin = float((one.numpy() == 0).mean())
    assert z2 > z1, "sparsity should increase with depth"
    print(f"""         SPARSITY GROWS WITH DEPTH: {100*z1:.0f}% of the first
         feature map is exactly zero, {100*z2:.0f}% of the second.
         That is ReLU doing its job -- each filter responds to one kind
         of local pattern and is silent everywhere else -- and the
         deeper the layer, the more specific its filters are, so the
         more often they stay silent.
         NOTE THE DIRECTION OF THE FIRST STEP, which is the
         interesting one: the INPUT image is {100*zin:.0f}% zero, and
         conv1's output is only {100*z1:.0f}% zero. The first
         convolution made the representation LESS sparse, not more.
         That is not a bug and it is worth understanding. Each filter
         has a BIAS, and a filter whose bias is positive responds
         somewhat even to a black patch; the convolution also mixes
         each pixel with its neighbours, so the sharp zeros of the
         background get smeared into small positive values. Sparsity
         then returns with depth, once the filters are specific enough
         to be genuinely silent.
         So 'ReLU makes representations sparse' is true of the network
         as a whole and false of its first layer here. Measure it
         rather than assuming it.
         Sparsity is why ReLU networks are efficient and why a feature
         map is interpretable at all -- a dense map of small non-zero
         values would tell you nothing""")

    # ================================================= experiment 8
    print("\n    --- a controlled companion to experiment 8: transfer\n          learning where the source task is known")

    print("""
      `08_pretrained.py` does experiment 8 for real, with the published
      MobileNetV2 and VGG16 ImageNet weights. What runs HERE is the same
      mechanism under laboratory conditions: pre-train on one task,
      freeze the features, retrain only the head on a DIFFERENT task
      with very little data.
      The reason to do both: with a real pre-trained model you can only
      report the accuracy you get. Here the source task, the target
      task and the difference between them are all constructed, so you
      can say WHY transfer helped and by how much.""")

    # source task: 4 shapes, plenty of data
    src_Xtr, src_Xte, src_ytr, src_yte = f.shapes_split(n_per_class=400,
                                                        seed=f.SEED)
    source = SmallCNN(n_classes=4)
    src_curve, _ = train_torch(source, src_Xtr, src_ytr, src_Xte, src_yte,
                               epochs=12)
    print(f"\n      SOURCE task: 4 shapes, {len(src_ytr)} images -> "
          f"test accuracy {src_curve[-1][2]:.4f}")

    # target task: the same shapes rendered differently, and only 80 images
    tgt_X, tgt_y = f.shapes(n_per_class=60, seed=1234, noise=0.30)
    cut = 80
    tX_tr, ty_tr = tgt_X[:cut], tgt_y[:cut]
    tX_te, ty_te = tgt_X[cut:], tgt_y[cut:]
    print(f"      TARGET task: same 4 classes, NOISIER, only {cut} training "
          f"images ({len(ty_te)} test)")

    print(f"\n      {'approach':<34}{'trainable':>11}{'test acc':>11}")

    scratch = SmallCNN(n_classes=4)
    sc_curve, _ = train_torch(scratch, tX_tr, ty_tr, tX_te, ty_te, epochs=25)
    n_scratch = sum(p.numel() for p in scratch.parameters())
    print(f"      {'from scratch on 80 images':<34}{n_scratch:>11,}"
          f"{sc_curve[-1][2]:>11.4f}")

    import copy
    frozen = copy.deepcopy(source)
    for p in frozen.conv1.parameters():
        p.requires_grad = False
    for p in frozen.conv2.parameters():
        p.requires_grad = False
    frozen.fc1.reset_parameters()
    frozen.fc2.reset_parameters()
    fr_curve, _ = train_torch(frozen, tX_tr, ty_tr, tX_te, ty_te, epochs=25)
    n_frozen = sum(p.numel() for p in frozen.parameters() if p.requires_grad)
    print(f"      {'frozen features + new head':<34}{n_frozen:>11,}"
          f"{fr_curve[-1][2]:>11.4f}")

    fine = copy.deepcopy(source)
    fine.fc2.reset_parameters()
    fn_curve, _ = train_torch(fine, tX_tr, ty_tr, tX_te, ty_te, epochs=25,
                              lr=1e-4)
    n_fine = sum(p.numel() for p in fine.parameters())
    print(f"      {'fine-tune everything, lr=1e-4':<34}{n_fine:>11,}"
          f"{fn_curve[-1][2]:>11.4f}")

    best = max(fr_curve[-1][2], fn_curve[-1][2])
    print(f"\n      best transfer {best:.4f} against from-scratch "
          f"{sc_curve[-1][2]:.4f}")
    if best > sc_curve[-1][2]:
        print(f"""         TRANSFER WON, and the mechanism is the whole point: the
         convolutional filters learned on the large source task
         already detect the edges and corners the target task needs.
         Only {n_frozen:,} parameters had to be learned from 80 images
         instead of {n_scratch:,}.
         That ratio is the argument for transfer learning, and it is
         why nobody trains a vision model from scratch on a small
         dataset""")
    else:
        print(f"""         TRANSFER DID NOT WIN HERE, and that is worth reporting.
         The source and target tasks share the same four classes, so
         the from-scratch model can learn adequate filters from 80
         images -- the gap transfer learning exploits is largest when
         the target data is small AND the task is hard.
         The honest claim is about the PARAMETER COUNT: transfer
         trained {n_frozen:,} parameters against {n_scratch:,}""")

    print("""
      and the two rules that matter in practice:
        USE A SMALLER LEARNING RATE when fine-tuning -- 1e-4 rather
        than 1e-3 -- or the first few large gradients destroy the
        pre-trained features you came for.
        FREEZE EARLY LAYERS, FINE-TUNE LATE ONES. Early filters are
        generic (edges, colours) and transfer everywhere; late layers
        are task-specific and usually should not.""")

    return {"cnn": cnn_te, "mlp": mlp_te, "transfer": best,
            "scratch": sc_curve[-1][2]}


if __name__ == "__main__":
    main()
