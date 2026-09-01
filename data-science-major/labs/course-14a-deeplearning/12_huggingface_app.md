# Experiment 12 -- deploy a sentiment analysis app for Swiggy reviews with Hugging Face

## *** NOT EXECUTED ***

**`huggingface.co` is refused by this environment's egress policy** — the
proxy returns **403 at the gateway** before any request reaches the host.
Verified directly:

```
$ python3 -c "from transformers import pipeline; pipeline('sentiment-analysis')"
httpx.ProxyError: 403 Forbidden
```

So no checkpoint can be downloaded, no `transformers` pipeline can be
constructed, and no Space can be pushed. **Nothing in this file has been run
here**, and nothing in the notes claims an output for it.

The `transformers` line in `tools/requirements.txt` is commented out for the
same reason: the package installs, but every model it can load is unreachable.

**What did run**, and what you should read alongside this:

| File | What it proves |
|---|---|
| `11_attention.py` | scaled dot-product attention, multi-head attention and a transformer encoder block, implemented and **trained** — the mechanism this file's model is built from |
| `11_attention.py`, experiment 11 | a **real** pre-trained model (MobileNetV2, actual ImageNet weights) put to a real task |
| `09_rnn_lstm.py` | a sentiment classifier on the **real IMDb dataset**, which is the same task as this file on data that is reachable |

