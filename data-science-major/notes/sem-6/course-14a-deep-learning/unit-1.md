# Unit 1 — Foundations of Deep Learning

**Syllabus topics:** What is Artificial Intelligence, Machine Learning, and
Deep Learning? History and applications of deep learning. Biological vs.
Artificial Neurons. Introduction to Neural Networks. Perceptron and activation
functions (Linear, ReLU, Sigmoid, Tanh, Softmax). Types of Neural Networks
(shallow vs. deep, feedforward vs. recurrent). Gradient descent and
backpropagation (conceptual only). Concept of loss functions (MSE,
cross-entropy) at intuitive level.

---

## 1.1 AI, machine learning and deep learning are nested, not synonymous

### 🎯 The one sentence

**Deep learning is a subset of machine learning, which is a subset of
artificial intelligence — and the distinguishing feature at each level is how
much of the solution a human has to specify.**

| Level | Who decides the rules | Who decides the features | Example |
|---|---|---|---|
| **Classical AI** | the human writes them | the human | a rule engine, minimax, A\* — Course 13 A |
| **Machine learning** | learned from data | **the human engineers them** | logistic regression on TF-IDF — Course 12 A |
| **Deep learning** | learned from data | **learned from data** | a CNN on raw pixels |

> **The exam wording to memorise:** deep learning is *representation
> learning*. It learns the features and the classifier together, in one
> optimisation, from raw input.

### ⚠️ The cost nobody mentions in the definition

