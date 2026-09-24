# Unit 4 — Knowledge Representation and Reasoning

**Syllabus topics:** Knowledge representation — issues, approaches.
Propositional logic — syntax, semantics, truth tables, inference rules. First
Order Logic (FOL) — syntax, semantics, quantifiers, substitution, unification.
Inference in logic — forward chaining, backward chaining, resolution.
Knowledge-based agents.

> **This unit and Unit 3 carry the marks.** Resolution with unification is the
> hardest procedure in the course and the most reliably examined.

---

## 4.1 Knowledge-based agents

### 🎯 The shift from Units 2 and 3

**A search agent is told what the states are. A knowledge-based agent is told
what is *true*, and works out the rest.**

| | **Search agent** | **Knowledge-based agent** |
|---|---|---|
| Holds | A state, and a frontier | A **knowledge base** of sentences |
| Reasons by | Generating successors | **Inference** |
| Adding new information means | Rewriting the problem | **Adding a sentence** |
| Explains itself | By the path | **By the derivation** |

### 🔢 The architecture

```
   percept ──► TELL(KB, percept sentence)
                     │
                     ▼
                ┌────────┐
                │   KB   │ ◄── background knowledge
                └────┬───┘
                     │  ASK(KB, "what should I do?")
                     ▼
                  action ──► TELL(KB, action taken)
```

Two operations, and that is all:

| Operation | Does |
|---|---|
| **TELL** | Add a sentence to the knowledge base |
| **ASK** | Query what follows from it |

**The knowledge is declarative** — you state what is true, not how to compute
it. That is the defining property, and it is why adding a new rule requires no
change to the reasoning engine.

---

## 4.2 Knowledge representation — issues and approaches

### 🔢 The issues the syllabus asks for

| Issue | The question |
|---|---|
| **Expressiveness vs tractability** | The more you can say, the slower reasoning gets — the central trade-off |
| **The frame problem** | How to state what does **not** change when an action occurs, without listing everything |
| **The qualification problem** | No rule can list every precondition ("a car starts if it has fuel, and a battery, and no elephant on the bonnet…") |
| **The ramification problem** | Actions have implicit consequences nobody stated |
| Default reasoning | "Birds fly" — but not penguins. Requires **non-monotonic** logic |
| Uncertainty | Logic is true/false; the world is probabilistic — **Unit 5** |
| Granularity | How finely to carve the world into predicates |
| Inheritance | Sharing properties down a hierarchy |

**The frame and qualification problems are worth naming**, because they are why
pure logical agents were largely displaced by probabilistic ones.

### 🔢 The approaches

| Approach | Represents knowledge as | Note |
|---|---|---|
| **Logic** | Sentences in a formal language | Propositional and FOL — this unit |
| **Semantic networks** | A graph of concepts and relations | Inheritance is a path in the graph |
| **Frames** | Objects with slots and fillers | The ancestor of object-oriented modelling |
| **Production rules** | IF–THEN rules | **Expert systems** — Unit 5 |
| **Scripts** | Stereotyped event sequences | "Going to a restaurant" |
| **Ontologies** | Formal shared vocabularies | OWL, RDF, the semantic web |

**Semantic networks and frames are notational variants of logic** — anything
they express can be expressed in FOL. Saying that is worth a mark, and it
explains why the field converged on logic.

---

## 4.3 Propositional logic

### 🔢 Syntax

| Element | Symbols |
|---|---|
| **Atomic sentences** | Propositional symbols: P, Q, `Rains`, `W1,2` — each true or false |
| **Connectives** | ¬ (not), ∧ (and), ∨ (or), ⇒ (implies), ⇔ (iff) |
| **Precedence** | ¬ , ∧ , ∨ , ⇒ , ⇔ — highest to lowest |

### 🔢 Semantics — the truth tables

| P | Q | ¬P | P ∧ Q | P ∨ Q | **P ⇒ Q** | P ⇔ Q |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| F | F | T | F | F | **T** | T |
| F | T | T | F | T | **T** | F |
| T | F | F | F | T | **F** | F |
| T | T | F | T | T | **T** | T |

### ⚠️ Implication is the row that confuses everyone

**P ⇒ Q is TRUE whenever P is false**, regardless of Q. "If the moon is made of
cheese then 2 + 2 = 5" is **true**.

**Why:** ⇒ is not causation, and it makes no claim about the case where P is
false. It says only *there is no case where P holds and Q fails* — which is
exactly **¬P ∨ Q**, and that equivalence is the one to memorise, because every
conversion to CNF starts with it.

