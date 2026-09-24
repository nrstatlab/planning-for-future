# Unit 3 — Information Extraction and Representation

**Syllabus topics:** Named Entity Recognition (NER): concepts, examples,
using spaCy and NLTK. Word embeddings: Word2Vec (Skip-Gram, CBOW),
comparison, implementations. Bag of Words and N-grams. Text classification
pipeline. Sentiment analysis applications. Ethical considerations in
preprocessing and classification.

---

## 3.1 Named Entity Recognition

### 📖 What it is

Find the spans of text that name a thing, and say what kind of thing.

| Label | Covers |
|---|---|
| `PERSON` | people |
| `ORG` | companies, agencies, institutions |
| `GPE` | **geo-political entities** — countries, cities, states |
| `LOC` | non-GPE locations — mountains, rivers |
| `DATE`, `TIME` | temporal expressions |
| `MONEY`, `CARDINAL`, `PERCENT` | numbers |

**`GPE` vs `LOC` is examined.** A GPE has a government; a LOC does not.
*Karnataka* is a GPE, *the Western Ghats* is a LOC.

### 📖 The tagging scheme

NER is a **sequence labelling** problem, and the standard encoding is **BIO**:

| Token | Tag |
|---|---|
| Salil | `B-PERSON` |
| Parekh | `I-PERSON` |
| said | `O` |

**B** begins an entity, **I** continues it, **O** is outside. Without B/I you
cannot tell two adjacent entities from one long one — which is the reason the
scheme exists.

### 🔢 The measurement, scored against hand-labelled truth

`07_parsing_ner_similarity.py`
runs spaCy's `en_core_web_sm` on a paragraph of Indian business news with
**13 hand-assigned entity labels**:

**11 of 13 exactly right, 2 wrong labels, 0 missed.**

| Entity | spaCy said | Truth |
|---|---|---|
| Infosys | ORG | ORG ✓ |
| Hyderabad | GPE | GPE ✓ |
| Bengaluru | GPE | GPE ✓ |
| Salil Parekh | PERSON | PERSON ✓ |
| Siddaramaiah | PERSON | PERSON ✓ |
| **Andhra Pradesh** | **ORG** | **GPE** ✗ |
| **Tamil Nadu** | **PERSON** | **GPE** ✗ |

### ⚠️ Read which two failed

**Both are states, and both cities were correct.** `en_core_web_sm` was
trained on OntoNotes — mostly American news — where Indian state names are
rare. The model falls back on surface cues, and *Tamil Nadu* has the shape of
a two-token personal name.

> ### 🎯 This is domain shift, and it is the single most important thing to
> know before using a pre-trained NLP model on Indian text
>
> The model is not broken. **It is being used outside its training
> distribution, and the errors are systematic rather than random** — which
> means you can predict and fix them.

### 💡 And the fix is not a bigger model

The lab adds a **gazetteer** through spaCy's `EntityRuler` — nine lines of
patterns naming Indian cities and states — and re-scores:

| | Correct |
|---|---|
| before the gazetteer | **11 / 13** |
| **after the gazetteer** | **13 / 13** |

```python
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns([{"label": "GPE", "pattern": p} for p in places])
```

**When your domain has a closed list of entities, matching it beats any amount
of inference.** A gazetteer is unglamorous and very often correct. The
alternative — annotating a few hundred sentences of your own domain and
fine-tuning — is the right answer when the list is open.

### ⚠️ And a lesson about your own gold standard

spaCy also found `2,400` (CARDINAL) and `three years` (DATE), which were **not
in the hand-built truth list**. Both are correct — **the gold list was
incomplete.**

> That is the most common defect in a hand-built evaluation set: the annotator
> marks what they were thinking about and misses the rest, and every model is
> then punished for finding it. **Annotate exhaustively, or state explicitly
> which categories you covered.**

---

## 3.2 Bag of Words and N-grams

### 📖 Bag of words

Count each word; discard order. A document becomes a vector as long as the
vocabulary.

| Variant | Value in each cell |
|---|---|
| **Count** | how many times the word appears |
| **Binary** | 1 if present |
| **TF-IDF** | `tf × log(N / df)` — down-weights words common across documents |

### 🎯 What IDF actually is

The lab fits TF-IDF on 400 Reuters documents and prints the extremes:

| | Words |
|---|---|
| **Lowest IDF** (in nearly every document) | `of`, `the`, `said`, `to`, `and`, `in` |
| **Highest IDF** (in one or two) | rare tokens and numbers |

