# Unit 4 — Recurrent Neural Networks and NLP

**Syllabus topics:** Sequences and time series data. Introduction to RNNs:
vanishing/exploding gradient issue. LSTM and GRU (intuitive and architectural
view). Word embeddings: Word2Vec, GloVe, introduction to contextual embeddings
(BERT at high level). Applications: Sentiment analysis, text generation,
simple time-series forecasting.

---

## 4.1 What makes a sequence different

A dense or convolutional network takes a **fixed-size** input and treats the
positions as independent features. A sequence has neither property: it can be
any length, and the meaning depends on the order.

| Property | Why a feedforward net cannot handle it |
|---|---|
| **variable length** | the input layer has a fixed width |
| **order matters** | "dog bites man" ≠ "man bites dog" |
| **long-range dependence** | the subject of a sentence can be 40 words from its verb |
| **shared structure across positions** | a feedforward net learns position 3 and position 30 separately |

### 📖 The recurrent answer

$$h_t = f(W_h h_{t-1} + W_x x_t + b) \qquad y_t = g(W_y h_t + c)$$

This is a **recurrent neural network**: **one set of weights, applied at every timestep**, with a hidden state `h`
carried forward. That is the whole idea: `W_h`, `W_x` and `W_y` do not depend
on `t`, so the network handles any length and shares what it learns across
positions — exactly the weight-sharing argument that made convolution work in
Unit 3, applied along time instead of space.

### 📖 The input/output shapes

| Pattern | Example |
|---|---|
| many-to-one | **sentiment analysis** — a sequence in, one label out |
| one-to-many | image captioning |
| many-to-many, aligned | part-of-speech tagging |
| many-to-many, unaligned | translation (encoder–decoder) |

---

## 4.2 The vanishing and exploding gradient

### 🔢 The arithmetic, exactly

Backpropagation through time multiplies the same recurrent weight at every
step. Over `T` steps the gradient carries a factor of roughly `wᵀ`:

| Sequence length | RNN gradient at `w = 0.5` | LSTM cell path |
|---|---|---|
| 5 | 3.12e-02 | 1.00 |
| 10 | 9.77e-04 | 1.00 |
| 50 | 8.88e-16 | 1.00 |
| 100 | 7.89e-31 | 1.00 |
| **500** | **3.05e-151** | **1.00** |
| **1100** | **0.00e+00** | **1.00** |

> ### ⚠️ Be precise about what "vanishes" means
>
> **3.05e-151 is not zero.** It is a perfectly representable float64, and
> saying "the gradient vanishes" as though floating point were the problem
> gets the mechanism wrong. The problem is that this gradient is so much
> smaller than the others in the sum that **it changes no weight by any
> amount you could measure.**
>
> Genuine underflow to exactly zero only happens past **T = 1074**, the last
> power of 0.5 a float64 can hold — the last row above. The lab asserts both
> facts.

**Exploding is the mirror image:** if `w > 1` the product grows without bound
and the weights become `nan` in a few steps. The fix is **gradient clipping**
— cap the gradient vector's norm before the update. It is a one-line change
and it is standard in every RNN implementation.

---

## 4.3 LSTM

### 📖 The architecture

An LSTM carries **two** things forward: a hidden state `h_t` and a **cell
state `c_t`**, controlled by three gates.

| Gate | Formula | Decides |
|---|---|---|
| **forget** `f_t` | `σ(W_f·[h_{t-1}, x_t] + b_f)` | how much of the old cell state to keep |
| **input** `i_t` | `σ(W_i·[h_{t-1}, x_t] + b_i)` | how much of the new candidate to write |
| **candidate** `g_t` | `tanh(W_g·[h_{t-1}, x_t] + b_g)` | what the new content would be |
| **output** `o_t` | `σ(W_o·[h_{t-1}, x_t] + b_o)` | how much of the cell to expose as `h_t` |

$$c_t = f_t \odot c_{t-1} + i_t \odot g_t \qquad h_t = o_t \odot \tanh(c_t)$$

### 🎯 The one sentence that answers "why LSTM?"

