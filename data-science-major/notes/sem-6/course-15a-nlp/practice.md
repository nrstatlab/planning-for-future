# Course 15 A — Practice Questions with Worked Solutions

Grouped by unit. **Attempt each before reading the solution.** Numeric answers
that come from the lab name the file that printed them.

---

## Unit 1 — Fundamentals and ambiguity

### Q1. Distinguish lexical, structural and contextual ambiguity, with an example of each. *(6 marks)*

<details><summary>Solution</summary>

| Kind | What varies | Example |
|---|---|---|
| **Lexical** | one **word** has several senses | "The **bank** was closed." — financial or river |
| **Structural** | one word sequence has several **parse trees** | "I saw the man with the telescope." |
| **Contextual** | words and structure fixed; **reference or intent** is not | "Can you pass the salt?" — question or request |

**The distinction that earns the marks:** lexical ambiguity gives one
structure and several meanings; structural ambiguity gives unambiguous words
and several groupings; contextual ambiguity leaves both fixed and the meaning
still undetermined.

**Verified:** `03_ambiguity_tokenize.py` reports **18 WordNet senses for
"bank"** and finds **exactly 2 parses** for the telescope sentence.
</details>

### Q2. Why is "The old man the boats" grammatical? *(4 marks)*

<details><summary>Solution</summary>

**"man" is the verb** (to man, to staff) and **"the old"** is the subject — a
nominalised adjective meaning "old people".

`[The old]ₙₚ [man the boats]ᵥₚ` — "Old people staff the boats."

It is a **garden-path** sentence: the reader commits early to *the old man* as
a noun phrase and cannot cheaply revise. **A parser fails for the same reason
you do.**
</details>

### Q3. Explain greedy vs lazy quantifiers, with a worked example. *(4 marks)*

<details><summary>Solution</summary>

**`*` is greedy**: it consumes as much as possible and gives back only what it
must. **`*?` is lazy**: it consumes as little as possible.

On `<b>bold</b> and <i>italic</i>`:

| Pattern | Result |
|---|---|
| `<.*>` | `['<b>bold</b> and <i>italic</i>']` — **one match, the whole line** |
| `<.*?>` | `['<b>', '</b>', '<i>', '</i>']` |

**One character, completely different behaviour** — and the most common cause
of a regex that "works on one example".

**Verified:** `01_setup_regex.py`.
</details>

### Q4. `re.findall(r'\w+@\w+', text)` returns `reddy@nrigroup` for the address `asha.reddy@nrigroup.ac.in`. Explain and fix. *(5 marks)*

<details><summary>Solution</summary>

**`\w` matches `[A-Za-z0-9_]` only — not `.` or `-`.** So the match starts
after the dot in `asha.` and stops at the dot in `.ac`.

Fix:

```python
r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
```

> **Why this bug survives into production:** the output is still a list of
> plausible-looking email addresses. Nothing raises an error, and the failure
> is only visible if you compare against ground truth — which is why
> `01_setup_regex.py` scores its patterns rather than printing them.
</details>

---

## Unit 2 — Preprocessing and parsing

### Q5. Why can sentence tokenization not be done by splitting on "."? *(4 marks)*

<details><summary>Solution</summary>

**Abbreviations contain full stops that do not end sentences** — *Dr.*,
*U.S.A.*, *p.m.*, *Rs.*, *B.Sc.*, decimal points, ellipses.

The lab measures it:

| True sentences | Naive split gives |
|---|---|
| 2 | **5** |
| 1 | **4** |

**The right tool is a trained tokeniser** (`nltk.sent_tokenize`, spaCy) which
has learned which full stops are terminal. **A regex is right for a pattern
you can write down; sentence boundaries are not one.**
</details>

### Q6. Compare stemming and lemmatization on `ran`, `better` and `university`/`universal`. *(6 marks)*

<details><summary>Solution</summary>

| Word | Porter | Lemma |
|---|---|---|
| **ran** | **ran** | **run** (with the verb tag) |
| **better** | better | **good** (as an adjective) |
| university | **univers** | university |
| universal | **univers** | universal |

1. **`ran` → Porter leaves it.** A stemmer chops suffixes and *ran* has none;
   the change is internal. A lemmatiser looks it up in WordNet.
2. **`better` → `good`** requires a dictionary of irregular forms. No amount
   of string surgery finds it.