Learning the features instead of engineering them means the model needs far
more data and far more compute, and it gives up interpretability. In
[experiment 4](lab.md#experiment-4) a linear model on MNIST reaches **0.9100**
with 7,850 parameters; the best deep network reaches **0.9410** with 59,210.

**Three accuracy points for 7.5× the parameters.** That is not an argument
against deep learning — it is an argument for always measuring the baseline
before you claim the depth was necessary.

---

## 1.2 A very short history, and why each date matters

| Year | Event | Why it is examinable |
|---|---|---|
| 1943 | McCulloch & Pitts: a neuron as a threshold logic unit | the first mathematical neuron |
| 1958 | Rosenblatt's **Perceptron**, with a learning rule | first *learning* machine; convergence proved for separable data |
| 1969 | Minsky & Papert, *Perceptrons* | proved a single layer **cannot compute XOR** — funding collapsed |
| 1986 | Rumelhart, Hinton & Williams popularise **backpropagation** | made multi-layer training practical; ended the first "AI winter" |
| 1998 | LeCun's **LeNet-5** reads cheques | the first genuinely deployed CNN |
| 2012 | **AlexNet** wins ImageNet by ~10 points | GPUs + ReLU + dropout; the modern era starts here |
| 2014 | **GANs** (Goodfellow) | generation as a two-player game |
| 2017 | **"Attention Is All You Need"** — the Transformer | removed recurrence; led directly to BERT and GPT |

### 📖 What actually changed in 2012

Not the idea. Backpropagation was 26 years old. **Three practical things
changed:** labelled data at ImageNet scale, GPUs making the matrix multiplies
affordable, and ReLU replacing sigmoid so that deep networks could train at
all. Section 1.5 shows why the last one mattered so much.

---

## 1.3 Biological vs artificial neurons

| Biological | Artificial |
|---|---|
| dendrites collect signals | inputs **x₁ … xₙ** |
| synaptic strength | weights **w₁ … wₙ** |
| cell body sums | **z = Σwᵢxᵢ + b** |
| fires above a threshold | activation **a = f(z)** |
| axon carries the output | the output feeds the next layer |
| ~10¹¹ neurons, ~10¹⁵ synapses, spiking and asynchronous | thousands to billions of parameters, continuous, synchronous |

> ### ⚠️ Do not push the analogy
>
> **Real neurons spike; artificial ones output a real number. Real learning is
> local; backpropagation is not** — it requires a global error signal
> travelling backwards through the exact forward weights, which no known
> biological mechanism does. The analogy is a naming convention and a source
> of intuition, not a claim about the brain.

---

## 1.4 The perceptron, and the thing it cannot do

### 📖 The model

$$\hat{y} = \begin{cases} 1 & \text{if } \mathbf{w}\cdot\mathbf{x} + b > 0 \\ 0 & \text{otherwise}\end{cases}$$

### 🔢 The learning rule

For each misclassified example, **w ← w + η(y − ŷ)x** and **b ← b + η(y − ŷ)**.

If the data is linearly separable, this is *proved* to converge in a finite
number of steps. If it is not, it never converges — it cycles forever.

### The measurement that makes the point

`01_perceptron_scratch.py`
trains one perceptron on each of the four basic logic gates:

| Gate | Linearly separable? | Epochs to converge | Accuracy |
|---|---|---|---|
| AND | yes | **6** | 1.00 |
| OR | yes | **4** | 1.00 |
| NAND | yes | **4** | 1.00 |
| **XOR** | **no** | **never** | **0.50** |

**0.50 on a two-class problem is chance.** The perceptron is not learning
slowly; it is provably incapable.

### 🔢 Why, in one line of arithmetic

XOR needs `f(0,0)=0`, `f(0,1)=1`, `f(1,0)=1`, `f(1,1)=0`. A linear boundary
`w₁x₁ + w₂x₂ + b` would need:

| Point | Required | Constraint |
|---|---|---|
| (0,0) → 0 | `b ≤ 0` | |
| (0,1) → 1 | `w₂ + b > 0` | so `w₂ > −b ≥ 0` |
| (1,0) → 1 | `w₁ + b > 0` | so `w₁ > −b ≥ 0` |
| (1,1) → 0 | `w₁ + w₂ + b ≤ 0` | but `w₁ + w₂ > −2b ≥ −b`, so `w₁+w₂+b > 0` |

**The last two lines contradict.** No weights exist. This is the 1969 result
that stopped the field for fifteen years, and it fits in a table.

### 💡 And the fix, measured

Add one hidden layer of two units with a non-linearity, and the same script
reports loss falling **0.9287 → 0.0016** and accuracy **1.00**.

> **The hidden layer does not "try harder". It bends the space.** Each hidden
> unit learns one straight line; the output unit combines them into a region
> that is not a half-plane. That is the entire idea of depth, and
> `02_playground.md`
> has you watch it happen in a browser.

---

## 1.5 Activation functions

### 🎯 Why they exist at all — the most examinable fact in the unit

**Without a non-linear activation, a deep network collapses to a shallow one.**

$$W_3(W_2(W_1x)) = (W_3W_2W_1)x = Wx$$

Three layers, one matrix. **A hundred linear layers still compute a line.**
Every bit of representational power depth gives you comes from the
non-linearity between the layers.

### 📖 The five the syllabus names

| Name | Formula | Range | Derivative | Use it for |
|---|---|---|---|---|
| **Linear** | `z` | (−∞, ∞) | 1 | output layer of a **regression** |
| **Sigmoid** | `1/(1+e⁻ᶻ)` | (0, 1) | ≤ **0.25** | output of **binary** classification |
| **Tanh** | `(eᶻ−e⁻ᶻ)/(eᶻ+e⁻ᶻ)` | (−1, 1) | ≤ **1.0** | RNN hidden states |
| **ReLU** | `max(0, z)` | `0, ∞) | **0 or 1** | **hidden layers — the default** |
| **Softmax** | `eᶻⁱ/Σeᶻʲ` | (0,1), sums to 1 | — | output of **multi-class** classification |

### 🔢 Why ReLU won, as arithmetic

Backpropagation multiplies derivatives along the chain. Over `n` layers the
gradient carries a factor of roughly `(max derivative)ⁿ`.
[`01_perceptron_scratch.py``
computes it:

| Activation | 10 layers | 50 layers |
|---|---|---|
| sigmoid, **best case** (0.25) | 9.54e-07 | **7.89e-31** |
| sigmoid, **typical** | ~1e-10 | **~1e-50** |
| tanh, **typical** | ~1e-3 | **8.88e-16** |
| **ReLU** (where active) | **1.0** | **1.0** |

> **7.89e-31 is the best case for sigmoid, and it is already hopeless.** The
> gradient reaching layer 1 is thirty orders of magnitude smaller than the one
> at layer 50, so the early layers receive no usable learning signal at all.
> **ReLU's derivative is exactly 1 wherever the unit is active**, so the
> product does not shrink.

### ⚠️ ReLU's own failure: the dying unit

If a unit's input is negative for every example, its gradient is **exactly
zero** and it never recovers. The lab shows both sides:

```
ReLU        d/dz at z = [-2, -1, -0.5]  ->  [0, 0, 0]      dead for ever
Leaky ReLU  d/dz at z = [-2, -1, -0.5]  ->  [0.01, 0.01, 0.01]   still learning
```

Leaky ReLU (`max(0.01z, z)`) exists for exactly this, and ELU and GELU are
smoother variants of the same fix.

### ⚠️ Softmax overflows if you write it the obvious way

`exp(1000)` is `inf`, and `inf/inf` is `nan`. The lab measures it:

| Implementation | `softmax([1000, 1001, 1002])` |
|---|---|
| naive `exp(z)/Σexp(z)` | **`nan`** (overflow to `inf`) |
| stable `exp(z − max z)/Σexp(z − max z)` | `[0.0900, 0.2447, 0.6652]` |

Subtracting the maximum changes nothing mathematically — the constant cancels
— and changes everything numerically. **Every real library does this**, and
knowing why is a standard viva question.

---

## 1.6 Types of neural network

| Axis | Options | The distinction |
|---|---|---|
| Depth | **shallow** (0–1 hidden layers) vs **deep** (2+) | shallow can approximate anything *in theory*, deep does it with exponentially fewer units |
| Connection | **feedforward** vs **recurrent** | recurrent has a cycle, so it has *state*, so it can process sequences |
| Layer type | dense, convolutional, recurrent, attention | what structure is assumed about the input |

### 📖 The universal approximation theorem, stated honestly

A network with **one** hidden layer and enough units can approximate any
continuous function on a bounded domain to any accuracy.

> **This is often quoted as though it made depth unnecessary. It does not.**
> The theorem says such a network *exists*; it says nothing about how many
> units it needs (possibly exponentially many), and nothing about whether
> gradient descent can *find* it. Depth is about efficiency and
> learnability, not about what is representable.

---

## 1.7 Loss functions, intuitively

### 📖 The two you must know

| Loss | Formula | Use for | Why |
|---|---|---|---|
| **MSE** | `(1/n)Σ(y − ŷ)²` | regression | penalises large errors quadratically |
| **Cross-entropy** | `−Σ y log ŷ` | classification | penalises *confident* wrong answers enormously |

### 🔢 Why not MSE for classification

Suppose the true class is 1 and the model says `ŷ = 0.01`.

| Loss | Value | Gradient signal |
|---|---|---|
| MSE | `(1 − 0.01)² = 0.98` | bounded, and **shrinks** as sigmoid saturates |
| Cross-entropy | `−log(0.01) = 4.61` | large, and **does not vanish** with saturation |

**Cross-entropy is unbounded as ŷ → 0.** A confidently wrong prediction
produces an enormous loss and an enormous gradient, which is exactly the
behaviour you want. MSE paired with a sigmoid produces a *small* gradient
precisely when the model is most wrong — the saturation problem — which is why
the pairing is a classic exam trap.

### 💡 The reading that makes cross-entropy click

`−log ŷ` where `ŷ` is the probability assigned to the *correct* class. A loss
of **ln(10) = 2.303** on a 10-class problem means the model is assigning 1/10
to the right answer — **it knows nothing**. That number shows up as the
starting loss in every 10-class run in this course, and in
[experiment 4](lab.md#experiment-4) the `lr = 0.0001` row is diagnosed as
"barely moved off ln(10)" for exactly that reason.

---

## 1.8 Gradient descent and backpropagation, conceptually

### 📖 Gradient descent

Repeat: **w ← w − η ∂L/∂w**. The gradient points uphill; step against it.

| Variant | Batch size | Trade-off |
|---|---|---|
| **Batch** | all n | smooth, exact, slow, needs all data in memory |
| **Stochastic (SGD)** | 1 | noisy, fast per step, the noise can escape shallow minima |
| **Mini-batch** | 32–256 | **what everyone actually uses** — vectorises well, noise is useful |

### 📖 Backpropagation in one paragraph

Backpropagation is **the chain rule, applied efficiently**. A forward pass
computes and stores each layer's output. A backward pass starts with
`∂L/∂output` and walks backwards, at each layer turning the gradient with
respect to its output into the gradient with respect to its weights *and* the
gradient with respect to its input, which is what the previous layer needs.

> **The efficiency claim is the point.** Naively computing each parameter's
> derivative separately would cost one forward pass per parameter.
> Backpropagation gets all of them in **one** backward pass, at roughly the
> cost of the forward pass. Unit 2 does the arithmetic on a concrete network.

### ⚠️ What "conceptual only" means for your exam

The syllabus says backpropagation is conceptual in this unit. **You still need
to be able to state:** that it is the chain rule; that it requires storing the
forward activations (which is why memory scales with depth × batch size); that
it needs the activation to be differentiable; and that the gradient is a
*product* along the chain — which is the whole reason vanishing and exploding
gradients exist.

---

## What to be able to do after this unit

- [ ] State the AI ⊃ ML ⊃ DL nesting and name the distinguishing feature
- [ ] **Prove** in four lines that no perceptron computes XOR
- [ ] Explain why a stack of linear layers is one linear layer
- [ ] Give the formula, range and derivative bound of all five activations
- [ ] Explain the vanishing gradient using `0.25ⁿ`
- [ ] Say why softmax must subtract the maximum
- [ ] Justify cross-entropy over MSE for classification
- [ ] State what backpropagation computes and why it is efficient

**Cross-check yourself:** run
`01_perceptron_scratch.py`.
Every number quoted in this unit is printed by it.