> **The cell state is an *additive* path.** `c_t = f·c_{t-1} + i·g` — with the
> forget gate near 1, the gradient along `c` is multiplied by something near
> **1** regardless of length, instead of by `w` at every step.
>
> **"An additive path instead of repeated multiplication"** is the whole
> answer, and it is what the table in 4.2 is showing.

### ⚠️ The exam detail on the forget gate bias

**Initialise the forget-gate bias to 1**, not 0. At bias 0 the sigmoid outputs
0.5, so the cell state halves at every step and the memory decays anyway. At
bias 1 it starts near 0.73 and the network can *learn* to forget rather than
having forgetting as its default.

---

## 4.4 GRU

Merges the forget and input gates into a single **update gate**, drops the
separate cell state, and adds a **reset gate**.

| Cell | Gates | Parameters vs RNN |
|---|---|---|
| RNN | none | 1× |
| **LSTM** | forget, input, output (+ cell state) | **4×** |
| **GRU** | reset, update | **3×** |

**GRU is usually indistinguishable from LSTM in accuracy and faster to train.**
It is a reasonable default; LSTM is the one you name in an exam.

---

## 4.5 The measurement: RNN vs LSTM vs GRU, twice

The lab runs the comparison on **two** datasets, deliberately, and they
disagree — which is the point.

### On a generated dataset with exactly one decisive word per sentence

| Cell | Parameters | Epoch 1 | Final |
|---|---|---|---|
| **RNN** | 3,002 | 0.5175 | **0.6600** |
| **LSTM** | 8,570 | 0.5175 | **0.9975** |
| **GRU** | 6,714 | 0.5300 | **1.0000** |

**A gap of +0.3375 between LSTM and RNN**, on sequences of only 20 tokens.

### On the real IMDb dataset

| Cell | Parameters | Epoch 1 | Final test |
|---|---|---|---|
| **RNN** | 326,402 | 0.5567 | **0.6523** |
| **LSTM** | 345,218 | 0.5927 | **0.7357** |
| **GRU** | 338,946 | 0.6090 | **0.7570** |

Majority-class baseline: **0.5130**. A gap of **+0.0833**, four times narrower.

> ### 💡 Why the gap narrowed, and why both numbers are worth having
>
> **Sentiment in a real review is redundant.** "Terrible", "waste", "boring"
> and "awful" may all appear in the same paragraph, so a model that catches
> any one of them scores. The generated task had **exactly one** decisive word
> per sentence and no redundancy at all, which is what made the gap so wide.
>
> **Both numbers are real; they measure different things.** Reporting only the
> one that flatters the LSTM would be the dishonest version of this lab.

### 🎯 And the check only a generated dataset can give you

Feed the trained LSTM a **single word** and read off the probability it
assigns:

| Word group | Mean P(positive) | n |
|---|---|---|
| POSITIVE vocabulary | **0.9998** | 10 |
| NEGATIVE vocabulary | **0.0002** | 10 |
| neutral filler | 0.8332 | 6 |

**The model found exactly the right words.** On IMDb you can measure accuracy
and you *cannot* verify what the model attended to. That is why a built
dataset is the better teaching tool even though it is the smaller achievement.

---

## 4.6 Word embeddings

### 📖 Why one-hot is not enough

A one-hot vector for a 10,000-word vocabulary is 10,000 numbers, almost all
zero, and **every pair of words is equidistant** — "cat" is exactly as far
from "dog" as from "hydroelectric". The representation carries no meaning.

An embedding is a dense, learned vector — typically 50 to 300 numbers — in
which **distance means something.**

| Method | Year | How it learns |
|---|---|---|
| **Word2Vec** (skip-gram) | 2013 | predict the context words from the centre word |
| **Word2Vec** (CBOW) | 2013 | predict the centre word from its context |
| **GloVe** | 2014 | factorise the global word **co-occurrence** matrix |
| **fastText** | 2016 | Word2Vec over character n-grams — handles unseen words |

### 🎯 The distributional hypothesis

> **"You shall know a word by the company it keeps."** (Firth, 1957)
>
> Every method above is a way of operationalising that one sentence. Words
> appearing in similar contexts get similar vectors — and that is *all* the
> supervision there is.

### 📖 The famous property, stated carefully

$$\text{king} - \text{man} + \text{woman} \approx \text{queen}$$

