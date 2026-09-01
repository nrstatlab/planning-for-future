# Course 14 A — Practice Questions with Worked Solutions

Grouped by unit. **Attempt each before reading the solution.** Every numeric
answer that comes from the lab is marked with the file that printed it.

---

## Unit 1 — Foundations

### Q1. Prove that a single perceptron cannot compute XOR. *(6 marks)*

<details><summary>Solution</summary>

A perceptron outputs 1 when `w₁x₁ + w₂x₂ + b > 0`. XOR requires:

| Point | Required output | Constraint |
|---|---|---|
| (0,0) | 0 | `b ≤ 0` |
| (0,1) | 1 | `w₂ + b > 0` ⟹ `w₂ > −b ≥ 0` |
| (1,0) | 1 | `w₁ + b > 0` ⟹ `w₁ > −b ≥ 0` |
| (1,1) | 0 | `w₁ + w₂ + b ≤ 0` |

From rows 2 and 3, `w₁ + w₂ > −2b`. Since `b ≤ 0`, `−2b ≥ −b`, so
`w₁ + w₂ + b > −2b + b = −b ≥ 0`.

**This contradicts row 4**, which requires `w₁ + w₂ + b ≤ 0`. No weights
exist. ∎

**Verified:** `01_perceptron_scratch.py` reports XOR accuracy **0.50**,
converged **never**, while AND, OR and NAND converge in 6, 4 and 4 epochs.
</details>

### Q2. Why does a deep network need non-linear activations? *(4 marks)*

<details><summary>Solution</summary>

Composing linear maps gives a linear map:

`W₃(W₂(W₁x)) = (W₃W₂W₁)x = Wx`

**A hundred linear layers compute the same function class as one.** Depth adds
representational power *only* through the non-linearity between layers.

**A common half-answer:** "to introduce non-linearity." State the collapse
explicitly — that is where the marks are.
</details>

### Q3. Explain the vanishing gradient using sigmoid's derivative. *(5 marks)*

<details><summary>Solution</summary>

`σ'(z) = σ(z)(1 − σ(z))`, maximised at `z = 0` where `σ = 0.5`, giving
`0.5 × 0.5 = 0.25`. **So `σ' ≤ 0.25` everywhere.**

Backpropagation multiplies one such factor per layer, so over `n` layers the
gradient carries roughly `0.25ⁿ`:

| Layers | Best case |
|---|---|
| 10 | 9.54e-07 |
| **50** | **7.89e-31** |

The gradient reaching layer 1 is ~30 orders of magnitude smaller than at layer
50, so the early layers receive no usable signal. **ReLU's derivative is
exactly 1 where the unit is active**, so the product does not shrink.

**Verified:** `01_perceptron_scratch.py`.
</details>

### Q4. Why must softmax subtract the maximum? *(4 marks)*

<details><summary>Solution</summary>

`exp(1000)` overflows to `inf`, and `inf/inf = nan`.

Subtracting the maximum is **mathematically identity** — multiplying numerator
and denominator by `e^{−max}` cancels — and numerically essential, because the
largest exponent becomes `e⁰ = 1`.

| Implementation | `softmax([1000, 1001, 1002])` |
|---|---|
| naive | **`nan`** |
| stable | `[0.0900, 0.2447, 0.6652]` |

**Verified:** `01_perceptron_scratch.py`.
</details>

### Q5. Why cross-entropy rather than MSE for classification? *(5 marks)*

<details><summary>Solution</summary>

Take true class 1, prediction `ŷ = 0.01`:

| Loss | Value | Gradient behaviour |
|---|---|---|
| MSE | `(1 − 0.01)² = 0.98` | bounded; **shrinks** when sigmoid saturates |
| Cross-entropy | `−log(0.01) = 4.61` | large; **does not vanish** with saturation |