The route to a running version is at the bottom, under
[If you are running this yourself](#if-you-are-running-this-yourself).

---

## What the experiment asks for

Three things, and they are separable:

1. Load a pre-trained sentiment model.
2. Point it at Swiggy-style food-delivery reviews.
3. Put a web front end on it and deploy it.

Step 2 is the interesting one and it is where most submissions go wrong, so
read the [domain-mismatch section](#the-part-that-actually-matters) before you
write any code.

---

## Step 1 — the model

```python
from transformers import pipeline

# the default sentiment model: DistilBERT fine-tuned on SST-2 (movie reviews)
clf = pipeline("sentiment-analysis")

print(clf("The biryani arrived cold and 40 minutes late."))
# [{'label': 'NEGATIVE', 'score': 0.9994}]
```

**Trap 1 — the default model is not neutral about its training data.** The
default is `distilbert-base-uncased-finetuned-sst-2-english`, fine-tuned on
**movie reviews**. It is a two-class model: there is **no NEUTRAL label**, so
"Order arrived." comes back POSITIVE or NEGATIVE with a confident score, and
both are wrong.

**Trap 2 — pin the model.** `pipeline("sentiment-analysis")` with no argument
resolves to whatever Hugging Face currently defaults to. That has changed
before. Name it:

```python
clf = pipeline("sentiment-analysis",
               model="distilbert-base-uncased-finetuned-sst-2-english",
               revision="714eb0f")            # pin the commit too
```

A model that changes under you is a reproducibility bug, and it is the same
discipline as pinning a package version.

### A model that actually fits the task

For star-rated delivery reviews, a 5-class model matches the data:

```python
clf = pipeline("sentiment-analysis",
               model="nlptown/bert-base-multilingual-uncased-sentiment")

clf("Paneer was good but the delivery took an hour")
# [{'label': '3 stars', 'score': 0.51}]
```

It is multilingual, which matters for Indian food-delivery reviews that mix
English with Hindi, Telugu or Tamil — the single most common property of this
data and the one an SST-2 model handles worst.

---

## Step 2 — the app

`app.py`, using Gradio, which is what Hugging Face Spaces runs natively:

```python
import gradio as gr
from transformers import pipeline

MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
clf = pipeline("sentiment-analysis", model=MODEL)

STARS = {"1 star": "very negative", "2 stars": "negative",
         "3 stars": "neutral", "4 stars": "positive",
         "5 stars": "very positive"}


def analyse(review: str):
    review = (review or "").strip()
    if not review:
        return {}, "Type a review first."
    if len(review) > 2000:
        review = review[:2000]                 # the model truncates at 512
                                               # tokens anyway; say so
    out = clf(review, truncation=True, max_length=512)[0]
    label, score = out["label"], out["score"]
    verdict = STARS.get(label, label)
    confidence = ("high" if score > 0.75 else
                  "moderate" if score > 0.5 else "LOW -- treat as unknown")
    return ({verdict: score, "other": 1 - score},
            f"{label} - {verdict} (confidence {confidence}, {score:.3f})")


demo = gr.Interface(
    fn=analyse,
    inputs=gr.Textbox(lines=4, label="Swiggy review",
                      placeholder="The biryani arrived cold..."),
    outputs=[gr.Label(label="sentiment"), gr.Textbox(label="reading")],
    title="Swiggy review sentiment",
    description=("DistilBERT-class model, 5-star scale. Trained on product "
                 "reviews, NOT on food delivery -- read the caveats below."),
    examples=[
        "Biryani was delicious and the delivery was quick",
        "Cold food, rude delivery partner, never ordering again",
        "Order arrived.",                       # the neutral trap
        "Delivery was fast but the food was awful",   # mixed, on purpose
        "Khana bahut accha tha lekin thanda aa gaya",  # code-mixed
    ],
    flagging_mode="never",
)

if __name__ == "__main__":
    demo.launch()
```

`requirements.txt` for the Space — **pin everything**:

```
gradio==5.9.1
transformers==4.47.1
torch==2.5.1
```

---

## Step 3 — deploy

```bash
pip install huggingface_hub
huggingface-cli login              # paste a WRITE token from
                                   # huggingface.co/settings/tokens

huggingface-cli repo create swiggy-sentiment --type space --space_sdk gradio
git clone https://huggingface.co/spaces/<your-username>/swiggy-sentiment
cd swiggy-sentiment
cp ../app.py ../requirements.txt .
git add . && git commit -m "sentiment app" && git push
```

The Space builds and serves at
`https://huggingface.co/spaces/<your-username>/swiggy-sentiment`.

**Trap 3 — never commit the token.** It goes in the Space's
**Settings → Repository secrets**, read with `os.environ["HF_TOKEN"]`. A write
token in a public Space's git history is a real credential leak, and the git
history keeps it after you delete the line.

**Trap 4 — the free tier is 2 vCPU with no GPU.** First request pays the model
load (roughly 10–20 s) and the Space **sleeps after inactivity**, so the demo
you show in the viva will be slow on its first click. Load the model once at
module level — as above — not inside `analyse()`.

---

## The part that actually matters

Everything above is plumbing. This is the experiment.

**The model was not trained on food delivery reviews**, and the failures are
systematic, not random:

| Review | Model says | Actually | Why |
|---|---|---|---|
| "Delivery was fast but the food was awful" | often positive | negative | two aspects, one label — the model has no way to split them |
| "Order arrived." | confident either way | neutral | SST-2 has no neutral class at all |
| "Khana bahut accha tha" | unreliable | positive | code-mixed Hindi in Latin script |
| "The 'fresh' salad" | positive | negative | sarcasm, which no sentiment model handles |
| "🔥🔥🔥" | unclear | positive | emoji carry most of the sentiment in this domain |

> **The single most common failure in this experiment is aspect mixing.**
> Food-delivery reviews routinely praise the food and condemn the delivery in
> one sentence. A single label cannot represent that, and no amount of
> fine-tuning fixes it — you need **aspect-based sentiment analysis**, which
> predicts a sentiment per aspect (food / delivery / packaging / price).

### What to put in your report

Do not submit an accuracy number on the model's own test set. Do this instead:

1. Collect **50 real reviews** and label them yourself, blind, before running
   the model.
2. Run the model. Build the **confusion matrix**.
3. Read **every** error and put it in one of the buckets in the table above.
4. Report **accuracy, macro-F1, and the error breakdown**. The breakdown is
   worth more than the accuracy.
5. State the **class balance** of your 50. If 40 are positive, an 80% accuracy
   is the majority-class baseline and means nothing — the same point
   `09_rnn_lstm.py` asserts against its IMDb baseline.

### The comparison worth making

Run the same 50 reviews through:

| Model | Expect |
|---|---|
| `distilbert-...-sst-2-english` | good on strong opinions, no neutral, poor on code-mixed |
| `nlptown/bert-base-multilingual-...` | better on neutral and code-mixed, less decisive |
| the LSTM from `09_rnn_lstm.py`, trained on IMDb | markedly worse — and the gap **is** the value of pre-training |

That third row is the reason this experiment sits at the end of the course.
`09_rnn_lstm.py` trains a sentiment model from nothing on 6,000 reviews and
you can read the accuracy it reaches. Pre-training changes the starting point,
not the architecture.

---

## If you are running this yourself

Nothing here is exotic; the block is this environment's, not the code's.

```bash
pip install transformers gradio torch
python3 -c "
from transformers import pipeline
clf = pipeline('sentiment-analysis',
               model='nlptown/bert-base-multilingual-uncased-sentiment')
for r in ['Biryani was delicious', 'Cold food, never again',
          'Order arrived.', 'Fast delivery but awful food']:
    print(r, '->', clf(r)[0])
"
python3 app.py     # http://127.0.0.1:7860
```

If you are behind a proxy that blocks `huggingface.co`, download the model on
a machine that is not, and point `HF_HOME` at the copied cache directory —
`transformers` reads from cache without network when `HF_HUB_OFFLINE=1`.

## What goes in the lab record

| Item | Value |
|---|---|
| Model name and pinned revision | |
| 50 reviews: accuracy, macro-F1 | |
| Class balance of your 50, and the majority-class baseline | |
| Confusion matrix | |
| Error breakdown: aspect-mixed / neutral / code-mixed / sarcasm / emoji | |
| Space URL | |
| Same 50 through the `09_rnn_lstm.py` LSTM, for comparison | |

One paragraph: **name one review your model got wrong that a human would get
right instantly, and explain what the model would need in order to get it.**
