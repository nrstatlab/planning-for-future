# Unit 5 — Advanced and Emerging Topics

**Syllabus topics:** Generative models: GANs (Generator & Discriminator
intuition), VAEs (introduction only). Transformers: attention mechanism
(intuitive), BERT, GPT family (overview). Transfer learning & fine-tuning
pre-trained models (vision & NLP). AI ethics: Bias, fairness, privacy, safety,
explainability.

---

## 5.1 Attention, which is the core of the unit

### 📖 The one equation

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^{T}}{\sqrt{d_k}}\right)V$$

| Symbol | Name | Think of it as |
|---|---|---|
| **Q** | query | what this position is looking for |
| **K** | key | what each position advertises |
| **V** | value | what each position actually contributes |

### 🔢 A worked example you can check by hand

The lab uses numbers chosen so the answer is obvious. One query, three keys,
`d_k = 4`:

```
Q = [1, 0, 0, 0]
K = [[1, 0, 0, 0],      identical to Q
     [0, 1, 0, 0],      orthogonal to Q
     [0.7, 0.7, 0, 0]]  partly aligned
V = [[10, 0], [0, 10], [5, 5]]
```

| Step | Value |
|---|---|
| raw scores `Q·Kᵀ` | `[1.0, 0.0, 0.7]` |
| scaled by `√d_k = 2.0` | `[0.5, 0.0, 0.35]` |
| attention weights (softmax) | **`[0.4053, 0.2458, 0.3489]`** |
| output = weights @ V | **`[5.7974, 4.2026]`** |

**The query matched key 0 exactly, key 2 partly, key 1 not at all — and the
weights rank them in exactly that order.**

> ### 🎯 The one sentence
>
> **Attention is a soft, learned lookup table.** The output is a weighted
> average of the values, weighted by how well each key matched the query.
> Everything else in a transformer is plumbing around that.

### 🔢 Why divide by √d_k — measured, not asserted

The dot product of two random `d_k`-dimensional vectors has a standard
deviation that grows as `√d_k`. The lab measures it:

| `d_k` | std of `Q·K` | std ÷ `√d_k` | max softmax weight |
|---|---|---|---|
| 4 | 2.025 | 1.013 | 0.1615 |
| 16 | 3.997 | 0.999 | 0.4230 |
| 64 | 8.060 | 1.008 | 0.7146 |
| 256 | 15.655 | 0.978 | 0.5659 |
| **1024** | **33.167** | 1.036 | **0.9857** |

> **At `d_k = 1024` one weight goes to ~0.99 and the rest to ~0.** The softmax
> **saturates**, its gradient vanishes, and the model stops learning.
>
> **Dividing by `√d_k` holds the score variance at 1 whatever the dimension** —
> the third column shows it working. That is the entire reason for the scaling
> factor, and it is the detail most people cannot explain in a viva.

### 📖 Multi-head attention

Run `h` attention operations in parallel on `d_model/h`-dimensional
projections, concatenate, and project back.

**Why:** one attention head produces one weighted average, so it can express
one kind of relationship. **Eight heads can attend to eight different things
at once** — one tracking syntax, another coreference, another position — and
the concatenation lets the next layer use all of them.

### 📖 The transformer encoder block

```
x → multi-head self-attention → add & layer-norm
  → feed-forward (d_model → 4·d_model → d_model) → add & layer-norm
```

| Component | Why it is there |
|---|---|
| **self-attention** | mixes information *between* positions |
| **feed-forward** | transforms each position *independently* — this is where most parameters live |
| **residual (add)** | gives the gradient a path that skips the block — the same additive-path idea as the LSTM cell state |
| **layer norm** | stabilises the scale, per example rather than per batch |

### ⚠️ Positional encoding, and an honest null result

**Attention is permutation-equivariant**: shuffle the input and the outputs
shuffle with it. It has *no* notion of order, which is why position must be
added to the input explicitly — either as fixed sinusoids or as learned
vectors.

The lab ablates it:

| | Test accuracy |
|---|---|
| with positional encoding | **1.0000** |
| **without** positional encoding | **1.0000** |

> **Barely any difference — and that is the correct result for *this* task.**
> The lab's sentiment task is a bag-of-words problem: the label depends on
> *which* sentiment word appears, not on where. So order carries no
> information and removing the position signal costs nothing.
>
> **On translation or parsing, removing them is catastrophic.** Reporting the
> null result honestly is better than choosing a task that flatters the claim.

### 🎯 Attention weights are not an explanation

The lab's dataset is built so the decisive word in every sentence is known.
Scoring the attention map against it:

**The sentiment word was the most-attended token in 111/120 = 92.5% of
sentences.**

> **Note the rate is 92.5%, not 100%.** A model can reach the right answer
> while attending elsewhere, because information also flows through the
> residual stream and the feed-forward layer. **"Attention is
> interpretability" is a claim that has been argued down in the literature**,
> and this number is a small piece of why. It is also a check a downloaded
> model cannot give you.