### 🔢 The vocabulary of entailment

| Term | Means |
|---|---|
| **Model** | An assignment of true/false to every symbol |
| **Satisfiable** | True in **at least one** model |
| **Valid** (tautology) | True in **every** model |
| **Unsatisfiable** | True in **no** model |
| **Entailment α ⊨ β** | β is true in **every model where α is true** |

**The deduction theorem:** α ⊨ β **if and only if** (α ⇒ β) is valid.
**And:** α ⊨ β if and only if (α ∧ ¬β) is **unsatisfiable**.

**That second form is the basis of resolution** (§4.6) — proof by
contradiction, mechanised.

### 🔢 The inference rules to know

| Rule | Form |
|---|---|
| **Modus Ponens** | From α ⇒ β and α, infer **β** |
| **Modus Tollens** | From α ⇒ β and ¬β, infer **¬α** |
| **And-Elimination** | From α ∧ β, infer α |
| **And-Introduction** | From α and β, infer α ∧ β |
| **Or-Introduction** | From α, infer α ∨ β |
| **Resolution** | From α ∨ β and ¬β ∨ γ, infer **α ∨ γ** |
| **Unit resolution** | From α ∨ β and ¬β, infer α |

### 💡 Two properties every inference procedure is judged on

| Property | Means | Read as |
|---|---|---|
| **Sound** | Everything derived is entailed | It never lies |
| **Complete** | Everything entailed can be derived | It never misses |

**Resolution is sound and complete for propositional logic** — refutation
complete, meaning it will derive the empty clause from any unsatisfiable set.
That is why it is the procedure worth learning.

---

## 4.4 First Order Logic

### 🎯 Why propositional logic is not enough

**Propositional logic has no way to say "all".** To express "every student who
studies passes" you would need one sentence per student, and a new one whenever
a student enrols.

**FOL adds objects, relations and quantifiers**, so one sentence covers them
all. That is the whole motivation, and it is the answer to "why FOL?".

| | **Propositional** | **First order** |
|---|---|---|
| The world is | Facts | **Objects** with **relations** and **functions** |
| Can say "all" | **No** | **Yes** — ∀ |
| Sentences needed for n students | n | **1** |
| Decidable | **Yes** | **No** — only semi-decidable |

### 🔢 Syntax

| Element | Examples |
|---|---|
| **Constants** | `Ram`, `India`, `2` |
| **Variables** | `x`, `y` |
| **Predicates** | `Student(x)`, `Parent(x, y)`, `Greater(x, y)` — return true/false |
| **Functions** | `FatherOf(x)`, `Plus(x, y)` — return an **object** |
| **Terms** | A constant, a variable, or a function applied to terms |
| **Atomic sentence** | A predicate applied to terms: `Parent(Ram, Asha)` |
| **Quantifiers** | **∀** (for all), **∃** (there exists) |

⚠️ **A function returns an object; a predicate returns a truth value.**
`FatherOf(Asha)` is a *person*; `Father(Ram, Asha)` is *true or false*. Mixing
them is a standard lost mark.

### 🔢 Quantifiers — the pairing rule

**∀ goes with ⇒. ∃ goes with ∧.** This is the most common FOL error and the
most reliably examined.

```
∀x Student(x) ⇒ Passes(x)          "all students pass"          ✓
∀x Student(x) ∧ Passes(x)          "EVERYTHING is a student
                                    and passes"                  ✗

∃x Student(x) ∧ Passes(x)          "some student passes"         ✓
∃x Student(x) ⇒ Passes(x)          TRUE if anything is not a
                                    student -- vacuously          ✗
```

**Why:** with ∀ you want to say nothing about non-students, and ⇒ is vacuously
true for them. With ∃ you want to assert both parts of one witness, so you need
∧.

### 🔢 Quantifier equivalences — De Morgan for quantifiers

| | |
|---|---|
| ¬∀x P(x) | ≡ **∃x ¬P(x)** |
| ¬∃x P(x) | ≡ **∀x ¬P(x)** |
| ∀x P(x) | ≡ ¬∃x ¬P(x) |
| ∃x P(x) | ≡ ¬∀x ¬P(x) |

⚠️ **Nested quantifier order matters.**

- `∀x ∃y Loves(x, y)` — everybody loves **someone** (possibly different people)
- `∃y ∀x Loves(x, y)` — there is **one person** everybody loves

**Not the same claim**, and swapping them is a favourite exam trap.

