# Unit 5 — Transformers and Modern NLP

**Syllabus topics:** Transformer architecture basics (self-attention,
encoder-decoder). BERT: pretraining, fine-tuning. GPT and generative NLP.
Hugging Face ecosystem (using pre-trained models). Text summarization:
extractive, abstractive, hybrid approaches. Applications: document
classification, chatbots, virtual assistants.

---

## 5.1 Transformer architecture basics: self-attention

### 📖 The one equation

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^{T}}{\sqrt{d_k}}\right)V$$

| Symbol | Think of it as |
|---|---|
| **Q** query | what this position is looking for |
| **K** key | what each position advertises |
| **V** value | what each position contributes |

> **Attention is a soft, learned lookup table.** The output is a weighted
> average of the values, weighted by how well each key matched the query.

### 🔢 Worked, on checkable numbers

Course 14 A's lab uses a query aligned with key 0, orthogonal to key 1, and
partly aligned with key 2:

| Step | Value |
|---|---|
| raw scores `Q·Kᵀ` | `[1.0, 0.0, 0.7]` |
| scaled by `√d_k = 2.0` | `[0.5, 0.0, 0.35]` |
| **attention weights** | **`[0.4053, 0.2458, 0.3489]`** |
| output | `[5.7974, 4.2026]` |

**The weights rank the keys in exactly the order of match.**

### 🔢 Why divide by `√d_k` — measured

The dot product of two random `d_k`-dimensional vectors has standard deviation
growing as `√d_k`:

| `d_k` | std of `Q·K` | max softmax weight |
|---|---|---|
| 4 | 2.025 | 0.1615 |
| 64 | 8.060 | 0.7146 |
| **1024** | **33.167** | **0.9857** |

> **At `d_k = 1024` one weight goes to ~0.99 and the rest to ~0.** The softmax
> **saturates**, its gradient vanishes, and the model stops learning.
> Dividing by `√d_k` holds the score variance at 1 whatever the dimension.
>
> **This is the detail most people cannot explain in a viva.**

### 📖 Multi-head attention, and the encoder block

One head produces one weighted average and can express one kind of
relationship. **Eight heads attend to eight things at once** — one tracking
syntax, another coreference — and the concatenation lets the next layer use
all of them.

```
x → multi-head self-attention → add & layer-norm
  → feed-forward (d → 4d → d)  → add & layer-norm
```

| Component | Why |
|---|---|
| self-attention | mixes information **between** positions |
| feed-forward | transforms each position **independently** — most parameters live here |
| **residual (add)** | a gradient path that skips the block — the LSTM cell-state idea again |
| layer norm | stabilises scale, per example rather than per batch |

### ⚠️ Positional encoding

**Attention is permutation-equivariant**: shuffle the input and the outputs
shuffle with it. It has *no* notion of order, so position must be added
explicitly — as fixed sinusoids or as learned vectors.

Course 14 A ablates it and finds **no difference at all** on a bag-of-words
sentiment task — because order carries no information there. **On translation
or parsing, removing it is catastrophic.** The null result is reported as
such rather than replaced with a task that flatters the claim.

### 📖 Encoder-decoder

| Part | Attention | Used for |
|---|---|---|
| **Encoder** | bidirectional self-attention | reads the source |
| **Decoder** | **causal** self-attention **+ cross-attention to the encoder** | writes the target |

**Cross-attention is where translation happens**: the decoder's query at each
output position attends over every encoder position, so the model can align
target words to source words wherever they are.

| Architecture | Example | Good for |
|---|---|---|
| Encoder only | **BERT** | understanding — classification, NER, QA |
| Decoder only | **GPT** | generation |
| Encoder-decoder | **T5, BART** | **transformation** — translation, summarization |

---

## 5.2 BERT

### 📖 Pretraining

Two objectives, of which only one turned out to matter:

| Objective | What it is | Status |
|---|---|---|
| **Masked LM** | hide 15% of tokens, predict them | **the one that matters** |
| **Next Sentence Prediction** | does B follow A? | **later shown unhelpful**; RoBERTa dropped it and scored better |

### 🔢 The masking recipe, which is not just `[MASK]`

