# Experiment 14 — an FAQ chatbot on transformer embeddings

## *** NOT EXECUTED ***

**`huggingface.co` is refused by this environment's egress policy** — 403 at
the gateway — so `sentence-transformers` cannot download a model. **Nothing
in this file has been run here**, and nothing in the notes claims an output
for it.

**The runnable half is `12_transformer_local.py`,
experiment 14**, which builds the identical retriever on TF-IDF embeddings
and scores it against hand-labelled answers. **The architecture is the same
— embed, cosine, argmax, threshold — and only the embedding function
changes**, which is what makes the comparison worth making.

---

## The code

```python
from sentence_transformers import SentenceTransformer, util

# 22M parameters, 384-dim embeddings, fast on CPU
model = SentenceTransformer("all-MiniLM-L6-v2")

faq = [
    ("How do I reset my password?",
     "Use the 'Forgot password' link on the sign-in page."),
    ("What are the library opening hours?",
     "08:00-20:00 on weekdays, 09:00-13:00 on Saturday."),
    # ... the same six entries as fixtures.FAQ
]
questions = [q for q, _ in faq]
answers = [a for _, a in faq]

# encode ONCE, at startup -- not per query
index = model.encode(questions, normalize_embeddings=True)


def answer(query, threshold=0.45):
    q = model.encode(query, normalize_embeddings=True)
    scores = util.cos_sim(q, index)[0]
    best = int(scores.argmax())
    if scores[best] < threshold:
        return "I don't have an answer for that. Please contact the office."
    return answers[best], float(scores[best])


for q, _ in FAQ_QUERIES:
    print(q, "->", answer(q))
```

**Trap 1 — encode the index once.** Re-encoding six FAQ entries on every
query is the most common performance bug in this experiment, and it is
invisible at six entries and fatal at six thousand.

**Trap 2 — `normalize_embeddings=True`.** With normalised vectors, cosine
similarity is a dot product, which is what every vector database is
optimised for. Without it you will eventually compare a normalised query
against an unnormalised index and get silently wrong rankings.

**Trap 3 — the threshold, which `12_transformer_local.py` measures.**
`argmax` *always* returns something. Ask "what is the wifi password" and an
untresholded bot confidently returns its nearest entry. **Setting a floor is
the single cheapest improvement to any retrieval bot and the most commonly
omitted.** Tune it on queries you know should fail.

---

## Why this should beat the TF-IDF version

### ⚠️ First, the measured result — because it is not what you would guess

`12_transformer_local.py` runs three TF-IDF variants on these six queries:

| Representation | Correct | Accuracy |
|---|---|---|
| TF-IDF, words | 5 / 6 | 0.8333 |
| TF-IDF, words, no stopwords | 5 / 6 | 0.8333 |
| **TF-IDF, character 3-5 grams** | **6 / 6** | **1.0000** |

**Character n-grams got every one of them.** So on this FAQ there is nothing
for a transformer to improve, and a report claiming embeddings were necessary
here would be wrong.

**Why character n-grams win:** "exams" and "examination" share the substrings
`exam`, `xam`, `ams`; "timings" and "opening hours" share little, but
"library" carries the query on its own. Character n-grams get much of the
morphological robustness that people reach for embeddings to obtain, **at
roughly zero cost**.

### The one query word-level TF-IDF got wrong, which is the instructive part

| | |
|---|---|
| Query | `when are the exams` |
| Matched | "What are the library opening hours?" — score **0.4014** |
| Should have matched | "When does the semester examination begin?" — score **0.4014** |

**It was an exact tie, broken by which entry came first in the list.** And
look at *why* both scored 0.4014: the only shared terms are **"are", "the"
and "when"** — function words. **Neither match had anything to do with
meaning**, and the "right" answer would have been equally accidental.

That is the failure sentence embeddings genuinely fix: *exams* and
*examination* are near each other in an embedding space and unrelated as
strings.

### So report both, and let the numbers decide

On a small FAQ with topically distinct entries, **keyword matching is often
enough**. The argument for embeddings strengthens as entries start sharing
vocabulary and as queries paraphrase more freely — scale this FAQ to a
hundred entries and it will. **Report the baseline** rather than assuming the
sophisticated method was needed.

---

## What to build if you have time

| Step | Why |
|---|---|
| **Hybrid retrieval** — combine the TF-IDF score and the embedding score | keyword matching still wins on rare exact terms like a form number |
| **A rejection set** — 10 queries with no correct answer | the only way to tune the threshold honestly |
| **Top-3 instead of top-1** | measure recall@3; a bot that offers three options is often more useful than one that guesses |
| **Log the misses** | the queries your bot rejects are the FAQ entries you are missing |

---

## Evaluation

Do not report "it worked". Report:

| Metric | Meaning |
|---|---|
| **Accuracy @1** | the top answer is correct |
| **Recall @3** | the correct answer is in the top three |
| **Rejection rate on out-of-scope queries** | how often it correctly says "I don't know" |
| **False-answer rate** | how often it answers confidently and wrongly — **the one that matters** |

**The last row is the one users feel.** A bot that says "I don't know" 20% of
the time is useful; a bot that is confidently wrong 20% of the time is worse
than no bot.

---

## If you are running this yourself

```bash
pip install sentence-transformers
python3 -c "
from sentence_transformers import SentenceTransformer, util
m = SentenceTransformer('all-MiniLM-L6-v2')
a = m.encode(['How much is the hostel fee?'], normalize_embeddings=True)
b = m.encode(['cost of staying in the hostel'], normalize_embeddings=True)
print('similarity', float(util.cos_sim(a, b)))
"
```

Expect roughly 0.7 — against TF-IDF's near-zero for the same pair, which
`12_transformer_local.py` prints. The first run downloads about 90 MB.

## What goes in the lab record

| Item | Value |
|---|---|
| Model name and revision | |
| Accuracy @1 and recall @3, on the same six queries | |
| **The same figures from `12_transformer_local.py`'s TF-IDF version** | |
| Chosen threshold, and how you chose it | |
| Rejection rate on 10 out-of-scope queries | |
| False-answer rate | |

One paragraph: **name one query TF-IDF got wrong and the embedding model got
right, and explain in terms of vectors why.**