### 🔢 Substitution and unification

**A substitution θ = {x/Ram, y/Asha}** replaces variables with terms.
`SUBST(θ, Parent(x, y))` = `Parent(Ram, Asha)`.

> **UNIFY(p, q) returns a substitution θ such that SUBST(θ, p) = SUBST(θ, q),
> or failure.**

| p | q | UNIFY |
|---|---|---|
| `Knows(Ram, x)` | `Knows(Ram, Asha)` | **{x/Asha}** |
| `Knows(Ram, x)` | `Knows(y, Ravi)` | **{y/Ram, x/Ravi}** |
| `Knows(Ram, x)` | `Knows(y, MotherOf(y))` | **{y/Ram, x/MotherOf(Ram)}** |
| `Knows(Ram, x)` | `Knows(x, Ravi)` | **FAILURE** — x cannot be both |

**The last row is why standardising apart matters:** rename the variables in
one sentence and it unifies. Every implementation does this automatically.

**The occurs check:** unifying `x` with `f(x)` must fail, or you build an
infinite term. Prolog omits it by default **for speed**, which is a known
unsoundness — and a good viva answer.

**The most general unifier (MGU)** is the substitution that commits to as
little as possible. `UNIFY(Knows(Ram,x), Knows(y,z))` gives `{y/Ram, x/z}`, not
`{y/Ram, x/Ravi, z/Ravi}`.

---

## 4.5 Forward and backward chaining

Both apply to **definite clauses** — a disjunction with **exactly one positive
literal**, equivalently `A ∧ B ∧ … ⇒ C`. Most practical rule bases are of this
form, and inference over them is efficient.

### 🔢 Forward chaining — data-driven

**Start from the known facts. Apply every rule whose premises are satisfied.
Add the conclusions. Repeat until nothing new appears or the goal is derived.**

```
facts:  A, B
rules:  A ∧ B ⇒ C
        C     ⇒ D
        D ∧ A ⇒ E

pass 1: A, B satisfy rule 1  →  add C
pass 2: C satisfies rule 2   →  add D
pass 3: D, A satisfy rule 3  →  add E
pass 4: nothing new  →  stop.   Derived: {A, B, C, D, E}
```

### 🔢 Backward chaining — goal-driven

**Start from the goal. Find a rule concluding it. Prove that rule's premises
as sub-goals, recursively.**

```
goal: E
  E ⟸ D ∧ A
    D ⟸ C
      C ⟸ A ∧ B
        A ✓ (a fact)
        B ✓ (a fact)
      C proved
    D proved
    A ✓
  E PROVED
```

### 🔢 The comparison — a guaranteed question

| | **Forward chaining** | **Backward chaining** |
|---|---|---|
| Driven by | **Data** | **The goal** |
| Starts from | Known facts | The query |
| Derives | **Everything derivable** | **Only what is needed** |
| Suits | Monitoring; many possible conclusions | Diagnosis; one specific question |
| Work | Can derive masses of irrelevant facts | Focused |
| Used by | Production systems, **CLIPS**, Rete | **Prolog** |
| Search | Breadth-first-ish | **Depth-first** — so it can loop |

**Prolog is backward chaining with depth-first search**, which is exactly why a
left-recursive rule loops for ever — and why rule order matters in Prolog but
not in logic.

### 💡 Which to use — the deciding question

**How many possible conclusions are there, and how many facts?**

- **Few facts, many possible conclusions** → **forward.** A sensor reading
  arrives; work out everything it implies.
- **Many facts, one question** → **backward.** "Does this patient have
  malaria?" — do not derive every other disease first.

---

## 4.6 Resolution

### 🎯 The idea

**Resolution is proof by contradiction, mechanised.** To prove KB ⊨ α, show
that **KB ∧ ¬α is unsatisfiable** — derive the **empty clause**.

It is **sound and refutation-complete**, and it needs **only one inference
rule**, which is why it is the basis of automated theorem proving and of
Prolog.

### 🔢 Conversion to CNF — the procedure to memorise

Resolution requires **conjunctive normal form**: a conjunction of clauses, each
a disjunction of literals.