Of the 15% picked:

| Share | Replaced with |
|---|---|
| **80%** | `[MASK]` |
| **10%** | a **random** word |
| **10%** | **left unchanged** |

> **Why the last two rows exist:** `[MASK]` never appears at fine-tuning or
> inference. If every masked position were the literal `[MASK]`, the model
> would learn "predict well only where I see `[MASK]`" and build no useful
> representation anywhere else.

### 🎯 Why bidirectionality is the point

Two sentences, same mask position, differing only at the end:

| Sentence | BERT predicts |
|---|---|
| "The `[MASK]` was closed, so I could not deposit the cheque." | **`bank`** — financial sense |
| "The `[MASK]` was closed, so I could not cross the river." | **`bridge`/`bank`** — the other sense |

**The disambiguating evidence is to the RIGHT of the mask**, and only a
bidirectional model can use it. **Word2Vec cannot do this — it assigns *bank*
one vector, for ever.**

### 📖 Fine-tuning

Replace the pre-trained head with a task head and train on your labelled data.

| Task | Head |
|---|---|
| Classification | a linear layer on the `[CLS]` token |
| NER | a linear layer on **every** token |
| Question answering | two heads predicting the answer's **start** and **end** span |

**Typical fine-tuning: 2–4 epochs, learning rate 2e-5 to 5e-5.** Those numbers
are small for a reason — Course 14 A measured what happens when you unfreeze
too much on too little data: **accuracy fell from 0.8260 to 0.7760.**

> **The rule from that measurement: how much you unfreeze must scale with how
> much data you have.**

---

## 5.3 GPT and generative NLP

**Decoder-only, causally masked, trained on next-token prediction.** The mask
is a triangular matrix that stops position `t` attending to anything after it
— which is what makes generation coherent and makes right-hand context
unavailable.

| Approach | What you provide |
|---|---|
| **Zero-shot** | an instruction only |
| **Few-shot** | a handful of examples in the prompt |
| **Fine-tuning** | a labelled dataset and a training run |

### ⚠️ The failure mode to name

**Hallucination.** A generative model produces text that is *probable*, not
text that is *supported*. It has no representation of "I do not know", and
fluency is uncorrelated with accuracy.

---

## 5.4 Text summarization

### 📖 The three approaches the syllabus names

| | **Extractive** | **Abstractive** | **Hybrid** |
|---|---|---|---|
| Mechanism | select existing sentences | generate new text | extract, then rewrite |
| Grammatical | **always** | usually | usually |
| Faithful | **guaranteed** | **not guaranteed** | mostly |
| Can compress or rephrase | **no** | **yes** | yes |
| Needs a pre-trained model | **no** | yes | yes |

### 🔢 The measurement — and the baseline nobody reports

`12_transformer_local.py`
builds **TextRank** — PageRank over a TF-IDF sentence-similarity graph — on a
real 22-sentence Reuters article, and compares it with **lead-3**:

| Method | Sentences chosen |
|---|---|
| TextRank | 1, 3, 14 |
| **Lead-3** | 0, 1, 2 |

**They agree on one of three.**

> ### 🎯 Lead-3 is the baseline to beat, and it is free
>
> News writing is deliberately front-loaded — **the inverted pyramid** — so
> "take the first three sentences" is a genuinely strong summarizer on news.
> Many published systems beat it by very little.
>
> **If your method cannot beat lead-3, say so.** That is a result about the
> data, and omitting the baseline is the most common flaw in summarization
> reports.

### ⚠️ Why the extractive/abstractive distinction matters in practice

**Abstractive models hallucinate** — they can assert a number, a date or a
causal claim the source does not contain.

> This is not hypothetical. **It is the main reason production summarizers in
> medicine, law and finance are still extractive**: an extractive summary of a
> medical report is at worst badly chosen, while an abstractive one can state
> a dosage that appears nowhere in the source.

### 📖 Evaluation

| Metric | Measures | Weakness |
|---|---|---|
| **ROUGE-1 / -2** | unigram / bigram overlap with a reference | **rewards copying**; blind to paraphrase |
| ROUGE-L | longest common subsequence | same |
| BERTScore | embedding similarity | needs a model |
| **Human judgement** | what you care about | expensive, and the only real answer |