**Vector arithmetic captures analogies** because the offset between "man" and
"woman" is roughly the same as between "king" and "queen".

> ⚠️ **And the same property encodes the corpus's biases.** `doctor − man +
> woman ≈ nurse` is a real, reproducible result on standard embeddings. The
> geometry has no notion of which analogies are facts about language and which
> are prejudices in the training text — it learned both from the same
> statistics. **Unit 5's section on bias is not a separate topic from this
> one.**

### 📖 Contextual embeddings — what BERT changed

Word2Vec and GloVe give each word **one** vector, for ever. So "bank" has a
single vector that has to serve both the river and the money.

**BERT gives a different vector for every occurrence**, computed from the whole
sentence. "River bank" and "savings bank" get different vectors, because the
representation is a function of the context.

| | Word2Vec / GloVe | BERT |
|---|---|---|
| vectors per word | **one** | **one per occurrence** |
| trained by | predicting nearby words | **masked language modelling** — hide 15% of tokens, predict them |
| direction | — | **bidirectional** — sees left and right context at once |
| architecture | shallow | transformer encoder stack (Unit 5) |

> **BERT is the mechanism of Unit 5 applied to the problem of this one.** The
> lab cannot download BERT — `huggingface.co` is refused at the gateway — but
> `11_attention.py`
> implements and trains the attention mechanism BERT is built from, and
> `12_huggingface_app.md`
> carries the pipeline code marked NOT EXECUTED.

---

## 4.7 Text generation

### 📖 A character-level RNN

Train on the task "given the last `n` characters, predict the next one", then
sample repeatedly, feeding each output back in.

### 🔢 Temperature — the knob every generation API exposes

Before sampling, divide the logits by a **temperature** `T`:

$$p_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

| `T` | Effect | The lab's output |
|---|---|---|
| **0.2** | conservative, repetitive | `'the loss falls when the weights move down the gradient. the quick brow'` |
| **0.7** | balanced | `'the quick brown fox jumps over the lazy dog. a neural network learns a'` |
| **1.5** | creative, error-prone | `'the loss falls when qunt fomplex ones. an attention head compares ethe'` |

> **Low temperature is safe and boring; high temperature is creative and
> wrong.** `T → 0` is greedy argmax; `T → ∞` is uniform random. This is the
> same knob every LLM API exposes, and it is worth knowing when somebody asks
> why a model "made something up".

### ⚠️ What the experiment makes obvious

**A character RNN learns spelling and local grammar** — those are decided
within a few characters — **and it does not learn what a sentence is about**,
because that dependency is hundreds of characters long. **That gap is exactly
what attention was invented to close**, which is Unit 5.

---

## 4.8 Simple time series forecasting

An RNN can forecast a **time series**: feed `y_{t−n} … y_{t−1}`, predict
`y_t`.

> ### 💡 But read Course 14 B before you reach for one
>
> The Track B course measures this directly: on a 120-month sales series,
> **SARIMA reached RMSE 6.891 and Holt-Winters 5.259**, while a gradient-
> boosted tree on lag features managed 11.318. **Classical methods win on
> short, clean, seasonal series**, and a neural network needs far more data
> than a typical business series contains.
>
> Use an RNN for sequences when the input is high-dimensional (text, audio,
> sensor arrays) or when you have many related series. For one univariate
> monthly series, fit an ARIMA.

---

## What to be able to do after this unit

- [ ] Write the RNN recurrence and say why the weights are shared across `t`
- [ ] Name the four many-to-* patterns with an example of each
- [ ] Explain the vanishing gradient as `wᵀ` — **and be precise that 3e-151 is not zero**
- [ ] Give the three LSTM gates, their formulas, and what each decides
- [ ] Answer "why LSTM?" in one sentence about the additive path
- [ ] Say why the forget-gate bias is initialised to 1
- [ ] Give the GRU's two gates and its parameter ratio
- [ ] Explain what an embedding buys over one-hot, and how Word2Vec learns it
- [ ] State what BERT changed about embeddings, and how it is trained
- [ ] Explain the temperature parameter and its two limits

**Cross-check yourself:** run
`09_rnn_lstm.py`. Both
comparison tables, the single-word probe and the temperature samples are
printed by it.
