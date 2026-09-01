# Unit 3 — Convolutional Neural Networks

**Syllabus topics:** Introduction to images and pixels. Filters/kernels,
padding, and pooling. CNN architecture and layers (Conv, Pooling, Fully
Connected, Softmax). Classical CNN architectures: LeNet-5 (digit recognition —
first CNN model), AlexNet (ImageNet breakthrough — deeper CNN), VGG (concept of
depth, simplicity). Applications in image classification, object detection,
facial recognition.

---

## 3.1 Images and pixels

| Kind | Shape | Values |
|---|---|---|
| Grayscale | `(H, W)` | 0–255, or 0.0–1.0 after scaling |
| Colour | `(H, W, 3)` | one channel each for R, G, B |
| A batch | `(N, H, W, C)` in Keras, `(N, C, H, W)` in PyTorch | — |

> ### ⚠️ The channel-order trap
>
> **Keras is channels-last `(N, H, W, C)`; PyTorch is channels-first
> `(N, C, H, W)`.** Mixing them produces a shape error if you are lucky and a
> silently wrong model if you are not. The lab hits this explicitly — the
> Fashion-MNIST loader returns `(N, 28, 28)` and `06_cnn.py` has to insert the
> channel axis before any torch convolution will accept it.

**Always scale to [0, 1] or standardise.** Raw 0–255 inputs make the first
layer's gradients 255× larger than they should be, and training becomes
needlessly sensitive to the learning rate.

---

## 3.2 Why a dense layer is the wrong tool for an image

Flattening a 28×28 image into 784 numbers throws away the fact that pixel
(5,5) is next to pixel (5,6). A dense layer must **learn that adjacency from
data**, separately for every position.

### 📖 The three properties a convolution has and a dense layer does not

| Property | What it means |
|---|---|
| **Local connectivity** | a unit sees a 5×5 patch, not all 784 pixels |
| **Weight sharing** | the *same* kernel slides across the whole image |
| **Translation equivariance** | move the object, and the response moves with it |

**Weight sharing is where the parameter saving comes from.** One 5×5 kernel is
25 numbers *whatever the image size*; a dense layer over 784 pixels needs 784
weights **per unit**.

### 🔢 The measurement that shows it matters