3. **`university` and `universal` collapse to one stem** — two unrelated words
   become one feature. **That is over-stemming**, a genuine precision loss.

| | Stemming | Lemmatization |
|---|---|---|
| Needs | nothing | **WordNet + a POS tag** |
| Speed | very fast | slower |
| Output | may not be a word | a real word **if the tag is right** |

**Verified:** `03_ambiguity_tokenize.py`.
</details>

### Q7. `lemmatize("was")` returns `"wa"`. Explain. *(4 marks)*

<details><summary>Solution</summary>

**`WordNetLemmatizer.lemmatize()` defaults to POS = noun.** Asked for the
singular of the noun *was*, it applied the plural rule and stripped the `s`,
producing a string that is **not an English word at all**.

`lemmatize("was", "v")` returns **`be`**, which is correct.

> **This is the most common silent mistake in NLP coursework.** Every tutorial
> that calls `lemmatize(w)` without a tag is asking the wrong question of
> every verb in the text. **Tag first, then lemmatise.**
>
> It also qualifies the usual claim: "lemmatization always returns a real
> word" is only true when the tag is right.
</details>

### Q8. Why does a top-down parser fail on `NP -> NP PP`? *(5 marks)*

<details><summary>Solution</summary>

**Left recursion.** To parse an NP, recursive descent applies the rule and
must first parse an NP, which applies the rule again… **it recurses without
consuming any input and never terminates.**

| Parser | Handles it? |
|---|---|
| Top-down (recursive descent) | **no — infinite recursion** |
| Bottom-up (shift-reduce) | **yes** — it builds from the words up |
| Chart (CYK, Earley) | **yes** — partial results are memoised |

**The answer is "left recursion", not "ambiguity"** — which is the trap in
this question.

Fix by rewriting: `NP -> N NP'`, `NP' -> PP NP' | ε`.
</details>

### Q9. State the CYK algorithm and derive its complexity. *(6 marks)*

<details><summary>Solution</summary>

**Requires Chomsky Normal Form** — every rule is `A → B C` or `A → w`.

```
for i in 0..n-1:                       # length-1 spans
    table[i][i+1] = {A : A -> w_i}

for length in 2..n:
    for i in 0..n-length:
        j = i + length
        for k in i+1..j-1:             # every split point
            for each rule A -> B C:
                if B in table[i][k] and C in table[k][j]:
                    add A to table[i][j]

accept if S in table[0][n]
```

**Complexity:** three nested loops over `length`, `i` and `k` give **O(n³)**,
times the grammar size, so **O(n³·|G|)**. Space is **O(n²)**.

**It finds all parses**, because a cell holds every non-terminal deriving that
span — which is what makes it dynamic programming rather than search.
</details>

---

## Unit 3 — Extraction and representation

### Q10. spaCy labels "Andhra Pradesh" as ORG and "Tamil Nadu" as PERSON, but gets Hyderabad and Bengaluru right. Explain and give two fixes. *(6 marks)*

<details><summary>Solution</summary>

**Domain shift.** `en_core_web_sm` was trained on **OntoNotes**, which is
mostly American news. Indian **state** names are rare in it, so the model has
no learned representation and falls back on surface cues — *Tamil Nadu* has
the shape of a two-token personal name.

**The cities were correct**, which localises the failure: the model has seen
major Indian cities and not the states.

| Fix | When it is right |
|---|---|
| **Gazetteer** via spaCy's `EntityRuler` | your domain has a **closed list** of entities |
| **Fine-tune** on a few hundred annotated sentences of your own domain | the list is open |

The lab adds **nine lines of `EntityRuler` patterns and recovers the wrong
labels.**

> **The model is not broken.** It is being used outside its training
> distribution, and the errors are **systematic rather than random** — which
> means they are predictable and fixable. A bigger model is not the answer.
</details>

### Q11. Bag-of-words scores a paraphrase at 0.0925 and an unrelated document at 0.3077. Explain. *(6 marks)*

<details><summary>Solution</summary>

Documents 0 and 2 are paraphrases — *"the model learns weights from the
training data by gradient descent"* and *"parameters are fitted to
observations by iteratively minimising a loss"*. They share **almost no
strings**.

Documents 0 and 3 (about the monsoon) share **`the`, `and`, `are`** — function
words and nothing else.

