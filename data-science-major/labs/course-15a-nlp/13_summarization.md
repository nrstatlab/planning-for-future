# Experiment 13 — extractive and abstractive summarization with Hugging Face

## *** NOT EXECUTED ***

**The abstractive half cannot run here.** `huggingface.co` returns **403 at
the gateway**, so BART, T5 and Pegasus cannot be downloaded. **Nothing in
this file has been run**, and nothing in the notes claims an output for it.

**The extractive half needed no pre-trained model and therefore did run** —
`12_transformer_local.py`, experiment 13, builds
TextRank over TF-IDF sentence similarity on a real Reuters article and scores
it against the lead-3 baseline. Read that first; this file is the half that
is missing.

---

## The code

```python
from transformers import pipeline

summarizer = pipeline("summarization",
                      model="facebook/bart-large-cnn",
                      revision="37f520f")

article = open("article.txt").read()

print(summarizer(article,
                 max_length=130, min_length=40,
                 do_sample=False)[0]["summary_text"])
```

**Trap 1 — the input limit.** `bart-large-cnn` accepts **1,024 tokens**, and
`truncation=True` silently discards everything after that. A 3,000-word
article is summarized from its first third and the summary looks fine. For
long documents you must chunk and summarize hierarchically.

**Trap 2 — `min_length` is not advice.** The model will pad a short article
into a longer summary rather than stop, producing repetition. Scale both
bounds to the input.

**Trap 3 — `bart-large-cnn` was fine-tuned on CNN/DailyMail news** and has
learned the inverted-pyramid style. On a scientific paper or a legal document
it produces news-shaped output that reads well and summarizes badly.

---

## The comparison that is the actual experiment

Run **both** halves on the same article and put them side by side.

| | Extractive (TextRank — **this ran**) | Abstractive (BART) |
|---|---|---|
| Mechanism | selects existing sentences | generates new text |
| Grammatical | **always** — the sentences were already | usually |
| Faithful to the source | **guaranteed** | **not guaranteed** |
| Can compress or rephrase | no | **yes** |
| Can merge two facts into one sentence | no | yes |
| Needs a pre-trained model | **no** | yes |
| Needs a GPU to be quick | no | yes |

### ⚠️ The failure mode that matters

**Abstractive models hallucinate.** They can assert things the source does
not say — a number, a date, a causal claim — because they are generating text
that is *probable*, not text that is *supported*.

This is not hypothetical. It is the main reason production summarizers in
medicine, law and finance are still extractive: **an extractive summary of a
medical report is at worst badly chosen, while an abstractive one can state a
dosage that appears nowhere in the source.**

### How to detect it in your own report

For every noun phrase, number and date in the generated summary, **search the
source for it**. Anything that is not there is a hallucination. Report the
count. That check takes ten minutes and is worth more than any ROUGE score.

---

## Evaluation

| Metric | Measures | Weakness |
|---|---|---|
| **ROUGE-1 / ROUGE-2** | unigram / bigram overlap with a reference | rewards copying; blind to paraphrase |
| **ROUGE-L** | longest common subsequence | same |
| **BERTScore** | embedding similarity | needs a model, so also blocked here |
| **Human judgement** | what you actually care about | expensive, and the only real answer |

> ### 🎯 And the baseline to report, which `12_transformer_local.py` measures
>
> **Lead-3 — "take the first three sentences" — is a genuinely strong
> summarizer on news**, because news is deliberately front-loaded. Many
> published systems beat it by very little.
>
> **If your method cannot beat lead-3, say so.** That is a result about the
> data, and omitting the baseline is the most common flaw in summarization
> reports.

---

## If you are running this yourself

```bash
pip install transformers torch
python3 -c "
from transformers import pipeline
s = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')
print(s(open('article.txt').read()[:4000], max_length=120, min_length=40)[0])
"
```

`distilbart-cnn-12-6` is roughly half the size of `bart-large-cnn` and much
faster on CPU. The first run downloads about 1.2 GB.

## What goes in the lab record

| Item | Value |
|---|---|
| The article, with its sentence count and word count | |
| The extractive summary (from `12_transformer_local.py`) | |
| The lead-3 baseline summary | |
| The abstractive summary, with the model name and revision | |
| ROUGE-1/2/L of each against a reference you write yourself | |
| **Hallucination count** in the abstractive summary | |

One paragraph: **give one sentence the abstractive model produced that is
better than anything extraction could have selected, and one thing it got
wrong that extraction could not have.**
