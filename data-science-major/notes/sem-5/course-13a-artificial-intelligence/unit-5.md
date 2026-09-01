# Unit 5 — Expert Systems, Probabilistic and Emerging AI

**Syllabus topics:** Expert Systems — architecture, knowledge base,
inference engine, explanation facility. Probabilistic Reasoning — Bayes'
theorem, Bayesian Belief Networks (concepts and examples). Fuzzy Logic and
uncertainty handling. Emerging topics — NLP basics, Robotics, AI Ethics and
societal impact.

---

## 5.1 Expert systems

### 🎯 The big idea

**An expert system captures a human expert's knowledge as explicit rules, and
applies them to new cases — showing its reasoning.**

It was AI's first commercial success, and it remains the right architecture
whenever **the rules are known and the decision must be justified**.

### 🔢 The architecture — a standard diagram question

```
   ┌──────────────┐        ┌─────────────────────────────────┐
   │ Domain       │        │        EXPERT SYSTEM            │
   │ expert       │───────►│  ┌──────────────────────────┐   │
   └──────────────┘        │  │    KNOWLEDGE BASE        │   │
          via              │  │  facts + IF-THEN rules   │   │
   ┌──────────────┐        │  └────────────┬─────────────┘   │
   │ Knowledge    │───────►│               │                 │
   │ engineer     │        │  ┌────────────▼─────────────┐   │
   └──────────────┘        │  │    INFERENCE ENGINE      │   │
                           │  │  forward / backward      │   │
                           │  └────────────┬─────────────┘   │
                           │               │                 │
   ┌──────────────┐        │  ┌────────────▼─────────────┐   │
   │    USER      │◄──────►│  │  EXPLANATION FACILITY    │   │
   └──────────────┘   UI   │  │  WORKING MEMORY          │   │
                           │  └──────────────────────────┘   │
                           └─────────────────────────────────┘
```

| Component | Holds / does |
|---|---|
| **Knowledge base** | Domain facts and **IF–THEN production rules**. The expertise |
| **Inference engine** | Applies the rules — **forward or backward chaining** (Unit 4 §4.5) |
| **Working memory** | Facts about **the current case** |
| **Explanation facility** | Answers **"why are you asking?"** and **"how did you conclude that?"** |
| **User interface** | Asks questions, reports conclusions |
| **Knowledge acquisition** | How new rules get in |

### ⚠️ Two distinctions the exam asks for

**Knowledge base vs working memory.** The knowledge base holds *general*
knowledge and persists across cases; working memory holds facts about *this*
patient and is cleared for the next one.

**Domain expert vs knowledge engineer.** The expert has the knowledge; the
**knowledge engineer elicits it and encodes it as rules**. That elicitation is
the hard part, and it is called the **knowledge acquisition bottleneck** — the
reason expert systems proved expensive to build and maintain.

### 💡 The explanation facility is why they persist

**Ask a neural network why it refused the loan and you get nothing. Ask an
expert system and you get the rule chain.** In medicine, credit and law that is
often a requirement rather than a preference.

- **"Why?"** — asked when the system requests information: *because I am trying
  to establish rule R, and I need its second premise.*
- **"How?"** — asked about a conclusion: *by rule R, from facts A and B, which
  came from rules S and T.*

### 🔢 The famous systems

| System | Year | Domain | Note |
|---|---|---|---|
| **DENDRAL** | 1965 | Molecular structure | **The first** |
| **MYCIN** | 1972 | Bacterial infections | ~450 rules; used **certainty factors**; matched specialists |
| **PROSPECTOR** | 1978 | Mineral exploration | Found a molybdenum deposit |
| **XCON / R1** | 1980 | Configuring VAX orders | **Saved DEC ~$40M a year** — the commercial proof |

**MYCIN is the one to know in detail** for its certainty factors, and because
it was never deployed clinically — for reasons of liability and workflow, not
accuracy, which is itself a lesson about deploying AI.

### 🔢 Advantages and limitations

| Advantages | Limitations |
|---|---|
| **Explains its reasoning** | **Knowledge acquisition bottleneck** — experts find their knowledge hard to state |
| Consistent, never tired | **Brittle** — fails badly just outside its domain, with no sense that it is out of its depth |
| Preserves expertise when experts leave | **No common sense** and no learning |
| Cheap to replicate | Maintenance grows hard as rules interact |
| Rules can be added without changing the engine | Poor with **uncertainty**, unless bolted on — hence §5.2 |

