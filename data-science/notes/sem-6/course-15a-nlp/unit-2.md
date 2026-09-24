# Unit 2 — Text Preprocessing and Linguistic Analysis

**Syllabus topics:** Key NLP terminologies: morphology, lexicon,
orthographic rules. Finite state transducers. Text preprocessing techniques:
tokenization, stopword removal, stemming, lemmatization. Grammar and
context-free grammar. Parsing techniques: top-down, bottom-up, CYK algorithm.
Semantic analysis: elements, meaning representation.

---

## 2.1 The terminology

| Term | Definition | Example |
|---|---|---|
| **Morphology** | how words are built from smaller meaningful units | *un-happi-ness* |
| **Morpheme** | the smallest unit carrying meaning | *un*, *happy*, *ness* |
| **Lexicon** | the inventory of words and their properties | a dictionary with POS and features |
| **Orthographic rules** | spelling rules applied when morphemes combine | *city + s → cities*, not *citys* |
| **Lemma** | the dictionary form | *run* for *ran*, *running*, *runs* |
| **Token / type** | one occurrence / one distinct word | "the cat sat on the mat" — 6 tokens, 5 types |

### 📖 The two kinds of morphology

| | **Inflectional** | **Derivational** |
|---|---|---|
| Changes | grammatical form | **the word itself** |
| Part of speech | unchanged | often changes |
| Example | *cat → cats*, *walk → walked* | *happy → happiness*, *teach → teacher* |
| Lemmatization | **undoes it** | **does not** |

**Lemmatization reverses inflection only.** *happiness* lemmatises to
*happiness*, not to *happy*, and that is correct — they are different words.

### 📖 Finite state transducers

An FST is a finite automaton whose transitions carry **input:output** pairs,
so it maps one string to another.

For morphology, the classic use is the **two-level** model:

```
    surface form:   c  a  t  s
    lexical form:   c  a  t  +N +PL
```

**Why an FST and not a lookup table:** it is **bidirectional** — the same
machine analyses *cats → cat+N+PL* and generates *cat+N+PL → cats*. It is also
compact and composable, so orthographic rules (`city + s → cities`) compose
with the morphology as another transducer.

> **The exam answer:** an FST is a finite-state machine over *pairs* of
> symbols, it is bidirectional, and it is how morphological analysers were
> built before statistical methods. NLTK does not ship one; a stemmer is the
> crude approximation you get instead.

---

## 2.2 Tokenization

### ⚠️ Sentence tokenization is not splitting on "."

`03_ambiguity_tokenize.py`
runs three methods on one hard sentence containing *Dr.*, *U.S.A.*, *Rs.* and
an email address:

| Method | Sentences found |
|---|---|
| split on `"."` | over-counts badly |
| **NLTK `sent_tokenize`** | correct-ish |
| **spaCy** | correct-ish, **and it disagrees with NLTK** |

> ### 🎯 Neither trained tokeniser is "correct" in the abstract
>
> They were trained on **different annotation guidelines**, and abbreviations
> are exactly where guidelines differ. **Report which tokeniser you used.**
> Two results produced with different tokenisers are not directly comparable,
> and this is why.

### Word tokenization, and the contraction problem

| Input | NLTK | spaCy |
|---|---|---|
| `didn't` | `did` + `n't` | `did` + `n't` |
| `"It's far!"` | quotes split one way | quotes split another |
| `Rs. 1,20,000` | handled differently again | — |

**These are choices, not errors.** A model trained on one tokenisation
degrades on the other, which is a real and commonly-missed source of
production bugs.

---

## 2.3 Stopword removal

### 🔢 What it costs and what it buys

On 100,000 words of the Brown corpus:

| | Before | After | Change |
|---|---|---|---|
| Tokens | 100,000-ish | roughly half | **~50% reduction** |
| Distinct types | many thousands | **almost unchanged** | negligible |

**Stopwords are few words repeated constantly**, so removal cuts the token
count hugely and the vocabulary barely at all. For a bag-of-words model that
is close to free.

### ⚠️ And the sentences it destroys

| Sentence | After removal |
|---|---|
| "to be or not to be" | **(empty)** |
| **"The film was not good"** | **"film good"** |
| "It is a war of all against all" | "war" |
| "Who is she?" | **(empty)** |

