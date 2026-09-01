# Course 14 A — Laboratory

**12 practicals**

Every number on this page was **printed by code in this repository**. Run
everything with:

```bash
KERAS_BACKEND=torch python3 tools/run_deeplearning_labs.py
```

---

## What ran, and what did not

**Ten of the twelve experiments run against real data and real pre-trained
weights.**

| # | Experiment | File | Status |
|---|---|---|---|
| 1 | Perceptron from scratch | `01_perceptron_scratch.py` | **runs** |
| 2 | Teachable Machine / TF Playground | `02_playground.md` | ***NOT EXECUTED*** — interactive web apps |
| 3 | Visualise activations and gradients | `01_perceptron_scratch.py` | **runs** |
| 4 | Deep network for classification (MNIST) | `04_deep_network.py` | **runs — real MNIST** |
| 5 | Dropout, batch norm, activations | `04_deep_network.py` | **runs** |
| 6 | CNN on Fashion-MNIST | `06_cnn.py` | **runs — real Fashion-MNIST** |
| 7 | Visualise filters and feature maps | `06_cnn.py` | **runs** |
| 8 | Fine-tune a pre-trained CNN | `08_pretrained.py` | **runs — real MobileNetV2 + VGG16** |
| 9 | LSTM sentiment on IMDb | `09_rnn_lstm.py` | **runs — real IMDb** |
| 10 | Character-level text generation | `09_rnn_lstm.py` | **runs** |
| 11 | Use a pre-trained model for a simple task | `11_attention.py` | **runs — real MobileNetV2** |
| 12 | Hugging Face sentiment app | `12_huggingface_app.md` | ***NOT EXECUTED*** — `huggingface.co` 403 at the gateway |

`tools/run_deeplearning_labs.py` asserts that both `*** NOT EXECUTED ***`
markers are still present, so neither file can quietly start claiming an
output it never produced.

### 📖 On Keras and TensorFlow

The syllabus says Keras/TensorFlow. **TensorFlow is not installed here, but
Keras 3 is backend-agnostic** — `KERAS_BACKEND=torch` runs the identical API
on PyTorch. The lab prints `Keras 3.15.1, backend 'torch'`, and every
`Sequential`, `.compile()` and `.fit()` is the real thing.

---

## Experiment 1 — a perceptron from scratch

Pure NumPy, no framework. One perceptron per logic gate:

| Gate | Linearly separable | Epochs to converge | Accuracy |
|---|---|---|---|
| AND | yes | **6** | 1.00 |
| OR | yes | **4** | 1.00 |
| NAND | yes | **4** | 1.00 |
| **XOR** | **no** | **never** | **0.50** |