**And the check worth more than any ROUGE score:** for every noun phrase,
number and date in the generated summary, search the source for it. **Anything
not there is a hallucination. Report the count.**

---

## 5.5 Applications, and the Hugging Face ecosystem in practice

### 📖 Document classification

The pipeline of [Unit 3](unit-3.md) with a transformer as the encoder.
**Report the baseline.** Course 15 A's own measurement: six models on movie
reviews differed by **less than the spread between cross-validation folds** —
so a transformer that beats TF-IDF by half a point has not beaten anything.

### 📖 Chatbots and virtual assistants — the two kinds

A **virtual assistant** is a chatbot with actions attached: it must also
classify the user's *intent* and fill the *slots* that action needs
("book a room" → date, duration, room type). The retrieval/generative split
below applies to both.

| | **Retrieval** | **Generative** |
|---|---|---|
| Answers come from | a fixed set you wrote | the model |
| Can be wrong in a new way | **no** | **yes** |
| Can handle an unseen question | no | yes |
| Auditable | **yes** | not really |

**For an institutional FAQ, retrieval is almost always the right answer**,
because a wrong answer about fees or examination dates is a real harm and a
fixed answer set is auditable.

### 🔢 The retrieval measurement

The lab scores an FAQ retriever on six queries, none of which copies an FAQ
question:

| Representation | Correct |
|---|---|
| TF-IDF, words | **5 / 6** |
| **TF-IDF, character 3-5 grams** | **6 / 6** |

**Character n-grams got every one** — because *exams* and *examination* share
the substrings `exam`, `xam`. **On this FAQ there is nothing for a transformer
to improve**, and a report claiming embeddings were necessary would be wrong.

The one word-level failure is the instructive part: *"when are the exams"*
matched the library-hours entry at **0.4014** — an **exact tie** with the
right answer, broken by list order, **and both matches came only from the
function words "are", "the" and "when".** Neither had anything to do with
meaning.

### ⚠️ The threshold every retrieval bot needs

**`argmax` always returns something.** Asked *"what is the wifi password"* —
not in the FAQ — the bot confidently returns its nearest entry at similarity
**0.3561**.

> **Compare the top score against a threshold and say "I don't know" below
> it.** It is the single cheapest improvement to any retrieval bot and the
> most commonly omitted.

### 🎯 And the metric users actually feel

| Metric | Meaning |
|---|---|
| Accuracy @1 | the top answer is correct |
| Recall @3 | the correct answer is in the top three |
| Rejection rate on out-of-scope queries | how often it correctly declines |
| **False-answer rate** | **how often it answers confidently and wrongly** |

**A bot that says "I don't know" 20% of the time is useful. A bot that is
confidently wrong 20% of the time is worse than no bot.**

---

## What to be able to do after this unit

- [ ] Write the attention equation and say what Q, K and V mean
- [ ] Work an attention example by hand
- [ ] **Explain `√d_k` in terms of softmax saturation**
- [ ] Draw the encoder block and justify the residual and layer norm
- [ ] Explain why positional encoding is needed and when its absence does not matter
- [ ] **Explain what cross-attention does and why translation needs it**
- [ ] Match encoder-only / decoder-only / encoder-decoder to BERT / GPT / T5
- [ ] **Give BERT's masking recipe including the 10% random and 10% unchanged**
- [ ] Say why NSP was dropped
- [ ] **Use the two "bank" sentences to explain bidirectionality**
- [ ] Give typical fine-tuning hyperparameters and say why they are small
- [ ] Compare extractive, abstractive and hybrid summarization
- [ ] **State the lead-3 baseline and why it must be reported**
- [ ] Explain why regulated domains still use extractive summarization
- [ ] Give ROUGE's weakness and the hallucination check that beats it
- [ ] **Distinguish retrieval from generative chatbots and say which suits an FAQ**
- [ ] Explain why a retrieval bot needs a threshold

**Cross-check yourself:** run
`12_transformer_local.py`,
and Course 14 A's
`11_attention.py` for
the attention numbers.