### 🔢 Why attention replaced recurrence, and what it cost

| | RNN / LSTM | Self-attention |
|---|---|---|
| parallel over the sequence | **no — inherently serial** | **yes** |
| compute per layer | `O(T·d²)` | **`O(T²·d)`** |
| memory | `O(T·d)` | **`O(T²)`** |
| long dependencies | gradient decays | **direct connection** |
| needs position info | implicit in the order | **must be added** |

**The parallelism is why transformers won** — an RNN cannot start step `t`
until step `t−1` finishes, so it cannot use a GPU properly.

**The `O(T²)` is the price**, and it is the whole reason context windows are a
topic:

| Sequence length | Attention scores | vs T=512 |
|---|---|---|
| 512 | 262,144 | 1× |
| 1,024 | 1,048,576 | **4×** |
| 4,096 | 16,777,216 | **64×** |

Doubling the context **quadruples** the cost. Every "long context" technique —
sparse attention, sliding windows, FlashAttention, linear attention — exists
to attack this one line.

---

## 5.2 BERT and GPT

| | **BERT** (2018) | **GPT** (2018–) |
|---|---|---|
| Architecture | transformer **encoder** | transformer **decoder** |
| Attention | **bidirectional** — sees left and right | **causal** — masked to see only the left |
| Trained by | **masked language modelling** — hide 15% of tokens, predict them | **next-token prediction** |
| Natural at | *understanding*: classification, NER, QA | *generation* |
| Used by | fine-tuning a task head | prompting, or fine-tuning |

### 🎯 The distinction that gets examined

**BERT cannot generate text**, because it sees the whole sentence at once —
there is no "next" token in its training objective. **GPT cannot use
right-hand context**, because its attention is causally masked. The masking is
the entire architectural difference; both are stacks of the same block.

---

## 5.3 Transfer learning and fine-tuning

### 📖 The idea

A network trained on a large dataset has learned features that are **generic**
in its early layers. Keep those, replace the task-specific head, and train on
your small dataset.

### 🔢 The measurement — real MobileNetV2 and VGG16 on 500 images