Cross-entropy is **unbounded as `ŷ → 0`**, so a confidently wrong prediction
produces a large gradient — exactly what you want. MSE with a sigmoid gives
the *smallest* gradient precisely when the model is most wrong.

**Bonus:** with softmax, cross-entropy's output gradient simplifies to
`dz = a − y`.
</details>

---

## Unit 2 — Training deep networks

### Q6. A network trains to 10% accuracy on 10 classes with loss stuck at 2.30. Diagnose. *(5 marks)*

<details><summary>Solution</summary>

**`ln(10) = 2.303` is the loss of a model assigning 1/10 to every class — it
has learned nothing.** 10% is chance. Two distinct causes:

| Cause | Distinguishing symptom | Fix |
|---|---|---|
| **learning rate far too small** | loss falls, extremely slowly | raise it |
| **learning rate far too large** | loss **rises** or goes `nan` | lower it |
| **all-zero initialisation** | loss flat from step 1, both train and test | random init |

**Check whether the loss moved at all, and in which direction.** The lab shows
both failures:

| lr | Final train loss | Test acc | Behaviour |
|---|---|---|---|
| 10.0 | **14.5063** | 0.1000 | diverged — loss went **up** |
| 0.0001 | 2.2373 | 0.1920 | too slow — barely off 2.303 |

**Verified:** `04_deep_network.py`.

**The trap:** a student who sees 0.1000 and concludes "the model is too small"
will make it bigger and fail again.
</details>

### Q7. What is the symmetry problem, and how does initialisation solve it? *(5 marks)*

<details><summary>Solution</summary>

If all weights in a layer start equal, every unit computes the same output,
receives the same gradient, and updates identically — **for ever**. A 64-unit
layer behaves exactly like a 1-unit layer.

Random initialisation breaks the symmetry. The **scale** matters too:

| Scheme | Variance | For |
|---|---|---|
| Glorot / Xavier | `1/fan_in` | tanh, sigmoid |
| **He** | `2/fan_in` | **ReLU** |

**He's factor of 2:** ReLU zeroes about half its inputs, halving the output
variance; doubling the initial variance restores it, so the signal neither
shrinks nor explodes through depth.

**Verified:** `04_deep_network.py` — zeros give **0.1000** at epoch 1 and
**0.1000** at the end, while Glorot reaches 0.9340 and He 0.9400.
</details>

### Q8. Distinguish dropout from batch normalisation. Why must both know train vs eval mode? *(6 marks)*

<details><summary>Solution</summary>

| | Dropout | Batch norm |
|---|---|---|
| Does | zeroes a random fraction of activations | normalises pre-activations to zero mean, unit variance, then rescales with two learned parameters |
| Purpose | regularisation — an implicit ensemble over 2ⁿ sub-networks | stabilises the distribution each layer sees |
| Parameters | none | 2 per channel (γ, β) |
| At training | **active** | uses **batch** statistics |
| At inference | **off entirely** | uses **running averages** |

**Both behave differently in the two modes**, so the model must be told which
it is in — `model.eval()` in PyTorch, `training=False` in Keras. Forgetting it
silently corrupts every evaluation, and the symptom is a test score that
jitters between runs.

**Measured:** dropout 0.5 gave the smallest train/test gap (**0.0335** vs
0.0510) while **batch norm gave the best test score (0.9530)**. They answer
different questions — report both columns.
</details>

### Q9. A model gets train 1.0000, test 0.9490. Diagnose and give three fixes. *(5 marks)*

<details><summary>Solution</summary>

**Overfitting** — the training score is perfect and the test score is not, a
gap of 0.0510.

The cause is capacity relative to data: **335,114 parameters for 4,000 images,
about 84 per example.** The network can memorise the training set outright.

Three fixes, in order of usual effectiveness:

1. **More data** (or data augmentation — cheapest and often the most effective)
2. **Regularisation** — dropout, L2 weight decay, batch norm
3. **Early stopping**, or simply a smaller network