**"Brittle" is the word to use.** A human expert who meets an unfamiliar case
says so; an expert system produces a confident wrong answer.

---

## 5.2 Probabilistic reasoning

### 🎯 Why logic is not enough

**Logic is true or false; the world is uncertain.** A rule like
`Toothache ⇒ Cavity` is simply false — toothaches have other causes. Patching
it with every exception hits the **qualification problem** of Unit 4 §4.2.

**Probability is the principled alternative:** instead of asserting the rule,
give **P(Cavity | Toothache) = 0.8**.

### 🔢 Bayes' theorem — Course 4 again

> **P(H | E) = P(E | H) × P(H) / P(E)**

| Term | Name |
|---|---|
| P(H \| E) | **Posterior** — belief in the hypothesis after seeing the evidence |
| P(E \| H) | **Likelihood** |
| P(H) | **Prior** |
| P(E) | Evidence / normalising constant |

### 🔢 The worked example that everyone should know

A disease affects **1 in 1,000**. A test is **99% accurate** both ways. You
test positive. What is P(disease)?

- P(D) = 0.001, P(¬D) = 0.999
- P(+ | D) = 0.99, P(+ | ¬D) = 0.01
- P(+) = 0.99(0.001) + 0.01(0.999) = 0.00099 + 0.00999 = **0.01098**
- **P(D | +) = 0.00099 / 0.01098 = 0.0902 ≈ 9%**

**A 99%-accurate positive test means a 9% chance of having the disease.**

**Why:** the disease is rare, so the 1% false-positive rate applied to the
999 healthy people produces **about ten times more false positives than true
positives**. The prior dominates.

**This is base-rate neglect**, and it is the same argument as Course 12 A §2.5:
on rare events, an impressive-sounding accuracy is not what it appears.

### 🔢 Bayesian Belief Networks

> **A directed acyclic graph where nodes are random variables and edges are
> direct probabilistic influences. Each node carries P(node | its parents).**

**The point is compactness.** A joint distribution over n boolean variables
needs **2ⁿ − 1** numbers. A Bayes net needs only the conditional probability
table of each node given its parents:

> **P(X₁…Xₙ) = ∏ᵢ P(Xᵢ | Parents(Xᵢ))**

### 🔢 The standard example — burglary and earthquake

```
      Burglary          Earthquake
          \                /
           \              /
            ▼            ▼
              [ Alarm ]
              /        \
             ▼          ▼
       JohnCalls    MaryCalls
```

| Node | Table size |
|---|---:|
| Burglary | 1 |
| Earthquake | 1 |
| Alarm (2 parents) | 4 |
| JohnCalls (1 parent) | 2 |
| MaryCalls (1 parent) | 2 |
| **Total** | **10** |

**The full joint over 5 boolean variables would need 2⁵ − 1 = 31 numbers. The
network needs 10.** With 30 variables each having at most 5 parents, the saving
is from about **10⁹** to **960**.

**That compression is the whole reason Bayes nets exist**, and it is the number
to quote.

### 💡 What the missing edges say

**A Bayes net encodes conditional independence.** There is no edge from
Burglary to JohnCalls because **John calls because of the alarm, not because of
the burglary** — given the alarm, his call is independent of the burglary.

**The absent edges carry as much information as the present ones.** Saying that
distinguishes a real answer from a redrawn diagram.

### ⚠️ Explaining away — the effect worth knowing

Learning that there was an **earthquake** *reduces* your belief in a
**burglary**, even though the two are independent a priori.

**Both are causes of the alarm.** Once the alarm is observed, confirming one
cause explains the evidence and lowers the need for the other. This is
**explaining away**, and it is a pattern of reasoning that no purely logical
system produces naturally.

---

## 5.3 Fuzzy logic

### 🎯 Fuzzy is not probability, and this is the examinable point

| | **Probability** | **Fuzzy logic** |
|---|---|---|
| Handles | **Uncertainty** — you do not know which case holds | **Vagueness** — the category itself has no sharp edge |
| "0.8" means | 80% chance it **is** true | It is true **to degree 0.8** |
| Resolves when | You **observe** the outcome | **Never** — it was never a yes/no question |
| Example | "There is a 0.8 chance of rain" | "The water is warm" |