> **The similarity is entirely an artefact of English grammar.** A
> representation that ranks by function words is not measuring meaning.

**TF-IDF narrows the gap** (0.0766 vs 0.1802) because IDF discounts words that
appear in every document — **but it does not reverse the ordering, and no
count-based representation can.** *weights* and *parameters* are different
strings and nothing in the counts says otherwise.

**This is exactly the failure word embeddings were invented for.**

**Verified:** `07_parsing_ner_similarity.py`.
</details>

### Q12. Compare CBOW and skip-gram. *(5 marks)*

<details><summary>Solution</summary>

| | **CBOW** | **Skip-gram** |
|---|---|---|
| Predicts | the **centre** word from its context | the **context** from the centre word |
| Direction | many → one | one → many |
| Speed | **faster** | slower |
| Rare words | worse | **better** |
| Small corpora | worse | **better** |

**Remember by direction:** CBOW collapses context *into* a word; skip-gram
fans a word *out* into its context.

**Why skip-gram is better on rare words:** each occurrence generates several
training pairs (one per context word), so a word seen five times still
produces meaningful gradient. CBOW averages the context and a rare centre word
contributes to only one prediction.
</details>

### Q13. Why does Word2Vec use negative sampling? *(5 marks)*

<details><summary>Solution</summary>

**The naive objective requires a softmax over the whole vocabulary at every
training step** — hundreds of thousands of exponentials per example, which is
computationally impossible at corpus scale.

**Negative sampling** replaces it with a binary task: for each true (word,
context) pair, draw `k` random "negative" pairs and train a classifier to tell
them apart.

| | Cost per example |
|---|---|
| Full softmax | **\|V\|** — say 500,000 |
| Negative sampling | **k + 1** — typically 6 to 21 |

Negatives are drawn from the unigram distribution raised to the **3/4 power**,
which up-samples rare words relative to their frequency.

**The one-line answer: the full softmax over the vocabulary is computationally
impossible.**
</details>

### Q14. Six sentiment models score between 0.8060 and 0.8240, and 5-fold CV gives a spread of 0.0075. What do you conclude? *(6 marks)*

<details><summary>Solution</summary>

**That the models are indistinguishable on this data**, and that no ranking
among them is defensible.

| Comparison | Gap | Verdict |
|---|---|---|
| stopwords on vs off | 0.0060 | **noise** — smaller than the fold spread |
| best vs second-best | 0.0080 | **noise** |
| **best vs the majority baseline** | **0.3240** | **real** |

**Only the gap to the baseline is far outside the spread.**

> **This is the finding most lab reports get wrong.** They rank six models on
> a single train/test split and declare a winner that a different random seed
> would reverse. A single split gives you **one draw** from the distribution
> whose width the cross-validation is measuring.

**The correct report:** "all six models reach roughly 0.82, indistinguishable
within a fold spread of 0.0075, against a 0.50 baseline."

**Verified:** `10_sentiment_rnn.py`.
</details>

### Q15. Name three ethical concerns in NLP preprocessing and classification, with a mechanism for each. *(6 marks)*

<details><summary>Solution</summary>

| Concern | Mechanism |
|---|---|
| **Bias in embeddings** | `doctor − man + woman ≈ nurse` is reproducible on standard embeddings — the geometry learned the corpus's prejudices from the same statistics as its facts |
| **Preprocessing that erases meaning** | **stopword removal deletes negation**: "The film was not good" → "film good". On a complaints corpus or a medical note this **inverts the record** |
| **Dialect penalties** | classifiers trained on standard written English systematically score non-standard dialects lower — a documented harm in automated essay scoring |
| **The gold standard is a value judgement** | somebody decided what counts as "toxic", and that decision is not neutral |

> **The general principle: every preprocessing step discards information, and
> you must be able to say what it discards and for whom that matters.** "It is
> standard practice" is not an answer.
</details>

---

## Unit 4 — Deep learning for NLP

### Q16. Compare RNN, CNN and feedforward networks for text. *(6 marks)*

<details><summary>Solution</summary>

| | **Feedforward** | **CNN** | **RNN** |
|---|---|---|---|
| Input length | **fixed** | variable (with pooling) | **variable** |
| What it sees | everything at once | a **window** of `k` words | the whole prefix, serially |
| Word order | ignored | **local order only** | **full order** |
| Parallel | yes | **yes** | **no** |
| Good at | nothing much, for text | local phrase patterns | agreement, structure |

