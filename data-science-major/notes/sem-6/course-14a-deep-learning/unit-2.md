# Unit 2 — Deep Neural Networks

**Syllabus topics:** Forward and backward propagation. Weight
initialization, learning rate, and optimization algorithms (SGD, Adam,
RMSProp). Overfitting & underfitting: Regularization, Dropout, Batch
normalization. Activation functions in deep networks. Loss functions in detail
(MSE, cross-entropy, hinge loss). Introduction to Keras/TensorFlow framework.

---

## 2.1 Forward propagation

### 📖 The whole of it

For each layer `ℓ`:

$$z^{[\ell]} = W^{[\ell]}a^{[\ell-1]} + b^{[\ell]} \qquad a^{[\ell]} = f(z^{[\ell]})$$

with `a⁽⁰⁾ = x`. That is the entire forward pass — **a matrix multiply, an
add, and an element-wise function, repeated.**

### 🔢 Shapes, which is where the marks are lost

For a batch of `m` examples with layer sizes `n⁽ˡ⁻¹⁾ → n⁽ˡ⁾`:

| Object | Shape |
|---|---|
| `a⁽ˡ⁻¹⁾` | `(n⁽ˡ⁻¹⁾, m)` |
| `W⁽ˡ⁾` | `(n⁽ˡ⁾, n⁽ˡ⁻¹⁾)` |
| `b⁽ˡ⁾` | `(n⁽ˡ⁾, 1)` — **broadcast** across the batch |
| `z⁽ˡ⁾`, `a⁽ˡ⁾` | `(n⁽ˡ⁾, m)` |