**"Is 30 °C hot?" is not a question about uncertainty.** You know the
temperature exactly. The vagueness is in the word *hot*, and that is what fuzzy
logic represents.

### 🔢 Fuzzy sets and membership

A **membership function** μ_A(x) ∈ [0, 1] gives the degree to which x belongs
to set A.

```
 μ    Cold        Warm         Hot
1.0 ──────╲      ╱────╲       ╱──────
          ╲    ╱      ╲     ╱
0.5        ╲  ╱        ╲   ╱
            ╲╱          ╲ ╱
0.0 ─────────╳───────────╳──────────► °C
        10   20    30    40
```

At 25 °C: μ_Cold = 0, μ_Warm = **0.7**, μ_Hot = **0.3**. **Memberships need not
sum to 1** — that is a probability constraint, not a fuzzy one.

### 🔢 Fuzzy operations

| Operation | Definition |
|---|---|
| **AND** (intersection) | **min**(μ_A, μ_B) |
| **OR** (union) | **max**(μ_A, μ_B) |
| **NOT** (complement) | **1 − μ_A** |

### 🔢 The three stages of a fuzzy system

1. **Fuzzification** — crisp input → membership degrees ("25 °C" → warm 0.7,
   hot 0.3)
2. **Inference** — apply fuzzy rules: `IF temperature IS hot THEN fan IS fast`
3. **Defuzzification** — fuzzy output → a crisp action, usually by the
   **centroid** (centre of gravity) method

**Where it is used:** washing machines, air conditioners, camera autofocus,
anti-lock brakes, train braking. **Control systems**, where a smooth response
matters more than a provably correct one.

---

## 5.4 NLP basics

**Natural language processing is hard because language is ambiguous at every
level**, and naming the levels is the exam answer.

| Level | Deals with | An ambiguity |
|---|---|---|
| **Phonology** | Sounds | "ice cream" / "I scream" |
| **Morphology** | Word structure | un-happi-ness |
| **Lexical** | Word meaning | *bank* — river or financial |
| **Syntactic** | Grammar | "I saw the man with the telescope" — who has it? |
| **Semantic** | Meaning | "Every student read a book" — the same book, or one each? |
| **Pragmatic** | Context and intent | "Can you pass the salt?" is a request, not a question |
| **Discourse** | Across sentences | What does *it* refer to? |

### 🔢 The classical pipeline

```
text → tokenise → stop-word removal → stemming / lemmatisation
     → POS tagging → parsing → named entity recognition
     → semantic analysis
```

| Step | Note |
|---|---|
| **Tokenisation** | Splitting into words. Harder than it looks — "don't", "New York" |
| **Stemming** | Chops affixes — fast, crude: *studies* → *studi* |
| **Lemmatisation** | Dictionary form — slower, correct: *studies* → *study* |
| **POS tagging** | Assigns noun, verb, adjective |
| **Parsing** | Builds a syntax tree — **experiment 18's DCG** |
| **NER** | Finds people, places, organisations |

### 💡 The connection to this course

**A DCG (definite clause grammar) in Prolog is a parser written as logic
rules** — grammar as inference, which is exactly Unit 4's machinery applied to
language. That is lab experiment 18, and it is the point where the two halves
of this course meet.

**Modern NLP is statistical and neural**, and the classical pipeline is largely
replaced by learned representations — but the *ambiguity levels* remain the
right way to describe why the problem is hard.

---

## 5.5 Robotics

| Concept | Means |
|---|---|
| **Perception** | Sensors → a model of the world. Noisy and partial |
| **Localisation** | Where am I? |
| **Mapping / SLAM** | Building a map **while** localising in it |
| **Path planning** | **This course's search**, in continuous space |
| **Motion control** | Actuators, feedback, kinematics |
| **Effectors and actuators** | What moves, and what drives it |

### 💡 Moravec's paradox — the observation worth quoting

**What humans find hard, computers find easy; what humans find effortless,
computers find nearly impossible.**

Chess fell in 1997. **Reliably picking up an unfamiliar object still has not
been solved.** Perception and motor control took evolution hundreds of millions
of years and run below conscious awareness; chess is a few thousand years old
and is done deliberately.