[Experiment 8](lab.md#experiment-8), Fashion-MNIST, 50 images per class:

| Approach | Total params | **Trainable** | Test accuracy |
|---|---|---|---|
| CNN from scratch | 105,866 | 105,866 | 0.7810 |
| dense head on raw pixels | 50,890 | 50,890 | 0.7500 |
| **MobileNetV2 frozen + new head** | 2,340,618 | **82,634** | **0.8260** |
| VGG16 frozen + new head | 14,748,170 | 33,482 | **0.7660** |

**Transfer won: 0.8260 against 0.7810 from scratch.** ImageNet's filters never
saw a shoe on a black background, and they transferred anyway — because the
early layers of any vision model learn edges, corners and textures, and those
are the same features whatever the pictures are of.

### ⚠️ Two results that contradict the usual story

> **1. VGG16 lost to a small CNN trained from scratch** — 0.7660 against
> 0.7810, and 3.7× slower than MobileNetV2 for the privilege. **Bigger is not
> better.** VGG16's features are tuned for 224×224 photographs; at 96×96 on
> upscaled grayscale it is far outside what it was built for.
>
> **Benchmark the pre-trained model you chose against a small model you
> trained yourself.** Most people never run that baseline.

> **2. Fine-tuning made it *worse*.** Unfreezing MobileNetV2's top 20 layers
> at `lr = 1e-4` gave **0.7760**, against **0.8260** for the frozen features.
>
> Count the parameters: unfreezing put **1,135,114** weights under gradient
> descent with **500** training images — about **2,270 parameters per
> example.** The network has more than enough freedom to fit the 500 images
> exactly, and what it fits is their noise.

### 🎯 The rule the measurement actually supports

> **How much you unfreeze must scale with how much data you have.**
>
> | Data | Strategy |
> |---|---|
> | hundreds of images | **freeze everything, train a head** |
> | thousands | unfreeze the top block |
> | tens of thousands | fine-tune the whole network |
>
> The small learning rate (`1e-4`, not `1e-3`) is still right and still
> necessary — so the first large gradients do not erase the features you came
> for — **it is just not sufficient.** "Use a small learning rate" is the
> advice everyone repeats; "unfreeze in proportion to your data" is the one
> that would have prevented that number.

### 💡 And why the head must be thrown away

Feeding the pre-trained classifier a Fashion-MNIST pullover, ImageNet's top-3
guesses are **`lab_coat` (0.1561), `sweatshirt` (0.0421), `pill_bottle`
(0.0375)**.

**ImageNet has 1,000 classes and none of them is "pullover".** The classifier
head is useless for this task — which is exactly why transfer learning keeps
the convolutions and discards the head.

---

## 5.4 Generative models

### 📖 GANs — the two-player game

| Player | Job | Loss |
|---|---|---|
| **Generator** `G` | map noise `z` to a fake sample | wants `D` to call its output real |
| **Discriminator** `D` | tell real from fake | wants to be right |

They train **against each other**. At the ideal equilibrium `G`'s output
distribution matches the data and `D` is reduced to guessing — 50%.

### ⚠️ Why GANs are famously hard to train

| Failure | What it looks like |
|---|---|
| **Mode collapse** | `G` finds one output that fools `D` and produces only that |
| **Non-convergence** | the two losses oscillate instead of settling |
| **Vanishing gradient** | `D` gets too good too fast, so `G` gets no usable signal |

**There is no single loss curve to watch.** A falling generator loss can mean
the generator improved *or* that the discriminator got worse — which is why
GAN papers show samples rather than curves.

### 📖 VAEs — introduction only

An autoencoder compresses input to a latent code and reconstructs it. A
**variational** autoencoder makes the latent a **distribution** — the encoder
outputs a mean and a variance, and the loss adds a KL term pulling that
distribution toward a standard normal.

**Why the KL term matters:** it makes the latent space *continuous*, so you
can sample a random point and decode something sensible. A plain autoencoder's
latent space has holes.

| | GAN | VAE |
|---|---|---|
| Sample quality | **sharper** | blurrier |
| Training stability | **hard** | stable |
| Latent space | not directly interpretable | **smooth and samplable** |
| Loss | adversarial | reconstruction + KL |

---

## 5.5 AI ethics

This is examinable, and it is not a soft topic — each item below has a
concrete mechanism.

### ⚠️ Bias

**The model learns the statistics of its training data, including the ones you
did not want.**

| Example | Mechanism |
|---|---|
| `doctor − man + woman ≈ nurse` in standard embeddings | Unit 4's distributional hypothesis, applied to a biased corpus |
| A hiring model that penalises women's colleges | the historical labels encoded the historical decisions |
| Face recognition with far higher error rates on darker skin | the training set was not representative |

**The lab's own version of this:** the
Teachable Machine exercise
has you deliberately photograph one class against a window and the other
against a dark wall. Accuracy looks perfect; swap the backgrounds and it
collapses. **The model learned the background.** That five-minute experiment is
the same failure behind a string of real medical-imaging papers that turned
out to be detecting which hospital took the scan.

### 📖 Fairness — and why the definitions conflict

| Definition | Requires |
|---|---|
| **Demographic parity** | equal positive rate across groups |
| **Equalised odds** | equal true-positive *and* false-positive rate |
| **Calibration** | a predicted 0.7 means 70% for every group |

> **These are provably incompatible** when base rates differ between groups
> (Kleinberg et al., 2016). You cannot satisfy all three. **Choosing which one
> your application needs is a decision about values, not a technical
> optimisation** — and that sentence is what an exam question on fairness is
> looking for.

### 📖 Privacy

| Risk | Mitigation |
|---|---|
| Models **memorise** training data and can be made to emit it | **differential privacy** — bounded noise in training |
| Data must be centralised to train | **federated learning** — train on device, share gradients |
| Model inversion reconstructs training examples | limit query access; add output noise |

### 📖 Safety and explainability

| Concern | Note |
|---|---|
| **Adversarial examples** | an imperceptible perturbation flips the prediction — a genuine security issue for anything vision-based |
| **Distribution shift** | the model is confidently wrong on inputs unlike its training data |
| **Explainability** | LIME, SHAP, saliency maps, attention maps |

> ### ⚠️ And the caveat this course has already measured
>
> **Attention maps are not explanations.** The lab scored them against a known
> ground truth and got **92.5%** — high, but not an explanation, and the
> remaining 7.5% are cases where the model was right while attending
> elsewhere. **Every post-hoc explanation method has a version of this
> problem: it produces a plausible story, and plausibility is not
> correctness.**

---

## What to be able to do after this unit

- [ ] Write the attention equation and say what Q, K and V each mean
- [ ] Work through a small attention example by hand
- [ ] **Explain `√d_k` in terms of softmax saturation** — the classic viva question
- [ ] Say what multi-head attention buys over single-head
- [ ] Draw the encoder block and justify the residual and the layer norm
- [ ] Explain why positional encoding is needed, and when its absence does not matter
- [ ] Give the `O(T²)` cost and its consequence for context length
- [ ] State the architectural difference between BERT and GPT, and what each cannot do
- [ ] Give the transfer-learning strategy for three different dataset sizes
- [ ] Explain mode collapse, and why GAN losses are not diagnostic
- [ ] Say what the KL term does in a VAE
- [ ] **State why the three fairness definitions cannot all be satisfied**
- [ ] Explain why attention maps are not explanations

**Cross-check yourself:** run
`11_attention.py` and
`08_pretrained.py`.
Every number in this unit is printed by one of them.
