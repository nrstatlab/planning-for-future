# Experiment 12 — masked word prediction with a pre-trained BERT

## *** NOT EXECUTED ***

**`huggingface.co` is refused by this environment's egress policy** — the
proxy returns **403 at the gateway** before any request reaches the host. No
BERT checkpoint can be downloaded, so no `pipeline("fill-mask")` can be
constructed. **Nothing in this file has been run here**, and nothing in the
notes claims an output for it.

**The runnable half is
`12_transformer_local.py`**, which trains the same
architecture — a bidirectional transformer encoder with a masked-LM objective
— from scratch on the Brown corpus, and reports honestly that its predictions
are weak. **That gap is the measurement**: it is what pre-training on 3.3
billion words buys, seen from below.

---

## The code

```python
from transformers import pipeline

# bert-base-uncased: 110M parameters, trained on BooksCorpus + Wikipedia
fill = pipeline("fill-mask",
                model="bert-base-uncased",
                revision="86b5e07")          # pin it -- defaults change

for sent in [
    "The president of the United [MASK] said so.",
    "She opened the [MASK] and walked in.",
    "The capital of France is [MASK].",
    "The [MASK] was closed, so I could not deposit the cheque.",
    "The [MASK] was closed, so I could not cross the river.",
]:
    print(sent)
    for r in fill(sent, top_k=5):
        print(f"   {r['token_str']:<14}{r['score']:.4f}")
```

**Expected output for the third line** is `paris` with a probability above
0.9. The local model in `12_transformer_local.py` cannot produce that,
because *knowing the capital of France is not a fact about English grammar* —
it is a fact about the world, and it arrives only with scale.

### 🎯 The two lines to run together

The fourth and fifth sentences are the experiment. **They differ by one word
at the end and the mask is in the same position.**

| Sentence ends | BERT's top prediction |
|---|---|
| "…could not deposit the cheque" | `bank` (financial sense) |
| "…could not cross the river" | `bridge`, `river`, `bank` (the other sense) |

**A bidirectional model sees the words to the RIGHT of the mask**, so the
disambiguating evidence is available to it. This is the single clearest
demonstration of what "contextual embedding" means, and it is why BERT is an
*encoder*: masked-LM training is only possible when the model may look both
ways.

Word2Vec cannot do this. It assigns "bank" one vector, for ever.

---

## The details that are examined

### The masking recipe is not just "replace with [MASK]"

BERT picks **15%** of tokens, and then:

| Share of the picked tokens | Replaced with |
|---|---|
| **80%** | `[MASK]` |
| **10%** | a **random** word |
| **10%** | **left unchanged** |

**Why the last two rows exist:** `[MASK]` never appears at fine-tuning or
inference time. If every masked position were the literal `[MASK]` token, the
model would learn "produce a good prediction only where I see `[MASK]`" and
would build no useful representation anywhere else. The random and unchanged
cases force it to build a good representation of **every** position.

> `12_transformer_local.py` implements the simple 100%-`[MASK]` version for
> clarity, and its docstring says so. **This is the difference between the
> two, and it is a standard viva question.**

### Why 15%

Too low and most positions supply no training signal, so training is slow.
Too high and there is not enough surrounding context left to predict from.
15% was chosen empirically and later work has questioned it — but "it is a
tuned hyperparameter, not a law" is the right answer.

### The two objectives BERT was trained on

| Objective | What it is | Status |
|---|---|---|
| **Masked LM** | predict the hidden tokens | the one that matters |
| **Next Sentence Prediction** | does sentence B follow sentence A? | **later shown to be unhelpful**; RoBERTa dropped it and scored better |

Naming NSP *and* knowing it was dropped is what distinguishes a good answer
from a memorised one.

### BERT vs GPT, in one line

**BERT is an encoder with bidirectional attention and cannot generate text;
GPT is a decoder with causally-masked attention and cannot use right-hand
context.** The masking is the entire architectural difference — both are
stacks of the same block.

---

## If you are running this yourself

```bash
pip install transformers torch
python3 -c "
from transformers import pipeline
fill = pipeline('fill-mask', model='bert-base-uncased')
print(fill('The capital of France is [MASK].', top_k=3))
"
```

The first run downloads about 440 MB. Behind a proxy that blocks
`huggingface.co`, fetch the model elsewhere and point `HF_HOME` at the copied
cache with `HF_HUB_OFFLINE=1`.

## What goes in the lab record

| Item | Value |
|---|---|
| Model name and pinned revision | |
| Top-5 predictions for each of the five sentences | |
| **The two "bank" sentences, side by side** | |
| Perplexity of the local model in `12_transformer_local.py`, for comparison | |
| One sentence where BERT is confidently wrong | |

One paragraph: **the local model in `12_transformer_local.py` learned the
shape of English but none of the facts. Name one prediction where the
difference is visible, and say what BERT saw that it did not.**