**A CNN over text is an n-gram detector with learned filters.** That is
genuinely useful for sentiment — where a few key phrases decide the label —
which is why CNNs stayed competitive on sentiment long after RNNs won
elsewhere.
</details>

### Q17. An LSTM beats a plain RNN by 0.3375 on a constructed dataset and by 0.0833 on real IMDb. Explain. *(6 marks)*

<details><summary>Solution</summary>

**Sentiment in a real review is redundant.** "Terrible", "waste", "boring" and
"awful" may all appear in one paragraph, so a weaker model that catches **any
one** of them still classifies correctly.

The constructed dataset had **exactly one decisive word per sentence and no
redundancy**, so missing it meant getting the example wrong.

> **Both numbers are real and they measure different things.** Redundancy in
> real data masks differences between models — a general fact about
> benchmarking, not a fact about LSTMs. Reporting only the flattering number
> would be dishonest.

**Verified:** Course 14 A's `09_rnn_lstm.py`.
</details>

### Q18. Define perplexity and say what value means "no better than guessing". *(4 marks)*

<details><summary>Solution</summary>

**Perplexity = exp(cross-entropy loss)**, and it reads as *"the model is as
uncertain as if it were choosing uniformly among this many options"*.

**Uniform guessing over an alphabet of size `V` gives perplexity `V`.**

The lab's character model on Austen: **47 distinct characters**, so 47 is the
baseline. **Perplexity fell from ~6.5 to ~2.7** — the model is effectively
choosing among fewer than three characters.

**Why perplexity rather than loss:** the number means something on its own,
against a baseline anyone can compute.
</details>

### Q19. State the architectural difference between BERT and GPT and what each cannot do. *(5 marks)*

<details><summary>Solution</summary>

| | **BERT** | **GPT** |
|---|---|---|
| Architecture | transformer **encoder** | transformer **decoder** |
| Attention | **bidirectional** | **causal** — left context only |
| Pre-training | **masked language modelling** | **next-token prediction** |
| **Cannot** | **generate text** | **use right-hand context** |

**The masking is the entire architectural difference** — both are stacks of
the same block.

**Why BERT cannot generate:** it sees the whole sentence at once, so there is
no "next" token in its objective.

**Why GPT cannot use right context:** its attention is causally masked so
position `t` cannot attend past itself — which is what makes generation
coherent.
</details>

---

## Unit 5 — Transformers and modern NLP

### Q20. Why are attention scores divided by √d_k? *(6 marks)*

<details><summary>Solution</summary>

**The dot product of two random `d_k`-dimensional vectors has standard
deviation growing as `√d_k`.** Feed those raw scores to a softmax at large
`d_k` and one weight approaches 1 while the rest approach 0 — **the softmax
saturates, its gradient vanishes, and the model stops learning.**

| `d_k` | std of `Q·K` | std ÷ √d_k | max softmax weight |
|---|---|---|---|
| 4 | 2.025 | **1.013** | 0.1615 |
| 64 | 8.060 | **1.008** | 0.7146 |
| **1024** | **33.167** | **1.036** | **0.9857** |

**The third column is the point:** dividing by `√d_k` holds the score variance
at 1 whatever the dimension.

**Verified:** Course 14 A's `11_attention.py`.
</details>

### Q21. Give BERT's masking recipe in full and explain the parts most people omit. *(6 marks)*

<details><summary>Solution</summary>

**15% of tokens are picked.** Of those:

| Share | Replaced with |
|---|---|
| **80%** | `[MASK]` |
| **10%** | a **random** word |
| **10%** | **left unchanged** |

**Why the last two rows exist:** `[MASK]` never appears at fine-tuning or
inference time. If every masked position carried the literal `[MASK]` token,
the model would learn *"produce a good prediction only where I see `[MASK]`"*
and build no useful representation of any other position. The random and
unchanged cases force a good representation **everywhere**.

**Why 15%:** too low and most positions supply no signal, so training is slow;
too high and there is not enough context left to predict from. **It is a tuned
hyperparameter, not a law**, and later work has questioned it.
</details>

### Q22. Use the two "bank" sentences to explain why BERT is bidirectional. *(5 marks)*