**And the honest caveat the lab supplies:** the best regulariser here moved
test accuracy from 0.9490 to 0.9530 — four examples in a thousand. **On this
data, regularisation is a refinement, not a transformation.**
</details>

---

## Unit 3 — CNNs

### Q10. A 32×32×3 image enters conv(16 filters, 5×5, padding 2, stride 1) then maxpool 2×2. Give the output shape and the parameter count. *(5 marks)*

<details><summary>Solution</summary>

**Conv output size:** `floor((32 + 2(2) − 5)/1) + 1 = floor(31) + 1 = 32`

So conv output is **32 × 32 × 16**.

**Conv parameters:** `(k × k × C_in + 1) × C_out = (5 × 5 × 3 + 1) × 16
= 76 × 16 = ` **1,216**

**After maxpool 2×2 (stride 2):** `floor((32 − 2)/2) + 1 = 16`, so
**16 × 16 × 16**. **Pooling has 0 parameters.**
</details>

### Q11. Why do two stacked 3×3 convolutions beat one 5×5? *(5 marks)*

<details><summary>Solution</summary>

**Same receptive field, fewer parameters, more non-linearity.**

| | Parameters (per channel pair) | Non-linearities |
|---|---|---|
| one 5×5 | 25 | 1 |
| **two 3×3** | **18** | **2** |

Three 3×3 convs give a 7×7 field for 27 weights against 49.

**This is the VGG insight**, and it is why 3×3 is the near-universal default.
</details>

### Q12. In a classical CNN, where do the parameters actually live? What is the modern fix? *(5 marks)*

<details><summary>Solution</summary>

**In the first dense layer, not in the convolutions.** From the lab's
LeNet-shaped net:

| | Parameters |
|---|---|
| conv1 + conv2 | **3,424** |
| **fc1 (784 → 64)** | **50,240** |

**The convolutions do the work and the dense layers hold the weights.**

**The fix:** replace `flatten` with **global average pooling** — take the mean
of each feature map, giving one number per channel. That deletes ~90% of the
parameters and usually improves generalisation, because it removes the layer
most able to memorise.

**Verified:** `06_cnn.py`.
</details>

### Q13. "CNNs learn edge detectors." Evaluate this claim against evidence. *(6 marks)*

<details><summary>Solution</summary>

**The claim is true in the regime it came from and not universal.**

The famous figure is AlexNet's first layer: **96 filters at 11×11 on 224×224
colour photographs.** With that capacity and that data, filters specialise
into clean oriented edges and Gabor patches.

**The lab measures the same property on 8 filters at 5×5 on 28×28 grayscale
Fashion-MNIST**, calling a kernel oriented when its gradient along one axis
exceeds the other by 1.6×:

**0 of 8 kernels are clearly oriented.**

**The correct conclusion:** with 8 filters the network does not *need* 8
distinct edge detectors, so it does not learn them. Not every filter learns
something a human can name. **A lab report claiming otherwise has not looked.**
</details>

### Q14. The CNN drops 0.3940 under a 3-pixel shift; the MLP drops 0.5980. Interpret. *(5 marks)*

<details><summary>Solution</summary>

**Both degrade badly, and the CNN degrades less.**

**Why the CNN is better:** pooling gives partial translation invariance, and
weight sharing means the same kernel detects a feature wherever it appears.
The MLP learned a weight for every *absolute* pixel position, so a shift moves
the evidence to weights that never saw it.

**Why the CNN still fails:** a 3-pixel shift on a 28-pixel image is a large
perturbation, and neither model was trained with augmentation. Two pooling
layers give invariance to roughly ±2 pixels, not ±3.

> **The practical lesson: if you need shift invariance, train for it with data
> augmentation.** The architecture gives a head start, not the property.
</details>

---

## Unit 4 — RNNs

### Q15. Why does an LSTM handle long sequences better than a plain RNN? *(6 marks)*

<details><summary>Solution</summary>

