# Unit 1 — Introduction to NLP and Language Fundamentals

**Syllabus topics:** Definition, goals and scope of NLP. Real-world
applications (assistants, chatbots, translation, summarization, QA, spam
detection). Fundamentals of language processing. Ambiguities in NLP (lexical,
structural, contextual). Installations: Python setup, NLTK, spaCy basics.
Regular expressions (essential patterns, `findall`, `split`, `sub`, matching
tokens).

---

## 1.1 What NLP is, and what makes it hard

### 🎯 The definition, the goals and the scope

**Definition.** NLP is the branch of computing concerned with **language
processing** — getting a machine to read, analyse and produce language that
was written for a human.

**Its goals** are two, and they pull in different directions:

| Goal | Means |
|---|---|
| **Natural Language Understanding (NLU)** | text → structured meaning |
| **Natural Language Generation (NLG)** | structured meaning → text |

**The scope of NLP** runs from character-level operations (tokenization,
spelling) through sentence-level analysis (parsing, NER) to document- and
discourse-level tasks (summarization, dialogue).

**And it is hard because language is ambiguous, infinite and
context-dependent — three properties no other data type in this programme
has.**

| Property | Consequence |
|---|---|
| **Ambiguous** | the same string has several readings, and nothing in the string chooses |
| **Infinite** | you can always write a sentence nobody has written before |
| **Context-dependent** | "it" means whatever the last paragraph made it mean |
| **Not i.i.d.** | words are heavily dependent on neighbours — the same problem Course 14 B has with time |

### 📖 The levels of analysis

Worth memorising as a list, because exam questions ask you to place a
technique at a level.

| Level | Concerns | Example task |
|---|---|---|
| **Phonology** | sounds | speech recognition |
| **Morphology** | word structure | stemming, lemmatization |
| **Lexical** | words and their senses | tokenization, POS tagging |
| **Syntax** | sentence structure | parsing |
| **Semantics** | meaning | NER, word sense disambiguation |
| **Pragmatics** | meaning in context | coreference, sarcasm, implicature |
| **Discourse** | across sentences | summarization, dialogue |

**The techniques in this course sit at the lexical, syntactic and semantic
levels.** Pragmatics is where current systems are weakest, and it is why
sarcasm detection is still unsolved.

---

## 1.2 Applications, and what each one actually requires

| Application | The hard part |
|---|---|
| **Virtual assistants** | intent classification plus slot filling, under speech-recognition errors |
| **Chatbots** | retrieval (find an existing answer) or generation (write one) — very different systems |
| **Machine translation** | word order differs between languages; the encoder-decoder was invented for this |
| **Summarization** | extractive is safe, abstractive can hallucinate ([Unit 5](unit-5.md)) |
| **Question answering** | extractive QA finds a span; generative QA can invent one |
| **Spam detection** | an **adversarial** problem — the spammer adapts to your classifier |

### 💡 Why spam detection is the odd one out

Every other task has a fixed target. **Spam is adversarial: the moment your
classifier works, spammers change their text to defeat it.** That is why spam
filters are retrained continuously and why "my classifier got 98%" means much
less here than elsewhere. Course 15 B's drift-detection material is the
industrial answer to it.

---

## 1.3 Ambiguity — the core of the unit

### 📖 The three kinds

| Kind | What varies | Example |
|---|---|---|
| **Lexical** | one **word** has several senses | "The **bank** was closed." |
| **Structural** | one word sequence has several **parse trees** | "I saw the man with the telescope." |
| **Contextual (pragmatic)** | the words and structure are fixed; the **reference** or **intent** is not | "Can you pass the salt?" — a question or a request? |

> **The distinction is examined.** Lexical ambiguity: one structure, several
> meanings. Structural ambiguity: the words are unambiguous, the *grouping* is
> not. Contextual: both are fixed and the meaning still is not.

### 🔢 Lexical ambiguity is countable

WordNet puts a number on it, and
`03_ambiguity_tokenize.py`
prints it:

| Word | WordNet senses |
|---|---|
| **bank** | **18** |
| duck | 8 |
| run | 57 |
| **set** | **the most of any English word** |

**That number is what word sense disambiguation has to choose between**, and
it explains why WSD is hard: the classes are many, fine-grained and
unbalanced.

### 🔢 Structural ambiguity produces actual trees

The same script parses *"I saw the man with the telescope"* with a
hand-written CFG and gets **exactly 2 parses**:

- the PP attaches to the **VP** — I used the telescope
- the PP attaches to the **NP** — the man had it

**Nothing in the grammar prefers either, and nothing in the sentence resolves
it.**

> ### 🎯 This is why parsing is not enough
>
> A parser gives you the *possible* structures. Choosing between them needs
> **world knowledge** — telescopes are instruments of seeing — which a
> hand-written CFG cannot have and a statistical parser approximates from a
> treebank.

### The garden-path sentences worth knowing