| # | Step | Example |
|---|---|---|
| 1 | **Eliminate ⇔** | (α ⇒ β) ∧ (β ⇒ α) |
| 2 | **Eliminate ⇒** — `α ⇒ β` becomes **¬α ∨ β** | The key step |
| 3 | **Move ¬ inwards** — De Morgan, including for quantifiers | ¬∀x P ⇒ ∃x ¬P |
| 4 | **Standardise apart** — rename variables so none is shared | ∀x P(x) ∧ ∀x Q(x) → ∀x P(x) ∧ ∀y Q(y) |
| 5 | **Skolemise** — replace ∃ | See below |
| 6 | **Drop ∀** — all remaining variables are universally quantified | |
| 7 | **Distribute ∨ over ∧** | (A ∧ B) ∨ C → (A ∨ C) ∧ (B ∨ C) |

### ⚠️ Skolemisation, and the rule people get wrong

- **∃ not inside any ∀** → replace with a new **constant**.
  `∃x Rich(x)` → `Rich(S1)`
- **∃ inside ∀** → replace with a **function of the enclosing universals**.
  `∀x ∃y Loves(x, y)` → `Loves(x, F(x))`

**The function is essential.** Using a constant would assert that everyone
loves *the same* person, which is a different and stronger claim — precisely
the ∀∃ / ∃∀ distinction from §4.4.

### 🔢 A worked resolution proof

**Knowledge base:**

1. All men are mortal: `∀x Man(x) ⇒ Mortal(x)`
2. Socrates is a man: `Man(Socrates)`

**Goal:** `Mortal(Socrates)`

**Step 1 — convert to CNF.**

| From | CNF clause |
|---|---|
| ∀x Man(x) ⇒ Mortal(x) | **¬Man(x) ∨ Mortal(x)** |
| Man(Socrates) | **Man(Socrates)** |

**Step 2 — negate the goal and add it.**

| | |
|---|---|
| ¬Mortal(Socrates) | **¬Mortal(Socrates)** |

**Step 3 — resolve.**

```
   ¬Man(x) ∨ Mortal(x)        ¬Mortal(Socrates)
              └──────── unify Mortal(x) with Mortal(Socrates), θ = {x/Socrates}
                     ▼
              ¬Man(Socrates)                 Man(Socrates)
                          └──────── resolve ────────┘
                                    ▼
                                   [ ]        ← the EMPTY CLAUSE
```

**The empty clause means a contradiction**, so KB ∧ ¬Goal is unsatisfiable,
so **KB ⊨ Mortal(Socrates)**. ∎

### 💡 Reading the empty clause correctly

`[ ]` is a disjunction of **no** literals, and a disjunction is true only if
some disjunct is true. With none, it is **false in every model** — a
contradiction. Since the only new assumption was ¬Goal, the goal must follow.

### ⚠️ Resolution's limits, worth stating

- **Refutation complete, not complete** — it proves entailment by
  contradiction, and cannot generate all consequences directly.
- **Semi-decidable in FOL.** If KB ⊨ α it will find a proof; **if not, it may
  run for ever.** No algorithm can do better — that is Church and Turing's
  result, not a defect of resolution.
- **The search space is large.** Strategies (unit preference, set of support,
  input resolution, subsumption) exist to control it.

---

## Practice problems

### Problem 1

Convert to CNF and prove `Mortal(Socrates)` by resolution. *(10 marks)*

**Solution.** Set out the CNF procedure as seven steps — eliminate ⇔, eliminate
⇒ (`α ⇒ β` → `¬α ∨ β`), move ¬ inwards, standardise apart, Skolemise, drop ∀,
distribute ∨ over ∧.

**Apply it:**

| Sentence | CNF |
|---|---|
| ∀x Man(x) ⇒ Mortal(x) | ¬Man(x) ∨ Mortal(x) |
| Man(Socrates) | Man(Socrates) |
| **¬Goal:** ¬Mortal(Socrates) | ¬Mortal(Socrates) |

**Resolve**, showing the unifier at each step:

1. Resolve `¬Man(x) ∨ Mortal(x)` with `¬Mortal(Socrates)` using
   **θ = {x/Socrates}** → `¬Man(Socrates)`
2. Resolve `¬Man(Socrates)` with `Man(Socrates)` → **[ ]**

**The empty clause is a contradiction**, so KB ∧ ¬Goal is unsatisfiable and
**KB ⊨ Mortal(Socrates)**.

**Explain why [ ] means contradiction:** it is a disjunction of no literals, and
a disjunction needs at least one true disjunct, so it is false in every model.

Add that resolution is **sound and refutation-complete**, and that in FOL it is
**semi-decidable** — guaranteed to find a proof if one exists, but possibly
non-terminating if none does.

### Problem 2

Distinguish forward from backward chaining, with a worked example. *(10 marks)*