**A plain RNN multiplies** the same recurrent weight at every step, so the
gradient carries `wᵀ`:

| T | gradient at w = 0.5 |
|---|---|
| 50 | 8.88e-16 |
| 100 | 7.89e-31 |
| 500 | **3.05e-151** |

**The LSTM's cell state is an *additive* path:** `c_t = f·c_{t-1} + i·g`. With
the forget gate near 1, the gradient along `c` is multiplied by ~**1**
regardless of length.

> **"An additive path instead of repeated multiplication"** is the
> one-sentence answer.

**A precision mark:** 3.05e-151 is **not zero** — it is a perfectly
representable float64. The problem is that it is negligible *relative to the
other gradients in the sum*, not that floating point failed. Genuine underflow
to exactly 0.0 needs T > 1074.

**Verified:** `09_rnn_lstm.py` asserts both facts.
</details>

### Q16. Name the LSTM gates and state what each decides. Why is the forget bias initialised to 1? *(6 marks)*

<details><summary>Solution</summary>

| Gate | Decides |
|---|---|
| **forget** `f_t` | how much of the old cell state to keep |
| **input** `i_t` | how much of the new candidate to write |
| **candidate** `g_t` | what the new content would be (tanh) |
| **output** `o_t` | how much of the cell to expose as `h_t` |

`c_t = f_t ⊙ c_{t-1} + i_t ⊙ g_t`, `h_t = o_t ⊙ tanh(c_t)`

**Forget bias = 1:** at bias 0 the sigmoid outputs 0.5, so the cell state
**halves at every step** and memory decays by default. At bias 1 it starts near
0.73, so the network must *learn* to forget rather than forgetting as its
default behaviour.
</details>

### Q17. An LSTM beats an RNN by 0.3375 on a generated dataset and by only 0.0833 on IMDb. Explain. *(6 marks)*

<details><summary>Solution</summary>

| Dataset | RNN | LSTM | Gap |
|---|---|---|---|
| generated, one decisive word per sentence | 0.6600 | 0.9975 | **+0.3375** |
| **real IMDb** | 0.6523 | 0.7357 | **+0.0833** |

**Sentiment in a real review is redundant.** "Terrible", "waste", "boring" and
"awful" may all appear in the same paragraph, so a weaker model that catches
*any one* of them still scores. The generated task had **exactly one** decisive
word per sentence and no redundancy, so missing it meant getting the example
wrong.

> **Both numbers are real and they measure different things.** Redundancy in
> real data masks differences between models — which is a general fact about
> benchmarking, not a fact about LSTMs.

**Verified:** `09_rnn_lstm.py`.
</details>

### Q18. What does the temperature parameter do? Give its two limits. *(4 marks)*

<details><summary>Solution</summary>

Divide the logits by `T` before the softmax: `p_i = exp(z_i/T) / Σ exp(z_j/T)`.

| `T` | Effect |
|---|---|
| **→ 0** | greedy **argmax** — always the single most likely token |
| low (0.2) | conservative, repetitive, safe |
| 0.7 | balanced |
| high (1.5) | creative and error-prone |
| **→ ∞** | **uniform random** |

**Low temperature is safe and boring; high temperature is creative and
wrong.** This is the same knob every LLM API exposes.

**Verified:** `09_rnn_lstm.py` prints samples at all three settings.
</details>

### Q19. What did BERT change about word embeddings? *(5 marks)*

<details><summary>Solution</summary>

**Word2Vec and GloVe give each word one vector, for ever.** So "bank" has a
single vector serving both the river and the money.

**BERT produces a different vector for every occurrence**, computed from the
whole sentence — a *contextual* embedding.

| | Word2Vec / GloVe | BERT |
|---|---|---|
| vectors per word | one | **one per occurrence** |
| trained by | predicting nearby words | **masked language modelling** (hide 15%, predict) |
| direction | — | **bidirectional** |
| architecture | shallow | transformer encoder stack |
</details>