[Experiment 6](lab.md#experiment-6), real Fashion-MNIST, 8,000 training
images:

| Model | Parameters | Test accuracy |
|---|---|---|
| linear softmax, no hidden layer | 7,850 | **0.8060** |
| MLP on raw pixels | 82,218 | 0.8210 |
| **CNN (2 conv + 2 dense)** | **54,314** | **0.8455** |

> **The CNN wins with fewer parameters than the MLP.** That is the argument
> in one line.
>
> But notice how *small* the MLP-to-CNN gap is: **0.0245**. On centred,
> size-normalised, single-object images, a dense model does nearly as well.
> **The next table is where the CNN actually earns its keep.**

### 🎯 The property that matters — shift every test image by 3 pixels

| Model | Original | Shifted 3px | Drop |
|---|---|---|---|
| **CNN** | 0.8455 | 0.4435 | **0.3940** |
| MLP | 0.8210 | 0.2260 | **0.5980** |

**Both degrade badly**, and that is worth saying honestly — a 3-pixel shift on
a 28-pixel image is a large perturbation, and neither model was trained with
augmentation. But **the MLP loses half again as much**, because it learned a
weight for every *absolute* pixel position. Pooling gives the CNN partial
invariance to where the object sits.

> ### 💡 The practical lesson
>
> If you need real shift invariance, **do not rely on the architecture — train
> with data augmentation.** The architecture gives you a head start; it does
> not give you the property.

---

## 3.3 Convolution, precisely

### 🔢 The output-size formula — memorise this

$$\text{out} = \left\lfloor\frac{\text{in} + 2p - k}{s}\right\rfloor + 1$$

where `p` = padding, `k` = kernel size, `s` = stride.

### The lab's LeNet-shaped network, layer by layer

| Layer | in | k | p | s | out | Parameters |
|---|---|---|---|---|---|---|
| conv1 (1→8, 5×5) | 28 | 5 | 2 | 1 | **28** | 208 |
| maxpool 2×2 | 28 | 2 | 0 | 2 | **14** | 0 |
| conv2 (8→16, 5×5) | 14 | 5 | 2 | 1 | **14** | 3,216 |
| maxpool 2×2 | 14 | 2 | 0 | 2 | **7** | 0 |
| flatten | 7×7×16 | | | | 784 | 0 |
| fc1 — **fully connected** (784→64) | 784 | | | | 64 | **50,240** |

### 🔢 Where the parameters are — check this against your intuition

**The two convolutions hold 3,424 weights between them. The first dense layer
holds 50,240.**

> **In a classical CNN, the convolutions do the work and the dense layers hold
> the weights.** That single observation is why every modern architecture
> replaces the flatten with **global average pooling** — it deletes ~90% of
> the parameters and usually improves generalisation.

### 🔢 Conv layer parameter count

$$(k \times k \times C_{\text{in}} + 1) \times C_{\text{out}}$$

Check: conv2 is `(5×5×8 + 1) × 16 = 201 × 16 = 3,216`. ✓

---

## 3.4 Padding

| Mode | Padding | 28×28 through four 5×5 convs |
|---|---|---|
| `valid` | 0 | 28 → 24 → 20 → 16 → **12** |
| `same` | `(k−1)/2` = 2 | 28 → 28 → 28 → 28 → **28** |

**Without padding the image shrinks at every layer**, so your depth is limited
by arithmetic rather than by what you want. `same` is the default in almost
every modern architecture for exactly this reason, and it also stops the
border pixels from being under-sampled.

---

## 3.5 Pooling

| Type | Operation | Use |
|---|---|---|
| **Max pooling** | maximum of each window | **the default** — keeps the strongest response |
| **Average pooling** | mean of each window | smoother; used in some older nets |
| **Global average pooling** | mean of each entire feature map | replaces flatten; one number per channel |

### 📖 What pooling buys and what it costs

| Buys | Costs |
|---|---|
| downsamples — fewer parameters downstream | **throws away spatial precision** |
| partial translation invariance | bad for segmentation and detection, where position *is* the answer |
| larger receptive field per unit | — |

**Pooling has no parameters.** It is a fixed function, so it contributes
nothing to the parameter count and nothing to the gradient except routing.

---

## 3.6 What the filters actually learn

### ⚠️ The claim, and the measurement

Every textbook says the first convolutional layer learns edge detectors. The
lab measures it, by computing each kernel's gradient along both axes and
calling a kernel **oriented** when one axis exceeds the other by 1.6×:

| Kernel | Horizontal gradient | Vertical gradient | Verdict |
|---|---|---|---|
| 0 | 0.1599 | 0.1523 | blob / mixed |
| 1 | 0.1736 | 0.1459 | blob / mixed |
| … | … | … | … |
| 7 | 0.1091 | 0.1221 | blob / mixed |

**0 of 8 kernels are clearly oriented.**

> ### 💡 Reporting 0 rather than 8 is the honest version of "CNNs learn edge detectors"
>
> The claim comes from AlexNet's first layer — **96 filters at 11×11 on
> 224×224 colour photographs.** With that much capacity and that much data,
> some filters specialise into clean oriented edges and Gabor patches, and
> the famous figure is real.
>
> **Eight 5×5 filters on 28×28 grayscale clothing is a different regime.** The
> network does not need eight distinct edge detectors, so it does not learn
> them. Not every filter learns something a human can name, and a lab report
> that claims otherwise has not looked.

### 🔢 Feature-map sparsity, and how it changes with depth

| Stage | Shape | Mean activation | % exactly zero |
|---|---|---|---|
| input | (1, 1, 28, 28) | 0.3634 | **41.6** |
| conv1 + ReLU | (1, 8, 28, 28) | 0.4328 | **16.9** |
| pool1 | (1, 8, 14, 14) | 0.5296 | 9.9 |
| conv2 + ReLU | (1, 16, 14, 14) | 0.5282 | **41.5** |
| pool2 | (1, 16, 7, 7) | 0.8754 | 22.6 |

**Sparsity grows with depth** — 16.9% at conv1, 41.5% at conv2 — because
deeper filters are more specific and so stay silent more often.

> ### ⚠️ But look at the first step, which goes the wrong way
>
> The **input** is 41.6% zero and conv1's output is only 16.9% zero. **The
> first convolution made the representation *less* sparse.**
>
> That is not a bug. Each filter has a **bias**, so a filter with a positive
> bias responds somewhat even to a black patch; and the convolution mixes
> each pixel with its neighbours, smearing the background's sharp zeros into
> small positive values. Sparsity returns with depth once the filters are
> specific enough to be genuinely silent.
>
> So **"ReLU makes representations sparse" is true of the network as a whole
> and false of its first layer here.** Measure it rather than assuming it.

---

## 3.7 The classical architectures

| Net | Year | Depth | Key idea | Parameters |
|---|---|---|---|---|
| **LeNet-5** | 1998 | 7 | the first working CNN; conv-pool-conv-pool-dense; **tanh** | ~60 K |
| **AlexNet** | 2012 | 8 | **ReLU**, dropout, GPU training, data augmentation; ImageNet top-5 error 26% → **15%** | ~60 M |
| **VGG-16** | 2014 | 16 | **only 3×3 convs, stacked**; simple and uniform | ~138 M |

### 🎯 The VGG insight, which is the examinable one

**Two stacked 3×3 convolutions have the same 5×5 receptive field as one 5×5
convolution, but use fewer parameters and add an extra non-linearity.**

| | Parameters (per channel pair) | Non-linearities |
|---|---|---|
| one 5×5 conv | 25 | 1 |
| two 3×3 convs | **18** | **2** |

Three 3×3 convs give a 7×7 field for 27 weights against 49. **Small filters,
stacked deep** — that is the whole VGG argument, and it is why 3×3 is now the
near-universal default.

### ⚠️ And the honest footnote on VGG

VGG-16 is 138 M parameters, most of them in its dense layers, and it is
**slow**. The lab measures it directly in
[experiment 8](lab.md#experiment-8): as a frozen feature extractor on 500
images, VGG16 scored **0.7660** — *worse* than a small CNN trained from
scratch (0.7810) and **3.7× slower** than MobileNetV2, which scored 0.8260.

> **Bigger is not better.** Benchmark the pre-trained model you chose against
> a small model you trained yourself. Most people never run that baseline and
> so never find out.

---

## 3.8 Applications

| Task | Output | Typical architecture |
|---|---|---|
| **Image classification** | one label | CNN + softmax |
| **Object detection** | boxes + labels | YOLO, Faster R-CNN |
| **Semantic segmentation** | a label per pixel | U-Net, FCN — **no pooling away of position** |
| **Face recognition** (facial recognition) | an embedding | Siamese / triplet loss, then nearest neighbour |

### 💡 Why facial recognition uses embeddings, not classification

You cannot train a classifier with one class per person — you would have to
retrain for every new employee. **Instead, train a network to map faces to a
space where the same person's photos are close together**, then recognise by
nearest neighbour. Adding a person means adding one vector.

[Experiment 11](lab.md#experiment-11) does exactly this mechanism with a
pre-trained MobileNetV2: embed 1,200 images, retrieve by cosine distance, and
measure whether the nearest neighbour shares the label — **0.8150 against
0.7150 for raw pixel distance, with nothing trained.**

---

## What to be able to do after this unit

- [ ] Give the channel order for Keras and for PyTorch
- [ ] Apply `out = floor((in + 2p − k)/s) + 1` to any layer stack
- [ ] Count the parameters of a conv layer and of a dense layer
- [ ] Say where the parameters actually sit in a classical CNN, and what GAP fixes
- [ ] State the three properties convolution has that a dense layer lacks
- [ ] Explain why two 3×3 convs beat one 5×5
- [ ] Name what LeNet, AlexNet and VGG each contributed
- [ ] Explain why pooling is wrong for segmentation
- [ ] Explain why face recognition uses embeddings rather than classes

**Cross-check yourself:** run
`06_cnn.py`. Every table in
this unit is printed by it, including the ones that disagree with the textbook.