<details><summary>Solution</summary>

| Sentence | Prediction |
|---|---|
| "The `[MASK]` was closed, so I could not **deposit the cheque**." | **`bank`** — financial |
| "The `[MASK]` was closed, so I could not **cross the river**." | **`bridge`/`bank`** — the other sense |

**The mask is in the same position in both. The disambiguating evidence is
entirely to its RIGHT.**

A left-to-right model cannot see it. **Only a bidirectional model can**, and
masked-LM training is possible *only* when the model may look both ways —
which is why BERT is an encoder.

**Word2Vec cannot do this at all**: it assigns *bank* one vector, for ever,
and WordNet lists **18 senses** for the word.
</details>

### Q23. Compare extractive and abstractive summarization, and say why regulated domains still use extractive. *(6 marks)*

<details><summary>Solution</summary>

| | **Extractive** | **Abstractive** |
|---|---|---|
| Mechanism | selects existing sentences | generates new text |
| Grammatical | **always** | usually |
| **Faithful to the source** | **guaranteed** | **not guaranteed** |
| Can compress or rephrase | no | **yes** |
| Needs a pre-trained model | **no** | yes |

**Why regulated domains stay extractive:** abstractive models **hallucinate**
— they produce text that is *probable*, not text that is *supported*.

> **An extractive summary of a medical report is at worst badly chosen; an
> abstractive one can state a dosage that appears nowhere in the source.**
> That is the argument, and it is not hypothetical.

**The check to run:** for every noun phrase, number and date in the generated
summary, search the source. **Anything not there is a hallucination. Report
the count** — it is worth more than any ROUGE score, which only measures
overlap and rewards copying.
</details>

### Q24. Why must a summarization report include the lead-3 baseline? *(4 marks)*

<details><summary>Solution</summary>

**Because news is deliberately front-loaded** — the inverted pyramid puts the
key facts in the first sentences — so *"take the first three sentences"* is a
genuinely strong summarizer, and it is free.

The lab's measurement on a 22-sentence Reuters article: **TextRank picked
sentences 1, 3, 14; lead-3 picked 0, 1, 2 — they agree on one of three.**

**Many published systems beat lead-3 by very little.** If your method cannot
beat it, **say so** — that is a result about the data, and omitting the
baseline is the most common flaw in summarization reports.
</details>

### Q25. A TF-IDF FAQ bot scores 5/6 with word features and 6/6 with character n-grams. What do you conclude, and when would embeddings help? *(6 marks)*

<details><summary>Solution</summary>

**That on this FAQ there is nothing for a transformer to improve**, and a
report claiming embeddings were necessary would be wrong.

**Why character n-grams win:** *exams* and *examination* share the substrings
`exam`, `xam`. Character n-grams recover much of the morphological robustness
people reach for embeddings to get, at **roughly zero cost**.

**The word-level failure is the instructive part:**

| | |
|---|---|
| Query | `when are the exams` |
| Matched | "What are the library opening hours?" — **0.4014** |
| Should have | "When does the semester examination begin?" — **0.4014** |

**An exact tie, broken by list order**, and both matches came only from the
function words *are*, *the*, *when*. **Neither had anything to do with
meaning.**

**Embeddings help when** entries share vocabulary, queries paraphrase without
sharing strings, or the FAQ grows large enough that keyword collisions become
common. **Report the baseline and let the numbers decide.**
</details>

### Q26. Why does every retrieval chatbot need a threshold? *(4 marks)*

<details><summary>Solution</summary>

**`argmax` always returns something.** There is no "none of these" option in a
maximum.

The lab asks *"what is the wifi password"*, which is not in the FAQ, and the
bot returns its nearest entry at similarity **0.3561** — confidently and
wrongly.

**The fix:** compare the top similarity against a threshold and return *"I
don't know"* below it. Tune the threshold on queries you know should fail.

> **A bot that says "I don't know" 20% of the time is useful. A bot that is
> confidently wrong 20% of the time is worse than no bot.** The metric to
> report is the **false-answer rate**, not accuracy.
</details>

---

## Long-answer questions

### L1. Design a complete sentiment-analysis project for 5,000 labelled Hinglish product reviews. *(15 marks)*

<details><summary>Solution outline</summary>

**1. Look at the data first.** Class balance, length distribution, and how
much is code-mixed. **Report the majority-class baseline before anything
else** — if 80% are positive, 0.80 accuracy is worthless.

