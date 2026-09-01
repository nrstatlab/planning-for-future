# Course 15 A — Laboratory

**14 practicals**

Every number on this page was **printed by code in this repository**:

```bash
python3 tools/run_nlp_labs.py
```

---

## What ran, and what did not

**Eleven of the fourteen experiments run against real corpora and real
models.**

| # | Experiment | File | Status |
|---|---|---|---|
| 1 | Install NLTK, spaCy; list corpora and models | `01_setup_regex.py` | **runs** |
| 2 | Regex for emails, phones, hashtags, dates | `01_setup_regex.py` | **runs — and is scored** |
| 3 | Lexical and structural ambiguity, parse trees | `03_ambiguity_tokenize.py` | **runs** |
| 4 | Tokenization, NLTK vs spaCy | `03_ambiguity_tokenize.py` | **runs** |
| 5 | Stopword removal and length reduction | `03_ambiguity_tokenize.py` | **runs — real Brown corpus** |
| 6 | Stemming vs lemmatization | `03_ambiguity_tokenize.py` | **runs — real WordNet** |
| 7 | Top-down and bottom-up parsing | `07_parsing_ner_similarity.py` | **runs** |
| 8 | spaCy NER on news text | `07_parsing_ner_similarity.py` | **runs — and is scored** |
| 9 | Text representation and similarity | `07_parsing_ner_similarity.py` | **runs** |
| 10 | Sentiment classifier, scikit-learn | `10_sentiment_rnn.py` | **runs — 2,000 real reviews** |
| 11 | Character-level RNN generation | `10_sentiment_rnn.py` | **runs — real Austen** |
| 12 | BERT masked-word prediction | `12_bert_mlm.md` | ***NOT EXECUTED*** — HF is 403 |
| 13 | Extractive + abstractive summarization | `13_summarization.md` | ***NOT EXECUTED*** — the abstractive half |
| 14 | FAQ chatbot on transformer embeddings | `14_faq_chatbot.md` | ***NOT EXECUTED*** — HF is 403 |

**All three blocked experiments have a runnable half** in
`12_transformer_local.py`, which trains a bidirectional transformer encoder
with a masked-LM objective, builds TextRank extractive summarization, and
scores an FAQ retriever. `tools/run_nlp_labs.py` asserts all three
`*** NOT EXECUTED ***` markers survive.

---

## Experiment 1 — the toolchain

| Tool | Version |
|---|---|
| NLTK | 3.10.3 |
| spaCy | 3.8.16 (`en_core_web_sm`) |
| scikit-learn | 1.9.0 |

spaCy's pipeline: `['tok2vec', 'tagger', 'parser', 'attribute_ruler',
'lemmatizer', 'ner']` — **components run in order**, which is why
`nlp.pipe(..., disable=[...])` is the fix when spaCy is slow.

| Corpus | Size |
|---|---|
| **brown** | **1,161,192 words**, 15 genres |
| **treebank** | **3,914 parsed sentences** |
| **movie_reviews** | **2,000 documents**, `['neg', 'pos']` |
| **reuters** | **10,788 documents**, 90 topics |
| gutenberg | 18 texts |
| stopwords | 179 English words |
| **wordnet** | a lexical database, **not a corpus** |

---

## Experiment 2 — regular expressions, scored

| Pattern | Precision | Recall | F1 |
|---|---|---|---|
| emails | 1.000 | 1.000 | **1.000** |
| hashtags | 1.000 | 1.000 | **1.000** |
| dates | 1.000 | 1.000 | **1.000** |
| phones | 1.000 | 1.000 | **1.000** |

Scored against a hand-labelled text containing deliberate near-misses:
`asha at nrigroup dot ac dot in`, the handle `@nri_official`, `C#`, and a
number too short to be a phone number.

### The naive pattern, and what it costs

| Pattern | On `asha.reddy@nrigroup.ac.in` |
|---|---|
| `\w+@\w+` | **`reddy@nrigroup`** |

`\w` does not match `.` or `-`, **so it truncates silently** — and the output
still looks like a list of emails.

### Greedy vs lazy

| Pattern | On `<b>bold</b> and <i>italic</i>` |
|---|---|
| `<.*>` | `['<b>bold</b> and <i>italic</i>']` |
| `<.*?>` | `['<b>', '</b>', '<i>', '</i>']` |

### Where regex stops working

| True sentences | Split on `"."` gives |
|---|---|
| 2 | **5** |
| 1 | **4** |

---

## Experiment 3 — ambiguity

| Word | WordNet senses |
|---|---|
| **bank** | **18** |
| duck | 8 |
| run | 57 |

