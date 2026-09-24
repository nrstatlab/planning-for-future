# Unit 4 — Deep Learning for NLP

**Syllabus topics:** Recurrent Neural Networks (RNN): basics, RNN vs
CNN/feedforward NN. LSTM and GRU for sequence modeling. Transformer models:
introduction, pretrained models (BERT, GPT), Hugging Face ecosystem.

---

> ### 💡 Read this unit alongside Course 14 A's Unit 4
>
> They cover the same architectures from two directions.
> [Course 14 A Unit 4](../course-14a-deep-learning/unit-4.md) builds the RNN
> and LSTM and measures them; this unit is about applying them to language.
> **Doing both in the same week roughly halves the work**, and the numbers
> quoted here come from both courses' labs.

---

## 4.1 Why sequences break the models you already have

| Model | Assumes | Fails on language because |
|---|---|---|
| **Feedforward** | fixed-size input, independent features | sentences vary in length; word 3 and word 30 are learned separately |
| **CNN** | local, translation-invariant patterns | **captures local n-grams well**, cannot reach long dependencies |
| **RNN** | order matters, state carries forward | **this is the right shape** — and it has its own problem |

### 📖 RNN vs CNN for text — the comparison the syllabus asks for

| | **CNN** | **RNN** |
|---|---|---|
| What it sees | a **window** of `k` words, everywhere | the **whole prefix**, one word at a time |
| Parallel over the sequence | **yes** | **no — inherently serial** |
| Long dependencies | only by stacking layers | in principle yes, in practice limited |
| Speed | **fast** | slow |
| Good at | local phrase patterns — "not good", "highly recommend" | order, agreement, structure |

> **A CNN over text is an n-gram detector with learned filters.** That is a
> genuinely useful thing for sentiment — where a few key phrases decide the
> label — and it is why CNNs were competitive on sentiment classification long
> after RNNs took over elsewhere.

---

## 4.2 The RNN, and the problem that defines the unit

A **recurrent neural network** is defined by one recurrence:

$$h_t = f(W_h h_{t-1} + W_x x_t + b)$$

**One set of weights applied at every timestep**, with a hidden state carried
forward. The weights do not depend on `t`, so the network handles any length
and shares what it learns across positions.

### 🔢 The vanishing gradient, as arithmetic

Backpropagation through time multiplies the same recurrent weight at every
step:

| Sequence length | Gradient at `w = 0.5` |
|---|---|
| 50 | 8.88e-16 |
| 100 | 7.89e-31 |
| **500** | **3.05e-151** |
| **1100** | **0.00e+00** |

> ### ⚠️ Be precise about what "vanishes" means
>
> **3.05e-151 is not zero.** It is a perfectly representable float64, and
> saying "the gradient vanishes" as though floating point were the problem
> gets the mechanism wrong. The problem is that this gradient is so much
> smaller than the others in the sum that **it changes no weight by any
> measurable amount.**
>
> Genuine underflow to exactly zero needs `T > 1074`. Course 14 A's lab
> asserts both facts.

**Exploding is the mirror image** and the fix is **gradient clipping** — cap
the gradient vector's norm before the update. Both labs in this semester do
it in one line.

---

## 4.3 LSTM and GRU for sequence modeling

### 📖 The LSTM's three gates

| Gate | Decides |
|---|---|
| **forget** | how much of the old cell state to keep |
| **input** | how much of the new candidate to write |
| **output** | how much of the cell to expose |

$$c_t = f_t \odot c_{t-1} + i_t \odot g_t \qquad h_t = o_t \odot \tanh(c_t)$$

### 🎯 Why it works, in one sentence

> **The cell state is an *additive* path.** With the forget gate near 1, the
> gradient along `c` is multiplied by something near **1** regardless of
> length, instead of by `w` at every step.
>
> **"An additive path instead of repeated multiplication"** is the whole
> answer — and it is the same idea as the residual connection in a
> transformer.

### 📖 GRU

Merges forget and input into one **update** gate, adds a **reset** gate, drops
the separate cell state.

| Cell | Gates | Parameters vs RNN |
|---|---|---|
| RNN | none | 1× |
| **LSTM** | forget, input, output | **4×** |
| **GRU** | reset, update | **3×** |

**Usually indistinguishable in accuracy and faster to train.** GRU is a
reasonable default; LSTM is the one you name in an exam.

### 🔢 The measurement — and it depends on the data

Course 14 A ran the comparison twice:

| Dataset | RNN | LSTM | GRU | Gap (LSTM−RNN) |
|---|---|---|---|---|
| generated, one decisive word per sentence | 0.6600 | 0.9975 | 1.0000 | **+0.3375** |
| **real IMDb** | 0.6523 | 0.7357 | 0.7570 | **+0.0833** |

> **The gap is four times narrower on real data**, because sentiment in a real
> review is **redundant** — "terrible", "waste" and "boring" may all appear in
> one paragraph, so a weaker model that catches any one of them still scores.
>
> **Both numbers are real and they measure different things.** Reporting only
> the one that flatters the LSTM would be dishonest.

---

## 4.4 Text generation with an RNN

`10_sentiment_rnn.py`
trains a character-level LSTM on **Jane Austen's *Emma*** from NLTK's
Gutenberg corpus — 119,232 characters, 47 distinct, 197,183 parameters.

### 🔢 Perplexity, and why it is quoted instead of loss

**Perplexity = exp(cross-entropy)**, and it reads as *"the model is as
uncertain as if it were choosing uniformly among this many characters"*.

| | Value |
|---|---|
| Alphabet size (uniform guessing) | **47** |
| Perplexity, epoch 0 | ~6.5 |
| Perplexity, final | **~2.7** |