**Solution.** Give the comparison table — data-driven vs goal-driven, what each
derives, what each suits, and that **Prolog uses backward chaining with
depth-first search**.

**The worked example.** Facts A, B; rules `A ∧ B ⇒ C`, `C ⇒ D`, `D ∧ A ⇒ E`;
goal E.

**Forward:** pass 1 adds C; pass 2 adds D; pass 3 adds E; pass 4 adds nothing
and stops. Derived {A, B, C, D, E} — **including anything else derivable,
whether or not it was wanted**.

**Backward:** goal E ⟸ D ∧ A; D ⟸ C; C ⟸ A ∧ B; A and B are facts, so C is
proved, so D, so E. **Only the facts needed were touched.**

**The deciding question:** how many possible conclusions, and how many facts?
Few facts and many conclusions → **forward** (a sensor reading arrives; derive
what it implies). Many facts and one question → **backward** ("does this patient
have malaria?" — do not derive every other disease first).

Close with the practical consequence: **because backward chaining is depth-first,
Prolog loops for ever on a left-recursive rule**, which is why clause order
matters in Prolog and does not matter in logic.

### Problem 3

Represent these in FOL and explain the quantifier rules. *(10 marks)*

> (a) All students study. (b) Some students study. (c) No student fails.
> (d) Everybody loves someone. (e) There is someone everybody loves.

**Solution.**

| | FOL |
|---|---|
| (a) | **∀x Student(x) ⇒ Studies(x)** |
| (b) | **∃x Student(x) ∧ Studies(x)** |
| (c) | **∀x Student(x) ⇒ ¬Fails(x)**, equivalently ¬∃x Student(x) ∧ Fails(x) |
| (d) | **∀x ∃y Loves(x, y)** |
| (e) | **∃y ∀x Loves(x, y)** |

**The pairing rule — state it explicitly, because it is the marks:**

> **∀ goes with ⇒. ∃ goes with ∧.**

Explain why with the counter-examples: `∀x Student(x) ∧ Studies(x)` claims
**everything in the universe** is a student who studies, which is wrong; and
`∃x Student(x) ⇒ Studies(x)` is **vacuously true** the moment anything is not
a student, so it asserts nothing.

**Then the nesting point, from (d) and (e):** `∀x ∃y` lets y depend on x —
everybody loves *someone*, possibly different people. `∃y ∀x` fixes one y for
all x — there is **one person** everybody loves. **Order changes the meaning.**

Add the connection to Skolemisation: (d) becomes `Loves(x, F(x))` — a
**function** of x, because y depends on x — while (e) becomes `Loves(x, S1)`
with a **constant**, because it does not.

---

## Exam questions from this unit

**Two marks**

1. What are TELL and ASK?
2. When is P ⇒ Q false?
3. Give the equivalence for P ⇒ Q in terms of ∨.
4. Define entailment.
5. What is the difference between a predicate and a function in FOL?
6. What does UNIFY return?
7. What does the empty clause mean in resolution?

**Five marks**

1. Explain the issues in knowledge representation.
2. Explain the inference rules of propositional logic.
3. Explain unification with examples, and the occurs check.
4. Explain Skolemisation, including the ∃-inside-∀ case.
5. Compare propositional logic with first order logic.
6. Explain soundness and completeness.

**Ten marks**

1. Convert to CNF and prove a goal by resolution.
2. Distinguish forward from backward chaining with a worked example.
3. Represent English sentences in FOL and explain the quantifier rules.
4. Explain knowledge-based agents and the approaches to representation.

---

## Mistakes that cost marks

- **Writing `∀x P(x) ∧ Q(x)`.** ∀ goes with ⇒.
- **Writing `∃x P(x) ⇒ Q(x)`.** ∃ goes with ∧, or it is vacuously true.
- **Swapping ∀∃ and ∃∀.** Different claims entirely.
- **Skolemising an ∃ inside a ∀ to a constant.** It must be a **function** of
  the enclosing universal variables.
- **Saying P ⇒ Q means P causes Q.** It is ¬P ∨ Q, and it is true whenever P is
  false.
- **Forgetting to negate the goal.** Resolution proves by contradiction;
  without ¬Goal there is nothing to contradict.
- **Confusing a predicate with a function.** `FatherOf(x)` is a person;
  `Father(x, y)` is true or false.
- **Calling resolution complete without qualification.** It is **refutation**
  complete, and FOL is only semi-decidable.
- **Saying forward chaining is always more efficient.** It derives everything,
  most of which may be irrelevant.