*"I saw the man with the telescope"* has **exactly 2 parses** under the lab's
CFG — the PP attaching to the VP or to the NP, both grammatical, with nothing
in the sentence to choose.

---

## Experiment 4 — tokenization

On `Dr. Reddy didn't visit the U.S.A. in 2024. He said, "It's far!" -- the
trip cost Rs. 1,20,000. Email: a.b@nri.ac.in`:

| Method | Sentences |
|---|---|
| split on `"."` | over-counts badly |
| NLTK `sent_tokenize` | correct-ish |
| spaCy | correct-ish, **and disagrees with NLTK** |

**Neither trained tokeniser is "correct" in the abstract.** They were trained
on different annotation guidelines, and abbreviations are where guidelines
differ. **Report which tokeniser you used.**

---

## Experiment 5 — stopwords

On 100,000 words of Brown: **roughly 50% of tokens removed, and almost none of
the vocabulary.**

| Sentence | After removal |
|---|---|
| "to be or not to be" | **(empty)** |
| **"The film was not good"** | **"film good"** |
| "Who is she?" | **(empty)** |

---

## Experiment 6 — stemming vs lemmatization

| Word | Porter | Lemma (noun) | Lemma (verb) |
|---|---|---|---|
| **ran** | ran | ran | **run** |
| **better** | better | better | *(adj: **good**)* |
| **university** | **univers** | university | university |
| **universal** | **univers** | universal | universal |
| **was** | wa | **wa** | **be** |

**`university` and `universal` collapse to the same stem** — over-stemming.
**`was` → `wa` untagged** is not an English word, so "lemmatization always
returns a real word" is only true when the tag is right.

---

## Experiment 7 — parsing

| Parser | Parses found |
|---|---|
| RecursiveDescent (top-down) | 2 |
| ShiftReduce (bottom-up) | **fewer — it is greedy** |
| **Chart (dynamic programming)** | **2** |

**Shift-reduce commits to a reduction and never backtracks.** The rule that
kills a top-down parser is `NP -> NP PP` — **left recursion**, not ambiguity.

---

## Experiment 8 — NER, scored against 13 hand-labelled entities

**11 of 13 exactly right, 2 wrong labels, 0 missed.**

| Entity | spaCy | Truth | |
|---|---|---|---|
| Infosys | ORG | ORG | ✓ |
| Hyderabad | GPE | GPE | ✓ |
| Bengaluru | GPE | GPE | ✓ |
| Salil Parekh | PERSON | PERSON | ✓ |
| Siddaramaiah | PERSON | PERSON | ✓ |
| **Andhra Pradesh** | **ORG** | GPE | ✗ |
| **Tamil Nadu** | **PERSON** | GPE | ✗ |

**Both failures are states; both cities were correct.** `en_core_web_sm` was
trained on OntoNotes — mostly American news — so Indian state names are rare
and the model falls back on surface cues.

### The gazetteer fix

Nine lines of `EntityRuler` patterns took it from **11/13 to 13/13**. When
your domain has a closed list of entities, matching it beats inference.

### And a lesson about the gold standard

spaCy also found `2,400` (CARDINAL) and `three years` (DATE), **which were not
in the hand-built truth list — and both are correct.** The gold list was
incomplete. **Annotate exhaustively, or state which categories you covered.**

---

## Experiment 9 — text representation

| Representation | Features | sim 0-1 | **sim 0-2** | **sim 0-3** |
|---|---|---|---|---|
| bag of words | 28 | 0.8006 | **0.0925** | **0.3077** |
| BoW, binary | 28 | 0.7379 | 0.1054 | 0.1000 |
| TF-IDF | 28 | 0.6993 | **0.0766** | **0.1802** |
| TF-IDF, 1-2 grams | 61 | 0.5018 | 0.0380 | 0.0892 |
| TF-IDF, char 3-5 grams | 409 | 0.6727 | 0.0332 | 0.1093 |

Document 2 is a **paraphrase** of document 0; document 3 is about the monsoon.

> **Bag-of-words ranks the unrelated document (0.3077) above the paraphrase
> (0.0925).** Documents 0 and 3 share `the`, `and`, `are` — function words and
> nothing else. TF-IDF narrows the gap but does not reverse it.

### What IDF is

| | Words |
|---|---|
| Lowest IDF | `of`, `the`, `said`, `to`, `and`, `in` |
| Highest IDF | rare tokens and numbers |

**IDF is a learned stopword list**, derived from your corpus.

### N-grams and word order

| | `the dog bit the man` vs `the man bit the dog` |
|---|---|
| unigrams | **1.0000 — identical** |
| bigrams | 0.7500 |

---

## Experiment 10 — sentiment classification