**The number means something on its own**, which loss does not. Uniform
guessing over 47 characters is the baseline; the model is choosing among fewer
than three.

### 🔢 Temperature

| `T` | Output |
|---|---|
| **0.2** | conservative, repetitive |
| 0.6–1.0 | English-shaped: correct spelling, plausible word boundaries |
| **1.6** | invented words — *"troublebond"*, *"meepleavule"* |

`T → 0` is greedy argmax; `T → ∞` is uniform random. **This is the same knob
every LLM API exposes.**

### ⚠️ What a character model can and cannot learn

> **Spelling and local grammar are decided within a few characters, so the
> LSTM's memory reaches them. What a paragraph is *about* is decided over
> hundreds of characters, and it does not.**
>
> That gap is exactly what attention was invented to close.

---

## 4.5 Transformers — the introduction

*(The mechanism in full is [Unit 5](unit-5.md); this is the motivation.)*

### 🔢 Why attention replaced recurrence

| | RNN / LSTM | Self-attention |
|---|---|---|
| Parallel over the sequence | **no** | **yes** |
| Compute per layer | `O(T·d²)` | **`O(T²·d)`** |
| Long dependencies | gradient decays | **direct connection** |
| Needs position info | implicit in the order | **must be added** |

**The parallelism is why transformers won.** An RNN cannot start step `t`
until step `t−1` finishes, so it cannot use a GPU properly. A transformer
processes every position at once.

**The `O(T²)` is the price**, and it is why context length is a topic at all:
doubling the context **quadruples** the cost.

---

## 4.6 Pretrained models

| | **BERT** (2018) | **GPT** (2018–) |
|---|---|---|
| Architecture | transformer **encoder** | transformer **decoder** |
| Attention | **bidirectional** | **causal** — left only |
| Trained by | **masked language modelling** | **next-token prediction** |
| Natural at | classification, NER, QA | **generation** |
| Used by | fine-tuning a task head | prompting, or fine-tuning |

### 🎯 The distinction that gets examined

**BERT cannot generate text**, because it sees the whole sentence at once —
there is no "next" token in its objective. **GPT cannot use right-hand
context**, because its attention is causally masked. **The masking is the
entire architectural difference**; both are stacks of the same block.

### 🔢 What pre-training buys, measured from below

`12_transformer_local.py`
trains **the same architecture** — a bidirectional transformer encoder with a
masked-LM objective, BERT's exact shape — on the Brown corpus, and asks it to
fill masks.

| | This model | `bert-base-uncased` |
|---|---|---|
| Parameters | ~700 K | **110,000,000** |
| Training words | ~200 K | **3,300,000,000** |
| Fills "The capital of France is `[MASK]`" | function words | **`paris`, p > 0.9** |

**Its single best guess is usually `<unk>`** — "some word I do not have" — which
is a correct prediction about the *data* and a useless one about the
*sentence*.

> ### 🎯 The reading
>
> **The small model learned the shape of English and none of the facts.**
> Knowing the capital of France is not a fact about grammar; it arrives only
> with scale.
>
> **You can only see the size of that gap by training the small version
> yourself**, which is why this experiment exists in a course where the
> pre-trained model cannot be downloaded.

---

## 4.7 The Hugging Face ecosystem

| Piece | What it is |
|---|---|
| **`transformers`** | the model library; `pipeline()` is the one-line interface |
| **`datasets`** | loaders with memory-mapping for datasets larger than RAM |
| **`tokenizers`** | fast subword tokenizers (BPE, WordPiece, SentencePiece) |
| **Hub** | hosted model and dataset weights |
| **Spaces** | hosted demo apps (Gradio, Streamlit) |

### 📖 Subword tokenization, which is the piece people skip

Neither words nor characters: **frequent words stay whole and rare words split
into pieces.**

```
"tokenization"  ->  ["token", "##ization"]
"Siddaramaiah"  ->  ["Sid", "##dara", "##maia", "##h"]
```

| Solves | How |
|---|---|
| **Out-of-vocabulary words** | any string can be built from subwords — no `<unk>` |
| **Vocabulary size** | 30 K subwords covers what 1 M words would |
| **Morphology** | *running* → *run* + *##ning* shares the stem's vector |

**This is why modern models have no `<unk>` token** — and the local model in
experiment 12, which uses a fixed word vocabulary, predicts `<unk>` constantly
precisely because it lacks this.

### ⚠️ In this repository

> **`huggingface.co` is refused by this environment's egress policy — 403 at
> the gateway.** No checkpoint can be downloaded. Experiments 12, 13 and 14
> carry the code marked `*** NOT EXECUTED ***`, and each names a runnable half
> that trains or builds the same mechanism from parts that are available.

---

## What to be able to do after this unit

- [ ] **Compare RNN, CNN and feedforward networks for text**, with one strength each
- [ ] Write the RNN recurrence and say why the weights are shared across `t`
- [ ] Give the vanishing-gradient arithmetic — **and be precise that 3e-151 is not zero**
- [ ] Name the LSTM gates and answer "why LSTM?" in one sentence
- [ ] Give the GRU's gates and parameter ratio
- [ ] **Explain why the LSTM-RNN gap narrowed on real IMDb**
- [ ] Define perplexity and say what value means "no better than guessing"
- [ ] Explain temperature and its two limits
- [ ] Give the `O(T²)` cost and why parallelism made transformers win
- [ ] **State the architectural difference between BERT and GPT and what each cannot do**
- [ ] Explain subword tokenization and the two problems it solves
- [ ] Name the five pieces of the Hugging Face ecosystem

**Cross-check yourself:** run
`10_sentiment_rnn.py` and
`12_transformer_local.py`.
