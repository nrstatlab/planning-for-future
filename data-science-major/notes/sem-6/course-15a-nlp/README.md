# Course 15 A — Natural Language Processing

**Semester VI**

**This is a Track A course**, paired with
Course 14 A (Neural Networks & Deep Learning),
and it is the last course of the track you began in Semester V.

---

## The one thing to understand before anything else

**Every other course in this programme works on data that was already
numeric, or was numeric once you encoded it. Language is not, and every
technique here is an answer to the question "how do I turn this text into
numbers without throwing away what it means?"**

The course is essentially four answers to that question, in increasing order
of power and cost:

| Answer | Represents | Cannot represent |
|---|---|---|
| **Bag of words** | which words appear | word order, or that two words mean the same |
| **N-grams** | short local order | anything beyond `n` |
| **Word embeddings** (Word2Vec, GloVe) | that "fee" and "cost" are related | that "bank" has two senses |
| **Contextual embeddings** (BERT) | a different vector per occurrence | — but needs enormous pre-training |

### 🎯 The single most examinable idea

> **Ambiguity is not an edge case in language; it is the normal condition.**
> "I saw the man with the telescope" has two grammatical parses and nothing in
> the sentence chooses between them. "The bank was closed" has 18 WordNet
> senses for one word.
>
> Every NLP technique is, at bottom, a way of choosing among readings — and
> the ones that work choose using **context**, which is why the field ended up
> at contextual embeddings.

### ⚠️ The measurement that makes the point