---

## Unit 5 — Advanced topics

### Q20. Write the attention equation and explain why it divides by √d_k. *(6 marks)*

<details><summary>Solution</summary>

$$\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^{T}}{\sqrt{d_k}}\right)V$$

**The dot product of two random `d_k`-dimensional vectors has standard
deviation growing as `√d_k`.** Feed those raw scores to a softmax at large
`d_k` and one weight goes to ~1 and the rest to ~0 — **the softmax saturates,
its gradient vanishes, and the model stops learning.**

Dividing by `√d_k` holds the score variance at 1 whatever the dimension:

| `d_k` | std of `Q·K` | std ÷ `√d_k` | max softmax weight |
|---|---|---|---|
| 4 | 2.025 | **1.013** | 0.1615 |
| 64 | 8.060 | **1.008** | 0.7146 |
| 1024 | 33.167 | **1.036** | **0.9857** |

**The third column is the point** — the scaling works at every dimension.

**Verified:** `11_attention.py`.
</details>

### Q21. Given Q, K, V below, compute the attention output by hand. *(6 marks)*

```
Q = [1, 0, 0, 0]          V = [[10, 0],
K = [[1, 0, 0, 0],              [0, 10],
     [0, 1, 0, 0],              [5,  5]]
     [0.7, 0.7, 0, 0]]
```

<details><summary>Solution</summary>

1. **Scores** `Q·Kᵀ = [1.0, 0.0, 0.7]`
2. **Scale** by `√d_k = √4 = 2`: `[0.5, 0.0, 0.35]`
3. **Softmax:** `e^0.5 = 1.6487`, `e^0 = 1.0`, `e^0.35 = 1.4191`; sum = 4.0678
   → **`[0.4053, 0.2458, 0.3489]`**
4. **Output** = `0.4053·[10,0] + 0.2458·[0,10] + 0.3489·[5,5]`
   = `[4.053 + 1.745, 2.458 + 1.745]` = **`[5.7974, 4.2026]`**

**Sanity check:** the query matched key 0 exactly, key 2 partly, key 1 not at
all — and the weights rank them in that order. ✓

**Verified:** `11_attention.py`.
</details>

### Q22. Removing positional encoding changed accuracy from 1.0000 to 1.0000. Is the experiment broken? *(5 marks)*

<details><summary>Solution</summary>

**No. It is the correct result for this task, and reporting it is better than
hiding it.**

The lab's task is **bag-of-words**: the label depends on *which* sentiment word
appears, not on where. Order carries no information, so removing the position
signal costs nothing.

**What the null result does not mean:** that positional encoding is
unnecessary in general. Attention is **permutation-equivariant** — shuffle the
input and the outputs shuffle with it — so it has no notion of order at all.
**On translation or parsing, removing positional encoding is catastrophic.**

> **The methodological point:** an ablation that shows nothing has told you
> something about your *task*. Choosing a different task to make the claim
> look good would be the dishonest version.
</details>

### Q23. Attention identified the decisive word in 92.5% of sentences. Does that make attention an explanation? *(6 marks)*

<details><summary>Solution</summary>

**No, and the 7.5% is why.**

**What the number does show:** the model's attention correlates strongly with
the feature that actually determines the label — a check made possible *only*
because the dataset was constructed so the decisive word is known.

**Why it is not an explanation:**

1. **The other 7.5% got the right answer while attending elsewhere.** So high
   attention is not necessary for the prediction.
2. **Information also flows through the residual stream and the feed-forward
   layer**, neither of which the attention map shows.
3. Different attention distributions can produce identical outputs — so the
   map is not *identified* by the model's behaviour.

**"Attention is interpretability" has been argued down in the literature**, and
this measurement is a small piece of why. **The general lesson: every post-hoc
explanation method produces a plausible story, and plausibility is not
correctness.**
</details>