> **IDF is a learned stopword list.** The lowest-scoring words are exactly the
> ones a stopword list contains — but derived from *your* corpus rather than
> from a fixed list in someone else's language.
>
> That is the argument for TF-IDF over raw counts, **and it is also why
> removing stopwords before TF-IDF changes less than students expect**.

### 🔢 N-grams, and the order that unigrams cannot see

| | `the dog bit the man` vs `the man bit the dog` |
|---|---|
| **Unigrams** | similarity **1.0000** — identical, same words |
| **Bigrams** | similarity **0.7500** — `dog bit` ≠ `man bit` |

**That is the whole argument for n-grams**, and also their cost: the feature
space grows enormously and most bigrams appear once, so **you gain word order
and lose statistical strength.**

### ⚠️ The measurement that motivates the rest of the course

Four documents with a known answer — 0 and 1 are near-duplicates, **2 is a
paraphrase of 0 in different words**, 3 is about the monsoon:

| Representation | sim 0-1 | **sim 0-2** | **sim 0-3** |
|---|---|---|---|
| Bag of words | 0.8006 | **0.0925** | **0.3077** |
| TF-IDF | 0.6993 | **0.0766** | **0.1802** |

**Bag-of-words ranks the unrelated document above the paraphrase.**

Why? Documents 0 and 3 share `the`, `and`, `are`. **Function words. Nothing
else.** The similarity is entirely an artefact of English grammar, and the one
pair that shares actual *meaning* shares almost no strings.

TF-IDF narrows the gap — IDF discounts those function words — **but does not
reverse it.** No count-based representation can: *weights* and *parameters*
are different strings and nothing in the counts says otherwise.

> **This is exactly the failure word embeddings were invented for.**

---

## 3.3 Word embeddings

### 🎯 The distributional hypothesis

> **"You shall know a word by the company it keeps."** (Firth, 1957)

Every embedding method operationalises that one sentence: words appearing in
similar contexts get similar vectors, and **that is the only supervision
there is.**

### 📖 Word2Vec — the two architectures

| | **CBOW** | **Skip-gram** |
|---|---|---|
| Predicts | the **centre** word from its context | the **context** words from the centre |
| Input → output | many → one | one → many |
| Speed | **faster** | slower |
| Rare words | worse | **better** |
| Small corpora | worse | **better** |
| Use when | you have a large corpus and want speed | you have less data or care about rare words |

**Remember them by direction:** CBOW collapses context *into* a word;
skip-gram fans a word *out* into its context.

### 📖 How it is trained, and why negative sampling exists

The naive objective requires a softmax over the whole vocabulary at every
step — **hundreds of thousands of exponentials per training example**.

**Negative sampling** replaces it: for each true (word, context) pair, draw
`k` random "negative" pairs and train a binary classifier to tell them apart.
The cost drops from |V| to `k + 1`, typically **5–20 instead of 500,000**.

> **"Why negative sampling?" — because the full softmax over the vocabulary is
> computationally impossible.** That is the answer.

### 📖 GloVe, and how it differs

Word2Vec is **predictive** and works locally, one window at a time. GloVe is
**count-based**: build the global word–word co-occurrence matrix, then
factorise it so that the dot product of two vectors approximates the log of
their co-occurrence count.

**In practice they perform similarly.** The distinction to state is *local
prediction* against *global co-occurrence factorisation*.

### 🔢 The famous property

$$\text{king} - \text{man} + \text{woman} \approx \text{queen}$$

**Vector arithmetic captures analogies** because the offset between *man* and
*woman* is roughly the offset between *king* and *queen*.

### ⚠️ And the limitation that ends this line of work

**One vector per word, for ever.** *Bank* gets a single vector that must serve
the river and the money — and WordNet lists **18 senses** for it.