**0.50 is chance.** The four-line impossibility proof is in
[Unit 1 §1.4](unit-1.md#14-the-perceptron-and-the-thing-it-cannot-do).

### Adding one hidden layer

| | Value |
|---|---|
| loss, first epoch → last | **0.9287 → 0.0016** |
| accuracy | **1.00** |

### And a three-layer NumPy network on real MNIST-style digits

| Model | Test accuracy |
|---|---|
| majority class | 0.1022 |
| logistic regression | 0.9622 |
| **3-layer NumPy network** | **0.9733** |

> **Report the baselines.** 0.9733 alone means nothing; 0.9733 against 0.9622
> from logistic regression is a claim you can defend.

---

## Experiment 3 — activations and their gradients

### The vanishing gradient, as arithmetic

| Activation | 10 layers | 50 layers |
|---|---|---|
| sigmoid, best case (0.25) | 9.54e-07 | **7.89e-31** |
| sigmoid, typical | ~1e-10 | **~1e-50** |
| tanh, typical | ~1e-3 | **8.88e-16** |
| **ReLU** (where active) | **1.0** | **1.0** |

### The dying ReLU

```
ReLU        d/dz at z = [-2, -1, -0.5]  ->  [0, 0, 0]
Leaky ReLU  d/dz at z = [-2, -1, -0.5]  ->  [0.01, 0.01, 0.01]
```

### Softmax overflow

| Implementation | `softmax([1000, 1001, 1002])` |
|---|---|
| naive | **`nan`** |
| stable (subtract the max) | `[0.0900, 0.2447, 0.6652]` |

---

## Experiment 4 — a deep network for classification

**The real MNIST**, a stratified 4,000-image subset (400 per class), 1,000
test.

### Does depth help?

| Architecture | Params | Train | Test | Gap | Secs |
|---|---|---|---|---|---|
| none (linear softmax) | 7,850 | 0.9538 | **0.9100** | 0.0437 | 11.1 |
| 1 × 32 | 25,450 | 0.9992 | 0.9150 | 0.0842 | 13.2 |
| 2 × 32 | 26,506 | 0.9995 | 0.9260 | 0.0735 | 15.6 |
| **3 × 64** | 59,210 | 1.0000 | **0.9410** | 0.0590 | 17.8 |

> **Three accuracy points for 7.5× the parameters.** MNIST digits are close to
> linearly separable in raw pixel space, which is exactly why Fashion-MNIST
> was published to replace it — see experiment 6.

### Optimisers

| Optimiser | lr | Epoch 1 | Epoch 5 | Final test |
|---|---|---|---|---|
| SGD | 0.01 | 0.5500 | 0.8650 | 0.9060 |
| SGD | 0.1 | 0.8570 | 0.9130 | **0.9310** |
| RMSProp | 0.001 | 0.8900 | 0.9200 | 0.9290 |
| Adam | 0.001 | **0.8910** | 0.9230 | 0.9300 |

### Learning rate — the one that can make training fail

| lr | Final train loss | Final test acc | Behaviour |
|---|---|---|---|
| **10.0** | **14.5063** | 0.1000 | **DIVERGED — the loss went up** |
| 1.0 | 0.6238 | 0.7750 | converged, badly |
| **0.1** | 0.0217 | **0.9310** | converged |
| 0.01 | 0.3041 | 0.9060 | converged, still climbing |
| **0.0001** | 2.2373 | 0.1920 | **too slow — barely off ln(10) = 2.303** |

### Weight initialisation

| Initialiser | Epoch 1 test | Final test |
|---|---|---|
| **zeros — BROKEN** | **0.1000** | **0.1000** |
| Glorot (default) | 0.8910 | 0.9340 |
| He (for ReLU) | 0.8860 | **0.9400** |

---

## Experiment 5 — dropout, batch norm, activations

A 3×256 network on 4,000 images: **335,114 parameters, ~84 per example.**

| Regularisation | Train | Test | Gap |
|---|---|---|---|
| none | 1.0000 | 0.9490 | 0.0510 |
| dropout 0.2 | 0.9948 | 0.9490 | 0.0458 |
| **dropout 0.5** | 0.9835 | 0.9500 | **0.0335** ← smallest gap |
| **batch norm** | 0.9990 | **0.9530** | 0.0460 ← best test |
| batch norm + dropout 0.3 | 0.9885 | 0.9500 | 0.0385 |

> **The two columns disagree**, and the table reports both. See
> [Unit 2 §2.6](unit-2.md#26-overfitting-underfitting-and-the-three-fixes).

| Activation | Epoch 1 test | Final test | Final train loss |
|---|---|---|---|
| ReLU | 0.7200 | **0.9778** | 0.0052 |
| tanh | 0.8133 | 0.9689 | 0.0099 |
| **sigmoid** | **0.1022** | 0.9133 | 0.2412 |
| ELU | 0.8111 | 0.9711 | 0.0058 |

---

## Experiment 6 — a CNN on Fashion-MNIST

**The real Fashion-MNIST**, a stratified 8,000-image subset, 2,000 test.

| Model | Params | Test accuracy |
|---|---|---|
| linear softmax | 7,850 | **0.8060** |
| MLP on raw pixels | 82,218 | 0.8210 |
| **CNN (2 conv + 2 dense)** | **54,314** | **0.8455** |

> **The linear model fell from 0.9100 on MNIST to 0.8060 here; the best
> network fell 0.9410 → 0.8455.** The linear model lost roughly twice as much,
> which is what Fashion-MNIST was published to expose.

### Shift every test image by 3 pixels

| Model | Original | Shifted 3px | Drop |
|---|---|---|---|
| **CNN** | 0.8455 | 0.4435 | **0.3940** |
| MLP | 0.8210 | 0.2260 | **0.5980** |

### The output-size arithmetic

`out = floor((in + 2p − k)/s) + 1`

| Layer | in | k | p | s | out | Params |
|---|---|---|---|---|---|---|
| conv1 (1→8, 5×5) | 28 | 5 | 2 | 1 | 28 | 208 |
| maxpool | 28 | 2 | 0 | 2 | 14 | 0 |
| conv2 (8→16, 5×5) | 14 | 5 | 2 | 1 | 14 | 3,216 |
| maxpool | 14 | 2 | 0 | 2 | 7 | 0 |
| flatten | 7×7×16 | | | | 784 | 0 |
| **fc1 (784→64)** | 784 | | | | 64 | **50,240** |

**Convolutions: 3,424 weights. First dense layer: 50,240.**

---

## Experiment 7 — filters and feature maps

### Are the filters edge detectors? Measured, not assumed

| Kernel | Horiz. gradient | Vert. gradient | Verdict |
|---|---|---|---|
| 0 | 0.1599 | 0.1523 | blob / mixed |
| 1 | 0.1736 | 0.1459 | blob / mixed |
| … | … | … | … |
| 7 | 0.1091 | 0.1221 | blob / mixed |

**0 of 8 kernels are clearly oriented.** See
[Unit 3 §3.6](unit-3.md#36-what-the-filters-actually-learn) for why that is the
honest version of "CNNs learn edge detectors".

### Feature-map sparsity

| Stage | Shape | Mean activation | % zero |
|---|---|---|---|
| input | (1, 1, 28, 28) | 0.3634 | **41.6** |
| conv1 + ReLU | (1, 8, 28, 28) | 0.4328 | **16.9** |
| pool1 | (1, 8, 14, 14) | 0.5296 | 9.9 |
| conv2 + ReLU | (1, 16, 14, 14) | 0.5282 | **41.5** |
| pool2 | (1, 16, 7, 7) | 0.8754 | 22.6 |

> **The first convolution made the representation *less* sparse than the
> input.** The explanation — filter biases and neighbourhood mixing — is in
> [Unit 3 §3.6](unit-3.md#36-what-the-filters-actually-learn).

---

## Experiment 8 — fine-tuning a pre-trained CNN

**Real MobileNetV2 and VGG16 ImageNet weights**, fetched from
`storage.googleapis.com`. 500 training images, 50 per class.

| Approach | Total params | Trainable | Test acc | Secs |
|---|---|---|---|---|
| CNN from scratch | 105,866 | 105,866 | 0.7810 | 9.0 |
| dense head on raw pixels | 50,890 | 50,890 | 0.7500 | 2.8 |
| **MobileNetV2 frozen + new head** | 2,340,618 | **82,634** | **0.8260** | 15.1 |
| VGG16 frozen + new head | 14,748,170 | 33,482 | **0.7660** | 55.7 |

### Then actually fine-tune

| | Trainable | Test acc |
|---|---|---|
| MobileNetV2 frozen | 82,634 | **0.8260** |
| MobileNetV2, top 20 layers unfrozen, lr = 1e-4 | **1,135,114** | **0.7760** |

> ### ⚠️ Two results that contradict the usual story
>
> **VGG16 lost to a small CNN trained from scratch**, and **fine-tuning made
> MobileNetV2 worse.** Both are reported as measured and explained in
> [Unit 5 §5.3](unit-5.md#53-transfer-learning-and-fine-tuning).

### What the pre-trained head actually knows

Fed a Fashion-MNIST **Pullover**, ImageNet's top-3:

| Class | Probability |
|---|---|
| `lab_coat` | 0.1561 |
| `sweatshirt` | 0.0421 |
| `pill_bottle` | 0.0375 |

**ImageNet has 1,000 classes and none is "pullover."**

---

## Experiment 9 — LSTM sentiment analysis

### On a generated dataset (one decisive word per sentence)

| Cell | Params | Epoch 1 | Epoch 4 | Final |
|---|---|---|---|---|
| **RNN** | 3,002 | 0.5175 | 0.5300 | **0.6600** |
| **LSTM** | 8,570 | 0.5175 | 1.0000 | **0.9975** |
| **GRU** | 6,714 | 0.5300 | 0.9775 | **1.0000** |

### Ask the model what it learned

| Word group | Mean P(positive) | n |
|---|---|---|
| POSITIVE vocabulary | **0.9998** | 10 |
| NEGATIVE vocabulary | **0.0002** | 10 |
| neutral filler | 0.8332 | 6 |

### On the real IMDb dataset

6,000 training reviews, 3,000 test, 10,000-word vocabulary, 200 tokens.

| Cell | Params | Epoch 1 | Final test |
|---|---|---|---|
| RNN | 326,402 | 0.5567 | **0.6523** |
| LSTM | 345,218 | 0.5927 | **0.7357** |
| GRU | 338,946 | 0.6090 | **0.7570** |

**Majority-class baseline: 0.5130.**

> **The LSTM–RNN gap was +0.3375 on the generated task and +0.0833 on IMDb.**
> Both numbers are real and they measure different things —
> [Unit 4 §4.5](unit-4.md#45-the-measurement-rnn-vs-lstm-vs-gru-twice).

### The vanishing gradient

| Sequence length | RNN gradient (w = 0.5) | LSTM cell path |
|---|---|---|
| 50 | 8.88e-16 | 1.00 |
| 100 | 7.89e-31 | 1.00 |
| **500** | **3.05e-151** | 1.00 |
| **1100** | **0.00e+00** | 1.00 |

---

## Experiment 10 — character-level text generation

| `T` | Sample |
|---|---|
| **0.2** | `the loss falls when the weights move down the gradient. the quick brow` |
| **0.7** | `the quick brown fox jumps over the lazy dog. a neural network learns a` |
| **1.5** | `the loss falls when qunt fomplex ones. an attention head compares ethe` |

**It learned spelling and local grammar and not what a sentence is about** —
which is the dependency length attention was invented to close.

---

## Experiment 11 — a pre-trained model on a simple task

**Real MobileNetV2, 2,257,984 parameters, nothing trained.** 200 query images
against a 1,000-image database; retrieve the nearest neighbour by cosine
distance and ask whether it shares the label.

| Retrieval space | Top-1 same-class |
|---|---|
| **MobileNetV2 embedding (1280-d)** | **0.8150** |
| raw pixels (784-d) | 0.7150 |
| chance | 0.1000 |

---

## Experiment 12 — attention from scratch

*(The Hugging Face deployment itself is
`12_huggingface_app.md`,
marked NOT EXECUTED. What runs is the mechanism.)*

### Scaled dot-product attention, on checkable numbers

| Step | Value |
|---|---|
| raw scores `Q·Kᵀ` | `[1.0, 0.0, 0.7]` |
| scaled by `√d_k = 2.0` | `[0.5, 0.0, 0.35]` |
| attention weights | **`[0.4053, 0.2458, 0.3489]`** |
| output | **`[5.7974, 4.2026]`** |

### Why `√d_k` — measured

| `d_k` | std of `Q·K` | std ÷ `√d_k` | max softmax weight |
|---|---|---|---|
| 4 | 2.025 | 1.013 | 0.1615 |
| 64 | 8.060 | 1.008 | 0.7146 |
| **1024** | **33.167** | 1.036 | **0.9857** |

### A trained transformer encoder

One block, 4 heads, `d_model` 32 — **10,690 parameters, test accuracy
1.0000**.

**The sentiment word was the most-attended token in 111/120 = 92.5% of
sentences.**

```
very really script wonderful was actor movie
decisive word: 'wonderful' at position 3
most-attended: 'wonderful' at position 3
...#...
```

### Positional-encoding ablation

| | Test accuracy |
|---|---|
| with positions | 1.0000 |
| **without** positions | **1.0000** |

**A null result, reported as such** — the task is bag-of-words, so order
carries no information.

### The `O(T²)` cost

| Sequence length | Attention scores | vs T=512 |
|---|---|---|
| 512 | 262,144 | 1× |
| 1,024 | 1,048,576 | **4×** |
| 4,096 | 16,777,216 | **64×** |

---

## Experiments 2 and 12 — the two that cannot run

| File | Why | What it contains |
|---|---|---|
| `02_playground.md` | TensorFlow Playground and Teachable Machine are **interactive web apps** — there is no output to capture | a full experiment protocol: eight settings to run, what to record, and the deliberate background-bias experiment |
| `12_huggingface_app.md` | `huggingface.co` returns **403 at the gateway** | the complete Gradio app, four deployment traps, and the error analysis that carries the marks |

Neither claims an output. Both name the runnable half that covers the same
ground.

---

## Running it yourself

```bash
pip install -r tools/requirements.txt
KERAS_BACKEND=torch python3 tools/run_deeplearning_labs.py
```

The datasets download once and cache under `KERAS_HOME`. On CPU the full suite
takes roughly half an hour; individual scripts run in one to five minutes each.