[Experiment 9](lab.md#experiment-9) compares four documents where the answer
is known in advance. Two of them are paraphrases; a third is about the
monsoon. **Bag-of-words scores the paraphrase at 0.0925 and the unrelated
document at 0.3077** — it ranks the wrong one higher, because documents 0 and
3 share "the", "and" and "are" and nothing else.

**A representation that ranks by function words is not measuring meaning at
all**, and that single table is the argument for everything in Units 3–5.

---

## What runs here

**Eleven of the fourteen experiments run against real corpora and real
models.**

| Tool | What it is here |
|---|---|
| **NLTK** 3.10 | Brown (1.16M words), Reuters (10,788 docs), Penn Treebank (3,914 parsed sentences), movie_reviews (2,000 labelled), Gutenberg, WordNet |
| **spaCy** 3.8 with `en_core_web_sm` | real NER, real dependency parsing, real tokenization |
| **scikit-learn** 1.9 | the classification pipeline, TF-IDF, cross-validation |
| **PyTorch** | a character LSTM and a transformer encoder, both trained here |

### The three that do not run

All three fail for the same reason: **`huggingface.co` is refused by this
environment's egress policy with a 403 at the gateway.**

| # | Experiment | File | Its runnable half |
|---|---|---|---|
| 12 | BERT masked-word prediction | `12_bert_mlm.md` | a bidirectional transformer encoder **trained here** on Brown with a masked-LM objective |
| 13 | Abstractive summarization | `13_summarization.md` | **extractive** TextRank on a real Reuters article, scored against lead-3 |
| 14 | FAQ chatbot on embeddings | `14_faq_chatbot.md` | the same retriever on TF-IDF, **scored** against hand-labelled answers |

**The runnable halves are not filler.** In each case the architecture is
identical and only the embedding function differs — which is precisely what
makes the comparison instructive. Training the small version yourself is how
you find out what pre-training on billions of words actually buys.

`tools/run_nlp_labs.py` asserts all three `*** NOT EXECUTED ***` markers are
still present.

### 📖 Why so much is scored rather than shown

Where an experiment could have printed "it worked", this course **scores it
against hand-labelled truth** instead:

| Experiment | What is graded |
|---|---|
| 2 — regex | precision, recall and F1 against a labelled contact list containing deliberate near-misses |
| 8 — NER | spaCy's output against 13 hand-assigned entity labels |
| 9 — similarity | four documents whose correct ranking is known |
| 14 — retrieval | six queries with known answers, none copying an FAQ question |

**Three of those scores came out worse than expected, and the notes explain
them rather than hide them.** That is the point of grading.

---

## Course objectives (verbatim)

1. Introduce the foundations of Natural Language Processing and its
   applications in real-world tasks.
2. Familiarize students with text preprocessing, linguistic analysis, and
   parsing techniques.
3. Equip learners with methods for information extraction, word
   representations, and sentiment classification.
4. Explore deep learning techniques for NLP, including RNNs, LSTMs, GRUs, and
   Transformers.
5. Provide hands-on experience with modern NLP tools (NLTK, spaCy, Hugging
   Face) for implementing applications such as chatbots, summarization, and
   document classification.

## The five units

| Unit | Topic | Notes | Hardest part |
|---|---|---|---|
| 1 | NLP fundamentals, ambiguity, regex | [unit-1.md](unit-1.md) | the three kinds of ambiguity, told apart |
| 2 | Preprocessing, morphology, grammar, parsing | [unit-2.md](unit-2.md) | CYK, and why top-down parsers loop |
| 3 | NER, embeddings, classification | [unit-3.md](unit-3.md) | what Word2Vec learns and how |
| 4 | Deep learning for NLP | [unit-4.md](unit-4.md) | RNN against CNN against transformer, honestly compared |
| 5 | Transformers and modern NLP | [unit-5.md](unit-5.md) | BERT vs GPT, and summarization's failure modes |

Plus [lab.md](lab.md) — all fourteen experiments with their measured output —
and [practice.md](practice.md) — exam questions with worked solutions.

---

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 14 practicals
- `labs/course-15a-nlp/` — the code, and the runner that asserts every figure
  these notes quote
- `data/course-15a-nlp/` — **practice datasets**, CSV: `ner-sentences.csv`, `sentiment-reviews.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.

## How this course connects to the rest of the programme

| Course | What it gives you here |
|---|---|
| **Course 3** (Python) | string handling and regular expressions |
| **Course 9** (Python for Data Analysis) | the pipeline and the train/test discipline |
| **Course 12 A** (Machine Learning) | the classifier, the baselines, cross-validation |
| **Course 14 A** (Deep Learning) | **the RNN, LSTM and attention material is shared** — study Unit 4 of both together |
| **Course 8** (Data Mining) | TF-IDF and similarity measures |

> ### 💡 Read Course 14 A's Units 4 and 5 alongside this course's Units 4 and 5
>
> They cover the same architectures from two directions. Course 14 A builds
> attention from scratch and measures it; this course applies it to language.
> **Doing them in the same week roughly halves the work.**

---

## Textbooks

- Pulari, Maramreddy & Vasudevan, *Natural Language Processing*, Oxford
  University Press — the prescribed text, and the closest match to Units 1–3.
- Jurafsky & Martin, *Speech and Language Processing*, Pearson, 2023 — the
  standard reference for the whole field. **Draft chapters of the 3rd edition
  are free** from the authors, and they are the current ones for Units 4 and 5.

**References:** Siddiqui & Tiwary, *Natural Language Processing and Information
Retrieval*, Oxford University Press · Kulkarni & Shivananda, *Natural Language
Processing Recipes*, Apress, 2019.

> ### ⚠️ The second reference is numbered "2. 2."
>
> The list reads "Reference Book: 1. … 2. **2.** Natural Language Processing
> Recipes …" — a duplicated numeral, not a missing entry. There are two
> reference books, not three. See review finding **D27**.

## How to study this course

1. **Install NLTK and spaCy on your own machine, and download the models.**
   `python -m spacy download en_core_web_sm` is the step everyone forgets, and
   nothing in Units 2–3 runs without it.
2. **Tokenize a real paragraph in both, side by side.** NLTK and spaCy disagree
   on contractions, hyphens and punctuation, and seeing where is worth more
   than the definition of a token.
3. **Learn the difference between stemming and lemmatization by example.**
   `studies` → `studi` against `study` answers the exam question in one line.
4. **Do the parsing by hand.** CYK on a five-word sentence is tedious exactly
   once, and then the algorithm is obvious. This is the unit students skip and
   then lose ten marks on.
5. **Score your own output.** Every result in these notes is checked against
   hand-labelled truth rather than eyeballed — that is how it emerged that
   bag-of-words ranked an unrelated document above a paraphrase, and that spaCy
   mislabels two Indian state names while getting both cities right.
6. **Do not wait for a GPU.** Everything up to Unit 4 runs on a laptop CPU, and
   the transformer material can be understood from the mechanism before it is
   ever run at scale.

## If you read one thing

**Unit 1's section on ambiguity**, and then run
`03_ambiguity_tokenize.py`.

Six sentences, each ambiguous in a documented way, with WordNet sense counts
and actual parse trees for the structural cases. **Everything else in the
course is a technique for resolving what those six sentences demonstrate**,
and the techniques make far more sense once you have seen the problem clearly.