> **"The film was not good" becomes "film good".** That is the single most
> damaging thing stopword removal does, and it is why a sentiment classifier
> that strips stopwords can be worse than one that does not.

### 🎯 The rule

| Remove stopwords for | Keep them for |
|---|---|
| **topic** tasks — what a document is *about* | **sentiment** — "not" carries the label |
| document clustering, retrieval | question answering — "who", "when" are the question |
| keyword extraction | anything syntactic — parsing needs function words |

**And [experiment 10](lab.md#experiment-10) measures it rather than asserting
it**, which turns out to matter: the difference it makes on movie reviews is
smaller than the variation between cross-validation folds.

---

## 2.4 Stemming and lemmatization

### 🔢 The comparison table, measured

| Word | Porter | Snowball | Lemma (noun) | Lemma (verb) |
|---|---|---|---|---|
| running | run | run | running | **run** |
| **ran** | **ran** | **ran** | ran | **run** |
| **better** | better | better | better | *(as adjective: **good**)* |
| **university** | **univers** | **univers** | university | university |
| **universal** | **univers** | **univers** | universal | universal |
| geese | gees | gees | **goose** | geese |
| **was** | wa | was | **wa** | **be** |

### Read four rows closely

1. **"ran" → Porter leaves it alone.** A stemmer chops suffixes and *ran* has
   none. The lemmatiser **with the verb tag** gives *run*.
2. **"better" → "good"** needs WordNet, not string surgery.
3. **"university" and "universal" both → "univers".** Two unrelated words
   collapsed into one feature. **That is over-stemming**, and it is a real
   precision loss.
4. **"was" → "wa"** without a tag. The lemmatiser stripped what it took for a
   plural *s* and produced a string that is not an English word.

> ### ⚠️ So the usual claim needs qualifying
>
> "Lemmatization always returns a real word" is **only true when the tag is
> right**. Tagged as a verb, *was* gives *be*, which is correct.

### ⚠️ The most common silent mistake in NLP coursework

**`WordNetLemmatizer.lemmatize(w)` defaults to POS = noun.** Every tutorial
that calls it without a tag is asking "what is the singular of this noun",
which does nothing at all to a verb.

| Word | `lemmatize(w)` | `lemmatize(w, 'v')` |
|---|---|---|
| running | running | **run** |
| ran | ran | **run** |
| was | **wa** | **be** |

**Tag first, then lemmatise.**

### 🎯 The summary table

| | Stemming | Lemmatization |
|---|---|---|
| What it is | chop affixes by rule | map to a dictionary form |
| Needs | nothing | **WordNet, and ideally a POS tag** |
| Speed | very fast | slower |
| Output | may not be a word (*univers*) | a real word **if the tag is right** |
| Errors | over- and under-stemming | wrong sense without a tag |
| Use for | search, retrieval, recall | anything a human reads |

---

## 2.5 Grammar and context-free grammar

### 📖 A CFG is four things

**G = (N, Σ, R, S)** — non-terminals, terminals, rules, start symbol. Every
rule has the form **A → β**: *a single* non-terminal on the left. That
restriction is what "context-free" means — the rule applies regardless of
what surrounds A.

```
S   -> NP VP
NP  -> Det N | Det N PP | 'I'
VP  -> V NP | VP PP
PP  -> P NP
```

### 📖 Chomsky hierarchy, in one table

| Type | Grammar | Recognised by | Enough for English? |
|---|---|---|---|
| 3 | Regular | finite automaton | **no** — cannot do nesting |
| **2** | **Context-free** | pushdown automaton | **mostly** |
| 1 | Context-sensitive | linear bounded automaton | yes |
| 0 | Unrestricted | Turing machine | yes |

**Why regular is not enough:** matching nested clauses requires counting, and
a finite automaton has no memory to count with. That is the standard exam
justification for CFGs.

---

## 2.6 Parsing

### 📖 The three strategies

| Strategy | Direction | Behaviour |
|---|---|---|
| **Top-down** (recursive descent) | S → words | expands rules; **loops for ever on left recursion** |
| **Bottom-up** (shift-reduce) | words → S | fast, **greedy — one bad reduce and it never backtracks** |
| **Chart** (CYK, Earley) | dynamic programming | stores partial results; finds **all** parses efficiently |

### 🔢 The measurement

`07_parsing_ner_similarity.py`
runs all three on *"I saw the man with the telescope"*:

| Parser | Parses found |
|---|---|
| RecursiveDescent (top-down) | 2 |
| **ShiftReduce (bottom-up)** | **fewer — it is greedy** |
| **Chart (dynamic programming)** | **2** |

**Shift-reduce returns at most one parse and sometimes none**, because it
commits to a reduction and never revises. Chart parsing stores every partial
result, so it gets all of them without the exponential re-work — **the same
memoisation idea as Course 2**.

### ⚠️ The rule that kills a top-down parser

```
NP -> NP PP        <-- LEFT RECURSIVE
```

To parse an NP, recursive descent must first parse an NP, which requires
parsing an NP… **it recurses without consuming a single word and never
terminates.**

> **This is the standard exam question on parsing strategies, and the answer
> is "left recursion", not "ambiguity".** Bottom-up and chart parsers handle
> it without difficulty.

### 🔢 CYK, which the syllabus names explicitly

**Requires Chomsky Normal Form**: every rule is `A → B C` or `A → w`.

Fill an upper-triangular table where cell `(i, j)` holds every non-terminal
deriving the substring from `i` to `j`:

```
for length in 2..n:
    for i in 0..n-length:
        j = i + length
        for k in i+1..j-1:                     # every split point
            for each rule A -> B C:
                if B in table[i][k] and C in table[k][j]:
                    add A to table[i][j]
accept if S in table[0][n]
```

| Property | Value |
|---|---|
| Time | **O(n³ · \|G\|)** |
| Space | O(n²) |
| Finds | **all** parses |
| Requires | **CNF** |

**The three nested loops over `i`, `length` and `k` are where the n³ comes
from** — that is the answer to "derive CYK's complexity".

### ⚠️ And why nobody hand-writes a CFG for real text

A real Penn Treebank sentence has dozens of leaves and a height in double
figures, and there are 3,914 of them in NLTK's sample. **A hand-written CFG
does not scale**: real sentences need thousands of rules and still fail.

**Every production parser is statistical** — it learns rule probabilities from
a treebank and returns the most probable tree instead of all of them.

---

## 2.7 Semantic analysis

### 📖 The elements

| Element | Question it answers |
|---|---|
| **Word sense disambiguation** | which sense of *bank*? |
| **Semantic roles** | who did what to whom? |
| **Coreference** | what does *it* refer to? |
| **Entailment** | does sentence A imply sentence B? |

### 📖 Meaning representation

| Form | Example |
|---|---|
| **First-order logic** | `∀x (student(x) → ∃y (course(y) ∧ enrolled(x, y)))` |
| **Semantic network** | nodes for concepts, edges for relations — WordNet is one |
| **Frames / slots** | BUY: *buyer*, *seller*, *goods*, *price* |
| **AMR** | a rooted graph, one per sentence |

> **Course 13 A's first-order logic material is the same material.** The
> difference is only that there you wrote the logic and here you must derive
> it from text — which is the hard part, and still largely unsolved.

### 💡 Lesk, the algorithm to know for WSD

To disambiguate a word: for each of its WordNet senses, **count the overlap
between that sense's gloss and the words around the target**. Pick the sense
with the most overlap.

It is crude, it is unsupervised, it needs no training data, and it is the
baseline every WSD paper reports.

---

## What to be able to do after this unit

- [ ] Define morpheme, lexicon, lemma, and distinguish inflectional from derivational morphology
- [ ] **Explain what an FST is and why bidirectionality matters**
- [ ] Say why sentence tokenization cannot be done with `"."`
- [ ] Give the token/type effect of stopword removal, and the sentence it destroys
- [ ] **Compare stemming and lemmatization on `ran`, `better` and `university`**
- [ ] Explain why `lemmatize(w)` without a POS tag does almost nothing
- [ ] Define a CFG formally and say what "context-free" restricts
- [ ] Place CFGs in the Chomsky hierarchy and say why regular grammars fail
- [ ] **Explain why top-down parsing loops on left recursion**
- [ ] **Write CYK and derive its O(n³) complexity**
- [ ] Name the four elements of semantic analysis and one meaning representation

**Cross-check yourself:** run
`03_ambiguity_tokenize.py`
and
`07_parsing_ner_similarity.py`.