**Contextual embeddings ([Unit 5](unit-5.md)) exist for precisely this**, and
[experiment 12](lab.md#experiment-12) trains a small bidirectional model to
show the mechanism.

---

## 3.4 The text classification pipeline

### 📖 The steps, in order

```
raw text
  → tokenize
  → normalise (lowercase, optionally stem/lemmatise)
  → vectorise (BoW / TF-IDF / embeddings)
  → classify (Naive Bayes / logistic regression / neural)
  → evaluate AGAINST A BASELINE
```

### ⚠️ The order matters, and this is examined

**Fit the vectoriser on the training set only, then `transform` the test
set.** Fitting on everything leaks test-set vocabulary and IDF statistics into
training and inflates your score.

`sklearn`'s `Pipeline` exists to make this mistake hard to commit — which is
why the lab uses `make_pipeline` throughout rather than vectorising by hand.

### 📖 Sentiment analysis as an application of the pipeline

**Sentiment analysis** is the pipeline above with a polarity label, and it is
the one application where the preprocessing advice from
[Unit 2](unit-2.md) inverts: **keep the stopwords**, because *not* carries the
label.

### 🔢 The measurement, on NLTK's 2,000 movie reviews

| Model | Features | Accuracy |
|---|---|---|
| **majority class** | — | **0.5000** |
| Naive Bayes, counts | 35,466 | **0.8240** |
| Naive Bayes, TF-IDF | 35,466 | 0.8060 |
| LogReg, TF-IDF | 35,466 | 0.8160 |
| LogReg, TF-IDF, no stopwords | 35,323 | 0.8220 |
| LogReg, TF-IDF 1-2 grams | 110,116 | 0.8180 |

### 🎯 Now the part that matters

5-fold cross-validation on the same data: **mean 0.8215, spread between folds
0.0075.**

| Comparison | Gap | Verdict |
|---|---|---|
| stopwords on vs off | 0.0060 | **noise** |
| best vs second-best model | 0.0080 | **noise** |
| **best vs the baseline** | **0.3240** | **real** |

> ### ⚠️ Re-read the first table with that in mind
>
> **Every difference between the real models is smaller than the variation
> between folds.** Naive Bayes "beating" logistic regression, and stopword
> removal "helping", are both inside the noise.
>
> **The honest conclusion is that these models are indistinguishable on this
> data.** That is a legitimate finding, and it is the one most lab reports get
> wrong: they rank six models on a single split and declare a winner that a
> different random seed would reverse.

### 💡 The cheapest sanity check in all of NLP

A linear model hands you its coefficients. **Print the ten most positive and
ten most negative features.**

- If the strongest features are sentiment words, the model learned the task.
- **If they are punctuation, a film title, or a reviewer's name, it learned an
  artefact of the corpus and will not transfer.**

Course 14 A's deep models do not offer this, which is why that course had to
*build a dataset with a known answer* to get the same check.

---

## 3.5 Ethical considerations

The syllabus lists this under preprocessing and classification, and each item
has a concrete mechanism rather than a slogan.

| Concern | The mechanism |
|---|---|
| **Bias in embeddings** | `doctor − man + woman ≈ nurse` is reproducible on standard embeddings; the geometry learned the corpus's prejudices from the same statistics as its facts |
| **Bias from preprocessing** | a stopword list built for English, applied to code-mixed Hinglish, removes different proportions of different people's text |
| **Dialect penalties** | classifiers trained on standard written English systematically score non-standard dialects as lower quality — a documented harm in automated essay scoring |
| **Anonymisation is not enough** | writing style identifies authors; removing names does not remove identifiability |
| **The gold standard is a value judgement** | somebody decided *Tamil Nadu* is a GPE and what counts as "toxic"; that decision is not neutral and should be documented |

### ⚠️ The one specific to this unit

**Stopword removal deletes negation.** "The film was not good" becomes "film
good". Applied to a complaints corpus or a medical note, **that is not a
performance issue; it inverts the meaning of the record.**

> **The general principle:** every preprocessing step discards information,
> and you must be able to say *what* it discards and *for whom* that matters.
> "It is standard practice" is not an answer.

---

## What to be able to do after this unit

- [ ] List the main NER labels and distinguish `GPE` from `LOC`
- [ ] Explain the BIO scheme and why `B` and `I` are both needed
- [ ] **Explain domain shift** using the Andhra Pradesh / Tamil Nadu failures
- [ ] Give two fixes for a pre-trained NER model on your own domain
- [ ] Compute a TF-IDF weight and explain what IDF does
- [ ] **Explain why bag-of-words ranked an unrelated document above a paraphrase**
- [ ] Give the n-gram argument with the dog/man example
- [ ] State the distributional hypothesis
- [ ] **Compare CBOW and skip-gram**, and say when each is better
- [ ] **Explain why negative sampling exists**
- [ ] Distinguish Word2Vec from GloVe
- [ ] Give the pipeline in order, and say why the vectoriser is fitted on train only
- [ ] **Compare a model gap against the cross-validation spread before claiming a winner**
- [ ] Name three ethical concerns with a mechanism for each

**Cross-check yourself:** run
`07_parsing_ner_similarity.py`
and
`10_sentiment_rnn.py`.