### Q24. You have 500 images and a pre-trained MobileNetV2. Frozen features gave 0.8260; fine-tuning the top 20 layers at lr=1e-4 gave 0.7760. Explain and give the rule. *(6 marks)*

<details><summary>Solution</summary>

**Count the parameters against the data.** Unfreezing put **1,135,114**
weights under gradient descent with **500** training images — about **2,270
parameters per example.** The network has more than enough freedom to fit the
500 images exactly, and what it fits is their **noise**.

> **The rule: how much you unfreeze must scale with how much data you have.**
>
> | Data | Strategy |
> |---|---|
> | hundreds | **freeze everything, train a head** |
> | thousands | unfreeze the top block |
> | tens of thousands | fine-tune the whole network |

**On the learning rate:** `1e-4` rather than `1e-3` is still right and still
necessary — so the first large gradients do not erase the pre-trained features
— **but it is not sufficient.** "Use a small learning rate" is the advice
everyone repeats; **"unfreeze in proportion to your data"** is the one that
would have prevented this number.

**Verified:** `08_pretrained.py`, real ImageNet weights.
</details>

### Q25. VGG16's frozen features scored 0.7660, below a small CNN trained from scratch at 0.7810. What does this show? *(5 marks)*

<details><summary>Solution</summary>

**That "use a bigger pre-trained model" is not a method.**

Three contributing reasons:

1. **Domain gap.** VGG16's features are tuned for 224×224 natural photographs
   with colour and texture statistics. Fashion-MNIST is 28×28 grayscale
   upscaled to 96×96 — almost none of that information is present.
2. **Architecture age.** VGG16 (2014) has 138 M parameters, most in dense
   layers, and no batch normalisation or residual connections.
3. **Cost.** It was **3.7× slower** than MobileNetV2, which scored 0.8260.

> **The methodological point: benchmark the pre-trained model you chose
> against a small model you trained yourself.** Most people never run that
> baseline and so never find out. It costs nine seconds here.
</details>

### Q26. State three fairness definitions and explain why you cannot satisfy all three. *(6 marks)*

<details><summary>Solution</summary>

| Definition | Requires |
|---|---|
| **Demographic parity** | equal positive prediction rate across groups |
| **Equalised odds** | equal true-positive **and** false-positive rate across groups |
| **Calibration** | a predicted 0.7 means 70% for **every** group |

**They are provably incompatible whenever the base rates differ between
groups** (Kleinberg, Mullainathan & Raghavan, 2016). A calibrated classifier on
groups with different prevalence must produce different error rates; forcing
equal error rates breaks calibration.

> **Therefore choosing which definition your application needs is a decision
> about values, not a technical optimisation.** That sentence is what the
> question is looking for.
</details>

### Q27. Describe the GAN training objective and two ways it fails. *(6 marks)*

<details><summary>Solution</summary>

**A two-player minimax game.** The generator `G` maps noise to fake samples;
the discriminator `D` classifies real vs fake. `D` maximises its accuracy; `G`
minimises `D`'s accuracy on its output. At the ideal equilibrium `G`'s
distribution matches the data and `D` is reduced to 50% — guessing.

| Failure | Symptom |
|---|---|
| **Mode collapse** | `G` finds one output that fools `D` and produces only that — no diversity |
| **Non-convergence** | the two losses oscillate rather than settling |
| **Vanishing gradient** | `D` becomes too good too fast, so `G` receives no usable signal |

> **And the practical consequence:** there is no single loss curve to watch. A
> falling generator loss may mean `G` improved **or** that `D` got worse. That
> is why GAN papers show samples rather than curves.
</details>

---

## Long-answer questions

### L1. Design a complete image-classification project for a 600-image, 6-class dataset. Justify every choice. *(15 marks)*

<details><summary>Solution outline</summary>

**1. Baselines first, before any deep model.**