| Sentence | Why it breaks you |
|---|---|
| "The old man the boats." | **"man" is the verb**; "the old" is the subject |
| "Time flies like an arrow." | "time" noun or imperative verb; "flies" verb or noun; "like" preposition or verb |
| "The horse raced past the barn fell." | "raced" is a reduced relative — "that was raced" |

**These are grammatical.** Your parser fails on them for the same reason you
do: it commits to the likely reading early and cannot cheaply revise.

---

## 1.4 The toolchain

### 📖 NLTK against spaCy

| | **NLTK** | **spaCy** |
|---|---|---|
| Designed for | **teaching and research** | **production** |
| Style | many small independent functions | one pipeline over a `Doc` object |
| Corpora | **extensive** — this course uses six | none bundled |
| Speed | slow | **fast**, Cython |
| Models | classic algorithms, older models | modern neural models |
| Use it for | corpora, WordNet, classic algorithms, comparison | tokenization, POS, parsing, NER |

> **Use both, and say which.** This course does: NLTK for corpora and the
> classic algorithms, spaCy for anything you would put in a system.

### The pipeline, which is the thing to understand about spaCy

```python
nlp = spacy.load("en_core_web_sm")
print(nlp.pipe_names)
# ['tok2vec', 'tagger', 'parser', 'attribute_ruler', 'lemmatizer', 'ner']
```

Each name is a component that runs **in order** on every document: the tagger
before the parser, the parser before the entity recogniser.

**When spaCy is slow, the fix is `nlp.pipe(texts, disable=[...])`** — turn off
the components you are not using. Doing NER only? Disable the parser.

---

## 1.5 Regular expressions

### 📖 The four functions the syllabus names

| Function | Returns |
|---|---|
| `re.findall(pat, s)` | **every** non-overlapping match, as a list |
| `re.split(pat, s)` | the string split **on** the pattern |
| `re.sub(pat, repl, s)` | the string with matches replaced |
| `re.match` / `re.search` | `match` anchors at the **start**; `search` scans |

**`match` vs `search` is a standard exam question**, and the standard bug:
`re.match("world", "hello world")` returns `None`.

### 🔢 The patterns to know cold

| Pattern | Matches |
|---|---|
| `\d` `\w` `\s` | digit, word character (`[A-Za-z0-9_]`), whitespace |
| `\b` | word **boundary** — zero width |
| `+` `*` `?` | one-or-more, zero-or-more, zero-or-one |
| `{m,n}` | between m and n |
| `[^abc]` | anything **but** a, b or c |
| `(...)` vs `(?:...)` | capturing vs **non-capturing** group |
| `(?=...)` `(?!...)` | lookahead, negative lookahead |

### ⚠️ Greedy against lazy — the single most common regex bug

`01_setup_regex.py` measures
it on `<b>bold</b> and <i>italic</i>`:

| Pattern | Result |
|---|---|
| `<.*>` | `['<b>bold</b> and <i>italic</i>']` — **one match, the whole line** |
| `<.*?>` | `['<b>', '</b>', '<i>', '</i>']` |

**`*` is greedy**: it takes as much as it can and gives back only what it
must. **`*?` is lazy** and stops at the first `>`. One character, entirely
different behaviour.

### ⚠️ And the email pattern everyone writes first

| Pattern | On `asha.reddy@nrigroup.ac.in` |
|---|---|
| `\w+@\w+` | **`reddy@nrigroup`** |
| `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` | the whole address |

**`\w` does not match `.` or `-`, so the naive pattern truncates silently.**
The output still *looks* like a list of emails, which is exactly why this bug
survives into production.

### 🎯 Score your regex, do not eyeball it

The lab grades four patterns against a hand-labelled text that contains
deliberate near-misses — `asha at nrigroup dot ac dot in`, the handle
`@nri_official`, `C#`, and a phone number too short to be one.

**"It found some emails" is not a result.** Precision, recall and F1 against
labelled truth is, and building the truth takes five minutes.

### ⚠️ Where regex stops being the right tool

The lab splits two sentences on `"."`:

| True sentences | Naive split gives |
|---|---|
| 2 | **5** |
| 1 | **4** |

"Dr.", "p.m.", "B.Sc." and "Rs." all contain a full stop that does not end a
sentence.

> **A regex is right for a pattern you can write down. Sentence boundaries are
> not one** — they need a trained tokeniser, which is [Unit 2](unit-2.md).

---

## What to be able to do after this unit

- [ ] Define NLP and give the three properties that make language hard
- [ ] List the levels of analysis and place a technique at the right one
- [ ] **Distinguish lexical, structural and contextual ambiguity**, with an example of each
- [ ] Explain why "The old man the boats" is grammatical
- [ ] Say when to use NLTK and when to use spaCy
- [ ] Explain what spaCy's pipeline is and how to speed it up
- [ ] Write patterns for emails, dates, hashtags and phone numbers
- [ ] **Explain greedy vs lazy quantifiers** and give the `<.*>` example
- [ ] Say why splitting on `"."` is wrong, and what to use instead

**Cross-check yourself:** run
`01_setup_regex.py` and
`03_ambiguity_tokenize.py`.
Every figure in this unit is printed by one of them.