**Parameter count for a dense layer: `n⁽ˡ⁾ × n⁽ˡ⁻¹⁾ + n⁽ˡ⁾`.** Check it
against the lab: a linear softmax on MNIST is `10 × 784 + 10 = 7,850`, which
is exactly what [experiment 4](lab.md#experiment-4) prints.

---

## 2.2 Backward propagation

### 📖 The four equations

$$dz^{[L]} = a^{[L]} - y \qquad\text{(for softmax + cross-entropy)}$$
$$dW^{[\ell]} = \tfrac{1}{m}\,dz^{[\ell]}a^{[\ell-1]T} \qquad db^{[\ell]} = \tfrac{1}{m}\textstyle\sum dz^{[\ell]}$$
$$dz^{[\ell-1]} = W^{[\ell]T}dz^{[\ell]} \odot f'(z^{[\ell-1]})$$

### 💡 The one detail worth memorising

**`dz⁽ᴸ⁾ = a⁽ᴸ⁾ − y`** — the output-layer gradient of softmax with
cross-entropy is just *prediction minus truth*. The messy softmax Jacobian and
the `1/ŷ` from the log cancel exactly. **This cancellation is why the pairing
is universal**, and it is a standard viva question.

### ⚠️ The two things that make it fail

The last equation is a **product** along the chain. Over many layers:

| If each factor is | Then after `n` layers | Called |
|---|---|---|
| < 1 (e.g. sigmoid's ≤ 0.25) | → 0 | **vanishing gradient** |
| > 1 (e.g. badly initialised weights) | → ∞ | **exploding gradient** |

Vanishing is fixed with ReLU, residual connections and batch norm. Exploding
is fixed with **gradient clipping** — cap the norm of the whole gradient
vector at some threshold (1.0 is typical) before the update.

---

## 2.3 Weight initialisation

### 🎯 The symmetry problem

**If every weight starts at the same value, every unit in a layer computes the
same thing, receives the same gradient, and updates identically — for ever.**
A 64-unit layer with all-zero weights has the expressive power of one unit.

The lab measures it directly:

| Initialiser | Epoch 1 test | Final test |
|---|---|---|
| **all zeros** | **0.1000** | **0.1000** |
| Glorot uniform (Keras default) | 0.8910 | 0.9340 |
| He normal (for ReLU) | 0.8860 | **0.9400** |

**0.1000 is chance on ten classes, at epoch 1 and at epoch 30 alike.** The
all-zero network never learns anything at all, while the two random schemes
are at 0.89 after a single epoch. **Random initialisation exists solely to
break this symmetry.**

Note also how close Glorot and He are here — 0.9340 against 0.9400. **The
choice between them matters at depth, not at three layers**; what matters at
any depth is that they are not both zero.

### 📖 The two schemes worth naming

| Scheme | Variance | Use with |
|---|---|---|
| **Glorot / Xavier** | `1/fan_in` (or `2/(fan_in+fan_out)`) | tanh, sigmoid |
| **He** | `2/fan_in` | **ReLU** |

**Why He has the factor of 2:** ReLU zeroes roughly half its inputs, which
halves the variance of the output. Doubling the initial variance restores it,
so the signal neither shrinks nor grows as it passes through many layers.

---

## 2.4 The learning rate — the one that can make training fail

### 🎯 The measurement

[Experiment 4](lab.md#experiment-4), same network and same data, only the
learning rate changing:

| Learning rate | Final train loss | Final test accuracy | Behaviour |
|---|---|---|---|
| **10.0** | **14.5063** | **0.1000** | **DIVERGED — the loss went *up*** |
| 1.0 | 0.6238 | 0.7750 | converged, badly |
| **0.1** | **0.0217** | **0.9310** | converged |
| 0.01 | 0.3041 | 0.9060 | converged, still climbing |
| **0.0001** | **2.2373** | **0.1920** | **too slow — barely moved off ln(10) = 2.303** |

> ### ⚠️ Read the two failure rows carefully
>
> **They fail differently and the fix is opposite.** At `lr = 10.0` the loss
> is *higher than it started* — the updates overshoot the minimum and climb
> the other wall. At `lr = 0.0001` the loss is still 2.2373, essentially
> `ln(10) = 2.303`, which is the loss of a model assigning 1/10 to every
> class: **it has learned nothing at all.**
>
> A student who sees 0.1000 accuracy and concludes "the model is too small"
> will make it bigger and fail again.

### 💡 How to find it in practice

Start at `1e-3` with Adam. If the loss is `nan` or rising, divide by 10. If it
is falling but glacially, multiply by 3. **Then add a schedule** — reduce the
rate when validation loss stops improving (`ReduceLROnPlateau`), or use cosine
decay. Large steps early to travel, small steps late to settle.

---

## 2.5 Optimisers

### 📖 The three the syllabus names

| Optimiser | Update rule, in words | Cost |
|---|---|---|
| **SGD** | step against the gradient | 0 extra state |
| **RMSProp** | divide the step by a running RMS of recent gradients — a **per-parameter** rate | 1 extra array |
| **Adam** | RMSProp **plus momentum**: running estimates of both the mean (1st moment) and the variance (2nd moment) of the gradient, bias-corrected | 2 extra arrays |

### 🔢 The measurement

| Optimiser | lr | Epoch 1 | Epoch 5 | Final test |
|---|---|---|---|---|
| SGD | 0.01 | 0.5500 | 0.8650 | 0.9060 |
| SGD | 0.1 | 0.8570 | 0.9130 | **0.9310** |
| RMSProp | 0.001 | 0.8900 | 0.9200 | 0.9290 |
| **Adam** | 0.001 | **0.8910** | 0.9230 | 0.9300 |

> **Adam reached 0.8910 in one epoch where SGD at `lr = 0.01` was at 0.5500.**
> But look at the SGD `lr = 0.1` row: it ends *highest*. **The adaptive
> methods do not reach a better place; they reach a good place without you
> having to find the right learning rate.** That is the honest summary, and
> "the right learning rate" is precisely the hard part.

**Practical answer:** Adam at `1e-3` is the default and you need a reason to
deviate. SGD with momentum plus a schedule still wins on large vision models
— worth knowing, not where you start.

---

## 2.6 Overfitting, underfitting, and the three fixes

### 🎯 Diagnose before you treat

| Symptom | Diagnosis | Fix |
|---|---|---|
| train **and** test both poor | **underfitting** | bigger model, train longer, better features, higher lr |
| train excellent, test poor | **overfitting** | more data, regularisation, smaller model, early stopping |
| train poor, test better | a bug, or dropout inflating training loss | check `model.eval()` |

### The lab makes it overfit on purpose

A 3×256 network on 4,000 MNIST images — **335,114 parameters for 4,000
examples, about 84 parameters per example.** The network can memorise the
training set outright, and does:

| Regularisation | Train | Test | **Gap** |
|---|---|---|---|
| none | 1.0000 | 0.9490 | **0.0510** |
| dropout 0.2 | 0.9948 | 0.9490 | 0.0458 |
| **dropout 0.5** | 0.9835 | 0.9500 | **0.0335** ← smallest gap |
| batch norm | 0.9990 | **0.9530** | 0.0460 ← best test |
| batch norm + dropout 0.3 | 0.9885 | 0.9500 | 0.0385 |

> ### ⚠️ Report both columns, and notice they disagree
>
> **Dropout 0.5 gave the smallest gap; batch norm gave the best test score.**
> They are not the same question. A regulariser that shrinks the gap by
> dragging the *training* score down has not helped anyone — and a table that
> reports only "the gap closed" is hiding that.
>
> Note also how small the wins are: 0.9490 → 0.9530 is four examples in a
> thousand. **On this data, regularisation is a refinement.** Say so, rather
> than claiming dropout transformed the model.

### 📖 What each one actually does

| Technique | Mechanism | The catch |
|---|---|---|
| **L2 / weight decay** | adds `λ‖w‖²` to the loss | shrinks weights toward zero |
| **Dropout** | zeroes a random fraction of activations **each batch, training only** | an implicit ensemble over 2ⁿ sub-networks |
| **Batch norm** (batch normalization) | normalises pre-activations to zero mean, unit variance **per batch**, then rescales with two learned parameters | **behaves differently at train and test time** |
| **Early stopping** | halt when validation loss stops improving | needs a validation set held out from training |
| **Data augmentation** | flip, crop, rotate | the cheapest and often the most effective |

> ### ⚠️ The classic bug
>
> **Batch norm uses batch statistics while training and running averages at
> inference. Dropout is active while training and off at inference.** Both
> need the model told which mode it is in. Forgetting `model.eval()` in
> PyTorch — or `training=False` in Keras — silently corrupts every evaluation
> you run, and the symptom is a test score that jitters between runs.

---

## 2.7 Activation functions in deep networks

| Activation | Epoch 1 test | Final test | Final train loss |
|---|---|---|---|
| ReLU | 0.7200 | **0.9778** | 0.0052 |
| tanh | 0.8133 | 0.9689 | 0.0099 |
| **sigmoid** | **0.1022** | 0.9133 | 0.2412 |
| ELU | 0.8111 | 0.9711 | 0.0058 |

> **All four eventually work, and that is the honest result at three layers.**
> The vanishing gradient is a problem of **depth**, and three layers is not
> deep.
>
> **Read the first-epoch column instead.** Sigmoid starts at 0.1022 —
> *chance* — because its gradient is at most 0.25 per layer, so the early
> updates are tiny. Stack thirty such layers and it stops training
> altogether, which is the `0.25ⁿ` arithmetic from Unit 1.

---

## 2.8 Loss functions in detail

| Loss | Formula | Use for | Property |
|---|---|---|---|
| **MSE** | `(1/n)Σ(y−ŷ)²` | regression | differentiable everywhere; sensitive to outliers |
| **MAE** | `(1/n)Σ|y−ŷ|` | regression with outliers | robust; not differentiable at 0 |
| **Binary cross-entropy** | `−[y log ŷ + (1−y)log(1−ŷ)]` | 2 classes | pair with **sigmoid** |
| **Categorical cross-entropy** | `−Σ y log ŷ` | k classes | pair with **softmax** |
| **Hinge** | `max(0, 1 − y·ŷ)`, `y ∈ {−1,+1}` | SVM-style margins | zero loss once correct **by a margin of 1** |

### 💡 What makes hinge different

Cross-entropy keeps pushing forever — a correct prediction at 0.99 still has
a non-zero gradient. **Hinge loss goes exactly to zero once the example is
correct by a margin of 1** and stops caring. That is the max-margin idea from
Course 12 A's SVM, expressed as a loss you can drop into a neural network.

### ⚠️ Keras naming, which trips everyone

| Your labels look like | Use |
|---|---|
| `[0, 3, 7]` — integers | `sparse_categorical_crossentropy` |
| `[[1,0,0],[0,0,1]]` — one-hot | `categorical_crossentropy` |

Using the wrong one raises a shape error at best, and silently trains on
nonsense at worst.

---

## 2.9 Keras and TensorFlow

### 📖 What Keras is

A high-level API. Since **Keras 3 it is backend-agnostic** — the same code
runs on TensorFlow, PyTorch or JAX, selected by the `KERAS_BACKEND`
environment variable.

> **That is exactly how this course's labs run.** TensorFlow is not installed
> here, but `KERAS_BACKEND=torch` runs the identical Keras API on PyTorch. The
> lab prints `Keras 3.15.1, backend 'torch'` and every `Sequential`,
> `.compile()` and `.fit()` below is the real API — **character-for-character
> what you would write against TensorFlow.**

### The three lines that are the whole framework

```python
model = keras.Sequential([                       # 1. architecture
    keras.layers.Input((784,)),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(10, activation="softmax"),
])
model.compile(optimizer="adam",                   # 2. how to train
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(Xtr, ytr, validation_data=(Xte, yte),   # 3. train
          epochs=30, batch_size=32)
```

### 📖 Sequential vs Functional

| API | Use when |
|---|---|
| **Sequential** | one input, one output, layers in a line |
| **Functional** | branches, merges, multiple inputs or outputs, skip connections |

ResNet's skip connection cannot be expressed in `Sequential`. **That is the
standard exam example.**

---

## What to be able to do after this unit

- [ ] Write the forward-pass equations and get every shape right
- [ ] Count the parameters of a dense layer and check it against a summary
- [ ] State why `dz⁽ᴸ⁾ = a⁽ᴸ⁾ − y` for softmax + cross-entropy
- [ ] Explain the symmetry problem and why He uses `2/fan_in`
- [ ] Distinguish a diverging learning rate from one that is merely too small — **and give the different fixes**
- [ ] Say what Adam adds to RMSProp, and what RMSProp adds to SGD
- [ ] Diagnose over- vs underfitting from a train/test pair
- [ ] Explain why dropout and batch norm need a train/eval mode
- [ ] Choose between `sparse_categorical_crossentropy` and `categorical_crossentropy`

**Cross-check yourself:** run
`04_deep_network.py`.
Every table in this unit is printed by it.