| Baseline | Why |
|---|---|
| majority class | tells you what chance looks like given the class balance |
| logistic regression on raw pixels | tells you whether the problem is even hard |
| small CNN from scratch | the honest comparator for any transfer result |

**2. Split before anything else.** Stratified train/val/test. **Never** tune on
the test set. With 600 images, use cross-validation for the model choice and
hold out a genuine test set.

**3. Architecture: frozen pre-trained features + a new head.**
100 images per class is firmly in the "freeze everything" regime — the lab
measured what happens otherwise: fine-tuning 1.1 M parameters on 500 images
*lost* 5 points to the frozen version.

**4. Augmentation**, which matters more than architecture at this size:
random flips, small rotations, random crops, brightness jitter.

**5. Training:** Adam at `1e-3`, batch 32, early stopping on validation loss,
`ReduceLROnPlateau`.

**6. Evaluation:** accuracy **and** macro-F1 **and** the confusion matrix.
State the class balance so accuracy can be interpreted.

**7. The check that separates a good report from a demo:** compare against the
from-scratch CNN, and *read the errors*. If one class dominates the confusion
matrix, that is a data problem, not a model problem.

**8. Report the failure modes you tested for** — the deliberate
background-bias experiment from `02_playground.md` applied to your own data.
</details>

### L2. "Deep learning has made feature engineering obsolete." Discuss. *(15 marks)*

<details><summary>Solution outline</summary>

**The claim is true in a narrow domain and false as a general statement.**

**Where it holds:** images, audio and text, where the raw signal is
high-dimensional, the structure is local and hierarchical, and huge labelled
datasets exist. Hand-designed features (SIFT, HOG, MFCC) were genuinely
superseded.

**Where it does not:**

| Situation | Why features still matter |
|---|---|
| **Tabular data** | gradient-boosted trees still generally beat neural nets; domain features carry most of the signal |
| **Small data** | the lab's own measurement — 500 images, and the from-scratch CNN reached only 0.7810 |
| **Short univariate time series** | Course 14 B measured SARIMA at RMSE 6.891 and Holt-Winters at 5.259 against a gradient-boosted tree's 11.318 |
| **When you already know the feature** | `02_playground.md` §A3: adding the `X1X2` feature lets a *linear* model solve XOR instantly, with no hidden layer |

**The reframing that earns the marks:** deep learning does not remove the need
for domain knowledge — **it relocates it.** You now express it in the
architecture (convolution assumes locality; recurrence assumes order;
attention assumes relevance is learnable), in the augmentation policy, and in
the loss. A CNN *is* a hand-designed feature extractor; what is learned are its
coefficients.

**And the cost, measured:** experiment 4 bought three accuracy points for 7.5×
the parameters. Depth is a tool with a price, not a default.
</details>

---

## Quick self-test

Answer without looking anything up. If you cannot, reread the unit named.

| # | Question | Unit |
|---|---|---|
| 1 | Why is a stack of linear layers one linear layer? | 1 |
| 2 | What is sigmoid's maximum derivative, and why does it matter? | 1 |
| 3 | What loss value means "the model knows nothing" on 10 classes? | 1 |
| 4 | Give the two opposite causes of 10% accuracy on 10 classes | 2 |
| 5 | Why does He initialisation use `2/fan_in`? | 2 |
| 6 | What breaks if you forget `model.eval()`? | 2 |
| 7 | Give the conv output-size formula | 3 |
| 8 | Where do a classical CNN's parameters actually live? | 3 |
| 9 | Why two 3×3 convs rather than one 5×5? | 3 |
| 10 | Why is an LSTM's cell state an "additive path"? | 4 |
| 11 | What does the forget-gate bias of 1 prevent? | 4 |
| 12 | What does temperature do at `T → 0`? | 4 |
| 13 | Why divide attention scores by `√d_k`? | 5 |
| 14 | What is the cost of doubling a transformer's context length? | 5 |
| 15 | Which three fairness definitions conflict, and when? | 5 |