NLTK `movie_reviews`: 2,000 documents, 1,500 train / 500 test, perfectly
balanced, mean length 746 words.

| Model | Features | Accuracy |
|---|---|---|
| **majority class** | — | **0.5000** |
| **Naive Bayes, counts** | 35,466 | **0.8240** |
| Naive Bayes, TF-IDF | 35,466 | 0.8060 |
| LogReg, TF-IDF | 35,466 | 0.8160 |
| LogReg, TF-IDF, no stopwords | 35,323 | 0.8220 |
| LogReg, TF-IDF 1-2 grams | 110,116 | 0.8180 |

Confusion matrix for the best model: **206 / 44 / 44 / 206** — errors evenly
split, macro-F1 0.82.

### 5-fold cross-validation

`[0.8225, 0.825, 0.825, 0.8175, 0.8175]` — **mean 0.8215, spread 0.0075.**

| Comparison | Gap | Verdict |
|---|---|---|
| stopwords on vs off | 0.0060 | **noise** |
| best vs second-best | 0.0080 | **noise** |
| **best vs baseline** | **0.3240** | **real** |

> **Every difference between the real models is smaller than the variation
> between folds.** The honest conclusion is that they are indistinguishable on
> this data — and that is the finding most lab reports get wrong.

---

## Experiment 11 — character-level generation

Jane Austen's *Emma* from NLTK's Gutenberg corpus: **119,232 characters, 47
distinct, 39,724 training sequences, 197,183 parameters.**

**Perplexity fell from ~6.5 to ~2.7**, against **47** for uniform guessing.

| `T` | Sample |
|---|---|
| 0.2 | conservative, repetitive |
| 1.0 | `'full bideal of one profors. an having on this being so superior for harriet.'` |
| **1.6** | `'well-just. she, troublebond as earful... mrs. meepleavule.'` |

**Correct spelling, plausible word boundaries, no meaning** — which is exactly
what a character model can learn.

---

## Experiment 12 — masked language modelling (mechanism)

A **2-layer bidirectional transformer encoder** trained on the Brown corpus
with BERT's masked-LM objective.

| | This model | `bert-base-uncased` |
|---|---|---|
| Parameters | ~700 K | **110,000,000** |
| Training words | ~200 K | **3,300,000,000** |

**Its top prediction is usually `<unk>`** — "some word I do not have" — which
is a correct prediction about the *data* and useless about the *sentence*.
Strip the special tokens and what remains is function words.

> **The small model learned the shape of English and none of the facts.** That
> gap is what pre-training buys, and you can only see its size by training the
> small version yourself.

The full BERT code is in
`12_bert_mlm.md`, marked NOT
EXECUTED.

---

## Experiment 13 — summarization (extractive half)

A real Reuters article: **2,858 characters, 22 sentences.**

| Method | Sentences chosen |
|---|---|
| **TextRank** (PageRank over TF-IDF similarity) | 1, 3, 14 |
| **Lead-3 baseline** | 0, 1, 2 |

**They agree on one of three.** Lead-3 is a genuinely strong summarizer on
news because news is front-loaded — **and it is the baseline nobody reports.**

The abstractive half needs BART or T5 and is in
`13_summarization.md`,
marked NOT EXECUTED.

---

## Experiment 14 — FAQ retrieval, scored

Six FAQ entries, six test queries, **none copying an FAQ question**.

| Representation | Correct | Accuracy |
|---|---|---|
| TF-IDF, words | 5 / 6 | 0.8333 |
| TF-IDF, words, no stopwords | 5 / 6 | 0.8333 |
| **TF-IDF, character 3-5 grams** | **6 / 6** | **1.0000** |

**Character n-grams got every one**, because *exams* and *examination* share
`exam`, `xam`. **On this FAQ there is nothing for a transformer to improve.**

### The one word-level failure

| | |
|---|---|
| Query | `when are the exams` |
| Matched | "What are the library opening hours?" — **0.4014** |
| Should have | "When does the semester examination begin?" — **0.4014** |

**An exact tie, broken by list order** — and both matches came only from the
function words *are*, *the*, *when*.

### The threshold

`what is the wifi password` → best similarity **0.3561** against an unrelated
entry. **`argmax` always returns something.**

The sentence-transformer version is in
`14_faq_chatbot.md`, marked
NOT EXECUTED.

---

## Running it yourself

```bash
pip install -r tools/requirements.txt
python3 -m spacy download en_core_web_sm
python3 tools/fetch_nlp_data.py     # 17 NLTK corpora
python3 tools/run_nlp_labs.py
```

The whole suite takes a few minutes on CPU, most of it in experiments 11
and 12.