This is also a **PEAS and environment** point from Unit 1: a robot's world is
**partially observable, stochastic, dynamic, continuous and multi-agent** —
the hardest cell of every dimension.

---

## 5.6 AI ethics and societal impact

### 🔢 The issues, each with a concrete case

| Issue | Concretely |
|---|---|
| **Bias and fairness** | Training data reflects historical discrimination, so the model reproduces it. A hiring model trained on past hires learns past prejudice |
| **Transparency** | A model that cannot explain a refusal may be legally unusable — the argument for §5.1's expert systems |
| **Accountability** | A self-driving car crashes. Who is responsible — owner, manufacturer, programmer? |
| **Privacy** | Face recognition and inference from data people did not knowingly provide |
| **Employment** | Automation displaces work; the benefit and the cost fall on different people |
| **Autonomous weapons** | Delegating a lethal decision to a machine |
| **Concentration of power** | Frontier systems need capital few possess |
| **Environmental cost** | Training large models consumes substantial energy |
| **Misinformation** | Generated text, images and audio at scale |

### ⚠️ Bias is a data problem before it is an algorithm problem

**A model trained on biased data will be biased, however fair the algorithm
is.** Three distinct sources, and naming them is the mark:

1. **Historical bias** — the world the data came from was unfair
2. **Representation bias** — some groups are under-sampled
3. **Measurement bias** — the recorded label is a poor proxy for what you
   actually care about (arrests are not crimes)

**And "fairness" is not one thing.** Equal accuracy across groups, equal
false-positive rates, and equal positive-prediction rates are **mathematically
incompatible** except in degenerate cases. **You must choose which fairness you
mean**, and that choice is a value judgement, not a technical one.

Saying that last sentence is what separates a thoughtful answer from a list.

### 💡 The principles most frameworks agree on

**Fairness · Accountability · Transparency · Privacy · Safety · Human
oversight · Beneficence.**

Note the practical point: **the EU AI Act and similar rules are
risk-tiered** — the obligations depend on the application, not the algorithm.
A recommender and a diagnostic system may use the same model and face very
different requirements.

---

## Practice problems

### Problem 1

Explain the architecture of an expert system, and its advantages and
limitations. *(10 marks)*

**Solution.**

Draw the architecture and name every component: **knowledge base** (facts and
IF–THEN rules — the expertise), **inference engine** (forward or backward
chaining), **working memory** (facts about the current case), **explanation
facility**, **user interface**, and **knowledge acquisition**.

**Make the two distinctions the examiner is looking for:**

- **Knowledge base vs working memory** — general knowledge that persists,
  against facts about *this* case that are cleared for the next.
- **Domain expert vs knowledge engineer** — the expert has the knowledge; the
  engineer elicits and encodes it, which is the **knowledge acquisition
  bottleneck**.

**Explain the explanation facility properly**, since it is named in the
syllabus: **"Why?"** answers why a question is being asked (I am trying to
establish rule R and need its second premise); **"How?"** answers how a
conclusion was reached (by rule R from facts A and B). **This is why expert
systems persist in medicine, credit and law** — a neural network cannot do it.

**Advantages:** explains itself; consistent and never tired; preserves
expertise; cheap to replicate; rules can be added without changing the engine.

**Limitations:** the acquisition bottleneck; **brittleness** — it fails badly
just outside its domain with no sense of being out of its depth; no common
sense; no learning; maintenance grows hard as rules interact; poor with
uncertainty.

Name **MYCIN** (450 rules, certainty factors, matched specialists, never
deployed clinically) and **XCON** (saved DEC about $40M a year).

### Problem 2

Explain Bayesian belief networks. Why are they more compact than a full joint
distribution? *(10 marks)*

**Solution.**

**Definition:** a **directed acyclic graph** whose nodes are random variables
and whose edges are direct probabilistic influences; each node carries a
conditional probability table **P(node | its parents)**.

**The chain rule for a Bayes net:**

> P(X₁ … Xₙ) = ∏ᵢ P(Xᵢ | Parents(Xᵢ))

**The compactness argument, with numbers.** Draw the burglary–earthquake
network and count:

| Node | Parents | Table entries |
|---|---|---:|
| Burglary | — | 1 |
| Earthquake | — | 1 |
| Alarm | B, E | 4 |
| JohnCalls | A | 2 |
| MaryCalls | A | 2 |
| | | **10** |

**A full joint over 5 boolean variables needs 2⁵ − 1 = 31 numbers; the network
needs 10.** With 30 variables each having at most 5 parents, it is about
**10⁹ against 960**.

**Then the conceptual half, which most answers omit: the missing edges are the
content.** There is no edge from Burglary to JohnCalls because John calls
because of the **alarm** — given the alarm, his call is independent of the
burglary. **A Bayes net encodes conditional independence, and the absent edges
carry as much information as the present ones.**

Finish with **explaining away**: learning there was an earthquake *reduces*
belief in a burglary, though the two are independent a priori — because once
the alarm is observed, one confirmed cause reduces the need for the other. No
purely logical system produces that pattern naturally.

### Problem 3

Distinguish fuzzy logic from probability. Explain the stages of a fuzzy system.
*(10 marks)*

**Solution.**

**The distinction, first and clearly:**

| | **Probability** | **Fuzzy logic** |
|---|---|---|
| Handles | **Uncertainty** — which case holds is unknown | **Vagueness** — the category has no sharp edge |
| 0.8 means | 80% chance it **is** true | True **to degree** 0.8 |
| Resolves when | You observe the outcome | **Never** — it was never yes/no |
| Example | "0.8 chance of rain" | "The water is warm" |

**Make the point with the example:** *"Is 30 °C hot?"* involves no uncertainty
at all — you know the temperature exactly. The vagueness is in the **word**.

**Membership functions:** μ_A(x) ∈ [0, 1]. At 25 °C, μ_Warm = 0.7 and
μ_Hot = 0.3 — and note that **memberships need not sum to 1**, which is a
probability constraint and not a fuzzy one.

**Operations:** AND = **min**, OR = **max**, NOT = **1 − μ**.

**The three stages:**

1. **Fuzzification** — crisp input to membership degrees
2. **Inference** — apply fuzzy rules (`IF temperature IS hot THEN fan IS fast`)
3. **Defuzzification** — fuzzy output back to a crisp action, usually by the
   **centroid** method

**Applications:** washing machines, air conditioners, camera autofocus,
anti-lock brakes, train braking — **control systems**, where a smooth response
matters more than a provably correct one.

---

## Exam questions from this unit

**Two marks**

1. Name the components of an expert system.
2. What does the explanation facility do?
3. What is the knowledge acquisition bottleneck?
4. State Bayes' theorem.
5. How many numbers does a full joint over n boolean variables need?
6. Give the fuzzy definitions of AND, OR and NOT.
7. What is defuzzification?

**Five marks**

1. Explain the architecture of an expert system.
2. Explain MYCIN and its significance.
3. Explain Bayes' theorem with the medical test example.
4. Explain the levels of ambiguity in natural language.
5. Explain Moravec's paradox.
6. Explain three sources of bias in AI systems.

**Ten marks**

1. Explain expert systems — architecture, advantages, limitations.
2. Explain Bayesian belief networks and why they are compact.
3. Distinguish fuzzy logic from probability, and explain a fuzzy system.
4. Discuss AI ethics — the issues, with concrete cases.

---

## Mistakes that cost marks

- **Saying fuzzy logic handles uncertainty.** It handles **vagueness**;
  probability handles uncertainty.
- **Claiming fuzzy memberships must sum to 1.** That is a probability
  constraint.
- **Drawing a Bayes net without saying what the missing edges mean.** They
  encode conditional independence, which is the point.
- **Giving the joint-distribution saving without numbers.** 31 against 10 on
  five variables; ~10⁹ against 960 on thirty.
- **Confusing the knowledge base with working memory.** General and persistent
  against case-specific and cleared.
- **Saying expert systems failed because they were inaccurate.** They were
  **brittle** and expensive to maintain; MYCIN matched specialists and was
  still never deployed.
- **Listing ethics issues with no case.** "Bias" earns nothing; "a hiring model
  trained on past hires learns past prejudice" earns the mark.
- **Treating fairness as one thing.** The main definitions are mathematically
  incompatible, and choosing between them is a value judgement.