**2. Tokenization is the first hard problem.** English tokenisers and English
stopword lists do not fit Hinglish. Romanised Hindi ("bahut accha") is not in
any English lexicon. **Character n-grams are unusually strong here** — the
FAQ experiment shows why — and are a sensible first representation.

**3. Do not strip stopwords.** *Not*, *nahi*, *no* carry the label. The lab's
"The film was not good" → "film good" is exactly the failure.

**4. Baselines, in order:**
- majority class
- TF-IDF word unigrams + logistic regression
- **TF-IDF character 3-5 grams** + logistic regression
- multilingual transformer, if reachable

**5. Cross-validate, and report the fold spread.** Any model difference
smaller than that spread is not a result — the movie-review experiment shows
six models separated by less than the noise.

**6. Read the coefficients.** A linear model hands them over free. If the top
features are sentiment words the model learned the task; if they are a brand
name it learned an artefact.

**7. Error analysis, which carries the marks.** Bucket every error:
code-mixing, sarcasm, negation, aspect-mixing ("delivery fast, product bad"),
emoji. **The breakdown is worth more than the accuracy.**

**8. Ethics.** State who wrote the reviews and who the labels came from, and
whether the classifier scores one dialect systematically lower.
</details>

### L2. "Large pre-trained models have made classical NLP obsolete." Discuss. *(15 marks)*

<details><summary>Solution outline</summary>

**The claim is true for accuracy on benchmark tasks and false as a general
statement about practice.**

**Where pre-training genuinely won:** contextual disambiguation (the two
"bank" sentences), transfer to small labelled datasets, and any task needing
world knowledge. The local model in `12_transformer_local.py` — the same
architecture on 200 K words instead of 3.3 billion — **learned the shape of
English and none of the facts.** That gap is real and large.

**Where classical methods still hold:**

| Situation | Why |
|---|---|
| **Small, distinct FAQ** | the lab's character n-grams scored **6/6**; there was nothing to improve |
| **Interpretability required** | a linear model's coefficients are readable; a transformer's are not |
| **Compute or latency constrained** | TF-IDF + logistic regression trains in 1.5 seconds |
| **Domain far from the training data** | spaCy's failure on Indian state names, fixed by **nine lines of gazetteer** |
| **Regulated domains** | extractive summarization is auditable; abstractive hallucinates |

**The reframing that earns the marks:** pre-training relocates the work rather
than removing it. You now spend your effort on **data**, on **evaluation**,
and on **knowing when the model is outside its distribution** — and the
classical methods remain the **baselines** that tell you whether the large
model earned its cost.

**And the measurement that makes this concrete:** six sentiment models on
movie reviews differed by **less than the spread between cross-validation
folds**. A transformer that beats TF-IDF by half a point on that data has not
beaten anything at all.
</details>

---

## Quick self-test

| # | Question | Unit |
|---|---|---|
| 1 | Name the three kinds of ambiguity | 1 |
| 2 | Why does `\w+@\w+` truncate an email? | 1 |
| 3 | Greedy vs lazy — give the `<.*>` example | 1 |
| 4 | Why can't you split sentences on "."? | 2 |
| 5 | Which sentence does stopword removal destroy, and how? | 2 |
| 6 | Why does `lemmatize("was")` give "wa"? | 2 |
| 7 | What kills a top-down parser? | 2 |
| 8 | Derive CYK's O(n³) | 2 |
| 9 | Why did spaCy call Tamil Nadu a PERSON? | 3 |
| 10 | Why did bag-of-words rank the unrelated document higher? | 3 |
| 11 | CBOW vs skip-gram — which for rare words? | 3 |
| 12 | Why does Word2Vec need negative sampling? | 3 |
| 13 | When is a model gap "noise"? | 3 |
| 14 | What perplexity means "no better than guessing"? | 4 |
| 15 | What can BERT not do, and what can GPT not do? | 4 |
| 16 | Why divide attention scores by √d_k? | 5 |
| 17 | Why does BERT leave 10% of masked tokens unchanged? | 5 |
| 18 | Why do regulated domains use extractive summarization? | 5 |
| 19 | What baseline must a summarization report include? | 5 |
| 20 | Why does a retrieval bot need a threshold? | 5 |
